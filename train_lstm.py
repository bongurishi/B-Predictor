from src.data_processing import load_and_process
from src.lstm_forecasting import create_lstm
import os
import pickle
import argparse


def main(timesteps, epochs, batch_size):
    print("Loading and processing data...")
    df, scaler = load_and_process()

    metric_cols = [c for c in df.columns if c not in ["timestamp", "incident"]]
    X = df[metric_cols].values
    y = df["incident"].astype(int).values

    print(f"Data shapes: X={X.shape}, y={y.shape}")

    # Ensure timesteps is appropriate for the dataset size
    n_samples = X.shape[0]
    if n_samples <= timesteps:
        effective_timesteps = max(1, n_samples - 1)
        print(f"Warning: requested timesteps={timesteps} but only {n_samples} samples available. Using timesteps={effective_timesteps}.")
    else:
        effective_timesteps = timesteps

    print("Training LSTM (this may take a while)...")
    model = create_lstm(X, y, timesteps=effective_timesteps, features=X.shape[1], epochs=epochs, batch_size=batch_size)

    # Save scaler for inference
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    os.makedirs(MODELS_DIR, exist_ok=True)
    scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)

    print(f"Saved scaler to {scaler_path}")
    print("Training complete. Model saved to models/lstm_model.h5")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train LSTM model and save to models/")
    parser.add_argument("--timesteps", type=int, default=10)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()

    # Note: the `create_lstm` function currently sets epochs/batch_size internally.
    # If you want to pass epochs/batch_size through, update `create_lstm` accordingly.
    main(args.timesteps, args.epochs, args.batch_size)
