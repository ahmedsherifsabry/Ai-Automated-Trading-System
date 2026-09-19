# services/signal_service.py

from database.db import get_conn
from datetime import datetime


class SignalService:
    @staticmethod
    def log_signal(ticker: str, signal_type: str, confidence: float, status: str = 'PENDING'):
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO signals (ticker, signal_type, confidence, status, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (ticker, signal_type, confidence, status, datetime.now().isoformat())
        )

        conn.commit()

    @staticmethod
    def list_pending(limit: int = 20, only_pending: bool = True):
        conn = get_conn()
        cur = conn.cursor()
        if only_pending:
            cur.execute(
                "SELECT id, ticker, signal_type, confidence, status, created_at "
                "FROM signals WHERE status='PENDING' ORDER BY id DESC LIMIT ?", (limit,))
        else:
            cur.execute(
                "SELECT id, ticker, signal_type, confidence, status, created_at "
                "FROM signals ORDER BY id DESC LIMIT ?", (limit,))
        return cur.fetchall()

    @staticmethod
    def update_status(signal_id: int, status: str):
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "UPDATE signals SET status=? WHERE id=?",
            (status, signal_id)
        )

        conn.commit()
