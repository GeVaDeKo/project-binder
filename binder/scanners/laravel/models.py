import binder.config as config
from binder.metrics import count_lines
from binder.files import should_skip, read_file
from binder.warnings import detect_warnings
from binder.analyzers.database_relations import guess_laravel_table

# Extractors
from binder.extractors.laravel.relations import find_model_relations
from binder.extractors.laravel.methods import find_php_methods
from binder.extractors.laravel.model_metadata import extract_model_table
from binder.extractors.laravel.comments import collect_laravel_comments

def scan_models(deep=False) -> list:
    results = []
    path = config.ROOT / "app/Models"
    
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
        
        model_name = file.stem
        explicit_table = extract_model_table(text)
        table = explicit_table or guess_laravel_table(model_name)
        
        results.append({
            "path": rel,
            "table": table,
            "table_source": "explicit" if explicit_table else "laravel_default",
            "metrics": count_lines(text),
            "relations": find_model_relations(text),
            "methods": methods,
            "comments": collect_laravel_comments(text),
            "warnings": detect_warnings(rel, text)
        })
    
    return results