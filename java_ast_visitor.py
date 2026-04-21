from JavaParserVisitor import JavaParserVisitor
from ast_nodes import *


class JavaASTVisitor(JavaParserVisitor):

    def visitProgram(self, ctx):
        elements = []
        if ctx.packageDecl():
            elements.append(self.visit(ctx.packageDecl()))

        for imp in ctx.importDecl():
            elements.append(self.visit(imp))

        for c in ctx.classDecl():
            elements.append(self.visit(c))

        return Program(elements)

    def visitPackageDecl(self, ctx):
        return PackageDecl(ctx.qualifiedName().getText())

    def visitImportDecl(self, ctx):
        name = ctx.qualifiedName().getText()
        wildcard = True if ctx.MUL() else False
        return ImportDecl(name, wildcard)

    def visitClassDecl(self, ctx):
        name = ctx.IDENTIFIER().getText()
        members = []
        for m in ctx.classBody():
            node = self.visit(m)
            if node:
                members.append(node)
        return ClassDecl(name, members=members)

    def visitMethodDecl(self, ctx):
        return_type = Type(ctx.type().getText())
        name = ctx.IDENTIFIER().getText()
        body = self.visit(ctx.block())
        return MethodDecl(return_type, name, [], body)

    def visitFieldDecl(self, ctx):
        type_node = Type(ctx.type().getText())
        name = ctx.declaratorList().declarator(0).IDENTIFIER().getText()
        return FieldDecl(type_node, name)

    def visitBlock(self, ctx):
        statements = []
        for s in ctx.statement():
            statements.append(self.visit(s))
        return Block(statements)
