# backend/vector_store.py
import chromadb
from backend.embedding import get_embedding
import os
from backend.utils import clean_text, chunk_text
import numpy as np

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

collection_name = "fewfinder_subtitles"

def get_chroma_client():
    """Get or create ChromaDB client and collection."""
    chroma_client = chromadb.Client()
    try:
        collection = chroma_client.get_collection(name=collection_name)
    except Exception:
        collection = chroma_client.create_collection(name=collection_name)
    return collection

# Initialize collection
collection = get_chroma_client()

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

def search_transcript_chunks(query, transcript, max_chunk_length=200):
    """
    Given a transcript (list of dicts with 'text' and 'start'), chunk it, embed the chunks, and return the best match to the query.
    Returns a dict with 'text', 'start', and 'score'.
    """
    # Combine all text
    full_text = " ".join([seg["text"] for seg in transcript])
    chunks = chunk_text(full_text, max_length=max_chunk_length)
    if not chunks:
        return None
    # Get start times for each chunk (approximate by mapping to first segment in chunk)
    starts = []
    seg_idx = 0
    for chunk in chunks:
        # Find the first segment whose text appears in the chunk
        while seg_idx < len(transcript) and transcript[seg_idx]["text"] not in chunk:
            seg_idx += 1
        if seg_idx < len(transcript):
            starts.append(transcript[seg_idx]["start"])
        else:
            starts.append(0.0)
    # Embed query and chunks
    query_emb = get_embedding(query)
    chunk_embs = [get_embedding(chunk) for chunk in chunks]
    # Compute cosine similarity
    scores = [float(np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))) for emb in chunk_embs]
    best_idx = int(np.argmax(scores))
    return {
        "text": chunks[best_idx],
        "start": starts[best_idx],
        "score": scores[best_idx]
    }
