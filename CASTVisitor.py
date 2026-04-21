from CParserVisitor import CParserVisitor
from CParser import CParser
from ast_nodes import *


class CASTVisitor(CParserVisitor):

    # ================= PROGRAM =================

    def visitProgram(self, ctx):
        elements = []
        for child in ctx.getChildren():
            node = self.visit(child)
            if node:
                elements.append(node)
        return Program(elements)

    # ================= PREPROCESSOR =================

    def visitPreprocessor(self, ctx):
        if ctx.INCLUDE():
            return Include(ctx.HEADER().getText())
        if ctx.DEFINE():
            name = ctx.IDENTIFIER().getText()
            value = self.visit(ctx.expression()) if ctx.expression() else None
            return Define(name, value)

    # ================= FUNCTION =================

    def visitFunctionDef(self, ctx):
        return_type = Type(ctx.type().getText())
        name = ctx.IDENTIFIER().getText()

        params = []
        if ctx.parameterList():
            for p in ctx.parameterList().parameter():
                param_type = Type(p.type().getText())
                param_name = p.IDENTIFIER().getText()
                params.append(Parameter(param_type, param_name))

        body = self.visit(ctx.compoundStmt())

        return FunctionDef(return_type, name, params, body)

    # ================= DECLARATION =================

    def visitDeclaration(self, ctx):
        type_node = Type(ctx.type().getText())
        declarators = []

        for d in ctx.declaratorList().declarator():
            name = d.IDENTIFIER().getText()
            init = self.visit(d.expression()) if d.expression() else None
            declarators.append(VariableDeclarator(name, init))

        return VarDeclaration(type_node, declarators)

    # ================= BLOCK =================

    def visitCompoundStmt(self, ctx):
        statements = []
        for s in ctx.statement():
            statements.append(self.visit(s))
        return Block(statements)

    # ================= STATEMENTS =================

    def visitSelectionStmt(self, ctx):
        condition = self.visit(ctx.expression())
        then_branch = self.visit(ctx.statement(0))
        else_branch = self.visit(ctx.statement(1)) if ctx.ELSE() else None
        return If(condition, then_branch, else_branch)

    def visitIterationStmt(self, ctx):
        if ctx.WHILE():
            return While(self.visit(ctx.expression()),
                         self.visit(ctx.statement()))
        if ctx.FOR():
            return For(
                self.visit(ctx.expression(0)) if ctx.expression(0) else None,
                self.visit(ctx.expression(1)) if ctx.expression(1) else None,
                self.visit(ctx.expression(2)) if ctx.expression(2) else None,
                self.visit(ctx.statement())
            )

    def visitJumpStmt(self, ctx):
        if ctx.RETURN():
            return Return(self.visit(ctx.expression()) if ctx.expression() else None)

    # ================= EXPRESSIONS =================

    def visitAssignment(self, ctx):
        if ctx.ASSIGN():
            return Assignment(
                self.visit(ctx.logicalOr()),
                self.visit(ctx.assignment())
            )
        return self.visit(ctx.logicalOr())

    def visitAdditive(self, ctx):
        if len(ctx.children) == 1:
            return self.visit(ctx.multiplicative(0))

        left = self.visit(ctx.multiplicative(0))
        for i in range(1, len(ctx.multiplicative())):
            op = ctx.getChild(2*i-1).getText()
            right = self.visit(ctx.multiplicative(i))
            left = BinaryOp(left, op, right)
        return left

    def visitMultiplicative(self, ctx):
        if len(ctx.children) == 1:
            return self.visit(ctx.unary(0))

        left = self.visit(ctx.unary(0))
        for i in range(1, len(ctx.unary())):
            op = ctx.getChild(2*i-1).getText()
            right = self.visit(ctx.unary(i))
            left = BinaryOp(left, op, right)
        return left

    def visitPrimary(self, ctx):
        if ctx.IDENTIFIER():
            return Variable(ctx.getText())
        if ctx.INTEGER():
            return Literal(ctx.getText())
        if ctx.STRING():
            return Literal(ctx.getText())
        if ctx.expression():
            return self.visit(ctx.expression())
