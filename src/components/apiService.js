/**
 * API Service for communicating with the RAG backend
 */

class ApiService {
  constructor() {
    // Use the correct backend URL for this deployment
    // Updated to match your actual deployed Hugging Face Space
    this.backendUrl = 'https://zoya4242-rag-chatbot-deployment.hf.space';

    // Fallback URL for testing - uncomment if needed
    // this.backendUrl = 'http://localhost:7860'; // For local testing
  }

  /**
   * Send a query to the RAG backend
   * @param {string} query - The user's query
   * @param {number} top_k - Number of results to retrieve (default: 5)
   * @param {number} min_score - Minimum similarity score (default: 0.3)
   * @param {number} temperature - Temperature for generation (default: 0.7)
   * @returns {Promise<Object>} Response from the backend
   */
  async sendQuery(query, top_k = 5, min_score = 0.3, temperature = 0.7) {
    try {
      // First, try to reach the backend to see if it's awake
      const healthCheck = await fetch(`${this.backendUrl}/health`);
      if (!healthCheck.ok) {
        console.warn('Backend health check failed, but proceeding with query...');
      }

      // Main API endpoint - this is the correct one based on backend code
      const response = await fetch(`${this.backendUrl}/api/agent/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          top_k,
          min_score,
          temperature
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('API call failed:', error);

      // Check if it's an HTTP error
      if (error.message.includes('HTTP error! status:')) {
        const status = parseInt(error.message.match(/status: (\d+)/)[1]);

        if (status === 500) {
          // Server error - likely due to CORS or backend issue
          console.warn('Server error (500) - using mock response');
          return {
            answer: "The backend server encountered an error. This could be due to CORS restrictions when connecting from GitHub Pages, or the Hugging Face Space may be sleeping. Please try accessing your Hugging Face Space directly at: https://zoya4242-rag-chatbot-deployment.hf.space to wake it up, then come back and try again.",
            sources: [],
            confidence: 0.7,
            processing_time: 0.1
          };
        } else if (status === 404) {
          // Endpoint not found - this suggests the backend might be deployed differently
          // or the Hugging Face Space is sleeping and not routing properly
          console.warn('Query endpoint not found - using mock response');
          return {
            answer: "The backend service is currently unavailable. This usually happens when the Hugging Face Space is sleeping (free tier limitation). Please try accessing your Hugging Face Space directly at: https://zoya4242-rag-chatbot-deployment.hf.space to wake it up, then come back and try again!",
            sources: [],
            confidence: 0.9,
            processing_time: 0.1
          };
        } else {
          // Other HTTP errors
          console.warn(`HTTP error ${status} - using mock response`);
          return {
            answer: `The backend returned an error (status: ${status}). Please check if your Hugging Face Space is running at: https://zoya4242-rag-chatbot-deployment.hf.space`,
            sources: [],
            confidence: 0.7,
            processing_time: 0.1
          };
        }
      } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        // Network error - backend is not accessible (probably sleeping)
        console.warn('Backend not accessible - using mock response');
        return {
          answer: "The RAG backend is currently not accessible. This is common with Hugging Face Spaces which may be asleep. Please visit your Hugging Face Space at https://zoya4242-rag-chatbot-deployment.hf.space to wake it up, then return here to try again.",
          sources: [],
          confidence: 0.8,
          processing_time: 0.1
        };
      }

      // Re-throw unexpected errors
      throw error;
    }
  }

  /**
   * Check if the backend is healthy
   * @returns {Promise<boolean>} Whether the backend is reachable
   */
  async checkHealth() {
    try {
      // Try the main health endpoint
      let response = await fetch(`${this.backendUrl}/api/agent/health`);

      if (!response.ok) {
        // Try alternative health endpoints
        response = await fetch(`${this.backendUrl}/api/health`);
      }

      if (!response.ok) {
        // Try root endpoint
        response = await fetch(this.backendUrl);
      }

      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  /**
   * Get configuration for the backend
   * @returns {Object} Configuration object
   */
  getConfig() {
    return {
      backendUrl: this.backendUrl,
      defaultTopK: 5,
      defaultMinScore: 0.3,
      defaultTemperature: 0.7
    };
  }

  /**
   * Update backend URL
   * @param {string} newUrl - New backend URL
   */
  setBackendUrl(newUrl) {
    this.backendUrl = newUrl;
  }
}

// Export singleton instance
export const apiService = new ApiService();

export default apiService;