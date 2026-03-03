import json
from pathlib import Path
from typing import List, Dict, Any

from src.config import RAW_DATA_DIR, METADATA_INDEX, CONTENT_INDEX, setup_logger
from src.services import OpenSearchClient
from src.ingestion.processors import (
    processar_json_dolphin,
    extract_article_metadata,
)

logger = setup_logger(__name__)


def load_dolphin_json(json_path: Path) -> Dict[str, Any]:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def process_all_jsons(json_dir: Path) -> tuple[List[Dict], List[Dict]]:
    """
    Processa todos os JSONs do Dolphin em um diretório.
    
    Returns:
        Tupla (metadados, chunks_conteudo)
    """
    all_metadata = []
    all_chunks = []
    
    json_files = list(json_dir.glob("*.json"))
    logger.info(f"Encontrados {len(json_files)} arquivos JSON")
    
    for json_file in json_files:
        book_id = json_file.stem
        logger.info(f"Processando: {book_id}")
        
        dolphin_json = load_dolphin_json(json_file)
        
        # Extrai metadados
        metadata = extract_article_metadata(dolphin_json, book_id)
        if metadata:
            all_metadata.append(metadata)
        
        # Gera chunks
        chunks = processar_json_dolphin(dolphin_json, book_id)
        all_chunks.extend(chunks)
    
    logger.info(f"Total: {len(all_metadata)} metadados, {len(all_chunks)} chunks")
    return all_metadata, all_chunks


def main():
    """Função principal de ingestão."""
    logger.info("=== Iniciando Ingestão ===")
    
    # Diretório com JSONs do Dolphin
    json_dir = RAW_DATA_DIR / "json_extraction"
    
    if not json_dir.exists():
        logger.error(f"Diretório não encontrado: {json_dir}")
        return
    
    # Processa JSONs
    metadata_docs, content_chunks = process_all_jsons(json_dir)
    
    # Conecta ao OpenSearch
    os_client = OpenSearchClient()
    
    # TODO: Criar índices com mappings apropriados
    # os_client.create_index(METADATA_INDEX, metadata_mapping)
    # os_client.create_index(CONTENT_INDEX, content_mapping)
    
    # TODO: Inserir documentos
    # os_client.bulk_insert(METADATA_INDEX, metadata_docs)
    # os_client.bulk_insert(CONTENT_INDEX, content_chunks)
    
    logger.info("=== Ingestão Concluída ===")


if __name__ == "__main__":
    main()
