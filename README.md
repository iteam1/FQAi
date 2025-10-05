# FQAi

```
┌──────────────────────────────────────────────────────────────┐
│           Shared Docker Network: fqa-network                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                   ┌─────────────────┐                        │
│                   │  Ollama (shared)│                        │
│                   │    :11434       │                        │
│                   └────────┬────────┘                        │
│                            │                                 │
│              ┌─────────────┼─────────────┐                   │
│              │             │             │                   │
│         ┌────▼─────┐  ┌────▼─────┐   ┌───▼──────┐            │
│         │   AI-1   │  │   AI-2   │   │   AI-3   │            │
│         ├──────────┤  ├──────────┤   ├──────────┤            │
│         │ FastAPI-1│  │ FastAPI-2│   │ FastAPI-3│            │
│         │  :8001   │  │  :8002   │   │  :8003   │            │
│         ├──────────┤  ├──────────┤   ├──────────┤            │
│         │Weaviate-1│  │Weaviate-2│   │Weaviate-3│            │
│         │  :8081   │  │  :8082   │   │  :8083   │            │
│         ├──────────┤  ├──────────┤   ├──────────┤            │
│         │ Neo4j-1  │  │ Neo4j-2  │   │ Neo4j-3  │            │
│         │  :7475   │  │  :7476   │   │  :7477   │            │
│         │  :7688   │  │  :7689   │   │  :7690   │            │
│         └──────────┘  └──────────┘   └──────────┘            │
└──────────────────────────────────────────────────────────────┘
```

## Quickstart

- Create a virtual environment and activate it

```bash
python -m venv .venv
source .venv/bin/activate
```

- Install dependencies

```bash
pip install -r requirements.txt
```

or 

```bash
uv venv .venv -p 3.10
source .venv/bin/activate
uv pip install -r requirements.txt
```

- Configure environment variables

```bash
cp .env.template .env
```

Edit the `.env` file to set the environment variables

For Weaviate:

```bash

```

For Neo4j:

```bash

```

- Create `fqai-network`: `docker network create fqai-network`

- Start ollama (*required*): `make ollama`

- Start cadvisor (*optional*): `make cadvisor`

- Start weaviate and neo4j (*required*): `docker compose up -d` or `docker-compose up -d`

## Targets
1. Initialize the codebase
2. Complete the flexible configuration
3. Simple RAG pipeline with Ollama (embedding model, generative model, reranker model)
4. Complete API server with FastAPI (`/health`, `/query`, `/query/stream`, `/collections`, etc.)

## General Process
1. Gather the data
2. Chunk the data
3. Vectorize the data
4. Extract Entities & Relationships
5. Generate the graph
6. Perform the retrieval
7. Generate the answer


## Codebase Structure

```
/
├── /docs
|
├── /backend (FastAPI application)
|
├── /tools (CLI tools)
|
├── /src (Core Logic)
|  ├── /pipeline (Data Processing Pipeline)
|  |  ├── SimpleRAGPipeline
|  |  ├── SimpleGraphRAGPipeline
|  |  |...
|  |  
|  ├── /preprocess
|  |
|  ├── /inference
|  |
|  |...
|
├── /scripts (Build scripts)
|
├── /tests (Unit tests)
|
├── requirements.txt
├── .env.template
├── .gitignore
├── .Makefile
└── README.md
```

## References

- [Ollama](https://ollama.com/)
- [Weaviate](https://weaviate.io/)
- [Neo4j](https://neo4j.com/)