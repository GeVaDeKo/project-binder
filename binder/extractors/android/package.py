import re

def extract_package(text):
    match = re.search(r'^\s*package\s+([A-Za-z0-9_.]+)', text, re.MULTILINE)
    return match.group(1) if match else None