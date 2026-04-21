# Generated from C.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete generic visitor for a parse tree produced by CParser.

class CVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CParser#program.
    def visitProgram(self, ctx:CParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#topLevel.
    def visitTopLevel(self, ctx:CParser.TopLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#preprocessor.
    def visitPreprocessor(self, ctx:CParser.PreprocessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#includeFile.
    def visitIncludeFile(self, ctx:CParser.IncludeFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structDecl.
    def visitStructDecl(self, ctx:CParser.StructDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structMember.
    def visitStructMember(self, ctx:CParser.StructMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unionDecl.
    def visitUnionDecl(self, ctx:CParser.UnionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumDecl.
    def visitEnumDecl(self, ctx:CParser.EnumDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumeratorList.
    def visitEnumeratorList(self, ctx:CParser.EnumeratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#enumerator.
    def visitEnumerator(self, ctx:CParser.EnumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typedefDecl.
    def visitTypedefDecl(self, ctx:CParser.TypedefDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionDecl.
    def visitFunctionDecl(self, ctx:CParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameterList.
    def visitParameterList(self, ctx:CParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#parameter.
    def visitParameter(self, ctx:CParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#block.
    def visitBlock(self, ctx:CParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declaration.
    def visitDeclaration(self, ctx:CParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initDeclarator.
    def visitInitDeclarator(self, ctx:CParser.InitDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initializer.
    def visitInitializer(self, ctx:CParser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#initializerList.
    def visitInitializerList(self, ctx:CParser.InitializerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#designatedInitializer.
    def visitDesignatedInitializer(self, ctx:CParser.DesignatedInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignment.
    def visitAssignment(self, ctx:CParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#lvalue.
    def visitLvalue(self, ctx:CParser.LvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignmentOp.
    def visitAssignmentOp(self, ctx:CParser.AssignmentOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expressionStatement.
    def visitExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#ifStatement.
    def visitIfStatement(self, ctx:CParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#whileStatement.
    def visitWhileStatement(self, ctx:CParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forStatement.
    def visitForStatement(self, ctx:CParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forInit.
    def visitForInit(self, ctx:CParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forUpdate.
    def visitForUpdate(self, ctx:CParser.ForUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#switchStatement.
    def visitSwitchStatement(self, ctx:CParser.SwitchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#caseStatement.
    def visitCaseStatement(self, ctx:CParser.CaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#returnStatement.
    def visitReturnStatement(self, ctx:CParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#breakStatement.
    def visitBreakStatement(self, ctx:CParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#continueStatement.
    def visitContinueStatement(self, ctx:CParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#gotoStatement.
    def visitGotoStatement(self, ctx:CParser.GotoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#labelStatement.
    def visitLabelStatement(self, ctx:CParser.LabelStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeQualifier.
    def visitTypeQualifier(self, ctx:CParser.TypeQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#baseType.
    def visitBaseType(self, ctx:CParser.BaseTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx:CParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#bitwiseOrExpression.
    def visitBitwiseOrExpression(self, ctx:CParser.BitwiseOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#bitwiseXorExpression.
    def visitBitwiseXorExpression(self, ctx:CParser.BitwiseXorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#bitwiseAndExpression.
    def visitBitwiseAndExpression(self, ctx:CParser.BitwiseAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#equalityExpression.
    def visitEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#relationalExpression.
    def visitRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#shiftExpression.
    def visitShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#castExpression.
    def visitCastExpression(self, ctx:CParser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryExpression.
    def visitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#postfixExpression.
    def visitPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#postfixOp.
    def visitPostfixOp(self, ctx:CParser.PostfixOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#builtinCall.
    def visitBuiltinCall(self, ctx:CParser.BuiltinCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#scanfArg.
    def visitScanfArg(self, ctx:CParser.ScanfArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#argumentList.
    def visitArgumentList(self, ctx:CParser.ArgumentListContext):
        return self.visitChildren(ctx)



del CParser