# =============================
# 📚 PDF Chat Bot with LangChain
# =============================

import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="🤖 PDF Chat Bot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================
# 🔧 Helper Functions
# =============================

def initialize_components():
    """Initialize embeddings and LLM"""
    # Get API key from environment or user input
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = st.sidebar.text_input("🔑 Enter your Google API Key:", type="password")
        if not api_key:
            st.sidebar.error("Please provide your Google API Key!")
            st.sidebar.markdown("[Get API Key here](https://makersuite.google.com/app/apikey)")
            return None, None
    
    # Initialize embeddings (HuggingFace - free)
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        st.sidebar.success("✅ Embeddings loaded!")
    except Exception as e:
        st.sidebar.error(f"Error loading embeddings: {str(e)}")
        return None, None
    
    # Initialize LLM (Gemini)
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0,
            api_key=api_key
        )
        st.sidebar.success("✅ Gemini AI connected!")
        return embeddings, llm
    except Exception as e:
        st.sidebar.error(f"Error connecting to Gemini: {str(e)}")
        return embeddings, None

def process_pdf(uploaded_file, embeddings):
    """Process uploaded PDF and create vector store"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Load PDF with LangChain
        loader = PyPDFLoader(tmp_file_path)
        documents = loader.load()
        
        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = splitter.split_documents(documents)
        
        # Create vector store
        vectorstore = FAISS.from_documents(splits, embeddings)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return vectorstore, len(splits)
    
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None, 0

def format_docs(docs):
    """Format documents for the prompt"""
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain(vectorstore, llm):
    """Create the RAG chain"""
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful document analysis assistant.
    Answer the question based ONLY on the provided context.
    If the answer is not found in the context, say "The information is not available in the uploaded document."
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:""")
    
    # Build RAG chain
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# =============================
# 🚀 Main Application
# =============================

def main():
    # Header
    st.title("🤖 PDF Chat Bot")
    st.markdown("*Upload a PDF and chat with your documents using AI!*")
    
    # Initialize session state
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "pdf_processed" not in st.session_state:
        st.session_state.pdf_processed = False
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Setup")
        
        # Initialize components
        embeddings, llm = initialize_components()
        
        if embeddings and llm:
            st.divider()
            
            # File upload
            st.subheader("Upload PDF")
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type="pdf",
                help="Upload a PDF document to start chatting!"
            )
            
            if uploaded_file is not None:
                if st.button("🔄 Process PDF", type="primary", use_container_width=True):
                    with st.spinner("Processing your PDF... This may take a few moments."):
                        vectorstore, num_chunks = process_pdf(uploaded_file, embeddings)
                        
                        if vectorstore:
                            st.session_state.rag_chain = create_rag_chain(vectorstore, llm)
                            st.session_state.pdf_processed = True
                            st.session_state.chat_history = []  # Clear previous chat
                            
                            st.success(f"✅ PDF processed successfully!")
                            st.info(f"📄 Created {num_chunks} text chunks")
                        else:
                            st.error("❌ Failed to process PDF")
            
            # Status
            st.divider()
            st.subheader("Status")
            if st.session_state.pdf_processed:
                st.success("🟢 Ready to chat!")
            else:
                st.warning("🟡 Upload and process a PDF first")
        
        # Instructions
        st.divider()
        st.subheader("💡 How to use")
        st.markdown("""
        1. **Setup**: Enter your Google API Key if needed
        2. **Upload**: Choose a PDF file
        3. **Process**: Click 'Process PDF' button  
        4. **Chat**: Ask questions about your document
        5. **Explore**: Try different questions!
        """)
        
        st.markdown("[🔑 Get Google API Key](https://makersuite.google.com/app/apikey)")
    
    # Main content area
    if not st.session_state.pdf_processed:
        # Welcome message
        st.info("👋 Welcome! Please upload and process a PDF to start chatting.")
        
        # Sample questions for demonstration
        st.subheader("💡 Example questions you can ask:")
        sample_questions = [
            "What is this document about?",
            "Summarize the main points",
            "What are the key findings?",
            "Who are the main stakeholders mentioned?",
            "What are the important dates or deadlines?"
        ]
        
        for i, question in enumerate(sample_questions, 1):
            st.write(f"**{i}.** {question}")
            
    else:
        # Chat interface
        st.subheader("💬 Chat with your PDF")
        
        # Display chat history
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.container():
                st.markdown(f"**You:** {question}")
                st.markdown(f"**Bot:** {answer}")
                st.divider()
        
        # Question input
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_question = st.text_input(
                    "Ask a question about your PDF:",
                    placeholder="What is this document about?",
                    key="user_input"
                )
            
            with col2:
                ask_button = st.button("Ask", type="primary", use_container_width=True)
            
            # Clear chat button
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
        
        # Process question
        if ask_button and user_question and st.session_state.rag_chain:
            with st.spinner("Thinking... 🤔"):
                try:
                    response = st.session_state.rag_chain.invoke(user_question)
                    
                    # Add to chat history
                    st.session_state.chat_history.append((user_question, response))
                    
                    # Clear input and rerun to show new message
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()