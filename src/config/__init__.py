"""
Módulo de configurações do projeto.
"""
from .settings import (
    OPENSEARCH_HOST,
    OPENSEARCH_PORT,
    OPENSEARCH_USER,
    OPENSEARCH_PASSWORD,
    OPENSEARCH_USE_SSL,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    ANTHROPIC_API_KEY,
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    METADATA_INDEX,
    CONTENT_INDEX,
    TAGS_IGNORADAS,
)
from .logger import setup_logger

__all__ = [
    "OPENSEARCH_HOST",
    "OPENSEARCH_PORT",
    "OPENSEARCH_USER",
    "OPENSEARCH_PASSWORD",
    "OPENSEARCH_USE_SSL",
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "ANTHROPIC_API_KEY",
    "DATA_DIR",
    "RAW_DATA_DIR",
    "PROCESSED_DATA_DIR",
    "METADATA_INDEX",
    "CONTENT_INDEX",
    "TAGS_IGNORADAS",
    "setup_logger",
]
