from pydantic import BaseModel, Field
from typing import List, Optional
from .agent_models import Query, AgentResponse


class AgentQueryRequest(BaseModel):
    """
    API request model for the agent query endpoint
    """
    query: str = Field(..., description="The natural language question to answer", min_length=1)
    top_k: Optional[int] = Field(default=5, ge=1, le=20, description="Number of top results to retrieve")
    min_score: Optional[float] = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity score threshold")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=1.0, description="Temperature setting for the LLM")


class AgentQueryResponse(BaseModel):
    """
    API response model for the agent query endpoint
    """
    query: str = Field(..., description="The original query text")
    answer: str = Field(..., description="The AI-generated answer based on retrieved context")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the answer")
    sources: List[str] = Field(..., description="List of source URLs used in the response")
    processing_time: float = Field(..., description="Total time for retrieval and generation in seconds")


class HealthCheckResponse(BaseModel):
    """
    API response model for the health check endpoint
    """
    status: str = Field(..., description="Health status of the service")
    timestamp: str = Field(..., description="Timestamp of the health check")
    services: dict = Field(..., description="Status of dependent services")


class ErrorResponse(BaseModel):
    """
    API response model for error responses
    """
    error: str = Field(..., description="Error message")
    message: Optional[str] = Field(default=None, description="Detailed error message")
    details: Optional[dict] = Field(default=None, description="Additional error details")