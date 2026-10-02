"""Pydantic schemas for Contract IR and API view payloads (PDD §7.4, §10, §11, §12)."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SourceLeaf(BaseModel):
    id: str
    page: int
    section_label: str
    bbox: List[float] = [0.0, 0.0, 500.0, 100.0]
    text: str

class ClauseSchema(BaseModel):
    id: str
    section: str
    title: str
    page: int
    bbox: List[float] = [0.0, 0.0, 500.0, 100.0]
    type: str = "general"
    summary: str
    text: Optional[str] = None

class FinancialTermSchema(BaseModel):
    id: str
    source_id: str
    label: str
    amount: float
    currency: str = "INR"
    frequency: str = "one_time"  # monthly, one_time, annual, other
    trigger: str
    evidence: str
    confidence: float = 1.0
    type: str = "recurring_commitment"  # recurring_commitment, upfront_capital, latent_liability, contingent_penalty

class DeadlineSchema(BaseModel):
    id: str
    source_id: str
    date: str
    relative_label: str
    event: str
    consequence: str
    action: str
    category: str = "payment"  # payment, notice, critical
    attention_tier: str = "medium"  # high, medium, low
    confidence: float = 1.0

class ObligationSchema(BaseModel):
    id: str
    source_id: str
    actor: str
    action: str
    condition: Optional[str] = None
    confidence: float = 1.0

class FindingSchema(BaseModel):
    id: str
    source_id: str
    category: str
    title: str
    severity_tier: str  # high, medium, low
    explanation: str
    matters: str
    bullets: List[str] = []
    evidence: str
    ambiguity_detected: bool = False
    ambiguity_note: Optional[str] = None
    confidence: float = 1.0
    validation_status: str = "PASSED"

class PartySchema(BaseModel):
    role: str
    name: str
    type: Optional[str] = None
    reg: Optional[str] = None

class ContractMetadataSchema(BaseModel):
    id: str
    filename: str
    title: str
    parties: List[PartySchema] = []
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    tenure_months: Optional[int] = None
    page_count: int = 1
    char_count: int = 0
    sha256: str
    status: str = "COMPLETED"
    engine_version: str = "v2.5-CONTRACTLENS"
    pydantic_validation: str = "Pass (Strict v2.8)"
    traceability_rate: float = 100.0

class ContractIR(BaseModel):
    metadata: ContractMetadataSchema
    sources: Dict[str, SourceLeaf]
    financial_terms: List[FinancialTermSchema]
    deadlines: List[DeadlineSchema]
    obligations: List[ObligationSchema] = []
    findings: List[FindingSchema]
    clauses: List[ClauseSchema]

# REST API Response Models (PDD §11)
class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    stage: str
    page_count: int
    char_count: int
    sha256: str
    message: str

class DocumentStatusResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    stage: str
    progress: int
    error_message: Optional[str] = None

class OverviewResponse(BaseModel):
    metadata: ContractMetadataSchema
    vitals: Dict[str, Any]
    summary_counts: Dict[str, int]

class FindingsResponse(BaseModel):
    document_id: str
    findings: List[FindingSchema]
    tier_counts: Dict[str, int]
    ambiguity_count: int

class MoneyResponse(BaseModel):
    document_id: str
    financial_terms: List[FinancialTermSchema]
    monthly_recurring_total: float
    upfront_total: float
    currency: str = "INR"

class TimelineResponse(BaseModel):
    document_id: str
    deadlines: List[DeadlineSchema]
    upcoming_events: List[Dict[str, Any]]

class ClausesResponse(BaseModel):
    document_id: str
    clauses: List[ClauseSchema]

class ExportResponse(BaseModel):
    document_id: str
    filename: str
    markdown_report: str
    contract_ir: Dict[str, Any]
