"""
FastAPI Backend for Music Guessing Game

Main application entry point with CORS configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import game, songs, admin

app = FastAPI(
    title="Music Guessing Game API",
    description="Backend API for the Music Guessing Game with multi-provider support and custom admin lists",
    version="2.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(game.router, prefix="/api/game", tags=["game"])
app.include_router(songs.router, prefix="/api/songs", tags=["songs"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Music Guessing Game API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
