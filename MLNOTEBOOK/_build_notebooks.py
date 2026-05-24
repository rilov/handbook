"""
Builds all ML practice notebooks into the MLNOTEBOOK/ directory.

Run once:
    python _build_notebooks.py

Each notebook is self-contained, runs in Google Colab with zero setup,
uses publicly available datasets (sklearn, seaborn, or direct URLs),
and includes EDA, modeling, evaluation, and exercises.
"""
import json
import os
from pathlib import Path

OUT = Path(__file__).parent

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.split("\n")}

def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.split("\n"),
    }

def save(name, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = OUT / name
    with open(path, "w") as f:
        json.dump(nb, f, indent=1)
    print(f"  wrote {path}")

# Common header used in every notebook
INSTALL = """# Run this cell first if running locally. In Google Colab everything is pre-installed.
# !pip install -q numpy pandas scikit-learn matplotlib seaborn scipy xgboost lightgbm"""

IMPORTS = """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
np.random.seed(42)"""


# ============================================================
# 01. LINEAR REGRESSION - California Housing
# ============================================================
def nb_linear_regression():
    cells = [
        md("""# 01. Linear Regression - California Housing Prices

**Topic:** Predict median house values in California districts using simple and multiple linear regression.

**Dataset:** California Housing (built into scikit-learn, no download needed).

**What you will do:**
1. Load and explore the data
2. Visualize relationships between features and target
3. Train a simple linear regression model
4. Evaluate using MAE, RMSE, R²
5. Try multiple linear regression with all features
6. Interpret the coefficients

**Open in Colab:** [Use File → Upload Notebook] or run locally."""),
        code(INSTALL),
        code(IMPORTS),
        md("## 1. Load the data"),
        code("""from sklearn.datasets import fetch_california_housing

data = fetch_california_housing(as_frame=True)
df = data.frame
print(df.shape)
df.head()"""),
        code("""print(df.info())
df.describe()"""),
        md("""## 2. Explore the data

`MedHouseVal` is the target (median house value in $100,000s)."""),
        code("""# Distribution of the target
plt.figure(figsize=(10, 5))
sns.histplot(df["MedHouseVal"], bins=50, kde=True, color="gray")
plt.title("Distribution of Median House Value")
plt.show()"""),
        code("""# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Matrix")
plt.show()"""),
        code("""# Scatter: median income vs house value (the strongest predictor)
plt.figure(figsize=(10, 6))
sns.scatterplot(x="MedInc", y="MedHouseVal", data=df.sample(2000), alpha=0.4, color="steelblue")
plt.title("Median Income vs House Value")
plt.show()"""),
        md("## 3. Simple Linear Regression (one feature)"),
        code("""from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

X = df[["MedInc"]]
y = df["MedHouseVal"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Slope:     {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"MAE:       {mean_absolute_error(y_test, y_pred):.4f}")
print(f"RMSE:      {mean_squared_error(y_test, y_pred, squared=False):.4f}")
print(f"R^2:       {r2_score(y_test, y_pred):.4f}")"""),
        code("""# Plot the regression line
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_test["MedInc"], y=y_test, alpha=0.3, color="steelblue", label="Actual")
sns.lineplot(x=X_test["MedInc"], y=y_pred, color="red", label="Predicted")
plt.title("Linear Regression: MedInc vs House Value")
plt.legend()
plt.show()"""),
        md("## 4. Multiple Linear Regression (all features)"),
        code("""X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"MAE:  {mean_absolute_error(y_test, y_pred):.4f}")
print(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.4f}")
print(f"R^2:  {r2_score(y_test, y_pred):.4f}")"""),
        code("""# Coefficient interpretation
coef_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_,
}).sort_values("Coefficient", key=abs, ascending=False)
print(coef_df)"""),
        code("""# Predicted vs Actual plot
plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_pred, alpha=0.3, color="steelblue")
plt.plot([0, 5], [0, 5], color="red", linestyle="--")
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Predicted vs Actual House Values")
plt.show()"""),
        md("""## 5. Exercises

Try these on your own:

1. **Add polynomial features** (`from sklearn.preprocessing import PolynomialFeatures`) and see if R² improves.
2. **Drop highly correlated features** and re-fit. Does R² stay the same?
3. **Plot residuals** (`y_test - y_pred`). Are they centered around 0? Any patterns?
4. **Try a different dataset** (e.g. `from sklearn.datasets import fetch_openml; fetch_openml('boston', version=1)` if available).
5. **Compute Adjusted R²** manually using the formula and compare to plain R².

When you are done, head to notebook **02 - Logistic Regression**."""),
    ]
    save("01_linear_regression.ipynb", cells)


# ============================================================
# 02. LOGISTIC REGRESSION - Titanic
# ============================================================
def nb_logistic_regression():
    cells = [
        md("""# 02. Logistic Regression - Titanic Survival

**Topic:** Predict whether a Titanic passenger survived based on their information.

**Dataset:** Titanic (built into seaborn).

**What you will do:**
1. Load and clean the Titanic dataset
2. Engineer simple features
3. Train a logistic regression model
4. Evaluate with accuracy, precision, recall, F1, ROC-AUC
5. Plot the ROC curve and confusion matrix"""),
        code(INSTALL),
        code(IMPORTS),
        md("## 1. Load the data"),
        code("""df = sns.load_dataset("titanic")
print(df.shape)
df.head()"""),
        code("""print(df.isnull().sum().sort_values(ascending=False))"""),
        md("""## 2. Clean and prepare features"""),
        code("""# Pick useful columns
df = df[["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]].copy()

# Engineer family size + alone flag
df["family_size"] = df["sibsp"] + df["parch"] + 1
df["is_alone"] = (df["family_size"] == 1).astype(int)

# Fill missing values
df["age"].fillna(df["age"].median(), inplace=True)
df["embarked"].fillna(df["embarked"].mode()[0], inplace=True)

# One-hot encode categoricals
df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=True)
df.head()"""),
        md("## 3. Train / Test Split"),
        code("""from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

X = df.drop(columns=["survived"])
y = df["survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(X_train.shape, X_test.shape)"""),
        md("## 4. Logistic Regression Pipeline"),
        code("""pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  LogisticRegression(max_iter=1000)),
])
pipe.fit(X_train, y_train)

y_pred  = pipe.predict(X_test)
y_proba = pipe.predict_proba(X_test)[:, 1]"""),
        md("## 5. Evaluation"),
        code("""from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve,
)

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall:    {recall_score(y_test, y_pred):.3f}")
print(f"F1:        {f1_score(y_test, y_pred):.3f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_proba):.3f}")
print()
print(classification_report(y_test, y_pred, target_names=["Died", "Survived"]))"""),
        code("""# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Greys",
            xticklabels=["Died", "Survived"], yticklabels=["Died", "Survived"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()"""),
        code("""# ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color="black", lw=2, label=f"AUC = {roc_auc_score(y_test, y_proba):.2f}")
plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.show()"""),
        md("## 6. Inspect coefficients"),
        code("""coef_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": pipe.named_steps["model"].coef_[0],
}).sort_values("Coefficient", key=abs, ascending=False)
print(coef_df)"""),
        md("""## 7. Exercises

1. **Adjust the threshold** from the default 0.5 and watch precision/recall change.
2. **Try a different solver** like `solver="liblinear"` or `"saga"`.
3. **Add L1 regularization** with `penalty="l1"` and `solver="liblinear"`.
4. **Add the passenger title** as a feature (extract from the original `name` column - load the raw Kaggle dataset).
5. **Plot a calibration curve** to check if probabilities are well-calibrated."""),
    ]
    save("02_logistic_regression.ipynb", cells)


# ============================================================
# 03. REGULARIZATION
# ============================================================
def nb_regularization():
    cells = [
        md("""# 03. Regularization - Ridge, Lasso, Elastic Net

**Topic:** Compare unregularized linear regression with Ridge (L2), Lasso (L1), and Elastic Net.

**Dataset:** California Housing (sklearn).

**What you will do:**
1. Train a plain Linear Regression baseline
2. Train Ridge, Lasso, Elastic Net with the same data
3. Compare RMSE and R²
4. Visualize how coefficients shrink as regularization increases
5. Use cross-validated tuning to pick the best `alpha`"""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, RidgeCV, LassoCV
from sklearn.metrics import mean_squared_error, r2_score

data = fetch_california_housing(as_frame=True)
df = data.frame
X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"""),
        md("## 1. Compare four models"),
        code("""def evaluate(name, model):
    pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    rmse = mean_squared_error(y_test, pred, squared=False)
    r2 = r2_score(y_test, pred)
    print(f"{name:18s}  RMSE = {rmse:.4f}   R^2 = {r2:.4f}")
    return pipe

models = {
    "Linear":       LinearRegression(),
    "Ridge":        Ridge(alpha=1.0),
    "Lasso":        Lasso(alpha=0.1),
    "Elastic Net":  ElasticNet(alpha=0.1, l1_ratio=0.5),
}
fitted = {name: evaluate(name, m) for name, m in models.items()}"""),
        md("## 2. Visualize how coefficients shrink as alpha increases"),
        code("""alphas = np.logspace(-3, 3, 50)
ridge_coefs = []
lasso_coefs = []

scaler = StandardScaler().fit(X_train)
X_train_s = scaler.transform(X_train)

for a in alphas:
    r = Ridge(alpha=a).fit(X_train_s, y_train)
    l = Lasso(alpha=a, max_iter=5000).fit(X_train_s, y_train)
    ridge_coefs.append(r.coef_)
    lasso_coefs.append(l.coef_)

ridge_coefs = np.array(ridge_coefs)
lasso_coefs = np.array(lasso_coefs)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for i, name in enumerate(X.columns):
    axes[0].plot(alphas, ridge_coefs[:, i], label=name)
    axes[1].plot(alphas, lasso_coefs[:, i], label=name)

for ax, title in zip(axes, ["Ridge (L2)", "Lasso (L1)"]):
    ax.set_xscale("log")
    ax.set_xlabel("alpha")
    ax.set_ylabel("coefficient")
    ax.set_title(title)
    ax.legend(fontsize=8)
plt.tight_layout()
plt.show()"""),
        md("Notice how Lasso drives coefficients exactly to zero, while Ridge shrinks them gently."),
        md("## 3. Pick the best alpha with cross validation"),
        code("""ridge_cv = RidgeCV(alphas=np.logspace(-3, 3, 50)).fit(X_train_s, y_train)
lasso_cv = LassoCV(alphas=np.logspace(-3, 3, 50), cv=5, max_iter=5000).fit(X_train_s, y_train)

print(f"Best Ridge alpha: {ridge_cv.alpha_:.5f}")
print(f"Best Lasso alpha: {lasso_cv.alpha_:.5f}")"""),
        md("""## 4. Exercises

1. **Generate noisy fake features** (random columns) and check that Lasso zeroes them out.
2. **Try `Lasso(alpha=10)`** - what happens to the model?
3. **Plot RMSE vs alpha** for Ridge and Lasso. Where is the sweet spot?
4. **Try a real Kaggle dataset** like the Ames Housing dataset (more features = regularization matters more)."""),
    ]
    save("03_regularization.ipynb", cells)


# ============================================================
# 04. DECISION TREES
# ============================================================
def nb_decision_trees():
    cells = [
        md("""# 04. Decision Trees - Iris Classification

**Topic:** Train a decision tree, visualize it, and observe overfitting.

**Dataset:** Iris (sklearn).

**What you will do:**
1. Train a decision tree on the Iris dataset
2. Visualize the tree as a flowchart
3. Show how depth controls overfitting
4. Compute feature importance"""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report

iris = load_iris(as_frame=True)
X, y = iris.data, iris.target
print(X.shape)
X.head()"""),
        md("## 1. Train a shallow tree"),
        code("""X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

tree = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train)
print(f"Train accuracy: {tree.score(X_train, y_train):.3f}")
print(f"Test accuracy:  {tree.score(X_test, y_test):.3f}")"""),
        code("""# Visualize the tree
plt.figure(figsize=(16, 8))
plot_tree(tree, feature_names=X.columns, class_names=iris.target_names, filled=True, rounded=True)
plt.show()"""),
        md("## 2. Show overfitting with deep tree"),
        code("""train_accs = []
test_accs = []
depths = range(1, 16)
for d in depths:
    t = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train, y_train)
    train_accs.append(t.score(X_train, y_train))
    test_accs.append(t.score(X_test, y_test))

plt.figure(figsize=(10, 5))
plt.plot(depths, train_accs, "o-", label="Training accuracy", color="black")
plt.plot(depths, test_accs,  "o-", label="Test accuracy",     color="gray")
plt.xlabel("max_depth")
plt.ylabel("Accuracy")
plt.title("Decision Tree: Train vs Test Accuracy by Depth")
plt.legend()
plt.show()"""),
        md("## 3. Feature importance"),
        code("""importance = pd.Series(tree.feature_importances_, index=X.columns).sort_values()
plt.figure(figsize=(8, 4))
importance.plot.barh(color="gray")
plt.title("Feature Importance")
plt.show()
print(importance)"""),
        md("""## 4. Exercises

1. **Try entropy** as the criterion (`criterion="entropy"`) and compare.
2. **Set `min_samples_leaf=10`** and observe the effect.
3. **Use the wine dataset** (`from sklearn.datasets import load_wine`).
4. **Try `DecisionTreeRegressor`** on California Housing data."""),
    ]
    save("04_decision_trees.ipynb", cells)


# ============================================================
# 05. RANDOM FOREST
# ============================================================
def nb_random_forest():
    cells = [
        md("""# 05. Random Forest - Breast Cancer Classification

**Topic:** Compare a single decision tree vs a random forest. Demonstrate how ensembling reduces variance.

**Dataset:** Breast Cancer Wisconsin (sklearn)."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, confusion_matrix

data = load_breast_cancer(as_frame=True)
X, y = data.data, data.target
print(X.shape)
print(data.target_names)"""),
        md("## 1. Single tree vs Random Forest"),
        code("""X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

tree   = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
forest = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)

for name, m in [("Decision Tree", tree), ("Random Forest", forest)]:
    pred = m.predict(X_test)
    proba = m.predict_proba(X_test)[:, 1]
    print(f"{name:15s}  Acc = {accuracy_score(y_test, pred):.3f}   AUC = {roc_auc_score(y_test, proba):.3f}")"""),
        md("## 2. Effect of n_estimators"),
        code("""ns = [1, 5, 10, 25, 50, 100, 200, 500]
scores = []
for n in ns:
    rf = RandomForestClassifier(n_estimators=n, random_state=42)
    s = cross_val_score(rf, X_train, y_train, cv=5, scoring="accuracy").mean()
    scores.append(s)

plt.figure(figsize=(10, 5))
plt.plot(ns, scores, "o-", color="black")
plt.xscale("log")
plt.xlabel("n_estimators")
plt.ylabel("CV accuracy")
plt.title("More trees = more stable predictions")
plt.show()"""),
        md("## 3. Feature importance"),
        code("""imp = pd.Series(forest.feature_importances_, index=X.columns).sort_values().tail(15)
plt.figure(figsize=(8, 6))
imp.plot.barh(color="gray")
plt.title("Top 15 most important features")
plt.show()"""),
        md("## 4. Confusion matrix"),
        code("""cm = confusion_matrix(y_test, forest.predict(X_test))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greys",
            xticklabels=data.target_names, yticklabels=data.target_names)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()"""),
        md("""## 5. Exercises

1. **Try `max_features="sqrt"` vs `"log2"` vs `1.0`** and compare.
2. **Try `RandomForestRegressor`** on the California Housing dataset.
3. **Use OOB score** (`oob_score=True`, `bootstrap=True`) instead of CV.
4. **Time the training** of 1000 trees vs 100. How does it scale?"""),
    ]
    save("05_random_forest.ipynb", cells)


# ============================================================
# 06. GRADIENT BOOSTING / XGBOOST
# ============================================================
def nb_gradient_boosting():
    cells = [
        md("""# 06. Gradient Boosting & XGBoost - Titanic

**Topic:** Train sklearn's GradientBoostingClassifier and XGBoost on the Titanic dataset. Tune hyperparameters and compare.

**Dataset:** Titanic (seaborn)."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

# Try XGBoost if available
try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False
    print("XGBoost not installed. Run: pip install xgboost")

df = sns.load_dataset("titanic")
df = df[["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]].copy()
df["family_size"] = df["sibsp"] + df["parch"] + 1
df["is_alone"]    = (df["family_size"] == 1).astype(int)
df["age"].fillna(df["age"].median(), inplace=True)
df["embarked"].fillna(df["embarked"].mode()[0], inplace=True)
df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=True)

X = df.drop(columns=["survived"])
y = df["survived"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)"""),
        md("## 1. Compare three models"),
        code("""rf  = RandomForestClassifier(n_estimators=300, random_state=42).fit(X_train, y_train)
gb  = GradientBoostingClassifier(random_state=42).fit(X_train, y_train)

for name, m in [("Random Forest", rf), ("Gradient Boosting", gb)]:
    pred  = m.predict(X_test)
    proba = m.predict_proba(X_test)[:, 1]
    print(f"{name:20s}  Acc = {accuracy_score(y_test, pred):.3f}   AUC = {roc_auc_score(y_test, proba):.3f}")

if HAS_XGB:
    xgb = XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=4,
                        use_label_encoder=False, eval_metric="logloss", random_state=42)
    xgb.fit(X_train, y_train)
    pred  = xgb.predict(X_test)
    proba = xgb.predict_proba(X_test)[:, 1]
    print(f"{'XGBoost':20s}  Acc = {accuracy_score(y_test, pred):.3f}   AUC = {roc_auc_score(y_test, proba):.3f}")"""),
        md("## 2. Tune Gradient Boosting with Grid Search"),
        code("""param_grid = {
    "learning_rate": [0.05, 0.1, 0.2],
    "n_estimators":  [100, 300],
    "max_depth":     [2, 3, 4],
}
grid = GridSearchCV(
    GradientBoostingClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring="roc_auc",
    n_jobs=-1,
)
grid.fit(X_train, y_train)
print("Best params:", grid.best_params_)
print(f"Best CV AUC: {grid.best_score_:.3f}")

best = grid.best_estimator_
print(f"\\nTest AUC: {roc_auc_score(y_test, best.predict_proba(X_test)[:, 1]):.3f}")"""),
        md("## 3. Feature importance"),
        code("""imp = pd.Series(best.feature_importances_, index=X.columns).sort_values()
plt.figure(figsize=(8, 5))
imp.plot.barh(color="gray")
plt.title("Gradient Boosting Feature Importance")
plt.show()"""),
        md("""## 4. Exercises

1. **Try LightGBM** (`from lightgbm import LGBMClassifier`).
2. **Use early stopping** with XGBoost (`early_stopping_rounds=20`, supply `eval_set`).
3. **Tune subsample and colsample_bytree** for XGBoost.
4. **Try a Kaggle competition dataset** (House Prices Advanced Regression for tabular boosting practice)."""),
    ]
    save("06_gradient_boosting_xgboost.ipynb", cells)


# ============================================================
# 07. DISTANCE METRICS
# ============================================================
def nb_distance_metrics():
    cells = [
        md("""# 07. Distance & Similarity Metrics

**Topic:** Compute Euclidean, Manhattan, Cosine, Pearson, and Jaccard distances on real data.

**Dataset:** Iris (numerical) and synthetic sets (Jaccard)."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_iris
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances, cosine_similarity
from scipy.spatial.distance import pdist, squareform, jaccard

iris = load_iris(as_frame=True)
X = iris.data.values
y = iris.target.values
print(X.shape)"""),
        md("## 1. Euclidean and Manhattan on first 5 flowers"),
        code("""sample = X[:5]
print("Euclidean:")
print(np.round(euclidean_distances(sample), 2))
print("\\nManhattan:")
print(np.round(manhattan_distances(sample), 2))"""),
        md("## 2. Cosine similarity"),
        code("""print("Cosine similarity (first 5 flowers):")
print(np.round(cosine_similarity(sample), 3))"""),
        md("## 3. Pearson correlation"),
        code("""# Correlation between features
df = iris.data
print("Pearson correlation between features:")
print(df.corr().round(2))"""),
        md("## 4. Jaccard on sets"),
        code("""user1 = {"action", "comedy", "thriller", "drama"}
user2 = {"comedy", "drama", "romance"}
user3 = {"horror", "thriller", "action"}

def jaccard_sim(a, b):
    return len(a & b) / len(a | b)

print(f"User1 vs User2 Jaccard: {jaccard_sim(user1, user2):.2f}")
print(f"User1 vs User3 Jaccard: {jaccard_sim(user1, user3):.2f}")"""),
        md("## 5. Visualize distance matrix"),
        code("""dist = squareform(pdist(X, metric="euclidean"))
plt.figure(figsize=(8, 6))
sns.heatmap(dist, cmap="Greys")
plt.title("Pairwise Euclidean Distance Matrix (Iris)")
plt.show()"""),
        md("""## 6. Exercises

1. **Find the most similar pair of flowers** using each distance metric.
2. **Compare Cosine vs Euclidean** when one feature has a much larger scale than others.
3. **Build a tiny recommender** that suggests songs to a user based on cosine similarity of listening histories.
4. **Compute Hamming distance** between two binary strings."""),
    ]
    save("07_distance_metrics.ipynb", cells)


# ============================================================
# 08. K-MEANS CLUSTERING
# ============================================================
def nb_kmeans():
    cells = [
        md("""# 08. K-Means Clustering

**Topic:** Cluster customers and demonstrate the elbow method.

**Dataset:** Synthetic blobs + the Mall Customers dataset (loaded directly from a public URL).

> **Mall Customers Kaggle source:** https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python"""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score"""),
        md("## 1. Synthetic blobs (so you can see clusters)"),
        code("""X, _ = make_blobs(n_samples=400, centers=4, cluster_std=0.8, random_state=42)
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], s=15, color="gray")
plt.title("Raw data (no labels)")
plt.show()"""),
        code("""km = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X)
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=km.labels_, s=15, cmap="tab10")
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], s=200, marker="X", c="red")
plt.title("K-Means clusters (K=4)")
plt.show()"""),
        md("## 2. Elbow method to pick K"),
        code("""ks = range(1, 11)
inertias = []
silhouettes = []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    inertias.append(km.inertia_)
    if k > 1:
        silhouettes.append(silhouette_score(X, km.labels_))

fig, ax = plt.subplots(1, 2, figsize=(14, 4))
ax[0].plot(ks, inertias, "o-", color="black")
ax[0].set_xlabel("K")
ax[0].set_ylabel("Inertia (WCSS)")
ax[0].set_title("Elbow Method")

ax[1].plot(list(ks)[1:], silhouettes, "o-", color="black")
ax[1].set_xlabel("K")
ax[1].set_ylabel("Silhouette score")
ax[1].set_title("Silhouette by K")
plt.show()"""),
        md("## 3. Real data: Mall Customers"),
        code("""# Direct download from a public mirror (no Kaggle login needed)
url = "https://raw.githubusercontent.com/SteffiPeTaffy/machineLearningAZ/master/Machine%20Learning%20A-Z%20Template%20Folder/Part%204%20-%20Clustering/Section%2024%20-%20K-Means%20Clustering/Mall_Customers.csv"
try:
    mall = pd.read_csv(url)
    print(mall.shape)
    mall.head()
except Exception as e:
    print("Could not fetch online. Upload Mall_Customers.csv manually and load with pd.read_csv.")
    mall = None"""),
        code("""if mall is not None:
    Xm = mall[["Annual Income (k$)", "Spending Score (1-100)"]].values
    Xm_s = StandardScaler().fit_transform(Xm)

    km = KMeans(n_clusters=5, n_init=10, random_state=42).fit(Xm_s)
    plt.figure(figsize=(10, 6))
    plt.scatter(Xm[:, 0], Xm[:, 1], c=km.labels_, s=40, cmap="tab10")
    plt.xlabel("Annual Income (k$)")
    plt.ylabel("Spending Score")
    plt.title("Mall Customer Segments")
    plt.show()"""),
        md("""## 4. Exercises

1. **Try different K values** (3, 4, 6) and see which makes most business sense.
2. **Use all numeric columns** of Mall Customers including Age.
3. **Try `init="random"` vs `"k-means++"`** and compare stability across runs.
4. **Try the iris dataset** without using the labels."""),
    ]
    save("08_kmeans_clustering.ipynb", cells)


# ============================================================
# 09. HIERARCHICAL CLUSTERING
# ============================================================
def nb_hierarchical():
    cells = [
        md("""# 09. Hierarchical Clustering

**Topic:** Build a dendrogram, compare linkage methods, and cut the tree at different levels.

**Dataset:** Iris (sklearn)."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

iris = load_iris(as_frame=True)
X = StandardScaler().fit_transform(iris.data)
y = iris.target.values"""),
        md("## 1. Plot dendrogram (Ward linkage)"),
        code("""Z = linkage(X, method="ward")
plt.figure(figsize=(14, 6))
dendrogram(Z, color_threshold=10, no_labels=True)
plt.title("Iris Dendrogram (Ward linkage)")
plt.xlabel("Samples")
plt.ylabel("Distance")
plt.show()"""),
        md("## 2. Cut at K=3 and compare to actual species"),
        code("""labels = fcluster(Z, t=3, criterion="maxclust")
ari = adjusted_rand_score(y, labels)
print(f"Adjusted Rand Index vs true species: {ari:.3f}")

plt.figure(figsize=(10, 5))
sns.scatterplot(x=iris.data["petal length (cm)"], y=iris.data["petal width (cm)"],
                hue=labels, palette="tab10", s=60)
plt.title("Hierarchical clusters (cut at K=3)")
plt.show()"""),
        md("## 3. Compare linkage methods"),
        code("""fig, axes = plt.subplots(2, 2, figsize=(14, 8))
for ax, method in zip(axes.ravel(), ["single", "complete", "average", "ward"]):
    Z = linkage(X, method=method)
    dendrogram(Z, ax=ax, no_labels=True, color_threshold=0)
    ax.set_title(method)
plt.tight_layout()
plt.show()"""),
        md("""## 4. Exercises

1. **Cut at different K values** (2, 3, 4, 5) and compute the Adjusted Rand Index for each.
2. **Try the breast cancer dataset** with hierarchical clustering.
3. **Visualize a heatmap with hierarchical clustering** using `sns.clustermap`.
4. **Compare hierarchical clustering with K-Means** on the same data."""),
    ]
    save("09_hierarchical_clustering.ipynb", cells)


# ============================================================
# 10. KNN
# ============================================================
def nb_knn():
    cells = [
        md("""# 10. K-Nearest Neighbours

**Topic:** Use KNN for both classification and regression. Show the importance of scaling and choosing K.

**Dataset:** Iris and Wine (sklearn)."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score"""),
        md("## 1. Iris with raw vs scaled features"),
        code("""iris = load_iris(as_frame=True)
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Without scaling
knn1 = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
print(f"Raw features:    {knn1.score(X_test, y_test):.3f}")

# With scaling
pipe = Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=5))])
pipe.fit(X_train, y_train)
print(f"Scaled features: {pipe.score(X_test, y_test):.3f}")"""),
        md("## 2. Choose K with cross-validation"),
        code("""ks = range(1, 31)
scores = []
for k in ks:
    pipe = Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=k))])
    s = cross_val_score(pipe, X_train, y_train, cv=5).mean()
    scores.append(s)

plt.figure(figsize=(10, 5))
plt.plot(ks, scores, "o-", color="black")
plt.xlabel("K")
plt.ylabel("CV accuracy")
plt.title("Choosing K for KNN (Iris)")
plt.show()
best_k = ks[np.argmax(scores)]
print(f"Best K: {best_k}")"""),
        md("## 3. KNN on Wine dataset"),
        code("""wine = load_wine(as_frame=True)
X, y = wine.data, wine.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Critical: scale because Wine features have very different ranges
pipe = Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=7, weights="distance"))])
pipe.fit(X_train, y_train)
print(f"Wine test accuracy: {pipe.score(X_test, y_test):.3f}")"""),
        md("""## 4. Exercises

1. **Try different distance metrics** (`metric="manhattan"`, `"chebyshev"`).
2. **Try KNN regression** on California Housing.
3. **Plot the decision boundary** of KNN on the first two features of Iris.
4. **Try `weights="uniform"` vs `"distance"`** and compare."""),
    ]
    save("10_knn.ipynb", cells)


# ============================================================
# 11. END-TO-END TITANIC
# ============================================================
def nb_end_to_end():
    cells = [
        md("""# 11. End-to-End ML Project - Titanic

**Topic:** Complete pipeline from raw data to final test evaluation. The capstone notebook.

**Dataset:** Titanic (seaborn).

**What you will do:**
1. Load and explore
2. Clean and engineer features
3. Compare 5 models
4. Tune the best one with GridSearchCV
5. Evaluate on a held-out test set
6. Inspect feature importance and predictions"""),
        code(INSTALL),
        code(IMPORTS),
        md("## 1. Load and explore"),
        code("""df = sns.load_dataset("titanic")
print(df.shape)
df.head()"""),
        code("""print("Missing values:")
print(df.isnull().sum().sort_values(ascending=False).head())
print()
print("Class balance:")
print(df["survived"].value_counts(normalize=True).round(3))"""),
        md("## 2. Clean and engineer"),
        code("""df = df[["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]].copy()
df["family_size"] = df["sibsp"] + df["parch"] + 1
df["is_alone"]    = (df["family_size"] == 1).astype(int)

df["age"].fillna(df["age"].median(), inplace=True)
df["embarked"].fillna(df["embarked"].mode()[0], inplace=True)

df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=True)
df.head()"""),
        md("## 3. Split"),
        code("""from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

X = df.drop(columns=["survived"])
y = df["survived"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(X_train.shape, X_test.shape)"""),
        md("## 4. Compare 5 models"),
        code("""from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

models = {
    "Logistic Regression":  LogisticRegression(max_iter=1000),
    "Decision Tree":        DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest":        RandomForestClassifier(n_estimators=300, random_state=42),
    "Gradient Boosting":    GradientBoostingClassifier(random_state=42),
    "KNN":                  KNeighborsClassifier(n_neighbors=7),
}

for name, m in models.items():
    pipe = Pipeline([("scaler", StandardScaler()), ("model", m)])
    s = cross_val_score(pipe, X_train, y_train, cv=5, scoring="accuracy")
    print(f"{name:25s}  CV acc = {s.mean():.3f} (+/- {s.std():.3f})")"""),
        md("## 5. Tune Gradient Boosting"),
        code("""pipe = Pipeline([
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
print("Best params:", grid.best_params_)
print(f"Best CV acc: {grid.best_score_:.3f}")"""),
        md("## 6. Final test evaluation"),
        code("""from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, roc_auc_score
)

best = grid.best_estimator_
y_pred  = best.predict(X_test)
y_proba = best.predict_proba(X_test)[:, 1]

print(f"Test accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"Test ROC-AUC:  {roc_auc_score(y_test, y_proba):.3f}")
print()
print(classification_report(y_test, y_pred, target_names=["Died", "Survived"]))"""),
        code("""cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Greys",
            xticklabels=["Died", "Survived"], yticklabels=["Died", "Survived"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Final Test Set Confusion Matrix")
plt.show()"""),
        md("## 7. Feature importance"),
        code("""model = best.named_steps["model"]
imp = pd.Series(model.feature_importances_, index=X.columns).sort_values()
plt.figure(figsize=(8, 5))
imp.plot.barh(color="gray")
plt.title("Gradient Boosting Feature Importance")
plt.show()"""),
        md("""## 8. Inspect predictions"""),
        code("""sample = X_test.head(10).copy()
sample["actual"]    = y_test.head(10).values
sample["predicted"] = best.predict(sample.drop(columns=["actual"]))
sample["prob_survived"] = best.predict_proba(sample.drop(columns=["actual", "predicted"]))[:, 1].round(3)
sample[["actual", "predicted", "prob_survived"]]"""),
        md("""## 9. Next steps

1. **Try XGBoost / LightGBM** - often beats GradientBoosting.
2. **Extract title from passenger name** (load raw Kaggle CSV) for a better feature.
3. **Save the model** with `joblib.dump(best, "titanic_model.pkl")`.
4. **Deploy** the model behind a Flask or FastAPI endpoint.
5. **Try a different problem** - House Prices, IMDB sentiment, MNIST digits."""),
    ]
    save("11_end_to_end_titanic.ipynb", cells)


def main():
    print("Building notebooks in:", OUT)
    nb_linear_regression()
    nb_logistic_regression()
    nb_regularization()
    nb_decision_trees()
    nb_random_forest()
    nb_gradient_boosting()
    nb_distance_metrics()
    nb_kmeans()
    nb_hierarchical()
    nb_knn()
    nb_end_to_end()
    print("Done. All notebooks built.")


if __name__ == "__main__":
    main()
