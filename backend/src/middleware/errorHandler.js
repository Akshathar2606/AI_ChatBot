/**
 * Centralized error handling middleware
 */
const errorHandler = (err, req, res, next) => {
  console.error('Error:', err.message);
  
  // Don't log full stack in production to avoid exposing secrets
  if (process.env.NODE_ENV !== 'production') {
    console.error('Stack:', err.stack);
  }

  const statusCode = res.statusCode === 200 ? 500 : res.statusCode;
  
  res.status(statusCode).json({
    error: err.message || 'Internal Server Error',
    // Never expose stack traces in production
    ...(process.env.NODE_ENV !== 'production' && { stack: err.stack })
  });
};

module.exports = errorHandler;
