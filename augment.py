# ============================================================
# augment.py
# DATA AUGMENTATION PIPELINE
# Reads  : dataset/processed/train.json   (or dataset/train.json)
# Writes : dataset/processed/train_augmented.json
# ============================================================

import json
import os
import re
import random
import copy
from datetime import datetime

random.seed(42)

# ─────────────────────────────────────────────────────────────
# PATH RESOLUTION  — works on Windows and Linux
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _find_train(candidates):
    for p in candidates:
        full = os.path.join(BASE_DIR, p)
        if os.path.exists(full):
            return full
    return None

TRAIN_PATH = _find_train([
    os.path.join("dataset", "processed", "train.json"),
    os.path.join("dataset", "train.json"),
    "train.json",
])

OUT_DIR   = os.path.join(BASE_DIR, "dataset", "processed")
OUT_PATH  = os.path.join(OUT_DIR, "train_augmented.json")


# ─────────────────────────────────────────────────────────────
# AUGMENTATION STRATEGIES
# ─────────────────────────────────────────────────────────────

def aug_add_blank_line(sample):
    """Insert a blank line after a { line."""
    code = sample.get("code") or sample.get("correct", "")
    if not code:
        return None
    lines = code.splitlines()
    positions = [i for i, l in enumerate(lines) if l.rstrip().endswith("{")]
    if not positions:
        return None
    idx = random.choice(positions)
    lines.insert(idx + 1, "")
    new = copy.deepcopy(sample)
    new["code"]         = "\n".join(lines)
    new["id"]           = sample.get("id", "x") + "_aug_blank"
    new["augmented"]    = True
    new["aug_strategy"] = "add_blank_line"
    return new


def aug_remove_blank_line(sample):
    """Remove a blank line from the code."""
    code = sample.get("code") or sample.get("correct", "")
    if not code:
        return None
    lines = code.splitlines()
    blanks = [i for i, l in enumerate(lines) if l.strip() == ""]
    if not blanks:
        return None
    lines.pop(random.choice(blanks))
    new = copy.deepcopy(sample)
    new["code"]         = "\n".join(lines)
    new["id"]           = sample.get("id", "x") + "_aug_rmblank"
    new["augmented"]    = True
    new["aug_strategy"] = "remove_blank_line"
    return new


def aug_rename_variable(sample):
    """Rename a local variable consistently throughout the code."""
    code = sample.get("code") or sample.get("correct", "")
    if not code:
        return None
    # Find declared variables (simple int/double/float/char/bool x = ...)
    matches = re.findall(r'\b(?:int|double|float|char|bool|string)\s+([a-z]\w*)\s*[=;,)]', code)
    if not matches:
        return None
    old_name = random.choice(matches)
    new_name = old_name + "_v2"
    # Only rename if it appears more than once (it's actually used)
    if code.count(old_name) < 2:
        return None
    new_code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)
    new = copy.deepcopy(sample)
    new["code"]         = new_code
    new["id"]           = sample.get("id", "x") + "_aug_rename"
    new["augmented"]    = True
    new["aug_strategy"] = "rename_variable"
    return new


def aug_add_comment(sample):
    """Add an inline comment to a random statement line."""
    code = sample.get("code") or sample.get("correct", "")
    if not code:
        return None
    lines = code.splitlines()
    candidates = [i for i, l in enumerate(lines)
                  if l.strip().endswith(";") and not l.strip().startswith("//")]
    if not candidates:
        return None
    idx = random.choice(candidates)
    comments = [
        "// initialise",
        "// compute result",
        "// check condition",
        "// update value",
        "// loop body",
        "// return result",
    ]
    lines[idx] = lines[idx] + "  " + random.choice(comments)
    new = copy.deepcopy(sample)
    new["code"]         = "\n".join(lines)
    new["id"]           = sample.get("id", "x") + "_aug_comment"
    new["augmented"]    = True
    new["aug_strategy"] = "add_comment"
    return new


def aug_swap_literal(sample):
    """Replace an integer literal with a different one."""
    code = sample.get("code") or sample.get("correct", "")
    if not code:
        return None
    # Find standalone integer literals not in #include lines
    lines = code.splitlines()
    new_lines = []
    changed = False
    for line in lines:
        if not changed and not line.strip().startswith("#"):
            nums = re.findall(r'\b([2-9]|[1-9]\d+)\b', line)
            if nums:
                old = random.choice(nums)
                new_val = str(int(old) + random.choice([1, 2, 5, 10]))
                line = re.sub(r'\b' + re.escape(old) + r'\b', new_val, line, count=1)
                changed = True
        new_lines.append(line)
    if not changed:
        return None
    new = copy.deepcopy(sample)
    new["code"]         = "\n".join(new_lines)
    new["id"]           = sample.get("id", "x") + "_aug_literal"
    new["augmented"]    = True
    new["aug_strategy"] = "swap_literal"
    return new


def aug_reorder_declarations(sample):
    """Swap two consecutive variable declarations."""
    code = sample.get("code") or sample.get("correct", "")
    if not code:
        return None
    lines = code.splitlines()
    decl_pat = re.compile(r'^\s+(?:int|double|float|char|bool|string)\s+\w+')
    decl_indices = [i for i, l in enumerate(lines) if decl_pat.match(l)]
    consec = [(decl_indices[i], decl_indices[i+1])
              for i in range(len(decl_indices)-1)
              if decl_indices[i+1] == decl_indices[i] + 1]
    if not consec:
        return None
    a, b = random.choice(consec)
    lines[a], lines[b] = lines[b], lines[a]
    new = copy.deepcopy(sample)
    new["code"]         = "\n".join(lines)
    new["id"]           = sample.get("id", "x") + "_aug_reorder"
    new["augmented"]    = True
    new["aug_strategy"] = "reorder_declarations"
    return new


AUGMENTERS = [
    aug_add_blank_line,
    aug_remove_blank_line,
    aug_rename_variable,
    aug_add_comment,
    aug_swap_literal,
    aug_reorder_declarations,
]


# ─────────────────────────────────────────────────────────────
# MAIN AUGMENTATION RUNNER
# ─────────────────────────────────────────────────────────────

def run_augmentation(
    train_path   = None,
    out_path     = None,
    augment_ratio = 0.5,   # augment 50% of NONE samples
    seed          = 42,
):
    random.seed(seed)

    # ── resolve paths ────────────────────────────────────────
    t_path = train_path or TRAIN_PATH
    o_path = out_path   or OUT_PATH

    if t_path is None or not os.path.exists(t_path):
        # Search more aggressively
        for root, dirs, files in os.walk(BASE_DIR):
            for fname in files:
                if fname == "train.json":
                    t_path = os.path.join(root, fname)
                    break
            if t_path and os.path.exists(t_path):
                break

    if t_path is None or not os.path.exists(t_path):
        print(f"[AUGMENT] ✗ Could not find train.json")
        print(f"[AUGMENT]   Make sure preprocessing.py has been run first.")
        print(f"[AUGMENT]   Searched in: {BASE_DIR}")
        return False

    print(f"[AUGMENT] Loading : {t_path}")

    with open(t_path, encoding="utf-8") as f:
        train_data = json.load(f)

    print(f"[AUGMENT] Loaded  : {len(train_data)} samples")

    # ── select NONE samples to augment ───────────────────────
    none_samples = [s for s in train_data
                    if s.get("error_type") == "NONE" or s.get("error_label") == 0]
    n_aug        = max(1, int(len(none_samples) * augment_ratio))
    to_augment   = random.sample(none_samples, min(n_aug, len(none_samples)))

    print(f"[AUGMENT] Augmenting {len(to_augment)} of {len(none_samples)} NONE samples ...")

    augmented = []
    strategy_counts = {}

    for sample in to_augment:
        shuffled_aug = AUGMENTERS[:]
        random.shuffle(shuffled_aug)
        for aug_fn in shuffled_aug:
            result = aug_fn(sample)
            if result:
                augmented.append(result)
                strat = result.get("aug_strategy", "unknown")
                strategy_counts[strat] = strategy_counts.get(strat, 0) + 1
                break

    # ── combine & save ───────────────────────────────────────
    combined = train_data + augmented
    random.shuffle(combined)

    os.makedirs(os.path.dirname(o_path), exist_ok=True)
    with open(o_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    # ── report ───────────────────────────────────────────────
    print(f"\n[AUGMENT] Augmentation complete")
    print(f"  Original samples  : {len(train_data)}")
    print(f"  Augmented added   : {len(augmented)}")
    print(f"  Total combined    : {len(combined)}")
    print(f"\n  Strategy breakdown:")
    for strat, cnt in sorted(strategy_counts.items()):
        print(f"    {strat:30s} : {cnt}")
    print(f"\n  Saved → {o_path}")
    return True


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  DATA AUGMENTATION PIPELINE")
    print("=" * 60)
    success = run_augmentation()
    if not success:
        import sys
        sys.exit(1)