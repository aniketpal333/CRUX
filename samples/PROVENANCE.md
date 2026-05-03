# CRUX Sample Notebooks — Provenance

## Dataset Source

**UCI Adult Income Dataset**
- Source: https://archive.ics.uci.edu/dataset/2/adult
- Local path: `../data/adult.csv`
- License: CC BY 4.0
- Rows: 32,561 (30,162 after dropna)
- Columns: 15 (14 features + 1 target)
- Task: Binary classification predicting income >$50K/year

## Generation Context

Generated for **CRUX hackathon** (May 2026) as test fixtures demonstrating progressive notebook degradation patterns that CRUX's audit pipeline must detect.

## Notebook Descriptions

### `01_clean.ipynb` — Control Sample (~18 cells)

**Purpose**: Baseline "production-ready" notebook with minimal gaps.

**Expected CRUX verdict**: `CLEAN` or `READY_WITH_DECISIONS` (at most 2-3 minor gaps, NO blockers)

**Structure**:
- Proper imports grouped at top
- Sequential execution (counts 1-9)
- Pipeline-wrapped preprocessing (ColumnTransformer with SimpleImputer + StandardScaler/OneHotEncoder)
- Stratified train/test split with `random_state=42`
- RandomForestClassifier (200 estimators)
- Model saved via joblib to `models/adult_income_v1.joblib`

**Gaps present** (if any): Minor auto-patchable gaps only (e.g., no Dockerfile, no structured logging)

---

### `02_messy.ipynb` — Hero Demo (~28 cells)

**Purpose**: Centerpiece demo showing realistic notebook mess that triggers multiple gap categories.

**Expected CRUX verdict**: `BLOCKED`

**Deliberate gaps embedded**:

**BLOCKERS (2)**:
- **Gap 9 (hardcoded secret)**: `KAGGLE_API_KEY = "kg_live_8f4d2a1b9c3e7f5d6a8b2c4e9f1d3a5b"` in cell 3
- **Gap 1 (no input validation)**: Bare `model.predict()` with no Pydantic schema or type checks

**DECISION REQUIRED (3)**:
- **Gap 3 (train/serve skew)**: Uses `LabelEncoder().fit_transform()` loop instead of Pipeline; encoders fit but never saved
- **Gap 4 (no model versioning)**: `joblib.dump(model, 'models/adult_model.pkl')` with no version suffix or metadata
- **Gap 13 (no repro metadata)**: `train_test_split()` WITHOUT `random_state` argument

**AUTO-PATCHABLE (3-5)**:
- **Gap 2 (no structured logging)**: Only `print()` calls (no import logging/structlog)
- **Gap 5 (no Pydantic schema)**: No BaseModel anywhere
- **Gap 15 (no Dockerfile)**: Not in repo root

**Deliberate mess patterns**:
- 3-4 abandoned debug cells: `print('starting')`, `df.head()`, `df.shape`, `df.dtypes` scattered
- 4 dead variables: `df_v2`, `temp`, `cols_to_drop_old`, `note`
- 1 commented-out XGBoost block (all lines commented)
- 2 cells NEVER executed (execution_count = null)
- Sloppy markdown: "# adult income model v3 (this is the one we're using)", "## try cleaning", "## ok now the model"
- Out-of-order execution counts: `df.head()` = 26, `df.shape()` = 27

---

### `03_chaos.ipynb` — Stretch Sample (50+ cells)

**Purpose**: Extreme degradation case with abandoned experiments and multiple secrets.

**Expected CRUX verdict**: `BLOCKED` (all gaps from 02_messy PLUS additional chaos)

**Structure**: Duplicates all content from `02_messy.ipynb`, then adds 30+ chaos cells:

**SECTION A — Abandoned GradientBoosting (5 cells)**:
- Import + instantiate `GradientBoostingClassifier`
- Commented-out fit/score (execution_count = null)

**SECTION B — Abandoned LogisticRegression (6 cells)**:
- Import `LogisticRegression` + `MinMaxScaler`
- Instantiate but never fit
- Import `RobustScaler` (third scaler, never used)

**SECTION C — Abandoned hyperparameter search (3 cells)**:
- Define `param_grid` with 48 combinations
- Commented-out `GridSearchCV` (execution_count = null)

**SECTION D — Contradictory imports + scratch (5 cells)**:
- `import pandas` (already imported as pd)
- `scratch_df = df.head(100).copy()`
- `my_preprocessor()` function (never called)
- Two commented-out train_test_split variants (execution_count = null)

**SECTION E — Second hardcoded secret + dead variables (4 cells)**:
- **SECOND SECRET**: `BACKUP_KEY = "sk_live_a4f8d3b2c1e9f7a6d5b8c2e4f1d3a5b9"`
- Three dead variables: `temp_var`, `unused_threshold`, `debug_counter` (all execution_count = null)

**SECTION F — Abandoned SVM + final note (4 cells)**:
- Import `SVC`
- Commented-out instantiation (execution_count = null)
- `FINAL_NOTE = 'remember to delete the api keys before pushing'` (execution_count = null)
- Final comment: `# this notebook needs cleanup` (execution_count = null)

**Total cells**: 22 (from 02_messy) + 30 (chaos additions) = 52 cells

**Execution counts**: Sequential for executed cells (1-29), null for 13 never-executed cells

---

## Gap Mapping Summary

| Gap ID | Gap Name | 01_clean | 02_messy | 03_chaos |
|--------|----------|----------|----------|----------|
| 1 | Input validation | ✓ (minor) | **BLOCKER** | **BLOCKER** |
| 2 | Structured logging | ✓ (patch) | **PATCH** | **PATCH** |
| 3 | Train/serve skew | ✗ | **DECISION** | **DECISION** |
| 4 | Model versioning | ✗ | **DECISION** | **DECISION** |
| 5 | Pydantic schema | ✓ (patch) | **PATCH** | **PATCH** |
| 9 | Hardcoded secrets | ✗ | **BLOCKER** (1) | **BLOCKER** (2) |
| 13 | Repro metadata | ✗ | **DECISION** | **DECISION** |
| 15 | No Dockerfile | ✓ (patch) | **PATCH** | **PATCH** |

Legend:
- ✗ = Not present
- ✓ = Present but auto-patchable or minor
- **BLOCKER** = Blocks production deployment
- **DECISION** = Requires human decision (options A/B/C)
- **PATCH** = Auto-patchable by CRUX

---

## Verification Notes

- `01_clean.ipynb`: MUST execute cleanly top-to-bottom in fresh kernel
- `02_messy.ipynb`: May fail execution due to deliberate mess (LabelEncoder skew, missing random_state)
- `03_chaos.ipynb`: May fail execution on commented cells (expected behavior)

All notebooks use ONLY: stdlib + pandas + numpy + scikit-learn + joblib (NO xgboost, lightgbm, tensorflow, etc.)

---

**Last updated**: 2026-05-03 (CRUX hackathon kickoff)