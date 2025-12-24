# Humanoid Robotics RAG Pipeline

This backend service processes the Humanoid Robotics textbook content, generates embeddings, and stores them in Qdrant for semantic search capabilities.

## Overview

The RAG (Retrieval-Augmented Generation) pipeline consists of three main components:

1. **Content Extraction** (`src/extraction/`) - Discovers and extracts clean content from deployed Docusaurus URLs
2. **Embedding Generation** (`src/embeddings/`) - Chunks content and generates vector embeddings using Cohere
3. **Vector Storage** (`src/storage/`) - Stores embeddings with metadata in Qdrant vector database

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Cohere API key for embedding generation
- Qdrant Cloud account for vector storage

## Setup

1. **Install dependencies with pip** (alternative to uv):
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -r ../requirements.txt
   # Or install from pyproject.toml:
   # pip install -e .
   ```

2. **Configure environment variables**:
   ```bash
   cp .env .env.local
   # Edit .env.local with your actual API keys and configuration
   # Or copy the example:
   cp .env.example .env.local
   # Then edit .env.local with your actual API keys
   ```

3. **Environment Variables**:
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant Cloud cluster URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `BOOK_BASE_URL`: Base URL of the deployed Docusaurus book (default: https://ZoyaAfzal.github.io/humanoid_robotic_book)
   - `CHUNK_SIZE`: Maximum size of text chunks (default: 1000)
   - `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
   - `BATCH_SIZE`: Batch size for embedding generation (default: 96)
   - `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: humanoid_robotics_book)

## Usage

### Run the complete pipeline:

With uv (recommended):
```bash
cd backend
uv run src.main:main
```

Or using the defined script:
```bash
uv run process-book
```

Alternative with pip/virtual environment:
```bash
cd backend
source .venv/bin/activate
python src/main.py
```

### Run individual components:

1. **Extract content only**:
   ```bash
   uv run extract-content
   ```

2. **Generate embeddings only** (requires extracted_content.json):
   ```bash
   uv run generate-embeddings
   ```

3. **Store vectors only** (requires embedded_chunks.json):
   ```bash
   uv run store-vectors
   ```

## Architecture

### Content Extraction
- Discovers URLs from sitemap.xml and known Docusaurus structure
- Extracts clean text content, removing navigation, headers, footers
- Preserves headings and document structure
- Handles multiple URLs concurrently with rate limiting

### Embedding Generation
- Chunks content semantically with configurable size and overlap
- Uses Cohere's `embed-english-v3.0` model optimized for search documents
- Processes content in batches to respect API limits
- Preserves metadata for each chunk

### Vector Storage
- Creates/uses Qdrant collection with appropriate vector dimensions (1024 for Cohere)
- Stores vectors with rich metadata (URL, title, content, headings)
- Implements proper error handling and verification

## Data Schema

Each stored vector contains:
- `url`: Source URL of the content
- `title`: Page title
- `content`: Text content chunk
- `headings`: List of headings found in the content
- `chunk_index`: Position of the chunk in the original document
- `source_document`: Reference to the original document
- `metadata`: Additional metadata including original chunk index and text length

## Configuration

The pipeline is fully configurable through environment variables, allowing you to:
- Adjust chunk size and overlap for optimal semantic preservation
- Modify batch sizes for API efficiency
- Change the target Qdrant collection
- Update the source book URL

## Testing & Validation

A comprehensive test and validation suite is available to verify the RAG pipeline functionality:

### Core Testing
```bash
python test_main.py
```

This tests:
- URL fetching from sitemap
- Text extraction from web pages
- Text chunking functionality
- All without requiring API keys or external services

### RAG Retrieval Validation

This project includes comprehensive validation tools to verify the semantic retrieval functionality:

- **Query Validation**: `validate_queries.py` - Validates that semantic queries return relevant content with proper metadata
- **Metadata Validation**: `validate_metadata.py` - Validates that metadata associated with retrieved chunks remains intact and queryable
- **Relevance Validation**: `validate_relevance.py` - Validates that retrieved content is semantically relevant to the query
- **Comprehensive Validation**: `validate_all_criteria.py` - Validates all success criteria defined in the specification

#### Running Validation Tests

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run query validation
python validate_queries.py

# Run metadata validation
python validate_metadata.py

# Run semantic relevance validation
python validate_relevance.py

# Run comprehensive validation of all success criteria
python validate_all_criteria.py

# Run specific test files
python -m pytest tests/
```

#### Required Environment Variables

The validation tools require the following environment variables to be set in `.env`:

```env
QDRANT_URL="your_qdrant_cluster_url"
QDRANT_API_KEY="your_qdrant_api_key"
COHERE_API_KEY="your_cohere_api_key"
QDRANT_COLLECTION_NAME="humanoid_robotics_book"  # Default collection name
```

#### Validation Framework

The system includes a comprehensive validation framework that:
- Tests semantic query response with proper metadata
- Validates metadata integrity and completeness
- Checks semantic relevance of retrieved content
- Measures performance against all success criteria
- Provides detailed validation reports

## Output

The pipeline generates the following statistics:
- Count of discovered URLs
- Count of content chunks created
- Count of vectors stored in Qdrant
- Verification of successful storage and retrieval

## Retrieval-Aware AI Agent

The system now includes a retrieval-aware AI agent that answers questions using content from the humanoid robotics textbook. The agent integrates semantic retrieval from Qdrant and exposes functionality through a FastAPI endpoint.

### API Endpoints

- `POST /api/agent/query` - Submit a query to the AI agent
- `GET /api/agent/health` - Check the health status of the agent service
- `GET /api/agent/` - Get information about the agent service

### Frontend Integration

The AI agent is seamlessly integrated into the Docusaurus documentation site with a floating chat widget that appears on all pages:

#### Features
- **Floating Chat Widget**: A 💬 icon appears in the bottom-right corner of every page
- **Context-Aware Queries**: Select text on any page and ask questions about specific content
- **Persistent Across Pages**: Chat history persists as you navigate through the documentation

#### Configuration
The frontend-backend connection is configured via environment variables:

```env
# URL for the backend RAG service
REACT_APP_BACKEND_URL=http://localhost:8000  # For development
# REACT_APP_BACKEND_URL=https://your-production-url.com  # For production
```

#### Usage
1. Click the 💬 icon to open the chat interface
2. Type your question about humanoid robotics concepts
3. Select text on the page and ask context-specific questions
4. View responses with source citations and confidence scores

### API Usage

1. **Start the FastAPI server**:
   ```bash
   cd backend
   uv run uvicorn main:app --reload --port 8000
   ```

2. **Query the agent**:
   ```bash
   curl -X POST http://localhost:8000/api/agent/query \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the key principles of humanoid robot locomotion?",
       "top_k": 5,
       "min_score": 0.3,
       "temperature": 0.7
     }'
   ```

3. **Check health status**:
   ```bash
   curl http://localhost:8000/api/agent/health
   ```

### Required Environment Variables

For the AI agent functionality, you need to add the following to your `.env` file:

```env
GEMINI_API_KEY="your_gemini_api_key"  # For OpenAI-compatible API access to Gemini
```

### Agent Configuration

The agent supports the following parameters:
- `query`: The natural language question to answer (required)
- `top_k`: Number of top results to retrieve (default: 5, min: 1, max: 20)
- `min_score`: Minimum similarity score threshold (default: 0.3, min: 0.0, max: 1.0)
- `temperature`: Temperature setting for the LLM (default: 0.7, min: 0.0, max: 1.0)

## Reproducibility

The pipeline is designed to be idempotent - running it multiple times will update the collection without creating duplicates. The Qdrant collection is recreated on each run to ensure consistency.