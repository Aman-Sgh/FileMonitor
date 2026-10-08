from pathlib import Path

from src.fim.database import add_file, create_database
from src.fim.monitor import (
    check_file,
    find_deleted_files,
    mark_deleted_files,
    scan_integrity,
)


def test_check_file_modified(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Original")

    database_path = tmp_path / "test.db"
    connection = create_database(database_path)

    add_file(connection, test_file)

    test_file.write_text("Modified")

    result = check_file(connection, test_file)

    assert result == "modified"

    connection.close()


def test_find_deleted_files(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello FIM!")

    database_path = tmp_path / "test.db"
    connection = create_database(database_path)

    add_file(connection, test_file)

    test_file.unlink()

    deleted_files = find_deleted_files(connection, tmp_path)

    assert test_file in deleted_files

    connection.close()


def test_mark_deleted_files(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello FIM!")

    database_path = tmp_path / "test.db"
    connection = create_database(database_path)

    add_file(connection, test_file)

    test_file.unlink()

    mark_deleted_files(connection, tmp_path)

    result = connection.execute(
        "SELECT status FROM files WHERE path = ?",
        (str(test_file),)
    ).fetchone()

    assert result is not None
    assert result[0] == "deleted"

    connection.close()


def test_scan_integrity(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Original")

    database_path = tmp_path / "test.db"
    connection = create_database(database_path)

    add_file(connection, test_file)

    test_file.write_text("Modified")

    scan_integrity(connection, tmp_path)

    result = connection.execute(
        "SELECT status FROM files WHERE path = ?",
        (str(test_file),)
    ).fetchone()

    assert result is not None
    assert result[0] == "modified"

    connection.close()
    
    
def test_scan_integrity_new_file(tmp_path: Path):
    database_path = tmp_path / "test.db"
    connection = create_database(database_path)

    old_file = tmp_path / "old.txt"
    old_file.write_text("Old")
    add_file(connection, old_file)

    new_file = tmp_path / "new.txt"
    new_file.write_text("New")

    scan_integrity(connection, tmp_path)

    result = connection.execute(
        "SELECT status FROM files WHERE path = ?",
        (str(new_file),)
    ).fetchone()

    assert result is not None
    assert result[0] == "new"

    connection.close()
    
    
    
def test_scan_integrity_new_file(tmp_path: Path):
    database_path = tmp_path / "test.db"
    connection = create_database(database_path)

    old_file = tmp_path / "old.txt"
    old_file.write_text("Old")
    add_file(connection, old_file)

    new_file = tmp_path / "new.txt"
    new_file.write_text("New")

    scan_integrity(connection, tmp_path)

    result = connection.execute(
        "SELECT status FROM files WHERE path = ?",
        (str(new_file),)
    ).fetchone()

    assert result is not None
    assert result[0] == "new"

    connection.close()