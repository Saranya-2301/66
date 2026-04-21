# Generated from CParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CParserListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#program.
    def enterProgram(self, ctx:CParser.ProgramContext):
        pass

    # Exit a parse tree produced by CParser#program.
    def exitProgram(self, ctx:CParser.ProgramContext):
        pass


    # Enter a parse tree produced by CParser#preprocessor.
    def enterPreprocessor(self, ctx:CParser.PreprocessorContext):
        pass

    # Exit a parse tree produced by CParser#preprocessor.
    def exitPreprocessor(self, ctx:CParser.PreprocessorContext):
        pass


    # Enter a parse tree produced by CParser#declaration.
    def enterDeclaration(self, ctx:CParser.DeclarationContext):
        pass

    # Exit a parse tree produced by CParser#declaration.
    def exitDeclaration(self, ctx:CParser.DeclarationContext):
        pass


    # Enter a parse tree produced by CParser#declaratorList.
    def enterDeclaratorList(self, ctx:CParser.DeclaratorListContext):
        pass

    # Exit a parse tree produced by CParser#declaratorList.
    def exitDeclaratorList(self, ctx:CParser.DeclaratorListContext):
        pass


    # Enter a parse tree produced by CParser#declarator.
    def enterDeclarator(self, ctx:CParser.DeclaratorContext):
        pass

    # Exit a parse tree produced by CParser#declarator.
    def exitDeclarator(self, ctx:CParser.DeclaratorContext):
        pass


    # Enter a parse tree produced by CParser#functionDef.
    def enterFunctionDef(self, ctx:CParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by CParser#functionDef.
    def exitFunctionDef(self, ctx:CParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by CParser#parameterList.
    def enterParameterList(self, ctx:CParser.ParameterListContext):
        pass

    # Exit a parse tree produced by CParser#parameterList.
    def exitParameterList(self, ctx:CParser.ParameterListContext):
        pass


    # Enter a parse tree produced by CParser#parameter.
    def enterParameter(self, ctx:CParser.ParameterContext):
        pass

    # Exit a parse tree produced by CParser#parameter.
    def exitParameter(self, ctx:CParser.ParameterContext):
        pass


    # Enter a parse tree produced by CParser#type.
    def enterType(self, ctx:CParser.TypeContext):
        pass

    # Exit a parse tree produced by CParser#type.
    def exitType(self, ctx:CParser.TypeContext):
        pass


    # Enter a parse tree produced by CParser#compoundStmt.
    def enterCompoundStmt(self, ctx:CParser.CompoundStmtContext):
        pass

    # Exit a parse tree produced by CParser#compoundStmt.
    def exitCompoundStmt(self, ctx:CParser.CompoundStmtContext):
        pass


    # Enter a parse tree produced by CParser#statement.
    def enterStatement(self, ctx:CParser.StatementContext):
        pass

    # Exit a parse tree produced by CParser#statement.
    def exitStatement(self, ctx:CParser.StatementContext):
        pass


    # Enter a parse tree produced by CParser#expressionStmt.
    def enterExpressionStmt(self, ctx:CParser.ExpressionStmtContext):
        pass

    # Exit a parse tree produced by CParser#expressionStmt.
    def exitExpressionStmt(self, ctx:CParser.ExpressionStmtContext):
        pass


    # Enter a parse tree produced by CParser#selectionStmt.
    def enterSelectionStmt(self, ctx:CParser.SelectionStmtContext):
        pass

    # Exit a parse tree produced by CParser#selectionStmt.
    def exitSelectionStmt(self, ctx:CParser.SelectionStmtContext):
        pass


    # Enter a parse tree produced by CParser#iterationStmt.
    def enterIterationStmt(self, ctx:CParser.IterationStmtContext):
        pass

    # Exit a parse tree produced by CParser#iterationStmt.
    def exitIterationStmt(self, ctx:CParser.IterationStmtContext):
        pass


    # Enter a parse tree produced by CParser#jumpStmt.
    def enterJumpStmt(self, ctx:CParser.JumpStmtContext):
        pass

    # Exit a parse tree produced by CParser#jumpStmt.
    def exitJumpStmt(self, ctx:CParser.JumpStmtContext):
        pass


    # Enter a parse tree produced by CParser#expression.
    def enterExpression(self, ctx:CParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CParser#expression.
    def exitExpression(self, ctx:CParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CParser#assignment.
    def enterAssignment(self, ctx:CParser.AssignmentContext):
        pass

    # Exit a parse tree produced by CParser#assignment.
    def exitAssignment(self, ctx:CParser.AssignmentContext):
        pass


    # Enter a parse tree produced by CParser#logicalOr.
    def enterLogicalOr(self, ctx:CParser.LogicalOrContext):
        pass

    # Exit a parse tree produced by CParser#logicalOr.
    def exitLogicalOr(self, ctx:CParser.LogicalOrContext):
        pass


    # Enter a parse tree produced by CParser#logicalAnd.
    def enterLogicalAnd(self, ctx:CParser.LogicalAndContext):
        pass

    # Exit a parse tree produced by CParser#logicalAnd.
    def exitLogicalAnd(self, ctx:CParser.LogicalAndContext):
        pass


    # Enter a parse tree produced by CParser#equality.
    def enterEquality(self, ctx:CParser.EqualityContext):
        pass

    # Exit a parse tree produced by CParser#equality.
    def exitEquality(self, ctx:CParser.EqualityContext):
        pass


    # Enter a parse tree produced by CParser#relational.
    def enterRelational(self, ctx:CParser.RelationalContext):
        pass

    # Exit a parse tree produced by CParser#relational.
    def exitRelational(self, ctx:CParser.RelationalContext):
        pass


    # Enter a parse tree produced by CParser#additive.
    def enterAdditive(self, ctx:CParser.AdditiveContext):
        pass

    # Exit a parse tree produced by CParser#additive.
    def exitAdditive(self, ctx:CParser.AdditiveContext):
        pass


    # Enter a parse tree produced by CParser#multiplicative.
    def enterMultiplicative(self, ctx:CParser.MultiplicativeContext):
        pass

    # Exit a parse tree produced by CParser#multiplicative.
    def exitMultiplicative(self, ctx:CParser.MultiplicativeContext):
        pass


    # Enter a parse tree produced by CParser#unary.
    def enterUnary(self, ctx:CParser.UnaryContext):
        pass

    # Exit a parse tree produced by CParser#unary.
    def exitUnary(self, ctx:CParser.UnaryContext):
        pass


    # Enter a parse tree produced by CParser#primary.
    def enterPrimary(self, ctx:CParser.PrimaryContext):
        pass

    # Exit a parse tree produced by CParser#primary.
    def exitPrimary(self, ctx:CParser.PrimaryContext):
        pass



del CParser