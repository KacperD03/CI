"""Generate clean, high-DPI Class 4 figures for prezentacja.html."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
PLOTS_DIR = RESULTS_DIR / "plots"

# Palette matching prezentacja.html
PRIMARY = "#1d4ed8"
PRIMARY_LIGHT = "#dbeafe"
EMERALD = "#047857"
EMERALD_LIGHT = "#d1fae5"
AMBER = "#b45309"
AMBER_LIGHT = "#fef3c7"
RED = "#dc2626"
SLATE = "#334155"
MUTED = "#64748b"
GRID = "#e2e8f0"
BG = "#ffffff"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "axes.edgecolor": "#cbd5e1",
            "axes.labelcolor": SLATE,
            "axes.titlecolor": "#0f172a",
            "xtick.color": SLATE,
            "ytick.color": SLATE,
            "text.color": "#0f172a",
            "font.family": "DejaVu Sans",
            "font.size": 10.5,
            "axes.titlesize": 12.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 10.5,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linestyle": "--",
            "grid.linewidth": 0.7,
            "legend.frameon": True,
            "legend.facecolor": "#ffffff",
            "legend.edgecolor": "#e2e8f0",
        }
    )


def plot_data_audit() -> None:
    audit = json.loads((RESULTS_DIR / "data_audit_report.json").read_text(encoding="utf-8"))
    feat_df = pd.read_csv(RESULTS_DIR / "data_audit_feature_power.csv")
    feat_df = feat_df.sort_values("univariate_roc_auc_train", ascending=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.3), dpi=220)
    fig.subplots_adjust(wspace=0.42, left=0.12, right=0.97, top=0.84, bottom=0.15)

    # Panel 1: Univariate feature power (Train pool only)
    colors = []
    for f, v in zip(feat_df["feature"], feat_df["univariate_roc_auc_train"]):
        if v >= 0.85:
            colors.append(PRIMARY)
        elif v >= 0.60:
            colors.append(EMERALD)
        else:
            colors.append("#94a3b8")

    bars1 = ax1.barh(feat_df["feature"], feat_df["univariate_roc_auc_train"], color=colors, height=0.64, edgecolor="none")
    ax1.axvline(0.50, color=MUTED, linestyle=":", linewidth=1.3, label="Random (0.50)")
    ax1.set_xlim(0.45, 1.00)
    ax1.set_xlabel("Single-Feature ROC-AUC (Train Pool Only)")
    ax1.set_title("1. Which Features Predict Heart Attack?")
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(False)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    for bar, val in zip(bars1, feat_df["univariate_roc_auc_train"]):
        ax1.text(
            val + 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}",
            va="center",
            ha="left",
            fontsize=9.5,
            fontweight="bold",
            color="#0f172a" if val >= 0.60 else MUTED,
        )

    # Panel 2: Anomalies found in dataset
    anom = audit["anomalies"]
    anom_items = [
        ("Low BP >= High BP\n(impossible pressure)", anom["pressurelow_ge_pressurehight"], RED),
        ("High BP < 70\n(extreme low systolic)", anom["pressurehight_lt_70"], AMBER),
        ("Heart Rate = 1111\n(data entry error)", anom["impluse_gt_220"], RED),
        ("Age < 18 or > 100\n(extreme age)", anom["age_lt_18_or_gt_100"], "#64748b"),
        ("Heart Rate = 20\n(extreme low pulse)", anom["impluse_lt_35"], AMBER),
    ]
    anom_items.reverse()
    labels = [x[0] for x in anom_items]
    counts = [x[1] for x in anom_items]
    acolors = [x[2] for x in anom_items]

    bars2 = ax2.barh(labels, counts, color=acolors, height=0.62)
    ax2.set_xlim(0, 14.0)
    ax2.set_xlabel("Number of Patient Rows (out of 1,319)")
    ax2.set_title("2. Real Measurement Errors Found")
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(False)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    for bar, val in zip(bars2, counts):
        ax2.text(
            val + 0.25,
            bar.get_y() + bar.get_height() / 2,
            f"{val} rows",
            va="center",
            ha="left",
            fontsize=9.5,
            fontweight="bold",
            color="#0f172a",
        )

    fig.savefig(PLOTS_DIR / "fig1_data_audit.png", dpi=220, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def plot_baseline_curves() -> None:
    summary_df = pd.read_csv(RESULTS_DIR / "baseline_learning_curves_summary.csv")
    report = json.loads((RESULTS_DIR / "baseline_summary.json").read_text(encoding="utf-8"))

    naive = report["naive_majority_baseline"]
    full = report["full_data_upper_bound"]
    rs = report["random_sampling_baseline"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.35), dpi=220)
    fig.subplots_adjust(wspace=0.24, left=0.07, right=0.98, top=0.83, bottom=0.16)

    panels = [
        (ax1, "macro_f1", "Macro F1-Score (Test Set, 330 Patients)", "Macro F1 Learning Curve (5 Seeds)"),
        (ax2, "accuracy", "Accuracy (Test Set, 330 Patients)", "Accuracy Learning Curve (5 Seeds)"),
    ]

    model_styles = {
        "RandomForest": ("Random Forest (Random Sampling)", EMERALD, "o"),
        "LogisticRegression": ("Logistic Regression (Random Sampling)", PRIMARY, "s"),
    }

    for ax, metric, ylabel, title in panels:
        for model_name, (label, color, marker) in model_styles.items():
            sub = summary_df[summary_df["model"] == model_name].sort_values("n_labels")
            x = sub["n_labels"].to_numpy()
            mean = sub[f"{metric}_mean"].to_numpy()
            std = sub[f"{metric}_std"].to_numpy()

            ax.plot(x, mean, color=color, linewidth=2.3, marker=marker, markersize=4, markevery=3, label=label)
            ax.fill_between(x, np.clip(mean - std, 0, 1), np.clip(mean + std, 0, 1), color=color, alpha=0.14)

            # Full-Data Upper Bound line
            fd_val = full[model_name][f"{metric}_mean"]
            ax.axhline(fd_val, color=color, linestyle="--", linewidth=1.35, alpha=0.85)

            # 95% Target line
            t95_val = full[model_name][f"target_95_{metric}"]
            ax.axhline(t95_val, color=color, linestyle=":", linewidth=1.1, alpha=0.65)

        # Naive Majority Floor
        naive_val = naive[metric]
        ax.axhline(naive_val, color="#94a3b8", linestyle="-.", linewidth=1.25, label=f"Majority Class Floor ({naive_val:.2f})")

        # Clean inline annotations on right side for Upper Bounds
        rf_fd = full["RandomForest"][f"{metric}_mean"]
        lr_fd = full["LogisticRegression"][f"{metric}_mean"]
        ax.text(302, rf_fd + 0.008, f"RF Full (989): {rf_fd:.1%}", color=EMERALD, fontsize=8.5, fontweight="bold", ha="right", va="bottom")
        ax.text(302, lr_fd + 0.010, f"LogReg Full (989): {lr_fd:.1%}", color=PRIMARY, fontsize=8.5, fontweight="bold", ha="right", va="bottom")

        # Annotate average labels to reach 95% target
        rf_95_lbl = rs["RandomForest"][f"labels_to_95_{metric}_mean"]
        lr_95_lbl = rs["LogisticRegression"][f"labels_to_95_{metric}_mean"]
        rf_t95 = full["RandomForest"][f"target_95_{metric}"]
        lr_t95 = full["LogisticRegression"][f"target_95_{metric}"]

        ax.scatter([rf_95_lbl], [rf_t95], color=EMERALD, s=46, zorder=6, edgecolor="#ffffff", linewidth=1.2)
        rf_text_pos = (rf_95_lbl + 36, rf_t95 - 0.075) if metric == "macro_f1" else (rf_95_lbl + 42, rf_t95 - 0.062)
        ax.annotate(
            f"95% target: ~{rf_95_lbl:.0f} labels",
            xy=(rf_95_lbl, rf_t95),
            xytext=rf_text_pos,
            fontsize=8.5,
            fontweight="bold",
            color=EMERALD,
            arrowprops=dict(arrowstyle="->", color=EMERALD, lw=1.1),
            bbox=dict(boxstyle="round,pad=0.25", fc="#f0fdf4", ec="#bbf7d0", lw=0.8),
        )

        ax.scatter([lr_95_lbl], [lr_t95], color=PRIMARY, s=46, zorder=6, edgecolor="#ffffff", linewidth=1.2)
        lr_text_pos = (lr_95_lbl + 38, lr_t95 - 0.105) if metric == "macro_f1" else (lr_95_lbl + 22, lr_t95 + 0.088)
        ax.annotate(
            f"95% target: ~{lr_95_lbl:.0f} labels",
            xy=(lr_95_lbl, lr_t95),
            xytext=lr_text_pos,
            fontsize=8.5,
            fontweight="bold",
            color=PRIMARY,
            arrowprops=dict(arrowstyle="->", color=PRIMARY, lw=1.1),
            bbox=dict(boxstyle="round,pad=0.25", fc="#eff6ff", ec="#bfdbfe", lw=0.8),
        )

        ax.set_xlim(15, 308)
        ax.set_ylim(0.32 if metric == "macro_f1" else 0.55, 1.04)
        ax.set_xlabel("Number of Labeled Patients (Budget)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(loc="lower right", fontsize=8.3)

    fig.savefig(PLOTS_DIR / "fig2_baseline_curves.png", dpi=220, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def plot_diagnostics() -> None:
    report = json.loads((RESULTS_DIR / "baseline_summary.json").read_text(encoding="utf-8"))
    seeds = report["protocol"]["seeds"]
    rs = report["random_sampling_baseline"]
    cms = report["full_data_confusion_matrices_mean"]

    fig = plt.figure(figsize=(11.6, 4.15), dpi=220)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.45, 0.9, 0.9], wspace=0.34, left=0.06, right=0.98, top=0.83, bottom=0.16)

    # Panel 1: Per-seed labels needed to reach 95% of Full-Data Macro F1
    ax1 = fig.add_subplot(gs[0, 0])
    x = np.arange(len(seeds))
    w = 0.36
    lr_vals = rs["LogisticRegression"]["labels_to_95_macro_f1_per_seed"]
    rf_vals = rs["RandomForest"]["labels_to_95_macro_f1_per_seed"]

    b1 = ax1.bar(x - w / 2, lr_vals, width=w, color=PRIMARY, label=f"LogReg (mean = {np.mean(lr_vals):.0f})")
    b2 = ax1.bar(x + w / 2, rf_vals, width=w, color=EMERALD, label=f"Random Forest (mean = {np.mean(rf_vals):.0f})")

    ax1.axhline(np.mean(lr_vals), color=PRIMARY, linestyle="--", linewidth=1.1, alpha=0.7)
    ax1.axhline(np.mean(rf_vals), color=EMERALD, linestyle="--", linewidth=1.1, alpha=0.7)

    for bar in list(b1) + list(b2):
        h = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            h + 4,
            f"{int(h)}",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
        )

    ax1.set_xticks(x)
    ax1.set_xticklabels([f"Seed\n{s}" for s in seeds], fontsize=9)
    ax1.set_ylim(0, 305)
    ax1.set_ylabel("Labels Needed for 95% Macro F1")
    ax1.set_title("1. Seed Variance: Why 1 Seed Is Not Enough")
    ax1.xaxis.grid(False)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper center", ncol=2, fontsize=8.3, frameon=True)

    # Panels 2 & 3: Confusion Matrices (Full-Data on Locked 330 Test Set)
    cm_specs = [
        (fig.add_subplot(gs[0, 1]), "LogisticRegression", "2. LogReg Full-Data\n(77 / 330 Errors)", "Blues"),
        (fig.add_subplot(gs[0, 2]), "RandomForest", "3. Random Forest Full-Data\n(8 / 330 Errors)", "Greens"),
    ]
    for ax, mname, title, cmap in cm_specs:
        cm = np.array(cms[mname], dtype=float)
        ax.imshow(cm, cmap=cmap, vmin=0, vmax=210)
        ax.grid(False)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Pred\nNeg", "Pred\nPos"], fontsize=9)
        ax.set_yticklabels(["True\nNeg", "True\nPos"], fontsize=9)
        ax.set_title(title, fontsize=11)

        labels_cm = [["TN", "FP"], ["FN", "TP"]]
        for i in range(2):
            for j in range(2):
                val = cm[i, j]
                txt_color = "#ffffff" if val > 115 else "#0f172a"
                ax.text(
                    j,
                    i,
                    f"{int(round(val))}\n({labels_cm[i][j]})",
                    ha="center",
                    va="center",
                    fontsize=10.5,
                    fontweight="bold",
                    color=txt_color,
                )

    fig.savefig(PLOTS_DIR / "fig3_diagnostics.png", dpi=220, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def main() -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    setup_style()
    plot_data_audit()
    plot_baseline_curves()
    plot_diagnostics()
    print("Saved 3 plots to:", PLOTS_DIR)


if __name__ == "__main__":
    main()
