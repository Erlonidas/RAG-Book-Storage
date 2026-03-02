# RAG Book Challenge

> ⚠️ **Project Under Construction** - This project is currently in active development.

RAG (Retrieval-Augmented Generation) system for processing and searching academic documents using OpenSearch and LangGraph.

## 📋 Overview

This project implements an autonomous agent architecture with semantic routing and hybrid search (Map-Reduce) for intelligent querying of PDF documents.

**Tech Stack:**
- **LangGraph**: Agent orchestration
- **OpenSearch**: Vector database and hybrid search
- **Dolphin**: PDF content extraction (runs on Google Colab)
- **Docker**: Local infrastructure

## 🏗️ Project Structure

```
rag_book_challenge/
├── data/
│   ├── raw/                    # Dolphin JSONs, original PDFs, figures
│   └── processed/              # Processed data for ingestion
├── src/
│   ├── config/                 # Global configurations
│   ├── services/               # Connectors (OpenSearch, LLM)
│   ├── ingestion/              # Ingestion pipeline (ETL)
│   │   └── processors/         # Chunk builder, metadata extractor
│   ├── rag/                    # RAG system with LangGraph (coming soon)
│   └── utils/                  # Utility functions
├── docs/                       # Documentation and guides
├── test/                       # Tests and experimental notebooks
├── docker-compose.yml          # OpenSearch configuration
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Google Account (for Colab PDF extraction)

### 2. Installation

```bash
# Clone the repository
git clone <repo-url>
cd rag_book_challenge

# Create virtual environment
python -m venv _venv
source _venv/bin/activate  # Windows: _venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 3. Start OpenSearch

```bash
docker-compose up -d
```

Access:
- OpenSearch: http://localhost:9200
- Dashboards: http://localhost:5601

### 4. Process PDFs (Google Colab)

Follow the guide in `docs/GUIA_COLAB_DOLPHIN.md` to:
1. Extract PDF content using Dolphin
2. Download generated JSONs
3. Place them in `data/raw/json_extraction/`

### 5. Run Ingestion (Coming Soon)

```bash
python -m src.ingestion.main
```

## 📚 Documentation

- **[PLANO_DE_ACAO.md](docs/PLANO_DE_ACAO.md)**: Complete project roadmap (Portuguese)
- **[GUIA_COLAB_DOLPHIN.md](docs/GUIA_COLAB_DOLPHIN.md)**: PDF extraction tutorial (Portuguese)

## 🔧 Configuration

### Environment Variables (.env)

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

# Anthropic (optional)
ANTHROPIC_API_KEY=your_key_here
```

## 🎯 Development Roadmap

### ✅ Phase 1: Data Factory (Colab) - COMPLETED
- [x] Dolphin setup on Colab
- [x] PDF extraction pipeline
- [x] Structured JSON generation

### 🚧 Phase 2: Chunk Preparation for OpenSearch - IN PROGRESS
- [x] Docker Compose for OpenSearch
- [x] Chunk builder processor
- [x] Metadata extractor
- [ ] Index creation scripts (metadata + content)
- [ ] Bulk ingestion to OpenSearch
- [ ] Embedding generation

### 📋 Phase 3: RAG Agent Workflow (LangGraph) - PLANNED
- [ ] State definition
- [ ] Router node (decomposer)
- [ ] Worker nodes (retrievers)
- [ ] Aggregator node (synthesizer)
- [ ] End-to-end query pipeline

## 🧪 Testing

```bash
# Run test notebooks
jupyter notebook test/random_test/
```

## 📦 Main Dependencies

- `opensearch-py`: OpenSearch client
- `langgraph`: Agent orchestration
- `langchain`: LLM framework
- `sentence-transformers`: Embeddings
- `markdownify`: HTML → Markdown conversion

## 🤝 Contributing

1. Fork the project
2. Create a branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

[To be defined]

