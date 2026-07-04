#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

import json, sys, shlex
import binder.config as config

from binder.files import collect_class_names

# Scanners
from binder.scanners.php import scan_php_directory
from binder.scanners.migrations import scan_migrations
from binder.scanners.models import scan_models
from binder.scanners.services import scan_services
from binder.scanners.routes import scan_routes
from binder.scanners.views import scan_views
from binder.scanners.disks import scan_disk

# Parsers
from binder.parsers import parse_args, parse_focus_scope

from binder.database import build_database_snapshot
from binder.summary import build_project_summary
from binder.packages import (
    scan_composer_packages,
    scan_frontend_packages,
)

# Analyzers
from binder.analyzers.database_relations import detect_database_relations
from binder.analyzers.context_graph import build_context_graph

# Focus
from binder.focus import (
    filter_controllers,
    filter_models,
    filter_routes,
    filter_by_path,
)

def scope_enabled(scopes, name):
    if not any(scopes.values()):
        return True
    
    return scopes.get(name, False)

def scan_project(focus=None):
    deep = bool(focus)
    
    migrations = scan_migrations()
    
    model_names = collect_class_names("app/Models")
    services_names = collect_class_names("app/Services")
    request_names = collect_class_names("app/Http/Requests")
    
    controllers = scan_php_directory(
        "app/Http/Controllers",
        models=model_names,
        services=services_names,
        requests=request_names,
        deep=deep,
    )
    
    models = scan_models()
    services = scan_services()
    views = scan_views()
    routes = scan_routes()
    
    database = build_database_snapshot(migrations)
    disks = scan_disk()
    
    context_graph = build_context_graph(database, models)
    
    return {
        "controllers": controllers,
        "models": models,
        "services": services,
        "views": views,
        "routes": routes,
        "database": database,
        "disks": disks,
        "context_graph": context_graph,
    }

def write_context(filename, context):
    output_file = config.ROOT / filename
    
    output_file.write_text(
        json.dumps(context, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    
    print(f"Laravel context geschreven naar: {output_file}")

def build_focus_project_info():
    return{
        "name": config.ROOT.name,
        "root": str(config.ROOT),
        "project_summary": f"See {config.ROOT.name}_project_context.json",
    }

def build_project_info(scan):
    return {
        "name": config.ROOT.name,
        "root": str(config.ROOT),
        "project_summary": build_project_summary({
            "project": {
                "packages": {
                    "composer": scan_composer_packages(),
                    "frontend": scan_frontend_packages(),
                }
            },
            "controllers": scan["controllers"],
            "models": scan["models"],
            "services": scan["services"],
            "database": scan["database"],
            "routes": scan["routes"],
        }),
    }
    
def build_full_context(scan):
    return {
        "generator": {
            "name": "Project-Binder",
            "vendor": "GeVaDeKo",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "command": "",
            "executable": "",
            "scopes": {},
            "context_mode": "full",
            "focus": None,
        },
        "project": build_project_info(scan),

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

def build_focus_context(scan, focus, scopes):
    controllers = filter_controllers(scan["controllers"], focus)
    models = filter_models(scan["models"], focus)
    services = filter_controllers(scan["services"], focus)
    views = filter_by_path(scan["views"], focus)
    routes = filter_routes(scan["routes"], focus)
    
    executable = Path(sys.argv[0])
    command = " ".join(
        [Path(sys.argv[0]).name] +
        [sys.argv[6]]
    )
    
    context = build_full_context(scan)
    
    context["generator"]["command"] = command
    context["generator"]["executable"] = executable
    context["generator"]["scopes"] = scopes
    context["generator"]["context_mode"] = "focus"
    context["generator"]["focus"] = focus
    
    context["project"] = build_focus_project_info()
    
    context["controllers"] = controllers if scope_enabled(scopes, "controllers") else []
    context["models"] = models if scope_enabled(scopes, "models") else []
    context["services"] = services if scope_enabled(scopes, "services") else []
    context["views"] = views if scope_enabled(scopes, "views") else []
    context["routes"] = routes if scope_enabled(scopes, "routes") else []
    
    context["shared_context"] = {
        "database": f"See {config.ROOT.name}_project_context.json",
        "context_graph": build_focused_context_graph(
            scan["context_graph"],
            focus,
        ),
        "disks": f"See {config.ROOT.name}_project_context.json",
    }
    
    if scope_enabled(scopes, "database") and any(scopes.values()):
        context["shared_context"]["database"] = scan["database"]
    
    return context

def build_focused_context_graph(context_graph, focus):
    if not focus:
        return context_graph

    return {
        "focus": focus,
        "models": {
            key: value
            for key, value in context_graph.get("models", {}).items()
            if focus.lower() in key.lower()
        },
        "tables": {
            key: value
            for key, value in context_graph.get("tables", {}).items()
            if focus.lower() in key.lower()
            or (
                value.get("model")
                and focus.lower() in value.get("model", "").lower()
            )
        },
    }

def binder_dir():
    path = config.ROOT / "project-binder"
    path.mkdir(exist_ok=True)
    return path

def ensure_gitignore_entry():
    gitignore = config.ROOT / ".gitignore"
    entry = "/project-binder/"
    
    if not gitignore.exists():
        gitignore.write_text(f"# Project Binder\n{entry}\n", encoding="utf-8")
        return
    
    text = gitignore.read_text(encoding="utf-8", errors="ignore")
    
    if entry in text:
        return
    
    with gitignore.open("a", encoding="utf-8") as f:
        f.write(f"\n# Project Binder\n{entry}\n")

def main():
    args = parse_args()
    focus_type, focus, scopes = parse_focus_scope(args)
    
    config.set_root(args.project_path)
    ensure_gitignore_entry()
    
    scan = scan_project(focus)
    
    full_context = build_full_context(scan)
    write_context(
        binder_dir() / f"{config.ROOT.name}_project_context.json",
        full_context,
    )
    
    if focus or any(scopes.values()):
        focused_context = build_focus_context(scan, focus, scopes)
        write_context(
            binder_dir() / f"{config.ROOT.name}_{focus or 'selection'}_context.json",
            focused_context,
        )

if __name__ == "__main__":
    main()