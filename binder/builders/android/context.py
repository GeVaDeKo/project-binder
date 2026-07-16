from binder.analyzers.android.context_graph import build_android_filter_graph

def build_android_context(scan):
    return {
        "android": scan["android"],
        "android_context_graph": scan.get("android_context_graph", {}),
    }

def build_android_focus_context(scan, focus):
    files = scan.get("android", [])
    graph = scan.get("android_context_graph", {})
    
    return {
        "android": filter_android_files(files, focus),
        "android_context_graph": build_android_filter_graph(graph, focus),
    }

def filter_android_files(files, focus):
    if not focus:
        return files
    
    focus = focus.lower()
    
    return [
        file for file in files
        if android_file_matches(file, focus)
    ]

def android_file_matches(file, focus):
    haystack = [
        file.get("path", ""),
        file.get("package", ""),
        *file.get("imports", []),
    ]
    
    for declaration in file.get("declarations", []):
        haystack.append(declaration.get("name", ""))
        haystack.append(declaration.get("type", ""))
    
    for method in file.get("methods", []):
        haystack.append(method.get("name", ""))
        haystack.append(method.get("arguments", ""))
        haystack.append(method.get("returns", ""))
        haystack.append(method.get("annotations", []))
        haystack.append(method.get("calls", []))
    
    for lines in file.get("comments", {}).values():
        haystack.extend(lines)
    
    return any(focus in str(value).lower() for value in haystack)