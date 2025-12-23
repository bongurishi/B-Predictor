import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from tensorflow.keras.callbacks import EarlyStopping
import os

def create_lstm(X_train, y_train, timesteps=10, features=5, epochs=20, batch_size=32):
    X_train_seq, y_train_seq = [], []
    for i in range(len(X_train) - timesteps):
        X_train_seq.append(X_train[i:i+timesteps])
        y_train_seq.append(y_train[i+timesteps])
    X_train_seq, y_train_seq = np.array(X_train_seq), np.array(y_train_seq)

    if X_train_seq.size == 0 or len(X_train_seq) == 0:
        raise ValueError(
            f"Not enough samples to create sequences: got {len(X_train)} samples with timesteps={timesteps}. "
            "Reduce `timesteps` or provide more data."
        )

    model = Sequential([
        Input(shape=(timesteps, features)),
        LSTM(64),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train_seq, y_train_seq, epochs=epochs, batch_size=batch_size,
              callbacks=[EarlyStopping(patience=3)])

    # Save model
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, "../models")
    os.makedirs(MODELS_DIR, exist_ok=True)
    model.save(os.path.join(MODELS_DIR, "lstm_model.h5"))

    return model
