#!/bin/bash

# Weaviate Chatbot Setup Script
# Alternative to Makefile for systems without make

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for Weaviate to be ready
wait_for_weaviate() {
    print_status "Waiting for Weaviate to be ready..."
    timeout 60 bash -c 'until curl -f http://localhost:8080/v1/meta >/dev/null 2>&1; do echo "Waiting for Weaviate..."; sleep 2; done' || {
        print_error "Weaviate failed to start"
        exit 1
    }
    print_status "Weaviate is ready!"
}

# Function to show usage
show_usage() {
    echo "Weaviate Chatbot Setup Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start              Start Weaviate"
    echo "  stop               Stop Weaviate"
    echo "  setup              Complete setup (install + start + wait)"
    echo "  install            Install dependencies"
    echo "  add-sample-data    Add sample data"
    echo "  add-all-data       Add all sample data files"
    echo "  chat               Start CLI chatbot"
    echo "  streamlit          Start Streamlit app"
    echo "  status             Check status"
    echo "  clean              Clean up containers"
    echo "  quick-start        Complete quick start"
    echo "  help               Show this help"
    echo ""
}

# Main script logic
case "${1:-help}" in
    "start")
        print_status "Starting Weaviate..."
        docker-compose up -d
        print_status "Weaviate started. Access it at http://localhost:8080"
        ;;
    
    "stop")
        print_warning "Stopping Weaviate..."
        docker-compose down
        ;;
    
    "setup")
        print_status "Setting up environment..."
        
        # Check prerequisites
        if ! command_exists docker; then
            print_error "Docker is not installed"
            exit 1
        fi
        
        if ! command_exists poetry; then
            print_warning "Poetry not found, trying pip..."
            pip install -r requirements.txt
        else
            poetry install
        fi
        
        # Start services
        docker-compose up -d
        wait_for_weaviate
        ;;
    
    "install")
        print_status "Installing dependencies..."
        if command_exists poetry; then
            poetry install
        else
            pip install -r requirements.txt
        fi
        ;;
    
    "add-sample-data")
        print_status "Adding sample data..."
        if command_exists poetry; then
            poetry run python -c "from chatbot import WeaviateChatbot; bot = WeaviateChatbot(); bot.add_text_file('sample_data.txt'); print('Sample data added successfully!')"
        else
            python -c "from chatbot import WeaviateChatbot; bot = WeaviateChatbot(); bot.add_text_file('sample_data.txt'); print('Sample data added successfully!')"
        fi
        ;;
    
    "add-all-data")
        print_status "Adding all sample data files..."
        for file in sample_data*.txt; do
            print_status "Adding $file..."
            if command_exists poetry; then
                poetry run python -c "from chatbot import WeaviateChatbot; bot = WeaviateChatbot(); bot.add_text_file('$file'); print('Added $file')"
            else
                python -c "from chatbot import WeaviateChatbot; bot = WeaviateChatbot(); bot.add_text_file('$file'); print('Added $file')"
            fi
        done
        print_status "All sample data added successfully!"
        ;;
    
    "chat")
        print_status "Starting chat session..."
        if command_exists poetry; then
            poetry run python chatbot.py
        else
            python chatbot.py
        fi
        ;;
    
    "streamlit")
        print_status "Starting Streamlit app..."
        if command_exists poetry; then
            poetry run streamlit run streamlit_app.py
        else
            streamlit run streamlit_app.py
        fi
        ;;
    
    "status")
        print_status "Service Status:"
        docker-compose ps
        echo ""
        print_status "Weaviate Health Check:"
        if curl -f http://localhost:8080/v1/meta >/dev/null 2>&1; then
            print_status "✓ Weaviate is running"
        else
            print_error "✗ Weaviate is not responding"
        fi
        ;;
    
    "clean")
        print_warning "Cleaning up..."
        docker-compose down -v
        docker system prune -f
        print_status "Cleanup complete!"
        ;;
    
    "quick-start")
        print_status "Quick start: Setting up everything..."
        
        # Run setup
        $0 setup
        
        # Add sample data
        $0 add-sample-data
        
        print_status "Quick start complete! You can now run:"
        print_status "  $0 chat        - Start CLI chat"
        print_status "  $0 streamlit   - Start web interface"
        ;;
    
    "help"|*)
        show_usage
        ;;
esac
