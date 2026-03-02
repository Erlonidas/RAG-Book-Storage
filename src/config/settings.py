"""
Configurações globais do projeto.
Carrega variáveis de ambiente e define constantes.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env do diretório raiz do projeto
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_PATH = PROJECT_ROOT / "src" / ".env"
load_dotenv(ENV_PATH)

# OpenSearch
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", "9200"))
OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD", "my_password")
OPENSEARCH_USE_SSL = os.getenv("OPENSEARCH_USE_SSL", "true").lower() == "true"

# OpenAI / LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
EVERY_FIGS_PDF = RAW_DATA_DIR / "figs"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# OpenSearch Indexes
METADATA_INDEX = "metadata-index"
CONTENT_INDEX = "content-index"

TAGS_IGNORADAS = {'foot', 'fnote', 'que', 'sec_0', 'header'}
