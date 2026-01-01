# Data Model: Retrieval-Aware AI Agent

## Core Entities

### RetrievedChunk
Represents a segment of book content returned by the semantic query

**Fields:**
- `score` (float): Similarity score between query and chunk (0.0 to 1.0)
- `payload` (dict): Original stored data containing:
  - `url` (string): Source URL of the content
  - `title` (string): Page title or section heading
  - `content` (string): Text content of the chunk
  - `headings` (list): List of section headings
  - `chunk_index` (int): Position of chunk in original document
  - `source_document` (string): Identifier for the source document
  - `metadata` (dict): Additional metadata

### QueryRequest
Represents a semantic query submitted to the RAG pipeline

**Fields:**
- `query_text` (string): Natural language query text
- `limit` (int): Maximum number of results to return (default: 5)
- `collection_name` (string): Name of Qdrant collection to search
- `min_score` (float): Minimum similarity score threshold (default: 0.3)

### SearchResults
Container for retrieval results

**Fields:**
- `results` (list): List of RetrievedChunk objects
- `query_time` (float): Time taken to execute the search (seconds)
- `total_results` (int): Total number of matching results found

### AgentResponse
Response from the retrieval-aware AI agent

**Fields:**
- `query` (string): The original query text
- `answer` (string): The AI-generated answer based on retrieved context
- `retrieved_chunks` (list): List of RetrievedChunk objects used to generate the answer
- `confidence` (float): Confidence score for the answer (0.0 to 1.0)
- `sources` (list): List of source URLs used in the response
- `processing_time` (float): Total time for retrieval and generation (seconds)

### AgentConfig
Configuration for the retrieval-aware AI agent

**Fields:**
- `model_name` (string): Name of the LLM to use (e.g., "gemini-2.5-flash")
- `max_tokens` (int): Maximum tokens for the response
- `temperature` (float): Temperature setting for the LLM (0.0 to 1.0)
- `context_window` (int): Maximum context window size in tokens

## Relationships
- QueryRequest → SearchResults (1:1) - Each query produces one result set
- SearchResults → RetrievedChunk (1:*) - Each result set contains multiple chunks
- QueryRequest → AgentResponse (1:1) - Each query produces one agent response
- AgentResponse → RetrievedChunk (1:*) - Each response uses multiple retrieved chunks

## Validation Rules
- RetrievedChunk.score must be between 0.0 and 1.0
- RetrievedChunk.payload must contain all required metadata fields (url, title, content)
- QueryRequest.query_text must not be empty
- QueryRequest.limit must be between 1 and 20
- QueryRequest.min_score must be between 0.0 and 1.0
- AgentResponse.answer must not be empty when retrieved_chunks is not empty
- AgentResponse.confidence must be between 0.0 and 1.0
- AgentResponse.sources must correspond to the URLs in retrieved_chunks

## State Transitions
- QueryRequest: PENDING → PROCESSING → COMPLETED/ERROR
- RetrievedChunk: RETRIEVED → VALIDATED → RETURNED
- AgentResponse: PROCESSING → COMPLETED/ERROR