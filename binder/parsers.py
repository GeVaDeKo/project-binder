import re, argparse

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

# Parsed de argumenten die mee worden gegeven als "--flag"
def parse_args():
    parser = argparse.ArgumentParser(description="Project Binder")
    parser.add_argument("project_path")
    parser.add_argument("--focus", default=None)
    
    return parser.parse_args()

# Zoekt naar het einde van een "method" als de teller op -1 staat is het einde van een method behaald
def find_matching_brace(text: str, open_index: int) -> int:
    depth = 0
    
    for i in range(open_index, len(text)):
        char = text[i]
        
        if char == "{":
            depth += 1
            
        elif char == "}":
            depth -= 1
            
            if depth == 0:
                return i
    
    return -1