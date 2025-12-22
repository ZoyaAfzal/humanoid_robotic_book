/**
 * API Service for communicating with the RAG backend
 */

class ApiService {
  constructor() {
    // Use the correct backend URL for this deployment
    this.backendUrl = 'http://localhost:8003';
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
      throw error;
    }
  }

  /**
   * Check if the backend is healthy
   * @returns {Promise<boolean>} Whether the backend is reachable
   */
  async checkHealth() {
    try {
      const response = await fetch(`${this.backendUrl}/api/agent/health`);
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