import pytest
from app.extraction.validator import DeterministicValidator

def test_gate1_schema_validation(sample_contract_text):
    """Test Gate 1 validates proper schema structure."""
    raw_valid = {
        "title": "Residential Lease Agreement",
        "parties": ["Rajesh Kumar", "Priya Sharma"],
        "effective_date": "2026-02-01",
        "expiration_date": "2026-12-31",
        "tenure_months": 11,
        "financial_terms": [
            {
                "id": "ft-1",
                "label": "Monthly Rent",
                "amount": 38000,
                "currency": "INR",
                "frequency": "monthly",
                "trigger": "Monthly tenancy",
                "evidence": "The Monthly Rent shall be INR 38,000 payable in advance",
                "confidence": 1.0,
                "type": "recurring_commitment"
            }
        ],
        "findings": [
            {
                "id": "fnd-1",
                "category": "Termination Risk",
                "title": "Lock-in Period Forfeiture",
                "severity_tier": "high",
                "explanation": "Security deposit forfeited if tenant vacates within 6 months.",
                "evidence": "If Tenant vacates during the lock-in period, the entire security deposit shall be forfeited."
            }
        ]
    }
    validated, audit = DeterministicValidator.validate_extraction(raw_valid, sample_contract_text)
    assert len(validated["findings"]) == 1
    assert any(a.check_type == "gate1_schema" and a.passed for a in audit)

def test_gate2_verbatim_evidence_pass(sample_contract_text):
    """Test Gate 2 passes exact verbatim text."""
    raw = {
        "findings": [
            {
                "id": "fnd-lockin",
                "category": "Lock-in Risk",
                "title": "Strict Lock-in",
                "severity_tier": "high",
                "evidence": "Both parties agree to a mandatory lock-in period of 6 months."
            }
        ]
    }
    validated, audit = DeterministicValidator.validate_extraction(raw, sample_contract_text)
    assert len(validated["findings"]) == 1
    assert validated["findings"][0]["confidence"] == 1.0
    gate2_audits = [a for a in audit if a.check_type == "gate2_evidence"]
    assert len(gate2_audits) == 1
    assert gate2_audits[0].passed is True

def test_gate2_hallucinated_evidence_dropped(sample_contract_text):
    """Test Gate 2 drops or flags ungrounded findings where evidence is fabricated."""
    raw = {
        "findings": [
            {
                "id": "fnd-fake",
                "category": "Fabrication",
                "title": "Astronomical Roof Tax",
                "severity_tier": "high",
                "evidence": "Tenant shall pay a special rooftop satellite tax of 50,000 gold coins annually."
            }
        ]
    }
    validated, audit = DeterministicValidator.validate_extraction(raw, sample_contract_text)
    # The validator drops findings with confidence < 0.70 or ungrounded evidence
    assert len(validated["findings"]) == 0
    gate2_audits = [a for a in audit if a.check_type == "gate2_evidence"]
    assert len(gate2_audits) == 1
    assert gate2_audits[0].passed is False

def test_gate3_amount_and_date_check(sample_contract_text):
    """Test Gate 3 cross-references amounts in explanation/evidence against source."""
    raw = {
        "findings": [
            {
                "id": "fnd-penalty",
                "category": "Financial Penalty",
                "title": "Late Fee",
                "severity_tier": "medium",
                "explanation": "Late payment penalty of INR 1,500 applies.",
                "evidence": "Failure to pay within 5 days of due date shall attract a late payment penalty of INR 1,500."
            }
        ]
    }
    validated, audit = DeterministicValidator.validate_extraction(raw, sample_contract_text)
    assert len(validated["findings"]) == 1
    gate3_audits = [a for a in audit if a.check_type == "gate3_amount_date"]
    assert len(gate3_audits) == 1
    assert gate3_audits[0].passed is True

def test_gate4_ambiguity_flagging(sample_contract_text):
    """Test Gate 4 flags ambiguous terms."""
    raw = {
        "findings": [
            {
                "id": "fnd-ambig",
                "category": "Ambiguity",
                "title": "Deductions from Deposit",
                "severity_tier": "medium",
                "explanation": "The contract mentions deductions but does not specify wear and tear criteria.",
                "evidence": "refunded within 30 days following peaceful surrender of the premises, subject to deductions."
            }
        ]
    }
    validated, audit = DeterministicValidator.validate_extraction(raw, sample_contract_text)
    assert len(validated["findings"]) == 1
    fnd = validated["findings"][0]
    assert fnd["ambiguity_detected"] is True
    assert "does not clearly specify" in fnd["ambiguity_note"]
