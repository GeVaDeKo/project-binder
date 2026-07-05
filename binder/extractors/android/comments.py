def collect_android_comments(text: str) -> dict:
    comments = {}

    lines = text.splitlines()

    in_block = False
    block_start = None
    block_lines = []

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()

        if in_block:
            cleaned = stripped.lstrip("*").strip()

            if "*/" in cleaned:
                cleaned = cleaned.replace("*/", "").strip()
                if cleaned:
                    block_lines.append(cleaned)

                comments[block_start] = block_lines
                in_block = False
                block_start = None
                block_lines = []
                continue

            if cleaned:
                block_lines.append(cleaned)

            continue

        if stripped.startswith("//"):
            comments.setdefault(index, []).append(stripped[2:].strip())

        elif stripped.startswith("/*"):
            in_block = True
            block_start = index

            cleaned = (
                stripped
                .replace("/**", "")
                .replace("/*", "")
                .strip()
                .lstrip("*")
                .strip()
            )

            if "*/" in cleaned:
                cleaned = cleaned.replace("*/", "").strip()
                if cleaned:
                    comments.setdefault(index, []).append(cleaned)
                in_block = False
                block_start = None
            elif cleaned:
                block_lines.append(cleaned)

    return comments


def comments_above(line_number: int, comments: dict) -> list:
    found = []
    line = line_number - 1

    while line in comments:
        found = comments[line] + found
        line -= 1

    return found

def strip_android_comments(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    in_block = False

    for line in lines:
        stripped = line.strip()

        if in_block:
            if "*/" in stripped:
                in_block = False
            cleaned.append("")
            continue

        if stripped.startswith("/*"):
            if "*/" not in stripped:
                in_block = True
            cleaned.append("")
            continue

        if "//" in line:
            line = line[:line.index("//")]

        cleaned.append(line)

    return "\n".join(cleaned)