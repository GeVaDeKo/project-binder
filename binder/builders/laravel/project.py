from binder.summary import build_project_summary
from binder.packages import (
    scan_composer_packages,
    scan_frontend_packages,
)

def build_laravel_project_summary(scan):
    return build_project_summary({
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
    