#!/bin/bash

echo "Starting Weaviate and vLLM embedding server..."

# Start the services
docker-compose up -d

echo "Waiting for services to be ready..."

# Wait for Weaviate
echo "Checking Weaviate..."
until curl -f http://localhost:8080/v1/.well-known/ready; do
    echo "Waiting for Weaviate to be ready..."
    sleep 5
done

# Wait for vLLM embedding server
echo "Checking vLLM embedding server..."
until curl -f http://localhost:8000/health; do
    echo "Waiting for vLLM embedding server to be ready..."
    sleep 5
done

echo "All services are ready!"
echo "Weaviate: http://localhost:8080"
echo "vLLM Embedding Server: http://localhost:8000"
echo ""
echo "You can now run the chatbot with: python chatbot.py"
