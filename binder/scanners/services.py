import binder.config as config
from binder.metrics import count_lines
from binder.files import should_skip, read_file
from binder.warnings import detect_warnings
from binder.extractors.relations import find_model_relations
from binder.extractors.methods import find_php_methods

def scan_services(deep=False) -> list:
    results = []
    path = config.ROOT / "app/Services"
    
    if not path.exists():
        return results
    
    for file in path.rglob("*.php"):
        if should_skip(file):
            continue
        
        text = read_file(file)
        rel = str(file.relative_to(config.ROOT))
        
        methods = find_php_methods(
            text,
            models=[],
            services=[],
            requests=[],
            deep=deep,
        )
        
        results.append({
            "path": rel,
            "metrics": count_lines(text),
            "relations": find_model_relations(text),
            "methods": methods,
            "warnings": detect_warnings(rel, text)
        })
    
    return results