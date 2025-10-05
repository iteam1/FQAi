.PHONY: clean help

# Show help
help:
	@echo "Available targets:"
	@echo "  clean   - Remove untracked files, directories recursively"

# Clean up
clean:
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned .pytest_cache directories"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned __pycache__ directories"

# Start docker containers

# Backup docker volumes