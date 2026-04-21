# ============================================================
# auto_corrector.py
# WEEK 9 — AUTOMATIC ERROR CORRECTION
# ============================================================

import os
import re
import sys
import tempfile
from datetime import datetime

LANG_MAP = {
    "c"   : "C",    "C"   : "C",
    "cpp" : "CPP",  "CPP" : "CPP",
    "c++" : "CPP",  "C++" : "CPP",
    "java": "Java", "Java": "Java", "JAVA": "Java",
}
FILE_EXT = {"C": ".c", "CPP": ".cpp", "Java": ".java"}


# ─────────────────────────────────────────────────────────────
# AUTO-FIXER
# ─────────────────────────────────────────────────────────────
class AutoFixer:

    def fix(self, source: str, label: str, error_line: int,
            offending_symbol: str = "", message: str = "") -> tuple:
        """Returns (new_source, description, changed: bool)"""

        lines = source.splitlines(keepends=True)
        idx   = error_line - 1
        if idx < 0 or idx >= len(lines):
            return source, "Line out of range", False

        # ── ADD_SEMICOLON ─────────────────────────────────
        if label == "ADD_SEMICOLON":
            target_idx = max(0, idx - 1)
            target     = lines[target_idx].rstrip("\n\r")
            stripped   = target.rstrip()
            if (stripped
                    and not stripped.endswith(";")
                    and not stripped.endswith("{")
                    and not stripped.endswith("}")
                    and not stripped.endswith(",")
                    and not stripped.startswith("//")
                    and not stripped.startswith("#")):
                lines[target_idx] = stripped + ";\n"
                return "".join(lines), f"Added ';' at end of line {target_idx + 1}", True
            # Try current line
            stripped = lines[idx].rstrip("\n\r").rstrip()
            if (stripped
                    and not stripped.endswith(";")
                    and not stripped.endswith("{")
                    and not stripped.endswith("}")):
                lines[idx] = stripped + ";\n"
                return "".join(lines), f"Added ';' at end of line {error_line}", True
            return source, "Semicolon already present", False

        # ── REMOVE_EXTRA_SEMICOLON ────────────────────────
        elif label == "REMOVE_EXTRA_SEMICOLON":
            for i in [idx, max(0, idx - 1)]:
                if ";;" in lines[i]:
                    lines[i] = lines[i].replace(";;", ";", 1)
                    return "".join(lines), f"Removed ';;' on line {i + 1}", True
            return source, "No ;; found", False

        # ── ADD_CLOSING_BRACE ─────────────────────────────
        elif label == "ADD_CLOSING_BRACE":
            insert_at = len(lines)
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip():
                    insert_at = i + 1
                    break
            indent = self._indent(lines[insert_at - 1]) if insert_at > 0 else ""
            lines.insert(insert_at, indent + "}\n")
            return "".join(lines), f"Added '}}' at line {insert_at + 1}", True

        # ── ADD_OPENING_BRACE ─────────────────────────────
        elif label == "ADD_OPENING_BRACE":
            stripped   = lines[idx].rstrip("\n\r").rstrip()
            lines[idx] = stripped + " {\n"
            return "".join(lines), f"Added '{{' at line {error_line}", True

        # ── ADD_CLOSING_PAREN ─────────────────────────────
        elif label == "ADD_CLOSING_PAREN":
            stripped   = lines[idx].rstrip("\n\r").rstrip()
            lines[idx] = stripped + ")\n"
            return "".join(lines), f"Added ')' at line {error_line}", True

        # ── FIX_OPERATOR_SHIFT ───────────────────────────
        elif label == "FIX_OPERATOR_SHIFT":
            for i in range(len(lines)):
                line     = lines[i]
                stripped = line.strip()
                # Never touch preprocessor lines
                if stripped.startswith("#"):
                    continue
                # Only fix lines that have cout or cin
                if "cout" not in line and "cin" not in line:
                    continue
                # Replace single < that is NOT already << and NOT <=
                fixed = re.sub(r'(?<![<>=!])(<)(?![<=])', '<<', line)
                if fixed != line:
                    lines[i] = fixed
                    return "".join(lines), f"Fixed '<' → '<<' on line {i + 1}", True
            return source, "Operator not found", False

        # ── FIX_TYPO_RETURN ───────────────────────────────
        elif label == "FIX_TYPO_RETURN":
            for typo in ["retun", "retrun", "retur", "reutrn", "retrn"]:
                for i in range(len(lines)):
                    if typo in lines[i]:
                        lines[i] = lines[i].replace(typo, "return", 1)
                        return "".join(lines), f"Fixed '{typo}' → 'return' on line {i + 1}", True
            return source, "Typo not found", False

        # ── FIX_TYPO_VOID ─────────────────────────────────
        elif label == "FIX_TYPO_VOID":
            for typo in ["viod", "vodi", "voide", "ovid", "ovdi"]:
                for i in range(len(lines)):
                    if typo in lines[i]:
                        lines[i] = lines[i].replace(typo, "void", 1)
                        return "".join(lines), f"Fixed '{typo}' → 'void' on line {i + 1}", True
            return source, "Typo not found", False

        # ── FIX_TYPO_INT ──────────────────────────────────
        elif label == "FIX_TYPO_INT":
            for typo in [" nt ", " itn ", " intt ", "nit", "innt"]:
                for i in range(len(lines)):
                    if typo in lines[i]:
                        lines[i] = lines[i].replace(typo, " int ", 1)
                        return "".join(lines), f"Fixed '{typo.strip()}' → 'int' on line {i + 1}", True
            return source, "Typo not found", False

        # ── FIX_TYPO_CLASS ────────────────────────────────
        elif label == "FIX_TYPO_CLASS":
            for typo in ["clas ", "calss ", "claas ", "lcas "]:
                for i in range(len(lines)):
                    if typo in lines[i]:
                        lines[i] = lines[i].replace(typo, "class ", 1)
                        return "".join(lines), f"Fixed '{typo.strip()}' → 'class' on line {i + 1}", True
            return source, "Typo not found", False

        # ── FIX_TYPO_PUBLIC ───────────────────────────────
        elif label == "FIX_TYPO_PUBLIC":
            for typo in ["pubic", "publci", "pubilc", "upblic", "pbulic"]:
                for i in range(len(lines)):
                    if typo in lines[i]:
                        lines[i] = lines[i].replace(typo, "public", 1)
                        return "".join(lines), f"Fixed '{typo}' → 'public' on line {i + 1}", True
            return source, "Typo not found", False

        # ── FIX_TYPO_STATIC ───────────────────────────────
        elif label == "FIX_TYPO_STATIC":
            for typo in ["statc", "statci", "sttaic", "tsatic", "sttic", "satic"]:
                for i in range(len(lines)):
                    if typo in lines[i]:
                        lines[i] = lines[i].replace(typo, "static", 1)
                        return "".join(lines), f"Fixed '{typo}' → 'static' on line {i + 1}", True
            return source, "Typo not found", False

        # ── FIX_TYPO_INCLUDE ──────────────────────────────
        elif label == "FIX_TYPO_INCLUDE":
            for typo in ["includ", "incldue", "inculde", "nclude", "inclue", "niclude"]:
                for i in range(len(lines)):
                    if typo in lines[i]:
                        lines[i] = lines[i].replace(typo, "include", 1)
                        return "".join(lines), f"Fixed '{typo}' → 'include' on line {i + 1}", True
            return source, "Typo not found", False

        # ── FIX_TYPO_ENDL ─────────────────────────────────
        elif label == "FIX_TYPO_ENDL":
            for typo in ["enl", "nedl", "ednl", "edn"]:
                for i in range(len(lines)):
                    if typo in lines[i] and "endl" not in lines[i]:
                        lines[i] = lines[i].replace(typo, "endl", 1)
                        return "".join(lines), f"Fixed '{typo}' → 'endl' on line {i + 1}", True
            return source, "Typo not found", False

        # ── FIX_TYPO_PRINTF ───────────────────────────────
        elif label == "FIX_TYPO_PRINTF":
            for typo in ["pirntf", "pirnt", "iprntf", "prinft"]:
                for i in range(len(lines)):
                    if typo in lines[i]:
                        lines[i] = lines[i].replace(typo, "printf", 1)
                        return "".join(lines), f"Fixed '{typo}' → 'printf' on line {i + 1}", True
            return source, "Typo not found", False

        # ── UNRECOGNIZED_TOKEN ─────────────────────────────
        elif label == "UNRECOGNIZED_TOKEN":
            sym = offending_symbol.strip("'\"")
            if sym and sym != "<EOF>":
                for i in range(len(lines)):
                    if sym in lines[i]:
                        lines[i] = lines[i].replace(sym, "", 1)
                        return "".join(lines), f"Removed token '{sym}' on line {i + 1}", True
            return source, "Could not remove token", False

        return source, f"No fixer for label: {label}", False

    def _indent(self, line: str) -> str:
        s = line.lstrip("\n\r")
        return s[: len(s) - len(s.lstrip())]


# ─────────────────────────────────────────────────────────────
# AUTO CORRECTOR
# ─────────────────────────────────────────────────────────────
class AutoCorrector:

    def __init__(self, model_path: str = "error_model.pkl",
                 out_dir: str = "auto_corrected"):
        from ErrorPredictor import ErrorPredictor
        self.predictor = ErrorPredictor()
        if os.path.exists(model_path):
            self.predictor.load(model_path)
        else:
            print(f"[AutoCorrector] No model at '{model_path}' — using rule-based predictor.")
        self.fixer   = AutoFixer()
        self.out_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)

    # ── single file ─────────────────────────────────────────

    def run(self, language: str, file_path: str,
            max_iter: int = 5, silent: bool = False) -> dict:

        language = LANG_MAP.get(language, language)

        if not os.path.isfile(file_path):
            print(f"[AutoCorrector] File not found: {file_path}")
            return {}

        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()

        source       = original
        all_fixes    = []
        errors_start = self._collect(language, source)

        if not silent:
            self._print_header(language, file_path, errors_start)

        if not errors_start:
            if not silent:
                print("  Already clean — no corrections needed.")
            out_path = self._save(file_path, source)
            if not silent:
                print(f"  Saved to  : {out_path}")
                print("─" * 62)
            return {
                "language": language, "file": file_path, "out_file": out_path,
                "errors_before": 0, "errors_after": 0, "fixes_applied": 0,
                "success": True, "fixes": [], "original": original, "corrected": source,
            }

        for iteration in range(max_iter):
            errors = self._collect(language, source)
            if not errors:
                break

            preds    = self.predictor.predict_batch(errors)
            made_fix = False

            for pred in preds:
                e      = pred.error_record
                d      = e.to_dict() if hasattr(e, "to_dict") else e
                label  = pred.label
                e_line = int(d.get("line", 1))
                sym    = str(d.get("offending_symbol") or "")
                msg    = str(d.get("message", ""))

                if label in ("NO_ERROR", "OTHER"):
                    continue

                new_source, desc, changed = self.fixer.fix(
                    source, label, e_line, sym, msg
                )

                if changed:
                    all_fixes.append({
                        "iteration"  : iteration + 1,
                        "line"       : e_line,
                        "label"      : label,
                        "description": desc,
                        "confidence" : round(pred.confidence, 2),
                    })
                    source   = new_source
                    made_fix = True
                    break

            if not made_fix:
                break

        errors_end = self._collect(language, source)
        out_path   = self._save(file_path, source)

        result = {
            "language"      : language,
            "file"          : file_path,
            "out_file"      : out_path,
            "errors_before" : len(errors_start),
            "errors_after"  : len(errors_end),
            "fixes_applied" : len(all_fixes),
            "success"       : len(errors_end) == 0,
            "fixes"         : all_fixes,
            "original"      : original,
            "corrected"     : source,
        }

        if not silent:
            self._print_result(result, errors_end)

        return result

    # ── directory ───────────────────────────────────────────

    def run_directory(self, language: str, directory: str) -> list:
        language = LANG_MAP.get(language, language)
        ext      = FILE_EXT.get(language, ".txt")

        if not os.path.isdir(directory):
            print(f"[AutoCorrector] Directory not found: {directory}")
            return []

        files   = sorted(f for f in os.listdir(directory) if f.endswith(ext))
        results = []

        print(f"\n{'=' * 62}")
        print(f"  AUTO-CORRECTING {len(files)} {language} files in {directory}")
        print(f"{'=' * 62}")

        for fname in files:
            result = self.run(language, os.path.join(directory, fname))
            results.append(result)

        self._print_batch_summary(results)
        return results

    # ── all samples ─────────────────────────────────────────

    def run_all(self,
                c_dir    = "samples/c",
                cpp_dir  = "samples/cpp",
                java_dir = "samples/java"):
        all_results = []
        if os.path.isdir(c_dir):
            all_results += self.run_directory("C",    c_dir)
        if os.path.isdir(cpp_dir):
            all_results += self.run_directory("CPP",  cpp_dir)
        if os.path.isdir(java_dir):
            all_results += self.run_directory("Java", java_dir)
        return all_results

    # ── internals ───────────────────────────────────────────

    def _collect(self, language: str, source: str) -> list:
        from error_collector import ErrorCollector
        suffix = FILE_EXT.get(language, ".txt")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        ) as f:
            f.write(source)
            tmp = f.name
        try:
            return ErrorCollector().collect(language, tmp)
        finally:
            os.unlink(tmp)

    def _save(self, original_path: str, corrected_source: str) -> str:
        base     = os.path.basename(original_path)
        name, ext = os.path.splitext(base)
        out_path = os.path.join(self.out_dir, f"{name}_corrected{ext}")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(corrected_source)
        return out_path

    def _print_header(self, language, file_path, errors):
        print()
        print("╔" + "═" * 60 + "╗")
        print(f"║  AUTO-CORRECTOR  [{language}]  {os.path.basename(file_path):<34}║")
        print("╚" + "═" * 60 + "╝")
        print(f"  Errors detected : {len(errors)}")
        for e in errors:
            d = e.to_dict() if hasattr(e, "to_dict") else e
            print(f"    Line {d.get('line','?'):>3} | "
                  f"{d.get('error_type','?'):7} | "
                  f"{d.get('message','')[:55]}")

    def _print_result(self, result, errors_after):
        fixes = result["fixes"]
        print()
        if fixes:
            print("  ── Fixes Applied ───────────────────────────────────")
            for i, fix in enumerate(fixes, 1):
                print(f"  [{i}] Line {fix['line']:>3}  "
                      f"Label={fix['label']}  "
                      f"Conf={fix['confidence']:.0%}")
                print(f"       {fix['description']}")
        else:
            print("  No automatic fixes could be applied.")

        print()
        print("  ── Before vs After ─────────────────────────────────")
        orig_lines = result["original"].splitlines()
        corr_lines = result["corrected"].splitlines()
        changed    = False
        for i in range(max(len(orig_lines), len(corr_lines))):
            o = orig_lines[i] if i < len(orig_lines) else ""
            c = corr_lines[i] if i < len(corr_lines) else ""
            if o != c:
                print(f"  Line {i + 1:>3}  - {o}")
                print(f"  Line {i + 1:>3}  + {c}")
                changed = True
        if not changed:
            print("  No source changes made.")

        print()
        status = "✓ FULLY CORRECTED" if result["success"] \
            else f"⚠ {len(errors_after)} error(s) remain"
        print(f"  Status    : {status}")
        print(f"  Saved to  : {result['out_file']}")
        print("─" * 62)

    def _print_batch_summary(self, results):
        print()
        print("=" * 62)
        print("  BATCH AUTO-CORRECTION SUMMARY")
        print("=" * 62)
        print(f"  {'File':<28} {'Before':>7} {'After':>6} {'Fixes':>6}  Status")
        print("  " + "-" * 58)
        for r in results:
            fname  = os.path.basename(r.get("file", "?"))[:26]
            before = r.get("errors_before", 0)
            after  = r.get("errors_after",  0)
            fixes  = r.get("fixes_applied", 0)
            ok     = r.get("success", False)
            status = "✓ FIXED" if ok else ("~ PARTIAL" if fixes else "✗ FAILED")
            print(f"  {fname:<28} {before:>7} {after:>6} {fixes:>6}  {status}")
        total_ok = sum(1 for r in results if r.get("success"))
        print("  " + "-" * 58)
        print(f"  Fully corrected : {total_ok}/{len(results)} files")
        print("=" * 62)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="auto_corrector.py",
        description="Week 9 — Automatic Error Correction"
    )
    parser.add_argument("language", nargs="?",
                        choices=["C","c","CPP","cpp","Java","java","JAVA","ALL","all"],
                        default="ALL")
    parser.add_argument("file",     nargs="?", default=None)
    parser.add_argument("--model",  default="error_model.pkl")
    parser.add_argument("--out",    default="auto_corrected")
    parser.add_argument("--all",    action="store_true")
    args = parser.parse_args()

    corrector = AutoCorrector(model_path=args.model, out_dir=args.out)

    if args.all or (args.language and args.language.upper() == "ALL"):
        corrector.run_all()
    elif args.file and os.path.isdir(args.file):
        corrector.run_directory(LANG_MAP.get(args.language, args.language), args.file)
    elif args.file and os.path.isfile(args.file):
        corrector.run(LANG_MAP.get(args.language, args.language), args.file)
    else:
        parser.print_help()