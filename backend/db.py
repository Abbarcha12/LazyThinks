import chromadb
from chromadb.config import Settings
import os

# Define the persistence directory
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def get_chroma_client():
    """
    Returns a persistent ChromaDB client.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return client

def get_collection(collection_name="documents"):
    """
    Returns a collection from ChromaDB.
    """
    client = get_chroma_client()
    # using default embedding function if none provided, 
    # but normally we want to use the same one as ingestion.
    # For now, let's keep it simple.
    collection = client.get_or_create_collection(name=collection_name)
    return collection
