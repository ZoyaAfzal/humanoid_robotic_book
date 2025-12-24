/**
 * Test file to verify that the chat widget components are properly connected
 */

import React from 'react';
import { render } from 'react-dom';

// Simple test to ensure the component can be imported and instantiated
console.log('Testing RAG Chat Widget integration...');

// Try to dynamically import the component to verify it exists
const testComponentImport = async () => {
  try {
    const { default: RAGChatWidget } = await import('./RAGChatWidget');
    console.log('✅ RAGChatWidget component loaded successfully');

    // Verify it's a function/component
    if (typeof RAGChatWidget === 'function') {
      console.log('✅ RAGChatWidget is a valid React component');
    } else {
      console.error('❌ RAGChatWidget is not a function/component');
    }
  } catch (error) {
    console.error('❌ Failed to import RAGChatWidget:', error);
  }
};

// Run the test
testComponentImport();

// Test API service
const testApiService = async () => {
  try {
    const { apiService } = await import('./apiService');
    console.log('✅ ApiService loaded successfully');

    // Test config method
    const config = apiService.getConfig();
    console.log('✅ ApiService configuration:', config);
  } catch (error) {
    console.error('❌ Failed to import ApiService:', error);
  }
};

testApiService();

console.log('Frontend-backend integration test completed.');