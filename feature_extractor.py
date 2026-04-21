import re

LANGUAGES        = ["C", "CPP", "Java"]
ERROR_TYPES      = ["LEXICAL", "SYNTAX", "NONE"]
ERROR_CATEGORIES = [
    "MISSING_TOKEN", "EXTRANEOUS_TOKEN", "MISMATCHED_TOKEN",
    "NO_VIABLE_ALT", "UNRECOGNIZED_TOKEN", "OTHER",
]
KEYWORD_HINTS = [
    "semicolon", ";", "{", "}", "(", ")",
    "identifier", "return", "int", "void",
    "class", "if", "while", "for", "string",
]

TOKEN_PATTERN = re.compile(r"'([^']+)'")


def _one_hot(value, vocab):
    return [1 if v == value else 0 for v in vocab]


def _quoted_tokens(message):
    return TOKEN_PATTERN.findall(message)


class FeatureExtractor:
    FEATURE_DIM = 37

    def extract(self, error_record) -> list:
        if hasattr(error_record, "to_dict"):
            d = error_record.to_dict()
        else:
            d = error_record

        language       = d.get("language",       "C")
        error_type     = d.get("error_type",     "SYNTAX")
        error_category = d.get("error_category", "OTHER")
        line           = int(d.get("line",   1))
        column         = int(d.get("column", 0))
        message        = str(d.get("message", ""))
        source_line    = str(d.get("source_line", ""))

        features = []

        features += _one_hot(language, LANGUAGES)            # 3
        features += _one_hot(error_type, ERROR_TYPES)        # 3
        features += _one_hot(error_category, ERROR_CATEGORIES)  # 6
        features.append(min(line,   1000) / 1000.0)          # 1
        features.append(min(column,  200) / 200.0)           # 1
        features.append(min(len(source_line), 300) / 300.0)  # 1
        features.append(min(len(_quoted_tokens(message)), 10) / 10.0)  # 1
        features.append(min(len(message), 300) / 300.0)      # 1
        features.append(1.0 if source_line.count("{") != source_line.count("}") else 0.0)  # 1
        features.append(1.0 if source_line.count("(") != source_line.count(")") else 0.0)  # 1
        features.append(1.0 if ";" in source_line else 0.0)  # 1
        features.append(1.0 if "main" in source_line.lower() else 0.0)  # 1

        combined = message.lower() + " " + source_line.lower()
        for kw in KEYWORD_HINTS:
            features.append(1.0 if kw in combined else 0.0)  # 15

        lang_idx = LANGUAGES.index(language) if language in LANGUAGES else 0
        features.append(lang_idx / max(len(LANGUAGES) - 1, 1))  # 1

        # total = 3+3+6+1+1+1+1+1+1+1+1+1+15+1 = 37
        if len(features) < self.FEATURE_DIM:
            features += [0.0] * (self.FEATURE_DIM - len(features))
        return features[:self.FEATURE_DIM]

    def extract_batch(self, records: list) -> list:
        return [self.extract(r) for r in records]

    def feature_names(self) -> list:
        names  = [f"lang_{l}"  for l in LANGUAGES]
        names += [f"type_{t}"  for t in ERROR_TYPES]
        names += [f"cat_{c}"   for c in ERROR_CATEGORIES]
        names += [
            "line_norm", "col_norm", "src_len_norm",
            "quoted_token_count", "msg_len_norm",
            "brace_balance_flag", "paren_balance_flag",
            "has_semicolon", "has_main",
        ]
        hint_names = []
        for kw in KEYWORD_HINTS:
            safe = kw
            safe = safe.replace(";", "semi")
            safe = safe.replace("{", "lbrace")
            safe = safe.replace("}", "rbrace")
            safe = safe.replace("(", "lparen")
            safe = safe.replace(")", "rparen")
            safe = re.sub(r"[^a-zA-Z0-9_]", "_", safe)
            hint_names.append(f"hint_{safe}")
        names += hint_names
        names += ["language_label_norm"]
        if len(names) < self.FEATURE_DIM:
            names += [f"extra_{i}" for i in range(self.FEATURE_DIM - len(names))]
        return names[:self.FEATURE_DIM]


if __name__ == "__main__":
    fe = FeatureExtractor()
    sample = {
        "language"       : "Java",
        "error_type"     : "SYNTAX",
        "error_category" : "MISSING_TOKEN",
        "line"           : 5,
        "column"         : 12,
        "message"        : "missing ';' at '}'",
        "source_line"    : "    int x = 10",
    }
    vec = fe.extract(sample)
    print(f"Feature dim : {len(vec)}  expected={fe.FEATURE_DIM}")
    print("PASS" if len(vec) == 37 else "FAIL")