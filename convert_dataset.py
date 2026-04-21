# ============================================================
# convert_dataset.py
# Generates a rich annotated_dataset.json with:
#   - 100 C samples   (34 NONE, 33 LEXICAL, 33 SYNTAX)
#   - 100 CPP samples (34 NONE, 33 LEXICAL, 33 SYNTAX)
#   - 100 Java samples(32 NONE, 34 LEXICAL, 34 SYNTAX)
#   Total: 300 samples | ~150 LEXICAL | ~150 SYNTAX | ~100 NONE
# ============================================================

import json
import os
import random
random.seed(42)

# ─────────────────────────────────────────────────────────────
# CLEAN SOURCE TEMPLATES
# ─────────────────────────────────────────────────────────────

C_TEMPLATES = [
    # 1
    ("""\
#include <stdio.h>
int main() {
    int x = 10;
    int y = 20;
    int sum = x + y;
    printf("%d\\n", sum);
    return 0;
}""", "basic addition"),
    # 2
    ("""\
#include <stdio.h>
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
int main() {
    int result = factorial(5);
    printf("%d\\n", result);
    return 0;
}""", "factorial recursion"),
    # 3
    ("""\
#include <stdio.h>
int main() {
    int i;
    int sum = 0;
    for (i = 1; i <= 10; i++) {
        sum = sum + i;
    }
    printf("Sum: %d\\n", sum);
    return 0;
}""", "for loop sum"),
    # 4
    ("""\
#include <stdio.h>
int main() {
    int n = 5;
    int fact = 1;
    while (n > 0) {
        fact = fact * n;
        n--;
    }
    printf("Fact: %d\\n", fact);
    return 0;
}""", "while loop"),
    # 5
    ("""\
#include <stdio.h>
int main() {
    int arr[5];
    int i;
    for (i = 0; i < 5; i++) {
        arr[i] = i * 2;
    }
    for (i = 0; i < 5; i++) {
        printf("%d\\n", arr[i]);
    }
    return 0;
}""", "array loop"),
    # 6
    ("""\
#include <stdio.h>
#include <string.h>
int main() {
    char name[50];
    strcpy(name, "hello");
    int len = strlen(name);
    printf("Length: %d\\n", len);
    return 0;
}""", "string length"),
    # 7
    ("""\
#include <stdio.h>
int add(int a, int b) {
    return a + b;
}
int subtract(int a, int b) {
    return a - b;
}
int main() {
    printf("%d\\n", add(10, 5));
    printf("%d\\n", subtract(10, 5));
    return 0;
}""", "functions"),
    # 8
    ("""\
#include <stdio.h>
int main() {
    int x = 10;
    if (x > 5) {
        printf("Greater\\n");
    } else {
        printf("Smaller\\n");
    }
    return 0;
}""", "if else"),
    # 9
    ("""\
#include <stdio.h>
int main() {
    int day = 3;
    switch (day) {
        case 1: printf("Mon\\n"); break;
        case 2: printf("Tue\\n"); break;
        case 3: printf("Wed\\n"); break;
        default: printf("Other\\n"); break;
    }
    return 0;
}""", "switch"),
    # 10
    ("""\
#include <stdio.h>
struct Point {
    int x;
    int y;
};
int main() {
    struct Point p;
    p.x = 3;
    p.y = 4;
    printf("%d %d\\n", p.x, p.y);
    return 0;
}""", "struct"),
]

CPP_TEMPLATES = [
    # 1
    ("""\
#include <iostream>
using namespace std;
int main() {
    int x = 10;
    int y = 20;
    cout << x + y << endl;
    return 0;
}""", "basic cout"),
    # 2
    ("""\
#include <iostream>
using namespace std;
class Animal {
private:
    string name;
public:
    Animal(string n) {
        name = n;
    }
    void speak() {
        cout << name << " speaks" << endl;
    }
};
int main() {
    Animal a("Dog");
    a.speak();
    return 0;
}""", "class constructor"),
    # 3
    ("""\
#include <iostream>
using namespace std;
class Shape {
public:
    virtual double area() {
        return 0;
    }
};
class Circle : public Shape {
    double r;
public:
    Circle(double radius) {
        r = radius;
    }
    double area() override {
        return 3.14 * r * r;
    }
};
int main() {
    Circle c(5.0);
    cout << c.area() << endl;
    return 0;
}""", "inheritance virtual"),
    # 4
    ("""\
#include <iostream>
using namespace std;
int main() {
    int i = 0;
    int sum = 0;
    for (i = 0; i < 10; i++) {
        sum += i;
    }
    cout << sum << endl;
    return 0;
}""", "for loop"),
    # 5
    ("""\
#include <iostream>
using namespace std;
int divide(int a, int b) {
    if (b == 0) {
        throw "Division by zero";
    }
    return a / b;
}
int main() {
    try {
        cout << divide(10, 2) << endl;
        cout << divide(5, 0) << endl;
    } catch (const char* msg) {
        cout << msg << endl;
    }
    return 0;
}""", "try catch throw"),
    # 6
    ("""\
#include <iostream>
using namespace std;
namespace Math {
    int add(int a, int b) {
        return a + b;
    }
    int square(int n) {
        return n * n;
    }
}
int main() {
    cout << Math::add(3, 4) << endl;
    cout << Math::square(5) << endl;
    return 0;
}""", "namespace"),
    # 7
    ("""\
#include <iostream>
using namespace std;
template <typename T>
T maxOf(T a, T b) {
    if (a > b) return a;
    return b;
}
int main() {
    cout << maxOf(3, 7) << endl;
    cout << maxOf(3.5, 2.1) << endl;
    return 0;
}""", "template function"),
    # 8
    ("""\
#include <iostream>
using namespace std;
struct Point {
    int x;
    int y;
    void display() {
        cout << x << " " << y << endl;
    }
};
int main() {
    Point p;
    p.x = 3;
    p.y = 4;
    p.display();
    return 0;
}""", "struct method"),
    # 9
    ("""\
#include <iostream>
using namespace std;
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
int main() {
    cout << factorial(5) << endl;
    cout << factorial(7) << endl;
    return 0;
}""", "recursion"),
    # 10
    ("""\
#include <iostream>
using namespace std;
class Counter {
    static int count;
    int id;
public:
    Counter() {
        count++;
        id = count;
    }
    static int getCount() {
        return count;
    }
    int getId() const {
        return id;
    }
};
int Counter::count = 0;
int main() {
    Counter c1;
    Counter c2;
    cout << Counter::getCount() << endl;
    cout << c1.getId() << endl;
    return 0;
}""", "static member"),
]

JAVA_TEMPLATES = [
    # 1
    ("""\
public class Hello {
    public static void main(String[] args) {
        int x = 10;
        int y = 20;
        System.out.println(x + y);
    }
}""", "basic println"),
    # 2
    ("""\
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    public int multiply(int a, int b) {
        return a * b;
    }
    public static void main(String[] args) {
        Calculator c = new Calculator();
        System.out.println(c.add(5, 3));
        System.out.println(c.multiply(4, 6));
    }
}""", "class methods"),
    # 3
    ("""\
public class Loop {
    public static void main(String[] args) {
        int sum = 0;
        for (int i = 1; i <= 10; i++) {
            sum = sum + i;
        }
        System.out.println(sum);
    }
}""", "for loop"),
    # 4
    ("""\
public class Factorial {
    public static int factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    public static void main(String[] args) {
        System.out.println(factorial(5));
        System.out.println(factorial(7));
    }
}""", "recursion"),
    # 5
    ("""\
public class Conditions {
    public static void main(String[] args) {
        int x = 15;
        if (x > 10) {
            System.out.println("Greater than 10");
        } else if (x > 5) {
            System.out.println("Greater than 5");
        } else {
            System.out.println("Small");
        }
    }
}""", "if else if"),
    # 6
    ("""\
public class ArrayDemo {
    public static void main(String[] args) {
        int[] arr = new int[5];
        for (int i = 0; i < 5; i++) {
            arr[i] = i * 3;
        }
        for (int i = 0; i < 5; i++) {
            System.out.println(arr[i]);
        }
    }
}""", "array"),
    # 7
    ("""\
public class StringDemo {
    public static void main(String[] args) {
        String name = "Hello";
        int len = name.length();
        System.out.println(name);
        System.out.println(len);
        System.out.println(name.toUpperCase());
    }
}""", "string methods"),
    # 8
    ("""\
public class SwitchDemo {
    public static void main(String[] args) {
        int day = 3;
        switch (day) {
            case 1: System.out.println("Mon"); break;
            case 2: System.out.println("Tue"); break;
            case 3: System.out.println("Wed"); break;
            default: System.out.println("Other"); break;
        }
    }
}""", "switch"),
    # 9
    ("""\
public class TryCatch {
    public static int divide(int a, int b) {
        return a / b;
    }
    public static void main(String[] args) {
        try {
            int result = divide(10, 2);
            System.out.println(result);
            int bad = divide(5, 0);
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}""", "try catch"),
    # 10
    ("""\
public class WhileDemo {
    public static void main(String[] args) {
        int n = 1;
        int sum = 0;
        while (n <= 100) {
            sum = sum + n;
            n++;
        }
        System.out.println(sum);
    }
}""", "while loop"),
]


# ─────────────────────────────────────────────────────────────
# LEXICAL ERROR INJECTORS
# Each returns (incorrect_code, error_desc, error_line)
# ─────────────────────────────────────────────────────────────

def lex_unclosed_string(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if '"' in line and not line.strip().startswith('//'):
            idx = line.index('"')
            end = line.rfind('"')
            if end > idx:
                lines[i] = line[:end]   # remove closing quote
                return "\n".join(lines), "Unclosed string literal", i + 1
    return None

def lex_invalid_identifier(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if 'int ' in line and '=' not in line and '{' not in line:
            lines[i] = line.replace('int ', 'int 2bad_', 1)
            return "\n".join(lines), "Identifier starts with digit", i + 1
    return None

def lex_typo_keyword_return(code):
    if 'return' in code:
        bad = code.replace('return', 'retrun', 1)
        line = next((i+1 for i,l in enumerate(code.splitlines()) if 'return' in l), 1)
        return bad, "Typo in keyword: retrun instead of return", line
    return None

def lex_typo_keyword_void(code):
    if 'void' in code:
        bad = code.replace('void', 'viod', 1)
        line = next((i+1 for i,l in enumerate(code.splitlines()) if 'void' in l), 1)
        return bad, "Typo in keyword: viod instead of void", line
    return None

def lex_typo_keyword_int(code):
    if '\nint ' in code:
        bad = code.replace('\nint ', '\nnt ', 1)
        line = next((i+1 for i,l in enumerate(code.splitlines()) if l.strip().startswith('int ')), 1)
        return bad, "Typo in keyword: nt instead of int", line
    return None

def lex_typo_include(code):
    if '#include' in code:
        bad = code.replace('#include', '#includ', 1)
        return bad, "Typo in preprocessor: includ instead of include", 1
    return None

def lex_typo_class(code):
    if 'class ' in code:
        bad = code.replace('class ', 'clas ', 1)
        line = next((i+1 for i,l in enumerate(code.splitlines()) if 'class ' in l), 1)
        return bad, "Typo in keyword: clas instead of class", line
    return None

def lex_typo_public(code):
    if 'public' in code:
        bad = code.replace('public', 'pubic', 1)
        line = next((i+1 for i,l in enumerate(code.splitlines()) if 'public' in l), 1)
        return bad, "Typo in keyword: pubic instead of public", line
    return None

def lex_typo_static(code):
    if 'static' in code:
        bad = code.replace('static', 'statc', 1)
        line = next((i+1 for i,l in enumerate(code.splitlines()) if 'static' in l), 1)
        return bad, "Typo in keyword: statc instead of static", line
    return None

def lex_invalid_char(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if '=' in line and not line.strip().startswith('//'):
            lines[i] = line.replace('=', '@=', 1)
            return "\n".join(lines), "Invalid character @ in expression", i + 1
    return None

LEXICAL_INJECTORS = [
    lex_unclosed_string,
    lex_invalid_identifier,
    lex_typo_keyword_return,
    lex_typo_keyword_void,
    lex_typo_keyword_int,
    lex_typo_include,
    lex_typo_class,
    lex_typo_public,
    lex_typo_static,
    lex_invalid_char,
]


# ─────────────────────────────────────────────────────────────
# SYNTAX ERROR INJECTORS
# ─────────────────────────────────────────────────────────────

def syn_missing_semicolon(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        s = line.rstrip()
        if s.endswith(';') and not s.strip().startswith('//') and not s.strip().startswith('for'):
            lines[i] = s[:-1]
            return "\n".join(lines), "Missing semicolon at end of statement", i + 1
    return None

def syn_missing_closing_brace(code):
    if code.count('{') > code.count('}'):
        return None
    lines = code.splitlines()
    for i in range(len(lines)-1, -1, -1):
        if lines[i].strip() == '}':
            lines.pop(i)
            return "\n".join(lines), "Missing closing brace", i + 1
    return None

def syn_extra_semicolon(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        s = line.rstrip()
        if s.endswith(';') and not s.strip().startswith('//'):
            lines[i] = s + ';'
            return "\n".join(lines), "Extra semicolon after statement", i + 1
    return None

def syn_missing_opening_brace(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        s = line.rstrip()
        if s.endswith('{'):
            lines[i] = s[:-1]
            return "\n".join(lines), "Missing opening brace", i + 1
    return None

def syn_missing_closing_paren(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if 'if (' in line or 'while (' in line or 'for (' in line:
            if line.rstrip().endswith(')') or ') {' in line:
                lines[i] = line.replace(')', '', 1)
                return "\n".join(lines), "Missing closing parenthesis", i + 1
    return None

def syn_missing_return(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('return ') and line.strip().endswith(';'):
            lines[i] = line.replace('return ', '', 1)
            return "\n".join(lines), "Missing return keyword", i + 1
    return None

def syn_extra_brace(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == '}':
            lines.insert(i, '}')
            return "\n".join(lines), "Extra closing brace", i + 1
    return None

def syn_mismatched_paren(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if 'printf(' in line or 'cout' in line or 'System.out' in line:
            if ')' in line:
                lines[i] = line.replace(')', ']', 1)
                return "\n".join(lines), "Mismatched parenthesis: ) replaced with ]", i + 1
    return None

def syn_missing_comma(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if ',' in line and ('printf' in line or 'cout' not in line):
            lines[i] = line.replace(',', '', 1)
            return "\n".join(lines), "Missing comma in argument list", i + 1
    return None

def syn_wrong_operator(code):
    if '==' in code:
        bad = code.replace('==', '=', 1)
        line = next((i+1 for i,l in enumerate(code.splitlines()) if '==' in l), 1)
        return bad, "Assignment used instead of comparison ==", line
    return None

SYNTAX_INJECTORS = [
    syn_missing_semicolon,
    syn_missing_closing_brace,
    syn_extra_semicolon,
    syn_missing_opening_brace,
    syn_missing_closing_paren,
    syn_missing_return,
    syn_extra_brace,
    syn_mismatched_paren,
    syn_missing_comma,
    syn_wrong_operator,
]


# ─────────────────────────────────────────────────────────────
# GENERATE SAMPLES FOR ONE LANGUAGE
# ─────────────────────────────────────────────────────────────

def generate_samples(language, templates, target_none, target_lex, target_syn, id_offset=0):
    samples = []
    sample_id = id_offset

    templates_cycle = templates * 20   # repeat templates to get enough variety
    random.shuffle(templates_cycle)

    lex_injectors = LEXICAL_INJECTORS * 20
    syn_injectors = SYNTAX_INJECTORS  * 20
    random.shuffle(lex_injectors)
    random.shuffle(syn_injectors)

    lex_idx = 0
    syn_idx = 0

    for code, desc in templates_cycle:
        if len([s for s in samples if s["error_type"] == "NONE"]) < target_none:
            samples.append({
                "id"          : f"{language}_{sample_id:04d}",
                "language"    : language,
                "error_type"  : "NONE",
                "error_desc"  : "",
                "error_line"  : 0,
                "incorrect"   : "",
                "correct"     : code,
            })
            sample_id += 1

        if len([s for s in samples if s["error_type"] == "LEXICAL"]) < target_lex:
            while lex_idx < len(lex_injectors):
                inj = lex_injectors[lex_idx]
                lex_idx += 1
                result = inj(code)
                if result:
                    inc_code, err_desc, err_line = result
                    samples.append({
                        "id"         : f"{language}_{sample_id:04d}",
                        "language"   : language,
                        "error_type" : "LEXICAL",
                        "error_desc" : err_desc,
                        "error_line" : err_line,
                        "incorrect"  : inc_code,
                        "correct"    : code,
                    })
                    sample_id += 1
                    break

        if len([s for s in samples if s["error_type"] == "SYNTAX"]) < target_syn:
            while syn_idx < len(syn_injectors):
                inj = syn_injectors[syn_idx]
                syn_idx += 1
                result = inj(code)
                if result:
                    inc_code, err_desc, err_line = result
                    samples.append({
                        "id"         : f"{language}_{sample_id:04d}",
                        "language"   : language,
                        "error_type" : "SYNTAX",
                        "error_desc" : err_desc,
                        "error_line" : err_line,
                        "incorrect"  : inc_code,
                        "correct"    : code,
                    })
                    sample_id += 1
                    break

        none_done = len([s for s in samples if s["error_type"] == "NONE"])
        lex_done  = len([s for s in samples if s["error_type"] == "LEXICAL"])
        syn_done  = len([s for s in samples if s["error_type"] == "SYNTAX"])
        if none_done >= target_none and lex_done >= target_lex and syn_done >= target_syn:
            break

    return samples


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  DATASET CONVERTER")
    print("  Generating 300 annotated samples")
    print("  C:100  CPP:100  Java:100")
    print("  ~150 LEXICAL | ~150 SYNTAX | ~100 NONE")
    print("=" * 60)

    all_samples = []

    # ── C: 100 samples ──────────────────────────────────────
    print("\n[+] Generating C samples ...")
    c_samples = generate_samples(
        language    = "C",
        templates   = C_TEMPLATES,
        target_none = 34,
        target_lex  = 33,
        target_syn  = 33,
        id_offset   = 0,
    )
    all_samples.extend(c_samples)
    print(f"    NONE={sum(1 for s in c_samples if s['error_type']=='NONE')}  "
          f"LEXICAL={sum(1 for s in c_samples if s['error_type']=='LEXICAL')}  "
          f"SYNTAX={sum(1 for s in c_samples if s['error_type']=='SYNTAX')}  "
          f"TOTAL={len(c_samples)}")

    # ── CPP: 100 samples ────────────────────────────────────
    print("\n[+] Generating CPP samples ...")
    cpp_samples = generate_samples(
        language    = "CPP",
        templates   = CPP_TEMPLATES,
        target_none = 34,
        target_lex  = 33,
        target_syn  = 33,
        id_offset   = 1000,
    )
    all_samples.extend(cpp_samples)
    print(f"    NONE={sum(1 for s in cpp_samples if s['error_type']=='NONE')}  "
          f"LEXICAL={sum(1 for s in cpp_samples if s['error_type']=='LEXICAL')}  "
          f"SYNTAX={sum(1 for s in cpp_samples if s['error_type']=='SYNTAX')}  "
          f"TOTAL={len(cpp_samples)}")

    # ── Java: 100 samples ───────────────────────────────────
    print("\n[+] Generating Java samples ...")
    java_samples = generate_samples(
        language    = "Java",
        templates   = JAVA_TEMPLATES,
        target_none = 32,
        target_lex  = 34,
        target_syn  = 34,
        id_offset   = 2000,
    )
    all_samples.extend(java_samples)
    print(f"    NONE={sum(1 for s in java_samples if s['error_type']=='NONE')}  "
          f"LEXICAL={sum(1 for s in java_samples if s['error_type']=='LEXICAL')}  "
          f"SYNTAX={sum(1 for s in java_samples if s['error_type']=='SYNTAX')}  "
          f"TOTAL={len(java_samples)}")

    # ── Shuffle & save ──────────────────────────────────────
    random.shuffle(all_samples)
    os.makedirs("dataset", exist_ok=True)
    out_path = "dataset/annotated_dataset.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_samples, f, indent=2, ensure_ascii=False)

    # ── Final report ─────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  FINAL SUMMARY")
    print("=" * 60)
    print(f"  Total samples  : {len(all_samples)}")
    print(f"  NONE           : {sum(1 for s in all_samples if s['error_type']=='NONE')}")
    print(f"  LEXICAL        : {sum(1 for s in all_samples if s['error_type']=='LEXICAL')}")
    print(f"  SYNTAX         : {sum(1 for s in all_samples if s['error_type']=='SYNTAX')}")
    print(f"  C              : {sum(1 for s in all_samples if s['language']=='C')}")
    print(f"  CPP            : {sum(1 for s in all_samples if s['language']=='CPP')}")
    print(f"  Java           : {sum(1 for s in all_samples if s['language']=='Java')}")
    print(f"\n  Saved → {out_path}")
    print("=" * 60)
