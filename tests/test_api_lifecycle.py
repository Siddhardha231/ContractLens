import pytest
from fastapi.testclient import TestClient

def test_api_models_endpoint(client: TestClient):
    """Test /api/models returns available models list."""
    response = client.get("/api/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0

def test_document_lifecycle(client: TestClient, sample_contract_text):
    """Test full document lifecycle: upload, status, overview, delete."""
    # 1. Upload
    files = {"file": ("test_lease_agreement.txt", sample_contract_text.encode("utf-8"), "text/plain")}
    upload_res = client.post("/documents", files=files)
    assert upload_res.status_code == 200
    upload_data = upload_res.json()
    doc_id = upload_data["document_id"]
    assert doc_id.startswith("doc-")

    # 2. Status poll
    status_res = client.get(f"/documents/{doc_id}/status")
    assert status_res.status_code == 200
    status_data = status_res.json()
    assert "status" in status_data

    # 3. List documents
    list_res = client.get("/documents")
    assert list_res.status_code == 200
    doc_list = list_res.json()
    assert any(d["id"] == doc_id for d in doc_list)

    # 4. Fetch raw document file
    file_res = client.get(f"/documents/{doc_id}/file")
    assert file_res.status_code == 200
    assert len(file_res.content) > 0

    # 5. Test SSE Event Stream
    with client.stream("GET", f"/documents/{doc_id}/events") as event_stream:
        assert event_stream.status_code == 200
        first_line = next(event_stream.iter_lines())
        assert "data:" in first_line or "event:" in first_line

    # 6. Test Export Endpoints (Markdown & HTML Report)
    export_res = client.get(f"/documents/{doc_id}/export")
    assert export_res.status_code == 200
    assert "markdown_report" in export_res.json()

    html_export_res = client.get(f"/documents/{doc_id}/export/html")
    assert html_export_res.status_code == 200
    assert "ContractLens Executive Audit" in html_export_res.text

    # 7. Delete document
    del_res = client.delete(f"/documents/{doc_id}")
    assert del_res.status_code == 200
    assert del_res.json()["deleted"] is True
