# backend/utils.py
import re
from typing import List

def clean_text(text: str) -> str:
    """
    Clean and normalize transcript text.
    Removes excessive whitespace and unwanted characters.
    """
    text = text.replace('\n', ' ')           # Replace newlines with space
    text = re.sub(r'\s+', ' ', text)         # Collapse multiple spaces
    text = text.strip()
    return text

def chunk_text(text: str, max_length: int = 200) -> List[str]:
    """
    Split text into chunks of max_length characters, ideally at sentence boundaries.
    
    Args:
        text (str): Input transcript text
        max_length (int): Max chunk size in characters
    
    Returns:
        List[str]: List of text chunks
    """
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split by sentence endings
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
