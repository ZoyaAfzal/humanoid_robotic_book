# Chatbot Integration Guide

This document explains the integration of the RAG chatbot into the Humanoid Robotics textbook Docusaurus site.

## Components Integrated

1. **RAGChatWidget.jsx** - Main chat widget component that provides:
   - Floating chat button that appears in different positions
   - Theme-aware design that adapts to light/dark mode
   - Toggle functionality to open/close the chat interface
   - Fixed positioning with high z-index to ensure visibility

2. **ChatInterface.jsx** - Core chat interface component that includes:
   - Message display area with user and agent avatars
   - Input form with text field and send button
   - Loading indicators and error handling
   - Context-aware querying (can ask about selected text)
   - Source attribution for retrieved content
   - Auto-scrolling to latest messages
   - Welcome message with instructions

3. **useChatState.js** - Custom React hook for managing chat state and API communication

4. **apiService.js** - API service layer that communicates with the RAG backend

## Integration Method

The chatbot is integrated using a Layout wrapper approach:

1. **src/theme/Layout/index.js** - Modified to wrap the original layout with ChatLayout
2. **src/theme/ChatLayout.jsx** - Provides the chat interface as an overlay on all pages
3. The chat widget appears as a floating button on all pages and can be toggled open/closed

## Deployment Configuration

The site is configured for GitHub Pages deployment with:
- URL: `https://ZoyaAfzal.github.io`
- Base URL: `/humanoid_robotic_book/`

## How It Works

1. The chat widget appears as a floating button in the bottom-right corner of all pages
2. When clicked, it opens a chat interface that communicates with the RAG backend
3. The backend is configured to connect to the Hugging Face Space at `https://zoya4242-rag-chatbot-deployment.hf.space`
4. The chatbot can access and respond to queries about the humanoid robotics textbook content

## Backend Connection

The chatbot connects to a RAG backend that retrieves information from a Qdrant vector database containing embeddings of the humanoid robotics textbook content. The frontend handles fallback scenarios when the backend is unavailable (common with free-tier Hugging Face Spaces that may be sleeping).

## Development

To run the site locally with the chatbot:
```bash
npm run start
```

The site will be available at `http://localhost:3000/humanoid_robotic_book/`

## GitHub Pages Deployment

The site can be deployed to GitHub Pages using:
```bash
npm run deploy
```

The chatbot will be available on all pages of the deployed site.