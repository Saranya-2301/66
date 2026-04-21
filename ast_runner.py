import sys
from antlr4 import *

# C
try:
    from CLexer  import CLexer
    from CParser import CParser
except ImportError:
    CLexer = CParser = None

# C++
try:
    from CPPLexer  import CPPLexer
    from CPPParser import CPPParser
except ImportError:
    CPPLexer = CPPParser = None

# Java
try:
    from JavaLexer  import JavaLexer
    from JavaParser import JavaParser
except ImportError:
    JavaLexer = JavaParser = None


# Visual Tree Printer (preorder)

def print_tree(node, prefix="", is_last=True, lines=None):
    if lines is None:
        lines = []

    connector  = "└── " if is_last else "├── "
    child_pipe = "    " if is_last else "│   "

    if isinstance(node, TerminalNode):
        text = node.getText()
        if text == '<EOF>':
            return lines
        lines.append(f"{prefix}{connector}{text}")
    else:
        rule_name = type(node).__name__
        lines.append(f"{prefix}{connector}{rule_name}")

        child_count = node.getChildCount()
        for i in range(child_count):
            child   = node.getChild(i)
            is_last_child = (i == child_count - 1)
            print_tree(
                child,
                prefix + child_pipe,
                is_last_child,
                lines
            )

    return lines


def print_ast_tree(root, lines=None):
    if lines is None:
        lines = []

    if root is None:
        return lines

    lines.append(type(root).__name__)

    child_count = root.getChildCount()
    for i in range(child_count):
        child         = root.getChild(i)
        is_last_child = (i == child_count - 1)
        print_tree(child, "", is_last_child, lines)

    return lines


# Build parse tree
def build_tree(language, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"[AST] File not found: {file_path}")
        return None

    stream = InputStream(code)

    if language == 'C':
        if not CLexer:
            print("[AST] C lexer/parser missing.")
            print("      Run: java -jar antlr*.jar -Dlanguage=Python3 -visitor C.g4")
            return None
        tokens = CommonTokenStream(CLexer(stream))
        parser = CParser(tokens)
        return parser.program()

    elif language in ('CPP', 'C++'):
        if not CPPLexer:
            print("[AST] CPP lexer/parser missing.")
            print("      Run: java -jar antlr*.jar -Dlanguage=Python3 -visitor CPP.g4")
            return None
        tokens = CommonTokenStream(CPPLexer(stream))
        parser = CPPParser(tokens)
        return parser.program()

    elif language == 'Java':
        if not JavaLexer:
            print("[AST] Java lexer/parser missing.")
            print("      Run: java -jar antlr*.jar -Dlanguage=Python3 -visitor Java.g4")
            return None
        tokens = CommonTokenStream(JavaLexer(stream))
        parser = JavaParser(tokens)
        return parser.program()

    else:
        print(f"[AST] Unsupported language: {language}")
        return None


# Show AST for one language
def show_ast(language, file_path):
    print("\n" + "=" * 60)
    print(f"  AST [ {language} ]  —  Preorder Visual Tree")
    print(f"  File: {file_path}")
    print("=" * 60)

    tree = build_tree(language, file_path)
    if tree is None:
        print(f"[AST] Failed to build tree for {language}")
        print("=" * 60)
        return

    lines = print_ast_tree(tree)

    for line in lines:
        print(line)

    print("=" * 60)
    print(f"  Total nodes : {len(lines)}")
    print("=" * 60)


def run_ast(language, file_path):
    """
    Called from main.py:

        from ast_runner import run_ast
        run_ast(language, file_path)
    """
    show_ast(language, file_path)


def run_all_ast(c_file=None, cpp_file=None, java_file=None):
    """
    Called to generate AST for all 3 languages:

        from ast_runner import run_all_ast
        run_all_ast(
            c_file    = "hello.c",
            cpp_file  = "hello.cpp",
            java_file = "Hello.java"
        )
    """
    print("\n" + "#" * 60)
    print("    GENERATING VISUAL AST FOR ALL 3 LANGUAGES")
    print("#" * 60)

    if c_file:
        show_ast('C', c_file)
    else:
        print("\n[AST] C    — skipped (no file provided)")

    if cpp_file:
        show_ast('CPP', cpp_file)
    else:
        print("\n[AST] CPP  — skipped (no file provided)")

    if java_file:
        show_ast('Java', java_file)
    else:
        print("\n[AST] Java — skipped (no file provided)")

    print("\n" + "#" * 60)
    print("    ALL AST GENERATION COMPLETE")
    print("#" * 60)


if __name__ == "__main__":

    if len(sys.argv) == 5 and sys.argv[1].upper() == 'ALL':
        run_all_ast(
            c_file    = sys.argv[2],
            cpp_file  = sys.argv[3],
            java_file = sys.argv[4]
        )

    elif len(sys.argv) == 3:
        run_ast(sys.argv[1], sys.argv[2])

    else:
        print()
        print("=" * 55)
        print("  ast_runner.py — Usage")
        print("=" * 55)
        print("  Single:")
        print("    py ast_runner.py C      hello.c")
        print("    py ast_runner.py CPP    hello.cpp")
        print("    py ast_runner.py Java   Hello.java")
        print()
        print("  All 3 at once:")
        print("    py ast_runner.py ALL hello.c hello.cpp Hello.java")
        print("=" * 55)
        sys.exit(1)
