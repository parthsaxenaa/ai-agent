import os
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def format_docs(docs):
    """Formats the retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain_gemini(pdf_path: str, api_key: str):
    """
    Creates a RAG chain using Google Gemini models for both embeddings and LLM,
    using ChromaDB and UnstructuredPDFLoader for better portability.
    
    Args:
        pdf_path: Path to the PDF file.
        api_key: The Gemini API key.
        
    Returns:
        A runnable RAG chain object.
    """
    
    # 1. Initialize Gemini components
    # Using a fast embedding model
    embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004", api_key=api_key)
    
    # Using a fast LLM for quick responses
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, api_key=api_key)
    
    # 2. Vector Store Setup
    persist_directory = "chroma_db_gemini"
    
    # Check if vector store exists in cache
    if os.path.exists(persist_directory):
        # Load from cache
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
        # Build vector store
        # Load the PDF using UnstructuredPDFLoader for better compatibility
        loader = UnstructuredPDFLoader(pdf_path)
        docs = loader.load()

        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # Create embeddings and vector store with persistence
        vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=embeddings, 
            persist_directory=persist_directory
        )
        vectorstore.persist()

    # 3. Create the retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Reduced k for speed

    # 4. Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """You are an AI assistant specialized in answering questions based *only* on the provided context from the PDF document.
            
            Instructions:
            1. Analyze the user's question and the provided context.
            2. If the context contains the answer, provide a clear, concise, and direct answer.
            3. **CRITICAL:** If the context does not contain the answer, you MUST respond with: "I apologize, but I can only answer questions based on the information in the provided document, and I could not find the answer there."
            4. Do not use any external knowledge.
            
            Context from PDF:
            {context}"""),
            ("human", "{question}"),
        ]
    )

    # 5. Create the RAG chain using LCEL
    def get_question(x):
        if isinstance(x, str):
            return x
        elif isinstance(x, dict):
            return x.get("question", str(x))
        return str(x)
    
    rag_chain = (
        RunnablePassthrough.assign(
            question=lambda x: get_question(x),
            context=lambda x: format_docs(retriever.invoke(get_question(x)))
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# Simple wrapper to match the expected interface for Streamlit
class RAGChainWrapper:
    def __init__(self, chain):
        self.chain = chain
    
    def invoke(self, input_text):
        # The chain can now handle both string input and dict input
        return self.chain.invoke(input_text)
        
def get_rag_chain(pdf_path: str, api_key: str):
    """Public function to get the wrapped RAG chain."""
    chain = get_rag_chain_gemini(pdf_path, api_key)
    return RAGChainWrapper(chain)
