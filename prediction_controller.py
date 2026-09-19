# controllers/prediction_controller.py


from services.data_service import DataService
from services.model_service import ModelService
from services.prediction_service import PredictionService
from services.signal_service import SignalService
import streamlit as st


def run_prediction(ticker: str, future_days: int, threshold: float):
    df = DataService.fetch_and_prepare(ticker)
    if df is None or df.empty:
        st.error("Prediction aborted: No valid data")
        return None

    try:
        lstm, rf, scaler, meta = ModelService.load(ticker)
    except Exception as e:
        st.error(f"Error loading models for {ticker}: {e}")
        return None

    try:
        out = PredictionService.predict(df, lstm, rf, scaler, meta, future_days, threshold)
        SignalService.log_signal(ticker, out['signal'], out['confidence'])
        return out
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        return None
