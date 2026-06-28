import re
from binder.extractors.dependencies import extract_typed_dependencies

# Doorzoekt het bestand op "methods" (private|public function)
def find_php_methods(text: str, models=None, services=None, requests=None) -> list:
    methods = []
    
    models = models or set()
    services = services or set()
    requests = requests or set()
    
    pattern = re.compile(
        r"(public|protected|private)\s+function\s+(\w+)\s*\((.*?)\)",
        re.DOTALL
    )
    
    for match in pattern.finditer(text):
        arguments = " ".join(match.group(3).split())
        deps = extract_typed_dependencies(arguments, models, services, requests)
        
        methods.append({
            "visibility": match.group(1),
            "name": match.group(2),
            "arguments": arguments,
            **deps
        })
        
    return methods