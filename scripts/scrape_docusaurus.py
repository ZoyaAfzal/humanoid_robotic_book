#!/usr/bin/env python3
"""
Script to scrape the deployed Docusaurus book, extract content, and prepare for embedding.
"""

import os
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
from typing import List, Dict, Tuple
import re

def get_all_urls(base_url: str) -> List[str]:
    """
    Discover all URLs from the deployed Docusaurus site.
    Since Docusaurus generates static sites, we'll construct URLs based on the sidebar structure.
    """
    # Base URLs based on the sidebar structure we identified
    urls = [
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

    return urls

def extract_content_from_page(url: str) -> Tuple[str, str, str]:
    """
    Extract clean content from a Docusaurus page.
    Returns (title, content, url).
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove navigation, footer, and other non-content elements
        for element in soup.find_all(['nav', 'header', 'footer', 'aside']):
            element.decompose()

        # Remove search bars, table of contents, and other UI elements
        for element in soup.find_all(class_=lambda x: x and any(remove_class in x for remove_class in [
            'navbar', 'menu', 'toc', 'table-of-contents', 'pagination', 'theme-edit-this-page',
            'theme-last-updated', 'theme-doc-sidebar', 'button', 'search', 'carbon-ads'
        ])):
            element.decompose()

        # Try to find the main content area (Docusaurus typically uses main or article tags)
        main_content = soup.find('main') or soup.find('article') or soup.find('div', {'role': 'main'})

        if main_content:
            # Extract the title - typically in h1 tags or title tag
            title_elem = soup.find('h1')
            if title_elem:
                title = title_elem.get_text().strip()
            else:
                title_tag = soup.find('title')
                title = title_tag.get_text().strip() if title_tag else "No Title"

            # Extract text content, preserving paragraph structure
            content = main_content.get_text(separator='\n', strip=True)

            # Clean up excessive whitespace
            content = re.sub(r'\n\s*\n', '\n\n', content)

            return title, content, url
        else:
            # If we can't find main content, extract from the whole body
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "No Title"

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            content = soup.get_text(separator='\n', strip=True)
            content = re.sub(r'\n\s*\n', '\n\n', content)

            return title, content, url

    except Exception as e:
        print(f"Error extracting content from {url}: {str(e)}")
        return "", "", url

def main():
    base_url = "https://ZoyaAfzal.github.io/humanoid_robotic_book"
    urls = get_all_urls(base_url)

    print(f"Found {len(urls)} URLs to process")

    all_pages = []

    for i, url in enumerate(urls, 1):
        print(f"Processing ({i}/{len(urls)}): {url}")

        title, content, page_url = extract_content_from_page(url)

        if content.strip():  # Only save if we got content
            page_data = {
                'url': page_url,
                'title': title,
                'content': content
            }
            all_pages.append(page_data)
            print(f"  Extracted title: '{title[:50]}...' ({len(content)} chars)")
        else:
            print(f"  Warning: No content extracted from {url}")

        # Be respectful to the server
        time.sleep(0.5)

    # Save the extracted content
    import json
    output_file = "extracted_content.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_pages, f, indent=2, ensure_ascii=False)

    print(f"\nExtraction complete! Saved {len(all_pages)} pages to {output_file}")

    # Print summary statistics
    total_chars = sum(len(page['content']) for page in all_pages)
    avg_chars = total_chars / len(all_pages) if all_pages else 0

    print(f"Total characters extracted: {total_chars:,}")
    print(f"Average characters per page: {avg_chars:,.0f}")

if __name__ == "__main__":
    main()