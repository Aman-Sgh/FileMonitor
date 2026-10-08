from pathlib import Path

from src.fim.config import load_config


def test_load_config(tmp_path: Path):
    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
paths:
  - "C:\\\\FIM\\\\important"

scan:
  recursive: true

hash:
  algorithm: sha256
""",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config["paths"] == ["C:\\FIM\\important"]
    assert config["scan"]["recursive"] is True
    assert config["hash"]["algorithm"] == "sha256"