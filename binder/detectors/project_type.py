from binder.detectors.laravel import is_laravel_project
from binder.detectors.python import is_python_project

def detect_project_type(root):
    has_laravel = is_laravel_project(root)
    has_python = is_python_project(root)
    
    if has_laravel and has_python:
        return "mixed"
    
    if has_laravel:
        return "laravel"
    
    if has_python:
        return "python"
    
    return "unknown"