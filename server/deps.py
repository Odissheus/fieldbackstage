from fastapi import Header, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from jose import jwt
from .db import get_session
from .models import UserTenantRole
from .config import settings
import time
from fastapi import Request


def _decode_bearer(authorization: Optional[str]) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split()[1]
    # Try HS256 first (local accounts)
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        return payload
    except Exception:
        pass
    # Fallback to JWKS if configured
    from server.routers.auth import _get_key  # local import to avoid cycle
    try:
        headers = jwt.get_unverified_header(token)
        key = _get_key(headers.get("kid", ""))
        if not key:
            raise Exception("Unknown key id")
        payload = jwt.decode(token, key, algorithms=[key.get("alg", "RS256")], audience=settings.JWT_AUDIENCE)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def get_current_user(authorization: Optional[str] = Header(default=None)):
    payload = _decode_bearer(authorization)
    return {
        "userId": payload.get("sub"),
        "role": payload.get("role", "viewer"),
        "tenantId": payload.get("tenantId"),
    }


def require_role(*allowed_roles: str):
    def dependency(user=Depends(get_current_user)):
        role = user.get("role")
        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return dependency


def resolve_tenant_id(user=Depends(get_current_user), tenant_id_header: Optional[str] = Header(default=None, alias="X-Tenant-Id")) -> Optional[str]:
    # Prefer tenant from token; allow super_admin to override via header
    if user.get("role") == "super_admin" and tenant_id_header:
        return tenant_id_header
    return user.get("tenantId")


def get_user_roles(user=Depends(get_current_user), session: Session = Depends(get_session)):
    # Query roles for user across tenants
    items = session.query(UserTenantRole).filter(UserTenantRole.user_id == user["userId"]).all()
    roles = [
        {
            "tenantId": it.tenant_id,
            "role": it.role,
            "productLineIds": it.product_line_ids or [],
        }
        for it in items
    ]
    return roles


_RATE_BUCKETS: dict[str, list[float]] = {}


def rate_limit(limit_per_minute: int):
    def dependency(request: Request):
        key = request.client.host + '|' + request.url.path
        now = time.time()
        window_start = now - 60
        bucket = _RATE_BUCKETS.setdefault(key, [])
        # drop old
        while bucket and bucket[0] < window_start:
            bucket.pop(0)
        if len(bucket) >= limit_per_minute:
            raise HTTPException(status_code=429, detail="Too Many Requests")
        bucket.append(now)
    return dependency


