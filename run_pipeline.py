
import os, sys, json, time, argparse, subprocess
from pathlib import Path

# ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
# ────────────────────────────────────────────────────────────────

STAGES = {
    1: ("Dataset Generation",   "dataset_creator.py"),
    2: ("Preprocessing",        "preprocess.py"),
    3: ("Data Augmentation",    "augment.py"),
    4: ("Feature Extraction",   "feature_extraction.py"),
    5: ("Model Training",       "models/transformer_model.py"),
    6: ("Evaluation",           "evaluation/evaluate.py test"),
    7: ("Correction Validation","error_correction/validate_corrections.py test"),
}


def run_stage(stage_num: int, stage_name: str, script_path: str) -> bool:
    full_path = BASE_DIR / script_path.split()[0]
    args_str  = " ".join(script_path.split()[1:])

    print(f"\n{'═'*65}")
    print(f"  STAGE {stage_num}: {stage_name}")
    print(f"  Script : {script_path}")
    print(f"{'═'*65}")

    if not full_path.exists():
        print(f"  [SKIP] Script not found: {full_path}")
        return False

    cmd = [sys.executable, str(full_path)] + (args_str.split() if args_str else [])
    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        elapsed = time.time() - start
        if result.returncode == 0:
            print(f"\n  Stage {stage_num} completed in {elapsed:.1f}s")
            return True
        else:
            print(f"\n  Stage {stage_num} failed (exit {result.returncode})")
            return False
    except Exception as e:
        print(f"\n  Stage {stage_num} error: {e}")
        return False


def print_summary(results: dict):
    print(f"\n\n{'═'*65}")
    print("  PIPELINE SUMMARY")
    print(f"{'═'*65}")
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    for stage, ok in results.items():
        name = STAGES[stage][0]
        status = " OK  " if ok else "✗ FAIL"
        print(f"  Stage {stage}  [{status}]  {name}")
    print(f"{'─'*65}")
    print(f"  {passed}/{total} stages completed successfully")
    print(f"{'═'*65}\n")


def run_demo():
    print("\n" + "═"*65)
    print("  AI CODE ERROR CORRECTION — QUICK DEMO")
    print("═"*65)

    demo_samples = [
        {
            "id": "DEMO_001", "language": "C",
            "incorrect": '#include <stdio.h>\nint main() {\n    int reslt = 5 * 5\n    printff("%d\\n", reslt);\n    retun 0;\n}',
            "correct":   '#include <stdio.h>\nint main() {\n    int result = 5 * 5;\n    printf("%d\\n", result);\n    return 0;\n}',
            "error_type": "LEXICAL", "error_line": 3,
            "error_desc": "Multiple lexical errors: misspelled 'reslt', 'printff', 'retun'; missing semicolon",
        },
        {
            "id": "DEMO_002", "language": "CPP",
            "incorrect": '#include <iostream>\nusing namespace std;\nint main() {\n    cot << "Hello" << ENDL;\n    return 0;\n}',
            "correct":   '#include <iostream>\nusing namespace std;\nint main() {\n    cout << "Hello" << endl;\n    return 0;\n}',
            "error_type": "LEXICAL", "error_line": 4,
            "error_desc": "'cot' should be 'cout'; 'ENDL' should be 'endl'",
        },
        {
            "id": "DEMO_003", "language": "Java",
            "incorrect": 'public class Demo {\n    public static void main(String[] args) {\n        int x = 10\n        System.out.println(x);\n    }\n}',
            "correct":   'public class Demo {\n    public static void main(String[] args) {\n        int x = 10;\n        System.out.println(x);\n    }\n}',
            "error_type": "SYNTAX", "error_line": 3,
            "error_desc": "Missing semicolon after variable declaration",
        },
    ]

    from correction_module.error_correction_module import ErrorCorrectionModule
    corrector = ErrorCorrectionModule()

    for demo in demo_samples:
        print(f"\n  {'─'*60}")
        print(f"  {demo['id']}  |  {demo['language']}  |  {demo['error_type']}")
        print(f"  Error: {demo['error_desc']}")
        print(f"\n  Incorrect Code:")
        for i, line in enumerate(demo["incorrect"].splitlines(), 1):
            arrow = " ◄" if i == demo["error_line"] else ""
            print(f"    {i:2d}│ {line}{arrow}")

        result = corrector.analyze(demo["incorrect"], demo["language"])

        print(f"\n  Diagnostics ({len(result.diagnostics)} found):")
        for d in result.diagnostics[:3]:
            print(f"    Line {d.line}: [{d.error_type.name}] {d.message}")

        if result.suggestions:
            sug = result.best_suggestion()
            print(f"\n  Best Suggestion (confidence={sug.confidence:.0%}):")
            print(f"    Original  → {sug.original_line.strip()}")
            print(f"    Corrected → {sug.corrected_line.strip()}")
            print(f"    Reason    : {sug.explanation}")

    print(f"\n{'═'*65}\n")


def main():
    parser = argparse.ArgumentParser(description="AI Code Error Correction Pipeline")
    parser.add_argument("--stage", type=int, nargs="+",
                        help="Run specific stage numbers (e.g. --stage 1 2 3)")
    parser.add_argument("--demo",  action="store_true",
                        help="Run quick interactive demo")
    parser.add_argument("--list",  action="store_true",
                        help="List all stages and exit")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable stages:")
        for n, (name, script) in STAGES.items():
            print(f"  {n}. {name:30s} ({script})")
        return

    if args.demo:
        try:
            run_demo()
        except ImportError:
            print("  [INFO] Run stages 1-4 first to generate the full pipeline artifacts.")
        return

    stages_to_run = args.stage if args.stage else list(STAGES.keys())

    print("\n" + "═"*65)
    print("  AI-ASSISTED CODE ERROR CORRECTION — PIPELINE")
    print(f"  Stages: {stages_to_run}")
    print("═"*65)

    results = {}
    for stage_num in stages_to_run:
        if stage_num not in STAGES:
            print(f"  [WARN] Unknown stage {stage_num}, skipping.")
            continue
        name, script = STAGES[stage_num]
        ok = run_stage(stage_num, name, script)
        results[stage_num] = ok

    print_summary(results)


if __name__ == "__main__":
    main()