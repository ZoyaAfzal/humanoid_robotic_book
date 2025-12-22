"""
Content extraction module for the Humanoid Robotics RAG pipeline.
Handles discovering URLs and extracting clean content from Docusaurus pages.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import re

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from src.utils.config import get_config

logger = logging.getLogger(__name__)


class ContentChunk(BaseModel):
    """Represents a chunk of content with metadata."""
    url: str
    title: str
    content: str
    headings: List[str] = Field(default_factory=list)
    chunk_index: int = 0
    source_document: str = ""


class DocusaurusExtractor:
    """Extracts content from deployed Docusaurus book URLs."""

    def __init__(self):
        self.config = get_config()
        self.base_url = self.config.base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    async def discover_urls(self) -> List[str]:
        """
        Discover all URLs from the deployed Docusaurus site.
        Since Docusaurus generates static sites, we'll construct URLs based on the known structure.
        """
        # Known URLs based on the sidebar structure
        urls = [
            f"{self.base_url}/",
            f"{self.base_url}/docs/intro",
            f"{self.base_url}/docs/chapter1/index",
            f"{self.base_url}/docs/chapter1/lesson1/spec-kit-plus-workflow",
            f"{self.base_url}/docs/chapter1/lesson2/physical-ai-embodied-intelligence",
            f"{self.base_url}/docs/chapter1/lesson3/development-environment-setup",
            f"{self.base_url}/docs/chapter2/index",
            f"{self.base_url}/docs/chapter2/lesson1/ros2-architecture",
            f"{self.base_url}/docs/chapter2/lesson2/humanoid-robot-modeling",
            f"{self.base_url}/docs/chapter2/lesson3/bridging-ai-agents",
            f"{self.base_url}/docs/chapter3/index",
            f"{self.base_url}/docs/chapter3/lesson1/gazebo-environment-setup",
            f"{self.base_url}/docs/chapter3/lesson2/simulating-physics-collisions",
            f"{self.base_url}/docs/chapter3/lesson3/sensor-simulation",
            f"{self.base_url}/docs/chapter4/index",
            f"{self.base_url}/docs/chapter4/lesson1/isaac-sim-synthetic-data",
            f"{self.base_url}/docs/chapter4/lesson2/hardware-accelerated-navigation",
            f"{self.base_url}/docs/chapter4/lesson3/bipedal-path-planning",
            f"{self.base_url}/docs/chapter5/index",
            f"{self.base_url}/docs/chapter5/lesson1/voice-to-action",
            f"{self.base_url}/docs/chapter5/lesson2/cognitive-planning",
            f"{self.base_url}/docs/chapter5/lesson3/capstone-project-execution",
            f"{self.base_url}/docs/adr/adr-004",
        ]

        # Also try to get URLs from sitemap if available
        sitemap_url = f"{self.base_url}/sitemap.xml"
        sitemap_urls = await self._extract_from_sitemap(sitemap_url)

        # Combine and deduplicate URLs
        all_urls = list(set(urls + sitemap_urls))

        return all_urls

    async def _extract_from_sitemap(self, sitemap_url: str) -> List[str]:
        """Extract URLs from sitemap.xml if available."""
        try:
            response = self.session.get(sitemap_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')
            loc_tags = soup.find_all('loc')
            urls = [loc.text.strip() for loc in loc_tags if loc.text.strip().startswith(self.base_url)]

            logger.info(f"Found {len(urls)} URLs from sitemap")
            return urls
        except Exception as e:
            logger.warning(f"Could not fetch sitemap: {e}")
            return []

    async def extract_content(self, url: str) -> Optional[ContentChunk]:
        """
        Extract clean content from a single Docusaurus page.
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove navigation, footer, and other non-content elements
            for element in soup.find_all(['nav', 'header', 'footer', 'aside']):
                element.decompose()

            # Remove search bars, table of contents, and other UI elements
            for element in soup.find_all(class_=lambda x: x and any(remove_class in x for remove_class in [
                'navbar', 'menu', 'toc', 'table-of-contents', 'pagination', 'theme-edit-this-page',
                'theme-last-updated', 'theme-doc-sidebar', 'button', 'search', 'carbon-ads', 'doc-sidebar',
                'doc-page', 'doc-item', 'doc-markdown', 'docusaurus-maintenance', 'doc-title'
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

                # Extract headings for context
                headings = []
                for heading in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                    heading_text = heading.get_text().strip()
                    if heading_text:
                        headings.append(heading_text)

                # Extract text content, preserving paragraph structure
                content = main_content.get_text(separator='\n', strip=True)

                # Clean up excessive whitespace
                content = re.sub(r'\n\s*\n', '\n\n', content)

                return ContentChunk(
                    url=url,
                    title=title,
                    content=content,
                    headings=headings
                )
            else:
                logger.warning(f"No main content found for {url}")
                return None

        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return None

    async def extract_content_batch(self, urls: List[str]) -> List[ContentChunk]:
        """
        Extract content from multiple URLs concurrently.
        """
        # Create tasks for concurrent processing
        tasks = [self.extract_content(url) for url in urls]

        # Execute tasks concurrently with a limit to avoid overwhelming the server
        semaphore = asyncio.Semaphore(10)  # Limit to 10 concurrent requests

        async def limited_extract(url):
            async with semaphore:
                return await self.extract_content(url)

        tasks = [limited_extract(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out None results and exceptions
        content_chunks = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing {urls[i]}: {result}")
            elif result is not None:
                content_chunks.append(result)

        return content_chunks


async def main():
    """Main function for content extraction CLI."""
    extractor = DocusaurusExtractor()
    urls = await extractor.discover_urls()
    logger.info(f"Discovered {len(urls)} URLs")

    content_chunks = await extractor.extract_content_batch(urls)
    logger.info(f"Extracted {len(content_chunks)} content chunks")

    # Save to file for debugging
    import json
    with open("extracted_content.json", "w", encoding="utf-8") as f:
        json.dump([chunk.model_dump() for chunk in content_chunks], f, indent=2, ensure_ascii=False)

    logger.info("Content extraction completed and saved to extracted_content.json")


if __name__ == "__main__":
    asyncio.run(main())