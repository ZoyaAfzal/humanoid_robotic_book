import { useState, useCallback } from 'react';
import { apiService } from '../components/apiService';

const useChatState = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Add a message to the chat
  const addMessage = useCallback((message) => {
    setMessages(prev => [...prev, message]);
  }, []);

  // Clear all messages
  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  // Send a query to the backend
  const sendQuery = useCallback(async (query, options = {}) => {
    const {
      top_k = 5,
      min_score = 0.3,
      temperature = 0.7
    } = options;

    setIsLoading(true);
    setError(null);

    try {
      // Add user message immediately
      addMessage({
        type: 'user',
        content: query,
        timestamp: new Date().toISOString()
      });

      // Call the backend API
      const response = await apiService.sendQuery(query, top_k, min_score, temperature);

      // Add agent response
      addMessage({
        type: 'agent',
        content: response.answer,
        sources: response.sources || [],
        confidence: response.confidence,
        processingTime: response.processing_time,
        timestamp: new Date().toISOString()
      });

      return response;
    } catch (err) {
      setError(err.message);

      // Add error message to chat
      addMessage({
        type: 'error',
        content: `Sorry, I encountered an error: ${err.message}`,
        timestamp: new Date().toISOString()
      });

      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [addMessage]);

  // Check if backend is healthy
  const checkBackendHealth = useCallback(async () => {
    try {
      const isHealthy = await apiService.checkHealth();
      return isHealthy;
    } catch (err) {
      setError(err.message);
      return false;
    }
  }, []);

  // Get current chat statistics
  const getStats = useCallback(() => {
    const userMessages = messages.filter(m => m.type === 'user').length;
    const agentMessages = messages.filter(m => m.type === 'agent').length;
    const errorMessages = messages.filter(m => m.type === 'error').length;

    return {
      totalMessages: messages.length,
      userMessages,
      agentMessages,
      errorMessages,
      isLoading
    };
  }, [messages, isLoading]);

  return {
    messages,
    isLoading,
    error,
    addMessage,
    clearMessages,
    sendQuery,
    checkBackendHealth,
    getStats
  };
};

export default useChatState;