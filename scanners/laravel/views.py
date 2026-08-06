import binder.config as config
from binder.metrics import count_lines
from binder.files import read_file
from binder.warnings import detect_warnings

def scan_views() -> list:
    results = []
    path = config.ROOT / "resources/views"
    
    if not path.exists():
        return results
    
    for file in path.rglob("*.blade.php"):
        text = read_file(file)
        rel = str(file.relative_to(config.ROOT))
        lines = text.splitlines()
        
        entry = {
            "path": rel,
            "warnings": detect_warnings(rel, text)
        }
        
        if len(lines) > 60:
            entry["metrics"] = count_lines(text)
        
        results.append(entry)
        
    return results