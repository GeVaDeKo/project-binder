import re

# Zoekt en vind een "relation" in models zoals: hasMany en belongsTo
def find_model_relations(text: str) -> list:
    relations = []
    
    method_pattern = re.compile(
        r"public\s+function\s+(\w+)\s*\(.*?\)\s*\{(.*?)\n\s*\}",
        re.DOTALL
    )
    
    relation_pattern = re.compile(
        r"return\s+\$this->(hasMany|belongsTo|belongsToMany|hasOne|morphMany|morphTo|morphOne)\s*\(\s*(\w+)::class",
        re.DOTALL
    )
    
    for method in method_pattern.finditer(text):
        name = method.group(1)
        body = method.group(2)
        
        relation = relation_pattern.search(body)
        
        if relation:
            relations.append({
                "name": name,
                "type": relation.group(1),
                "target": relation.group(2)
            })
    
    return relations