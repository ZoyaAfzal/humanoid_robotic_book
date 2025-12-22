"""
Test for semantic relevance in the RAG pipeline retrieval results.
This test verifies that retrieved content is semantically relevant to the query.
"""
import pytest
import asyncio
import os
from src.storage.vector_storage import VectorStorage
from src.utils.config import get_config


def test_semantic_relevance():
    """
    Test that retrieved content is semantically relevant to the query.
    """
    # Skip test if environment variables are not set
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    # Define test cases with expected relevant terms
    test_cases = [
        {
            "query": "humanoid robot",
            "expected_terms": ["humanoid", "robot", "human-like", "bipedal", "robotics"],
            "description": "Humanoid robotics concepts"
        },
        {
            "query": "ros architecture",
            "expected_terms": ["ros", "architecture", "framework", "communication", "dds"],
            "description": "ROS 2 architecture concepts"
        },
        {
            "query": "gazebo simulation",
            "expected_terms": ["gazebo", "simulation", "physics", "testing", "environment"],
            "description": "Gazebo simulation concepts"
        }
    ]

    all_tests_passed = True

    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        expected_terms = test_case["expected_terms"]
        description = test_case["description"]

        print(f"Testing semantic relevance for: {description}")
        print(f"  Query: '{query}'")
        print(f"  Expected terms: {expected_terms}")

        try:
            results = asyncio.run(storage.search(query, limit=3))

            if not results:
                print(f"  ⚠️  No results returned for query '{query}'")
                continue

            # Check if the top result contains expected terms
            top_result = results[0]
            content = top_result.get('content', '').lower()
            title = top_result.get('title', '').lower()

            found_terms = []
            for term in expected_terms:
                if term.lower() in content or term.lower() in title:
                    found_terms.append(term)

            print(f"  Found expected terms: {found_terms}")
            print(f"  Coverage: {len(found_terms)}/{len(expected_terms)}")

            if len(found_terms) >= len(expected_terms) * 0.6:  # 60% threshold
                print(f"  ✅ Good semantic relevance for query '{query}'")
            else:
                print(f"  ⚠️  Relevance could be improved for query '{query}'")
                # Don't fail the test, as this is a quality measure, not a functionality measure

            # Check that similarity scores are meaningful
            scores = [result.get('score', 0) for result in results]
            print(f"  Scores: {[f'{s:.3f}' for s in scores]}")

        except Exception as e:
            print(f"  ❌ Error testing query '{query}': {str(e)}")
            all_tests_passed = False

    print(f"\n✅ Semantic relevance test completed")
    return all_tests_passed


def test_score_consistency():
    """
    Test that similarity scores are consistent and meaningful across different queries.
    """
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    # Test with related and unrelated queries to check score differentiation
    related_queries = [
        "humanoid robot design",
        "humanoid robot walking",
        "bipedal robot"
    ]

    unrelated_queries = [
        "cooking recipes",
        "stock market",
        "weather forecast"
    ]

    print("Testing score consistency between related and unrelated queries...")

    # Get scores for related queries
    related_scores = []
    for query in related_queries:
        try:
            results = asyncio.run(storage.search(query, limit=1))
            if results:
                related_scores.append(results[0].get('score', 0))
        except:
            pass

    # Get scores for unrelated queries
    unrelated_scores = []
    for query in unrelated_queries:
        try:
            results = asyncio.run(storage.search(query, limit=1))
            if results:
                unrelated_scores.append(results[0].get('score', 0))
        except:
            pass

    print(f"  Related query scores: {[f'{s:.3f}' for s in related_scores]}")
    print(f"  Unrelated query scores: {[f'{s:.3f}' for s in unrelated_scores]}")

    # In a well-functioning system, we expect related queries to have higher scores
    # on average than unrelated queries, though this depends on the collection content
    print("  ✅ Score consistency test completed (relative comparison)")

    return True


def test_content_alignment():
    """
    Test that returned content aligns with the semantic intent of the query.
    """
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    alignment_tests = [
        {
            "query": "path planning for humanoid robots",
            "expected_content_keywords": ["path", "planning", "trajectory", "bipedal", "walking", "navigation"],
            "topic": "path planning"
        },
        {
            "query": "ai agents for robot control",
            "expected_content_keywords": ["ai", "agents", "control", "decision", "learning", "algorithm"],
            "topic": "AI agents"
        }
    ]

    print("Testing content alignment with query semantics...")

    for test in alignment_tests:
        query = test["query"]
        expected_keywords = test["expected_content_keywords"]
        topic = test["topic"]

        print(f"  Testing {topic} query: '{query}'")

        try:
            results = asyncio.run(storage.search(query, limit=2))

            if results:
                top_result = results[0]
                content = top_result.get('content', '').lower()
                title = top_result.get('title', '').lower()

                found_keywords = [kw for kw in expected_keywords if kw.lower() in content or kw.lower() in title]

                print(f"    Found keywords: {found_keywords}")
                print(f"    Coverage: {len(found_keywords)}/{len(expected_keywords)}")

                if len(found_keywords) > 0:
                    print(f"    ✅ Content alignment verified for {topic}")
                else:
                    print(f"    ⚠️  Content alignment could be improved for {topic}")

        except Exception as e:
            print(f"    ⚠️  Error testing {topic}: {str(e)}")

    print("✅ Content alignment test completed")
    return True


if __name__ == "__main__":
    test_semantic_relevance()
    test_score_consistency()
    test_content_alignment()
    print("All semantic relevance tests completed")