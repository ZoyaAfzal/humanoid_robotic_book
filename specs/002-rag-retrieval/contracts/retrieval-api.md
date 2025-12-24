# API Contract: RAG Retrieval Service

## Overview
This document specifies the API contract for the RAG retrieval service that validates semantic search functionality against the `humanoid_robotics_book` Qdrant collection.

## Endpoints

### POST /retrieve
Execute a semantic search against the vector database.

**Request**
```json
{
  "query": "natural language query text",
  "limit": 5,
  "collection": "humanoid_robotics_book"
}
```

**Request Parameters**
- `query` (string, required): Natural language query to search for
- `limit` (integer, optional): Maximum number of results to return (default: 5, max: 10)
- `collection` (string, optional): Name of collection to search (default: "humanoid_robotics_book")

**Response - Success (200)**
```json
{
  "query": "natural language query text",
  "results": [
    {
      "score": 0.7421,
      "payload": {
        "url": "https://example.com/page",
        "title": "Page Title",
        "content": "Full content text...",
        "headings": ["Heading 1", "Heading 2"],
        "chunk_index": 0,
        "source_document": "doc_id",
        "metadata": {}
      },
      "url": "https://example.com/page",
      "title": "Page Title",
      "content": "Content preview..."
    }
  ],
  "total_results": 1,
  "query_time_ms": 123.45
}
```

**Response - Error (400/500)**
```json
{
  "error": "error message",
  "status_code": 400
}
```

### GET /validate
Validate the retrieval pipeline status.

**Response - Success (200)**
```json
{
  "collection_exists": true,
  "vector_count": 1250,
  "sample_search_works": true,
  "last_updated": "2025-12-17T10:30:00Z"
}
```

## Data Models

### QueryRequest
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | Natural language search query |
| limit | integer | No | Number of results to return (1-10) |
| collection | string | No | Collection name to search |

### SearchResult
| Field | Type | Description |
|-------|------|-------------|
| score | number | Similarity score (0.0-1.0) |
| payload | object | Original stored data |
| url | string | Source URL |
| title | string | Document title |
| content | string | Content preview |

### ValidationResponse
| Field | Type | Description |
|-------|------|-------------|
| collection_exists | boolean | Whether collection exists |
| vector_count | integer | Number of vectors in collection |
| sample_search_works | boolean | Whether sample search succeeds |
| last_updated | string | ISO timestamp of last update |

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Invalid query parameters |
| 404 | Collection not found |
| 500 | Internal server error (API connectivity, etc.) |
| 503 | Service unavailable (Qdrant/Cohere down) |

## Performance Requirements

- Response time: <5 seconds for 90% of requests
- Availability: >95% uptime
- Throughput: Support concurrent queries