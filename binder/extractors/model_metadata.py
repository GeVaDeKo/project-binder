import re

def extract_model_table(text: str) -> str | None:
    match = re.search(
        r"protected\s+\$table\s*=\s*['\"]([^'\"]+)['\"]\s*;",
        text
    )

    if match:
        return match.group(1)

    return None