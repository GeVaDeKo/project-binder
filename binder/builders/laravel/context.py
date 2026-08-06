import binder.config as config

from binder.builders.generator import scope_enabled

def build_laravel_context(scan):
    return{
        "custom_classes": scan["custom_classes"],
        "controllers": scan["controllers"],
        "models": scan["models"],
        "services": scan["services"],
        "views": scan["views"],
        "routes": scan["routes"],
        "shared_context": {
            "database": scan["database"],
            "context_graph": scan["context_graph"],
            "disks": scan["disks"],
        },
    }
    
def build_laravel_focus_shared_context(scan, focus, include_database=False):
    from binder.builders.context import build_focused_context_graph
    
    return {
        "database": scan["database"] if include_database else f"See {config.ROOT.name}_project_context.json",
        "context_graph": build_focused_context_graph(scan["context_graph"], focus),
        "disks": f"See {config.ROOT.name}_project_context.json",
    }

def build_laravel_focus_context(filtered, scopes):  
    return {
        "custom_classes": filtered["custom_classes"],
        "controllers": filtered["controllers"] if scope_enabled(scopes, "controllers") else [],
        "models": filtered["models"] if scope_enabled(scopes, "models") else [],
        "services": filtered["services"] if scope_enabled(scopes, "services") else [],
        "views": filtered["views"] if scope_enabled(scopes, "views") else [],
        "routes": filtered["routes"] if scope_enabled(scopes, "routes") else [],
    }