"""
Streamlit Web Interface for Weaviate Chatbot
"""
import streamlit as st
import os
from dotenv import load_dotenv
from chatbot import WeaviateChatbot

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Weaviate Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initialized" not in st.session_state:
    st.session_state.initialized = False


def initialize_chatbot():
    """Initialize the chatbot with error handling"""
    try:
        chatbot = WeaviateChatbot()
        st.session_state.chatbot = chatbot
        st.session_state.initialized = True
        st.success("✅ Chatbot initialized successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize chatbot: {e}")
        st.error("Make sure:")
        st.error("1. Weaviate is running (docker-compose up)")
        st.error("2. OPENAI_API_KEY is set in .env file")
        return False


# Sidebar
with st.sidebar:
    st.title("🤖 Weaviate Chatbot")
    st.markdown("---")
    
    # Initialize chatbot button
    if st.button("Initialize Chatbot", disabled=st.session_state.initialized):
        initialize_chatbot()
    
    if st.session_state.initialized:
        st.success("Chatbot Ready!")
    
    st.markdown("---")
    
    # File upload section
    st.subheader("📄 Add Knowledge")
    uploaded_file = st.file_uploader(
        "Upload a text file",
        type=['txt', 'md', 'py', 'js', 'html', 'css']
    )
    
    if uploaded_file is not None and st.session_state.chatbot:
        if st.button("Add File to Knowledge Base"):
            try:
                # Save uploaded file temporarily
                temp_path = f"/tmp/{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Add to chatbot
                st.session_state.chatbot.add_text_file(temp_path)
                st.success(f"✅ Added {uploaded_file.name} to knowledge base!")
                
                # Clean up
                os.remove(temp_path)
                
            except Exception as e:
                st.error(f"❌ Error adding file: {e}")
    
    # Manual text input
    st.subheader("📝 Add Text")
    manual_text = st.text_area("Enter text to add to knowledge base:")
    if st.button("Add Text") and manual_text and st.session_state.chatbot:
        try:
            st.session_state.chatbot.add_documents([manual_text])
            st.success("✅ Text added to knowledge base!")
        except Exception as e:
            st.error(f"❌ Error adding text: {e}")
    
    st.markdown("---")
    
    # Clear chat history
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    # Clear knowledge base
    if st.button("🗑️ Clear Knowledge Base") and st.session_state.chatbot:
        try:
            st.session_state.chatbot.clear_knowledge_base()
            st.success("✅ Knowledge base cleared!")
        except Exception as e:
            st.error(f"❌ Error clearing knowledge base: {e}")

# Main chat interface
st.title("💬 Chat with your Weaviate Knowledge Base")

if not st.session_state.initialized:
    st.info("👈 Please initialize the chatbot using the sidebar first.")
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your knowledge base..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chatbot.chat(prompt)
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except Exception as e:
                    error_msg = f"❌ Error: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )

# Footer
st.markdown("---")
st.markdown(
    "🔧 Built with [LlamaIndex](https://llamaindex.ai/) and "
    "[Weaviate](https://weaviate.io/)"
)
