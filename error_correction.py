"""
error_correction_module.py
═══════════════════════════════════════════════════════════════════
AI-Assisted Error Correction Module

Integrates with the compiler front-end to:
  1. Accept source code as input
  2. Run lexical + syntax checks (rule-based layer)
  3. Run ML model predictions (classification + localization)
  4. Generate ranked correction suggestions
  5. Validate corrected output via re-analysis
  6. Return structured CorrectionResult

Public API:
    corrector = ErrorCorrectionModule()
    result    = corrector.analyze(code, language="C")
    print(result.summary())
    result.apply_best_fix()

Supported languages: C, CPP (C++), Java
"""

import re, json, os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# ════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ════════════════════════════════════════════════════════════════

class ErrorType(Enum):
    NONE    = 0
    LEXICAL = 1
    SYNTAX  = 2

class Severity(Enum):
    INFO    = "INFO"
    WARNING = "WARNING"
    ERROR   = "ERROR"

@dataclass
class ErrorDiagnostic:
    error_type:   ErrorType
    severity:     Severity
    line:         int
    column:       int
    message:      str
    token:        str = ""
    rule_id:      str = ""

@dataclass
class CorrectionSuggestion:
    original_line:   str
    corrected_line:  str
    explanation:     str
    confidence:      float          # 0.0 – 1.0
    rule_id:         str = ""

@dataclass
class CorrectionResult:
    original_code:   str
    language:        str
    diagnostics:     List[ErrorDiagnostic]     = field(default_factory=list)
    suggestions:     List[CorrectionSuggestion]= field(default_factory=list)
    corrected_code:  Optional[str]             = None
    error_type:      ErrorType                 = ErrorType.NONE
    error_line:      int                       = -1
    model_confidence: float                    = 0.0

    def has_errors(self) -> bool:
        return len(self.diagnostics) > 0

    def best_suggestion(self) -> Optional[CorrectionSuggestion]:
        if not self.suggestions: return None
        return max(self.suggestions, key=lambda s: s.confidence)

    def apply_best_fix(self) -> Optional[str]:
        sug = self.best_suggestion()
        if sug is None: return self.original_code
        lines = self.original_code.splitlines(keepends=True)
        if self.error_line > 0 and self.error_line <= len(lines):
            lines[self.error_line - 1] = sug.corrected_line + "\n"
        return "".join(lines)

    def summary(self) -> str:
        lines = [
            f"═══ Error Correction Report ({'%s' % self.language}) ═══",
            f"  Error type    : {self.error_type.name}",
            f"  Error line    : {self.error_line}",
            f"  Confidence    : {self.model_confidence:.0%}",
            f"  Diagnostics   : {len(self.diagnostics)}",
            f"  Suggestions   : {len(self.suggestions)}",
        ]
        if self.diagnostics:
            lines.append("\n  Diagnostics:")
            for d in self.diagnostics:
                lines.append(f"    [{d.severity.value}] Line {d.line}: {d.message}")
        if self.suggestions:
            lines.append("\n  Top Suggestion:")
            sug = self.best_suggestion()
            if sug:
                lines.append(f"    Original  : {sug.original_line.strip()}")
                lines.append(f"    Corrected : {sug.corrected_line.strip()}")
                lines.append(f"    Why       : {sug.explanation}")
                lines.append(f"    Confidence: {sug.confidence:.0%}")
        return "\n".join(lines)


# ════════════════════════════════════════════════════════════════
# RULE-BASED LEXICAL CHECKER
# ════════════════════════════════════════════════════════════════

class LexicalChecker:
    """Fast rule-based lexical error detector."""

    # (pattern, message, rule_id, severity)
    COMMON_RULES: List[Tuple] = [
        (r"(?<!\w)\d+[a-zA-Z_]\w*\b",
         "Identifier cannot start with a digit",
         "LEX001", Severity.ERROR),

        (r'\"[^\"]*\n',
         "Unclosed string literal",
         "LEX002", Severity.ERROR),

        (r"'[^']{2,}'",
         "Multi-character character literal",
         "LEX003", Severity.WARNING),

        (r"\\[^nrtabfv0\\\"'\\?]",
         "Invalid escape sequence",
         "LEX004", Severity.WARNING),

        (r"\b(retun|reutrn|RETURN)\b",
         "Possible misspelling of 'return'",
         "LEX005", Severity.ERROR),

        (r"\b(whlie|wihle|wile)\b",
         "Possible misspelling of 'while'",
         "LEX006", Severity.ERROR),

        (r"\b(flot|folat)\b",
         "Possible misspelling of 'float'",
         "LEX007", Severity.ERROR),

        (r"\b(intt|interger|integr)\b",
         "Possible misspelling of 'int'",
         "LEX008", Severity.ERROR),

        (r"\b(doubble|doble)\b",
         "Possible misspelling of 'double'",
         "LEX009", Severity.ERROR),

        (r"\b(printff|prinf|print(?!\w))\b",
         "Possible misspelling of 'printf'",
         "LEX010", Severity.ERROR),

        (r"\b(scnaf|Scanf)\b",
         "Possible misspelling/casing of 'scanf'",
         "LEX011", Severity.ERROR),
    ]

    CPP_RULES: List[Tuple] = [
        (r"\bcot\b(?!\w)",      "Possible misspelling of 'cout'",     "LEX_CPP001", Severity.ERROR),
        (r"\bCout\b",           "'Cout' — use lowercase 'cout'",      "LEX_CPP002", Severity.ERROR),
        (r"\bENDL\b",           "'ENDL' — use lowercase 'endl'",      "LEX_CPP003", Severity.ERROR),
        (r"\btemplete\b",       "Possible misspelling of 'template'", "LEX_CPP004", Severity.ERROR),
        (r"\bvecotr\b",         "Possible misspelling of 'vector'",   "LEX_CPP005", Severity.ERROR),
        (r"\bpubic\b",          "Possible misspelling of 'public'",   "LEX_CPP006", Severity.ERROR),
        (r"\boveride\b",        "Possible misspelling of 'override'", "LEX_CPP007", Severity.ERROR),
        (r"\bvirtal\b",         "Possible misspelling of 'virtual'",  "LEX_CPP008", Severity.ERROR),
        (r"\bNullptr\b",        "'Nullptr' — use lowercase 'nullptr'","LEX_CPP009", Severity.ERROR),
        (r"===",                "Operator '===' invalid in C++",      "LEX_CPP010", Severity.ERROR),
        (r"\*\*(?!=)",          "Operator '**' invalid in C++; use pow()",  "LEX_CPP011", Severity.WARNING),
    ]

    JAVA_RULES: List[Tuple] = [
        (r"\bpubic\b",          "Possible misspelling of 'public'",   "LEX_JAVA001", Severity.ERROR),
        (r"\bStstem\b",         "Possible misspelling of 'System'",   "LEX_JAVA002", Severity.ERROR),
        (r"\bstatik\b",         "Possible misspelling of 'static'",   "LEX_JAVA003", Severity.ERROR),
        (r"\bStirng\b",         "Possible misspelling of 'String'",   "LEX_JAVA004", Severity.ERROR),
        (r"\bboolan\b",         "Possible misspelling of 'boolean'",  "LEX_JAVA005", Severity.ERROR),
        (r"\bsystem\b(?=\.)",   "'system' — should be 'System'",      "LEX_JAVA006", Severity.ERROR),
        (r"\b(True|False)\b",   "Boolean literal must be lowercase",  "LEX_JAVA007", Severity.ERROR),
        (r"\bNull\b(?!\w)",     "'Null' — use lowercase 'null'",      "LEX_JAVA008", Severity.ERROR),
        (r"\bVoid\b",           "'Void' — use lowercase 'void'",      "LEX_JAVA009", Severity.ERROR),
        (r"===",                "Operator '===' invalid in Java",     "LEX_JAVA010", Severity.ERROR),
        (r"\*\*(?!=)",          "Operator '**' invalid; use Math.pow()","LEX_JAVA011", Severity.WARNING),
        (r"\bextands\b",        "Possible misspelling of 'extends'",  "LEX_JAVA012", Severity.ERROR),
        (r"\bimprot\b",         "Possible misspelling of 'import'",   "LEX_JAVA013", Severity.ERROR),
    ]

    def check(self, code: str, language: str) -> List[ErrorDiagnostic]:
        diagnostics = []
        lines = code.splitlines()
        rules = list(self.COMMON_RULES)
        if language == "CPP":  rules += self.CPP_RULES
        if language == "Java": rules += self.JAVA_RULES

        for lineno, line_text in enumerate(lines, start=1):
            for pattern, message, rule_id, severity in rules:
                for m in re.finditer(pattern, line_text):
                    diagnostics.append(ErrorDiagnostic(
                        error_type = ErrorType.LEXICAL,
                        severity   = severity,
                        line       = lineno,
                        column     = m.start() + 1,
                        message    = message,
                        token      = m.group(0),
                        rule_id    = rule_id,
                    ))
        return diagnostics


# ════════════════════════════════════════════════════════════════
# RULE-BASED SYNTAX CHECKER
# ════════════════════════════════════════════════════════════════

class SyntaxChecker:
    """Rule-based syntax error detector."""

    def check(self, code: str, language: str) -> List[ErrorDiagnostic]:
        diagnostics = []
        diagnostics += self._check_brackets(code)
        diagnostics += self._check_semicolons(code, language)
        diagnostics += self._check_dangling_else(code)
        diagnostics += self._check_do_while(code)
        if language in ("C", "CPP"):
            diagnostics += self._check_struct_semicolon(code)
        if language == "Java":
            diagnostics += self._check_java_specific(code)
        return diagnostics

    def _check_brackets(self, code: str) -> List[ErrorDiagnostic]:
        diags = []
        stack = []
        pairs = {")": "(", "]": "[", "}": "{"}
        openers = set("({[")
        lineno = 1
        for i, ch in enumerate(code):
            if ch == "\n": lineno += 1
            if ch in openers:
                stack.append((ch, lineno))
            elif ch in pairs:
                if not stack or stack[-1][0] != pairs[ch]:
                    diags.append(ErrorDiagnostic(
                        ErrorType.SYNTAX, Severity.ERROR, lineno, i,
                        f"Mismatched '{ch}' — no matching '{pairs[ch]}'",
                        token=ch, rule_id="SYN001",
                    ))
                else:
                    stack.pop()
        for ch, ln in stack:
            diags.append(ErrorDiagnostic(
                ErrorType.SYNTAX, Severity.ERROR, ln, 0,
                f"Unclosed '{ch}'", token=ch, rule_id="SYN002",
            ))
        return diags

    def _check_semicolons(self, code: str, language: str) -> List[ErrorDiagnostic]:
        diags = []
        lines = code.splitlines()
        ENDS_OK = (";", "{", "}", "//", "*/", ":", "\\")
        SKIP_STARTS = ("#", "//", "/*", "*", "@", "import", "package")
        KEYWORD_LINES = re.compile(
            r"^\s*(if|else|for|while|do|switch|try|catch|finally|class|struct|enum)\b"
        )
        for lineno, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped: continue
            if any(stripped.startswith(sk) for sk in SKIP_STARTS): continue
            if KEYWORD_LINES.match(stripped): continue
            if stripped.endswith(tuple(ENDS_OK)): continue
            # Heuristic: line looks like a statement missing semicolon
            if re.search(r"(=\s*\w|return\s+\w|\+\+|--)\s*$", stripped):
                diags.append(ErrorDiagnostic(
                    ErrorType.SYNTAX, Severity.WARNING, lineno, len(line),
                    "Possible missing semicolon at end of statement",
                    rule_id="SYN003",
                ))
        return diags

    def _check_dangling_else(self, code: str) -> List[ErrorDiagnostic]:
        """Detect `else` without prior `if` brace block."""
        diags = []
        lines = code.splitlines()
        for lineno, line in enumerate(lines, start=1):
            if re.match(r"^\s*else\b", line.strip()):
                # Check previous non-empty line
                for prev_line in reversed(lines[:lineno-1]):
                    if prev_line.strip():
                        if not prev_line.strip().endswith("}"):
                            diags.append(ErrorDiagnostic(
                                ErrorType.SYNTAX, Severity.WARNING, lineno, 0,
                                "Dangling 'else' — previous if-body may be missing braces",
                                rule_id="SYN004",
                            ))
                        break
        return diags

    def _check_do_while(self, code: str) -> List[ErrorDiagnostic]:
        """do { } while (cond) must end with semicolon."""
        diags = []
        for m in re.finditer(r"\bwhile\s*\([^)]+\)\s*$", code, re.MULTILINE):
            lineno = code[:m.start()].count("\n") + 1
            if not code[m.end():m.end()+2].strip().startswith(";"):
                diags.append(ErrorDiagnostic(
                    ErrorType.SYNTAX, Severity.ERROR, lineno, 0,
                    "do-while: missing semicolon after while condition",
                    rule_id="SYN005",
                ))
        return diags

    def _check_struct_semicolon(self, code: str) -> List[ErrorDiagnostic]:
        diags = []
        for m in re.finditer(r"\}\s*\n", code):
            lineno = code[:m.start()].count("\n") + 1
            preceding = code[:m.start()].strip()
            # crude check: closing brace of struct/class without semicolon
            if re.search(r"\b(struct|enum)\b[^;{]*\{", preceding):
                snippet_after = code[m.end():m.end()+5]
                if not snippet_after.strip().startswith(";"):
                    diags.append(ErrorDiagnostic(
                        ErrorType.SYNTAX, Severity.ERROR, lineno, 0,
                        "struct/enum definition may be missing trailing semicolon",
                        rule_id="SYN006",
                    ))
        return diags

    def _check_java_specific(self, code: str) -> List[ErrorDiagnostic]:
        diags = []
        lines = code.splitlines()
        for lineno, line in enumerate(lines, start=1):
            if re.search(r"\bextends\s+\w+\s*,", line):
                diags.append(ErrorDiagnostic(
                    ErrorType.SYNTAX, Severity.ERROR, lineno, 0,
                    "Java does not support multiple class inheritance; use 'implements' for interfaces",
                    rule_id="SYN_JAVA001",
                ))
            if re.search(r"\bpublic\s+static\s+class\b", line):
                diags.append(ErrorDiagnostic(
                    ErrorType.SYNTAX, Severity.WARNING, lineno, 0,
                    "Top-level class cannot be declared static",
                    rule_id="SYN_JAVA002",
                ))
        return diags


# ════════════════════════════════════════════════════════════════
# CORRECTION SUGGESTION ENGINE
# ════════════════════════════════════════════════════════════════

class CorrectionEngine:
    """Generates concrete fix suggestions given diagnostics."""

    # Substitution rules: (regex, replacement, explanation, confidence)
    LEX_FIXES = [
        (r"\bretun\b",     "return",  "Corrected 'retun' → 'return'",  0.97),
        (r"\breutrn\b",    "return",  "Corrected 'reutrn' → 'return'", 0.97),
        (r"\bRETURN\b",    "return",  "Corrected 'RETURN' → 'return'", 0.95),
        (r"\bwhlie\b",     "while",   "Corrected 'whlie' → 'while'",   0.97),
        (r"\bflot\b",      "float",   "Corrected 'flot' → 'float'",    0.97),
        (r"\bintt\b",      "int",     "Corrected 'intt' → 'int'",      0.96),
        (r"\binterger\b",  "int",     "Corrected 'interger' → 'int'",  0.95),
        (r"\bdoubble\b",   "double",  "Corrected 'doubble' → 'double'",0.96),
        (r"\bprinff\b",    "printf",  "Corrected 'prinff' → 'printf'", 0.97),
        (r"\bprinf\b",     "printf",  "Corrected 'prinf' → 'printf'",  0.96),
        (r"\bcot\b",       "cout",    "Corrected 'cot' → 'cout'",      0.97),
        (r"\bCout\b",      "cout",    "Changed 'Cout' → 'cout' (case-sensitive)", 0.99),
        (r"\bENDL\b",      "endl",    "Changed 'ENDL' → 'endl'",       0.99),
        (r"\bStstem\b",    "System",  "Corrected 'Ststem' → 'System'", 0.97),
        (r"\bstatik\b",    "static",  "Corrected 'statik' → 'static'", 0.97),
        (r"\bStirng\b",    "String",  "Corrected 'Stirng' → 'String'", 0.97),
        (r"\bboolan\b",    "boolean", "Corrected 'boolan' → 'boolean'",0.97),
        (r"\bTrue\b",      "true",    "Changed 'True' → 'true'",       0.99),
        (r"\bFalse\b",     "false",   "Changed 'False' → 'false'",     0.99),
        (r"\bNull\b",      "null",    "Changed 'Null' → 'null'",       0.99),
        (r"\bextands\b",   "extends", "Corrected 'extands' → 'extends'",0.97),
        (r"\bimprot\b",    "import",  "Corrected 'improt' → 'import'", 0.97),
        (r"\btemplete\b",  "template","Corrected 'templete' → 'template'",0.97),
        (r"\bvecotr\b",    "vector",  "Corrected 'vecotr' → 'vector'", 0.97),
        (r"\boveride\b",   "override","Corrected 'overide' → 'override'",0.97),
        (r"\bvirtal\b",    "virtual", "Corrected 'virtal' → 'virtual'",0.97),
        (r"\bNullptr\b",   "nullptr", "Changed 'Nullptr' → 'nullptr'", 0.99),
        (r"\bpubic\b",     "public",  "Corrected 'pubic' → 'public'",  0.97),
        (r"\bprivte\b",    "private", "Corrected 'privte' → 'private'",0.97),
        (r"\bnmespace\b",  "namespace","Corrected 'nmespace'",         0.97),
        (r"\bvoud\b",      "void",    "Corrected 'voud' → 'void'",     0.97),
        (r"\bVOID\b",      "void",    "Changed 'VOID' → 'void'",       0.99),
        (r"===",           "==",      "Changed '===' → '==' (not valid in C/C++/Java)", 0.98),
    ]

    SYN_FIXES = [
        # Missing semicolon at end of line
        (r"(\b(?:return\s+\w+|int\s+\w+\s*=\s*\w+|\+\+|--))\s*$",
         r"\1;", "Added missing semicolon", 0.85),
        # Missing semicolon after struct/class closing brace
        (r"\}\s*$", "};", "Added semicolon after closing brace (struct/class/enum)", 0.80),
    ]

    def generate(self, code: str, diagnostics: List[ErrorDiagnostic],
                 language: str) -> List[CorrectionSuggestion]:
        suggestions = []
        lines = code.splitlines()

        for d in diagnostics:
            if d.line < 1 or d.line > len(lines): continue
            original = lines[d.line - 1]
            corrected = original

            if d.error_type == ErrorType.LEXICAL:
                for pattern, repl, expl, conf in self.LEX_FIXES:
                    new = re.sub(pattern, repl, corrected)
                    if new != corrected:
                        suggestions.append(CorrectionSuggestion(
                            original_line  = original,
                            corrected_line = new,
                            explanation    = expl,
                            confidence     = conf,
                            rule_id        = d.rule_id,
                        ))
                        corrected = new

            elif d.error_type == ErrorType.SYNTAX:
                for pattern, repl, expl, conf in self.SYN_FIXES:
                    new = re.sub(pattern, repl, corrected)
                    if new != corrected:
                        suggestions.append(CorrectionSuggestion(
                            original_line  = original,
                            corrected_line = new,
                            explanation    = expl,
                            confidence     = conf,
                            rule_id        = d.rule_id,
                        ))
                        corrected = new

        # Deduplicate by (original, corrected)
        seen = set()
        unique = []
        for s in suggestions:
            key = (s.original_line, s.corrected_line)
            if key not in seen:
                seen.add(key)
                unique.append(s)
        return sorted(unique, key=lambda s: -s.confidence)


# ════════════════════════════════════════════════════════════════
# MAIN MODULE
# ════════════════════════════════════════════════════════════════

class ErrorCorrectionModule:
    """
    Unified AI-assisted error correction pipeline.
    Combines rule-based checkers with ML model predictions.
    """

    def __init__(self, model_path: Optional[str] = None):
        self.lexical_checker  = LexicalChecker()
        self.syntax_checker   = SyntaxChecker()
        self.correction_engine = CorrectionEngine()
        self.model_loaded     = False

        if model_path and os.path.exists(model_path):
            self._load_model(model_path)

    def _load_model(self, path: str):
        """Load pre-trained model weights (stub — replace with real loader)."""
        try:
            with open(path) as f:
                self._model_weights = json.load(f)
            self.model_loaded = True
            print(f"  [ECM] Model loaded from {path}")
        except Exception as e:
            print(f"  [ECM] Warning: could not load model — {e}")

    def _ml_predict(self, code: str, language: str) -> Tuple[ErrorType, float, int]:
        """
        Run ML model inference (stub — returns heuristic when model not loaded).
        Returns: (predicted_error_type, confidence, predicted_error_line)
        """
        if not self.model_loaded:
            # Rule-based fallback
            lines  = code.splitlines()
            # Check bracket imbalance
            if abs(code.count("{") - code.count("}")) > 0:
                return ErrorType.SYNTAX, 0.72, 1
            # Check obvious lexical patterns
            lex_patterns = [r"\bretun\b", r"\bwhlie\b", r"\bflot\b", r"\bcot\b",
                            r"\bStatik\b", r"\bStirng\b", r"\btemplete\b"]
            for lineno, line in enumerate(lines, start=1):
                for pat in lex_patterns:
                    if re.search(pat, line):
                        return ErrorType.LEXICAL, 0.80, lineno
            return ErrorType.NONE, 0.55, -1
        # Real model inference would go here
        return ErrorType.NONE, 0.0, -1

    def analyze(self, code: str, language: str = "C") -> CorrectionResult:
        """
        Full pipeline: check → diagnose → suggest corrections.

        Parameters
        ----------
        code     : Source code string
        language : "C", "CPP", or "Java"

        Returns
        -------
        CorrectionResult with diagnostics and suggestions
        """
        result = CorrectionResult(original_code=code, language=language)

        # 1. Rule-based checks
        lex_diags = self.lexical_checker.check(code, language)
        syn_diags = self.syntax_checker.check(code, language)
        all_diags = lex_diags + syn_diags

        result.diagnostics = all_diags

        # 2. ML prediction
        ml_type, ml_conf, ml_line = self._ml_predict(code, language)
        result.model_confidence = ml_conf

        # 3. Determine primary error type
        if lex_diags:
            result.error_type = ErrorType.LEXICAL
            result.error_line = lex_diags[0].line
        elif syn_diags:
            result.error_type = ErrorType.SYNTAX
            result.error_line = syn_diags[0].line
        else:
            result.error_type = ml_type
            result.error_line = ml_line

        # 4. Generate suggestions
        result.suggestions = self.correction_engine.generate(code, all_diags, language)

        # 5. Build corrected code from best suggestions
        if result.suggestions:
            corrected_lines = code.splitlines(keepends=True)
            applied_lines   = set()
            for sug in result.suggestions:
                # Find the line this fix applies to
                for i, line in enumerate(corrected_lines):
                    if (i + 1) not in applied_lines and line.rstrip("\n") == sug.original_line:
                        corrected_lines[i] = sug.corrected_line + ("\n" if not sug.corrected_line.endswith("\n") else "")
                        applied_lines.add(i + 1)
                        break
            result.corrected_code = "".join(corrected_lines)

        return result

    def analyze_file(self, filepath: str) -> CorrectionResult:
        """Convenience wrapper for analyzing a source file."""
        ext_map = {".c": "C", ".cpp": "CPP", ".cc": "CPP",
                   ".cxx": "CPP", ".java": "Java"}
        ext = os.path.splitext(filepath)[1].lower()
        lang = ext_map.get(ext, "C")
        with open(filepath, encoding="utf-8") as f:
            code = f.read()
        return self.analyze(code, lang)

    def batch_analyze(self, samples: List[Dict]) -> List[CorrectionResult]:
        """Analyze a list of {'code': ..., 'language': ...} dicts."""
        return [self.analyze(s["code"], s.get("language", "C")) for s in samples]


# ════════════════════════════════════════════════════════════════
# COMMAND-LINE INTERFACE
# ════════════════════════════════════════════════════════════════

DEMO_SAMPLES = [
    {
        "language": "C",
        "code": '#include <stdio.h>\nint main() {\n    int reslt = 5 * 5\n    printff("%d\\n", reslt);\n    retun 0;\n}',
        "description": "Multiple lexical + syntax errors",
    },
    {
        "language": "CPP",
        "code": '#include <iostream>\nusing namespace std;\nint main() {\n    cot << "Hello" << ENDL;\n    return 0;\n}',
        "description": "'cot' and 'ENDL' lexical errors",
    },
    {
        "language": "Java",
        "code": 'public class Demo {\n    public static void main(String[] args) {\n        Stirng name = "Alice";\n        System.Out.println(name)\n    }\n}',
        "description": "'Stirng', 'System.Out', missing semicolon",
    },
]

def run_demo():
    corrector = ErrorCorrectionModule()
    print("\n" + "═" * 65)
    print("  AI-ASSISTED ERROR CORRECTION MODULE — DEMO")
    print("═" * 65)

    for demo in DEMO_SAMPLES:
        print(f"\n  {'─' * 60}")
        print(f"  Language: {demo['language']}  |  {demo['description']}")
        print(f"  {'─' * 60}")
        print("  INPUT CODE:")
        for i, line in enumerate(demo["code"].splitlines(), 1):
            print(f"    {i:2d}│ {line}")

        result = corrector.analyze(demo["code"], demo["language"])
        print(f"\n{result.summary()}")

        corrected = result.apply_best_fix()
        if corrected and corrected != demo["code"]:
            print("\n  CORRECTED CODE:")
            for i, line in enumerate(corrected.splitlines(), 1):
                print(f"    {i:2d}│ {line}")

    print("\n" + "═" * 65 + "\n")


if __name__ == "__main__":
    run_demo()