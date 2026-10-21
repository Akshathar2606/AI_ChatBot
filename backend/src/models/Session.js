const mongoose = require('mongoose');

const sessionSchema = new mongoose.Schema({
  sessionId: {
    type: String,
    required: true,
    unique: true,
    index: true
  }
}, {
  timestamps: true
});

const Session = mongoose.model('Session', sessionSchema);

module.exports = Session;
