"""
Contract tests for the API endpoints.
These tests verify that the API endpoints conform to the expected contract.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.agent_endpoint import router
from fastapi import FastAPI


# Create a test app with the agent router
app = FastAPI()
app.include_router(router, prefix="/api/agent", tags=["agent"])
client = TestClient(app)


def test_health_endpoint_contract():
    """Test that the health endpoint follows the expected contract."""
    response = client.get("/api/agent/health")

    # Should return 200 status
    assert response.status_code == 200

    # Should return expected structure
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "services" in data

    # Services should contain expected keys
    assert "qdrant" in data["services"]
    assert "retrieval_pipeline" in data["services"]
    assert "openai_compatible_api" in data["services"]


def test_query_endpoint_exists():
    """Test that the query endpoint exists and has expected method."""
    # Check if the endpoint is registered by trying to access the OpenAPI schema
    schema_response = client.get("/openapi.json")
    assert schema_response.status_code == 200

    schema = schema_response.json()

    # Verify that the /api/agent/query endpoint is in the schema
    assert "/api/agent/query" in schema["paths"]
    assert "post" in schema["paths"]["/api/agent/query"]


def test_agent_info_endpoint():
    """Test that the agent info endpoint exists."""
    response = client.get("/api/agent/")

    # Should return 200 status
    assert response.status_code == 200

    # Should return expected structure
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "description" in data
    assert "endpoints" in data


def test_api_request_response_models():
    """Test that the API request/response models have expected structure."""
    from src.models.api_models import AgentQueryRequest, AgentQueryResponse, HealthCheckResponse, ErrorResponse

    # Test AgentQueryRequest structure
    assert hasattr(AgentQueryRequest, '__annotations__')
    annotations = AgentQueryRequest.__annotations__
    assert 'query' in annotations

    # Test AgentQueryResponse structure
    assert hasattr(AgentQueryResponse, '__annotations__')
    response_annotations = AgentQueryResponse.__annotations__
    assert 'query' in response_annotations
    assert 'answer' in response_annotations
    assert 'confidence' in response_annotations
    assert 'sources' in response_annotations
    assert 'processing_time' in response_annotations

    # Test HealthCheckResponse structure
    assert hasattr(HealthCheckResponse, '__annotations__')
    health_annotations = HealthCheckResponse.__annotations__
    assert 'status' in health_annotations
    assert 'timestamp' in health_annotations
    assert 'services' in health_annotations


def test_error_response_structure():
    """Test that error responses follow expected structure."""
    from src.models.api_models import ErrorResponse

    assert hasattr(ErrorResponse, '__annotations__')
    error_annotations = ErrorResponse.__annotations__
    assert 'error' in error_annotations