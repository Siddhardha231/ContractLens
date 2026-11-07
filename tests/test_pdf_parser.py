import pytest
from app.pipeline.pdf_parser import PDFParser, LayoutBlock

def test_parse_text_document(sample_contract_text):
    """Test text document parsing produces valid pages and layout blocks."""
    parsed = PDFParser.parse_document(sample_contract_text.encode("utf-8"), "sample_lease.txt")
    assert parsed["page_count"] >= 1
    assert parsed["char_count"] > 0
    assert len(parsed["blocks"]) > 0
    assert parsed["full_text"] == sample_contract_text

    # Verify blocks have valid bboxes
    for b in parsed["blocks"]:
        assert len(b.bbox) == 4
        assert b.bbox[0] < b.bbox[2]  # ymin < ymax
        assert b.bbox[1] < b.bbox[3]  # xmin < xmax

def test_locate_text_coordinates(sample_contract_text):
    """Test locating coordinates of a snippet inside layout blocks."""
    parsed = PDFParser.parse_document(sample_contract_text.encode("utf-8"), "sample_lease.txt")
    blocks = parsed["blocks"]

    page, bbox = PDFParser.locate_text_coordinates("The Monthly Rent shall be INR 38,000", blocks)
    assert page >= 1
    assert len(bbox) == 4
    assert bbox[0] < bbox[2]
