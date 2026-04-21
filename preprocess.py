import json
import csv
import os
import re
import ast
import math
import random
import hashlib
import unicodedata
from collections import Counter
from datetime import datetime

#   WEEK 7 — FULL PREPROCESSING PIPELINE

# SECTION 1: LABEL & LANGUAGE MAPS

LABEL_MAP = {
    "NONE"    : 0,
    "LEXICAL" : 1,
    "SYNTAX"  : 2,
}

LABEL_MAP_INV = {v: k for k, v in LABEL_MAP.items()}

LANGUAGE_MAP = {
    "C"    : 0,
    "CPP"  : 1,
    "Java" : 2,
}

LANGUAGE_MAP_INV = {v: k for k, v in LANGUAGE_MAP.items()}

# SECTION 2: KEYWORD DICTIONARIES

KEYWORDS = {
    "C": {
        "auto", "break", "case", "char", "const", "continue", "default",
        "do", "double", "else", "enum", "extern", "float", "for", "goto",
        "if", "inline", "int", "long", "register", "restrict", "return",
        "short", "signed", "sizeof", "static", "struct", "switch", "typedef",
        "union", "unsigned", "void", "volatile", "while",
        "_Bool", "_Complex", "_Imaginary",
    },
    "CPP": {
        "alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand",
        "bitor", "bool", "break", "case", "catch", "char", "char8_t",
        "char16_t", "char32_t", "class", "compl", "concept", "const",
        "consteval", "constexpr", "constinit", "const_cast", "continue",
        "co_await", "co_return", "co_yield", "decltype", "default", "delete",
        "do", "double", "dynamic_cast", "else", "enum", "explicit", "export",
        "extern", "false", "float", "for", "friend", "goto", "if", "inline",
        "int", "long", "mutable", "namespace", "new", "noexcept", "not",
        "not_eq", "nullptr", "operator", "or", "or_eq", "private",
        "protected", "public", "register", "reinterpret_cast", "requires",
        "return", "short", "signed", "sizeof", "static", "static_assert",
        "static_cast", "struct", "switch", "template", "this", "thread_local",
        "throw", "true", "try", "typedef", "typeid", "typename", "union",
        "unsigned", "using", "virtual", "void", "volatile", "wchar_t",
        "while", "xor", "xor_eq",
        # common stdlib
        "cout", "cin", "cerr", "endl", "string", "vector", "map", "set",
        "pair", "queue", "stack", "list", "array", "tuple", "optional",
        "unique_ptr", "shared_ptr", "weak_ptr", "make_shared", "make_unique",
        "override", "final",
    },
    "Java": {
        "abstract", "assert", "boolean", "break", "byte", "case", "catch",
        "char", "class", "const", "continue", "default", "do", "double",
        "else", "enum", "extends", "final", "finally", "float", "for",
        "goto", "if", "implements", "import", "instanceof", "int",
        "interface", "long", "native", "new", "package", "private",
        "protected", "public", "return", "short", "static", "strictfp",
        "super", "switch", "synchronized", "this", "throw", "throws",
        "transient", "try", "void", "volatile", "while",
        # common types & annotations
        "String", "System", "Override", "Deprecated", "SuppressWarnings",
        "Integer", "Double", "Boolean", "Long", "Float", "Short", "Byte",
        "Character", "Object", "Exception", "RuntimeException",
        "NullPointerException", "ArrayList", "HashMap", "List", "Map",
        "Set", "Iterator", "Optional", "Stream", "Arrays", "Math",
    },
}

# SECTION 3: COMMON LEXICAL ERROR PATTERNS

LEXICAL_PATTERNS = {
    "undefined_variable_hint" : re.compile(r'\b([a-z_]\w*)\b\s*(?:=|\+=|-=|\*=|/=)'),
    "string_not_closed"       : re.compile(r'"[^"\n]*$', re.MULTILINE),
    "char_not_closed"         : re.compile(r"'[^'\n]{2,}'"),
    "invalid_identifier_start": re.compile(r'\b\d+[a-zA-Z_]\w*\b'),
    "double_operator"         : re.compile(r'[+\-*/]{3,}'),
    "hex_literal"             : re.compile(r'\b0[xX][0-9a-fA-F]+\b'),
    "octal_literal"           : re.compile(r'\b0[0-7]+\b'),
    "float_literal"           : re.compile(r'\b\d+\.\d*[fFlL]?\b'),
    "char_escape"             : re.compile(r"'\\[ntrb0\\\"']'"),
    "comment_single"          : re.compile(r'//.*'),
    "comment_multi"           : re.compile(r'/\*.*?\*/', re.DOTALL),
    "preprocessor_directive"  : re.compile(r'^\s*#\s*\w+', re.MULTILINE),
}

# SECTION 4: COMMON SYNTAX ERROR PATTERNS

SYNTAX_PATTERNS = {
    "missing_semicolon_hint"  : re.compile(r'\)\s*\n\s*[^{;,)]'),
    "extra_semicolon"         : re.compile(r';\s*;'),
    "empty_block"             : re.compile(r'\{\s*\}'),
    "dangling_else"           : re.compile(r'\belse\b\s*(?!if\b|\{)'),
    "missing_return_type"     : re.compile(r'^\s*(\w+)\s*\(', re.MULTILINE),
    "unclosed_paren"          : re.compile(r'\([^)]*$', re.MULTILINE),
    "unclosed_brace"          : re.compile(r'\{[^}]*$', re.MULTILINE),
    "nested_function_def"     : re.compile(r'\{\s*\w+\s+\w+\s*\([^)]*\)\s*\{'),
    "comma_after_last_arg"    : re.compile(r',\s*\)'),
    "double_colon_java"       : re.compile(r'::\s*\w+'),
}

# SECTION 5: LOAD DATASET

def load_dataset(path="dataset.json"):
    """Load the annotated JSON dataset from disk."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"[ERROR] Dataset not found at: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"[PREPROCESS] Loaded {len(data)} samples from '{path}'")
    return data


# SECTION 6: TEXT CLEANING & NORMALIZATION

def normalize_unicode(text):
    """Normalize unicode characters to ASCII-safe equivalents."""
    return unicodedata.normalize('NFKC', text)

def remove_bom(text):
    """Remove BOM (Byte Order Mark) characters if present."""
    return text.lstrip('\ufeff')

def clean_code(code):
    """
    Full code cleaning pipeline:
    - Remove BOM & normalize unicode
    - Normalize line endings (CRLF → LF)
    - Strip trailing whitespace per line
    - Collapse excess blank lines (max 1 consecutive)
    - Strip leading/trailing blank lines
    - Replace tabs with 4 spaces
    """
    if not code:
        return ""

    code = remove_bom(code)
    code = normalize_unicode(code)
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    code = code.replace('\t', '    ')

    lines = [line.rstrip() for line in code.split('\n')]

    cleaned = []
    blank_count = 0
    for line in lines:
        if line == '':
            blank_count += 1
            if blank_count <= 1:
                cleaned.append(line)
        else:
            blank_count = 0
            cleaned.append(line)

    return '\n'.join(cleaned).strip()


def strip_comments(code, language):
    """
    Remove comments from code 
    """
    if not code:
        return code

    # Remove multi-line comments /* ... */
    code = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group().count('\n'), code, flags=re.DOTALL)

    # Remove single-line comments // ...
    code = re.sub(r'//[^\n]*', '', code)

    if language == "Java":
        # Also remove Javadoc
        code = re.sub(r'/\*\*.*?\*/', lambda m: '\n' * m.group().count('\n'), code, flags=re.DOTALL)

    return code


def remove_string_literals(code):
    """Replace string and char literals with placeholders to avoid false token matches."""
    code = re.sub(r'"(?:[^"\\]|\\.)*"', '"<STR>"', code)
    code = re.sub(r"'(?:[^'\\]|\\.)'",  "'<CHR>'", code)
    return code


# SECTION 7: TOKENIZATION

def tokenize(code):
    """
    Tokenize source code into a flat list of token strings.
    Captures: identifiers, numbers, operators, punctuation.
    """
    token_pattern = re.compile(
        r'0[xX][0-9a-fA-F]+'       # hex literals
        r'|\d+\.\d*[fFlL]?'         # float literals
        r'|\d+[lLuU]*'              # integer literals
        r'|[a-zA-Z_]\w*'            # identifiers / keywords
        r'|<<=|>>=|->|\+\+|--|<<|>>'# multi-char operators
        r'|&&|\|\||[+\-*/%&|^~!<>=]=?'
        r'|[{}()\[\];,.:?]'         # punctuation
        r'|"(?:[^"\\]|\\.)*"'       # string literals
        r"|'(?:[^'\\]|\\.)*'"       # char literals
    )
    return token_pattern.findall(code)


def tokenize_with_types(code, language):
    """
    Tokenize and classify each token into a type category.
    Returns a list of (token, type) tuples.
    """
    tokens = tokenize(code)
    kw_set = KEYWORDS.get(language, set())
    typed  = []

    for tok in tokens:
        if tok in kw_set:
            typed.append((tok, "KEYWORD"))
        elif re.fullmatch(r'[a-zA-Z_]\w*', tok):
            typed.append((tok, "IDENTIFIER"))
        elif re.fullmatch(r'0[xX][0-9a-fA-F]+', tok):
            typed.append((tok, "LITERAL_INT"))
        elif re.fullmatch(r'\d+[lLuU]*', tok):
            typed.append((tok, "LITERAL_INT"))
        elif re.fullmatch(r'\d+\.\d*[fFlL]?', tok):
            typed.append((tok, "LITERAL_FLOAT"))
        elif tok.startswith('"'):
            typed.append((tok, "LITERAL_STRING"))
        elif tok.startswith("'"):
            typed.append((tok, "LITERAL_CHAR"))
        elif re.fullmatch(r'[{}()\[\];,.:?]', tok):
            typed.append((tok, "PUNCTUATION"))
        elif re.fullmatch(r'[+\-*/%&|^~!<>=]=?|<<=|>>=|->|\+\+|--|<<|>>|&&|\|\|', tok):
            typed.append((tok, "OPERATOR"))
        else:
            typed.append((tok, "UNKNOWN"))

    return typed


def get_token_type_distribution(typed_tokens):
    """Return a Counter of token type frequencies."""
    return Counter(ttype for _, ttype in typed_tokens)


# SECTION 8: LABEL ENCODING

def encode_labels(data):
    """Attach numeric label columns for error type and language."""
    for sample in data:
        sample["error_label"]    = LABEL_MAP.get(sample.get("error_type", "NONE"), -1)
        sample["language_label"] = LANGUAGE_MAP.get(sample.get("language", ""), -1)
    return data


# SECTION 9: BASIC FEATURE EXTRACTION

def extract_basic_features(code, language):
    """
    Extract core numerical features:
    - line_count         : total lines
    - non_empty_lines    : lines with non-whitespace content
    - token_count        : total tokens (rough)
    - brace_balance      : { - }
    - paren_balance      : ( - )
    - bracket_balance    : [ - ]
    - angle_balance      : < - > (for templates / generics)
    - semicolon_count    : number of ;
    - has_main           : 1 if main present
    - avg_line_length    : average length of non-empty lines
    - max_line_length    : longest line
    - keyword_count      : keywords present
    - identifier_count   : unique identifiers
    - operator_count     : operator tokens
    - literal_count      : string + char + numeric literals
    - indent_depth_max   : max indentation level (in spaces/4)
    - indent_depth_avg   : average indentation depth
    - comment_line_count : lines that are pure comments
    - string_literal_count : number of string literals
    - char_literal_count   : number of char literals
    - numeric_literal_count: number of numeric literals
    - blank_line_ratio   : blank lines / total lines
    - code_density       : non-empty lines / total lines
    """
    if not code:
        return _zero_basic_features()

    lines     = code.split('\n')
    typed_tok = tokenize_with_types(code, language)
    kw_set    = KEYWORDS.get(language, set())

    non_empty     = [l for l in lines if l.strip()]
    line_lens     = [len(l) for l in non_empty]
    blank_lines   = len(lines) - len(non_empty)

    indent_depths = []
    for l in non_empty:
        stripped = l.lstrip()
        indent   = len(l) - len(stripped)
        indent_depths.append(indent // 4)

    type_dist    = get_token_type_distribution(typed_tok)
    identifiers  = set(tok for tok, ttype in typed_tok if ttype == "IDENTIFIER")

    comment_lines = sum(
        1 for l in lines if re.match(r'\s*//', l) or re.match(r'\s*\*', l)
    )

    return {
        "line_count"           : len(lines),
        "non_empty_lines"      : len(non_empty),
        "token_count"          : len(typed_tok),
        "brace_balance"        : code.count('{') - code.count('}'),
        "paren_balance"        : code.count('(') - code.count(')'),
        "bracket_balance"      : code.count('[') - code.count(']'),
        "angle_balance"        : code.count('<') - code.count('>'),
        "semicolon_count"      : code.count(';'),
        "has_main"             : 1 if re.search(r'\bmain\b', code) else 0,
        "avg_line_length"      : round(sum(line_lens) / len(line_lens), 2) if line_lens else 0.0,
        "max_line_length"      : max(line_lens) if line_lens else 0,
        "keyword_count"        : type_dist.get("KEYWORD", 0),
        "identifier_count"     : len(identifiers),
        "operator_count"       : type_dist.get("OPERATOR", 0),
        "literal_count"        : (type_dist.get("LITERAL_INT", 0) +
                                   type_dist.get("LITERAL_FLOAT", 0) +
                                   type_dist.get("LITERAL_STRING", 0) +
                                   type_dist.get("LITERAL_CHAR", 0)),
        "indent_depth_max"     : max(indent_depths) if indent_depths else 0,
        "indent_depth_avg"     : round(sum(indent_depths) / len(indent_depths), 2) if indent_depths else 0.0,
        "comment_line_count"   : comment_lines,
        "string_literal_count" : type_dist.get("LITERAL_STRING", 0),
        "char_literal_count"   : type_dist.get("LITERAL_CHAR", 0),
        "numeric_literal_count": type_dist.get("LITERAL_INT", 0) + type_dist.get("LITERAL_FLOAT", 0),
        "blank_line_ratio"     : round(blank_lines / len(lines), 4) if lines else 0.0,
        "code_density"         : round(len(non_empty) / len(lines), 4) if lines else 0.0,
    }


def _zero_basic_features():
    return {k: 0 for k in [
        "line_count", "non_empty_lines", "token_count",
        "brace_balance", "paren_balance", "bracket_balance", "angle_balance",
        "semicolon_count", "has_main", "avg_line_length", "max_line_length",
        "keyword_count", "identifier_count", "operator_count", "literal_count",
        "indent_depth_max", "indent_depth_avg", "comment_line_count",
        "string_literal_count", "char_literal_count", "numeric_literal_count",
        "blank_line_ratio", "code_density",
    ]}


# SECTION 10: ADVANCED LEXICAL FEATURES

def extract_lexical_features(code, language):
    """
    Advanced lexical analysis features:
    - unique_tokens          : vocabulary size
    - token_diversity        : unique / total token ratio (TTR)
    - top_identifiers        : top 5 most frequent identifiers
    - keyword_density        : keyword_count / token_count
    - identifier_avg_length  : average length of identifier names
    - long_identifier_count  : identifiers longer than 20 chars
    - camel_case_count       : identifiers in camelCase
    - snake_case_count       : identifiers in snake_case
    - upper_case_count       : identifiers in ALL_CAPS
    - numeric_in_ident_count : identifiers containing digits
    - undefined_var_hints    : potential undefined variable assignments
    - unclosed_string_count  : potentially unclosed string literals
    - invalid_id_count       : identifiers starting with digits
    - double_operator_count  : suspicious repeated operators
    """
    if not code:
        return _zero_lexical_features()

    typed_tok    = tokenize_with_types(code, language)
    all_tokens   = [tok for tok, _ in typed_tok]
    identifiers  = [tok for tok, ttype in typed_tok if ttype == "IDENTIFIER"]
    kw_set       = KEYWORDS.get(language, set())
    total        = len(all_tokens) if all_tokens else 1

    id_lengths   = [len(i) for i in identifiers]
    id_counter   = Counter(identifiers)
    top5         = [tok for tok, _ in id_counter.most_common(5)]

    camel  = sum(1 for i in identifiers if re.match(r'^[a-z]+(?:[A-Z][a-z0-9]+)+$', i))
    snake  = sum(1 for i in identifiers if re.match(r'^[a-z][a-z0-9_]+$', i) and '_' in i)
    upper  = sum(1 for i in identifiers if re.match(r'^[A-Z][A-Z0-9_]+$', i))
    numid  = sum(1 for i in identifiers if re.search(r'\d', i))
    longid = sum(1 for i in identifiers if len(i) > 20)

    undef_vars     = len(LEXICAL_PATTERNS["undefined_variable_hint"].findall(code))
    unclosed_str   = len(LEXICAL_PATTERNS["string_not_closed"].findall(code))
    invalid_id     = len(LEXICAL_PATTERNS["invalid_identifier_start"].findall(code))
    double_ops     = len(LEXICAL_PATTERNS["double_operator"].findall(code))
    hex_lits       = len(LEXICAL_PATTERNS["hex_literal"].findall(code))
    octal_lits     = len(LEXICAL_PATTERNS["octal_literal"].findall(code))

    return {
        "unique_tokens"          : len(set(all_tokens)),
        "token_diversity"        : round(len(set(all_tokens)) / total, 4),
        "top_identifiers"        : ",".join(top5),
        "keyword_density"        : round(sum(1 for t in all_tokens if t in kw_set) / total, 4),
        "identifier_avg_length"  : round(sum(id_lengths) / len(id_lengths), 2) if id_lengths else 0.0,
        "long_identifier_count"  : longid,
        "camel_case_count"       : camel,
        "snake_case_count"       : snake,
        "upper_case_count"       : upper,
        "numeric_in_ident_count" : numid,
        "undefined_var_hints"    : undef_vars,
        "unclosed_string_count"  : unclosed_str,
        "invalid_id_count"       : invalid_id,
        "double_operator_count"  : double_ops,
        "hex_literal_count"      : hex_lits,
        "octal_literal_count"    : octal_lits,
    }


def _zero_lexical_features():
    return {k: 0 for k in [
        "unique_tokens", "token_diversity", "top_identifiers",
        "keyword_density", "identifier_avg_length", "long_identifier_count",
        "camel_case_count", "snake_case_count", "upper_case_count",
        "numeric_in_ident_count", "undefined_var_hints", "unclosed_string_count",
        "invalid_id_count", "double_operator_count", "hex_literal_count",
        "octal_literal_count",
    ]}


# SECTION 11: ADVANCED SYNTAX FEATURES

def extract_syntax_features(code, language):
    """
    Advanced syntax structure features:
    - function_count         : number of function/method definitions
    - class_count            : number of class definitions
    - if_count               : number of if statements
    - else_count             : number of else branches
    - for_count              : number of for loops
    - while_count            : number of while loops
    - do_while_count         : number of do-while loops
    - switch_count           : number of switch statements
    - return_count           : number of return statements
    - nesting_depth_max      : max {} nesting depth
    - nesting_depth_avg      : average nesting depth per block
    - try_catch_count        : number of try-catch blocks (Java/C++)
    - include_import_count   : #include / import statements
    - extra_semicolons       : suspicious double semicolons
    - empty_block_count      : {} with nothing inside
    - dangling_else_count    : else without braces
    - missing_semi_hints     : lines ending without ; where expected
    - comma_after_arg_count  : trailing comma before )
    - ternary_count          : ternary operator usage
    - pointer_count          : pointer usage (C/C++)
    - reference_count        : reference usage (C++)
    - template_count         : template usage (C++)
    - annotation_count       : @annotations (Java)
    - lambda_count           : lambda expressions
    - operator_overload_count: operator overloading (C++)
    """
    if not code:
        return _zero_syntax_features()

    stripped = remove_string_literals(strip_comments(code, language))

    def count_kw(pattern):
        return len(re.findall(pattern, stripped))

    # Function / method definition patterns per language
    if language == "C":
        func_pat = r'\b\w[\w\s\*]+\s+\w+\s*\([^)]*\)\s*\{'
    elif language == "CPP":
        func_pat = r'\b(?:[\w:<>]+\s+)+\w+\s*\([^)]*\)\s*(?:const\s*)?\{'
    else:  # Java
        func_pat = r'\b(?:public|private|protected|static|final|abstract|synchronized)[\w\s<>\[\]]*\s+\w+\s*\([^)]*\)\s*(?:throws\s+[\w,\s]+)?\{'

    # Nesting depth analysis
    depth     = 0
    depths    = []
    for ch in code:
        if ch == '{':
            depth += 1
            depths.append(depth)
        elif ch == '}':
            depth = max(0, depth - 1)

    return {
        "function_count"          : len(re.findall(func_pat, stripped)),
        "class_count"             : count_kw(r'\bclass\b'),
        "if_count"                : count_kw(r'\bif\s*\('),
        "else_count"              : count_kw(r'\belse\b'),
        "for_count"               : count_kw(r'\bfor\s*\('),
        "while_count"             : count_kw(r'\bwhile\s*\('),
        "do_while_count"          : count_kw(r'\bdo\s*\{'),
        "switch_count"            : count_kw(r'\bswitch\s*\('),
        "return_count"            : count_kw(r'\breturn\b'),
        "nesting_depth_max"       : max(depths) if depths else 0,
        "nesting_depth_avg"       : round(sum(depths) / len(depths), 2) if depths else 0.0,
        "try_catch_count"         : count_kw(r'\btry\s*\{'),
        "include_import_count"    : len(re.findall(r'^\s*(?:#include|import)\b', code, re.MULTILINE)),
        "extra_semicolons"        : len(SYNTAX_PATTERNS["extra_semicolon"].findall(stripped)),
        "empty_block_count"       : len(SYNTAX_PATTERNS["empty_block"].findall(stripped)),
        "dangling_else_count"     : len(SYNTAX_PATTERNS["dangling_else"].findall(stripped)),
        "missing_semi_hints"      : len(SYNTAX_PATTERNS["missing_semicolon_hint"].findall(stripped)),
        "comma_after_arg_count"   : len(SYNTAX_PATTERNS["comma_after_last_arg"].findall(stripped)),
        "ternary_count"           : stripped.count('?'),
        "pointer_count"           : len(re.findall(r'\*\s*\w+', stripped)) if language in ("C", "CPP") else 0,
        "reference_count"         : len(re.findall(r'&\s*\w+', stripped)) if language == "CPP" else 0,
        "template_count"          : count_kw(r'\btemplate\s*<') if language == "CPP" else 0,
        "annotation_count"        : len(re.findall(r'@\w+', code)) if language == "Java" else 0,
        "lambda_count"            : (len(re.findall(r'\[.*?\]\s*\(', code)) if language == "CPP"
                                     else len(re.findall(r'->', code)) if language == "Java" else 0),
        "operator_overload_count" : count_kw(r'\boperator\s*[+\-*/<>=!&|^~%]+') if language == "CPP" else 0,
    }


def _zero_syntax_features():
    return {k: 0 for k in [
        "function_count", "class_count", "if_count", "else_count",
        "for_count", "while_count", "do_while_count", "switch_count",
        "return_count", "nesting_depth_max", "nesting_depth_avg",
        "try_catch_count", "include_import_count", "extra_semicolons",
        "empty_block_count", "dangling_else_count", "missing_semi_hints",
        "comma_after_arg_count", "ternary_count", "pointer_count",
        "reference_count", "template_count", "annotation_count",
        "lambda_count", "operator_overload_count",
    ]}


# SECTION 12: DIFF / DELTA FEATURES 

def extract_diff_features(incorrect_code, correct_code):
    """
    Compute difference-based features between incorrect and correct versions:
    - line_diff          : difference in line count
    - token_diff         : difference in token count
    - char_diff          : character length difference
    - semicolon_diff     : semicolon count difference
    - brace_diff         : brace balance difference
    - added_tokens       : tokens in correct but not incorrect
    - removed_tokens     : tokens in incorrect but not correct
    - edit_distance_approx : approximate edit distance (line-level)
    - similarity_ratio   : Jaccard similarity of token sets
    """
    if not incorrect_code or not correct_code:
        return _zero_diff_features()

    tok_inc = set(tokenize(incorrect_code))
    tok_cor = set(tokenize(correct_code))

    lines_inc = incorrect_code.split('\n')
    lines_cor = correct_code.split('\n')

    intersection = tok_inc & tok_cor
    union        = tok_inc | tok_cor
    jaccard      = round(len(intersection) / len(union), 4) if union else 1.0

    added   = tok_cor - tok_inc
    removed = tok_inc - tok_cor

    # Line-level Levenshtein approximation (fast, rough)
    set_inc = set(lines_inc)
    set_cor = set(lines_cor)
    edit_approx = len(set_inc.symmetric_difference(set_cor))

    return {
        "line_diff"            : len(lines_cor) - len(lines_inc),
        "token_diff"           : len(tokenize(correct_code)) - len(tokenize(incorrect_code)),
        "char_diff"            : len(correct_code) - len(incorrect_code),
        "semicolon_diff"       : correct_code.count(';') - incorrect_code.count(';'),
        "brace_diff"           : (correct_code.count('{') - correct_code.count('}')) -
                                  (incorrect_code.count('{') - incorrect_code.count('}')),
        "added_token_count"    : len(added),
        "removed_token_count"  : len(removed),
        "edit_distance_approx" : edit_approx,
        "similarity_ratio"     : jaccard,
    }


def _zero_diff_features():
    return {k: 0 for k in [
        "line_diff", "token_diff", "char_diff", "semicolon_diff",
        "brace_diff", "added_token_count", "removed_token_count",
        "edit_distance_approx", "similarity_ratio",
    ]}


# SECTION 13: METADATA FEATURES

def extract_metadata(sample, code):
    """
    Generate metadata / provenance features:
    - code_hash           : SHA-256 hash of code (deduplication)
    - error_line_ratio    : error_line / line_count
    - error_line_valid    : 1 if error_line is within bounds
    - has_error_desc      : 1 if error_desc is non-empty
    - error_desc_length   : character length of error description
    - processed_at        : ISO timestamp
    """
    code_hash        = hashlib.sha256(code.encode('utf-8')).hexdigest()[:16]
    line_count       = len(code.split('\n'))
    error_line       = sample.get("error_line", 0) or 0
    error_line_ratio = round(error_line / line_count, 4) if line_count else 0.0
    error_desc       = sample.get("error_desc", "") or ""

    return {
        "code_hash"         : code_hash,
        "error_line_ratio"  : error_line_ratio,
        "error_line_valid"  : 1 if 1 <= error_line <= line_count else 0,
        "has_error_desc"    : 1 if error_desc.strip() else 0,
        "error_desc_length" : len(error_desc),
        "processed_at"      : datetime.utcnow().isoformat(),
    }


# SECTION 14: FULL PREPROCESSING PIPELINE

def preprocess(data):
    """
    Full preprocessing pipeline:
    1. Encode labels
    2. Clean code (incorrect & correct)
    3. Extract all feature groups
    4. Build ML-ready flat records
    """
    data = encode_labels(data)
    processed = []

    for sample in data:
        lang = sample.get("language", "")

        # Select primary code (incorrect if error, else correct)
        raw_incorrect = sample.get("incorrect", "") or ""
        raw_correct   = sample.get("correct",   "") or ""

        code          = clean_code(raw_incorrect if sample["error_type"] != "NONE" else raw_correct)
        correct_code  = clean_code(raw_correct)

        # Feature extraction
        basic   = extract_basic_features(code, lang)
        lexical = extract_lexical_features(code, lang)
        syntax  = extract_syntax_features(code, lang)
        diff    = extract_diff_features(clean_code(raw_incorrect), correct_code)
        meta    = extract_metadata(sample, code)

        record = {
            "id"                      : sample.get("id", ""),
            "language"                : lang,
            "language_label"          : sample["language_label"],
            "error_type"              : sample.get("error_type", "NONE"),
            "error_label"             : sample["error_label"],
            "error_desc"              : sample.get("error_desc", ""),
            "error_line"              : sample.get("error_line", 0),

            "code"                    : code,
            "correct_code"            : correct_code,

            **{f"b_{k}": v for k, v in basic.items()},

            # ── Lexical Features ─────────────────────────────
            **{f"l_{k}": v for k, v in lexical.items()},

            # ── Syntax Features ──────────────────────────────
            **{f"s_{k}": v for k, v in syntax.items()},

            # ── Diff Features ─────────────────────────────────
            **{f"d_{k}": v for k, v in diff.items()},

            # ── Metadata ──────────────────────────────────────
            **{f"m_{k}": v for k, v in meta.items()},
        }

        processed.append(record)

    print(f"[PREPROCESS] Processed {len(processed)} samples "
          f"({sum(1 for d in processed if d['error_label']==1)} LEXICAL, "
          f"{sum(1 for d in processed if d['error_label']==2)} SYNTAX, "
          f"{sum(1 for d in processed if d['error_label']==0)} NONE)")
    return processed


# ──────────────────────────────────────────────────────────────
# SECTION 15: TRAIN / VAL / TEST SPLIT

def train_val_test_split(data, val_ratio=0.1, test_ratio=0.2, seed=42):
    """
    Stratified 3-way split by language to preserve class balance.
    Returns (train, val, test).
    """
    random.seed(seed)
    train, val, test = [], [], []

    languages = list(set(d["language"] for d in data))
    for lang in languages:
        subset = [d for d in data if d["language"] == lang]
        random.shuffle(subset)
        n         = len(subset)
        n_test    = max(1, int(n * test_ratio))
        n_val     = max(1, int(n * val_ratio))
        n_train   = n - n_test - n_val

        train.extend(subset[:n_train])
        val.extend(subset[n_train:n_train + n_val])
        test.extend(subset[n_train + n_val:])

    random.shuffle(train)
    random.shuffle(val)
    random.shuffle(test)

    print(f"[PREPROCESS] Train : {len(train)} | Val : {len(val)} | Test : {len(test)}")
    return train, val, test


def train_test_split(data, test_ratio=0.2, seed=42):
    train, _, test = train_val_test_split(data, val_ratio=0.0, test_ratio=test_ratio, seed=seed)
    print(f"[PREPROCESS] Train samples : {len(train)}")
    print(f"[PREPROCESS] Test  samples : {len(test)}")
    return train, test


# SECTION 16: SAVE PREPROCESSED DATA

def _save_json(records, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"[PREPROCESS] Saved → {path}")


def _save_csv(records, path):
    if not records:
        return
    flat = []
    for r in records:
        flat.append({k: (str(v) if isinstance(v, (list, dict)) else v)
                     for k, v in r.items()})
    fields = list(flat[0].keys())
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(flat)
    print(f"[PREPROCESS] Saved → {path}")


def save_preprocessed(train, test, val=None, out_dir="dataset"):
    os.makedirs(out_dir, exist_ok=True)

    _save_json(train, os.path.join(out_dir, "train.json"))
    _save_json(test,  os.path.join(out_dir, "test.json"))
    _save_csv(train,  os.path.join(out_dir, "train.csv"))
    _save_csv(test,   os.path.join(out_dir, "test.csv"))

    if val:
        _save_json(val, os.path.join(out_dir, "val.json"))
        _save_csv(val,  os.path.join(out_dir, "val.csv"))


# SECTION 17: DATA VALIDATION

REQUIRED_FIELDS = ["id", "language", "error_type", "correct"]

def validate_dataset(data):
    
    valid, invalid = [], []
    for i, sample in enumerate(data):
        issues = []
        for field in REQUIRED_FIELDS:
            if field not in sample or sample[field] is None:
                issues.append(f"missing field '{field}'")
        if sample.get("error_type") not in LABEL_MAP:
            issues.append(f"unknown error_type '{sample.get('error_type')}'")
        if sample.get("language") not in LANGUAGE_MAP:
            issues.append(f"unknown language '{sample.get('language')}'")
        if issues:
            sample["_validation_issues"] = "; ".join(issues)
            invalid.append(sample)
        else:
            valid.append(sample)

    print(f"[VALIDATE] Valid: {len(valid)} | Invalid: {len(invalid)}")
    if invalid:
        print(f"[VALIDATE] WARNING: {len(invalid)} samples skipped due to validation errors.")
    return valid, invalid


# SECTION 18: DEDUPLICATION

def deduplicate(data):
    
    seen    = set()
    unique  = []
    dupes   = 0
    for sample in data:
        key = hashlib.md5(
            (sample.get("language","") + (sample.get("incorrect","") or sample.get("correct",""))).encode()
        ).hexdigest()
        if key not in seen:
            seen.add(key)
            unique.append(sample)
        else:
            dupes += 1
    print(f"[PREPROCESS] Deduplicated: removed {dupes} duplicates, {len(unique)} remain")
    return unique


# SECTION 19: FEATURE SUMMARY REPORT

def _feature_stats(all_data, feat):
    vals = [d[feat] for d in all_data if isinstance(d.get(feat), (int, float))]
    if not vals:
        return {"min": "N/A", "max": "N/A", "avg": "N/A"}
    return {
        "min": min(vals),
        "max": max(vals),
        "avg": round(sum(vals) / len(vals), 3),
    }


def print_report(train, test, val=None):
    """Print a comprehensive preprocessing summary report."""
    all_data = train + (val or []) + test
    print("\n" + "═" * 65)
    print("   PREPROCESSING REPORT")
    print("═" * 65)
    print(f"   Generated : {datetime.utcnow().isoformat()} UTC")
    print(f"   Total     : {len(all_data)} samples")

    print("\n  ── Label Distribution ──────────────────────────────")
    for label, val_ in LABEL_MAP.items():
        count = sum(1 for d in all_data if d["error_label"] == val_)
        bar   = "█" * (count // max(1, len(all_data) // 30))
        print(f"    {label:10s} (label={val_}) : {count:4d} samples  {bar}")

    print("\n  ── Language Distribution ───────────────────────────")
    for lang, val_ in LANGUAGE_MAP.items():
        count = sum(1 for d in all_data if d["language_label"] == val_)
        bar   = "█" * (count // max(1, len(all_data) // 30))
        print(f"    {lang:6s} (label={val_}) : {count:4d} samples  {bar}")

    print("\n  ── Split Summary ───────────────────────────────────")
    print(f"    Train : {len(train)}")
    if val:
        print(f"    Val   : {len(val)}")
    print(f"    Test  : {len(test)}")

    print("\n  ──  Basic Feature Ranges ────────────────────────────")
    for feat in ["b_line_count", "b_token_count", "b_keyword_count",
                 "b_identifier_count", "b_semicolon_count", "b_nesting_depth_max" if "b_nesting_depth_max" in (all_data[0] if all_data else {}) else "b_indent_depth_max"]:
        if not all_data or feat not in all_data[0]:
            continue
        s = _feature_stats(all_data, feat)
        print(f"    {feat:28s} : min={s['min']}  max={s['max']}  avg={s['avg']}")

    print("\n  ── Lexical Feature Ranges ──────────────────────────")
    for feat in ["l_unique_tokens", "l_token_diversity", "l_keyword_density",
                 "l_camel_case_count", "l_snake_case_count"]:
        if not all_data or feat not in all_data[0]:
            continue
        s = _feature_stats(all_data, feat)
        print(f"    {feat:28s} : min={s['min']}  max={s['max']}  avg={s['avg']}")

    print("\n  ── Syntax Feature Ranges ───────────────────────────")
    for feat in ["s_function_count", "s_if_count", "s_for_count",
                 "s_nesting_depth_max", "s_return_count"]:
        if not all_data or feat not in all_data[0]:
            continue
        s = _feature_stats(all_data, feat)
        print(f"    {feat:28s} : min={s['min']}  max={s['max']}  avg={s['avg']}")

    print("\n  ── Diff Feature Ranges ─────────────────────────────")
    for feat in ["d_similarity_ratio", "d_edit_distance_approx", "d_token_diff"]:
        if not all_data or feat not in all_data[0]:
            continue
        s = _feature_stats(all_data, feat)
        print(f"    {feat:28s} : min={s['min']}  max={s['max']}  avg={s['avg']}")

    print("═" * 65)


# SECTION 20: EXPORT FEATURE SCHEMA

def export_feature_schema(processed, out_dir="dataset"):
    """
    Save a JSON schema listing all feature names, their types,
    and which group they belong to (basic, lexical, syntax, diff, meta).
    Useful for downstream model input validation.
    """
    if not processed:
        return
    os.makedirs(out_dir, exist_ok=True)
    schema = {}
    for key, val in processed[0].items():
        if key.startswith("b_"):   group = "basic"
        elif key.startswith("l_"): group = "lexical"
        elif key.startswith("s_"): group = "syntax"
        elif key.startswith("d_"): group = "diff"
        elif key.startswith("m_"): group = "metadata"
        else:                       group = "identity"
        schema[key] = {
            "group"      : group,
            "dtype"      : type(val).__name__,
            "sample_val" : str(val)[:80],
        }
    path = os.path.join(out_dir, "feature_schema.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
    print(f"[PREPROCESS] Feature schema saved → {path}  ({len(schema)} features)")


# SECTION 21: AUGMENTATION (optional)

def augment_whitespace(code, seed=None):
    """
    Simple augmentation: randomly add/remove blank lines between functions.
    Preserves semantic equivalence for training diversity.
    """
    if seed is not None:
        random.seed(seed)
    lines   = code.split('\n')
    augmented = []
    for line in lines:
        augmented.append(line)
        if line.strip() == '' and random.random() < 0.3:
            continue   # randomly drop blank line
        elif line.strip().endswith('{') and random.random() < 0.2:
            augmented.append('')  # add blank line after {
    return '\n'.join(augmented)


def augment_dataset(data, augment_ratio=0.2, seed=42):
    """
    Augment training data by creating slightly modified copies of NONE samples.
    Only whitespace-level changes — labels are preserved.
    """
    random.seed(seed)
    augmented = []
    none_samples = [d for d in data if d["error_type"] == "NONE"]
    n_aug = int(len(none_samples) * augment_ratio)
    chosen = random.sample(none_samples, min(n_aug, len(none_samples)))

    for sample in chosen:
        new_sample = dict(sample)
        new_sample["id"]   = sample["id"] + "_aug"
        new_sample["code"] = augment_whitespace(sample["code"], seed=random.randint(0, 9999))
        augmented.append(new_sample)

    print(f"[AUGMENT] Added {len(augmented)} augmented NONE samples")
    return data + augmented


# MAIN PIPELINE

if __name__ == "__main__":
    print("\n" + "═" * 65)
    print("   LEXICAL & SYNTAX PREPROCESSING PIPELINE")
    print("═" * 65)

    # ── Step 1: Load ──────────────────────────────────────────
    raw_data = load_dataset("dataset/annotated_dataset.json")

    # ── Step 2: Validate ─────────────────────────────────────
    raw_data, invalid = validate_dataset(raw_data)
    if invalid:
        _save_json(invalid, "dataset/invalid_samples.json")

    # ── Step 3: Deduplicate ───────────────────────────────────
    raw_data = deduplicate(raw_data)

    # ── Step 4: Full preprocessing ───────────────────────────
    processed = preprocess(raw_data)

    # ── Step 5: (Optional) Augment training data ─────────────
    # processed = augment_dataset(processed, augment_ratio=0.2)

    # ── Step 6: Split ─────────────────────────────────────────
    train, val, test = train_val_test_split(processed, val_ratio=0.1, test_ratio=0.2)

    # ── Step 7: Save ──────────────────────────────────────────
    save_preprocessed(train, test, val=val, out_dir="dataset")

    # ── Step 8: Export Feature Schema ────────────────────────
    export_feature_schema(processed, out_dir="dataset")

    # ── Step 9: Report ───────────────────────────────────────
    print_report(train, test, val=val)

    print("\n[PREPROCESS] Pipeline complete ✓")
    print("[PREPROCESS] Output files in dataset/ folder.")
    print("═" * 65)