import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_and_process():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    metrics_path = os.path.join(BASE_DIR, "../data/metrics.csv")
    incidents_path = os.path.join(BASE_DIR, "../data/incidents.csv")

    metrics = pd.read_csv(metrics_path, parse_dates=["timestamp"])

    # Read incidents; handle empty or missing file gracefully by creating
    # a zero-filled incidents series matching the metrics timestamps.
    try:
        incidents = pd.read_csv(incidents_path, parse_dates=["timestamp"])
        if incidents.empty:
            incidents = pd.DataFrame({"timestamp": metrics["timestamp"], "incident": 0})
    except (pd.errors.EmptyDataError, FileNotFoundError):
        incidents = pd.DataFrame({"timestamp": metrics["timestamp"], "incident": 0})

    # Merge and sort
    df = metrics.merge(incidents, on="timestamp", how="left").fillna(0)

    # Scale metrics
    metric_cols = [col for col in df.columns if col not in ["timestamp", "incident"]]
    scaler = MinMaxScaler()
    df[metric_cols] = scaler.fit_transform(df[metric_cols])

    return df, scaler
