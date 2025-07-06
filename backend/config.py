# backend/config.py

# Paths
TRANSCRIPTS_DIR = "data/transcripts"
CHROMA_DB_DIR = "data/chroma"

# Sentence Transformer model name
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# YouTube API key (if used)
YOUTUBE_API_KEY = ""  # Add your API key here or load from environment variables

# Frontend URLs allowed for CORS (adjust as needed)
FRONTEND_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://localhost:5173",  # Vite dev server
]

# Other settings
MAX_CHUNK_LENGTH = 200  # Max characters per subtitle chunk
