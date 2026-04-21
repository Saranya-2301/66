AI Assisted Compiler Front End

Overview This project is an AI Assisted Compiler Front End that performs lexical analysis, syntax parsing using ANTLR, abstract syntax tree generation, and AI based error prediction with suggestions. It also provides a graphical user interface for interaction.

Supported languages C C++ Java

Project flow

Input Code → Lexer → Parser → AST Generator → Error Predictor → Output (Terminal / GUI / HTML)

Project structure

Core modules Main1.py – Main entry point for CLI and pipeline run_pipeline.py – Runs full pipeline lexer_runner.py – Handles lexical analysis parser_runner.py – Handles syntax parsing ast_runner.py – Builds AST

Grammar files (ANTLR) C.g4 CPP.g4 Java.g4 CParser.g4 Parser.g4 Test.g4

Generated lexer and parser files CLexer.py, CParser.py CPPLexer.py, CPPParser.py JavaLexer.py, JavaParser.py

AST handling ast_nodes.py ASTVisitor.py CVisitor.py, CPPVisitor.py, JavaVisitor.py c_ast_visitor.py java_ast_visitor.py print_ast.py

Error handling error.py error_listener.py error_collector.py error_display.py error_correction.py auto_corrector.py

AI and ML components ErrorPredictor.py feature_extraction.py preprocess.py dataset_creator.py DatasetBuilder.py convert_dataset.py dataset.csv dataset.json error_model.pkl Ml pipeline.py LSTM_Model.py

GUI gui.py – Provides interface for selecting file and running analysis

Testing and validation test.c hello.c system_validation.py performance_evaluation.py security_robustness.py

Reports report.html report_c.html

Installation

Install required packages pip install antlr4-python3-runtime scikit-learn pandas numpy

Setup ANTLR Download antlr-4.13.2-complete.jar

To regenerate parser files java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 C.g4

Usage

Run using command line python Main1.py C test.c

Optional flags --no-lex to skip lexer --no-parse to skip parser --no-ast to skip AST --only-errors to run only error prediction --html report.html to generate HTML report

Train ML model python Main1.py --train --c-dir samples/c/

Run GUI python gui.py

Features

Detects lexical and syntax errors Predicts corrections using machine learning Displays confidence scores Generates HTML reports Supports multiple programming languages Modular and extensible design

Example output

Syntax error at line 5 Missing semicolon Suggestion Add semicolon Confidence 89 percent

Limitations

Accuracy depends on dataset quality Some syntax errors may produce multiple cascading errors ANTLR setup required

Future improvements

Automatic error correction Semantic analysis Code optimization Improved graphical interface Support for more languages
