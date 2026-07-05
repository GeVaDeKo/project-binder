def camel_to_snake(name: str) -> str:
    result = ""

    for index, char in enumerate(name):
        if char.isupper() and index > 0:
            result += "_"
        result += char.lower()

    return result

def guess_laravel_table(model_name: str) -> str:
    snake = camel_to_snake(model_name)

    if snake.endswith("y"):
        return snake[:-1] + "ies"

    if snake.endswith(("s", "x", "z", "ch", "sh")):
        return snake + "es"

    return snake + "s"