PAIRS = {
    "{": "}",
    "(": ")",
    "<": ">",
    "[": "]",
}

# Zoekt naar het einde van een "method" als de teller op -1 staat is het einde van een method behaald
def find_matching(text: str, open_index: int) -> int:
    open_char = text[open_index]
    close_char = PAIRS.get(open_char)
    
    if close_char is None:
        return -1
    
    depth = 0
    
    for i in range(open_index, len(text)):
        char = text[i]
        
        if char == open_char:
            depth += 1
            
        elif char == close_char:
            depth -= 1
            
            if depth == 0:
                return i
    
    return -1