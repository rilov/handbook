---
title: "27. ML Quick Reference - Libraries, Metrics and Cheat Sheet"
category: Machine Learning
order: 27
tags:
  - machine-learning
  - cheat-sheet
  - reference
  - libraries
  - metrics
  - rmse
  - r2
  - precision
  - recall
  - f1
  - roc-auc
summary: A single-page quick reference for every ML topic in this handbook. Libraries to import, classes to use, key hyperparameters, evaluation metrics with formulas, and a master cheat sheet for picking the right tool and the right metric.
---

# ML Quick Reference - Libraries, Metrics and Cheat Sheet

A single page you can come back to whenever you need to remember which library, which class, or which metric to use. Everything here is covered in detail in the earlier tutorials. This page is the pocket reference.

---

## Core Libraries

The handful of libraries that show up in every ML project.

| Library | What it does | Typical import |
|---|---|---|
| **NumPy** | Fast arrays and math | `import numpy as np` |
| **Pandas** | Tables (DataFrames) | `import pandas as pd` |
| **scikit-learn** | The classical ML toolkit | `from sklearn... import ...` |
| **Matplotlib** | Plotting basics | `import matplotlib.pyplot as plt` |
| **Seaborn** | Prettier statistical plots | `import seaborn as sns` |
| **SciPy** | Stats, linkage for hierarchical clustering | `from scipy.cluster.hierarchy import linkage, dendrogram` |
| **XGBoost** | Gradient boosting champion | `from xgboost import XGBClassifier, XGBRegressor` |
| **LightGBM** | Fast gradient boosting | `from lightgbm import LGBMClassifier, LGBMRegressor` |
| **CatBoost** | Boosting with categorical support | `from catboost import CatBoostClassifier, CatBoostRegressor` |
| **statsmodels** | Statistical inference (p-values, VIF) | `import statsmodels.api as sm` |

Install command for the whole stack:

```bash
pip install numpy pandas scikit-learn matplotlib seaborn scipy xgboost lightgbm catboost statsmodels
```

---

## Algorithms - which class to import

Every model in this handbook, with its scikit-learn (or other) import.

### Regression (predict a number)

| Algorithm | What it does | Import | Class |
|---|---|---|---|
| Linear Regression | Fits the best straight line through your data | `from sklearn.linear_model import LinearRegression` | `LinearRegression()` |
| Ridge Regression | Linear regression + L2 penalty to shrink all coefficients gently and stop overfitting | `from sklearn.linear_model import Ridge` | `Ridge(alpha=1.0)` |
| Lasso Regression | Linear regression + L1 penalty that drives weak coefficients to exactly zero (auto feature selection) | `from sklearn.linear_model import Lasso` | `Lasso(alpha=1.0)` |
| Elastic Net | Mix of Ridge and Lasso (both L1 and L2 penalties) | `from sklearn.linear_model import ElasticNet` | `ElasticNet(alpha=1.0, l1_ratio=0.5)` |
| Polynomial Features | Adds squared, cubed, and interaction features so linear models can fit curves | `from sklearn.preprocessing import PolynomialFeatures` | `PolynomialFeatures(degree=2)` |
| Decision Tree | Splits the data with yes/no questions to predict a number; interpretable but prone to overfit | `from sklearn.tree import DecisionTreeRegressor` | `DecisionTreeRegressor()` |
| Random Forest | Many decision trees trained on random data slices, average their predictions; strong + low tuning | `from sklearn.ensemble import RandomForestRegressor` | `RandomForestRegressor(n_estimators=100)` |
| Gradient Boosting | Trains trees sequentially, each fixing the previous ones' residual errors | `from sklearn.ensemble import GradientBoostingRegressor` | `GradientBoostingRegressor()` |
| XGBoost | Highly optimized gradient boosting, the competition champion | `from xgboost import XGBRegressor` | `XGBRegressor()` |
| LightGBM | Even faster gradient boosting, excels on very large datasets | `from lightgbm import LGBMRegressor` | `LGBMRegressor()` |
| KNN | Predicts by averaging the K most similar training points (no real training, slow at predict time) | `from sklearn.neighbors import KNeighborsRegressor` | `KNeighborsRegressor(n_neighbors=5)` |

### Classification (predict yes/no or a category)

| Algorithm | What it does | Import | Class |
|---|---|---|---|
| Logistic Regression | Predicts a probability between 0 and 1 using the sigmoid curve, then threshold for yes/no | `from sklearn.linear_model import LogisticRegression` | `LogisticRegression()` |
| Decision Tree | Yes/no question flowchart, each path ends in a class prediction; easy to read | `from sklearn.tree import DecisionTreeClassifier` | `DecisionTreeClassifier()` |
| Random Forest | Many trees vote on the answer; reliable baseline with little tuning | `from sklearn.ensemble import RandomForestClassifier` | `RandomForestClassifier(n_estimators=100)` |
| AdaBoost | Sequentially adds weak learners, each focusing on previously misclassified examples | `from sklearn.ensemble import AdaBoostClassifier` | `AdaBoostClassifier()` |
| Gradient Boosting | Sequential trees that fix the errors of previous trees; one of the strongest classical methods | `from sklearn.ensemble import GradientBoostingClassifier` | `GradientBoostingClassifier()` |
| XGBoost | Industry-standard boosting with regularization; usually the top performer on tabular data | `from xgboost import XGBClassifier` | `XGBClassifier()` |
| LightGBM | Faster boosting alternative; handles big datasets and categorical features well | `from lightgbm import LGBMClassifier` | `LGBMClassifier()` |
| KNN | Predicts the class by majority vote of the K closest training examples | `from sklearn.neighbors import KNeighborsClassifier` | `KNeighborsClassifier(n_neighbors=5)` |

### Clustering (find groups in unlabelled data)

| Algorithm | What it does | Import | Class |
|---|---|---|---|
| K-Means | Splits data into K round-shaped groups by iteratively assigning points to the nearest centroid | `from sklearn.cluster import KMeans` | `KMeans(n_clusters=K, n_init=10)` |
| Hierarchical (sklearn) | Builds a tree of merges from the bottom up; outputs flat clusters by cutting the tree | `from sklearn.cluster import AgglomerativeClustering` | `AgglomerativeClustering(n_clusters=K, linkage="ward")` |
| Hierarchical (scipy) | Same as above but returns the full linkage matrix you can plot as a dendrogram | `from scipy.cluster.hierarchy import linkage, dendrogram` | `linkage(X, method="ward")` |
| DBSCAN | Density-based clustering; finds arbitrary-shape clusters and labels outliers as noise | `from sklearn.cluster import DBSCAN` | `DBSCAN(eps=0.5, min_samples=5)` |

---

## Preprocessing - the tools you will use every time

| Task | What it does | Import | Class |
|---|---|---|---|
| Standard scaling | Centers each feature to mean 0 and scales to std 1; essential for distance-based and regularized models | `from sklearn.preprocessing import StandardScaler` | `StandardScaler()` |
| Min-max scaling | Squeezes each feature into the 0 to 1 range; useful for neural nets and image data | `from sklearn.preprocessing import MinMaxScaler` | `MinMaxScaler()` |
| One-hot encoding | Turns one categorical column into multiple 0/1 columns, one per category | `from sklearn.preprocessing import OneHotEncoder` | `OneHotEncoder(sparse_output=False)` |
| Ordinal encoding | Maps each category to an integer (use only when categories have natural order, e.g. low/med/high) | `from sklearn.preprocessing import OrdinalEncoder` | `OrdinalEncoder()` |
| Target encoding | Replaces each category with the mean target value of that category; powerful but risk of leakage | `from category_encoders import TargetEncoder` | `TargetEncoder()` |
| Train/test split | Randomly splits data into a training set and a held-out test set | `from sklearn.model_selection import train_test_split` | `train_test_split(X, y, test_size=0.2)` |
| Cross validation | Repeatedly trains and tests the model on K different folds for a robust performance estimate | `from sklearn.model_selection import cross_val_score` | `cross_val_score(model, X, y, cv=5)` |
| Grid search | Tries every combination of hyperparameters with cross validation and keeps the best | `from sklearn.model_selection import GridSearchCV` | `GridSearchCV(model, param_grid, cv=5)` |
| Pipeline | Chains preprocessing and modeling steps into one object so train/test stay leak-free | `from sklearn.pipeline import Pipeline` | `Pipeline([("scaler", StandardScaler()), ("model", LR())])` |

---

## Evaluation Metrics

### Regression metrics

For regression problems (predicting a number). All available in `sklearn.metrics`.

| Metric | Formula | What it tells you | Good if |
|---|---|---|---|
| **MAE** (Mean Absolute Error) | `mean(|y - y_pred|)` | Average size of error in original units | Easier to explain |
| **MSE** (Mean Squared Error) | `mean((y - y_pred)^2)` | Average squared error, penalizes big errors more | Internal optimization |
| **RMSE** (Root Mean Squared Error) | `sqrt(MSE)` | Like MAE but more sensitive to large errors. Same units as y | Most common reporting metric |
| **R²** (R-squared) | `1 - SS_res / SS_tot` | Fraction of variance explained. 0 to 1, higher better | Comparing models |
| **MAPE** (Mean Absolute % Error) | `mean(|y - y_pred| / |y|) * 100` | Percentage error. Easy to communicate | Forecasting |
| **Adjusted R²** | `1 - (1-R²)(n-1)/(n-p-1)` | R² penalized for extra features | Linear regression with many features |

```python
from sklearn.metrics import (
    mean_absolute_error,    # MAE
    mean_squared_error,     # MSE (and RMSE with squared=False)
    r2_score,
    mean_absolute_percentage_error,
)

mae  = mean_absolute_error(y_true, y_pred)
mse  = mean_squared_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)
r2   = r2_score(y_true, y_pred)
```

**Rule of thumb.** Report RMSE and R² together. RMSE tells you how big the typical error is. R² tells you how much of the variance you captured.

### Classification metrics

For classification problems (yes/no or a category).

#### The confusion matrix

Every classification metric is built from these four numbers.

|   | Predicted positive | Predicted negative |
|---|---|---|
| **Actual positive** | **TP** True Positive | **FN** False Negative |
| **Actual negative** | **FP** False Positive | **TN** True Negative |

#### Key metrics

| Metric | Formula | What it tells you | Good for |
|---|---|---|---|
| **Accuracy** | `(TP + TN) / total` | Overall correctness | Balanced classes |
| **Precision** | `TP / (TP + FP)` | When you predict yes, how often are you right? | When false positives are costly (spam, fraud) |
| **Recall** (sensitivity, TPR) | `TP / (TP + FN)` | Of all real positives, how many did you catch? | When false negatives are costly (medical, security) |
| **F1 Score** | `2 * P * R / (P + R)` | Harmonic mean of precision and recall | Imbalanced classes |
| **Specificity** (TNR) | `TN / (TN + FP)` | Of all real negatives, how many did you correctly reject? | Medical screening |
| **ROC-AUC** | Area under ROC curve | Probability the model ranks a positive above a negative | Best overall classifier score |
| **PR-AUC** | Area under Precision-Recall curve | Better than ROC-AUC for imbalanced data | Rare-event detection |
| **Log Loss** | `-mean(y log(p) + (1-y) log(1-p))` | Penalizes confident wrong predictions | Probability calibration |

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    log_loss,
    confusion_matrix,
    classification_report,
)

print(classification_report(y_true, y_pred))   # all in one
print(confusion_matrix(y_true, y_pred))
auc = roc_auc_score(y_true, y_pred_proba)      # NOTE: needs probabilities, not labels
```

**Rule of thumb.**

* **Balanced classes** → report **Accuracy** and **F1**.
* **Imbalanced classes** → ignore accuracy, report **Precision, Recall, F1, ROC-AUC, PR-AUC**.
* **Probabilities matter** → report **Log Loss** and **ROC-AUC**.

### Clustering metrics

There are no ground-truth labels in clustering, so we measure cluster quality differently.

| Metric | What it measures | Good if |
|---|---|---|
| **WCSS / Inertia** | Within-cluster sum of squared distances. K-Means objective. Lower is tighter | Elbow method to pick K |
| **Silhouette Score** | How well-separated clusters are. Range -1 to 1, higher is better | Compare different K values |
| **Davies-Bouldin Index** | Ratio of within-cluster to between-cluster distances. Lower is better | Compare clustering algorithms |
| **Calinski-Harabasz** | Ratio of between-cluster to within-cluster dispersion. Higher is better | Compare different K values |
| **Adjusted Rand Index** | If you have true labels, compares them to predicted clusters | Benchmark evaluation |

```python
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
    adjusted_rand_score,
)

sil = silhouette_score(X, labels)
db  = davies_bouldin_score(X, labels)
ch  = calinski_harabasz_score(X, labels)
```

---

## Distance and Similarity Metrics

The metrics behind clustering, KNN, and similarity search. All in `scipy.spatial.distance` or `sklearn.metrics.pairwise`.

| Metric | Use it for | scikit-learn / scipy |
|---|---|---|
| **Euclidean** | Continuous features, similar scales | `"euclidean"` |
| **Manhattan** | Robust to outliers, grid data | `"manhattan"` |
| **Minkowski** | Generalization of Euclidean/Manhattan | `"minkowski"` |
| **Chebyshev** | Chess king move, max coordinate diff | `"chebyshev"` |
| **Cosine** | High-dimensional sparse data, text | `"cosine"` |
| **Pearson** | Time series, signals moving together | `np.corrcoef(a, b)[0,1]` |
| **Jaccard** | Sets, market basket, document shingles | `"jaccard"` |
| **Hamming** | Binary vectors, strings of equal length | `"hamming"` |

---

## Choose the Right Metric for the Job

A condensed cheat sheet to point you to the right metric immediately.

| You are doing... | Use these metrics |
|---|---|
| Predicting house prices, demand, sales | **RMSE**, **MAE**, **R²** |
| Forecasting (time series) | **RMSE**, **MAPE** |
| Email spam, fraud detection (imbalanced classification) | **Precision**, **Recall**, **F1**, **PR-AUC** |
| Disease diagnosis | **Recall** (sensitivity), **Specificity**, **ROC-AUC** |
| Multi-class classification (balanced) | **Accuracy**, **F1 macro** |
| Ranking, recommendations | **ROC-AUC**, **NDCG**, **MAP@K** |
| K-Means clustering | **WCSS (elbow)**, **Silhouette** |
| Comparing clustering algorithms | **Silhouette**, **Davies-Bouldin** |
| Calibrated probability predictions | **Log Loss**, **Brier Score** |

---

## Choose the Right Algorithm for the Job

The condensed pick-an-algorithm cheat sheet.

| Your situation | Try this first |
|---|---|
| Quick baseline for any tabular problem | **Linear Regression** or **Logistic Regression** |
| Many features, overfitting | **Ridge** / **Lasso** / **Elastic Net** |
| Need interpretable rules | **Decision Tree** |
| Strong model with little tuning | **Random Forest** |
| Maximum accuracy on tabular data | **XGBoost** or **LightGBM** |
| Many categorical features | **CatBoost** |
| Quick lookup based on similar past examples | **KNN** |
| Find natural groups, fast, you know K | **K-Means** |
| See the full structure of your data | **Hierarchical Clustering** |
| Find outliers and weird shapes | **DBSCAN** |
| Compare items by direction not magnitude | **Cosine similarity** |
| Compare items by set overlap | **Jaccard** |

---

## Hyperparameters You Will Tune Most Often

The knobs that actually move the needle for each algorithm.

| Algorithm | Top hyperparameters | What they do |
|---|---|---|
| Linear / Logistic Regression | `C`, `penalty` | `C` is inverse of regularization strength (smaller C = stronger regularization). `penalty` picks L1 (Lasso), L2 (Ridge), or elasticnet |
| Ridge / Lasso | `alpha` | Regularization strength. Higher alpha = simpler model, less overfitting |
| Elastic Net | `alpha`, `l1_ratio` | `alpha` = strength. `l1_ratio` = mix between Lasso (1.0) and Ridge (0.0) |
| Decision Tree | `max_depth`, `min_samples_split`, `min_samples_leaf`, `criterion` | `max_depth` limits tree depth (smaller = simpler). `min_samples_*` set min samples for a split/leaf. `criterion` = gini or entropy |
| Random Forest | `n_estimators`, `max_depth`, `max_features`, `min_samples_leaf` | `n_estimators` = how many trees. `max_features` = features per split (sqrt is default). Others limit each tree's complexity |
| Gradient Boosting / XGBoost / LightGBM | `n_estimators`, `learning_rate`, `max_depth`, `subsample`, `colsample_bytree`, `reg_alpha`, `reg_lambda` | `learning_rate` is the step size (smaller = more careful). `subsample`/`colsample_bytree` use a random fraction per tree. `reg_*` add L1/L2 penalties |
| KNN | `n_neighbors`, `weights`, `metric` | `n_neighbors` = K. `weights` = uniform or distance (closer points count more). `metric` = euclidean, manhattan, cosine, etc. |
| K-Means | `n_clusters`, `init`, `n_init` | `n_clusters` = K. `init` = k-means++ (smart init) or random. `n_init` = how many random restarts to try |
| Hierarchical | `n_clusters`, `linkage` | `linkage` defines distance between clusters: ward (default, min variance), complete, average, or single |
| DBSCAN | `eps`, `min_samples` | `eps` = max distance to be considered a neighbour. `min_samples` = points needed to form a dense region |

### Generic tuning template

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    "n_estimators": [100, 200, 500],
    "max_depth":    [3, 5, 7, None],
}
grid = GridSearchCV(
    estimator=YourModel(),
    param_grid=param_grid,
    cv=5,
    scoring="roc_auc",     # or "f1", "accuracy", "neg_root_mean_squared_error"
    n_jobs=-1,
    verbose=1,
)
grid.fit(X_train, y_train)
print(grid.best_params_, grid.best_score_)
```

---

## A Reusable Workflow Template

Drop this into any new ML project. It covers the 90% case.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

# 1. Load
df = pd.read_csv("data.csv")
X = df.drop(columns=["target"])
y = df["target"]

# 2. Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Pipeline (scale + model)
from sklearn.ensemble import RandomForestClassifier
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model",  RandomForestClassifier(random_state=42)),
])

# 4. Tune
param_grid = {
    "model__n_estimators": [100, 300, 500],
    "model__max_depth":    [None, 5, 10],
}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring="roc_auc", n_jobs=-1)
grid.fit(X_train, y_train)

# 5. Evaluate on held-out test set
best_model = grid.best_estimator_
y_pred  = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]
print("Best params:", grid.best_params_)
print("Test ROC-AUC:", roc_auc_score(y_test, y_proba))
print(classification_report(y_test, y_pred))
```

For regression, swap `RandomForestClassifier` → `RandomForestRegressor`, `stratify=y` → `stratify=None`, and use `scoring="neg_root_mean_squared_error"`.

---

## Quick Symbol Reference

Notation that shows up in every ML tutorial.

| Symbol | Meaning |
|---|---|
| `X` | Feature matrix, shape (n_samples, n_features) |
| `y` | Target vector, shape (n_samples,) |
| `n` | Number of samples (rows) |
| `p` | Number of features (columns) |
| `K` | Number of clusters or neighbours |
| `y_pred` | Predicted values |
| `y_proba` | Predicted probabilities |
| `α` (alpha) | Regularization strength |
| `λ` (lambda) | Same as alpha in some notations |
| `θ` (theta) | Model parameters / weights |
| `β` (beta) | Coefficients in linear models |

---

## One Last Tip

If you forget everything else on this page, remember three things.

1. **Always scale your features** before using any distance-based algorithm (KNN, K-Means, SVM, regularized linear models).
2. **Never evaluate on training data.** The test score is the only score that matters.
3. **Start with the simplest model that could possibly work.** If a linear model already does well, you are probably done. Only reach for boosting and ensembles when you actually need the extra accuracy.

That is the entire classical ML toolkit in one page. Bookmark this and come back to it any time you forget which class to import or which metric to use.
