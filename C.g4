grammar C;

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

// Keywords
INT         : 'int';
FLOAT       : 'float';
DOUBLE      : 'double';
CHAR        : 'char';
VOID        : 'void';
SHORT       : 'short';
LONG        : 'long';
UNSIGNED    : 'unsigned';
SIGNED      : 'signed';
CONST       : 'const';
STATIC      : 'static';
EXTERN      : 'extern';
REGISTER    : 'register';
VOLATILE    : 'volatile';
AUTO        : 'auto';
INLINE      : 'inline';
RESTRICT    : 'restrict';
STRUCT      : 'struct';
UNION       : 'union';
ENUM        : 'enum';
TYPEDEF     : 'typedef';
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
SIZEOF      : 'sizeof';

// Standard IO
PRINTF      : 'printf';
SCANF       : 'scanf';
FPRINTF     : 'fprintf';
FSCANF      : 'fscanf';
SPRINTF     : 'sprintf';
SSCANF      : 'sscanf';
PUTS        : 'puts';
GETS        : 'gets';
GETCHAR     : 'getchar';
PUTCHAR     : 'putchar';

// Memory
MALLOC      : 'malloc';
CALLOC      : 'calloc';
REALLOC     : 'realloc';
FREE        : 'free';
MEMCPY      : 'memcpy';
MEMSET      : 'memset';
MEMMOVE     : 'memmove';

// String
STRLEN      : 'strlen';
STRCPY      : 'strcpy';
STRNCPY     : 'strncpy';
STRCAT      : 'strcat';
STRNCAT     : 'strncat';
STRCMP      : 'strcmp';
STRNCMP     : 'strncmp';
STRCHR      : 'strchr';
STRSTR      : 'strstr';

// Conversion
ATOI        : 'atoi';
ATOF        : 'atof';
ATOL        : 'atol';

// File IO
FOPEN       : 'fopen';
FCLOSE      : 'fclose';
FREAD       : 'fread';
FWRITE      : 'fwrite';
FGETS       : 'fgets';
FPUTS       : 'fputs';
FEOF        : 'feof';
FFLUSH      : 'fflush';
REWIND      : 'rewind';
FSEEK       : 'fseek';
FTELL       : 'ftell';

// Math
ABS         : 'abs';
FABS        : 'fabs';
SQRT        : 'sqrt';
POW         : 'pow';
CEIL        : 'ceil';
FLOOR       : 'floor';
RAND        : 'rand';
SRAND       : 'srand';

// System
EXIT        : 'exit';
ABORT       : 'abort';
ASSERT      : 'assert';
TIME        : 'time';
CLOCK       : 'clock';

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

// Identifier
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
    | structDecl
    | unionDecl
    | enumDecl
    | typedefDecl
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

// ---------------- STRUCT ----------------
structDecl
    : STRUCT IDENTIFIER LBRACE structMember+ RBRACE SEMI
    ;

structMember
    : typeSpecifier MUL* IDENTIFIER (LBRACKET expression RBRACKET)? SEMI
    | typeSpecifier MUL* IDENTIFIER COLON NUMBER SEMI
    ;

// ---------------- UNION ----------------
unionDecl
    : UNION IDENTIFIER LBRACE structMember+ RBRACE SEMI
    ;

// ---------------- ENUM ----------------
enumDecl
    : ENUM IDENTIFIER LBRACE enumeratorList COMMA? RBRACE SEMI
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
    | TYPEDEF STRUCT IDENTIFIER? LBRACE structMember+ RBRACE IDENTIFIER SEMI
    | TYPEDEF UNION  IDENTIFIER? LBRACE structMember+ RBRACE IDENTIFIER SEMI
    | TYPEDEF ENUM   IDENTIFIER? LBRACE enumeratorList RBRACE IDENTIFIER SEMI
    | TYPEDEF typeSpecifier LPAREN MUL IDENTIFIER RPAREN
              LPAREN parameterList? RPAREN SEMI
    ;

// ---------------- FUNCTION ----------------
// ---------------- FUNCTION ----------------
functionDecl
    : typeSpecifier MUL* IDENTIFIER LPAREN parameterList? RPAREN block
    | typeSpecifier MUL* IDENTIFIER LPAREN parameterList? RPAREN SEMI
    ;

parameterList
    : parameter (COMMA parameter)*
    | parameter (COMMA parameter)* COMMA ELLIPSIS
    | VOID
    ;

parameter
    : typeSpecifier MUL* IDENTIFIER
    | typeSpecifier MUL* IDENTIFIER LBRACKET expression? RBRACKET
    | typeSpecifier MUL* IDENTIFIER LBRACKET MUL RBRACKET
    | typeSpecifier MUL*
    | typeSpecifier LPAREN MUL IDENTIFIER RPAREN
      LPAREN parameterList? RPAREN
    | typeSpecifier LPAREN MUL RPAREN
      LPAREN parameterList? RPAREN
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
    | switchStatement
    | returnStatement
    | breakStatement
    | continueStatement
    | gotoStatement
    | labelStatement
    | expressionStatement
    | block
    ;
// ---------------- DECLARATION ----------------

declaration
    : typeQualifier* typeSpecifier initDeclarator (COMMA initDeclarator)* SEMI
    | typeQualifier* typeSpecifier LPAREN MUL IDENTIFIER RPAREN
      LPAREN parameterList? RPAREN SEMI
    | typeQualifier* typeSpecifier LPAREN MUL IDENTIFIER RPAREN
      LPAREN parameterList? RPAREN ASSIGN IDENTIFIER SEMI
    ;

initDeclarator
    : MUL* IDENTIFIER (ASSIGN initializer)?
    | MUL* IDENTIFIER LBRACKET expression? RBRACKET
      (LBRACKET expression? RBRACKET)* (ASSIGN initializer)?
    ;

// ---------------- INITIALIZER ----------------
// Handles: = 5, = {1,2,3}, = {1,{2,3}}, = {[0]=1}
initializer
    : assignmentExpression
    | LBRACE initializerList COMMA? RBRACE
    ;

initializerList
    : designatedInitializer (COMMA designatedInitializer)*
    ;

designatedInitializer
    : (LBRACKET expression RBRACKET ASSIGN
      | DOT IDENTIFIER ASSIGN)*
      initializer
    ;

// ---------------- ASSIGNMENT ----------------
assignment
    : lvalue assignmentOp expression SEMI
    ;

lvalue
    : MUL* IDENTIFIER (LBRACKET expression RBRACKET)*
    | MUL* LPAREN expression RPAREN
    | IDENTIFIER (ARROW IDENTIFIER)+
    | IDENTIFIER (DOT IDENTIFIER)+
    | IDENTIFIER ARROW IDENTIFIER (LBRACKET expression RBRACKET)*
    | IDENTIFIER DOT  IDENTIFIER (LBRACKET expression RBRACKET)*
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

// ---------------- IF ELSE ----------------
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

// ---------------- JUMP STATEMENTS ----------------
returnStatement   : RETURN expression? SEMI ;
breakStatement    : BREAK SEMI ;
continueStatement : CONTINUE SEMI ;
gotoStatement     : GOTO IDENTIFIER SEMI ;
labelStatement    : IDENTIFIER COLON statement ;

// ---------------- TYPE SPECIFIER ----------------
typeSpecifier
    : baseType
    | STRUCT IDENTIFIER
    | UNION  IDENTIFIER
    | ENUM   IDENTIFIER
    | IDENTIFIER
    ;

typeQualifier
    : CONST | VOLATILE | STATIC | EXTERN
    | REGISTER | AUTO | INLINE | RESTRICT
    | UNSIGNED | SIGNED | LONG | SHORT
    ;

baseType
    : INT | FLOAT | DOUBLE | CHAR | VOID
    | SHORT | LONG | UNSIGNED | SIGNED
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

// Handles: (int*)arg, (int)x, (void*)ptr
castExpression
    : LPAREN typeSpecifier MUL* RPAREN castExpression
    | unaryExpression
    ;

// Handles: *ptr, *(int*)arg, &var, !x, -x, ++i, sizeof(int)
unaryExpression
    : NOT       unaryExpression
    | MINUS     unaryExpression
    | PLUS      unaryExpression
    | BIT_NOT   unaryExpression
    | BIT_AND   castExpression
    | MUL       castExpression
    | INC       unaryExpression
    | DEC       unaryExpression
    | SIZEOF LPAREN typeSpecifier MUL* RPAREN
    | SIZEOF LPAREN expression RPAREN
    | postfixExpression
    ;

// Handles: arr[i], ptr->field, obj.field, func(), i++, i--
postfixExpression
    : primaryExpression postfixOp*
    ;

postfixOp
    : INC
    | DEC
    | LBRACKET expression RBRACKET
    | DOT   IDENTIFIER
    | ARROW IDENTIFIER
    | LPAREN argumentList? RPAREN
    ;
primaryExpression
    : NUMBER
    | HEX_NUMBER
    | OCTAL_NUMBER
    | FLOAT_NUMBER
    | CHAR_LITERAL
    | STRING+
    | NULL_LIT
    | BOOL_TRUE
    | BOOL_FALSE
    | IDENTIFIER
    | builtinCall
    | LPAREN expression RPAREN
    ;


// ---------------- BUILTIN CALLS ----------------
builtinCall
    : PRINTF   LPAREN expression (COMMA expression)* RPAREN
    | FPRINTF  LPAREN expression (COMMA expression)* RPAREN
    | SPRINTF  LPAREN expression (COMMA expression)* RPAREN
    | SCANF    LPAREN STRING (COMMA scanfArg)* RPAREN
    | FSCANF   LPAREN expression COMMA STRING (COMMA scanfArg)* RPAREN
    | SSCANF   LPAREN expression COMMA STRING (COMMA scanfArg)* RPAREN
    | MALLOC   LPAREN expression RPAREN
    | CALLOC   LPAREN expression COMMA expression RPAREN
    | REALLOC  LPAREN expression COMMA expression RPAREN
    | FREE     LPAREN expression RPAREN
    | MEMCPY   LPAREN expression COMMA expression COMMA expression RPAREN
    | MEMSET   LPAREN expression COMMA expression COMMA expression RPAREN
    | MEMMOVE  LPAREN expression COMMA expression COMMA expression RPAREN
    | STRLEN   LPAREN expression RPAREN
    | STRCPY   LPAREN expression COMMA expression RPAREN
    | STRNCPY  LPAREN expression COMMA expression COMMA expression RPAREN
    | STRCAT   LPAREN expression COMMA expression RPAREN
    | STRNCAT  LPAREN expression COMMA expression COMMA expression RPAREN
    | STRCMP   LPAREN expression COMMA expression RPAREN
    | STRNCMP  LPAREN expression COMMA expression COMMA expression RPAREN
    | STRCHR   LPAREN expression COMMA expression RPAREN
    | STRSTR   LPAREN expression COMMA expression RPAREN
    | ATOI     LPAREN expression RPAREN
    | ATOF     LPAREN expression RPAREN
    | ATOL     LPAREN expression RPAREN
    | FOPEN    LPAREN expression COMMA expression RPAREN
    | FCLOSE   LPAREN expression RPAREN
    | FREAD    LPAREN expression COMMA expression COMMA expression COMMA expression RPAREN
    | FWRITE   LPAREN expression COMMA expression COMMA expression COMMA expression RPAREN
    | FGETS    LPAREN expression COMMA expression COMMA expression RPAREN
    | FPUTS    LPAREN expression COMMA expression RPAREN
    | FEOF     LPAREN expression RPAREN
    | FFLUSH   LPAREN expression RPAREN
    | REWIND   LPAREN expression RPAREN
    | FSEEK    LPAREN expression COMMA expression COMMA expression RPAREN
    | FTELL    LPAREN expression RPAREN
    | EXIT     LPAREN expression RPAREN
    | ABORT    LPAREN RPAREN
    | ASSERT   LPAREN expression RPAREN
    | PUTS     LPAREN expression RPAREN
    | GETS     LPAREN expression RPAREN
    | GETCHAR  LPAREN RPAREN
    | PUTCHAR  LPAREN expression RPAREN
    | ABS      LPAREN expression RPAREN
    | FABS     LPAREN expression RPAREN
    | SQRT     LPAREN expression RPAREN
    | POW      LPAREN expression COMMA expression RPAREN
    | CEIL     LPAREN expression RPAREN
    | FLOOR    LPAREN expression RPAREN
    | RAND     LPAREN RPAREN
    | SRAND    LPAREN expression RPAREN
    | TIME     LPAREN expression RPAREN
    | CLOCK    LPAREN RPAREN
    | SIZEOF   LPAREN expression RPAREN
    ;

scanfArg
    : BIT_AND postfixExpression
    | postfixExpression
    ;

// ---------------- ARGUMENT LIST ----------------
argumentList
    : expression (COMMA expression)*
    ;