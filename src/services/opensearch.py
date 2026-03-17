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
        self._validate_connection()
    

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
    

    def semantic_search(self, index_name: str,
           query_vector: List[float], book_id: str,
           query_text: str = None, k: int = 7, 
           min_score: float = 0.4, sorted_output=True
           ) -> List[Dict]:
        """
        Search chunks by semantic or hybrid (semantic + BM25) similarity.

        Args:
            query_text: Optional text for hybrid search (BM25 + vector)
            k: Number of chunks to return
            min_score: Minimum similarity score threshold
            sorted_output: If True, sorts by page_number then reading_order.
                           If False, returns by relevance score (OpenSearch default).

        Returns:
            List of matching chunks
        """
        try:
            should_clauses = [
                {
                    "knn": {
                        "vector": {
                            "vector": query_vector,
                            "k": k
                        }
                    }
                }
            ]

            if query_text:
                should_clauses.append({
                    "match": {
                        "content": query_text
                    }
                })

            search_body = {
                "min_score": min_score,
                "size": k,
                "track_scores": True,
                "query": {
                    "bool": {
                        "should": should_clauses,
                        "minimum_should_match": 1,
                        "filter": [
                            {"term": {"book_id": book_id}}
                        ]
                    }
                }
            }

            if sorted_output:
                search_body["sort"] = [
                    {"page_number": {"order": "asc"}},
                    {"reading_order": {"order": "asc"}}
                ]

            response = self.client.search(index=index_name, body=search_body)
            hits = response["hits"]["hits"]

            modo = "hybrid" if query_text else "semantic"
            logger.info(f"{len(hits)} chunks found at index '{index_name}' | mode: {modo} | book_id: '{book_id}'")
            return hits

        except Exception as e:
            logger.error(f"Error during search at index '{index_name}': {e}")
            return []


    def collect_all(self, index_name, pdf_name=None, exclude_fields=None):
        """
        Retrieve all chunks from an specific index. You can filter the chunks by pdf_name.
        Use 'exclude_fields' (list of strings) to prevent downloading heavy fields like vectors.
        """
        try:
            if pdf_name:
                query_body = {
                    "query": {
                        "term": {
                            "book_id": pdf_name
                        }
                    }
                }
            else:
                query_body = {
                    "query":{
                        "match_all": {}
                    }
                }
            
            if exclude_fields:
                query_body["_source"] = {
                    "excludes": exclude_fields
                }

            retrieval = self.client.search(index=index_name, body=query_body, size=10000)
            hits = retrieval['hits']['hits']

            logger.info(f"{len(hits)} chunks retrieved from index '{index_name}'" + (f" filtered by pdf_name='{pdf_name}'" if pdf_name else ""))
            return hits
            
        except Exception as e:
            logger.error(f"Error retrieving chunks from index '{index_name}': {e}")
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
