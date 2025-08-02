# app/services/predict.py
import pandas as pd
import joblib
from app.core.config import MODEL_PATH, ENCODER_PATH, FEATURES_PATH

model = joblib.load(MODEL_PATH)
category_encoder = joblib.load(ENCODER_PATH)
selected_features = joblib.load(FEATURES_PATH)

def safe_label_encode(series, encoder):
    known_classes = set(encoder.classes_)
    return series.apply(lambda val: encoder.transform([val])[0] if val in known_classes else -1)

def predict_fraud(input_data: dict, threshold=0.3) -> dict:
    df = pd.DataFrame([input_data])
    if "category" in df.columns:
        df["category"] = safe_label_encode(df["category"], category_encoder)
    df = df.reindex(columns=selected_features, fill_value=0)

    probability = model.predict_proba(df)[0][1]
    print(f"Raw probability for is_fraud=1: {probability}")
    prediction = 1 if probability >= threshold else 0

    return {
        "is_fraud": int(prediction),
        "fraud_probability": round(probability, 4)
    }

# if __name__ == "__main__":
#     sample_input = {
#         "amount": 999999.99,
#         "category": "transfer",
#         "hour": 13,
#         "dayofweek": 5,
#         "is_weekend": 1,
#         "days_since_login": 0
#     }
#     result = predict_fraud(sample_input)
#     print(result)