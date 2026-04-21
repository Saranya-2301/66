grammar Java;

// ---------------- LEXER ----------------

DOT         : '.';
SEMI        : ';';
COMMA       : ',';
LPAREN      : '(';
RPAREN      : ')';
LBRACE      : '{';
RBRACE      : '}';
LBRACKET    : '[';
RBRACKET    : ']';
COLON       : ':';
DOUBLE_COLON: '::';
ELLIPSIS    : '...';
AT          : '@';
QUESTION    : '?';
STAR        : '*';

// Operators
SHIFT_LEFT    : '<<';
SHIFT_RIGHT   : '>>';
USHIFT_RIGHT  : '>>>';
GE            : '>=';
LE            : '<=';
EQ            : '==';
NEQ           : '!=';
AND           : '&&';
OR            : '||';
NOT           : '!';
ADD_ASSIGN    : '+=';
SUB_ASSIGN    : '-=';
MUL_ASSIGN    : '*=';
DIV_ASSIGN    : '/=';
MOD_ASSIGN    : '%=';
AND_ASSIGN    : '&=';
OR_ASSIGN     : '|=';
XOR_ASSIGN    : '^=';
LSHIFT_ASSIGN : '<<=';
RSHIFT_ASSIGN : '>>=';
URSHIFT_ASSIGN: '>>>=';
ASSIGN        : '=';
INC           : '++';
DEC           : '--';
PLUS          : '+';
MINUS         : '-';
DIV           : '/';
MOD           : '%';
BIT_AND       : '&';
BIT_OR        : '|';
BIT_XOR       : '^';
BIT_NOT       : '~';
ARROW         : '->';
LT            : '<';
GT            : '>';

// Keywords
PACKAGE     : 'package';
IMPORT      : 'import';
CLASS       : 'class';
INTERFACE   : 'interface';
ENUM        : 'enum';
EXTENDS     : 'extends';
IMPLEMENTS  : 'implements';
ABSTRACT    : 'abstract';
FINAL       : 'final';
STATIC      : 'static';
STRICTFP    : 'strictfp';
NATIVE      : 'native';
SYNCHRONIZED: 'synchronized';
TRANSIENT   : 'transient';
VOLATILE    : 'volatile';
PUBLIC      : 'public';
PRIVATE     : 'private';
PROTECTED   : 'protected';
NEW         : 'new';
THIS        : 'this';
SUPER       : 'super';
INSTANCEOF  : 'instanceof';
VOID        : 'void';
IF          : 'if';
ELSE        : 'else';
WHILE       : 'while';
DO          : 'do';
FOR         : 'for';
SWITCH      : 'switch';
CASE        : 'case';
DEFAULT     : 'default';
BREAK       : 'break';
CONTINUE    : 'continue';
RETURN      : 'return';
THROW       : 'throw';
THROWS      : 'throws';
TRY         : 'try';
CATCH       : 'catch';
FINALLY     : 'finally';
ASSERT      : 'assert';
GOTO        : 'goto';
SEALED      : 'sealed';
PERMITS     : 'permits';
RECORD      : 'record';
YIELD       : 'yield';

// Types
INT         : 'int';
LONG        : 'long';
SHORT       : 'short';
BYTE        : 'byte';
FLOAT       : 'float';
DOUBLE      : 'double';
CHAR        : 'char';
BOOLEAN     : 'boolean';
VAR         : 'var';

// Literals
TRUE        : 'true';
FALSE       : 'false';
NULL_LIT    : 'null';

// Number Literals
HEX_LITERAL    : '0' [xX] [0-9a-fA-F] ([0-9a-fA-F_]* [0-9a-fA-F])? [lL]?;
OCTAL_LITERAL  : '0' [0-7]+ [lL]?;
BINARY_LITERAL : '0' [bB] [01]+ [lL]?;
FLOAT_LITERAL  : [0-9]* '.' [0-9]+ ([eE] [+-]? [0-9]+)? [fFdD]?
               | [0-9]+ '.' ([eE] [+-]? [0-9]+)? [fFdD]?
               | [0-9]+ [eE] [+-]? [0-9]+ [fFdD]?
               | [0-9]+ [fFdD]
               ;
INTEGER_LITERAL: [0-9] ([0-9_]* [0-9])? [lL]?;
CHAR_LITERAL   : '\'' (~['\\\r\n] | '\\' .) '\'';
STRING_LITERAL : '"' (~["\\\r\n] | '\\' .)* '"';
TEXT_BLOCK     : '"""' .*? '"""';

// Identifier MUST be after all keywords
IDENTIFIER  : [a-zA-Z_$][a-zA-Z0-9_$]*;

// Whitespace & Comments
WS              : [ \t\r\n]+    -> skip;
LINE_COMMENT    : '//' .*? '\n' -> skip;
BLOCK_COMMENT   : '/*' .*? '*/' -> skip;
JAVADOC_COMMENT : '/**' .*? '*/'-> skip;

// ================================================
// ---------------- PARSER ----------------
// ================================================

program
    : packageDeclaration?
      importDeclaration*
      typeDeclaration+
      EOF
    ;

// ---------------- PACKAGE ----------------
packageDeclaration
    : annotation* PACKAGE qualifiedName SEMI
    ;

// ---------------- IMPORT ----------------
importDeclaration
    : IMPORT STATIC? qualifiedName (DOT STAR)? SEMI
    ;

// ---------------- TYPE DECLARATIONS ----------------
typeDeclaration
    : classDeclaration
    | interfaceDeclaration
    | enumDeclaration
    | recordDeclaration
    | annotationDeclaration
    | sealedClassDeclaration
    ;

// ---------------- ANNOTATIONS ----------------
annotation
    : AT qualifiedName (LPAREN annotationArgs? RPAREN)?
    ;

annotationArgs
    : annotationArg (COMMA annotationArg)*
    ;

annotationArg
    : IDENTIFIER ASSIGN elementValue
    | elementValue
    ;

elementValue
    : expression
    | annotation
    | LBRACE (elementValue (COMMA elementValue)*)? COMMA? RBRACE
    ;

annotationDeclaration
    : modifier* AT INTERFACE IDENTIFIER LBRACE annotationMember* RBRACE
    ;

annotationMember
    : modifier* typeType IDENTIFIER LPAREN RPAREN (DEFAULT elementValue)? SEMI
    | modifier* typeType IDENTIFIER SEMI
    ;

// ---------------- CLASS ----------------
classDeclaration
    : annotation* modifier* CLASS IDENTIFIER
      typeParameters?
      (EXTENDS typeType)?
      (IMPLEMENTS typeList)?
      (PERMITS typeList)?
      LBRACE classBody RBRACE
    ;

classBody
    : classMember*
    ;

classMember
    : fieldDeclaration
    | methodDeclaration
    | constructorDeclaration
    | staticInitializer
    | instanceInitializer
    | classDeclaration
    | interfaceDeclaration
    | enumDeclaration
    | recordDeclaration
    ;

staticInitializer
    : STATIC block
    ;

instanceInitializer
    : block
    ;

// ---------------- SEALED CLASS ----------------
sealedClassDeclaration
    : annotation* modifier* SEALED CLASS IDENTIFIER
      typeParameters?
      (EXTENDS typeType)?
      (IMPLEMENTS typeList)?
      PERMITS typeList
      LBRACE classBody RBRACE
    ;

// ---------------- RECORD ----------------
recordDeclaration
    : annotation* modifier* RECORD IDENTIFIER
      LPAREN recordComponentList? RPAREN
      (IMPLEMENTS typeList)?
      LBRACE classMember* RBRACE
    ;

recordComponentList
    : recordComponent (COMMA recordComponent)*
    ;

recordComponent
    : annotation* typeType IDENTIFIER
    ;

// ---------------- INTERFACE ----------------
interfaceDeclaration
    : annotation* modifier* INTERFACE IDENTIFIER
      typeParameters?
      (EXTENDS typeList)?
      LBRACE interfaceMember* RBRACE
    ;

interfaceMember
    : interfaceMethodDeclaration
    | fieldDeclaration
    | classDeclaration
    | interfaceDeclaration
    ;

interfaceMethodDeclaration
    : annotation* modifier* typeParameters?
      typeType IDENTIFIER
      LPAREN parameterList? RPAREN
      (THROWS typeList)?
      (block | SEMI)
    ;

// ---------------- ENUM ----------------
enumDeclaration
    : annotation* modifier* ENUM IDENTIFIER
      (IMPLEMENTS typeList)?
      LBRACE enumeratorList COMMA?
      (SEMI classMember*)? RBRACE
    ;

enumeratorList
    : enumerator (COMMA enumerator)*
    ;

enumerator
    : annotation* IDENTIFIER (LPAREN argumentList? RPAREN)?
      (LBRACE classMember* RBRACE)?
    ;

// ---------------- MODIFIERS ----------------
modifier
    : PUBLIC | PRIVATE | PROTECTED
    | STATIC | FINAL | ABSTRACT
    | SYNCHRONIZED | NATIVE | STRICTFP
    | TRANSIENT | VOLATILE | SEALED
    | annotation
    ;

// ---------------- TYPE PARAMETERS ----------------
typeParameters
    : LT typeParameter (COMMA typeParameter)* GT
    ;

typeParameter
    : annotation* IDENTIFIER (EXTENDS typeBound)?
    ;

typeBound
    : typeType (BIT_AND typeType)*
    ;

// ---------------- TYPE ----------------
typeType
    : annotation* (primitiveType | qualifiedName) typeArguments?
      (LBRACKET RBRACKET)*
    ;

primitiveType
    : INT | LONG | SHORT | BYTE
    | FLOAT | DOUBLE | CHAR | BOOLEAN | VOID
    ;

typeArguments
    : LT typeArgument (COMMA typeArgument)* GT
    | LT GT
    ;

typeArgument
    : typeType
    | QUESTION ((EXTENDS | SUPER) typeType)?
    ;

typeList
    : typeType (COMMA typeType)*
    ;

// ---------------- FIELDS ----------------
fieldDeclaration
    : annotation* modifier* typeType
      variableDeclarator (COMMA variableDeclarator)* SEMI
    ;

variableDeclarator
    : IDENTIFIER (LBRACKET RBRACKET)*
      (ASSIGN variableInitializer)?
    ;

variableInitializer
    : arrayInitializer
    | expression
    ;

arrayInitializer
    : LBRACE (variableInitializer (COMMA variableInitializer)*)? COMMA? RBRACE
    ;

// ---------------- METHODS ----------------
methodDeclaration
    : annotation* modifier* typeParameters?
      typeType IDENTIFIER
      LPAREN parameterList? RPAREN
      (LBRACKET RBRACKET)*
      (THROWS typeList)?
      (block | SEMI)
    ;

// ---------------- CONSTRUCTOR ----------------
constructorDeclaration
    : annotation* modifier* typeParameters?
      IDENTIFIER LPAREN parameterList? RPAREN
      (THROWS typeList)?
      block
    ;

// ---------------- PARAMETERS ----------------
parameterList
    : parameter (COMMA parameter)*
    ;

parameter
    : annotation* modifier* typeType ELLIPSIS? IDENTIFIER
      (LBRACKET RBRACKET)*
    ;

// ---------------- BLOCK ----------------
block
    : LBRACE blockStatement* RBRACE
    ;

blockStatement
    : localVariableDeclaration
    | statement
    | classDeclaration
    | enumDeclaration
    ;

// ---------------- LOCAL VARIABLE ----------------
localVariableDeclaration
    : annotation* modifier* (typeType | VAR)
      variableDeclarator (COMMA variableDeclarator)* SEMI
    ;

// ---------------- STATEMENTS ----------------
statement
    : block
    | ifStatement
    | whileStatement
    | doWhileStatement
    | forStatement
    | enhancedForStatement
    | switchStatement
    | returnStatement
    | throwStatement
    | tryStatement
    | assertStatement
    | breakStatement
    | continueStatement
    | gotoStatement
    | synchronizedStatement
    | yieldStatement
    | expressionStatement
    | labelStatement
    | SEMI
    ;

// ---------------- IF ----------------
ifStatement
    : IF LPAREN expression RPAREN statement
      (ELSE statement)?
    ;

// ---------------- WHILE ----------------
whileStatement
    : WHILE LPAREN expression RPAREN statement
    ;

// ---------------- DO WHILE ----------------
doWhileStatement
    : DO statement WHILE LPAREN expression RPAREN SEMI
    ;

// ---------------- FOR ----------------
forStatement
    : FOR LPAREN forInit? SEMI expression? SEMI forUpdate? RPAREN statement
    ;

forInit
    : localVariableDeclaration
    | expressionList
    ;

forUpdate
    : expressionList
    ;

// ---------------- ENHANCED FOR ----------------
enhancedForStatement
    : FOR LPAREN annotation* modifier* (typeType | VAR)
      IDENTIFIER COLON expression RPAREN statement
    ;

// ---------------- SWITCH ----------------
switchStatement
    : SWITCH LPAREN expression RPAREN
      LBRACE switchCase* RBRACE
    ;

switchCase
    : CASE expression COLON blockStatement*
    | CASE expression ARROW statement
    | CASE expression (COMMA expression)* ARROW statement
    | DEFAULT COLON blockStatement*
    | DEFAULT ARROW statement
    ;

// ---------------- TRY ----------------
tryStatement
    : TRY resourceSpec? block
      catchClause*
      finallyClause?
    ;

resourceSpec
    : LPAREN resource (SEMI resource)* SEMI? RPAREN
    ;

resource
    : modifier* typeType IDENTIFIER ASSIGN expression
    ;

catchClause
    : CATCH LPAREN modifier* catchType IDENTIFIER RPAREN block
    ;

catchType
    : typeType (BIT_OR typeType)*
    ;

finallyClause
    : FINALLY block
    ;

// ---------------- ASSERT ----------------
assertStatement
    : ASSERT expression (COLON expression)? SEMI
    ;

// ---------------- SYNCHRONIZED ----------------
synchronizedStatement
    : SYNCHRONIZED LPAREN expression RPAREN block
    ;

// ---------------- YIELD (Java 14+) ----------------
yieldStatement
    : YIELD expression SEMI
    ;

// ---------------- JUMP STATEMENTS ----------------
returnStatement   : RETURN expression? SEMI ;
throwStatement    : THROW expression SEMI ;
breakStatement    : BREAK IDENTIFIER? SEMI ;
continueStatement : CONTINUE IDENTIFIER? SEMI ;
gotoStatement     : GOTO IDENTIFIER SEMI ;
labelStatement    : IDENTIFIER COLON statement ;
expressionStatement : expression SEMI ;
expressionList    : expression (COMMA expression)* ;

// ---------------- QUALIFIED NAME ----------------
qualifiedName
    : IDENTIFIER (DOT IDENTIFIER)*
    ;

// ---------------- EXPRESSIONS ----------------

expression
    : assignmentExpression
    ;

assignmentExpression
    : conditionalExpression
    | unaryExpression assignmentOp assignmentExpression
    ;

assignmentOp
    : ASSIGN | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN
    | DIV_ASSIGN | MOD_ASSIGN | AND_ASSIGN | OR_ASSIGN
    | XOR_ASSIGN | LSHIFT_ASSIGN | RSHIFT_ASSIGN | URSHIFT_ASSIGN
    ;

conditionalExpression
    : logicalOrExpression (QUESTION expression COLON expression)?
    ;

logicalOrExpression
    : logicalAndExpression (OR logicalAndExpression)*
    ;

logicalAndExpression
    : bitwiseOrExpression (AND bitwiseOrExpression)*
    ;

bitwiseOrExpression
    : bitwiseXorExpression (BIT_OR bitwiseXorExpression)*
    ;

bitwiseXorExpression
    : bitwiseAndExpression (BIT_XOR bitwiseAndExpression)*
    ;

bitwiseAndExpression
    : equalityExpression (BIT_AND equalityExpression)*
    ;

equalityExpression
    : relationalExpression ((EQ | NEQ) relationalExpression)*
    ;

relationalExpression
    : shiftExpression ((LT | GT | LE | GE) shiftExpression)*
    | shiftExpression INSTANCEOF typeType
    ;

shiftExpression
    : additiveExpression
      ((SHIFT_LEFT | SHIFT_RIGHT | USHIFT_RIGHT) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : castExpression ((STAR | DIV | MOD) castExpression)*
    ;

castExpression
    : LPAREN typeType RPAREN castExpression
    | unaryExpression
    ;

unaryExpression
    : NOT         unaryExpression
    | BIT_NOT     unaryExpression
    | MINUS       unaryExpression
    | PLUS        unaryExpression
    | INC         unaryExpression
    | DEC         unaryExpression
    | postfixExpression
    ;

postfixExpression
    : primaryExpression postfixOp*
    ;

postfixOp
    : INC
    | DEC
    | (DOT IDENTIFIER)+
    | (DOT IDENTIFIER)+ LPAREN argumentList? RPAREN
    | DOT NEW typeType LPAREN argumentList? RPAREN
    | DOT THIS
    | DOT SUPER
    | LBRACKET expression RBRACKET
    | LPAREN argumentList? RPAREN
    | DOUBLE_COLON IDENTIFIER
    | DOUBLE_COLON NEW
    ;

primaryExpression
    : INTEGER_LITERAL
    | HEX_LITERAL
    | OCTAL_LITERAL
    | BINARY_LITERAL
    | FLOAT_LITERAL
    | CHAR_LITERAL
    | STRING_LITERAL
    | TEXT_BLOCK
    | TRUE
    | FALSE
    | NULL_LIT
    | THIS
    | SUPER
    | IDENTIFIER
    | typeType DOT CLASS
    | VOID DOT CLASS
    | NEW creator
    | LPAREN expression RPAREN
    | lambdaExpression
    ;

// ---------------- LAMBDA ----------------
lambdaExpression
    : lambdaParams ARROW lambdaBody
    ;

lambdaParams
    : IDENTIFIER
    | LPAREN RPAREN
    | LPAREN IDENTIFIER (COMMA IDENTIFIER)* RPAREN
    | LPAREN parameterList RPAREN
    ;

lambdaBody
    : expression
    | block
    ;

// ---------------- NEW / CREATOR ----------------
creator
    : createdName classCreatorRest
    | createdName arrayCreatorRest
    ;

createdName
    : IDENTIFIER typeArguments?
      (DOT IDENTIFIER typeArguments?)*
    | primitiveType
    ;

classCreatorRest
    : LPAREN argumentList? RPAREN
      (LBRACE classMember* RBRACE)?
    ;

arrayCreatorRest
    : LBRACKET RBRACKET (LBRACKET RBRACKET)* arrayInitializer
    | (LBRACKET expression RBRACKET)+ (LBRACKET RBRACKET)*
    ;

// ---------------- ARGUMENT LIST ----------------
argumentList
    : expression (COMMA expression)*
    ;