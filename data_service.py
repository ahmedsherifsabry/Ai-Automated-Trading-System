# services/data_service.py

import yfinance as yf
import pandas as pd
import numpy as np

class DataService:
    @staticmethod
    def fetch_data(ticker: str, period: str = '5y', interval: str = '1d') -> pd.DataFrame:
        df = yf.download(ticker, period=period, interval=interval, auto_adjust=True, progress=False)

        # Ensure we always return a DataFrame
        if df is None or df.empty:
            print(f"Warning: No data fetched for {ticker}")
            return pd.DataFrame()  # empty DataFrame instead of None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]

        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
        df.index.name = 'Date'
        return df

    @staticmethod
    def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        df = df.copy()
        df = df.fillna(method='bfill').fillna(0)
        return df

    @staticmethod
    def fetch_and_prepare(ticker: str):
        df = DataService.fetch_data(ticker)
        # Flatten MultiIndex columns if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col) if isinstance(col, tuple) else col for col in df.columns]

        if df.empty:
            return None  # still return None for the page to handle
        df = DataService.add_technical_indicators(df)
        return df
