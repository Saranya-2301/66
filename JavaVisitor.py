# Generated from Java.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser

# This class defines a complete generic visitor for a parse tree produced by JavaParser.

class JavaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JavaParser#program.
    def visitProgram(self, ctx:JavaParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#packageDeclaration.
    def visitPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#importDeclaration.
    def visitImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:JavaParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotation.
    def visitAnnotation(self, ctx:JavaParser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationArgs.
    def visitAnnotationArgs(self, ctx:JavaParser.AnnotationArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationArg.
    def visitAnnotationArg(self, ctx:JavaParser.AnnotationArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#elementValue.
    def visitElementValue(self, ctx:JavaParser.ElementValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationDeclaration.
    def visitAnnotationDeclaration(self, ctx:JavaParser.AnnotationDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#annotationMember.
    def visitAnnotationMember(self, ctx:JavaParser.AnnotationMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classDeclaration.
    def visitClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classBody.
    def visitClassBody(self, ctx:JavaParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classMember.
    def visitClassMember(self, ctx:JavaParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#staticInitializer.
    def visitStaticInitializer(self, ctx:JavaParser.StaticInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#instanceInitializer.
    def visitInstanceInitializer(self, ctx:JavaParser.InstanceInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#sealedClassDeclaration.
    def visitSealedClassDeclaration(self, ctx:JavaParser.SealedClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordDeclaration.
    def visitRecordDeclaration(self, ctx:JavaParser.RecordDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordComponentList.
    def visitRecordComponentList(self, ctx:JavaParser.RecordComponentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#recordComponent.
    def visitRecordComponent(self, ctx:JavaParser.RecordComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceDeclaration.
    def visitInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMember.
    def visitInterfaceMember(self, ctx:JavaParser.InterfaceMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def visitInterfaceMethodDeclaration(self, ctx:JavaParser.InterfaceMethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumDeclaration.
    def visitEnumDeclaration(self, ctx:JavaParser.EnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumeratorList.
    def visitEnumeratorList(self, ctx:JavaParser.EnumeratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enumerator.
    def visitEnumerator(self, ctx:JavaParser.EnumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#modifier.
    def visitModifier(self, ctx:JavaParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeParameters.
    def visitTypeParameters(self, ctx:JavaParser.TypeParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeParameter.
    def visitTypeParameter(self, ctx:JavaParser.TypeParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeBound.
    def visitTypeBound(self, ctx:JavaParser.TypeBoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeType.
    def visitTypeType(self, ctx:JavaParser.TypeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#primitiveType.
    def visitPrimitiveType(self, ctx:JavaParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArguments.
    def visitTypeArguments(self, ctx:JavaParser.TypeArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeArgument.
    def visitTypeArgument(self, ctx:JavaParser.TypeArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#typeList.
    def visitTypeList(self, ctx:JavaParser.TypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableDeclarator.
    def visitVariableDeclarator(self, ctx:JavaParser.VariableDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#variableInitializer.
    def visitVariableInitializer(self, ctx:JavaParser.VariableInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayInitializer.
    def visitArrayInitializer(self, ctx:JavaParser.ArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#constructorDeclaration.
    def visitConstructorDeclaration(self, ctx:JavaParser.ConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#parameterList.
    def visitParameterList(self, ctx:JavaParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#parameter.
    def visitParameter(self, ctx:JavaParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#block.
    def visitBlock(self, ctx:JavaParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#blockStatement.
    def visitBlockStatement(self, ctx:JavaParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#localVariableDeclaration.
    def visitLocalVariableDeclaration(self, ctx:JavaParser.LocalVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#statement.
    def visitStatement(self, ctx:JavaParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#ifStatement.
    def visitIfStatement(self, ctx:JavaParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#whileStatement.
    def visitWhileStatement(self, ctx:JavaParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:JavaParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forStatement.
    def visitForStatement(self, ctx:JavaParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forInit.
    def visitForInit(self, ctx:JavaParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#forUpdate.
    def visitForUpdate(self, ctx:JavaParser.ForUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#enhancedForStatement.
    def visitEnhancedForStatement(self, ctx:JavaParser.EnhancedForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchStatement.
    def visitSwitchStatement(self, ctx:JavaParser.SwitchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#switchCase.
    def visitSwitchCase(self, ctx:JavaParser.SwitchCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#tryStatement.
    def visitTryStatement(self, ctx:JavaParser.TryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resourceSpec.
    def visitResourceSpec(self, ctx:JavaParser.ResourceSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#resource.
    def visitResource(self, ctx:JavaParser.ResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catchClause.
    def visitCatchClause(self, ctx:JavaParser.CatchClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#catchType.
    def visitCatchType(self, ctx:JavaParser.CatchTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#finallyClause.
    def visitFinallyClause(self, ctx:JavaParser.FinallyClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#assertStatement.
    def visitAssertStatement(self, ctx:JavaParser.AssertStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#synchronizedStatement.
    def visitSynchronizedStatement(self, ctx:JavaParser.SynchronizedStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#yieldStatement.
    def visitYieldStatement(self, ctx:JavaParser.YieldStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#returnStatement.
    def visitReturnStatement(self, ctx:JavaParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#throwStatement.
    def visitThrowStatement(self, ctx:JavaParser.ThrowStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#breakStatement.
    def visitBreakStatement(self, ctx:JavaParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#continueStatement.
    def visitContinueStatement(self, ctx:JavaParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#gotoStatement.
    def visitGotoStatement(self, ctx:JavaParser.GotoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#labelStatement.
    def visitLabelStatement(self, ctx:JavaParser.LabelStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expressionStatement.
    def visitExpressionStatement(self, ctx:JavaParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expressionList.
    def visitExpressionList(self, ctx:JavaParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#qualifiedName.
    def visitQualifiedName(self, ctx:JavaParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#expression.
    def visitExpression(self, ctx:JavaParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:JavaParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#assignmentOp.
    def visitAssignmentOp(self, ctx:JavaParser.AssignmentOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:JavaParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:JavaParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:JavaParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#bitwiseOrExpression.
    def visitBitwiseOrExpression(self, ctx:JavaParser.BitwiseOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#bitwiseXorExpression.
    def visitBitwiseXorExpression(self, ctx:JavaParser.BitwiseXorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#bitwiseAndExpression.
    def visitBitwiseAndExpression(self, ctx:JavaParser.BitwiseAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#equalityExpression.
    def visitEqualityExpression(self, ctx:JavaParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#relationalExpression.
    def visitRelationalExpression(self, ctx:JavaParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#shiftExpression.
    def visitShiftExpression(self, ctx:JavaParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:JavaParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:JavaParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#castExpression.
    def visitCastExpression(self, ctx:JavaParser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#unaryExpression.
    def visitUnaryExpression(self, ctx:JavaParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#postfixExpression.
    def visitPostfixExpression(self, ctx:JavaParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#postfixOp.
    def visitPostfixOp(self, ctx:JavaParser.PostfixOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:JavaParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaExpression.
    def visitLambdaExpression(self, ctx:JavaParser.LambdaExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaParams.
    def visitLambdaParams(self, ctx:JavaParser.LambdaParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#lambdaBody.
    def visitLambdaBody(self, ctx:JavaParser.LambdaBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#creator.
    def visitCreator(self, ctx:JavaParser.CreatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#createdName.
    def visitCreatedName(self, ctx:JavaParser.CreatedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#classCreatorRest.
    def visitClassCreatorRest(self, ctx:JavaParser.ClassCreatorRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#arrayCreatorRest.
    def visitArrayCreatorRest(self, ctx:JavaParser.ArrayCreatorRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaParser#argumentList.
    def visitArgumentList(self, ctx:JavaParser.ArgumentListContext):
        return self.visitChildren(ctx)



del JavaParser