"""Configuration settings for ContractLens."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"

# Ensure data directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Database Configuration (SQLite default with PostgreSQL support)
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATA_DIR / 'contractlens.db'}")

# MongoDB Atlas Configuration
MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "contractlens")

# AI Engine / Provider Configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
LM_STUDIO_BASE_URL = os.environ.get("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_CLIENT_ID = os.environ.get("GEMINI_CLIENT_ID")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

DEFAULT_MODEL = "gemini-3.8-flash" if GEMINI_API_KEY else "qwen2.5-coder:1.5b"
DEFAULT_PROVIDER = "gemini" if GEMINI_API_KEY else "ollama"

# Processing Thresholds (PDD §7, §8)
OCR_MIN_CHARS_PER_PAGE = 40
MAX_CLAUSE_CONTEXT_CHARS = 35000
CONFIDENCE_THRESHOLD = 0.70
