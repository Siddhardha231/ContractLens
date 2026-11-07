"""Server-Sent Events (SSE) router for real-time document extraction streaming."""
import asyncio
import json
from typing import Dict, List, Any
from fastapi import APIRouter, Request, HTTPException
from sse_starlette.sse import EventSourceResponse

from app.db.session import SessionLocal
from app.db.models import Document

router = APIRouter(tags=["Events & Real-Time Streaming"])

class DocumentEventBroadcaster:
    """Pub/Sub manager for real-time document processing events."""
    _subscribers: Dict[str, List[asyncio.Queue]] = {}

    @classmethod
    def subscribe(cls, doc_id: str) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        if doc_id not in cls._subscribers:
            cls._subscribers[doc_id] = []
        cls._subscribers[doc_id].append(q)
        return q

    @classmethod
    def unsubscribe(cls, doc_id: str, q: asyncio.Queue):
        if doc_id in cls._subscribers:
            try:
                cls._subscribers[doc_id].remove(q)
                if not cls._subscribers[doc_id]:
                    del cls._subscribers[doc_id]
            except ValueError:
                pass

    @classmethod
    async def emit(cls, doc_id: str, event_data: Dict[str, Any]):
        """Publish event to all queues listening for this document."""
        if doc_id in cls._subscribers:
            for q in cls._subscribers[doc_id]:
                await q.put(event_data)

@router.get("/documents/{doc_id}/events")
@router.get("/api/documents/{doc_id}/events")
async def stream_document_events(doc_id: str, request: Request):
    """Stream real-time background processing status events for a document."""
    # Check if document exists
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found.")
        current_status = doc.status
        current_progress = doc.progress
        current_stage = doc.stage
    finally:
        db.close()

    async def event_generator():
        # Yield initial status immediately
        yield {
            "event": "message",
            "data": json.dumps({
                "document_id": doc_id,
                "status": current_status,
                "progress": current_progress,
                "stage": current_stage
            })
        }

        # If already terminal, exit stream
        if current_status in ["COMPLETED", "FAILED"]:
            return

        queue = DocumentEventBroadcaster.subscribe(doc_id)
        try:
            while True:
                # Disconnect check
                if await request.is_disconnected():
                    break

                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield {
                        "event": "message",
                        "data": json.dumps(event)
                    }
                    if event.get("status") in ["COMPLETED", "FAILED"]:
                        break
                except asyncio.TimeoutError:
                    # Keep-alive heartbeat comment
                    yield {"event": "ping", "data": "keep-alive"}
        finally:
            DocumentEventBroadcaster.unsubscribe(doc_id, queue)

    return EventSourceResponse(event_generator())
