from pathlib import Path
from src.fim.scanner import find_files
from src.fim.database import create_database
from src.fim.scanner import scan_directory

def test_find_files(tmp_path: Path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    
    subfolder = tmp_path / "subfolder"
    subfolder.mkdir()
    file3 = subfolder / "file3.txt"
    
    file1.write_text("File 1")
    file2.write_text("File 2")
    file3.write_text("File 3")
    
    files = find_files(tmp_path)
    assert len(files) == 3
    

def test_file_metadata(tmp_path: Path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello, World!")
    
    stat = test_file.stat()
    
    assert stat.st_size > 0
    assert stat.st_mtime > 0
    assert stat.st_birthtime > 0
    
    
def test_scan_directory(tmp_path: Path):
    scan_dir = tmp_path / "scan"
    scan_dir.mkdir()
    file_1 = scan_dir / "file1.txt"
    file_2 = scan_dir / "file2.txt"

    file_1.write_text("File 1")
    file_2.write_text("File 2")

    database_path = tmp_path / "test.db"
    connection = create_database(database_path)

    scan_directory(scan_dir, connection)

    result = connection.execute(
        "SELECT path FROM files"
    ).fetchall()

    assert len(result) == 2
    assert (str(file_1),) in result
    assert (str(file_2),) in result

    connection.close()