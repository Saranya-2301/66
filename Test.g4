grammar Test;

/* ---------------- PROGRAM ---------------- */

program
    : (preprocessor
    | declaration
    | functionDefinition
    | statement
    )* EOF
    ;


/* ---------------- FUNCTIONS ---------------- */

functionDefinition
    : typeSpecifier IDENTIFIER LPAREN parameterList? RPAREN compoundStatement
    ;

parameterList
    : parameter (COMMA parameter)*
    ;

parameter
    : typeSpecifier IDENTIFIER
    ;




/* ---------------- EXPRESSIONS ---------------- */

expression
    : assignmentExpression
    ;

assignmentExpression
    : logicalOrExpression
    | IDENTIFIER ASSIGN assignmentExpression
    ;

logicalOrExpression
    : logicalAndExpression (OROR logicalAndExpression)*
    ;

logicalAndExpression
    : equalityExpression (ANDAND equalityExpression)*
    ;

equalityExpression
    : relationalExpression ((EQUAL | NOT_EQUAL) relationalExpression)*
    ;

relationalExpression
    : additiveExpression ((LESS | GREATER | LESS_EQUAL | GREATER_EQUAL) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : unaryExpression ((STAR | SLASH | PERCENT) unaryExpression)*
    ;

unaryExpression
    : primaryExpression
    | NOT unaryExpression
    | PLUSPLUS unaryExpression
    | MINUSMINUS unaryExpression
    ;

primaryExpression
    : IDENTIFIER
    | IDENTIFIER LPAREN argumentList? RPAREN   // ✅ function call added
    | literal
    | LPAREN expression RPAREN
    ;

argumentList
    : expression (COMMA expression)*
    ;

/* ---------------- STATEMENTS ---------------- */

statement
    : expressionStatement
    | ifStatement
    | whileStatement
    | compoundStatement
    ;

expressionStatement
    : expression? SEMICOLON
    ;

ifStatement
    : IF LPAREN expression RPAREN statement (ELSE statement)?
    ;

whileStatement
    : WHILE LPAREN expression RPAREN statement
    ;


/* ---------------- DECLARATIONS ---------------- */

declaration
    : typeSpecifier IDENTIFIER SEMICOLON
    | typeSpecifier IDENTIFIER ASSIGN expression SEMICOLON
    ;

/* ---------------- PREPROCESSOR ---------------- */

preprocessor
    : INCLUDE STRING_LITERAL
    | DEFINE IDENTIFIER (INTEGER_LITERAL | STRING_LITERAL)?
    ;

/* ---------------- TYPES ---------------- */

typeSpecifier
    : INT
    | FLOAT
    | DOUBLE
    | CHAR
    | VOID
    | BOOL
    | LONG
    | SHORT
    | SIGNED
    | UNSIGNED
    ;

/* ---------------- LITERALS ---------------- */

literal
    : INTEGER_LITERAL
    | FLOATING_LITERAL
    | STRING_LITERAL
    | CHARACTER_LITERAL
    | TRUE
    | FALSE
    | NULL
    | NULLPTR
    ;




compoundStatement
    : LBRACE statement* RBRACE
    ;



/* -------- IF / SWITCH -------- */

selectionStatement
    : IF LPAREN expression RPAREN statement (ELSE statement)?
    | SWITCH LPAREN expression RPAREN compoundStatement
    ;

/* -------- LOOPS -------- */

iterationStatement
    : WHILE LPAREN expression RPAREN statement
    | DO statement WHILE LPAREN expression RPAREN SEMICOLON
    | FOR LPAREN expressionStatement expressionStatement expression? RPAREN statement
    ;

/* -------- RETURN / BREAK -------- */

jumpStatement
    : RETURN expression? SEMICOLON
    | BREAK SEMICOLON
    | CONTINUE SEMICOLON
    ;


/* ---------------- LEXER RULES ---------------- */

/* IDENTIFIERS */
IDENTIFIER : [a-zA-Z_] [a-zA-Z_0-9]* ;

/* LITERALS */
INTEGER_LITERAL : [0-9]+ ;
FLOATING_LITERAL : [0-9]+ '.' [0-9]+ ;
HEX_LITERAL : '0x' [0-9a-fA-F]+ ;
OCTAL_LITERAL : '0' [0-7]+ ;
BINARY_LITERAL : '0b' [01]+ ;

STRING_LITERAL : '"' (~["\\] | '\\' .)* '"' ;
CHARACTER_LITERAL : '\'' (~['\\] | '\\' .) '\'' ;

TRUE : 'true' ;
FALSE : 'false' ;
NULL : 'null' ;
NULLPTR : 'nullptr' ;

/* OPERATORS */
PLUS : '+' ;
MINUS : '-' ;
STAR : '*' ;
SLASH : '/' ;
PERCENT : '%' ;

PLUSPLUS : '++' ;
MINUSMINUS : '--' ;

ASSIGN : '=' ;
PLUS_ASSIGN : '+=' ;
MINUS_ASSIGN : '-=' ;
STAR_ASSIGN : '*=' ;
SLASH_ASSIGN : '/=' ;
PERCENT_ASSIGN : '%=' ;

AND_ASSIGN : '&=' ;
OR_ASSIGN : '|=' ;
XOR_ASSIGN : '^=' ;
LEFT_SHIFT_ASSIGN : '<<=' ;
RIGHT_SHIFT_ASSIGN : '>>=' ;

/* RELATIONAL */
LESS : '<' ;
GREATER : '>' ;
LESS_EQUAL : '<=' ;
GREATER_EQUAL : '>=' ;
EQUAL : '==' ;
NOT_EQUAL : '!=' ;

/* LOGICAL */
ANDAND : '&&' ;
OROR : '||' ;
NOT : '!' ;

/* BITWISE */
AND : '&' ;
OR : '|' ;
XOR : '^' ;
TILDE : '~' ;
LEFT_SHIFT : '<<' ;
RIGHT_SHIFT : '>>' ;

/* SPECIAL */
ARROW : '->' ;
SCOPE : '::' ;
ELLIPSIS : '...' ;

/* SYMBOLS */
LPAREN : '(' ;
RPAREN : ')' ;
LBRACE : '{' ;
RBRACE : '}' ;
LBRACKET : '[' ;
RBRACKET : ']' ;
SEMICOLON : ';' ;
COMMA : ',' ;
DOT : '.' ;
COLON : ':' ;
QUESTION : '?' ;

/* PREPROCESSOR */
HASH : '#' ;
INCLUDE : '#include' ;
DEFINE : '#define' ;

/* CONTROL FLOW */
IF : 'if' ;
ELSE : 'else' ;
FOR : 'for' ;
WHILE : 'while' ;
DO : 'do' ;
SWITCH : 'switch' ;
CASE : 'case' ;
DEFAULT : 'default' ;
BREAK : 'break' ;
CONTINUE : 'continue' ;
RETURN : 'return' ;
GOTO : 'goto' ;

/* DATA TYPES */
INT : 'int' ;
FLOAT : 'float' ;
DOUBLE : 'double' ;
CHAR : 'char' ;
VOID : 'void' ;
LONG : 'long' ;
SHORT : 'short' ;
SIGNED : 'signed' ;
UNSIGNED : 'unsigned' ;
BOOL : 'bool' ;

/* STORAGE */
STATIC : 'static' ;
CONST : 'const' ;
VOLATILE : 'volatile' ;
TYPEDEF : 'typedef' ;
AUTO : 'auto' ;
REGISTER : 'register' ;
EXTERN : 'extern' ;

/* OOP */
CLASS : 'class' ;
STRUCT : 'struct' ;
UNION : 'union' ;
PUBLIC : 'public' ;
PRIVATE : 'private' ;
PROTECTED : 'protected' ;
THIS : 'this' ;
NEW : 'new' ;
DELETE : 'delete' ;

/* JAVA STYLE */
PACKAGE : 'package' ;
IMPORT : 'import' ;
INTERFACE : 'interface' ;
EXTENDS : 'extends' ;
IMPLEMENTS : 'implements' ;
THROW : 'throw' ;
THROWS : 'throws' ;
TRY : 'try' ;
CATCH : 'catch' ;
FINALLY : 'finally' ;

/* C++ STYLE */
NAMESPACE : 'namespace' ;
TEMPLATE : 'template' ;
TYPENAME : 'typename' ;
USING : 'using' ;
VIRTUAL : 'virtual' ;
OVERRIDE : 'override' ;
FRIEND : 'friend' ;

/* COMMENTS */
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;

/* WHITESPACE */
WS : [ \t\r\n]+ -> skip ;

/* ERROR */
ERROR_CHAR : . ;
