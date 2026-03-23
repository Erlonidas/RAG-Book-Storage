import json
from pathlib import Path
from typing import List, Dict, Any

from src.config import RAW_DATA_DIR, METADATA_INDEX, CONTENT_INDEX, PROJECT_ROOT, setup_logger
from src.services import OpenSearchClient
from src.ingestion.processors import (
    process_json_dolphin,
    extract_article_metadata,
)
from src.services.embedding_processor import VectorProcessor
from src.ingestion.processors.chunk_preprocessor import ContentAggregator

logger = setup_logger(__name__)


def load_dolphin_json(json_path: Path) -> Dict[str, Any]:
    """Loads raw chunks json format from Dolphin tool"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_opensearch_mapping(mapping_path: Path) -> Dict[str, Any]:
    """Load format to mapping in OpenSearch"""
    with open(mapping_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def process_all_jsons(json_dir: Path) -> tuple[List[Dict], List[Dict]]:
    """
    Process all JSONs from the Dolphin tool in this directory
    
    Returns:
        Tuple (metadata, chunks_content)
    """
    all_metadata = []
    all_chunks = []
    
    json_files = list(json_dir.glob("*.json"))
    logger.info(f"Found {len(json_files)} files JSON")
    
    for json_file in json_files:
        dolphin_json = load_dolphin_json(json_file)
        book_id = dolphin_json["source_file"]
        logger.info(f"Processing: {book_id}")
        
        # extract metadata type dict
        metadata = extract_article_metadata(dolphin_json, book_id)
        if metadata:
            all_metadata.append(metadata)
        
        # Gen chunks
        chunks = process_json_dolphin(dolphin_json, book_id)
        all_chunks.extend(chunks)
    
    logger.info(f"Total: {len(all_metadata)} metadata, {len(all_chunks)} chunks")
    return all_metadata, all_chunks


def main():
    logger.info("=== Start Ingestion ===")
    json_dir = RAW_DATA_DIR / "json_extraction"
    
    if not json_dir.exists():
        logger.error(f"Directory not found: {json_dir}")
        return
    
    logger.info("Step 1: Processing JSON and generating chunks")
    metadata_docs, content_chunks = process_all_jsons(json_dir)
    
    if not content_chunks:
        logger.error("No chunks were generated. Aborting mission.")
        return
    
    logger.info("Step 2: Enhancing chunks for figures and tables")
    aggregator = ContentAggregator()
    enriched_chunks = aggregator.centralize_section_context_for_element(content_chunks)
    
    # Embeddings used to gen vectors
    logger.info("Step 3: Vector convertion")
    vector_processor = VectorProcessor()
    chunks_with_embeddings = vector_processor.add_vectors_to_chunks(enriched_chunks)
    metadata_with_embeddings = vector_processor.add_vectors_to_chunks(metadata_docs)

    # Adjust schemas with proper embbedding dimension
    mapping_path_shema_pdf_content = PROJECT_ROOT / "src" / "config" / "opensearch_chunk_search_schema.json"
    mapping_path_shema_abstract_pdf = PROJECT_ROOT / "src" / "config" / "opensearch_metadata_search_schema.json"
    content_mapping = load_opensearch_mapping(mapping_path_shema_pdf_content)
    metadata_mapping = load_opensearch_mapping(mapping_path_shema_abstract_pdf)
    content_mapping["mappings"]["properties"]["vector"]["dimension"] = vector_processor.dimension
    metadata_mapping["mappings"]["properties"]["vector"]["dimension"] = vector_processor.dimension
    
    logger.info("Etapa 4: Conecting to OpenSearch...")
    os_client = OpenSearchClient()
    
    logger.info("Step 5: Creating Indexes in OpenSearch")
    
    os_client.create_index(METADATA_INDEX, metadata_mapping)
    os_client.create_index(CONTENT_INDEX, content_mapping)
    
    logger.info("Etapa 6: Inserting dosc into OpenSearch...")
    if metadata_docs:
        inserted_metadata = os_client.bulk_insert(METADATA_INDEX, metadata_with_embeddings)
        logger.info(f"Metadados inseridos: {inserted_metadata}")
    
    inserted_chunks = os_client.bulk_insert(CONTENT_INDEX, chunks_with_embeddings)
    logger.info(f"Chunks inseridos: {inserted_chunks}")
    
    logger.info("=== Ingestão Concluída com Sucesso ===")


if __name__ == "__main__":
    main()
