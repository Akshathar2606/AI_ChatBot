const express = require('express');
const cors = require('cors');
const errorHandler = require('./middleware/errorHandler');
const chatRoutes = require('./routes/chatRoutes');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({
    status: 'ok'
  });
});

// API Routes
app.use('/api', chatRoutes);

// Error handling middleware (must be last)
app.use(errorHandler);

module.exports = app;
