from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.db import get_session
from server.models import Tenant, User, UserTenantRole, LoginAccount, InsightRaw
from server.deps import require_role
from hashlib import sha256
from datetime import datetime
from server.jobs.weekly_report_job import run_weekly
import hashlib


router = APIRouter(tags=["admin"])


@router.get("/admin/tenants")
def list_tenants(session: Session = Depends(get_session), user=Depends(require_role("super_admin"))):
    """List all tenants"""
    tenants = session.query(Tenant).all()
    return [{"id": str(t.id), "name": t.name, "companyCode": t.company_code} for t in tenants]


@router.post("/admin/tenants", status_code=201)
def create_tenant(body: dict, session: Session = Depends(get_session), user=Depends(require_role("super_admin"))):
    name = (body or {}).get("name")
    company_code = (body or {}).get("companyCode")
    if not name:
        raise HTTPException(status_code=400, detail="name required")
    t = Tenant(name=name, company_code=company_code)
    session.add(t)
    session.commit()
    return {"id": t.id, "name": t.name, "companyCode": t.company_code}


@router.post("/admin/users", status_code=201)
def create_user(body: dict, session: Session = Depends(get_session), user=Depends(require_role("super_admin", "admin"))):
    # Integrazione con IdP esterno non gestita qui: si registra solo nel DB interno
    uid = (body or {}).get("id")  # opzionale: forzare un id uguale al sub IdP
    email = (body or {}).get("email")
    full_name = (body or {}).get("fullName")
    if not uid:
        # se non fornito, non possiamo creare credenziali IdP qui; creiamo solo il record
        from server.models import uuid_str
        uid = uuid_str()
    u = User(id=uid, email=email, full_name=full_name)
    session.add(u)
    session.commit()
    return {"id": u.id}


@router.post("/admin/users/{user_id}/roles", status_code=201)
def assign_role(user_id: str, body: dict, session: Session = Depends(get_session), user=Depends(require_role("super_admin", "admin"))):
    tenant_id = (body or {}).get("tenantId")
    role = (body or {}).get("role")
    product_line_ids = (body or {}).get("productLineIds")
    username = (body or {}).get("username")
    password = (body or {}).get("password")
    if not tenant_id or not role:
        raise HTTPException(status_code=400, detail="tenantId and role required")
    r = UserTenantRole(user_id=user_id, tenant_id=tenant_id, role=role, product_line_ids=product_line_ids)
    session.add(r)
    if username and password:
        pwd_hash = sha256(password.encode("utf-8")).hexdigest()
        acc = session.query(LoginAccount).filter(LoginAccount.username == username, LoginAccount.tenant_id == tenant_id).first()
        if acc:
            acc.password_hash = pwd_hash
            acc.user_id = user_id
            acc.role = role
            session.add(acc)
        else:
            session.add(LoginAccount(username=username, password_hash=pwd_hash, tenant_id=tenant_id, user_id=user_id, role=role))
    session.commit()
    return {"id": r.id}


@router.post("/admin/jobs/generate-weekly-reports")
def generate_weekly_reports(body: dict, session: Session = Depends(get_session), user=Depends(require_role("super_admin", "admin"))):
    tenant_id = (body or {}).get("tenantId")
    product_line_id = (body or {}).get("productLineId")
    week_id = (body or {}).get("weekId")  # es. 2025-W33; se assente usa settimana corrente
    if not tenant_id or not product_line_id:
        raise HTTPException(status_code=400, detail="tenantId and productLineId required")
    if not week_id:
        week_id = datetime.utcnow().strftime("%G-W%V")
    # Esegue il job sincrono (MVP)
    run_weekly(product_line_id=product_line_id, week_id=week_id, tenant_id=tenant_id)
    # Proof semplice
    proof = hashlib.sha256(f"{tenant_id}:{product_line_id}:{week_id}".encode("utf-8")).hexdigest()
    return {"status": "ok", "weekId": week_id, "proof": proof}


@router.post("/admin/jobs/purge-ephemeral")
def purge_ephemeral(body: dict, session: Session = Depends(get_session), user=Depends(require_role("super_admin", "admin"))):
    before = (body or {}).get("before")  # YYYY-MM-DD
    if not before:
        raise HTTPException(status_code=400, detail="before required (YYYY-MM-DD)")
    try:
        cutoff = datetime.strptime(before, "%Y-%m-%d")
    except Exception:
        raise HTTPException(status_code=400, detail="invalid before date")
    # Cancella grezzi (MVP). In futuro aggiungere anche evidenze CI e media S3 via lifecycle policy.
    q = session.query(InsightRaw).filter(InsightRaw.created_at < cutoff)
    count = q.count()
    q.delete(synchronize_session=False)
    session.commit()
    proof = hashlib.sha256(f"purge:{before}:{count}".encode("utf-8")).hexdigest()
    return {"status": "ok", "deleted": count, "proof": proof}

