import binder.config as config

# Project builders
from binder.builders.laravel.project import build_laravel_project_summary
from binder.builders.python.project import build_python_project_summary
from binder.builders.android.project import build_android_project_summary

from binder.summary import build_project_summary

from binder.packages import (
    scan_composer_packages,
    scan_frontend_packages,
)

def build_focus_project_info(scan, project_type):
    return{
        "name": config.ROOT.name,
        "root": str(config.ROOT),
        **build_project_identity(scan, project_type),
        "project_summary": f"See {config.ROOT.name}_project_context.json",
    }

def build_project_info(scan, project_type):
    identity = build_project_identity(
        scan,
        project_type,
    )
    
    if project_type == "laravel":
        summary = build_laravel_project_summary(scan)
    elif project_type == "python":
        summary = build_python_project_summary(scan)
    elif project_type == "android":
        summary = build_android_project_summary(scan)
    else:
        summary = {}
        
    return {
        "name": config.ROOT.name,
        "root": str(config.ROOT),
        **identity,
        "project_summary": summary,
    }

def build_project_identity(scan, project_type):
    if project_type == "laravel":
        return{
            "project_type": "laravel",
            "language": "php",
        }
    
    if project_type == "python":
        return {
            "project_type": "python",
            "language": "python",
            "framework": None,
        }

    if project_type == "android":
        android_files = scan.get("android", [])

        kotlin_count = sum(
            1 for file in android_files
            if file.get("extension") == ".kt"
        )

        java_count = sum(
            1 for file in android_files
            if file.get("extension") == ".java"
        )

        language = "kotlin" if kotlin_count >= java_count else "java"
        
        return {
            "project_type": "android",
            "language": language,
            "framework": "android",
        }

    return {
        "project_type": project_type or "unknown",
        "language": None,
        "framework": None,
    }