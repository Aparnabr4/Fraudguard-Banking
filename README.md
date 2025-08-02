💳 Fraud Detection System
A machine learning-based system that detects fraudulent financial transactions in real time using an XGBoost model and a FastAPI backend.

🚀 **Overview**

- Predicts whether a transaction is fraudulent or legitimate.
- Uses features like amount, category, time, and user behavior.
- Deployed using FastAPI to enable real-time fraud checks.
- Built with XGBoost, and handles class imbalance with SMOTE.

  
✅ **Features**

- 📊 Trains an XGBoost model for high accuracy.
- ⚖️ Handles class imbalance using SMOTE (Synthetic Minority Oversampling Technique).
- 🧠 Performs hyperparameter tuning via GridSearchCV.
- 🌐 Provides a REST API for real-time fraud prediction.
- 📝 Accepts custom transaction input with automatic categorical encoding.


📦 **Prerequisites**

- 🐍 Python 3.13  
- ✅ Use of a virtual environment is recommended  
- 📚 Required Python libraries:
  - `pandas`
  - `xgboost`
  - `scikit-learn`
  - `imblearn`
  - `fastapi`
  - `uvicorn`
  - `joblib`



✅ FraudGuard - Block Diagram

```text
+-----------------------+
|    User/API Client    |
+----------+------------+
           |
           v
+--------------------------+
| FastAPI Application      |
|  (main.py, endpoints.py) |
+----------+---------------+
           |
           v
+---------------------------+
| Input Validation          |
| (TransactionInput model)  |
+---------------------------+
           |
           v
+---------------------------+
| Load Trained ML Model     |
| - model.pkl               |
| - encoder.pkl             |
| - features.pkl            |
| (.env used for paths)     |
+---------------------------+
           |
           v
+---------------------------+
| Preprocess Input Data     |
| - Encode categorical      |
| - Select saved features   |
+---------------------------+
           |
           v
+---------------------------+
| Predict Fraud             |
| (predict_fraud function)  |
| → is_fraud (0/1)          |
| → fraud_probability       |
+---------------------------+
           |
           v
+---------------------------+
| Return JSON Response      |
| (PredictionResponse model)|
+---------------------------+
'''


🔁 Model Training Flow

```text
+----------------------------+
| Run: /train API            |
+------------+---------------+
             |
             v
+--------------------------------------+
| Load Raw Data (CSV)                  |
| e.g., data/preprocessed_dataset.csv  |
+------------+-------------------------+
             |
             v
+----------------------------+
| Preprocess + Feature Engg. |
| - Label encode             |
| - Feature selection        |
+------------+---------------+
             |
             v
+----------------------------+
| Train Model (LightGBM)     |
+------------+---------------+
             |
             v
+---------------------------+
| Save:                     |
| - model.pkl               |
| - encoder.pkl             |
| - features.pkl            |
+---------------------------+

+-----------------------+
|    User/API Client    |
+----------+------------+
           |
           v
+--------------------------+
|   FastAPI Application    |
| (main.py, endpoints.py)  |
+----------+---------------+
           |
           v
+---------------------------+
|     Input Validation      |
| (TransactionInput model)  |
+---------------------------+
           |
           v
+---------------------------+
| Load Trained ML Model     |
| - model.pkl               |
| - encoder.pkl             |
| - features.pkl            |
| (.env used for paths)     |
+---------------------------+
           |
           v
+---------------------------+
|   Preprocess Input Data   |
| - Encode categorical      |
| - Select saved features   |
+---------------------------+
           |
           v
+---------------------------+
|      Predict Fraud        |
| (predict_fraud function)  |
| → is_fraud (0/1)          |
| → fraud_probability       |
+---------------------------+
           |
           v
+---------------------------+
|    Return JSON Response   |
| (PredictionResponse model)|
+---------------------------+

<<<<<<< HEAD
🔁 Model Training Flow
+----------------------------+
|      Run: /train API       |
+------------+---------------+
             |
             v
+--------------------------------------+
|     Load Raw Data (CSV)            |
| e.g., data/preprocessed_dataset.csv |
+------------+-------------------------+
             |
             v
+----------------------------+
| Preprocess + Feature Engg. |
| - Label encode             |
| - Feature selection        |
+------------+---------------+
             |
             v
+----------------------------+
|  Train Model (LightGBM)    |
+------------+---------------+
             |
             v
+---------------------------+
|         Save:             |
| - model.pkl               |
| - encoder.pkl             |
| - features.pkl            |
+---------------------------+
=======
---



>>>>>>> 1a271cca2cbc9fda6db3c1d894508ac25efbe0de

🧪 Case Study: Sample Predictions
✅ Non-Fraudulent Transactions
Case 1:
{
  "amount": 250.50,
  "balance": 3500.75,
  "age": 34,
  "merchant_rating": 4.0,
  "transaction_type": "purchase",
  "is_international": true
}

Case 2:
{
  "amount": 1200.00,
  "balance": 5200.00,
  "age": 38,
  "merchant_rating": 4.2,
  "transaction_type": "transfer",
  "is_international": false
}

Case 3:
{
  "amount": 600.25,
  "balance": 1500.80,
  "age": 30,
  "merchant_rating": 5.0,
  "transaction_type": "payment",
  "is_international": false
}

🚨 Fraudulent Transactions
Case 1:
{
  "amount": 97500.00,
  "balance": 10.00,
  "age": 19,
  "merchant_rating": 1.3,
  "transaction_type": "withdrawal",
  "is_international": true
}

Case 2:
{
  "amount": 88000.00,
  "balance": 5.00,
  "age": 21,
  "merchant_rating": 2.0,
  "transaction_type": "purchase",
  "is_international": true
}

Case 3:
{
  "amount": 99999.99,
  "balance": 0.00,
  "age": 18,
  "merchant_rating": 1.0,
  "transaction_type": "transfer",
  "is_international": true
}
