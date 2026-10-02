"""SQLAlchemy ORM models conforming strictly to PDD §10 and TDA §5."""
import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.db.session import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), default="anonymous", index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=True)
    title = Column(String(255), nullable=True)
    parties_json = Column(Text, nullable=True)  # JSON string
    effective_date = Column(String(64), nullable=True)
    expiration_date = Column(String(64), nullable=True)
    tenure_months = Column(Integer, nullable=True)
    page_count = Column(Integer, default=1)
    char_count = Column(Integer, default=0)
    sha256 = Column(String(64), nullable=False, index=True)
    
    status = Column(String(32), default="UPLOADED", index=True)  # UPLOADED, PARSING, SEGMENTING, EXTRACTING, VALIDATING, COMPLETED, FAILED
    stage = Column(String(64), default="Pending Ingestion")
    progress = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    
    raw_text = Column(Text, nullable=True)
    engine_version = Column(String(64), default="v2.5-CONTRACTLENS")
    traceability_rate = Column(Float, default=100.0)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships with cascade delete
    pages = relationship("Page", back_populates="document", cascade="all, delete-orphan")
    sources = relationship("Source", back_populates="document", cascade="all, delete-orphan")
    clauses = relationship("Clause", back_populates="document", cascade="all, delete-orphan")
    financial_terms = relationship("FinancialTerm", back_populates="document", cascade="all, delete-orphan")
    deadlines = relationship("Deadline", back_populates="document", cascade="all, delete-orphan")
    obligations = relationship("Obligation", back_populates="document", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="document", cascade="all, delete-orphan")


class Page(Base):
    __tablename__ = "pages"

    id = Column(String(96), primary_key=True, index=True)
    document_id = Column(String(64), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    page_number = Column(Integer, nullable=False)
    width = Column(Float, default=612.0)
    height = Column(Float, default=792.0)
    char_count = Column(Integer, default=0)
    is_scanned = Column(Boolean, default=False)

    document = relationship("Document", back_populates="pages")
    sources = relationship("Source", back_populates="page", cascade="all, delete-orphan")
    clauses = relationship("Clause", back_populates="page")


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(96), primary_key=True, index=True)
    document_id = Column(String(64), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    page_id = Column(String(96), ForeignKey("pages.id", ondelete="CASCADE"), nullable=True, index=True)
    page_number = Column(Integer, default=1)
    section_label = Column(String(128), default="General")
    bbox_ymin = Column(Float, default=0.0)
    bbox_xmin = Column(Float, default=0.0)
    bbox_ymax = Column(Float, default=100.0)
    bbox_xmax = Column(Float, default=500.0)
    text = Column(Text, nullable=False)

    document = relationship("Document", back_populates="sources")
    page = relationship("Page", back_populates="sources")
    clauses = relationship("Clause", back_populates="source")
    financial_terms = relationship("FinancialTerm", back_populates="source", cascade="all, delete-orphan")
    deadlines = relationship("Deadline", back_populates="source", cascade="all, delete-orphan")
    obligations = relationship("Obligation", back_populates="source", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="source", cascade="all, delete-orphan")


class Clause(Base):
    __tablename__ = "clauses"

    id = Column(String(96), primary_key=True, index=True)
    document_id = Column(String(64), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    page_id = Column(String(96), ForeignKey("pages.id", ondelete="CASCADE"), nullable=True)
    source_id = Column(String(96), ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    section_label = Column(String(128), nullable=False)
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    clause_type = Column(String(64), default="general")
    summary = Column(Text, nullable=True)
    importance = Column(String(32), default="standard")
    page_number = Column(Integer, default=1)
    bbox_ymin = Column(Float, default=0.0)
    bbox_xmin = Column(Float, default=0.0)
    bbox_ymax = Column(Float, default=100.0)
    bbox_xmax = Column(Float, default=500.0)

    document = relationship("Document", back_populates="clauses")
    page = relationship("Page", back_populates="clauses")
    source = relationship("Source", back_populates="clauses")


class FinancialTerm(Base):
    __tablename__ = "financial_terms"

    id = Column(String(96), primary_key=True, index=True)
    document_id = Column(String(64), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(String(96), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(16), default="INR")
    frequency = Column(String(32), default="one_time")  # monthly, one_time, annual, other
    trigger = Column(Text, nullable=False)
    evidence = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    term_type = Column(String(64), default="recurring_commitment")  # recurring_commitment, upfront_capital, latent_liability, contingent_penalty

    document = relationship("Document", back_populates="financial_terms")
    source = relationship("Source", back_populates="financial_terms")


class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(String(96), primary_key=True, index=True)
    document_id = Column(String(64), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(String(96), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(String(64), nullable=False)
    relative_label = Column(String(128), default="Day 0")
    event = Column(String(255), nullable=False)
    action = Column(Text, nullable=False)
    consequence = Column(Text, nullable=False)
    category = Column(String(64), default="payment")  # payment, notice, critical
    attention_tier = Column(String(32), default="medium")  # high, medium, low
    confidence = Column(Float, default=1.0)

    document = relationship("Document", back_populates="deadlines")
    source = relationship("Source", back_populates="deadlines")


class Obligation(Base):
    __tablename__ = "obligations"

    id = Column(String(96), primary_key=True, index=True)
    document_id = Column(String(64), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(String(96), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    actor = Column(String(128), nullable=False)
    action = Column(Text, nullable=False)
    condition = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0)

    document = relationship("Document", back_populates="obligations")
    source = relationship("Source", back_populates="obligations")


class Finding(Base):
    __tablename__ = "findings"

    id = Column(String(96), primary_key=True, index=True)
    document_id = Column(String(64), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(String(96), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(128), nullable=False)
    title = Column(String(255), nullable=False)
    severity_tier = Column(String(32), nullable=False)  # high, medium, low
    explanation = Column(Text, nullable=False)
    matters = Column(Text, nullable=False)
    bullets_json = Column(Text, default="[]")  # JSON list
    evidence = Column(Text, nullable=False)
    ambiguity_detected = Column(Boolean, default=False)
    ambiguity_note = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0)
    validation_status = Column(String(32), default="PASSED")  # PASSED, FLAGGED, REJECTED

    document = relationship("Document", back_populates="findings")
    source = relationship("Source", back_populates="findings")
    validations = relationship("Validation", back_populates="finding", cascade="all, delete-orphan")


class Validation(Base):
    __tablename__ = "validations"

    id = Column(String(96), primary_key=True, index=True)
    finding_id = Column(String(96), ForeignKey("findings.id", ondelete="CASCADE"), nullable=False, index=True)
    check_type = Column(String(64), nullable=False)  # gate1_schema, gate2_evidence, gate3_amount_date, gate4_ambiguity
    passed = Column(Boolean, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    finding = relationship("Finding", back_populates="validations")
