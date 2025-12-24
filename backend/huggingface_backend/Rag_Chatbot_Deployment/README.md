---
title: Humanoid Robotics RAG Agent
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
---

# Humanoid Robotics RAG Agent

This is a Retrieval-Augmented Generation (RAG) system for humanoid robotics documentation. It uses vector search to find relevant information from the Humanoid Robotics textbook and generates contextual answers to user queries.

## Features

- Semantic search across humanoid robotics documentation
- Context-aware response generation using AI
- Real-time query processing
- Comprehensive coverage of humanoid robotics topics including:
  - Spec-Kit Plus methodology
  - ROS 2 architecture
  - Gazebo simulation
  - Path planning
  - AI agents for control

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/agent/query` - Query endpoint for asking questions about humanoid robotics

## How to Use

Send a POST request to `/api/agent/query` with a JSON body containing your query:

```json
{
  "query": "What is the Spec-Kit Plus workflow?"
}
```

## Architecture

- FastAPI backend
- Qdrant vector database for semantic search
- Cohere for embeddings
- Google Gemini for response generation
- Comprehensive documentation from humanoid robotics textbook

## Environment Variables Required

- `QDRANT_URL`: URL for Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant
- `QDRANT_COLLECTION_NAME`: Name of the collection to use
- `COHERE_API_KEY`: API key for Cohere embeddings
- `GEMINI_API_KEY`: API key for Google Gemini

## Deployment

This space is deployed using Docker on Hugging Face Spaces. The application is built using FastAPI and runs on port 7860 by default.

## About

This RAG system was developed to provide easy access to comprehensive information about humanoid robotics, including methodologies like Spec-Kit Plus, ROS 2 architecture, simulation environments, and AI control systems.