#!/usr/bin/env python3
"""
Test script to run the main functionality without external dependencies
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

def test_functionality():
    """
    Test the core functionality without external dependencies
    """
    print("Testing core functionality...")

    # Test URL fetching
    print("Testing URL fetching...")
    urls = get_all_urls()
    print(f"Found {len(urls)} URLs")

    # Test text extraction with a sample URL (just the first one)
    if urls:
        print(f"Testing text extraction from: {urls[0]}")
        text = extract_text_from_url(urls[0])
        if text:
            print(f"Successfully extracted text of length: {len(text)} characters")

            # Test chunking
            print("Testing text chunking...")
            chunks = chunk_text(text[:2000])  # Use only first 2000 chars for testing
            print(f"Generated {len(chunks)} chunks from sample text")

            if chunks:
                print(f"First chunk length: {len(chunks[0])} characters")
                print(f"First chunk preview: {chunks[0][:100]}...")
        else:
            print("Could not extract text from sample URL")
    else:
        print("No URLs found to test with")

    print("All tests completed successfully!")

if __name__ == "__main__":
    test_functionality()