import os
import sys
import json
from pathlib import Path
from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend_server import app
from app.db.session import init_db, SessionLocal
from app.db.models import Document
from app.extraction.llm_client import LLMClient

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure database tables exist for tests."""
    init_db()
    yield

@pytest.fixture(autouse=True)
def mock_llm_extraction(monkeypatch):
    """Mock external LLM calls to prevent external network requests during unit tests."""
    mock_payload = {
        "title": "Residential Lease Agreement",
        "parties": ["Rajesh Kumar", "Priya Sharma"],
        "effective_date": "2026-02-01",
        "expiration_date": "2026-12-31",
        "tenure_months": 11,
        "financial_terms": [
            {
                "id": "ft-rent",
                "label": "Monthly Rent",
                "amount": 38000,
                "currency": "INR",
                "frequency": "monthly",
                "trigger": "Monthly lease payment",
                "evidence": "The Monthly Rent shall be INR 38,000 payable in advance",
                "confidence": 1.0,
                "type": "recurring_commitment"
            }
        ],
        "deadlines": [
            {
                "id": "dl-1",
                "date": "2026-02-05",
                "relative_label": "Monthly 5th",
                "event": "Rent Due",
                "action": "The Monthly Rent shall be INR 38,000 payable in advance on or before the 5th day of each calendar month.",
                "consequence": "Late payment penalty of INR 1,500.",
                "category": "payment",
                "attention_tier": "medium",
                "confidence": 1.0
            }
        ],
        "obligations": [
            {
                "id": "ob-1",
                "actor": "Tenant",
                "action": "The Tenant shall directly pay electricity charges as per BESCOM meter and society maintenance charges of INR 4,500 monthly.",
                "condition": None,
                "confidence": 1.0
            }
        ],
        "findings": [
            {
                "id": "fnd-1",
                "category": "Lock-in Risk",
                "title": "Mandatory Lock-in Period",
                "severity_tier": "high",
                "explanation": "6-month mandatory lock-in period with full deposit forfeiture.",
                "evidence": "Both parties agree to a mandatory lock-in period of 6 months. If Tenant vacates during the lock-in period, the entire security deposit shall be forfeited.",
                "ambiguity_detected": False,
                "confidence": 1.0
            }
        ]
    }

    async def mock_query(*args, **kwargs):
        return json.dumps(mock_payload)

    monkeypatch.setattr(LLMClient, "query_extraction", mock_query)

@pytest.fixture
def client():
    """FastAPI Test Client."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_contract_text():
    return """RESIDENTIAL LEASE AGREEMENT
This agreement is entered into between Landlord Rajesh Kumar and Tenant Priya Sharma on January 15, 2026.
1. TERM & PROPERTY
The term of this lease shall be 11 months commencing on February 1, 2026 and expiring on December 31, 2026.
The premises is Apartment 402, Green Glen Layout, Bellandur, Bengaluru.
2. RENT AND PAYMENT
The Monthly Rent shall be INR 38,000 payable in advance on or before the 5th day of each calendar month.
Failure to pay within 5 days of due date shall attract a late payment penalty of INR 1,500.
3. SECURITY DEPOSIT
The Tenant has deposited an interest-free refundable security deposit of INR 2,00,000.
The deposit shall be refunded within 30 days following peaceful surrender of the premises, subject to deductions.
4. LOCK-IN PERIOD & TERMINATION
Both parties agree to a mandatory lock-in period of 6 months. If Tenant vacates during the lock-in period, the entire security deposit shall be forfeited.
Either party may terminate after lock-in by providing 2 calendar months written notice.
5. MAINTENANCE & UTILITIES
The Tenant shall directly pay electricity charges as per BESCOM meter and society maintenance charges of INR 4,500 monthly.
6. JURISDICTION
This agreement shall be governed by the laws of Bengaluru, Karnataka, India."""
