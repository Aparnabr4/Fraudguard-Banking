import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))

def check_columns(folder, filename):
    path = os.path.join(BASE_DIR, folder, filename)
    try:
        df = pd.read_csv(path, nrows=2)
        print(f"✅ {folder}/{filename} ➜ Columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"❌ {folder}/{filename} ➜ Failed: {e}")

files = {
    "Transaction Data": ["transaction_records.csv", "transaction_metadata.csv"],
    "Customer Profiles": ["customer_data.csv", "account_activity.csv"],
    "Fraudulent Patterns": ["fraud_indicators.csv", "suspicious_activity.csv"],
    "Transaction Amounts": ["amount_data.csv", "anomaly_scores.csv"],
    "Merchant Information": ["merchant_data.csv", "transaction_category_labels.csv"]
}

for folder, filenames in files.items():
    for filename in filenames:
        check_columns(folder, filename)
