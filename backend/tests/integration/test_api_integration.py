"""
Integration tests for the API endpoints.
Tests the integration between API endpoints and underlying services.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from src.api.agent_endpoint import router
from fastapi import FastAPI
from src.models.agent_models import RetrievedContext, AgentResponse


# Create a test app with the agent router
app = FastAPI()
app.include_router(router, prefix="/api/agent", tags=["agent"])
client = TestClient(app)


def test_health_endpoint_integration():
    """Test the health endpoint integration."""
    with patch('src.services.retrieval_service.retrieval_service.get_retrieval_stats') as mock_stats:
        mock_stats.return_value = {
            'collection_exists': True,
            'sample_search_works': True
        }

        response = client.get("/api/agent/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] in ["healthy", "degraded"]


@pytest.mark.asyncio
def test_query_endpoint_with_mocked_services():
    """Test the query endpoint with mocked services."""
    # Mock the agent service response
    mock_response = AgentResponse(
        query="test query",
        answer="This is a test answer.",
        retrieved_context=[
            RetrievedContext(
                score=0.8,
                content="Test content",
                url="https://example.com",
                title="Test Title",
                headings=["Test"],
                chunk_index=0,
                source_document="test_doc",
                metadata={}
            )
        ],
        confidence=0.85,
        sources=["https://example.com"],
        processing_time=0.1
    )

    # Mock the agent service
    with patch('src.services.ai_agent_service.AIAgentService') as mock_agent_class:
        mock_agent_instance = Mock()
        mock_agent_instance.process_query = AsyncMock(return_value=mock_response)
        mock_agent_class.return_value = mock_agent_instance

        # Test the query endpoint
        query_data = {
            "query": "What are the basics of humanoid robotics?",
            "top_k": 5,
            "min_score": 0.3,
            "temperature": 0.7
        }

        response = client.post("/api/agent/query", json=query_data)

        # Should return 200 status
        assert response.status_code == 200

        # Should return expected structure
        data = response.json()
        assert "query" in data
        assert "answer" in data
        assert "confidence" in data
        assert "sources" in data
        assert "processing_time" in data


def test_query_endpoint_validation():
    """Test the query endpoint validation."""
    # Test with empty query
    response = client.post("/api/agent/query", json={"query": ""})
    # Should return 422 for validation error or 400 depending on how validation is handled
    # In our implementation, this would be handled by the agent service raising ValidationError

    # Test with valid query but potentially no results
    query_data = {
        "query": "test query",
        "top_k": 5,
        "min_score": 0.3,
        "temperature": 0.7
    }

    # Since we're testing validation, we expect this to at least reach the validation stage
    with patch('src.services.ai_agent_service.AIAgentService') as mock_agent_class:
        # Mock an exception to test error handling
        mock_agent_instance = Mock()
        from src.models.error_models import InsufficientContextError
        mock_agent_instance.process_query = AsyncMock(side_effect=InsufficientContextError())
        mock_agent_class.return_value = mock_agent_instance

        response = client.post("/api/agent/query", json=query_data)
        # Should return 422 for insufficient context
        assert response.status_code == 422


def test_api_endpoint_registration():
    """Test that all expected API endpoints are registered."""
    # Get the OpenAPI schema to verify endpoints
    schema_response = client.get("/openapi.json")
    assert schema_response.status_code == 200

    schema = schema_response.json()

    # Check that expected endpoints exist
    expected_endpoints = [
        "/api/agent/health",
        "/api/agent/query",
        "/api/agent/"
    ]

    for endpoint in expected_endpoints:
        assert endpoint in schema["paths"]
        # Each endpoint should have appropriate methods
        if endpoint == "/api/agent/query":
            assert "post" in schema["paths"][endpoint]
        elif endpoint == "/api/agent/health":
            assert "get" in schema["paths"][endpoint]
        elif endpoint == "/api/agent/":
            assert "get" in schema["paths"][endpoint]


@pytest.mark.asyncio
def test_query_endpoint_with_different_parameters():
    """Test the query endpoint with different parameter combinations."""
    mock_response = AgentResponse(
        query="test query",
        answer="This is a test answer.",
        retrieved_context=[
            RetrievedContext(
                score=0.8,
                content="Test content",
                url="https://example.com",
                title="Test Title",
                headings=["Test"],
                chunk_index=0,
                source_document="test_doc",
                metadata={}
            )
        ],
        confidence=0.85,
        sources=["https://example.com"],
        processing_time=0.1
    )

    with patch('src.services.ai_agent_service.AIAgentService') as mock_agent_class:
        mock_agent_instance = Mock()
        mock_agent_instance.process_query = AsyncMock(return_value=mock_response)
        mock_agent_class.return_value = mock_agent_instance

        # Test with minimal parameters
        response = client.post("/api/agent/query", json={"query": "simple query"})
        assert response.status_code == 200

        # Test with all parameters
        response = client.post("/api/agent/query", json={
            "query": "detailed query",
            "top_k": 3,
            "min_score": 0.5,
            "temperature": 0.3
        })
        assert response.status_code == 200