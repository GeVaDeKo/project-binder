def camel_to_snake(name: str) -> str:
    result = ""
    
    for index, char in enumerate(name):
        if char.isupper() and index > 0:
            result += "_"
        result += char.lower()
    
    return result

def singularize(name: str) -> str:
    if name.endswith("ies"):
        return name[:3] + "y"
    if name.endswith("ses"):
        return name[:2]
    if name.endswith("s"):
        return name[:1]
    return name

# Convert model naar table bijv: TicketFromUser naar ticket_from_users
def guess_laravel_table(model_name: str) -> str:
    snake = camel_to_snake(model_name)
    
    if snake.endswith("y"):
        return snake[:-1] + "ies"
    
    if snake.endswith(("s", "x", "z", "ch", "sh")):
        return snake + "es"
    
    return snake + "s"

def detect_database_relations(database: dict, models: list) -> dict:
    relations = {
        "foreign_keys": [],
        "pivot_like_tables": [],
        "table_links": {},
        "model": "",
    }
    
    tables = set(database.keys())
    
    for table, info in database.items():
        columns = info.get("columns", [])
        
        fk_columns = [
            col.get("name")
            for col in columns
            if col.get("name", "").endswith("_id")
        ]
        
        for column in fk_columns:
            base = column[:-3]
            guessed_table = base + "s"
            
            if guessed_table not in tables:
                guessed_table = base + "es"
                
                relation = {
                    "from_table": table,
                    "column": column,
                    "guessed_target_table": guessed_table,
                    "target_exists": guessed_table in tables,
                }
                
                relations["foreign_keys"].append(relation)
                
                relations["table_links"].setdefault(table, []).append(relation)
                
                for model in models:
                    relations["model"] = model
            
            if len(fk_columns) >= 2:
                relations["pivot_like_tables"].append({
                    "table": table,
                    "foreign_key_columns": fk_columns,
                    "confidence": "medium" if len(fk_columns) == 2 else "low",
                })
        
    return relations
