# Kijkt naar het aantal "lines" en returned metrics
def count_lines(text: str) -> dict:
    lines = text.splitlines()
    code = [l for l in lines if l.strip() and not l.strip().startswith(("//", "#", "{{--"))]
    comments = [l for l in lines if l.strip().startswith(("//", "#", "{{--"))]
    
    return {
        "total_lines": len(lines),
        "code_lines": len(code),
        "comment_lines": len(comments),
        "empty_lines": len(lines) - len([l for l in lines if l.strip()])
    }