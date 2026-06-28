def matches_focus(value, focus):
    if not focus:
        return True
    
    if value is None:
        return False
    
    return focus.lower() in str(value).lower()

def filter_by_path(items, focus):
    if not focus:
        return items
    
    return [
        item for item in items
        if matches_focus(item.get("path"), focus)
    ]
    
def filter_controllers(items, focus):
    if not focus:
        return items
    
    filtered = []
    
    for item in items:
        path_match = matches_focus(item.get("path"), focus)
        focused_methods = filter_methods(item.get("methods", []), focus)
        
        copy = dict(item)
        
        if path_match:
            copy["focus_match"] = "path"
            copy["focused_methods"] = focused_methods
            filtered.append(copy)
            continue
        
        if focused_methods:
            copy["focus_match"] = "methods"
            copy["methods"] = focused_methods
            filtered.append(copy)

    return filtered
    
def filter_models(items, focus):
    if not focus:
        return items
    
    return [
        item for item in items
        if matches_focus(item.get("path"), focus)
        or any(matches_focus(rel.get("name"), focus) for rel in item.get("relations"))
        or any(matches_focus(rel.get("target"), focus) for rel in item.get("relations", []))
    ]
    
def filter_routes(items, focus):
    if not focus:
        return items

    filtered = []

    for file in items:
        routes = [
            route for route in file.get("routes", [])
            if matches_focus(route.get("uri"), focus)
            or matches_focus(route.get("controller"), focus)
            or matches_focus(route.get("action"), focus)
        ]

        if routes or matches_focus(file.get("path"), focus):
            copy = dict(file)
            copy["routes"] = routes
            copy["route_count"] = len(routes)
            filtered.append(copy)

    return filtered

def filter_methods(methods, focus):
    if not focus:
        return methods

    return [
        method for method in methods
        if matches_focus(method.get("name"), focus)
        or matches_focus(method.get("arguments"), focus)
        or any(matches_focus(model, focus) for model in method.get("models_used", []))
        or any(matches_focus(service, focus) for service in method.get("services_used", []))
        or any(matches_focus(request, focus) for request in method.get("requests_used", []))
    ]