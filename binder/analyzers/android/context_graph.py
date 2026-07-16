def build_android_context_graph(files):
    declarations = {}
    
    for file in files:
        for decl in file.get("declarations", []):
            declarations[decl["name"]] = {
                "path": file["path"],
                "type": decl["type"],
                "package": file.get("package"),
                "imports": file.get("imports", []),
            }
            
    graph = {}
    
    for name, info in declarations.items():
        dependencies = []
        
        for imported in info["imports"]:
            imported_name = imported.split(".")[-1]
            
            if imported_name in declarations:
                dependencies.append({
                    "name": imported_name,
                    "path": declarations[imported_name]["path"],
                    "via": "import",
                })
        
        graph[name] = {
            "path": info["path"],
            "type": info["type"],
            "package": info["package"],
            "dependencies": dependencies,
        }
    
    return graph

def build_android_filter_graph(context_graph, focus):
    if not focus:
        return context_graph
    
    focus = focus.lower()
    
    return {
        name: info
        for name, info in context_graph.items()
        if (
            focus in name.lower()
            or focus in info.get("path", "").lower()
            or any(
                focus in dep["name"].lower()
                or focus in dep["path"].lower()
                for dep in info.get("dependencies", [])
            )
        )
    }