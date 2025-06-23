#!/usr/bin/env python3
"""
Test script to verify the vLLM embedding server is working correctly
"""

import requests
import json


def test_vllm_embeddings():
    """Test the vLLM embedding server"""
    url = "http://localhost:8000/v1/embeddings"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer dummy-key"
    }
    
    data = {
        "model": "bge-small-en-v1.5",
        "input": "Hello, this is a test sentence for embeddings."
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        if "data" in result and len(result["data"]) > 0:
            embedding = result["data"][0]["embedding"]
            print("✅ vLLM embedding server is working!")
            print(f"   Model: {result['data'][0]['object']}")
            print(f"   Embedding dimension: {len(embedding)}")
            print(f"   First 5 values: {embedding[:5]}")
            return True
        else:
            print("❌ Unexpected response format")
            print(json.dumps(result, indent=2))
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to vLLM server: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_weaviate():
    """Test Weaviate connection"""
    try:
        response = requests.get("http://localhost:8080/v1/.well-known/ready")
        response.raise_for_status()
        print("✅ Weaviate is ready!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to Weaviate: {e}")
        return False


if __name__ == "__main__":
    print("Testing services...")
    print("-" * 40)
    
    weaviate_ok = test_weaviate()
    vllm_ok = test_vllm_embeddings()
    
    print("-" * 40)
    if weaviate_ok and vllm_ok:
        print("🎉 All services are working correctly!")
        print("You can now use the chatbot with vLLM embeddings.")
    else:
        print("⚠️  Some services are not working. Please check the logs.")
        print("Run: docker-compose logs to see detailed logs.")
