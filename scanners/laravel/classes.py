import binder.config as config

from binder.files import should_skip
from binder.scanners.laravel.php import scan_php_directory

KNOWN_APP_DIRECTORIES = {
    "Http",
    "Models",
    "Services"
}

def scan_custom_classes(
    models=None,
    services=None,
    requests=None,
    deep=False,
) -> list:
    results = []
    app_path = config.ROOT / "app"
    
    if not app_path.exists():
        return results
    
    for directory in app_path.iterdir():
        if not directory.is_dir():
            continue
        
        if should_skip(directory):
            continue
        
        if directory.name in KNOWN_APP_DIRECTORIES:
            continue
        
        classes = scan_php_directory(
            f"app/{directory.name}",
            models=models,
            services=services,
            requests=requests,
            deep=deep,
        )
        
        for entry in classes:
            entry["group"] = directory.name
            entry["category"] = classify_custom_class(
                directory.name,
                entry["path"],
            )
        
        results.extend(classes)
    
    return results

def classify_custom_class(group: str, path: str) -> str:
    normalized_group = group.lower()
    
    if normalized_group == "actions":
        return "action"
    
    if normalized_group == "jobs":
        return "job"
    
    if normalized_group == "events":
        return "event"
     
    if normalized_group == "listeners":
        return "listerner"
    
    if normalized_group == "notifications":
        return "notification"
    
    if normalized_group == "policies":
        return "policy"
    
    if normalized_group == "rules":
        return "rule"
    
    return "custom"