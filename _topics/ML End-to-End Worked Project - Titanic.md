---
title: "24. ML End-to-End Worked Project - Titanic"
category: Machine Learning
order: 24
tags:
  - machine-learning
  - end-to-end
  - project
  - titanic
  - tutorial
  - walkthrough
summary: A complete end-to-end ML project on the Titanic dataset, from raw CSV to final evaluation. We do data exploration, cleaning, feature engineering, model comparison, hyperparameter tuning, and final test set evaluation - showing exactly how all the pieces from the previous tutorials fit together.
---

# ML End-to-End Worked Project - Titanic

This is the project that ties everything together. We will take a real (but small) dataset and build a complete ML pipeline from scratch, using almost every concept from the previous tutorials.

By the end you will have:

* Explored a real dataset.
* Cleaned messy data.
* Engineered useful features.
* Compared multiple models.
* Tuned the best one.
* Evaluated honestly on a held-out test set.

This is the workflow you will use again and again in real ML work.

---

## The problem

The Titanic dataset contains passenger information from the 1912 disaster. For each passenger we know things like age, sex, ticket class, fare, and whether they survived.

**Goal:** Build a model that predicts whether a passenger survived.

This is a **binary classification** problem. Survived = 1, did not survive = 0.

---

## Step 1. Load and explore the data

We use the version built into seaborn so you do not need to download anything.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset("titanic")
print(df.shape)        # (891, 15)
print(df.head())
print(df.info())
print(df.describe())
```

You will see columns like:

* `survived` (0 or 1, the target)
* `pclass` (1, 2, or 3 - ticket class)
* `sex`, `age`, `sibsp`, `parch`, `fare`, `embarked`, `class`, `who`, `adult_male`, `alone`, etc.

Some are redundant (e.g. `pclass` and `class`). Some have missing values (`age`, `deck`, `embarked`).

### Check class balance

```python
print(df["survived"].value_counts(normalize=True))
# 0  ~61%
# 1  ~39%
```

Slightly imbalanced but not dramatically. Accuracy will be a reasonable starting metric.

### Look at missing values

```python
print(df.isnull().sum().sort_values(ascending=False))
```

You will see `deck` has many missing values (drop it), `age` has some missing values (impute it), `embarked` has two missing (impute or drop).

---

## Step 2. Clean and engineer features

### Pick the columns we want

```python
df = df[["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]].copy()
```

We dropped redundant columns (`class`, `who`, `adult_male`, `alone`, `embark_town`, `alive`, `adult_male`) and the mostly-missing `deck`.

### Engineer some new features

```python
# Family size = siblings/spouses + parents/children + self
df["family_size"] = df["sibsp"] + df["parch"] + 1

# Is the passenger travelling alone?
df["is_alone"] = (df["family_size"] == 1).astype(int)
```

Feature engineering like this often beats fancy models. Always look for combinations that have real-world meaning.

### Handle missing values

```python
# Age: fill with median
df["age"].fillna(df["age"].median(), inplace=True)

# Embarked: fill with most common value
df["embarked"].fillna(df["embarked"].mode()[0], inplace=True)

# Fare: just in case
df["fare"].fillna(df["fare"].median(), inplace=True)
```

For a more rigorous project, you would impute inside a Pipeline so it does not leak from test data. We will do that with `SimpleImputer` below.

### Encode categorical variables

```python
df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=True)
print(df.columns)
```

`sex` and `embarked` are categorical. `pd.get_dummies` turns them into 0/1 columns.

---

## Step 3. Split into train and test

This must happen before any further preprocessing fitting.

```python
from sklearn.model_selection import train_test_split

X = df.drop(columns=["survived"])
y = df["survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y,    # keep class balance the same in train and test
)

print(X_train.shape, X_test.shape)
```

Notice `stratify=y`. With imbalanced data, this ensures both train and test have similar class proportions.

---

## Step 4. Build a baseline pipeline

Always start with the simplest reasonable model. A Logistic Regression baseline tells us how hard the problem is.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

baseline = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  LogisticRegression(max_iter=1000)),
])

cv_scores = cross_val_score(baseline, X_train, y_train, cv=5, scoring="accuracy")
print(f"Baseline CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
```

You should see somewhere around 0.79-0.81. That is the bar to beat.

---

## Step 5. Compare several models

Now try a few different families and see which looks promising.

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

models = {
    "Logistic Regression":  LogisticRegression(max_iter=1000),
    "Decision Tree":        DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest":        RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting":    GradientBoostingClassifier(random_state=42),
    "KNN (k=5)":            KNeighborsClassifier(n_neighbors=5),
}

results = {}
for name, model in models.items():
    pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
    scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="accuracy")
    results[name] = scores.mean()
    print(f"{name:25s} {scores.mean():.3f} (+/- {scores.std():.3f})")
```

You will typically see Gradient Boosting and Random Forest leading the pack, around 0.83-0.84.

---

## Step 6. Tune the best model

Once you pick a winning algorithm, tune its hyperparameters.

```python
from sklearn.model_selection import GridSearchCV

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  GradientBoostingClassifier(random_state=42)),
])

param_grid = {
    "model__n_estimators":  [100, 200, 300],
    "model__learning_rate": [0.05, 0.1, 0.2],
    "model__max_depth":     [2, 3, 4],
}

grid = GridSearchCV(
    pipe,
    param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
    verbose=1,
)
grid.fit(X_train, y_train)

print("Best params:", grid.best_params_)
print("Best CV accuracy:", grid.best_score_)
```

This fits 27 candidates x 5 folds = 135 models. With `n_jobs=-1` it runs in parallel.

---

## Step 7. Final evaluation on the held-out test set

This is the moment of truth. We have not touched `X_test` and `y_test` yet.

```python
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]

print(f"Test accuracy:  {accuracy_score(y_test, y_pred):.3f}")
print(f"Test ROC-AUC:   {roc_auc_score(y_test, y_proba):.3f}")
print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification report:")
print(classification_report(y_test, y_pred, target_names=["Died", "Survived"]))
```

Typical result is around 0.82-0.85 accuracy with ROC-AUC around 0.86-0.88. The confusion matrix tells you exactly what kinds of mistakes the model makes.

---

## Step 8. Look at feature importance

Gradient Boosting gives you free feature importance scores. Use them to understand what drove the predictions.

```python
import pandas as pd

model = best_model.named_steps["model"]
importance = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(x=importance.values, y=importance.index, color="gray")
plt.title("Feature Importance (Gradient Boosting)")
plt.xlabel("Importance")
plt.tight_layout()
plt.show()
```

You will almost certainly see `sex_male` and `fare` at the top, followed by `age`, `pclass`, and `family_size`. The model learned what we already knew historically: women, the rich, and children had higher survival rates.

This is what good ML looks like: numbers that align with reality.

---

## Step 9. Sanity check with predictions

It is always a good idea to spot-check actual predictions.

```python
sample = X_test.head(5)
print(sample)
print("\nPredicted probabilities of survival:")
print(best_model.predict_proba(sample)[:, 1].round(2))
print("\nActual:")
print(y_test.head(5).values)
```

If the model says "5% survival" for an actual non-survivor, great. If it says "5% survival" for an actual survivor, look at the row and see why the model was wrong. Was that person old? Travelling third class? Now you understand both your data and your model.

---

## The full pipeline as one block

Here is the entire project in one paste-ready snippet.

```python
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

# 1. Load
df = sns.load_dataset("titanic")
df = df[["survived","pclass","sex","age","sibsp","parch","fare","embarked"]].copy()

# 2. Feature engineering
df["family_size"] = df["sibsp"] + df["parch"] + 1
df["is_alone"]    = (df["family_size"] == 1).astype(int)

# 3. Missing values
df["age"].fillna(df["age"].median(), inplace=True)
df["embarked"].fillna(df["embarked"].mode()[0], inplace=True)
df["fare"].fillna(df["fare"].median(), inplace=True)

# 4. Encode
df = pd.get_dummies(df, columns=["sex","embarked"], drop_first=True)

# 5. Split
X, y = df.drop(columns="survived"), df["survived"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 6. Pipeline + grid search
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  GradientBoostingClassifier(random_state=42)),
])
param_grid = {
    "model__n_estimators":  [100, 200, 300],
    "model__learning_rate": [0.05, 0.1, 0.2],
    "model__max_depth":     [2, 3, 4],
}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)
print("Best:", grid.best_params_, grid.best_score_)

# 7. Final evaluation
best = grid.best_estimator_
y_pred  = best.predict(X_test)
y_proba = best.predict_proba(X_test)[:, 1]
print(f"Test acc:    {accuracy_score(y_test, y_pred):.3f}")
print(f"Test ROC-AUC: {roc_auc_score(y_test, y_proba):.3f}")
print(classification_report(y_test, y_pred, target_names=["Died","Survived"]))
```

---

## What you just did

You ran the entire classical ML pipeline:

1. **Loaded and explored** real data (with missing values and categorical features).
2. **Engineered features** from your domain understanding.
3. **Cleaned** the data and handled missing values.
4. **Split** into train and test, stratified.
5. **Built a Pipeline** with scaling and a classifier to prevent leakage.
6. **Compared** several models with cross validation.
7. **Tuned** the best one with GridSearchCV.
8. **Evaluated** on a held-out test set with multiple metrics.
9. **Inspected** feature importance to make sure the model learned sensible things.

This workflow generalizes to almost any tabular ML problem. Take any new dataset, drop in your own columns, and 80% of the steps stay the same.

---

## Common improvements you can try

* **Stratified K-fold** instead of plain K-fold for imbalanced data.
* **Smarter imputation.** Use `SimpleImputer` inside the Pipeline so test data is never leaked.
* **Extract title from name** (Mr, Mrs, Miss, Master, Dr) - often a strong predictor.
* **Try XGBoost / LightGBM** instead of GradientBoostingClassifier. They are usually faster and often more accurate.
* **Try CatBoost** if you have many categorical features.
* **Try a simple neural net** with `MLPClassifier`. On this problem it will not help much, but it is good practice.
* **Calibrate probabilities** with `CalibratedClassifierCV` if you need actual probability estimates.
* **Save your model** with `joblib.dump(best, "model.pkl")` to use in production.

---

## What this taught you

Every concept from the previous tutorials showed up here. Linear regression's foundation. Decision trees' splits. Random forests' voting. Gradient boosting's sequential corrections. Cross validation's robustness. Grid search's tuning. Pipeline's safety. Metric selection's importance.

This is what ML really looks like. Not 95% writing models from scratch. It is 80% data wrangling, 10% picking algorithms, 5% tuning, and 5% interpreting results.

If you can do this project comfortably, you can do most real ML jobs. That is the whole point. 🚢
