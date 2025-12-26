import streamlit as st
import os
from rag_logic_gemini import get_rag_chain
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()

# Get API Key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PDF_PATH = "completedata.pdf"

# --- Streamlit App Setup ---
st.set_page_config(page_title="Gemini RAG Chatbot", page_icon="📚")
st.title("📚 Gemini RAG Chatbot")
st.caption(f"Powered by Gemini API and knowledge from **{PDF_PATH}**.")

# Initialize session state for chat history and RAG chain
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

# --- Sidebar for API Key Input ---
with st.sidebar:
    st.header("Configuration")
    
    # Check if API key is already set in environment
    if GEMINI_API_KEY:
        st.success("Gemini API Key loaded from environment.")
    else:
        # Allow user to input API key if not found
        GEMINI_API_KEY = st.text_input("Enter your Gemini API Key:", type="password")
        if GEMINI_API_KEY:
            os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
            st.success("API Key set for this session.")
        else:
            st.warning("Please enter your Gemini API Key to start the RAG Chatbot.")

# --- Initialization Logic ---
def initialize_rag_chain():
    """Initializes the RAG chain and stores it in session state."""
    if not GEMINI_API_KEY:
        st.error("Cannot initialize: Gemini API Key is missing.")
        return False
        
    if not os.path.exists(PDF_PATH):
        st.error(f"Cannot initialize: PDF file '{PDF_PATH}' not found.")
        return False

    try:
        with st.spinner("Initializing RAG chain... This may take a moment to process the PDF."):
            st.session_state.rag_chain = get_rag_chain(PDF_PATH, GEMINI_API_KEY)
        st.success("RAG Chain initialized successfully!")
        return True
    except Exception as e:
        st.error(f"Error during RAG chain initialization: {e}")
        st.session_state.rag_chain = None
        return False

# Lazy initialization: only initialize when a question is asked or if it's the first run
if st.session_state.rag_chain is None and GEMINI_API_KEY:
    initialize_rag_chain()

# --- Display Chat Messages ---
if not st.session_state.messages:
    # Show welcome message if no chat history
    welcome_message = "👋 Hello! I'm your RAG Chatbot. I can answer questions based on the content of the **completedata.pdf** file. Ask me anything about it!"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and Response Generation ---
if prompt := st.chat_input("Ask a question about the PDF..."):
    # 1. Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate response
    if st.session_state.rag_chain:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Use the RAG chain to get the answer
                with st.spinner("Thinking..."):
                    answer = st.session_state.rag_chain.invoke(prompt)
                
                full_response = answer
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                full_response = f"An error occurred while generating the response: {e}"
                message_placeholder.markdown(full_response)

            # 3. Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        # Display error if RAG chain is not initialized
        with st.chat_message("assistant"):
            st.markdown("Cannot generate response. The RAG system is not initialized. Please check your API key and ensure the PDF file is present.")

# Rerun to display all messages (Streamlit handles this automatically with st.chat_input, but good practice)
# st.rerun() # Not needed with st.chat_input in the latest Streamlit versions
