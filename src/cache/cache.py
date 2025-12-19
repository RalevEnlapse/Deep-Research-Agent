import sqlite3
import json
import hashlib
from pathlib import Path
from typing import Optional, Any
import time

class Cache:
    def __init__(self, db_path: str = ".deep_research/cache.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp REAL
                )
            """)

    def _get_key(self, query: str, params: dict = None) -> str:
        key_data = {"query": query, "params": params or {}}
        return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()

    def get(self, query: str, params: dict = None, ttl: int = 3600) -> Optional[Any]:
        key = self._get_key(query, params)
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT value, timestamp FROM cache WHERE key = ?",
                (key,)
            ).fetchone()
            if row:
                value, timestamp = row
                if time.time() - timestamp < ttl:
                    return json.loads(value)
        return None

    def set(self, query: str, value: Any, params: dict = None):
        key = self._get_key(query, params)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache (key, value, timestamp) VALUES (?, ?, ?)",
                (key, json.dumps(value), time.time())
            )