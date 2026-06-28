import re

import binder.config as config
from binder.files import read_file

# Defineert het migration pad en scant alle migrations in die map
def scan_migrations() -> list:
    results = []
    path = config.ROOT / "database/migrations"
    
    if not path.exists():
        return results
    
    block_pattern = re.compile(
        r"Schema::(create|table)\(['\"](.+?)['\"],\s*function\s*\(Blueprint\s+\$table\)\s*\{(.*?)\n\s*\}\);",
        re.DOTALL
    )
    column_pattern = re.compile(r"\$table->(\w+)\(['\"](.+?)['\"]")
    
    for file in path.glob("*.php"):
        text = read_file(file)
        rel = str(file.relative_to(config.ROOT))
        
        tables = []
        columns = []
        
        for block in block_pattern.finditer(text):
            action = block.group(1)
            table = block.group(2)
            body = block.group(3)
            
            block_columns= [
                {"type": m.group(1), "name": m.group(2)}
                for m in column_pattern.finditer(body)
            ]
            
            tables.append({
                "action": action,
                "table": table,
                "columns": block_columns
            })
            
            columns.extend(block_columns)
        
        results.append({
            "path": rel,
            "tables": tables
        })
    
    return results