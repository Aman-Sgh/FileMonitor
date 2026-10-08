from pathlib import Path
import hashlib


def calc_hash(file_path: Path) -> str:
    
    sha256_hash = hashlib.sha256()
    
    with file_path.open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
            
        return sha256_hash.hexdigest();