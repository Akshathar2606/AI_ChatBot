const ESCALATION_THRESHOLD = 0.40;
const CLARIFICATION_THRESHOLD = 0.70;

function normalizeMessage(message) {
  if (typeof message !== 'string') {
    return '';
  }

  return message.toLowerCase();
}

function containsHumanRequest(message) {
  if (!message) {
    return false;
  }

  const patterns = [
    'talk to a human',
    'talk to an agent',
    'human agent',
    'customer support agent',
    'real person',
    'speak to someone',
    'connect me to support'
  ];

  return patterns.some((pattern) => message.includes(pattern));
}

function containsSecurityIssue(message) {
  if (!message) {
    return false;
  }

  const patterns = [
    'fraud',
    'fraudulent',
    'unauthorized transaction',
    'scam',
    'stolen'
  ];

  return patterns.some((pattern) => message.includes(pattern));
}

function shouldEscalate(intent, confidence, message, clarificationAttempts = 0) {
  if (typeof intent === 'string' && intent.toLowerCase() === 'human_agent') {
    return true;
  }

  const normalizedMessage = normalizeMessage(message);

  if (containsHumanRequest(normalizedMessage)) {
    return true;
  }

  if (containsSecurityIssue(normalizedMessage)) {
    return true;
  }

  const numericConfidence = Number(confidence);
  if (!Number.isFinite(numericConfidence)) {
    return false;
  }

  if (numericConfidence < ESCALATION_THRESHOLD) {
    return true;
  }

  if (Number.isFinite(clarificationAttempts) && clarificationAttempts >= 2) {
    return true;
  }

  return false;
}

function needsClarification(confidence) {
  const numericConfidence = Number(confidence);

  if (!Number.isFinite(numericConfidence)) {
    return false;
  }

  return numericConfidence >= ESCALATION_THRESHOLD && numericConfidence < CLARIFICATION_THRESHOLD;
}

module.exports = {
  shouldEscalate,
  needsClarification,
  ESCALATION_THRESHOLD,
  CLARIFICATION_THRESHOLD
};
