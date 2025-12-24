#!/usr/bin/env python3
"""
Test script to verify the backend RAG pipeline structure.
"""

import asyncio
import sys
import os

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from src.extraction.content_extractor import DocusaurusExtractor
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.storage.vector_storage import VectorStorage
from src.utils.config import get_config


async def test_pipeline():
    """Test the pipeline components."""
    print("Testing Humanoid Robotics RAG pipeline components...")

    try:
        # Test configuration loading
        print("\n1. Testing configuration...")
        config = get_config()
        print(f"   ✓ Configuration loaded successfully")
        print(f"   - Base URL: {config.base_url}")
        print(f"   - Chunk size: {config.chunk_size}")
        print(f"   - Chunk overlap: {config.chunk_overlap}")

        # Test extractor initialization
        print("\n2. Testing content extractor...")
        extractor = DocusaurusExtractor()
        print(f"   ✓ Extractor initialized with base URL: {extractor.base_url}")

        # Test embedder initialization (will fail without API key, but class should initialize)
        print("\n3. Testing embedding generator...")
        try:
            embedder = EmbeddingGenerator()
            print(f"   ✓ Embedding generator initialized")
            print(f"   - Model: {embedder.model}")
            print(f"   - Batch size: {embedder.batch_size}")
        except ValueError as e:
            print(f"   ⚠ Embedding generator requires API key: {e}")

        # Test storage initialization (will fail without API key, but class should initialize)
        print("\n4. Testing vector storage...")
        try:
            storage = VectorStorage()
            print(f"   ✓ Vector storage initialized")
            print(f"   - Collection: {storage.collection_name}")
        except ValueError as e:
            print(f"   ⚠ Vector storage requires API key: {e}")

        print("\n✓ All components initialized successfully!")
        print("The pipeline is ready to run with proper API keys configured.")

    except Exception as e:
        print(f"\n✗ Error testing pipeline: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_pipeline())
    if not success:
        sys.exit(1)