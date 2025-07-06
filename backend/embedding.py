# backend/embedding.py
from sentence_transformers import SentenceTransformer

# Load model once at startup to avoid reloading every call
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    """
    Generate a vector embedding for the input text.
    
    Args:
        text (str): Input sentence or paragraph to embed.
    
    Returns:
        List[float]: The embedding vector as a list of floats.
    """
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding
