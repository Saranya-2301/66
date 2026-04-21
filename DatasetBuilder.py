# ============================================================
# dataset_builder.py
# Builds the ML training dataset by:
#   1. Scanning clean source files
#   2. Injecting known errors programmatically
#   3. Running the error collector
#   4. Labelling (error type → correction suggestion)
#   5. Saving to CSV / JSON for model training
# ============================================================

import os
import json
import random
import csv
import tempfile

from error_collector import ErrorCollector

# NOTE: FeatureExtractor is NOT used here anymore.
# Raw error fields are stored directly. The ErrorPredictor
# builds features at prediction time from these raw fields.


# ─────────────────────────────────────────────────────────────
# Error injection strategies
# Each returns (mutated_source_code, label, description)
# ─────────────────────────────────────────────────────────────

def _inject_missing_semicolon(source: str, lang: str):
    lines = source.splitlines()
    candidates = [i for i, l in enumerate(lines) if ";" in l
                  and not l.strip().startswith("//")
                  and not l.strip().startswith("*")]
    if not candidates:
        return None
    idx = random.choice(candidates)
    col = lines[idx].rfind(";")
    lines[idx] = lines[idx][:col] + lines[idx][col + 1:]
    return "\n".join(lines), "ADD_SEMICOLON", f"Missing ';' on line {idx+1}"


def _inject_missing_brace(source: str, lang: str):
    lines = source.splitlines()
    candidates = [i for i, l in enumerate(lines) if l.strip() == "}"]
    if not candidates:
        return None
    idx = random.choice(candidates)
    lines[idx] = lines[idx].replace("}", "", 1)
    return "\n".join(lines), "ADD_CLOSING_BRACE", f"Missing '}}' on line {idx+1}"


def _inject_typo_keyword(source: str, lang: str):
    replacements = {
        "C":    [("return", "retun"),  ("int", "nt"),    ("void", "viod")],
        "CPP":  [("return", "retun"),  ("class", "clas"), ("void", "viod")],
        "Java": [("public", "pubic"),  ("return", "retun"), ("class", "clas")],
    }
    pairs = replacements.get(lang, replacements["C"])
    random.shuffle(pairs)
    for original, typo in pairs:
        if original in source:
            source = source.replace(original, typo, 1)
            return source, f"FIX_TYPO_{original.upper()}", \
                   f"Typo: '{typo}' should be '{original}'"
    return None


def _inject_extra_token(source: str, lang: str):
    lines = source.splitlines()
    candidates = [i for i, l in enumerate(lines)
                  if l.strip() and not l.strip().startswith("//")]
    if not candidates:
        return None
    idx = random.choice(candidates)
    lines[idx] = lines[idx] + ";"
    return "\n".join(lines), "REMOVE_EXTRA_SEMICOLON", \
           f"Extra ';' on line {idx+1}"


INJECTORS = [
    _inject_missing_semicolon,
    _inject_missing_brace,
    _inject_typo_keyword,
    _inject_extra_token,
]


# ─────────────────────────────────────────────────────────────
# DatasetBuilder
# ─────────────────────────────────────────────────────────────
class DatasetBuilder:

    def __init__(self, injections_per_file: int = 4, seed: int = 42):
        self.injections_per_file = injections_per_file
        self.records  = []
        self.collector = ErrorCollector()
        random.seed(seed)

    # ── public API ───────────────────────────────────────────

    def add_file(self, language: str, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
        except FileNotFoundError:
            print(f"[DatasetBuilder] File not found: {file_path}")
            return

        # Clean file → NO_ERROR row
        errors = self.collector.collect(language, file_path)
        if not errors:
            self.records.append(
                self._make_row(language, file_path, None, "NO_ERROR", source)
            )

        # Injected variants
        injectors = random.choices(INJECTORS, k=self.injections_per_file)
        for inj in injectors:
            result = inj(source, language)
            if result is None:
                continue
            mutated_src, label, _ = result
            self._run_on_source(language, file_path, mutated_src, label)

    def add_directory(self, language: str, directory: str, ext: str):
        if not os.path.isdir(directory):
            print(f"[DatasetBuilder] Directory not found: {directory}")
            return
        for fname in sorted(os.listdir(directory)):
            if fname.endswith(ext):
                self.add_file(language, os.path.join(directory, fname))

    def save_csv(self, path: str):
        if not self.records:
            print("[DatasetBuilder] No records to save.")
            return
        fieldnames = list(self.records[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.records)
        print(f"[DatasetBuilder] Saved {len(self.records)} rows → {path}")

    def save_json(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)
        print(f"[DatasetBuilder] Saved {len(self.records)} rows → {path}")

    def summary(self):
        from collections import Counter
        labels = [r["label"] for r in self.records]
        counts = Counter(labels)
        print("\n[DatasetBuilder] Dataset summary:")
        print(f"  Total records : {len(self.records)}")
        for label, count in sorted(counts.items()):
            print(f"  {label:35s}: {count}")

    # ── internals ────────────────────────────────────────────

    def _run_on_source(self, language, orig_path, source, label):
        suffix = {"C": ".c", "CPP": ".cpp", "Java": ".java"}.get(language, ".txt")
        with tempfile.NamedTemporaryFile(mode="w", suffix=suffix,
                                        delete=False, encoding="utf-8") as tmp:
            tmp.write(source)
            tmp_path = tmp.name
        try:
            errors = self.collector.collect(language, tmp_path)
            if errors:
                for e in errors:
                    self.records.append(
                        self._make_row(language, orig_path, e, label, source)
                    )
            else:
                self.records.append(
                    self._make_row(language, orig_path, None, label, source)
                )
        finally:
            os.unlink(tmp_path)

    def _make_row(self, language, file_path, error, label, source):
        """
        Build one dataset row.
        Stores raw error fields directly — NO FeatureExtractor call.
        Features are built at prediction time by ErrorPredictor.
        """
        row = {
            "label"    : label,
            "language" : language,
            "file_path": file_path,
        }

        if error:
            row.update({
                "error_type"      : error.error_type,
                "error_category"  : error.error_category,
                "line"            : error.line,
                "column"          : error.column,
                "message"         : error.message,
                "offending_symbol": error.offending_symbol or "",
                "source_line"     : error.source_line,
            })
        else:
            row.update({
                "error_type"      : "NONE",
                "error_category"  : "OTHER",
                "line"            : 0,
                "column"          : 0,
                "message"         : "",
                "offending_symbol": "",
                "source_line"     : "",
            })

        # Build feature columns directly — no FeatureExtractor import needed
        from feature_extractor import FeatureExtractor
        fe = FeatureExtractor()
        d = {
            "language"      : language,
            "error_type"    : row["error_type"],
            "error_category": row["error_category"],
            "line"          : row["line"],
            "column"        : row["column"],
            "message"       : row["message"],
            "source_line"   : row["source_line"],
        }
        try:
            features = fe.extract(d)
        except Exception:
            features = [0.0] * fe.FEATURE_DIM

        for name, val in zip(fe.feature_names(), features):
            row[f"feat_{name}"] = val

        return row


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("DatasetBuilder — run programmatically or via ml_pipeline.py")