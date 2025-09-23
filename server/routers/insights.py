from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import InsightCreate
from models import InsightRaw
from db import get_session
from deps import get_current_user
from fastapi import Header, Depends
from deps import resolve_tenant_id
from sqlalchemy import select
from processing_queue import enqueue_insight


router = APIRouter(tags=["insights"])


@router.post("/insights", status_code=201)
def create_insight(
    body: InsightCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
    tenant_id: str | None = Depends(resolve_tenant_id),
):
    item = InsightRaw(
        tenant_id=tenant_id,
        product_line_id=body.productLineId,
        territory_id=body.territoryId,
        type=body.type,
        text=body.text,
        audio_url=body.audioUrl,
        photo_url=body.photoUrl,
        ocr_text=body.ocrText,
    )
    session.add(item)
    session.commit()
    # Enqueue per processing asincrono leggero
    enqueue_insight(item.id)
    return {"id": item.id, "status": "queued"}


@router.get('/insights')
def list_insights(
    productLineId: str | None = None,
    type: str | None = None,
    q: str | None = None,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
    tenant_id: str | None = Depends(resolve_tenant_id),
):
    q = session.query(InsightRaw)
    if tenant_id:
        q = q.filter(InsightRaw.tenant_id == tenant_id)
    if productLineId:
        q = q.filter(InsightRaw.product_line_id == productLineId)
    if type:
        q = q.filter(InsightRaw.type == type)
    if q:
        like = f"%{q}%"
        from sqlalchemy import or_
        q = q.filter(or_(InsightRaw.text.ilike(like), InsightRaw.ocr_text.ilike(like)))
    items = q.order_by(InsightRaw.created_at.desc()).limit(50).all()
    return [
        {
            "id": it.id,
            "productLineId": it.product_line_id,
            "territoryId": it.territory_id,
            "type": it.type,
            "text": it.text,
            "audioUrl": it.audio_url,
            "photoUrl": it.photo_url,
            "createdAt": it.created_at.isoformat() if it.created_at else None,
        }
        for it in items
    ]

