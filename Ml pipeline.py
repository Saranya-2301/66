# ============================================================
# ML PIPELINE
# Orchestrates the full machine-learning workflow:
#   1. Build dataset (inject errors into clean files)
#   2. Train classifier
#   3. Evaluate on held-out set
#   4. Save trained model
#   5. Run prediction on new files
#
# Can be run stand-alone OR imported for programmatic use.
# ============================================================

import os
import sys
import json
import argparse

from DatasetBuilder  import DatasetBuilder
from ErrorPredictor  import ErrorPredictor
from ErrorDisplay    import display_predictions


# ─────────────────────────────────────────────────────────────
# Default paths
# ─────────────────────────────────────────────────────────────
DEFAULT_DATASET_JSON = "dataset.json"
DEFAULT_DATASET_CSV  = "dataset.csv"
DEFAULT_MODEL_PATH   = "error_model.pkl"


# ─────────────────────────────────────────────────────────────
# Pipeline class
# ─────────────────────────────────────────────────────────────
class MLPipeline:
    """
    Unified pipeline entry point.

    Usage (programmatic):
        pipeline = MLPipeline()

        # Step 1 — build dataset
        pipeline.build_dataset(
            sources=[
                ("C",    "samples/c/",    ".c"),
                ("CPP",  "samples/cpp/",  ".cpp"),
                ("Java", "samples/java/", ".java"),
            ],
            dataset_json=DEFAULT_DATASET_JSON,
        )

        # Step 2 — train
        pipeline.train(dataset_json=DEFAULT_DATASET_JSON,
                       model_path=DEFAULT_MODEL_PATH,
                       model_type="random_forest")

        # Step 3 — predict
        pipeline.predict("Java", "Hello.java", html_report="report.html")
    """

    def __init__(self):
        self.predictor = None

    # ── BUILD ────────────────────────────────────────────────

    def build_dataset(self, sources: list,
                      dataset_json: str = DEFAULT_DATASET_JSON,
                      dataset_csv:  str = DEFAULT_DATASET_CSV,
                      injections_per_file: int = 4):
        """
        sources: list of (language, directory_or_file, extension)
          e.g. [("C", "samples/c/", ".c"), ...]
        """
        print("\n" + "━" * 60)
        print("  STEP 1 — Building dataset")
        print("━" * 60)

        builder = DatasetBuilder(injections_per_file=injections_per_file)

        for lang, path, ext in sources:
            if os.path.isdir(path):
                print(f"  [+] Scanning {lang} directory: {path}")
                builder.add_directory(lang, path, ext)
            elif os.path.isfile(path):
                print(f"  [+] Adding {lang} file: {path}")
                builder.add_file(lang, path)
            else:
                print(f"  [!] Path not found, skipping: {path}")

        if not builder.records:
            print("  [!] No records collected. Exiting.")
            return False

        builder.summary()
        builder.save_json(dataset_json)
        builder.save_csv(dataset_csv)
        return True

    # ── TRAIN ────────────────────────────────────────────────

    def train(self, dataset_json: str = DEFAULT_DATASET_JSON,
              model_path: str  = DEFAULT_MODEL_PATH,
              model_type: str  = "random_forest",
              test_size: float = 0.2):

        print("\n" + "━" * 60)
        print("  STEP 2 — Training ML model")
        print("━" * 60)

        if not os.path.exists(dataset_json):
            print(f"  [!] Dataset not found: {dataset_json}")
            print("      Run pipeline.build_dataset() first.")
            return False

        self.predictor = ErrorPredictor(model_type=model_type)
        self.predictor.train_from_json(dataset_json, test_size=test_size)
        self.predictor.save(model_path)
        return True

    # ── PREDICT ─────────────────────────────────────────────

    def predict(self, language: str, file_path: str,
                model_path: str = DEFAULT_MODEL_PATH,
                html_report: str = None,
                text_report: str = None):

        print("\n" + "━" * 60)
        print(f"  STEP 3 — Predicting errors [{language}]  {file_path}")
        print("━" * 60)

        if self.predictor is None:
            self.predictor = ErrorPredictor()
            if os.path.exists(model_path):
                self.predictor.load(model_path)
            else:
                print(f"  [!] No trained model found at {model_path}.")
                print("      Using rule-based fallback predictor.")

        preds = self.predictor.predict_file(language, file_path)

        display_predictions(
            language, file_path, preds,
            terminal  = True,
            html_out  = html_report,
            text_out  = text_report,
        )

        return preds

    # ── QUICK DEMO (no real source files needed) ─────────────

    def demo(self):
        """
        Runs a self-contained demo using synthetic (injected) errors.
        No external source files needed.
        """
        import tempfile, textwrap

        demo_sources = {
            "C": textwrap.dedent("""\
                #include <stdio.h>

                int main() {
                    int x = 10;
                    int y = 20;
                    printf("%d\\n", x + y);
                    return 0;
                }
            """),
            "CPP": textwrap.dedent("""\
                #include <iostream>
                using namespace std;

                int main() {
                    int a = 5;
                    cout << a << endl;
                    return 0;
                }
            """),
            "Java": textwrap.dedent("""\
                public class Hello {
                    public static void main(String[] args) {
                        int x = 42;
                        System.out.println(x);
                    }
                }
            """),
        }

        exts  = {"C": ".c", "CPP": ".cpp", "Java": ".java"}
        tmpfiles = []

        print("\n" + "★" * 60)
        print("  DEMO MODE — Injecting synthetic errors")
        print("★" * 60)

        for lang, src in demo_sources.items():
            # Write buggy version (remove a semicolon)
            lines = src.splitlines()
            for i, l in enumerate(lines):
                if ";" in l and not l.strip().startswith("//"):
                    lines[i] = l.replace(";", "", 1)
                    break
            buggy_src = "\n".join(lines)

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=exts[lang], delete=False, encoding="utf-8"
            ) as f:
                f.write(buggy_src)
                tmpfiles.append((lang, f.name))

        for lang, path in tmpfiles:
            self.predict(lang, path)
            os.unlink(path)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
def _cli():
    parser = argparse.ArgumentParser(
        description="AI Compiler Front-End — ML Pipeline",
        formatter_class=argparse.RawTextHelpFormatter
    )
    sub = parser.add_subparsers(dest="command")

    # build
    p_build = sub.add_parser("build", help="Build training dataset")
    p_build.add_argument("--c-dir",    default=None)
    p_build.add_argument("--cpp-dir",  default=None)
    p_build.add_argument("--java-dir", default=None)
    p_build.add_argument("--out",      default=DEFAULT_DATASET_JSON)

    # train
    p_train = sub.add_parser("train", help="Train ML model")
    p_train.add_argument("--dataset",    default=DEFAULT_DATASET_JSON)
    p_train.add_argument("--model",      default=DEFAULT_MODEL_PATH)
    p_train.add_argument("--model-type", default="random_forest",
                         choices=["random_forest","gradient_boost","svm","naive_bayes"])

    # predict
    p_pred = sub.add_parser("predict", help="Predict errors in a file")
    p_pred.add_argument("language", choices=["C","CPP","Java"])
    p_pred.add_argument("file")
    p_pred.add_argument("--model",  default=DEFAULT_MODEL_PATH)
    p_pred.add_argument("--html",   default=None)
    p_pred.add_argument("--text",   default=None)

    # demo
    sub.add_parser("demo", help="Run self-contained demo")

    args = parser.parse_args()
    pipe = MLPipeline()

    if args.command == "build":
        sources = []
        if args.c_dir:    sources.append(("C",    args.c_dir,    ".c"))
        if args.cpp_dir:  sources.append(("CPP",  args.cpp_dir,  ".cpp"))
        if args.java_dir: sources.append(("Java", args.java_dir, ".java"))
        if not sources:
            parser.error("Provide at least one of --c-dir, --cpp-dir, --java-dir")
        pipe.build_dataset(sources, dataset_json=args.out)

    elif args.command == "train":
        pipe.train(dataset_json=args.dataset, model_path=args.model,
                   model_type=args.model_type)

    elif args.command == "predict":
        pipe.predict(args.language, args.file,
                     model_path=args.model,
                     html_report=args.html,
                     text_report=args.text)

    elif args.command == "demo":
        pipe.demo()

    else:
        parser.print_help()


if __name__ == "__main__":
    _cli()