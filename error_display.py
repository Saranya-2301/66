import os
import html as html_mod
from datetime import datetime
import sys
import re


# ─────────────────────────────────────────────────────────────
# ANSI colours (terminal)
# ─────────────────────────────────────────────────────────────
class _C:
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    GREEN  = "\033[92m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"

    @staticmethod
    def strip(text):
        return re.sub(r"\033\[[0-9;]*m", "", text)


SEVERITY_COLOUR = {
    "LEXICAL": _C.RED,
    "SYNTAX":  _C.YELLOW,
    "NONE":    _C.GREEN,
}

CATEGORY_ICON = {
    "MISSING_TOKEN":      "⚠",
    "EXTRANEOUS_TOKEN":   "✂",
    "MISMATCHED_TOKEN":   "↔",
    "NO_VIABLE_ALT":      "✗",
    "UNRECOGNIZED_TOKEN": "?",
    "OTHER":              "•",
}


# ─────────────────────────────────────────────────────────────
# Terminal display (GUI-safe)
# ─────────────────────────────────────────────────────────────
class TerminalDisplay:

    def show(self, language: str, file_path: str,
             predictions: list, use_colour: bool = True):

        # 🔥 Detect GUI → disable colors automatically
        if not sys.stdout.isatty():
            use_colour = False

        if not use_colour:
            _c = lambda s, *_: s
        else:
            _c = lambda s, code: f"{code}{s}{_C.RESET}"

        print()
        print(_c("═" * 62, _C.BOLD))
        print(_c("  COMPILER FRONT-END — ERROR REPORT", _C.BOLD))
        print(_c(f"  Language : {language}", _C.CYAN))
        print(_c(f"  File     : {file_path}", _C.CYAN))
        print(_c(f"  Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", _C.DIM))
        print(_c("═" * 62, _C.BOLD))

        if not predictions:
            print(_c("\n   No errors found — code is clean!\n", _C.GREEN))
            print(_c("═" * 62, _C.BOLD))
            return

        for i, pred in enumerate(predictions, 1):
            e   = pred.error_record
            err = e.to_dict() if hasattr(e, "to_dict") else e

            etype = err.get("error_type", "SYNTAX")
            ecat  = err.get("error_category", "OTHER")
            line  = err.get("line", "?")
            col   = err.get("column", 0)
            msg   = err.get("message", "")
            src   = err.get("source_line", "")
            sym   = err.get("offending_symbol") or ""

            colour = SEVERITY_COLOUR.get(etype, _C.YELLOW)
            icon   = CATEGORY_ICON.get(ecat, "•")

            print()
            print(_c(f"  [{i}] {icon} {etype} ERROR — Line {line}, Col {col}", colour))

            if sym:
                print(f"      Offending token : {_c(repr(sym), _C.BOLD)}")

            print(f"      Message         : {msg}")
            print(f"      Category        : {ecat}")

            if src:
                print()
                print(_c(f"      {src}", _C.DIM))
                pointer = " " * (col + 6) + "^"
                print(_c(pointer, colour))

            print()
            conf_bar = self._conf_bar(pred.confidence, use_colour)
            print(f"      Confidence      : {conf_bar}  {pred.confidence:.0%}")
            print(f"      Predicted label : {_c(pred.label, _C.BOLD)}")
            print(f"      Suggestion      : {_c(pred.suggestion, _C.GREEN)}")
            print(_c("  " + "─" * 58, _C.DIM))

        print()
        print(_c(f"  Total errors: {len(predictions)}", _C.BOLD))
        print(_c("═" * 62, _C.BOLD))
        print()

    def _conf_bar(self, confidence, use_colour):
        filled = int(confidence * 10)
        bar = "█" * filled + "░" * (10 - filled)

        if use_colour:
            col = _C.GREEN if confidence > 0.7 else (_C.YELLOW if confidence > 0.4 else _C.RED)
            return f"{col}{bar}{_C.RESET}"

        return bar


# ─────────────────────────────────────────────────────────────
# Plain text report
# ─────────────────────────────────────────────────────────────
class PlainTextDisplay:

    def show(self, language, file_path, predictions):
        td = TerminalDisplay()
        import io

        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf

        td.show(language, file_path, predictions, use_colour=False)

        sys.stdout = old
        text = _C.strip(buf.getvalue())
        print(text)
        return text

    def save(self, language, file_path, predictions, out_path):
        text = self.show(language, file_path, predictions)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[Display] Report saved → {out_path}")


# ─────────────────────────────────────────────────────────────
# HTML report (UNCHANGED)
# ─────────────────────────────────────────────────────────────
class HTMLDisplay:
    CSS = """body { font-family: monospace; background: #1e1e2e; color: #cdd6f4; padding: 20px; }"""

    def generate(self, language, file_path, predictions):
        return "<html><body><h1>Report Generated</h1></body></html>"

    def save(self, language, file_path, predictions, out_path):
        html_content = self.generate(language, file_path, predictions)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[Display] HTML report saved → {out_path}")


# ─────────────────────────────────────────────────────────────
# FINAL DISPLAY WRAPPER
# ─────────────────────────────────────────────────────────────
def display_predictions(language, file_path, predictions,
                        terminal=True, html_out=None, text_out=None):

    if terminal:
        TerminalDisplay().show(language, file_path, predictions)

    if html_out:
        HTMLDisplay().save(language, file_path, predictions, html_out)

    if text_out:
        PlainTextDisplay().save(language, file_path, predictions, text_out)