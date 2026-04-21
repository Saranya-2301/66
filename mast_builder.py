class ASTNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"{self.name} -> {self.children}"