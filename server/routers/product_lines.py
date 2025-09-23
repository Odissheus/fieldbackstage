from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_session
from models import ProductLine
from deps import require_role, resolve_tenant_id, get_current_user


router = APIRouter(tags=["product-lines"])


@router.post("/admin/tenants/{tenant_id}/product-lines", status_code=201)
def create_product_line(tenant_id: str, body: dict, session: Session = Depends(get_session), user=Depends(require_role("super_admin", "admin"))):
    name = (body or {}).get("name")
    if not name:
        raise HTTPException(status_code=400, detail="name required")
    pl = ProductLine(tenant_id=tenant_id, name=name, active="true")
    session.add(pl)
    session.commit()
    return {"id": pl.id, "name": pl.name}


@router.get("/admin/tenants/{tenant_id}/product-lines")
def list_product_lines_admin(tenant_id: str, session: Session = Depends(get_session), user=Depends(require_role("super_admin", "admin"))):
    items = session.query(ProductLine).filter(ProductLine.tenant_id == tenant_id).all()
    return [{"id": it.id, "name": it.name, "active": it.active} for it in items]


@router.get("/product-lines")
def list_product_lines(session: Session = Depends(get_session), user=Depends(get_current_user), tenant_id: str | None = Depends(resolve_tenant_id)):
    if not tenant_id:
        return []
    items = session.query(ProductLine).filter(ProductLine.tenant_id == tenant_id).all()
    return [{"id": it.id, "name": it.name, "active": it.active} for it in items]

