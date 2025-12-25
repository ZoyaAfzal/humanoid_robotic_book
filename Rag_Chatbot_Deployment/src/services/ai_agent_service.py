import os
import logging
import time
from typing import List
from datetime import datetime
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents import function_tool

from src.models.agent_models import AgentResponse, RetrievedContext, AgentConfig
from src.models.error_models import AgentError, InsufficientContextError, RetrievalError
from src.services.retrieval_service import retrieval_service


logger = logging.getLogger(__name__)


class AIAgentService:
    """
    Service class for the retrieval-aware AI agent using OpenAI Agents SDK with OpenAI-compatible API.
    Implements custom RAG workflow with explicit retrieval step before generation.
    """

    def __init__(self):
        # Initialize OpenAI client with Google's OpenAI-compatible API
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required for AI agent")

        # Configure AsyncOpenAI client with Google's OpenAI-compatible endpoint
        self.client = AsyncOpenAI(
            api_key=gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Initialize the OpenAI Chat Completions Model with the custom client
        self.model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=self.client
        )

        # Create the agent with tools
        self.agent = Agent(
            name="Humanoid Robotics RAG Agent",
            model=self.model,
            tools=[self._create_retrieval_tool()],
            instructions="You are a helpful assistant for the Humanoid Robotics textbook. First, call the retrieve_context_tool to find relevant information from the book. Then, use ONLY the retrieved context to answer the user's question. Formulate a complete answer based on the retrieved content. If the retrieved context doesn't contain direct information about the query, synthesize the most relevant information available to provide the best possible answer. Only respond with 'I don't know' if absolutely no relevant information is found in the context."
        )

        # Default configuration
        self.default_config = AgentConfig()

    def _create_retrieval_tool(self):
        """Create a retrieval tool that can be used by the agent."""
        @function_tool
        def retrieve_context_tool(query: str, top_k: int = 5, min_score: float = 0.3) -> List[dict]:
            """
            Retrieve context from the humanoid robotics book based on the query.

            Args:
                query: The search query
                top_k: Number of top results to retrieve
                min_score: Minimum similarity score threshold

            Returns:
                List of context chunks with content, score, and metadata
            """
            import asyncio
            # Run the async retrieval in a new event loop if needed
            try:
                loop = asyncio.get_event_loop()
                retrieved = loop.run_until_complete(
                    retrieval_service.retrieve_context(query, top_k=top_k, min_score=min_score)
                )
            except RuntimeError:
                # If no event loop is running, create a new one
                retrieved = asyncio.run(
                    retrieval_service.retrieve_context(query, top_k=top_k, min_score=min_score)
                )

            # Convert RetrievedContext objects to dictionaries
            result = []
            for ctx in retrieved:
                result.append({
                    'content': ctx.content,
                    'score': ctx.score,
                    'url': ctx.url,
                    'title': ctx.title,
                    'headings': ctx.headings,
                    'chunk_index': ctx.chunk_index,
                    'source_document': ctx.source_document
                })

            return result

        return retrieve_context_tool

    async def process_query(
        self,
        query_text: str,
        top_k: int = 5,
        min_score: float = 0.3,
        temperature: float = 0.7
    ) -> AgentResponse:
        """
        Process a user query through the retrieval-aware AI agent.

        Args:
            query_text: The natural language query from the user
            top_k: Number of top results to retrieve
            min_score: Minimum similarity score threshold
            temperature: Temperature setting for the LLM

        Returns:
            AgentResponse with the answer and metadata

        Raises:
            InsufficientContextError: If no relevant context is found
            AgentError: If there's an error during agent processing
        """
        start_time = datetime.now()

        try:
            # First, retrieve the context to provide to the agent
            retrieved_contexts = await retrieval_service.retrieve_context(
                query_text,
                top_k=top_k,
                min_score=min_score
            )

            if not retrieved_contexts:
                # Try with a lower threshold to see if we can get any results at all
                lower_threshold_results = await retrieval_service.retrieve_context(
                    query_text,
                    top_k=top_k,
                    min_score=0.0  # Lower threshold to get any possible results
                )

                if lower_threshold_results:
                    # We found some results even with a very low threshold
                    # Use these results but with very low confidence
                    formatted_context = self._format_context_for_model(lower_threshold_results)

                    messages = [
                        {
                            "role": "system",
                            "content": "You are an expert assistant for the Humanoid Robotics textbook. Use ONLY the provided context to answer the user's question. If the exact information is not available, use related information from the context to provide the best possible answer. Do not make up information that is not in the context. Note that the retrieved information may not be directly related to the query."
                        },
                        {
                            "role": "user",
                            "content": f"Context from Humanoid Robotics textbook:\n\n{formatted_context}\n\nQuestion: {query_text}\n\nPlease provide a comprehensive answer based on the provided context. If the exact information is not available, use related information to provide the best possible answer. If the context is not relevant to the query, please explain that the specific topic may not be covered in the textbook."
                        }
                    ]

                    response = await self.client.chat.completions.create(
                        model="gemini-2.5-flash",
                        messages=messages,
                        temperature=temperature,
                        max_tokens=2000
                    )

                    response_text = response.choices[0].message.content.strip()

                    confidence = self._calculate_confidence(lower_threshold_results, response_text and "I don't know" not in response_text.lower()) * 0.5  # Reduce confidence for low-quality results

                    # Calculate processing time
                    processing_time = (datetime.now() - start_time).total_seconds()

                    sources = list(set([ctx.url for ctx in lower_threshold_results if ctx.url]))  # Unique sources

                    agent_response = AgentResponse(
                        query=query_text,
                        answer=response_text,
                        retrieved_context=lower_threshold_results,
                        confidence=max(confidence, 0.1),  # Ensure minimum confidence of 0.1
                        sources=sources,
                        processing_time=processing_time
                    )

                    logger.info(f"Query processed with low-quality context: '{query_text[:50]}...' "
                               f"(retrieved {len(lower_threshold_results)} low-score contexts, "
                               f"confidence: {max(confidence, 0.1):.2f}, time: {processing_time:.3f}s)")

                    return agent_response
                else:
                    # Use a fallback response when no context is found even with low threshold
                    fallback_response = await self._generate_fallback_response(query_text)

                    processing_time = (datetime.now() - start_time).total_seconds()

                    agent_response = AgentResponse(
                        query=query_text,
                        answer=fallback_response,
                        retrieved_context=[],
                        confidence=0.1,  # Low confidence for fallback
                        sources=[],
                        processing_time=processing_time
                    )

                    logger.warning(f"Fallback response generated for query with no context: '{query_text[:50]}...' "
                                  f"(total time: {processing_time:.3f}s)")

                    return agent_response

            # Format the context for the model
            formatted_context = self._format_context_for_model(retrieved_contexts)

            # Use the OpenAI API directly to generate a response based on the context
            # This gives us more control over how the context is used
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert assistant for the Humanoid Robotics textbook. Use ONLY the provided context to answer the user's question. If the exact information is not available, use related information from the context to provide the best possible answer. Do not make up information that is not in the context."
                },
                {
                    "role": "user",
                    "content": f"Context from Humanoid Robotics textbook:\n\n{formatted_context}\n\nQuestion: {query_text}\n\nPlease provide a comprehensive answer based on the provided context. If the exact information is not available, use related information to provide the best possible answer."
                }
            ]

            response = await self.client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )

            response_text = response.choices[0].message.content.strip()

            # Calculate a basic confidence score based on the number and quality of retrieved contexts
            confidence = self._calculate_confidence(retrieved_contexts, response_text and "I don't know" not in response_text.lower())

            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()

            sources = list(set([ctx.url for ctx in retrieved_contexts if ctx.url]))  # Unique sources

            agent_response = AgentResponse(
                query=query_text,
                answer=response_text,
                retrieved_context=retrieved_contexts,
                confidence=confidence,
                sources=sources,
                processing_time=processing_time
            )

            logger.info(f"Query processed successfully: '{query_text[:50]}...' "
                       f"(retrieved {len(retrieved_contexts)} contexts, "
                       f"confidence: {confidence:.2f}, time: {processing_time:.3f}s)")

            return agent_response

        except Exception as e:
            logger.error(f"Error processing query '{query_text[:50]}...': {str(e)}")
            raise AgentError(f"Failed to process query: {str(e)}")

    async def _generate_fallback_response(self, query: str) -> str:
        """
        Generate a fallback response when no relevant context is found.
        This method is kept for compatibility but may not be used with the Agents SDK approach.

        Args:
            query: The original query that couldn't be answered

        Returns:
            A fallback response explaining the situation
        """
        return (f"I'm sorry, but I couldn't find any relevant information in the humanoid robotics textbook "
                f"to answer your query: '{query}'. The content you're looking for may not be covered in the "
                f"available materials. Please try rephrasing your question or consult other resources.")

    def _format_context_for_model(self, contexts: List[RetrievedContext]) -> str:
        """
        Format retrieved contexts into a string that can be provided to the model.

        Args:
            contexts: List of retrieved contexts

        Returns:
            Formatted string with all contexts
        """
        formatted_parts = ["Here is the relevant context from the humanoid robotics textbook:\n"]

        for i, ctx in enumerate(contexts, 1):
            formatted_parts.append(
                f"Context {i}:\n"
                f"Title: {ctx.title}\n"
                f"URL: {ctx.url}\n"
                f"Content: {ctx.content}\n"
                f"Score: {ctx.score}\n"
                f"---\n"
            )

        return "\n".join(formatted_parts)

    def _calculate_confidence(self, contexts: List[RetrievedContext], is_valid: bool) -> float:
        """
        Calculate a confidence score based on the quality of retrieved contexts and validation result.

        Args:
            contexts: List of retrieved contexts
            is_valid: Whether the response passed grounding validation

        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not contexts:
            return 0.0

        # Calculate average score of retrieved contexts, ensuring scores are numeric
        numeric_scores = []
        for ctx in contexts:
            try:
                numeric_score = float(ctx.score)
            except (TypeError, ValueError):
                numeric_score = 0.0
            numeric_scores.append(numeric_score)
        avg_score = sum(numeric_scores) / len(numeric_scores) if numeric_scores else 0.0

        # Calculate confidence based on average score and number of contexts
        score_factor = min(avg_score * 2, 1.0)  # Normalize score to 0-1 range (scores are typically 0-0.5)
        count_factor = min(len(contexts) / 5.0, 1.0)  # Up to 5 contexts gives full score

        # Combine factors
        base_confidence = (score_factor * 0.6 + count_factor * 0.4)

        return min(base_confidence, 1.0)  # Ensure it doesn't exceed 1.0

# Singleton instance for the service
# Initialize only when needed to avoid API key issues during testing
try:
    agent_service = AIAgentService()
except ValueError:
    # If API key is not set, create a placeholder that will raise an error when used
    class PlaceholderAgentService:
        async def process_query(self, *args, **kwargs):
            raise ValueError("GEMINI_API_KEY environment variable is required for AI agent")

    agent_service = PlaceholderAgentService()