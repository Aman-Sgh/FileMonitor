from pathlib import Path
from src.fim.database import add_event, add_file, create_database

def test_create_database(tmp_path: Path):
    db_path = tmp_path / "test.db"
    
    connection = create_database(db_path)
    tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    
    
    assert ("files",) in tables
    connection.close()


def test_add_file(tmp_path: Path):
    database_path = tmp_path / "test.db"
    test_file = tmp_path / "test.txt"

    test_file.write_text("Hello FIM!")

    connection = create_database(database_path)

    add_file(connection, test_file)

    result = connection.execute(
        "SELECT path, hash, size, status FROM files"
    ).fetchone()

    assert result is not None
    assert result[0] == str(test_file)
    assert len(result[1]) == 64
    assert result[2] == test_file.stat().st_size
    assert result[3] == "unchanged"

    connection.close()
    
    
def test_add_event(tmp_path: Path):
    database_path = tmp_path / "test.db"
    test_file = tmp_path / "test.txt"

    test_file.write_text("Hello FIM!")

    connection = create_database(database_path)

    add_file(connection, test_file)

    add_event(
        connection,
        test_file,
        "modified",
        "old_hash",
        "new_hash",
    )

    result = connection.execute(
        """
        SELECT event_type, old_hash, new_hash
        FROM events
        """
    ).fetchone()

    assert result == ("modified", "old_hash", "new_hash")

    connection.close()