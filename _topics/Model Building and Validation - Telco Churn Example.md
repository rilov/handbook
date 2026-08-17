---
title: "Model Building and Validation - Telco Churn Example"
category: Model Evaluation
order: 2
permalink: /topics/model-building-validation-telco-churn/
tags:
  - machine-learning
  - cross-validation
  - pipelines
  - imbalanced-data
  - churn
summary: "A practical walkthrough of building and validating a churn model: loading data, building a scikit-learn pipeline, using holdout, K-fold, and stratified cross-validation, and avoiding data leakage."
date: 2026-08-16
---

# Model Building and Validation - Telco Churn Example

This is a hands-on example of how to take a real dataset, prepare it, build a model, and validate it honestly. We use the **Telco Customer Churn** dataset, where the goal is to predict whether a customer will leave the service.

The same ideas apply to many classification problems: use a **pipeline**, split the data, and pick a validation strategy that matches the data.

---

## 1. The dataset

The dataset has 7,043 customers and 21 columns. Each row is one customer, and the target is `Churn` (Yes/No). Typical columns include:

- **Services:** phone, multiple lines, internet, streaming
- **Account details:** contract, payment method, paperless billing, charges
- **Demographics:** gender, senior citizen, partner, dependents
- **Target:** `Churn`

The first step is always to look at the data before you build anything.

```python
import pandas as pd

df = pd.read_csv("telco_customer_churn.csv")
print(df.head())
print(df.info())
print(df.describe().T)
```

---

## 2. Cleaning and preparing

A few common cleaning steps:

- `TotalCharges` is stored as a string but should be a number. Convert it with `errors="coerce"` so non-numeric values become `NaN`.
- Drop the small number of rows that contain `NaN` after conversion.
- Convert object-type categorical columns to `category` for efficient storage.
- Drop `customerID` because it is a unique identifier, not a useful feature.
- Convert `Churn` to `0` (No) and `1` (Yes).

```python
# Convert TotalCharges to a number
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# Drop rows with missing values
df = df.dropna()

# Convert categorical columns from object to category
categorical_cols = df.select_dtypes(include="object").columns.tolist()
categorical_cols.remove("customerID")
df[categorical_cols] = df[categorical_cols].astype("category")

# Separate features and target
X = df.drop(columns=["customerID", "Churn"])
y = df["Churn"].map({"No": 0, "Yes": 1})
```

---

## 3. Build a preprocessing pipeline

The most important habit in a real project is to put everything inside a **pipeline**. A pipeline makes sure that every transformation is fitted only on the training data and then applied to the validation or test data.

- **Numerical features** are scaled with `StandardScaler`.
- **Categorical features** are one-hot encoded with `OneHotEncoder(handle_unknown="ignore")`. This means if a new category appears in the test set, the model ignores it instead of crashing.

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), X.select_dtypes(include=["int64", "float64"]).columns),
        ("cat", OneHotEncoder(handle_unknown="ignore"), X.select_dtypes(include="category").columns)
    ]
)

pipeline = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, random_state=1))
])
```

The pipeline guarantees that scaling and encoding happen inside each cross-validation fold, preventing data leakage.

---

## 4. Holdout validation

The simplest validation is a single **train-test split**. We hold back some data as a final test set and never use it until the end.

```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1, stratify=y
)

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print("Recall:", recall_score(y_test, predictions))
print("ROC-AUC:", roc_auc_score(y_test, pipeline.predict_proba(X_test)[:, 1]))
```

Typical holdout results for this kind of model might look like:

```
Accuracy:  0.796
Recall:    0.533
ROC-AUC:   0.847
```

Notice that **accuracy is much higher than recall**. The data is imbalanced: most customers do not churn. A model that gets 80% accuracy can still miss almost half the actual churners. This is why recall and ROC-AUC matter here.

---

## 5. K-fold cross-validation

Instead of one split, K-fold splits the training data into `K` folds, trains `K` times, and averages the scores.

```python
from sklearn.model_selection import KFold, cross_val_score

kf = KFold(n_splits=5, shuffle=True, random_state=1)
scores = cross_val_score(pipeline, X_train, y_train, cv=kf, scoring="recall")
print("K-fold recall scores:", scores)
print("Average:", scores.mean())
```

K-fold is more robust than a single holdout split, but with imbalanced classes the folds can end up with slightly different class proportions. That can change the score from one fold to the next.

---

## 6. Stratified K-fold for imbalanced data

**Stratified K-fold** keeps the same class ratio in every fold. If 27% of customers churn in the full data, every fold also has about 27% churners.

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
stratified_scores = cross_val_score(
    pipeline, X_train, y_train, cv=skf, scoring="recall"
)
print("Stratified K-fold recall:", stratified_scores)
print("Average:", stratified_scores.mean())
```

For imbalanced problems like churn, **stratified K-fold is usually the better choice** because every fold is a fair mini-version of the whole dataset.

---

## 7. Cross-validation for model selection

Cross-validation is not just for getting a score. It is also for **choosing the best model or settings** without touching the final test set.

For example, you might compare:

- Logistic Regression
- Random Forest
- Gradient Boosting

You score each model on the cross-validation folds and pick the one with the best average. Only then do you train the final model and evaluate it on the held-out test set.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

models = {
    "Logistic Regression": pipeline,
    "Random Forest": Pipeline(steps=[
        ("preprocess", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=1))
    ])
}

for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=skf, scoring="recall")
    print(f"{name}: {scores.mean():.3f} recall")
```

---

## 8. Final model on the holdout set

Once you have chosen the best approach using cross-validation, train the final model on the full training set and evaluate it on the holdout set.

```python
best_model = pipeline
best_model.fit(X_train, y_train)
final_predictions = best_model.predict(X_test)

print("Final accuracy:", accuracy_score(y_test, final_predictions))
print("Final recall:", recall_score(y_test, final_predictions))
print("Final ROC-AUC:", roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1]))
```

The holdout scores should be close to the cross-validation averages. If they are very different, the model is unstable or the data has been leaked into the validation process.

---

## 9. One-sentence takeaway

**Build everything inside a pipeline, split early, use stratified cross-validation for imbalanced data, and only evaluate on the final holdout set once you have made all your decisions.**
