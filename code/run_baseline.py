"""Class 4 — Reproducible Baseline & Evaluation Pipeline.

Implements the locked Class 3 experimental protocol:
  - Locked stratified 75/25 split (989 train pool / 330 locked test set)
  - 5 random seeds: [42, 100, 2026, 7, 99]
  - Initial balanced labeled set |L_0| = 20 (10 positive, 10 negative)
  - Passive Random Sampling: +10 samples/step up to 300 labels (29 steps)
  - Zero data leakage: StandardScaler fitted strictly on L_t at each step
  - Base models: Logistic Regression & Random Forest (+ Majority-Class floor)
  - Upper bound: Full-Data models trained on all 989 training pool rows
"""

from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "Heart Attack.csv"
RESULTS_DIR = ROOT / "results"

FEATURES = [
    "age",
    "gender",
    "impluse",
    "pressurehight",
    "pressurelow",
    "glucose",
    "kcm",
    "troponin",
]
TARGET_COL = "class"
SPLIT_SEED = 42
TEST_SIZE = 0.25
SEEDS = [42, 100, 2026, 7, 99]
INIT_PER_CLASS = 10  # |L_0| = 20 balanced
STEP_SIZE = 10
MAX_BUDGET = 300  # 20, 30, ..., 300 -> 29 steps


def build_model(model_name: str, seed: int) -> Pipeline:
    """Return a leak-free Pipeline with fixed hyperparameters."""
    if model_name == "LogisticRegression":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(max_iter=1000, random_state=seed)),
            ]
        )
    if model_name == "RandomForest":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    RandomForestClassifier(
                        n_estimators=100,
                        random_state=seed,
                        n_jobs=1,
                    ),
                ),
            ]
        )
    raise ValueError(f"Unknown model_name: {model_name}")


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray | None) -> dict:
    res = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "pos_recall": float(recall_score(y_true, y_pred, pos_label=1)),
        "neg_recall": float(recall_score(y_true, y_pred, pos_label=0)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)) if y_prob is not None else float("nan"),
    }
    return res


def compute_aulc(budgets: np.ndarray, scores: np.ndarray) -> float:
    """Normalized Area Under Learning Curve (average score over budget span)."""
    trapezoid_fn = getattr(np, "trapezoid", None) or np.trapz
    area = float(trapezoid_fn(scores, budgets))
    return area / float(budgets[-1] - budgets[0])


def first_budget_reaching(budgets: np.ndarray, scores: np.ndarray, threshold: float) -> int | None:
    hits = budgets[scores >= threshold]
    return int(hits[0]) if len(hits) > 0 else None


def load_or_create_split(df: pd.DataFrame, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    split_file = RESULTS_DIR / "locked_split_indices.json"
    if split_file.exists():
        payload = json.loads(split_file.read_text(encoding="utf-8"))
        return np.array(payload["train_indices"], dtype=int), np.array(payload["test_indices"], dtype=int)

    train_idx, test_idx = train_test_split(
        np.arange(len(df)),
        test_size=TEST_SIZE,
        stratify=y,
        random_state=SPLIT_SEED,
    )
    return np.sort(train_idx), np.sort(test_idx)


def run_baseline() -> dict:
    t0 = time.perf_counter()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    X_all = df[FEATURES].to_numpy(dtype=float)
    y_all = (df[TARGET_COL] == "positive").astype(int).to_numpy()

    train_idx, test_idx = load_or_create_split(df, y_all)
    X_pool, y_pool = X_all[train_idx], y_all[train_idx]
    X_test, y_test = X_all[test_idx], y_all[test_idx]

    # 1. Naive Majority-Class Floor
    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X_pool, y_pool)
    dummy_pred = dummy.predict(X_test)
    naive_metrics = evaluate_predictions(y_test, dummy_pred, None)

    # 2. Full-Data Upper Bound (trained on all 989 pool rows across 5 seeds)
    model_names = ["LogisticRegression", "RandomForest"]
    full_data_raw = []
    full_data_summary = {}
    full_data_cms = {}

    for model_name in model_names:
        per_seed = []
        cm_sum = np.zeros((2, 2), dtype=float)
        for seed in SEEDS:
            pipe = build_model(model_name, seed)
            pipe.fit(X_pool, y_pool)
            y_pred = pipe.predict(X_test)
            y_prob = pipe.predict_proba(X_test)[:, 1]
            m = evaluate_predictions(y_test, y_pred, y_prob)
            cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
            cm_sum += cm
            row = {"model": model_name, "seed": seed, "n_labels": int(len(X_pool)), **m}
            per_seed.append(row)
            full_data_raw.append(row)

        pdf = pd.DataFrame(per_seed)
        full_data_summary[model_name] = {
            "n_labels": int(len(X_pool)),
            "accuracy_mean": float(pdf["accuracy"].mean()),
            "accuracy_std": float(pdf["accuracy"].std(ddof=1)),
            "macro_f1_mean": float(pdf["macro_f1"].mean()),
            "macro_f1_std": float(pdf["macro_f1"].std(ddof=1)),
            "roc_auc_mean": float(pdf["roc_auc"].mean()),
            "roc_auc_std": float(pdf["roc_auc"].std(ddof=1)),
            "pos_recall_mean": float(pdf["pos_recall"].mean()),
            "neg_recall_mean": float(pdf["neg_recall"].mean()),
            "target_95_accuracy": float(0.95 * pdf["accuracy"].mean()),
            "target_95_macro_f1": float(0.95 * pdf["macro_f1"].mean()),
        }
        full_data_cms[model_name] = (cm_sum / len(SEEDS)).round(2).tolist()

    pd.DataFrame(full_data_raw).to_csv(RESULTS_DIR / "baseline_full_data_raw.csv", index=False)

    # 3. Passive Random Sampling Loop (20 -> 300 labels, +10/step, 5 seeds)
    curve_rows = []
    random_300_cms = {m: np.zeros((2, 2), dtype=float) for m in model_names}

    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        pos_pool = np.where(y_pool == 1)[0]
        neg_pool = np.where(y_pool == 0)[0]

        init_pos = rng.choice(pos_pool, size=INIT_PER_CLASS, replace=False)
        init_neg = rng.choice(neg_pool, size=INIT_PER_CLASS, replace=False)
        labeled = np.concatenate([init_pos, init_neg])
        rng.shuffle(labeled)

        labeled_set = set(labeled.tolist())
        unlabeled = np.array([i for i in range(len(X_pool)) if i not in labeled_set], dtype=int)
        rng.shuffle(unlabeled)

        # Build exact passive random sequence up to MAX_BUDGET
        n_steps = (MAX_BUDGET - len(labeled)) // STEP_SIZE + 1  # 29 steps: 20..300
        for step in range(n_steps):
            n_cur = len(labeled)
            X_L, y_L = X_pool[labeled], y_pool[labeled]

            for model_name in model_names:
                pipe = build_model(model_name, seed)
                pipe.fit(X_L, y_L)
                y_pred = pipe.predict(X_test)
                y_prob = pipe.predict_proba(X_test)[:, 1]
                m = evaluate_predictions(y_test, y_pred, y_prob)
                curve_rows.append(
                    {
                        "strategy": "RandomSampling",
                        "model": model_name,
                        "seed": seed,
                        "step": step,
                        "n_labels": int(n_cur),
                        **m,
                    }
                )
                if n_cur == MAX_BUDGET:
                    random_300_cms[model_name] += confusion_matrix(y_test, y_pred, labels=[0, 1])

            if n_cur < MAX_BUDGET:
                take = unlabeled[:STEP_SIZE]
                unlabeled = unlabeled[STEP_SIZE:]
                labeled = np.concatenate([labeled, take])

    raw_df = pd.DataFrame(curve_rows)
    raw_df.to_csv(RESULTS_DIR / "baseline_learning_curves_raw.csv", index=False)

    # Aggregate learning curves across seeds
    summary_df = (
        raw_df.groupby(["strategy", "model", "n_labels"], as_index=False)
        .agg(
            accuracy_mean=("accuracy", "mean"),
            accuracy_std=("accuracy", "std"),
            macro_f1_mean=("macro_f1", "mean"),
            macro_f1_std=("macro_f1", "std"),
            roc_auc_mean=("roc_auc", "mean"),
            roc_auc_std=("roc_auc", "std"),
            pos_recall_mean=("pos_recall", "mean"),
            neg_recall_mean=("neg_recall", "mean"),
        )
        .sort_values(["model", "n_labels"])
    )
    summary_df.to_csv(RESULTS_DIR / "baseline_learning_curves_summary.csv", index=False)

    # Compute AULC and Labels-to-95% per seed and aggregated
    baseline_metrics = {}
    for model_name in model_names:
        target_acc = full_data_summary[model_name]["target_95_accuracy"]
        target_f1 = full_data_summary[model_name]["target_95_macro_f1"]

        aulc_accs, aulc_f1s = [], []
        lbl95_accs, lbl95_f1s = [], []
        at_20_acc, at_20_f1 = [], []
        at_100_acc, at_100_f1 = [], []
        at_300_acc, at_300_f1 = [], []

        for seed in SEEDS:
            sub = raw_df[(raw_df["model"] == model_name) & (raw_df["seed"] == seed)].sort_values("n_labels")
            budgets = sub["n_labels"].to_numpy()
            accs = sub["accuracy"].to_numpy()
            f1s = sub["macro_f1"].to_numpy()

            aulc_accs.append(compute_aulc(budgets, accs))
            aulc_f1s.append(compute_aulc(budgets, f1s))
            lbl95_accs.append(first_budget_reaching(budgets, accs, target_acc))
            lbl95_f1s.append(first_budget_reaching(budgets, f1s, target_f1))

            at_20_acc.append(float(sub.loc[sub["n_labels"] == 20, "accuracy"].iloc[0]))
            at_20_f1.append(float(sub.loc[sub["n_labels"] == 20, "macro_f1"].iloc[0]))
            at_100_acc.append(float(sub.loc[sub["n_labels"] == 100, "accuracy"].iloc[0]))
            at_100_f1.append(float(sub.loc[sub["n_labels"] == 100, "macro_f1"].iloc[0]))
            at_300_acc.append(float(sub.loc[sub["n_labels"] == 300, "accuracy"].iloc[0]))
            at_300_f1.append(float(sub.loc[sub["n_labels"] == 300, "macro_f1"].iloc[0]))

        valid_acc_hits = [x for x in lbl95_accs if x is not None]
        valid_f1_hits = [x for x in lbl95_f1s if x is not None]

        baseline_metrics[model_name] = {
            "aulc_accuracy_mean": float(np.mean(aulc_accs)),
            "aulc_accuracy_std": float(np.std(aulc_accs, ddof=1)),
            "aulc_macro_f1_mean": float(np.mean(aulc_f1s)),
            "aulc_macro_f1_std": float(np.std(aulc_f1s, ddof=1)),
            "labels_to_95_accuracy_per_seed": lbl95_accs,
            "labels_to_95_accuracy_mean": float(np.mean(valid_acc_hits)) if valid_acc_hits else None,
            "labels_to_95_accuracy_std": float(np.std(valid_acc_hits, ddof=1)) if len(valid_acc_hits) > 1 else 0.0,
            "labels_to_95_macro_f1_per_seed": lbl95_f1s,
            "labels_to_95_macro_f1_mean": float(np.mean(valid_f1_hits)) if valid_f1_hits else None,
            "labels_to_95_macro_f1_std": float(np.std(valid_f1_hits, ddof=1)) if len(valid_f1_hits) > 1 else 0.0,
            "at_20_accuracy": [float(np.mean(at_20_acc)), float(np.std(at_20_acc, ddof=1))],
            "at_20_macro_f1": [float(np.mean(at_20_f1)), float(np.std(at_20_f1, ddof=1))],
            "at_100_accuracy": [float(np.mean(at_100_acc)), float(np.std(at_100_acc, ddof=1))],
            "at_100_macro_f1": [float(np.mean(at_100_f1)), float(np.std(at_100_f1, ddof=1))],
            "at_300_accuracy": [float(np.mean(at_300_acc)), float(np.std(at_300_acc, ddof=1))],
            "at_300_macro_f1": [float(np.mean(at_300_f1)), float(np.std(at_300_f1, ddof=1))],
            "confusion_matrix_300_mean": (random_300_cms[model_name] / len(SEEDS)).round(2).tolist(),
        }

    elapsed = time.perf_counter() - t0
    report = {
        "protocol": {
            "dataset": DATA_PATH.name,
            "n_total": int(len(df)),
            "n_train_pool": int(len(train_idx)),
            "n_test_locked": int(len(test_idx)),
            "split_seed": SPLIT_SEED,
            "seeds": SEEDS,
            "initial_labels": INIT_PER_CLASS * 2,
            "step_size": STEP_SIZE,
            "max_budget": MAX_BUDGET,
            "n_steps": 29,
            "zero_leakage": "StandardScaler fitted strictly inside sklearn Pipeline on current L_t",
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "processor": platform.processor(),
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "scikit_learn": sklearn.__version__,
            "runtime_seconds": round(elapsed, 3),
        },
        "naive_majority_baseline": naive_metrics,
        "full_data_upper_bound": full_data_summary,
        "full_data_confusion_matrices_mean": full_data_cms,
        "random_sampling_baseline": baseline_metrics,
    }
    (RESULTS_DIR / "baseline_summary.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    print("=== CLASS 4 BASELINE SUMMARY ===")
    print(f"Runtime: {elapsed:.2f}s | Seeds: {SEEDS}")
    print(
        f"Naive Majority-Class Floor: Acc={naive_metrics['accuracy']:.4f}, Macro F1={naive_metrics['macro_f1']:.4f}"
    )
    for m in model_names:
        fd = full_data_summary[m]
        rs = baseline_metrics[m]
        print(f"\n[{m}]")
        print(
            f"  Full-Data (989): Acc={fd['accuracy_mean']:.4f} ± {fd['accuracy_std']:.4f} | "
            f"Macro F1={fd['macro_f1_mean']:.4f} ± {fd['macro_f1_std']:.4f} | "
            f"ROC-AUC={fd['roc_auc_mean']:.4f}"
        )
        print(
            f"  95% Targets:     Acc>={fd['target_95_accuracy']:.4f} | Macro F1>={fd['target_95_macro_f1']:.4f}"
        )
        print(
            f"  Random @20:      Acc={rs['at_20_accuracy'][0]:.4f}±{rs['at_20_accuracy'][1]:.4f} | "
            f"F1={rs['at_20_macro_f1'][0]:.4f}±{rs['at_20_macro_f1'][1]:.4f}"
        )
        print(
            f"  Random @100:     Acc={rs['at_100_accuracy'][0]:.4f}±{rs['at_100_accuracy'][1]:.4f} | "
            f"F1={rs['at_100_macro_f1'][0]:.4f}±{rs['at_100_macro_f1'][1]:.4f}"
        )
        print(
            f"  Random @300:     Acc={rs['at_300_accuracy'][0]:.4f}±{rs['at_300_accuracy'][1]:.4f} | "
            f"F1={rs['at_300_macro_f1'][0]:.4f}±{rs['at_300_macro_f1'][1]:.4f}"
        )
        print(
            f"  AULC (20..300):  Acc={rs['aulc_accuracy_mean']:.4f}±{rs['aulc_accuracy_std']:.4f} | "
            f"F1={rs['aulc_macro_f1_mean']:.4f}±{rs['aulc_macro_f1_std']:.4f}"
        )
        print(
            f"  Labels to 95%:   Acc={rs['labels_to_95_accuracy_mean']} ({rs['labels_to_95_accuracy_per_seed']}) | "
            f"F1={rs['labels_to_95_macro_f1_mean']} ({rs['labels_to_95_macro_f1_per_seed']})"
        )
        print(f"  Full-Data CM (rows=true [0,1], cols=pred [0,1]): {full_data_cms[m]}")
        print(f"  Random @300 CM: {rs['confusion_matrix_300_mean']}")

    return report


if __name__ == "__main__":
    run_baseline()
