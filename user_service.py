# services/user_service.py

from database.db import get_conn


class UserService:

    @staticmethod
    def register(username: str, password: str) -> bool:
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
            conn.commit()
            return True
        except Exception:
            return False

    @staticmethod
    def login(username: str, password: str) -> bool:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        return cur.fetchone() is not None
