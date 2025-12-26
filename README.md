# Vellicate Agent: RAG Chatbot for Students

This guide provides step-by-step instructions on how to set up and run the **Vellicate Agent**, a Retrieval-Augmented Generation (RAG) chatbot built with LangChain, the Gemini API, and Streamlit. This agent is designed to answer student questions based on the provided PDF document, "complete data.pdf" (Requirements Engineering Fundamentals).

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1.  **Python 3.9+**: Download and install Python from [python.org](https://www.python.org/downloads/).
2.  **Visual Studio Code (VS Code)**: Download and install VS Code from [code.visualstudio.com](https://code.visualstudio.com/).
3.  **Gemini API Key**: Obtain a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Step-by-Step Setup in VS Code

Follow these steps to get your Vellicate Agent running:

### Step 1: Create the Project Directory

Open your terminal or command prompt and create a new folder for your project.

```bash
mkdir vellicate_agent
cd vellicate_agent
```

### Step 2: Place the PDF Document

Copy the PDF file you provided, **`complete data.pdf`**, into the newly created `vellicate_agent` folder. The application is hardcoded to look for this file name.

### Step 3: Create the Code Files

Inside the `vellicate_agent` folder, create two new files: `rag_logic.py` and `app.py`.

#### **`rag_logic.py`** (The Core RAG Logic)

This file contains the functions to load the PDF, create vector embeddings using Gemini, and set up the LangChain RAG chain.

```python
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

def get_rag_chain(pdf_path, api_key):
    # 1. Load the PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # 2. Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 3. Create embeddings and vector store
    # Using a robust embedding model from Gemini
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

    # 4. Create the retriever
    retriever = vectorstore.as_retriever()

    # 5. Create the LLM
    # Using a fast and capable model for chat
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

    # 6. Create the prompt template
    system_prompt = (
        "You are 'Vellicate Agent', an AI assistant for students. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, say that you don't know. "
        "Keep the answer concise and helpful for a student."
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # 7. Create the chains
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain
```

#### **`app.py`** (The Streamlit Interface)

This file creates the web interface, handles the user's API key input, manages the chat history, and calls the RAG logic.

```python
import streamlit as st
import os
from rag_logic import get_rag_chain
from dotenv import load_dotenv

# Load environment variables if .env exists (optional, but good practice)
load_dotenv()

st.set_page_config(page_title="Vellicate Agent", page_icon="🎓")

st.title("🎓 Vellicate Agent")
st.markdown("### Your AI Study Assistant for Requirements Engineering")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    # User inputs the API key directly into the app
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
    
    # Path to the PDF
    pdf_path = "complete data.pdf"
    
    if not os.path.exists(pdf_path):
        st.error(f"PDF file '{pdf_path}' not found in the directory.")

# Initialize session state for chat history and RAG chain
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

# Button to initialize the agent
if st.sidebar.button("Initialize Agent"):
    if not api_key:
        st.error("Please enter your Gemini API Key.")
    elif not os.path.exists(pdf_path):
        st.error("PDF file not found.")
    else:
        with st.spinner("Initializing Vellicate Agent... This may take a minute."):
            try:
                # The get_rag_chain function handles the heavy lifting of loading and indexing the PDF
                st.session_state.rag_chain = get_rag_chain(pdf_path, api_key)
                st.success("Vellicate Agent is ready! You can now ask questions.")
            except Exception as e:
                st.error(f"Error initializing agent: {str(e)}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about the study guide..."):
    if st.session_state.rag_chain is None:
        st.warning("Please initialize the agent first by providing the API key and clicking 'Initialize Agent'.")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Invoke the RAG chain
                    response = st.session_state.rag_chain.invoke({"input": prompt})
                    answer = response["answer"]
                    st.markdown(answer)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
```

### Step 4: Install Dependencies

Open your terminal in the `vellicate_agent` directory and run the following command to install all necessary Python packages:

```bash
pip install streamlit langchain langchain-google-genai google-generativeai pypdf faiss-cpu python-dotenv
```

### Step 5: Run the Streamlit Application

Execute the following command in your terminal to start the Streamlit web application:

```bash
streamlit run app.py
```

Your default web browser will automatically open to the application (usually at `http://localhost:8501`).

### Step 6: Use the Vellicate Agent

1.  In the Streamlit application, paste your **Gemini API Key** into the sidebar input field.
2.  Click the **"Initialize Agent"** button. This process will load the PDF, split it into chunks, create vector embeddings, and store them in a local index. This may take a minute depending on the size of the PDF.
3.  Once you see the "Vellicate Agent is ready!" message, you can start asking questions in the chat box. The agent will use the content of your PDF to provide relevant answers.
