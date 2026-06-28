#!/usr/bin/env python3

from datetime import datetime
import json, sys
import binder.config as config

from binder.files import collect_class_names

# Scanners
from binder.scanners.php import scan_php_directory
from binder.scanners.migrations import scan_migrations
from binder.scanners.models import scan_models
from binder.scanners.routes import scan_routes
from binder.scanners.views import scan_views
from binder.scanners.disks import scan_disk

from binder.database import build_database_snapshot
from binder.summary import build_project_summary
from binder.packages import (
    scan_composer_packages,
    scan_frontend_packages,
)

def main():
    if len(sys.argv) < 2:
        print("Gebruik: python project_scanner.py /pad/naar/jouw/project")
        sys.exit(1)
    
    config.set_root(sys.argv[1])
    
    migrations = scan_migrations()
    
    # Bepaal de mappen voor "models", "services" en "requests"
    model_names = collect_class_names("app/Models")
    service_names = collect_class_names("app/Services")
    request_names = collect_class_names("app/Http/Requests")
    controllers = scan_php_directory(
        "app/Http/Controllers",
        models=model_names,
        services=service_names,
        requests=request_names
    )
    services = scan_php_directory(
        "app/Services",
        models=model_names,
        services=service_names,
        requests=request_names
    )
    
    
    not_showed_context = {
        "project": {
            "packages": {
                "composer": scan_composer_packages(),
                "frontend": scan_frontend_packages(),
            }
        },
        "controllers": controllers,
        "models": scan_models(),
        "services": services,
        "database": build_database_snapshot(migrations),
        "routes": scan_routes(),
    }
    
    context = {
        "project": {
            "name": config.ROOT.name,
            "root": str(config.ROOT),
            "project_summary": None,
        },
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        
        "controllers": controllers,
        "models": scan_models(),
        "services": services,
        "views": scan_views(),
        "routes": scan_routes(),
        "database": build_database_snapshot(migrations),
        "disks": scan_disk(),
    }
    
    context["project"]["project_summary"] = build_project_summary(not_showed_context)
    
    project = str(config.ROOT.name)
    output_file = config.ROOT / f"{project}_project_context.json"
    
    output_file.write_text(
        json.dumps(context, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Laravel context geschreven naar: {output_file}")

if __name__ == "__main__":
    main()