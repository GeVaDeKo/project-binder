from binder.scanners.laravel.project import scan_laravel_project
from binder.scanners.python.files import scan_python_files
from binder.scanners.android.files import scan_android_files

def scan_project(focus=None, project_type="unknown"):
    scan = {
        "project_type": project_type,
        "controllers": [],
        "models": [],
        "services": [],
        "views": [],
        "routes": [],
        "python": [],
        "database": {},
        "disks": {},
        "context_graph": {},
    }
    
    if project_type == "android":
        scan["android"] = scan_android_files()

    if project_type in ("laravel", "mixed"):
        scan.update(scan_laravel_project(focus))

    if project_type in ("python", "mixed"):
        scan["python"] = scan_python_files()

    return scan