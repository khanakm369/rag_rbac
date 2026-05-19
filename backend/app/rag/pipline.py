import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

# 1. Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FILES_PATH = os.path.join(BASE_DIR, "../static")

def process_and_store_docs():
    # 2. Load all Markdown files recursively
    # This will pick up engineering_master_doc.md and others
    loader = DirectoryLoader(
        STATIC_FILES_PATH, 
        glob="**/*.md", 
        loader_cls=UnstructuredMarkdownLoader
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents.")

    # 3. Chunking the data
    # We use RecursiveCharacterTextSplitter to keep paragraphs/sentences together
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks.")

    # 4. Initialize Embeddings (Ensure OPENAI_API_KEY is in your .env)
    embeddings = OpenAIEmbeddings()

    # 5. Store in Qdrant
    # 'vector-db' is the service name from your docker-compose
    url = "http://localhost:6333" 
    
    qdrant = Qdrant.from_documents(
        chunks,
        embeddings,
        url=url,
        collection_name="finsolve_docs",
    )
    print("Successfully ingested data into Qdrant!")

if __name__ == "__main__":
    process_and_store_docs()