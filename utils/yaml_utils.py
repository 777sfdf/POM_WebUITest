import yaml
from pathlib import Path

def load_yaml(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"YAML config not found: {path}")
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f)
