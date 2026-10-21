/**
 * Response Service
 * Handles chatbot response generation based on intent
 * 
 * NOTE FOR M4 (chatbot team member):
 * This is a TEMPORARY implementation with basic responses.
 * Please replace this with your detailed conversation flow,
 * escalation rules, and context-aware response generation.
 * 
 * Interface to preserve:
 * - Input: intent (string), confidence (number)
 * - Output: { reply: string, escalated: boolean }
 */

/**
 * Generate chatbot reply based on intent
 * @param {string} intent - Detected intent from AI service
 * @param {number} confidence - Confidence score (0-1)
 * @returns {Object} - { reply, escalated }
 */
const generateResponse = (intent, confidence) => {
  // TEMPORARY: Basic response mapping
  // M4 should replace this with proper conversation flow
  
  const responses = {
    'return_request': 'Sure! I can help you with your return. Please provide your order ID.',
    'track_order': 'I\'ll help you track your order. Please provide your order ID or tracking number.',
    'product_inquiry': 'I\'d be happy to help with product information. What would you like to know?',
    'complaint': 'I understand your concern. Let me connect you with a specialist who can assist you better.',
    'payment_issue': 'I can help with payment issues. Please describe the problem you\'re experiencing.',
    'cancel_order': 'I can help you cancel your order. Please provide your order ID.',
    'greeting': 'Hello! How can I assist you today?',
    'thanks': 'You\'re welcome! Is there anything else I can help you with?',
    'goodbye': 'Thank you for contacting us. Have a great day!'
  };

  // Default response for unknown intents
  const defaultReply = 'I understand you need assistance. Could you please provide more details?';
  
  // Get reply based on intent
  const reply = responses[intent] || defaultReply;

  // TEMPORARY: Simple escalation rule based on confidence
  // M4 should implement proper escalation logic
  const escalated = confidence < 0.5 || intent === 'complaint';

  return {
    reply,
    escalated
  };
};

module.exports = {
  generateResponse
};
