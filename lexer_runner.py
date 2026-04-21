from antlr4 import *

def run_lexer(language, file_path):

    input_stream = FileStream(file_path)

    if language == "C":
        from CLexer import CLexer as Lexer

    elif language == "CPP":
        from CPPLexer import CPPLexer as Lexer

    elif language == "Java":
        from JavaLexer import JavaLexer as Lexer

    else:
        print("Unsupported language")
        return

    lexer = Lexer(input_stream)
    tokens = CommonTokenStream(lexer)
    tokens.fill()

    print("\nTOKENS:\n")

    for token in tokens.tokens:
        print(token)