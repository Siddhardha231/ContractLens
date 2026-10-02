"""Extraction schemas for LLM structured output parsing."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class RawParty(BaseModel):
    role: str = "Party"
    name: str = "Unknown"
    type: Optional[str] = None
    reg: Optional[str] = None

class RawClause(BaseModel):
    section: str = "1.0"
    title: str = "Clause"
    page: int = 1
    type: str = "general"
    summary: str = ""
    text: Optional[str] = None

class RawFinancialTerm(BaseModel):
    label: str
    amount: float
    currency: str = "INR"
    frequency: str = "one_time"
    trigger: str = ""
    evidence: str
    type: str = "recurring_commitment"

class RawDeadline(BaseModel):
    date: str = "Due Date"
    relative_label: str = "Day 0"
    event: str = "Milestone"
    action: str = ""
    consequence: str = ""
    category: str = "payment"
    attention_tier: str = "medium"

class RawObligation(BaseModel):
    actor: str = "Tenant"
    action: str = ""
    condition: Optional[str] = None

class RawFinding(BaseModel):
    category: str = "General"
    title: str = ""
    severity_tier: str = "medium"
    explanation: str = ""
    matters: str = ""
    bullets: List[str] = []
    evidence: str = ""
    ambiguity_detected: bool = False
    ambiguity_note: Optional[str] = None

class RawExtractionResult(BaseModel):
    title: str = "Contract Document"
    parties: List[RawParty] = []
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    tenure_months: Optional[int] = None
    clauses: List[RawClause] = []
    financial_terms: List[RawFinancialTerm] = []
    deadlines: List[RawDeadline] = []
    obligations: List[RawObligation] = []
    findings: List[RawFinding] = []

class EvaluationRequest(BaseModel):
    contract_text: str
    contract_title: Optional[str] = "Uploaded Contract"
    model: str = "gemini-3.8-flash"
    provider: str = "gemini"
    custom_endpoint: Optional[str] = None
    temperature: float = 0.1

class AskRequest(BaseModel):
    question: str
    contract_text: str
    model: str = "gemini-3.8-flash"
    provider: str = "gemini"
