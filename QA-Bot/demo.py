# =============================
# 📚 Simple Demo Script
#Git Changes 001
# =============================

"""
Simple demo script to test the core RAG functionality
without Streamlit interface.
"""

import os
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

def format_docs(docs):
    """Format documents for the prompt"""
    return "\n\n".join(doc.page_content for doc in docs)

def demo_pdf_chat(pdf_path, question):
    """Demo function to test PDF chat functionality"""
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ Please set GOOGLE_API_KEY in your .env file")
        return
    
    try:
        print("🔄 Loading PDF...")
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"✅ Loaded {len(documents)} pages")
        
        # Split documents
        print("🔄 Splitting documents...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = splitter.split_documents(documents)
        print(f"✅ Created {len(splits)} chunks")
        
        # Create embeddings
        print("🔄 Loading embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        print("✅ Embeddings loaded")
        
        # Create vector store
        print("🔄 Creating vector store...")
        vectorstore = FAISS.from_documents(splits, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        print("✅ Vector store created")
        
        # Initialize LLM
        print("🔄 Connecting to Gemini AI...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            api_key=api_key
        )
        print("✅ Connected to Gemini AI")
        
        # Create prompt
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful document analysis assistant.
        Answer the question based ONLY on the provided context.
        If the answer is not found in the context, say "The information is not available in the uploaded document."
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:""")
        
        # Build RAG chain
        print("🔄 Building RAG chain...")
        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        print("✅ RAG chain ready")
        
        # Ask question
        print("\n" + "="*50)
        print(f"❓ Question: {question}")
        print("="*50)
        print("🤖 Thinking...")
        
        response = rag_chain.invoke(question)
        
        print("\n💭 Answer:")
        print("-" * 40)
        print(response)
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Example usage
    print("🤖 PDF Chat Demo")
    print("=" * 40)
    
    # Ask user for PDF path and question
    pdf_path = input("📁 Enter path to PDF file: ").strip()
    if not os.path.exists(pdf_path):
        print("❌ PDF file not found!")
        exit()
    
    question = input("❓ Enter your question: ").strip()
    if not question:
        print("❌ Please enter a question!")
        exit()
    
    # Run demo
    demo_pdf_chat(pdf_path, question)