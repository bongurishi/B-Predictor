# src/root_cause.py
import shap
import numpy as np
from tensorflow.keras.models import load_model

def get_shap_values(X_background, X_sample):
    """
    Returns SHAP values for LSTM time-series model
    Shape: (samples, timesteps, features)
    """
    model = load_model("models/lstm_model.h5")

    # Use GradientExplainer (correct for LSTM)
    explainer = shap.GradientExplainer(
        model,
        X_background[:50]
    )

    shap_values = explainer.shap_values(X_sample)
    return shap_values
