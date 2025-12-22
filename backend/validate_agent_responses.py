"""
Comprehensive validation script for the retrieval-aware AI agent.
Validates response accuracy, grounding, and success criteria.
"""
import asyncio
import time
from typing import List, Dict, Any
from datetime import datetime

from src.services.ai_agent_service import AIAgentService
from src.services.retrieval_service import retrieval_service
from src.models.agent_models import AgentResponse


class AgentValidator:
    """
    Comprehensive validator for the retrieval-aware AI agent.
    Validates responses against success criteria and quality metrics.
    """

    def __init__(self):
        self.agent_service = AIAgentService()

    async def validate_response_quality(self, response: AgentResponse) -> Dict[str, Any]:
        """
        Validate the quality of a single agent response.

        Args:
            response: The agent response to validate

        Returns:
            Dictionary with validation results
        """
        validation_results = {
            'query_valid': len(response.query.strip()) > 0,
            'answer_valid': len(response.answer.strip()) > 0,
            'confidence_valid': 0.0 <= response.confidence <= 1.0,
            'sources_valid': len(response.sources) >= 0,  # Allow empty sources if no context found
            'processing_time_valid': response.processing_time >= 0,
            'context_grounding_valid': False,  # This will be calculated separately
            'content_relevance': 0.0,  # Calculated based on context and answer similarity
        }

        # Check if answer is grounded in retrieved context
        if response.retrieved_context:
            # Calculate similarity between answer and retrieved contexts
            answer_lower = response.answer.lower()
            total_similarity = 0
            valid_contexts = 0

            for ctx in response.retrieved_context:
                if len(ctx.content) > 10:  # Only consider meaningful contexts
                    ctx_lower = ctx.content.lower()
                    # Calculate word overlap
                    answer_words = set(answer_lower.split())
                    ctx_words = set(ctx_lower.split())

                    if answer_words and ctx_words:
                        intersection = answer_words.intersection(ctx_words)
                        similarity = len(intersection) / max(len(answer_words), len(ctx_words))
                        total_similarity += similarity
                        valid_contexts += 1

            if valid_contexts > 0:
                avg_similarity = total_similarity / valid_contexts
                validation_results['content_relevance'] = avg_similarity
                validation_results['context_grounding_valid'] = avg_similarity > 0.05  # 5% threshold

        # If no contexts were retrieved, the answer should indicate this appropriately
        else:
            # For fallback responses, check if it acknowledges lack of context
            answer_lower = response.answer.lower()
            has_fallback_indicators = any(
                indicator in answer_lower
                for indicator in ["couldn't find", "no relevant", "not covered", "sorry"]
            )
            validation_results['context_grounding_valid'] = has_fallback_indicators
            validation_results['content_relevance'] = 1.0 if has_fallback_indicators else 0.0

        # Overall quality score
        quality_score = (
            (1.0 if validation_results['query_valid'] else 0.0) * 0.1 +
            (1.0 if validation_results['answer_valid'] else 0.0) * 0.2 +
            (validation_results['confidence_valid'] * 0.1) +
            (validation_results['context_grounding_valid'] * 0.4) +
            (min(validation_results['content_relevance'], 1.0) * 0.2)
        )

        validation_results['overall_quality_score'] = quality_score

        return validation_results

    async def validate_success_criteria(self) -> Dict[str, Any]:
        """
        Validate the agent against the defined success criteria.

        Returns:
            Dictionary with validation results for all success criteria
        """
        test_queries = [
            "What are the key principles of humanoid robot locomotion?",
            "Explain the design of humanoid robot joints.",
            "How do humanoid robots maintain balance?",
            "What sensors are used in humanoid robotics?",
            "Describe the control systems for humanoid robots."
        ]

        results = {
            'total_queries': len(test_queries),
            'successful_responses': 0,
            'grounded_responses': 0,
            'avg_confidence': 0.0,
            'avg_processing_time': 0.0,
            'validation_details': []
        }

        total_confidence = 0.0
        total_processing_time = 0.0

        for query in test_queries:
            try:
                # Process the query
                response = await self.agent_service.process_query(
                    query_text=query,
                    top_k=5,
                    min_score=0.3,
                    temperature=0.7
                )

                # Validate the response
                validation = await self.validate_response_quality(response)

                results['validation_details'].append({
                    'query': query,
                    'validation': validation,
                    'confidence': response.confidence,
                    'processing_time': response.processing_time
                })

                if validation['query_valid'] and validation['answer_valid']:
                    results['successful_responses'] += 1

                if validation['context_grounding_valid']:
                    results['grounded_responses'] += 1

                total_confidence += response.confidence
                total_processing_time += response.processing_time

            except Exception as e:
                print(f"Error processing query '{query}': {str(e)}")
                # Add failed validation entry
                results['validation_details'].append({
                    'query': query,
                    'validation': {'error': str(e)},
                    'confidence': 0.0,
                    'processing_time': 0.0
                })

        # Calculate averages
        successful_count = len([v for v in results['validation_details']
                               if 'error' not in v['validation']])
        if successful_count > 0:
            results['avg_confidence'] = total_confidence / successful_count
            results['avg_processing_time'] = total_processing_time / successful_count

        # Calculate success rates
        results['success_rate'] = results['successful_responses'] / len(test_queries) if test_queries else 0
        results['grounding_rate'] = results['grounded_responses'] / len(test_queries) if test_queries else 0

        return results

    async def run_comprehensive_validation(self) -> Dict[str, Any]:
        """
        Run comprehensive validation of the agent system.

        Returns:
            Dictionary with comprehensive validation results
        """
        start_time = datetime.now()

        print("Starting comprehensive validation of the retrieval-aware AI agent...")

        # Validate retrieval system
        retrieval_stats = await retrieval_service.get_retrieval_stats()
        print(f"Retrieval system status: {retrieval_stats}")

        # Validate success criteria
        success_validation = await self.validate_success_criteria()

        # Validate edge cases
        edge_case_results = await self.validate_edge_cases()

        total_time = (datetime.now() - start_time).total_seconds()

        comprehensive_results = {
            'validation_timestamp': start_time.isoformat(),
            'total_validation_time': total_time,
            'retrieval_system': retrieval_stats,
            'success_criteria': success_validation,
            'edge_case_validation': edge_case_results,
            'overall_status': 'pass' if success_validation['success_rate'] >= 0.8 else 'partial_pass'
        }

        return comprehensive_results

    async def validate_edge_cases(self) -> Dict[str, Any]:
        """
        Validate the agent with edge cases.

        Returns:
            Dictionary with edge case validation results
        """
        edge_cases = [
            "This is a completely random query that should not match any content.",
            "Short query.",
            "What? Explain.",
            "",  # Empty query (this might cause validation errors)
        ]

        results = {
            'tested_cases': len(edge_cases),
            'handled_gracefully': 0,
            'fallback_responses': 0,
            'edge_case_details': []
        }

        for case in edge_cases:
            try:
                if case.strip():  # Only process non-empty queries
                    response = await self.agent_service.process_query(
                        query_text=case,
                        top_k=5,
                        min_score=0.3,
                        temperature=0.7
                    )

                    # Check if it's a fallback response
                    is_fallback = "couldn't find" in response.answer.lower() or \
                                 "no relevant" in response.answer.lower() or \
                                 "sorry" in response.answer.lower()

                    results['edge_case_details'].append({
                        'case': case,
                        'handled': True,
                        'is_fallback': is_fallback,
                        'response_length': len(response.answer)
                    })

                    results['handled_gracefully'] += 1
                    if is_fallback:
                        results['fallback_responses'] += 1
                else:
                    # Skip empty query as it should raise validation error
                    results['edge_case_details'].append({
                        'case': case,
                        'handled': False,
                        'error': 'Empty query validation error expected',
                        'is_fallback': False
                    })
            except Exception as e:
                # Expected for some edge cases
                results['edge_case_details'].append({
                    'case': case,
                    'handled': False,
                    'error': str(e),
                    'is_fallback': False
                })

        return results


async def main():
    """
    Main function to run the comprehensive validation.
    """
    validator = AgentValidator()

    print("Running comprehensive validation of the retrieval-aware AI agent...")
    print("=" * 60)

    try:
        results = await validator.run_comprehensive_validation()

        print("\nCOMPREHENSIVE VALIDATION RESULTS")
        print("=" * 60)
        print(f"Validation Timestamp: {results['validation_timestamp']}")
        print(f"Total Validation Time: {results['total_validation_time']:.2f} seconds")
        print()

        print("RETRIEVAL SYSTEM STATUS:")
        print(f"  Collection exists: {results['retrieval_system'].get('collection_exists', 'Unknown')}")
        print(f"  Sample search works: {results['retrieval_system'].get('sample_search_works', 'Unknown')}")
        print(f"  Vector count: {results['retrieval_system'].get('vector_count', 'Unknown')}")
        print()

        print("SUCCESS CRITERIA VALIDATION:")
        success_data = results['success_criteria']
        print(f"  Total queries tested: {success_data['total_queries']}")
        print(f"  Successful responses: {success_data['successful_responses']}")
        print(f"  Success rate: {success_data['success_rate']:.2%}")
        print(f"  Grounded responses: {success_data['grounded_responses']}")
        print(f"  Grounding rate: {success_data['grounding_rate']:.2%}")
        print(f"  Average confidence: {success_data['avg_confidence']:.2f}")
        print(f"  Average processing time: {success_data['avg_processing_time']:.3f}s")
        print()

        print("EDGE CASE VALIDATION:")
        edge_data = results['edge_case_validation']
        print(f"  Test cases: {edge_data['tested_cases']}")
        print(f"  Handled gracefully: {edge_data['handled_gracefully']}")
        print(f"  Fallback responses: {edge_data['fallback_responses']}")

        print("\nOVERALL STATUS:", results['overall_status'].upper())

    except Exception as e:
        print(f"Validation failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())