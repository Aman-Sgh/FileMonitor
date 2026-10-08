import sqlite3
from pathlib import Path

from datetime import datetime

from src.fim.hasher import calc_hash

def create_database(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            hash TEXT NOT NULL,
            size INTEGER NOT NULL,
            created_at TEXT,
            modified_at TEXT,
            first_seen TEXT NOT NULL,
            last_checked TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    
    connection.execute("""
                       CREATE TABLE IF NOT EXISTS events (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            file_id INTEGER NOT NULL,
                            event_type TEXT NOT NULL,
                            old_hash TEXT, 
                            new_hash TEXT,
                            timestamp TEXT NOT NULL,
                            FOREIGN KEY (file_id) REFERENCES files (id)
                          )
                       """)

    connection.commit()

    return connection


def add_file(connection: sqlite3.Connection, file_path: Path):
    stats = file_path.stat()
    file_hash = calc_hash(file_path)
    
    now = datetime.now().isoformat()
    
    connection.execute("""
                       INSERT INTO files(
                           path,
                           hash,
                           size,
                           created_at,
                           modified_at,
                           first_seen,
                           last_checked,
                           status                           
                       )
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """,
                          (
                            str(file_path),
                            file_hash,
                            stats.st_size,
                            datetime.fromtimestamp(stats.st_birthtime).isoformat(),
                            datetime.fromtimestamp(stats.st_mtime).isoformat(),
                            now,
                            now,
                            "unchanged",
                          ),
                          )
    connection.commit()
    
def update_file_status(connection: sqlite3.Connection, file_path: Path, status: str):
    connection.execute(
        """
        UPDATE files
        SET status = ?
        WHERE path = ?
        """,
        (status, str(file_path)),
    )

    connection.commit()
    
def add_event(
    connection: sqlite3.Connection,
    file_path: Path,
    event_type: str,
    old_hash: str = None,
    new_hash: str = None,
    ):
    result = connection.execute("SELECT id FROM files WHERE path = ?", (str(file_path),)).fetchone()
    
    if result is None:
        return
    file_id = result[0]
    timestamp = datetime.now().isoformat()
    
    connection.execute(
    """
    INSERT INTO events (
        file_id,
        event_type,
        old_hash,
        new_hash,
        timestamp
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (file_id, event_type, old_hash, new_hash, timestamp)
    
    
)
    connection.commit()