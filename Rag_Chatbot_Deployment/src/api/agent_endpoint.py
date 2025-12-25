from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Optional
import time
import logging

from src.models.api_models import AgentQueryRequest, AgentQueryResponse, HealthCheckResponse, ErrorResponse
from src.models.error_models import InsufficientContextError, RetrievalError, AgentError
from src.services.retrieval_service import retrieval_service
from src.services.ai_agent_service import AIAgentService


logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

# Import the agent service instance (with fallback if API key is missing)
from src.services.ai_agent_service import agent_service


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify the agent service is operational.
    """
    try:
        # Get retrieval system stats
        retrieval_stats = await retrieval_service.get_retrieval_stats()

        # Check if OpenAI-compatible API is accessible (basic check)
        openai_compatible_api_accessible = True  # This would require actual API call to verify

        # Overall service status
        overall_status = "healthy" if (
            retrieval_stats.get('collection_exists', False) and
            retrieval_stats.get('sample_search_works', False) and
            openai_compatible_api_accessible
        ) else "degraded"

        response = HealthCheckResponse(
            status=overall_status,
            timestamp=str(time.time()),
            services={
                "qdrant": "connected" if retrieval_stats.get('collection_exists', False) else "disconnected",
                "retrieval_pipeline": "operational" if retrieval_stats.get('sample_search_works', False) else "error",
                "openai_compatible_api": "available" if openai_compatible_api_accessible else "unavailable"
            }
        )

        return response

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


@router.post("/query", response_model=AgentQueryResponse)
async def query_agent(request: AgentQueryRequest):
    """
    Submit a query to the retrieval-aware AI agent and receive a grounded response based on retrieved content.
    """
    start_time = time.time()

    try:
        # Use the AI agent service to process the query
        result = await agent_service.process_query(
            query_text=request.query,
            top_k=request.top_k or 5,
            min_score=request.min_score or 0.3,
            temperature=request.temperature or 0.7
        )

        processing_time = time.time() - start_time

        response = AgentQueryResponse(
            query=result.query,
            answer=result.answer,
            confidence=result.confidence,
            sources=result.sources,
            processing_time=processing_time
        )

        logger.info(f"Query processed successfully in {processing_time:.3f}s")
        return response

    except InsufficientContextError as e:
        processing_time = time.time() - start_time
        logger.warning(f"Insufficient context for query: {str(e)} (processed in {processing_time:.3f}s)")

        raise HTTPException(
            status_code=422,
            detail={
                "error": "Insufficient context",
                "message": e.message,
                "processing_time": processing_time
            }
        )

    except RetrievalError as e:
        processing_time = time.time() - start_time
        logger.error(f"Retrieval error for query: {str(e)} (processed in {processing_time:.3f}s)")

        raise HTTPException(
            status_code=500,
            detail={
                "error": "Retrieval error",
                "message": e.message,
                "processing_time": processing_time
            }
        )

    except AgentError as e:
        processing_time = time.time() - start_time
        logger.error(f"Agent error for query: {str(e)} (processed in {processing_time:.3f}s)")

        raise HTTPException(
            status_code=500,
            detail={
                "error": "Agent error",
                "message": e.message,
                "processing_time": processing_time
            }
        )

    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Unexpected error processing query: {str(e)} (processed in {processing_time:.3f}s)")

        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": f"Failed to process query due to internal error: {str(e)}",
                "processing_time": processing_time
            }
        )


@router.get("/")
async def agent_info():
    """
    Get information about the agent service.
    """
    return {
        "name": "Humanoid Robotics RAG Agent",
        "version": "0.1.0",
        "description": "Retrieval-Augmented Generation API for humanoid robotics textbook content",
        "endpoints": ["/query", "/health"]
    }