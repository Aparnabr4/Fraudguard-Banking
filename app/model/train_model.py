# app/model/train_model.py
import os
import joblib
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, f1_score
from imblearn.over_sampling import SMOTE

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data"))

DATA_PATH = os.path.join(DATA_DIR, "preprocessed_dataset.csv")
MODEL_PATH = os.path.join(DATA_DIR, "model.pkl")
FEATURES_PATH = os.path.join(DATA_DIR, "features.pkl")
ENCODER_PATH = os.path.join(DATA_DIR, "category_encoder.pkl")

def train_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Training data not found at: {DATA_PATH}")

    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Drop ID-like or non-informative fields
    drop_cols = [
        "transactionid", "customerid", "merchantid",
        "name", "address", "merchantname", "location"
    ]
    df.drop(columns=drop_cols, inplace=True, errors="ignore")

    # Handle timestamp features (using current date as reference)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['dayofweek'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    df.drop(columns=['timestamp'], inplace=True)

    # Handle last login as "days since last login"
    df['lastlogin'] = pd.to_datetime(df['lastlogin'])
    current_date = pd.Timestamp.now()  # 01:57 PM IST, August 02, 2025
    df['days_since_login'] = (current_date - df['lastlogin']).dt.days
    df.drop(columns=['lastlogin'], inplace=True)

    # Encode 'category' using LabelEncoder
    if 'category' not in df.columns:
        raise ValueError("Missing 'category' column for encoding")

    category_encoder = LabelEncoder()
    df['category'] = category_encoder.fit_transform(df['category'].astype(str))

    # Separate features and label
    if 'isfraud' not in df.columns:
        raise ValueError("Dataset must contain 'isfraud' column as label.")

    X = df.drop(columns=['isfraud'])
    y = df['isfraud']

    # Debug: Check class distribution
    print("Original class distribution:\n", y.value_counts())

    # Handle class imbalance with SMOTE
    if (y == 1).sum() / len(y) < 0.1:
        smote = SMOTE(random_state=42)
        X, y = smote.fit_resample(X, y)
        print("After SMOTE class distribution:\n", pd.Series(y).value_counts())

    # Save feature names and encoder
    joblib.dump(list(X.columns), FEATURES_PATH)
    joblib.dump(category_encoder, ENCODER_PATH)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Calculate scale_pos_weight
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    print(f"Scale pos weight: {scale_pos_weight}")

    # Hyperparameter tuning with GridSearchCV
    param_grid = {
        'n_estimators': [200, 300],
        'max_depth': [5, 6],
        'learning_rate': [0.1, 0.05]
    }
    model = GridSearchCV(
        XGBClassifier(
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss',
            scale_pos_weight=scale_pos_weight
        ),
        param_grid,
        cv=5,
        scoring='f1'
    )
    model.fit(X_train, y_train)

    # Save best model
    joblib.dump(model.best_estimator_, MODEL_PATH)
    print(f"Best parameters: {model.best_params_}")

    # Evaluate
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("✅ Model trained and saved.")
    print("📊 Evaluation:\n", report)

    return {
        "model_path": MODEL_PATH,
        "accuracy": round(acc, 4),
        "f1_score": round(f1, 4)
    }

# if __name__ == "__main__":
#     train_model()