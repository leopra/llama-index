# Makefile for Weaviate Chatbot Project

install: ## Install Python dependencies using Poetry
	poetry install

start: ## Start Weaviate using Docker Compose
	docker compose up -d

chat: ## Start interactive chat session
	poetry run python chatbot.py
