"""
database.py
-----------
Database layer for the ID Card Generator.

Supports two backends, chosen via app.config.DB_TYPE:
  - "sqlite" (default, zero-config, file based)
  - "mysql"  (requires `mysql-connector-python` and a running MySQL server)

Both backends expose the exact same public API (see IDCardDatabase),
so the rest of the application never needs to know which one is active.
"""

import os
import sqlite3
import datetime
from typing import Optional, List, Dict, Any

from app import config


class IDCardDatabase:
    """Unified database interface for storing generated ID card records."""

    def __init__(self, db_type: str = None):
        self.db_type = (db_type or config.DB_TYPE).lower()
        self._conn = None
        self._connect()
        self._create_tables()

    # ------------------------------------------------------------------
    # Connection handling
    # ------------------------------------------------------------------
    def _connect(self):
        if self.db_type == "mysql":
            try:
                import mysql.connector  # imported lazily, optional dependency
                self._conn = mysql.connector.connect(**config.MYSQL_CONFIG)
                self._placeholder = "%s"
            except Exception as exc:
                print(f"[Database] Could not connect to MySQL ({exc}). "
                      f"Falling back to SQLite.")
                self.db_type = "sqlite"
                self._connect_sqlite()
        else:
            self._connect_sqlite()

    def _connect_sqlite(self):
        self._conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._placeholder = "?"

    def _create_tables(self):
        cur = self._conn.cursor()
        if self.db_type == "mysql":
            cur.execute("""
                CREATE TABLE IF NOT EXISTS id_cards (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_number VARCHAR(64) UNIQUE,
                    name VARCHAR(255),
                    department VARCHAR(255),
                    phone VARCHAR(64),
                    address TEXT,
                    photo_path TEXT,
                    logo_path TEXT,
                    signature_path TEXT,
                    template_path TEXT,
                    card_image_path TEXT,
                    created_at DATETIME
                )
            """)
        else:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS id_cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_number TEXT UNIQUE,
                    name TEXT,
                    department TEXT,
                    phone TEXT,
                    address TEXT,
                    photo_path TEXT,
                    logo_path TEXT,
                    signature_path TEXT,
                    template_path TEXT,
                    card_image_path TEXT,
                    created_at TEXT
                )
            """)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Automatic ID numbering
    # ------------------------------------------------------------------
    def get_next_id_number(self, prefix: str = None) -> str:
        """Generate the next sequential ID number, e.g. AIT-0001, AIT-0002..."""
        prefix = prefix or config.ID_PREFIX
        cur = self._conn.cursor()
        cur.execute("SELECT id_number FROM id_cards WHERE id_number LIKE "
                    f"{self._placeholder}", (f"{prefix}-%",))
        rows = cur.fetchall()
        max_n = 0
        for row in rows:
            id_number = row["id_number"] if self.db_type == "sqlite" else row[0]
            try:
                n = int(str(id_number).split("-")[-1])
                max_n = max(max_n, n)
            except (ValueError, IndexError):
                continue
        return f"{prefix}-{max_n + 1:04d}"

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def insert_record(self, data: Dict[str, Any]) -> int:
        cur = self._conn.cursor()
        fields = ["id_number", "name", "department", "phone", "address",
                  "photo_path", "logo_path", "signature_path",
                  "template_path", "card_image_path", "created_at"]
        values = [
            data.get("id_number"),
            data.get("name"),
            data.get("department"),
            data.get("phone"),
            data.get("address"),
            data.get("photo_path"),
            data.get("logo_path"),
            data.get("signature_path"),
            data.get("template_path"),
            data.get("card_image_path"),
            datetime.datetime.now().isoformat(timespec="seconds"),
        ]
        placeholders = ", ".join([self._placeholder] * len(fields))
        sql = f"INSERT INTO id_cards ({', '.join(fields)}) VALUES ({placeholders})"
        cur.execute(sql, values)
        self._conn.commit()
        return cur.lastrowid

    def update_record(self, record_id: int, data: Dict[str, Any]):
        cur = self._conn.cursor()
        fields = ["name", "department", "phone", "address", "photo_path",
                  "logo_path", "signature_path", "template_path",
                  "card_image_path"]
        set_clause = ", ".join([f"{f} = {self._placeholder}" for f in fields])
        values = [data.get(f) for f in fields] + [record_id]
        sql = f"UPDATE id_cards SET {set_clause} WHERE id = {self._placeholder}"
        cur.execute(sql, values)
        self._conn.commit()

    def get_all_records(self) -> List[Dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM id_cards ORDER BY id DESC")
        rows = cur.fetchall()
        if self.db_type == "sqlite":
            return [dict(row) for row in rows]
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in rows]

    def get_record_by_id_number(self, id_number: str) -> Optional[Dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute(
            f"SELECT * FROM id_cards WHERE id_number = {self._placeholder}",
            (id_number,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        if self.db_type == "sqlite":
            return dict(row)
        columns = [desc[0] for desc in cur.description]
        return dict(zip(columns, row))

    def delete_record(self, record_id: int):
        cur = self._conn.cursor()
        cur.execute(f"DELETE FROM id_cards WHERE id = {self._placeholder}",
                    (record_id,))
        self._conn.commit()

    def close(self):
        if self._conn:
            self._conn.close()
