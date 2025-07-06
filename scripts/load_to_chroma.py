# scripts/load_to_chroma.py
import os
import json
import uuid
from backend.utils import clean_text, chunk_text
from backend.vector_store import add_subtitle_chunks
from backend.config import TRANSCRIPTS_DIR

def load_transcripts_and_store():
    all_chunks = []

    # Loop through all transcript files
    for filename in os.listdir(TRANSCRIPTS_DIR):
        if not filename.endswith(".json"):
            continue

        video_id = filename[:-5]  # Remove '.json' extension
        filepath = os.path.join(TRANSCRIPTS_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        # Each transcript is a list of dicts with keys like 'text', 'start', 'duration'
        for entry in transcript:
            raw_text = entry.get("text", "")
            start_time = entry.get("start", 0.0)
            cleaned_text = clean_text(raw_text)
            chunks = chunk_text(cleaned_text)

            for chunk_text_part in chunks:
                chunk_id = str(uuid.uuid4())  # Unique ID for this chunk
                all_chunks.append({
                    "id": chunk_id,
                    "text": chunk_text_part,
                    "video_id": video_id,
                    "start": start_time,
                })

    print(f"Adding {len(all_chunks)} chunks to Chroma vector store...")
    add_subtitle_chunks(all_chunks)
    print("Done.")

if __name__ == "__main__":
    load_transcripts_and_store()
