"""Canonical Source Traceability API (PDD §11)."""
from fastapi import APIRouter, HTTPException
from app.services.document_service import DocumentService

router = APIRouter(tags=["Sources"])

@router.get("/sources/{source_id}")
@router.get("/api/sources/{source_id}")
async def get_source(source_id: str):
    """Retrieve canonical source grounding record with exact page, section, bbox, and text."""
    src = DocumentService.get_source(source_id)
    if not src:
        raise HTTPException(status_code=404, detail="Source not found.")
    return src
