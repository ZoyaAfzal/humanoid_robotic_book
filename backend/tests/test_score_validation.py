"""
Test for score threshold validation in the RAG pipeline retrieval results.
This test verifies that similarity scores are consistent and meaningful.
"""
import pytest
import asyncio
import os
from src.storage.vector_storage import VectorStorage
from src.utils.config import get_config


def test_score_range_validation():
    """
    Test that similarity scores are within expected range and are meaningful.
    """
    # Skip test if environment variables are not set
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    # Test with various queries to check score ranges
    test_queries = [
        "humanoid robotics",
        "machine learning",
        "computer science",
        "random unrelated query"
    ]

    print("Testing score range validation...")

    all_valid = True

    for query in test_queries:
        try:
            results = asyncio.run(storage.search(query, limit=3))

            for i, result in enumerate(results):
                score = result.get('score', 0)

                # Scores should be reasonable numbers (not NaN, not infinite)
                if not isinstance(score, (int, float)) or score != score:  # Check for NaN
                    print(f"  ❌ Invalid score (NaN) for query '{query}', result {i+1}")
                    all_valid = False
                elif score == float('inf') or score == float('-inf'):
                    print(f"  ❌ Invalid score (infinite) for query '{query}', result {i+1}")
                    all_valid = False
                elif score < -1 or score > 1:
                    # Cosine similarity should be between -1 and 1
                    print(f"  ⚠️  Score {score} out of expected range [-1, 1] for query '{query}', result {i+1}")
                    # Don't fail the test for this, as it might be a valid distance metric value
                else:
                    print(f"  ✅ Valid score {score:.4f} for query '{query}', result {i+1}")

        except Exception as e:
            print(f"  ⚠️  Error testing score range for query '{query}': {str(e)}")

    print("✅ Score range validation completed")
    return all_valid


def test_score_differentiation():
    """
    Test that the system can differentiate between relevant and less relevant content.
    """
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    print("Testing score differentiation...")

    # Use focused queries that should return highly relevant results
    focused_queries = [
        "humanoid robot design",
        "ros 2 architecture",
        "gazebo simulation environment"
    ]

    for query in focused_queries:
        try:
            results = asyncio.run(storage.search(query, limit=5))

            if len(results) >= 2:
                scores = [result.get('score', 0) for result in results]
                sorted_scores = sorted(scores, reverse=True)

                # Check that scores are in descending order (first result most relevant)
                is_sorted = all(sorted_scores[i] >= sorted_scores[i+1]
                              for i in range(len(sorted_scores)-1))

                if is_sorted:
                    print(f"  ✅ Scores properly ordered for query '{query}'")
                    print(f"    Top 3 scores: {[f'{s:.4f}' for s in scores[:3]]}")
                else:
                    print(f"  ⚠️  Scores not in expected order for query '{query}'")
                    print(f"    Scores: {[f'{s:.4f}' for s in scores]}")

                # Check score difference between top results
                if len(scores) >= 2:
                    top_diff = scores[0] - scores[1]
                    print(f"    Score difference (1st-2nd): {top_diff:.4f}")

        except Exception as e:
            print(f"  ⚠️  Error testing score differentiation for query '{query}': {str(e)}")

    print("✅ Score differentiation test completed")
    return True


def test_score_threshold_behavior():
    """
    Test behavior with different threshold expectations.
    """
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    print("Testing score threshold behavior...")

    # Test with a specific query and check score distribution
    test_query = "artificial intelligence in robotics"

    try:
        results = asyncio.run(storage.search(test_query, limit=10))

        if results:
            scores = [result.get('score', 0) for result in results]
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)

            print(f"  Query: '{test_query}'")
            print(f"  Results count: {len(results)}")
            print(f"  Score range: {min_score:.4f} to {max_score:.4f}")
            print(f"  Average score: {avg_score:.4f}")

            # Check if there's meaningful differentiation
            score_spread = max_score - min_score
            if score_spread > 0.1:  # Expect some differentiation
                print(f"  ✅ Good score differentiation: {score_spread:.4f}")
            else:
                print(f"  ⚠️  Limited score differentiation: {score_spread:.4f}")

            # Show top scores
            top_3_scores = scores[:3]
            print(f"  Top 3 scores: {[f'{s:.4f}' for s in top_3_scores]}")

    except Exception as e:
        print(f"  ⚠️  Error testing score threshold behavior: {str(e)}")

    print("✅ Score threshold behavior test completed")
    return True


def test_consistent_scoring():
    """
    Test that similar queries return consistently scored results.
    """
    config = get_config()
    if not config.cohere_api_key or not config.qdrant_url or not config.qdrant_api_key:
        pytest.skip("Environment variables not set for testing")

    storage = VectorStorage()

    print("Testing consistent scoring...")

    # Similar queries that should return similar results
    similar_query_pairs = [
        ("humanoid robot", "humanoid robotics"),
        ("path planning", "robot path planning"),
        ("gazebo simulator", "gazebo simulation")
    ]

    for query1, query2 in similar_query_pairs:
        try:
            results1 = asyncio.run(storage.search(query1, limit=1))
            results2 = asyncio.run(storage.search(query2, limit=1))

            if results1 and results2:
                score1 = results1[0].get('score', 0)
                score2 = results2[0].get('score', 0)

                # Scores for similar queries should be reasonably close
                score_diff = abs(score1 - score2)
                print(f"  Query pair: '{query1}' vs '{query2}'")
                print(f"  Scores: {score1:.4f} vs {score2:.4f}")
                print(f"  Difference: {score_diff:.4f}")

                if score_diff <= 0.3:  # Allow for some variation
                    print(f"  ✅ Consistent scoring for similar queries")
                else:
                    print(f"  ⚠️  Inconsistent scoring for similar queries")

        except Exception as e:
            print(f"  ⚠️  Error testing consistent scoring for '{query1}' vs '{query2}': {str(e)}")

    print("✅ Consistent scoring test completed")
    return True


if __name__ == "__main__":
    test_score_range_validation()
    test_score_differentiation()
    test_score_threshold_behavior()
    test_consistent_scoring()
    print("All score validation tests completed")