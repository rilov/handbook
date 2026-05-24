---
title: "22. ML Algorithm Intuition Flashcards"
category: Machine Learning
order: 22
tags:
  - machine-learning
  - flashcards
  - intuition
  - review
  - quick-reference
summary: One flashcard per algorithm. The core idea, an everyday analogy, when to use it, and a tiny code snippet. Perfect for review, revision, or refreshing your memory right before an interview.
---

# ML Algorithm Intuition Flashcards

Each card is the smallest unit you need to remember about an algorithm. Read top to bottom for a quick refresher of the entire classical ML toolkit.

---

## Linear Regression

> **Core idea.** Fit the best straight line through your data to predict a continuous number.
>
> **Analogy.** Drawing a single line through a scatter plot of house sizes and prices.
>
> **Use when.** You want to predict a number, the relationship looks roughly linear, you want a quick interpretable baseline.
>
> **Watch out for.** Outliers and multicollinearity. Always scale features if you regularize.

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X_train, y_train)
```

---

## Logistic Regression

> **Core idea.** Pass a linear combination through a sigmoid to get a probability between 0 and 1, then threshold for yes/no.
>
> **Analogy.** A smooth dimmer switch from "definitely no" to "definitely yes" instead of a hard light switch.
>
> **Use when.** You want yes/no predictions with probability scores, you need interpretable coefficients, you have a clean baseline problem.
>
> **Watch out for.** Imbalanced classes. Sigmoid saturates for extreme inputs. Tune `C` for regularization strength.

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(C=1.0).fit(X_train, y_train)
```

---

## Ridge Regression (L2)

> **Core idea.** Linear regression with an L2 penalty that shrinks all coefficients gently toward zero.
>
> **Analogy.** A teacher saying "be reasonable, do not bet everything on one student" so every feature gets a smaller voice.
>
> **Use when.** You have many features and want a smoother, more stable model. Especially good with multicollinearity.
>
> **Watch out for.** Does not zero out any coefficients (still keeps every feature).

```python
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0).fit(X_train, y_train)
```

---

## Lasso Regression (L1)

> **Core idea.** Linear regression with an L1 penalty that drives weak coefficients exactly to zero.
>
> **Analogy.** A strict editor cutting every unnecessary word until only the important ones remain.
>
> **Use when.** You have many features and want automatic feature selection. Useful when you suspect most features are useless.
>
> **Watch out for.** With highly correlated features, Lasso picks one almost at random.

```python
from sklearn.linear_model import Lasso
model = Lasso(alpha=0.1).fit(X_train, y_train)
```

---

## Elastic Net

> **Core idea.** Combine Ridge and Lasso. Penalty is a weighted mix of L1 and L2.
>
> **Analogy.** A compromise that gets the best of both worlds.
>
> **Use when.** You have many features, some correlated, and want both selection (L1) and stability (L2).
>
> **Watch out for.** Two hyperparameters to tune (`alpha` and `l1_ratio`).

```python
from sklearn.linear_model import ElasticNet
model = ElasticNet(alpha=0.1, l1_ratio=0.5).fit(X_train, y_train)
```

---

## Decision Tree

> **Core idea.** Repeatedly split the data with yes/no questions to maximize purity at each step.
>
> **Analogy.** A flowchart that asks the most useful question first, then drills down.
>
> **Use when.** You need a model someone can read and explain. Handles nonlinear patterns and feature interactions naturally.
>
> **Watch out for.** Overfits very easily. Always limit `max_depth` or `min_samples_leaf`.

```python
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth=5).fit(X_train, y_train)
```

---

## Random Forest

> **Core idea.** Train many decision trees on random data subsets and random feature subsets. Average or vote on predictions.
>
> **Analogy.** A committee of independent experts each looking at a slightly different angle of the problem.
>
> **Use when.** You want a strong reliable model with minimal tuning. Excellent baseline for most tabular problems.
>
> **Watch out for.** Slower to predict than linear models. Less interpretable. `n_estimators=100` is the safe default.

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=200, max_depth=10).fit(X_train, y_train)
```

---

## AdaBoost

> **Core idea.** Train weak learners sequentially. After each round, increase weight on the misclassified examples so the next learner focuses on them.
>
> **Analogy.** A tutor who reviews mistakes more carefully each pass.
>
> **Use when.** You want a boosting baseline. Works well on clean data with simple weak learners.
>
> **Watch out for.** Sensitive to noise and outliers because it keeps amplifying them.

```python
from sklearn.ensemble import AdaBoostClassifier
model = AdaBoostClassifier(n_estimators=100).fit(X_train, y_train)
```

---

## Gradient Boosting

> **Core idea.** Train trees sequentially. Each new tree predicts the residual errors left over from the ensemble so far.
>
> **Analogy.** A relay race where each runner picks up where the previous one left off.
>
> **Use when.** You want maximum accuracy on tabular data and have time to tune.
>
> **Watch out for.** Easily overfits with high `learning_rate` or too many trees. Tune `learning_rate` (small), `n_estimators` (large), and `max_depth` (small) together.

```python
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier(learning_rate=0.05, n_estimators=300, max_depth=3).fit(X_train, y_train)
```

---

## XGBoost

> **Core idea.** Highly optimized gradient boosting with built-in regularization. The competition winner for nearly a decade.
>
> **Analogy.** A gradient boosting machine with a turbocharger and seat belts.
>
> **Use when.** You want top-of-the-line accuracy on tabular data and you are willing to tune.
>
> **Watch out for.** Many hyperparameters. Start with defaults, then tune `learning_rate`, `max_depth`, `n_estimators`, and regularization.

```python
from xgboost import XGBClassifier
model = XGBClassifier(n_estimators=500, learning_rate=0.05, max_depth=5).fit(X_train, y_train)
```

---

## LightGBM

> **Core idea.** Like XGBoost but with a different tree-growing strategy (leaf-wise) that makes it faster on large datasets.
>
> **Analogy.** A leaner, more agile cousin of XGBoost.
>
> **Use when.** You have a lot of data (hundreds of thousands of rows) or many features.
>
> **Watch out for.** Can overfit on small datasets because of leaf-wise growth.

```python
from lightgbm import LGBMClassifier
model = LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=31).fit(X_train, y_train)
```

---

## CatBoost

> **Core idea.** Gradient boosting with native handling of categorical features. No need for manual encoding.
>
> **Analogy.** XGBoost that already knows how to handle text columns without you doing anything.
>
> **Use when.** You have many high-cardinality categorical features and want to skip the encoding step.
>
> **Watch out for.** Slower to predict than LightGBM. Worth using when you have lots of categoricals.

```python
from catboost import CatBoostClassifier
model = CatBoostClassifier(iterations=500, learning_rate=0.05, verbose=0).fit(X_train, y_train)
```

---

## K-Nearest Neighbours (KNN)

> **Core idea.** To predict a new point, look at the K nearest training points and vote (classification) or average (regression).
>
> **Analogy.** "Show me your friends and I'll tell you who you are."
>
> **Use when.** You have a small to medium dataset, low feature count, and want a simple baseline.
>
> **Watch out for.** Slow at predict time on large datasets. Useless in very high dimensions. Always scale features.

```python
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=5, weights="distance").fit(X_train, y_train)
```

---

## K-Means

> **Core idea.** Pick K random centroids. Assign each point to the nearest one. Move each centroid to the mean of its assigned points. Repeat until stable.
>
> **Analogy.** Sorting laundry into K piles, then adjusting the piles each time something new arrives.
>
> **Use when.** You want fast clustering of large data into roughly round groups.
>
> **Watch out for.** Picks K upfront. Assumes spherical clusters of similar size. Always scale. Always set `n_init=10` for stability.

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X_scaled)
labels = km.labels_
```

---

## Hierarchical Clustering

> **Core idea.** Start with every point as its own cluster. Repeatedly merge the two closest clusters until only one remains.
>
> **Analogy.** Building a family tree from the bottom up.
>
> **Use when.** You want to visualise structure, do not know K in advance, or expect nested groups.
>
> **Watch out for.** Slow on large data (O(n²) memory). Once two points merge they cannot separate again.

```python
from sklearn.cluster import AgglomerativeClustering
model = AgglomerativeClustering(n_clusters=4, linkage="ward").fit_predict(X_scaled)
```

---

## DBSCAN

> **Core idea.** Find dense regions of points and grow clusters from them. Points in low density become noise.
>
> **Analogy.** A flashlight in a dark room: anywhere with a lot of objects clustered together becomes a group, lone objects become outliers.
>
> **Use when.** Clusters have weird shapes, you want automatic outlier detection, you do not want to pick K.
>
> **Watch out for.** Two hyperparameters (`eps`, `min_samples`) that are sensitive. Struggles with clusters of varying density.

```python
from sklearn.cluster import DBSCAN
labels = DBSCAN(eps=0.5, min_samples=5).fit_predict(X_scaled)
```

---

## Quick recall: pick a model in 5 seconds

Just need a fast cue?

| You want to... | Reach for |
|---|---|
| Predict a number, quick baseline | **Linear Regression** |
| Predict yes/no, quick baseline | **Logistic Regression** |
| Stop overfitting in a linear model | **Ridge** (gentle) or **Lasso** (drops features) |
| Explain a decision flowchart | **Decision Tree** |
| Solid model, low tuning | **Random Forest** |
| Maximum accuracy, willing to tune | **XGBoost** or **LightGBM** |
| Lazy similarity-based prediction | **KNN** |
| Quick clustering of round groups | **K-Means** |
| See full clustering structure | **Hierarchical Clustering** |
| Find arbitrary-shape clusters + outliers | **DBSCAN** |

---

## How to use these flashcards

Cover the explanation, look at the algorithm name, and try to recite:

1. The core idea in one sentence.
2. The everyday analogy.
3. When to use it.
4. One thing to watch out for.

If you can do all four for every card, you have internalized the entire classical ML toolkit. That is genuinely impressive and almost everything you need for any tabular problem.
