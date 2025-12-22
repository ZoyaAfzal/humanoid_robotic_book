#!/usr/bin/env python3
"""
Script to analyze what the chunking would look like with the full dataset
"""
import requests
import trafilatura
from xml.etree import ElementTree
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

def analyze_chunking():
    """
    Analyze what the chunking would look like with the full dataset
    """
    print("Analyzing full dataset chunking...")

    # Get all URLs
    print("Fetching URLs from sitemap...")
    urls = get_all_urls()
    print(f"Found {len(urls)} URLs to process")

    total_chunks = 0
    total_chars = 0

    for i, url in enumerate(urls):
        print(f"Processing URL {i+1}/{len(urls)}: {url}")

        # Extract text
        text = extract_text_from_url(url)
        if not text:
            print(f"  Skipping {url} - no text extracted")
            continue

        chars = len(text)
        total_chars += chars
        print(f"  Extracted {chars} characters")

        # Chunk text
        chunks = chunk_text(text)
        chunk_count = len(chunks)
        total_chunks += chunk_count
        print(f"  Generated {chunk_count} chunks")

        # Show sample of first chunk if there are chunks
        if chunks:
            first_chunk = chunks[0]
            print(f"    First chunk: {len(first_chunk)} chars - '{first_chunk[:100]}...'")

        # Show last chunk if there are multiple chunks
        if len(chunks) > 1:
            last_chunk = chunks[-1]
            print(f"    Last chunk: {len(last_chunk)} chars - '{last_chunk[:100]}...'")

    print(f"\n=== Analysis Summary ===")
    print(f"Total URLs processed: {len(urls)}")
    print(f"Total characters extracted: {total_chars:,}")
    print(f"Total chunks generated: {total_chunks:,}")
    print(f"Average characters per chunk: {total_chars/total_chunks if total_chunks > 0 else 0:.0f}")
    print(f"Average chunks per URL: {total_chunks/len(urls) if len(urls) > 0 else 0:.1f}")

    # If the application were to run with Qdrant, this is what would be stored:
    print(f"\n=== If Qdrant were configured ===")
    print(f"A collection named 'robotic_book_embedding' would be created")
    print(f"Each chunk would be stored as a vector with:")
    print(f"  - ID: {len(urls)}*1000 + chunk_index (unique integer)")
    print(f"  - Vector: 1024-dimensional embedding")
    print(f"  - Payload: {{'url': source_url, 'text': chunk_content}}")
    print(f"Total vectors that would be stored: {total_chunks:,}")

if __name__ == "__main__":
    analyze_chunking()