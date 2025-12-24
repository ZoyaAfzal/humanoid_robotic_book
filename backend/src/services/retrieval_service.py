import asyncio
import logging
from typing import List, Optional
from datetime import datetime

from src.storage.vector_storage import VectorStorage
from src.models.agent_models import RetrievedContext, Query
from src.models.error_models import RetrievalError, ValidationError


logger = logging.getLogger(__name__)


class RetrievalService:
    """
    Service class for handling semantic retrieval from Qdrant collection.
    Integrates with existing vector storage functionality.
    """

    def __init__(self):
        self.vector_storage = VectorStorage()

    async def retrieve_context(self, query: str, top_k: int = 5, min_score: float = 0.3) -> List[RetrievedContext]:
        """
        Retrieve relevant context from the Qdrant collection based on the query.

        Args:
            query: The natural language query to search for
            top_k: Number of top results to retrieve (default: 5)
            min_score: Minimum similarity score threshold (default: 0.3)

        Returns:
            List of RetrievedContext objects with relevant content

        Raises:
            RetrievalError: If there's an error during retrieval
            ValidationError: If query parameters are invalid
        """
        # Validate input parameters
        if not query or not query.strip():
            raise ValidationError("Query cannot be empty")

        if top_k < 1 or top_k > 20:
            raise ValidationError("top_k must be between 1 and 20")

        if min_score < 0.0 or min_score > 1.0:
            raise ValidationError("min_score must be between 0.0 and 1.0")

        try:
            start_time = datetime.now()

            # Use the existing search method from VectorStorage
            search_results = await self.vector_storage.search(query, limit=top_k)

            # Filter results based on minimum score threshold
            filtered_results = [
                result for result in search_results
                if result.get('score', 0) >= min_score
            ]

            # Convert search results to RetrievedContext objects
            retrieved_contexts = []
            for result in filtered_results:
                payload = result.get('payload', {})

                context = RetrievedContext(
                    score=result.get('score', 0.0),
                    content=payload.get('content', ''),
                    url=payload.get('url', ''),
                    title=payload.get('title', ''),
                    headings=payload.get('headings', []),
                    chunk_index=payload.get('chunk_index', 0),
                    source_document=payload.get('source_document', ''),
                    metadata=payload.get('metadata', {})
                )
                retrieved_contexts.append(context)

            # Log the retrieval operation
            retrieval_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Retrieved {len(retrieved_contexts)} context chunks for query '{query[:50]}...' "
                       f"in {retrieval_time:.3f}s")

            return retrieved_contexts

        except Exception as e:
            logger.error(f"Error during context retrieval: {str(e)}")
            raise RetrievalError(f"Failed to retrieve context: {str(e)}")

    async def validate_retrieval_quality(self, query: str, contexts: List[RetrievedContext]) -> dict:
        """
        Validate the quality of retrieved contexts for the given query.

        Args:
            query: The original query
            contexts: List of retrieved contexts

        Returns:
            Dictionary with validation results
        """
        validation_result = {
            'query': query,
            'context_count': len(contexts),
            'has_content': len(contexts) > 0,
            'avg_score': 0.0,
            'min_score': 0.0,
            'max_score': 0.0,
            'score_variance': 0.0,
            'total_content_length': sum(len(ctx.content) for ctx in contexts),
            'has_valid_sources': all(ctx.url for ctx in contexts) if contexts else False
        }

        if contexts:
            scores = [ctx.score for ctx in contexts]
            validation_result['avg_score'] = sum(scores) / len(scores)
            validation_result['min_score'] = min(scores)
            validation_result['max_score'] = max(scores)

            # Calculate variance
            avg_score = validation_result['avg_score']
            variance = sum((score - avg_score) ** 2 for score in scores) / len(scores)
            validation_result['score_variance'] = variance

        return validation_result

    async def get_retrieval_stats(self) -> dict:
        """
        Get statistics about the retrieval system.

        Returns:
            Dictionary with retrieval system statistics
        """
        try:
            verification = await self.vector_storage.verify_storage()
            return {
                'collection_exists': verification.get('collection_exists', False),
                'vector_count': verification.get('vector_count', 0),
                'sample_search_works': verification.get('sample_search_works', False),
                'error': verification.get('error', None)
            }
        except Exception as e:
            logger.error(f"Error getting retrieval stats: {str(e)}")
            return {
                'collection_exists': False,
                'vector_count': 0,
                'sample_search_works': False,
                'error': str(e)
            }


# Singleton instance for the service
retrieval_service = RetrievalService()