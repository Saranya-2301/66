"""
system_validation.py
════════════════════════════════════════════════════════════════════
Week 13 — System Validation
Tests the full pipeline with real-world-style programs.

Validates:
  1. Correctness  — does the system find the right error?
  2. Reliability  — does it produce consistent results on same input?
  3. Edge cases   — empty functions, single-line programs, huge classes
  4. End-to-end   — run the entire pipeline on a real program file

Outputs:
    evaluation/validation_results.json
    evaluation/validation_results.txt
    evaluation/test_cases.json          ← all test cases documented
"""

import os, sys, json, re, time
from dataclasses import dataclass, asdict
from typing      import List, Dict, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from correction_module.error_correction_module import (
        ErrorCorrectionModule, ErrorType
    )
    ECM_AVAILABLE = True
except ImportError:
    ECM_AVAILABLE = False

EVAL_DIR = "evaluation"
os.makedirs(EVAL_DIR, exist_ok=True)

# ════════════════════════════════════════════════════════════════
# VALIDATION TEST CASES — real-world-style programs
# ════════════════════════════════════════════════════════════════

TEST_CASES = [

    # ══════════════ C — Real-World Programs ══════════════════════

    {
        "id": "VAL-C-01",
        "language": "C",
        "description": "Fibonacci function — missing semicolon",
        "category": "real-world",
        "incorrect": """\
#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) return n
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    for (int i = 0; i < 10; i++) {
        printf("%d ", fibonacci(i));
    }
    return 0;
}""",
        "correct": """\
#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    for (int i = 0; i < 10; i++) {
        printf("%d ", fibonacci(i));
    }
    return 0;
}""",
        "expected_error_type": "SYNTAX",
        "expected_error_line": 4,
        "expected_fix_contains": "return n;",
    },

    {
        "id": "VAL-C-02",
        "language": "C",
        "description": "Bubble sort — misspelled printf",
        "category": "real-world",
        "incorrect": """\
#include <stdio.h>

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main() {
    int arr[] = {64, 34, 25, 12, 22};
    int n = 5;
    bubbleSort(arr, n);
    for (int i = 0; i < n; i++)
        prinff("%d ", arr[i]);
    return 0;
}""",
        "correct": """\
#include <stdio.h>

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main() {
    int arr[] = {64, 34, 25, 12, 22};
    int n = 5;
    bubbleSort(arr, n);
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    return 0;
}""",
        "expected_error_type": "LEXICAL",
        "expected_error_line": 19,
        "expected_fix_contains": "printf",
    },

    {
        "id": "VAL-C-03",
        "language": "C",
        "description": "Linked list node — struct missing semicolon",
        "category": "real-world",
        "incorrect": """\
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
}

int main() {
    struct Node* head = NULL;
    return 0;
}""",
        "correct": """\
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

int main() {
    struct Node* head = NULL;
    return 0;
}""",
        "expected_error_type": "SYNTAX",
        "expected_error_line": 7,
        "expected_fix_contains": "};",
    },

    {
        "id": "VAL-C-04",
        "language": "C",
        "description": "Temperature converter — wrong return keyword",
        "category": "real-world",
        "incorrect": """\
#include <stdio.h>

float celsiusToFahrenheit(float c) {
    retun (c * 9 / 5) + 32;
}

int main() {
    printf("%.2f\\n", celsiusToFahrenheit(100));
    return 0;
}""",
        "correct": """\
#include <stdio.h>

float celsiusToFahrenheit(float c) {
    return (c * 9 / 5) + 32;
}

int main() {
    printf("%.2f\\n", celsiusToFahrenheit(100));
    return 0;
}""",
        "expected_error_type": "LEXICAL",
        "expected_error_line": 4,
        "expected_fix_contains": "return",
    },

    # ══════════════ C++ — Real-World Programs ════════════════════

    {
        "id": "VAL-CPP-01",
        "language": "CPP",
        "description": "Stack class — missing closing brace",
        "category": "real-world",
        "incorrect": """\
#include <iostream>
#include <vector>
using namespace std;

class Stack {
private:
    vector<int> data;
public:
    void push(int val) { data.push_back(val); }
    void pop() { if (!data.empty()) data.pop_back(); }
    int top() { return data.back(); }
    bool empty() { return data.empty(); }
;

int main() {
    Stack s;
    s.push(1);
    s.push(2);
    cout << s.top() << endl;
    return 0;
}""",
        "correct": """\
#include <iostream>
#include <vector>
using namespace std;

class Stack {
private:
    vector<int> data;
public:
    void push(int val) { data.push_back(val); }
    void pop() { if (!data.empty()) data.pop_back(); }
    int top() { return data.back(); }
    bool empty() { return data.empty(); }
};

int main() {
    Stack s;
    s.push(1);
    s.push(2);
    cout << s.top() << endl;
    return 0;
}""",
        "expected_error_type": "SYNTAX",
        "expected_error_line": 12,
        "expected_fix_contains": "};",
    },

    {
        "id": "VAL-CPP-02",
        "language": "CPP",
        "description": "Template max function — misspelled template",
        "category": "real-world",
        "incorrect": """\
#include <iostream>
using namespace std;

templete <typename T>
T maxVal(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    cout << maxVal(3, 7) << endl;
    cout << maxVal(3.14, 2.71) << endl;
    return 0;
}""",
        "correct": """\
#include <iostream>
using namespace std;

template <typename T>
T maxVal(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    cout << maxVal(3, 7) << endl;
    cout << maxVal(3.14, 2.71) << endl;
    return 0;
}""",
        "expected_error_type": "LEXICAL",
        "expected_error_line": 4,
        "expected_fix_contains": "template",
    },

    {
        "id": "VAL-CPP-03",
        "language": "CPP",
        "description": "Calculator — cout misspelling",
        "category": "real-world",
        "incorrect": """\
#include <iostream>
using namespace std;

int main() {
    int a = 10, b = 5;
    cot << "Sum: " << a + b << endl;
    cot << "Diff: " << a - b << endl;
    cot << "Product: " << a * b << ENDL;
    return 0;
}""",
        "correct": """\
#include <iostream>
using namespace std;

int main() {
    int a = 10, b = 5;
    cout << "Sum: " << a + b << endl;
    cout << "Diff: " << a - b << endl;
    cout << "Product: " << a * b << endl;
    return 0;
}""",
        "expected_error_type": "LEXICAL",
        "expected_error_line": 6,
        "expected_fix_contains": "cout",
    },

    # ══════════════ Java — Real-World Programs ═══════════════════

    {
        "id": "VAL-JAVA-01",
        "language": "Java",
        "description": "BankAccount class — misspelled String",
        "category": "real-world",
        "incorrect": """\
public class BankAccount {
    private Stirng owner;
    private double balance;

    public BankAccount(String owner, double initialBalance) {
        this.owner   = owner;
        this.balance = initialBalance;
    }

    public void deposit(double amount) {
        balance += amount;
    }

    public void withdraw(double amount) {
        if (amount <= balance) balance -= amount;
    }

    public static void main(String[] args) {
        BankAccount acc = new BankAccount("Alice", 1000.0);
        acc.deposit(500);
        System.out.println(acc.balance);
    }
}""",
        "correct": """\
public class BankAccount {
    private String owner;
    private double balance;

    public BankAccount(String owner, double initialBalance) {
        this.owner   = owner;
        this.balance = initialBalance;
    }

    public void deposit(double amount) {
        balance += amount;
    }

    public void withdraw(double amount) {
        if (amount <= balance) balance -= amount;
    }

    public static void main(String[] args) {
        BankAccount acc = new BankAccount("Alice", 1000.0);
        acc.deposit(500);
        System.out.println(acc.balance);
    }
}""",
        "expected_error_type": "LEXICAL",
        "expected_error_line": 2,
        "expected_fix_contains": "String",
    },

    {
        "id": "VAL-JAVA-02",
        "language": "Java",
        "description": "Grade calculator — missing semicolon",
        "category": "real-world",
        "incorrect": """\
public class GradeCalculator {
    public static String getGrade(int score) {
        if (score >= 90)      return "A";
        else if (score >= 80) return "B";
        else if (score >= 70) return "C"
        else                  return "F";
    }

    public static void main(String[] args) {
        System.out.println(getGrade(85));
        System.out.println(getGrade(72));
    }
}""",
        "correct": """\
public class GradeCalculator {
    public static String getGrade(int score) {
        if (score >= 90)      return "A";
        else if (score >= 80) return "B";
        else if (score >= 70) return "C";
        else                  return "F";
    }

    public static void main(String[] args) {
        System.out.println(getGrade(85));
        System.out.println(getGrade(72));
    }
}""",
        "expected_error_type": "SYNTAX",
        "expected_error_line": 5,
        "expected_fix_contains": '"C";',
    },

    {
        "id": "VAL-JAVA-03",
        "language": "Java",
        "description": "Student record — boolean misspelling",
        "category": "real-world",
        "incorrect": """\
public class Student {
    private String name;
    private int    age;
    private boolan enrolled;

    public Student(String name, int age, boolean enrolled) {
        this.name     = name;
        this.age      = age;
        this.enrolled = enrolled;
    }

    public static void main(String[] args) {
        Student s = new Student("Bob", 20, True);
        System.out.println(s.name + " enrolled: " + s.enrolled);
    }
}""",
        "correct": """\
public class Student {
    private String name;
    private int    age;
    private boolean enrolled;

    public Student(String name, int age, boolean enrolled) {
        this.name     = name;
        this.age      = age;
        this.enrolled = enrolled;
    }

    public static void main(String[] args) {
        Student s = new Student("Bob", 20, true);
        System.out.println(s.name + " enrolled: " + s.enrolled);
    }
}""",
        "expected_error_type": "LEXICAL",
        "expected_error_line": 4,
        "expected_fix_contains": "boolean",
    },

    # ══════════════ EDGE CASES ════════════════════════════════════

    {
        "id": "VAL-EDGE-01",
        "language": "C",
        "description": "Single-line program — no error",
        "category": "edge-case",
        "incorrect": "int main() { return 0; }",
        "correct":   "int main() { return 0; }",
        "expected_error_type": "NONE",
        "expected_error_line": -1,
        "expected_fix_contains": None,
    },
    {
        "id": "VAL-EDGE-02",
        "language": "CPP",
        "description": "Empty function body — no error",
        "category": "edge-case",
        "incorrect": "void doNothing() {}\nint main() { doNothing(); return 0; }",
        "correct":   "void doNothing() {}\nint main() { doNothing(); return 0; }",
        "expected_error_type": "NONE",
        "expected_error_line": -1,
        "expected_fix_contains": None,
    },
    {
        "id": "VAL-EDGE-03",
        "language": "Java",
        "description": "Import statement only — no body error",
        "category": "edge-case",
        "incorrect": "improt java.util.List;\npublic class X { }",
        "correct":   "import java.util.List;\npublic class X { }",
        "expected_error_type": "LEXICAL",
        "expected_error_line": 1,
        "expected_fix_contains": "import",
    },
    {
        "id": "VAL-EDGE-04",
        "language": "C",
        "description": "Comment-only file",
        "category": "edge-case",
        "incorrect": "// This is just a comment\n/* Another comment */",
        "correct":   "// This is just a comment\n/* Another comment */",
        "expected_error_type": "NONE",
        "expected_error_line": -1,
        "expected_fix_contains": None,
    },
    {
        "id": "VAL-EDGE-05",
        "language": "C",
        "description": "Multiple errors on different lines",
        "category": "edge-case",
        "incorrect": "#include <stdio.h>\nint main() {\n    intt x = 5\n    printff(\"%d\", x)\n    retun 0;\n}",
        "correct":   "#include <stdio.h>\nint main() {\n    int x = 5;\n    printf(\"%d\", x);\n    return 0;\n}",
        "expected_error_type": "LEXICAL",   # first error found
        "expected_error_line": 3,
        "expected_fix_contains": "int",
    },
    {
        "id": "VAL-EDGE-06",
        "language": "C",
        "description": "Consistency check — same input twice should give same output",
        "category": "reliability",
        "incorrect": "int main() {\n    flot x = 1.0;\n    return 0;\n}",
        "correct":   "int main() {\n    float x = 1.0;\n    return 0;\n}",
        "expected_error_type": "LEXICAL",
        "expected_error_line": 2,
        "expected_fix_contains": "float",
    },
]


# ════════════════════════════════════════════════════════════════
# VALIDATION RUNNER
# ════════════════════════════════════════════════════════════════

@dataclass
class ValidationResult:
    id:                    str
    language:              str
    description:           str
    category:              str
    type_correct:          bool
    line_correct:          bool
    fix_correct:           bool
    predicted_type:        str
    predicted_line:        int
    predicted_fix_snippet: str
    consistency_pass:      bool
    time_ms:               float
    overall_pass:          bool

def run_validation():
    print("\n" + "═" * 70)
    print("  WEEK 13 — SYSTEM VALIDATION REPORT")
    print("═" * 70)

    if not ECM_AVAILABLE:
        print("  [WARN] ECM not importable — running structural tests only.\n")

    val_results: List[ValidationResult] = []

    for tc in TEST_CASES:
        start = time.perf_counter()

        # Run twice to check consistency (reliability test)
        outputs = []
        for _ in range(2 if tc["category"] == "reliability" else 1):
            if ECM_AVAILABLE:
                ecm    = ErrorCorrectionModule()
                result = ecm.analyze(tc["incorrect"], tc["language"])
                pred_type = result.error_type.name
                pred_line = result.error_line
                fix_code  = result.corrected_code or tc["incorrect"]
                best_sug  = result.best_suggestion()
                fix_snip  = best_sug.corrected_line if best_sug else ""
            else:
                pred_type = "NONE"
                pred_line = -1
                fix_code  = tc["incorrect"]
                fix_snip  = ""
            outputs.append((pred_type, pred_line, fix_snip))

        elapsed = (time.perf_counter() - start) * 1000

        pred_type, pred_line, fix_snip = outputs[0]

        type_ok = (pred_type == tc["expected_error_type"])
        line_ok = (
            tc["expected_error_line"] == -1 or
            abs(pred_line - tc["expected_error_line"]) <= 1
        )
        fix_ok  = (
            tc["expected_fix_contains"] is None or
            (tc["expected_fix_contains"] in fix_snip or
             tc["expected_fix_contains"] in fix_code)
        )

        # Consistency: both runs gave same type & line
        consistent = (len(outputs) < 2 or outputs[0][:2] == outputs[1][:2])

        overall = type_ok and line_ok and (fix_ok or tc["expected_fix_contains"] is None)

        val_results.append(ValidationResult(
            id                    = tc["id"],
            language              = tc["language"],
            description           = tc["description"],
            category              = tc["category"],
            type_correct          = type_ok,
            line_correct          = line_ok,
            fix_correct           = fix_ok,
            predicted_type        = pred_type,
            predicted_line        = pred_line,
            predicted_fix_snippet = fix_snip[:80],
            consistency_pass      = consistent,
            time_ms               = round(elapsed, 2),
            overall_pass          = overall,
        ))

    # ── Print results ─────────────────────────────────────────────
    passed  = sum(1 for r in val_results if r.overall_pass)
    total   = len(val_results)
    by_cat  = {}
    for r in val_results:
        by_cat.setdefault(r.category, {"pass": 0, "total": 0})
        by_cat[r.category]["total"] += 1
        if r.overall_pass:
            by_cat[r.category]["pass"] += 1

    by_lang = {}
    for r in val_results:
        by_lang.setdefault(r.language, {"pass": 0, "total": 0})
        by_lang[r.language]["total"] += 1
        if r.overall_pass:
            by_lang[r.language]["pass"] += 1

    print(f"\n  Total test cases : {total}")
    print(f"  Passed           : {passed} ({100*passed//total}%)")

    print(f"\n  By Category:")
    for cat, m in by_cat.items():
        bar = "█" * m["pass"] + "░" * (m["total"] - m["pass"])
        print(f"    {cat:15s} {m['pass']}/{m['total']}  {bar}")

    print(f"\n  By Language:")
    for lang, m in by_lang.items():
        bar = "█" * m["pass"] + "░" * (m["total"] - m["pass"])
        print(f"    {lang:8s} {m['pass']}/{m['total']}  {bar}")

    print(f"\n  Detailed Results:")
    print(f"  {'ID':18s} {'Type':6s} {'Line':5s} {'Fix':5s} {'Cons':5s} {'ms':6s}  Status")
    print(f"  {'-'*65}")
    for r in val_results:
        t  = "✓" if r.type_correct  else "✗"
        l  = "✓" if r.line_correct  else "✗"
        f  = "✓" if r.fix_correct   else "✗"
        c  = "✓" if r.consistency_pass else "✗"
        st = "PASS" if r.overall_pass else "FAIL"
        print(f"  {r.id:18s}  {t}     {l}     {f}     {c}   {r.time_ms:5.1f}  [{st}] {r.description[:35]}")

    # ── Save ──────────────────────────────────────────────────────
    report = {
        "summary": {
            "total":    total,
            "passed":   passed,
            "pass_rate":round(passed / total, 4),
            "by_category": by_cat,
            "by_language": by_lang,
        },
        "results": [asdict(r) for r in val_results],
    }
    json_path = os.path.join(EVAL_DIR, "validation_results.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    # Save test cases for documentation
    tc_path = os.path.join(EVAL_DIR, "test_cases.json")
    with open(tc_path, "w", encoding="utf-8") as f:
        json.dump(TEST_CASES, f, indent=2, ensure_ascii=False)

    txt_path = os.path.join(EVAL_DIR, "validation_results.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("WEEK 13 — SYSTEM VALIDATION RESULTS\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total: {total}  Passed: {passed}  Rate: {100*passed//total}%\n\n")
        for r in val_results:
            st = "PASS" if r.overall_pass else "FAIL"
            f.write(f"[{st}] {r.id} — {r.description}\n")
            f.write(f"  Type: expected={TEST_CASES[[t['id'] for t in TEST_CASES].index(r.id)]['expected_error_type']} "
                    f"got={r.predicted_type} correct={r.type_correct}\n")
            f.write(f"  Line: got={r.predicted_line} correct={r.line_correct}\n")
            f.write(f"  Fix:  snippet='{r.predicted_fix_snippet[:60]}' correct={r.fix_correct}\n\n")

    print(f"\n  Saved:")
    print(f"    {json_path}")
    print(f"    {tc_path}")
    print(f"    {txt_path}")
    print("═" * 70 + "\n")
    return report


if __name__ == "__main__":
    run_validation()