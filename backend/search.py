# backend/search.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.vector_store import search_transcripts
from backend.youtube import get_video_url_at_time

router = APIRouter()

class SearchRequest(BaseModel):
    question: str

class SearchResponse(BaseModel):
    video_url: str
    transcript_text: str
    start_time: float

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    result = search_transcripts(request.question)
    if not result:
        raise HTTPException(status_code=404, detail="No relevant match found.")
    
    video_url = get_video_url_at_time(result["video_id"], result["start"])
    return SearchResponse(
        video_url=video_url,
        transcript_text=result["text"],
        start_time=result["start"]
    )
