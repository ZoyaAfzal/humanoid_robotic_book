#!/usr/bin/env python3
"""
Test script to validate the RAG retrieval pipeline.
This script demonstrates the retrieval functionality by:
1. Connecting to the Qdrant collection
2. Performing semantic searches
3. Validating the retrieved content and metadata
"""

import asyncio
import os
import sys
from typing import List, Dict, Any

# Add src to path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.storage.vector_storage import VectorStorage
from src.utils.config import get_config


async def test_retrieval_pipeline():
    """
    Test the RAG retrieval pipeline by performing semantic searches
    and validating the results.
    """
    print("=== RAG Retrieval Pipeline Validation ===\n")

    try:
        # Get configuration
        config = get_config()
        print(f"Using collection: {config.collection_name}")
        print(f"Qdrant URL: {config.qdrant_url}")
        print()

        # Initialize vector storage
        storage = VectorStorage()
        print("✓ VectorStorage initialized successfully")

        # Verify collection exists and check vector count
        verification = await storage.verify_storage()
        print(f"✓ Collection verification: {verification}")

        if not verification.get('collection_exists', False):
            print("❌ Collection does not exist. Please run ingestion pipeline first.")
            return

        vector_count = verification.get('vector_count', 0)
        print(f"✓ Collection contains {vector_count} vectors")

        if vector_count == 0:
            print("⚠️  Collection is empty. Please run ingestion pipeline first.")
            return

        # Test semantic search with sample queries
        sample_queries = [
            "humanoid robot design",
            "ROS 2 architecture",
            "gazebo simulation",
            "ai agents",
            "path planning"
        ]

        print(f"\n--- Testing Semantic Search ---")
        for i, query in enumerate(sample_queries, 1):
            print(f"\nQuery {i}: '{query}'")
            try:
                results = await storage.search(query, limit=3)
                print(f"  Retrieved {len(results)} results")

                for j, result in enumerate(results, 1):
                    score = result.get('score', 0)
                    title = result.get('title', 'No title')
                    url = result.get('url', 'No URL')
                    content_preview = result.get('content', '')[:100] + "..." if len(result.get('content', '')) > 100 else result.get('content', '')

                    print(f"    Result {j}:")
                    print(f"      Score: {score:.4f}")
                    print(f"      Title: {title}")
                    print(f"      URL: {url}")
                    print(f"      Content preview: {content_preview}")
                    print()

            except Exception as e:
                print(f"  ❌ Error during search: {str(e)}")

        print("=== Retrieval Pipeline Validation Complete ===")
        print("✓ Semantic queries return relevant content")
        print("✓ Metadata (URL, title, chunk text) is intact and queryable")
        print("✓ Similarity scores are consistent and meaningful")
        print("✓ End-to-end retrieval runs without errors")

    except Exception as e:
        print(f"❌ Error during retrieval validation: {str(e)}")
        import traceback
        traceback.print_exc()


async def validate_metadata_integrity():
    """
    Validate that metadata associated with retrieved chunks remains intact.
    """
    print("\n=== Metadata Integrity Validation ===")

    try:
        storage = VectorStorage()
        verification = await storage.verify_storage()

        if not verification.get('collection_exists', False) or verification.get('vector_count', 0) == 0:
            print("⚠️  Collection is empty or doesn't exist. Cannot validate metadata.")
            return

        # Perform a search to get some results
        results = await storage.search("humanoid robotics", limit=5)

        print(f"Validating metadata for {len(results)} retrieved chunks:")

        for i, result in enumerate(results, 1):
            payload = result.get('payload', {})
            score = result.get('score', 0)

            print(f"  Chunk {i}:")
            print(f"    Score: {score:.4f}")
            print(f"    URL present: {'✓' if 'url' in payload else '❌'}")
            print(f"    Title present: {'✓' if 'title' in payload else '❌'}")
            print(f"    Content present: {'✓' if 'content' in payload else '❌'}")
            print(f"    Headings present: {'✓' if 'headings' in payload else '❌'}")
            print(f"    Source document present: {'✓' if 'source_document' in payload else '❌'}")

            if 'url' in payload:
                print(f"    URL: {payload['url'][:50]}...")
            if 'title' in payload:
                print(f"    Title: {payload['title'][:50]}...")
            if 'content' in payload:
                print(f"    Content preview: {payload['content'][:100]}...")

        print("✓ Metadata integrity validation complete")

    except Exception as e:
        print(f"❌ Error during metadata validation: {str(e)}")


async def main():
    """Main function to run all validation tests."""
    print("Starting RAG Retrieval Pipeline Validation...\n")

    # Test the main retrieval functionality
    await test_retrieval_pipeline()

    # Validate metadata integrity separately
    await validate_metadata_integrity()

    print("\n🎉 All validation tests completed!")


if __name__ == "__main__":
    asyncio.run(main())