from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Query(BaseModel):
    """
    User input question requiring book-based response
    """
    query_text: str = Field(..., description="The natural language question to answer", min_length=1)
    top_k: int = Field(default=5, ge=1, le=20, description="Number of top results to retrieve")
    min_score: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity score threshold")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperature setting for the LLM")


class RetrievedContext(BaseModel):
    """
    Book content chunks retrieved from Qdrant collection
    """
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score between query and chunk")
    content: str = Field(..., description="The actual text content of the chunk")
    url: str = Field(..., description="Source URL of the content")
    title: str = Field(..., description="Page title or section heading")
    headings: List[str] = Field(default_factory=list, description="List of section headings")
    chunk_index: int = Field(..., description="Position of chunk in original document")
    source_document: str = Field(..., description="Identifier for the source document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AgentResponse(BaseModel):
    """
    Structured response including answer, sources, and confidence
    """
    query: str = Field(..., description="The original query text")
    answer: str = Field(..., description="The AI-generated answer based on retrieved context")
    retrieved_context: List[RetrievedContext] = Field(..., description="List of context chunks used to generate the answer")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the answer")
    sources: List[str] = Field(..., description="List of source URLs used in the response")
    processing_time: float = Field(..., description="Total time for retrieval and generation in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the response was generated")


class AgentConfig(BaseModel):
    """
    Configuration for the retrieval-aware AI agent
    """
    model_name: str = Field(default="gemini-2.5-flash", description="Name of the LLM to use")
    max_tokens: int = Field(default=1024, ge=1, le=8192, description="Maximum tokens for the response")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperature setting for the LLM")
    context_window: int = Field(default=1048576, description="Maximum context window size in tokens (1M for gemini-2.5-flash)")