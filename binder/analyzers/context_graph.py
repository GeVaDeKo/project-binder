def class_name_from_path(path: str) -> str:
    return path.split("/")[-1].replace(".php", "")

def build_model_table_map(models: list) -> dict:
    result = {}
    
    for model in models:
        name = class_name_from_path(model.get("path", ""))
        table = model.get("table")
        
        if name and table:
            result[name] = {
                "model": name,
                "path": model.get("path"),
                "table": table,
                "table_source": model.get("table_source"),
            }
    
    return result

def build_table_model_map(model_table_map: dict) -> dict:
    return {
        info["table"]: model
        for model, info in model_table_map.items()
        if info.get("table")
    }

def find_foreign_key_links(database: dict, table_model_map: dict) -> list:
    links = []
    tables = set(database.keys())
    
    for table, info in database.items():
        for column in info.get("columns", []):
            column_name = column.get("name", "")
            
            if not column_name.endswith("_id"):
                continue
            
            base = column_name[:-3]
            guesses = [
                f"{base}s",
                f"{base}es",
            ]
            
            target_table = next((guess for guess in guesses if guess in tables), None)
            
            links.append({
                "from_table": table,
                "column": column_name,
                "to_table": target_table,
                "to_model": table_model_map.get(target_table),
                "target_exists": target_table is not None,
            })
    
    return links

def build_referenced_by(foreign_key_links: list) -> dict:
    referenced_by = {}
    
    for link in foreign_key_links:
        to_table = link.get("to_table")
        
        if not to_table:
            continue
        
        referenced_by.setdefault(to_table, []).append({
            "table": link.get("from_table"),
            "column": link.get("column"),
        })
    
    return referenced_by

def build_context_graph(database: dict, models: list) -> dict:
    model_table_map = build_model_table_map(models)
    table_model_map = build_table_model_map(model_table_map)
    foreign_key_links = find_foreign_key_links(database, table_model_map)
    referenced_by = build_referenced_by(foreign_key_links)
    
    graph = {
        "models": {},
        "tables": {},
        "foreign_key_links": foreign_key_links,
    }
    
    for model_name, info in model_table_map.items():
        table = info.get("table")
        
        graph["models"][model_name] = {
            "path": info.get("path"),
            "table": table,
            "table_source": info.get("table_source"),
            "referenced_by": referenced_by.get(table, []),
        }
    
    for table, info in database.items():
        graph["tables"][table] = {
            "model": table_model_map.get(table),
            "columns": info.get("columns", []),
            "references": [
                link for link in foreign_key_links
                if link.get("from_table") == table
            ],
            "referenced_by": referenced_by.get(table, []),
        }
        
    return graph