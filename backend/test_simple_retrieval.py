#!/usr/bin/env python3
"""
Simple script to check Qdrant collection status and run a quick test
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.storage.vector_storage import VectorStorage
from src.utils.config import get_config

async def check_and_test():
    config = get_config()
    print(f"Using collection: {config.collection_name}")

    storage = VectorStorage()

    # Try to create the collection if it doesn't exist
    try:
        storage.initialize_collection()
        print("✓ Collection initialized")
    except Exception as e:
        print(f"❌ Error initializing collection: {e}")
        return

    # Check collection status
    verification = await storage.verify_storage()
    print(f"Collection verification: {verification}")

    # If collection is empty, let's try to add a simple test entry
    if verification.get('vector_count', 0) == 0:
        print("Collection is empty. Creating a test entry...")

        # Create a simple test entry using the vector storage directly
        import random
        from qdrant_client.http import models
        from qdrant_client.http.models import PointStruct

        # Create a simple embedding for testing (using a dummy vector)
        test_embedding = [0.1] * 1024  # Dummy embedding vector

        try:
            storage.client.upsert(
                collection_name=storage.collection_name,
                points=[
                    PointStruct(
                        id=random.randint(1, 1000000),  # Use smaller random ID to avoid range issues
                        vector=test_embedding,
                        payload={
                            'url': 'https://test.example.com',
                            'title': 'Test Document',
                            'content': 'This is a test document for the RAG pipeline validation. It contains information about humanoid robotics and AI.',
                            'headings': ['Test Heading'],
                            'chunk_index': 0,
                            'source_document': 'test_doc',
                            'metadata': {'test': True}
                        }
                    )
                ]
            )
            print("✓ Test entry added successfully")

            # Verify again
            verification = await storage.verify_storage()
            print(f"Updated verification: {verification}")

        except Exception as e:
            print(f"❌ Error adding test entry: {e}")
            return

    # Now try a search
    try:
        results = await storage.search("humanoid robotics", limit=5)
        print(f"Search results: {len(results)} items found")

        for i, result in enumerate(results, 1):
            print(f"  Result {i}:")
            print(f"    Score: {result.get('score', 0):.4f}")
            print(f"    Title: {result.get('title', 'N/A')}")
            print(f"    URL: {result.get('url', 'N/A')}")
            print(f"    Content: {result.get('content', 'N/A')[:100]}...")
            print()

    except Exception as e:
        print(f"❌ Error during search: {e}")

if __name__ == "__main__":
    asyncio.run(check_and_test())