import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))

def load_csv(folder, filename):
    path = os.path.join(BASE_DIR, folder, filename)
    return pd.read_csv(path)

def merge_data():
    print("🔁 Loading CSV files...")

    # Load core datasets
    transactions = load_csv('Transaction Data', 'transaction_records.csv')
    metadata = load_csv('Transaction Data', 'transaction_metadata.csv')
    customer_data = load_csv('Customer Profiles', 'customer_data.csv')
    account_activity = load_csv('Customer Profiles', 'account_activity.csv')
    fraud_indicators = load_csv('Fraudulent Patterns', 'fraud_indicators.csv')
    suspicious_activity = load_csv('Fraudulent Patterns', 'suspicious_activity.csv')
    amount_data = load_csv('Transaction Amounts', 'amount_data.csv')
    anomaly_scores = load_csv('Transaction Amounts', 'anomaly_scores.csv')
    merchant_data = load_csv('Merchant Information', 'merchant_data.csv')
    category_labels = load_csv('Merchant Information', 'transaction_category_labels.csv')

    print("🧩 Merging datasets...")

    # Merge all dataframes step-by-step
    df = transactions.merge(metadata, on='TransactionID', how='left')
    df = df.merge(fraud_indicators, on='TransactionID', how='left')
    df = df.merge(amount_data, on='TransactionID', how='left')
    df = df.merge(anomaly_scores, on='TransactionID', how='left')
    df = df.merge(category_labels, on='TransactionID', how='left')
    df = df.merge(customer_data, on='CustomerID', how='left')
    df = df.merge(account_activity, on='CustomerID', how='left')
    df = df.merge(suspicious_activity, on='CustomerID', how='left')
    df = df.merge(merchant_data, on='MerchantID', how='left')

    print("✅ Final dataset shape:", df.shape)

    output_path = os.path.join(os.path.dirname(__file__), 'merged_dataset.csv')
    df.to_csv(output_path, index=False)
    print(f"📁 Saved merged dataset to {output_path}")

