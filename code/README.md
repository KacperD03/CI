# Pool-Based Active Learning for Medical Classification — Code

Solo project by **Kacper Drożdż** (Computational Intelligence, Project Classes 2026/27, AGH University).

## Dataset

- **Name:** Heart Attack Classification Dataset (Kaggle)
- **File expected at project root:** `Heart Attack.csv` (1,319 patients, 8 clinical features, binary target `class`: `positive` / `negative`, 0 missing values).
- **Source:** Kaggle Heart Attack Classification Dataset (place `Heart Attack.csv` in the repository root; raw training data is excluded from the final code zip per submission guidelines).

## Environment Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r code\requirements.txt
```

## Exact Run Commands (Class 4 — Data Audit & Reproducible Baseline)

Run from the project root directory:

```powershell
# 1. Data audit & locked 75/25 stratified split (saved to results/locked_split_indices.json)
.\.venv\Scripts\python code\data_audit.py

# 2. Reproducible baseline: Full-Data Upper Bound + Passive Random Sampling (5 seeds: 42, 100, 2026, 7, 99)
.\.venv\Scripts\python code\run_baseline.py

# 3. Generate Class 4 plots for the presentation
.\.venv\Scripts\python code\make_class4_plots.py
```

## Saved Outputs (`results/`)

- `locked_split_indices.json` — Frozen 75% training pool (989 rows) / 25% test set (330 rows), stratified (`split_seed=42`).
- `data_audit_report.json`, `data_audit_summary.csv`, `data_audit_feature_power.csv` — Data quality, anomaly counts, and training-only univariate feature power.
- `baseline_full_data_raw.csv`, `baseline_learning_curves_raw.csv`, `baseline_learning_curves_summary.csv`, `baseline_summary.json` — Raw per-seed metrics, aggregated learning curves (`mean ± std`), AULC, labels-to-95%, confusion matrices, environment versions, and runtime.
- `plots/` — Publication-ready PNG figures embedded in `prezentacja.html`.
