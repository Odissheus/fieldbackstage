from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class InsightCreate(BaseModel):
    productLineId: str
    territoryId: Optional[str] = None
    type: str = Field(pattern="^(INSIGHT|CI)$")
    text: Optional[str] = None
    audioUrl: Optional[str] = None
    photoUrl: Optional[str] = None
    ocrText: Optional[str] = None


class UploadPresignResponse(BaseModel):
    url: str
    fields: Dict[str, Any]


class ReportItem(BaseModel):
    id: str
    tenantId: Optional[str] = None
    productLineId: str
    weekId: str
    executiveSummary: str
    ciSummary: Optional[str] = None
    heatmap: Dict[str, Any]
    contributors: List[str]
    urlPdf: Optional[str] = None
    urlHtml: Optional[str] = None


class QARequest(BaseModel):
    query: str
    productLineId: Optional[str] = None
    territoryId: Optional[str] = None
    dateRange: Optional[Dict[str, str]] = None
    includeCI: bool = False


class QACitation(BaseModel):
    reportId: str
    section: str
    weekId: str


class QAResponse(BaseModel):
    answer: str
    citations: List[QACitation]


