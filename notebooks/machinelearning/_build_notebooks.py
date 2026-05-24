"""
Builds all ML practice notebooks into the MLNOTEBOOK/ directory.

Each notebook is heavily commented with:
- Clear markdown intros and section headers
- Plain-English explanations BEFORE every code cell ("What we are about to do")
- Inline `# comments` on almost every line of code
- Markdown notes AFTER key cells ("What just happened")
- Exercises at the end

Run once:
    python _build_notebooks.py
"""
import json
from pathlib import Path

OUT = Path(__file__).parent

def _splitlines_keep_nl(text):
    """Split text into lines, keeping trailing \\n on every line except possibly the last.

    The .ipynb spec requires each entry in `source` to end with \\n (except the last)
    so that joining them recreates the original text. A plain str.split("\\n") drops
    the newlines and Jupyter renders all lines on a single line - which makes code
    cells syntactically invalid.
    """
    lines = text.split("\n")
    return [ln + "\n" for ln in lines[:-1]] + ([lines[-1]] if lines[-1] else [])

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": _splitlines_keep_nl(text)}

def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _splitlines_keep_nl(text),
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
INSTALL = """# If you're running locally, uncomment and run this once.
# In Google Colab, all of these are pre-installed - you can skip this cell.
# !pip install -q numpy pandas scikit-learn matplotlib seaborn scipy xgboost lightgbm"""

IMPORTS = """# Standard imports used in every ML notebook
import numpy as np                 # numerical arrays
import pandas as pd                # tabular data (DataFrames)
import matplotlib.pyplot as plt    # plotting
import seaborn as sns              # prettier statistical plots

# Set up plot style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# Set a random seed so results are reproducible
np.random.seed(42)"""


# ============================================================
# 01. LINEAR REGRESSION
# ============================================================
def nb_linear_regression():
    cells = [
        md("""# 01. Linear Regression - California Housing Prices

## What is this notebook about?

In this notebook we predict the **median value of houses** in California districts using **Linear Regression**.

Linear Regression is the simplest possible ML algorithm. It draws the best straight line (or hyperplane in multiple dimensions) through your data and uses that line to predict a number.

## What you will learn

1. How to **load** a real dataset
2. How to **explore** it with summary stats and plots
3. How to **train** a simple linear regression on one feature
4. How to **evaluate** a regression model with MAE, RMSE, and R²
5. How to extend to **multiple features** and **interpret the coefficients**

## Dataset

We use the **California Housing** dataset built into scikit-learn (no download needed).
- 20,640 rows (each row = one census district)
- 8 features (income, age of houses, location, etc.)
- Target: `MedHouseVal` (median house value, in $100,000s)

Let's get started!"""),
        code(INSTALL),
        code(IMPORTS),
        md("""## Step 1. Load the data

The dataset is included in scikit-learn. We just need to call one function. Setting `as_frame=True` returns it as a pandas DataFrame, which is easier to explore."""),
        code("""from sklearn.datasets import fetch_california_housing

# Load the dataset (returns features X and target y as a single DataFrame)
data = fetch_california_housing(as_frame=True)
df = data.frame                # the full DataFrame with both X and y

print(f"Dataset shape: {df.shape}")  # (rows, columns)
df.head()                            # show the first 5 rows"""),
        md("""**What just happened?**
We loaded a DataFrame `df` with 20,640 rows and 9 columns. The first 8 columns are features. The last column `MedHouseVal` is the target we want to predict.

Each row is one census district in California."""),
        code("""# .info() shows the data type and missing-value count of each column
print(df.info())

# .describe() gives summary statistics (mean, std, min, max, quartiles)
df.describe()"""),
        md("""## Step 2. Explore the data

Before modelling, **always look at your data**. We will:
1. Plot the distribution of the target.
2. Check correlations between features.
3. Plot the strongest predictor against the target."""),
        code("""# Distribution of the target value (price)
plt.figure(figsize=(10, 5))
sns.histplot(df["MedHouseVal"], bins=50, kde=True, color="gray")
plt.title("Distribution of Median House Value")
plt.xlabel("Median House Value ($100,000s)")
plt.show()"""),
        md("""**Notice:** the distribution is right-skewed and there is a spike at 5.0 - that's the maximum value (anything above $500k was capped). This is a real-world data quirk worth being aware of."""),
        code("""# Heatmap of how each pair of features correlates
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Matrix")
plt.show()"""),
        md("""**What to look for:** the bottom row (correlation with `MedHouseVal`) tells you which features are best for prediction. `MedInc` (median income) jumps out at +0.69 - far stronger than anything else."""),
        code("""# Scatter plot of the strongest predictor against the target
# Use a sample to avoid plotting 20,000 dots
plt.figure(figsize=(10, 6))
sns.scatterplot(x="MedInc", y="MedHouseVal", data=df.sample(2000), alpha=0.4, color="steelblue")
plt.title("Median Income vs Median House Value")
plt.show()"""),
        md("""You can see a clear upward trend: higher income areas tend to have more expensive houses. A straight line through this scatter would be a reasonable predictor.

## Step 3. Simple Linear Regression (one feature)

Let's fit a straight line using **only `MedInc`** as the predictor."""),
        code("""from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# X is the feature(s), y is the target
X = df[["MedInc"]]               # double brackets keep it as a DataFrame
y = df["MedHouseVal"]

# Split into 80% training data, 20% test data
# random_state=42 makes the split reproducible
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the model and fit it on the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Print the learned line: y = slope * x + intercept
print(f"Slope (coefficient):  {model.coef_[0]:.4f}")
print(f"Intercept:            {model.intercept_:.4f}")

# Evaluate the predictions on the test set
print(f"\\nMAE:   {mean_absolute_error(y_test, y_pred):.4f}    (avg error in $100k)")
print(f"RMSE:  {mean_squared_error(y_test, y_pred, squared=False):.4f}    (penalizes big errors more)")
print(f"R^2:   {r2_score(y_test, y_pred):.4f}    (1.0 = perfect, 0 = no better than mean)")"""),
        md("""**Reading the results:**
- **Slope ≈ 0.42** means: each $10k increase in median income corresponds to a $42k increase in predicted house value.
- **R² ≈ 0.47** means our one-variable model captures about 47% of the variance. Not bad, but we can do better with more features."""),
        code("""# Plot: actual values (dots) vs the fitted line (red)
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_test["MedInc"], y=y_test, alpha=0.3, color="steelblue", label="Actual")
sns.lineplot(x=X_test["MedInc"], y=y_pred, color="red", label="Predicted (line)")
plt.title("Linear Regression Fit: Income vs House Value")
plt.xlabel("Median Income")
plt.ylabel("Median House Value")
plt.legend()
plt.show()"""),
        md("""## Step 4. Multiple Linear Regression (all features)

Now let's use **all 8 features** instead of just one. The math is the same: we still find the best linear combination, but now in 8-dimensional space."""),
        code("""# Use all features except the target
X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

# Re-split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a new linear regression model
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluate
print(f"MAE:  {mean_absolute_error(y_test, y_pred):.4f}")
print(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.4f}")
print(f"R^2:  {r2_score(y_test, y_pred):.4f}")"""),
        md("""**R² should jump from ~0.47 to ~0.60.** Adding more features helped a lot.

Now let's see which features mattered most by inspecting the learned coefficients."""),
        code("""# Coefficients tell us how each feature contributes to the prediction
coef_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_,
}).sort_values("Coefficient", key=abs, ascending=False)  # sort by absolute size

print(coef_df)"""),
        md("""**Interpretation:**
- A **positive** coefficient means more of that feature → higher predicted price.
- A **negative** coefficient means more of that feature → lower predicted price.
- The **bigger the absolute value**, the more influence the feature has (assuming features are on similar scales)."""),
        code("""# Predicted vs Actual plot - the closer to the diagonal line, the better
plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_pred, alpha=0.3, color="steelblue")
plt.plot([0, 5], [0, 5], color="red", linestyle="--", label="Perfect prediction")
plt.xlabel("Actual House Value")
plt.ylabel("Predicted House Value")
plt.title("Predicted vs Actual House Values")
plt.legend()
plt.show()"""),
        md("""## Step 5. Exercises - try these on your own!

1. **Add polynomial features:**
   ```python
   from sklearn.preprocessing import PolynomialFeatures
   poly = PolynomialFeatures(degree=2)
   X_poly = poly.fit_transform(X_train)
   ```
   Does R² improve?

2. **Drop the most correlated features** (`AveRooms` and `AveBedrms` are highly correlated). Does it hurt much?

3. **Plot residuals**: `residuals = y_test - y_pred`. Are they centered around 0? Any patterns? Patterns suggest a non-linear effect you missed.

4. **Compute Adjusted R² manually**:
   `Adj R² = 1 - (1 - R²) * (n - 1) / (n - p - 1)` where n = sample size, p = number of features.

5. **Try a Kaggle dataset** (e.g. House Prices: Advanced Regression Techniques). The workflow is the same.

When you are done, head to **02 - Logistic Regression**!"""),
    ]
    save("01_linear_regression.ipynb", cells)


# ============================================================
# 02. LOGISTIC REGRESSION
# ============================================================
def nb_logistic_regression():
    cells = [
        md("""# 02. Logistic Regression - Titanic Survival Prediction

## What is this notebook about?

We predict whether a Titanic passenger **survived** or **died**, based on their age, ticket class, sex, and other info.

Despite the name, **Logistic Regression** is a **classification** algorithm (yes/no), not regression. It uses a sigmoid (S-curve) to convert a linear combination of features into a probability between 0 and 1.

## What you will learn

1. How to handle a real, **messy** dataset (with missing values)
2. **Feature engineering** to create more useful columns
3. **One-hot encoding** for categorical features
4. How to train Logistic Regression with a **Pipeline** (prevents data leakage)
5. **Classification metrics**: accuracy, precision, recall, F1, ROC-AUC
6. How to read a **confusion matrix** and **ROC curve**

## Dataset

The classic Titanic dataset, built into seaborn. Columns include `survived` (target), `pclass` (ticket class), `sex`, `age`, `sibsp` (siblings/spouses aboard), `parch` (parents/children aboard), `fare`, `embarked` (port).

Let's go!"""),
        code(INSTALL),
        code(IMPORTS),
        md("""## Step 1. Load and peek at the data"""),
        code("""# Load the Titanic dataset
df = sns.load_dataset("titanic")

print(f"Shape: {df.shape}")
df.head()"""),
        code("""# Check for missing values - this is critical before training!
# isnull() returns True/False, sum() counts the Trues per column
print("Missing values per column:")
print(df.isnull().sum().sort_values(ascending=False).head(8))"""),
        md("""**What we see:** `deck` is mostly missing (drop it). `age` has many missing values (we'll fill them in). `embarked` has just 2 missing values (fill with the most common port).

## Step 2. Clean and engineer features

We will:
1. Pick only the useful columns
2. Create new features (`family_size`, `is_alone`)
3. Fill missing values
4. Convert categorical columns to numbers"""),
        code("""# Keep only the columns we plan to use
df = df[["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]].copy()

# Engineer new features from existing ones
# family_size = number of family members onboard, including self
df["family_size"] = df["sibsp"] + df["parch"] + 1

# is_alone = 1 if travelling alone, else 0
df["is_alone"] = (df["family_size"] == 1).astype(int)

# Fill missing values
df["age"].fillna(df["age"].median(), inplace=True)              # use median age
df["embarked"].fillna(df["embarked"].mode()[0], inplace=True)   # use most common port

# One-hot encode the categorical columns: sex and embarked
# drop_first=True drops one dummy to avoid the "dummy variable trap"
df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=True)

print(f"Shape after cleaning: {df.shape}")
df.head()"""),
        md("""**What changed:** `sex` became `sex_male` (1 if male, 0 if female). `embarked` became 2 columns: `embarked_Q` and `embarked_S`.

## Step 3. Split into Training and Test sets

We hold out 20% of the data as a final test set the model will not see during training."""),
        code("""from sklearn.model_selection import train_test_split

# Separate features (X) from the target (y)
X = df.drop(columns=["survived"])
y = df["survived"]

# Split. stratify=y keeps class proportions the same in train and test (important for imbalanced data)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,         # 20% for testing
    random_state=42,       # reproducibility
    stratify=y,            # preserve class ratio
)
print(f"Training set: {X_train.shape}")
print(f"Test set:     {X_test.shape}")"""),
        md("""## Step 4. Train Logistic Regression in a Pipeline

A **Pipeline** chains preprocessing and modelling into one object. Why?
- It prevents **data leakage** (e.g. fitting the scaler on test data by accident).
- It makes your code cleaner.
- It treats the whole thing as one model for cross-validation."""),
        code("""from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# Pipeline: first scale features (mean 0, std 1), then fit logistic regression
pipe = Pipeline([
    ("scaler", StandardScaler()),                  # step 1: scale
    ("model",  LogisticRegression(max_iter=1000)), # step 2: classify
])

# Train on the training data only
pipe.fit(X_train, y_train)

# Make predictions on the test data
y_pred  = pipe.predict(X_test)                  # 0 or 1 predictions
y_proba = pipe.predict_proba(X_test)[:, 1]      # probabilities of survival"""),
        md("""## Step 5. Evaluate

We compute several metrics. Each tells us something different about the model."""),
        code("""from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve,
)

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.3f}    (overall fraction correct)")
print(f"Precision: {precision_score(y_test, y_pred):.3f}    (when we say survived, how often right)")
print(f"Recall:    {recall_score(y_test, y_pred):.3f}    (of actual survivors, how many we caught)")
print(f"F1 Score:  {f1_score(y_test, y_pred):.3f}    (harmonic mean of precision and recall)")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_proba):.3f}    (overall ranking quality)")
print()
print("Detailed report:")
print(classification_report(y_test, y_pred, target_names=["Died", "Survived"]))"""),
        md("""## Step 6. Confusion Matrix

A 2x2 grid showing how often we got each combination right or wrong."""),
        code("""# Build and plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Greys",
            xticklabels=["Died", "Survived"],
            yticklabels=["Died", "Survived"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

print("\\nReading the matrix:")
print(f"  True Negatives  (correctly predicted Died):     {cm[0, 0]}")
print(f"  False Positives (predicted Survived, but Died): {cm[0, 1]}")
print(f"  False Negatives (predicted Died, but Survived): {cm[1, 0]}")
print(f"  True Positives  (correctly predicted Survived): {cm[1, 1]}")"""),
        md("""## Step 7. ROC Curve

The ROC curve shows the trade-off between True Positive Rate and False Positive Rate as we vary the decision threshold. The **AUC** (area under the curve) summarizes this in one number from 0.5 (random) to 1.0 (perfect)."""),
        code("""# Compute ROC curve points
fpr, tpr, thresholds = roc_curve(y_test, y_proba)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color="black", lw=2, label=f"AUC = {roc_auc_score(y_test, y_proba):.2f}")
plt.plot([0, 1], [0, 1], color="gray", linestyle="--", label="Random guessing")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.show()"""),
        md("""## Step 8. Inspect the Coefficients

Logistic regression is interpretable. Each coefficient tells us how a feature affects the predicted log-odds of survival."""),
        code("""# Coefficients (positive = increases survival chance, negative = decreases)
coef_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": pipe.named_steps["model"].coef_[0],
}).sort_values("Coefficient", key=abs, ascending=False)

print(coef_df)"""),
        md("""**Typical findings:**
- `sex_male` strongly **negative** (men less likely to survive - "women and children first")
- `pclass` negative (higher class number = lower class = lower survival)
- `fare` positive (more expensive ticket = better cabin = higher survival)

These match what we know historically about the disaster.

## Step 9. Exercises

1. **Adjust the threshold** away from 0.5 (e.g. 0.3 or 0.7). How does it change precision and recall?
   ```python
   y_pred_threshold = (y_proba > 0.3).astype(int)
   ```

2. **Add L1 regularization** (Lasso) to do automatic feature selection:
   ```python
   LogisticRegression(penalty="l1", solver="liblinear", C=0.5)
   ```

3. **Try `class_weight="balanced"`** to handle the slight class imbalance.

4. **Plot the calibration curve** (`sklearn.calibration.calibration_curve`) - are the predicted probabilities trustworthy?

5. **Extract the `Title`** (Mr, Mrs, Miss, Master, Dr) from the original Kaggle Titanic data. It's often a strong predictor.

When done, head to **03 - Regularization**!"""),
    ]
    save("02_logistic_regression.ipynb", cells)


# ============================================================
# 03. REGULARIZATION
# ============================================================
def nb_regularization():
    cells = [
        md("""# 03. Regularization - Ridge, Lasso, Elastic Net

## What is this notebook about?

When a linear model has too many features or its data has noise, it can **overfit** - learning noise instead of patterns. **Regularization** adds a penalty to the loss so the model can't go wild.

Three flavours:
- **Ridge (L2 penalty):** shrinks all coefficients gently toward zero
- **Lasso (L1 penalty):** drives weak coefficients **exactly to zero** (automatic feature selection!)
- **Elastic Net:** mix of L1 and L2

## What you will learn

1. Why plain Linear Regression overfits when you have many features
2. How Ridge and Lasso shrink coefficients differently
3. How to **visualize coefficient paths** as regularization strength changes
4. How to **pick the best alpha** with cross-validation

## Dataset

California Housing again - same as notebook 01. We'll see what happens when we regularize."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, RidgeCV, LassoCV
from sklearn.metrics import mean_squared_error, r2_score

# Load the data
data = fetch_california_housing(as_frame=True)
df = data.frame
X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training shape: {X_train.shape}")"""),
        md("""## Step 1. Compare four models head-to-head

We'll train Linear, Ridge, Lasso, and Elastic Net using the same data and compare RMSE and R²."""),
        code("""def evaluate(name, model):
    \"\"\"Train one model in a Pipeline (with scaling) and print test scores.\"\"\"
    pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    rmse = mean_squared_error(y_test, pred, squared=False)
    r2 = r2_score(y_test, pred)
    print(f"{name:18s}  RMSE = {rmse:.4f}   R^2 = {r2:.4f}")
    return pipe

# Compare models
print("Test set performance:")
print("-" * 50)
models = {
    "Linear":       LinearRegression(),                          # no regularization
    "Ridge":        Ridge(alpha=1.0),                           # L2 penalty
    "Lasso":        Lasso(alpha=0.1),                           # L1 penalty
    "Elastic Net":  ElasticNet(alpha=0.1, l1_ratio=0.5),        # both
}
fitted = {name: evaluate(name, m) for name, m in models.items()}"""),
        md("""**On California Housing all four are similar** because the dataset isn't strongly affected by overfitting (only 8 features, 20k rows). Regularization shines more on datasets with **many features and few rows**.

## Step 2. Visualize how coefficients shrink as alpha grows

This is the most beautiful illustration of how Ridge vs Lasso behave differently. We sweep `alpha` from very small (no regularization) to very large (heavy regularization)."""),
        code("""# Try 50 different alpha values, log-spaced from 0.001 to 1000
alphas = np.logspace(-3, 3, 50)
ridge_coefs = []
lasso_coefs = []

# Scale once, outside the loop
scaler = StandardScaler().fit(X_train)
X_train_s = scaler.transform(X_train)

# For each alpha, fit Ridge and Lasso and record the coefficients
for a in alphas:
    r = Ridge(alpha=a).fit(X_train_s, y_train)
    l = Lasso(alpha=a, max_iter=5000).fit(X_train_s, y_train)
    ridge_coefs.append(r.coef_)
    lasso_coefs.append(l.coef_)

ridge_coefs = np.array(ridge_coefs)
lasso_coefs = np.array(lasso_coefs)

# Plot the two paths side by side
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for i, name in enumerate(X.columns):
    axes[0].plot(alphas, ridge_coefs[:, i], label=name)
    axes[1].plot(alphas, lasso_coefs[:, i], label=name)

for ax, title in zip(axes, ["Ridge (L2): smooth shrinkage", "Lasso (L1): exact zeros"]):
    ax.set_xscale("log")
    ax.set_xlabel("alpha (regularization strength)")
    ax.set_ylabel("coefficient value")
    ax.set_title(title)
    ax.legend(fontsize=8)
plt.tight_layout()
plt.show()"""),
        md("""**Key observation:**
- **Ridge** (left): all coefficients smoothly shrink toward zero but never reach it.
- **Lasso** (right): coefficients hit zero one by one as alpha grows. By alpha=10, only 1-2 features survive.

This is why Lasso is great for **feature selection**.

## Step 3. Pick the best alpha with cross-validation

Instead of guessing, let scikit-learn try many alphas and pick the best."""),
        code("""# RidgeCV and LassoCV try a list of alphas and select the one with best CV score
ridge_cv = RidgeCV(alphas=np.logspace(-3, 3, 50)).fit(X_train_s, y_train)
lasso_cv = LassoCV(alphas=np.logspace(-3, 3, 50), cv=5, max_iter=5000).fit(X_train_s, y_train)

print(f"Best Ridge alpha: {ridge_cv.alpha_:.5f}")
print(f"Best Lasso alpha: {lasso_cv.alpha_:.5f}")

# How many features did Lasso keep (non-zero coefficients)?
n_kept = (lasso_cv.coef_ != 0).sum()
print(f"\\nLasso kept {n_kept} of {len(X.columns)} features")
print("Selected features:", X.columns[lasso_cv.coef_ != 0].tolist())"""),
        md("""## Step 4. Exercises

1. **Generate noise features** to see Lasso filter them out:
   ```python
   X_noisy = X.copy()
   for i in range(20):
       X_noisy[f"noise_{i}"] = np.random.randn(len(X))
   ```
   Now train Lasso. How many noise features did it drop to zero?

2. **Try `Lasso(alpha=10)`** - what's left of the model?

3. **Plot RMSE vs alpha** for both Ridge and Lasso. Find the sweet spot visually.

4. **Apply to a higher-dimensional dataset** like the Ames Housing competition on Kaggle - regularization makes a much bigger difference there.

Next up: **04 - Decision Trees**!"""),
    ]
    save("03_regularization.ipynb", cells)


# ============================================================
# 04. DECISION TREES
# ============================================================
def nb_decision_trees():
    cells = [
        md("""# 04. Decision Trees - Iris Classification

## What is this notebook about?

A **Decision Tree** is a flowchart of yes/no questions. It splits the data step by step, asking the most useful question at each node. The leaves of the tree are the predictions.

Decision Trees are:
- **Interpretable** - you can read the tree and explain its decisions
- **Non-linear** - they can capture complex patterns
- **Prone to overfitting** - left unchecked, they memorize the training data

## What you will learn

1. How to **train** a decision tree
2. How to **visualize** the tree as a flowchart
3. How **tree depth** controls overfitting
4. How to read **feature importance**

## Dataset

The classic **Iris** dataset: 150 flowers, 4 measurements (sepal length/width, petal length/width), 3 species."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report

# Load Iris (built into sklearn)
iris = load_iris(as_frame=True)
X, y = iris.data, iris.target

print(f"Shape: {X.shape}")
print(f"Classes: {iris.target_names}")
X.head()"""),
        md("""## Step 1. Train a shallow tree (max_depth=3)

`max_depth=3` means the tree can ask at most 3 questions in a row before making a prediction. Limiting depth prevents overfitting."""),
        code("""# Train/test split with stratification (keeps class balance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Build the tree
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

# How does it score on training and test data?
print(f"Train accuracy: {tree.score(X_train, y_train):.3f}")
print(f"Test accuracy:  {tree.score(X_test, y_test):.3f}")"""),
        md("""## Step 2. Visualize the Tree

This is the killer feature of Decision Trees - you can literally read the model."""),
        code("""# plot_tree draws the flowchart of decisions
plt.figure(figsize=(16, 8))
plot_tree(
    tree,
    feature_names=X.columns,         # what to label each split
    class_names=iris.target_names,   # what to call each leaf
    filled=True,                     # color leaves by predicted class
    rounded=True,
)
plt.title("Decision Tree (max_depth=3)")
plt.show()"""),
        md("""**How to read this tree:**
1. Start at the top node (root).
2. Follow the **left** branch if the condition is **True**, **right** if **False**.
3. Each leaf shows the predicted class.

A doctor or business stakeholder can look at this tree and understand exactly how the model decides.

## Step 3. Watch the tree overfit

Now let's grow the tree deeper and see what happens to training vs test accuracy."""),
        code("""# Try depths 1 through 15
train_accs = []
test_accs = []
depths = range(1, 16)

for d in depths:
    t = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train, y_train)
    train_accs.append(t.score(X_train, y_train))
    test_accs.append(t.score(X_test, y_test))

# Plot the two curves
plt.figure(figsize=(10, 5))
plt.plot(depths, train_accs, "o-", label="Training accuracy", color="black")
plt.plot(depths, test_accs,  "o-", label="Test accuracy",     color="gray")
plt.xlabel("max_depth")
plt.ylabel("Accuracy")
plt.title("Decision Tree: Train vs Test Accuracy by Depth")
plt.legend()
plt.show()"""),
        md("""**The classic overfitting picture:**
- **Training accuracy** keeps rising toward 1.0 as the tree grows.
- **Test accuracy** plateaus or even drops past a certain depth.

The sweet spot is somewhere in the middle. For Iris, depth 3-4 is great.

## Step 4. Feature Importance

Decision Trees give you a free score for how useful each feature was."""),
        code("""# feature_importances_ sums to 1.0 across all features
importance = pd.Series(tree.feature_importances_, index=X.columns).sort_values()

# Plot as horizontal bar chart
plt.figure(figsize=(8, 4))
importance.plot.barh(color="gray")
plt.title("Feature Importance")
plt.xlabel("Relative importance (sums to 1.0)")
plt.show()

print(importance)"""),
        md("""**Petal length and petal width** dominate. The tree barely uses sepal measurements. This matches biology: petals differ much more between species than sepals.

## Step 5. Exercises

1. **Try `criterion="entropy"`** instead of the default `"gini"`. Does it change the tree?

2. **Set `min_samples_leaf=10`** - prevents leaves with fewer than 10 samples. Compare to depth limit.

3. **Try the Wine dataset** instead of Iris:
   ```python
   from sklearn.datasets import load_wine
   wine = load_wine(as_frame=True)
   ```

4. **Train a `DecisionTreeRegressor`** on California Housing data. The visualization works the same way.

5. **Export the tree as text** with `from sklearn.tree import export_text` and read it.

Next: **05 - Random Forest** (a forest of decision trees)!"""),
    ]
    save("04_decision_trees.ipynb", cells)


# ============================================================
# 05. RANDOM FOREST
# ============================================================
def nb_random_forest():
    cells = [
        md("""# 05. Random Forest - Breast Cancer Diagnosis

## What is this notebook about?

A **Random Forest** is many decision trees trained on random slices of the data. Each tree votes on the prediction, and the majority wins.

This simple idea (the "wisdom of crowds") fixes the biggest weakness of Decision Trees: their tendency to overfit.

## What you will learn

1. How a Random Forest improves over a single Decision Tree
2. How the number of trees (`n_estimators`) affects stability
3. How to read **feature importance** in a Random Forest
4. How to evaluate a binary classifier with **ROC-AUC**

## Dataset

The **Breast Cancer Wisconsin** dataset: 569 tumour samples, 30 features (cell measurements), and a binary target (malignant or benign). Built into sklearn.

This is a classic medical-classification task and exactly the kind of problem Random Forests excel at."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, roc_auc_score, confusion_matrix,
)

# Load the dataset
data = load_breast_cancer(as_frame=True)
X, y = data.data, data.target

print(f"Shape: {X.shape}")
print(f"Classes: {data.target_names}")
print(f"Class distribution: {np.bincount(y)}")"""),
        md("""## Step 1. Single Tree vs Random Forest

Let's compare them head to head."""),
        code("""X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# A single decision tree (no depth limit - so it might overfit)
tree   = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)

# A random forest of 200 trees
forest = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)

# Compare them on accuracy AND ROC-AUC
print(f"{'Model':20s} {'Accuracy':>10s} {'ROC-AUC':>10s}")
print("-" * 42)
for name, m in [("Decision Tree", tree), ("Random Forest", forest)]:
    pred = m.predict(X_test)
    proba = m.predict_proba(X_test)[:, 1]
    print(f"{name:20s} {accuracy_score(y_test, pred):>10.3f} {roc_auc_score(y_test, proba):>10.3f}")"""),
        md("""**Random Forest wins** because averaging 200 trees smooths out the variance of a single tree.

## Step 2. Effect of the number of trees

More trees = more stable predictions, with diminishing returns past a certain point."""),
        code("""# Try several values of n_estimators and measure CV accuracy
ns = [1, 5, 10, 25, 50, 100, 200, 500]
scores = []

for n in ns:
    rf = RandomForestClassifier(n_estimators=n, random_state=42)
    s = cross_val_score(rf, X_train, y_train, cv=5, scoring="accuracy").mean()
    scores.append(s)
    print(f"n_estimators = {n:4d} -> CV accuracy = {s:.4f}")

# Plot the curve
plt.figure(figsize=(10, 5))
plt.plot(ns, scores, "o-", color="black")
plt.xscale("log")
plt.xlabel("Number of trees (n_estimators)")
plt.ylabel("CV accuracy")
plt.title("More trees stabilize predictions, with diminishing returns")
plt.show()"""),
        md("""**Common practice:** start with `n_estimators=100`, then go up to 500 if you have the compute. Past that the gain is tiny.

## Step 3. Feature Importance

Random Forests aggregate feature importance across all 200 trees, giving a robust signal."""),
        code("""# Take only the top 15 most important features (out of 30)
imp = pd.Series(forest.feature_importances_, index=X.columns).sort_values().tail(15)

plt.figure(figsize=(8, 6))
imp.plot.barh(color="gray")
plt.title("Top 15 Most Important Features")
plt.xlabel("Importance")
plt.show()"""),
        md("""**What you'll see:** measurements like `worst concave points`, `worst perimeter`, and `worst area` dominate. These describe the most extreme tumour cells observed - which makes biological sense.

## Step 4. Confusion Matrix"""),
        code("""# Get predictions on the test set
y_pred = forest.predict(X_test)

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Greys",
            xticklabels=data.target_names, yticklabels=data.target_names)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Random Forest Confusion Matrix")
plt.show()

# In medical contexts, false negatives (missed malignancies) are the most costly.
# Look closely at the off-diagonal numbers.
print("\\nDetailed report:")
print(classification_report(y_test, y_pred, target_names=data.target_names))"""),
        md("""## Step 5. Exercises

1. **Try `max_features="sqrt"` vs `"log2"` vs `1.0`** (use all features). The default for classification is `"sqrt"`. How does it affect the score?

2. **Train a `RandomForestRegressor`** on California Housing.

3. **Use the OOB score** instead of cross-validation:
   ```python
   rf = RandomForestClassifier(n_estimators=200, oob_score=True).fit(X, y)
   print(rf.oob_score_)
   ```

4. **Time how long it takes** to train 1000 trees vs 100. Does it scale linearly?

5. **Try a Kaggle dataset** like the Telco Customer Churn dataset.

Next: **06 - Gradient Boosting & XGBoost**!"""),
    ]
    save("05_random_forest.ipynb", cells)


# ============================================================
# 06. GRADIENT BOOSTING / XGBOOST
# ============================================================
def nb_gradient_boosting():
    cells = [
        md("""# 06. Gradient Boosting & XGBoost - Titanic

## What is this notebook about?

**Gradient Boosting** trains many decision trees **sequentially**, where each new tree fixes the mistakes of the previous ones. It is one of the strongest classical ML algorithms.

**XGBoost** is a heavily optimized gradient boosting library that has won countless ML competitions.

## What you will learn

1. How Gradient Boosting differs from Random Forest (sequential vs parallel)
2. How to use **scikit-learn's GradientBoostingClassifier** and **XGBoost**
3. How to **tune hyperparameters** with GridSearchCV
4. Why `learning_rate` is the most important boosting hyperparameter

## Dataset

Back to Titanic. We've already cleaned it in notebook 02 - we'll redo the cleaning briefly and then focus on modelling."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

# Try to import XGBoost - if not installed, the notebook will skip XGBoost cells
try:
    from xgboost import XGBClassifier
    HAS_XGB = True
    print("XGBoost is available")
except ImportError:
    HAS_XGB = False
    print("XGBoost not installed. Run: pip install xgboost")"""),
        md("""## Step 1. Load and prepare Titanic (same as notebook 02)"""),
        code("""# Load + clean + engineer features (same as notebook 02)
df = sns.load_dataset("titanic")
df = df[["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]].copy()
df["family_size"] = df["sibsp"] + df["parch"] + 1
df["is_alone"]    = (df["family_size"] == 1).astype(int)
df["age"].fillna(df["age"].median(), inplace=True)
df["embarked"].fillna(df["embarked"].mode()[0], inplace=True)
df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=True)

X = df.drop(columns=["survived"])
y = df["survived"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Training shape: {X_train.shape}")"""),
        md("""## Step 2. Compare three models

Random Forest, Gradient Boosting, and XGBoost on the same data."""),
        code("""# Random Forest baseline
rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(X_train, y_train)

# scikit-learn's Gradient Boosting
gb = GradientBoostingClassifier(random_state=42).fit(X_train, y_train)

print(f"{'Model':22s} {'Acc':>8s} {'AUC':>8s}")
print("-" * 40)
for name, m in [("Random Forest", rf), ("Gradient Boosting", gb)]:
    pred  = m.predict(X_test)
    proba = m.predict_proba(X_test)[:, 1]
    print(f"{name:22s} {accuracy_score(y_test, pred):>8.3f} {roc_auc_score(y_test, proba):>8.3f}")

# XGBoost (only if available)
if HAS_XGB:
    xgb = XGBClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42,
    )
    xgb.fit(X_train, y_train)
    pred  = xgb.predict(X_test)
    proba = xgb.predict_proba(X_test)[:, 1]
    print(f"{'XGBoost':22s} {accuracy_score(y_test, pred):>8.3f} {roc_auc_score(y_test, proba):>8.3f}")"""),
        md("""## Step 3. Tune Gradient Boosting with GridSearchCV

The most impactful hyperparameters are:
- `n_estimators`: how many boosting rounds (more = more powerful, but slower and can overfit)
- `learning_rate`: step size at each round (smaller = more careful, needs more rounds)
- `max_depth`: depth of each tree (small trees, usually 2-4)

We'll search over a small grid and use 5-fold CV."""),
        code("""# 3 x 2 x 3 = 18 combinations, each evaluated with 5-fold CV = 90 fits
param_grid = {
    "learning_rate": [0.05, 0.1, 0.2],
    "n_estimators":  [100, 300],
    "max_depth":     [2, 3, 4],
}

grid = GridSearchCV(
    GradientBoostingClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring="roc_auc",     # ROC-AUC is robust to class imbalance
    n_jobs=-1,             # use all CPU cores
    verbose=1,
)
grid.fit(X_train, y_train)

print("\\nBest hyperparameters:", grid.best_params_)
print(f"Best CV ROC-AUC:        {grid.best_score_:.3f}")

# Evaluate the best model on the test set
best = grid.best_estimator_
test_auc = roc_auc_score(y_test, best.predict_proba(X_test)[:, 1])
print(f"Test ROC-AUC:           {test_auc:.3f}")"""),
        md("""**The best hyperparameters tell you something:** if `learning_rate=0.05` won, that means small steps with many trees are better than big steps with few trees. This is almost always the lesson with boosting.

## Step 4. Feature Importance

Gradient Boosting also provides feature importance scores."""),
        code("""# Sort and plot
imp = pd.Series(best.feature_importances_, index=X.columns).sort_values()

plt.figure(figsize=(8, 5))
imp.plot.barh(color="gray")
plt.title("Gradient Boosting Feature Importance")
plt.xlabel("Importance")
plt.show()"""),
        md("""## Step 5. Exercises

1. **Try LightGBM** instead of XGBoost (often faster, similar accuracy):
   ```python
   from lightgbm import LGBMClassifier
   lgb = LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=31)
   ```

2. **Use early stopping** with XGBoost so it stops adding trees when the validation score stops improving:
   ```python
   xgb.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=20)
   ```

3. **Tune `subsample` and `colsample_bytree`** (both 0.6-1.0). They add randomness like Random Forest does.

4. **Try a Kaggle competition** dataset. Boosting is the go-to choice for tabular data competitions.

Next: **07 - Distance Metrics**!"""),
    ]
    save("06_gradient_boosting_xgboost.ipynb", cells)


# ============================================================
# 07. DISTANCE METRICS
# ============================================================
def nb_distance_metrics():
    cells = [
        md("""# 07. Distance & Similarity Metrics

## What is this notebook about?

Many ML algorithms (KNN, K-Means, hierarchical clustering, recommender systems) need a way to measure **how similar** two data points are.

This notebook introduces the most common distance/similarity metrics, when to use each, and how to compute them.

## What you will learn

1. **Euclidean distance** - the everyday "ruler" distance
2. **Manhattan distance** - city-block distance
3. **Cosine similarity** - angle between vectors (great for text)
4. **Pearson correlation** - linear association between variables
5. **Jaccard similarity** - overlap between sets

## Datasets

Iris (numerical features) and synthetic sets (for Jaccard)."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_iris
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances, cosine_similarity
from scipy.spatial.distance import pdist, squareform

# Load Iris
iris = load_iris(as_frame=True)
X = iris.data.values     # convert to numpy array
y = iris.target.values
print(f"Shape: {X.shape}")"""),
        md("""## Step 1. Euclidean Distance

This is the everyday "as the crow flies" distance. For two points (x1, y1) and (x2, y2):

`distance = sqrt( (x1-x2)^2 + (y1-y2)^2 )`

Generalizes to any number of dimensions."""),
        code("""# Take the first 5 flowers
sample = X[:5]

# Pairwise euclidean distances - returns a 5x5 matrix
print("Euclidean distance matrix (5 flowers):")
print(np.round(euclidean_distances(sample), 2))"""),
        md("""**Reading the matrix:** entry [i, j] is the distance between flower i and flower j. Diagonal is 0 (same flower). Matrix is symmetric (distance from A to B = distance from B to A).

## Step 2. Manhattan Distance

Distance you'd walk on a city grid - sum of absolute differences along each axis.

`distance = |x1-x2| + |y1-y2|`"""),
        code("""print("Manhattan distance matrix (5 flowers):")
print(np.round(manhattan_distances(sample), 2))"""),
        md("""Notice Manhattan distances are larger than Euclidean (the diagonal shortcut is unavailable on a grid).

## Step 3. Cosine Similarity

Cosine similarity measures the **angle** between two vectors, **ignoring their magnitudes**. It ranges from -1 (opposite directions) to 1 (same direction), with 0 meaning perpendicular.

This is the **go-to metric for text** because document length shouldn't affect similarity."""),
        code("""print("Cosine similarity matrix (5 flowers):")
print(np.round(cosine_similarity(sample), 3))"""),
        md("""Almost all 1.0 here - because all flowers point in roughly the same direction in feature space (they all have positive values for all 4 measurements). Cosine works better when items can have very different magnitudes but similar profiles.

## Step 4. Pearson Correlation

Pearson measures **linear association** between two variables. Range from -1 to 1.
- +1 = perfectly positively correlated
- 0 = no linear relation
- -1 = perfectly negatively correlated"""),
        code("""# Correlation between features (not between samples!)
print("Pearson correlation between features:")
print(iris.data.corr().round(2))

# Visualize as a heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(iris.data.corr(), annot=True, cmap="coolwarm", center=0)
plt.title("Pearson Correlation between Iris Features")
plt.show()"""),
        md("""Petal length and petal width are very strongly correlated (0.96) - they grow together.

## Step 5. Jaccard Similarity

For comparing **sets**, not numbers. It's the size of the intersection divided by the size of the union.

`Jaccard(A, B) = |A ∩ B| / |A ∪ B|`

Used heavily in document deduplication, recommender systems, and shopping cart analysis."""),
        code("""# Three users and the genres they like
user1 = {"action", "comedy", "thriller", "drama"}
user2 = {"comedy", "drama", "romance"}
user3 = {"horror", "thriller", "action"}

def jaccard_sim(a, b):
    \"\"\"Jaccard similarity between two sets.\"\"\"
    return len(a & b) / len(a | b)

# Compare all pairs
print(f"User1 vs User2 Jaccard: {jaccard_sim(user1, user2):.2f}  (overlap: {user1 & user2})")
print(f"User1 vs User3 Jaccard: {jaccard_sim(user1, user3):.2f}  (overlap: {user1 & user3})")
print(f"User2 vs User3 Jaccard: {jaccard_sim(user2, user3):.2f}  (overlap: {user2 & user3})")"""),
        md("""**A simple recommender:** find the user most similar to you (highest Jaccard), then recommend the genres they liked that you don't yet.

## Step 6. Visualize the full Iris distance matrix"""),
        code("""# Pairwise distances between ALL 150 flowers, visualized as a heatmap
dist = squareform(pdist(X, metric="euclidean"))

plt.figure(figsize=(8, 6))
sns.heatmap(dist, cmap="Greys")
plt.title("Pairwise Euclidean Distance Matrix (150 flowers)")
plt.xlabel("Flower index")
plt.ylabel("Flower index")
plt.show()"""),
        md("""**The block pattern reveals the species!** Iris setosa (first 50 flowers) is far from the others. Versicolor (50-100) and virginica (100-150) are closer to each other but still distinct. This is exactly what clustering algorithms detect.

## Step 7. Exercises

1. **Find the most similar pair of flowers** with each metric (`np.argmin` of the off-diagonal entries).

2. **Compare cosine vs euclidean** when one feature is on a much bigger scale:
   ```python
   X_unscaled = X.copy()
   X_unscaled[:, 0] *= 1000   # blow up feature 0
   ```
   Euclidean breaks. Cosine still works.

3. **Build a tiny recommender** that suggests songs to a user based on cosine similarity of listening histories.

4. **Compute Hamming distance** between two equal-length binary strings.

5. **Try the Jaccard metric** on Wikipedia article shingles to find duplicate articles.

Next: **08 - K-Means Clustering**!"""),
    ]
    save("07_distance_metrics.ipynb", cells)


# ============================================================
# 08. K-MEANS CLUSTERING
# ============================================================
def nb_kmeans():
    cells = [
        md("""# 08. K-Means Clustering

## What is this notebook about?

**K-Means** is the most popular clustering algorithm. Given a number K, it partitions your data into K groups by:

1. Picking K random "centroids".
2. Assigning each data point to its nearest centroid.
3. Moving each centroid to the mean of its assigned points.
4. Repeating until nothing changes.

The result: K clean groups, with no labels needed.

## What you will learn

1. How K-Means partitions a synthetic dataset
2. How to **pick the right K** with the **elbow method** and **silhouette score**
3. How to apply K-Means to a real customer-segmentation problem
4. Why **scaling matters** before K-Means

## Datasets

- Synthetic blobs (so you can SEE the clusters)
- Mall Customers from Kaggle (loaded from public URL, no Kaggle account needed)"""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score"""),
        md("""## Step 1. Synthetic blobs - the easy case

Make 4 clearly separated groups so we can see exactly what K-Means does."""),
        code("""# Create 400 points in 4 clusters
X, _ = make_blobs(n_samples=400, centers=4, cluster_std=0.8, random_state=42)

# Plot the raw points (no labels yet)
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], s=15, color="gray")
plt.title("Raw data (we don't know the groups yet)")
plt.show()"""),
        md("""You can see 4 visual clumps. But the algorithm doesn't get to see this picture - it only sees coordinates."""),
        code("""# Run K-Means with K=4
# n_init=10 means try 10 random starts and keep the best
km = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X)

# Plot points colored by cluster, with red X marks at the centroids
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=km.labels_, s=15, cmap="tab10")
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
            s=200, marker="X", c="red", label="centroids")
plt.title("K-Means clusters (K=4)")
plt.legend()
plt.show()"""),
        md("""K-Means correctly recovered the 4 groups. But how would you have known to use K=4 without looking?

## Step 2. Elbow method + silhouette score

If you don't know K up-front, try several values and look at:

1. **Inertia (WCSS):** sum of squared distances from each point to its centroid. Always decreases as K grows. Look for an "elbow" where the decrease slows.
2. **Silhouette score:** measures cluster separation. Range -1 to 1, higher is better."""),
        code("""ks = range(1, 11)
inertias = []
silhouettes = []

for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    inertias.append(km.inertia_)
    if k > 1:                                    # silhouette undefined for K=1
        silhouettes.append(silhouette_score(X, km.labels_))

# Plot side by side
fig, ax = plt.subplots(1, 2, figsize=(14, 4))

ax[0].plot(ks, inertias, "o-", color="black")
ax[0].set_xlabel("K")
ax[0].set_ylabel("Inertia (WCSS)")
ax[0].set_title("Elbow Method - look for the bend")

ax[1].plot(list(ks)[1:], silhouettes, "o-", color="black")
ax[1].set_xlabel("K")
ax[1].set_ylabel("Silhouette score (higher is better)")
ax[1].set_title("Silhouette Score by K")
plt.show()"""),
        md("""**Both plots peak/elbow at K=4** - confirming the right answer. In real-world data this is rarely so clean, but the same techniques apply.

## Step 3. Real data - Mall Customers

The Mall Customers dataset has 200 customers with their annual income and spending score. We want to find natural customer segments."""),
        code("""# Try to load from a public URL (no Kaggle account needed)
url = "https://raw.githubusercontent.com/SteffiPeTaffy/machineLearningAZ/master/Machine%20Learning%20A-Z%20Template%20Folder/Part%204%20-%20Clustering/Section%2024%20-%20K-Means%20Clustering/Mall_Customers.csv"
try:
    mall = pd.read_csv(url)
    print(f"Loaded {len(mall)} customers")
    mall.head()
except Exception as e:
    print(f"Could not fetch online: {e}")
    print("If this fails, download Mall_Customers.csv manually from Kaggle and load it.")
    mall = None"""),
        code("""if mall is not None:
    # Pick the two most useful features for visualization
    Xm = mall[["Annual Income (k$)", "Spending Score (1-100)"]].values

    # IMPORTANT: scale features! K-Means is distance-based.
    Xm_s = StandardScaler().fit_transform(Xm)

    # Try K=5 (a common number for customer segments)
    km = KMeans(n_clusters=5, n_init=10, random_state=42).fit(Xm_s)

    # Plot in original (unscaled) space for interpretability
    plt.figure(figsize=(10, 6))
    plt.scatter(Xm[:, 0], Xm[:, 1], c=km.labels_, s=40, cmap="tab10")
    plt.xlabel("Annual Income (k$)")
    plt.ylabel("Spending Score (1-100)")
    plt.title("Mall Customer Segments (K=5)")
    plt.show()"""),
        md("""**Real-world segments revealed!** You'll typically see:
- High income, high spending (the dream customer)
- High income, low spending (target with marketing!)
- Low income, high spending (enthusiasts to cherish)
- Low income, low spending (value seekers)
- Average everything (the middle)

This is exactly how marketing teams use K-Means.

## Step 4. Exercises

1. **Try different K values** (3, 4, 6, 7) and decide which makes most business sense.

2. **Use all numeric features** of Mall Customers including Age. Does the result change?

3. **Compare `init="random"` vs `"k-means++"`** with `n_init=1`. K-means++ is the smart initialization.

4. **Try clustering Iris** without using the species labels. Does K-Means recover the 3 species?

5. **Try DBSCAN** instead - it doesn't need K up-front and finds arbitrary shapes:
   ```python
   from sklearn.cluster import DBSCAN
   ```

Next: **09 - Hierarchical Clustering**!"""),
    ]
    save("08_kmeans_clustering.ipynb", cells)


# ============================================================
# 09. HIERARCHICAL CLUSTERING
# ============================================================
def nb_hierarchical():
    cells = [
        md("""# 09. Hierarchical Clustering

## What is this notebook about?

Unlike K-Means (which gives flat groups), **Hierarchical Clustering** builds a **tree** of clusters from the bottom up:

1. Start with each point as its own cluster.
2. Repeatedly merge the two closest clusters.
3. Stop when only one cluster remains.

The full tree is called a **dendrogram**, and you can "cut" it at any level to get K flat clusters.

## What you will learn

1. How to compute hierarchical clustering with **scipy** and **sklearn**
2. How to read a **dendrogram**
3. How to **cut** the dendrogram to get K clusters
4. How **linkage methods** (ward, complete, average, single) change the result

## Dataset

Iris again - perfect for clustering since we know the true 3 species and can verify."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

# Load and scale (always scale before distance-based methods)
iris = load_iris(as_frame=True)
X = StandardScaler().fit_transform(iris.data)
y = iris.target.values
print(f"Shape: {X.shape}")"""),
        md("""## Step 1. Build the linkage matrix

`linkage()` runs the full hierarchical clustering and returns a matrix describing every merge."""),
        code("""# Ward linkage: merges the pair of clusters that produces the smallest increase in within-cluster variance
# It's the most popular default
Z = linkage(X, method="ward")

print(f"Linkage matrix shape: {Z.shape}")
print("First 5 merges (each row = [cluster_a, cluster_b, distance, num_points_in_new_cluster]):")
print(Z[:5])"""),
        md("""## Step 2. Plot the dendrogram

This is the entire history of merges visualized."""),
        code("""plt.figure(figsize=(14, 6))
dendrogram(
    Z,
    color_threshold=10,    # color the branches below this distance
    no_labels=True,         # too many points to label
)
plt.title("Iris Dendrogram (Ward Linkage)")
plt.xlabel("Samples")
plt.ylabel("Distance at which clusters merged")
plt.axhline(y=10, color="red", linestyle="--", label="cut here for 3 clusters")
plt.legend()
plt.show()"""),
        md("""**How to read this:**
- Each leaf at the bottom is one flower.
- Vertical lines going up show merges. Higher = clusters were further apart.
- A horizontal line cutting across the tree creates clusters: each connected sub-tree below is one cluster.
- Cut high → few big clusters. Cut low → many small clusters.

The red dashed line shows where to cut for **3 clusters** - matching the 3 species!

## Step 3. Cut the tree at K=3 and compare to true species"""),
        code("""# fcluster cuts the tree to give exactly 3 clusters
labels = fcluster(Z, t=3, criterion="maxclust")

# Adjusted Rand Index measures how well the predicted clusters match the true labels
# 1.0 = perfect match, 0 = random
ari = adjusted_rand_score(y, labels)
print(f"Adjusted Rand Index (vs true species): {ari:.3f}")
print(f"  1.0 = perfect, 0.0 = random")

# Visualize the clusters in 2D
plt.figure(figsize=(10, 5))
sns.scatterplot(
    x=iris.data["petal length (cm)"],
    y=iris.data["petal width (cm)"],
    hue=labels, palette="tab10", s=60,
)
plt.title("Hierarchical Clusters (cut at K=3) on Iris")
plt.show()"""),
        md("""ARI of ~0.6-0.8 typically. Iris has overlapping species, so perfect recovery is hard - but the algorithm got most of it right.

## Step 4. Compare four linkage methods

Linkage = the rule for measuring distance between two clusters when deciding what to merge next.

- **Single:** distance between the two closest points (creates "chains")
- **Complete:** distance between the two farthest points (creates compact clusters)
- **Average:** average pairwise distance
- **Ward:** minimizes within-cluster variance (default, usually best)"""),
        code("""fig, axes = plt.subplots(2, 2, figsize=(14, 8))
for ax, method in zip(axes.ravel(), ["single", "complete", "average", "ward"]):
    Z = linkage(X, method=method)
    dendrogram(Z, ax=ax, no_labels=True, color_threshold=0)
    ax.set_title(f"Linkage: {method}")
plt.tight_layout()
plt.show()"""),
        md("""Notice how dramatically different the trees look. **Ward** is usually a safe default.

## Step 5. Exercises

1. **Cut at different K values** (2, 3, 4, 5) and compute the ARI for each.

2. **Try the Breast Cancer dataset** with hierarchical clustering. Does it separate malignant from benign?

3. **Visualize a heatmap with clustered rows and columns** using `sns.clustermap`:
   ```python
   sns.clustermap(iris.data, cmap="viridis")
   ```

4. **Compare with K-Means** on the same data using ARI - which gives a higher score?

5. **Try `sklearn.cluster.AgglomerativeClustering`** - it's the sklearn API for the same algorithm.

Next: **10 - K-Nearest Neighbours**!"""),
    ]
    save("09_hierarchical_clustering.ipynb", cells)


# ============================================================
# 10. KNN
# ============================================================
def nb_knn():
    cells = [
        md("""# 10. K-Nearest Neighbours (KNN)

## What is this notebook about?

KNN is the simplest possible algorithm. To predict a new point:
1. Find the K most similar points in the training data.
2. Take the majority vote (classification) or average (regression).

That's it. There's **no real "training"** - the algorithm just memorizes the training data and uses it at predict time.

## What you will learn

1. How to use KNN for classification
2. Why **feature scaling is critical** for KNN (distances are everything!)
3. How to choose **K** with cross-validation
4. KNN's strengths (simplicity) and weaknesses (slow at predict time)

## Datasets

Iris and Wine - both built into sklearn."""),
        code(INSTALL),
        code(IMPORTS),
        code("""from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score"""),
        md("""## Step 1. KNN with and without scaling

KNN measures distances between points. If one feature has a huge range (income in $) and another has a small range (age in years), the big-range feature dominates. **Always scale before KNN.**"""),
        code("""# Load Iris
iris = load_iris(as_frame=True)
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# WITHOUT scaling
knn1 = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
acc_raw = knn1.score(X_test, y_test)
print(f"Raw features (no scaling):    {acc_raw:.3f}")

# WITH scaling, using a Pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=5)),
])
pipe.fit(X_train, y_train)
acc_scaled = pipe.score(X_test, y_test)
print(f"Scaled features:               {acc_scaled:.3f}")"""),
        md("""On Iris, all 4 features are already on similar scales (centimeters), so scaling makes little difference. You'll see a bigger effect on the Wine dataset later.

## Step 2. Choose K with cross-validation

Small K = sensitive to noise (overfit). Large K = too smooth (underfit). Find the sweet spot."""),
        code("""# Try K from 1 to 30
ks = range(1, 31)
scores = []

for k in ks:
    pipe = Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=k))])
    s = cross_val_score(pipe, X_train, y_train, cv=5).mean()
    scores.append(s)

plt.figure(figsize=(10, 5))
plt.plot(ks, scores, "o-", color="black")
plt.xlabel("K (number of neighbours)")
plt.ylabel("Cross-validation accuracy")
plt.title("Choosing K for KNN (Iris)")
plt.show()

best_k = ks[np.argmax(scores)]
print(f"Best K: {best_k}")"""),
        md("""**Common rule of thumb:** start with K = sqrt(n_samples). On Iris that's ≈ 12.

## Step 3. KNN on the Wine dataset

Wine has 13 chemical features with very different scales (some near 1, others near 1000). This is where scaling REALLY matters."""),
        code("""# Load Wine
wine = load_wine(as_frame=True)
X, y = wine.data, wine.target

# Look at the wildly different feature scales
print("Feature mean values (notice the huge differences):")
print(X.mean().round(2))"""),
        code("""X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# WITHOUT scaling - typically performs poorly
knn_raw = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
print(f"WITHOUT scaling: {knn_raw.score(X_test, y_test):.3f}")

# WITH scaling, using weights="distance" so closer neighbours count more
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=7, weights="distance")),
])
pipe.fit(X_train, y_train)
print(f"WITH scaling:    {pipe.score(X_test, y_test):.3f}")"""),
        md("""**Massive jump from scaling.** This is why every KNN tutorial hammers on scaling.

## Step 4. Exercises

1. **Try different distance metrics:**
   ```python
   KNeighborsClassifier(n_neighbors=5, metric="manhattan")
   ```

2. **Try KNN regression** on California Housing (`KNeighborsRegressor`). Is it competitive with linear regression?

3. **Plot the decision boundary** of KNN on the first two Iris features. (Use `sklearn.inspection.DecisionBoundaryDisplay`.)

4. **Time the prediction** of KNN with 10,000 training points vs 1,000. KNN gets slow on big data.

5. **Compare `weights="uniform"` vs `weights="distance"`**. Distance weighting often wins.

Next: **11 - End-to-End Titanic** (the capstone)!"""),
    ]
    save("10_knn.ipynb", cells)


# ============================================================
# 11. END-TO-END TITANIC
# ============================================================
def nb_end_to_end():
    cells = [
        md("""# 11. End-to-End ML Project - Titanic (Capstone)

## What is this notebook about?

This is the **capstone notebook**. We tie everything together with a complete ML pipeline:

1. **Load** raw data
2. **Explore** with visualizations and stats
3. **Clean** missing values
4. **Engineer** features
5. **Split** into train/test
6. **Compare** 5 different models with cross-validation
7. **Tune** the best one with GridSearchCV
8. **Evaluate** on the held-out test set with multiple metrics
9. **Inspect** feature importance and individual predictions

This workflow generalizes to **any tabular ML problem**. Drop in your own dataset and 80% of the code stays the same.

## Dataset

The Titanic dataset (built into seaborn). Goal: predict whether a passenger survived."""),
        code(INSTALL),
        code(IMPORTS),
        md("""## Step 1. Load and explore"""),
        code("""# Load the Titanic dataset
df = sns.load_dataset("titanic")
print(f"Shape: {df.shape}")
df.head()"""),
        code("""# Always check missing values and class balance before modelling
print("Missing values (top 5 columns):")
print(df.isnull().sum().sort_values(ascending=False).head())
print()
print("Class balance (0 = died, 1 = survived):")
print(df["survived"].value_counts(normalize=True).round(3))"""),
        md("""**Slight imbalance** (62% died, 38% survived). Stratified split is a good idea.

## Step 2. Clean and engineer features"""),
        code("""# Pick the columns we want
df = df[["survived", "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]].copy()

# Engineer new features
df["family_size"] = df["sibsp"] + df["parch"] + 1     # total family on board
df["is_alone"]    = (df["family_size"] == 1).astype(int)

# Fill missing values with sensible defaults
df["age"].fillna(df["age"].median(), inplace=True)
df["embarked"].fillna(df["embarked"].mode()[0], inplace=True)

# Convert categoricals to numbers (one-hot encoding)
df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=True)

print(f"Shape after cleaning: {df.shape}")
df.head()"""),
        md("""## Step 3. Split into train and test"""),
        code("""from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Separate features (X) from target (y)
X = df.drop(columns=["survived"])
y = df["survived"]

# Use stratify to keep the survival rate the same in train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y,
)
print(f"Training: {X_train.shape}")
print(f"Test:     {X_test.shape}")"""),
        md("""## Step 4. Compare 5 models with 5-fold cross-validation

We'll try Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, and KNN."""),
        code("""from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

# Each model wrapped in a Pipeline (scaler + model) - prevents leakage
models = {
    "Logistic Regression":  LogisticRegression(max_iter=1000),
    "Decision Tree":        DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest":        RandomForestClassifier(n_estimators=300, random_state=42),
    "Gradient Boosting":    GradientBoostingClassifier(random_state=42),
    "KNN":                  KNeighborsClassifier(n_neighbors=7),
}

# Cross-validate each
print(f"{'Model':25s} {'CV Accuracy (mean +/- std)':30s}")
print("-" * 60)
for name, m in models.items():
    pipe = Pipeline([("scaler", StandardScaler()), ("model", m)])
    s = cross_val_score(pipe, X_train, y_train, cv=5, scoring="accuracy")
    print(f"{name:25s} {s.mean():.3f} +/- {s.std():.3f}")"""),
        md("""**Gradient Boosting and Random Forest typically lead.** Let's tune Gradient Boosting in the next step.

## Step 5. Tune Gradient Boosting with GridSearchCV"""),
        code("""# Pipeline with the best-looking model from above
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  GradientBoostingClassifier(random_state=42)),
])

# Grid of hyperparameters to try
# Total: 3 x 3 x 3 = 27 combinations, each tested with 5-fold CV = 135 fits
param_grid = {
    "model__n_estimators":  [100, 200, 300],
    "model__learning_rate": [0.05, 0.1, 0.2],
    "model__max_depth":     [2, 3, 4],
}

# Run the search (use n_jobs=-1 to parallelize across CPU cores)
grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)

print("Best hyperparameters:", grid.best_params_)
print(f"Best CV accuracy:     {grid.best_score_:.3f}")"""),
        md("""## Step 6. Final test set evaluation

This is the moment of truth. We have not touched the test set yet."""),
        code("""from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, roc_auc_score,
)

# Use the best tuned model
best = grid.best_estimator_

# Predict on the held-out test set
y_pred  = best.predict(X_test)
y_proba = best.predict_proba(X_test)[:, 1]

# Multiple metrics give a complete picture
print(f"Test accuracy:  {accuracy_score(y_test, y_pred):.3f}")
print(f"Test ROC-AUC:   {roc_auc_score(y_test, y_proba):.3f}")
print()
print(classification_report(y_test, y_pred, target_names=["Died", "Survived"]))"""),
        code("""# Confusion matrix shows what kind of mistakes the model makes
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Greys",
            xticklabels=["Died", "Survived"],
            yticklabels=["Died", "Survived"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Final Test Set Confusion Matrix")
plt.show()"""),
        md("""## Step 7. Feature Importance

Understand WHY the model makes its predictions."""),
        code("""# Get the trained Gradient Boosting model from inside the pipeline
model = best.named_steps["model"]

# Plot importance (sums to 1.0)
imp = pd.Series(model.feature_importances_, index=X.columns).sort_values()
plt.figure(figsize=(8, 5))
imp.plot.barh(color="gray")
plt.title("Feature Importance - Gradient Boosting")
plt.xlabel("Importance")
plt.show()"""),
        md("""**You'll typically see:** `sex_male`, `fare`, `age`, and `pclass` at the top. Historically: women, the wealthy, and children had higher survival rates.

## Step 8. Inspect individual predictions

Always sanity-check by looking at actual predictions vs reality."""),
        code("""# Take 10 test samples
sample = X_test.head(10).copy()
sample["actual"]    = y_test.head(10).values
sample["predicted"] = best.predict(sample.drop(columns=["actual"]))
sample["prob_survived"] = best.predict_proba(
    sample.drop(columns=["actual", "predicted"])
)[:, 1].round(3)

# Show actual vs predicted
sample[["actual", "predicted", "prob_survived"]]"""),
        md("""## Step 9. Save the model for later use"""),
        code("""# Save the entire pipeline (scaler + model) to disk
import joblib

joblib.dump(best, "titanic_model.pkl")
print("Saved to titanic_model.pkl")

# Loading it later:
# loaded = joblib.load("titanic_model.pkl")
# loaded.predict(new_data)"""),
        md("""## Step 10. Where to go next

You just built a complete ML system from scratch! To level up:

1. **Try XGBoost or LightGBM** instead of GradientBoostingClassifier - usually faster and a bit more accurate.

2. **Engineer the `Title` feature** (Mr/Mrs/Miss/Master/Dr) from the original Kaggle Titanic CSV. It's often a top predictor.

3. **Try a different problem:**
   - **House Prices** (Kaggle) - regression
   - **IMDB sentiment** - text classification
   - **MNIST digits** - image classification

4. **Deploy** the model: wrap it in a Flask or FastAPI endpoint.

5. **Build a Streamlit dashboard** that takes user inputs and returns predictions.

Congratulations on completing the notebook series! You now know:
- Linear regression, logistic regression, regularization
- Decision trees, random forests, gradient boosting
- Distance metrics, K-Means, hierarchical clustering, KNN
- The complete ML workflow from data to deployment

Go build something cool. 🚢"""),
    ]
    save("11_end_to_end_titanic.ipynb", cells)


def main():
    print("Building richly-commented notebooks in:", OUT)
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
    print("Done. All notebooks rebuilt with detailed explanations.")


if __name__ == "__main__":
    main()
