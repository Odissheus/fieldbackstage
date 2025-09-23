from fastapi import APIRouter, Header, HTTPException, Depends
from jose import jwt
import httpx
from functools import lru_cache
from config import settings
from db import get_session
from sqlalchemy.orm import Session
from models import User, LoginAccount, Tenant
from datetime import datetime, timedelta
from jose import jwt as jose_jwt
from fastapi import Body
from hashlib import sha256
from email import send_mail
from deps import rate_limit
from config import settings


router = APIRouter(tags=["auth"])


@lru_cache(maxsize=1)
def _fetch_jwks():
    if not settings.JWT_JWKS_URL:
        return {"keys": []}
    resp = httpx.get(settings.JWT_JWKS_URL, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _get_key(kid: str):
    jwks = _fetch_jwks()
    for k in jwks.get("keys", []):
        if k.get("kid") == kid:
            return k
    return None


@router.get("/auth/me")
def me(authorization: str | None = Header(default=None), session: Session = Depends(get_session)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split()[1]
    headers = jwt.get_unverified_header(token)
    key = _get_key(headers.get("kid", ""))
    if not key:
        raise HTTPException(status_code=401, detail="Unknown key id")
    try:
        payload = jwt.decode(token, key, algorithms=[key.get("alg", "RS256")], audience=settings.JWT_AUDIENCE)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    sub = payload.get("sub")
    # ensure local user record exists
    if sub:
        u = session.get(User, sub)
        if not u:
            u = User(id=sub, email=payload.get("email"), full_name=payload.get("name"))
            session.add(u)
            session.commit()
    return {"userId": sub, "role": payload.get("role", "viewer")}


def _hash_password(pwd: str) -> str:
    return sha256(pwd.encode("utf-8")).hexdigest()


def _issue_jwt(sub: str, role: str, tenant_id: str | None = None) -> str:
    now = datetime.utcnow()
    payload = {
        "iss": settings.JWT_ISSUER,
        "sub": sub,
        "role": role,
        "tenantId": tenant_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=settings.JWT_TTL_SECONDS)).timestamp()),
    }
    return jose_jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


@router.post("/auth/landlord/login")
def landlord_login(body: dict = Body(...), session: Session = Depends(get_session), _rl=Depends(rate_limit(settings.RATE_LIMIT_AUTH_PER_MIN))):
    username = (body or {}).get("username")
    password = (body or {}).get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    # Built-in superadmin from env
    if username == settings.SUPERADMIN_USERNAME and password == settings.SUPERADMIN_PASSWORD:
        token = _issue_jwt(settings.SUPERADMIN_USER_ID, role="super_admin")
        return {"accessToken": token}
    # Or lookup in login_account (tenant_id null)
    acc = session.query(LoginAccount).filter(LoginAccount.username == username, LoginAccount.tenant_id.is_(None)).first()
    if not acc or acc.password_hash != _hash_password(password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = _issue_jwt(acc.user_id or acc.id, role=acc.role)
    return {"accessToken": token}


@router.post("/auth/landing/login")
def landing_login(body: dict = Body(...), session: Session = Depends(get_session), _rl=Depends(rate_limit(settings.RATE_LIMIT_AUTH_PER_MIN))):
    company_code = (body or {}).get("companyCode")
    username = (body or {}).get("username")
    password = (body or {}).get("password")
    if not company_code or not username or not password:
        raise HTTPException(status_code=400, detail="companyCode, username, password required")
    tenant = session.query(Tenant).filter(Tenant.company_code == company_code).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="company not found")
    acc = session.query(LoginAccount).filter(LoginAccount.username == username, LoginAccount.tenant_id == tenant.id).first()
    if not acc or acc.password_hash != _hash_password(password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = _issue_jwt(acc.user_id or acc.id, role=acc.role, tenant_id=tenant.id)
    return {"accessToken": token}


@router.post("/auth/landing/reset-password")
def landing_reset_password(body: dict = Body(...), session: Session = Depends(get_session)):
    company_code = (body or {}).get("companyCode")
    username = (body or {}).get("username")
    email = (body or {}).get("email")
    if not company_code or not username or not email:
        raise HTTPException(status_code=400, detail="companyCode, username, email required")
    tenant = session.query(Tenant).filter(Tenant.company_code == company_code).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="company not found")
    acc = session.query(LoginAccount).filter(LoginAccount.username == username, LoginAccount.tenant_id == tenant.id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="user not found")
    # Generate temp password and email it
    temp = "Temp-" + username[:3] + "-" + company_code[:3]
    acc.password_hash = _hash_password(temp)
    session.add(acc)
    session.commit()
    send_mail(email, "Reset password Fieldback", f"Password temporanea: {temp}")
    return {"status": "sent"}


@router.post("/auth/landing/change-password")
def landing_change_password(body: dict = Body(...), session: Session = Depends(get_session)):
    company_code = (body or {}).get("companyCode")
    username = (body or {}).get("username")
    old_password = (body or {}).get("oldPassword")
    new_password = (body or {}).get("newPassword")
    if not company_code or not username or not old_password or not new_password:
        raise HTTPException(status_code=400, detail="companyCode, username, oldPassword, newPassword required")
    tenant = session.query(Tenant).filter(Tenant.company_code == company_code).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="company not found")
    acc = session.query(LoginAccount).filter(LoginAccount.username == username, LoginAccount.tenant_id == tenant.id).first()
    if not acc or acc.password_hash != _hash_password(old_password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    acc.password_hash = _hash_password(new_password)
    session.add(acc)
    session.commit()
    return {"status": "ok"}

