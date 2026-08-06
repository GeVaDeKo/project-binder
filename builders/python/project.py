def build_python_project_summary(scan):
    files = scan.get("python", [])

    return {
        "statistics": {
            "files": len(files),
            "classes": sum(len(f.get("classes", [])) for f in files),
            "functions": sum(len(f.get("functions", [])) for f in files),
            "imports": sum(len(f.get("imports", [])) for f in files),
        },
    }