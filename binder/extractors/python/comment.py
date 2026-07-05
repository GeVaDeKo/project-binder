import tokenize
from pathlib import Path

def collect_python_comments(path: Path):
    comments = {}
    
    with tokenize.open(path) as f:
        tokens = tokenize.generate_tokens(f.readline)
        
        for token in tokens:
            if token.type == tokenize.COMMENT:
                line = token.start[0]
                text = token.string.lstrip("#").strip()
                comments.setdefault(line, []).append(text)
    
    return comments

def comments_above(line_number, comments):
    found = []
    line = line_number - 1
    
    while line in comments:
        found = comments[line] + found
        line -= 1
    
    return found