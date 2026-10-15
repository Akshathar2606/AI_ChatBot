# AI-Powered Customer Service Chatbot

## 1. Module Overview

The `chatbot` module provides the response-handling portion of an AI-powered customer service chatbot. It accepts an intent, a confidence score, and a customer message, then selects a predefined response, extracts supported identifiers, requests missing required information, asks for clarification, or escalates the conversation.

Intent classification is not performed by `getResponse()`; it receives the intent and confidence as inputs. The current implementation does not connect to a live order, payment, or product service.

## 2. Features

- Handles supported customer-service intents using predefined response messages.
- Extracts order, transaction, and product IDs from customer messages.
- Checks for required identifiers and asks for missing information where applicable.
- Applies confidence-based clarification and escalation rules.
- Escalates explicit human-agent requests and recognized fraud or security concerns.
- Provides a helper to merge extracted entities into a conversation context object.

## 3. Project Files

| File                           | Purpose                                                                                                                                                                          |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `intents.json`                 | Lists the supported intent names and describes what each intent represents.                                                                                                      |
| `responses.json`               | Maps intents to predefined response messages, required entities, and escalation settings.                                                                                        |
| `entityExtractor.js`           | Extracts the first matching order ID (`ORD`), transaction ID (`TXN`), and product ID (`PROD`) from a message. IDs may include an optional hyphen before the digits.              |
| `escalation.js`                | Defines the confidence thresholds and checks for explicit human-agent requests, recognized security-related terms, low confidence, and repeated clarification attempts.          |
| `conversation.js`              | Implements `getResponse()`, including escalation checks, clarification, required-entity validation, predefined response selection, and the `updateConversationContext()` helper. |
| `testChatbot.js`               | Runs 17 chatbot test scenarios and prints the request, response, extracted entities, escalation status, and clarification status.                                                |
| `../evaluation/test_cases.csv` | Contains 32 customer-service test cases with expected intents and escalation labels for evaluation.                                                                              |

## 4. Supported Intents

The chatbot module recognizes these intent names:

- `greeting`
- `order_tracking`
- `order_status`
- `order_cancellation`
- `delivery_delay`
- `return_request`
- `refund_status`
- `payment_failed`
- `payment_issue`
- `product_information`
- `account_login`
- `password_reset`
- `damaged_product`
- `complaint`
- `human_agent`
- `goodbye`
- `unknown`

The intent definitions are maintained in `intents.json`. The caller supplies the intent and confidence score; the current `conversation.js` module does not classify customer messages into intents.

## 5. Entity Extraction

`entityExtractor.js` searches the customer message for identifiers matching these patterns:

- Order ID: `ORD` followed by digits, optionally separated by a hyphen (for example, `ORD12345` or `ORD-12345`).
- Transaction ID: `TXN` followed by digits, optionally separated by a hyphen.
- Product ID: `PROD` followed by digits, optionally separated by a hyphen.

The extractor returns the first match for each identifier type it finds. It does not look up or verify an identifier against an external system.

## 6. Confidence-Based Escalation

`escalation.js` uses the following confidence thresholds:

- **Below 0.40:** Escalate.
- **From 0.40 to below 0.70:** Request clarification.
- **0.70 or above:** Continue normal intent handling, unless another escalation rule applies.

Confidence escalation is not the only escalation rule. A `human_agent` intent, recognized explicit requests for a human, and messages containing recognized security terms such as “fraud,” “scam,” or “stolen” trigger escalation regardless of confidence. Two or more clarification attempts also trigger escalation.

## 7. Conversation Handling

`getResponse(intent, confidence, message, clarificationAttempts)` first extracts identifiers and applies escalation rules. If no escalation applies, it requests clarification when confidence is between 0.40 and below 0.70, or when the intent is `unknown` or unsupported. For supported intents, it checks required entities and asks for missing information before selecting one of the intent’s predefined responses.

`updateConversationContext(context, entities)` returns a new object combining the supplied context and entities; entity values overwrite context values with the same keys. This helper does not provide persistent storage or maintain conversation state by itself.

## 8. Running the Tests

From the project root, run:

```sh
node .\chatbot\testChatbot.js
```

The script prints a results header followed by each of the 17 scenarios and the chatbot response details. It uses Node.js CommonJS modules and requires no additional package installation.

## 9. Test Coverage

`testChatbot.js` contains 17 predefined scenarios covering greetings, order requests, delivery delays, returns, refunds, payments, product information, account access, damaged products, complaints, human-agent requests, fraud, unknown questions, confidence-based handling, and goodbyes.

The separate `evaluation/test_cases.csv` dataset contains 32 cases, including order requests with and without identifiers, payment and refund identifiers, security concerns, unsupported questions, and ambiguous messages. These are evaluation data rows; the CSV is not automatically executed by `testChatbot.js`.

## 10. Limitations and Future Improvements

- Responses are predefined and selected from the messages in `responses.json`; they are not generated dynamically.
- The module handles supplied intents and confidence scores but does not implement an intent classifier.
- Entity extraction recognizes only the stated identifier formats and does not validate identifiers.
- Real order tracking, cancellations, refunds, and payment lookups require backend or database integration. The current implementation does not retrieve or change live order or payment information.
- Conversation context is only merged by a helper function; it is not persisted between messages.
- Future work could integrate an intent-classification component, secure backend services for order and payment operations, persistent conversation state, and automated execution of the evaluation dataset.
