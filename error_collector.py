# ============================================================
# ERROR COLLECTOR
# Hooks into ANTLR4's error listeners to capture lexical
# and syntax errors with full context for ML training/prediction.
# Supports: C, C++, Java
# ============================================================

import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener


# ─────────────────────────────────────────────────────────────
# Data class for a single captured error
# ─────────────────────────────────────────────────────────────
class ErrorRecord:
    """Represents one lexical or syntax error found in source code."""

    def __init__(self, error_type, line, column, message,
                 offending_symbol=None, source_line=""):
        self.error_type     = error_type        # "LEXICAL" | "SYNTAX"
        self.line           = line              # 1-based line number
        self.column         = column            # 0-based column
        self.message        = message          # raw ANTLR message
        self.offending_symbol = offending_symbol  # token text or None
        self.source_line    = source_line       # full source line text
        self.language       = None              # set by collector
        self.file_path      = None              # set by collector

    # Derived features used by ML pipeline
    @property
    def error_category(self):
        msg = self.message.lower()
        if "missing" in msg:
            return "MISSING_TOKEN"
        if "extraneous" in msg:
            return "EXTRANEOUS_TOKEN"
        if "mismatched" in msg:
            return "MISMATCHED_TOKEN"
        if "no viable" in msg:
            return "NO_VIABLE_ALT"
        if "token recognition" in msg:
            return "UNRECOGNIZED_TOKEN"
        return "OTHER"

    def to_dict(self):
        return {
            "language":         self.language,
            "file_path":        self.file_path,
            "error_type":       self.error_type,
            "error_category":   self.error_category,
            "line":             self.line,
            "column":           self.column,
            "message":          self.message,
            "offending_symbol": self.offending_symbol,
            "source_line":      self.source_line,
        }

    def __repr__(self):
        sym = f" [{self.offending_symbol}]" if self.offending_symbol else ""
        return (f"[{self.error_type}] Line {self.line}:{self.column}{sym}"
                f" — {self.error_category} — {self.message[:80]}")


# ─────────────────────────────────────────────────────────────
# Custom ANTLR Error Listener
# ─────────────────────────────────────────────────────────────
class CollectingErrorListener(ErrorListener):
    """
    Replaces ANTLR's default console error listener.
    Stores all errors in self.errors for later use.
    """

    def __init__(self, source_lines=None, error_type="SYNTAX"):
        super().__init__()
        self.errors       = []
        self.source_lines = source_lines or []
        self.error_type   = error_type  # "LEXICAL" or "SYNTAX"

    def syntaxError(self, recognizer, offendingSymbol, line, column,
                    msg, e):
        source_line = ""
        if self.source_lines and 0 < line <= len(self.source_lines):
            source_line = self.source_lines[line - 1]

        sym_text = None
        if offendingSymbol is not None:
            try:
                sym_text = offendingSymbol.text
            except Exception:
                pass

        record = ErrorRecord(
            error_type       = self.error_type,
            line             = line,
            column           = column,
            message          = msg,
            offending_symbol = sym_text,
            source_line      = source_line.rstrip("\n"),
        )
        self.errors.append(record)


# ─────────────────────────────────────────────────────────────
# Main collector
# ─────────────────────────────────────────────────────────────
class ErrorCollector:
    """
    Runs lexer + parser on a source file, suppresses default
    ANTLR console output, and returns a list of ErrorRecord objects.

    Usage:
        collector = ErrorCollector()
        errors = collector.collect("C", "hello.c")
        for e in errors:
            print(e)
    """

    def collect(self, language: str, file_path: str) -> list:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
        except FileNotFoundError:
            print(f"[ErrorCollector] File not found: {file_path}")
            return []

        source_lines = source.splitlines()

        # ── choose lexer/parser ──────────────────────────────
        if language == "C":
            try:
                from CLexer  import CLexer
                from CParser import CParser
            except ImportError:
                print("[ErrorCollector] C lexer/parser not found. Generate with ANTLR.")
                return []
            lexer_class  = CLexer
            parser_class = CParser

        elif language in ("CPP", "C++"):
            try:
                from CPPLexer  import CPPLexer
                from CPPParser import CPPParser
            except ImportError:
                print("[ErrorCollector] CPP lexer/parser not found.")
                return []
            lexer_class  = CPPLexer
            parser_class = CPPParser

        elif language == "Java":
            try:
                from JavaLexer  import JavaLexer
                from JavaParser import JavaParser
            except ImportError:
                print("[ErrorCollector] Java lexer/parser not found.")
                return []
            lexer_class  = JavaLexer
            parser_class = JavaParser

        else:
            print(f"[ErrorCollector] Unsupported language: {language}")
            return []

        # ── lexer pass ───────────────────────────────────────
        lex_listener = CollectingErrorListener(source_lines, "LEXICAL")
        stream       = InputStream(source)
        lexer        = lexer_class(stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(lex_listener)
        token_stream = CommonTokenStream(lexer)
        token_stream.fill()

        # ── parser pass ─────────────────────────────────────
        syn_listener = CollectingErrorListener(source_lines, "SYNTAX")
        token_stream.reset()
        parser = parser_class(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(syn_listener)
        parser.program()

        # ── combine & tag ───────────────────────────────────
        all_errors = lex_listener.errors + syn_listener.errors
        for e in all_errors:
            e.language  = language
            e.file_path = file_path

# ── deduplicate same line+col errors ────────────────────
# ANTLR often reports the same error from both lexer and
# parser passes. Keep only the most specific one per location.
        seen     = {}
        unique   = []
        for e in all_errors:
            key = (e.line, e.column)
            if key not in seen:
                seen[key] = e
                unique.append(e)
            else:
        # Keep SYNTAX over LEXICAL, and longer messages
                existing = seen[key]
                if (e.error_type == "SYNTAX" and existing.error_type == "LEXICAL") \
                   or len(e.message) > len(existing.message):
                    seen[key]         = e
                    unique[unique.index(existing)] = e

        return unique

    def collect_and_print(self, language: str, file_path: str):
        errors = self.collect(language, file_path)

        print("\n" + "=" * 60)
        print(f"  ERROR COLLECTION  [{language}]  —  {file_path}")
        print("=" * 60)

        if not errors:
            print("  ✓  No errors found.")
        else:
            for e in errors:
                print(f"\n  {e}")
                if e.source_line:
                    print(f"  >>> {e.source_line}")
                    print(f"  {'':>4}{'^':>{e.column + 1}}")

        print(f"\n  Total errors: {len(errors)}")
        print("=" * 60)
        return errors


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python error_collector.py <C|CPP|Java> <file>")
        sys.exit(1)
    ErrorCollector().collect_and_print(sys.argv[1], sys.argv[2])