const Session = require('../models/Session');
const Message = require('../models/Message');
const aiService = require('../services/aiService');
const responseService = require('../services/responseService');

/**
 * Handle chat message
 * POST /api/chat
 * Request: { sessionId, message }
 * Response: { reply, intent, confidence, escalated }
 */
const handleChat = async (req, res, next) => {
  try {
    // Step 1: Validate input
    const { sessionId, message } = req.body;

    if (!sessionId || typeof sessionId !== 'string' || sessionId.trim() === '') {
      res.status(400);
      throw new Error('sessionId is required and must be a non-empty string');
    }

    if (!message || typeof message !== 'string' || message.trim() === '') {
      res.status(400);
      throw new Error('message is required and must be a non-empty string');
    }

    // Step 2: Get AI prediction from Python service
    let prediction;
    try {
      prediction = await aiService.getPrediction(message);
    } catch (aiError) {
      console.error('AI Service failed:', aiError.message);
      res.status(502);
      throw new Error('AI service is unavailable. Please try again later.');
    }

    // Step 3: Validate AI response
    if (!prediction || typeof prediction.intent !== 'string' || typeof prediction.confidence !== 'number') {
      console.error('Invalid AI response:', prediction);
      res.status(502);
      throw new Error('AI service returned invalid response');
    }

    const { intent, confidence } = prediction;

    // Step 4: Generate chatbot response
    // M4 owns detailed response logic - this uses the service interface
const responseData = responseService.generateResponse(
  intent,
  confidence,
  message.trim()
);    const { reply, escalated } = responseData;

    // Step 5: Create or find Session
    let session;
    try {
      session = await Session.findOne({ sessionId });
      if (!session) {
        session = await Session.create({ sessionId });
      }
    } catch (dbError) {
      console.error('Database error (Session):', dbError.message);
      res.status(503);
      throw new Error('Database service is unavailable');
    }

    // Step 6: Store message in database
    try {
      await Message.create({
        sessionId,
        message: message.trim(),
        intent,
        confidence,
        reply,
        escalated
      });
    } catch (dbError) {
      console.error('Database error (Message):', dbError.message);
      res.status(503);
      throw new Error('Failed to save message to database');
    }

    // Step 7: Return response with exact contract fields
    res.status(200).json({
      reply,
      intent,
      confidence,
      escalated
    });

  } catch (error) {
    next(error);
  }
};

module.exports = {
  handleChat
};
