from antlr4 import *

def run_parser(language, file_path):

    input_stream = FileStream(file_path)

    if language == "C":
        from CLexer import CLexer
        from CParser import CParser
        lexer = CLexer(input_stream)
        parser_class = CParser

    elif language == "CPP":
        from CPPLexer import CPPLexer
        from CPPParser import CPPParser
        lexer = CPPLexer(input_stream)
        parser_class = CPPParser

    elif language == "Java":
        from JavaLexer import JavaLexer
        from JavaParser import JavaParser
        lexer = JavaLexer(input_stream)
        parser_class = JavaParser

    else:
        print("Unsupported language")
        return

    token_stream = CommonTokenStream(lexer)
    parser = parser_class(token_stream)

    tree = parser.program()  
    print("\nPARSE TREE:\n")
    print(tree.toStringTree(recog=parser))