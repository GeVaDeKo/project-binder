import re

# Deelt de routes op in uri, controller en action
def parse_route_definition(definition):
    route = {
        "uri": None,
        "controller": None,
        "action": None
    }
    
    uri_match = re.search(r"['\"]([^'\"]+)['\"]", definition)
    
    if uri_match:
        route["uri"] = uri_match.group(1)
        
    controller_match = re.search(
        r"\[(\w+)::class,\s*['\"](\w+)['\"]\]",
        definition
    )
    
    if controller_match:
        route["controller"] = controller_match.group(1)
        route["action"] = controller_match.group(2)
    
    return route