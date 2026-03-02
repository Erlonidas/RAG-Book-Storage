# RAG Book Challenge

Sistema RAG (Retrieval-Augmented Generation) para processamento e busca em documentos acadêmicos usando OpenSearch e LangGraph.

## 📋 Visão Geral

Este projeto implementa uma arquitetura de agentes autônomos com roteamento semântico e busca híbrida (Map-Reduce) para consulta inteligente em documentos PDF.

**Stack Tecnológica:**
- **LangGraph**: Orquestração de agentes
- **OpenSearch**: Banco de dados vetorial e busca híbrida
- **Dolphin**: Extração de conteúdo de PDFs (executado no Google Colab)
- **Docker**: Infraestrutura local

## 🏗️ Estrutura do Projeto

```
rag_book_challenge/
├── data/
│   ├── raw/                    # JSONs do Dolphin, PDFs originais, figuras
│   └── processed/              # Dados processados para ingestão
├── src/
│   ├── config/                 # Configurações globais
│   ├── services/               # Conectores (OpenSearch, LLM)
│   ├── ingestion/              # Pipeline de ingestão (ETL)
│   │   └── processors/         # Chunk builder, metadata extractor
│   ├── rag/                    # Sistema RAG com LangGraph
│   └── utils/                  # Funções utilitárias
├── docs/                       # Documentação e guias
├── test/                       # Testes e notebooks experimentais
├── docker-compose.yml          # Configuração OpenSearch
├── requirements.txt            # Dependências Python
└── .env                        # Variáveis de ambiente
```

## 🚀 Início Rápido

### 1. Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Conta Google (para usar Colab na extração de PDFs)

### 2. Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd rag_book_challenge

# Crie ambiente virtual
python -m venv _venv
source _venv/bin/activate  # Windows: _venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais
```

### 3. Subir OpenSearch

```bash
docker-compose up -d
```

Acesse:
- OpenSearch: http://localhost:9200
- Dashboards: http://localhost:5601

### 4. Processar PDFs (Google Colab)

Siga o guia em `docs/GUIA_COLAB_DOLPHIN.md` para:
1. Extrair conteúdo dos PDFs usando Dolphin
2. Baixar JSONs gerados
3. Colocar em `data/raw/json_extraction/`

### 5. Executar Ingestão

```bash
python -m src.ingestion.main
```

## 📚 Documentação

- **[PLANO_DE_ACAO.md](docs/PLANO_DE_ACAO.md)**: Roadmap completo do projeto
- **[GUIA_COLAB_DOLPHIN.md](docs/GUIA_COLAB_DOLPHIN.md)**: Tutorial de extração de PDFs

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# OpenSearch
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_USER=admin
OPENSEARCH_INITIAL_ADMIN_PASSWORD=my_password
OPENSEARCH_USE_SSL=true

# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini

# Anthropic (opcional)
ANTHROPIC_API_KEY=your_key_here
```

## 🎯 Roadmap

### ✅ Fase 1: Fábrica de Dados (Colab)
- [x] Setup Dolphin no Colab
- [x] Pipeline de extração de PDFs
- [x] Geração de JSONs estruturados

### 🚧 Fase 2: Infraestrutura Local
- [x] Docker Compose para OpenSearch
- [ ] Scripts de indexação
- [ ] Criação de índices (metadata + content)

### 📋 Fase 3: Sistema RAG (LangGraph)
- [ ] Definição de estados
- [ ] Nó Router (decomposer)
- [ ] Nós Worker (buscadores)
- [ ] Nó Aggregator (sintetizador)

## 🧪 Testes

```bash
# Executar notebooks de teste
jupyter notebook test/random_test/
```

## 📦 Dependências Principais

- `opensearch-py`: Cliente OpenSearch
- `langgraph`: Orquestração de agentes
- `langchain`: Framework LLM
- `sentence-transformers`: Embeddings
- `markdownify`: Conversão HTML → Markdown

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

[Adicionar licença]

## 👥 Autores

[Adicionar autores]
