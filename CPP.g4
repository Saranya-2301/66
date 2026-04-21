grammar CPP;

// ---------------- LEXER ----------------
HASH        : '#';
INCLUDE     : 'include';
DEFINE      : 'define';
PRAGMA      : 'pragma';
UNDEF       : 'undef';
IFDEF       : 'ifdef';
IFNDEF      : 'ifndef';
ENDIF       : 'endif';
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

// Operators
SHIFT_LEFT    : '<<';
SHIFT_RIGHT   : '>>';
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
ASSIGN        : '=';
INC           : '++';
DEC           : '--';
PLUS          : '+';
MINUS         : '-';
MUL           : '*';
DIV           : '/';
MOD           : '%';
BIT_AND       : '&';
BIT_OR        : '|';
BIT_XOR       : '^';
BIT_NOT       : '~';
ARROW         : '->';
QUESTION      : '?';
LT            : '<';
GT            : '>';

CLASS       : 'class';
STRUCT      : 'struct';
UNION       : 'union';
ENUM        : 'enum';
NAMESPACE   : 'namespace';
USING       : 'using';
TEMPLATE    : 'template';
TYPENAME    : 'typename';
OPERATOR    : 'operator';
PUBLIC      : 'public';
PRIVATE     : 'private';
PROTECTED   : 'protected';
VIRTUAL     : 'virtual';
OVERRIDE    : 'override';
FINAL       : 'final';
EXPLICIT    : 'explicit';
FRIEND      : 'friend';
INLINE      : 'inline';
STATIC      : 'static';
EXTERN      : 'extern';
CONST       : 'const';
CONSTEXPR   : 'constexpr';
VOLATILE    : 'volatile';
MUTABLE     : 'mutable';
REGISTER    : 'register';
AUTO        : 'auto';
TYPEDEF     : 'typedef';
NEW         : 'new';
DELETE      : 'delete';
THIS        : 'this';
NULLPTR     : 'nullptr';
SIZEOF      : 'sizeof';
THROW       : 'throw';
TRY         : 'try';
CATCH       : 'catch';
INT         : 'int';
FLOAT       : 'float';
DOUBLE      : 'double';
CHAR        : 'char';
VOID        : 'void';
BOOL        : 'bool';
SHORT       : 'short';
LONG        : 'long';
UNSIGNED    : 'unsigned';
SIGNED      : 'signed';
WCHAR       : 'wchar_t';
STRING_TYPE : 'string';
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
GOTO        : 'goto';
RETURN      : 'return';
COUT        : 'cout';
CIN         : 'cin';
ENDL        : 'endl';

// Literals
NULL_LIT    : 'NULL';
BOOL_TRUE   : 'true';
BOOL_FALSE  : 'false';

// Number Literals
HEX_NUMBER   : '0x' [0-9a-fA-F]+ [uUlL]*;
OCTAL_NUMBER : '0' [0-7]+ [uUlL]*;
FLOAT_NUMBER : [0-9]* '.' [0-9]+ ([eE] [+-]? [0-9]+)? [fFlL]?
             | [0-9]+ '.' ([eE] [+-]? [0-9]+)? [fFlL]?
             | [0-9]+ [eE] [+-]? [0-9]+ [fFlL]?
             ;
NUMBER       : [0-9]+ [uUlL]*;
CHAR_LITERAL : '\'' (~['\\\r\n] | '\\' .) '\'';
STRING       : '"' (~["\\\r\n] | '\\' .)* '"';

IDENTIFIER  : [a-zA-Z_][a-zA-Z0-9_]*;

// Whitespace & Comments
WS            : [ \t\r\n]+    -> skip;
LINE_COMMENT  : '//' .*? '\n' -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;

// ---------------- PARSER ----------------

program
    : topLevel* EOF
    ;

topLevel
    : preprocessor
    | usingNamespace
    | namespaceDecl
    | classDecl
    | structDecl
    | unionDecl
    | enumDecl
    | typedefDecl
    | templateDecl
    | functionDecl
    | declaration
    ;

// ---------------- PREPROCESSOR ----------------
preprocessor
    : HASH INCLUDE LT includeFile GT
    | HASH INCLUDE STRING
    | HASH DEFINE IDENTIFIER expression
    | HASH DEFINE IDENTIFIER STRING
    | HASH DEFINE IDENTIFIER
    | HASH UNDEF  IDENTIFIER
    | HASH PRAGMA IDENTIFIER
    | HASH IFDEF  IDENTIFIER
    | HASH IFNDEF IDENTIFIER
    | HASH ENDIF
    ;

includeFile
    : IDENTIFIER (DOT IDENTIFIER)*
    | IDENTIFIER (DIV IDENTIFIER)* (DOT IDENTIFIER)?
    ;

// ---------------- NAMESPACE ----------------
usingNamespace
    : USING NAMESPACE qualifiedName SEMI
    ;

namespaceDecl
    : NAMESPACE IDENTIFIER LBRACE topLevel* RBRACE
    ;

// ---------------- TEMPLATE ----------------
templateDecl
    : TEMPLATE LT templateParamList GT
      (classDecl | functionDecl | structDecl)
    ;

templateParamList
    : templateParam (COMMA templateParam)*
    ;

templateParam
    : TYPENAME IDENTIFIER (ASSIGN typeSpecifier)?
    | CLASS    IDENTIFIER (ASSIGN typeSpecifier)?
    | typeSpecifier IDENTIFIER (ASSIGN expression)?
    ;

// ---------------- CLASS ----------------
classDecl
    : CLASS IDENTIFIER (COLON inheritanceList)?
      LBRACE classMember* RBRACE SEMI?
    ;

inheritanceList
    : inheritanceSpec (COMMA inheritanceSpec)*
    ;

inheritanceSpec
    : (PUBLIC | PRIVATE | PROTECTED)? qualifiedName
    ;

classMember
    : accessModifier
    | constructorDecl
    | destructorDecl
    | functionDecl
    | declaration
    | friendDecl
    | usingNamespace
    ;

accessModifier
    : (PUBLIC | PRIVATE | PROTECTED) COLON
    ;

friendDecl
    : FRIEND CLASS IDENTIFIER SEMI
    | FRIEND functionDecl
    ;

// ---------------- CONSTRUCTOR ----------------
constructorDecl
    : EXPLICIT? qualifiedName LPAREN parameterList? RPAREN
      (COLON memberInitList)? block
    ;

memberInitList
    : memberInitializer (COMMA memberInitializer)*
    ;

memberInitializer
    : IDENTIFIER LPAREN argumentList? RPAREN
    | IDENTIFIER LBRACE argumentList? RBRACE
    ;

destructorDecl
    : VIRTUAL? BIT_NOT IDENTIFIER LPAREN RPAREN block
    | VIRTUAL? qualifiedName DOUBLE_COLON BIT_NOT IDENTIFIER LPAREN RPAREN block
    ;

// ---------------- STRUCT ----------------
structDecl
    : STRUCT IDENTIFIER? (COLON inheritanceList)?
      LBRACE structMember* RBRACE SEMI?
    ;

structMember
    : accessModifier
    | declaration
    | functionDecl
    | constructorDecl
    | destructorDecl
    ;

// ---------------- UNION ----------------
unionDecl
    : UNION IDENTIFIER? LBRACE structMember* RBRACE SEMI?
    ;

// ---------------- ENUM ----------------
enumDecl
    : ENUM CLASS? IDENTIFIER (COLON typeSpecifier)?
      LBRACE enumeratorList COMMA? RBRACE SEMI
    ;

enumeratorList
    : enumerator (COMMA enumerator)*
    ;

enumerator
    : IDENTIFIER (ASSIGN expression)?
    ;

// ---------------- TYPEDEF ----------------
typedefDecl
    : TYPEDEF typeSpecifier MUL* IDENTIFIER SEMI
    | TYPEDEF STRUCT IDENTIFIER? LBRACE structMember* RBRACE IDENTIFIER SEMI
    | TYPEDEF typeSpecifier LPAREN MUL IDENTIFIER RPAREN
              LPAREN parameterList? RPAREN SEMI
    ;

// ---------------- FUNCTION ----------------
functionDecl
    : functionQualifier* typeSpecifier MUL* BIT_AND?
      qualifiedName LPAREN parameterList? RPAREN
      functionSuffix* (block | SEMI)
    ;

functionQualifier
    : INLINE | STATIC | VIRTUAL | EXPLICIT
    | EXTERN | CONSTEXPR | FRIEND
    ;

functionSuffix
    : CONST | OVERRIDE | FINAL
    | ASSIGN NUMBER
    ;

operatorName
    : OPERATOR (PLUS | MINUS | MUL | DIV | MOD
               | EQ | NEQ | LT | GT | LE | GE
               | AND | OR | NOT | ASSIGN
               | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN | DIV_ASSIGN
               | LBRACKET RBRACKET
               | LPAREN RPAREN
               | SHIFT_LEFT | SHIFT_RIGHT
               | INC | DEC
               | BIT_AND | BIT_OR | BIT_XOR | BIT_NOT)
    ;

anyIdentifier
    : IDENTIFIER
    | DELETE
    | NEW
    | OVERRIDE
    | FINAL
    ;

qualifiedName
    : anyIdentifier (DOUBLE_COLON anyIdentifier)*
    | anyIdentifier DOUBLE_COLON BIT_NOT anyIdentifier
    | anyIdentifier DOUBLE_COLON operatorName
    | operatorName
    ;


parameterList
    : parameter (COMMA parameter)*
    | parameter (COMMA parameter)* COMMA ELLIPSIS
    | VOID
    ;

parameter
    : typeQualifier* typeSpecifier MUL* BIT_AND? IDENTIFIER?
    | typeQualifier* typeSpecifier MUL* BIT_AND? IDENTIFIER ASSIGN expression
    | typeQualifier* typeSpecifier MUL* BIT_AND? IDENTIFIER
      LBRACKET expression? RBRACKET
    | typeSpecifier LPAREN MUL IDENTIFIER? RPAREN LPAREN parameterList? RPAREN
    ;

// ---------------- BLOCK ----------------
block
    : LBRACE statement* RBRACE
    ;

// ---------------- STATEMENTS ----------------
statement
    : declaration
    | assignment
    | ifStatement
    | whileStatement
    | doWhileStatement
    | forStatement
    | rangeForStatement
    | switchStatement
    | returnStatement
    | breakStatement
    | continueStatement
    | gotoStatement
    | labelStatement
    | tryStatement
    | throwStatement
    | coutStatement
    | cinStatement
    | expressionStatement
    | block
    ;

// ---------------- DECLARATION ----------------
declaration
    : typeQualifier* typeSpecifier MUL* BIT_AND?
      initDeclarator (COMMA initDeclarator)* SEMI
    | typeQualifier* typeSpecifier LPAREN MUL IDENTIFIER RPAREN
      LPAREN parameterList? RPAREN (ASSIGN IDENTIFIER)? SEMI
    ;

initDeclarator
    : MUL* BIT_AND? IDENTIFIER (ASSIGN initializer)?
    | MUL* BIT_AND? IDENTIFIER
      LBRACKET expression? RBRACKET
      (LBRACKET expression? RBRACKET)*
      (ASSIGN initializer)?
    | MUL* IDENTIFIER LPAREN argumentList? RPAREN
    ;

// ---------------- INITIALIZER ----------------
initializer
    : assignmentExpression
    | LBRACE initializerList2 COMMA? RBRACE
    ;

initializerList2
    : designatedInitializer (COMMA designatedInitializer)*
    ;

designatedInitializer
    : (LBRACKET expression RBRACKET ASSIGN | DOT IDENTIFIER ASSIGN)*
      initializer
    ;

// ---------------- ASSIGNMENT ----------------
assignment
    : lvalue assignmentOp expression SEMI
    ;

lvalue
    : MUL* qualifiedName (LBRACKET expression RBRACKET)*
    | MUL* LPAREN expression RPAREN
    | qualifiedName ARROW qualifiedName (LBRACKET expression RBRACKET)*
    | qualifiedName DOT   qualifiedName (LBRACKET expression RBRACKET)*
    | THIS ARROW IDENTIFIER
    | THIS DOT   IDENTIFIER
    ;

assignmentOp
    : ASSIGN | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN
    | DIV_ASSIGN | MOD_ASSIGN | AND_ASSIGN | OR_ASSIGN
    | XOR_ASSIGN | LSHIFT_ASSIGN | RSHIFT_ASSIGN
    ;

// ---------------- EXPRESSION STATEMENT ----------------
expressionStatement
    : expression SEMI
    ;

// ---------------- IF ----------------
ifStatement
    : IF LPAREN expression RPAREN statement (ELSE statement)?
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
    : FOR LPAREN forInit expression? SEMI forUpdate? RPAREN statement
    ;

rangeForStatement
    : FOR LPAREN typeQualifier* typeSpecifier MUL* BIT_AND?
      IDENTIFIER COLON expression RPAREN statement
    ;

forInit
    : declaration
    | assignment
    | expressionStatement
    | SEMI
    ;

forUpdate
    : expression (COMMA expression)*
    ;

// ---------------- SWITCH ----------------
switchStatement
    : SWITCH LPAREN expression RPAREN LBRACE caseStatement+ RBRACE
    ;

caseStatement
    : CASE expression COLON statement*
    | DEFAULT COLON statement*
    ;

// ---------------- TRY CATCH ----------------
tryStatement
    : TRY block catchClause+
    ;

catchClause
    : CATCH LPAREN (typeSpecifier MUL* BIT_AND? IDENTIFIER? | ELLIPSIS) RPAREN block
    ;

throwStatement
    : THROW expression? SEMI
    ;

// ---------------- COUT / CIN ----------------
coutStatement
    : COUT (SHIFT_LEFT expression)+ SEMI
    ;

cinStatement
    : CIN (SHIFT_RIGHT lvalue)+ SEMI
    ;

// ---------------- JUMP STATEMENTS ----------------
returnStatement   : RETURN expression? SEMI ;
breakStatement    : BREAK SEMI ;
continueStatement : CONTINUE SEMI ;
gotoStatement     : GOTO IDENTIFIER SEMI ;
labelStatement    : IDENTIFIER COLON statement ;

// ---------------- TYPE SPECIFIER ----------------
typeSpecifier
    : typeQualifier* baseType
    | typeQualifier* qualifiedName
    | typeQualifier* qualifiedName LT typeArgList GT
    | typeQualifier* STRUCT IDENTIFIER
    | typeQualifier* CLASS  IDENTIFIER
    | typeQualifier* UNION  IDENTIFIER
    | typeQualifier* ENUM   IDENTIFIER
    | AUTO
    ;

typeArgList
    : typeSpecifier MUL* (COMMA typeSpecifier MUL*)*
    ;

typeQualifier
    : CONST | VOLATILE | STATIC | EXTERN | MUTABLE
    | REGISTER | INLINE | CONSTEXPR | UNSIGNED
    | SIGNED | LONG | SHORT | VIRTUAL | EXPLICIT
    ;

baseType
    : INT | FLOAT | DOUBLE | CHAR | VOID | BOOL
    | SHORT | LONG | UNSIGNED | SIGNED | WCHAR
    | STRING_TYPE
    ;

// ---------------- EXPRESSIONS ----------------
expression
    : assignmentExpression (COMMA assignmentExpression)*
    ;

assignmentExpression
    : conditionalExpression
    | unaryExpression assignmentOp assignmentExpression
    ;

conditionalExpression
    : logicalOrExpression (QUESTION expression COLON conditionalExpression)?
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
    : shiftExpression ((GT | LT | GE | LE) shiftExpression)*
    ;

shiftExpression
    : additiveExpression ((SHIFT_LEFT | SHIFT_RIGHT) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : castExpression ((MUL | DIV | MOD) castExpression)*
    ;

castExpression
    : LPAREN typeSpecifier MUL* BIT_AND? RPAREN castExpression
    | LPAREN typeSpecifier LPAREN MUL RPAREN LPAREN parameterList? RPAREN RPAREN castExpression
    | unaryExpression
    ;

unaryExpression
    : NOT       unaryExpression
    | MINUS     unaryExpression
    | PLUS      unaryExpression
    | BIT_NOT   unaryExpression
    | BIT_AND   castExpression
    | MUL       castExpression
    | INC       unaryExpression
    | DEC       unaryExpression
    | SIZEOF    LPAREN typeSpecifier MUL* RPAREN
    | SIZEOF    LPAREN expression RPAREN
    | NEW       typeSpecifier (LBRACKET expression RBRACKET)?
                (LPAREN argumentList? RPAREN)?
    | DELETE    LBRACKET RBRACKET? expression
    | THROW     expression
    | postfixExpression
    ;

postfixExpression
    : primaryExpression postfixOp*
    ;

postfixOp
    : INC
    | DEC
    | LBRACKET expression RBRACKET
    | DOT   qualifiedName
    | ARROW qualifiedName
    | LPAREN argumentList? RPAREN
    | LT typeArgList GT LPAREN argumentList? RPAREN
    ;

lambdaExpression
    : LBRACKET captureList? RBRACKET
      LPAREN parameterList? RPAREN
      (ARROW typeSpecifier)?
      block
    ;

captureList
    : captureItem (COMMA captureItem)*
    ;

captureItem
    : BIT_AND IDENTIFIER
    | BIT_AND
    | MUL
    | THIS
    | IDENTIFIER
    ;

primaryExpression
    : NUMBER
    | HEX_NUMBER
    | OCTAL_NUMBER
    | FLOAT_NUMBER
    | CHAR_LITERAL
    | STRING+
    | NULL_LIT
    | NULLPTR
    | BOOL_TRUE
    | BOOL_FALSE
    | ENDL
    | THIS
    | qualifiedName
    | lambdaExpression
    | LPAREN expression RPAREN
    ;

// ---------------- ARGUMENT LIST ----------------
argumentList
    : expression (COMMA expression)*
    ;