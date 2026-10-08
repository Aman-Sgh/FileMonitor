from pathlib import Path
from src.fim.hasher import calc_hash

def test_calc_same_hash(tmp_path: Path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello, World!")
    
    hash_1 = calc_hash(test_file)
    hash_2 = calc_hash(test_file)

    assert hash_1 == hash_2;
    
def test_calc_different_hash(tmp_path: Path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello, World!")

    hash_1 = calc_hash(test_file)

    test_file.write_text("Hello, FIM!")

    hash_2 = calc_hash(test_file)

    assert hash_1 != hash_2;