"""Backward-compatible routes ensuring existing UI (index.html) continues to operate flawlessly."""
import os
import hashlib
import httpx
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import (
    OLLAMA_BASE_URL,
    LM_STUDIO_BASE_URL,
    GEMINI_API_KEY,
    MONGODB_DB_NAME,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER
)
from app.db.session import get_mongo_db
from app.schemas.extraction import EvaluationRequest, AskRequest
from app.extraction.llm_client import LLMClient
from app.services.document_service import DocumentService
from app.pipeline.pdf_parser import PDFParser

router = APIRouter(tags=["Legacy & Compatibility"])

@router.get("/api/models")
async def get_available_models():
    """Detect available models across Gemini Cloud, Ollama, and LM Studio."""
    discovered = []

    # 1. Gemini Cloud
    if GEMINI_API_KEY:
        discovered.append({
            "id": "gemini-3.8-flash",
            "name": "Gemini 3.8 Flash (Default / Google Cloud)",
            "provider": "gemini",
            "size": "Cloud AI",
            "endpoint": "Google Generative AI",
            "status": "online",
            "recommended": True
        })
        discovered.append({
            "id": "gemini-2.5-pro",
            "name": "Gemini 2.5 Pro (Deep Analysis / Google Cloud)",
            "provider": "gemini",
            "size": "Cloud AI",
            "endpoint": "Google Generative AI",
            "status": "online",
            "recommended": False
        })

    # 2. Ollama
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                data = resp.json()
                for m in data.get("models", []):
                    name = m.get("name")
                    size_gb = round(m.get("size", 0) / (1024**3), 2)
                    discovered.append({
                        "id": name,
                        "name": name,
                        "provider": "ollama",
                        "size": f"{size_gb} GB" if size_gb > 0 else "Local",
                        "endpoint": OLLAMA_BASE_URL,
                        "status": "online",
                        "recommended": "qwen2.5-coder:7b" in name or "qwen2.5-coder:1.5b" in name
                    })
    except Exception:
        pass

    # 3. LM Studio
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{LM_STUDIO_BASE_URL}/models")
            if resp.status_code == 200:
                data = resp.json()
                for m in data.get("data", []):
                    model_id = m.get("id")
                    discovered.append({
                        "id": model_id,
                        "name": model_id,
                        "provider": "lmstudio",
                        "size": "Local",
                        "endpoint": LM_STUDIO_BASE_URL,
                        "status": "online",
                        "recommended": False
                    })
    except Exception:
        pass

    if not discovered:
        discovered = [
            {"id": "qwen2.5-coder:7b", "name": "qwen2.5-coder:7b", "provider": "ollama", "size": "4.7 GB", "endpoint": OLLAMA_BASE_URL, "status": "standby", "recommended": True},
            {"id": "qwen2.5-coder:1.5b", "name": "qwen2.5-coder:1.5b", "provider": "ollama", "size": "1.0 GB", "endpoint": OLLAMA_BASE_URL, "status": "standby", "recommended": False}
        ]

    return {
        "status": "success",
        "models": discovered,
        "gemini_connected": bool(GEMINI_API_KEY),
        "ollama_connected": any(m["provider"] == "ollama" and m["status"] == "online" for m in discovered),
        "lmstudio_connected": any(m["provider"] == "lmstudio" and m["status"] == "online" for m in discovered)
    }

@router.post("/api/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """Extract text using layout-aware parser."""
    contents = await file.read()
    filename = file.filename or "uploaded_contract"
    
    parsed = PDFParser.parse_document(contents, filename)
    sha256 = hashlib.sha256(contents).hexdigest()

    return {
        "status": "success",
        "filename": filename,
        "page_count": parsed["page_count"],
        "char_count": parsed["char_count"],
        "sha256": sha256,
        "text": parsed["full_text"]
    }

@router.post("/api/evaluate")
async def evaluate_contract(req: EvaluationRequest):
    """Synchronous evaluation endpoint persisting and returning Contract IR."""
    if not req.contract_text.strip():
        raise HTTPException(status_code=400, detail="Contract text cannot be empty.")

    filename = req.contract_title or "contract.txt"
    if not filename.endswith((".pdf", ".txt", ".md")):
        filename += ".txt"

    file_bytes = req.contract_text.encode("utf-8")
    doc = DocumentService.create_document(filename=filename, file_bytes=file_bytes)

    # Process through pipeline
    await DocumentService.process_document_pipeline(
        doc_id=doc.id,
        model=req.model,
        provider=req.provider,
        temperature=req.temperature
    )

    contract_ir = DocumentService.build_contract_ir_dict(doc.id)
    if not contract_ir:
        raise HTTPException(status_code=500, detail="Contract evaluation failed to assemble Contract IR.")

    return {
        "status": "success",
        "model_used": req.model,
        "provider": req.provider,
        "contract_ir": contract_ir
    }

@router.post("/api/ask")
async def ask_contract_question(req: AskRequest):
    """Answer questions about the contract with strict grounding."""
    try:
        answer = await LLMClient.query_ask(
            question=req.question,
            contract_text=req.contract_text,
            model=req.model,
            provider=req.provider
        )
        return {"status": "success", "answer": answer}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/api/db-status")
async def get_db_status():
    """Verify MongoDB Atlas connectivity and return cluster information."""
    mongo_db = get_mongo_db()
    if mongo_db is None:
        return {
            "status": "disconnected",
            "message": "MongoDB Atlas is not configured or offline."
        }
    try:
        collections = mongo_db.list_collection_names()
        return {
            "status": "connected",
            "database": MONGODB_DB_NAME,
            "collections": collections,
            "cluster": "cluster0.zxh6if2.mongodb.net"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
