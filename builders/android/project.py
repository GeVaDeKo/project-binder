def build_android_project_summary(scan):
    project = scan.get("android_project", {})

    return {
        "sdk": project.get("sdk", {}),
        "features": project.get("features", []),
        "statistics": {
            "files": len(scan.get("android", [])),
            "kotlin": len([f for f in scan.get("android", []) if f.get("extension") == ".kt"]),
            "java": len([f for f in scan.get("android", []) if f.get("extension") == ".java"]),
        }
    }