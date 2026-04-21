# Generated from CPP.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CPPParser import CPPParser
else:
    from CPPParser import CPPParser

# This class defines a complete listener for a parse tree produced by CPPParser.
class CPPListener(ParseTreeListener):

    # Enter a parse tree produced by CPPParser#program.
    def enterProgram(self, ctx:CPPParser.ProgramContext):
        pass

    # Exit a parse tree produced by CPPParser#program.
    def exitProgram(self, ctx:CPPParser.ProgramContext):
        pass


    # Enter a parse tree produced by CPPParser#topLevel.
    def enterTopLevel(self, ctx:CPPParser.TopLevelContext):
        pass

    # Exit a parse tree produced by CPPParser#topLevel.
    def exitTopLevel(self, ctx:CPPParser.TopLevelContext):
        pass


    # Enter a parse tree produced by CPPParser#preprocessor.
    def enterPreprocessor(self, ctx:CPPParser.PreprocessorContext):
        pass

    # Exit a parse tree produced by CPPParser#preprocessor.
    def exitPreprocessor(self, ctx:CPPParser.PreprocessorContext):
        pass


    # Enter a parse tree produced by CPPParser#includeFile.
    def enterIncludeFile(self, ctx:CPPParser.IncludeFileContext):
        pass

    # Exit a parse tree produced by CPPParser#includeFile.
    def exitIncludeFile(self, ctx:CPPParser.IncludeFileContext):
        pass


    # Enter a parse tree produced by CPPParser#usingNamespace.
    def enterUsingNamespace(self, ctx:CPPParser.UsingNamespaceContext):
        pass

    # Exit a parse tree produced by CPPParser#usingNamespace.
    def exitUsingNamespace(self, ctx:CPPParser.UsingNamespaceContext):
        pass


    # Enter a parse tree produced by CPPParser#namespaceDecl.
    def enterNamespaceDecl(self, ctx:CPPParser.NamespaceDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#namespaceDecl.
    def exitNamespaceDecl(self, ctx:CPPParser.NamespaceDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#templateDecl.
    def enterTemplateDecl(self, ctx:CPPParser.TemplateDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#templateDecl.
    def exitTemplateDecl(self, ctx:CPPParser.TemplateDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#templateParamList.
    def enterTemplateParamList(self, ctx:CPPParser.TemplateParamListContext):
        pass

    # Exit a parse tree produced by CPPParser#templateParamList.
    def exitTemplateParamList(self, ctx:CPPParser.TemplateParamListContext):
        pass


    # Enter a parse tree produced by CPPParser#templateParam.
    def enterTemplateParam(self, ctx:CPPParser.TemplateParamContext):
        pass

    # Exit a parse tree produced by CPPParser#templateParam.
    def exitTemplateParam(self, ctx:CPPParser.TemplateParamContext):
        pass


    # Enter a parse tree produced by CPPParser#classDecl.
    def enterClassDecl(self, ctx:CPPParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#classDecl.
    def exitClassDecl(self, ctx:CPPParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#inheritanceList.
    def enterInheritanceList(self, ctx:CPPParser.InheritanceListContext):
        pass

    # Exit a parse tree produced by CPPParser#inheritanceList.
    def exitInheritanceList(self, ctx:CPPParser.InheritanceListContext):
        pass


    # Enter a parse tree produced by CPPParser#inheritanceSpec.
    def enterInheritanceSpec(self, ctx:CPPParser.InheritanceSpecContext):
        pass

    # Exit a parse tree produced by CPPParser#inheritanceSpec.
    def exitInheritanceSpec(self, ctx:CPPParser.InheritanceSpecContext):
        pass


    # Enter a parse tree produced by CPPParser#classMember.
    def enterClassMember(self, ctx:CPPParser.ClassMemberContext):
        pass

    # Exit a parse tree produced by CPPParser#classMember.
    def exitClassMember(self, ctx:CPPParser.ClassMemberContext):
        pass


    # Enter a parse tree produced by CPPParser#accessModifier.
    def enterAccessModifier(self, ctx:CPPParser.AccessModifierContext):
        pass

    # Exit a parse tree produced by CPPParser#accessModifier.
    def exitAccessModifier(self, ctx:CPPParser.AccessModifierContext):
        pass


    # Enter a parse tree produced by CPPParser#friendDecl.
    def enterFriendDecl(self, ctx:CPPParser.FriendDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#friendDecl.
    def exitFriendDecl(self, ctx:CPPParser.FriendDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#constructorDecl.
    def enterConstructorDecl(self, ctx:CPPParser.ConstructorDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#constructorDecl.
    def exitConstructorDecl(self, ctx:CPPParser.ConstructorDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#memberInitList.
    def enterMemberInitList(self, ctx:CPPParser.MemberInitListContext):
        pass

    # Exit a parse tree produced by CPPParser#memberInitList.
    def exitMemberInitList(self, ctx:CPPParser.MemberInitListContext):
        pass


    # Enter a parse tree produced by CPPParser#memberInitializer.
    def enterMemberInitializer(self, ctx:CPPParser.MemberInitializerContext):
        pass

    # Exit a parse tree produced by CPPParser#memberInitializer.
    def exitMemberInitializer(self, ctx:CPPParser.MemberInitializerContext):
        pass


    # Enter a parse tree produced by CPPParser#destructorDecl.
    def enterDestructorDecl(self, ctx:CPPParser.DestructorDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#destructorDecl.
    def exitDestructorDecl(self, ctx:CPPParser.DestructorDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#structDecl.
    def enterStructDecl(self, ctx:CPPParser.StructDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#structDecl.
    def exitStructDecl(self, ctx:CPPParser.StructDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#structMember.
    def enterStructMember(self, ctx:CPPParser.StructMemberContext):
        pass

    # Exit a parse tree produced by CPPParser#structMember.
    def exitStructMember(self, ctx:CPPParser.StructMemberContext):
        pass


    # Enter a parse tree produced by CPPParser#unionDecl.
    def enterUnionDecl(self, ctx:CPPParser.UnionDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#unionDecl.
    def exitUnionDecl(self, ctx:CPPParser.UnionDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#enumDecl.
    def enterEnumDecl(self, ctx:CPPParser.EnumDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#enumDecl.
    def exitEnumDecl(self, ctx:CPPParser.EnumDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#enumeratorList.
    def enterEnumeratorList(self, ctx:CPPParser.EnumeratorListContext):
        pass

    # Exit a parse tree produced by CPPParser#enumeratorList.
    def exitEnumeratorList(self, ctx:CPPParser.EnumeratorListContext):
        pass


    # Enter a parse tree produced by CPPParser#enumerator.
    def enterEnumerator(self, ctx:CPPParser.EnumeratorContext):
        pass

    # Exit a parse tree produced by CPPParser#enumerator.
    def exitEnumerator(self, ctx:CPPParser.EnumeratorContext):
        pass


    # Enter a parse tree produced by CPPParser#typedefDecl.
    def enterTypedefDecl(self, ctx:CPPParser.TypedefDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#typedefDecl.
    def exitTypedefDecl(self, ctx:CPPParser.TypedefDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#functionDecl.
    def enterFunctionDecl(self, ctx:CPPParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by CPPParser#functionDecl.
    def exitFunctionDecl(self, ctx:CPPParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by CPPParser#functionQualifier.
    def enterFunctionQualifier(self, ctx:CPPParser.FunctionQualifierContext):
        pass

    # Exit a parse tree produced by CPPParser#functionQualifier.
    def exitFunctionQualifier(self, ctx:CPPParser.FunctionQualifierContext):
        pass


    # Enter a parse tree produced by CPPParser#functionSuffix.
    def enterFunctionSuffix(self, ctx:CPPParser.FunctionSuffixContext):
        pass

    # Exit a parse tree produced by CPPParser#functionSuffix.
    def exitFunctionSuffix(self, ctx:CPPParser.FunctionSuffixContext):
        pass


    # Enter a parse tree produced by CPPParser#operatorName.
    def enterOperatorName(self, ctx:CPPParser.OperatorNameContext):
        pass

    # Exit a parse tree produced by CPPParser#operatorName.
    def exitOperatorName(self, ctx:CPPParser.OperatorNameContext):
        pass


    # Enter a parse tree produced by CPPParser#anyIdentifier.
    def enterAnyIdentifier(self, ctx:CPPParser.AnyIdentifierContext):
        pass

    # Exit a parse tree produced by CPPParser#anyIdentifier.
    def exitAnyIdentifier(self, ctx:CPPParser.AnyIdentifierContext):
        pass


    # Enter a parse tree produced by CPPParser#qualifiedName.
    def enterQualifiedName(self, ctx:CPPParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by CPPParser#qualifiedName.
    def exitQualifiedName(self, ctx:CPPParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by CPPParser#parameterList.
    def enterParameterList(self, ctx:CPPParser.ParameterListContext):
        pass

    # Exit a parse tree produced by CPPParser#parameterList.
    def exitParameterList(self, ctx:CPPParser.ParameterListContext):
        pass


    # Enter a parse tree produced by CPPParser#parameter.
    def enterParameter(self, ctx:CPPParser.ParameterContext):
        pass

    # Exit a parse tree produced by CPPParser#parameter.
    def exitParameter(self, ctx:CPPParser.ParameterContext):
        pass


    # Enter a parse tree produced by CPPParser#block.
    def enterBlock(self, ctx:CPPParser.BlockContext):
        pass

    # Exit a parse tree produced by CPPParser#block.
    def exitBlock(self, ctx:CPPParser.BlockContext):
        pass


    # Enter a parse tree produced by CPPParser#statement.
    def enterStatement(self, ctx:CPPParser.StatementContext):
        pass

    # Exit a parse tree produced by CPPParser#statement.
    def exitStatement(self, ctx:CPPParser.StatementContext):
        pass


    # Enter a parse tree produced by CPPParser#declaration.
    def enterDeclaration(self, ctx:CPPParser.DeclarationContext):
        pass

    # Exit a parse tree produced by CPPParser#declaration.
    def exitDeclaration(self, ctx:CPPParser.DeclarationContext):
        pass


    # Enter a parse tree produced by CPPParser#initDeclarator.
    def enterInitDeclarator(self, ctx:CPPParser.InitDeclaratorContext):
        pass

    # Exit a parse tree produced by CPPParser#initDeclarator.
    def exitInitDeclarator(self, ctx:CPPParser.InitDeclaratorContext):
        pass


    # Enter a parse tree produced by CPPParser#initializer.
    def enterInitializer(self, ctx:CPPParser.InitializerContext):
        pass

    # Exit a parse tree produced by CPPParser#initializer.
    def exitInitializer(self, ctx:CPPParser.InitializerContext):
        pass


    # Enter a parse tree produced by CPPParser#initializerList2.
    def enterInitializerList2(self, ctx:CPPParser.InitializerList2Context):
        pass

    # Exit a parse tree produced by CPPParser#initializerList2.
    def exitInitializerList2(self, ctx:CPPParser.InitializerList2Context):
        pass


    # Enter a parse tree produced by CPPParser#designatedInitializer.
    def enterDesignatedInitializer(self, ctx:CPPParser.DesignatedInitializerContext):
        pass

    # Exit a parse tree produced by CPPParser#designatedInitializer.
    def exitDesignatedInitializer(self, ctx:CPPParser.DesignatedInitializerContext):
        pass


    # Enter a parse tree produced by CPPParser#assignment.
    def enterAssignment(self, ctx:CPPParser.AssignmentContext):
        pass

    # Exit a parse tree produced by CPPParser#assignment.
    def exitAssignment(self, ctx:CPPParser.AssignmentContext):
        pass


    # Enter a parse tree produced by CPPParser#lvalue.
    def enterLvalue(self, ctx:CPPParser.LvalueContext):
        pass

    # Exit a parse tree produced by CPPParser#lvalue.
    def exitLvalue(self, ctx:CPPParser.LvalueContext):
        pass


    # Enter a parse tree produced by CPPParser#assignmentOp.
    def enterAssignmentOp(self, ctx:CPPParser.AssignmentOpContext):
        pass

    # Exit a parse tree produced by CPPParser#assignmentOp.
    def exitAssignmentOp(self, ctx:CPPParser.AssignmentOpContext):
        pass


    # Enter a parse tree produced by CPPParser#expressionStatement.
    def enterExpressionStatement(self, ctx:CPPParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#expressionStatement.
    def exitExpressionStatement(self, ctx:CPPParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#ifStatement.
    def enterIfStatement(self, ctx:CPPParser.IfStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#ifStatement.
    def exitIfStatement(self, ctx:CPPParser.IfStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#whileStatement.
    def enterWhileStatement(self, ctx:CPPParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#whileStatement.
    def exitWhileStatement(self, ctx:CPPParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#doWhileStatement.
    def enterDoWhileStatement(self, ctx:CPPParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#doWhileStatement.
    def exitDoWhileStatement(self, ctx:CPPParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#forStatement.
    def enterForStatement(self, ctx:CPPParser.ForStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#forStatement.
    def exitForStatement(self, ctx:CPPParser.ForStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#rangeForStatement.
    def enterRangeForStatement(self, ctx:CPPParser.RangeForStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#rangeForStatement.
    def exitRangeForStatement(self, ctx:CPPParser.RangeForStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#forInit.
    def enterForInit(self, ctx:CPPParser.ForInitContext):
        pass

    # Exit a parse tree produced by CPPParser#forInit.
    def exitForInit(self, ctx:CPPParser.ForInitContext):
        pass


    # Enter a parse tree produced by CPPParser#forUpdate.
    def enterForUpdate(self, ctx:CPPParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by CPPParser#forUpdate.
    def exitForUpdate(self, ctx:CPPParser.ForUpdateContext):
        pass


    # Enter a parse tree produced by CPPParser#switchStatement.
    def enterSwitchStatement(self, ctx:CPPParser.SwitchStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#switchStatement.
    def exitSwitchStatement(self, ctx:CPPParser.SwitchStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#caseStatement.
    def enterCaseStatement(self, ctx:CPPParser.CaseStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#caseStatement.
    def exitCaseStatement(self, ctx:CPPParser.CaseStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#tryStatement.
    def enterTryStatement(self, ctx:CPPParser.TryStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#tryStatement.
    def exitTryStatement(self, ctx:CPPParser.TryStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#catchClause.
    def enterCatchClause(self, ctx:CPPParser.CatchClauseContext):
        pass

    # Exit a parse tree produced by CPPParser#catchClause.
    def exitCatchClause(self, ctx:CPPParser.CatchClauseContext):
        pass


    # Enter a parse tree produced by CPPParser#throwStatement.
    def enterThrowStatement(self, ctx:CPPParser.ThrowStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#throwStatement.
    def exitThrowStatement(self, ctx:CPPParser.ThrowStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#coutStatement.
    def enterCoutStatement(self, ctx:CPPParser.CoutStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#coutStatement.
    def exitCoutStatement(self, ctx:CPPParser.CoutStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#cinStatement.
    def enterCinStatement(self, ctx:CPPParser.CinStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#cinStatement.
    def exitCinStatement(self, ctx:CPPParser.CinStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#returnStatement.
    def enterReturnStatement(self, ctx:CPPParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#returnStatement.
    def exitReturnStatement(self, ctx:CPPParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#breakStatement.
    def enterBreakStatement(self, ctx:CPPParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#breakStatement.
    def exitBreakStatement(self, ctx:CPPParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#continueStatement.
    def enterContinueStatement(self, ctx:CPPParser.ContinueStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#continueStatement.
    def exitContinueStatement(self, ctx:CPPParser.ContinueStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#gotoStatement.
    def enterGotoStatement(self, ctx:CPPParser.GotoStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#gotoStatement.
    def exitGotoStatement(self, ctx:CPPParser.GotoStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#labelStatement.
    def enterLabelStatement(self, ctx:CPPParser.LabelStatementContext):
        pass

    # Exit a parse tree produced by CPPParser#labelStatement.
    def exitLabelStatement(self, ctx:CPPParser.LabelStatementContext):
        pass


    # Enter a parse tree produced by CPPParser#typeSpecifier.
    def enterTypeSpecifier(self, ctx:CPPParser.TypeSpecifierContext):
        pass

    # Exit a parse tree produced by CPPParser#typeSpecifier.
    def exitTypeSpecifier(self, ctx:CPPParser.TypeSpecifierContext):
        pass


    # Enter a parse tree produced by CPPParser#typeArgList.
    def enterTypeArgList(self, ctx:CPPParser.TypeArgListContext):
        pass

    # Exit a parse tree produced by CPPParser#typeArgList.
    def exitTypeArgList(self, ctx:CPPParser.TypeArgListContext):
        pass


    # Enter a parse tree produced by CPPParser#typeQualifier.
    def enterTypeQualifier(self, ctx:CPPParser.TypeQualifierContext):
        pass

    # Exit a parse tree produced by CPPParser#typeQualifier.
    def exitTypeQualifier(self, ctx:CPPParser.TypeQualifierContext):
        pass


    # Enter a parse tree produced by CPPParser#baseType.
    def enterBaseType(self, ctx:CPPParser.BaseTypeContext):
        pass

    # Exit a parse tree produced by CPPParser#baseType.
    def exitBaseType(self, ctx:CPPParser.BaseTypeContext):
        pass


    # Enter a parse tree produced by CPPParser#expression.
    def enterExpression(self, ctx:CPPParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#expression.
    def exitExpression(self, ctx:CPPParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:CPPParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:CPPParser.AssignmentExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#conditionalExpression.
    def enterConditionalExpression(self, ctx:CPPParser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#conditionalExpression.
    def exitConditionalExpression(self, ctx:CPPParser.ConditionalExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#logicalOrExpression.
    def enterLogicalOrExpression(self, ctx:CPPParser.LogicalOrExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#logicalOrExpression.
    def exitLogicalOrExpression(self, ctx:CPPParser.LogicalOrExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#logicalAndExpression.
    def enterLogicalAndExpression(self, ctx:CPPParser.LogicalAndExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#logicalAndExpression.
    def exitLogicalAndExpression(self, ctx:CPPParser.LogicalAndExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#bitwiseOrExpression.
    def enterBitwiseOrExpression(self, ctx:CPPParser.BitwiseOrExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#bitwiseOrExpression.
    def exitBitwiseOrExpression(self, ctx:CPPParser.BitwiseOrExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#bitwiseXorExpression.
    def enterBitwiseXorExpression(self, ctx:CPPParser.BitwiseXorExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#bitwiseXorExpression.
    def exitBitwiseXorExpression(self, ctx:CPPParser.BitwiseXorExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#bitwiseAndExpression.
    def enterBitwiseAndExpression(self, ctx:CPPParser.BitwiseAndExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#bitwiseAndExpression.
    def exitBitwiseAndExpression(self, ctx:CPPParser.BitwiseAndExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#equalityExpression.
    def enterEqualityExpression(self, ctx:CPPParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#equalityExpression.
    def exitEqualityExpression(self, ctx:CPPParser.EqualityExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#relationalExpression.
    def enterRelationalExpression(self, ctx:CPPParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#relationalExpression.
    def exitRelationalExpression(self, ctx:CPPParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#shiftExpression.
    def enterShiftExpression(self, ctx:CPPParser.ShiftExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#shiftExpression.
    def exitShiftExpression(self, ctx:CPPParser.ShiftExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:CPPParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:CPPParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:CPPParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:CPPParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#castExpression.
    def enterCastExpression(self, ctx:CPPParser.CastExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#castExpression.
    def exitCastExpression(self, ctx:CPPParser.CastExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#unaryExpression.
    def enterUnaryExpression(self, ctx:CPPParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#unaryExpression.
    def exitUnaryExpression(self, ctx:CPPParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#postfixExpression.
    def enterPostfixExpression(self, ctx:CPPParser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#postfixExpression.
    def exitPostfixExpression(self, ctx:CPPParser.PostfixExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#postfixOp.
    def enterPostfixOp(self, ctx:CPPParser.PostfixOpContext):
        pass

    # Exit a parse tree produced by CPPParser#postfixOp.
    def exitPostfixOp(self, ctx:CPPParser.PostfixOpContext):
        pass


    # Enter a parse tree produced by CPPParser#lambdaExpression.
    def enterLambdaExpression(self, ctx:CPPParser.LambdaExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#lambdaExpression.
    def exitLambdaExpression(self, ctx:CPPParser.LambdaExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#captureList.
    def enterCaptureList(self, ctx:CPPParser.CaptureListContext):
        pass

    # Exit a parse tree produced by CPPParser#captureList.
    def exitCaptureList(self, ctx:CPPParser.CaptureListContext):
        pass


    # Enter a parse tree produced by CPPParser#captureItem.
    def enterCaptureItem(self, ctx:CPPParser.CaptureItemContext):
        pass

    # Exit a parse tree produced by CPPParser#captureItem.
    def exitCaptureItem(self, ctx:CPPParser.CaptureItemContext):
        pass


    # Enter a parse tree produced by CPPParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:CPPParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by CPPParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:CPPParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by CPPParser#argumentList.
    def enterArgumentList(self, ctx:CPPParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by CPPParser#argumentList.
    def exitArgumentList(self, ctx:CPPParser.ArgumentListContext):
        pass



del CPPParser