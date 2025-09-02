from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.db import get_session
from server.models import WeeklyReport
from server.deps import resolve_tenant_id, get_current_user

router = APIRouter(tags=["analytics"])


@router.get('/analytics/weekly')
def analytics_weekly(productLineId: str | None = None, session: Session = Depends(get_session), user=Depends(get_current_user), tenant_id: str | None = Depends(resolve_tenant_id)):
    if not tenant_id:
        return {"kpi": {"reports": 0, "contributors": 0}, "trend": []}
    q = session.query(WeeklyReport).filter(WeeklyReport.tenant_id == tenant_id)
    if productLineId:
        q = q.filter(WeeklyReport.product_line_id == productLineId)
    items = q.order_by(WeeklyReport.created_at.desc()).limit(8).all()
    trend = [ {"weekId": r.week_id, "count": 1} for r in items ]
    contributors = sum(len(r.contributors or []) for r in items)
    return {"kpi": {"reports": len(items), "contributors": contributors}, "trend": trend}


@router.get('/analytics/heatmap')
def analytics_heatmap(productLineId: str | None = None, session: Session = Depends(get_session), user=Depends(get_current_user), tenant_id: str | None = Depends(resolve_tenant_id)):
    if not tenant_id:
        return {"bins": []}
    q = session.query(WeeklyReport).filter(WeeklyReport.tenant_id == tenant_id)
    if productLineId:
        q = q.filter(WeeklyReport.product_line_id == productLineId)
    items = q.order_by(WeeklyReport.created_at.desc()).limit(1).all()
    if not items:
        return {"bins": []}
    hm = items[0].heatmap or {"bins": []}
    return hm

