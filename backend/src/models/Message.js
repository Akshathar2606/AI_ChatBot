const mongoose = require('mongoose');

const messageSchema = new mongoose.Schema({
  sessionId: {
    type: String,
    required: true,
    index: true
  },
  message: {
    type: String,
    required: true
  },
  intent: {
    type: String,
    default: null
  },
  confidence: {
    type: Number,
    default: null
  },
  reply: {
    type: String,
    default: null
  },
  escalated: {
    type: Boolean,
    default: false
  }
}, {
  timestamps: true
});

const Message = mongoose.model('Message', messageSchema);

module.exports = Message;
