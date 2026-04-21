# ============================================================
# Main1.py (FIXED FOR GUI)
# ============================================================
import warnings
warnings.filterwarnings("ignore")
import sys
sys.stdout.reconfigure(encoding='utf-8')  # 🔥 FIX

import os
import argparse

from lexer_runner  import run_lexer
from parser_runner import run_parser
from ast_runner    import run_ast

# ─────────────────────────────────────────────────────────────
# SAFE BANNER (NO UNICODE ISSUE)
# ─────────────────────────────────────────────────────────────
BANNER = """
==================================================
   AI COMPILER FRONT-END
   Lexer | Parser | AST | Error Prediction
==================================================
"""

SUPPORTED = ["C", "CPP", "Java"]

LANG_MAP = {
    "c":"C","C":"C",
    "cpp":"CPP","CPP":"CPP",
    "c++":"CPP","C++":"CPP",
    "java":"Java","Java":"Java","JAVA":"Java",
}

def _check_file(path):
    if not os.path.isfile(path):
        print(f"[main] File not found: {path}")
        sys.exit(1)

# ─────────────────────────────────────────────────────────────
def analyse(language, file_path,
            run_lex=True,
            run_parse=True,
            run_tree=True,
            run_errors=True,
            model_path="error_model.pkl",
            html_out=None):

    _check_file(file_path)

    print(BANNER)
    print(f"Language : {language}")
    print(f"File     : {file_path}\n")

    if run_lex:
        print("-"*50)
        print("[1/4] LEXER")
        print("-"*50)
        run_lexer(language, file_path)

    if run_parse:
        print("\n" + "-"*50)
        print("[2/4] PARSER")
        print("-"*50)
        run_parser(language, file_path)

    if run_tree:
        print("\n" + "-"*50)
        print("[3/4] AST")
        print("-"*50)
        run_ast(language, file_path)

    if run_errors:
        print("\n" + "-"*50)
        print("[4/4] ERROR PREDICTION")
        print("-"*50)

        from ErrorPredictor import ErrorPredictor
        from error_display import display_predictions

        predictor = ErrorPredictor()

        if os.path.exists(model_path):
            predictor.load(model_path)
        else:
            print(f"[!] No model found. Using default rules.")

        preds = predictor.predict_file(language, file_path)

        display_predictions(language, file_path, preds,
                            terminal=True, html_out=html_out)

    print("\nAnalysis complete.")

# ─────────────────────────────────────────────────────────────
def _cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("language", nargs="?",
                        choices=["C","CPP","Java","c","cpp","java","c++","C++","JAVA"])
    parser.add_argument("file", nargs="?")

    args = parser.parse_args()

    if not args.language or not args.file:
        parser.print_help()
        sys.exit(0)

    lang = LANG_MAP.get(args.language, args.language)

    analyse(lang, args.file)

if __name__ == "__main__":
    _cli()