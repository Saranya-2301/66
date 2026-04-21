# ============================================================
# ERROR PREDICTOR
# Trains an ML classifier on the dataset and predicts
# correction suggestions for new errors.
#
# Models supported: RandomForest (default), SVM, NaiveBayes
# Saves/loads model with joblib for persistence.
# ============================================================

import os
import json
import pickle
import warnings
warnings.filterwarnings("ignore")

try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC
    from sklearn.naive_bayes import GaussianNB
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import (classification_report, confusion_matrix,
                                  accuracy_score)
    from sklearn.preprocessing import LabelEncoder
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

from feature_extractor import FeatureExtractor


# ─────────────────────────────────────────────────────────────
# Human-readable correction suggestions
# ─────────────────────────────────────────────────────────────
CORRECTION_MESSAGES = {
    "NO_ERROR":               "✓ No errors detected. Code looks clean.",
    "ADD_SEMICOLON":          "💡 Add a semicolon ';' at the end of the statement.",
    "ADD_CLOSING_BRACE":      "💡 Add a closing brace '}' to close the block.",
    "REMOVE_EXTRA_SEMICOLON": "💡 Remove the extra/duplicate semicolon ';'.",
    "FIX_TYPO_RETURN":        "💡 Fix typo: did you mean 'return'?",
    "FIX_TYPO_INT":           "💡 Fix typo: did you mean 'int'?",
    "FIX_TYPO_VOID":          "💡 Fix typo: did you mean 'void'?",
    "FIX_TYPO_CLASS":         "💡 Fix typo: did you mean 'class'?",
    "FIX_TYPO_PUBLIC":        "💡 Fix typo: did you mean 'public'?",
    "MISSING_TOKEN":          "💡 A required token appears to be missing at this position.",
    "EXTRANEOUS_TOKEN":       "💡 An unexpected token was found — consider removing it.",
    "MISMATCHED_TOKEN":       "💡 Token mismatch — check that opening/closing symbols match.",
    "NO_VIABLE_ALT":          "💡 The parser could not understand this construct — check syntax.",
    "UNRECOGNIZED_TOKEN":     "💡 Unrecognised character or token — check for typos or illegal chars.",
    "OTHER":                  "💡 Review this line carefully for syntax issues.",
}

# Map ANTLR error_category → likely correction label (rule-based fallback)
CATEGORY_TO_LABEL = {
    "MISSING_TOKEN":      "ADD_SEMICOLON",
    "EXTRANEOUS_TOKEN":   "REMOVE_EXTRA_SEMICOLON",
    "MISMATCHED_TOKEN":   "ADD_CLOSING_BRACE",
    "NO_VIABLE_ALT":      "OTHER",
    "UNRECOGNIZED_TOKEN": "FIX_TYPO_RETURN",
    "OTHER":              "OTHER",
}


# ─────────────────────────────────────────────────────────────
# Prediction result
# ─────────────────────────────────────────────────────────────
class Prediction:
    def __init__(self, label, confidence, suggestion, error_record=None):
        self.label        = label
        self.confidence   = confidence   # 0.0 – 1.0
        self.suggestion   = suggestion
        self.error_record = error_record

    def __repr__(self):
        return (f"Prediction(label={self.label!r}, "
                f"confidence={self.confidence:.0%}, "
                f"suggestion={self.suggestion!r})")


# ─────────────────────────────────────────────────────────────
# ErrorPredictor
# ─────────────────────────────────────────────────────────────
class ErrorPredictor:
    """
    Trains a classifier and predicts corrections for errors.

    Typical workflow:
        predictor = ErrorPredictor()
        predictor.train("dataset.csv")          # or train_from_json
        predictor.save("model.pkl")
        predictor.load("model.pkl")
        preds = predictor.predict_file("C", "buggy.c")
    """

    MODELS = {
        "random_forest": lambda: RandomForestClassifier(
            n_estimators=200, max_depth=None, random_state=42, n_jobs=-1),
        "gradient_boost": lambda: GradientBoostingClassifier(
            n_estimators=100, learning_rate=0.1, random_state=42),
        "svm": lambda: SVC(kernel="rbf", probability=True, random_state=42),
        "naive_bayes": lambda: GaussianNB(),
    }

    def __init__(self, model_type: str = "random_forest"):
        if not ML_AVAILABLE:
            raise ImportError(
                "scikit-learn and numpy are required.\n"
                "Run: pip install scikit-learn numpy joblib"
            )
        self.model_type  = model_type
        self.model       = self.MODELS[model_type]()
        self.label_enc   = LabelEncoder()
        self.extractor   = FeatureExtractor()
        self._trained    = False

    # ── training ────────────────────────────────────────────

    def train(self, csv_path: str, test_size: float = 0.2):
        """Train from a CSV produced by DatasetBuilder."""
        import csv as csv_mod
        rows = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv_mod.DictReader(f)
            for row in reader:
                rows.append(row)
        self._train_from_rows(rows, test_size)

    def train_from_json(self, json_path: str, test_size: float = 0.2):
        """Train from a JSON produced by DatasetBuilder."""
        with open(json_path, "r", encoding="utf-8") as f:
            rows = json.load(f)
        self._train_from_rows(rows, test_size)

    def _train_from_rows(self, rows, test_size):
        feat_prefix = "feat_"
        feat_cols   = [k for k in rows[0].keys() if k.startswith(feat_prefix)]

        X = np.array([[float(r[c]) for c in feat_cols] for r in rows])
        y_raw = [r["label"] for r in rows]

        y = self.label_enc.fit_transform(y_raw)

        # ── FIX 1: disable stratify when dataset is too small ──
        # stratify requires at least 2 samples per class in both splits.
        # With <30 rows it often fails, so we only use it for larger sets.
        use_stratify = len(rows) >= 30
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42,
            stratify=(y if use_stratify else None)
        )

        print(f"\n[Predictor] Training {self.model_type} on {len(X_train)} samples …")
        self.model.fit(X_train, y_train)
        self._trained = True

        y_pred = self.model.predict(X_test)
        acc    = accuracy_score(y_test, y_pred)
        print(f"[Predictor] Test accuracy: {acc:.2%}")

        # ── FIX 2: only pass labels that actually appear in the test set ──
        # label_enc.classes_ has ALL labels seen during fit_transform,
        # but the test split may not contain every class (small dataset).
        # We derive target_names only from classes present in y_test/y_pred.
        present_indices = sorted(set(y_test) | set(y_pred))
        present_names   = self.label_enc.inverse_transform(present_indices)
        print("\n" + classification_report(
            y_test, y_pred,
            labels       = present_indices,
            target_names = present_names,
            zero_division = 0
        ))

        # ── FIX 3: cap CV folds so we never ask for more folds than samples ──
        n_folds   = min(5, len(rows))          # never exceed total row count
        n_folds   = max(2, n_folds)            # need at least 2
        cv_scores = cross_val_score(self.model, X, y,
                                    cv=n_folds, scoring="accuracy")
        print(f"[Predictor] {n_folds}-fold CV: "
              f"{cv_scores.mean():.2%} ± {cv_scores.std():.2%}")

    # ── persistence ─────────────────────────────────────────

    def save(self, path: str):
        data = {
            "model":      self.model,
            "label_enc":  self.label_enc,
            "model_type": self.model_type,
        }
        joblib.dump(data, path)
        print(f"[Predictor] Model saved → {path}")

    def load(self, path: str):
        data = joblib.load(path)
        # Support both old format (label_enc) and new pipeline format (scaler)
        self.model      = data["model"]
        self.model_type = data.get("model_name", data.get("model_type", "unknown"))
        self._trained   = True

        if "label_enc" in data:
            # Old format from ErrorPredictor.train()
            self.label_enc   = data["label_enc"]
            self._use_pipeline = False
        else:
            # New format from models/transformer_model.py
            self.scaler          = data.get("scaler", None)
            self._feat_names     = list(data.get("feature_names", []))
            self._pipeline_labels = {0: "NONE", 1: "LEXICAL", 2: "SYNTAX"}
            self._use_pipeline   = True

        print(f"[Predictor] Model loaded ← {path}  (type={self.model_type})")

    # ── prediction ──────────────────────────────────────────

    def predict_error(self, error_record) -> Prediction:
        """Predict correction for a single ErrorRecord or dict."""
        if not self._trained:
            return self._rule_based(error_record)

        # ── pipeline model (73-feature, from transformer_model.py) ──
        if getattr(self, "_use_pipeline", False):
            return self._predict_pipeline(error_record)

        # ── old model (28-feature, from ErrorPredictor.train()) ──
        try:
            features  = np.array([self.extractor.extract(error_record)])
            label_idx = self.model.predict(features)[0]
            label     = self.label_enc.inverse_transform([label_idx])[0]
            if hasattr(self.model, "predict_proba"):
                proba      = self.model.predict_proba(features)[0]
                classes    = list(self.model.classes_)
                col        = classes.index(label_idx) if label_idx in classes else 0
                confidence = float(proba[col])
            else:
                confidence = 1.0
            suggestion = CORRECTION_MESSAGES.get(label, CORRECTION_MESSAGES["OTHER"])
            return Prediction(label, confidence, suggestion, error_record)
        except Exception:
            return self._rule_based(error_record)

    def _predict_pipeline(self, error_record) -> Prediction:
        """Use the 73-feature pipeline model (best_model.pkl)."""
        # Build feature vector from error record using same features
        # the pipeline model was trained on — derived from error properties
        if hasattr(error_record, "to_dict"):
            d = error_record.to_dict()
        else:
            d = error_record

        vec = self._build_pipeline_features(d)
        X   = np.array([vec], dtype=np.float32)

        if self.scaler is not None:
            X = self.scaler.transform(X)

        pred_idx  = int(self.model.predict(X)[0])
        classes   = list(self.model.classes_)
        col       = classes.index(pred_idx) if pred_idx in classes else 0

        if hasattr(self.model, "predict_proba"):
            proba      = self.model.predict_proba(X)[0]
            confidence = float(proba[col])
        else:
            confidence = 1.0

        # Map numeric label back to string
        label_str = self._pipeline_labels.get(pred_idx, "OTHER")

        # Map pipeline labels (NONE/LEXICAL/SYNTAX) to correction labels
        category = d.get("error_category", "OTHER")
        msg      = d.get("message", "").lower()
        label    = self._refine_label(label_str, category, msg)

        suggestion = CORRECTION_MESSAGES.get(label, CORRECTION_MESSAGES["OTHER"])
        return Prediction(label, confidence, suggestion, error_record)

    def _build_pipeline_features(self, d):
        """
        Build a feature vector that matches the 73-column pipeline model.
        Uses the same b_/l_/s_/d_ feature groups from preprocessing.py
        but computed live from the ErrorRecord fields.
        """
        msg      = str(d.get("message", ""))
        src      = str(d.get("source_line", ""))
        lang     = str(d.get("language", "C"))
        etype    = str(d.get("error_type", "SYNTAX"))
        ecat     = str(d.get("error_category", "OTHER"))
        line     = int(d.get("line", 1))
        col      = int(d.get("column", 0))

        msg_lower = msg.lower()
        src_lower = src.lower()

        # ── b_ basic features (24) ───────────────────────────
        b = [
            min(line, 100) / 100.0,             # b_line_count proxy
            min(len(src.split()), 50) / 50.0,   # b_non_empty_lines proxy
            min(len(src.split()), 50) / 50.0,   # b_token_count proxy
            1.0 if src.count('{') != src.count('}') else 0.0,  # b_brace_balance
            1.0 if src.count('(') != src.count(')') else 0.0,  # b_paren_balance
            1.0 if src.count('[') != src.count(']') else 0.0,  # b_bracket_balance
            0.0,                                # b_angle_balance
            min(src.count(';'), 10) / 10.0,    # b_semicolon_count
            1.0 if 'main' in src_lower else 0.0, # b_has_main
            min(len(src), 200) / 200.0,         # b_avg_line_length
            min(len(src), 200) / 200.0,         # b_max_line_length
            0.0,                                # b_keyword_count
            min(len(set(src.split())), 20) / 20.0, # b_identifier_count
            0.0,                                # b_operator_count
            0.0,                                # b_literal_count
            min(col // 4, 10) / 10.0,          # b_indent_depth_max
            min(col // 4, 10) / 10.0,          # b_indent_depth_avg
            0.0,                                # b_comment_line_count
            0.0,                                # b_string_literal_count
            0.0,                                # b_char_literal_count
            0.0,                                # b_numeric_literal_count
            0.0,                                # b_blank_line_ratio
            1.0,                                # b_code_density
            min(line, 100) / 100.0,             # language_label proxy
        ]

        # ── l_ lexical features (16) ─────────────────────────
        l = [
            min(len(set(msg.split())), 20) / 20.0,  # l_unique_tokens
            0.7,                                     # l_token_diversity
            0.0,                                     # l_top_identifiers (skip)
            0.2,                                     # l_keyword_density
            5.0 / 20.0,                              # l_identifier_avg_length
            0.0,                                     # l_long_identifier_count
            0.0,                                     # l_camel_case_count
            0.0,                                     # l_snake_case_count
            0.0,                                     # l_upper_case_count
            0.0,                                     # l_numeric_in_ident_count
            0.0,                                     # l_undefined_var_hints
            1.0 if 'unclosed' in msg_lower else 0.0, # l_unclosed_string_count
            1.0 if 'invalid' in msg_lower else 0.0,  # l_invalid_id_count
            1.0 if '+++' in msg or '---' in msg else 0.0, # l_double_operator_count
            1.0 if '0x' in src else 0.0,             # l_hex_literal_count
            0.0,                                     # l_octal_literal_count
        ]

        # ── s_ syntax features (25) ──────────────────────────
        s = [
            0.0,                                     # s_function_count
            0.0,                                     # s_class_count
            1.0 if 'if' in src_lower else 0.0,      # s_if_count
            1.0 if 'else' in src_lower else 0.0,    # s_else_count
            1.0 if 'for' in src_lower else 0.0,     # s_for_count
            1.0 if 'while' in src_lower else 0.0,   # s_while_count
            0.0,                                     # s_do_while_count
            1.0 if 'switch' in src_lower else 0.0,  # s_switch_count
            1.0 if 'return' in src_lower else 0.0,  # s_return_count
            min(col // 4, 5) / 5.0,                 # s_nesting_depth_max
            min(col // 4, 5) / 5.0,                 # s_nesting_depth_avg
            1.0 if 'try' in src_lower else 0.0,     # s_try_catch_count
            1.0 if '#include' in src or 'import' in src else 0.0, # s_include_import_count
            1.0 if ';;' in src else 0.0,             # s_extra_semicolons
            1.0 if '{}' in src else 0.0,             # s_empty_block_count
            0.0,                                     # s_dangling_else_count
            1.0 if 'missing' in msg_lower else 0.0, # s_missing_semi_hints
            1.0 if ',)' in src else 0.0,             # s_comma_after_arg_count
            1.0 if '?' in src else 0.0,              # s_ternary_count
            1.0 if '*' in src and lang in ('C','CPP') else 0.0,  # s_pointer_count
            1.0 if '&' in src and lang == 'CPP' else 0.0,        # s_reference_count
            1.0 if 'template' in src_lower else 0.0, # s_template_count
            1.0 if '@' in src else 0.0,              # s_annotation_count
            0.0,                                     # s_lambda_count
            1.0 if 'operator' in src_lower else 0.0, # s_operator_overload_count
        ]

        # ── d_ diff features (9) ─────────────────────────────
        d_feats = [
            0.0,   # d_line_diff
            0.0,   # d_token_diff
            0.0,   # d_char_diff
            1.0 if 'semicolon' in msg_lower or "';'" in msg else 0.0, # d_semicolon_diff
            1.0 if 'brace' in msg_lower or "'{'" in msg else 0.0,     # d_brace_diff
            0.0,   # d_added_token_count
            0.0,   # d_removed_token_count
            1.0,   # d_edit_distance_approx
            0.9,   # d_similarity_ratio
        ]

        vec = b + l + s + d_feats

        # Pad or trim to match model's expected feature count
        n_expected = len(self._feat_names) if self._feat_names else 73
        if len(vec) < n_expected:
            vec += [0.0] * (n_expected - len(vec))
        elif len(vec) > n_expected:
            vec = vec[:n_expected]

        return vec

    def _refine_label(self, pipeline_label, category, msg_lower):
        """Map NONE/LEXICAL/SYNTAX + ANTLR category to a specific correction label."""
        if pipeline_label == "NONE":
            return "NO_ERROR"
        if "';'" in msg_lower or "semicolon" in msg_lower or "missing_token" == category.lower():
            return "ADD_SEMICOLON"
        if "'}'" in msg_lower or "brace" in msg_lower:
            return "ADD_CLOSING_BRACE"
        if "extraneous" in msg_lower:
            return "REMOVE_EXTRA_SEMICOLON"
        if "typo" in msg_lower or "unrecognized" in category.lower():
            return "FIX_TYPO_RETURN"
        if pipeline_label == "LEXICAL":
            return "UNRECOGNIZED_TOKEN"
        if pipeline_label == "SYNTAX":
            return "MISSING_TOKEN"
        return "OTHER"

    def predict_batch(self, error_records: list) -> list:
        """Predict corrections for a list of ErrorRecords."""
        return [self.predict_error(e) for e in error_records]

    def predict_file(self, language: str, file_path: str) -> list:
        """
        Full pipeline: collect errors from file → predict corrections.
        Returns list of Prediction objects.
        """
        from error_collector import ErrorCollector
        collector = ErrorCollector()
        errors = collector.collect(language, file_path)
        if not errors:
            return []
        return self.predict_batch(errors)

    # ── rule-based fallback (no trained model needed) ───────

    def _rule_based(self, error_record) -> Prediction:
        if hasattr(error_record, "to_dict"):
            d = error_record.to_dict()
        else:
            d = error_record
        cat    = d.get("error_category", "OTHER")
        label  = CATEGORY_TO_LABEL.get(cat, "OTHER")
        msg    = d.get("message", "").lower()

        # Refine by message content
        if "';'" in msg or "semicolon" in msg:
            label = "ADD_SEMICOLON"
        elif "'}'" in msg or "'}'":
            pass  # keep label
        elif "extraneous" in msg:
            label = "REMOVE_EXTRA_SEMICOLON"

        suggestion = CORRECTION_MESSAGES.get(label, CORRECTION_MESSAGES["OTHER"])
        return Prediction(label, 0.6, suggestion, error_record)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python error_predictor.py <C|CPP|Java> <file> [model.pkl]")
        sys.exit(1)

    lang      = sys.argv[1]
    fpath     = sys.argv[2]
    model_pkl = sys.argv[3] if len(sys.argv) > 3 else None

    predictor = ErrorPredictor()
    if model_pkl and os.path.exists(model_pkl):
        predictor.load(model_pkl)

    preds = predictor.predict_file(lang, fpath)
    if not preds:
        print("✓ No errors found.")
    else:
        for p in preds:
            print(p)