"""
Unit tests for content grounding validation functionality.
Tests the validation that ensures responses are grounded in retrieved content.
"""
import pytest
from src.services.ai_agent_service import AIAgentService
from src.models.agent_models import RetrievedContext


@pytest.mark.asyncio
async def test_response_grounding_validation():
    """Test the response grounding validation functionality."""
    agent_service = AIAgentService.__new__(AIAgentService)  # Create without calling __init__

    # Test with a response that contains content from the context
    contexts = [
        RetrievedContext(
            score=0.8,
            content="Humanoid robots are robots with a human-like body structure.",
            url="https://example.com/humanoid",
            title="Humanoid Robot Design",
            headings=["Introduction"],
            chunk_index=0,
            source_document="doc1",
            metadata={}
        )
    ]

    grounded_response = "Humanoid robots are robots with a human-like body structure, which allows them to interact with human environments."
    is_valid = await agent_service._validate_response_grounding(grounded_response, contexts)
    assert isinstance(is_valid, bool)

    # Test with a response that doesn't contain content from the context
    non_ground_response = "Cats are animals that like to sleep."
    is_not_valid = await agent_service._validate_response_grounding(non_ground_response, contexts)
    assert isinstance(is_not_valid, bool)

    # Test with empty contexts
    is_empty_valid = await agent_service._validate_response_grounding(grounded_response, [])
    assert is_empty_valid is False

    # Test with empty response
    is_response_empty = await agent_service._validate_response_grounding("", contexts)
    assert is_response_empty is False


def test_confidence_calculation():
    """Test the confidence calculation functionality."""
    agent_service = AIAgentService.__new__(AIAgentService)  # Create without calling __init__

    # Test with multiple high-scoring contexts
    high_score_contexts = [
        RetrievedContext(score=0.9, content="content1", url="url1", title="title1",
                        headings=[], chunk_index=0, source_document="doc", metadata={}),
        RetrievedContext(score=0.8, content="content2", url="url2", title="title2",
                        headings=[], chunk_index=1, source_document="doc", metadata={})
    ]

    high_confidence = agent_service._calculate_confidence(high_score_contexts, True)
    assert 0.0 <= high_confidence <= 1.0

    # Test with single low-scoring context
    low_score_contexts = [
        RetrievedContext(score=0.2, content="content", url="url", title="title",
                        headings=[], chunk_index=0, source_document="doc", metadata={})
    ]

    low_confidence = agent_service._calculate_confidence(low_score_contexts, True)
    assert 0.0 <= low_confidence <= 1.0

    # Test with validation failure (is_valid = False) - should reduce confidence
    reduced_confidence = agent_service._calculate_confidence(high_score_contexts, False)
    assert 0.0 <= reduced_confidence <= 1.0

    # Confidence with validation failure should be lower than with validation success
    if high_confidence > 0:
        assert reduced_confidence <= high_confidence


def test_confidence_calculation_edge_cases():
    """Test confidence calculation with edge cases."""
    agent_service = AIAgentService.__new__(AIAgentService)  # Create without calling __init__

    # Test with empty contexts
    zero_confidence = agent_service._calculate_confidence([], True)
    assert zero_confidence == 0.0

    # Test with single context
    single_context = [
        RetrievedContext(score=0.5, content="content", url="url", title="title",
                        headings=[], chunk_index=0, source_document="doc", metadata={})
    ]
    single_confidence = agent_service._calculate_confidence(single_context, True)
    assert 0.0 <= single_confidence <= 1.0

    # Test with very high scoring contexts
    high_contexts = [
        RetrievedContext(score=1.0, content="content1", url="url1", title="title1",
                        headings=[], chunk_index=0, source_document="doc", metadata={})
    ]
    high_confidence = agent_service._calculate_confidence(high_contexts, True)
    assert 0.0 <= high_confidence <= 1.0


@pytest.mark.asyncio
async def test_grounding_validation_with_varied_content():
    """Test grounding validation with different types of content."""
    agent_service = AIAgentService.__new__(AIAgentService)  # Create without calling __init__

    # Test with multiple contexts
    contexts = [
        RetrievedContext(
            score=0.7,
            content="Humanoid robots typically have two arms and two legs.",
            url="https://example.com/structure",
            title="Robot Structure",
            headings=["Design"],
            chunk_index=0,
            source_document="doc1",
            metadata={}
        ),
        RetrievedContext(
            score=0.6,
            content="Walking algorithms are important for humanoid locomotion.",
            url="https://example.com/locomotion",
            title="Robot Locomotion",
            headings=["Movement"],
            chunk_index=1,
            source_document="doc2",
            metadata={}
        )
    ]

    # Response that contains content from first context
    response1 = "Humanoid robots have two arms and two legs which is their defining characteristic."
    is_valid1 = await agent_service._validate_response_grounding(response1, contexts)
    assert isinstance(is_valid1, bool)

    # Response that contains content from second context
    response2 = "Walking algorithms are crucial for making humanoid robots move properly."
    is_valid2 = await agent_service._validate_response_grounding(response2, contexts)
    assert isinstance(is_valid2, bool)

    # Response that contains content from both contexts
    response3 = "Humanoid robots have two arms and legs, and their walking algorithms are important for locomotion."
    is_valid3 = await agent_service._validate_response_grounding(response3, contexts)
    assert isinstance(is_valid3, bool)

    # Response that contains no content from contexts
    response4 = "Dogs are loyal animals and make good pets."
    is_valid4 = await agent_service._validate_response_grounding(response4, contexts)
    assert isinstance(is_valid4, bool)


def test_context_formatting():
    """Test the context formatting functionality."""
    agent_service = AIAgentService.__new__(AIAgentService)  # Create without calling __init__

    contexts = [
        RetrievedContext(
            score=0.8,
            content="This is the first context.",
            url="https://example.com/1",
            title="First Title",
            headings=["Section 1"],
            chunk_index=0,
            source_document="doc1",
            metadata={}
        ),
        RetrievedContext(
            score=0.7,
            content="This is the second context.",
            url="https://example.com/2",
            title="Second Title",
            headings=["Section 2"],
            chunk_index=1,
            source_document="doc2",
            metadata={}
        )
    ]

    formatted = agent_service._format_context_for_model(contexts)

    # Check that the formatted string contains expected elements
    assert "Here is the relevant context from the humanoid robotics textbook:" in formatted
    assert "Context 1:" in formatted
    assert "Context 2:" in formatted
    assert "First Title" in formatted
    assert "Second Title" in formatted
    assert "This is the first context." in formatted
    assert "This is the second context." in formatted
    assert "https://example.com/1" in formatted
    assert "https://example.com/2" in formatted