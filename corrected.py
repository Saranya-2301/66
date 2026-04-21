import os
import sys
import time
from auto_corrector import AutoCorrector

def main():
    try:
        print("\nEnter file path (example: test.c):")
        file_path = input().strip()

        if not os.path.exists(file_path):
            print("File not found")
            return

        # Detect language
        ext = file_path.split(".")[-1].lower()
        if ext == "c":
            language = "C"
        elif ext in ["cpp", "c++"]:
            language = "CPP"
        elif ext == "java":
            language = "Java"
        else:
            print("Unsupported file type")
            return

        start_time = time.time()

        corrector = AutoCorrector()
        result = corrector.run(language, file_path, silent=True)

        end_time = time.time()
        runtime = round((end_time - start_time) * 1000, 2)

        if not result:
            print("No result returned from AutoCorrector")
            return

        # ─────────────────────────────────────────────
        # FETCH DATA
        # ─────────────────────────────────────────────
        errors_before = result.get("errors_before", 0)
        errors_after = result.get("errors_after", 0)
        corrected_code = result.get("corrected", "")
        original_code = result.get("original", "")
        fixes_applied = result.get("fixes_applied", 0)

        # ─────────────────────────────────────────────
        # METRICS CALCULATION
        # ─────────────────────────────────────────────
        orig_lines = original_code.splitlines()
        corr_lines = corrected_code.splitlines()

        changed_lines = 0
        changed_chars = 0

        for i in range(max(len(orig_lines), len(corr_lines))):
            o = orig_lines[i] if i < len(orig_lines) else ""
            c = corr_lines[i] if i < len(corr_lines) else ""

            if o != c:
                changed_lines += 1
                changed_chars += abs(len(o) - len(c))

        status = "SUCCESS" if errors_after == 0 else "PARTIAL"
        success = errors_after == 0
        code_changed = "YES" if fixes_applied > 0 else "NO"

        # Dummy placeholders (can improve later)
        semantic_issues = 0
        security_warnings = 0

        # Green Score
        if errors_before == 0:
            green_score = 100
        else:
            green_score = round(
                ((errors_before - errors_after) / errors_before) * 100, 2
            )

        # ─────────────────────────────────────────────
        # OUTPUT
        # ─────────────────────────────────────────────
        print("="*60)
        print("AI COMPILER RESULT")
        print("="*60)

        print(f"\nStatus            : {status}")
        print(f"Success           : {success}")
        print(f"Code Changed      : {code_changed}")
        print(f"Changed Lines     : {changed_lines}")
        print(f"Changed Chars     : {changed_chars}")
        print(f"Errors Reported   : {errors_before}")
        print(f"Errors Remaining  : {errors_after}")
        print(f"Semantic Issues   : {semantic_issues}")
        print(f"Security Warnings : {security_warnings}")
        print(f"Green Score (%)   : {green_score}")
        print(f"Runtime (ms)      : {runtime}")

        print("\nCorrected Code:\n")
        print(corrected_code if corrected_code else "No corrected code generated")

        print("="*60)

    except Exception as e:
        print("\nERROR OCCURRED:")
        print(e)

if __name__ == "__main__":
    main()