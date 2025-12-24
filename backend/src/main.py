import requests
import trafilatura
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
import time
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize global variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Initialize clients
co = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True) if QDRANT_URL and QDRANT_API_KEY else None


def get_all_urls():
    """
    Fetch all documentation URLs from the sitemap.
    Return a list of valid page URLs.
    """
    base_url = "https://zoyaafzal.github.io/humanoid_robotic_book"
    sitemap_url = f"{base_url}/sitemap.xml"

    try:
        response = requests.get(sitemap_url, timeout=30)
        response.raise_for_status()

        # Parse the sitemap XML
        root = ElementTree.fromstring(response.content)
        urls = []

        # Find all <loc> elements which contain the URLs
        for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            url = loc.text.strip()
            if url and url.startswith(base_url):
                urls.append(url)

        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        # Fallback to known URLs if sitemap is not available
        return [
            f"{base_url}/",
            f"{base_url}/docs/intro",
            f"{base_url}/docs/chapter1/index",
            f"{base_url}/docs/chapter1/lesson1/spec-kit-plus-workflow",
            f"{base_url}/docs/chapter1/lesson2/physical-ai-embodied-intelligence",
            f"{base_url}/docs/chapter1/lesson3/development-environment-setup",
            f"{base_url}/docs/chapter2/index",
            f"{base_url}/docs/chapter2/lesson1/ros2-architecture",
            f"{base_url}/docs/chapter2/lesson2/humanoid-robot-modeling",
            f"{base_url}/docs/chapter2/lesson3/bridging-ai-agents",
            f"{base_url}/docs/chapter3/index",
            f"{base_url}/docs/chapter3/lesson1/gazebo-environment-setup",
            f"{base_url}/docs/chapter3/lesson2/simulating-physics-collisions",
            f"{base_url}/docs/chapter3/lesson3/sensor-simulation",
            f"{base_url}/docs/chapter4/index",
            f"{base_url}/docs/chapter4/lesson1/isaac-sim-synthetic-data",
            f"{base_url}/docs/chapter4/lesson2/hardware-accelerated-navigation",
            f"{base_url}/docs/chapter4/lesson3/bipedal-path-planning",
            f"{base_url}/docs/chapter5/index",
            f"{base_url}/docs/chapter5/lesson1/voice-to-action",
            f"{base_url}/docs/chapter5/lesson2/cognitive-planning",
            f"{base_url}/docs/chapter5/lesson3/capstone-project-execution",
            f"{base_url}/docs/adr/adr-004",
        ]


def extract_text_from_url(url):
    """
    Download HTML with a timeout.
    Extract clean readable text using `trafilatura`.
    Skip the page if extraction fails or returns empty text.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Use trafilatura to extract clean text from HTML
        text = trafilatura.extract(response.text, include_comments=False, include_tables=True)

        if text and text.strip():
            return text.strip()
        else:
            print(f"Warning: No text extracted from {url}")
            return None
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return None


def chunk_text(text):
    """
    Split text into ~1000–1200 character chunks.
    Prefer paragraph boundaries.
    Fallback to sentence or hard splits when needed.
    """
    chunks = []
    max_chunk_size = 1200
    min_chunk_size = 1000

    # First, try to split by paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    current_chunk = ""

    for paragraph in paragraphs:
        # If adding this paragraph would exceed the max size
        if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
            # If the current chunk is already at least the minimum size, save it
            if len(current_chunk) >= min_chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                # Otherwise, continue adding to the current chunk
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        else:
            current_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph

            # If the current chunk is now too large, we need to split it
            if len(current_chunk) > max_chunk_size:
                # Split by sentences if possible
                sentences = re.split(r'[.!?]+', current_chunk)
                temp_chunk = ""

                for sentence in sentences:
                    sentence = sentence.strip() + "."
                    if len(temp_chunk) + len(sentence) <= max_chunk_size:
                        temp_chunk += " " + sentence if temp_chunk else sentence
                    else:
                        if temp_chunk.strip():
                            chunks.append(temp_chunk.strip())
                        temp_chunk = sentence

                current_chunk = temp_chunk

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # If we have chunks that are still too small and we have more than one chunk,
    # consider merging small chunks with neighbors
    if len(chunks) > 1:
        merged_chunks = []
        i = 0
        while i < len(chunks):
            current = chunks[i]
            # If current chunk is too small and there's a next chunk, consider merging
            if len(current) < min_chunk_size and i < len(chunks) - 1:
                next_chunk = chunks[i + 1]
                if len(current) + len(next_chunk) <= max_chunk_size:
                    merged_chunks.append(current + "\n\n" + next_chunk)
                    i += 2  # Skip next chunk since we merged it
                else:
                    merged_chunks.append(current)
                    i += 1
            else:
                merged_chunks.append(current)
                i += 1
        return merged_chunks

    return chunks


def embed(text):
    """
    Generate vector embeddings.
    Trim text to model limits if required.
    Return the embedding vector or `None` on failure.
    """
    if not co:
        print("Error: Cohere client not initialized. Check COHERE_API_KEY.")
        return None

    try:
        # Cohere has a limit on text length, so we might need to trim
        max_length = 4096  # Approximate limit for Cohere
        if len(text) > max_length:
            text = text[:max_length]

        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )

        return response.embeddings[0]
    except Exception as e:
        print(f"Error generating embedding for text: {e}")
        return None


def create_collection():
    """
    Ensure Qdrant collection exists.
    Collection name: **`robotic_book_embedding`**
    Use **cosine distance**
    """
    if not qdrant_client:
        print("Error: Qdrant client not initialized. Check QDRANT_URL and QDRANT_API_KEY.")
        return

    try:
        # Check if collection exists
        qdrant_client.get_collection("robotic_book_embedding")
        print("Collection 'robotic_book_embedding' already exists")
    except:
        # Create collection with cosine distance
        qdrant_client.create_collection(
            collection_name="robotic_book_embedding",
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
        )
        print("Created collection 'robotic_book_embedding' with cosine distance")


def save_chunks_to_qdrant(chunk, id, url):
    """
    Store vectors in Qdrant.
    Payload must include:
      - `url`
      - `text`
    """
    if not qdrant_client:
        print("Error: Qdrant client not initialized. Check QDRANT_URL and QDRANT_API_KEY.")
        return

    embedding = embed(chunk)
    if embedding is None:
        print(f"Skipping chunk from {url} due to embedding failure")
        return

    try:
        qdrant_client.upsert(
            collection_name="robotic_book_embedding",
            points=[
                models.PointStruct(
                    id=id,
                    vector=embedding,
                    payload={
                        "url": url,
                        "text": chunk
                    }
                )
            ]
        )
    except Exception as e:
        print(f"Error saving chunk to Qdrant: {e}")


def main():
    """
    Execute the full ingestion pipeline:
      - Fetch URLs
      - Create collection
      - Extract → chunk → embed → store
    Print progress logs and final summary
    """
    print("Starting HTML-based ingestion pipeline...")

    # Fetch URLs
    print("Fetching URLs from sitemap...")
    urls = get_all_urls()
    print(f"Found {len(urls)} URLs")

    # Create collection
    print("Creating Qdrant collection...")
    create_collection()

    # Process each URL
    total_chunks = 0
    processed_urls = 0

    for i, url in enumerate(urls):
        print(f"Processing URL {i+1}/{len(urls)}: {url}")

        # Extract text
        text = extract_text_from_url(url)
        if not text:
            print(f"  Skipping {url} - no text extracted")
            continue

        # Chunk text
        chunks = chunk_text(text)
        print(f"  Generated {len(chunks)} chunks")

        # Process each chunk
        for j, chunk in enumerate(chunks):
            chunk_id = i * 1000 + j  # Create unique ID
            save_chunks_to_qdrant(chunk, chunk_id, url)
            total_chunks += 1

        processed_urls += 1
        print(f"  Saved {len(chunks)} chunks from this URL")

    # Print final summary
    print("\n=== Pipeline Summary ===")
    print(f"Total URLs processed: {processed_urls}/{len(urls)}")
    print(f"Total chunks saved: {total_chunks}")
    print("HTML-based ingestion pipeline completed!")


if __name__ == "__main__":
    main()