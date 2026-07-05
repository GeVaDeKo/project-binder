import re

from binder.parsers.delimiters import find_matching
from binder.parsers.parsers import skip_spaces
from binder.extractors.android.comments import collect_android_comments, comments_above

def extract_methods(text, comments=None):
    methods = []
    
    pattern = re.compile(
        r"(?P<annotations>(?:^\s*@\w+(?:\([^)]*\))?\s*\n)*)"
        r"^\s*(?P<visibility>private|public|internal|protected)?\s*"
        r"(?P<suspend>suspend\s+)?"
        r"fun\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*",
        re.MULTILINE,
    )
    
    for match in pattern.finditer(text):
        name = match.group("name")
        start = match.end()
        paren_start = text.find("(", match.end("name"))
        if paren_start == -1:
            continue
        
        paren_end = find_matching(text, paren_start)
        if paren_end == -1:
            continue
        
        arguments = text[paren_start + 1:paren_end]
        after_args_index = skip_spaces(text, paren_end + 1)
        
        returns = "Unit"
        
        if after_args_index < len(text) and text[after_args_index] == ":":
            type_start = skip_spaces(text, after_args_index + 1)
            returns = read_kotlin_type(text, type_start)
        
        body = None
        body_type = None
        
        after_args_index = skip_spaces(
            text,
            after_args_index if returns == "Unit" else after_args_index + 1
        )
        
        brace_index = text.find("{", paren_end, paren_end + 300)
        equals_index = text.find("=", paren_end, paren_end + 300)
        
        if brace_index != -1 and (equals_index == -1 or brace_index < equals_index):
            end = find_matching(text, brace_index)
            if end != -1:
                body = text[brace_index + 1:end]
                body_type = "block"
        
        elif equals_index != -1:
            body_type = "expression"
        
        comments = comments or {}
        line_number = text[:match.start()].count("\n") + 1
        
        methods.append({
            "name": name,
            "comments": comments_above(line_number, comments),
            "visibility": match.group("visibility") or "default",
            "suspend": bool(match.group("suspend")),
            "arguments": " ".join(arguments.split()),
            "returns": returns,
            "annotations": extract_annotations(match.group("annotations") or ""),
            "body_type": body_type,
            "calls": extract_calls(body) if body else [],
        })
        
    return methods

def extract_annotations(text):
    annotations = []
    
    for raw in re.findall(r"@\w+(?:\([^)]*\))?", text):
        annotations.append(raw.strip())
    
    return annotations

def extract_calls(body):
    calls = set()
    
    for match in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", body):
        if match not in {"if", "for", "while", "when", "return"}:
            calls.add(match)
    
    return sorted(calls)

def read_kotlin_type(text, index):
    end = index
    
    while end < len(text):
        char = text[end]
        
        if char == "<":
            close = find_matching(text, end)
            if close == -1:
                break
            end = close + 1
            continue
        
        if char in {"{", "=", "\n", "\r"}:
            break
        
        end += 1
    
    return text[index:end].strip() or "Unit"