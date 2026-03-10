"""
Processadores de ingestão (transformação de dados).
"""
from .chunk_builder import (
    process_json_dolphin,
    create_doc,
    get_section_content,
    get_section_hierarchy,
)
from .metadata_extractor import extract_article_metadata

__all__ = [
    "process_json_dolphin",
    "create_doc",
    "get_section_content",
    "get_section_hierarchy",
    "extract_article_metadata",
]
