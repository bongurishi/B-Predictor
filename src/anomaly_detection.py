from sklearn.ensemble import IsolationForest
import pickle
import os

def train_anomaly(df):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, "../models")
    os.makedirs(MODELS_DIR, exist_ok=True)
    model_path = os.path.join(MODELS_DIR, "anomaly_model.pkl")

    metric_cols = [col for col in df.columns if col not in ["timestamp", "incident"]]
    X = df[metric_cols]

    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(X)
    pickle.dump(model, open(model_path, "wb"))
    return model

def predict_anomaly(model, X):
    return model.predict(X)  # -1 = anomaly, 1 = normal
