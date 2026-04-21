# Generated from Java.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JavaParser import JavaParser
else:
    from JavaParser import JavaParser

# This class defines a complete listener for a parse tree produced by JavaParser.
class JavaListener(ParseTreeListener):

    # Enter a parse tree produced by JavaParser#program.
    def enterProgram(self, ctx:JavaParser.ProgramContext):
        pass

    # Exit a parse tree produced by JavaParser#program.
    def exitProgram(self, ctx:JavaParser.ProgramContext):
        pass


    # Enter a parse tree produced by JavaParser#packageDeclaration.
    def enterPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#packageDeclaration.
    def exitPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#importDeclaration.
    def enterImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#importDeclaration.
    def exitImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:JavaParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:JavaParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#annotation.
    def enterAnnotation(self, ctx:JavaParser.AnnotationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotation.
    def exitAnnotation(self, ctx:JavaParser.AnnotationContext):
        pass


    # Enter a parse tree produced by JavaParser#annotationArgs.
    def enterAnnotationArgs(self, ctx:JavaParser.AnnotationArgsContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationArgs.
    def exitAnnotationArgs(self, ctx:JavaParser.AnnotationArgsContext):
        pass


    # Enter a parse tree produced by JavaParser#annotationArg.
    def enterAnnotationArg(self, ctx:JavaParser.AnnotationArgContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationArg.
    def exitAnnotationArg(self, ctx:JavaParser.AnnotationArgContext):
        pass


    # Enter a parse tree produced by JavaParser#elementValue.
    def enterElementValue(self, ctx:JavaParser.ElementValueContext):
        pass

    # Exit a parse tree produced by JavaParser#elementValue.
    def exitElementValue(self, ctx:JavaParser.ElementValueContext):
        pass


    # Enter a parse tree produced by JavaParser#annotationDeclaration.
    def enterAnnotationDeclaration(self, ctx:JavaParser.AnnotationDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationDeclaration.
    def exitAnnotationDeclaration(self, ctx:JavaParser.AnnotationDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#annotationMember.
    def enterAnnotationMember(self, ctx:JavaParser.AnnotationMemberContext):
        pass

    # Exit a parse tree produced by JavaParser#annotationMember.
    def exitAnnotationMember(self, ctx:JavaParser.AnnotationMemberContext):
        pass


    # Enter a parse tree produced by JavaParser#classDeclaration.
    def enterClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#classDeclaration.
    def exitClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#classBody.
    def enterClassBody(self, ctx:JavaParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#classBody.
    def exitClassBody(self, ctx:JavaParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#classMember.
    def enterClassMember(self, ctx:JavaParser.ClassMemberContext):
        pass

    # Exit a parse tree produced by JavaParser#classMember.
    def exitClassMember(self, ctx:JavaParser.ClassMemberContext):
        pass


    # Enter a parse tree produced by JavaParser#staticInitializer.
    def enterStaticInitializer(self, ctx:JavaParser.StaticInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#staticInitializer.
    def exitStaticInitializer(self, ctx:JavaParser.StaticInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#instanceInitializer.
    def enterInstanceInitializer(self, ctx:JavaParser.InstanceInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#instanceInitializer.
    def exitInstanceInitializer(self, ctx:JavaParser.InstanceInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#sealedClassDeclaration.
    def enterSealedClassDeclaration(self, ctx:JavaParser.SealedClassDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#sealedClassDeclaration.
    def exitSealedClassDeclaration(self, ctx:JavaParser.SealedClassDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#recordDeclaration.
    def enterRecordDeclaration(self, ctx:JavaParser.RecordDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#recordDeclaration.
    def exitRecordDeclaration(self, ctx:JavaParser.RecordDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#recordComponentList.
    def enterRecordComponentList(self, ctx:JavaParser.RecordComponentListContext):
        pass

    # Exit a parse tree produced by JavaParser#recordComponentList.
    def exitRecordComponentList(self, ctx:JavaParser.RecordComponentListContext):
        pass


    # Enter a parse tree produced by JavaParser#recordComponent.
    def enterRecordComponent(self, ctx:JavaParser.RecordComponentContext):
        pass

    # Exit a parse tree produced by JavaParser#recordComponent.
    def exitRecordComponent(self, ctx:JavaParser.RecordComponentContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceDeclaration.
    def enterInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceDeclaration.
    def exitInterfaceDeclaration(self, ctx:JavaParser.InterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceMember.
    def enterInterfaceMember(self, ctx:JavaParser.InterfaceMemberContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMember.
    def exitInterfaceMember(self, ctx:JavaParser.InterfaceMemberContext):
        pass


    # Enter a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def enterInterfaceMethodDeclaration(self, ctx:JavaParser.InterfaceMethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#interfaceMethodDeclaration.
    def exitInterfaceMethodDeclaration(self, ctx:JavaParser.InterfaceMethodDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#enumDeclaration.
    def enterEnumDeclaration(self, ctx:JavaParser.EnumDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#enumDeclaration.
    def exitEnumDeclaration(self, ctx:JavaParser.EnumDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#enumeratorList.
    def enterEnumeratorList(self, ctx:JavaParser.EnumeratorListContext):
        pass

    # Exit a parse tree produced by JavaParser#enumeratorList.
    def exitEnumeratorList(self, ctx:JavaParser.EnumeratorListContext):
        pass


    # Enter a parse tree produced by JavaParser#enumerator.
    def enterEnumerator(self, ctx:JavaParser.EnumeratorContext):
        pass

    # Exit a parse tree produced by JavaParser#enumerator.
    def exitEnumerator(self, ctx:JavaParser.EnumeratorContext):
        pass


    # Enter a parse tree produced by JavaParser#modifier.
    def enterModifier(self, ctx:JavaParser.ModifierContext):
        pass

    # Exit a parse tree produced by JavaParser#modifier.
    def exitModifier(self, ctx:JavaParser.ModifierContext):
        pass


    # Enter a parse tree produced by JavaParser#typeParameters.
    def enterTypeParameters(self, ctx:JavaParser.TypeParametersContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameters.
    def exitTypeParameters(self, ctx:JavaParser.TypeParametersContext):
        pass


    # Enter a parse tree produced by JavaParser#typeParameter.
    def enterTypeParameter(self, ctx:JavaParser.TypeParameterContext):
        pass

    # Exit a parse tree produced by JavaParser#typeParameter.
    def exitTypeParameter(self, ctx:JavaParser.TypeParameterContext):
        pass


    # Enter a parse tree produced by JavaParser#typeBound.
    def enterTypeBound(self, ctx:JavaParser.TypeBoundContext):
        pass

    # Exit a parse tree produced by JavaParser#typeBound.
    def exitTypeBound(self, ctx:JavaParser.TypeBoundContext):
        pass


    # Enter a parse tree produced by JavaParser#typeType.
    def enterTypeType(self, ctx:JavaParser.TypeTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#typeType.
    def exitTypeType(self, ctx:JavaParser.TypeTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#primitiveType.
    def enterPrimitiveType(self, ctx:JavaParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#primitiveType.
    def exitPrimitiveType(self, ctx:JavaParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#typeArguments.
    def enterTypeArguments(self, ctx:JavaParser.TypeArgumentsContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArguments.
    def exitTypeArguments(self, ctx:JavaParser.TypeArgumentsContext):
        pass


    # Enter a parse tree produced by JavaParser#typeArgument.
    def enterTypeArgument(self, ctx:JavaParser.TypeArgumentContext):
        pass

    # Exit a parse tree produced by JavaParser#typeArgument.
    def exitTypeArgument(self, ctx:JavaParser.TypeArgumentContext):
        pass


    # Enter a parse tree produced by JavaParser#typeList.
    def enterTypeList(self, ctx:JavaParser.TypeListContext):
        pass

    # Exit a parse tree produced by JavaParser#typeList.
    def exitTypeList(self, ctx:JavaParser.TypeListContext):
        pass


    # Enter a parse tree produced by JavaParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#fieldDeclaration.
    def exitFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#variableDeclarator.
    def enterVariableDeclarator(self, ctx:JavaParser.VariableDeclaratorContext):
        pass

    # Exit a parse tree produced by JavaParser#variableDeclarator.
    def exitVariableDeclarator(self, ctx:JavaParser.VariableDeclaratorContext):
        pass


    # Enter a parse tree produced by JavaParser#variableInitializer.
    def enterVariableInitializer(self, ctx:JavaParser.VariableInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#variableInitializer.
    def exitVariableInitializer(self, ctx:JavaParser.VariableInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#arrayInitializer.
    def enterArrayInitializer(self, ctx:JavaParser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayInitializer.
    def exitArrayInitializer(self, ctx:JavaParser.ArrayInitializerContext):
        pass


    # Enter a parse tree produced by JavaParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#constructorDeclaration.
    def enterConstructorDeclaration(self, ctx:JavaParser.ConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#constructorDeclaration.
    def exitConstructorDeclaration(self, ctx:JavaParser.ConstructorDeclarationContext):
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


    # Enter a parse tree produced by JavaParser#block.
    def enterBlock(self, ctx:JavaParser.BlockContext):
        pass

    # Exit a parse tree produced by JavaParser#block.
    def exitBlock(self, ctx:JavaParser.BlockContext):
        pass


    # Enter a parse tree produced by JavaParser#blockStatement.
    def enterBlockStatement(self, ctx:JavaParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#blockStatement.
    def exitBlockStatement(self, ctx:JavaParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#localVariableDeclaration.
    def enterLocalVariableDeclaration(self, ctx:JavaParser.LocalVariableDeclarationContext):
        pass

    # Exit a parse tree produced by JavaParser#localVariableDeclaration.
    def exitLocalVariableDeclaration(self, ctx:JavaParser.LocalVariableDeclarationContext):
        pass


    # Enter a parse tree produced by JavaParser#statement.
    def enterStatement(self, ctx:JavaParser.StatementContext):
        pass

    # Exit a parse tree produced by JavaParser#statement.
    def exitStatement(self, ctx:JavaParser.StatementContext):
        pass


    # Enter a parse tree produced by JavaParser#ifStatement.
    def enterIfStatement(self, ctx:JavaParser.IfStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#ifStatement.
    def exitIfStatement(self, ctx:JavaParser.IfStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#whileStatement.
    def enterWhileStatement(self, ctx:JavaParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#whileStatement.
    def exitWhileStatement(self, ctx:JavaParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#doWhileStatement.
    def enterDoWhileStatement(self, ctx:JavaParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#doWhileStatement.
    def exitDoWhileStatement(self, ctx:JavaParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#forStatement.
    def enterForStatement(self, ctx:JavaParser.ForStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#forStatement.
    def exitForStatement(self, ctx:JavaParser.ForStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#forInit.
    def enterForInit(self, ctx:JavaParser.ForInitContext):
        pass

    # Exit a parse tree produced by JavaParser#forInit.
    def exitForInit(self, ctx:JavaParser.ForInitContext):
        pass


    # Enter a parse tree produced by JavaParser#forUpdate.
    def enterForUpdate(self, ctx:JavaParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by JavaParser#forUpdate.
    def exitForUpdate(self, ctx:JavaParser.ForUpdateContext):
        pass


    # Enter a parse tree produced by JavaParser#enhancedForStatement.
    def enterEnhancedForStatement(self, ctx:JavaParser.EnhancedForStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#enhancedForStatement.
    def exitEnhancedForStatement(self, ctx:JavaParser.EnhancedForStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#switchStatement.
    def enterSwitchStatement(self, ctx:JavaParser.SwitchStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#switchStatement.
    def exitSwitchStatement(self, ctx:JavaParser.SwitchStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#switchCase.
    def enterSwitchCase(self, ctx:JavaParser.SwitchCaseContext):
        pass

    # Exit a parse tree produced by JavaParser#switchCase.
    def exitSwitchCase(self, ctx:JavaParser.SwitchCaseContext):
        pass


    # Enter a parse tree produced by JavaParser#tryStatement.
    def enterTryStatement(self, ctx:JavaParser.TryStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#tryStatement.
    def exitTryStatement(self, ctx:JavaParser.TryStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#resourceSpec.
    def enterResourceSpec(self, ctx:JavaParser.ResourceSpecContext):
        pass

    # Exit a parse tree produced by JavaParser#resourceSpec.
    def exitResourceSpec(self, ctx:JavaParser.ResourceSpecContext):
        pass


    # Enter a parse tree produced by JavaParser#resource.
    def enterResource(self, ctx:JavaParser.ResourceContext):
        pass

    # Exit a parse tree produced by JavaParser#resource.
    def exitResource(self, ctx:JavaParser.ResourceContext):
        pass


    # Enter a parse tree produced by JavaParser#catchClause.
    def enterCatchClause(self, ctx:JavaParser.CatchClauseContext):
        pass

    # Exit a parse tree produced by JavaParser#catchClause.
    def exitCatchClause(self, ctx:JavaParser.CatchClauseContext):
        pass


    # Enter a parse tree produced by JavaParser#catchType.
    def enterCatchType(self, ctx:JavaParser.CatchTypeContext):
        pass

    # Exit a parse tree produced by JavaParser#catchType.
    def exitCatchType(self, ctx:JavaParser.CatchTypeContext):
        pass


    # Enter a parse tree produced by JavaParser#finallyClause.
    def enterFinallyClause(self, ctx:JavaParser.FinallyClauseContext):
        pass

    # Exit a parse tree produced by JavaParser#finallyClause.
    def exitFinallyClause(self, ctx:JavaParser.FinallyClauseContext):
        pass


    # Enter a parse tree produced by JavaParser#assertStatement.
    def enterAssertStatement(self, ctx:JavaParser.AssertStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#assertStatement.
    def exitAssertStatement(self, ctx:JavaParser.AssertStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#synchronizedStatement.
    def enterSynchronizedStatement(self, ctx:JavaParser.SynchronizedStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#synchronizedStatement.
    def exitSynchronizedStatement(self, ctx:JavaParser.SynchronizedStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#yieldStatement.
    def enterYieldStatement(self, ctx:JavaParser.YieldStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#yieldStatement.
    def exitYieldStatement(self, ctx:JavaParser.YieldStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#returnStatement.
    def enterReturnStatement(self, ctx:JavaParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#returnStatement.
    def exitReturnStatement(self, ctx:JavaParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#throwStatement.
    def enterThrowStatement(self, ctx:JavaParser.ThrowStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#throwStatement.
    def exitThrowStatement(self, ctx:JavaParser.ThrowStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#breakStatement.
    def enterBreakStatement(self, ctx:JavaParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#breakStatement.
    def exitBreakStatement(self, ctx:JavaParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#continueStatement.
    def enterContinueStatement(self, ctx:JavaParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#continueStatement.
    def exitContinueStatement(self, ctx:JavaParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#gotoStatement.
    def enterGotoStatement(self, ctx:JavaParser.GotoStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#gotoStatement.
    def exitGotoStatement(self, ctx:JavaParser.GotoStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#labelStatement.
    def enterLabelStatement(self, ctx:JavaParser.LabelStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#labelStatement.
    def exitLabelStatement(self, ctx:JavaParser.LabelStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#expressionStatement.
    def enterExpressionStatement(self, ctx:JavaParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by JavaParser#expressionStatement.
    def exitExpressionStatement(self, ctx:JavaParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by JavaParser#expressionList.
    def enterExpressionList(self, ctx:JavaParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by JavaParser#expressionList.
    def exitExpressionList(self, ctx:JavaParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by JavaParser#qualifiedName.
    def enterQualifiedName(self, ctx:JavaParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by JavaParser#qualifiedName.
    def exitQualifiedName(self, ctx:JavaParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by JavaParser#expression.
    def enterExpression(self, ctx:JavaParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#expression.
    def exitExpression(self, ctx:JavaParser.ExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:JavaParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:JavaParser.AssignmentExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#assignmentOp.
    def enterAssignmentOp(self, ctx:JavaParser.AssignmentOpContext):
        pass

    # Exit a parse tree produced by JavaParser#assignmentOp.
    def exitAssignmentOp(self, ctx:JavaParser.AssignmentOpContext):
        pass


    # Enter a parse tree produced by JavaParser#conditionalExpression.
    def enterConditionalExpression(self, ctx:JavaParser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#conditionalExpression.
    def exitConditionalExpression(self, ctx:JavaParser.ConditionalExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#logicalOrExpression.
    def enterLogicalOrExpression(self, ctx:JavaParser.LogicalOrExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#logicalOrExpression.
    def exitLogicalOrExpression(self, ctx:JavaParser.LogicalOrExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#logicalAndExpression.
    def enterLogicalAndExpression(self, ctx:JavaParser.LogicalAndExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#logicalAndExpression.
    def exitLogicalAndExpression(self, ctx:JavaParser.LogicalAndExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#bitwiseOrExpression.
    def enterBitwiseOrExpression(self, ctx:JavaParser.BitwiseOrExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#bitwiseOrExpression.
    def exitBitwiseOrExpression(self, ctx:JavaParser.BitwiseOrExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#bitwiseXorExpression.
    def enterBitwiseXorExpression(self, ctx:JavaParser.BitwiseXorExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#bitwiseXorExpression.
    def exitBitwiseXorExpression(self, ctx:JavaParser.BitwiseXorExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#bitwiseAndExpression.
    def enterBitwiseAndExpression(self, ctx:JavaParser.BitwiseAndExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#bitwiseAndExpression.
    def exitBitwiseAndExpression(self, ctx:JavaParser.BitwiseAndExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#equalityExpression.
    def enterEqualityExpression(self, ctx:JavaParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#equalityExpression.
    def exitEqualityExpression(self, ctx:JavaParser.EqualityExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#relationalExpression.
    def enterRelationalExpression(self, ctx:JavaParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#relationalExpression.
    def exitRelationalExpression(self, ctx:JavaParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#shiftExpression.
    def enterShiftExpression(self, ctx:JavaParser.ShiftExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#shiftExpression.
    def exitShiftExpression(self, ctx:JavaParser.ShiftExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:JavaParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:JavaParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:JavaParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:JavaParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#castExpression.
    def enterCastExpression(self, ctx:JavaParser.CastExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#castExpression.
    def exitCastExpression(self, ctx:JavaParser.CastExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#unaryExpression.
    def enterUnaryExpression(self, ctx:JavaParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#unaryExpression.
    def exitUnaryExpression(self, ctx:JavaParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#postfixExpression.
    def enterPostfixExpression(self, ctx:JavaParser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#postfixExpression.
    def exitPostfixExpression(self, ctx:JavaParser.PostfixExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#postfixOp.
    def enterPostfixOp(self, ctx:JavaParser.PostfixOpContext):
        pass

    # Exit a parse tree produced by JavaParser#postfixOp.
    def exitPostfixOp(self, ctx:JavaParser.PostfixOpContext):
        pass


    # Enter a parse tree produced by JavaParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:JavaParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:JavaParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#lambdaExpression.
    def enterLambdaExpression(self, ctx:JavaParser.LambdaExpressionContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaExpression.
    def exitLambdaExpression(self, ctx:JavaParser.LambdaExpressionContext):
        pass


    # Enter a parse tree produced by JavaParser#lambdaParams.
    def enterLambdaParams(self, ctx:JavaParser.LambdaParamsContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaParams.
    def exitLambdaParams(self, ctx:JavaParser.LambdaParamsContext):
        pass


    # Enter a parse tree produced by JavaParser#lambdaBody.
    def enterLambdaBody(self, ctx:JavaParser.LambdaBodyContext):
        pass

    # Exit a parse tree produced by JavaParser#lambdaBody.
    def exitLambdaBody(self, ctx:JavaParser.LambdaBodyContext):
        pass


    # Enter a parse tree produced by JavaParser#creator.
    def enterCreator(self, ctx:JavaParser.CreatorContext):
        pass

    # Exit a parse tree produced by JavaParser#creator.
    def exitCreator(self, ctx:JavaParser.CreatorContext):
        pass


    # Enter a parse tree produced by JavaParser#createdName.
    def enterCreatedName(self, ctx:JavaParser.CreatedNameContext):
        pass

    # Exit a parse tree produced by JavaParser#createdName.
    def exitCreatedName(self, ctx:JavaParser.CreatedNameContext):
        pass


    # Enter a parse tree produced by JavaParser#classCreatorRest.
    def enterClassCreatorRest(self, ctx:JavaParser.ClassCreatorRestContext):
        pass

    # Exit a parse tree produced by JavaParser#classCreatorRest.
    def exitClassCreatorRest(self, ctx:JavaParser.ClassCreatorRestContext):
        pass


    # Enter a parse tree produced by JavaParser#arrayCreatorRest.
    def enterArrayCreatorRest(self, ctx:JavaParser.ArrayCreatorRestContext):
        pass

    # Exit a parse tree produced by JavaParser#arrayCreatorRest.
    def exitArrayCreatorRest(self, ctx:JavaParser.ArrayCreatorRestContext):
        pass


    # Enter a parse tree produced by JavaParser#argumentList.
    def enterArgumentList(self, ctx:JavaParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by JavaParser#argumentList.
    def exitArgumentList(self, ctx:JavaParser.ArgumentListContext):
        pass



del JavaParser