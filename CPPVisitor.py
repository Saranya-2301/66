# Generated from CPP.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CPPParser import CPPParser
else:
    from CPPParser import CPPParser

# This class defines a complete generic visitor for a parse tree produced by CPPParser.

class CPPVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CPPParser#program.
    def visitProgram(self, ctx:CPPParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#topLevel.
    def visitTopLevel(self, ctx:CPPParser.TopLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#preprocessor.
    def visitPreprocessor(self, ctx:CPPParser.PreprocessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#includeFile.
    def visitIncludeFile(self, ctx:CPPParser.IncludeFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#usingNamespace.
    def visitUsingNamespace(self, ctx:CPPParser.UsingNamespaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#namespaceDecl.
    def visitNamespaceDecl(self, ctx:CPPParser.NamespaceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#templateDecl.
    def visitTemplateDecl(self, ctx:CPPParser.TemplateDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#templateParamList.
    def visitTemplateParamList(self, ctx:CPPParser.TemplateParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#templateParam.
    def visitTemplateParam(self, ctx:CPPParser.TemplateParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#classDecl.
    def visitClassDecl(self, ctx:CPPParser.ClassDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#inheritanceList.
    def visitInheritanceList(self, ctx:CPPParser.InheritanceListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#inheritanceSpec.
    def visitInheritanceSpec(self, ctx:CPPParser.InheritanceSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#classMember.
    def visitClassMember(self, ctx:CPPParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#accessModifier.
    def visitAccessModifier(self, ctx:CPPParser.AccessModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#friendDecl.
    def visitFriendDecl(self, ctx:CPPParser.FriendDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#constructorDecl.
    def visitConstructorDecl(self, ctx:CPPParser.ConstructorDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#memberInitList.
    def visitMemberInitList(self, ctx:CPPParser.MemberInitListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#memberInitializer.
    def visitMemberInitializer(self, ctx:CPPParser.MemberInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#destructorDecl.
    def visitDestructorDecl(self, ctx:CPPParser.DestructorDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#structDecl.
    def visitStructDecl(self, ctx:CPPParser.StructDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#structMember.
    def visitStructMember(self, ctx:CPPParser.StructMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#unionDecl.
    def visitUnionDecl(self, ctx:CPPParser.UnionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#enumDecl.
    def visitEnumDecl(self, ctx:CPPParser.EnumDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#enumeratorList.
    def visitEnumeratorList(self, ctx:CPPParser.EnumeratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#enumerator.
    def visitEnumerator(self, ctx:CPPParser.EnumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#typedefDecl.
    def visitTypedefDecl(self, ctx:CPPParser.TypedefDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#functionDecl.
    def visitFunctionDecl(self, ctx:CPPParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#functionQualifier.
    def visitFunctionQualifier(self, ctx:CPPParser.FunctionQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#functionSuffix.
    def visitFunctionSuffix(self, ctx:CPPParser.FunctionSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#operatorName.
    def visitOperatorName(self, ctx:CPPParser.OperatorNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#anyIdentifier.
    def visitAnyIdentifier(self, ctx:CPPParser.AnyIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#qualifiedName.
    def visitQualifiedName(self, ctx:CPPParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#parameterList.
    def visitParameterList(self, ctx:CPPParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#parameter.
    def visitParameter(self, ctx:CPPParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#block.
    def visitBlock(self, ctx:CPPParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#statement.
    def visitStatement(self, ctx:CPPParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#declaration.
    def visitDeclaration(self, ctx:CPPParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#initDeclarator.
    def visitInitDeclarator(self, ctx:CPPParser.InitDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#initializer.
    def visitInitializer(self, ctx:CPPParser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#initializerList2.
    def visitInitializerList2(self, ctx:CPPParser.InitializerList2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#designatedInitializer.
    def visitDesignatedInitializer(self, ctx:CPPParser.DesignatedInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#assignment.
    def visitAssignment(self, ctx:CPPParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#lvalue.
    def visitLvalue(self, ctx:CPPParser.LvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#assignmentOp.
    def visitAssignmentOp(self, ctx:CPPParser.AssignmentOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#expressionStatement.
    def visitExpressionStatement(self, ctx:CPPParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#ifStatement.
    def visitIfStatement(self, ctx:CPPParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#whileStatement.
    def visitWhileStatement(self, ctx:CPPParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:CPPParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#forStatement.
    def visitForStatement(self, ctx:CPPParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#rangeForStatement.
    def visitRangeForStatement(self, ctx:CPPParser.RangeForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#forInit.
    def visitForInit(self, ctx:CPPParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#forUpdate.
    def visitForUpdate(self, ctx:CPPParser.ForUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#switchStatement.
    def visitSwitchStatement(self, ctx:CPPParser.SwitchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#caseStatement.
    def visitCaseStatement(self, ctx:CPPParser.CaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#tryStatement.
    def visitTryStatement(self, ctx:CPPParser.TryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#catchClause.
    def visitCatchClause(self, ctx:CPPParser.CatchClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#throwStatement.
    def visitThrowStatement(self, ctx:CPPParser.ThrowStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#coutStatement.
    def visitCoutStatement(self, ctx:CPPParser.CoutStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#cinStatement.
    def visitCinStatement(self, ctx:CPPParser.CinStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#returnStatement.
    def visitReturnStatement(self, ctx:CPPParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#breakStatement.
    def visitBreakStatement(self, ctx:CPPParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#continueStatement.
    def visitContinueStatement(self, ctx:CPPParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#gotoStatement.
    def visitGotoStatement(self, ctx:CPPParser.GotoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#labelStatement.
    def visitLabelStatement(self, ctx:CPPParser.LabelStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CPPParser.TypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#typeArgList.
    def visitTypeArgList(self, ctx:CPPParser.TypeArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#typeQualifier.
    def visitTypeQualifier(self, ctx:CPPParser.TypeQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#baseType.
    def visitBaseType(self, ctx:CPPParser.BaseTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#expression.
    def visitExpression(self, ctx:CPPParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:CPPParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:CPPParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:CPPParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:CPPParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#bitwiseOrExpression.
    def visitBitwiseOrExpression(self, ctx:CPPParser.BitwiseOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#bitwiseXorExpression.
    def visitBitwiseXorExpression(self, ctx:CPPParser.BitwiseXorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#bitwiseAndExpression.
    def visitBitwiseAndExpression(self, ctx:CPPParser.BitwiseAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#equalityExpression.
    def visitEqualityExpression(self, ctx:CPPParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#relationalExpression.
    def visitRelationalExpression(self, ctx:CPPParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#shiftExpression.
    def visitShiftExpression(self, ctx:CPPParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:CPPParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:CPPParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#castExpression.
    def visitCastExpression(self, ctx:CPPParser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#unaryExpression.
    def visitUnaryExpression(self, ctx:CPPParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#postfixExpression.
    def visitPostfixExpression(self, ctx:CPPParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#postfixOp.
    def visitPostfixOp(self, ctx:CPPParser.PostfixOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#lambdaExpression.
    def visitLambdaExpression(self, ctx:CPPParser.LambdaExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#captureList.
    def visitCaptureList(self, ctx:CPPParser.CaptureListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#captureItem.
    def visitCaptureItem(self, ctx:CPPParser.CaptureItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:CPPParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPPParser#argumentList.
    def visitArgumentList(self, ctx:CPPParser.ArgumentListContext):
        return self.visitChildren(ctx)



del CPPParser