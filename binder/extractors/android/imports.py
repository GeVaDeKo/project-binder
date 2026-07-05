import re

def extract_imports(text):
    return sorted(set(
        re.findall(r'^\s*import\s+([A-Za-z0-9_.*]+)', text, re.MULTILINE)
    ))