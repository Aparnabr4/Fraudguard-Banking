# app/api/endpoint

from fastapi import APIRouter
from app.schemas.request_response import TransactionInput, PredictionResponse
from app.services.predict import predict_fraud
from app.model.train_model import train_model

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(data: TransactionInput):
    result = predict_fraud(data.dict())
    return result

@router.post("/train")
def trigger_training():
    model_path = train_model()
    return {"message": f"✅ Model trained and saved at: {model_path}"}

