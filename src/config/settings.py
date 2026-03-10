"""
Configurações globais do projeto.
Carrega variáveis de ambiente e define constantes.
"""
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(find_dotenv())

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", "9200"))
OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD", "my_password")
OPENSEARCH_USE_SSL = os.getenv("OPENSEARCH_USE_SSL", "true").lower() == "true"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING = os.getenv("OPENAI_EMBEDDING", "text-embedding-3-large")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
EVERY_FIGS_PDF = RAW_DATA_DIR / "figures"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

METADATA_INDEX = "metadata-pdfs"
CONTENT_INDEX = "content-pdfs"

TAGS_IGNORADAS = {'foot', 'fnote', 'que', 'sec_0', 'header'}

__all__ = [
    "PROJECT_ROOT",
    "OPENSEARCH_HOST",
    "OPENSEARCH_PORT",
    "OPENSEARCH_USER",
    "OPENSEARCH_PASSWORD",
    "OPENSEARCH_USE_SSL",
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "OPENAI_EMBEDDING",
    "ANTHROPIC_API_KEY",
    "DATA_DIR",
    "RAW_DATA_DIR",
    "EVERY_FIGS_PDF",
    "PROCESSED_DATA_DIR",
    "METADATA_INDEX",
    "CONTENT_INDEX",
    "TAGS_IGNORADAS",
]
