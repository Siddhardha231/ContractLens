"""Layout-aware PDF parsing engine extracting text spans with precise bounding boxes."""
import io
import os
import re
from typing import List, Dict, Any, Optional, Tuple
from app.pipeline.ocr_detector import OCRDetector

class LayoutBlock:
    """Represents a discrete text block with page and bounding box coordinates."""
    def __init__(
        self,
        page_number: int,
        bbox: List[float],  # [ymin, xmin, ymax, xmax]
        text: str,
        block_idx: int = 0
    ):
        self.page_number = page_number
        self.bbox = [round(b, 2) for b in bbox]
        self.text = text.strip()
        self.block_idx = block_idx

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page": self.page_number,
            "bbox": self.bbox,
            "text": self.text,
            "block_idx": self.block_idx
        }


class PDFParser:
    """Extracts structured text, page geometries, and coordinate-grounded blocks."""

    @classmethod
    def parse_document(cls, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Parse file content (PDF or Text), returning layout blocks and page metadata."""
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            return cls._parse_pdf(file_bytes)
        else:
            return cls._parse_text(file_bytes)

    @classmethod
    def _parse_pdf(cls, file_bytes: bytes) -> Dict[str, Any]:
        """Parse PDF with PyMuPDF, with graceful fallback to pypdf."""
        try:
            import pymupdf  # PyMuPDF
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            
            pages_data = []
            all_blocks: List[LayoutBlock] = []
            full_text_parts = []
            
            for page_idx in range(len(doc)):
                page_num = page_idx + 1
                page = doc[page_idx]
                width = page.rect.width
                height = page.rect.height
                
                # Extract text blocks with coordinates: (x0, y0, x1, y1, "text", block_no, block_type)
                raw_blocks = page.get_text("blocks")
                page_text_parts = []
                page_blocks = []
                
                for b_idx, b in enumerate(raw_blocks):
                    # block_type 0 = text, 1 = image
                    if len(b) >= 5 and b[4].strip():
                        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
                        # Standardize bbox to [ymin, xmin, ymax, xmax]
                        block_obj = LayoutBlock(
                            page_number=page_num,
                            bbox=[y0, x0, y1, x1],
                            text=text,
                            block_idx=b_idx
                        )
                        page_blocks.append(block_obj)
                        all_blocks.append(block_obj)
                        page_text_parts.append(text.strip())
                
                page_full_text = "\n".join(page_text_parts)
                is_scanned = OCRDetector.check_page_scanned(len(page_full_text))
                
                pages_data.append({
                    "page_number": page_num,
                    "width": width,
                    "height": height,
                    "char_count": len(page_full_text),
                    "is_scanned": is_scanned,
                    "blocks_count": len(page_blocks)
                })
                
                full_text_parts.append(f"--- PAGE {page_num} ---\n{page_full_text}")

            full_text = "\n\n".join(full_text_parts)
            return {
                "engine": "PyMuPDF",
                "page_count": len(pages_data),
                "char_count": len(full_text),
                "pages": pages_data,
                "blocks": all_blocks,
                "full_text": full_text
            }

        except ImportError:
            # Fallback to pypdf
            return cls._parse_pdf_pypdf(file_bytes)

    @classmethod
    def _parse_pdf_pypdf(cls, file_bytes: bytes) -> Dict[str, Any]:
        """Fallback PDF parser using pypdf."""
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages_data = []
        all_blocks: List[LayoutBlock] = []
        full_text_parts = []

        for page_idx, page in enumerate(reader.pages):
            page_num = page_idx + 1
            text = page.extract_text() or ""
            mediabox = page.mediabox
            width = float(mediabox.width) if mediabox else 612.0
            height = float(mediabox.height) if mediabox else 792.0

            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            for p_idx, para in enumerate(paragraphs):
                # Approximate vertical coordinates per paragraph
                total_paras = max(1, len(paragraphs))
                y0 = 60.0 + (p_idx / total_paras) * (height - 120.0)
                y1 = min(height - 40.0, y0 + 50.0)
                block_obj = LayoutBlock(
                    page_number=page_num,
                    bbox=[y0, 50.0, y1, width - 50.0],
                    text=para,
                    block_idx=p_idx
                )
                all_blocks.append(block_obj)

            is_scanned = OCRDetector.check_page_scanned(len(text))
            pages_data.append({
                "page_number": page_num,
                "width": width,
                "height": height,
                "char_count": len(text),
                "is_scanned": is_scanned,
                "blocks_count": len(paragraphs)
            })
            full_text_parts.append(f"--- PAGE {page_num} ---\n{text}")

        full_text = "\n\n".join(full_text_parts)
        return {
            "engine": "pypdf",
            "page_count": len(pages_data),
            "char_count": len(full_text),
            "pages": pages_data,
            "blocks": all_blocks,
            "full_text": full_text
        }

    @classmethod
    def _parse_text(cls, file_bytes: bytes) -> Dict[str, Any]:
        """Parse plain text, Markdown, or ASCII files."""
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = file_bytes.decode("latin-1", errors="ignore")

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        page_count = max(1, len(text) // 2500)
        paras_per_page = max(1, len(paragraphs) // page_count) if paragraphs else 1

        pages_data = []
        all_blocks = []

        for p_idx, para in enumerate(paragraphs):
            page_num = min(page_count, (p_idx // paras_per_page) + 1)
            offset = p_idx % paras_per_page
            y0 = 50.0 + offset * 80.0
            block_obj = LayoutBlock(
                page_number=page_num,
                bbox=[y0, 50.0, y0 + 60.0, 550.0],
                text=para,
                block_idx=p_idx
            )
            all_blocks.append(block_obj)

        for pg in range(1, page_count + 1):
            pages_data.append({
                "page_number": pg,
                "width": 612.0,
                "height": 792.0,
                "char_count": len(text) // page_count,
                "is_scanned": False,
                "blocks_count": len([b for b in all_blocks if b.page_number == pg])
            })

        return {
            "engine": "text_decoder",
            "page_count": page_count,
            "char_count": len(text),
            "pages": pages_data,
            "blocks": all_blocks,
            "full_text": text
        }

    @classmethod
    def locate_text_coordinates(
        cls,
        search_snippet: str,
        blocks: List[LayoutBlock],
        fallback_page: int = 1
    ) -> Tuple[int, List[float]]:
        """Find the real page and bounding box enclosing a text snippet or evidence quote."""
        if not search_snippet or not blocks:
            return fallback_page, [80.0, 50.0, 160.0, 520.0]

        clean_snippet = re.sub(r'\s+', ' ', search_snippet.strip().lower())
        snippet_words = clean_snippet.split()

        # 1. Exact or substring match in block text
        for b in blocks:
            block_text = re.sub(r'\s+', ' ', b.text.lower())
            if clean_snippet in block_text or (len(clean_snippet) > 15 and clean_snippet[:25] in block_text):
                return b.page_number, b.bbox

        # 2. Key word density match
        best_block = None
        best_score = 0.0
        min_words = min(5, len(snippet_words))

        if min_words > 0:
            for b in blocks:
                block_text = re.sub(r'\s+', ' ', b.text.lower())
                matches = sum(1 for w in snippet_words if len(w) > 3 and w in block_text)
                score = matches / len(snippet_words)
                if score > best_score and score >= 0.4:
                    best_score = score
                    best_block = b

        if best_block:
            return best_block.page_number, best_block.bbox

        return fallback_page, [80.0, 50.0, 160.0, 520.0]
