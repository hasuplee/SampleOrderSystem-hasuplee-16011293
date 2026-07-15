"""SQLite 연결 및 스키마 초기화."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS samples (
    sample_id             TEXT PRIMARY KEY,
    name                  TEXT NOT NULL,
    avg_production_time   REAL NOT NULL,
    yield_rate             REAL NOT NULL,
    stock                  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    order_id       TEXT PRIMARY KEY,
    sample_id      TEXT NOT NULL,
    customer_name  TEXT NOT NULL,
    quantity       INTEGER NOT NULL,
    status         TEXT NOT NULL,
    FOREIGN KEY (sample_id) REFERENCES samples (sample_id)
);
"""


def get_connection(db_path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path) -> None:
    conn = get_connection(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
