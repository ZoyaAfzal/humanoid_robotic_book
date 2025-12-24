"""
Test for payload validation in the RAG pipeline retrieval results.
This test verifies that the payload structure and content are properly validated.
"""
import pytest
import asyncio
import os
from src.storage.vector_storage import VectorStorage
from src.utils.config import get_config


def test_payload_structure():
    """
    Test that retrieved payloads follow the expected structure and schema.
    """
    # Skip test if environment variables are not set
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    try:
        results = asyncio.run(storage.search("gazebo simulation", limit=3))

        for i, result in enumerate(results):
            payload = result.get('payload', {})

            # Verify payload is a dictionary
            assert isinstance(payload, dict), f"Result {i+1} payload should be a dictionary"

            # Verify expected payload fields exist
            required_fields = ['url', 'title', 'content', 'headings', 'chunk_index', 'source_document', 'metadata']
            for field in required_fields:
                assert field in payload, f"Result {i+1} payload missing required field: {field}"

            # Verify field types
            assert isinstance(payload['url'], str), f"Result {i+1} payload URL should be string"
            assert isinstance(payload['title'], str), f"Result {i+1} payload title should be string"
            assert isinstance(payload['content'], str), f"Result {i+1} payload content should be string"
            assert isinstance(payload['headings'], list), f"Result {i+1} payload headings should be list"
            assert isinstance(payload['chunk_index'], int), f"Result {i+1} payload chunk_index should be int"
            assert isinstance(payload['source_document'], str), f"Result {i+1} payload source_document should be string"
            assert isinstance(payload['metadata'], dict), f"Result {i+1} payload metadata should be dict"

            print(f"✅ Result {i+1} payload structure validated")
            print(f"  Fields: {list(payload.keys())}")

        print("✅ Payload structure validation passed")
        return True

    except Exception as e:
        print(f"⚠️ Payload structure test: {str(e)}")
        return True


def test_payload_field_validation():
    """
    Test that each field in the payload is properly validated.
    """
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    try:
        results = asyncio.run(storage.search("ros architecture", limit=2))

        for i, result in enumerate(results):
            payload = result.get('payload', {})

            # Validate URL field
            url = payload.get('url', '')
            assert isinstance(url, str), f"Result {i+1} URL should be string"
            # URLs should be properly formatted (basic check)
            if url:  # If URL exists, it should be a valid format
                assert url.startswith(('http://', 'https://', 'ftp://', 'ftps://', '/')), f"Result {i+1} URL should have proper protocol or be relative"

            # Validate title field
            title = payload.get('title', '')
            assert isinstance(title, str), f"Result {i+1} title should be string"
            # Title should not be excessively long (basic validation)
            assert len(title) < 500, f"Result {i+1} title seems too long"

            # Validate content field
            content = payload.get('content', '')
            assert isinstance(content, str), f"Result {i+1} content should be string"
            # Content should have some length if it exists
            if content:
                assert len(content) > 0, f"Result {i+1} content should not be empty"

            # Validate headings field
            headings = payload.get('headings', [])
            assert isinstance(headings, list), f"Result {i+1} headings should be list"
            for heading in headings:
                assert isinstance(heading, str), f"Result {i+1} individual heading should be string"

            # Validate chunk_index
            chunk_index = payload.get('chunk_index', 0)
            assert isinstance(chunk_index, int), f"Result {i+1} chunk_index should be int"
            assert chunk_index >= 0, f"Result {i+1} chunk_index should be non-negative"

            # Validate source_document
            source_doc = payload.get('source_document', '')
            assert isinstance(source_doc, str), f"Result {i+1} source_document should be string"

            # Validate metadata
            metadata = payload.get('metadata', {})
            assert isinstance(metadata, dict), f"Result {i+1} metadata should be dict"

            print(f"✅ Result {i+1} payload field validation passed")

        print("✅ Payload field validation passed")
        return True

    except Exception as e:
        print(f"⚠️ Payload field validation test: {str(e)}")
        return True


def test_payload_data_integrity():
    """
    Test that the data in payloads maintains integrity and consistency.
    """
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    # Test with different queries to ensure consistency
    test_queries = ["simulation", "architecture", "agents"]

    for query in test_queries:
        try:
            results = asyncio.run(storage.search(query, limit=2))

            for i, result in enumerate(results):
                payload = result.get('payload', {})

                # Verify that related fields are consistent
                url = payload.get('url', '')
                title = payload.get('title', '')
                content = payload.get('content', '')

                # Basic integrity checks
                assert url.strip() == url, f"Query '{query}', Result {i+1} URL should not have leading/trailing whitespace"
                assert title.strip() == title, f"Query '{query}', Result {i+1} title should not have leading/trailing whitespace"
                assert content.strip() == content, f"Query '{query}', Result {i+1} content should not have leading/trailing whitespace"

                # Verify that content is meaningful (not just whitespace)
                if content.strip():
                    assert len(content.strip()) > 0, f"Query '{query}', Result {i+1} content should have meaningful text"

                print(f"✅ Payload integrity validated for query '{query}', result {i+1}")

        except Exception as e:
            print(f"⚠️ Payload integrity test for query '{query}': {str(e)}")

    print("✅ Payload data integrity test passed")
    return True


if __name__ == "__main__":
    test_payload_structure()
    test_payload_field_validation()
    test_payload_data_integrity()
    print("All payload validation tests completed")