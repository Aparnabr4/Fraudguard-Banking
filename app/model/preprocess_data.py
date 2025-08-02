# app/model/preprocess_data.py
import os
import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(__file__), "../../data")

def preprocess_data():
    print("📂 Loading raw datasets...")

    # Load CSVs
    transaction_records = pd.read_csv(os.path.join(BASE_DIR, "transaction_data", "transaction_records.csv"))
    transaction_metadata = pd.read_csv(os.path.join(BASE_DIR, "transaction_data", "transaction_metadata.csv"))
    amount_data = pd.read_csv(os.path.join(BASE_DIR, "transaction_amounts", "amount_data.csv"))
    anomaly_scores = pd.read_csv(os.path.join(BASE_DIR, "transaction_amounts", "anomaly_scores.csv"))
    customer_data = pd.read_csv(os.path.join(BASE_DIR, "customer_profiles", "customer_data.csv"))
    account_activity = pd.read_csv(os.path.join(BASE_DIR, "customer_profiles", "account_activity.csv"))
    merchant_data = pd.read_csv(os.path.join(BASE_DIR, "merchant_info", "merchant_data.csv"))
    category_labels = pd.read_csv(os.path.join(BASE_DIR, "merchant_info", "transaction_category_labels.csv"))
    fraud_indicators = pd.read_csv(os.path.join(BASE_DIR, "fraud_patterns", "fraud_indicators.csv"))
    suspicious_activity = pd.read_csv(os.path.join(BASE_DIR, "fraud_patterns", "suspicious_activity.csv"))

    print("✅ Raw data loaded.")

    print("🧽 Normalizing column names...")
    def normalize_columns(df):
        df.columns = [col.strip().lower() for col in df.columns]
        return df

    # Normalize all
    transaction_records = normalize_columns(transaction_records)
    transaction_metadata = normalize_columns(transaction_metadata)
    amount_data = normalize_columns(amount_data)
    anomaly_scores = normalize_columns(anomaly_scores)
    customer_data = normalize_columns(customer_data)
    account_activity = normalize_columns(account_activity)
    merchant_data = normalize_columns(merchant_data)
    category_labels = normalize_columns(category_labels)
    fraud_indicators = normalize_columns(fraud_indicators)
    suspicious_activity = normalize_columns(suspicious_activity)

    # ✅ Rename fraud column AFTER normalization
    if "fraudindicator" in fraud_indicators.columns:
        fraud_indicators = fraud_indicators.rename(columns={"fraudindicator": "isfraud"})

    print("🔗 Merging datasets...")

    # Merge transaction-related data
    merged_df = transaction_records.merge(transaction_metadata, on="transactionid", how="left")
    merged_df = merged_df.merge(amount_data, on="transactionid", how="left")
    merged_df = merged_df.merge(anomaly_scores, on="transactionid", how="left")

    # Merge customer-related data
    merged_df = merged_df.merge(customer_data, on="customerid", how="left")
    merged_df = merged_df.merge(account_activity, on="customerid", how="left")
    merged_df = merged_df.merge(suspicious_activity, on="customerid", how="left")

    # Merge merchant-related data
    merged_df = merged_df.merge(merchant_data, on="merchantid", how="left")

    # Merge category labels
    merged_df = merged_df.merge(category_labels, on="transactionid", how="left")

    # Merge fraud indicators
    merged_df = merged_df.merge(fraud_indicators, on="transactionid", how="left")

    print("💾 Saving preprocessed dataset...")
    output_path = os.path.join(BASE_DIR, "preprocessed_dataset.csv")
    merged_df.to_csv(output_path, index=False)

    print(f"✅ Preprocessed data saved to: {output_path}")
