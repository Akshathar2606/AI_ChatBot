# AI Customer Service Chatbot - Backend

## Overview
Node.js + Express backend API for the AI-Powered Customer Service Chatbot project.

## Technology Stack
- **Runtime**: Node.js
- **Framework**: Express.js
- **Database**: MongoDB + Mongoose
- **HTTP Client**: Axios
- **Environment**: dotenv
- **CORS**: cors
- **Dev Tool**: nodemon

## Project Structure
```
backend/
├── src/
│   ├── config/
│   │   └── db.js                 # MongoDB connection
│   ├── controllers/
│   │   └── chatController.js     # Chat endpoint handlers
│   ├── models/
│   │   ├── Session.js            # Session schema
│   │   └── Message.js            # Message schema
│   ├── routes/
│   │   └── chatRoutes.js         # API routes
│   ├── services/
│   │   ├── aiService.js          # Python AI service integration
│   │   └── responseService.js    # Response generation logic
│   ├── middleware/
│   │   └── errorHandler.js       # Centralized error handling
│   ├── app.js                    # Express app configuration
│   └── server.js                 # Server entry point
├── .env                          # Environment variables (not committed)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
└── package.json                  # Dependencies and scripts
```

## Installation

### Prerequisites
- Node.js (v14 or higher)
- MongoDB (running locally or remote)
- Python AI/ML service (running on port 8000)

### Steps
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Configure environment variables in `.env`:
   ```
   PORT=5000
   MONGODB_URI=mongodb://localhost:27017/ai_customer_service
   AI_SERVICE_URL=http://localhost:8000
   ```

## Running the Application

### Development Mode (with auto-reload)
```bash
npm run dev
```

### Production Mode
```bash
npm start
```

## API Endpoints

### Health Check
```
GET /api/health
```
**Response:**
```json
{
  "status": "ok"
}
```

### Chat Endpoint (Phase 2)
```
POST /api/chat
```
**Request:**
```json
{
  "sessionId": "abc123",
  "message": "I want to return my shoes"
}
```

**Response:**
```json
{
  "reply": "Sure! Please provide your order ID.",
  "intent": "return_request",
  "confidence": 0.94,
  "escalated": false
}
```

## API Contract

### React → Node
- **Endpoint**: `POST /api/chat`
- **Request**: `{ sessionId, message }`
- **Response**: `{ reply, intent, confidence, escalated }`

### Node → Python
- **Endpoint**: `POST {AI_SERVICE_URL}/predict`
- **Request**: `{ message }`
- **Response**: `{ intent, confidence }`

## Database Schema

### Session
- `sessionId`: String (unique, indexed)
- `createdAt`: Date (auto)
- `updatedAt`: Date (auto)

### Message
- `sessionId`: String (indexed)
- `message`: String
- `intent`: String
- `confidence`: Number
- `reply`: String
- `escalated`: Boolean
- `createdAt`: Date (auto)

## Development Notes

### Phase 1 (Current)
✅ Backend foundation setup
✅ Express server configuration
✅ MongoDB connection
✅ Database models
✅ Health check endpoint
✅ Service layer structure
✅ Error handling middleware

### Phase 2 (Planned)
- Implement POST /api/chat endpoint
- Integrate Python AI service
- Implement response generation logic
- Add conversation storage
- Add escalation handling

## Testing

### Test Health Endpoint
```bash
curl http://localhost:5000/api/health
```

### Expected Output
```json
{"status":"ok"}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 5000 |
| `MONGODB_URI` | MongoDB connection string | mongodb://localhost:27017/ai_customer_service |
| `AI_SERVICE_URL` | Python AI service URL | http://localhost:8000 |

## Git Branch
This backend is developed on the `feature/backend` branch.

## Team Integration
- **Frontend**: React app on `feature/frontend` branch
- **AI/ML**: Python service on `feature/ai-ml` branch
- **Chatbot**: Response logic on `feature/chatbot` branch

## Troubleshooting

### MongoDB Connection Error
If you see `ECONNREFUSED 127.0.0.1:27017`:
- Ensure MongoDB is installed and running
- Start MongoDB: `mongod`
- Verify connection string in `.env`

### Port Already in Use
If port 5000 is busy:
- Change `PORT` in `.env` to another port (e.g., 5001)
- Restart the server

### Python Service Unavailable
Phase 2 will require the Python AI service running on port 8000.
Coordinate with the AI/ML team member.

## Notes
- Do NOT commit `.env` file (contains secrets)
- Do NOT commit `node_modules/` directory
- Keep API contract consistent with team agreement
- Coordinate with other team members before changing endpoints

## Author
M2 - Backend Developer
