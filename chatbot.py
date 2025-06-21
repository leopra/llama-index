import os
import logging
from typing import List, Optional
from dotenv import load_dotenv

import weaviate
from llama_index.core import (
    VectorStoreIndex,
    Document,
    Settings,
    StorageContext,
)
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from transformers import AutoTokenizer

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeaviateChatbot:

    def __init__(self,
                 weaviate_url: str = "http://localhost:8080",
                 index_name: str = "ChatbotKnowledge",
                 model_name: str = "gpt-4o-mini",
                 openai_base_url: Optional[str] = None,
                 use_local_embeddings: bool = True,
                 embedding_model_name: str = "BAAI/bge-small-en-v1.5"):
        self.weaviate_url = weaviate_url
        self.index_name = index_name
        self.model_name = model_name
        self.use_local_embeddings = use_local_embeddings
        self.embedding_model_name = embedding_model_name
        self.openai_base_url = openai_base_url or os.getenv("BASE_URL")
        
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables"
            )

        llm_kwargs = {"model": model_name, "temperature": 0.1}
        
        if self.openai_base_url:
            llm_kwargs["api_base"] = self.openai_base_url
        
        Settings.llm = OpenAI(**llm_kwargs)
        
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=self.embedding_model_name,
            trust_remote_code=False,
            device="cpu"
        )
        
        Settings.tokenizer = AutoTokenizer.from_pretrained(
            self.embedding_model_name
        )
        
        # Initialize Weaviate client and vector store
        self._setup_weaviate()
        self._setup_index()
    
    def _setup_weaviate(self):
        """Setup Weaviate client and vector store"""
        try:
            # Connect to Weaviate
            self.weaviate_client = weaviate.Client(url=self.weaviate_url)
            
            # Test connection
            if self.weaviate_client.is_ready():
                logger.info(
                    f"Successfully connected to Weaviate at "
                    f"{self.weaviate_url}"
                )
            else:
                raise ConnectionError("Could not connect to Weaviate")
            
            # Initialize vector store
            self.vector_store = WeaviateVectorStore(
                weaviate_client=self.weaviate_client,
                index_name=self.index_name
            )
            
        except Exception as e:
            logger.error(f"Failed to setup Weaviate: {e}")
            raise
    
    def _setup_index(self):
        """Setup or load the vector index"""
        try:
            # Create storage context
            storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )

            # Try to load existing index or create new one
            try:
                self.index = VectorStoreIndex.from_vector_store(
                    vector_store=self.vector_store,
                    storage_context=storage_context
                )
                logger.info(f"Loaded existing index: {self.index_name}")
            except Exception:
                # Create new empty index
                self.index = VectorStoreIndex(
                    nodes=[],
                    storage_context=storage_context
                )
                logger.info(f"Created new index: {self.index_name}")
            
            # Create query engine
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=3,
                response_mode="tree_summarize"
            )
            
        except Exception as e:
            logger.error(f"Failed to setup index: {e}")
            raise
    
    def add_documents(self, documents: List[str],
                      titles: Optional[List[str]] = None):
        """
        Add documents to the knowledge base
        
        Args:
            documents: List of document texts
            titles: Optional list of document titles
        """
        try:
            # Create Document objects
            docs = []
            for i, doc_text in enumerate(documents):
                doc = Document(
                    text=doc_text,
                )
                docs.append(doc)
            
            # Add to index
            for doc in docs:
                self.index.insert(doc)
            
            logger.info(f"Added {len(docs)} documents to the knowledge base")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def add_text_file(self, file_path: str):
        """Add content from a text file to the knowledge base"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            doc = Document(
                text=content
            )
            
            self.index.insert(doc)
            logger.info(f"Added file {file_path} to knowledge base")
            
        except Exception as e:
            logger.error(f"Failed to add file {file_path}: {e}")
            raise
    
    def chat(self, message: str) -> str:
        """
        Send a message to the chatbot and get a response
        
        Args:
            message: User's message
            
        Returns:
            Bot's response
        """
        try:
            response = self.query_engine.query(message)
            return str(response)
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return f"I'm sorry, I encountered an error: {e}"
    
    def clear_knowledge_base(self):
        """Clear all documents from the knowledge base"""
        try:
            # Delete the class in Weaviate to clear all data
            self.weaviate_client.schema.delete_class(self.index_name)
            logger.info(f"Cleared knowledge base: {self.index_name}")
            
            # Reinitialize the index
            self._setup_index()
            
        except Exception as e:
            logger.error(f"Failed to clear knowledge base: {e}")
            raise
    
    def get_schema_info(self):
        """Get information about the Weaviate schema"""
        try:
            schema = self.weaviate_client.schema.get()
            return schema
        except Exception as e:
            logger.error(f"Failed to get schema: {e}")
            return None


def main():
    """Simple CLI interface for testing the chatbot"""
    try:
        # Initialize chatbot with local embeddings by default
        base_url = os.getenv("BASE_URL")
        chatbot = WeaviateChatbot(
            openai_base_url=base_url,
            embedding_model_name="BAAI/bge-small-en-v1.5"
        )
        print("-" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                chatbot.clear_knowledge_base()
                print("Knowledge base cleared!")
            elif user_input.lower().startswith('add_file '):
                file_path = user_input[9:].strip()
                try:
                    chatbot.add_text_file(file_path)
                    print(f"Added file: {file_path}")
                except Exception as e:
                    print(f"Error adding file: {e}")
            elif user_input:
                response = chatbot.chat(user_input)
                print(f"\n Bot: {response}")
        
        print("\nGoodbye!")
        
    except Exception as e:
        print(f"Error initializing chatbot: {e}")


if __name__ == "__main__":
    main()
