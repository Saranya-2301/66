lexer grammar JavaLexer;

// ===== PACKAGE =====
PACKAGE     : 'package';
IMPORT      : 'import';

// ===== OOP =====
CLASS       : 'class';
INTERFACE   : 'interface';
ENUM        : 'enum';
EXTENDS     : 'extends';
IMPLEMENTS  : 'implements';
PUBLIC      : 'public';
PRIVATE     : 'private';
PROTECTED   : 'protected';
STATIC      : 'static';
FINAL       : 'final';
ABSTRACT    : 'abstract';
NEW         : 'new';
THIS        : 'this';
SUPER       : 'super';

// ===== TYPES =====
INT         : 'int';
FLOAT       : 'float';
DOUBLE      : 'double';
CHAR        : 'char';
BOOLEAN     : 'boolean';
VOID        : 'void';
TRUE        : 'true';
FALSE       : 'false';
RETURN      : 'return';

// ===== CONTROL =====
IF          : 'if';
ELSE        : 'else';
FOR         : 'for';
WHILE       : 'while';
DO          : 'do';
SWITCH      : 'switch';
CASE        : 'case';
DEFAULT     : 'default';
BREAK       : 'break';
CONTINUE    : 'continue';
TRY         : 'try';
CATCH       : 'catch';
FINALLY     : 'finally';
THROW       : 'throw';

// ===== OPERATORS =====
PLUS        : '+';
MINUS       : '-';
MULT        : '*';
DIV         : '/';
MOD         : '%';
INCREMENT   : '++';
DECREMENT   : '--';
ASSIGN      : '=';
EQ          : '==';
NEQ         : '!=';
LT          : '<';
GT          : '>';
LE          : '<=';
GE          : '>=';
AND         : '&&';
OR          : '||';
NOT         : '!';
DOT         : '.';
SEMI        : ';';
COMMA       : ',';
COLON       : ':';

// ===== DELIMITERS =====
LPAREN      : '(';
RPAREN      : ')';
LBRACE      : '{';
RBRACE      : '}';
LBRACK      : '[';
RBRACK      : ']';

// ===== LITERALS =====
INTEGER     : [0-9]+;
FLOAT_LITERAL : [0-9]+ '.' [0-9]+;
CHAR_LITERAL  : '\'' . '\'';
STRING      : '"' .*? '"';

// ===== IDENTIFIER =====
IDENTIFIER  : [a-zA-Z_][a-zA-Z0-9_]*;

// ===== COMMENTS =====
LINE_COMMENT    : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT   : '/*' .*? '*/' -> skip;

// ===== WHITESPACE =====
WS : [ \t\r\n]+ -> skip;
