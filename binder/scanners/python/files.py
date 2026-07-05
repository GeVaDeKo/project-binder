import ast
import binder.config as config

from binder.files import should_skip, read_file
from binder.metrics import count_lines
from binder.warnings import detect_warnings

# Exctractors
from binder.extractors.python.imports import get_python_imports
from binder.extractors.python.functions import get_python_args, get_python_returns
from binder.extractors.python.comments import collect_python_comments, comments_above

def scan_python_files():
    results = []
    
    for file in config.ROOT.rglob("*.py"):
        if should_skip(file):
            continue
        
        text = read_file(file)
        relative_path = str(file.relative_to(config.ROOT)).replace("\\", "/")
        
        try:
            tree = ast.parse(text)
        except SyntaxError:
            results.append({
                "path": relative_path,
                "extension": ".py",
                "error": "SyntaxError",
                "imports": [],
                "classes": [],
                "functions": [],
            })
            continue
        
        comments = collect_python_comments(file)
        
        functions = []
        classes = []
        
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append({
                    "name": node.name,
                    "type": "async_function" if isinstance(node, ast.AsyncFunctionDef) else "function",
                    "line": node.lineno,
                    "arguments": get_python_args(node),
                    "docstring": ast.get_docstring(node),
                    "comments": comments_above(node.lineno, comments),
                    "returns": get_python_returns(node)
                })
            
            elif isinstance(node, ast.ClassDef):
                methods = []
            
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append({
                            "name": item.name,
                            "type": "async_method" if isinstance(item, ast.AsyncFunctionDef) else "method",
                            "line": item.lineno,
                            "arguments": get_python_args(item),
                            "docstring": ast.get_docstring(item),
                            "comments": comments_above(item.lineno, comments),
                            "returns": get_python_returns(item)
                        })
            
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "comments": comments_above(node.lineno, comments),
                    "methods": methods
                })
            
        results.append({
            "path": relative_path,
            "extension": ".py",
            "metrics": count_lines(text),
            "warnings": detect_warnings(relative_path, text),
            "imports": get_python_imports(tree),
            "classes": classes,
            "functions": functions,
        })
    
    return results