# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import router as search_router

app = FastAPI(title="Fewfinder API")

# Allow React frontend (adjust origins as needed)
origins = [
    "http://localhost:3000",  # React dev server default port
    "http://localhost:5173",  # Vite dev server default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include search API routes
app.include_router(search_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Fewfinder API"}
