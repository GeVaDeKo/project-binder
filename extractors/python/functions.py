import ast

def get_python_args(node):
    return [arg.arg for arg in node.args.args]

def get_python_returns(function_node):
    returns = []
    
    for node in ast.walk(function_node):
        if isinstance(node, ast.Return):
            if node.value is None:
                returns.append(None)
            else:
                try:
                    returns.append(ast.unparse(node.value))
                except Exception:
                    returns.append("unknown")
                    
    return returns