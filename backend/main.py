from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.agent_endpoint import router as agent_router
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI application instance
app = FastAPI(
    title="Humanoid Robotics RAG Agent API",
    description="Retrieval-Augmented Generation API for humanoid robotics textbook content",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow requests from the frontend
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
    return {"status": "healthy", "service": "humanoid-robotics-rag-agent"}

# For backward compatibility with existing main function
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
