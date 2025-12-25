from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import logging

# Add the current directory to the path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.api.agent_endpoint import router as agent_router

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI application instance
app = FastAPI(
    title="Humanoid Robotics RAG Agent API - Hugging Face Deployment",
    description="Retrieval-Augmented Generation API for humanoid robotics textbook content",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow requests from Hugging Face Spaces and other origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the agent API router
app.include_router(agent_router, prefix="/api/agent", tags=["agent"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "humanoid-robotics-rag-agent-hf"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Humanoid Robotics RAG Agent API - Running on Hugging Face Spaces"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 7860)),  # Hugging Face uses PORT environment variable
        log_level="info"
    )