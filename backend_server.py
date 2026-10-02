"""
ContractLens — Visual Contract Intelligence Platform
FastAPI Application Entrypoint
Conforms strictly to the Product Development Document (PDD) and Technical Design Architecture (TDA).
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.config import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    GEMINI_API_KEY,
    OLLAMA_BASE_URL,
    LM_STUDIO_BASE_URL,
    MONGODB_DB_NAME,
    DATABASE_URL,
)
from app.db.session import init_db, get_mongo_db
from app.api.documents import router as documents_router
from app.api.sources import router as sources_router
from app.api.legacy_compat import router as legacy_router

contractlens_dir = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite / PostgreSQL Database tables
    init_db()
    print(f"[ContractLens Engine] Initialized Relational Database: {DATABASE_URL}")
    mongo = get_mongo_db()
    if mongo is not None:
        try:
            mongo.command("ping")
            print(f"[ContractLens Engine] Connected to MongoDB Atlas: '{MONGODB_DB_NAME}'")
        except Exception as e:
            print(f"[ContractLens Engine] MongoDB Atlas ping failed: {e}")
    else:
        print("[ContractLens Engine] MongoDB Atlas: Not configured or offline")
    yield

app = FastAPI(
    title="ContractLens Visual Intelligence Backend",
    description="Deterministic, traceable legal contract analysis conforming to PDD & TDA specifications.",
    version="2.5.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Modular API Routers
app.include_router(documents_router)
app.include_router(sources_router)
app.include_router(legacy_router)

# Static Dashboard File Endpoints
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(contractlens_dir, "index.html"))

@app.get("/contract-ir.js")
async def serve_contract_ir():
    return FileResponse(os.path.join(contractlens_dir, "contract-ir.js"))

if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("  ContractLens Visual Intelligence Backend v2.5.0")
    print(f"  Web Dashboard:     http://localhost:8000")
    print(f"  Interactive Docs:  http://localhost:8000/docs")
    print(f"  Primary AI Engine: {DEFAULT_PROVIDER.upper()} ({DEFAULT_MODEL})")
    print(f"  Ollama Base:       {OLLAMA_BASE_URL}")
    print(f"  LM Studio Base:    {LM_STUDIO_BASE_URL}")
    print("=" * 70)
    uvicorn.run("backend_server:app", host="127.0.0.1", port=8000, reload=True)
