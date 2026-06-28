from binder.config import SKIP_COLUMN_TYPES
# Maakt van de gescande migrations een snapshot voor de structuur
def build_database_snapshot(migrations):
    database = {}
    
    for migration in migrations:
        tables = migration.get("tables", [])
        
        for table_info in tables:
            table_name = table_info.get("table")
            columns = table_info.get("columns", [])
            
            if not table_name:
                continue
            
            if table_name not in database:
                database[table_name] = {
                    "columns": []
                }
            
            existing = {
                (col["name"], col["type"])
                for col in database[table_name]["columns"]
            }
            
            for column in columns:
                key = (column.get("name"), column.get("type"))
                
                if key in existing:
                    continue
                
                if column.get("type") in SKIP_COLUMN_TYPES:
                    continue
                
                database[table_name]["columns"].append({
                    "name": column.get("name"),
                    "type": column.get("type"),
                })
                
                existing.add(key)
    
    return database