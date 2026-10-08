
from pathlib import Path

from src.fim.database import add_file

def find_files(directory: Path) -> list[Path]:
    return [path for path in Path(directory).rglob("*") if path.is_file()]


    
def scan_directory(directory: Path, connection):
    files = find_files(directory)
    for file_path in files:
        add_file(connection, file_path)