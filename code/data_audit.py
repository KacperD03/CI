"""Class 4 — Data Audit for Heart Attack Classification Dataset.

Checks schema, missing values, duplicates, class balance, physiological
anomalies/outliers, and feature-target separation (computed on the 75%
training pool only to avoid test-set leakage).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "Heart Attack.csv"
RESULTS_DIR = ROOT / "results"
PLOTS_DIR = RESULTS_DIR / "plots"

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


def run_audit() -> dict:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    y = (df[TARGET_COL] == "positive").astype(int)

    # Locked 75/25 stratified split (same split used in baseline & AL experiments)
    train_idx, test_idx = train_test_split(
        df.index.to_numpy(),
        test_size=TEST_SIZE,
        stratify=y,
        random_state=SPLIT_SEED,
    )
    train_df = df.loc[train_idx]
    test_df = df.loc[test_idx]

    # Save locked split indices for reproducibility across Classes 4-6
    split_payload = {
        "split_seed": SPLIT_SEED,
        "test_size": TEST_SIZE,
        "n_total": int(len(df)),
        "n_train_pool": int(len(train_idx)),
        "n_test_locked": int(len(test_idx)),
        "train_positive": int((train_df[TARGET_COL] == "positive").sum()),
        "train_negative": int((train_df[TARGET_COL] == "negative").sum()),
        "test_positive": int((test_df[TARGET_COL] == "positive").sum()),
        "test_negative": int((test_df[TARGET_COL] == "negative").sum()),
        "train_indices": [int(i) for i in sorted(train_idx)],
        "test_indices": [int(i) for i in sorted(test_idx)],
    }
    (RESULTS_DIR / "locked_split_indices.json").write_text(
        json.dumps(split_payload, indent=2), encoding="utf-8"
    )

    # Basic integrity checks
    missing_per_col = {col: int(df[col].isna().sum()) for col in df.columns}
    n_exact_duplicates = int(df.duplicated().sum())
    n_feature_duplicates = int(df.duplicated(subset=FEATURES).sum())
    # Check if any identical feature rows exist across train/test split
    train_feat_tuples = set(map(tuple, train_df[FEATURES].to_numpy()))
    test_feat_tuples = set(map(tuple, test_df[FEATURES].to_numpy()))
    cross_split_exact_feature_overlap = len(train_feat_tuples & test_feat_tuples)

    # Summary stats across full dataset
    stats_rows = []
    for col in FEATURES:
        s = df[col]
        stats_rows.append(
            {
                "feature": col,
                "min": float(s.min()),
                "q25": float(s.quantile(0.25)),
                "median": float(s.median()),
                "mean": float(s.mean()),
                "std": float(s.std()),
                "q75": float(s.quantile(0.75)),
                "q99": float(s.quantile(0.99)),
                "max": float(s.max()),
                "skewness": float(s.skew()),
            }
        )
    stats_df = pd.DataFrame(stats_rows)
    stats_df.to_csv(RESULTS_DIR / "data_audit_summary.csv", index=False)

    # Physiological / domain anomaly checks
    anomalies = {
        "impluse_gt_220": df[df["impluse"] > 220][["age", "impluse", "pressurehight", "pressurelow", "kcm", "troponin", "class"]].to_dict(orient="records"),
        "impluse_lt_35": df[df["impluse"] < 35][["age", "impluse", "class"]].to_dict(orient="records"),
        "pressurelow_ge_pressurehight": df[df["pressurelow"] >= df["pressurehight"]][["age", "pressurehight", "pressurelow", "class"]].to_dict(orient="records"),
        "pressurehight_lt_70": df[df["pressurehight"] < 70][["age", "pressurehight", "pressurelow", "class"]].to_dict(orient="records"),
        "pressurelow_lt_40": df[df["pressurelow"] < 40][["age", "pressurehight", "pressurelow", "class"]].to_dict(orient="records"),
        "age_lt_18_or_gt_100": df[(df["age"] < 18) | (df["age"] > 100)][["age", "class"]].to_dict(orient="records"),
        "glucose_gt_400": df[df["glucose"] > 400][["age", "glucose", "class"]].to_dict(orient="records"),
        "kcm_ge_250_count": int((df["kcm"] >= 250).sum()),
        "troponin_ge_5_count": int((df["troponin"] >= 5).sum()),
    }

    # Check how many impluse > 300 rows fall into train pool vs test set
    impluse_gt_300_train = int((train_df["impluse"] > 300).sum())
    impluse_gt_300_test = int((test_df["impluse"] > 300).sum())

    # Univariate predictive power on TRAINING POOL ONLY (no test leakage)
    y_train = (train_df[TARGET_COL] == "positive").astype(int)
    univariate = []
    for col in FEATURES:
        spearman = float(train_df[col].corr(y_train, method="spearman"))
        auc = float(roc_auc_score(y_train, train_df[col]))
        auc_sym = max(auc, 1.0 - auc)
        univariate.append(
            {
                "feature": col,
                "spearman_corr_train": round(spearman, 4),
                "univariate_roc_auc_train": round(auc_sym, 4),
                "direction": "higher -> positive" if auc >= 0.5 else "lower -> positive",
            }
        )
    univariate.sort(key=lambda r: r["univariate_roc_auc_train"], reverse=True)
    pd.DataFrame(univariate).to_csv(RESULTS_DIR / "data_audit_feature_power.csv", index=False)

    audit_report = {
        "dataset_file": DATA_PATH.name,
        "n_rows": int(len(df)),
        "n_features": len(FEATURES),
        "features": FEATURES,
        "missing_values_total": int(sum(missing_per_col.values())),
        "missing_per_col": missing_per_col,
        "exact_duplicate_rows": n_exact_duplicates,
        "feature_duplicate_rows": n_feature_duplicates,
        "cross_split_exact_feature_overlap": cross_split_exact_feature_overlap,
        "class_balance": {
            "positive": int((df[TARGET_COL] == "positive").sum()),
            "negative": int((df[TARGET_COL] == "negative").sum()),
            "positive_pct": round(float((df[TARGET_COL] == "positive").mean() * 100), 2),
            "negative_pct": round(float((df[TARGET_COL] == "negative").mean() * 100), 2),
        },
        "split_summary": {
            "n_train_pool": split_payload["n_train_pool"],
            "n_test_locked": split_payload["n_test_locked"],
            "train_positive_pct": round(split_payload["train_positive"] / split_payload["n_train_pool"] * 100, 2),
            "test_positive_pct": round(split_payload["test_positive"] / split_payload["n_test_locked"] * 100, 2),
            "impluse_gt_300_in_train": impluse_gt_300_train,
            "impluse_gt_300_in_test": impluse_gt_300_test,
        },
        "anomalies": {
            k: (len(v) if isinstance(v, list) else v) for k, v in anomalies.items()
        },
        "anomaly_examples": anomalies,
        "univariate_feature_power_train_only": univariate,
    }

    (RESULTS_DIR / "data_audit_report.json").write_text(
        json.dumps(audit_report, indent=2), encoding="utf-8"
    )

    print("=== DATA AUDIT SUMMARY ===")
    print(f"Rows: {audit_report['n_rows']}, Features: {audit_report['n_features']}")
    print(f"Missing values: {audit_report['missing_values_total']}")
    print(f"Exact duplicates: {n_exact_duplicates} (feature-only: {n_feature_duplicates}, cross-split overlap: {cross_split_exact_feature_overlap})")
    print(f"Class balance: positive={audit_report['class_balance']['positive']} ({audit_report['class_balance']['positive_pct']}%), negative={audit_report['class_balance']['negative']} ({audit_report['class_balance']['negative_pct']}%)")
    print(f"Split: train_pool={split_payload['n_train_pool']} ({audit_report['split_summary']['train_positive_pct']}% pos), test_locked={split_payload['n_test_locked']} ({audit_report['split_summary']['test_positive_pct']}% pos)")
    print(f"impluse > 300: train={impluse_gt_300_train}, test={impluse_gt_300_test}")
    print("\n--- Feature Summary Stats ---")
    print(stats_df.to_string(index=False))
    print("\n--- Anomaly Counts ---")
    for k, v in audit_report["anomalies"].items():
        print(f"  {k}: {v}")
    print("\n--- Anomaly Details ---")
    for k, v in anomalies.items():
        if isinstance(v, list) and len(v) > 0:
            print(f"  {k}: {v[:10]}")
    print("\n--- Univariate Feature Power (Train Pool Only) ---")
    print(pd.DataFrame(univariate).to_string(index=False))

    return audit_report


if __name__ == "__main__":
    run_audit()
