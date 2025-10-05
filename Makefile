.PHONY: clean help ollama cadvisor backup-volumes wipe

# Show help
help:
	@echo "Available targets:"
	@echo "  clean          - Remove untracked files, directories recursively"
	@echo "  ollama         - Start Ollama container"
	@echo "  cadvisor       - Start cAdvisor container"
	@echo "  backup-volumes - Backup all Docker volumes to ./backups/"
	@echo "  wipe           - Stop and remove all containers (keeps volumes and networks)"

# Clean up
clean:
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned .pytest_cache directories"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned __pycache__ directories"

# Start docker containers
ollama:
	@echo "Starting Ollama container..."
	@scripts/ollama.sh

cadvisor:
	@echo "Starting cAdvisor container..."
	@scripts/cadvisor.sh

# Backup docker volumes
backup-volumes:
	@echo "Creating backup directory..."
	@mkdir -p backups
	@echo "Loading environment variables..."
	@if [ -f .env ]; then \
		export $$(grep -v '^#' .env | xargs); \
		TIMESTAMP=$$(date +%Y%m%d_%H%M%S); \
		echo "Backing up volumes with timestamp: $$TIMESTAMP"; \
		echo ""; \
		echo "Backing up Ollama volume..."; \
		docker run --rm -v $${VOLUME_OLLAMA}:/data -v $$(pwd)/backups:/backup alpine tar czf /backup/ollama-volume_$$TIMESTAMP.tar.gz -C /data . && \
		echo "✓ Ollama backup: backups/ollama-volume_$$TIMESTAMP.tar.gz"; \
		echo ""; \
		echo "Backing up Weaviate volume..."; \
		docker run --rm -v $${VOLUME_WEAVIATE_DATA}:/data -v $$(pwd)/backups:/backup alpine tar czf /backup/weaviate-data-$${REPLICA_ID}_$$TIMESTAMP.tar.gz -C /data . && \
		echo "✓ Weaviate backup: backups/weaviate-data-$${REPLICA_ID}_$$TIMESTAMP.tar.gz"; \
		echo ""; \
		echo "Backing up Neo4j data volume..."; \
		docker run --rm -v $${VOLUME_NEO4J_DATA}:/data -v $$(pwd)/backups:/backup alpine tar czf /backup/neo4j-data-$${REPLICA_ID}_$$TIMESTAMP.tar.gz -C /data . && \
		echo "✓ Neo4j data backup: backups/neo4j-data-$${REPLICA_ID}_$$TIMESTAMP.tar.gz"; \
		echo ""; \
		echo "Backing up Neo4j logs volume..."; \
		docker run --rm -v $${VOLUME_NEO4J_LOGS}:/data -v $$(pwd)/backups:/backup alpine tar czf /backup/neo4j-logs-$${REPLICA_ID}_$$TIMESTAMP.tar.gz -C /data . && \
		echo "✓ Neo4j logs backup: backups/neo4j-logs-$${REPLICA_ID}_$$TIMESTAMP.tar.gz"; \
		echo ""; \
		echo "Backing up Neo4j import volume..."; \
		docker run --rm -v $${VOLUME_NEO4J_IMPORT}:/data -v $$(pwd)/backups:/backup alpine tar czf /backup/neo4j-import-$${REPLICA_ID}_$$TIMESTAMP.tar.gz -C /data . && \
		echo "✓ Neo4j import backup: backups/neo4j-import-$${REPLICA_ID}_$$TIMESTAMP.tar.gz"; \
		echo ""; \
		echo "All volumes backed up successfully to ./backups/"; \
	else \
		echo "Error: .env file not found. Please create it from .env.template"; \
		exit 1; \
	fi

# Wipe out all docker containers (keeps volumes and networks)
wipe:
	@echo "Stopping all running containers..."
	@docker ps -q | xargs -r docker stop || true
	@echo "Removing all containers (volumes and networks preserved)..."
	@docker ps -a -q | xargs -r docker rm || true
	@echo "✓ All containers removed. Volumes and networks are preserved."
	@echo ""
	@echo "To view remaining volumes: docker volume ls"
	@echo "To view remaining networks: docker network ls"