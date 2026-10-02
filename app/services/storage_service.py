"""Storage service for document files and local persistence."""
import os
import hashlib
from typing import Tuple
from app.config import UPLOAD_DIR

class StorageService:
    """Handles saving, reading, and deleting uploaded contract files."""

    @classmethod
    def save_file(cls, filename: str, content: bytes, doc_id: str) -> Tuple[str, str, int]:
        """Save file bytes to local disk, returning (file_path, sha256, byte_count)."""
        safe_filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
        target_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{safe_filename}")
        
        with open(target_path, "wb") as f:
            f.write(content)

        sha256 = hashlib.sha256(content).hexdigest()
        return target_path, sha256, len(content)

    @classmethod
    def read_file(cls, file_path: str) -> bytes:
        """Read file bytes from disk."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as f:
            return f.read()

    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        """Delete file from disk if it exists."""
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception:
                return False
        return False
