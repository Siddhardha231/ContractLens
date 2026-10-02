"""Semantic Clause Segmentation Engine (PDD §7.3, TDA §3)."""
import re
from typing import List, Dict, Any
from app.pipeline.pdf_parser import LayoutBlock

# Common clause header patterns
SECTION_HEADER_REGEX = re.compile(
    r'^(?:(?:clause|section|article)\s+([0-9A-Za-z\.\-]+)|([0-9]{1,2}(?:\.[0-9]{1,2}){0,3})\.?)\s*[:\-–—]?\s*(.*)$',
    re.IGNORECASE
)

CLAUSE_TYPE_KEYWORDS = {
    "rent": ["rent", "monthly payment", "consideration", "fee", "license fee"],
    "deposit": ["security deposit", "caution deposit", "earnest money"],
    "term": ["tenure", "term", "duration", "period", "effective date", "expiration"],
    "termination": ["termination", "lock-in", "eviction", "default", "breach", "cancel"],
    "notice": ["notice period", "intimation", "written notice", "registered post"],
    "maintenance": ["maintenance", "society charges", "repairs", "painting"],
    "utilities": ["electricity", "water", "gas", "utility", "power"],
    "use": ["permitted use", "residential use", "prohibition", "sublet", "sub-letting"],
    "entry": ["inspection", "entry", "access to premises", "visit"],
    "indemnity": ["indemnity", "liability", "damages", "force majeure"]
}

class SemanticClause:
    def __init__(
        self,
        section_label: str,
        title: str,
        text: str,
        page: int,
        bbox: List[float],
        clause_type: str = "general"
    ):
        self.section_label = section_label
        self.title = title
        self.text = text
        self.page = page
        self.bbox = bbox
        self.clause_type = clause_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section": self.section_label,
            "title": self.title,
            "text": self.text,
            "page": self.page,
            "bbox": self.bbox,
            "type": self.clause_type,
            "summary": self.text[:120].strip() + ("..." if len(self.text) > 120 else "")
        }


class ClauseSegmenter:
    """Segments document blocks into coherent legal clauses with bounding box aggregations."""

    @classmethod
    def segment_blocks(cls, blocks: List[LayoutBlock]) -> List[SemanticClause]:
        """Aggregate layout blocks into semantic clauses based on heading heuristics."""
        if not blocks:
            return []

        clauses: List[SemanticClause] = []
        current_label = "1.0"
        current_title = "Preamble & Recitals"
        current_text_parts = []
        current_page = blocks[0].page_number if blocks else 1
        current_bbox = list(blocks[0].bbox) if blocks else [50.0, 50.0, 150.0, 500.0]

        for block in blocks:
            lines = [l.strip() for l in block.text.split("\n") if l.strip()]
            if not lines:
                continue

            first_line = lines[0]
            header_match = SECTION_HEADER_REGEX.match(first_line)

            if header_match and current_text_parts:
                # Flush previous clause
                clause_text = "\n".join(current_text_parts).strip()
                if clause_text:
                    clauses.append(
                        SemanticClause(
                            section_label=current_label,
                            title=current_title,
                            text=clause_text,
                            page=current_page,
                            bbox=current_bbox,
                            clause_type=cls._infer_type(current_title + " " + clause_text)
                        )
                    )

                # Start new clause
                sec_no = header_match.group(1) or header_match.group(2) or f"1.{len(clauses)+1}"
                title_rest = header_match.group(3).strip()
                current_label = f"Sec {sec_no}"
                current_title = title_rest if title_rest else f"Clause {sec_no}"
                current_text_parts = lines[1:] if len(lines) > 1 else [first_line]
                current_page = block.page_number
                current_bbox = list(block.bbox)
            else:
                current_text_parts.append(block.text)
                # Expand bounding box if same page
                if block.page_number == current_page:
                    current_bbox[0] = min(current_bbox[0], block.bbox[0])
                    current_bbox[1] = min(current_bbox[1], block.bbox[1])
                    current_bbox[2] = max(current_bbox[2], block.bbox[2])
                    current_bbox[3] = max(current_bbox[3], block.bbox[3])

        # Flush final clause
        if current_text_parts:
            clause_text = "\n".join(current_text_parts).strip()
            clauses.append(
                SemanticClause(
                    section_label=current_label,
                    title=current_title,
                    text=clause_text,
                    page=current_page,
                    bbox=current_bbox,
                    clause_type=cls._infer_type(current_title + " " + clause_text)
                )
            )

        # Fallback if no sections detected: split into logical page-level or paragraph clauses
        if len(clauses) <= 1 and len(blocks) > 1:
            clauses = []
            for idx, b in enumerate(blocks):
                clauses.append(
                    SemanticClause(
                        section_label=f"Sec {idx+1}.0",
                        title=f"Clause {idx+1}",
                        text=b.text,
                        page=b.page_number,
                        bbox=b.bbox,
                        clause_type=cls._infer_type(b.text)
                    )
                )

        return clauses

    @classmethod
    def _infer_type(cls, text: str) -> str:
        """Infer clause categorization from keywords."""
        lower = text.lower()
        for ctype, kws in CLAUSE_TYPE_KEYWORDS.items():
            if any(kw in lower for kw in kws):
                return ctype
        return "general"
