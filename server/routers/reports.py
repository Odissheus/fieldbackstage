from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from server.db import get_session
from server.models import WeeklyReport
from server.schemas import ReportItem
from server.deps import get_current_user, resolve_tenant_id


router = APIRouter(tags=["reports"])


@router.get("/reports")
def list_reports(
    productLineId: str | None = None,
    frm: str | None = None,
    to: str | None = None,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
    tenant_id: str | None = Depends(resolve_tenant_id),
):
    q = session.query(WeeklyReport)
    # scope per tenant se header presente (o se l'utente non è super_admin)
    if tenant_id:
        q = q.filter(WeeklyReport.tenant_id == tenant_id)
    if productLineId:
        q = q.filter(WeeklyReport.product_line_id == productLineId)
    items = q.order_by(WeeklyReport.created_at.desc()).all()
    result = []
    for r in items:
        result.append(
            ReportItem(
                id=r.id,
                tenantId=r.tenant_id,
                productLineId=r.product_line_id,
                weekId=r.week_id,
                executiveSummary=r.executive_summary,
                ciSummary=r.ci_summary,
                heatmap=r.heatmap or {},
                contributors=r.contributors or [],
                urlPdf=r.url_pdf,
                urlHtml=r.url_html,
            ).model_dump()
        )
    return result


@router.get("/reports/{report_id}")
def get_report(
    report_id: str,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
    tenant_id: str | None = Depends(resolve_tenant_id),
):
    r = session.get(WeeklyReport, report_id)
    if not r:
        return {}
    if tenant_id and r.tenant_id != tenant_id:
        # nascondi report di altri tenant
        return {}
    return ReportItem(
        id=r.id,
        tenantId=r.tenant_id,
        productLineId=r.product_line_id,
        weekId=r.week_id,
        executiveSummary=r.executive_summary,
        ciSummary=r.ci_summary,
        heatmap=r.heatmap or {},
        contributors=r.contributors or [],
        urlPdf=r.url_pdf,
        urlHtml=r.url_html,
    ).model_dump()
    if not r:
        return {}
    return ReportItem(
        id=r.id,
        tenantId=r.tenant_id,
        productLineId=r.product_line_id,
        weekId=r.week_id,
        executiveSummary=r.executive_summary,
        ciSummary=r.ci_summary,
        heatmap=r.heatmap or {},
        contributors=r.contributors or [],
        urlPdf=r.url_pdf,
        urlHtml=r.url_html,
    ).model_dump()

