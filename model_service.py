# services/model_service.py

import os
import joblib
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_BASE_DIR = os.path.join(BASE_DIR, 'Models')


class ModelService:
    @staticmethod
    def load(ticker: str):
        ticker = ticker.upper()
        model_dir = os.path.join(MODEL_BASE_DIR, ticker)

        if not os.path.isdir(model_dir):
            raise FileNotFoundError(f"Model directory not found: {model_dir}")

        lstm_path = os.path.join(model_dir, 'lstm_model.keras')
        rf_path = os.path.join(model_dir, 'rf_model.joblib')
        scaler_path = os.path.join(model_dir, 'feature_scaler.joblib')
        meta_path = os.path.join(model_dir, 'meta.joblib')

        for p in [lstm_path, rf_path, scaler_path, meta_path]:
            if not os.path.exists(p):
                raise FileNotFoundError(f"Missing model asset: {p}")

        lstm = load_model(lstm_path)
        rf = joblib.load(rf_path)
        scaler = joblib.load(scaler_path)
        meta = joblib.load(meta_path)

        return lstm, rf, scaler, meta
