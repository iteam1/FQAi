# FQAi

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

## Capabilities

- **Contextual Retrieval**: Retrieve relevant context to provide for LLM-powered answers.
- **Querying Graph Data with Natural Language**: Use LLMs to translate user questions into Cypher queries, enabling natural language access to graph data.
- **Automated Reasoning**: Combine the reasoning abilities of LLMs with the structured relationships in Graph Database for more accurate and insightful responses.
- **Conversational AI**: Build chatbots and assistants that can answer questions about complex, connected data stored in Graph Database.
- **Knowledge Graph Construction**: Automatically construct knowledge graphs from unstructured data using LLMs, and store them in Graph Database for further analysis.

## References

- [Ollama](https://ollama.com/)
- [Weaviate](https://weaviate.io/)
- [Neo4j](https://neo4j.com/)
- [Code Graph RAG](https://github.com/vitali87/code-graph-rag)