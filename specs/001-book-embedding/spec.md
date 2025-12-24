# Spec 1: HTML-based RAG Pipeline for Humanoid Robotics Book

## Overview
HTML-based ingestion pipeline that extracts content from the deployed documentation site (https://zoyaafzal.github.io/humanoid_robotic_book/), generates embeddings, and stores them in a vector database to enable a Retrieval-Augmented Generation (RAG) chatbot for the technical book.

## Target Audience
- Developers and AI engineers building a RAG chatbot for a technical book
- End users who will query the chatbot for accurate, book-grounded answers

## Objective
Extract content from the deployed documentation site HTML, convert book content into high-quality vector embeddings using trafilatura for clean text extraction, and store embeddings in a scalable vector database to support semantic search and retrieval.

## Success Criteria
- All documentation URLs are discovered from the sitemap
- Text is cleanly extracted from HTML pages using trafilatura (no navigation, footer, or irrelevant noise)
- Embeddings are generated using Cohere embedding models
- Embeddings and metadata are successfully stored in Qdrant Cloud
- Each vector record contains: source URL and text content
- Data can later be retrieved by semantic similarity search with relevant results
- Implementation is contained in a single main.py file with specific required functions

## Constraints
- ✅ Use **deployed HTML only**
- ❌ Do **not** fetch Markdown or GitHub raw files
- ✅ Modify **only `main.py`**
- ❌ No extra scripts or folders
- Content source: Deployed documentation site (https://zoyaafzal.github.io/humanoid_robotic_book/)
- Embedding model: Cohere embeddings
- Vector database: Qdrant Cloud (Free Tier)
- Chunk size: ~1000-1200 characters
- Collection name: **`robotic_book_embedding`**
- Distance metric: **cosine distance**
- Payload must include: `url` and `text`

## Out of Scope
- User-facing chatbot interface
- Agent orchestration or reasoning logic
- Authentication or rate limiting
- Frontend integration
- Additional scripts or folders beyond main.py

## Assumptions
- Documentation site is deployed and publicly accessible at https://zoyaafzal.github.io/humanoid_robotic_book/
- Qdrant Cloud instance and API key are available
- Cohere API key is available
- This spec only prepares data for downstream RAG components

## Implementation Details

### Required Functions in main.py
- `get_all_urls()` - Fetch all documentation URLs from the sitemap
- `extract_text_from_url(url)` - Download HTML with a timeout, extract clean readable text using `trafilatura`
- `chunk_text(text)` - Split text into ~1000–1200 character chunks, prefer paragraph boundaries, fallback to sentence or hard splits when needed
- `embed(text)` - Generate vector embeddings, trim text to model limits if required, return the embedding vector or `None` on failure
- `create_collection()` - Ensure Qdrant collection exists with name `robotic_book_embedding` and cosine distance
- `save_chunks_to_qdrant(chunk, id, url)` - Store vectors in Qdrant with payload including `url` and `text`
- `main()` - Execute the full ingestion pipeline with progress logs and final summary

### Content Discovery
- Fetch all documentation URLs from the sitemap.xml of the deployed site
- Fallback to known URLs if sitemap is not available
- Handle URL deduplication

### Content Extraction
- Extract clean text content from HTML pages using trafilatura library
- Skip the page if extraction fails or returns empty text
- Handle multiple URLs with timeout protection

### Content Chunking
- Split text into ~1000–1200 character chunks
- Prefer paragraph boundaries for semantic coherence
- Fallback to sentence or hard splits when needed
- Maintain readability and context across chunks

### Embedding Generation
- Generate embeddings using Cohere API
- Use embed-english-v3.0 model optimized for search documents
- Trim text to model limits if required
- Handle API errors gracefully

### Vector Storage
- Store vectors in Qdrant Cloud with specific collection name: `robotic_book_embedding`
- Use cosine distance metric as required
- Include payload with `url` and `text` fields only
- Implement proper error handling and verification

## Outputs
- Single main.py file with all required functions implemented
- Qdrant collection named `robotic_book_embedding` populated with book embeddings
- Progress logs during pipeline execution
- Final summary of URLs processed, chunks created, and vectors stored
- Dependencies managed with uv including trafilatura

## Architecture
- Single-file implementation in main.py with specific function interfaces
- HTML content extraction using trafilatura library
- Cohere embedding generation with text trimming
- Qdrant vector storage with required collection name and cosine distance
- Configuration management with environment variables
- Error handling and logging throughout

---

# Complete Humanoid Robotics Textbook Project

This document also serves as the main specification for the overall Humanoid Robotics Textbook project, which includes multiple specs and plans.

## Project Overview
The Humanoid Robotics Textbook project is a comprehensive educational platform that includes:
1. A Docusaurus-based interactive textbook
2. A RAG-powered chatbot for Q&A
3. Backend services for content processing
4. User authentication and personalization features

## Current Status
- **Spec 1**: HTML-based RAG Pipeline (Completed) - This document
- **Spec 2**: [To be defined] - Frontend Chatbot Interface
- **Spec 3**: [To be defined] - User Authentication System
- **Spec 4**: [To be defined] - Personalization Engine

## Project Components
- **Frontend**: Docusaurus-based textbook interface
- **Backend**: HTML-based RAG pipeline and content processing
- **AI Services**: Cohere embeddings and Qdrant vector database
- **User Services**: Authentication and profile management

## Integration Points
- The HTML-based RAG pipeline feeds content into the vector database
- The chatbot interface queries the vector database
- User profiles influence content personalization
- All components work together to create an interactive learning experience