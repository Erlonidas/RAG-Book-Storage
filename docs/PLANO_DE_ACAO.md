# 🗺️ Planejamento do Projeto: Agente RAG com OpenSearch e LangGraph

**Objetivo:** Implementar arquitetura de Agentes Autônomos com Roteamento Semântico e Busca Híbrida (Map-Reduce).
**Stack:** LangGraph (Orquestração), OpenSearch (Vector/Hybrid DB), Google Colab (ETL/OCR), Docker (Infra Local).

---

## 🏭 Fase 1: Fábrica de Dados (Google Colab)
*Objetivo: Processar PDFs usando GPU na nuvem para não sobrecarregar a máquina local.*

- [ ] **Setup do Ambiente (T4 GPU)**
    - Instalar bibliotecas: `transformers`, `accelerate`, `bitsandbytes`, `pypdf`.
    - Configurar modelo VLM (ex: Dolphin-Mistral, Qwen-VL ou LLaVA) para OCR inteligente.

- [ ] **Pipeline de Ingestão (ETL)**
    - [ ] Script para iterar páginas do PDF como imagens.
    - [ ] Prompt do VLM: *"Transcreva para Markdown mantendo tabelas e estrutura."*
    - [ ] Limpeza de texto e conversão para formato estruturado.

- [ ] **Enriquecimento de Metadados**
    - [ ] Gerar resumo curto de cada livro (para o Router usar).
    - [ ] Extrair: `Título`, `Autor`, `Sinopse`.
    - [ ] Chunking do conteúdo (500-1000 tokens) mantendo referência do `book_id`.

- [ ] **Exportação**
    - [ ] Baixar `books_metadata.json` (Catálogo).
    - [ ] Baixar `books_content.json` (Vetores/Texto).

---

## 🐳 Fase 2: Infraestrutura Local (Docker)
*Objetivo: Subir o OpenSearch otimizado para 16GB RAM.*

- [ ] **Docker Compose (`docker-compose.yml`)**
    ```yaml
    version: '3'
    services:
      opensearch-node:
        image: opensearchproject/opensearch:latest
        container_name: opensearch-node
        environment:
          - discovery.type=single-node
          - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g" # Trava Heap em 1GB
        ports:
          - 9200:9200
        volumes:
          - opensearch-data:/usr/share/opensearch/data
    volumes:
      opensearch-data:
    ```

- [ ] **Script de Indexação (Python)**
    - [ ] Conectar em `localhost:9200`.
    - [ ] Criar índice **`metadata-index`**:
        - Configurar busca híbrida (Keyword + Vetor leve).
    - [ ] Criar índice **`content-index`**:
        - Configurar busca densa (KNN Vector) + Full Text Search (BM25).
    - [ ] Ingestão (`bulk_insert`) dos JSONs baixados do Colab.

---

## 🧠 Fase 3: Lógica do Agente (LangGraph)
*Objetivo: Implementar padrão Map-Reduce com `Send` API.*

- [ ] **Definição de Estado (`State`)**
    ```python
    from typing import Annotated, List, TypedDict
    import operator

    class AgentState(TypedDict):
        question: str
        # operator.add garante append na lista em paralelo
        context_chunks: Annotated[List[str], operator.add] 
        final_answer: str
    ```

- [ ] **Nó 1: Router (O Maestro)**
    - [ ] Tool: `search_metadata(query)` -> Busca no índice `metadata-index`.
    - [ ] LLM com `StructuredOutput` (Pydantic): Retorna lista de `{book_id, specific_query}`.
    - [ ] Lógica Condicional: 
        - Se lista vazia -> Fim.
        - Se lista ok -> Dispara `Send("worker_node", input)` para cada livro.

- [ ] **Nó 2: Worker (O Buscador)**
    - [ ] Recebe input isolado: `{book_id, query}`.
    - [ ] Busca no OpenSearch (`content-index`) com filtro: `filter: { term: { book_id: ... } }`.
    - [ ] (Opcional) Re-ranking/Resumo rápido com LLM local.
    - [ ] Retorna string formatada para o estado global.

- [ ] **Nó 3: Aggregator (O Sintetizador)**
    - [ ] Recebe `context_chunks` (lista de respostas dos Workers).
    - [ ] Prompt: *"Consolide as informações dos livros X e Y para responder à pergunta Z."*

---

## ✅ Checklist de Validação

- [ ] PDFs processados e JSONs gerados no Colab.
- [ ] Container OpenSearch rodando estável (sem estourar RAM).
- [ ] Índices populados e consultáveis via `curl`.
- [ ] Fluxo LangGraph completando o ciclo (Pergunta -> Router -> Busca Paralela -> Resposta).