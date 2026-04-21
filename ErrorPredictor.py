# ============================================================
# ErrorPredictor.py
# Trains an ML classifier on the dataset and predicts
# correction suggestions for new errors.
# Models supported: RandomForest (default), SVM, NaiveBayes
# ============================================================

import os
import json
import warnings
warnings.filterwarnings("ignore")

try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC
    from sklearn.naive_bayes import GaussianNB
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import classification_report, accuracy_score
    from sklearn.preprocessing import LabelEncoder
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

from feature_extractor import FeatureExtractor


# ─────────────────────────────────────────────────────────────
# Correction messages — every possible label
# ─────────────────────────────────────────────────────────────
CORRECTION_MESSAGES = {
    "NO_ERROR":               "✓ No errors detected. Code looks clean.",
    "ADD_SEMICOLON":          "💡 Add a semicolon ';' at the end of the statement.",
    "ADD_CLOSING_BRACE":      "💡 Add a closing brace '}' to close the block.",
    "ADD_OPENING_BRACE":      "💡 Add an opening brace '{' to start the block.",
    "REMOVE_EXTRA_SEMICOLON": "💡 Remove the extra/duplicate semicolon ';'.",
    "ADD_CLOSING_PAREN":      "💡 Add a closing parenthesis ')' to complete the expression.",
    "ADD_OPENING_PAREN":      "💡 Add an opening parenthesis '(' to complete the expression.",
    "FIX_TYPO_RETURN":        "💡 Fix typo: did you mean 'return'?",
    "FIX_TYPO_INT":           "💡 Fix typo: did you mean 'int'?",
    "FIX_TYPO_VOID":          "💡 Fix typo: did you mean 'void'?",
    "FIX_TYPO_CLASS":         "💡 Fix typo: did you mean 'class'?",
    "FIX_TYPO_PUBLIC":        "💡 Fix typo: did you mean 'public'?",
    "FIX_TYPO_STATIC":        "💡 Fix typo: did you mean 'static'?",
    "FIX_TYPO_INCLUDE":       "💡 Fix typo: did you mean '#include'?",
    "MISSING_TOKEN":          "💡 A required token is missing at this position.",
    "EXTRANEOUS_TOKEN":       "💡 An unexpected extra token was found — remove it.",
    "MISMATCHED_TOKEN":       "💡 Token mismatch — check opening/closing symbols match.",
    "NO_VIABLE_ALT":          "💡 Parser could not understand this — check overall syntax.",
    "UNRECOGNIZED_TOKEN":     "💡 Unrecognised character or token — check for typos.",
    "OTHER":                  "💡 Review this line carefully for syntax issues.",
}

# Map ANTLR error_category → correction label (used as fallback)
CATEGORY_TO_LABEL = {
    "MISSING_TOKEN":      "ADD_SEMICOLON",
    "EXTRANEOUS_TOKEN":   "REMOVE_EXTRA_SEMICOLON",
    "MISMATCHED_TOKEN":   "MISMATCHED_TOKEN",
    "NO_VIABLE_ALT":      "ADD_SEMICOLON",
    "UNRECOGNIZED_TOKEN": "UNRECOGNIZED_TOKEN",
    "OTHER":              "OTHER",
}


# ─────────────────────────────────────────────────────────────
# Prediction result
# ─────────────────────────────────────────────────────────────
class Prediction:
    def __init__(self, label, confidence, suggestion, error_record=None):
        self.label        = label
        self.confidence   = confidence
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

    MODELS = {
        "random_forest":  lambda: RandomForestClassifier(
            n_estimators=200, max_depth=None, random_state=42, n_jobs=-1),
        "gradient_boost": lambda: GradientBoostingClassifier(
            n_estimators=100, learning_rate=0.1, random_state=42),
        "svm":            lambda: SVC(kernel="rbf", probability=True, random_state=42),
        "naive_bayes":    lambda: GaussianNB(),
    }

    def __init__(self, model_type: str = "random_forest"):
        if not ML_AVAILABLE:
            raise ImportError(
                "scikit-learn and numpy are required.\n"
                "Run: pip install scikit-learn numpy joblib"
            )
        self.model_type    = model_type
        self.model         = self.MODELS[model_type]()
        self.label_enc     = LabelEncoder()
        self.extractor     = FeatureExtractor()
        self._trained      = False
        self._use_pipeline = False

    # ── training ────────────────────────────────────────────

    def train(self, csv_path: str, test_size: float = 0.2):
        import csv as csv_mod
        rows = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv_mod.DictReader(f)
            for row in reader:
                rows.append(row)
        self._train_from_rows(rows, test_size)

    def train_from_json(self, json_path: str, test_size: float = 0.2):
        with open(json_path, "r", encoding="utf-8") as f:
            rows = json.load(f)
        self._train_from_rows(rows, test_size)

    def _train_from_rows(self, rows, test_size):
        feat_prefix = "feat_"
        feat_cols   = [k for k in rows[0].keys() if k.startswith(feat_prefix)]

        X     = np.array([[float(r[c]) for c in feat_cols] for r in rows])
        y_raw = [r["label"] for r in rows]
        y     = self.label_enc.fit_transform(y_raw)

        use_stratify = len(rows) >= 30
        actual_test  = test_size if len(rows) >= 50 else 0.3
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=actual_test, random_state=42,
            stratify=(y if use_stratify else None)
        )

        print(f"\n[Predictor] Training {self.model_type} on {len(X_train)} samples ...")
        self.model.fit(X_train, y_train)
        self._trained      = True
        self._use_pipeline = False

        y_pred = self.model.predict(X_test)
        acc    = accuracy_score(y_test, y_pred)
        print(f"[Predictor] Test accuracy: {acc:.2%}")

        present_indices = sorted(set(y_test) | set(y_pred))
        present_names   = self.label_enc.inverse_transform(present_indices)
        print("\n" + classification_report(
            y_test, y_pred,
            labels=present_indices, target_names=present_names,
            zero_division=0
        ))

        n_folds   = min(5, max(2, len(rows)))
        cv_scores = cross_val_score(self.model, X, y, cv=n_folds, scoring="accuracy")
        print(f"[Predictor] {n_folds}-fold CV: "
              f"{cv_scores.mean():.2%} +/- {cv_scores.std():.2%}")

    # ── persistence ─────────────────────────────────────────

    def save(self, path: str):
        joblib.dump({
            "model":      self.model,
            "label_enc":  self.label_enc,
            "model_type": self.model_type,
        }, path)
        print(f"[Predictor] Model saved -> {path}")

    def load(self, path: str):
        data            = joblib.load(path)
        self.model      = data["model"]
        self.model_type = data.get("model_name", data.get("model_type", "unknown"))
        self._trained   = True

        if "label_enc" in data:
            self.label_enc     = data["label_enc"]
            self._use_pipeline = False
        else:
            self.scaler           = data.get("scaler", None)
            self._feat_names      = list(data.get("feature_names", []))
            self._pipeline_labels = {0: "NONE", 1: "LEXICAL", 2: "SYNTAX"}
            self._use_pipeline    = True

        print(f"[Predictor] Model loaded <- {path}  (type={self.model_type})")

    # ── prediction ──────────────────────────────────────────

    def predict_error(self, error_record) -> Prediction:
        """Predict correction for a single ErrorRecord or dict."""
        if not self._trained:
            return self._rule_based(error_record)

        if self._use_pipeline:
            return self._predict_pipeline(error_record)

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

            # Always override ML prediction with message-based rules
            # because ANTLR messages are highly reliable signals
            label = self._override_with_message(error_record, label)

            suggestion = CORRECTION_MESSAGES.get(label, CORRECTION_MESSAGES["OTHER"])
            return Prediction(label, confidence, suggestion, error_record)
        except Exception:
            return self._rule_based(error_record)

    # ─────────────────────────────────────────────────────────
    # _override_with_message
    # Overrides the ML-predicted label using ANTLR message content.
    # ANTLR messages are very reliable — more so than a small ML model.
    # Every error type is handled here.
    # ─────────────────────────────────────────────────────────
    def _override_with_message(self, error_record, ml_label: str) -> str:
        """
        Override ML prediction using the raw ANTLR error message.
        Returns the most accurate correction label.
        """
        if hasattr(error_record, "to_dict"):
            d = error_record.to_dict()
        else:
            d = error_record

        msg  = d.get("message", "").lower()
        cat  = d.get("error_category", "OTHER")
        src  = d.get("source_line", "").lower()
        sym  = str(d.get("offending_symbol", "") or "").lower()

        # ── SEMICOLON errors ────────────────────────────────
        if "';'" in msg or "semicolon" in msg:
            return "ADD_SEMICOLON"

        # ── MISSING token — check what token is missing ─────
        if "missing" in msg:
            if "'{'" in msg or "'{'" in msg:
                return "ADD_OPENING_BRACE"
            if "'}'" in msg:
                return "ADD_CLOSING_BRACE"
            if "'('" in msg:
                return "ADD_OPENING_PAREN"
            if "')'" in msg:
                return "ADD_CLOSING_PAREN"
            # default missing → semicolon (most common)
            return "ADD_SEMICOLON"

        # ── EXTRANEOUS token ────────────────────────────────
        if "extraneous" in msg:
            if "';'" in msg or sym == ";":
                return "REMOVE_EXTRA_SEMICOLON"
            return "EXTRANEOUS_TOKEN"

        # ── MISMATCHED token ────────────────────────────────────────
        if "mismatched" in msg:
            if "'}'" in msg or sym == "}":
                return "ADD_CLOSING_BRACE"
            if "')'" in msg or sym == ")":
                return "ADD_CLOSING_PAREN"
            if "';'" in msg or sym == ";":
                return "ADD_SEMICOLON"
            if "'<<'" in msg or "<<" in msg:
                return "FIX_OPERATOR_SHIFT"
            return "MISMATCHED_TOKEN"
        # ── NO VIABLE ALTERNATIVE ───────────────────────────
        if "no viable" in msg or "no viable alternative" in msg:
            # Check source line for clues
            if src.endswith("endl") or src.endswith("cin") or src.endswith("cout"):
                return "ADD_SEMICOLON"
            if src.count("{") > src.count("}"):
                return "ADD_CLOSING_BRACE"
            if src.count("(") > src.count(")"):
                return "ADD_CLOSING_PAREN"
            return "ADD_SEMICOLON"

        # ── TOKEN RECOGNITION (lexical) ─────────────────────
        if "token recognition" in msg or "extraneous input" in msg:
            return "UNRECOGNIZED_TOKEN"

        # ── TYPO detection from offending symbol ────────────
        if sym in ("retun", "retrun", "retur", "reutrn"):
            return "FIX_TYPO_RETURN"
        if sym in ("viod", "vodi", "voide"):
            return "FIX_TYPO_VOID"
        if sym in ("nt", "itn", "intt"):
            return "FIX_TYPO_INT"
        if sym in ("clas", "calss", "claas"):
            return "FIX_TYPO_CLASS"
        if sym in ("pubic", "publci", "pubilc"):
            return "FIX_TYPO_PUBLIC"
        if sym in ("statc", "statci", "sttaic"):
            return "FIX_TYPO_STATIC"
        if sym in ("includ", "incldue", "inculde"):
            return "FIX_TYPO_INCLUDE"

        # ── BRACE errors ────────────────────────────────────
        if "'}'" in msg or "brace" in msg:
            return "ADD_CLOSING_BRACE"

        # ── PAREN errors ────────────────────────────────────
        if "')'" in msg or "paren" in msg:
            return "ADD_CLOSING_PAREN"

        # No strong signal — keep ML prediction
        return ml_label

    def _predict_pipeline(self, error_record) -> Prediction:
        """Use the 73-feature pipeline model (best_model.pkl)."""
        if hasattr(error_record, "to_dict"):
            d = error_record.to_dict()
        else:
            d = error_record

        vec = self._build_pipeline_features(d)
        X   = np.array([vec], dtype=np.float32)

        if self.scaler is not None:
            X = self.scaler.transform(X)

        pred_idx = int(self.model.predict(X)[0])
        classes  = list(self.model.classes_)
        col      = classes.index(pred_idx) if pred_idx in classes else 0

        if hasattr(self.model, "predict_proba"):
            proba      = self.model.predict_proba(X)[0]
            confidence = float(proba[col])
        else:
            confidence = 1.0

        label_str = self._pipeline_labels.get(pred_idx, "OTHER")
        category  = d.get("error_category", "OTHER")
        msg       = d.get("message", "").lower()
        label     = self._refine_label(label_str, category, msg)

        # Also apply message override for pipeline model
        label = self._override_with_message(error_record, label)

        suggestion = CORRECTION_MESSAGES.get(label, CORRECTION_MESSAGES["OTHER"])
        return Prediction(label, confidence, suggestion, error_record)

    def _build_pipeline_features(self, d):
        """Build 73-dim feature vector from error record fields."""
        msg       = str(d.get("message", ""))
        src       = str(d.get("source_line", ""))
        lang      = str(d.get("language", "C"))
        line      = int(d.get("line", 1))
        col       = int(d.get("column", 0))
        msg_lower = msg.lower()
        src_lower = src.lower()

        b = [
            min(line, 100) / 100.0,
            min(len(src.split()), 50) / 50.0,
            min(len(src.split()), 50) / 50.0,
            1.0 if src.count('{') != src.count('}') else 0.0,
            1.0 if src.count('(') != src.count(')') else 0.0,
            1.0 if src.count('[') != src.count(']') else 0.0,
            0.0,
            min(src.count(';'), 10) / 10.0,
            1.0 if 'main'    in src_lower else 0.0,
            min(len(src), 200) / 200.0,
            min(len(src), 200) / 200.0,
            0.0, 0.0, 0.0, 0.0,
            min(col // 4, 10) / 10.0,
            min(col // 4, 10) / 10.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
            min(line, 100) / 100.0,
        ]
        l = [
            min(len(set(msg.split())), 20) / 20.0,
            0.7, 0.0, 0.2, 0.25,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            1.0 if 'unclosed' in msg_lower else 0.0,
            1.0 if 'invalid'  in msg_lower else 0.0,
            0.0,
            1.0 if '0x' in src else 0.0,
            0.0,
        ]
        s = [
            0.0, 0.0,
            1.0 if 'if'       in src_lower else 0.0,
            1.0 if 'else'     in src_lower else 0.0,
            1.0 if 'for'      in src_lower else 0.0,
            1.0 if 'while'    in src_lower else 0.0,
            0.0,
            1.0 if 'switch'   in src_lower else 0.0,
            1.0 if 'return'   in src_lower else 0.0,
            min(col // 4, 5) / 5.0,
            min(col // 4, 5) / 5.0,
            1.0 if 'try'      in src_lower else 0.0,
            1.0 if '#include' in src or 'import' in src else 0.0,
            1.0 if ';;'       in src else 0.0,
            1.0 if '{}'       in src else 0.0,
            0.0,
            1.0 if 'missing'  in msg_lower else 0.0,
            1.0 if ',)'       in src else 0.0,
            1.0 if '?'        in src else 0.0,
            1.0 if '*'        in src and lang in ('C', 'CPP') else 0.0,
            1.0 if '&'        in src and lang == 'CPP' else 0.0,
            1.0 if 'template' in src_lower else 0.0,
            1.0 if '@'        in src else 0.0,
            0.0,
            1.0 if 'operator' in src_lower else 0.0,
        ]
        d_feats = [
            0.0, 0.0, 0.0,
            1.0 if 'semicolon' in msg_lower or "';'" in msg else 0.0,
            1.0 if 'brace'     in msg_lower or "'{'" in msg else 0.0,
            0.0, 0.0, 1.0, 0.9,
        ]

        vec        = b + l + s + d_feats
        n_expected = len(self._feat_names) if self._feat_names else 73
        if len(vec) < n_expected:
            vec += [0.0] * (n_expected - len(vec))
        return vec[:n_expected]

    def _refine_label(self, pipeline_label, category, msg_lower):
        """Map NONE/LEXICAL/SYNTAX pipeline label to a specific correction label."""
        if pipeline_label == "NONE":
            return "NO_ERROR"
        if "';'" in msg_lower or "semicolon" in msg_lower:
            return "ADD_SEMICOLON"
        if "missing" in msg_lower:
            return "ADD_SEMICOLON"
        if "extraneous" in msg_lower:
            return "REMOVE_EXTRA_SEMICOLON"
        if "'}'" in msg_lower or "brace" in msg_lower:
            return "ADD_CLOSING_BRACE"
        if "')'" in msg_lower or "paren" in msg_lower:
            return "ADD_CLOSING_PAREN"
        if "typo" in msg_lower or "unrecognized" in category.lower():
            return "FIX_TYPO_RETURN"
        if pipeline_label == "LEXICAL":
            return "UNRECOGNIZED_TOKEN"
        if pipeline_label == "SYNTAX":
            return "ADD_SEMICOLON"
        return "OTHER"

    # ── rule-based fallback (no model needed) ───────────────

    def _rule_based(self, error_record) -> Prediction:
        """Pure rule-based prediction using ANTLR message content."""
        if hasattr(error_record, "to_dict"):
            d = error_record.to_dict()
        else:
            d = error_record

        cat = d.get("error_category", "OTHER")
        msg = d.get("message", "").lower()
        sym = str(d.get("offending_symbol", "") or "").lower()
        src = d.get("source_line", "").lower()

        # Use the full override logic
        dummy_label = CATEGORY_TO_LABEL.get(cat, "OTHER")
        label       = self._override_with_message(d, dummy_label)

        suggestion = CORRECTION_MESSAGES.get(label, CORRECTION_MESSAGES["OTHER"])
        return Prediction(label, 0.6, suggestion, error_record)

    def predict_batch(self, error_records: list) -> list:
        """Predict corrections for a list of ErrorRecords."""
        return [self.predict_error(e) for e in error_records]

    def predict_file(self, language: str, file_path: str) -> list:
        """Collect errors from file then predict corrections."""
        from error_collector import ErrorCollector
        errors = ErrorCollector().collect(language, file_path)
        if not errors:
            return []
        return self.predict_batch(errors)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python ErrorPredictor.py <C|CPP|Java> <file> [model.pkl]")
        sys.exit(1)

    lang      = sys.argv[1]
    fpath     = sys.argv[2]
    model_pkl = sys.argv[3] if len(sys.argv) > 3 else None

    predictor = ErrorPredictor()
    if model_pkl and os.path.exists(model_pkl):
        predictor.load(model_pkl)

    preds = predictor.predict_file(lang, fpath)
    if not preds:
        print("No errors found.")
    else:
        for p in preds:
            print(p)