"""PDD §11 RESTful Document Endpoints and View Payloads."""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from typing import Optional, List, Dict, Any
from app.services.document_service import DocumentService
from app.config import DEFAULT_MODEL, DEFAULT_PROVIDER
from app.db.session import SessionLocal
from app.db.models import Document

router = APIRouter(tags=["Documents"])

@router.post("/documents")
@router.post("/api/documents")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    model: str = Form(DEFAULT_MODEL),
    provider: str = Form(DEFAULT_PROVIDER),
    temperature: float = Form(0.1)
):
    """Upload document, initiate asynchronous extraction pipeline, and return document ID."""
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    filename = file.filename or "contract.pdf"
    doc = DocumentService.create_document(filename=filename, file_bytes=content)

    # Launch background extraction pipeline
    background_tasks.add_task(
        DocumentService.process_document_pipeline,
        doc_id=doc.id,
        model=model,
        provider=provider,
        temperature=temperature
    )

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "stage": doc.stage,
        "progress": doc.progress,
        "sha256": doc.sha256,
        "message": "Document uploaded successfully. Processing pipeline started in background."
    }

@router.get("/documents")
@router.get("/api/documents")
async def list_documents():
    """List all stored documents and their current processing status."""
    db = SessionLocal()
    try:
        docs = db.query(Document).order_by(Document.created_at.desc()).all()
        return [
            {
                "id": d.id,
                "filename": d.filename,
                "title": d.title,
                "status": d.status,
                "progress": d.progress,
                "page_count": d.page_count,
                "created_at": d.created_at.isoformat() if d.created_at else None
            }
            for d in docs
        ]
    finally:
        db.close()

@router.get("/documents/{doc_id}/status")
@router.get("/api/documents/{doc_id}/status")
async def get_document_status(doc_id: str):
    """Retrieve document processing status, stage, and progress percentage."""
    res = DocumentService.get_document_status(doc_id)
    if not res:
        raise HTTPException(status_code=404, detail="Document not found.")
    return res

@router.get("/documents/{doc_id}/overview")
@router.get("/api/documents/{doc_id}/overview")
async def get_document_overview(doc_id: str):
    """Retrieve document overview decision map (parties, vitals, tenure, totals)."""
    res = DocumentService.get_document_overview(doc_id)
    if not res:
        raise HTTPException(status_code=404, detail="Document not found or analysis incomplete.")
    return res

@router.get("/documents/{doc_id}/findings")
@router.get("/api/documents/{doc_id}/findings")
async def get_document_findings(doc_id: str):
    """Retrieve attention findings with severity tiers, ambiguity flags, and source citations."""
    res = DocumentService.get_document_findings(doc_id)
    if not res:
        raise HTTPException(status_code=404, detail="Document not found.")
    return res

@router.get("/documents/{doc_id}/money")
@router.get("/api/documents/{doc_id}/money")
async def get_document_money(doc_id: str):
    """Retrieve itemized financial obligations, upfront commitments, and contingent liabilities."""
    res = DocumentService.get_document_money(doc_id)
    if not res:
        raise HTTPException(status_code=404, detail="Document not found.")
    return res

@router.get("/documents/{doc_id}/timeline")
@router.get("/api/documents/{doc_id}/timeline")
async def get_document_timeline(doc_id: str):
    """Retrieve chronological deadlines, operational requirements, and consequences."""
    res = DocumentService.get_document_timeline(doc_id)
    if not res:
        raise HTTPException(status_code=404, detail="Document not found.")
    return res

@router.get("/documents/{doc_id}/clauses")
@router.get("/api/documents/{doc_id}/clauses")
async def get_document_clauses(doc_id: str):
    """Retrieve segmented clauses with exact bounding box coordinates and section labels."""
    res = DocumentService.get_document_clauses(doc_id)
    if not res:
        raise HTTPException(status_code=404, detail="Document not found.")
    return res

@router.get("/documents/{doc_id}/export")
@router.get("/api/documents/{doc_id}/export")
async def get_document_export(doc_id: str):
    """Export formatted Markdown summary and structured Contract IR."""
    res = DocumentService.get_document_export(doc_id)
    if not res:
        raise HTTPException(status_code=404, detail="Document not found.")
    return res

@router.delete("/documents/{doc_id}")
@router.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Cascading deletion of document, derived entities, physical files, and MongoDB records."""
    success = DocumentService.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"status": "success", "message": f"Document {doc_id} and derived records successfully deleted."}
