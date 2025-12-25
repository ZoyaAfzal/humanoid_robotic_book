"""
Vector storage module for the Humanoid Robotics RAG pipeline.
Handles storing embeddings in Qdrant vector database.
"""

import asyncio
import logging
import uuid
from typing import List, Dict, Any
import time

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct

from src.embeddings.embedding_generator import EmbeddedChunk
from src.utils.config import get_config

logger = logging.getLogger(__name__)


class VectorStorage:
    """Handles storage of embeddings in Qdrant vector database."""

    def __init__(self):
        self.config = get_config()
        self.client = QdrantClient(
            url=self.config.qdrant_url,
            api_key=self.config.qdrant_api_key,
            prefer_grpc=False  # Use HTTP instead of gRPC to avoid connection issues
        )
        self.collection_name = self.config.collection_name

    def initialize_collection(self):
        """Initialize the Qdrant collection with appropriate configuration."""
        # Check if collection exists
        try:
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists with {collection_info.points_count} vectors")
            return
        except:
            pass  # Collection doesn't exist, will create it

        # Create new collection
        # Cohere embeddings are 1024 dimensions for embed-english-v3.0
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"Created collection: {self.collection_name}")

    async def store_chunks(self, embedded_chunks: List[EmbeddedChunk]):
        """Store embedded chunks in Qdrant with metadata."""
        self.initialize_collection()

        # Convert embedded chunks to Qdrant points
        points = []
        for chunk in embedded_chunks:
            point = PointStruct(
                id=uuid.uuid4().int,  # Generate a unique ID
                vector=chunk.embedding,
                payload={
                    'url': chunk.url,
                    'title': chunk.title,
                    'content': chunk.content,
                    'headings': chunk.headings,
                    'chunk_index': chunk.chunk_index,
                    'source_document': chunk.source_document,
                    'metadata': chunk.metadata
                }
            )
            points.append(point)

        # Upload in batches for efficiency
        batch_size = 100
        total_points = len(points)

        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )

            batch_end = min(i + batch_size, total_points)
            logger.info(f"Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1} "
                       f"({batch_end}/{total_points} points)")

            # Small delay to avoid overwhelming the server
            await asyncio.sleep(0.1)

        logger.info(f"Successfully stored {len(points)} vectors in Qdrant collection '{self.collection_name}'")

    async def verify_storage(self) -> Dict[str, Any]:
        """Verify that vectors were stored correctly and return statistics."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            count = collection_info.points_count

            # Perform a sample search to verify functionality using try-catch approach
            sample_search_result = None
            last_exception = None

            # Try the most modern method first
            try:
                sample_search_result = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=[0.1] * 1024,  # Sample vector
                    limit=1
                )
            except AttributeError as e:
                last_exception = e
            except Exception as e:
                last_exception = e

            # If search failed, try search_points (older method)
            if sample_search_result is None:
                try:
                    sample_search_result = self.client.search_points(
                        collection_name=self.collection_name,
                        vector=[0.1] * 1024,  # Sample vector
                        limit=1
                    )
                except AttributeError as e:
                    last_exception = e
                except Exception as e:
                    last_exception = e

            # If both failed, try query_points (another version)
            if sample_search_result is None:
                try:
                    sample_search_result = self.client.query_points(
                        collection_name=self.collection_name,
                        query=[0.1] * 1024,  # Sample vector
                        limit=1
                    )
                except AttributeError as e:
                    last_exception = e
                except Exception as e:
                    last_exception = e

            # If all methods failed, raise an error
            if sample_search_result is None:
                raise last_exception or AttributeError("Qdrant client does not have a recognized search method for verification.")

            # Check if the search result has proper structure by examining the first result
            sample_works = False

            # Handle different Qdrant response types for getting result count
            if hasattr(sample_search_result, '__len__'):
                # It's a list or other iterable with length
                result_count = len(sample_search_result) if sample_search_result else 0
            elif hasattr(sample_search_result, 'results') and hasattr(sample_search_result.results, '__len__'):
                # It's a QueryResponse object with results attribute
                result_count = len(sample_search_result.results) if sample_search_result.results else 0
            elif hasattr(sample_search_result, 'points') and hasattr(sample_search_result.points, '__len__'):
                # It's a response object with points attribute
                result_count = len(sample_search_result.points) if sample_search_result.points else 0
            else:
                # Unknown response type, try to get length anyway
                try:
                    result_count = len(sample_search_result) if sample_search_result else 0
                except TypeError:
                    result_count = 0
                    logger.warning(f"Could not determine length of sample search result of type {type(sample_search_result)}")

            if result_count > 0:
                # Get the first result based on the response type
                if hasattr(sample_search_result, 'results'):
                    # It's a QueryResponse object, use the results attribute
                    first_result = sample_search_result.results[0] if sample_search_result.results else None
                elif hasattr(sample_search_result, 'points'):
                    # It's a response object with points
                    first_result = sample_search_result.points[0] if sample_search_result.points else None
                else:
                    # It's already a list or iterable
                    first_result = sample_search_result[0] if sample_search_result else None

                if first_result is not None:
                    # Check if the result has a score attribute or can be handled by our logic
                    if hasattr(first_result, 'score') or isinstance(first_result, tuple) or hasattr(first_result, '__getitem__'):
                        sample_works = True

            return {
                'vector_count': count,
                'sample_search_works': sample_works,
                'collection_exists': True
            }
        except Exception as e:
            logger.error(f"Error verifying storage: {str(e)}")
            return {
                'vector_count': 0,
                'sample_search_works': False,
                'collection_exists': False,
                'error': str(e)
            }

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search in the stored vectors."""
        import time
        import os
        import cohere
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required for search")

        start_time = time.time()

        co = cohere.Client(cohere_api_key)
        query_embedding = co.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"
        ).embeddings[0]

        # Determine the correct search method by trying each one in order of preference
        search_results = None
        last_exception = None

        # Try the most modern method first
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit*2,  # Double the limit to get more potential results
                with_payload=True
            )
        except AttributeError as e:
            last_exception = e
        except Exception as e:
            # If it's not an AttributeError, the method exists but had another issue
            last_exception = e

        # If search failed, try search_points (older method)
        if search_results is None:
            try:
                search_results = self.client.search_points(
                    collection_name=self.collection_name,
                    vector=query_embedding,
                    limit=limit*2,  # Double the limit to get more potential results
                    with_payload=True
                )
            except AttributeError as e:
                last_exception = e
            except Exception as e:
                last_exception = e

        # If both failed, try query_points (another version)
        if search_results is None:
            try:
                search_results = self.client.query_points(
                    collection_name=self.collection_name,
                    query=query_embedding,
                    limit=limit*2,  # Double the limit to get more potential results
                    with_payload=True
                )
            except AttributeError as e:
                last_exception = e
            except Exception as e:
                last_exception = e

        # If all methods failed, raise an error
        if search_results is None:
            raise last_exception or AttributeError("Qdrant client does not have a recognized search method.")

        # Calculate query time
        query_time = time.time() - start_time

        # Handle different Qdrant response types for getting result count
        if hasattr(search_results, '__len__'):
            # It's a list or other iterable with length
            results_count = len(search_results) if search_results else 0
        elif hasattr(search_results, 'results') and hasattr(search_results.results, '__len__'):
            # It's a QueryResponse object with results attribute
            results_count = len(search_results.results) if search_results.results else 0
        elif hasattr(search_results, 'points') and hasattr(search_results.points, '__len__'):
            # It's a response object with points attribute
            results_count = len(search_results.points) if search_results.points else 0
        else:
            # Unknown response type, try to get length anyway
            try:
                results_count = len(search_results) if search_results else 0
            except TypeError:
                results_count = 0
                logger.warning(f"Could not determine length of search results of type {type(search_results)}")

        logger.info(f"Raw search results count: {results_count} for query: '{query}'")

        results = []
        validation_errors = []

        # Handle different response types for iteration
        if hasattr(search_results, 'results'):
            # It's a QueryResponse object, use the results attribute
            search_result_items = search_results.results
        elif hasattr(search_results, 'points'):
            # It's a response object with points
            search_result_items = search_results.points
        else:
            # It's already a list or iterable
            search_result_items = search_results

        # Check if we should prioritize results that contain query terms in the content
        query_lower = query.lower()
        query_terms = [term.strip('\'".,!?()[]{}') for term in query_lower.split() if len(term) > 2]

        for result in search_result_items:
            # Handle different result formats from different Qdrant methods
            # Modern search() method returns objects with attributes
            # Older search_points() might return different formats
            if isinstance(result, tuple):
                # This might be from an older method returning tuples
                # Assuming format (payload, score) or similar
                if len(result) == 2:
                    raw_payload, score = result
                else:
                    # Unknown tuple format, try to extract score differently
                    # Attempt to find score in the tuple
                    raw_payload = result[0] if len(result) > 0 else {}
                    score = result[1] if len(result) > 1 else 0.0
                # Ensure payload is always a dictionary
                if isinstance(raw_payload, dict):
                    payload = raw_payload
                elif isinstance(raw_payload, str):
                    # If raw_payload is a string, we need to handle it appropriately
                    # For Qdrant results, payload should be a dictionary with metadata
                    logger.warning(f"Received string payload instead of dictionary: {type(raw_payload)}")
                    payload = {}
                else:
                    # For other types, try to convert or default to empty dict
                    payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
            elif hasattr(result, '__getitem__') and not isinstance(result, str):
                # This could be a dictionary-like object
                raw_payload = result.get('payload', result if isinstance(result, dict) else {})
                # Ensure payload is a dictionary
                if isinstance(raw_payload, dict):
                    payload = raw_payload
                elif isinstance(raw_payload, str):
                    logger.warning(f"Received string payload instead of dictionary: {type(raw_payload)}")
                    payload = {}
                else:
                    payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
                score = result.get('score', result.get('score', 0.0))
            elif hasattr(result, 'score'):
                # This is from the modern search method, but check if it's a tuple with score attribute
                # Some versions might have tuple-like objects with attributes
                try:
                    score = result.score
                    raw_payload = getattr(result, 'payload', {})
                    # Ensure payload is a dictionary
                    if isinstance(raw_payload, dict):
                        payload = raw_payload
                    elif isinstance(raw_payload, str):
                        logger.warning(f"Received string payload instead of dictionary: {type(raw_payload)}")
                        payload = {}
                    else:
                        payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
                except AttributeError as e:
                    logger.warning(f"Could not access score attribute: {e}. Result type: {type(result)}")
                    # If it has score attribute but accessing it fails, treat as unknown format
                    raw_payload = getattr(result, 'payload', {})
                    if isinstance(raw_payload, dict):
                        payload = raw_payload
                    elif isinstance(raw_payload, str):
                        logger.warning(f"Received string payload instead of dictionary: {type(raw_payload)}")
                        payload = {}
                    else:
                        payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
                    score = getattr(result, 'score',
                                   getattr(result, 'score_',
                                   getattr(result, 'similarity', 0.0)))
            else:
                # Unknown format, use default
                raw_payload = getattr(result, 'payload', {})
                # Ensure payload is a dictionary
                if isinstance(raw_payload, dict):
                    payload = raw_payload
                elif isinstance(raw_payload, str):
                    logger.warning(f"Received string payload instead of dictionary: {type(raw_payload)}")
                    payload = {}
                else:
                    payload = getattr(raw_payload, '__dict__', {}) if hasattr(raw_payload, '__dict__') else {}
                # Try to get score from various possible attributes
                score = getattr(result, 'score',
                               getattr(result, 'score_',
                               getattr(result, 'similarity', 0.0)))

            # Additional safety check: if score is still problematic, log and set to default
            if isinstance(score, tuple) and hasattr(score, '__len__') and len(score) > 0:
                # This means score itself is a problematic tuple, try to extract the actual score
                if isinstance(score[0], (int, float)):
                    score = score[0]
                else:
                    logger.warning(f"Score is still a complex object: {type(score)}, setting to 0.0")
                    score = 0.0
            elif isinstance(score, list) and len(score) > 0:
                # Handle case where score is a list
                if isinstance(score[0], (int, float)):
                    score = score[0]
                else:
                    logger.warning(f"Score is a list with non-numeric values: {type(score[0])}, setting to 0.0")
                    score = 0.0
            elif isinstance(score, (list, set, dict)):
                # Handle other collection types that can't be compared with >=
                logger.warning(f"Score is a collection type {type(score)} that can't be compared numerically, setting to 0.0")
                score = 0.0

            # Ensure score is a numeric value for comparisons
            try:
                score = float(score)
            except (TypeError, ValueError):
                logger.warning(f"Could not convert score to float: {type(score)}, setting to 0.0")
                score = 0.0

            # Boost score if the content contains query terms
            content_lower = payload.get('content', '').lower()
            title_lower = payload.get('title', '').lower()
            boost_factor = 1.0

            # Count how many query terms appear in content or title
            matched_terms = 0
            for term in query_terms:
                if term in content_lower or term in title_lower:
                    matched_terms += 1

            # Boost score based on number of matched terms
            if matched_terms > 0:
                boost_factor = 1.0 + (matched_terms * 0.2)  # Boost by 20% per matched term
                score = min(score * boost_factor, 1.0)  # Cap the score at 1.0

            result_dict = {
                'score': score,
                'payload': payload,
                'url': payload.get('url', ''),
                'title': payload.get('title', ''),
                'content': payload.get('content', '')[:200] + '...' if len(payload.get('content', '')) > 200 else payload.get('content', ''),
                'query_time': query_time  # Add query time to results
            }

            # Validate metadata for this result
            validation = self.validate_metadata(result_dict)
            result_dict['metadata_validation'] = validation

            # Log any validation issues
            if not validation['valid']:
                validation_errors.extend(validation['errors'])

            results.append(result_dict)

        # Log validation summary
        if validation_errors:
            logger.warning(f"Metadata validation found {len(validation_errors)} errors: {validation_errors[:3]}...")  # Limit log length

        # Sort results by score in descending order to ensure highest scoring (potentially boosted) results come first
        results.sort(key=lambda x: x['score'], reverse=True)

        # Handle case where no results are returned
        if not results:
            logger.info(f"No results found for query: '{query}' (query time: {query_time:.4f}s)")
            # Return empty list but with query time information for consistency
            return []

        logger.info(f"Semantic search completed in {query_time:.4f}s for query: '{query[:50]}...'")
        return results

    def validate_metadata(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate metadata integrity for a retrieval result.

        Args:
            result: A single retrieval result dictionary

        Returns:
            Dictionary with validation results including:
            - valid: boolean indicating if metadata is valid
            - errors: list of validation errors
            - warnings: list of validation warnings
        """
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }

        # Check required fields in the top-level result
        required_result_fields = ['score', 'payload', 'url', 'title', 'content']
        for field in required_result_fields:
            if field not in result:
                validation_result['valid'] = False
                validation_result['errors'].append(f"Missing required field: {field}")

        # Validate payload if it exists
        payload = result.get('payload', {})
        if not isinstance(payload, dict):
            validation_result['valid'] = False
            validation_result['errors'].append("Payload must be a dictionary")
        else:
            # Check required payload fields
            required_payload_fields = ['url', 'title', 'content', 'headings', 'chunk_index', 'source_document', 'metadata']
            for field in required_payload_fields:
                if field not in payload:
                    validation_result['valid'] = False
                    validation_result['errors'].append(f"Missing required payload field: {field}")
                else:
                    # Validate field types
                    value = payload[field]
                    if field == 'url' or field == 'title' or field == 'content' or field == 'source_document':
                        if not isinstance(value, str):
                            validation_result['valid'] = False
                            validation_result['errors'].append(f"Payload field '{field}' must be a string")
                    elif field == 'headings':
                        if not isinstance(value, list):
                            validation_result['valid'] = False
                            validation_result['errors'].append(f"Payload field '{field}' must be a list")
                    elif field == 'chunk_index':
                        if not isinstance(value, int):
                            validation_result['valid'] = False
                            validation_result['errors'].append(f"Payload field '{field}' must be an integer")
                    elif field == 'metadata':
                        if not isinstance(value, dict):
                            validation_result['valid'] = False
                            validation_result['errors'].append(f"Payload field '{field}' must be a dictionary")

        # Additional semantic validations
        if 'url' in result and result['url']:
            url = result['url']
            if not url.startswith(('http://', 'https://', '/', '#', 'mailto:', 'tel:')):
                validation_result['warnings'].append(f"URL may not be properly formatted: {url[:50]}...")

        if 'title' in result and len(result['title']) > 500:
            validation_result['warnings'].append("Title appears to be excessively long")

        if 'content' in result and len(result['content']) < 10 and result['content'].strip():
            validation_result['warnings'].append("Content appears to be very short")

        return validation_result

    def validate_relevance_scoring(self, results: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """
        Validate that the relevance scoring is meaningful and consistent.

        Args:
            results: List of retrieval results
            query: The original query string

        Returns:
            Dictionary with validation results including:
            - valid: boolean indicating if scoring is meaningful
            - score_analysis: statistics about the scores
            - relevance_indicators: measures of semantic relevance
        """
        if not results:
            return {
                'valid': True,
                'score_analysis': {'count': 0, 'avg': 0, 'min': 0, 'max': 0},
                'relevance_indicators': {'is_differentiated': False}
            }

        scores = [result.get('score', 0) for result in results]

        # Calculate basic statistics
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)
        score_range = max_score - min_score

        # Check if scores are differentiated (not all the same)
        is_differentiated = len(set(scores)) > 1 or len(scores) == 1

        # Analyze score distribution
        score_analysis = {
            'count': len(scores),
            'avg': avg_score,
            'min': min_score,
            'max': max_score,
            'range': score_range,
            'std_dev': (sum((x - avg_score) ** 2 for x in scores) / len(scores)) ** 0.5 if len(scores) > 1 else 0
        }

        # Check for meaningful score differences
        meaningful_diff = score_range > 0.05  # At least 5% difference between min and max

        # Validate that scores are within reasonable bounds
        valid_scores = all(isinstance(score, (int, float)) and score == score
                         and score != float('inf') and score != float('-inf')
                         for score in scores)

        relevance_indicators = {
            'is_differentiated': is_differentiated,
            'has_meaningful_diff': meaningful_diff,
            'scores_valid': valid_scores,
            'score_distribution': 'good' if score_range > 0.1 else 'limited'
        }

        validation_result = {
            'valid': valid_scores and len(scores) > 0,
            'score_analysis': score_analysis,
            'relevance_indicators': relevance_indicators
        }

        return validation_result


async def main():
    """Main function for vector storage CLI."""
    import json

    # Load embedded chunks from file
    try:
        with open("embedded_chunks.json", "r", encoding="utf-8") as f:
            embedded_data = json.load(f)

        # We need to reload the actual embeddings from a different file since we truncated them
        # Let's create a function to reconstruct the embedded chunks
        logger.info("Loading embedded chunks from file...")

        # For this example, we'll create a simple test
        storage = VectorStorage()

        # Initialize collection
        storage.initialize_collection()

        # Get collection info
        collection_info = storage.client.get_collection(storage.collection_name)
        logger.info(f"Collection '{storage.collection_name}' has {collection_info.points_count} vectors")

        # Verify storage
        verification = await storage.verify_storage()
        logger.info(f"Storage verification: {verification}")

    except FileNotFoundError:
        logger.error("embedded_chunks.json not found. Run embedding generation first.")
        return


if __name__ == "__main__":
    asyncio.run(main())