import re

# Kijkt of een er "model", "service" of "request" gebruikt word voor method binding
def extract_typed_dependencies(arguments: str, models: set, services: set, requests: set) -> dict:
    found = {
        "models_used": [],
        "services_used": [],
        "requests_used": []
    }
    
    pattern = re.compile(r"\??([A-Z]\w+)\s+\$\w+")
    
    for match in pattern.finditer(arguments):
        name = match.group(1)
        
        if name in models:
            found["models_used"].append(name)
        elif name in services:
            found["services_used"].append(name)
        elif name in requests or name.endswith("Request"):
            found["requests_used"].append(name)
    
    return{
        key: sorted(set(value))
        for key, value in found.items()
    }