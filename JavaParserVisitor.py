# Generated from JavaParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser

# This class defines a complete generic visitor for a parse tree produced by JavaParser.

class JavaParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JavaParser#program.
    def visitProgram(self, ctx:JavaParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#packageDecl.
    def visitPackageDecl(self, ctx:JavaParser.PackageDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#importDecl.
    def visitImportDecl(self, ctx:JavaParser.ImportDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#qualifiedName.
    def visitQualifiedName(self, ctx:JavaParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classDecl.
    def visitClassDecl(self, ctx:JavaParser.ClassDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#modifier.
    def visitModifier(self, ctx:JavaParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classBody.
    def visitClassBody(self, ctx:JavaParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#fieldDecl.
    def visitFieldDecl(self, ctx:JavaParser.FieldDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#declaratorList.
    def visitDeclaratorList(self, ctx:JavaParser.DeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#declarator.
    def visitDeclarator(self, ctx:JavaParser.DeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodDecl.
    def visitMethodDecl(self, ctx:JavaParser.MethodDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#parameterList.
    def visitParameterList(self, ctx:JavaParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#parameter.
    def visitParameter(self, ctx:JavaParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#type.
    def visitType(self, ctx:JavaParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#block.
    def visitBlock(self, ctx:JavaParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#statement.
    def visitStatement(self, ctx:JavaParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expressionStmt.
    def visitExpressionStmt(self, ctx:JavaParser.ExpressionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#selectionStmt.
    def visitSelectionStmt(self, ctx:JavaParser.SelectionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#iterationStmt.
    def visitIterationStmt(self, ctx:JavaParser.IterationStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#jumpStmt.
    def visitJumpStmt(self, ctx:JavaParser.JumpStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#tryStmt.
    def visitTryStmt(self, ctx:JavaParser.TryStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expression.
    def visitExpression(self, ctx:JavaParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#assignment.
    def visitAssignment(self, ctx:JavaParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#logicalOr.
    def visitLogicalOr(self, ctx:JavaParser.LogicalOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#logicalAnd.
    def visitLogicalAnd(self, ctx:JavaParser.LogicalAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#equality.
    def visitEquality(self, ctx:JavaParser.EqualityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#relational.
    def visitRelational(self, ctx:JavaParser.RelationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#additive.
    def visitAdditive(self, ctx:JavaParser.AdditiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#multiplicative.
    def visitMultiplicative(self, ctx:JavaParser.MultiplicativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unary.
    def visitUnary(self, ctx:JavaParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#primary.
    def visitPrimary(self, ctx:JavaParser.PrimaryContext):
        return self.visitChildren(ctx)



del JavaParser