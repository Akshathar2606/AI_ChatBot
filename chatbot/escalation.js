const ESCALATION_THRESHOLD = 0.10;
const CLARIFICATION_THRESHOLD = 0.20;

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
    'speak to a human',
    'speak to an agent',
    'connect me to support',
    'connect me to an agent'
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
  ];


  return patterns.some((pattern) => message.includes(pattern));
}

function shouldEscalate(
  intent,
  confidence,
  message,
  clarificationAttempts = 0
) {
  if (
    typeof intent === 'string' &&
    intent.toLowerCase() === 'human_agent'
  ) {
    return true;
  }

  const normalizedMessage = normalizeMessage(message);

  if (containsHumanRequest(normalizedMessage)) {
    return true;
  }

  if (containsSecurityIssue(normalizedMessage)) {
    return true;
  }

  if (
    Number.isFinite(clarificationAttempts) &&
    clarificationAttempts >= 2
  ) {
    return true;
  }

  const numericConfidence = Number(confidence);

  if (!Number.isFinite(numericConfidence)) {
    return false;
  }

  return numericConfidence < ESCALATION_THRESHOLD;
}

function needsClarification(confidence) {
  const numericConfidence = Number(confidence);

  if (!Number.isFinite(numericConfidence)) {
    return true;
  }

  return (
    numericConfidence >= ESCALATION_THRESHOLD &&
    numericConfidence < CLARIFICATION_THRESHOLD
  );
}

module.exports = {
  shouldEscalate,
  needsClarification,
  ESCALATION_THRESHOLD,
  CLARIFICATION_THRESHOLD
};