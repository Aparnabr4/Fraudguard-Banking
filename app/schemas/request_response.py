from pydantic import BaseModel

class TransactionInput(BaseModel):
    amount: float
    balance: float
    age: int
    merchant_rating: float
    transaction_type: str
    is_international: bool


class PredictionResponse(BaseModel):
    is_fraud: int
    fraud_probability: float
