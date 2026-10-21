from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Project root: AI_ChatBot/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ML_MODEL_DIR = PROJECT_ROOT / "ml_model"

# Allow importing predict_intent from ml_model/predict.py
sys.path.insert(0, str(ML_MODEL_DIR))

from predict import predict_intent

app = FastAPI(
    title="AI Customer Service Chatbot",
    description="Intent classification service",
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    message: str = Field(..., min_length=1)


class PredictionResponse(BaseModel):
    intent: str
    confidence: float
    needs_clarification: bool


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        result = predict_intent(request.message)

        return PredictionResponse(
            intent=result["intent"],
            confidence=result["confidence"],
            needs_clarification=result["needs_clarification"],
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Intent prediction failed. Check the ML model setup.",
        ) from error