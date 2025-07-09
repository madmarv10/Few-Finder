# backend/search.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.vector_store import search_transcripts
from backend.vector_store import search_transcript_chunks
from backend.youtube import get_video_url_at_time
from backend.youtube import search_youtube_videos
from backend.youtube import fetch_and_cache_transcript
from typing import List

router = APIRouter()

class SearchRequest(BaseModel):
    question: str

class SearchResponse(BaseModel):
    video_url: str
    transcript_text: str
    start_time: float

class YouTubeSearchRequest(BaseModel):
    query: str
    max_results: int = 5

class YouTubeVideoResult(BaseModel):
    title: str
    videoId: str
    description: str

class TranscriptRequest(BaseModel):
    videoId: str

class DynamicSearchRequest(BaseModel):
    question: str
    videoId: str

class DynamicSearchResponse(BaseModel):
    video_url: str
    transcript_text: str
    start_time: float
    score: float

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        result = search_transcripts(request.question)
        if not result:
            # Return a default response instead of 404 for now
            return SearchResponse(
                video_url="https://example.com/no-match",
                transcript_text="No relevant match found in the database.",
                start_time=0.0
            )
        
        video_url = get_video_url_at_time(result["video_id"], result["start"])
        return SearchResponse(
            video_url=video_url,
            transcript_text=result["text"],
            start_time=result["start"]
        )
    except Exception as e:
        # Return a default response on any error
        return SearchResponse(
            video_url="https://example.com/error",
            transcript_text=f"Error processing request: {str(e)}",
            start_time=0.0
        )

@router.post("/youtube_search", response_model=List[YouTubeVideoResult])
async def youtube_search(request: YouTubeSearchRequest):
    try:
        results = search_youtube_videos(request.query, max_results=request.max_results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fetch_transcript")
async def fetch_transcript(request: TranscriptRequest):
    try:
        transcript = fetch_and_cache_transcript(request.videoId)
        if transcript is None or not isinstance(transcript, list) or not transcript:
            raise HTTPException(status_code=404, detail="Transcript not available or empty for this video.")
        return {"transcript": transcript}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transcript: {e}")

@router.post("/dynamic_search", response_model=DynamicSearchResponse)
async def dynamic_search(request: DynamicSearchRequest):
    try:
        transcript = fetch_and_cache_transcript(request.videoId)
        if transcript is None or not isinstance(transcript, list) or not transcript:
            raise HTTPException(status_code=404, detail="Transcript not available or empty for this video.")
        result = search_transcript_chunks(request.question, transcript)
        if result is None:
            raise HTTPException(status_code=404, detail="No relevant match found in transcript.")
        video_url = get_video_url_at_time(request.videoId, result["start"])
        return DynamicSearchResponse(
            video_url=video_url,
            transcript_text=result["text"],
            start_time=result["start"],
            score=result["score"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during dynamic search: {e}")
