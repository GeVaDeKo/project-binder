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