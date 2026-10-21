const {
  getResponse,
  updateConversationContext
} = require('../../../chatbot/conversation');

/**
 * Generate a chatbot response using the conversation service.
 *
 * @param {string} intent
 * @param {number} confidence
 * @param {string} message
 * @param {number} clarificationAttempts
 * @returns {{ reply: string, escalated: boolean }}
 */
const generateResponse = (
  intent,
  confidence,
  message = '',
  clarificationAttempts = 0
) => {
  return getResponse(
    intent,
    confidence,
    message,
    clarificationAttempts
  );
};

module.exports = {
  generateResponse,
  updateConversationContext
};