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
    """Cliente reutilizável para operações no OpenSearch."""
    
    def __init__(self):
        self.client = self._create_client()
    
    def _create_client(self) -> OpenSearch:
        """Cria conexão com OpenSearch."""
        return OpenSearch(
            hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
            http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
            use_ssl=OPENSEARCH_USE_SSL,
            verify_certs=False,
            ssl_show_warn=False,
        )
    
    def create_index(self, index_name: str, body: Dict[str, Any]) -> bool:
        """
        Cria um índice no OpenSearch.
        
        Args:
            index_name: Nome do índice
            body: Configuração do índice (mappings, settings)
        
        Returns:
            True se criado com sucesso
        """
        try:
            if self.client.indices.exists(index=index_name):
                logger.info(f"Índice '{index_name}' já existe")
                return True
            
            self.client.indices.create(index=index_name, body=body)
            logger.info(f"Índice '{index_name}' criado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao criar índice '{index_name}': {e}")
            return False
    
    def bulk_insert(self, index_name: str, documents: List[Dict[str, Any]]) -> int:
        """
        Insere documentos em lote no OpenSearch.
        
        Args:
            index_name: Nome do índice
            documents: Lista de documentos para inserir
        
        Returns:
            Número de documentos inseridos com sucesso
        """
        from opensearchpy.helpers import bulk
        
        actions = [
            {
                "_index": index_name,
                "_source": doc
            }
            for doc in documents
        ]
        
        try:
            success, failed = bulk(self.client, actions, raise_on_error=False)
            logger.info(f"Bulk insert: {success} sucessos, {len(failed)} falhas")
            return success
        except Exception as e:
            logger.error(f"Erro no bulk insert: {e}")
            return 0
    
    def search(self, index_name: str, query: Dict[str, Any], size: int = 10) -> List[Dict[str, Any]]:
        """
        Busca documentos no OpenSearch.
        
        Args:
            index_name: Nome do índice
            query: Query DSL do OpenSearch
            size: Número máximo de resultados
        
        Returns:
            Lista de documentos encontrados
        """
        try:
            response = self.client.search(index=index_name, body=query, size=size)
            hits = response.get('hits', {}).get('hits', [])
            return [hit['_source'] for hit in hits]
        except Exception as e:
            logger.error(f"Erro na busca: {e}")
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
