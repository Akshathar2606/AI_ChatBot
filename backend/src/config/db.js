const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGODB_URI);
    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error(`MongoDB Connection Error: ${error.message}`);
    console.error('MongoDB is not running. The server will continue but database operations will fail.');
    console.error('Please start MongoDB to enable full functionality.');
    // Don't exit in development - allow testing of non-DB endpoints
  }
};

module.exports = connectDB;
