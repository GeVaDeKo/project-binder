import binder.config as config
from binder.files import should_skip, read_file
from binder.warnings import detect_warnings
from binder.extractors.methods import find_php_methods
from binder.metrics import count_lines

def scan_php_directory(
    directory: str,
    models=None,
    services=None,
    requests=None
) -> list:
    results = []
    path = config.ROOT / directory
    
    if not path.exists():
        return results
    
    for file in path.rglob("*.php"):
        if should_skip(file):
            continue
        
        text = read_file(file)
        rel = str(file.relative_to(config.ROOT))
        
        results.append({
            "path": rel,
            "metrics": count_lines(text),
            "methods": find_php_methods(
                text,
                models=models,
                services=services,
                requests=requests
            ),
            "warnings": detect_warnings(rel, text)
        })
    
    return results