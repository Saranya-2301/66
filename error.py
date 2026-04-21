import re

def classify_error(e, code):
    """
    Returns:
    error_type, explanation, corrected_code, line, column
    """

    error_type = type(e).__name__

    error_map = {
        "SyntaxError": "Invalid syntax. Possible missing operator, operand, or bracket.",
        "ZeroDivisionError": "Division by zero is not allowed.",
        "NameError": "Variable used before assignment.",
        "TypeError": "Invalid operation between incompatible types.",
        "ValueError": "Invalid value provided.",
        "IndexError": "Index out of range.",
        "KeyError": "Key not found in dictionary.",
        "AttributeError": "Object has no such attribute."
    }

    explanation = error_map.get(error_type, "Unknown error occurred")

    line = None
    column = None

    if isinstance(e, SyntaxError):
        line = e.lineno
        column = e.offset
    else:
        line = 1
        column = None

    corrected_code = auto_correct(code, error_type)

    return error_type, explanation, corrected_code, line, column


def auto_correct(code, error_type):
    """
    Rule-based auto correction
    """

    if not code:
        return None

    corrected = code.strip()

    if error_type == "SyntaxError":

        if re.search(r'[\+\-\*/]\s*$', corrected):
            corrected += " 0"

        elif re.search(r'\b\d+\s+\d+\b', corrected):
            corrected = re.sub(r'(\d+)\s+(\d+)', r'\1 + \2', corrected)

        if corrected.count('(') > corrected.count(')'):
            corrected += ')' * (corrected.count('(') - corrected.count(')'))

        corrected = re.sub(r'[^0-9a-zA-Z\+\-\*/\=\(\)\s]', '', corrected)

    elif error_type == "ZeroDivisionError":
        corrected = corrected.replace('/0', '/1')

    return corrected
