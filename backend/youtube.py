# backend/youtube.py
import os
import json
from urllib.parse import urlencode
from backend.config import YOUTUBE_API_KEY
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound  # type: ignore

# Add YouTube Data API search functionality
try:
    from googleapiclient.discovery import build  # type: ignore
except ImportError:
    build = None

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

def fetch_and_cache_transcript(video_id: str):
    """
    Fetch the transcript for a YouTube video and cache it locally as a JSON file.
    Returns the transcript as a list of dicts, or None if not available.
    Raises RuntimeError for unexpected errors or invalid transcript format.
    """
    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
    transcript_path = os.path.join(TRANSCRIPTS_DIR, f"{video_id}.json")
    # Check if already cached
    if os.path.exists(transcript_path):
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)
            if not isinstance(transcript, list) or not transcript:
                raise RuntimeError("Transcript file is empty or not in expected format.")
            return transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        if not isinstance(transcript, list) or not transcript:
            return None
        # Save to file
        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        raise RuntimeError(f"Error fetching transcript: {e}")

def search_youtube_videos(query, max_results=5):
    """
    Search YouTube for videos matching the query using the YouTube Data API.
    Returns a list of dicts with 'title', 'videoId', and 'description'.
    """
    if not YOUTUBE_API_KEY:
        raise RuntimeError("YOUTUBE_API_KEY is not set.")
    if build is None:
        raise ImportError("google-api-python-client is not installed.")
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results,
        safeSearch="moderate"
    )
    response = request.execute()
    results = []
    for item in response.get("items", []):
        video = {
            "title": item["snippet"]["title"],
            "videoId": item["id"]["videoId"],
            "description": item["snippet"]["description"]
        }
        results.append(video)
    return results
