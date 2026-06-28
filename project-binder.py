#!/usr/bin/env python3

from datetime import datetime
import json, sys
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
from binder.parsers import parse_args

from binder.database import build_database_snapshot
from binder.summary import build_project_summary
from binder.packages import (
    scan_composer_packages,
    scan_frontend_packages,
)

# Focus
from binder.focus import (
    filter_controllers,
    filter_models,
    filter_routes,
    filter_by_path,
)

def main():
    args = parse_args()
    print(args)
    
    config.set_root(args.project_path)
    
    focus = args.focus
    deep = bool(focus)
    
    migrations = scan_migrations()
    
    # Bepaal de mappen voor "models", "services" en "requests"
    model_names = collect_class_names("app/Models")
    service_names = collect_class_names("app/Services")
    request_names = collect_class_names("app/Http/Requests")
    
    controllers = scan_php_directory(
        "app/Http/Controllers",
        models=model_names,
        services=service_names,
        requests=request_names,
        deep=deep
    )
    models = scan_models()
    services = scan_php_directory(
        "app/Services",
        models=model_names,
        services=service_names,
        requests=request_names,
        deep=deep
    )
    views = scan_views()
    routes = scan_routes()
    
    controllers = filter_controllers(controllers, focus)
    models = filter_models(models, focus)
    services = filter_controllers(services, focus)
    views = filter_by_path(views, focus)
    routes = filter_routes(routes, focus)
    
    shared_context = {
        "database": build_database_snapshot(migrations),
        "disks": scan_disk(),
    }
    
    if focus:
        shared_context = {
                "database": f"See {config.ROOT.name}_context_file",
                "disks": f"See {config.ROOT.name}_context_file",
            }
    
    
    not_showed_context = {
        "project": {
            "packages": {
                "composer": scan_composer_packages(),
                "frontend": scan_frontend_packages(),
            }
        },
        "controllers": controllers,
        "models": models,
        "services": services,
        "database": build_database_snapshot(migrations),
        "routes": routes,
    }
    
    context = {
        "project": {
            "name": config.ROOT.name,
            "root": str(config.ROOT),
            "project_summary": None,
        },
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "context_mode": "focus" if focus else "full",
        "focus": focus,
        
        "controllers": controllers,
        "models": models,
        "services": services,
        "views": views,
        "routes": routes,
        
        "shared_context": shared_context,
    }
    
    context["project"]["project_summary"] = build_project_summary(not_showed_context)
    
    project = str(f"{config.ROOT.name}_{focus}_context.json" if focus else f"{config.ROOT.name}_project_context.json")
    output_file = config.ROOT / project
    
    output_file.write_text(
        json.dumps(context, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Laravel context geschreven naar: {output_file}")

if __name__ == "__main__":
    main()