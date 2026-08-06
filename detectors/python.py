from binder.files import should_skip

def is_python_project(root):
    markers = [
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "setup.cfg",
        "Pipfile",
    ]
    
    if any((root / marker).exists() for marker in markers):
        return True
    
    return any(
        not should_skip(file)
        for file in root.rglob("*.py")
        if file.is_file()
    )