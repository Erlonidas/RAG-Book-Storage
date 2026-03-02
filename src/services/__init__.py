"""
Serviços externos (OpenSearch, LLM, etc).
"""
from .opensearch import OpenSearchClient
from .llm_factory import create_llm, LLMProvider

__all__ = ["OpenSearchClient", "create_llm", "LLMProvider"]
