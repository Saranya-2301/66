# Generated from C.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#program.
    def enterProgram(self, ctx:CParser.ProgramContext):
        pass

    # Exit a parse tree produced by CParser#program.
    def exitProgram(self, ctx:CParser.ProgramContext):
        pass


    # Enter a parse tree produced by CParser#topLevel.
    def enterTopLevel(self, ctx:CParser.TopLevelContext):
        pass

    # Exit a parse tree produced by CParser#topLevel.
    def exitTopLevel(self, ctx:CParser.TopLevelContext):
        pass


    # Enter a parse tree produced by CParser#preprocessor.
    def enterPreprocessor(self, ctx:CParser.PreprocessorContext):
        pass

    # Exit a parse tree produced by CParser#preprocessor.
    def exitPreprocessor(self, ctx:CParser.PreprocessorContext):
        pass


    # Enter a parse tree produced by CParser#includeFile.
    def enterIncludeFile(self, ctx:CParser.IncludeFileContext):
        pass

    # Exit a parse tree produced by CParser#includeFile.
    def exitIncludeFile(self, ctx:CParser.IncludeFileContext):
        pass


    # Enter a parse tree produced by CParser#structDecl.
    def enterStructDecl(self, ctx:CParser.StructDeclContext):
        pass

    # Exit a parse tree produced by CParser#structDecl.
    def exitStructDecl(self, ctx:CParser.StructDeclContext):
        pass


    # Enter a parse tree produced by CParser#structMember.
    def enterStructMember(self, ctx:CParser.StructMemberContext):
        pass

    # Exit a parse tree produced by CParser#structMember.
    def exitStructMember(self, ctx:CParser.StructMemberContext):
        pass


    # Enter a parse tree produced by CParser#unionDecl.
    def enterUnionDecl(self, ctx:CParser.UnionDeclContext):
        pass

    # Exit a parse tree produced by CParser#unionDecl.
    def exitUnionDecl(self, ctx:CParser.UnionDeclContext):
        pass


    # Enter a parse tree produced by CParser#enumDecl.
    def enterEnumDecl(self, ctx:CParser.EnumDeclContext):
        pass

    # Exit a parse tree produced by CParser#enumDecl.
    def exitEnumDecl(self, ctx:CParser.EnumDeclContext):
        pass


    # Enter a parse tree produced by CParser#enumeratorList.
    def enterEnumeratorList(self, ctx:CParser.EnumeratorListContext):
        pass

    # Exit a parse tree produced by CParser#enumeratorList.
    def exitEnumeratorList(self, ctx:CParser.EnumeratorListContext):
        pass


    # Enter a parse tree produced by CParser#enumerator.
    def enterEnumerator(self, ctx:CParser.EnumeratorContext):
        pass

    # Exit a parse tree produced by CParser#enumerator.
    def exitEnumerator(self, ctx:CParser.EnumeratorContext):
        pass


    # Enter a parse tree produced by CParser#typedefDecl.
    def enterTypedefDecl(self, ctx:CParser.TypedefDeclContext):
        pass

    # Exit a parse tree produced by CParser#typedefDecl.
    def exitTypedefDecl(self, ctx:CParser.TypedefDeclContext):
        pass


    # Enter a parse tree produced by CParser#functionDecl.
    def enterFunctionDecl(self, ctx:CParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by CParser#functionDecl.
    def exitFunctionDecl(self, ctx:CParser.FunctionDeclContext):
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


    # Enter a parse tree produced by CParser#block.
    def enterBlock(self, ctx:CParser.BlockContext):
        pass

    # Exit a parse tree produced by CParser#block.
    def exitBlock(self, ctx:CParser.BlockContext):
        pass


    # Enter a parse tree produced by CParser#statement.
    def enterStatement(self, ctx:CParser.StatementContext):
        pass

    # Exit a parse tree produced by CParser#statement.
    def exitStatement(self, ctx:CParser.StatementContext):
        pass


    # Enter a parse tree produced by CParser#declaration.
    def enterDeclaration(self, ctx:CParser.DeclarationContext):
        pass

    # Exit a parse tree produced by CParser#declaration.
    def exitDeclaration(self, ctx:CParser.DeclarationContext):
        pass


    # Enter a parse tree produced by CParser#initDeclarator.
    def enterInitDeclarator(self, ctx:CParser.InitDeclaratorContext):
        pass

    # Exit a parse tree produced by CParser#initDeclarator.
    def exitInitDeclarator(self, ctx:CParser.InitDeclaratorContext):
        pass


    # Enter a parse tree produced by CParser#initializer.
    def enterInitializer(self, ctx:CParser.InitializerContext):
        pass

    # Exit a parse tree produced by CParser#initializer.
    def exitInitializer(self, ctx:CParser.InitializerContext):
        pass


    # Enter a parse tree produced by CParser#initializerList.
    def enterInitializerList(self, ctx:CParser.InitializerListContext):
        pass

    # Exit a parse tree produced by CParser#initializerList.
    def exitInitializerList(self, ctx:CParser.InitializerListContext):
        pass


    # Enter a parse tree produced by CParser#designatedInitializer.
    def enterDesignatedInitializer(self, ctx:CParser.DesignatedInitializerContext):
        pass

    # Exit a parse tree produced by CParser#designatedInitializer.
    def exitDesignatedInitializer(self, ctx:CParser.DesignatedInitializerContext):
        pass


    # Enter a parse tree produced by CParser#assignment.
    def enterAssignment(self, ctx:CParser.AssignmentContext):
        pass

    # Exit a parse tree produced by CParser#assignment.
    def exitAssignment(self, ctx:CParser.AssignmentContext):
        pass


    # Enter a parse tree produced by CParser#lvalue.
    def enterLvalue(self, ctx:CParser.LvalueContext):
        pass

    # Exit a parse tree produced by CParser#lvalue.
    def exitLvalue(self, ctx:CParser.LvalueContext):
        pass


    # Enter a parse tree produced by CParser#assignmentOp.
    def enterAssignmentOp(self, ctx:CParser.AssignmentOpContext):
        pass

    # Exit a parse tree produced by CParser#assignmentOp.
    def exitAssignmentOp(self, ctx:CParser.AssignmentOpContext):
        pass


    # Enter a parse tree produced by CParser#expressionStatement.
    def enterExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by CParser#expressionStatement.
    def exitExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by CParser#ifStatement.
    def enterIfStatement(self, ctx:CParser.IfStatementContext):
        pass

    # Exit a parse tree produced by CParser#ifStatement.
    def exitIfStatement(self, ctx:CParser.IfStatementContext):
        pass


    # Enter a parse tree produced by CParser#whileStatement.
    def enterWhileStatement(self, ctx:CParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by CParser#whileStatement.
    def exitWhileStatement(self, ctx:CParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by CParser#doWhileStatement.
    def enterDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by CParser#doWhileStatement.
    def exitDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by CParser#forStatement.
    def enterForStatement(self, ctx:CParser.ForStatementContext):
        pass

    # Exit a parse tree produced by CParser#forStatement.
    def exitForStatement(self, ctx:CParser.ForStatementContext):
        pass


    # Enter a parse tree produced by CParser#forInit.
    def enterForInit(self, ctx:CParser.ForInitContext):
        pass

    # Exit a parse tree produced by CParser#forInit.
    def exitForInit(self, ctx:CParser.ForInitContext):
        pass


    # Enter a parse tree produced by CParser#forUpdate.
    def enterForUpdate(self, ctx:CParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by CParser#forUpdate.
    def exitForUpdate(self, ctx:CParser.ForUpdateContext):
        pass


    # Enter a parse tree produced by CParser#switchStatement.
    def enterSwitchStatement(self, ctx:CParser.SwitchStatementContext):
        pass

    # Exit a parse tree produced by CParser#switchStatement.
    def exitSwitchStatement(self, ctx:CParser.SwitchStatementContext):
        pass


    # Enter a parse tree produced by CParser#caseStatement.
    def enterCaseStatement(self, ctx:CParser.CaseStatementContext):
        pass

    # Exit a parse tree produced by CParser#caseStatement.
    def exitCaseStatement(self, ctx:CParser.CaseStatementContext):
        pass


    # Enter a parse tree produced by CParser#returnStatement.
    def enterReturnStatement(self, ctx:CParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by CParser#returnStatement.
    def exitReturnStatement(self, ctx:CParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by CParser#breakStatement.
    def enterBreakStatement(self, ctx:CParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by CParser#breakStatement.
    def exitBreakStatement(self, ctx:CParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by CParser#continueStatement.
    def enterContinueStatement(self, ctx:CParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by CParser#continueStatement.
    def exitContinueStatement(self, ctx:CParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by CParser#gotoStatement.
    def enterGotoStatement(self, ctx:CParser.GotoStatementContext):
        pass

    # Exit a parse tree produced by CParser#gotoStatement.
    def exitGotoStatement(self, ctx:CParser.GotoStatementContext):
        pass


    # Enter a parse tree produced by CParser#labelStatement.
    def enterLabelStatement(self, ctx:CParser.LabelStatementContext):
        pass

    # Exit a parse tree produced by CParser#labelStatement.
    def exitLabelStatement(self, ctx:CParser.LabelStatementContext):
        pass


    # Enter a parse tree produced by CParser#typeSpecifier.
    def enterTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        pass

    # Exit a parse tree produced by CParser#typeSpecifier.
    def exitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        pass


    # Enter a parse tree produced by CParser#typeQualifier.
    def enterTypeQualifier(self, ctx:CParser.TypeQualifierContext):
        pass

    # Exit a parse tree produced by CParser#typeQualifier.
    def exitTypeQualifier(self, ctx:CParser.TypeQualifierContext):
        pass


    # Enter a parse tree produced by CParser#baseType.
    def enterBaseType(self, ctx:CParser.BaseTypeContext):
        pass

    # Exit a parse tree produced by CParser#baseType.
    def exitBaseType(self, ctx:CParser.BaseTypeContext):
        pass


    # Enter a parse tree produced by CParser#expression.
    def enterExpression(self, ctx:CParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CParser#expression.
    def exitExpression(self, ctx:CParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by CParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        pass


    # Enter a parse tree produced by CParser#conditionalExpression.
    def enterConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by CParser#conditionalExpression.
    def exitConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        pass


    # Enter a parse tree produced by CParser#logicalOrExpression.
    def enterLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        pass

    # Exit a parse tree produced by CParser#logicalOrExpression.
    def exitLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        pass


    # Enter a parse tree produced by CParser#logicalAndExpression.
    def enterLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        pass

    # Exit a parse tree produced by CParser#logicalAndExpression.
    def exitLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        pass


    # Enter a parse tree produced by CParser#bitwiseOrExpression.
    def enterBitwiseOrExpression(self, ctx:CParser.BitwiseOrExpressionContext):
        pass

    # Exit a parse tree produced by CParser#bitwiseOrExpression.
    def exitBitwiseOrExpression(self, ctx:CParser.BitwiseOrExpressionContext):
        pass


    # Enter a parse tree produced by CParser#bitwiseXorExpression.
    def enterBitwiseXorExpression(self, ctx:CParser.BitwiseXorExpressionContext):
        pass

    # Exit a parse tree produced by CParser#bitwiseXorExpression.
    def exitBitwiseXorExpression(self, ctx:CParser.BitwiseXorExpressionContext):
        pass


    # Enter a parse tree produced by CParser#bitwiseAndExpression.
    def enterBitwiseAndExpression(self, ctx:CParser.BitwiseAndExpressionContext):
        pass

    # Exit a parse tree produced by CParser#bitwiseAndExpression.
    def exitBitwiseAndExpression(self, ctx:CParser.BitwiseAndExpressionContext):
        pass


    # Enter a parse tree produced by CParser#equalityExpression.
    def enterEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by CParser#equalityExpression.
    def exitEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        pass


    # Enter a parse tree produced by CParser#relationalExpression.
    def enterRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by CParser#relationalExpression.
    def exitRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by CParser#shiftExpression.
    def enterShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        pass

    # Exit a parse tree produced by CParser#shiftExpression.
    def exitShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        pass


    # Enter a parse tree produced by CParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by CParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by CParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by CParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by CParser#castExpression.
    def enterCastExpression(self, ctx:CParser.CastExpressionContext):
        pass

    # Exit a parse tree produced by CParser#castExpression.
    def exitCastExpression(self, ctx:CParser.CastExpressionContext):
        pass


    # Enter a parse tree produced by CParser#unaryExpression.
    def enterUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by CParser#unaryExpression.
    def exitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by CParser#postfixExpression.
    def enterPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by CParser#postfixExpression.
    def exitPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        pass


    # Enter a parse tree produced by CParser#postfixOp.
    def enterPostfixOp(self, ctx:CParser.PostfixOpContext):
        pass

    # Exit a parse tree produced by CParser#postfixOp.
    def exitPostfixOp(self, ctx:CParser.PostfixOpContext):
        pass


    # Enter a parse tree produced by CParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by CParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by CParser#builtinCall.
    def enterBuiltinCall(self, ctx:CParser.BuiltinCallContext):
        pass

    # Exit a parse tree produced by CParser#builtinCall.
    def exitBuiltinCall(self, ctx:CParser.BuiltinCallContext):
        pass


    # Enter a parse tree produced by CParser#scanfArg.
    def enterScanfArg(self, ctx:CParser.ScanfArgContext):
        pass

    # Exit a parse tree produced by CParser#scanfArg.
    def exitScanfArg(self, ctx:CParser.ScanfArgContext):
        pass


    # Enter a parse tree produced by CParser#argumentList.
    def enterArgumentList(self, ctx:CParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by CParser#argumentList.
    def exitArgumentList(self, ctx:CParser.ArgumentListContext):
        pass



del CParser