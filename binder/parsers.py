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
    parser.add_argument("-c", "--controllers", action="store_true")
    parser.add_argument("-m", "--models", action="store_true")
    parser.add_argument("-s", "--services", action="store_true")
    parser.add_argument("-v", "--views", action="store_true")
    parser.add_argument("-r", "--routes", action="store_true")
    parser.add_argument("-d", "--database", action="store_true")
    
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

# Focus flags parser
def parse_focus_scope(args):
    if not args.focus:
        return None, None, {}
    
    if ":" in args.focus:
        focus_type, focus_value = args.focus.split(":", 1)
    else:
        focus_type, focus_value = "all", args.focus
    
    scopes = {
        "controllers": args.controllers,
        "models": args.models,
        "services": args.services,
        "views": args.views,
        "routes": args.routes,
        "database": args.database,
    }
    
    if focus_type == "model":
        scopes["models"] = True
        scopes["database"] = True
    
    if focus_type == "services":
        scopes["services"] = True
    
    if focus_type == "controller":
        scopes["controllers"] = True
        scopes["routes"] = True
    
    return focus_type, focus_value, scopes