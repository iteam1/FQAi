"""FastAPI application for backend."""

import os
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Backend API",
    description="RAG + GraphRAG",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Backend API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "replica_id": os.getenv("REPLICA_ID"),
        "services": {
            "api": "up",
        },
    }


@app.get("/config")
async def get_config() -> Dict[str, Any]:
    """Get current configuration."""
    return {
        "replica_id": os.getenv("REPLICA_ID"),
        "backend_port": os.getenv("BACKEND_PORT"),
        "weaviate": {
            "host": os.getenv("WEAVIATE_HOST"),
            "http_port": os.getenv("WEAVIATE_HTTP_PORT"),
            "grpc_port": os.getenv("WEAVIATE_GRPC_PORT"),
        },
        "neo4j": {
            "host": os.getenv("NEO4J_HOST"),
            "http_port": os.getenv("NEO4J_HTTP_PORT"),
            "bolt_port": os.getenv("NEO4J_BOLT_PORT"),
        },
        "ollama": {
            "host": os.getenv("OLLAMA_HOST"),
            "port": os.getenv("OLLAMA_PORT"),
        },
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("BACKEND_PORT"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )
