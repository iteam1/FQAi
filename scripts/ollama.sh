#!/bin/bash

set -e

# --- Configuration ---
# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found. Please create one from .env.template."
    exit 1
fi

# Models to download
EMBEDDING_MODELS=("embeddinggemma:latest" "nomic-embed-text:latest" "bge-m3:latest")
COMPLETION_MODELS=("gemma3:4b" "deepseek-r1:1.5b")

# --- Helper Functions ---
echo_green() {
    echo -e "\033[0;32m$1\033[0m"
}

echo_yellow() {
    echo -e "\033[1;33m$1\033[0m"
}

# --- Main Logic ---

# 1. Check and create Docker network
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    echo_yellow "Network '$NETWORK_NAME' not found. Creating..."
    docker network create "$NETWORK_NAME"
    echo_green "Network '$NETWORK_NAME' created."
else
    echo_green "Network '$NETWORK_NAME' already exists."
fi

# 2. Check and start Ollama container
if docker ps -a --format '{{.Names}}' | grep -q "^${OLLAMA_CONTAINER_NAME}$"; then
    if ! docker ps --format '{{.Names}}' | grep -q "^${OLLAMA_CONTAINER_NAME}$"; then
        echo_yellow "Ollama container '${OLLAMA_CONTAINER_NAME}' exists but is stopped. Starting..."
        docker start "${OLLAMA_CONTAINER_NAME}"
        echo_green "Ollama container started."
    else
        echo_green "Ollama container '${OLLAMA_CONTAINER_NAME}' is already running."
    fi
else
    echo_yellow "Ollama container '${OLLAMA_CONTAINER_NAME}' not found. Creating and starting..."
    docker run -d \
      --name "${OLLAMA_CONTAINER_NAME}" \
      --network "$NETWORK_NAME" \
      -p "${OLLAMA_PORT:-11434}:11434" \
      -e OLLAMA_NUM_PARALLEL="${OLLAMA_NUM_PARALLEL:-1}" \
      -v "${VOLUME_OLLAMA:-ollama-volume}:/root/.ollama" \
      --restart unless-stopped \
      --memory="${OLLAMA_MEMORY:-8g}" \
      --cpus="${OLLAMA_CPUS:-4}" \
      --health-cmd="ollama list >/dev/null 2>&1 || exit 1" \
      --health-interval=30s \
      --health-timeout=10s \
      --health-retries=3 \
      ollama/ollama

    echo_green "Ollama container created and started."
fi

# 3. Wait for Ollama to be healthy
echo_yellow "Waiting for Ollama service to become healthy..."
while [ "$(docker inspect -f '{{.State.Health.Status}}' "${OLLAMA_CONTAINER_NAME}")" != "healthy" ]; do
    sleep 5
done
echo_green "Ollama service is healthy."

# 4. Download models
ALL_MODELS=("${EMBEDDING_MODELS[@]}" "${COMPLETION_MODELS[@]}")

echo_yellow "Checking and downloading required models..."
for model in "${ALL_MODELS[@]}"; do
    if ! docker exec "${OLLAMA_CONTAINER_NAME}" ollama list | grep -q "$model"; then
        echo_yellow "Downloading model: $model..."
        docker exec "${OLLAMA_CONTAINER_NAME}" ollama pull "$model"
        echo_green "Model $model downloaded."
    else
        echo_green "Model $model already exists."
    fi
done

echo_green "Ollama setup complete!"