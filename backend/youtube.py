# backend/youtube.py
import os
import json
from urllib.parse import urlencode

TRANSCRIPTS_DIR = "data/transcripts"

def get_video_url_at_time(video_id: str, start_seconds: float) -> str:
    """Return a YouTube URL that starts playback at `start_seconds`."""
    # YouTube timestamp format is in seconds
    params = urlencode({"t": int(start_seconds)})
    return f"https://www.youtube.com/watch?v={video_id}&{params}"

def load_transcript(video_id: str):
    """Load the transcript JSON for a video from disk."""
    path = os.path.join(TRANSCRIPTS_DIR, f"{video_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Transcript not found for video: {video_id}")
    with open(path, "r", encoding="utf-8") as f:
        transcript = json.load(f)
    return transcript

# Optional: Implement this if you want to fetch metadata via YouTube API
# (Requires API key and 'google-api-python-client' package)
# from googleapiclient.discovery import build
# YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
# youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
# def fetch_video_metadata(video_id: str):
#     request = youtube.videos().list(part="snippet,contentDetails", id=video_id)
#     response = request.execute()
#     if "items" not in response or not response["items"]:
#         return None
#     return response["items"][0]
