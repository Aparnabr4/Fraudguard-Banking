import os
from dotenv import load_dotenv

load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH", "data/model.pkl")
ENCODER_PATH = os.getenv("ENCODER_PATH", "data/category_encoder.pkl")
FEATURES_PATH = os.getenv("FEATURES_PATH", "data/features.pkl")

print("MODEL_PATH:", MODEL_PATH)
print("ENCODER_PATH:", ENCODER_PATH)
print("FEATURES_PATH:", FEATURES_PATH)