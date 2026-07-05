import binder.config as config

# Project builders
from binder.builders.laravel.project import build_laravel_project_summary
from binder.builders.python.project import build_python_project_summary
from binder.builders.android.project import build_android_project_summary

def build_focus_project_info():
    return{
        "name": config.ROOT.name,
        "root": str(config.ROOT),
        "project_summary": f"See {config.ROOT.name}_project_context.json",
    }

def build_project_info(scan):
    project_type = scan.get("project_type", "unknown")
    
    if project_type == "python":
        summary = build_python_project_summary(scan)
        
    elif project_type == "laravel":
        summary = build_laravel_project_summary(scan)
    
    elif project_type == "android":
        summary = build_android_project_summary(scan)
        
    elif project_type == "mixed":
        summary = {
            "type": "mixed",
            "laravel": build_laravel_project_summary(scan),
            "python": build_python_project_summary(scan),
        }
    
    else:
        summary = {
            "type": "unknown"
        }
        
    return {
        "name": config.ROOT.name,
        "root": str(config.ROOT),
        "project_summary": summary,
    }