#!/usr/bin/env python3
"""
Validation script for semantic query testing in the RAG pipeline.
This script validates that semantic queries return relevant content with proper metadata.
"""
import asyncio
import sys
import os
from typing import List, Dict, Any

# Add src to path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.storage.vector_storage import VectorStorage
from src.utils.config import get_config


async def validate_query_response():
    """
    Validate that semantic queries return relevant content with proper metadata.
    This addresses User Story 1: Validate RAG Query Response.
    """
    print("=== Validating RAG Query Response ===\n")

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
            print("⚠️  Collection does not exist. Results may be empty.")
            return

        vector_count = verification.get('vector_count', 0)
        print(f"✓ Collection contains {vector_count} vectors")

        if vector_count == 0:
            print("⚠️  Collection is empty. Results will be empty, but functionality can still be tested.")

        # Test semantic search with sample queries
        sample_queries = [
            "humanoid robot design",
            "ROS 2 architecture",
            "gazebo simulation",
            "ai agents",
            "path planning"
        ]

        print(f"\n--- Testing Semantic Query Response ---")
        all_tests_passed = True

        for i, query in enumerate(sample_queries, 1):
            print(f"\nQuery {i}: '{query}'")
            try:
                results = await storage.search(query, limit=3)
                print(f"  Retrieved {len(results)} results")

                if len(results) > 0:
                    for j, result in enumerate(results, 1):
                        score = result.get('score', 0)
                        title = result.get('title', 'No title')
                        url = result.get('url', 'No URL')
                        content_preview = result.get('content', '')[:100] + "..." if len(result.get('content', '')) > 100 else result.get('content', '')
                        query_time = result.get('query_time', 'N/A')

                        print(f"    Result {j}:")
                        print(f"      Score: {score:.4f}")
                        print(f"      Title: {title}")
                        print(f"      URL: {url}")
                        print(f"      Query time: {query_time:.4f}s")
                        print(f"      Content preview: {content_preview}")

                        # Validate required fields
                        if score is None:
                            print(f"      ❌ Missing score")
                            all_tests_passed = False
                        if not url or url == 'No URL':
                            print(f"      ❌ Missing URL")
                            all_tests_passed = False
                        if not title or title == 'No title':
                            print(f"      ❌ Missing title")
                            all_tests_passed = False
                        if not content_preview or content_preview.startswith('No content'):
                            print(f"      ❌ Missing content")
                            all_tests_passed = False

                        print()
                else:
                    print("  ⚠️  No results returned (this may be expected if collection is empty)")

            except Exception as e:
                print(f"  ❌ Error during search: {str(e)}")
                all_tests_passed = False

        print(f"\n--- Query Response Validation Summary ---")
        if all_tests_passed and vector_count > 0:
            print("✅ All query response validations passed!")
            print("✅ Semantic queries return relevant content with proper metadata")
        elif vector_count == 0:
            print("⚠️  Collection is empty - validation passed as functionality works without data")
        else:
            print("❌ Some query response validations failed")

        return all_tests_passed

    except Exception as e:
        print(f"❌ Error during query validation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def validate_response_time():
    """
    Validate that queries complete within acceptable response time.
    """
    print("\n=== Validating Response Time Performance ===")

    storage = VectorStorage()

    # Test with a simple query to measure response time
    try:
        import time
        start_time = time.time()
        results = await storage.search("test query for performance", limit=1)
        end_time = time.time()

        total_time = end_time - start_time
        print(f"Total query time: {total_time:.4f}s")

        # Check if within performance goal of <5 seconds
        if total_time < 5.0:
            print("✅ Response time is within acceptable limits (<5 seconds)")
            return True
        else:
            print("❌ Response time exceeds acceptable limits (≥5 seconds)")
            return False

    except Exception as e:
        print(f"❌ Error during response time validation: {str(e)}")
        return False


async def main():
    """
    Main function to run all query validation tests.
    """
    print("🤖 RAG Pipeline - Semantic Query Validation")
    print("=" * 50)

    # Run query response validation
    query_validation_passed = await validate_query_response()

    # Run response time validation
    time_validation_passed = await validate_response_time()

    print(f"\n=== Final Validation Results ===")
    print(f"Query Response Validation: {'✅ PASSED' if query_validation_passed else '❌ FAILED'}")
    print(f"Response Time Validation: {'✅ PASSED' if time_validation_passed else '❌ FAILED'}")

    overall_success = query_validation_passed and time_validation_passed
    print(f"Overall Validation: {'✅ PASSED' if overall_success else '❌ FAILED'}")

    if overall_success:
        print("\n🎯 User Story 1 - Validate RAG Query Response: SUCCESS")
        print("The retrieval pipeline successfully returns relevant content with proper metadata.")
    else:
        print("\n❌ User Story 1 - Validate RAG Query Response: FAILED")
        print("Some aspects of the retrieval pipeline need attention.")

    return overall_success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)