# FQAi

## Quickstart


## Targets
1. Initialize the codebase
2. Complete the flexible configuration
3. Simple RAG pipeline with Ollama (embedding model, generative model, reranker model)
4. Complete API server with FastAPI (`/health`, `/query`, `/query/stream`, etc.)


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