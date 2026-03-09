from opensearchpy import OpenSearch
from typing import Optional, List, Dict, Any
from src.config import (
    OPENSEARCH_HOST,
    OPENSEARCH_PORT,
    OPENSEARCH_USER,
    OPENSEARCH_PASSWORD,
    OPENSEARCH_USE_SSL,
    setup_logger,
)

logger = setup_logger(__name__)


class OpenSearchClient:
    
    def __init__(self):
        self.client = self._create_client()
        self._validate_coinnection()
    

    def _create_client(self) -> OpenSearch:
        return OpenSearch(
            hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
            http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
            use_ssl=OPENSEARCH_USE_SSL,
            verify_certs=False,
            ssl_show_warn=False,
        )
    

    def _validate_connection(self) -> None:
        try:
            info = self.client.info()
            logger.info(f"Connection with OpenSearch has been achieved. Version: {info['version']['number']}")
        except Exception as e:
            logger.critical(f"Fail to connect to OpenSearch with credentials -> {OPENSEARCH_HOST}:{OPENSEARCH_PORT} → {e}")
            raise


    def create_index(self, index_name: str, body: Dict[str, Any]) -> bool:
        """
        Args:
            index_name: index name
            body: Chunks' schema (mappings, settings)
        
        Returns:
            return True if the index is already created or successfully created a new one.
        """
        try:
            if self.client.indices.exists(index=index_name):
                logger.info(f"Index '{index_name}' already exists")
                return True
            
            self.client.indices.create(index=index_name, body=body)
            logger.info(f"Index '{index_name}' successfully created")
            return True
        except Exception as e:
            logger.error(f"Error when trying to creating index '{index_name}': {e}")
            return False


    def bulk_insert(self, index_name: str, documents: List[Dict[str, Any]]) -> int:
        """
        Insert package block documents in parallel
        
        Args:
            index_name: Index's name
            documents: List of documents to insert
        
        Returns:
            Number of documents inserted
        """      
        try:
            data = list()
            for doc in documents:
                data.append({"index": {"_index":index_name}})
                data.append(doc)
            self.client.bulk(body=data)
            self.client.indices.refresh(index=index_name)
            logger.info(f"{len(documents)} documents inserted into index: '{index_name}'")
            return len(documents)

        except Exception as e:
            logger.error(f"Error during bulk insert: {e}")
            return 0
    

    def search(self, index_name: str,
                query_vector: List[float], book_id: str,
                k: int = 7, min_score: float = 0.4
                ) -> List[Dict]:
                
                """
                Busca chunks por similaridade semântica, ordenados por posição no documento.

                Args:
                    index_name: Nome do índice
                    query_vector: Vetor da pergunta gerado pelo embedding
                    book_id: Filtro pelo livro/paper específico
                    k: Quantidade de chunks mais similares a retornar
                    min_score: Score mínimo de similaridade

                Returns:
                    Lista de chunks ordenados por page_number e reading_order
                """
                try:
                    search_body = {
                        "min_score": min_score,
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        "knn": {
                                            "vetor": {
                                                "vector": query_vector,
                                                "k": k
                                            }
                                        }
                                    }
                                ],
                                "filter": [
                                    {"term": {"book_id": book_id}}
                                ]
                            }
                        },
                        "sort": [
                            {"page_number": {"order": "asc"}},
                            {"reading_order": {"order": "asc"}}
                        ],
                        "size": k
                    }

                    response = self.client.search(index=index_name, body=search_body)
                    hits = response["hits"]["hits"]

                    logger.info(f"{len(hits)} chunks encontrados no índice '{index_name}' para book_id='{book_id}'")
                    return hits

                except Exception as e:
                    logger.error(f"Erro durante a busca no índice '{index_name}': {e}")
                    return []
    

    def delete_index(self, index_name: str) -> bool:
        """Deleta um índice."""
        try:
            if self.client.indices.exists(index=index_name):
                self.client.indices.delete(index=index_name)
                logger.info(f"Índice '{index_name}' deletado")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao deletar índice: {e}")
            return False
