# Weaviate Chatbot with LlamaIndex

A chatbot application that uses LlamaIndex to connect to a local Weaviate vector database, enabling semantic search and conversational AI over your knowledge base.

## Features

- 🤖 Conversational AI powered by OpenAI GPT models
- 🔍 Semantic search using Weaviate vector database
- 📄 Support for multiple document formats
- 🌐 Web interface built with Streamlit
- 💻 Command-line interface for testing
- 🔄 Real-time document indexing

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- OpenAI API key

## Setup

### 1. Clone and Install Dependencies

```bash
# Install dependencies using Poetry
poetry install

# Or using pip
pip install -r requirements.txt
```

### 2. Start Weaviate

```bash
# Start Weaviate using Docker Compose
docker-compose up -d

# Check if Weaviate is running
curl http://localhost:8080/v1/meta
```

### 3. Configure Environment

Copy the `.env` file and add your OpenAI API key:

```bash
# Edit .env file
OPENAI_API_KEY=your_openai_api_key_here
WEAVIATE_URL=http://localhost:8080
```

## Quick Start with Makefile

We provide a comprehensive Makefile for easy project management:

### 🚀 One-Command Setup

```bash
# Complete setup with sample data (recommended for first-time users)
make quick-start

# Or full setup with ALL sample data files
make full-setup
```

### 📋 Available Make Commands

```bash
# Show all available commands
make help

# Environment setup
make install           # Install Python dependencies
make setup            # Install deps + start Weaviate
make start            # Start Weaviate only
make stop             # Stop Weaviate
make restart          # Restart Weaviate

# Data management
make add-sample-data              # Add basic sample data
make add-all-sample-data         # Add ALL sample data files
make add-document FILE=<file>    # Add specific document
make clear-data                  # Clear knowledge base

# Applications
make chat             # Start CLI chatbot
make streamlit        # Start web interface

# Monitoring & debugging
make status           # Check service status
make logs             # View Weaviate logs
make health-check     # Comprehensive health check
make test-connection  # Test Weaviate connection

# Cleanup
make clean            # Remove containers and volumes
```

### 🔧 Development Workflow

```bash
# 1. First time setup
make quick-start

# 2. Start developing
make chat           # Test CLI interface
make streamlit      # Test web interface

# 3. Add your own documents
make add-document FILE=my_document.txt

# 4. Monitor and debug
make logs           # View logs
make health-check   # Check system status
```

## Manual Usage

### Command Line Interface

```bash
# Run the CLI chatbot
python chatbot.py
```

Commands:
- Type any message to chat
- `add_file <path>` - Add a text file to knowledge base
- `clear` - Clear the knowledge base
- `quit` - Exit the application

### Web Interface

```bash
# Start the Streamlit web interface
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser.

### Adding Knowledge

You can add knowledge to the chatbot in several ways:

1. **Upload files** through the web interface
2. **Add text directly** through the web interface
3. **Use CLI commands** to add files

Supported file formats: `.txt`, `.md`, `.py`, `.js`, `.html`, `.css`

## Example Usage

### 1. Add Sample Data

```python
from chatbot import WeaviateChatbot

# Initialize chatbot
bot = WeaviateChatbot()

# Add the sample data file
bot.add_text_file("sample_data.txt")

# Ask questions
response = bot.chat("What is Weaviate?")
print(response)
```

### 2. Web Interface

1. Open the Streamlit app
2. Click "Initialize Chatbot"
3. Upload your documents using the sidebar
4. Start chatting!

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   LlamaIndex    │    │    Weaviate     │
│   Frontend      │◄──►│   Framework     │◄──►│   Vector DB     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │ (Embeddings +   │
                       │     Chat)       │
                       └─────────────────┘
```

## Configuration

### Weaviate Settings

The chatbot connects to Weaviate at `http://localhost:8080` by default. You can modify this in the `.env` file or when initializing the `WeaviateChatbot` class.

### LlamaIndex Settings

- **Embedding Model**: `text-embedding-ada-002`
- **Chat Model**: `gpt-3.5-turbo` (configurable)
- **Chunk Size**: 512 tokens
- **Chunk Overlap**: 20 tokens

### Customization

```python
# Custom initialization
chatbot = WeaviateChatbot(
    weaviate_url="http://localhost:8080",
    index_name="MyKnowledgeBase",
    model_name="gpt-4"
)
```

## Troubleshooting

### Common Issues

1. **"Cannot connect to Weaviate"**
   - Make sure Weaviate is running: `docker-compose up -d`
   - Check the URL in your `.env` file

2. **"OPENAI_API_KEY not found"**
   - Add your OpenAI API key to the `.env` file
   - Make sure the `.env` file is in the same directory

3. **Import errors**
   - Install dependencies: `poetry install` or `pip install -r requirements.txt`

### Logs

The application logs important events. Check the console output for debugging information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
