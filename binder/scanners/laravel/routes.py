import re

import binder.config as config
from binder.parsers import parse_route_definition
from binder.files import read_file
from binder.warnings import detect_warnings

def scan_routes() -> list:
    results = []
    path = config.ROOT / "routes"
    
    if not path.exists():
        return results
    
    route_pattern = re.compile(
        r"Route::(get|post|put|patch|delete|resource)\s*\((.*?)\);",
        re.DOTALL
    )
    
    for file in path.glob("*.php"):
        text = read_file(file)
        rel = str(file.relative_to(config.ROOT))
        
        routes = []
        for match in route_pattern.finditer(text):
            definition = " ".join(match.group(2).split())
            
            parsed = parse_route_definition(definition)
            
            routes.append({
                "method": match.group(1).upper(),
                "uri": parsed["uri"],
                "controller": parsed["controller"],
                "action": parsed["action"]
            })
        
        results.append({
            "path": rel,
            "route_count": len(routes),
            "routes": routes,
            "warnings": detect_warnings(rel, text)
        })
    
    return results