parser grammar CParser;

options { tokenVocab=CLexer; }

// ===== PROGRAM =====
program
    : (preprocessor | declaration | functionDef)* EOF
    ;

// ===== PREPROCESSOR =====
preprocessor
    : INCLUDE HEADER
    | DEFINE IDENTIFIER expression?
    ;

// ===== DECLARATION =====
declaration
    : type declaratorList SEMI
    ;

declaratorList
    : declarator (COMMA declarator)*
    ;

declarator
    : IDENTIFIER
    | IDENTIFIER ASSIGN expression
    ;

// ===== FUNCTION =====
functionDef
    : type IDENTIFIER LPAREN parameterList? RPAREN compoundStmt
    ;

parameterList
    : parameter (COMMA parameter)*
    ;

parameter
    : type IDENTIFIER
    ;

// ===== TYPE =====
type
    : INT | FLOAT | DOUBLE | CHAR | VOID
    ;

// ===== STATEMENTS =====
compoundStmt
    : LBRACE statement* RBRACE
    ;

statement
    : declaration
    | expressionStmt
    | compoundStmt
    | selectionStmt
    | iterationStmt
    | jumpStmt
    ;

expressionStmt
    : expression? SEMI
    ;

selectionStmt
    : IF LPAREN expression RPAREN statement (ELSE statement)?
    | SWITCH LPAREN expression RPAREN compoundStmt
    ;

iterationStmt
    : WHILE LPAREN expression RPAREN statement
    | DO statement WHILE LPAREN expression RPAREN SEMI
    | FOR LPAREN expression? SEMI expression? SEMI expression? RPAREN statement
    ;

jumpStmt
    : RETURN expression? SEMI
    | BREAK SEMI
    | CONTINUE SEMI
    ;

// ===== EXPRESSIONS =====
expression
    : assignment
    ;

assignment
    : logicalOr (ASSIGN assignment)?
    ;

logicalOr
    : logicalAnd (OR logicalAnd)*
    ;

logicalAnd
    : equality (AND equality)*
    ;

equality
    : relational ((EQ | NEQ) relational)*
    ;

relational
    : additive ((LT | GT | LE | GE) additive)*
    ;

additive
    : multiplicative ((PLUS | MINUS) multiplicative)*
    ;

multiplicative
    : unary ((MULT | DIV | MOD) unary)*
    ;

unary
    : (PLUS | MINUS | NOT) unary
    | primary
    ;

primary
    : IDENTIFIER
    | INTEGER
    | FLOAT_LITERAL
    | STRING
    | LPAREN expression RPAREN
    ;
