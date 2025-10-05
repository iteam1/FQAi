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
│         │  :6061   │  │  :6062   │   │  :6063   │            │
│         │  :50051  │  │  :50052  │   │  :50053  │            │
│         ├──────────┤  ├──────────┤   ├──────────┤            │
│         │ Neo4j-1  │  │ Neo4j-2  │   │ Neo4j-3  │            │
│         │  :7474   │  │  :7475   │   │  :7476   │            │
│         │  :7687   │  │  :7688   │   │  :7689   │            │
│         └──────────┘  └──────────┘   └──────────┘            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Quickstart

**Prerequisites**

- Docker `docker --version`
- Docker Compose `docker compose --version` or `docker-compose --version`
- Virtual environment `(.venv)` (Python 3.10)
- Ollama image (`ollama/ollama:latest`)
- Weaviate image (`semitechnologies/weaviate:latest`)
- Neo4j 5.20 image (`neo4j:5.20`)

- Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

or 

```bash
uv venv .venv -p 3.10
source .venv/bin/activate
uv pip install -r requirements.txt
```

- Configure environment variables:

```bash
cp .env.template .env
```

Edit the `.env` file to set the environment variables

For general configuration:

```bash
REPLICA_ID=<replica_id>
BACKEND_PORT=<backend_port> # default: 8000, 8001, 8002, ...

```

For Weaviate:

```bash
WEAVIATE_CONTAINER_NAME="weaviate-${REPLICA_ID}"
WEAVIATE_HTTP_PORT=<weaviate_http_port> # default: 8080, 8081, 8082, ...
WEAVIATE_METRICS_PORT=<weaviate_metrics_port> # default: 6060, 6061, 6062, ...
WEAVIATE_GRPC_PORT=<weaviate_grpc_port> # default: 50051, 50052, 50053, ...
VOLUME_WEAVIATE_DATA="weaviate-data-${REPLICA_ID}"

```

For Neo4j:

```bash
NEO4J_CONTAINER_NAME="neo4j-${REPLICA_ID}"
NEO4J_HTTP_PORT=<neo4j_http_port> # default: 7474, 7475, 7476, ...
NEO4J_BOLT_PORT=<neo4j_bolt_port> # default: 7687, 7688, 7689, ...
VOLUME_NEO4J_DATA="neo4j-data-${REPLICA_ID}"
VOLUME_NEO4J_LOGS="neo4j-logs-${REPLICA_ID}"
VOLUME_NEO4J_IMPORT="neo4j-import-${REPLICA_ID}"
```

Load environment variables:

```bash
source .env
```

- Create `fqai-network`: `docker network create fqai-network`

- Give permissions to scripts: `chmod +x scripts/*.sh`

- Start ollama (*required*): `make ollama`

- Start cadvisor (*optional*): `make cadvisor`

- Start weaviate and neo4j (*required*): `docker compose up -d` or `docker-compose up -d`

```bash
# Make sure .env exists
cp .env.template .env && source .env

# Start services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Check health
docker ps
```

If you want to stop the services, safely use `docker compose down` or `docker-compose down` do not use `-v` flag


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