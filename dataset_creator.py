"""
Generates a fully annotated dataset of 300 code samples:
  - 100 samples in C    (50 LEXICAL + 50 SYNTAX)
  - 100 samples in C++  (50 LEXICAL + 50 SYNTAX)
  - 100 samples in Java (50 LEXICAL + 50 SYNTAX)

Run:
    python annotated_dataset.py
Output:
    dataset/annotated_dataset.json
"""

import json, os

LABEL_MAP = {"NONE": 0, "LEXICAL": 1, "SYNTAX": 2}

#  C  —  50 LEXICAL  +  50 SYNTAX

C_LEXICAL = [
  {"id":"C_LEX_001","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Undefined variable 'reslt' used instead of 'result'",
   "incorrect":"#include <stdio.h>\nint square(int n) {\n    int reslt = n * n;\n    return reslt;\n}",
   "correct":  "#include <stdio.h>\nint square(int n) {\n    int result = n * n;\n    return result;\n}"},

  {"id":"C_LEX_002","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Unclosed string literal in printf",
   "incorrect":"#include <stdio.h>\nint main() {\n    printf(\"Hello World\\n);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    printf(\"Hello World\\n\");\n    return 0;\n}"},

  {"id":"C_LEX_003","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"Invalid identifier '2count' starts with a digit",
   "incorrect":"#include <stdio.h>\nint 2count = 0;\nint main() {\n    2count++;\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint count2 = 0;\nint main() {\n    count2++;\n    return 0;\n}"},

  {"id":"C_LEX_004","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Typo 'lenth' instead of 'length'",
   "incorrect":"#include <stdio.h>\n#include <string.h>\nint main() {\n    int lenth = strlen(\"hello\");\n    printf(\"%d\\n\", lenth);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\n#include <string.h>\nint main() {\n    int length = strlen(\"hello\");\n    printf(\"%d\\n\", length);\n    return 0;\n}"},

  {"id":"C_LEX_005","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Unknown type 'intg' instead of 'int'",
   "incorrect":"#include <stdio.h>\nint main() {\n    intg x = 10;\n    printf(\"%d\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 10;\n    printf(\"%d\\n\", x);\n    return 0;\n}"},

  {"id":"C_LEX_006","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Invalid character '@' in variable name",
   "incorrect":"#include <stdio.h>\nint main() {\n    int @value = 5;\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int value = 5;\n    return 0;\n}"},

  {"id":"C_LEX_007","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"Misspelled keyword 'retun' instead of 'return'",
   "incorrect":"#include <stdio.h>\nint getValue() { retun 42; }\nint main() {\n    printf(\"%d\\n\", getValue());\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint getValue() { return 42; }\nint main() {\n    printf(\"%d\\n\", getValue());\n    return 0;\n}"},

  {"id":"C_LEX_008","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Typo 'numbr' instead of 'number'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int number = 10;\n    printf(\"%d\\n\", numbr);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int number = 10;\n    printf(\"%d\\n\", number);\n    return 0;\n}"},

  {"id":"C_LEX_009","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Invalid escape sequence '\\q'",
   "incorrect":"#include <stdio.h>\nint main() {\n    printf(\"Value\\q\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    printf(\"Value\\n\");\n    return 0;\n}"},

  {"id":"C_LEX_010","language":"C","error_type":"LEXICAL","error_label":1,"error_line":1,
   "error_desc":"Misspelled directive '#includ'",
   "incorrect":"#includ <stdio.h>\nint main() {\n    printf(\"hi\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    printf(\"hi\\n\");\n    return 0;\n}"},

  {"id":"C_LEX_011","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Variable 'ans' used before declaration",
   "incorrect":"#include <stdio.h>\nint main() {\n    ans = 5 + 3;\n    int ans;\n    printf(\"%d\\n\", ans);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int ans;\n    ans = 5 + 3;\n    printf(\"%d\\n\", ans);\n    return 0;\n}"},

  {"id":"C_LEX_012","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"String literal missing closing quote",
   "incorrect":"#include <stdio.h>\nint main() {\n    char name[] = \"Alice;\n    printf(\"%s\\n\", name);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    char name[] = \"Alice\";\n    printf(\"%s\\n\", name);\n    return 0;\n}"},

  {"id":"C_LEX_013","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"Misspelled 'voud' instead of 'void'",
   "incorrect":"#include <stdio.h>\nvoud greet() {\n    printf(\"Hello\\n\");\n}\nint main() {\n    greet();\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nvoid greet() {\n    printf(\"Hello\\n\");\n}\nint main() {\n    greet();\n    return 0;\n}"},

  {"id":"C_LEX_014","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Wrong format specifier '%s' for integer",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 42;\n    printf(\"%s\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 42;\n    printf(\"%d\\n\", x);\n    return 0;\n}"},

  {"id":"C_LEX_015","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Undeclared function 'printff' (typo)",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 10;\n    printff(\"%d\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 10;\n    printf(\"%d\\n\", x);\n    return 0;\n}"},

  {"id":"C_LEX_016","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Illegal '$' in identifier name",
   "incorrect":"#include <stdio.h>\nint main() {\n    int $price = 100;\n    printf(\"%d\\n\", $price);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int price = 100;\n    printf(\"%d\\n\", price);\n    return 0;\n}"},

  {"id":"C_LEX_017","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"Misspelled 'flot' instead of 'float'",
   "incorrect":"#include <stdio.h>\nflot computeAvg(int a, int b) {\n    return (a + b) / 2.0;\n}\nint main() {\n    printf(\"%.2f\\n\", computeAvg(4, 6));\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nfloat computeAvg(int a, int b) {\n    return (a + b) / 2.0;\n}\nint main() {\n    printf(\"%.2f\\n\", computeAvg(4, 6));\n    return 0;\n}"},

  {"id":"C_LEX_018","language":"C","error_type":"LEXICAL","error_label":1,"error_line":5,
   "error_desc":"Undefined variable 'sm' should be 'sum'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int sum = 0;\n    for (int i=1; i<=5; i++) sum += i;\n    printf(\"%d\\n\", sm);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int sum = 0;\n    for (int i=1; i<=5; i++) sum += i;\n    printf(\"%d\\n\", sum);\n    return 0;\n}"},

  {"id":"C_LEX_019","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Char literal contains more than one character",
   "incorrect":"#include <stdio.h>\nint main() {\n    char c = 'ab';\n    printf(\"%c\\n\", c);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    char c = 'a';\n    printf(\"%c\\n\", c);\n    return 0;\n}"},

  {"id":"C_LEX_020","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"Missing <string.h> header; strlen undeclared",
   "incorrect":"#include <stdio.h>\nint main() {\n    char s[] = \"test\";\n    printf(\"%lu\\n\", strlen(s));\n    return 0;\n}",
   "correct":  "#include <stdio.h>\n#include <string.h>\nint main() {\n    char s[] = \"test\";\n    printf(\"%lu\\n\", strlen(s));\n    return 0;\n}"},

  {"id":"C_LEX_021","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Misspelled 'whlie' instead of 'while'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int i = 0;\n    whlie (i < 3) { printf(\"%d\\n\", i); i++; }\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int i = 0;\n    while (i < 3) { printf(\"%d\\n\", i); i++; }\n    return 0;\n}"},

  {"id":"C_LEX_022","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Undeclared variable 'idx' should be 'i'",
   "incorrect":"#include <stdio.h>\nint main() {\n    for (int i=0; i<3; i++)\n        printf(\"%d\\n\", idx);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    for (int i=0; i<3; i++)\n        printf(\"%d\\n\", i);\n    return 0;\n}"},

  {"id":"C_LEX_023","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'cahrr' is not a valid type — should be 'char'",
   "incorrect":"#include <stdio.h>\nint main() {\n    cahrr letter = 'A';\n    printf(\"%c\\n\", letter);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    char letter = 'A';\n    printf(\"%c\\n\", letter);\n    return 0;\n}"},

  {"id":"C_LEX_024","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'IF' is not a keyword — C is case-sensitive",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 5;\n    IF (x > 0) printf(\"positive\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 5;\n    if (x > 0) printf(\"positive\\n\");\n    return 0;\n}"},

  {"id":"C_LEX_025","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Double-quoted char literal — should use single quotes",
   "incorrect":"#include <stdio.h>\nint main() {\n    char c = \"A\";\n    printf(\"%c\\n\", c);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    char c = 'A';\n    printf(\"%c\\n\", c);\n    return 0;\n}"},

  {"id":"C_LEX_026","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'RETURN' is not a keyword — C is case-sensitive",
   "incorrect":"#include <stdio.h>\nint add(int a, int b) {\n    RETURN a + b;\n}\nint main() { printf(\"%d\\n\", add(2,3)); return 0; }",
   "correct":  "#include <stdio.h>\nint add(int a, int b) {\n    return a + b;\n}\nint main() { printf(\"%d\\n\", add(2,3)); return 0; }"},

  {"id":"C_LEX_027","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'doubble' is not a valid type — should be 'double'",
   "incorrect":"#include <stdio.h>\nint main() {\n    doubble pi = 3.14159;\n    printf(\"%.5f\\n\", pi);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    double pi = 3.14159;\n    printf(\"%.5f\\n\", pi);\n    return 0;\n}"},

  {"id":"C_LEX_028","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Undeclared 'maxVal' — should be 'maxValue'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int maxValue = 100;\n    printf(\"%d\\n\", maxVal);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int maxValue = 100;\n    printf(\"%d\\n\", maxValue);\n    return 0;\n}"},

  {"id":"C_LEX_029","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'3D' is invalid — identifier starts with digit",
   "incorrect":"#include <stdio.h>\nint main() {\n    int 3D = 9;\n    printf(\"%d\\n\", 3D);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int dim3 = 9;\n    printf(\"%d\\n\", dim3);\n    return 0;\n}"},

  {"id":"C_LEX_030","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'structt' is not a keyword — should be 'struct'",
   "incorrect":"#include <stdio.h>\nstructt Point { int x; int y; };\nint main() {\n    struct Point p = {1, 2};\n    printf(\"%d %d\\n\", p.x, p.y);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nstruct Point { int x; int y; };\nint main() {\n    struct Point p = {1, 2};\n    printf(\"%d %d\\n\", p.x, p.y);\n    return 0;\n}"},

  {"id":"C_LEX_031","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'Scanf' (capital S) is not valid — should be 'scanf'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int n;\n    Scanf(\"%d\", &n);\n    printf(\"%d\\n\", n);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int n;\n    scanf(\"%d\", &n);\n    printf(\"%d\\n\", n);\n    return 0;\n}"},

  {"id":"C_LEX_032","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Operator '**' is not valid in C for exponentiation",
   "incorrect":"#include <stdio.h>\nint main() {\n    int result = 2 ** 8;\n    printf(\"%d\\n\", result);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\n#include <math.h>\nint main() {\n    int result = (int)pow(2, 8);\n    printf(\"%d\\n\", result);\n    return 0;\n}"},

  {"id":"C_LEX_033","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'interger' is not a valid type name — should be 'int'",
   "incorrect":"#include <stdio.h>\ninterger countItems(int arr[], int n) {\n    return n;\n}\nint main() { printf(\"%d\\n\", countItems(NULL,5)); return 0; }",
   "correct":  "#include <stdio.h>\nint countItems(int arr[], int n) {\n    return n;\n}\nint main() { printf(\"%d\\n\", countItems(NULL,5)); return 0; }"},

  {"id":"C_LEX_034","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'iff' is not a keyword — should be 'if'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 10;\n    iff (x > 5) printf(\"big\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 10;\n    if (x > 5) printf(\"big\\n\");\n    return 0;\n}"},

  {"id":"C_LEX_035","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'intt' is not a valid type — should be 'int'",
   "incorrect":"#include <stdio.h>\nint main() {\n    intt a = 5, b = 3;\n    printf(\"%d\\n\", a + b);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int a = 5, b = 3;\n    printf(\"%d\\n\", a + b);\n    return 0;\n}"},

  {"id":"C_LEX_036","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'#define' value missing — incomplete macro definition",
   "incorrect":"#include <stdio.h>\n#define MAX\nint main() {\n    int x = MAX;\n    printf(\"%d\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\n#define MAX 100\nint main() {\n    int x = MAX;\n    printf(\"%d\\n\", x);\n    return 0;\n}"},

  {"id":"C_LEX_037","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'fro' is not a keyword — should be 'for'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int sum = 0;\n    fro (int i=1; i<=5; i++) sum += i;\n    printf(\"%d\\n\", sum);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int sum = 0;\n    for (int i=1; i<=5; i++) sum += i;\n    printf(\"%d\\n\", sum);\n    return 0;\n}"},

  {"id":"C_LEX_038","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'short int' written as 'shoort' — misspelled type",
   "incorrect":"#include <stdio.h>\nint main() {\n    shoort x = 32000;\n    printf(\"%d\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    short x = 32000;\n    printf(\"%d\\n\", x);\n    return 0;\n}"},

  {"id":"C_LEX_039","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'prinf' is misspelled — should be 'printf'",
   "incorrect":"#include <stdio.h>\nint main() {\n    prinf(\"Hello\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    printf(\"Hello\\n\");\n    return 0;\n}"},

  {"id":"C_LEX_040","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Missing '&' in scanf address-of operator",
   "incorrect":"#include <stdio.h>\nint main() {\n    int n;\n    scanf(\"%d\", n);\n    printf(\"%d\\n\", n);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int n;\n    scanf(\"%d\", &n);\n    printf(\"%d\\n\", n);\n    return 0;\n}"},

  {"id":"C_LEX_041","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'unsiged' misspelled — should be 'unsigned'",
   "incorrect":"#include <stdio.h>\nint main() {\n    unsiged int x = 255;\n    printf(\"%u\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    unsigned int x = 255;\n    printf(\"%u\\n\", x);\n    return 0;\n}"},

  {"id":"C_LEX_042","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'typdef' misspelled — should be 'typedef'",
   "incorrect":"#include <stdio.h>\ntypdef int Integer;\nint main() {\n    Integer x = 10;\n    printf(\"%d\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\ntypedef int Integer;\nint main() {\n    Integer x = 10;\n    printf(\"%d\\n\", x);\n    return 0;\n}"},

  {"id":"C_LEX_043","language":"C","error_type":"LEXICAL","error_label":1,"error_line":5,
   "error_desc":"'reutrn' misspelled — should be 'return'",
   "incorrect":"#include <stdio.h>\nint add(int a, int b) {\n    int sum = a + b;\n    printf(\"%d\\n\", sum);\n    reutrn sum;\n}",
   "correct":  "#include <stdio.h>\nint add(int a, int b) {\n    int sum = a + b;\n    printf(\"%d\\n\", sum);\n    return sum;\n}"},

  {"id":"C_LEX_044","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'conut' misspelled — should be 'count'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int conut = 0;\n    for (int i=0; i<5; i++) conut++;\n    printf(\"%d\\n\", conut);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int count = 0;\n    for (int i=0; i<5; i++) count++;\n    printf(\"%d\\n\", count);\n    return 0;\n}"},

  {"id":"C_LEX_045","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'PRINTF' not defined — C is case-sensitive",
   "incorrect":"#include <stdio.h>\nint main() {\n    PRINTF(\"Hello\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    printf(\"Hello\\n\");\n    return 0;\n}"},

  {"id":"C_LEX_046","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'long int' written as 'longg' — misspelled type",
   "incorrect":"#include <stdio.h>\nint main() {\n    longg x = 1234567890;\n    printf(\"%ld\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    long x = 1234567890;\n    printf(\"%ld\\n\", x);\n    return 0;\n}"},

  {"id":"C_LEX_047","language":"C","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'i++' written as 'i+++' — invalid token sequence",
   "incorrect":"#include <stdio.h>\nint main() {\n    int i = 0;\n    while (i < 5) { printf(\"%d \", i+++); }\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int i = 0;\n    while (i < 5) { printf(\"%d \", i++); }\n    return 0;\n}"},

  {"id":"C_LEX_048","language":"C","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'extern' misspelled as 'extrn'",
   "incorrect":"#include <stdio.h>\nextrn int globalVal;\nint main() {\n    printf(\"%d\\n\", globalVal);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nextern int globalVal;\nint main() {\n    printf(\"%d\\n\", globalVal);\n    return 0;\n}"},

  {"id":"C_LEX_049","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'sizof' misspelled — should be 'sizeof'",
   "incorrect":"#include <stdio.h>\nint main() {\n    printf(\"%zu\\n\", sizof(int));\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    printf(\"%zu\\n\", sizeof(int));\n    return 0;\n}"},

  {"id":"C_LEX_050","language":"C","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'#include' path uses wrong quotes — should use angle brackets for system header",
   "incorrect":"#include \"math.h\"\nint main() {\n    printf(\"%.2f\\n\", sqrt(9.0));\n    return 0;\n}",
   "correct":  "#include <stdio.h>\n#include <math.h>\nint main() {\n    printf(\"%.2f\\n\", sqrt(9.0));\n    return 0;\n}"},
]

C_SYNTAX = [
  {"id":"C_SYN_001","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing semicolon after return statement",
   "incorrect":"#include <stdio.h>\nint double_val(int x) {\n    return x * 2\n}\nint main() { printf(\"%d\\n\", double_val(5)); return 0; }",
   "correct":  "#include <stdio.h>\nint double_val(int x) {\n    return x * 2;\n}\nint main() { printf(\"%d\\n\", double_val(5)); return 0; }"},

  {"id":"C_SYN_002","language":"C","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Missing closing brace for if block",
   "incorrect":"#include <stdio.h>\nint main() {\n    if (1 > 0) {\n        printf(\"yes\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    if (1 > 0) {\n        printf(\"yes\\n\");\n    }\n    return 0;\n}"},

  {"id":"C_SYN_003","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing semicolon after variable declaration",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 5\n    printf(\"%d\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 5;\n    printf(\"%d\\n\", x);\n    return 0;\n}"},

  {"id":"C_SYN_004","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Extra semicolon after for loop header causes empty loop body",
   "incorrect":"#include <stdio.h>\nint main() {\n    for (int i=0; i<5; i++);\n        printf(\"%d\\n\", i);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    for (int i=0; i<5; i++)\n        printf(\"%d\\n\", i);\n    return 0;\n}"},

  {"id":"C_SYN_005","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing closing parenthesis in function call",
   "incorrect":"#include <stdio.h>\nint main() {\n    int a = 3, b = 4;\n    printf(\"%d\\n\", a + b;\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int a = 3, b = 4;\n    printf(\"%d\\n\", a + b);\n    return 0;\n}"},

  {"id":"C_SYN_006","language":"C","error_type":"SYNTAX","error_label":2,"error_line":2,
   "error_desc":"Missing return type in function definition",
   "incorrect":"#include <stdio.h>\nmultiply(int a, int b) {\n    return a * b;\n}\nint main() { printf(\"%d\\n\", multiply(3,4)); return 0; }",
   "correct":  "#include <stdio.h>\nint multiply(int a, int b) {\n    return a * b;\n}\nint main() { printf(\"%d\\n\", multiply(3,4)); return 0; }"},

  {"id":"C_SYN_007","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Assignment '=' used instead of '==' in condition",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 10;\n    if (x = 10) printf(\"ten\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 10;\n    if (x == 10) printf(\"ten\\n\");\n    return 0;\n}"},

  {"id":"C_SYN_008","language":"C","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Missing semicolon after printf statement",
   "incorrect":"#include <stdio.h>\nint main() {\n    int a=1, b=2;\n    int c = a+b;\n    printf(\"Sum=%d\\n\", c)\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int a=1, b=2;\n    int c = a+b;\n    printf(\"Sum=%d\\n\", c);\n    return 0;\n}"},

  {"id":"C_SYN_009","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"While loop condition missing parentheses",
   "incorrect":"#include <stdio.h>\nint main() {\n    int i = 0;\n    while i < 5 { printf(\"%d \", i); i++; }\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int i = 0;\n    while (i < 5) { printf(\"%d \", i); i++; }\n    return 0;\n}"},

  {"id":"C_SYN_010","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Nested function definition not allowed in C",
   "incorrect":"#include <stdio.h>\nint main() {\n    int helper(int x) { return x + 1; }\n    printf(\"%d\\n\", helper(5));\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint helper(int x) { return x + 1; }\nint main() {\n    printf(\"%d\\n\", helper(5));\n    return 0;\n}"},

  {"id":"C_SYN_011","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Trailing comma after last function argument",
   "incorrect":"#include <stdio.h>\nint add(int a, int b) { return a+b; }\nint main() {\n    printf(\"%d\\n\", add(3, 4,));\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint add(int a, int b) { return a+b; }\nint main() {\n    printf(\"%d\\n\", add(3, 4));\n    return 0;\n}"},

  {"id":"C_SYN_012","language":"C","error_type":"SYNTAX","error_label":2,"error_line":2,
   "error_desc":"Missing opening brace for function body",
   "incorrect":"#include <stdio.h>\nint cube(int x)\n    return x * x * x;\n}\nint main() { printf(\"%d\\n\", cube(3)); return 0; }",
   "correct":  "#include <stdio.h>\nint cube(int x) {\n    return x * x * x;\n}\nint main() { printf(\"%d\\n\", cube(3)); return 0; }"},

  {"id":"C_SYN_013","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Mismatched parentheses in expression",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 5;\n    int y = ((x + 3) * 2;\n    printf(\"%d\\n\", y);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 5;\n    int y = ((x + 3) * 2);\n    printf(\"%d\\n\", y);\n    return 0;\n}"},

  {"id":"C_SYN_014","language":"C","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"'else' without a matching 'if'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 3;\n    printf(\"%d\\n\", x);\n    else printf(\"no\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 3;\n    if (x > 0) printf(\"%d\\n\", x);\n    else printf(\"no\\n\");\n    return 0;\n}"},

  {"id":"C_SYN_015","language":"C","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Switch case missing break causes fall-through",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 1;\n    switch(x) {\n        case 1: printf(\"one\\n\");\n        case 2: printf(\"two\\n\"); break;\n    }\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 1;\n    switch(x) {\n        case 1: printf(\"one\\n\"); break;\n        case 2: printf(\"two\\n\"); break;\n    }\n    return 0;\n}"},

  {"id":"C_SYN_016","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Double semicolon in declaration",
   "incorrect":"#include <stdio.h>\nint main() {\n    int sum = 0;;\n    for (int i=1; i<=5; i++) sum += i;\n    printf(\"%d\\n\", sum);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int sum = 0;\n    for (int i=1; i<=5; i++) sum += i;\n    printf(\"%d\\n\", sum);\n    return 0;\n}"},

  {"id":"C_SYN_017","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing commas in printf argument list",
   "incorrect":"#include <stdio.h>\nint main() {\n    int a = 5, b = 10;\n    printf(\"%d + %d = %d\\n\" a b a+b);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int a = 5, b = 10;\n    printf(\"%d + %d = %d\\n\", a, b, a+b);\n    return 0;\n}"},

  {"id":"C_SYN_018","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"For loop header missing second semicolon",
   "incorrect":"#include <stdio.h>\nint main() {\n    for (int i=0; i<5) printf(\"%d \", i++);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    for (int i=0; i<5; i++) printf(\"%d \", i);\n    return 0;\n}"},

  {"id":"C_SYN_019","language":"C","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Struct member accessed with '.' on pointer — should use '->'",
   "incorrect":"#include <stdio.h>\n#include <stdlib.h>\ntypedef struct { int val; } Node;\nint main() {\n    Node *p = (Node*)malloc(sizeof(Node));\n    p.val = 10;\n    printf(\"%d\\n\", p->val);\n    free(p);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct { int val; } Node;\nint main() {\n    Node *p = (Node*)malloc(sizeof(Node));\n    p->val = 10;\n    printf(\"%d\\n\", p->val);\n    free(p);\n    return 0;\n}"},

  {"id":"C_SYN_020","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing closing bracket in array subscript",
   "incorrect":"#include <stdio.h>\nint main() {\n    int a[] = {10,20,30};\n    printf(\"%d\\n\", a[1);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int a[] = {10,20,30};\n    printf(\"%d\\n\", a[1]);\n    return 0;\n}"},

  {"id":"C_SYN_021","language":"C","error_type":"SYNTAX","error_label":2,"error_line":2,
   "error_desc":"Missing opening brace for main function body",
   "incorrect":"#include <stdio.h>\nint main()\n    printf(\"Hello\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    printf(\"Hello\\n\");\n    return 0;\n}"},

  {"id":"C_SYN_022","language":"C","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"do-while missing semicolon after while condition",
   "incorrect":"#include <stdio.h>\nint main() {\n    int i = 0;\n    do { printf(\"%d \", i); i++; }\n    while (i < 5)\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int i = 0;\n    do { printf(\"%d \", i); i++; }\n    while (i < 5);\n    return 0;\n}"},

  {"id":"C_SYN_023","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Ternary operator missing colon",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 7;\n    printf(\"%s\\n\", x > 5 ? \"big\" \"small\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 7;\n    printf(\"%s\\n\", x > 5 ? \"big\" : \"small\");\n    return 0;\n}"},

  {"id":"C_SYN_024","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"'=+' used instead of '+='",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 10;\n    x =+ 5;\n    printf(\"%d\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 10;\n    x += 5;\n    printf(\"%d\\n\", x);\n    return 0;\n}"},

  {"id":"C_SYN_025","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Comma used instead of semicolon between declarations",
   "incorrect":"#include <stdio.h>\nint main() {\n    int a = 1,\n    int b = 2;\n    printf(\"%d\\n\", a+b);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int a = 1;\n    int b = 2;\n    printf(\"%d\\n\", a+b);\n    return 0;\n}"},

  {"id":"C_SYN_026","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Dereferencing non-pointer variable",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 5;\n    printf(\"%d\\n\", *x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 5;\n    int *p = &x;\n    printf(\"%d\\n\", *p);\n    return 0;\n}"},

  {"id":"C_SYN_027","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing condition in while loop parentheses",
   "incorrect":"#include <stdio.h>\nint main() {\n    int i = 0;\n    while () { printf(\"%d\\n\", i); i++; if(i>=3) break; }\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int i = 0;\n    while (i < 3) { printf(\"%d\\n\", i); i++; }\n    return 0;\n}"},

  {"id":"C_SYN_028","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Extra closing brace at end of function",
   "incorrect":"#include <stdio.h>\nint getVal() {\n    return 99;\n}}\nint main() { printf(\"%d\\n\", getVal()); return 0; }",
   "correct":  "#include <stdio.h>\nint getVal() {\n    return 99;\n}\nint main() { printf(\"%d\\n\", getVal()); return 0; }"},

  {"id":"C_SYN_029","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Function prototype missing parameter types",
   "incorrect":"#include <stdio.h>\nint add(a, b);\nint main() { printf(\"%d\\n\", add(2,3)); return 0; }\nint add(int a, int b) { return a+b; }",
   "correct":  "#include <stdio.h>\nint add(int a, int b);\nint main() { printf(\"%d\\n\", add(2,3)); return 0; }\nint add(int a, int b) { return a+b; }"},

  {"id":"C_SYN_030","language":"C","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Variable declared inside case without braces",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 2;\n    switch(x) {\n        case 2: int y = 5; printf(\"%d\\n\", y); break;\n    }\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 2;\n    switch(x) {\n        case 2: { int y = 5; printf(\"%d\\n\", y); break; }\n    }\n    return 0;\n}"},

  {"id":"C_SYN_031","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"if-else dangling else ambiguity due to missing braces",
   "incorrect":"#include <stdio.h>\nint main() {\n    int a=5, b=10;\n    if (a > 3)\n    if (b > 8) printf(\"both\\n\");\n    else printf(\"only a\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int a=5, b=10;\n    if (a > 3) {\n        if (b > 8) printf(\"both\\n\");\n    } else printf(\"only a\\n\");\n    return 0;\n}"},

  {"id":"C_SYN_032","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Array size initializer mismatch — more elements than size",
   "incorrect":"#include <stdio.h>\nint main() {\n    int arr[3] = {1, 2, 3, 4, 5};\n    printf(\"%d\\n\", arr[0]);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int arr[5] = {1, 2, 3, 4, 5};\n    printf(\"%d\\n\", arr[0]);\n    return 0;\n}"},

  {"id":"C_SYN_033","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing semicolon after struct definition",
   "incorrect":"#include <stdio.h>\nstruct Point {\n    int x, y;\n}\nint main() {\n    struct Point p = {1,2};\n    printf(\"%d %d\\n\", p.x, p.y);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nstruct Point {\n    int x, y;\n};\nint main() {\n    struct Point p = {1,2};\n    printf(\"%d %d\\n\", p.x, p.y);\n    return 0;\n}"},

  {"id":"C_SYN_034","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"goto label missing colon",
   "incorrect":"#include <stdio.h>\nint main() {\n    goto myLabel;\n    myLabel\n    printf(\"reached\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    goto myLabel;\n    myLabel:\n    printf(\"reached\\n\");\n    return 0;\n}"},

  {"id":"C_SYN_035","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Postfix increment applied to expression — invalid lvalue",
   "incorrect":"#include <stdio.h>\nint main() {\n    int a=3, b=4;\n    printf(\"%d\\n\", (a+b)++);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int a=3, b=4;\n    int c = a+b;\n    c++;\n    printf(\"%d\\n\", c);\n    return 0;\n}"},

  {"id":"C_SYN_036","language":"C","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"switch case label missing colon",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 2;\n    switch(x) {\n        case 2 printf(\"two\\n\"); break;\n    }\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 2;\n    switch(x) {\n        case 2: printf(\"two\\n\"); break;\n    }\n    return 0;\n}"},

  {"id":"C_SYN_037","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Function called before declaration with no prototype",
   "incorrect":"#include <stdio.h>\nint main() {\n    printf(\"%d\\n\", square(5));\n    return 0;\n}\nint square(int x) { return x*x; }",
   "correct":  "#include <stdio.h>\nint square(int x);\nint main() {\n    printf(\"%d\\n\", square(5));\n    return 0;\n}\nint square(int x) { return x*x; }"},

  {"id":"C_SYN_038","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Bitwise AND '&' confused with logical AND '&&'",
   "incorrect":"#include <stdio.h>\nint main() {\n    int a=1, b=1;\n    if (a & b == 1) printf(\"both\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int a=1, b=1;\n    if (a == 1 && b == 1) printf(\"both\\n\");\n    return 0;\n}"},

  {"id":"C_SYN_039","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Void function returning a value",
   "incorrect":"#include <stdio.h>\nvoid printHello() {\n    printf(\"Hello\\n\");\n    return 1;\n}\nint main() { printHello(); return 0; }",
   "correct":  "#include <stdio.h>\nvoid printHello() {\n    printf(\"Hello\\n\");\n}\nint main() { printHello(); return 0; }"},

  {"id":"C_SYN_040","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing return statement in non-void function",
   "incorrect":"#include <stdio.h>\nint getNumber() {\n    int x = 42;\n}\nint main() { printf(\"%d\\n\", getNumber()); return 0; }",
   "correct":  "#include <stdio.h>\nint getNumber() {\n    int x = 42;\n    return x;\n}\nint main() { printf(\"%d\\n\", getNumber()); return 0; }"},

  {"id":"C_SYN_041","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Array subscript operator used on non-array variable",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 5;\n    printf(\"%d\\n\", x[0]);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x[] = {5};\n    printf(\"%d\\n\", x[0]);\n    return 0;\n}"},

  {"id":"C_SYN_042","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing opening parenthesis in if condition",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x = 5;\n    if x > 3) printf(\"big\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 5;\n    if (x > 3) printf(\"big\\n\");\n    return 0;\n}"},

  {"id":"C_SYN_043","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Modulo operator applied to float — invalid operand types",
   "incorrect":"#include <stdio.h>\nint main() {\n    float a = 5.5, b = 2.0;\n    printf(\"%.1f\\n\", a % b);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\n#include <math.h>\nint main() {\n    float a = 5.5, b = 2.0;\n    printf(\"%.1f\\n\", fmod(a, b));\n    return 0;\n}"},

  {"id":"C_SYN_044","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Declaring variable in for-loop init in C89 mode — needs C99",
   "incorrect":"#include <stdio.h>\nint main() {\n    for (int i=0; i<5; i++) printf(\"%d \", i);\n    printf(\"\\n\");\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int i;\n    for (i=0; i<5; i++) printf(\"%d \", i);\n    printf(\"\\n\");\n    return 0;\n}"},

  {"id":"C_SYN_045","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Assigning to array name directly — not allowed",
   "incorrect":"#include <stdio.h>\nint main() {\n    int a[] = {1,2,3};\n    int b[] = {4,5,6};\n    a = b;\n    return 0;\n}",
   "correct":  "#include <stdio.h>\n#include <string.h>\nint main() {\n    int a[] = {1,2,3};\n    int b[] = {4,5,6};\n    memcpy(a, b, sizeof(b));\n    return 0;\n}"},

  {"id":"C_SYN_046","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing semicolon inside for loop condition",
   "incorrect":"#include <stdio.h>\nint main() {\n    int s=0;\n    for (int i=0 i<5; i++) s+=i;\n    printf(\"%d\\n\",s);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int s=0;\n    for (int i=0; i<5; i++) s+=i;\n    printf(\"%d\\n\",s);\n    return 0;\n}"},

  {"id":"C_SYN_047","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Using '==' in assignment context — should use '='",
   "incorrect":"#include <stdio.h>\nint main() {\n    int x == 10;\n    printf(\"%d\\n\", x);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    int x = 10;\n    printf(\"%d\\n\", x);\n    return 0;\n}"},

  {"id":"C_SYN_048","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Enum definition missing semicolon",
   "incorrect":"#include <stdio.h>\nenum Color { RED, GREEN, BLUE }\nint main() {\n    enum Color c = GREEN;\n    printf(\"%d\\n\", c);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nenum Color { RED, GREEN, BLUE };\nint main() {\n    enum Color c = GREEN;\n    printf(\"%d\\n\", c);\n    return 0;\n}"},

  {"id":"C_SYN_049","language":"C","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Passing array by value instead of pointer",
   "incorrect":"#include <stdio.h>\nvoid fill(int arr[5]) {\n    for (int i=0; i<5; i++) arr[i] = i;\n}\nint main() {\n    int a[5];\n    fill(a);\n    printf(\"%d\\n\", a[0]);\n    return 0;\n}",
   "correct":  "#include <stdio.h>\nvoid fill(int *arr, int n) {\n    for (int i=0; i<n; i++) arr[i] = i;\n}\nint main() {\n    int a[5];\n    fill(a, 5);\n    printf(\"%d\\n\", a[0]);\n    return 0;\n}"},

  {"id":"C_SYN_050","language":"C","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Return outside of function",
   "incorrect":"#include <stdio.h>\nreturn 0;\nint main() {\n    printf(\"Hello\\n\");\n}",
   "correct":  "#include <stdio.h>\nint main() {\n    printf(\"Hello\\n\");\n    return 0;\n}"},
]

#  CPP  —  50 LEXICAL  +  50 SYNTAX

CPP_LEXICAL = [
  {"id":"CPP_LEX_001","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'cot' is undefined — should be 'cout'",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    cot << \"Hello\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello\" << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_002","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Unclosed string literal",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello World << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello World\" << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_003","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'clss' is not a keyword — should be 'class'",
   "incorrect":"#include <iostream>\nusing namespace std;\nclss Animal {\npublic:\n    void speak() { cout << \"...\" << endl; }\n};\nint main() { Animal a; a.speak(); return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Animal {\npublic:\n    void speak() { cout << \"...\" << endl; }\n};\nint main() { Animal a; a.speak(); return 0; }"},

  {"id":"CPP_LEX_004","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'1result' is an invalid identifier — starts with digit",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int 1result = 42;\n    cout << 1result << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int result1 = 42;\n    cout << result1 << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_005","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'templete' not a keyword — should be 'template'",
   "incorrect":"#include <iostream>\nusing namespace std;\ntemplete <typename T>\nT add(T a, T b) { return a + b; }\nint main() { cout << add(2,3) << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\ntemplate <typename T>\nT add(T a, T b) { return a + b; }\nint main() { cout << add(2,3) << endl; return 0; }"},

  {"id":"CPP_LEX_006","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":5,
   "error_desc":"'pubic' misspelled — should be 'public'",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Box {\n    int size;\npubic:\n    Box(int s): size(s) {}\n    int getSize() { return size; }\n};\nint main() { Box b(5); cout << b.getSize() << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Box {\n    int size;\npublic:\n    Box(int s): size(s) {}\n    int getSize() { return size; }\n};\nint main() { Box b(5); cout << b.getSize() << endl; return 0; }"},

  {"id":"CPP_LEX_007","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":5,
   "error_desc":"'vecotr' misspelled — should be 'vector'",
   "incorrect":"#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    vecotr<int> v = {1,2,3};\n    for (int x:v) cout << x << \" \";\n    return 0;\n}",
   "correct":  "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    vector<int> v = {1,2,3};\n    for (int x:v) cout << x << \" \";\n    return 0;\n}"},

  {"id":"CPP_LEX_008","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'Cout' (capital C) undefined — C++ is case-sensitive",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    Cout << \"test\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"test\" << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_009","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":5,
   "error_desc":"'===' operator does not exist in C++",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int x = 5;\n    if (x === 5) cout << \"yes\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int x = 5;\n    if (x == 5) cout << \"yes\" << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_010","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":1,
   "error_desc":"'#includ' is an invalid preprocessor directive",
   "incorrect":"#includ <iostream>\nusing namespace std;\nint main() { cout << \"hi\" << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() { cout << \"hi\" << endl; return 0; }"},

  {"id":"CPP_LEX_011","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":5,
   "error_desc":"'overide' misspelled — should be 'override'",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass A { public: virtual void f() {} };\nclass B : public A {\npublic: void f() overide { cout << \"B\" << endl; }\n};\nint main() { B b; b.f(); return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass A { public: virtual void f() {} };\nclass B : public A {\npublic: void f() override { cout << \"B\" << endl; }\n};\nint main() { B b; b.f(); return 0; }"},

  {"id":"CPP_LEX_012","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'sting' undeclared — should be 'string'",
   "incorrect":"#include <iostream>\n#include <string>\nusing namespace std;\nint main() { sting s = \"hello\"; cout << s << endl; return 0; }",
   "correct":  "#include <iostream>\n#include <string>\nusing namespace std;\nint main() { string s = \"hello\"; cout << s << endl; return 0; }"},

  {"id":"CPP_LEX_013","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'nmespace' not a keyword — should be 'namespace'",
   "incorrect":"#include <iostream>\nusing nmespace std;\nint main() { cout << \"hi\" << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() { cout << \"hi\" << endl; return 0; }"},

  {"id":"CPP_LEX_014","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Identifier '#result' contains illegal '#'",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int #result = 10;\n    cout << #result << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int result = 10;\n    cout << result << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_015","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'booleen' not valid — should be 'bool'",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() { booleen flag = true; cout << flag << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() { bool flag = true; cout << flag << endl; return 0; }"},

  {"id":"CPP_LEX_016","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'endll' undefined — should be 'endl'",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello\" << endll;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello\" << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_017","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'VOID' uppercase — not a C++ keyword",
   "incorrect":"#include <iostream>\nusing namespace std;\nVOID greet() { cout << \"Hi\" << endl; }\nint main() { greet(); return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nvoid greet() { cout << \"Hi\" << endl; }\nint main() { greet(); return 0; }"},

  {"id":"CPP_LEX_018","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":5,
   "error_desc":"'privte' misspelled — should be 'private'",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Car {\n    string brand;\nprivte:\n    int year;\npublic:\n    Car(string b, int y): brand(b), year(y) {}\n};\nint main() { Car c(\"Toyota\",2020); return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Car {\n    string brand;\nprivate:\n    int year;\npublic:\n    Car(string b, int y): brand(b), year(y) {}\n};\nint main() { Car c(\"Toyota\",2020); return 0; }"},

  {"id":"CPP_LEX_019","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"Missing closing '>' in template instantiation",
   "incorrect":"#include <iostream>\n#include <vector>\nusing namespace std;\nint main() { vector<int v = {1,2,3}; for(int x:v) cout<<x<<\" \"; return 0; }",
   "correct":  "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() { vector<int> v = {1,2,3}; for(int x:v) cout<<x<<\" \"; return 0; }"},

  {"id":"CPP_LEX_020","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'ENDL' uppercase not defined in C++",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello\" << ENDL;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello\" << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_021","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'<<' used for input — should be '>>'",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int x; cin << x;\n    cout << x << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int x; cin >> x;\n    cout << x << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_022","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'Nullptr' capital N is undefined",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int *p = Nullptr;\n    if (!p) cout << \"null\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int *p = nullptr;\n    if (!p) cout << \"null\" << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_023","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'conts' misspelled — should be 'const'",
   "incorrect":"#include <iostream>\nusing namespace std;\nconts int MAX = 100;\nint main() { cout << MAX << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nconst int MAX = 100;\nint main() { cout << MAX << endl; return 0; }"},

  {"id":"CPP_LEX_024","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":5,
   "error_desc":"'virtal' misspelled — should be 'virtual'",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Base {\npublic:\n    virtal void show() { cout << \"Base\" << endl; }\n};\nint main() { Base b; b.show(); return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Base {\npublic:\n    virtual void show() { cout << \"Base\" << endl; }\n};\nint main() { Base b; b.show(); return 0; }"},

  {"id":"CPP_LEX_025","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'mpa' undeclared — should be 'map'",
   "incorrect":"#include <iostream>\n#include <map>\nusing namespace std;\nint main() { mpa<int,int> m; m[1]=2; cout<<m[1]<<endl; return 0; }",
   "correct":  "#include <iostream>\n#include <map>\nusing namespace std;\nint main() { map<int,int> m; m[1]=2; cout<<m[1]<<endl; return 0; }"},

  {"id":"CPP_LEX_026","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'new[]' missing closing bracket",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int *arr = new int[5;\n    delete[] arr;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int *arr = new int[5];\n    delete[] arr;\n    return 0;\n}"},

  {"id":"CPP_LEX_027","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'functoin' misspelled — should be 'function'",
   "incorrect":"#include <iostream>\n#include <functional>\nusing namespace std;\nint apply(int x, functoin<int(int)> f) { return f(x); }\nint main() { cout << apply(3,[](int x){return x*2;}) << endl; return 0; }",
   "correct":  "#include <iostream>\n#include <functional>\nusing namespace std;\nint apply(int x, function<int(int)> f) { return f(x); }\nint main() { cout << apply(3,[](int x){return x*2;}) << endl; return 0; }"},

  {"id":"CPP_LEX_028","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'prtected' misspelled — should be 'protected'",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Shape {\nprtected:\n    double area;\npublic:\n    virtual void draw() {}\n};\nint main() { return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Shape {\nprotected:\n    double area;\npublic:\n    virtual void draw() {}\n};\nint main() { return 0; }"},

  {"id":"CPP_LEX_029","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'interace' not a C++ keyword",
   "incorrect":"#include <iostream>\nusing namespace std;\ninterace Drawable { virtual void draw() = 0; };\nint main() { return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Drawable { public: virtual void draw() = 0; };\nint main() { return 0; }"},

  {"id":"CPP_LEX_030","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'##' token not valid outside macros",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int a = 3 ## 4;\n    cout << a << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int a = 34;\n    cout << a << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_031","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'sortt' undefined — should be 'sort'",
   "incorrect":"#include <iostream>\n#include <algorithm>\n#include <vector>\nusing namespace std;\nint main() { vector<int> v={3,1,2}; sortt(v.begin(),v.end()); for(int x:v) cout<<x<<\" \"; return 0; }",
   "correct":  "#include <iostream>\n#include <algorithm>\n#include <vector>\nusing namespace std;\nint main() { vector<int> v={3,1,2}; sort(v.begin(),v.end()); for(int x:v) cout<<x<<\" \"; return 0; }"},

  {"id":"CPP_LEX_032","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'nullptr_t' used where 'nullptr' is intended",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int *p = nullptr_t;\n    if (!p) cout << \"null\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int *p = nullptr;\n    if (!p) cout << \"null\" << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_033","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":5,
   "error_desc":"'Woof' string not closed in cout",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Dog {\npublic:\n    void bark() { cout << \"Woof << endl; }\n};\nint main() { Dog d; d.bark(); return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Dog {\npublic:\n    void bark() { cout << \"Woof\" << endl; }\n};\nint main() { Dog d; d.bark(); return 0; }"},

  {"id":"CPP_LEX_034","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'auto_ptr' removed in C++17 — should use 'unique_ptr'",
   "incorrect":"#include <iostream>\n#include <memory>\nusing namespace std;\nint main() { auto_ptr<int> p(new int(5)); cout << *p << endl; return 0; }",
   "correct":  "#include <iostream>\n#include <memory>\nusing namespace std;\nint main() { unique_ptr<int> p = make_unique<int>(5); cout << *p << endl; return 0; }"},

  {"id":"CPP_LEX_035","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'<<=' used instead of '<<' for stream insertion",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    cout <<= \"Hello\" <<= endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello\" << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_036","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'sett' undefined — should be 'set'",
   "incorrect":"#include <iostream>\n#include <set>\nusing namespace std;\nint main() { sett<int> s={1,2,3}; for(int x:s) cout<<x<<\" \"; return 0; }",
   "correct":  "#include <iostream>\n#include <set>\nusing namespace std;\nint main() { set<int> s={1,2,3}; for(int x:s) cout<<x<<\" \"; return 0; }"},

  {"id":"CPP_LEX_037","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'RETURN' uppercase not a keyword in C++",
   "incorrect":"#include <iostream>\nusing namespace std;\nint square(int x) {\n    RETURN x * x;\n}\nint main() { cout << square(4) << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint square(int x) {\n    return x * x;\n}\nint main() { cout << square(4) << endl; return 0; }"},

  {"id":"CPP_LEX_038","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'deque' misspelled as 'dequeu'",
   "incorrect":"#include <iostream>\n#include <deque>\nusing namespace std;\nint main() { dequeu<int> d; d.push_back(1); cout<<d[0]<<endl; return 0; }",
   "correct":  "#include <iostream>\n#include <deque>\nusing namespace std;\nint main() { deque<int> d; d.push_back(1); cout<<d[0]<<endl; return 0; }"},

  {"id":"CPP_LEX_039","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'sizof' misspelled — should be 'sizeof'",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    cout << sizof(int) << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    cout << sizeof(int) << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_040","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'enumm' misspelled — should be 'enum'",
   "incorrect":"#include <iostream>\nusing namespace std;\nenumm Color { RED, GREEN, BLUE };\nint main() { Color c = RED; cout << c << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nenum Color { RED, GREEN, BLUE };\nint main() { Color c = RED; cout << c << endl; return 0; }"},

  {"id":"CPP_LEX_041","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'strnig' misspelled — should be 'string'",
   "incorrect":"#include <iostream>\n#include <string>\nusing namespace std;\nint main() { strnig s = \"world\"; cout << s << endl; return 0; }",
   "correct":  "#include <iostream>\n#include <string>\nusing namespace std;\nint main() { string s = \"world\"; cout << s << endl; return 0; }"},

  {"id":"CPP_LEX_042","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'**' not valid exponentiation in C++",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int r = 2 ** 10;\n    cout << r << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\n#include <cmath>\nusing namespace std;\nint main() {\n    int r = (int)pow(2, 10);\n    cout << r << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_043","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'#incldue' misspelled directive",
   "incorrect":"#incldue <iostream>\nusing namespace std;\nint main() { cout << 42 << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() { cout << 42 << endl; return 0; }"},

  {"id":"CPP_LEX_044","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'tupl' misspelled — should be 'tuple'",
   "incorrect":"#include <iostream>\n#include <tuple>\nusing namespace std;\nint main() { tupl<int,int> t = {1,2}; cout<<get<0>(t)<<endl; return 0; }",
   "correct":  "#include <iostream>\n#include <tuple>\nusing namespace std;\nint main() { tuple<int,int> t = {1,2}; cout<<get<0>(t)<<endl; return 0; }"},

  {"id":"CPP_LEX_045","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'piar' misspelled — should be 'pair'",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    piar<int,int> p = {1,2};\n    cout << p.first << \" \" << p.second << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    pair<int,int> p = {1,2};\n    cout << p.first << \" \" << p.second << endl;\n    return 0;\n}"},

  {"id":"CPP_LEX_046","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'statc' misspelled — should be 'static'",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Counter {\n    statc int count;\npublic:\n    static void inc() { count++; }\n    static int get() { return count; }\n};\nint Counter::count = 0;\nint main() { Counter::inc(); cout<<Counter::get()<<endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Counter {\n    static int count;\npublic:\n    static void inc() { count++; }\n    static int get() { return count; }\n};\nint Counter::count = 0;\nint main() { Counter::inc(); cout<<Counter::get()<<endl; return 0; }"},

  {"id":"CPP_LEX_047","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'stackk' misspelled — should be 'stack'",
   "incorrect":"#include <iostream>\n#include <stack>\nusing namespace std;\nint main() { stackk<int> s; s.push(1); cout<<s.top()<<endl; return 0; }",
   "correct":  "#include <iostream>\n#include <stack>\nusing namespace std;\nint main() { stack<int> s; s.push(1); cout<<s.top()<<endl; return 0; }"},

  {"id":"CPP_LEX_048","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'trow' misspelled — should be 'throw'",
   "incorrect":"#include <iostream>\nusing namespace std;\nvoid check(int x) { if(x<0) trow runtime_error(\"neg\"); }\nint main() { try{check(-1);}catch(exception&e){cout<<e.what()<<endl;} return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nvoid check(int x) { if(x<0) throw runtime_error(\"neg\"); }\nint main() { try{check(-1);}catch(exception&e){cout<<e.what()<<endl;} return 0; }"},

  {"id":"CPP_LEX_049","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'strcut' misspelled — should be 'struct'",
   "incorrect":"#include <iostream>\nusing namespace std;\nstrcut Point { int x, y; };\nint main() { Point p{1,2}; cout<<p.x<<\" \"<<p.y<<endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nstruct Point { int x, y; };\nint main() { Point p{1,2}; cout<<p.x<<\" \"<<p.y<<endl; return 0; }"},

  {"id":"CPP_LEX_050","language":"CPP","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'clas' misspelled — should be 'class' in template",
   "incorrect":"#include <iostream>\nusing namespace std;\ntemplate <clas T>\nT square(T x) { return x*x; }\nint main() { cout<<square(5)<<endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\ntemplate <class T>\nT square(T x) { return x*x; }\nint main() { cout<<square(5)<<endl; return 0; }"},
]

CPP_SYNTAX = [
  {"id":"CPP_SYN_001","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Missing semicolon after class definition",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Point {\n    int x, y;\n}\nint main() { return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Point {\n    int x, y;\n};\nint main() { return 0; }"},

  {"id":"CPP_SYN_002","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":6,
   "error_desc":"Constructor initializer list missing colon",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Box {\n    int size;\npublic:\n    Box(int s) size(s) {}\n};\nint main() { Box b(5); return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Box {\n    int size;\npublic:\n    Box(int s) : size(s) {}\n};\nint main() { Box b(5); return 0; }"},

  {"id":"CPP_SYN_003","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Missing closing brace for if block",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    if (true) {\n        cout << \"yes\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    if (true) {\n        cout << \"yes\" << endl;\n    }\n    return 0;\n}"},

  {"id":"CPP_SYN_004","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing semicolon after variable declaration",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int x = 10\n    cout << x << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int x = 10;\n    cout << x << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_005","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":6,
   "error_desc":"Range-based for loop missing colon",
   "incorrect":"#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    vector<int> v={1,2,3};\n    for (int x v) cout << x << \" \";\n    return 0;\n}",
   "correct":  "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() {\n    vector<int> v={1,2,3};\n    for (int x : v) cout << x << \" \";\n    return 0;\n}"},

  {"id":"CPP_SYN_006","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":6,
   "error_desc":"Pure virtual function missing '= 0'",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Shape {\npublic:\n    virtual ~Shape() {}\n    virtual double area();\n};\nint main() { return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Shape {\npublic:\n    virtual ~Shape() {}\n    virtual double area() = 0;\n};\nint main() { return 0; }"},

  {"id":"CPP_SYN_007","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Template parameter missing 'typename' or 'class'",
   "incorrect":"#include <iostream>\nusing namespace std;\ntemplate <T>\nT multiply(T a, T b) { return a * b; }\nint main() { cout << multiply(3, 4) << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\ntemplate <typename T>\nT multiply(T a, T b) { return a * b; }\nint main() { cout << multiply(3, 4) << endl; return 0; }"},

  {"id":"CPP_SYN_008","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Missing parentheses in while condition",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int i=0;\n    while i < 3 { cout << i++ << \" \"; }\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int i=0;\n    while (i < 3) { cout << i++ << \" \"; }\n    return 0;\n}"},

  {"id":"CPP_SYN_009","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Lambda missing '->' return type separator",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    auto square = [](int x) int { return x*x; };\n    cout << square(5) << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    auto square = [](int x) -> int { return x*x; };\n    cout << square(5) << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_010","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Catch block missing exception type",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    try { throw runtime_error(\"err\"); }\n    catch { cerr << \"caught\" << endl; }\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    try { throw runtime_error(\"err\"); }\n    catch (exception &e) { cerr << e.what() << endl; }\n    return 0;\n}"},

  {"id":"CPP_SYN_011","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Constructor called without 'new' keyword",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Dog { public: Dog() { cout<<\"Woof\"<<endl; } };\nint main() {\n    Dog *d = Dog();\n    delete d;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Dog { public: Dog() { cout<<\"Woof\"<<endl; } };\nint main() {\n    Dog *d = new Dog();\n    delete d;\n    return 0;\n}"},

  {"id":"CPP_SYN_012","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Using '.' on pointer — should use '->'",
   "incorrect":"#include <iostream>\nusing namespace std;\nstruct Node { int val; };\nint main() {\n    Node *n = new Node();\n    n.val = 10;\n    cout << n->val << endl;\n    delete n;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nstruct Node { int val; };\nint main() {\n    Node *n = new Node();\n    n->val = 10;\n    cout << n->val << endl;\n    delete n;\n    return 0;\n}"},

  {"id":"CPP_SYN_013","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing return in non-void function",
   "incorrect":"#include <iostream>\nusing namespace std;\nint getMax(int a, int b) {\n    if (a > b) return a;\n}\nint main() { cout << getMax(3,5) << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint getMax(int a, int b) {\n    if (a > b) return a;\n    return b;\n}\nint main() { cout << getMax(3,5) << endl; return 0; }"},

  {"id":"CPP_SYN_014","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Switch case label missing colon",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() { int x=2; switch(x){ case 1 cout<<\"one\"; break; case 2: cout<<\"two\"; break; } return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() { int x=2; switch(x){ case 1: cout<<\"one\"; break; case 2: cout<<\"two\"; break; } return 0; }"},

  {"id":"CPP_SYN_015","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":2,
   "error_desc":"Missing include — cout used without iostream",
   "incorrect":"int main() {\n    cout << \"Hello\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello\" << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_016","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"for loop uses commas instead of semicolons",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    for (int i=0, i<5, i++) cout << i << \" \";\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    for (int i=0; i<5; i++) cout << i << \" \";\n    return 0;\n}"},

  {"id":"CPP_SYN_017","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Missing closing parenthesis in sqrt call",
   "incorrect":"#include <iostream>\n#include <cmath>\nusing namespace std;\nint main() {\n    cout << sqrt(16.0 << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\n#include <cmath>\nusing namespace std;\nint main() {\n    cout << sqrt(16.0) << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_018","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Destructor name doesn't match class name",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass MyClass {\npublic:\n    ~WrongClass() { cout << \"destroyed\" << endl; }\n};\nint main() { MyClass m; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass MyClass {\npublic:\n    ~MyClass() { cout << \"destroyed\" << endl; }\n};\nint main() { MyClass m; return 0; }"},

  {"id":"CPP_SYN_019","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"try block without catch or finally",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    try { cout << \"try\" << endl; }\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    try { cout << \"try\" << endl; }\n    catch (...) {}\n    return 0;\n}"},

  {"id":"CPP_SYN_020","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Class inherits without access specifier",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass A {}; class B : A {};\nint main() { B b; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass A {}; class B : public A {};\nint main() { B b; return 0; }"},

  {"id":"CPP_SYN_021","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"static_cast missing target type",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    double x = 3.7;\n    int y = static_cast(x);\n    cout << y << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    double x = 3.7;\n    int y = static_cast<int>(x);\n    cout << y << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_022","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Comma instead of semicolon between statements",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int a = 5, cout << a << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int a = 5;\n    cout << a << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_023","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Member function defined outside class without scope resolution",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Counter { public: int count; void increment(); };\nvoid increment() { count++; }\nint main() { Counter c; c.count=0; c.increment(); cout<<c.count<<endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Counter { public: int count; void increment(); };\nvoid Counter::increment() { count++; }\nint main() { Counter c; c.count=0; c.increment(); cout<<c.count<<endl; return 0; }"},

  {"id":"CPP_SYN_024","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Multiple inheritance missing comma between base classes",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass A {}; class B {};\nclass C : public A public B {};\nint main() { C c; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass A {}; class B {};\nclass C : public A, public B {};\nint main() { C c; return 0; }"},

  {"id":"CPP_SYN_025","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"do-while missing semicolon after condition",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int i=0;\n    do { cout<<i<<\" \"; i++; } while(i<5)\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int i=0;\n    do { cout<<i<<\" \"; i++; } while(i<5);\n    return 0;\n}"},

  {"id":"CPP_SYN_026","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Namespace definition missing closing brace",
   "incorrect":"#include <iostream>\nnamespace Utils {\n    int square(int x) { return x*x; }\nint main() { std::cout << Utils::square(4) << std::endl; return 0; }",
   "correct":  "#include <iostream>\nnamespace Utils {\n    int square(int x) { return x*x; }\n}\nint main() { std::cout << Utils::square(4) << std::endl; return 0; }"},

  {"id":"CPP_SYN_027","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"delete called on stack (non-pointer) variable",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int x = 10;\n    delete x;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int *x = new int(10);\n    delete x;\n    return 0;\n}"},

  {"id":"CPP_SYN_028","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"vector initializer list missing closing brace",
   "incorrect":"#include <iostream>\n#include <vector>\nusing namespace std;\nint main() { vector<int> v = {1,2,3; cout<<v[0]<<endl; return 0; }",
   "correct":  "#include <iostream>\n#include <vector>\nusing namespace std;\nint main() { vector<int> v = {1,2,3}; cout<<v[0]<<endl; return 0; }"},

  {"id":"CPP_SYN_029","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":6,
   "error_desc":"Accessing private member outside class without getter",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Safe { int secret = 42; };\nint main() { Safe s; cout << s.secret << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Safe {\n    int secret = 42;\npublic:\n    int getSecret() { return secret; }\n};\nint main() { Safe s; cout << s.getSecret() << endl; return 0; }"},

  {"id":"CPP_SYN_030","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing nested template closing '>'",
   "incorrect":"#include <vector>\n#include <map>\nusing namespace std;\nint main() { map<int, vector<int> v; return 0; }",
   "correct":  "#include <vector>\n#include <map>\nusing namespace std;\nint main() { map<int, vector<int>> v; return 0; }"},

  {"id":"CPP_SYN_031","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Operator overload missing 'operator' keyword",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Vec { public: int x;\n    Vec +(const Vec &o) { return {x + o.x}; }\n};\nint main() { return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Vec { public: int x;\n    Vec operator+(const Vec &o) const { return {x + o.x}; }\n};\nint main() { return 0; }"},

  {"id":"CPP_SYN_032","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Dangling else due to missing braces",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int x=5;\n    if (x>3) cout<<\"big\"; cout<<\"test\";\n    else cout<<\"small\";\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int x=5;\n    if (x>3) { cout<<\"big\"; cout<<\"test\"; }\n    else cout<<\"small\";\n    return 0;\n}"},

  {"id":"CPP_SYN_033","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"'=' used instead of '==' in if condition",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int x = 5;\n    if (x = 5) cout << \"five\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int x = 5;\n    if (x == 5) cout << \"five\" << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_034","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing opening parenthesis in if condition",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int x = 5;\n    if x > 3) cout << \"big\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int x = 5;\n    if (x > 3) cout << \"big\" << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_035","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing semicolon after struct definition",
   "incorrect":"#include <iostream>\nusing namespace std;\nstruct Node { int val; int next; }\nint main() { Node n; n.val=1; cout<<n.val<<endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nstruct Node { int val; int next; };\nint main() { Node n; n.val=1; cout<<n.val<<endl; return 0; }"},

  {"id":"CPP_SYN_036","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Void function returning a value",
   "incorrect":"#include <iostream>\nusing namespace std;\nvoid sayHi() {\n    cout << \"Hi\" << endl;\n    return 1;\n}\nint main() { sayHi(); return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nvoid sayHi() {\n    cout << \"Hi\" << endl;\n}\nint main() { sayHi(); return 0; }"},

  {"id":"CPP_SYN_037","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Scope resolution used instead of dot for object member",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Box { public: int size = 5; };\nint main() { Box b; cout << b::size << endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Box { public: int size = 5; };\nint main() { Box b; cout << b.size << endl; return 0; }"},

  {"id":"CPP_SYN_038","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"super() used in C++ (Java syntax — should use BaseClass::method())",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass A { public: void hello() { cout<<\"A\"<<endl; } };\nclass B : public A {\npublic: void hello() { super(); cout<<\"B\"<<endl; }\n};\nint main() { B b; b.hello(); return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass A { public: void hello() { cout<<\"A\"<<endl; } };\nclass B : public A {\npublic: void hello() { A::hello(); cout<<\"B\"<<endl; }\n};\nint main() { B b; b.hello(); return 0; }"},

  {"id":"CPP_SYN_039","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Extra semicolon after class definition creates empty statement",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Empty {}; ;\nint main() { Empty e; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Empty {};\nint main() { Empty e; return 0; }"},

  {"id":"CPP_SYN_040","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing return type makes function implicitly int (invalid in C++11)",
   "incorrect":"#include <iostream>\nusing namespace std;\ncompute(int a, int b) {\n    return a * b;\n}\nint main() { cout<<compute(3,4)<<endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint compute(int a, int b) {\n    return a * b;\n}\nint main() { cout<<compute(3,4)<<endl; return 0; }"},

  {"id":"CPP_SYN_041","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"for loop missing increment expression",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    for (int i=0; i<5) cout<<i<<\" \";\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    for (int i=0; i<5; i++) cout<<i<<\" \";\n    return 0;\n}"},

  {"id":"CPP_SYN_042","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"enum class value accessed without scope resolution",
   "incorrect":"#include <iostream>\nusing namespace std;\nenum class Color { RED, GREEN, BLUE };\nint main() {\n    Color c = RED;\n    cout << (int)c << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nenum class Color { RED, GREEN, BLUE };\nint main() {\n    Color c = Color::RED;\n    cout << (int)c << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_043","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Array subscript missing closing bracket",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int a[3]={1,2,3};\n    cout << a[1 << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int a[3]={1,2,3};\n    cout << a[1] << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_044","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":6,
   "error_desc":"Calling super() — not valid syntax in C++",
   "incorrect":"#include <iostream>\nusing namespace std;\nclass Base { public: Base() { cout<<\"Base\"<<endl; } };\nclass Derived : public Base {\npublic:\n    Derived() { super(); cout<<\"Derived\"<<endl; }\n};\nint main() { Derived d; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nclass Base { public: Base() { cout<<\"Base\"<<endl; } };\nclass Derived : public Base {\npublic:\n    Derived() : Base() { cout<<\"Derived\"<<endl; }\n};\nint main() { Derived d; return 0; }"},

  {"id":"CPP_SYN_045","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Using '&' bitwise instead of '&&' logical in if condition",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int a=1, b=1;\n    if (a==1 & b==1) cout << \"both\" << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int a=1, b=1;\n    if (a==1 && b==1) cout << \"both\" << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_046","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing semicolon at end of return statement",
   "incorrect":"#include <iostream>\nusing namespace std;\nint getValue() {\n    return 42\n}\nint main() { cout<<getValue()<<endl; return 0; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint getValue() {\n    return 42;\n}\nint main() { cout<<getValue()<<endl; return 0; }"},

  {"id":"CPP_SYN_047","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Postfix increment on rvalue expression",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int a=2, b=3;\n    cout << (a+b)++ << endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int a=2, b=3;\n    int c = a+b;\n    cout << ++c << endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_048","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Ternary operator missing colon",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int x=7;\n    string s = x>5 ? \"big\" \"small\";\n    cout<<s<<endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int x=7;\n    string s = x>5 ? \"big\" : \"small\";\n    cout<<s<<endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_049","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Using '==' in variable initialisation instead of '='",
   "incorrect":"#include <iostream>\nusing namespace std;\nint main() {\n    int x == 10;\n    cout<<x<<endl;\n    return 0;\n}",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() {\n    int x = 10;\n    cout<<x<<endl;\n    return 0;\n}"},

  {"id":"CPP_SYN_050","language":"CPP","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Return statement outside function body",
   "incorrect":"#include <iostream>\nusing namespace std;\nreturn 0;\nint main() { cout<<\"Hello\"<<endl; }",
   "correct":  "#include <iostream>\nusing namespace std;\nint main() { cout<<\"Hello\"<<endl; return 0; }"},
]

#  JAVA  —  50 LEXICAL  +  50 SYNTAX

JAVA_LEXICAL = [
  {"id":"JAVA_LEX_001","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":1,
   "error_desc":"'pubic' misspelled — should be 'public'",
   "incorrect":"pubic class Hello {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}",
   "correct":  "public class Hello {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_LEX_002","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Ststem' undefined — should be 'System'",
   "incorrect":"public class Hello {\n    public static void main(String[] args) {\n        Ststem.out.println(\"Hello\");\n    }\n}",
   "correct":  "public class Hello {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_LEX_003","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'statik' misspelled — should be 'static'",
   "incorrect":"public class Demo {\n    public statik void main(String[] args) {\n        System.out.println(\"Hi\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hi\");\n    }\n}"},

  {"id":"JAVA_LEX_004","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Stirng' misspelled — should be 'String'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        Stirng name = \"Alice\";\n        System.out.println(name);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        String name = \"Alice\";\n        System.out.println(name);\n    }\n}"},

  {"id":"JAVA_LEX_005","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'1num' invalid identifier — starts with digit",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int 1num = 10;\n        System.out.println(1num);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int num1 = 10;\n        System.out.println(num1);\n    }\n}"},

  {"id":"JAVA_LEX_006","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Unclosed string literal",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello World);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello World\");\n    }\n}"},

  {"id":"JAVA_LEX_007","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":1,
   "error_desc":"'clas' misspelled — should be 'class'",
   "incorrect":"public clas Animal {\n    public void speak() { System.out.println(\"...\"); }\n    public static void main(String[] args) {\n        new Animal().speak();\n    }\n}",
   "correct":  "public class Animal {\n    public void speak() { System.out.println(\"...\"); }\n    public static void main(String[] args) {\n        new Animal().speak();\n    }\n}"},

  {"id":"JAVA_LEX_008","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'system' lowercase — should be 'System'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        system.out.println(\"Hello\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_LEX_009","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'boolan' misspelled — should be 'boolean'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        boolan flag = true;\n        System.out.println(flag);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        boolean flag = true;\n        System.out.println(flag);\n    }\n}"},

  {"id":"JAVA_LEX_010","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'printl' misspelled — should be 'println'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        System.out.printl(\"Hello\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_LEX_011","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":1,
   "error_desc":"'improt' misspelled — should be 'import'",
   "incorrect":"improt java.util.ArrayList;\npublic class Demo {\n    public static void main(String[] args) {\n        ArrayList<Integer> list = new ArrayList<>();\n        System.out.println(list);\n    }\n}",
   "correct":  "import java.util.ArrayList;\npublic class Demo {\n    public static void main(String[] args) {\n        ArrayList<Integer> list = new ArrayList<>();\n        System.out.println(list);\n    }\n}"},

  {"id":"JAVA_LEX_012","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'interger' misspelled — should be 'int'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        interger x = Integer.parseInt(\"42\");\n        System.out.println(x);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = Integer.parseInt(\"42\");\n        System.out.println(x);\n    }\n}"},

  {"id":"JAVA_LEX_013","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'flot' misspelled — should be 'float'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        flot pi = 3.14f;\n        System.out.println(pi);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        float pi = 3.14f;\n        System.out.println(pi);\n    }\n}"},

  {"id":"JAVA_LEX_014","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Math.Sqrt' — should be 'Math.sqrt' (case-sensitive)",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        double result = Math.Sqrt(16.0);\n        System.out.println(result);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        double result = Math.sqrt(16.0);\n        System.out.println(result);\n    }\n}"},

  {"id":"JAVA_LEX_015","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'Void' capital V is not a valid Java keyword",
   "incorrect":"public class Demo {\n    public static Void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_LEX_016","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Null' capital N is undefined — should be 'null'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        String s = Null;\n        System.out.println(s == null ? \"null\" : s);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        String s = null;\n        System.out.println(s == null ? \"null\" : s);\n    }\n}"},

  {"id":"JAVA_LEX_017","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'===' not a Java operator — should be '=='",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 5;\n        System.out.println(x === 5);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 5;\n        System.out.println(x == 5);\n    }\n}"},

  {"id":"JAVA_LEX_018","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"Char literal uses double quotes — should use single quotes",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        char c = \"A\";\n        System.out.println(c);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        char c = 'A';\n        System.out.println(c);\n    }\n}"},

  {"id":"JAVA_LEX_019","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'.length()' used on array — should be '.length'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int[] arr = {1,2,3,4,5};\n        System.out.println(arr.length());\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int[] arr = {1,2,3,4,5};\n        System.out.println(arr.length);\n    }\n}"},

  {"id":"JAVA_LEX_020","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'strng' undeclared — should be 'String'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        strng msg = \"Test\";\n        System.out.println(msg);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        String msg = \"Test\";\n        System.out.println(msg);\n    }\n}"},

  {"id":"JAVA_LEX_021","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'True' capital T — should be 'true'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        boolean b = True;\n        System.out.println(b);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        boolean b = true;\n        System.out.println(b);\n    }\n}"},

  {"id":"JAVA_LEX_022","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'**' not valid in Java — use Math.pow()",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        double result = 2 ** 8;\n        System.out.println(result);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        double result = Math.pow(2, 8);\n        System.out.println(result);\n    }\n}"},

  {"id":"JAVA_LEX_023","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'.lenght' misspelled — should be '.length'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        String s = \"Hello\";\n        System.out.println(s.lenght());\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        String s = \"Hello\";\n        System.out.println(s.length());\n    }\n}"},

  {"id":"JAVA_LEX_024","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'println' used without 'System.out' prefix",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 42;\n        println(x);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 42;\n        System.out.println(x);\n    }\n}"},

  {"id":"JAVA_LEX_025","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":1,
   "error_desc":"'inteface' misspelled — should be 'interface'",
   "incorrect":"public inteface Shape {\n    double area();\n}\nclass Circle implements Shape {\n    double r;\n    Circle(double r) { this.r = r; }\n    public double area() { return Math.PI * r * r; }\n    public static void main(String[] args) { System.out.println(new Circle(3).area()); }\n}",
   "correct":  "public interface Shape {\n    double area();\n}\nclass Circle implements Shape {\n    double r;\n    Circle(double r) { this.r = r; }\n    public double area() { return Math.PI * r * r; }\n    public static void main(String[] args) { System.out.println(new Circle(3).area()); }\n}"},

  {"id":"JAVA_LEX_026","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Hashmap' wrong casing — should be 'HashMap'",
   "incorrect":"import java.util.*;\npublic class Demo {\n    public static void main(String[] args) {\n        Hashmap<String,Integer> m = new HashMap<>();\n        m.put(\"a\",1);\n        System.out.println(m);\n    }\n}",
   "correct":  "import java.util.*;\npublic class Demo {\n    public static void main(String[] args) {\n        HashMap<String,Integer> m = new HashMap<>();\n        m.put(\"a\",1);\n        System.out.println(m);\n    }\n}"},

  {"id":"JAVA_LEX_027","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'extands' misspelled — should be 'extends'",
   "incorrect":"public class Animal { public void speak() { System.out.println(\"Animal\"); } }\nclass Dog extands Animal {\n    @Override public void speak() { System.out.println(\"Woof\"); }\n    public static void main(String[] args) { new Dog().speak(); }\n}",
   "correct":  "public class Animal { public void speak() { System.out.println(\"Animal\"); } }\nclass Dog extends Animal {\n    @Override public void speak() { System.out.println(\"Woof\"); }\n    public static void main(String[] args) { new Dog().speak(); }\n}"},

  {"id":"JAVA_LEX_028","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'Super()' capital S — should be 'super()'",
   "incorrect":"class Animal { Animal() { System.out.println(\"Animal\"); } }\nclass Dog extends Animal {\n    Dog() { Super(); System.out.println(\"Dog\"); }\n    public static void main(String[] args) { new Dog(); }\n}",
   "correct":  "class Animal { Animal() { System.out.println(\"Animal\"); } }\nclass Dog extends Animal {\n    Dog() { super(); System.out.println(\"Dog\"); }\n    public static void main(String[] args) { new Dog(); }\n}"},

  {"id":"JAVA_LEX_029","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'nextt' misspelled — should be 'next'",
   "incorrect":"import java.util.Scanner;\npublic class Demo {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.nextt();\n        System.out.println(s);\n    }\n}",
   "correct":  "import java.util.Scanner;\npublic class Demo {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String s = sc.next();\n        System.out.println(s);\n    }\n}"},

  {"id":"JAVA_LEX_030","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Arraylist' wrong casing — should be 'ArrayList'",
   "incorrect":"import java.util.*;\npublic class Demo {\n    public static void main(String[] args) {\n        Arraylist<Integer> list = new ArrayList<>();\n        list.add(1);\n        System.out.println(list);\n    }\n}",
   "correct":  "import java.util.*;\npublic class Demo {\n    public static void main(String[] args) {\n        ArrayList<Integer> list = new ArrayList<>();\n        list.add(1);\n        System.out.println(list);\n    }\n}"},

  {"id":"JAVA_LEX_031","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'$num' — '$' is bad practice and flagged as lexical warning",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int $num = 5;\n        System.out.println($num);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int num = 5;\n        System.out.println(num);\n    }\n}"},

  {"id":"JAVA_LEX_032","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Throws' capital T — should be 'throws'",
   "incorrect":"public class Demo {\n    public static void risky() Throws Exception {\n        throw new Exception(\"oops\");\n    }\n    public static void main(String[] args) throws Exception { risky(); }\n}",
   "correct":  "public class Demo {\n    public static void risky() throws Exception {\n        throw new Exception(\"oops\");\n    }\n    public static void main(String[] args) throws Exception { risky(); }\n}"},

  {"id":"JAVA_LEX_033","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'new()' used without class name",
   "incorrect":"import java.util.ArrayList;\npublic class Demo {\n    public static void main(String[] args) {\n        ArrayList<Integer> list = new();\n    }\n}",
   "correct":  "import java.util.ArrayList;\npublic class Demo {\n    public static void main(String[] args) {\n        ArrayList<Integer> list = new ArrayList<>();\n    }\n}"},

  {"id":"JAVA_LEX_034","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'False' capital F — should be 'false'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        boolean b = False;\n        System.out.println(b);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        boolean b = false;\n        System.out.println(b);\n    }\n}"},

  {"id":"JAVA_LEX_035","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":2,
   "error_desc":"'publc' misspelled — should be 'public'",
   "incorrect":"publc class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"test\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"test\");\n    }\n}"},

  {"id":"JAVA_LEX_036","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'Math.ABS' — should be 'Math.abs' (case-sensitive)",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = -5;\n        System.out.println(Math.ABS(x));\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = -5;\n        System.out.println(Math.abs(x));\n    }\n}"},

  {"id":"JAVA_LEX_037","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Linkedlist' wrong casing — should be 'LinkedList'",
   "incorrect":"import java.util.*;\npublic class Demo {\n    public static void main(String[] args) {\n        Linkedlist<Integer> list = new LinkedList<>();\n        list.add(1);\n        System.out.println(list);\n    }\n}",
   "correct":  "import java.util.*;\npublic class Demo {\n    public static void main(String[] args) {\n        LinkedList<Integer> list = new LinkedList<>();\n        list.add(1);\n        System.out.println(list);\n    }\n}"},

  {"id":"JAVA_LEX_038","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Implements' capital I — should be 'implements'",
   "incorrect":"public interface Greetable { void greet(); }\npublic class Hello Implements Greetable {\n    public void greet() { System.out.println(\"Hi\"); }\n    public static void main(String[] args) { new Hello().greet(); }\n}",
   "correct":  "public interface Greetable { void greet(); }\npublic class Hello implements Greetable {\n    public void greet() { System.out.println(\"Hi\"); }\n    public static void main(String[] args) { new Hello().greet(); }\n}"},

  {"id":"JAVA_LEX_039","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'System.Out.println' — 'Out' should be 'out'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 10;\n        System.Out.println(x);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 10;\n        System.out.println(x);\n    }\n}"},

  {"id":"JAVA_LEX_040","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'longg' misspelled — should be 'long'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        longg x = 9999999999L;\n        System.out.println(x);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        long x = 9999999999L;\n        System.out.println(x);\n    }\n}"},

  {"id":"JAVA_LEX_041","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'tostring()' should be 'toString()'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        Integer x = 42;\n        System.out.println(x.tostring());\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        Integer x = 42;\n        System.out.println(x.toString());\n    }\n}"},

  {"id":"JAVA_LEX_042","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'dobule' misspelled — should be 'double'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        dobule pi = 3.14159;\n        System.out.println(pi);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        double pi = 3.14159;\n        System.out.println(pi);\n    }\n}"},

  {"id":"JAVA_LEX_043","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Enum' capital E — should be 'enum'",
   "incorrect":"public class Demo {\n    Enum Season { SPRING, SUMMER, FALL, WINTER }\n    public static void main(String[] args) {\n        System.out.println(Season.SUMMER);\n    }\n}",
   "correct":  "public class Demo {\n    enum Season { SPRING, SUMMER, FALL, WINTER }\n    public static void main(String[] args) {\n        System.out.println(Season.SUMMER);\n    }\n}"},

  {"id":"JAVA_LEX_044","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'int[]' declared as 'int [' — missing closing bracket in type",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int[ arr = {1,2,3};\n        System.out.println(arr[0]);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int[] arr = {1,2,3};\n        System.out.println(arr[0]);\n    }\n}"},

  {"id":"JAVA_LEX_045","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Abstract' capital A — should be 'abstract'",
   "incorrect":"public Abstract class Shape {\n    public abstract double area();\n    public static void main(String[] args) {}\n}",
   "correct":  "public abstract class Shape {\n    public abstract double area();\n    public static void main(String[] args) {}\n}"},

  {"id":"JAVA_LEX_046","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'Math.ROUND' — should be 'Math.round'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        double x = 3.7;\n        System.out.println(Math.ROUND(x));\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        double x = 3.7;\n        System.out.println(Math.round(x));\n    }\n}"},

  {"id":"JAVA_LEX_047","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'byte' misspelled as 'byyte'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        byyte b = 127;\n        System.out.println(b);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        byte b = 127;\n        System.out.println(b);\n    }\n}"},

  {"id":"JAVA_LEX_048","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Final' capital F — should be 'final'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        Final int MAX = 100;\n        System.out.println(MAX);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        final int MAX = 100;\n        System.out.println(MAX);\n    }\n}"},

  {"id":"JAVA_LEX_049","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":4,
   "error_desc":"'Treemap' wrong casing — should be 'TreeMap'",
   "incorrect":"import java.util.*;\npublic class Demo {\n    public static void main(String[] args) {\n        Treemap<Integer,String> m = new TreeMap<>();\n        m.put(1,\"one\");\n        System.out.println(m);\n    }\n}",
   "correct":  "import java.util.*;\npublic class Demo {\n    public static void main(String[] args) {\n        TreeMap<Integer,String> m = new TreeMap<>();\n        m.put(1,\"one\");\n        System.out.println(m);\n    }\n}"},

  {"id":"JAVA_LEX_050","language":"Java","error_type":"LEXICAL","error_label":1,"error_line":3,
   "error_desc":"'Instanceof' capital I — should be 'instanceof'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        Object o = \"hello\";\n        System.out.println(o Instanceof String);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        Object o = \"hello\";\n        System.out.println(o instanceof String);\n    }\n}"},
]

JAVA_SYNTAX = [
  {"id":"JAVA_SYN_001","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing semicolon after variable declaration",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 10\n        System.out.println(x);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 10;\n        System.out.println(x);\n    }\n}"},

  {"id":"JAVA_SYN_002","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Missing closing brace for if block",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 5;\n        if (x > 0) {\n            System.out.println(\"positive\");\n        System.out.println(\"done\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 5;\n        if (x > 0) {\n            System.out.println(\"positive\");\n        }\n        System.out.println(\"done\");\n    }\n}"},

  {"id":"JAVA_SYN_003","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing parentheses in method call",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        String s = \"hello\";\n        System.out.println(s.toUpperCase;\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        String s = \"hello\";\n        System.out.println(s.toUpperCase());\n    }\n}"},

  {"id":"JAVA_SYN_004","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":2,
   "error_desc":"Method defined without return type",
   "incorrect":"public class Demo {\n    add(int a, int b) { return a + b; }\n    public static void main(String[] args) {\n        System.out.println(new Demo().add(2,3));\n    }\n}",
   "correct":  "public class Demo {\n    int add(int a, int b) { return a + b; }\n    public static void main(String[] args) {\n        System.out.println(new Demo().add(2,3));\n    }\n}"},

  {"id":"JAVA_SYN_005","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"catch block missing parentheses around exception",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        try {\n            int x = 1/0;\n        } catch Exception e {\n            System.out.println(e.getMessage());\n        }\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        try {\n            int x = 1/0;\n        } catch (Exception e) {\n            System.out.println(e.getMessage());\n        }\n    }\n}"},

  {"id":"JAVA_SYN_006","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"for-each loop missing colon",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int[] arr = {1,2,3};\n        for (int x arr) System.out.println(x);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int[] arr = {1,2,3};\n        for (int x : arr) System.out.println(x);\n    }\n}"},

  {"id":"JAVA_SYN_007","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"switch case missing break causes fall-through",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 1;\n        switch(x) {\n            case 1: System.out.println(\"one\");\n            case 2: System.out.println(\"two\"); break;\n        }\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 1;\n        switch(x) {\n            case 1: System.out.println(\"one\"); break;\n            case 2: System.out.println(\"two\"); break;\n        }\n    }\n}"},

  {"id":"JAVA_SYN_008","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Array initialised without 'new' keyword",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int[] arr = int[5];\n        arr[0] = 1;\n        System.out.println(arr[0]);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int[] arr = new int[5];\n        arr[0] = 1;\n        System.out.println(arr[0]);\n    }\n}"},

  {"id":"JAVA_SYN_009","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Missing semicolon after System.out.println",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int sum = 0;\n        for (int i=1; i<=5; i++) sum += i;\n        System.out.println(sum)\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int sum = 0;\n        for (int i=1; i<=5; i++) sum += i;\n        System.out.println(sum);\n    }\n}"},

  {"id":"JAVA_SYN_010","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Class extending multiple classes — not allowed in Java",
   "incorrect":"public class A {}\npublic class B {}\npublic class C extends A, B {\n    public static void main(String[] args) {}\n}",
   "correct":  "public class A {}\npublic interface B { void doSomething(); }\npublic class C extends A implements B {\n    public void doSomething() {}\n    public static void main(String[] args) {}\n}"},

  {"id":"JAVA_SYN_011","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Non-static method called in static context",
   "incorrect":"public class Demo {\n    public int getValue() { return 42; }\n    public static void main(String[] args) {\n        System.out.println(getValue());\n    }\n}",
   "correct":  "public class Demo {\n    public int getValue() { return 42; }\n    public static void main(String[] args) {\n        System.out.println(new Demo().getValue());\n    }\n}"},

  {"id":"JAVA_SYN_012","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"do-while missing semicolon after condition",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int i = 0;\n        do { System.out.println(i); i++; } while(i < 3)\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int i = 0;\n        do { System.out.println(i); i++; } while(i < 3);\n    }\n}"},

  {"id":"JAVA_SYN_013","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Instantiating abstract class directly",
   "incorrect":"public abstract class Shape {\n    public abstract double area();\n    public static void main(String[] args) {\n        Shape s = new Shape();\n        System.out.println(s.area());\n    }\n}",
   "correct":  "abstract class Shape { public abstract double area(); }\nclass Circle extends Shape {\n    double r; Circle(double r){this.r=r;}\n    public double area(){return Math.PI*r*r;}\n    public static void main(String[] args) {\n        Shape s = new Circle(3);\n        System.out.printf(\"%.2f%n\", s.area());\n    }\n}"},

  {"id":"JAVA_SYN_014","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"'=' used instead of '==' in if condition",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 10;\n        if (x = 10) System.out.println(\"ten\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 10;\n        if (x == 10) System.out.println(\"ten\");\n    }\n}"},

  {"id":"JAVA_SYN_015","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Constructor name doesn't match class name",
   "incorrect":"public class MyClass {\n    public WrongName() {\n        System.out.println(\"Created\");\n    }\n    public static void main(String[] args) { new MyClass(); }\n}",
   "correct":  "public class MyClass {\n    public MyClass() {\n        System.out.println(\"Created\");\n    }\n    public static void main(String[] args) { new MyClass(); }\n}"},

  {"id":"JAVA_SYN_016","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing closing parenthesis in while condition",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int i = 0;\n        while (i < 5 { System.out.println(i++); }\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int i = 0;\n        while (i < 5) { System.out.println(i++); }\n    }\n}"},

  {"id":"JAVA_SYN_017","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"throw without 'throws' declaration on method",
   "incorrect":"public class Demo {\n    public static void risky() {\n        throw new Exception(\"oops\");\n    }\n    public static void main(String[] args) { try{risky();}catch(Exception e){System.out.println(e.getMessage());} }\n}",
   "correct":  "public class Demo {\n    public static void risky() throws Exception {\n        throw new Exception(\"oops\");\n    }\n    public static void main(String[] args) { try{risky();}catch(Exception e){System.out.println(e.getMessage());} }\n}"},

  {"id":"JAVA_SYN_018","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Ternary operator missing colon",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 5;\n        String s = x > 3 ? \"big\" \"small\";\n        System.out.println(s);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 5;\n        String s = x > 3 ? \"big\" : \"small\";\n        System.out.println(s);\n    }\n}"},

  {"id":"JAVA_SYN_019","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Return statement in void method returning a value",
   "incorrect":"public class Demo {\n    public static void greet() {\n        System.out.println(\"Hello\");\n        return \"done\";\n    }\n    public static void main(String[] args) { greet(); }\n}",
   "correct":  "public class Demo {\n    public static void greet() {\n        System.out.println(\"Hello\");\n    }\n    public static void main(String[] args) { greet(); }\n}"},

  {"id":"JAVA_SYN_020","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"for loop condition uses assignment instead of comparison",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        for (int i=0; i=5; i++) System.out.println(i);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        for (int i=0; i<5; i++) System.out.println(i);\n    }\n}"},

  {"id":"JAVA_SYN_021","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing closing bracket in array access",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int[] arr = {10,20,30};\n        System.out.println(arr[1);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int[] arr = {10,20,30};\n        System.out.println(arr[1]);\n    }\n}"},

  {"id":"JAVA_SYN_022","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"finally block without try",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 5;\n        System.out.println(x);\n        finally { System.out.println(\"finally\"); }\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 5;\n        try { System.out.println(x); }\n        finally { System.out.println(\"finally\"); }\n    }\n}"},

  {"id":"JAVA_SYN_023","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"switch missing parentheses around selector",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x = 2;\n        switch x {\n            case 2: System.out.println(\"two\"); break;\n        }\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 2;\n        switch (x) {\n            case 2: System.out.println(\"two\"); break;\n        }\n    }\n}"},

  {"id":"JAVA_SYN_024","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":1,
   "error_desc":"Outer class declared as static — not allowed",
   "incorrect":"public static class Outer {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}",
   "correct":  "public class Outer {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_SYN_025","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"super() called after first statement in constructor",
   "incorrect":"class Animal { Animal() { System.out.println(\"Animal\"); } }\nclass Dog extends Animal {\n    Dog() {\n        System.out.println(\"Dog\");\n        super();\n    }\n    public static void main(String[] args) { new Dog(); }\n}",
   "correct":  "class Animal { Animal() { System.out.println(\"Animal\"); } }\nclass Dog extends Animal {\n    Dog() {\n        super();\n        System.out.println(\"Dog\");\n    }\n    public static void main(String[] args) { new Dog(); }\n}"},

  {"id":"JAVA_SYN_026","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Interface method has body without 'default' keyword",
   "incorrect":"public interface Flyable {\n    void fly() {\n        System.out.println(\"Flying\");\n    }\n}",
   "correct":  "public interface Flyable {\n    default void fly() {\n        System.out.println(\"Flying\");\n    }\n}"},

  {"id":"JAVA_SYN_027","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Field assigned outside constructor/method",
   "incorrect":"public class Demo {\n    int x;\n    x = 10;\n    public static void main(String[] args) { System.out.println(new Demo().x); }\n}",
   "correct":  "public class Demo {\n    int x = 10;\n    public static void main(String[] args) { System.out.println(new Demo().x); }\n}"},

  {"id":"JAVA_SYN_028","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing semicolon after return statement",
   "incorrect":"public class Demo {\n    public static int square(int x) {\n        return x * x\n    }\n    public static void main(String[] args) { System.out.println(square(5)); }\n}",
   "correct":  "public class Demo {\n    public static int square(int x) {\n        return x * x;\n    }\n    public static void main(String[] args) { System.out.println(square(5)); }\n}"},

  {"id":"JAVA_SYN_029","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Generic type argument missing in ArrayList declaration",
   "incorrect":"import java.util.ArrayList;\npublic class Demo {\n    public static void main(String[] args) {\n        ArrayList list = new ArrayList<Integer>();\n        list.add(1); list.add(\"two\");\n        System.out.println(list);\n    }\n}",
   "correct":  "import java.util.ArrayList;\npublic class Demo {\n    public static void main(String[] args) {\n        ArrayList<Integer> list = new ArrayList<>();\n        list.add(1);\n        System.out.println(list);\n    }\n}"},

  {"id":"JAVA_SYN_030","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing opening brace for class body",
   "incorrect":"public class Demo\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_SYN_031","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Comparing Strings with '==' instead of '.equals()'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        String a = new String(\"hello\");\n        String b = new String(\"hello\");\n        System.out.println(a == b);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        String a = new String(\"hello\");\n        String b = new String(\"hello\");\n        System.out.println(a.equals(b));\n    }\n}"},

  {"id":"JAVA_SYN_032","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing closing brace for method body",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_SYN_033","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":5,
   "error_desc":"Array out of bounds — loop condition uses '<=' instead of '<'",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int[] arr = new int[3];\n        for (int i = 0; i <= 3; i++)\n            arr[i] = i;\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int[] arr = new int[3];\n        for (int i = 0; i < 3; i++)\n            arr[i] = i;\n    }\n}"},

  {"id":"JAVA_SYN_034","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing opening brace for method",
   "incorrect":"public class Demo {\n    public static void main(String[] args)\n        System.out.println(\"Hello\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_SYN_035","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing parentheses around while condition",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int i=0;\n        while i < 5 { System.out.println(i++); }\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int i=0;\n        while (i < 5) { System.out.println(i++); }\n    }\n}"},

  {"id":"JAVA_SYN_036","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Dangling else without braces on outer if",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x=5;\n        if (x>3) System.out.println(\"big\"); System.out.println(\"test\");\n        else System.out.println(\"small\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x=5;\n        if (x>3) { System.out.println(\"big\"); System.out.println(\"test\"); }\n        else System.out.println(\"small\");\n    }\n}"},

  {"id":"JAVA_SYN_037","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"for loop uses commas instead of semicolons",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        for (int i=0, i<5, i++) System.out.println(i);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        for (int i=0; i<5; i++) System.out.println(i);\n    }\n}"},

  {"id":"JAVA_SYN_038","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing 'else' before final branch creates unreachable code",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x=3;\n        if (x>5) System.out.println(\"big\");\n        if (x>0) System.out.println(\"pos\");\n        System.out.println(\"neg\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x=3;\n        if (x>5) System.out.println(\"big\");\n        else if (x>0) System.out.println(\"pos\");\n        else System.out.println(\"neg\");\n    }\n}"},

  {"id":"JAVA_SYN_039","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing closing parenthesis in if condition",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x=5;\n        if (x > 3 System.out.println(\"big\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x=5;\n        if (x > 3) System.out.println(\"big\");\n    }\n}"},

  {"id":"JAVA_SYN_040","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Missing import — ArrayList used without import",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        ArrayList<Integer> list = new ArrayList<>();\n        list.add(1);\n        System.out.println(list);\n    }\n}",
   "correct":  "import java.util.ArrayList;\npublic class Demo {\n    public static void main(String[] args) {\n        ArrayList<Integer> list = new ArrayList<>();\n        list.add(1);\n        System.out.println(list);\n    }\n}"},

  {"id":"JAVA_SYN_041","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Switch case label missing colon",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x=1;\n        switch(x) { case 1 System.out.println(\"one\"); break; }\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x=1;\n        switch(x) { case 1: System.out.println(\"one\"); break; }\n    }\n}"},

  {"id":"JAVA_SYN_042","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing return statement in non-void method",
   "incorrect":"public class Demo {\n    public static int getVal() {\n        int x = 42;\n    }\n    public static void main(String[] args) { System.out.println(getVal()); }\n}",
   "correct":  "public class Demo {\n    public static int getVal() {\n        int x = 42;\n        return x;\n    }\n    public static void main(String[] args) { System.out.println(getVal()); }\n}"},

  {"id":"JAVA_SYN_043","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Extra semicolon after class declaration",
   "incorrect":"public class Demo; {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_SYN_044","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"Void function returning a value",
   "incorrect":"public class Demo {\n    public static void display() {\n        System.out.println(\"Hello\");\n        return 1;\n    }\n    public static void main(String[] args) { display(); }\n}",
   "correct":  "public class Demo {\n    public static void display() {\n        System.out.println(\"Hello\");\n    }\n    public static void main(String[] args) { display(); }\n}"},

  {"id":"JAVA_SYN_045","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing closing brace for for-loop block",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        for (int i=0; i<3; i++) {\n            System.out.println(i);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        for (int i=0; i<3; i++) {\n            System.out.println(i);\n        }\n    }\n}"},

  {"id":"JAVA_SYN_046","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":4,
   "error_desc":"'==' used in assignment — should be '='",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x == 10;\n        System.out.println(x);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x = 10;\n        System.out.println(x);\n    }\n}"},

  {"id":"JAVA_SYN_047","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing opening parenthesis in if condition",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        int x=5;\n        if x > 0) System.out.println(\"pos\");\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        int x=5;\n        if (x > 0) System.out.println(\"pos\");\n    }\n}"},

  {"id":"JAVA_SYN_048","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"for loop header missing second semicolon",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        for (int i=0; i<5) System.out.println(i++);\n    }\n}",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        for (int i=0; i<5; i++) System.out.println(i);\n    }\n}"},

  {"id":"JAVA_SYN_049","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Extra closing brace at end of class",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}}\n",
   "correct":  "public class Demo {\n    public static void main(String[] args) {\n        System.out.println(\"Hello\");\n    }\n}"},

  {"id":"JAVA_SYN_050","language":"Java","error_type":"SYNTAX","error_label":2,"error_line":3,
   "error_desc":"Missing import for HashMap",
   "incorrect":"public class Demo {\n    public static void main(String[] args) {\n        HashMap<String,Integer> m = new HashMap<>();\n        m.put(\"a\",1);\n        System.out.println(m);\n    }\n}",
   "correct":  "import java.util.HashMap;\npublic class Demo {\n    public static void main(String[] args) {\n        HashMap<String,Integer> m = new HashMap<>();\n        m.put(\"a\",1);\n        System.out.println(m);\n    }\n}"},
]

# ─────────────────────────────────────────────────────────────
# ASSEMBLE + SAVE
# ─────────────────────────────────────────────────────────────

def build_dataset():
    dataset = (
        C_LEXICAL    + C_SYNTAX    +
        CPP_LEXICAL  + CPP_SYNTAX  +
        JAVA_LEXICAL + JAVA_SYNTAX
    )

    from collections import Counter
    print("\n" + "=" * 60)
    print("  ANNOTATED DATASET SUMMARY")
    print("=" * 60)
    print(f"  Total samples : {len(dataset)}")
    print()
    for lang in ["C", "CPP", "Java"]:
        samples = [s for s in dataset if s["language"] == lang]
        ec = Counter(s["error_type"] for s in samples)
        print(f"  {lang:6s} → LEXICAL={ec['LEXICAL']:3d}  SYNTAX={ec['SYNTAX']:3d}  TOTAL={len(samples)}")
    print()
    ec_all = Counter(s["error_type"] for s in dataset)
    print(f"  LEXICAL total : {ec_all['LEXICAL']}")
    print(f"  SYNTAX  total : {ec_all['SYNTAX']}")
    print("=" * 60)

    os.makedirs("dataset", exist_ok=True)
    out_path = "dataset/annotated_dataset.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"\n[DATASET] Saved {len(dataset)} samples → {out_path}\n")
    return dataset


if __name__ == "__main__":
    build_dataset()