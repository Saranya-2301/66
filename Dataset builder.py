# ============================================================
# FEATURE EXTRACTOR
# Converts ErrorRecord objects into numerical/categorical
# feature vectors for ML training and prediction.
# ============================================================

import re
import json


# ─────────────────────────────────────────────────────────────
# Feature vocabulary (kept consistent across train/predict)
# ─────────────────────────────────────────────────────────────
LANGUAGES       = ["C", "CPP", "Java"]
ERROR_TYPES     = ["LEXICAL", "SYNTAX"]
ERROR_CATEGORIES = [
    "MISSING_TOKEN", "EXTRANEOUS_TOKEN", "MISMATCHED_TOKEN",
    "NO_VIABLE_ALT", "UNRECOGNIZED_TOKEN", "OTHER"
]

# Common C/C++/Java keywords likely to appear in error messages
KEYWORD_HINTS = [
    "semicolon", "semi", ";", "{", "}", "(", ")", "[", "]",
    "identifier", "type", "return", "int", "void", "class",
    "if", "while", "for", "else", "string", "eof"
]

# C-family punctuation/operator tokens that appear in ANTLR messages
TOKEN_PATTERN = re.compile(r"'([^']+)'")


def _one_hot(value, vocab):
    """Return a list of 0/1 for one-hot encoding."""
    return [1 if v == value else 0 for v in vocab]


def _extract_quoted_tokens(message):
    """Return all tokens inside single quotes from an ANTLR message."""
    return TOKEN_PATTERN.findall(message)


class FeatureExtractor:
    """
    Transforms an ErrorRecord (or its dict form) into a flat
    feature vector suitable for scikit-learn or any ML library.

    Feature layout (all numeric):
      [0..2]   language one-hot          (3)
      [3..4]   error_type one-hot        (2)
      [5..10]  error_category one-hot    (6)
      [11]     line number (normalised)  (1)
      [12]     column number             (1)
      [13]     source_line length        (1)
      [14]     num quoted tokens in msg  (1)
      [15]     message length            (1)
      [16..27] keyword hint flags        (12)
      ─────────────────────────────────────
      Total: 28 features
    """

    FEATURE_DIM = 28

    def extract(self, error_record) -> list:
        """
        Accept either an ErrorRecord object or a dict (from to_dict()).
        Returns a list of 28 numeric features.
        """
        if hasattr(error_record, "to_dict"):
            d = error_record.to_dict()
        else:
            d = error_record  # assume dict

        language        = d.get("language", "C")
        error_type      = d.get("error_type", "SYNTAX")
        error_category  = d.get("error_category", "OTHER")
        line            = int(d.get("line", 1))
        column          = int(d.get("column", 0))
        message         = str(d.get("message", ""))
        source_line     = str(d.get("source_line", ""))

        features = []

        # one-hot: language
        features += _one_hot(language, LANGUAGES)

        # one-hot: error_type
        features += _one_hot(error_type, ERROR_TYPES)

        # one-hot: error_category
        features += _one_hot(error_category, ERROR_CATEGORIES)

        # numeric: line (cap at 1000 and normalise)
        features.append(min(line, 1000) / 1000.0)

        # numeric: column
        features.append(min(column, 200) / 200.0)

        # numeric: source line length
        features.append(min(len(source_line), 300) / 300.0)

        # numeric: number of quoted tokens in message
        quoted = _extract_quoted_tokens(message)
        features.append(min(len(quoted), 10) / 10.0)

        # numeric: message length
        features.append(min(len(message), 300) / 300.0)

        # keyword hint flags (12)
        msg_lower = message.lower() + source_line.lower()
        for kw in KEYWORD_HINTS:
            features.append(1.0 if kw in msg_lower else 0.0)

        assert len(features) == self.FEATURE_DIM, \
            f"Feature vector has {len(features)} elements, expected {self.FEATURE_DIM}"

        return features

    def extract_batch(self, error_records: list) -> list:
        """Extract features for a list of errors. Returns list of feature lists."""
        return [self.extract(e) for e in error_records]

    def feature_names(self) -> list:
        names = []
        for lang in LANGUAGES:
            names.append(f"lang_{lang}")
        for et in ERROR_TYPES:
            names.append(f"type_{et}")
        for ec in ERROR_CATEGORIES:
            names.append(f"cat_{ec}")
        names += ["line_norm", "col_norm", "src_len_norm",
                  "quoted_token_count", "msg_len_norm"]
        for kw in KEYWORD_HINTS:
            safe = re.sub(r"[^a-zA-Z0-9_]", "_", kw)
            names.append(f"hint_{safe}")
        return names


# ─────────────────────────────────────────────────────────────
# Quick test / demo
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from error_collector import ErrorRecord

    sample = ErrorRecord(
        error_type       = "SYNTAX",
        line             = 10,
        column           = 4,
        message          = "missing ';' at '}'",
        offending_symbol = "}",
        source_line      = "    int x = 5"
    )
    sample.language  = "C"
    sample.file_path = "test.c"

    fe = FeatureExtractor()
    vec = fe.extract(sample)

    print("Feature names:", fe.feature_names())
    print("Feature vector:", vec)
    print(f"Dimension: {len(vec)}")