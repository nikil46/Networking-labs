"""Step 31: train a reusable Decision Tree and verify on a held-out group split.
Run from the project root: python step31_train_verify.py
"""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'data' / 'WSN-DS-preprocessed.csv'
OUT = ROOT / 'models'
OUT.mkdir(exist_ok=True)
if not SOURCE.is_file():
    raise FileNotFoundError(f'Missing dataset: {SOURCE}')
df = pd.read_csv(SOURCE)
df.columns = df.columns.str.strip()
if df.columns.duplicated().any():
    raise ValueError('Duplicate column names after stripping whitespace')
target = 'Attack type'
excluded = [target, 'dist_CH_To_BS', 'DATA_R']
missing = [c for c in excluded if c not in df.columns]
if missing:
    raise ValueError(f'Missing expected dataset columns: {missing}')
X = df.drop(columns=excluded)
y = df[target]
if X.shape[1] != 16:
    raise ValueError(f'Expected 16 predictors; found {X.shape[1]}: {X.columns.tolist()}')
if X.isna().any().any() or y.isna().any():
    raise ValueError('Missing values detected; use the validated preprocessed dataset')
if not all(pd.api.types.is_numeric_dtype(t) for t in X.dtypes):
    raise ValueError('Non-numeric features found; preprocessing must match the training dataset')
# Identical feature vectors stay on the same side of the split.
groups = pd.util.hash_pandas_object(X, index=False).to_numpy()
train_idx, test_idx = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42).split(X, y, groups))
X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
model = DecisionTreeClassifier(criterion='gini', random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
labels = sorted(y.unique().tolist())
print('Held-out accuracy:', f'{accuracy_score(y_test, pred):.4%}')
print('Held-out classification report:\n', classification_report(y_test, pred, labels=labels, zero_division=0))
print('Confusion matrix (rows=actual, columns=predicted):\n', confusion_matrix(y_test, pred, labels=labels))
print('Class order:', labels)
joblib.dump({'model': model, 'features': X.columns.tolist(), 'classes': labels,
             'evaluation': 'group-disjoint 80/20 holdout, random_state=42'}, OUT / 'step31_decision_tree.joblib')
heldout = X_test.copy()
heldout[target] = y_test.to_numpy()
heldout.to_csv(OUT / 'step31_unseen_test.csv', index=False)
(OUT / 'step31_metrics.json').write_text(json.dumps({
    'accuracy': accuracy_score(y_test, pred),
    'report': classification_report(y_test, pred, labels=labels, output_dict=True, zero_division=0),
    'confusion_matrix': confusion_matrix(y_test, pred, labels=labels).tolist(),
    'labels': labels, 'train_count': len(train_idx), 'test_count': len(test_idx),
    'method': 'GroupShuffleSplit on identical 16-feature vectors; 80/20, seed 42'
}, indent=2))
print('Saved model and held-out test data in:', OUT)
