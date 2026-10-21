const { getResponse } = require('./conversation');

const testCases = [
  { message: 'Hi', intent: 'greeting', confidence: 0.95 },
  { message: 'Where is my order?', intent: 'order_tracking', confidence: 0.92 },
  { message: 'Track my order ORD12345', intent: 'order_tracking', confidence: 0.95 },
  { message: 'Cancel order ORD12345', intent: 'order_cancellation', confidence: 0.94 },
  { message: 'My delivery is late ORD12345', intent: 'delivery_delay', confidence: 0.91 },
  { message: 'Return order ORD12345', intent: 'return_request', confidence: 0.93 },
  { message: 'Where is my refund for ORD12345?', intent: 'refund_status', confidence: 0.90 },
  { message: 'Payment failed TXN12345', intent: 'payment_failed', confidence: 0.94 },
  { message: 'Tell me about product PROD456', intent: 'product_information', confidence: 0.90 },
  { message: 'I forgot my password', intent: 'password_reset', confidence: 0.96 },
  { message: 'My product is damaged, order ORD12345', intent: 'damaged_product', confidence: 0.93 },
  { message: 'I want to speak to a human', intent: 'human_agent', confidence: 0.98 },
  { message: 'I think this is fraud', intent: 'complaint', confidence: 0.90 },
  { message: 'Tell me a joke', intent: 'unknown', confidence: 0.90 },
  { message: 'Something is wrong', intent: 'complaint', confidence: 0.25 },
  { message: 'I have a problem with something', intent: 'complaint', confidence: 0.55 },
  { message: 'Bye', intent: 'goodbye', confidence: 0.95 }
];

console.log('===== CHATBOT TEST RESULTS =====');

testCases.forEach(({ message, intent, confidence }, index) => {
  const result = getResponse(intent, confidence, message);

  console.log(`\nTest ${index + 1}: ${message}`);
  console.log(`Intent: ${intent}`);
  console.log(`Confidence: ${confidence}`);
  console.log(`Chatbot reply: ${result.reply}`);
  console.log(`Extracted entities: ${JSON.stringify(result.entities)}`);
  console.log(`Escalated: ${result.escalated}`);
  console.log(`Clarification required: ${Boolean(result.clarificationRequired)}`);

  if (result.escalationReason) {
    console.log(`Escalation reason: ${result.escalationReason}`);
  }
});