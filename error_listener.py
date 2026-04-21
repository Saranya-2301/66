from antlr4.error.ErrorListener import ErrorListener

class CustomErrorListener(ErrorListener):

    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol,
                    line, column, msg, e):
        error_message = f"Syntax Error at Line {line}:{column} -> {msg}"
        self.errors.append(error_message)
        print(error_message)