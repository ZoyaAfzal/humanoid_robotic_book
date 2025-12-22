#!/usr/bin/env python3
"""
Script to verify the Qdrant storage and test semantic search capability.
"""

import json
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

def test_semantic_search():
    """
    Test semantic search functionality in the Qdrant database.
    """
    # Initialize Qdrant client
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    cohere_api_key = os.getenv("COHERE_API_KEY")

    if not qdrant_url or not qdrant_api_key or not cohere_api_key:
        raise ValueError("Please set QDRANT_URL, QDRANT_API_KEY, and COHERE_API_KEY environment variables")

    qdrant_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True
    )

    co = cohere.Client(cohere_api_key)

    collection_name = "humanoid_robotics_book"

    # Test embedding a query
    query_text = "How to set up development environment for humanoid robotics?"
    query_embedding = co.embed(
        texts=[query_text],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings[0]

    # Determine the correct search method by trying each one in order of preference
    search_results = None
    last_exception = None

    # Try the most modern method first
    try:
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=5,  # Return top 5 results
            with_payload=True
        )
    except AttributeError as e:
        last_exception = e
    except Exception as e:
        # If it's not an AttributeError, the method exists but had another issue
        last_exception = e

    # If search failed, try search_points (older method)
    if search_results is None:
        try:
            search_results = qdrant_client.search_points(
                collection_name=collection_name,
                vector=query_embedding,
                limit=5,
                with_payload=True
            )
        except AttributeError as e:
            last_exception = e
        except Exception as e:
            last_exception = e

    # If both failed, try query_points (another version)
    if search_results is None:
        try:
            search_results = qdrant_client.query_points(
                collection_name=collection_name,
                query=query_embedding,
                limit=5,
                with_payload=True
            )
        except AttributeError as e:
            last_exception = e
        except Exception as e:
            last_exception = e

    # If all methods failed, raise an error
    if search_results is None:
        raise last_exception or AttributeError("Qdrant client does not have a recognized search method.")

    print("Semantic Search Results:")
    print("="*50)
    for i, result in enumerate(search_results, 1):
        # Handle different result formats from different Qdrant methods
        # Modern search() method returns objects with attributes
        # Older search_points() might return different formats
        if isinstance(result, tuple):
            # This might be from an older method returning tuples
            # Assuming format (payload, score) or similar
            if len(result) == 2:
                raw_payload, score = result
            else:
                # Unknown tuple format, try to extract score differently
                # Attempt to find score in the tuple
                raw_payload = result[0] if len(result) > 0 else {}
                score = result[1] if len(result) > 1 else 0.0
            # Ensure payload is always a dictionary
            if isinstance(raw_payload, dict):
                payload = raw_payload
            elif isinstance(raw_payload, str):
                # If raw_payload is a string, we need to handle it appropriately
                # For Qdrant results, payload should be a dictionary with metadata
                print(f"Warning: Received string payload instead of dictionary: {type(raw_payload)}")
                payload = {}
            else:
                # For other types, try to convert or default to empty dict
                payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
        elif hasattr(result, '__getitem__') and not isinstance(result, str):
            # This could be a dictionary-like object
            raw_payload = result.get('payload', result if isinstance(result, dict) else {})
            # Ensure payload is a dictionary
            if isinstance(raw_payload, dict):
                payload = raw_payload
            elif isinstance(raw_payload, str):
                print(f"Warning: Received string payload instead of dictionary: {type(raw_payload)}")
                payload = {}
            else:
                payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
            score = result.get('score', result.get('score', 0.0))
        elif hasattr(result, 'score'):
            # This is from the modern search method
            score = result.score
            raw_payload = getattr(result, 'payload', {})  # Use getattr for safety
            # Ensure payload is a dictionary
            if isinstance(raw_payload, dict):
                payload = raw_payload
            elif isinstance(raw_payload, str):
                print(f"Warning: Received string payload instead of dictionary: {type(raw_payload)}")
                payload = {}
            else:
                payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
        else:
            # Unknown format, use default
            raw_payload = getattr(result, 'payload', {})
            # Ensure payload is a dictionary
            if isinstance(raw_payload, dict):
                payload = raw_payload
            elif isinstance(raw_payload, str):
                print(f"Warning: Received string payload instead of dictionary: {type(raw_payload)}")
                payload = {}
            else:
                payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
            # Try to get score from various possible attributes
            score = getattr(result, 'score',
                           getattr(result, 'score_',
                           getattr(result, 'similarity', 0.0)))

        print(f"{i}. Score: {score:.4f}")
        print(f"   Title: {payload.get('title', 'N/A')}")
        print(f"   URL: {payload.get('url', 'N/A')}")
        print(f"   Content Preview: {payload.get('content', '')[:200]}...")
        print()

    # Test another query
    query_text2 = "ROS 2 architecture for humanoid robots"
    query_embedding2 = co.embed(
        texts=[query_text2],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings[0]

    # Determine the correct search method by trying each one in order of preference for the second query
    search_results2 = None
    last_exception2 = None

    # Try the most modern method first
    try:
        search_results2 = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding2,
            limit=5,
            with_payload=True
        )
    except AttributeError as e:
        last_exception2 = e
    except Exception as e:
        # If it's not an AttributeError, the method exists but had another issue
        last_exception2 = e

    # If search failed, try search_points (older method)
    if search_results2 is None:
        try:
            search_results2 = qdrant_client.search_points(
                collection_name=collection_name,
                vector=query_embedding2,
                limit=5,
                with_payload=True
            )
        except AttributeError as e:
            last_exception2 = e
        except Exception as e:
            last_exception2 = e

    # If both failed, try query_points (another version)
    if search_results2 is None:
        try:
            search_results2 = qdrant_client.query_points(
                collection_name=collection_name,
                query=query_embedding2,
                limit=5,
                with_payload=True
            )
        except AttributeError as e:
            last_exception2 = e
        except Exception as e:
            last_exception2 = e

    # If all methods failed, raise an error
    if search_results2 is None:
        raise last_exception2 or AttributeError("Qdrant client does not have a recognized search method.")

    print("Semantic Search Results for 'ROS 2 architecture':")
    print("="*50)
    for i, result in enumerate(search_results2, 1):
        # Handle different result formats from different Qdrant methods
        # Modern search() method returns objects with attributes
        # Older search_points() might return different formats
        if isinstance(result, tuple):
            # This might be from an older method returning tuples
            # Assuming format (payload, score) or similar
            if len(result) == 2:
                raw_payload, score = result
            else:
                # Unknown tuple format, try to extract score differently
                # Attempt to find score in the tuple
                raw_payload = result[0] if len(result) > 0 else {}
                score = result[1] if len(result) > 1 else 0.0
            # Ensure payload is always a dictionary
            if isinstance(raw_payload, dict):
                payload = raw_payload
            elif isinstance(raw_payload, str):
                # If raw_payload is a string, we need to handle it appropriately
                # For Qdrant results, payload should be a dictionary with metadata
                print(f"Warning: Received string payload instead of dictionary: {type(raw_payload)}")
                payload = {}
            else:
                # For other types, try to convert or default to empty dict
                payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
        elif hasattr(result, '__getitem__') and not isinstance(result, str):
            # This could be a dictionary-like object
            raw_payload = result.get('payload', result if isinstance(result, dict) else {})
            # Ensure payload is a dictionary
            if isinstance(raw_payload, dict):
                payload = raw_payload
            elif isinstance(raw_payload, str):
                print(f"Warning: Received string payload instead of dictionary: {type(raw_payload)}")
                payload = {}
            else:
                payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
            score = result.get('score', result.get('score', 0.0))
        elif hasattr(result, 'score'):
            # This is from the modern search method
            score = result.score
            raw_payload = getattr(result, 'payload', {})  # Use getattr for safety
            # Ensure payload is a dictionary
            if isinstance(raw_payload, dict):
                payload = raw_payload
            elif isinstance(raw_payload, str):
                print(f"Warning: Received string payload instead of dictionary: {type(raw_payload)}")
                payload = {}
            else:
                payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
        else:
            # Unknown format, use default
            raw_payload = getattr(result, 'payload', {})
            # Ensure payload is a dictionary
            if isinstance(raw_payload, dict):
                payload = raw_payload
            elif isinstance(raw_payload, str):
                print(f"Warning: Received string payload instead of dictionary: {type(raw_payload)}")
                payload = {}
            else:
                payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
            # Try to get score from various possible attributes
            score = getattr(result, 'score',
                           getattr(result, 'score_',
                           getattr(result, 'similarity', 0.0)))

        print(f"{i}. Score: {score:.4f}")
        print(f"   Title: {payload.get('title', 'N/A')}")
        print(f"   URL: {payload.get('url', 'N/A')}")
        print(f"   Content Preview: {payload.get('content', '')[:200]}...")
        print()

    # Get collection info
    collection_info = qdrant_client.get_collection(collection_name)
    print(f"Collection '{collection_name}' contains {collection_info.points_count} vectors")
    print(f"Vector size: {collection_info.config.params.vectors.size}")
    print(f"Distance metric: {collection_info.config.params.vectors.distance}")

def main():
    print("Verifying Qdrant storage and testing semantic search...")
    test_semantic_search()
    print("\nVerification complete!")

if __name__ == "__main__":
    main()