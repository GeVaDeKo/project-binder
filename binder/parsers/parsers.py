import re, argparse, sys

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

# Serve commando
def parse_serve_command():
    if len(sys.argv) < 2:
        return None
    if sys.argv[1].lower() != "serve":
        return None
    
    target = sys.argv[2] if len(sys.argv) > 2 else None
    
    return {
        "command": "serve",
        "target": target,
    }

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
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--serve-worker", action="store_true")
    parser.add_argument("--serve-status", action="store_true")
    parser.add_argument("--serve-stop", action="store_true")
    
    return parser.parse_args()

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

def skip_spaces(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    
    return index

def read_until_stop(text: str, index: int) -> str:
    stop_chars = {
        "{",
        "=",
        "\n",
        "\r",
    }

    end = index

    while end < len(text):
        if text[end] in stop_chars:
            break

        end += 1

    return text[index:end].strip()