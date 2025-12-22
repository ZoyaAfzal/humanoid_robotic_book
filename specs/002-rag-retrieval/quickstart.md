# Quickstart Guide: Retrieval-Aware AI Agent

## Prerequisites

1. **Environment Setup**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   # Or if using uv:
   uv sync
   ```

2. **Environment Variables**
   Create a `.env` file in the backend directory:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION_NAME=humanoid_robotics_book
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Setup for AI Agent

### 1. Install Additional Dependencies

Add the required dependencies to your `pyproject.toml`:

```toml
[project]
dependencies = [
    # ... existing dependencies ...
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "google-generativeai>=0.4.0",
    # ... other dependencies
]
```

Then install the dependencies:

```bash
cd backend
uv sync
```

### 2. Verify Qdrant Connection

Ensure the `humanoid_robotic_book` collection exists in Qdrant and contains embeddings from the humanoid robotics textbook.

## Running the Service

### 1. Start the FastAPI Server

```bash
cd backend
uv run uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### 2. Test the Health Endpoint

```bash
curl http://localhost:8000/api/agent/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-17T16:30:00Z",
  "services": {
    "qdrant": "connected",
    "gemini_api": "available",
    "retrieval_pipeline": "operational"
  }
}
```

### 3. Query the Agent

```bash
curl -X POST http://localhost:8000/api/agent/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key principles of humanoid robot locomotion?",
    "top_k": 5,
    "min_score": 0.3
  }'
```

Expected response:
```json
{
  "query": "What are the key principles of humanoid robot locomotion?",
  "answer": "The key principles of humanoid robot locomotion include...",
  "confidence": 0.85,
  "retrieved_chunks": [
    {
      "score": 0.87,
      "payload": {
        "url": "https://example.com/humanoid-locomotion",
        "title": "Humanoid Robot Locomotion Principles",
        "content": "The key principles of humanoid robot locomotion include...",
        "headings": ["Introduction", "Key Principles"],
        "chunk_index": 0,
        "source_document": "humanoid_robotics_textbook",
        "metadata": {}
      }
    }
  ],
  "sources": [
    "https://example.com/humanoid-locomotion"
  ],
  "processing_time": 1.23
}
```

## Validation Steps

### 1. Basic Retrieval Test
Run the basic retrieval validation:
```bash
cd backend
source .venv/bin/activate
python test_retrieval.py
```

This will:
- Connect to the Qdrant collection
- Verify collection exists and has vectors
- Test semantic search with sample queries
- Validate metadata integrity

### 2. Comprehensive Demonstration
Run the full demonstration:
```bash
cd backend
source .venv/bin/activate
python demonstrate_retrieval.py
```

This will:
- Populate test data if collection is empty
- Run multiple query types
- Validate semantic relevance
- Show detailed retrieval results

### 3. Agent Integration Test
Test the full agent pipeline:
```bash
cd backend
source .venv/bin/activate
python test_main.py
```

This will:
- Test retrieval from Qdrant
- Verify Gemini integration
- Validate grounded response generation
- Check error handling for insufficient context

### 4. Custom Query Test
To test with your own queries, create a simple script:
```python
import asyncio
from src.storage.vector_storage import VectorStorage

async def test_custom_query():
    storage = VectorStorage()
    results = await storage.search("your query here", limit=3)

    for result in results:
        print(f"Score: {result['score']:.4f}")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Content: {result['content'][:200]}...")
        print("---")

asyncio.run(test_custom_query())
```

## Expected Output

When running validation scripts, you should see:
- Collection verification status
- Number of vectors in the collection
- Query results with similarity scores
- Metadata validation results
- Performance metrics
- For the AI agent: grounded responses based only on retrieved content

## Troubleshooting

**Q: No results returned**
A: Ensure the Qdrant collection `humanoid_robotic_book` exists and contains vectors

**Q: API connection errors**
A: Verify COHERE_API_KEY, QDRANT credentials, and GOOGLE_API_KEY in your .env file

**Q: Module import errors**
A: Ensure you've activated the virtual environment and installed dependencies

**Q: Agent returns insufficient context error**
A: Check that your query matches content in the vector database or try with a lower min_score threshold

**Q: Gemini API errors**
A: Verify your Google API key and ensure you have access to the gemini-2.5-flash model

## Validation Success Criteria

The retrieval-aware AI agent is validated when:
- ✅ Semantic queries return relevant content from Qdrant
- ✅ Gemini generates responses based only on retrieved context
- ✅ Responses include proper citations to sources
- ✅ Error handling works when context is insufficient
- ✅ API endpoints respond within 5 seconds
- ✅ All metadata fields are preserved in responses