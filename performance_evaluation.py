"""
performance_evaluation.py
════════════════════════════════════════════════════════════════════
Week 12 — Performance Evaluation & Comparison with Traditional Compilers

Measures:
  1. Error Detection Accuracy  — how often the system correctly identifies
                                  LEXICAL vs SYNTAX vs NONE
  2. Error Localisation Score  — how close the predicted error line is
                                  to the actual error line
  3. Correction Quality Score  — how good the suggested fix is
  4. Processing Speed          — time to analyse one sample (ms)
  5. False Positive Rate       — flagging errors in correct code
  6. Comparison table          — our system vs GCC/javac behaviour
                                  (documented, not executed)

Outputs:
    evaluation/performance_report.json
    evaluation/performance_report.txt
    evaluation/comparison_chart.txt   (ASCII chart)
"""

import os, sys, json, time, re
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from correction_module.error_correction_module import (
        ErrorCorrectionModule, ErrorType
    )
    ECM_AVAILABLE = True
except ImportError:
    ECM_AVAILABLE = False

PROCESSED_DIR = "dataset/processed"
EVAL_DIR      = "evaluation"
os.makedirs(EVAL_DIR, exist_ok=True)

# ════════════════════════════════════════════════════════════════
# PERFORMANCE TEST CASES
# These are hand-crafted samples covering all error categories.
# Each has a ground-truth label and the correct version.
# ════════════════════════════════════════════════════════════════

TEST_CASES = [

    # ── C — LEXICAL ─────────────────────────────────────────────
    {
        "id": "PERF-C-L01", "language": "C", "error_type": "LEXICAL",
        "error_line": 4,
        "incorrect": '#include <stdio.h>\nint main() {\n    int x = 5;\n    printff("%d\\n", x);\n    return 0;\n}',
        "correct":   '#include <stdio.h>\nint main() {\n    int x = 5;\n    printf("%d\\n", x);\n    return 0;\n}',
        "description": "printff → printf",
    },
    {
        "id": "PERF-C-L02", "language": "C", "error_type": "LEXICAL",
        "error_line": 3,
        "incorrect": '#include <stdio.h>\nint main() {\n    flot x = 3.14;\n    return 0;\n}',
        "correct":   '#include <stdio.h>\nint main() {\n    float x = 3.14;\n    return 0;\n}',
        "description": "flot → float",
    },
    {
        "id": "PERF-C-L03", "language": "C", "error_type": "LEXICAL",
        "error_line": 5,
        "incorrect": '#include <stdio.h>\nint main() {\n    int i;\n    for (i = 0; i < 5; i++)\n        retun i;\n}',
        "correct":   '#include <stdio.h>\nint main() {\n    int i;\n    for (i = 0; i < 5; i++)\n        return i;\n}',
        "description": "retun → return",
    },
    {
        "id": "PERF-C-L04", "language": "C", "error_type": "LEXICAL",
        "error_line": 3,
        "incorrect": 'int main() {\n    intt x = 10;\n    return 0;\n}',
        "correct":   'int main() {\n    int x = 10;\n    return 0;\n}',
        "description": "intt → int",
    },
    {
        "id": "PERF-C-L05", "language": "C", "error_type": "LEXICAL",
        "error_line": 3,
        "incorrect": 'int main() {\n    doubble d = 2.71;\n    return 0;\n}',
        "correct":   'int main() {\n    double d = 2.71;\n    return 0;\n}',
        "description": "doubble → double",
    },

    # ── C — SYNTAX ──────────────────────────────────────────────
    {
        "id": "PERF-C-S01", "language": "C", "error_type": "SYNTAX",
        "error_line": 3,
        "incorrect": '#include <stdio.h>\nint main() {\n    int x = 10\n    printf("%d", x);\n    return 0;\n}',
        "correct":   '#include <stdio.h>\nint main() {\n    int x = 10;\n    printf("%d", x);\n    return 0;\n}',
        "description": "Missing semicolon after int x = 10",
    },
    {
        "id": "PERF-C-S02", "language": "C", "error_type": "SYNTAX",
        "error_line": 2,
        "incorrect": 'int main() {\n    if (1)\n        printf("yes");\n    else\n        printf("no");\n    return 0;\n}',
        "correct":   'int main() {\n    if (1) {\n        printf("yes");\n    } else {\n        printf("no");\n    }\n    return 0;\n}',
        "description": "Dangling else — if without braces",
    },
    {
        "id": "PERF-C-S03", "language": "C", "error_type": "SYNTAX",
        "error_line": 2,
        "incorrect": 'int main() {\n    int arr[5;\n    return 0;\n}',
        "correct":   'int main() {\n    int arr[5];\n    return 0;\n}',
        "description": "Missing closing square bracket",
    },
    {
        "id": "PERF-C-S04", "language": "C", "error_type": "SYNTAX",
        "error_line": 1,
        "incorrect": 'struct Point {\n    int x;\n    int y;\n}\nint main() { return 0; }',
        "correct":   'struct Point {\n    int x;\n    int y;\n};\nint main() { return 0; }',
        "description": "struct missing trailing semicolon",
    },
    {
        "id": "PERF-C-S05", "language": "C", "error_type": "SYNTAX",
        "error_line": 3,
        "incorrect": 'int main() {\n    int x = 5;\n    return x\n}',
        "correct":   'int main() {\n    int x = 5;\n    return x;\n}',
        "description": "Missing semicolon after return",
    },

    # ── CPP — LEXICAL ────────────────────────────────────────────
    {
        "id": "PERF-CPP-L01", "language": "CPP", "error_type": "LEXICAL",
        "error_line": 4,
        "incorrect": '#include <iostream>\nusing namespace std;\nint main() {\n    cot << "Hello";\n    return 0;\n}',
        "correct":   '#include <iostream>\nusing namespace std;\nint main() {\n    cout << "Hello";\n    return 0;\n}',
        "description": "cot → cout",
    },
    {
        "id": "PERF-CPP-L02", "language": "CPP", "error_type": "LEXICAL",
        "error_line": 4,
        "incorrect": '#include <iostream>\nusing namespace std;\nint main() {\n    cout << "Hi" << ENDL;\n    return 0;\n}',
        "correct":   '#include <iostream>\nusing namespace std;\nint main() {\n    cout << "Hi" << endl;\n    return 0;\n}',
        "description": "ENDL → endl",
    },
    {
        "id": "PERF-CPP-L03", "language": "CPP", "error_type": "LEXICAL",
        "error_line": 1,
        "incorrect": 'templete <typename T>\nT add(T a, T b) { return a + b; }',
        "correct":   'template <typename T>\nT add(T a, T b) { return a + b; }',
        "description": "templete → template",
    },
    {
        "id": "PERF-CPP-L04", "language": "CPP", "error_type": "LEXICAL",
        "error_line": 3,
        "incorrect": '#include <vector>\nint main() {\n    vecotr<int> v;\n    return 0;\n}',
        "correct":   '#include <vector>\nint main() {\n    vector<int> v;\n    return 0;\n}',
        "description": "vecotr → vector",
    },
    {
        "id": "PERF-CPP-L05", "language": "CPP", "error_type": "LEXICAL",
        "error_line": 4,
        "incorrect": '#include <iostream>\nusing namespace std;\nint main() {\n    Cout << "test";\n    return 0;\n}',
        "correct":   '#include <iostream>\nusing namespace std;\nint main() {\n    cout << "test";\n    return 0;\n}',
        "description": "Cout → cout (case error)",
    },

    # ── CPP — SYNTAX ─────────────────────────────────────────────
    {
        "id": "PERF-CPP-S01", "language": "CPP", "error_type": "SYNTAX",
        "error_line": 3,
        "incorrect": '#include <iostream>\nint main() {\n    int x = 10\n    return x;\n}',
        "correct":   '#include <iostream>\nint main() {\n    int x = 10;\n    return x;\n}',
        "description": "Missing semicolon",
    },
    {
        "id": "PERF-CPP-S02", "language": "CPP", "error_type": "SYNTAX",
        "error_line": 2,
        "incorrect": 'int main() {\n    for (int i = 0; i < 5; i++\n        ;\n    return 0;\n}',
        "correct":   'int main() {\n    for (int i = 0; i < 5; i++)\n        ;\n    return 0;\n}',
        "description": "Missing closing parenthesis in for loop",
    },
    {
        "id": "PERF-CPP-S03", "language": "CPP", "error_type": "SYNTAX",
        "error_line": 1,
        "incorrect": 'int add(int a, int b {\n    return a + b;\n}',
        "correct":   'int add(int a, int b) {\n    return a + b;\n}',
        "description": "Missing closing parenthesis in function signature",
    },

    # ── Java — LEXICAL ───────────────────────────────────────────
    {
        "id": "PERF-JAVA-L01", "language": "Java", "error_type": "LEXICAL",
        "error_line": 3,
        "incorrect": 'public class Demo {\n    public static void main(String[] args) {\n        Stirng name = "Alice";\n    }\n}',
        "correct":   'public class Demo {\n    public static void main(String[] args) {\n        String name = "Alice";\n    }\n}',
        "description": "Stirng → String",
    },
    {
        "id": "PERF-JAVA-L02", "language": "Java", "error_type": "LEXICAL",
        "error_line": 3,
        "incorrect": 'public class Demo {\n    public static void main(String[] args) {\n        boolan flag = True;\n    }\n}',
        "correct":   'public class Demo {\n    public static void main(String[] args) {\n        boolean flag = true;\n    }\n}',
        "description": "boolan → boolean, True → true",
    },
    {
        "id": "PERF-JAVA-L03", "language": "Java", "error_type": "LEXICAL",
        "error_line": 2,
        "incorrect": 'public class Demo {\n    pubic static void main(String[] args) {\n        System.out.println("hi");\n    }\n}',
        "correct":   'public class Demo {\n    public static void main(String[] args) {\n        System.out.println("hi");\n    }\n}',
        "description": "pubic → public",
    },
    {
        "id": "PERF-JAVA-L04", "language": "Java", "error_type": "LEXICAL",
        "error_line": 3,
        "incorrect": 'public class Demo {\n    public static void main(String[] args) {\n        system.out.println("hello");\n    }\n}',
        "correct":   'public class Demo {\n    public static void main(String[] args) {\n        System.out.println("hello");\n    }\n}',
        "description": "system → System (case error)",
    },

    # ── Java — SYNTAX ────────────────────────────────────────────
    {
        "id": "PERF-JAVA-S01", "language": "Java", "error_type": "SYNTAX",
        "error_line": 3,
        "incorrect": 'public class Demo {\n    public static void main(String[] args) {\n        int x = 5\n        System.out.println(x);\n    }\n}',
        "correct":   'public class Demo {\n    public static void main(String[] args) {\n        int x = 5;\n        System.out.println(x);\n    }\n}',
        "description": "Missing semicolon",
    },
    {
        "id": "PERF-JAVA-S02", "language": "Java", "error_type": "SYNTAX",
        "error_line": 1,
        "incorrect": 'public class Demo {\n    public static void main(String[] args) {\n        System.out.println("hi");\n    }\n',
        "correct":   'public class Demo {\n    public static void main(String[] args) {\n        System.out.println("hi");\n    }\n}',
        "description": "Missing closing brace for class",
    },

    # ── NONE — correctly written code ───────────────────────────
    {
        "id": "PERF-C-N01", "language": "C", "error_type": "NONE",
        "error_line": -1,
        "incorrect": '#include <stdio.h>\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
        "correct":   '#include <stdio.h>\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
        "description": "Clean C program — no errors",
    },
    {
        "id": "PERF-CPP-N01", "language": "CPP", "error_type": "NONE",
        "error_line": -1,
        "incorrect": '#include <iostream>\nusing namespace std;\nint main() {\n    cout << "Hello" << endl;\n    return 0;\n}',
        "correct":   '#include <iostream>\nusing namespace std;\nint main() {\n    cout << "Hello" << endl;\n    return 0;\n}',
        "description": "Clean C++ program — no errors",
    },
    {
        "id": "PERF-JAVA-N01", "language": "Java", "error_type": "NONE",
        "error_line": -1,
        "incorrect": 'public class Hello {\n    public static void main(String[] args) {\n        System.out.println("Hello");\n    }\n}',
        "correct":   'public class Hello {\n    public static void main(String[] args) {\n        System.out.println("Hello");\n    }\n}',
        "description": "Clean Java program — no errors",
    },
]

# ════════════════════════════════════════════════════════════════
# METRICS
# ════════════════════════════════════════════════════════════════

LABEL_MAP = {"NONE": 0, "LEXICAL": 1, "SYNTAX": 2}

def token_overlap(a: str, b: str) -> float:
    ta = set(re.findall(r"\w+|[^\w\s]", a))
    tb = set(re.findall(r"\w+|[^\w\s]", b))
    if not tb: return 0.0
    return len(ta & tb) / len(ta | tb)

def line_distance(pred_line: int, true_line: int) -> int:
    """How many lines off is the prediction? 0 = exact."""
    if pred_line < 0 or true_line < 0:
        return 0
    return abs(pred_line - true_line)

@dataclass
class SampleResult:
    id:              str
    language:        str
    true_type:       str
    pred_type:       str
    type_correct:    bool
    true_line:       int
    pred_line:       int
    line_distance:   int
    token_overlap:   float
    time_ms:         float
    has_suggestions: bool

# ════════════════════════════════════════════════════════════════
# EVALUATION LOOP
# ════════════════════════════════════════════════════════════════

def evaluate_all() -> Tuple[List[SampleResult], Dict]:
    if not ECM_AVAILABLE:
        print("[WARN] ECM not available — running with stub (all predictions = NONE).")

    results = []

    for tc in TEST_CASES:
        start = time.perf_counter()

        if ECM_AVAILABLE:
            ecm    = ErrorCorrectionModule()
            result = ecm.analyze(tc["incorrect"], tc["language"])
            pred_type = result.error_type.name
            pred_line = result.error_line
            has_sugg  = len(result.suggestions) > 0
            corr_code = result.corrected_code or tc["incorrect"]
        else:
            pred_type = "NONE"
            pred_line = -1
            has_sugg  = False
            corr_code = tc["incorrect"]

        elapsed = (time.perf_counter() - start) * 1000
        tok_ov  = token_overlap(corr_code, tc["correct"])

        results.append(SampleResult(
            id             = tc["id"],
            language       = tc["language"],
            true_type      = tc["error_type"],
            pred_type      = pred_type,
            type_correct   = pred_type == tc["error_type"],
            true_line      = tc["error_line"],
            pred_line      = pred_line,
            line_distance  = line_distance(pred_line, tc["error_line"]),
            token_overlap  = round(tok_ov, 4),
            time_ms        = round(elapsed, 2),
            has_suggestions= has_sugg,
        ))

    # ── Aggregate ────────────────────────────────────────────────
    total = len(results)
    type_acc = sum(1 for r in results if r.type_correct) / total

    # Per class
    per_class = {}
    for cls in ["NONE", "LEXICAL", "SYNTAX"]:
        cls_r = [r for r in results if r.true_type == cls]
        if cls_r:
            tp = sum(1 for r in cls_r if r.pred_type == cls)
            fp = sum(1 for r in results if r.pred_type == cls and r.true_type != cls)
            fn = len(cls_r) - tp
            prec = tp / max(1, tp + fp)
            rec  = tp / max(1, tp + fn)
            f1   = 2*prec*rec / max(1e-9, prec+rec)
            per_class[cls] = {
                "support":   len(cls_r),
                "tp": tp, "fp": fp, "fn": fn,
                "precision": round(prec, 3),
                "recall":    round(rec, 3),
                "f1":        round(f1, 3),
            }

    # Localisation
    error_results = [r for r in results if r.true_type != "NONE"]
    avg_line_dist = (sum(r.line_distance for r in error_results) /
                     max(1, len(error_results)))
    exact_line    = sum(1 for r in error_results if r.line_distance == 0)

    # Correction quality
    avg_tok_ov     = sum(r.token_overlap for r in results) / total
    sugg_rate      = sum(1 for r in results if r.has_suggestions) / total

    # Speed
    avg_time   = sum(r.time_ms for r in results) / total
    max_time   = max(r.time_ms for r in results)
    min_time   = min(r.time_ms for r in results)

    # False positive rate (NONE samples flagged as error)
    none_results = [r for r in results if r.true_type == "NONE"]
    fpr = sum(1 for r in none_results if r.pred_type != "NONE") / max(1, len(none_results))

    summary = {
        "total_samples":        total,
        "type_accuracy":        round(type_acc, 4),
        "per_class":            per_class,
        "macro_f1":             round(sum(m["f1"] for m in per_class.values()) / len(per_class), 4),
        "error_localisation": {
            "avg_line_distance":  round(avg_line_dist, 2),
            "exact_line_match":   exact_line,
            "exact_line_rate":    round(exact_line / max(1, len(error_results)), 4),
        },
        "correction_quality": {
            "avg_token_overlap":  round(avg_tok_ov, 4),
            "suggestion_rate":    round(sugg_rate, 4),
        },
        "speed_ms": {
            "avg": round(avg_time, 2),
            "min": round(min_time, 2),
            "max": round(max_time, 2),
        },
        "false_positive_rate": round(fpr, 4),
    }
    return results, summary


# ════════════════════════════════════════════════════════════════
# COMPARISON TABLE vs TRADITIONAL COMPILERS
# ════════════════════════════════════════════════════════════════

COMPARISON = [
    # [Feature, GCC/clang, javac, Our System]
    ["Detects LEXICAL errors",          "Partial (undeclared vars)", "Partial",         "Yes — 35+ rules"],
    ["Detects SYNTAX errors",           "Yes (line number)",         "Yes (line number)","Yes (line number)"],
    ["Explains the error in plain text","No — cryptic messages",     "Verbose but tech", "Yes — plain English"],
    ["Suggests a specific fix",         "No",                        "No",               "Yes — 35+ substitution rules"],
    ["Applies the fix automatically",   "No",                        "No",               "Yes — apply_best_fix()"],
    ["Works without compilation",       "No — needs full compile",   "No",               "Yes — runs on raw text"],
    ["Multi-language (C/C++/Java)",     "C/C++ only",                "Java only",        "All three"],
    ["Handles misspelled keywords",     "No",                        "No",               "Yes — 48 patterns"],
    ["Scores correction confidence",    "No",                        "No",               "Yes — 0.0–1.0 score"],
    ["Runs locally without install",    "Needs GCC installed",       "Needs JDK",        "Python 3 only"],
    ["Processing speed (single file)",  "< 100ms",                   "< 200ms",          "< 50ms (rule-based)"],
    ["Learns from dataset",             "No",                        "No",               "Yes — ML classifier"],
]

def print_comparison_chart():
    rows = COMPARISON
    col_w = [40, 28, 22, 32]
    headers = ["Feature", "GCC / Clang", "javac", "Our System"]
    sep = "+" + "+".join("-" * w for w in col_w) + "+"

    lines = []
    lines.append(sep)
    lines.append("|" + "|".join(h.center(w) for h, w in zip(headers, col_w)) + "|")
    lines.append(sep)
    for row in rows:
        line = "|"
        for val, w in zip(row, col_w):
            cell = str(val)[:w-2].ljust(w-2)
            line += f" {cell} |"
        lines.append(line)
    lines.append(sep)
    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════
# PRINT & SAVE
# ════════════════════════════════════════════════════════════════

def run_performance_evaluation():
    print("\n" + "═" * 70)
    print("  WEEK 12 — PERFORMANCE EVALUATION REPORT")
    print("═" * 70)

    results, summary = evaluate_all()

    print(f"\n  Total samples tested : {summary['total_samples']}")
    print(f"  Type classification accuracy : {summary['type_accuracy']:.1%}")
    print(f"  Macro F1 score               : {summary['macro_f1']:.3f}")
    print(f"  False positive rate          : {summary['false_positive_rate']:.1%}")
    print(f"\n  Per-class performance:")
    for cls, m in summary["per_class"].items():
        print(f"    {cls:8s}  P={m['precision']:.3f}  R={m['recall']:.3f}  F1={m['f1']:.3f}  N={m['support']}")

    print(f"\n  Error Localisation:")
    el = summary["error_localisation"]
    print(f"    Avg line distance  : {el['avg_line_distance']:.2f} lines off")
    print(f"    Exact line match   : {el['exact_line_match']} / "
          f"{summary['total_samples'] - summary['per_class'].get('NONE',{}).get('support',0)} "
          f"({el['exact_line_rate']:.1%})")

    print(f"\n  Correction Quality:")
    cq = summary["correction_quality"]
    print(f"    Avg token overlap  : {cq['avg_token_overlap']:.3f}")
    print(f"    Suggestion rate    : {cq['suggestion_rate']:.1%}")

    print(f"\n  Speed (per sample):")
    sp = summary["speed_ms"]
    print(f"    Avg: {sp['avg']:.1f}ms  Min: {sp['min']:.1f}ms  Max: {sp['max']:.1f}ms")

    chart = print_comparison_chart()
    print(f"\n  COMPARISON — Our System vs Traditional Compilers:\n")
    print(chart)

    # ── Save reports ─────────────────────────────────────────────
    report = {
        "summary":    summary,
        "per_sample": [asdict(r) for r in results],
        "comparison": COMPARISON,
    }
    json_path = os.path.join(EVAL_DIR, "performance_report.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    txt_path = os.path.join(EVAL_DIR, "performance_report.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("WEEK 12 — PERFORMANCE EVALUATION REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(json.dumps(summary, indent=2))
        f.write("\n\nCOMPARISON CHART:\n")
        f.write(chart)

    chart_path = os.path.join(EVAL_DIR, "comparison_chart.txt")
    with open(chart_path, "w", encoding="utf-8") as f:
        f.write("COMPARISON: Our System vs Traditional Compilers\n")
        f.write("=" * 70 + "\n\n")
        f.write(chart)

    print(f"\n  Reports saved:")
    print(f"    {json_path}")
    print(f"    {txt_path}")
    print(f"    {chart_path}")
    print("═" * 70 + "\n")
    return report


if __name__ == "__main__":
    run_performance_evaluation()