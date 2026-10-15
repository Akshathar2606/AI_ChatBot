function extractEntities(message) {
  const entities = {};

  if (typeof message !== 'string') {
    return entities;
  }

  const normalizedMessage = message.trim();
  if (!normalizedMessage) {
    return entities;
  }

  const patterns = {
    order_id: /\bORD-?\d+\b/gi,
    transaction_id: /\bTXN-?\d+\b/gi,
    product_id: /\bPROD-?\d+\b/gi,
  };

  for (const [key, pattern] of Object.entries(patterns)) {
    const matches = normalizedMessage.match(pattern);
    if (matches && matches.length > 0) {
      entities[key] = matches[0];
    }
  }

  return entities;
}

module.exports = { extractEntities };
