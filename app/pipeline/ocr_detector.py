"""OCR Detection for scanned vs digital documents."""
from typing import Dict, Any
from app.config import OCR_MIN_CHARS_PER_PAGE

class OCRDetector:
    """Evaluates whether document pages are scanned or digital text."""

    @staticmethod
    def check_page_scanned(char_count: int, has_images: bool = False) -> bool:
        """Flag page as scanned if extracted text density is below threshold."""
        if char_count < OCR_MIN_CHARS_PER_PAGE:
            return True
        return False

    @staticmethod
    def evaluate_document_scan_status(pages_info: list) -> Dict[str, Any]:
        """Aggregate document-level OCR and digital text readiness."""
        total_pages = len(pages_info)
        if total_pages == 0:
            return {"scanned_pages_count": 0, "is_mostly_scanned": False, "ratio": 0.0}

        scanned_count = sum(1 for p in pages_info if p.get("is_scanned", False))
        ratio = scanned_count / total_pages

        return {
            "total_pages": total_pages,
            "scanned_pages_count": scanned_count,
            "is_mostly_scanned": ratio >= 0.5,
            "scanned_ratio": round(ratio, 2)
        }
