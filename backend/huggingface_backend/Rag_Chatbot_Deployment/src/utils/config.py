"""
Configuration utilities for the Humanoid Robotics RAG pipeline.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    """Configuration class for the RAG pipeline."""
    # Cohere configuration
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")

    # Qdrant configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")

    # Docusaurus site configuration
    base_url: str = os.getenv("BOOK_BASE_URL", "https://ZoyaAfzal.github.io/humanoid_robotic_book")

    # Processing configuration
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "96"))

    # Collection name
    collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "humanoid_robotics_book")

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        errors = []

        if not self.cohere_api_key:
            errors.append("COHERE_API_KEY is required")

        if not self.qdrant_url:
            errors.append("QDRANT_URL is required")

        if not self.qdrant_api_key:
            errors.append("QDRANT_API_KEY is required")

        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")

        return True


def get_config() -> Config:
    """Get the application configuration."""
    config = Config()
    config.validate()
    return config