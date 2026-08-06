import re

def extract_declarations(text):
    pattern = r'^\s*(data\s+class|class|object|interface|enum\s+class)\s+([A-Za-z0-9_]+)'
    return [
        {"type": kind, "name": name}
        for kind, name in re.findall(pattern, text, re.MULTILINE)
    ]