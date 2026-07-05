from binder.focus import (
    filter_by_path,
)

def build_python_context(scan):
    return {
        "python": scan["python"],
    }

def build_python_focus_context(scan, focus):
    return {
        "python": filter_by_path(scan["python"], focus)
    }