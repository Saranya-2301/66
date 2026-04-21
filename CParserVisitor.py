# Generated from CParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete generic visitor for a parse tree produced by CParser.

class CParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CParser#program.
    def visitProgram(self, ctx:CParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#preprocessor.
    def visitPreprocessor(self, ctx:CParser.PreprocessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declaration.
    def visitDeclaration(self, ctx:CParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declaratorList.
    def visitDeclaratorList(self, ctx:CParser.DeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declarator.
    def visitDeclarator(self, ctx:CParser.DeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionDef.
    def visitFunctionDef(self, ctx:CParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameterList.
    def visitParameterList(self, ctx:CParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameter.
    def visitParameter(self, ctx:CParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#type.
    def visitType(self, ctx:CParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compoundStmt.
    def visitCompoundStmt(self, ctx:CParser.CompoundStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expressionStmt.
    def visitExpressionStmt(self, ctx:CParser.ExpressionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#selectionStmt.
    def visitSelectionStmt(self, ctx:CParser.SelectionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#iterationStmt.
    def visitIterationStmt(self, ctx:CParser.IterationStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#jumpStmt.
    def visitJumpStmt(self, ctx:CParser.JumpStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx:CParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignment.
    def visitAssignment(self, ctx:CParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalOr.
    def visitLogicalOr(self, ctx:CParser.LogicalOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalAnd.
    def visitLogicalAnd(self, ctx:CParser.LogicalAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#equality.
    def visitEquality(self, ctx:CParser.EqualityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#relational.
    def visitRelational(self, ctx:CParser.RelationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#additive.
    def visitAdditive(self, ctx:CParser.AdditiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#multiplicative.
    def visitMultiplicative(self, ctx:CParser.MultiplicativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unary.
    def visitUnary(self, ctx:CParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#primary.
    def visitPrimary(self, ctx:CParser.PrimaryContext):
        return self.visitChildren(ctx)



del CParser