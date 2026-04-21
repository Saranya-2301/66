# ============================================================
# UNIFIED AST NODES
# Supports: C, C++, Java
# Designed for full grammar-level implementation
# ============================================================


# ===================== BASE =====================

class ASTNode:
    pass


# ===================== PROGRAM ROOT =====================

class Program(ASTNode):
    def __init__(self, elements):
        self.elements = elements


# ===================== PREPROCESSOR (C/C++) =====================

class Include(ASTNode):
    def __init__(self, path):
        self.path = path


class Define(ASTNode):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value


# ===================== PACKAGE / IMPORT (Java) =====================

class PackageDecl(ASTNode):
    def __init__(self, name):
        self.name = name


class ImportDecl(ASTNode):
    def __init__(self, name, wildcard=False):
        self.name = name
        self.wildcard = wildcard


# ===================== NAMESPACE (C++) =====================

class NamespaceDecl(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body


# ===================== TYPES & DECLARATIONS =====================

class Type(ASTNode):
    def __init__(self, name):
        self.name = name


class QualifiedName(ASTNode):
    def __init__(self, parts):
        self.parts = parts


class ClassDecl(ASTNode):
    def __init__(self, name, modifiers=None, extends=None, implements=None, members=None):
        self.name = name
        self.modifiers = modifiers or []
        self.extends = extends
        self.implements = implements or []
        self.members = members or []


class InterfaceDecl(ASTNode):
    def __init__(self, name, modifiers=None, extends=None, members=None):
        self.name = name
        self.modifiers = modifiers or []
        self.extends = extends or []
        self.members = members or []


class EnumDecl(ASTNode):
    def __init__(self, name, values):
        self.name = name
        self.values = values


class RecordDecl(ASTNode):
    def __init__(self, name, parameters, members):
        self.name = name
        self.parameters = parameters
        self.members = members


# ===================== FUNCTIONS =====================

class FunctionDef(ASTNode):
    def __init__(self, return_type, name, parameters, body, modifiers=None):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters or []
        self.body = body
        self.modifiers = modifiers or []


class ConstructorDecl(ASTNode):
    def __init__(self, name, parameters, body, modifiers=None):
        self.name = name
        self.parameters = parameters or []
        self.body = body
        self.modifiers = modifiers or []


class MethodDecl(ASTNode):
    def __init__(self, return_type, name, parameters, body, modifiers=None):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters or []
        self.body = body
        self.modifiers = modifiers or []


# ===================== VARIABLES =====================

class VarDeclaration(ASTNode):
    def __init__(self, type_node, declarators):
        self.type_node = type_node
        self.declarators = declarators


class VariableDeclarator(ASTNode):
    def __init__(self, name, initializer=None):
        self.name = name
        self.initializer = initializer


class FieldDecl(ASTNode):
    def __init__(self, type_node, name, value=None, modifiers=None):
        self.type_node = type_node
        self.name = name
        self.value = value
        self.modifiers = modifiers or []


class Parameter(ASTNode):
    def __init__(self, type_node, name):
        self.type_node = type_node
        self.name = name


# ===================== STATEMENTS =====================

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements or []


class ExpressionStmt(ASTNode):
    def __init__(self, expression):
        self.expression = expression


class If(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class DoWhile(ASTNode):
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition


class For(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body


class Switch(ASTNode):
    def __init__(self, expression, cases):
        self.expression = expression
        self.cases = cases


class Case(ASTNode):
    def __init__(self, label, statements):
        self.label = label
        self.statements = statements


class Try(ASTNode):
    def __init__(self, try_block, catches, finally_block=None):
        self.try_block = try_block
        self.catches = catches
        self.finally_block = finally_block


class Catch(ASTNode):
    def __init__(self, type_node, name, block):
        self.type_node = type_node
        self.name = name
        self.block = block


class Return(ASTNode):
    def __init__(self, expression=None):
        self.expression = expression


class Break(ASTNode):
    pass


class Continue(ASTNode):
    pass


# ===================== EXPRESSIONS =====================

class Assignment(ASTNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value


class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class TernaryOp(ASTNode):
    def __init__(self, condition, true_expr, false_expr):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr


class CallExpr(ASTNode):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments or []


class MemberAccess(ASTNode):
    def __init__(self, object_expr, member):
        self.object_expr = object_expr
        self.member = member


class NewExpr(ASTNode):
    def __init__(self, class_name, arguments):
        self.class_name = class_name
        self.arguments = arguments or []


class ArrayAccess(ASTNode):
    def __init__(self, array, index):
        self.array = array
        self.index = index


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name


class Literal(ASTNode):
    def __init__(self, value):
        self.value = value
