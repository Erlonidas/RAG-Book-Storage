"""
Serviços externos (OpenSearch, LLM, etc).
"""
from .opensearch import OpenSearchClient
from .llm_factory import create_llm, LLMProvider
from .embedding_processor import VectorProcessor

__all__ = [
    "OpenSearchClient",
    "create_llm", 
    "LLMProvider",
    "VectorProcessor"
]
