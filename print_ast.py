# ============================================================
# AST Pretty Printer
# Works with unified ast_nodes.py
# ============================================================

def print_ast(node, indent=0):
    """
    Generic AST printer.
    Recursively prints all ASTNode objects.
    """

    if node is None:
        return

    spacing = "  " * indent
    node_name = node.__class__.__name__

    print(f"{spacing}{node_name}")

    for attr, value in vars(node).items():

        if isinstance(value, list):
            print(f"{spacing}  {attr}:")
            for item in value:
                if hasattr(item, "__dict__"):
                    print_ast(item, indent + 2)
                else:
                    print(f"{spacing}    {item}")

        elif hasattr(value, "__dict__"):
            print(f"{spacing}  {attr}:")
            print_ast(value, indent + 2)

        else:
            print(f"{spacing}  {attr}: {value}")
