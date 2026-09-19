# controllers/data_controller.py

from services.data_service import DataService


def fetch_ticker_data(ticker: str):
    """
    Fetch ticker data safely.
    Returns a DataFrame or None if fetch failed.
    """
    try:
        df = DataService.fetch_and_prepare(ticker)
        if df is None or df.empty:
            return None
        return df
    except Exception as e:
        print(f"Data fetch error for {ticker}: {e}")
        return None
