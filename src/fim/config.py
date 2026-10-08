from pathlib import Path
import yaml


def load_config(config_path: Path):
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config