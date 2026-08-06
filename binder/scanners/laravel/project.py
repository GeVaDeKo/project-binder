from binder.scanners.laravel.migrations import scan_migrations
from binder.scanners.laravel.php import scan_php_directory, collect_class_names
from binder.scanners.laravel.models import scan_models
from binder.scanners.laravel.services import scan_services
from binder.scanners.laravel.routes import scan_routes
from binder.scanners.laravel.classes import scan_custom_classes
from binder.scanners.laravel.views import scan_views
from binder.scanners.laravel.disks import scan_disk

from binder.database import build_database_snapshot
from binder.analyzers.context_graph import build_context_graph

def scan_laravel_project(focus=None):
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
    custom_classes = scan_custom_classes(
        models=model_names,
        services=services_names,
        requests=request_names,
        deep=deep,
    )
    
    database = build_database_snapshot(migrations)
    disks = scan_disk()
    context_graph = build_context_graph(database, models)
    
    return {
        "custom_classes": custom_classes,
        "controllers": controllers,
        "models": models,
        "services": services,
        "views": views,
        "routes": routes,
        "database": database,
        "disks": disks,
        "context_graph": context_graph,
    }