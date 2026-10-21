const axios = require('axios');

/**
 * Call Python AI/ML service to get intent prediction
 * @param {string} message - User message
 * @returns {Promise<Object>} - { intent, confidence }
 */
const getPrediction = async (message) => {
  try {
    const response = await axios.post(
      `${process.env.AI_SERVICE_URL}/predict`,
      { message },
      { timeout: 10000 } // 10 second timeout
    );

    // Python service returns: { intent, confidence }
    return {
      intent: response.data.intent,
      confidence: response.data.confidence
    };
  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      console.error('AI Service Error: Connection refused - service may not be running');
      throw new Error('AI prediction service is not available');
    } else if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
      console.error('AI Service Error: Request timeout');
      throw new Error('AI prediction service timeout');
    } else if (error.response) {
      console.error('AI Service Error: HTTP', error.response.status, error.response.statusText);
      throw new Error(`AI prediction service error: ${error.response.status}`);
    } else {
      console.error('AI Service Error:', error.message);
      throw new Error('Failed to get AI prediction');
    }
  }
};

module.exports = {
  getPrediction
};
