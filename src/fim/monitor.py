from pathlib import Path
import sqlite3

from src.fim.database import add_event, add_file, update_file_status
from src.fim.scanner import find_files
from src.fim.hasher import calc_hash


def check_file(connection: sqlite3.Connection, file_path: Path):
    current_hash = calc_hash(file_path)

    result = connection.execute(
        "SELECT hash FROM files WHERE path = ?",
        (str(file_path),)
    ).fetchone()

    if result is None:
        return "new"

    stored_hash = result[0]

    if current_hash != stored_hash:
        return "modified"

    return "unchanged"


def get_tracked_files(connection):
    result = connection.execute(
        "SELECT path FROM files"
    ).fetchall()

    return {Path(row[0]) for row in result}


def get_current_files(directory: Path):
    return set(find_files(directory))


def find_deleted_files(connection, directory: Path):
    tracked_files = get_tracked_files(connection)
    current_files = get_current_files(directory)

    return tracked_files - current_files


def mark_deleted_files(connection, directory: Path):
    deleted_files = find_deleted_files(connection, directory)

    for file_path in deleted_files:
        update_file_status(connection, file_path, "deleted")


def scan_integrity(connection: sqlite3.Connection, directory: Path):
    current_files = get_current_files(directory)

    stats = {
        "new": 0,
        "modified": 0,
        "deleted": 0,
        "unchanged": 0,
    }

    for file_path in current_files:
        status = check_file(connection, file_path)

        if status == "new":
            new_hash = calc_hash(file_path)
            add_file(connection, file_path)
            add_event(connection, file_path, "new", None, new_hash)
            update_file_status(connection, file_path,"new")

        elif status == "modified":
            result = connection.execute(
                "SELECT hash FROM files WHERE path = ?",
                (str(file_path),)
            ).fetchone()
            old_hash = result[0]
            new_hash = calc_hash(file_path)
            add_event(connection, file_path, "modified", old_hash, new_hash)
            update_file_status(connection, file_path, "modified")

        else:
            update_file_status(connection, file_path, "unchanged")

        stats[status] += 1

    deleted_files = find_deleted_files(connection, directory)

    for file_path in deleted_files:
        result = connection.execute("SELECT hash FROM files WHERE path = ?",
                                    (str(file_path),)).fetchone()
        old_hash = result[0]
        add_event(connection, file_path, "deleted", old_hash, None)
        
        update_file_status(connection, file_path, "deleted")

    stats["deleted"] = len(deleted_files)

    return stats


def get_status_counts(connection: sqlite3.Connection):
    result = connection.execute(
        """
        SELECT status, COUNT(*)
        FROM files
        GROUP BY status
        """
    ).fetchall()

    counts = {
        "new": 0,
        "modified": 0,
        "deleted": 0,
        "unchanged": 0,
    }

    for status, count in result:
        counts[status] = count

    return counts


def get_file_statuses(connection: sqlite3.Connection):
    result = connection.execute(
        """
        SELECT path, status
        FROM files
        ORDER BY path
        """
    ).fetchall()

    return result

def get_event_history(connection: sqlite3.Connection):
    result = connection.execute(
        """
        SELECT files.path, events.event_type, events.timestamp
        FROM events
        JOIN files ON events.file_id = files.id
        ORDER BY events.timestamp
        """
    ).fetchall()

    return result