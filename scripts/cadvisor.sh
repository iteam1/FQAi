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

# 2. Check and start Cadvisor container
if docker ps -a --format '{{.Names}}' | grep -q "^${CADVISOR_CONTAINER_NAME}$"; then
    if ! docker ps --format '{{.Names}}' | grep -q "^${CADVISOR_CONTAINER_NAME}$"; then
        echo_yellow "cAdvisor container '${CADVISOR_CONTAINER_NAME}' exists but is stopped. Starting..."
        docker start "${CADVISOR_CONTAINER_NAME}"
        echo_green "cAdvisor container started."
    else
        echo_green "cAdvisor container '${CADVISOR_CONTAINER_NAME}' is already running."
    fi
else
    echo_yellow "cAdvisor container '${CADVISOR_CONTAINER_NAME}' not found. Creating and starting..."
    docker run -d \
      --name="${CADVISOR_CONTAINER_NAME}" \
      --network="$NETWORK_NAME" \
      -p "${CADVISOR_PORT:-8081}:8080" \
      --volume=/:/rootfs:ro \
      --volume=/var/run:/var/run:rw \
      --volume=/sys:/sys:ro \
      --volume=/var/lib/docker/:/var/lib/docker:ro \
      --restart unless-stopped \
      --privileged \
      --device=/dev/kmsg \
      gcr.io/cadvisor/cadvisor:latest

    echo_green "cAdvisor container created and started."
fi

echo_green "cAdvisor setup complete!"
