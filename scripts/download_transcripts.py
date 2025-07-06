# scripts/download_transcripts.py
import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from backend.config import TRANSCRIPTS_DIR

def download_transcript(video_id: str) -> bool:
    """
    Download and save the transcript for a given YouTube video ID.
    
    Args:
        video_id (str): YouTube video ID
    
    Returns:
        bool: True if download succeeded, False otherwise
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Failed to fetch transcript for {video_id}: {e}")
        return False

    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
    filepath = os.path.join(TRANSCRIPTS_DIR, f"{video_id}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)
    
    print(f"Saved transcript for {video_id} to {filepath}")
    return True

if __name__ == "__main__":
    # List your YouTube video IDs here to download transcripts
    video_ids = [
        "YOUR_VIDEO_ID_1",
        "YOUR_VIDEO_ID_2",
        # Add more IDs as needed
    ]

    for vid in video_ids:
        download_transcript(vid)

