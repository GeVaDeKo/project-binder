import json
from pathlib import Path
import binder.config as config

def should_skip(path: Path) -> bool:
    rel = str(path.relative_to(config.ROOT))
    return any(rel.startswith(skip) for skip in config.IGNORE_DIRS)

def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

# Kan een .json bestand uitlezen zoals composer.json en package.json voor project details
def read_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

# Zoekt en vind "classes"
def collect_class_names(directory: str) -> set:
    path = config.ROOT / directory
    
    if not path.exists():
        return set()
    
    return {
        file.stem
        for file in path.rglob("*.php")
        if not should_skip(file)
    }