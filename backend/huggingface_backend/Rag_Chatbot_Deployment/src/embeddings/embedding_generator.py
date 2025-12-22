"""
Embedding generation module for the Humanoid Robotics RAG pipeline.
Handles chunking content and generating embeddings using Cohere.
"""

import asyncio
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
import time

import cohere

from src.extraction.content_extractor import ContentChunk
from src.utils.config import get_config

logger = logging.getLogger(__name__)


@dataclass
class EmbeddedChunk:
    """Represents a content chunk with its embedding vector."""
    url: str
    title: str
    content: str
    headings: List[str]
    chunk_index: int
    source_document: str
    embedding: List[float]
    metadata: Dict[str, Any]


class EmbeddingGenerator:
    """Generates embeddings for content chunks using Cohere."""

    def __init__(self):
        self.config = get_config()
        self.co = cohere.Client(self.config.cohere_api_key)
        self.model = "embed-english-v3.0"
        self.batch_size = self.config.batch_size  # Cohere's recommended batch size

    def chunk_text(self, text: str, max_chunk_size: int = None, overlap: int = None) -> List[str]:
        """
        Split text into overlapping chunks that preserve semantic meaning.
        Uses a hierarchical approach: tries to split on paragraphs first, then sentences.
        """
        if max_chunk_size is None:
            max_chunk_size = self.config.chunk_size
        if overlap is None:
            overlap = self.config.chunk_overlap

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

    async def generate_embeddings_batch(self, content_chunks: List[ContentChunk]) -> List[EmbeddedChunk]:
        """
        Generate embeddings for content chunks in batches.
        """
        all_embedded_chunks = []

        for i, content_chunk in enumerate(content_chunks):
            logger.info(f"Processing content chunk {i+1}/{len(content_chunks)}: {content_chunk.title[:50]}...")

            # Chunk the content
            text_chunks = self.chunk_text(content_chunk.content, max_chunk_size=1000, overlap=200)

            # Process each text chunk
            for j, text_chunk in enumerate(text_chunks):
                # Prepare for embedding
                chunk_data = EmbeddedChunk(
                    url=content_chunk.url,
                    title=content_chunk.title,
                    content=text_chunk,
                    headings=content_chunk.headings,
                    chunk_index=j,
                    source_document=content_chunk.url,
                    embedding=[],
                    metadata={
                        'original_chunk_index': i,
                        'total_chunks': len(text_chunks),
                        'text_length': len(text_chunk)
                    }
                )
                all_embedded_chunks.append(chunk_data)

        logger.info(f"Created {len(all_embedded_chunks)} text chunks from {len(content_chunks)} content chunks")

        # Generate embeddings in batches
        embedded_chunks = await self._generate_embeddings_in_batches(all_embedded_chunks)

        return embedded_chunks

    async def _generate_embeddings_in_batches(self, chunks: List[EmbeddedChunk]) -> List[EmbeddedChunk]:
        """Generate embeddings for chunks in batches to respect API limits."""
        all_embeddings = []
        batch_size = self.batch_size

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_texts = [chunk.content for chunk in batch]

            logger.info(f"Generating embeddings for batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")

            try:
                response = self.co.embed(
                    texts=batch_texts,
                    model=self.model,
                    input_type="search_document"  # Optimize for search documents
                )

                batch_embeddings = response.embeddings
                logger.info(f"Generated {len(batch_embeddings)} embeddings for batch")

                # Add embeddings to chunks
                for j, chunk in enumerate(batch):
                    chunk.embedding = batch_embeddings[j]
                    all_embeddings.append(chunk)

                # Add small delay to respect rate limits
                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"Error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
                # If one batch fails, we might want to retry or handle differently
                continue

        return all_embeddings


async def main():
    """Main function for embedding generation CLI."""
    import json

    # Load extracted content from file
    try:
        with open("extracted_content.json", "r", encoding="utf-8") as f:
            content_data = json.load(f)

        content_chunks = [ContentChunk(**chunk) for chunk in content_data]
        logger.info(f"Loaded {len(content_chunks)} content chunks from file")
    except FileNotFoundError:
        logger.error("extracted_content.json not found. Run content extraction first.")
        return

    generator = EmbeddingGenerator()
    embedded_chunks = await generator.generate_embeddings_batch(content_chunks)

    logger.info(f"Generated embeddings for {len(embedded_chunks)} text chunks")

    # Save embedded chunks to file for debugging
    embedded_data = []
    for chunk in embedded_chunks:
        chunk_dict = chunk.__dict__.copy()
        chunk_dict['embedding'] = chunk_dict['embedding'][:5] + ['...'] if len(chunk_dict['embedding']) > 5 else chunk_dict['embedding']  # Truncate embedding for readability
        embedded_data.append(chunk_dict)

    with open("embedded_chunks.json", "w", encoding="utf-8") as f:
        json.dump(embedded_data, f, indent=2, ensure_ascii=False)

    logger.info("Embeddings generated and saved to embedded_chunks.json")


if __name__ == "__main__":
    asyncio.run(main())