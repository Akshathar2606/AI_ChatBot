const { extractEntities } = require('./entityExtractor');
const { shouldEscalate } = require('./escalation');
const responses = require('./responses.json');

const CLARIFICATION_REPLY =
  "I'm not completely sure I understood your request. Could you please provide a little more information?";

function getResponse(intent, confidence, message, clarificationAttempts = 0) {
  const entities = extractEntities(message);

  const normalizedIntent =
    typeof intent === 'string' ? intent.toLowerCase() : '';

  const normalizedMessage =
    typeof message === 'string' ? message.toLowerCase() : '';

  // Detect explicit requests for a human agent.
  const explicitHumanRequest =
    normalizedIntent === 'human_agent' ||
    [
      'talk to a human',
      'talk to an agent',
      'human agent',
      'customer support agent',
      'real person',
      'speak to someone',
      'speak to a human',
      'speak to an agent',
      'connect me to support',
      'connect me to an agent'
    ].some((phrase) => normalizedMessage.includes(phrase));

  // Detect potentially fraudulent or unauthorized transactions.
  const securityIssue = [
    'fraud',
    'fraudulent',
    'unauthorized transaction',
    'unauthorised transaction',
    'scam',
    'stolen',
    'used my card without permission',
    'someone used my card',
    'card used without my permission',
    'unauthorized card use',
    'unauthorised card use',
    'charged without my permission',
    'transaction without my permission',
    'used my credit card without permission',
    'used my debit card without permission'
  ].some((phrase) => normalizedMessage.includes(phrase));

  // Escalate explicit human requests and security-sensitive issues.
  // Ordinary complaints are not automatically escalated by shouldEscalate().
  if (
    explicitHumanRequest ||
    securityIssue ||
    (
      normalizedIntent !== 'unknown' &&
      normalizedIntent !== 'complaint' &&
      shouldEscalate(
        intent,
        confidence,
        message,
        clarificationAttempts
      )
    )
  ) {
    return {
      reply:
        "I'm sorry, but this issue requires assistance from a customer-support agent. I'll connect you with an agent.",
      intent: 'human_agent',
      confidence,
      entities,
      escalated: true,
      escalationReason: 'Customer support escalation required',
      clarificationRequired: false
    };
  }

  // Ask for clarification when the intent is unknown.
  if (
    normalizedIntent === 'unknown' ||
    !Object.prototype.hasOwnProperty.call(responses, normalizedIntent)
  ) {
    return {
      reply: CLARIFICATION_REPLY,
      intent: 'unknown',
      confidence,
      entities,
      escalated: false,
      clarificationRequired: true
    };
  }

  const selectedResponse = responses[normalizedIntent];
  const requiredEntities = selectedResponse.requires || [];

  // Refund inquiries need an order ID or transaction ID.
  if (normalizedIntent === 'refund_status') {
    if (!entities.order_id && !entities.transaction_id) {
      return {
        reply:
          'Please provide your order ID or transaction ID so I can help check your refund.',
        intent: normalizedIntent,
        confidence,
        entities,
        escalated: false,
        clarificationRequired: false
      };
    }
  } else {
    // Check whether the user has supplied the required information.
    const missingEntity = requiredEntities.find(
      (entity) => !entities[entity]
    );

    if (
      missingEntity &&
      !(
        normalizedIntent === 'product_information' &&
        missingEntity === 'product_id'
      )
    ) {
      const prompts = {
        order_id: {
          order_tracking:
            'Sure! Please provide your order ID so I can help track your order.',
          order_status:
            'Please provide your order ID so I can help check its status.',
          order_cancellation:
            'Please provide your order ID so I can help with cancellation.',
          delivery_delay:
            'Please provide your order ID so I can help review the delivery delay.',
          return_request:
            'Please provide your order ID so I can help with your return.',
          damaged_product:
            'Please provide your order ID so I can help with the damaged product.'
        },
        transaction_id: {
          payment_failed:
            'Please provide your transaction ID so I can help with the failed payment.',
          payment_issue:
            'Please provide your transaction ID so I can help review the payment issue.'
        }
      };

      return {
        reply:
          prompts[missingEntity] &&
          prompts[missingEntity][normalizedIntent]
            ? prompts[missingEntity][normalizedIntent]
            : `Please provide your ${missingEntity.replace(/_/g, ' ')} so I can help.`,
        intent: normalizedIntent,
        confidence,
        entities,
        escalated: false,
        clarificationRequired: false
      };
    }
  }

  // Select a response for the predicted intent.
  const availableResponses = selectedResponse.responses;

  const reply =
    Array.isArray(availableResponses) && availableResponses.length > 0
      ? availableResponses[
          Math.floor(Math.random() * availableResponses.length)
        ]
      : CLARIFICATION_REPLY;

  return {
    reply,
    intent: normalizedIntent,
    confidence,
    entities,
    escalated: false,
    clarificationRequired: false
  };
}

// Merge newly extracted entities into the existing conversation context.
function updateConversationContext(context, entities) {
  const safeContext =
    context &&
    typeof context === 'object' &&
    !Array.isArray(context)
      ? context
      : {};

  const safeEntities =
    entities &&
    typeof entities === 'object' &&
    !Array.isArray(entities)
      ? entities
      : {};

  return {
    ...safeContext,
    ...safeEntities
  };
}

module.exports = {
  getResponse,
  updateConversationContext
};