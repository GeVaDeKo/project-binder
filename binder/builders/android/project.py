def build_android_project_summary(scan):
    files = scan.get("android", [])

    return {
        "type": "android",
        "statistics": {
            "files": len(files),
            "kotlin": sum(1 for f in files if f["extension"] == ".kt"),
            "java": sum(1 for f in files if f["extension"] == ".java"),
        }
    }