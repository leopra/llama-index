# Makefile for Weaviate Chatbot Project

.PHONY: help install start stop status clean setup add-documents add-all-sample-data chat streamlit logs restart

install: ## Install Python dependencies using Poetry
	poetry install

start: ## Start Weaviate using Docker Compose
	docker compose up -d

chat: ## Start interactive chat session
	poetry run python chatbot.py
