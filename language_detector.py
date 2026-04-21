def detect_language(filename):
    if filename.endswith(".c"):
        return "C"
    elif filename.endswith(".cpp"):
        return "CPP"
    elif filename.endswith(".java"):
        return "Java"
    else:
        return None