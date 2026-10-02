"""API routers package for ContractLens."""
from app.api.documents import router as documents_router
from app.api.sources import router as sources_router
from app.api.legacy_compat import router as legacy_router

__all__ = [
    "documents_router",
    "sources_router",
    "legacy_router",
]
