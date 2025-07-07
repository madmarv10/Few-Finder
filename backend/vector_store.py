# backend/vector_store.py
import chromadb
from embedding import get_embedding
import os

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Initialize Chroma client with new syntax
client = chromadb.PersistentClient(path="data/chroma")
collection_name = "fewfinder_subtitles"

# Create or get the collection
try:
    collection = client.get_collection(name=collection_name)
except Exception:
    collection = client.create_collection(name=collection_name)

def add_subtitle_chunks(chunks):
    """
    Add subtitle chunks to the vector store.
    
    Args:
        chunks (list of dict): Each dict must have keys:
            - 'id' (str): unique chunk ID
            - 'text' (str): subtitle text
            - 'video_id' (str): YouTube video ID
            - 'start' (float): start time in seconds
    """
    embeddings = [get_embedding(chunk['text']).tolist() for chunk in chunks]
    metadatas = [{"video_id": c["video_id"], "start": c["start"], "text": c["text"]} for c in chunks]
    ids = [c["id"] for c in chunks]

    collection.add(
        documents=[c["text"] for c in chunks],
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

def search_transcripts(query, n_results=1):
    """
    Search the vector store with a query string and return top match metadata.
    
    Args:
        query (str): User question
        n_results (int): Number of results to return
    
    Returns:
        dict or None: metadata of the top match, or None if empty
    """
    query_embedding = get_embedding(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    if not results['ids'][0]:
        return None
    
    # Extract metadata of the top result
    top_meta = results['metadatas'][0][0]
    return top_meta
