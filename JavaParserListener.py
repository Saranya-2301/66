# Generated from JavaParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser

# This class defines a complete listener for a parse tree produced by JavaParser.
class JavaParserListener(ParseTreeListener):

    # Enter a parse tree produced by JavaParser#program.
    def enterProgram(self, ctx:JavaParser.ProgramContext):
        pass

    # Exit a parse tree produced by JavaParser#program.
    def exitProgram(self, ctx:JavaParser.ProgramContext):
        pass


    # Enter a parse tree produced by JavaParser#packageDecl.
    def enterPackageDecl(self, ctx:JavaParser.PackageDeclContext):
        pass

    # Exit a parse tree produced by JavaParser#packageDecl.
    def exitPackageDecl(self, ctx:JavaParser.PackageDeclContext):
        pass


    # Enter a parse tree produced by JavaParser#importDecl.
    def enterImportDecl(self, ctx:JavaParser.ImportDeclContext):
        pass

    # Exit a parse tree produced by JavaParser#importDecl.
    def exitImportDecl(self, ctx:JavaParser.ImportDeclContext):
        pass


    # Enter a parse tree produced by JavaParser#qualifiedName.
    def enterQualifiedName(self, ctx:JavaParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by JavaParser#qualifiedName.
    def exitQualifiedName(self, ctx:JavaParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by JavaParser#classDecl.
    def enterClassDecl(self, ctx:JavaParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by JavaParser#classDecl.
    def exitClassDecl(self, ctx:JavaParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by JavaParser#modifier.
    def enterModifier(self, ctx:JavaParser.ModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#modifier.
    def exitModifier(self, ctx:JavaParser.ModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#classBody.
    def enterClassBody(self, ctx:JavaParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#classBody.
    def exitClassBody(self, ctx:JavaParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#fieldDecl.
    def enterFieldDecl(self, ctx:JavaParser.FieldDeclContext):
        pass

    # Exit a parse tree produced by JavaParser#fieldDecl.
    def exitFieldDecl(self, ctx:JavaParser.FieldDeclContext):
        pass


    # Enter a parse tree produced by JavaParser#declaratorList.
    def enterDeclaratorList(self, ctx:JavaParser.DeclaratorListContext):
        pass

    # Exit a parse tree produced by JavaParser#declaratorList.
    def exitDeclaratorList(self, ctx:JavaParser.DeclaratorListContext):
        pass


    # Enter a parse tree produced by JavaParser#declarator.
    def enterDeclarator(self, ctx:JavaParser.DeclaratorContext):
        pass

    # Exit a parse tree produced by JavaParser#declarator.
    def exitDeclarator(self, ctx:JavaParser.DeclaratorContext):
        pass


    # Enter a parse tree produced by JavaParser#methodDecl.
    def enterMethodDecl(self, ctx:JavaParser.MethodDeclContext):
        pass

    # Exit a parse tree produced by JavaParser#methodDecl.
    def exitMethodDecl(self, ctx:JavaParser.MethodDeclContext):
        pass


    # Enter a parse tree produced by JavaParser#parameterList.
    def enterParameterList(self, ctx:JavaParser.ParameterListContext):
        pass

    # Exit a parse tree produced by JavaParser#parameterList.
    def exitParameterList(self, ctx:JavaParser.ParameterListContext):
        pass


    # Enter a parse tree produced by JavaParser#parameter.
    def enterParameter(self, ctx:JavaParser.ParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#parameter.
    def exitParameter(self, ctx:JavaParser.ParameterContext):
        pass


    # Enter a parse tree produced by JavaParser#type.
    def enterType(self, ctx:JavaParser.TypeContext):
        pass

    # Exit a parse tree produced by JavaParser#type.
    def exitType(self, ctx:JavaParser.TypeContext):
        pass


    # Enter a parse tree produced by JavaParser#block.
    def enterBlock(self, ctx:JavaParser.BlockContext):
        pass

    # Exit a parse tree produced by JavaParser#block.
    def exitBlock(self, ctx:JavaParser.BlockContext):
        pass


    # Enter a parse tree produced by JavaParser#statement.
    def enterStatement(self, ctx:JavaParser.StatementContext):
        pass

    # Exit a parse tree produced by JavaParser#statement.
    def exitStatement(self, ctx:JavaParser.StatementContext):
        pass


    # Enter a parse tree produced by JavaParser#expressionStmt.
    def enterExpressionStmt(self, ctx:JavaParser.ExpressionStmtContext):
        pass

    # Exit a parse tree produced by JavaParser#expressionStmt.
    def exitExpressionStmt(self, ctx:JavaParser.ExpressionStmtContext):
        pass


    # Enter a parse tree produced by JavaParser#selectionStmt.
    def enterSelectionStmt(self, ctx:JavaParser.SelectionStmtContext):
        pass

    # Exit a parse tree produced by JavaParser#selectionStmt.
    def exitSelectionStmt(self, ctx:JavaParser.SelectionStmtContext):
        pass


    # Enter a parse tree produced by JavaParser#iterationStmt.
    def enterIterationStmt(self, ctx:JavaParser.IterationStmtContext):
        pass

    # Exit a parse tree produced by JavaParser#iterationStmt.
    def exitIterationStmt(self, ctx:JavaParser.IterationStmtContext):
        pass


    # Enter a parse tree produced by JavaParser#jumpStmt.
    def enterJumpStmt(self, ctx:JavaParser.JumpStmtContext):
        pass

    # Exit a parse tree produced by JavaParser#jumpStmt.
    def exitJumpStmt(self, ctx:JavaParser.JumpStmtContext):
        pass


    # Enter a parse tree produced by JavaParser#tryStmt.
    def enterTryStmt(self, ctx:JavaParser.TryStmtContext):
        pass

    # Exit a parse tree produced by JavaParser#tryStmt.
    def exitTryStmt(self, ctx:JavaParser.TryStmtContext):
        pass


    # Enter a parse tree produced by JavaParser#expression.
    def enterExpression(self, ctx:JavaParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#expression.
    def exitExpression(self, ctx:JavaParser.ExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#assignment.
    def enterAssignment(self, ctx:JavaParser.AssignmentContext):
        pass

    # Exit a parse tree produced by JavaParser#assignment.
    def exitAssignment(self, ctx:JavaParser.AssignmentContext):
        pass


    # Enter a parse tree produced by JavaParser#logicalOr.
    def enterLogicalOr(self, ctx:JavaParser.LogicalOrContext):
        pass

    # Exit a parse tree produced by JavaParser#logicalOr.
    def exitLogicalOr(self, ctx:JavaParser.LogicalOrContext):
        pass


    # Enter a parse tree produced by JavaParser#logicalAnd.
    def enterLogicalAnd(self, ctx:JavaParser.LogicalAndContext):
        pass

    # Exit a parse tree produced by JavaParser#logicalAnd.
    def exitLogicalAnd(self, ctx:JavaParser.LogicalAndContext):
        pass


    # Enter a parse tree produced by JavaParser#equality.
    def enterEquality(self, ctx:JavaParser.EqualityContext):
        pass

    # Exit a parse tree produced by JavaParser#equality.
    def exitEquality(self, ctx:JavaParser.EqualityContext):
        pass


    # Enter a parse tree produced by JavaParser#relational.
    def enterRelational(self, ctx:JavaParser.RelationalContext):
        pass

    # Exit a parse tree produced by JavaParser#relational.
    def exitRelational(self, ctx:JavaParser.RelationalContext):
        pass


    # Enter a parse tree produced by JavaParser#additive.
    def enterAdditive(self, ctx:JavaParser.AdditiveContext):
        pass

    # Exit a parse tree produced by JavaParser#additive.
    def exitAdditive(self, ctx:JavaParser.AdditiveContext):
        pass


    # Enter a parse tree produced by JavaParser#multiplicative.
    def enterMultiplicative(self, ctx:JavaParser.MultiplicativeContext):
        pass

    # Exit a parse tree produced by JavaParser#multiplicative.
    def exitMultiplicative(self, ctx:JavaParser.MultiplicativeContext):
        pass


    # Enter a parse tree produced by JavaParser#unary.
    def enterUnary(self, ctx:JavaParser.UnaryContext):
        pass

    # Exit a parse tree produced by JavaParser#unary.
    def exitUnary(self, ctx:JavaParser.UnaryContext):
        pass


    # Enter a parse tree produced by JavaParser#primary.
    def enterPrimary(self, ctx:JavaParser.PrimaryContext):
        pass

    # Exit a parse tree produced by JavaParser#primary.
    def exitPrimary(self, ctx:JavaParser.PrimaryContext):
        pass



del JavaParser