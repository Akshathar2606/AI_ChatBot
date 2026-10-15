const { extractEntities } = require('./entityExtractor');
const { shouldEscalate, needsClarification } = require('./escalation');
const responses = require('./responses.json');

const CLARIFICATION_REPLY =
  "I'm not completely sure I understood your request. Could you please provide a little more information?";

function getResponse(intent, confidence, message, clarificationAttempts = 0) {
  const entities = extractEntities(message);

  if (shouldEscalate(intent, confidence, message, clarificationAttempts)) {
    return {
      reply: "I'm sorry, but this issue requires assistance from a customer-support agent. I'll connect you with an agent.",
      intent: 'human_agent',
      confidence,
      entities,
      escalated: true,
      escalationReason: 'Customer support escalation required'
    };
  }

  if (needsClarification(confidence) || !Object.prototype.hasOwnProperty.call(responses, intent)) {
    return {
      reply: CLARIFICATION_REPLY,
      intent: 'unknown',
      confidence,
      entities,
      escalated: false,
      clarificationRequired: true
    };
  }

  const selectedResponse = responses[intent];
  const requiredEntities = selectedResponse.requires || [];

  if (intent === 'refund_status') {
    if (!entities.order_id && !entities.transaction_id) {
      return {
        reply: 'Please provide your order ID or transaction ID so I can help check your refund.',
        intent,
        confidence,
        entities,
        escalated: false,
        clarificationRequired: false
      };
    }
  } else {
    const missingEntity = requiredEntities.find((entity) => !entities[entity]);

    if (missingEntity && !(intent === 'product_information' && missingEntity === 'product_id')) {
      const prompts = {
        order_id: {
          order_tracking: 'Sure! Please provide your order ID so I can help track your order.',
          order_status: 'Please provide your order ID so I can help check its status.',
          order_cancellation: 'Please provide your order ID so I can help with cancellation.',
          delivery_delay: 'Please provide your order ID so I can help review the delivery delay.',
          return_request: 'Please provide your order ID so I can help with your return.',
          damaged_product: 'Please provide your order ID so I can help with the damaged product.'
        },
        transaction_id: {
          payment_failed: 'Please provide your transaction ID so I can help with the failed payment.',
          payment_issue: 'Please provide your transaction ID so I can help review the payment issue.'
        }
      };

      return {
        reply: prompts[missingEntity] && prompts[missingEntity][intent]
          ? prompts[missingEntity][intent]
          : `Please provide your ${missingEntity.replace(/_/g, ' ')} so I can help.`,
        intent,
        confidence,
        entities,
        escalated: false,
        clarificationRequired: false
      };
    }
  }

  const availableResponses = selectedResponse.responses;
  const reply = Array.isArray(availableResponses) && availableResponses.length > 0
    ? availableResponses[Math.floor(Math.random() * availableResponses.length)]
    : CLARIFICATION_REPLY;

  return {
    reply,
    intent,
    confidence,
    entities,
    escalated: false,
    clarificationRequired: false
  };
}

function updateConversationContext(context, entities) {
  const safeContext = context && typeof context === 'object' && !Array.isArray(context)
    ? context
    : {};
  const safeEntities = entities && typeof entities === 'object' && !Array.isArray(entities)
    ? entities
    : {};

  return { ...safeContext, ...safeEntities };
}

module.exports = {
  getResponse,
  updateConversationContext
};