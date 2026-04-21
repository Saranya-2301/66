# ============================================================
# feature_extraction.py
# Reads preprocessed train / val / test JSON files produced
# by preprocessing.py and builds numpy .npz feature matrices.
#
# IMPORTANT: Does NOT use FeatureExtractor or ErrorRecord.
#            Works purely on the JSON output of preprocessing.py
# ============================================================

import os
import sys
import json
import csv
import numpy as np
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────
# PATH RESOLUTION  (works on Windows + Linux)
# ─────────────────────────────────────────────────────────────
def _find(candidates):
    for p in candidates:
        full = os.path.join(BASE_DIR, p)
        if os.path.exists(full):
            return full
    return None

# Read augmented train first, fall back to plain train
TRAIN_PATH = _find([
    os.path.join("dataset", "processed", "train_augmented.json"),
    os.path.join("dataset", "processed", "train.json"),
    os.path.join("dataset", "train.json"),
])
VAL_PATH = _find([
    os.path.join("dataset", "processed", "val.json"),
    os.path.join("dataset", "val.json"),
])
TEST_PATH = _find([
    os.path.join("dataset", "processed", "test.json"),
    os.path.join("dataset", "test.json"),
])

OUT_DIR = os.path.join(BASE_DIR, "dataset", "features")

# ─────────────────────────────────────────────────────────────
# WHICH COLUMNS TO USE AS FEATURES
# Only numeric columns with these prefixes are included.
# String / metadata columns are skipped automatically.
# ─────────────────────────────────────────────────────────────
FEATURE_PREFIXES = ("b_", "l_", "s_", "d_")

ALWAYS_SKIP = {
    "id", "language", "error_type", "error_desc",
    "code", "correct_code",
    "l_top_identifiers",      
    "m_code_hash",            
    "m_processed_at",        
    "aug_strategy",           
    "augmented",             
}

LABEL_COLUMN = "error_label"      


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def _is_numeric(value):
    """Return True if value can be cast to float."""
    if value is None:
        return False
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def _discover_feature_columns(records):
    """
    Scan the first record and return all column names that:
      - start with b_ / l_ / s_ / d_  OR  are language_label
      - are NOT in ALWAYS_SKIP
      - hold a numeric value
    """
    if not records:
        return []
    first = records[0]
    cols = []
    for key, val in first.items():
        if key in ALWAYS_SKIP:
            continue
        if not (any(key.startswith(p) for p in FEATURE_PREFIXES)
                or key == "language_label"):
            continue
        if _is_numeric(val):
            cols.append(key)
    return cols


# MAIN EXTRACTION FUNCTION

def extract_feature_matrix(records, feature_cols=None):
    """
    Convert preprocessed records → (X, y, feature_names).

    Args:
        records      : list of dicts from preprocessing.py
        feature_cols : list of column names to use (discovered
                       automatically from first record if None)

    Returns:
        X            : np.float32 array  shape (n, n_features)
        y            : np.int32   array  shape (n,)
        feature_cols : list of feature column names used
    """
    if not records:
        return np.zeros((0, 0), dtype=np.float32), \
               np.zeros(0, dtype=np.int32), []

    if feature_cols is None:
        feature_cols = _discover_feature_columns(records)

    if not feature_cols:
        print("[WARN] No numeric feature columns found in records.")
        return np.zeros((len(records), 0), dtype=np.float32), \
               np.zeros(len(records), dtype=np.int32), []

    X_rows = []
    y_rows = []

    for rec in records:
        row = []
        for col in feature_cols:
            val = rec.get(col, 0)
            try:
                row.append(float(val))
            except (TypeError, ValueError):
                row.append(0.0)
        X_rows.append(row)
        y_rows.append(int(rec.get(LABEL_COLUMN, 0)))

    X = np.array(X_rows, dtype=np.float32)
    y = np.array(y_rows, dtype=np.int32)
    return X, y, feature_cols


# STATS PRINTER

def print_stats(X, y, split_name):
    label_map = {0: "NONE", 1: "LEXICAL", 2: "SYNTAX"}
    print(f"\n  [{split_name}]")
    print(f"    Samples  : {X.shape[0]}")
    print(f"    Features : {X.shape[1]}")
    counts = Counter(y.tolist())
    for lbl in sorted(counts):
        name = label_map.get(lbl, str(lbl))
        print(f"    Label {lbl} ({name:7s}) : {counts[lbl]}")
    if X.size > 0:
        print(f"    mean={X.mean():.4f}  std={X.std():.4f}  "
              f"min={X.min():.4f}  max={X.max():.4f}")


# SAVE

def save_features(X, y, feature_names, split, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    npz_path = os.path.join(out_dir, f"{split}_features.npz")
    np.savez(npz_path, X=X, y=y,
             feature_names=np.array(feature_names, dtype=str))
    print(f"    Saved → {npz_path}  shape={X.shape}")

    csv_path = os.path.join(out_dir, f"{split}_features.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(feature_names + ["label"])
        for row, lbl in zip(X.tolist(), y.tolist()):
            writer.writerow(row + [lbl])
    print(f"    Saved → {csv_path}")

    names_path = os.path.join(out_dir, "feature_names.json")
    with open(names_path, "w", encoding="utf-8") as f:
        json.dump(feature_names, f, indent=2)


# LOAD JSON HELPER

def load_json(path):
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []


# MAIN

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  FEATURE EXTRACTION")
    print("=" * 60)

    train_records = load_json(TRAIN_PATH)
    val_records   = load_json(VAL_PATH)
    test_records  = load_json(TEST_PATH)

    if not train_records:
        print("\n[ERROR] No training data found.")
        print("  Looked in:")
        for p in [
            os.path.join(BASE_DIR, "dataset", "processed", "train_augmented.json"),
            os.path.join(BASE_DIR, "dataset", "processed", "train.json"),
            os.path.join(BASE_DIR, "dataset", "train.json"),
        ]:
            exists = "" if os.path.exists(p) else "✗"
            print(f"    [{exists}] {p}")
        print("\n  Run: py preprocessing.py  first.")
        sys.exit(1)

    print(f"\n  train : {len(train_records)} records  ← {TRAIN_PATH}")
    if val_records:
        print(f"  val   : {len(val_records)} records   ← {VAL_PATH}")
    if test_records:
        print(f"  test  : {len(test_records)} records   ← {TEST_PATH}")

    feat_cols = _discover_feature_columns(train_records)
    print(f"\n  Feature columns discovered : {len(feat_cols)}")
    print(f"  First 10 : {feat_cols[:10]}")

    X_train, y_train, feat_cols = extract_feature_matrix(train_records, feat_cols)

    X_val,  y_val,  _ = (extract_feature_matrix(val_records,  feat_cols)
                          if val_records  else
                          (np.zeros((0, len(feat_cols)), dtype=np.float32),
                           np.zeros(0, dtype=np.int32), feat_cols))

    X_test, y_test, _ = (extract_feature_matrix(test_records, feat_cols)
                          if test_records else
                          (np.zeros((0, len(feat_cols)), dtype=np.float32),
                           np.zeros(0, dtype=np.int32), feat_cols))

    print("\n  ── Feature Matrix Stats ──────────────────────────")
    print_stats(X_train, y_train, "TRAIN")
    if val_records:
        print_stats(X_val,   y_val,   "VAL")
    if test_records:
        print_stats(X_test,  y_test,  "TEST")

    print("\n  ── Saving .npz + .csv Files ──────────────────────")
    save_features(X_train, y_train, feat_cols, "train", OUT_DIR)
    if val_records  and X_val.shape[0]  > 0:
        save_features(X_val,  y_val,  feat_cols, "val",   OUT_DIR)
    if test_records and X_test.shape[0] > 0:
        save_features(X_test, y_test, feat_cols, "test",  OUT_DIR)

    print("\n" + "=" * 60)
    print(f"  Feature extraction complete ✓")
    print(f"  Output : {OUT_DIR}")
    print(f"  Files  : train_features.npz / val_features.npz / test_features.npz")
    print("=" * 60)