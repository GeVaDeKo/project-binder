import binder.config as config

from binder.files import should_skip, read_file
from binder.metrics import count_lines
from binder.warnings import detect_warnings

from binder.extractors.android.package import extract_package
from binder.extractors.android.imports import extract_imports
from binder.extractors.android.declarations import extract_declarations
from binder.extractors.android.methods import extract_methods
from binder.extractors.android.comments import strip_android_comments, collect_android_comments

ANDROID_EXTENSIONS = {".kt", ".java"}

def scan_android_files():
    results = []
    
    for file in config.ROOT.rglob("*"):
        if not file.is_file():
            continue
        
        if should_skip(file):
            continue
        
        if file.suffix not in ANDROID_EXTENSIONS:
            continue
        
        text = read_file(file)
        relative_path = str(file.relative_to(config.ROOT)).replace("\\", "/")
        
        comments = collect_android_comments(text)
        clean_text = strip_android_comments(text)
        methods = extract_methods(clean_text, comments)
        
        results.append({
            "path": relative_path,
            "package": extract_package(text),
            "comments": comments,
            "imports": extract_imports(text),
            "declarations": extract_declarations(text),
            "methods": methods,
            "extension": file.suffix,
            "metrics": count_lines(text),
            "warnings": detect_warnings(relative_path, text),
        })
    
    return results