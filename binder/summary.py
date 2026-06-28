from binder.packages import detect_laravel_version, detect_php_version, detect_features

# Kijkt naar composer packages, frontend packages (.env), database snapshot en routes
def build_project_summary(context: dict) -> dict:
    composer = context["project"]["packages"]["composer"]
    frontend = context["project"]["packages"]["frontend"]
    
    return {
        "framework": {
            "laravel": detect_laravel_version(composer),
            "php": detect_php_version(composer)
        },
        
        "features": detect_features(
            composer,
            frontend
        ),
        
        "statistics": {
            "controllers": len(context["controllers"]),
            "models": len(context["models"]),
            "services": len(context["services"]),
            "routes": sum(
                r["route_count"]
                for r in context["routes"]
            ),
            "tables": len(context["database"])
        }
    }