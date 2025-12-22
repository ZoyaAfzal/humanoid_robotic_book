#!/usr/bin/env python3
"""
Script to generate embeddings from extracted content and store in Qdrant.
"""

import json
import os
from typing import List, Dict
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def chunk_text(text: str, max_chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks that preserve semantic meaning.
    Uses a hierarchical approach: tries to split on paragraphs first, then sentences.
    """
    # First try to split by paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # If adding this paragraph would exceed the max size
        if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
            # Save the current chunk
            chunks.append(current_chunk.strip())

            # Start a new chunk with overlap if specified
            if overlap > 0 and len(paragraph) <= max_chunk_size:
                # Add overlap from the end of the previous chunk
                overlap_text = current_chunk[-overlap:] if len(current_chunk) >= overlap else current_chunk
                current_chunk = overlap_text + " " + paragraph
            else:
                current_chunk = paragraph
        else:
            current_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph

        # If current chunk is still too large, split by sentences
        if len(current_chunk) > max_chunk_size:
            sentences = [s.strip() + '.' for s in current_chunk.split('.') if s.strip()]
            temp_chunk = ""

            for sentence in sentences:
                if len(temp_chunk) + len(sentence) <= max_chunk_size:
                    temp_chunk = temp_chunk + " " + sentence if temp_chunk else sentence
                else:
                    if temp_chunk.strip():
                        chunks.append(temp_chunk.strip())
                        temp_chunk = sentence
                    else:
                        # If a single sentence is too long, split by max_chunk_size
                        for i in range(0, len(sentence), max_chunk_size):
                            chunks.append(sentence[i:i + max_chunk_size])

            current_chunk = temp_chunk

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def generate_cohere_embeddings(texts: List[str], cohere_api_key: str) -> List[List[float]]:
    """
    Generate embeddings using Cohere's API.
    """
    co = cohere.Client(cohere_api_key)
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",  # Using Cohere's latest embedding model
        input_type="search_document"  # Optimize for search documents
    )
    return response.embeddings

def initialize_qdrant_collection(client: QdrantClient, collection_name: str):
    """
    Initialize the Qdrant collection with appropriate configuration.
    """
    # Delete collection if it already exists (optional - for re-initialization)
    try:
        client.delete_collection(collection_name)
        print(f"Deleted existing collection: {collection_name}")
    except:
        pass  # Collection might not exist, which is fine

    # Create new collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=1024,  # Cohere embeddings are 1024 dimensions for embed-english-v3.0
            distance=models.Distance.COSINE
        )
    )
    print(f"Created collection: {collection_name}")

def store_in_qdrant(client: QdrantClient, collection_name: str, chunks: List[Dict]):
    """
    Store the embedded chunks in Qdrant with metadata.
    """
    points = []
    for chunk in chunks:
        point = models.PointStruct(
            id=uuid.uuid4().int,  # Generate a unique ID
            vector=chunk['embedding'],
            payload={
                'url': chunk['url'],
                'title': chunk['title'],
                'content': chunk['content'],
                'source_document': chunk.get('source_document', ''),
                'chunk_index': chunk.get('chunk_index', 0)
            }
        )
        points.append(point)

    # Upload in batches for efficiency
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=collection_name,
            points=batch
        )
        print(f"Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")
        time.sleep(0.1)  # Small delay to avoid overwhelming the server

def main():
    # Load extracted content
    input_file = "extracted_content.json"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run scrape_docusaurus.py first.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        pages = json.load(f)

    print(f"Loaded {len(pages)} pages from {input_file}")

    # Initialize Cohere client
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("Please set COHERE_API_KEY environment variable")

    # Initialize Qdrant client
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("Please set QDRANT_URL and QDRANT_API_KEY environment variables")

    qdrant_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True
    )

    # Define collection name
    collection_name = "humanoid_robotics_book"

    # Initialize collection
    initialize_qdrant_collection(qdrant_client, collection_name)

    # Process each page
    all_chunks = []
    chunk_index = 0

    for page in pages:
        print(f"Processing: {page['title'][:50]}...")

        # Chunk the content
        content_chunks = chunk_text(page['content'], max_chunk_size=1000, overlap=200)

        # Prepare for embedding
        for i, chunk in enumerate(content_chunks):
            chunk_data = {
                'url': page['url'],
                'title': page['title'],
                'content': chunk,
                'source_document': page['url'],
                'chunk_index': i
            }
            all_chunks.append(chunk_data)
            chunk_index += 1

    print(f"Created {len(all_chunks)} content chunks")

    # Generate embeddings in batches to avoid rate limits
    batch_size = 96  # Cohere has limits, so we'll batch appropriately
    all_embeddings = []

    for i in range(0, len(all_chunks), batch_size):
        batch_chunks = all_chunks[i:i + batch_size]
        batch_texts = [chunk['content'] for chunk in batch_chunks]

        print(f"Generating embeddings for batch {i//batch_size + 1}/{(len(all_chunks)-1)//batch_size + 1}")

        try:
            batch_embeddings = generate_cohere_embeddings(batch_texts, cohere_api_key)
            all_embeddings.extend(batch_embeddings)
            print(f"  Generated {len(batch_embeddings)} embeddings")
        except Exception as e:
            print(f"  Error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
            # Handle the error by potentially retrying or skipping
            continue

        # Add small delay to respect API rate limits
        time.sleep(0.1)

    # Check that we have embeddings for all chunks
    if len(all_embeddings) != len(all_chunks):
        print(f"Warning: Expected {len(all_chunks)} embeddings, but got {len(all_embeddings)}")
        # Truncate all_chunks to match the number of embeddings
        all_chunks = all_chunks[:len(all_embeddings)]

    # Add embeddings to chunks
    for i, chunk in enumerate(all_chunks):
        chunk['embedding'] = all_embeddings[i]

    # Store in Qdrant
    print("Storing embeddings in Qdrant...")
    store_in_qdrant(qdrant_client, collection_name, all_chunks)

    print(f"Successfully stored {len(all_chunks)} chunks in Qdrant collection '{collection_name}'")

    # Print collection info
    collection_info = qdrant_client.get_collection(collection_name)
    print(f"Collection vectors count: {collection_info.points_count}")

if __name__ == "__main__":
    main()