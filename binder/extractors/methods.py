import re
from binder.extractors.dependencies import extract_typed_dependencies
from binder.parsers import find_matching_brace

# Doorzoekt het bestand op "methods" (private|public function)
def find_php_methods(text, models=None, services=None, requests=None, deep=False) -> list:
    methods = []
    
    models = models or set()
    services = services or set()
    requests = requests or set()
    
    signature_pattern = re.compile(
        r"(public|protected|private)\s+function\s+(\w+)\s*\((.*?)\)\s*(?::\s*[^{]+)?\s*\{",
        re.DOTALL
    )
    
    for match in signature_pattern.finditer(text):
        arguments = " ".join(match.group(3).split())
        deps = extract_typed_dependencies(arguments, models, services, requests)
        
        open_brace_index = match.end() - 1
        close_brace_index = find_matching_brace(text, open_brace_index)
        
        if close_brace_index == -1:
            continue
        
        body = text[open_brace_index + 1:close_brace_index]
        
        entry = {
            "visibility": match.group(1),
            "name": match.group(2),
            "arguments": arguments,
            **deps
        }
        
        if deep:
            entry["returns"] = extract_returns(body)
            entry["variables_used"] = extract_variables(body)
            entry["calls"] = extract_calls(body)
        
        methods.append(entry)

    return methods

# Zoekt naar returns en kan ze tonen met een "--focus" flag
def extract_returns(body: str) -> list:
    return [
        " ".join(match.split())
        for match in re.findall(r"return\s+(.+?);", body, re.DOTALL)
    ]

# Zoekt naar $variables en kan ze tonen met een "--focus" flag
def extract_variables(body: str) -> list:
    return sorted(set(
        re.findall(r"\$[a-zA-Z_][a-zA-Z0-9_]*", body)
    ))

def extract_calls(body:str) -> list:
    calls = []
    
    calls += re.findall(
        r"(\$[a-zA-Z_][a-zA-Z0-9_]*->\w+)",
        body
    )
    
    calls += re.findall(
        r"([A-Z][A-Za-z0-9_]*::\w+)",
        body
    )
    
    return sorted(set(calls))