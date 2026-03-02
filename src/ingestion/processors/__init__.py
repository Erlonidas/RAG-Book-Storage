"""
Processadores de ingestão (transformação de dados).
"""
from .chunk_builder import (
    processar_json_dolphin,
    criar_doc,
    get_section_content,
    get_section_hierarchy,
)
from .metadata_extractor import extract_article_metadata

__all__ = [
    "processar_json_dolphin",
    "criar_doc",
    "get_section_content",
    "get_section_hierarchy",
    "extract_article_metadata",
]
