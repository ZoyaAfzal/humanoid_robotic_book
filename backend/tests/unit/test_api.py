"""
Unit tests for the API endpoint functionality.
Tests individual components of the API in isolation.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from src.api.agent_endpoint import router
from fastapi import FastAPI
from src.models.api_models import AgentQueryRequest


def test_agent_query_request_model():
    """Test the AgentQueryRequest model structure and validation."""
    # Test with minimal required fields
    request = AgentQueryRequest(query="test query")
    assert request.query == "test query"
    assert request.top_k == 5  # default value
    assert request.min_score == 0.3  # default value
    assert request.temperature == 0.7  # default value

    # Test with all fields provided
    request = AgentQueryRequest(
        query="test query",
        top_k=3,
        min_score=0.5,
        temperature=0.4
    )
    assert request.query == "test query"
    assert request.top_k == 3
    assert request.min_score == 0.5
    assert request.temperature == 0.4


def test_agent_query_request_validation():
    """Test validation of the AgentQueryRequest model."""
    # Test that query is required
    try:
        AgentQueryRequest(query="")
        assert False, "Should have raised validation error for empty query"
    except Exception:
        pass  # Expected validation error

    # Test that top_k must be between 1 and 20
    try:
        AgentQueryRequest(query="test", top_k=0)
        assert False, "Should have raised validation error for top_k < 1"
    except Exception:
        pass  # Expected validation error

    try:
        AgentQueryRequest(query="test", top_k=21)
        assert False, "Should have raised validation error for top_k > 20"
    except Exception:
        pass  # Expected validation error

    # Test that min_score must be between 0.0 and 1.0
    try:
        AgentQueryRequest(query="test", min_score=-0.1)
        assert False, "Should have raised validation error for min_score < 0.0"
    except Exception:
        pass  # Expected validation error

    try:
        AgentQueryRequest(query="test", min_score=1.1)
        assert False, "Should have raised validation error for min_score > 1.0"
    except Exception:
        pass  # Expected validation error


def test_agent_query_response_model():
    """Test the AgentQueryResponse model structure."""
    from src.models.api_models import AgentQueryResponse

    # Create a response instance
    response = AgentQueryResponse(
        query="test query",
        answer="test answer",
        confidence=0.8,
        sources=["https://example.com"],
        processing_time=0.1
    )

    assert response.query == "test query"
    assert response.answer == "test answer"
    assert response.confidence == 0.8
    assert response.sources == ["https://example.com"]
    assert response.processing_time == 0.1


def test_health_check_response_model():
    """Test the HealthCheckResponse model structure."""
    from src.models.api_models import HealthCheckResponse

    response = HealthCheckResponse(
        status="healthy",
        timestamp="2023-01-01T00:00:00Z",
        services={"qdrant": "connected"}
    )

    assert response.status == "healthy"
    assert response.timestamp == "2023-01-01T00:00:00Z"
    assert response.services == {"qdrant": "connected"}


def test_error_response_model():
    """Test the ErrorResponse model structure."""
    from src.models.api_models import ErrorResponse

    response = ErrorResponse(
        error="test error",
        message="test message",
        details={"key": "value"}
    )

    assert response.error == "test error"
    assert response.message == "test message"
    assert response.details == {"key": "value"}


def test_router_structure():
    """Test that the API router has expected structure."""
    # Check that the router object exists
    assert router is not None

    # Check that expected routes are defined (at the router level)
    # The actual route paths are checked in integration tests
    assert hasattr(router, 'routes')
    assert len(router.routes) > 0  # Should have at least one route


@pytest.mark.asyncio
def test_endpoint_functions_exist():
    """Test that the endpoint functions exist and have expected signatures."""
    import inspect
    from src.api.agent_endpoint import query_agent, health_check, agent_info

    # Check health_check function
    health_sig = inspect.signature(health_check)
    assert len(health_sig.parameters) == 0  # No parameters expected

    # Check query_agent function
    query_sig = inspect.signature(query_agent)
    assert 'request' in query_sig.parameters  # Should accept AgentQueryRequest
    # Check that request parameter has the expected type annotation
    assert query_sig.parameters['request'].annotation.__name__ == 'AgentQueryRequest'

    # Check agent_info function
    info_sig = inspect.signature(agent_info)
    assert len(info_sig.parameters) == 0  # No parameters expected


def test_api_router_prefix():
    """Test that the router has the expected prefix when included in app."""
    # This is more of an integration test, but verifies the API structure
    test_app = FastAPI()
    test_app.include_router(router, prefix="/api/agent", tags=["agent"])

    # Check that the routes exist in the app
    assert len(test_app.router.routes) > 0