"""
lstm_model.py
═══════════════════════════════════════════════════════════════════
Bidirectional LSTM model for:
  Task A — Error Classification   (LEXICAL vs SYNTAX)
  Task B — Error Line Localization (sequence labeling)

Architecture:
  Embedding → BiLSTM stack → 
    ┌─ Classification head  (global pooled → Dense → Softmax)
    └─ Sequence labeling head (per-token Dense → Sigmoid)

Pure NumPy/Python implementation (no deep-learning framework required
for the reference version). Swap the `forward()` internals for
PyTorch/TF equivalents when running on GPU.
"""

import json, os, math, random
import numpy as np
from typing import List, Tuple, Dict, Optional

# ── Hyper-parameters ────────────────────────────────────────────
class Config:
    vocab_size        = 5000   # set from vocab file at runtime
    embed_dim         = 64
    hidden_dim        = 128
    num_layers        = 2
    dropout           = 0.3
    num_classes       = 3      # 0=none, 1=lexical, 2=syntax
    max_seq_len       = 512
    batch_size        = 32
    learning_rate     = 1e-3
    num_epochs        = 20
    patience          = 4      # early stopping
    clip_grad_norm    = 5.0
    seed              = 42

cfg = Config()
np.random.seed(cfg.seed)
random.seed(cfg.seed)

PROCESSED_DIR = "dataset/processed"
MODEL_DIR     = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


# ════════════════════════════════════════════════════════════════
# NUMPY LSTM CELL (reference — replace with nn.LSTM in PyTorch)
# ════════════════════════════════════════════════════════════════

def sigmoid(x):  return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
def tanh(x):     return np.tanh(np.clip(x, -500, 500))

class LSTMCell:
    """Single LSTM cell (forward only, for illustrative purposes)."""
    def __init__(self, input_dim: int, hidden_dim: int):
        scale = math.sqrt(1.0 / hidden_dim)
        self.Wf = np.random.uniform(-scale, scale, (hidden_dim, input_dim + hidden_dim))
        self.Wi = np.random.uniform(-scale, scale, (hidden_dim, input_dim + hidden_dim))
        self.Wc = np.random.uniform(-scale, scale, (hidden_dim, input_dim + hidden_dim))
        self.Wo = np.random.uniform(-scale, scale, (hidden_dim, input_dim + hidden_dim))
        self.bf = np.zeros(hidden_dim)
        self.bi = np.zeros(hidden_dim)
        self.bc = np.zeros(hidden_dim)
        self.bo = np.zeros(hidden_dim)

    def forward(self, x: np.ndarray, h_prev: np.ndarray, c_prev: np.ndarray):
        combined = np.concatenate([x, h_prev])
        f = sigmoid(self.Wf @ combined + self.bf)
        i = sigmoid(self.Wi @ combined + self.bi)
        c_hat = tanh(self.Wc @ combined + self.bc)
        o = sigmoid(self.Wo @ combined + self.bo)
        c = f * c_prev + i * c_hat
        h = o * tanh(c)
        return h, c

    def get_params(self):
        return {
            "Wf": self.Wf.tolist(), "Wi": self.Wi.tolist(),
            "Wc": self.Wc.tolist(), "Wo": self.Wo.tolist(),
            "bf": self.bf.tolist(), "bi": self.bi.tolist(),
            "bc": self.bc.tolist(), "bo": self.bo.tolist(),
        }


class BiLSTMLayer:
    """One bidirectional LSTM layer."""
    def __init__(self, input_dim: int, hidden_dim: int):
        self.fwd = LSTMCell(input_dim, hidden_dim)
        self.bwd = LSTMCell(input_dim, hidden_dim)
        self.hidden_dim = hidden_dim

    def forward(self, embeddings: np.ndarray) -> np.ndarray:
        """
        embeddings: (seq_len, embed_dim)
        returns:    (seq_len, 2 * hidden_dim)
        """
        T = len(embeddings)
        h_dim = self.hidden_dim

        h_f = np.zeros(h_dim); c_f = np.zeros(h_dim)
        fwd_outs = []
        for t in range(T):
            h_f, c_f = self.fwd.forward(embeddings[t], h_f, c_f)
            fwd_outs.append(h_f.copy())

        h_b = np.zeros(h_dim); c_b = np.zeros(h_dim)
        bwd_outs = []
        for t in reversed(range(T)):
            h_b, c_b = self.bwd.forward(embeddings[t], h_b, c_b)
            bwd_outs.append(h_b.copy())
        bwd_outs.reverse()

        return np.column_stack([fwd_outs, bwd_outs])  # (T, 2*H)


# ════════════════════════════════════════════════════════════════
# FULL MODEL
# ════════════════════════════════════════════════════════════════

class BiLSTMErrorModel:
    """
    BiLSTM model with dual heads:
      - Classification head  → error type (LEXICAL / SYNTAX)
      - Sequence label head  → per-token error indicator
    """
    def __init__(self, vocab_size: int, embed_dim: int, hidden_dim: int,
                 num_layers: int, num_classes: int):
        self.embed_dim  = embed_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        # Embedding matrix
        scale = math.sqrt(1.0 / embed_dim)
        self.embedding = np.random.uniform(-scale, scale, (vocab_size, embed_dim))

        # BiLSTM stack
        self.layers: List[BiLSTMLayer] = []
        in_dim = embed_dim
        for _ in range(num_layers):
            self.layers.append(BiLSTMLayer(in_dim, hidden_dim))
            in_dim = hidden_dim * 2

        out_dim = hidden_dim * 2   # bidirectional output dim

        # Classification head weights
        scale_c = math.sqrt(1.0 / out_dim)
        self.W_cls = np.random.uniform(-scale_c, scale_c, (num_classes, out_dim))
        self.b_cls = np.zeros(num_classes)

        # Sequence labeling head weights
        scale_s = math.sqrt(1.0 / out_dim)
        self.W_seq = np.random.uniform(-scale_s, scale_s, (1, out_dim))
        self.b_seq = np.zeros(1)

    def forward(self, token_ids: List[int]) -> Tuple[np.ndarray, np.ndarray]:
        """
        token_ids: list of int token indices (length ≤ MAX_SEQ_LEN)

        Returns:
          class_logits : (num_classes,)    — classification logits
          seq_probs    : (seq_len,)         — per-token error probability
        """
        # Embedding lookup
        ids = np.array(token_ids, dtype=np.int32)
        ids = np.clip(ids, 0, self.embedding.shape[0] - 1)
        x = self.embedding[ids]   # (T, D)

        # BiLSTM stack
        h = x
        for layer in self.layers:
            h = layer.forward(h)   # (T, 2*H)

        # Global mean pooling for classification
        pooled = h.mean(axis=0)            # (2*H,)
        class_logits = self.W_cls @ pooled + self.b_cls   # (C,)

        # Per-token scoring for sequence labeling
        seq_logits = (h @ self.W_seq.T).squeeze(-1) + self.b_seq[0]  # (T,)
        seq_probs  = sigmoid(seq_logits)

        return class_logits, seq_probs

    def softmax(self, logits: np.ndarray) -> np.ndarray:
        e = np.exp(logits - logits.max())
        return e / e.sum()

    def predict(self, token_ids: List[int]) -> Dict:
        logits, seq_probs = self.forward(token_ids)
        probs    = self.softmax(logits)
        cls_pred = int(np.argmax(probs))
        label_map = {0: "NONE", 1: "LEXICAL", 2: "SYNTAX"}
        return {
            "predicted_class":  cls_pred,
            "predicted_label":  label_map.get(cls_pred, "UNKNOWN"),
            "class_probs":      probs.tolist(),
            "error_token_probs": seq_probs.tolist(),
            "predicted_error_positions": [
                i for i, p in enumerate(seq_probs) if p > 0.5
            ],
        }

    def save(self, path: str):
        """Serialize model weights to JSON."""
        weights = {
            "embedding": self.embedding.tolist(),
            "W_cls": self.W_cls.tolist(),
            "b_cls": self.b_cls.tolist(),
            "W_seq": self.W_seq.tolist(),
            "b_seq": self.b_seq.tolist(),
            "bilstm_layers": [
                {
                    "fwd": l.fwd.get_params(),
                    "bwd": l.bwd.get_params(),
                } for l in self.layers
            ],
        }
        with open(path, "w") as f:
            json.dump(weights, f)
        print(f"  [Model] Saved → {path}")


# ════════════════════════════════════════════════════════════════
# LOSS FUNCTIONS
# ════════════════════════════════════════════════════════════════

def cross_entropy_loss(logits: np.ndarray, true_class: int) -> float:
    probs = np.exp(logits - logits.max())
    probs /= probs.sum()
    return -math.log(probs[true_class] + 1e-12)

def binary_cross_entropy(probs: np.ndarray, labels: np.ndarray) -> float:
    eps = 1e-12
    return float(-np.mean(
        labels * np.log(probs + eps) + (1 - labels) * np.log(1 - probs + eps)
    ))

def combined_loss(cls_logits, seq_probs, cls_label, seq_labels,
                  alpha=0.7, beta=0.3) -> float:
    l_cls = cross_entropy_loss(cls_logits, cls_label)
    l_seq = binary_cross_entropy(seq_probs, np.array(seq_labels[:len(seq_probs)]))
    return alpha * l_cls + beta * l_seq


# ════════════════════════════════════════════════════════════════
# SIMPLE TRAINING LOOP (demonstration — use PyTorch for real training)
# ════════════════════════════════════════════════════════════════

def evaluate(model: BiLSTMErrorModel, samples: List[dict]) -> Dict:
    correct_cls   = 0
    total         = 0
    total_loss    = 0.0
    tp = {1: 0, 2: 0}; fp = {1: 0, 2: 0}; fn = {1: 0, 2: 0}

    for s in samples:
        ids    = s["tok_input_ids"][:cfg.max_seq_len]
        label  = s["class_label"]
        s_lbls = s["seq_labels"][:len(ids)]

        logits, seq_probs = model.forward(ids)
        pred = int(np.argmax(model.softmax(logits)))

        total      += 1
        total_loss += combined_loss(logits, seq_probs, label, s_lbls)
        if pred == label: correct_cls += 1

        # Per-class precision / recall bookkeeping
        for c in [1, 2]:
            if pred == c and label == c:  tp[c] += 1
            if pred == c and label != c:  fp[c] += 1
            if pred != c and label == c:  fn[c] += 1

    acc = correct_cls / max(1, total)
    metrics = {"accuracy": round(acc, 4), "avg_loss": round(total_loss / max(1, total), 4)}
    for c, name in [(1, "LEXICAL"), (2, "SYNTAX")]:
        prec = tp[c] / max(1, tp[c] + fp[c])
        rec  = tp[c] / max(1, tp[c] + fn[c])
        f1   = 2 * prec * rec / max(1e-9, prec + rec)
        metrics[f"{name}_precision"] = round(prec, 4)
        metrics[f"{name}_recall"]    = round(rec,  4)
        metrics[f"{name}_f1"]        = round(f1,   4)
    return metrics


def train_model():
    """
    Main training entry point.
    NOTE: This is a simplified gradient-free evaluation demo.
    For real gradient-based training, use the PyTorch version in
    transformer_model.py or plug this architecture into an autograd engine.
    """
    print("\n" + "=" * 60)
    print("  BiLSTM MODEL — EVALUATION RUN")
    print("=" * 60)

    # Load vocab
    vocab_path = os.path.join(PROCESSED_DIR, "vocab_token.json")
    if not os.path.exists(vocab_path):
        print("  [ERROR] Run preprocess.py first.")
        return
    with open(vocab_path) as f:
        vocab = json.load(f)
    cfg.vocab_size = len(vocab["token2id"])
    print(f"  Vocab size: {cfg.vocab_size}")

    # Load data
    def load_split(name):
        p = os.path.join(PROCESSED_DIR, f"{name}.json")
        if not os.path.exists(p): return []
        with open(p) as f: return json.load(f)

    train_data = load_split("train")
    val_data   = load_split("val")
    test_data  = load_split("test")
    print(f"  Data: train={len(train_data)}  val={len(val_data)}  test={len(test_data)}")

    # Initialise model
    model = BiLSTMErrorModel(
        vocab_size  = cfg.vocab_size,
        embed_dim   = cfg.embed_dim,
        hidden_dim  = cfg.hidden_dim,
        num_layers  = cfg.num_layers,
        num_classes = cfg.num_classes,
    )

    # Evaluate (untrained baseline)
    if val_data:
        metrics = evaluate(model, val_data[:50])   # limit for speed
        print(f"\n  [Baseline] Validation metrics (untrained model):")
        for k, v in metrics.items():
            print(f"    {k:30s}: {v}")

    # Save initial model checkpoint
    model.save(os.path.join(MODEL_DIR, "bilstm_init.json"))

    print("\n  NOTE: For full gradient training, run transformer_model.py")
    print("  which uses PyTorch with AdamW + cosine LR schedule.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    train_model()