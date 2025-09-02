from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from sqlalchemy import or_
from server.db import get_session
from server.models import WeeklyReport
from server.schemas import QARequest, QAResponse, QACitation
from server.deps import get_current_user, resolve_tenant_id, rate_limit
from server.config import settings
from server.ai_services import qa_with_rag
import asyncio
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["qa"])


@router.post("/qa")
async def qa(body: QARequest, session: Session = Depends(get_session), user=Depends(get_current_user), tenant_id: str | None = Depends(resolve_tenant_id), _rl=Depends(rate_limit(settings.RATE_LIMIT_QA_PER_MIN))) -> QAResponse:
    """
    Advanced Q&A using RAG (Retrieval Augmented Generation) with fallback to basic search
    """
    try:
        # Try advanced RAG Q&A first
        if settings.ENABLE_AI_PROCESSING and settings.OPENAI_API_KEY:
            logger.info(f"Processing Q&A with RAG: {body.query}")
            
            rag_result = await qa_with_rag(
                query=body.query,
                product_line_id=body.productLineId,
                tenant_id=tenant_id
            )
            
            if "error" not in rag_result:
                return QAResponse(
                    answer=rag_result["answer"],
                    citations=[
                        QACitation(
                            reportId=citation["reportId"],
                            section=citation["section"],
                            weekId=citation["weekId"]
                        ) for citation in rag_result["citations"]
                    ]
                )
            else:
                logger.warning(f"RAG Q&A failed: {rag_result['error']}")
        
    except Exception as e:
        logger.error(f"Error in RAG Q&A: {e}")
    
    # Fallback to basic keyword search
    logger.info("Using fallback keyword search for Q&A")
    
    q = session.query(WeeklyReport)
    if tenant_id:
        q = q.filter(WeeklyReport.tenant_id == tenant_id)
    if body.productLineId:
        q = q.filter(WeeklyReport.product_line_id == body.productLineId)
    
    # Enhanced keyword search
    search_terms = body.query.lower().split()
    conditions = []
    
    for term in search_terms:
        if body.includeCI:
            conditions.append(
                or_(
                    WeeklyReport.executive_summary.ilike(f"%{term}%"),
                    WeeklyReport.ci_summary.ilike(f"%{term}%"),
                )
            )
        else:
            conditions.append(WeeklyReport.executive_summary.ilike(f"%{term}%"))
    
    if conditions:
        q = q.filter(or_(*conditions))
    
    top = q.order_by(WeeklyReport.created_at.desc()).limit(5).all()
    
    if not top:
        return QAResponse(
            answer="Non ho trovato informazioni rilevanti per la tua domanda. Prova a riformulare o usa termini più generali.",
            citations=[]
        )
    
    # Build enhanced answer from multiple reports
    answer_parts = []
    citations = []
    
    for i, report in enumerate(top[:3]):  # Use top 3 results
        citations.append(QACitation(
            reportId=report.id,
            section="summary",
            weekId=report.week_id
        ))
        
        # Extract relevant excerpts
        summary_lines = report.executive_summary.split('\n')
        relevant_lines = []
        
        for line in summary_lines:
            if any(term in line.lower() for term in search_terms):
                relevant_lines.append(line.strip())
        
        if relevant_lines:
            answer_parts.append(f"**Settimana {report.week_id}**: {' '.join(relevant_lines[:2])}")
    
    if answer_parts:
        answer = "Ecco cosa ho trovato:\n\n" + "\n\n".join(answer_parts)
    else:
        answer = f"Ho trovato {len(top)} report correlati ma potrebbero non essere direttamente rilevanti alla tua domanda specifica."
    
    return QAResponse(answer=answer, citations=citations)

