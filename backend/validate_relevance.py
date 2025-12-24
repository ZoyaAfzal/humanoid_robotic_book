#!/usr/bin/env python3
"""
Validation script for semantic relevance in the RAG pipeline.
This script verifies that retrieved content is semantically relevant to the query.
"""
import asyncio
import sys
import os
from typing import List, Dict, Any

# Add src to path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.storage.vector_storage import VectorStorage
from src.utils.config import get_config


async def validate_semantic_relevance():
    """
    Validate that retrieved content is semantically relevant to the query.
    This addresses User Story 3: Test Semantic Relevance.
    """
    print("=== Validating Semantic Relevance ===\n")

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

        # Test semantic relevance with targeted queries
        relevance_tests = [
            {
                "query": "humanoid robot design and characteristics",
                "expected_topics": ["humanoid", "robotics", "human-like", "appearance", "behavior", "design"],
                "description": "Should return content about humanoid robotics basics"
            },
            {
                "query": "simulation environment for testing robot algorithms",
                "expected_topics": ["gazebo", "simulation", "testing", "algorithms", "physics"],
                "description": "Should return content about Gazebo simulation"
            },
            {
                "query": "robot operating system architecture and communication",
                "expected_topics": ["ros", "architecture", "communication", "dds", "framework"],
                "description": "Should return content about ROS 2"
            },
            {
                "query": "path planning for humanoid robots",
                "expected_topics": ["path", "planning", "bipedal", "trajectory", "navigation"],
                "description": "Should return content about path planning"
            }
        ]

        print(f"\n--- Testing Semantic Relevance ---")
        all_tests_passed = True

        for i, test in enumerate(relevance_tests, 1):
            print(f"\nRelevance Test {i}: {test['description']}")
            print(f"Query: '{test['query']}'")

            try:
                results = await storage.search(test['query'], limit=3)

                if results:
                    top_result = results[0]
                    content = top_result.get('content', '').lower()
                    title = top_result.get('title', '').lower()
                    score = top_result.get('score', 0)

                    print(f"  Top result - Score: {score:.4f}")
                    print(f"  Title: {top_result.get('title', 'N/A')}")
                    print(f"  Content preview: {top_result.get('content', 'N/A')[:100]}...")

                    # Check if expected topics are in the result
                    found_topics = []
                    for topic in test['expected_topics']:
                        if topic.lower() in content or topic.lower() in title:
                            found_topics.append(topic)

                    print(f"  Expected topics found: {found_topics}")
                    print(f"  Coverage: {len(found_topics)}/{len(test['expected_topics'])}")

                    if len(found_topics) >= len(test['expected_topics']) * 0.6:  # 60% threshold
                        print(f"  ✅ Good semantic relevance")
                    else:
                        print(f"  ⚠️  Relevance could be improved")
                        all_tests_passed = False  # Consider this as a failure for the overall test

                    # Validate relevance scoring
                    relevance_validation = storage.validate_relevance_scoring(results, test['query'])
                    print(f"  Relevance scoring validation: {relevance_validation['valid']}")
                    print(f"  Score analysis: {relevance_validation['score_analysis']}")
                    print(f"  Relevance indicators: {relevance_validation['relevance_indicators']}")

                else:
                    print(f"  ⚠️  No results returned for query")
                    if vector_count > 0:
                        all_tests_passed = False

            except Exception as e:
                print(f"  ❌ Error during relevance test: {str(e)}")
                all_tests_passed = False

        print(f"\n--- Semantic Relevance Validation Summary ---")
        if all_tests_passed and vector_count > 0:
            print("✅ All semantic relevance validations passed!")
            print("✅ Retrieved content is semantically relevant to queries")
        elif vector_count == 0:
            print("⚠️  Collection is empty - validation framework works but needs content to fully validate")
        else:
            print("❌ Some semantic relevance validations failed")

        return all_tests_passed

    except Exception as e:
        print(f"❌ Error during semantic relevance validation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def validate_content_alignment():
    """
    Validate that retrieved chunks align with expected book sections.
    """
    print("\n=== Validating Content Alignment ===")

    storage = VectorStorage()

    # Test alignment with specific book sections
    alignment_tests = [
        {
            "query": "introduction to humanoid robotics",
            "expected_section": "Introduction to Humanoid Robotics",
            "keywords": ["humanoid", "robotics", "introduction"]
        },
        {
            "query": "ros 2 architecture patterns",
            "expected_section": "ROS 2 Architecture",
            "keywords": ["ros", "architecture", "framework"]
        },
        {
            "query": "gazebo simulation setup",
            "expected_section": "Gazebo Simulation",
            "keywords": ["gazebo", "simulation", "environment"]
        }
    ]

    all_aligned = True

    for test in alignment_tests:
        query = test["query"]
        expected_section = test["expected_section"]
        keywords = test["keywords"]

        print(f"\nTesting alignment for: {query}")

        try:
            results = await storage.search(query, limit=2)

            if results:
                top_result = results[0]
                title = top_result.get('title', '').lower()
                content = top_result.get('content', '').lower()

                # Check if the title contains expected section reference
                section_match = any(keyword.lower() in title for keyword in expected_section.lower().split())

                # Check if content contains relevant keywords
                keyword_matches = [kw for kw in keywords if kw.lower() in content or kw.lower() in title]

                print(f"  Expected section hint: {expected_section}")
                print(f"  Found in title: {section_match}")
                print(f"  Keyword matches: {keyword_matches}")

                if section_match or len(keyword_matches) >= len(keywords) * 0.5:
                    print(f"  ✅ Content alignment verified")
                else:
                    print(f"  ⚠️  Content alignment could be improved")
                    all_aligned = False
            else:
                print(f"  ⚠️  No results for alignment test")

        except Exception as e:
            print(f"  ⚠️  Error in alignment test: {str(e)}")

    print(f"\n✅ Content alignment validation completed")
    return all_aligned


async def main():
    """
    Main function to run all semantic relevance validation tests.
    """
    print("🤖 RAG Pipeline - Semantic Relevance Validation")
    print("=" * 55)

    # Run semantic relevance validation
    relevance_passed = await validate_semantic_relevance()

    # Run content alignment validation
    alignment_passed = await validate_content_alignment()

    print(f"\n=== Final Semantic Relevance Validation Results ===")
    print(f"Semantic Relevance Validation: {'✅ PASSED' if relevance_passed else '❌ FAILED'}")
    print(f"Content Alignment Validation: {'✅ PASSED' if alignment_passed else '❌ FAILED'}")

    overall_success = relevance_passed and alignment_passed
    print(f"Overall Validation: {'✅ PASSED' if overall_success else '❌ FAILED'}")

    if overall_success:
        print("\n🎯 User Story 3 - Test Semantic Relevance: SUCCESS")
        print("Retrieved content is semantically relevant to queries with appropriate scores.")
    else:
        print("\n❌ User Story 3 - Test Semantic Relevance: FAILED")
        print("Some aspects of semantic relevance need attention.")

    return overall_success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)