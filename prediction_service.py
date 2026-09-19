import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta

class PredictionService:
    @staticmethod
    def predict(df, lstm, rf, scaler, meta, future_days: int = 7, threshold: float = 0.5):
        """
        Predict future prices using LSTM + RF residual (hybrid model).
        Signal is based on the last day of the forecast horizon.
        df: DataFrame with 'Close' column
        lstm: trained LSTM model
        rf: trained Random Forest model
        scaler: MinMaxScaler fitted on training data
        meta: dict containing 'seq_len'
        future_days: number of days to forecast
        threshold: percentage change threshold for BUY/SELL/HOLD
        """
        seq_len = int(meta.get('seq_len', 30))

        if len(df) < seq_len:
            raise ValueError(f"Not enough data rows ({len(df)}) for seq_len={seq_len}")

        # ---------------------------
        # Prepare scaled data
        # ---------------------------
        scaled = scaler.transform(df[['Close']])
        last_seq_future = scaled[-seq_len:].copy()  # shape: (seq_len, 1)

        # ---------------------------
        # Forecast multiple future days
        # ---------------------------
        future_prices = []

        for _ in range(future_days):
            lstm_in = last_seq_future.reshape(1, seq_len, 1)
            lstm_scaled = float(lstm.predict(lstm_in, verbose=0)[0][0])

            rf_in = last_seq_future.flatten()
            rf_scaled = float(rf.predict(rf_in.reshape(1, -1))[0])

            hybrid_scaled = lstm_scaled + rf_scaled
            next_price = scaler.inverse_transform([[hybrid_scaled]])[0][0]
            future_prices.append(next_price)

            # Update sequence for next prediction
            last_seq_future = np.vstack([last_seq_future[1:], [[hybrid_scaled]]])

        # ---------------------------
        # Use last forecast day for signal
        # ---------------------------
        predicted_close = future_prices[-1]  # last day
        last_close = df['Close'].iloc[-1]    # current price
        pct_change = (predicted_close - last_close) / last_close * 100

        if pct_change > threshold:
            signal = 'BUY'
        elif pct_change < -threshold:
            signal = 'SELL'
        else:
            signal = 'HOLD'

        # ---------------------------
        # Future dates
        # ---------------------------
        future_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), periods=future_days)

        # ---------------------------
        # Plotly figure
        # ---------------------------
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines+markers', name='Actual'))
        fig.add_trace(go.Scatter(x=future_dates, y=future_prices, mode='lines+markers', name='Forecast'))

        # ---------------------------
        # Return results (include current price)
        # ---------------------------
        return {
            'current_price': last_close,           # actual current price
            'predicted_close': predicted_close,    # forecast final day
            'signal': signal,
            'confidence': abs(pct_change) / 100,
            'future_prices': future_prices,
            'future_dates': future_dates,
            'figure': fig
        }
