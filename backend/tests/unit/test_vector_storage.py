"""
Unit tests for the VectorStorage class in the RAG pipeline.
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from src.storage.vector_storage import VectorStorage
from src.utils.config import get_config


def test_vector_storage_initialization():
    """
    Test that VectorStorage initializes correctly with configuration.
    """
    # Test initialization
    storage = VectorStorage()

    # Verify that config was loaded
    config = get_config()
    assert storage.config.cohere_api_key == config.cohere_api_key
    assert storage.config.qdrant_url == config.qdrant_url
    assert storage.config.qdrant_api_key == config.qdrant_api_key
    assert storage.collection_name == config.collection_name

    print("✅ VectorStorage initialization test passed")


def test_validate_metadata_structure():
    """
    Test the metadata validation function with valid and invalid data.
    """
    storage = VectorStorage()

    # Test with valid metadata structure
    valid_result = {
        'score': 0.8,
        'payload': {
            'url': 'https://example.com',
            'title': 'Test Title',
            'content': 'Test content',
            'headings': ['Heading 1'],
            'chunk_index': 0,
            'source_document': 'doc1',
            'metadata': {}
        },
        'url': 'https://example.com',
        'title': 'Test Title',
        'content': 'Test content'
    }

    validation = storage.validate_metadata(valid_result)
    assert validation['valid'] == True
    assert len(validation['errors']) == 0
    print("✅ Valid metadata structure test passed")

    # Test with missing required field
    invalid_result = {
        'score': 0.8,
        'payload': {
            'url': 'https://example.com',
            # Missing 'title' field
            'content': 'Test content',
            'headings': ['Heading 1'],
            'chunk_index': 0,
            'source_document': 'doc1',
            'metadata': {}
        },
        'url': 'https://example.com',
        'title': 'Test Title',
        'content': 'Test content'
    }

    validation = storage.validate_metadata(invalid_result)
    assert validation['valid'] == False
    assert len(validation['errors']) > 0
    print("✅ Invalid metadata structure test passed")


def test_validate_relevance_scoring():
    """
    Test the relevance scoring validation function.
    """
    storage = VectorStorage()

    # Test with empty results
    validation = storage.validate_relevance_scoring([], "test query")
    assert validation['valid'] == True
    assert validation['score_analysis']['count'] == 0
    print("✅ Empty results relevance validation test passed")

    # Test with valid results
    results = [
        {'score': 0.8, 'payload': {}, 'url': '', 'title': '', 'content': ''},
        {'score': 0.6, 'payload': {}, 'url': '', 'title': '', 'content': ''},
        {'score': 0.4, 'payload': {}, 'url': '', 'title': '', 'content': ''}
    ]

    validation = storage.validate_relevance_scoring(results, "test query")
    assert validation['valid'] == True
    assert validation['score_analysis']['count'] == 3
    assert validation['score_analysis']['avg'] == 0.6  # (0.8 + 0.6 + 0.4) / 3
    assert validation['relevance_indicators']['is_differentiated'] == True
    print("✅ Valid results relevance validation test passed")


def test_metadata_validation_edge_cases():
    """
    Test metadata validation with various edge cases.
    """
    storage = VectorStorage()

    # Test with non-dict payload
    result_with_bad_payload = {
        'score': 0.8,
        'payload': "not a dict",  # This should cause validation to fail
        'url': 'https://example.com',
        'title': 'Test Title',
        'content': 'Test content'
    }

    validation = storage.validate_metadata(result_with_bad_payload)
    assert validation['valid'] == False
    assert len(validation['errors']) > 0
    print("✅ Bad payload validation test passed")

    # Test with missing top-level fields
    result_missing_fields = {
        'score': 0.8,
        # Missing 'payload', 'url', 'title', 'content'
    }

    validation = storage.validate_metadata(result_missing_fields)
    assert validation['valid'] == False
    assert len(validation['errors']) >= 4  # Should have errors for missing fields
    print("✅ Missing fields validation test passed")


if __name__ == "__main__":
    test_vector_storage_initialization()
    test_validate_metadata_structure()
    test_validate_relevance_scoring()
    test_metadata_validation_edge_cases()
    print("All unit tests for VectorStorage passed!")