---
title: "16. K-Nearest Neighbours"
category: Machine Learning
order: 16
tags:
  - machine-learning
  - knn
  - classification
  - regression
  - lazy-learning
summary: A complete beginner friendly guide to K-Nearest Neighbours (KNN). We cover how it works, weighted aggregation, picking K, key practical considerations, and a full Python demonstration for both classification and regression.
---

# K-Nearest Neighbours

## The simplest machine learning algorithm

K-Nearest Neighbours, almost always written **KNN**, is sometimes called "the simplest machine learning algorithm". And in some sense it really is. There is no fancy training, no gradient descent, no math beyond computing distances.

The idea is so simple a child could explain it.

> To predict something about a new data point, look at the K points in your training data that are most similar to it, and use their answers to vote.

That is the entire algorithm. But this simple idea is surprisingly powerful, and KNN is still used in real production systems today.

This tutorial covers:

1. The intuition behind KNN.
2. How KNN works step by step.
3. Weighted aggregation (giving closer neighbours more say).
4. Key considerations, especially picking K.
5. A full Python demonstration for both classification and regression.

Let us get started.

---

## The intuition

Imagine you are at a party where everyone is wearing a different colored shirt depending on what music they like. Suddenly someone new walks in, and you want to guess what music they like.

A reasonable approach is to look at the 5 people standing nearest to them and ask what music those 5 prefer. If 4 of them like jazz and 1 likes pop, your best guess is that the new person also likes jazz.

That is KNN.

The "K" is the number of neighbours you look at. The "nearest" means closest in some measure of similarity. The output is a vote among those K neighbours (for classification) or an average of their values (for regression).

### KNN is a lazy learner

Most ML algorithms train a model first, then use it to predict. KNN is the opposite. There is no real training. The "model" is just the training data itself. All the work happens at prediction time.

This is sometimes called **lazy learning** or **instance-based learning**.

That sounds silly, but it has real consequences.

* **Training is instant.** You just store the data.
* **Predicting is slow.** Every prediction requires comparing the new point against every training point.
* **The model uses lots of memory.** You have to keep the whole training set around.

For small datasets this is no problem. For huge datasets it can be a deal-breaker, though there are clever data structures (KD trees, ball trees) that speed it up.

---

## The KNN algorithm step by step

KNN works for both classification and regression. The only difference is how you aggregate the neighbours' answers at the end.

### KNN for classification

**Step 1.** Pick a value of K. Common choices are 3, 5, 7, 9.

**Step 2.** When a new data point arrives, compute its distance to every point in the training set.

**Step 3.** Sort the distances and pick the K smallest. These are the K nearest neighbours.

**Step 4.** Look at the labels of those K neighbours and take a majority vote. That is your prediction.

### KNN for regression

The first three steps are exactly the same. Step 4 changes.

**Step 4.** Look at the values of the K neighbours and take their average (or weighted average). That is your prediction.

That is it. Simple and clear.

### A small worked example

Suppose you want to classify a new fruit as either apple or orange based on weight and color score. Your training set has 6 fruits.

| Fruit | Weight | Color | Label |
|---|---|---|---|
| 1 | 150 | 0.9 | Apple |
| 2 | 130 | 0.85 | Apple |
| 3 | 170 | 0.6 | Orange |
| 4 | 180 | 0.55 | Orange |
| 5 | 160 | 0.8 | Apple |
| 6 | 175 | 0.5 | Orange |

A new fruit arrives with weight 165 and color 0.7.

Compute Euclidean distance from the new fruit to each:

* d(new, 1) = sqrt((165-150)^2 + (0.7-0.9)^2) = sqrt(225 + 0.04) ≈ 15.0
* d(new, 2) = sqrt(35^2 + (-0.15)^2) ≈ 35.0
* d(new, 3) = sqrt(5^2 + 0.1^2) ≈ 5.0
* d(new, 4) = sqrt(15^2 + 0.15^2) ≈ 15.0
* d(new, 5) = sqrt(5^2 + (-0.1)^2) ≈ 5.0
* d(new, 6) = sqrt(10^2 + 0.2^2) ≈ 10.0

With K = 3, the 3 nearest are fruits 3 (Orange), 5 (Apple), and 6 (Orange). Vote: 2 Orange, 1 Apple. **Prediction: Orange.**

Notice something important. Weight differences (in the tens) dwarfed color differences (in the tenths). That made color basically irrelevant in the distance calculation. This is why **you must always scale your features** before using KNN, just like with K-Means.

---

## Weighted aggregation

In the basic version of KNN, every one of the K neighbours gets one equal vote. But that is not always fair.

Suppose K = 5 and your new point has neighbours at distances 0.1, 0.2, 0.3, 1.5, and 1.6. The first three are right next to your point. The last two are far away. Should the far ones really get the same say as the close ones?

The answer is usually no. So we use **weighted KNN**.

The idea is to give closer neighbours more influence. A common weighting scheme is **inverse distance**:

```
weight of neighbour i = 1 / distance to neighbour i
```

For classification, you sum the weights for each class and pick the class with the highest total weight.

For regression, you compute a weighted average:

```
prediction = (sum over neighbours of weight_i * value_i) / (sum of weights)
```

Weighted KNN is almost always better than plain KNN. In scikit-learn you just set `weights="distance"`.

```python
KNeighborsClassifier(n_neighbors=5, weights="distance")
```

---

## Key considerations

KNN is simple but there are a few things you have to get right.

### Picking K

K is the most important hyperparameter.

* **K = 1.** Each prediction is whatever the single nearest neighbour says. Very flexible, very noisy, prone to overfitting.
* **K too large.** Your prediction becomes the majority class across a large chunk of the data, losing local detail.

Common values are 3, 5, 7, 9, 11. Usually an **odd number** for classification (to avoid ties). The right K depends on your data. Use cross validation to find the best one.

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

for k in [1, 3, 5, 7, 9, 11, 15, 21]:
    knn = KNeighborsClassifier(n_neighbors=k, weights="distance")
    scores = cross_val_score(knn, X_train_scaled, y_train, cv=5, scoring="accuracy")
    print(f"K = {k}, CV accuracy = {scores.mean():.3f}")
```

### Always scale your features

KNN uses distances. Without scaling, large-valued features dominate. Always use StandardScaler (or MinMaxScaler) on your features before fitting KNN.

### The curse of dimensionality

In high dimensions, distances become meaningless. Every pair of points ends up roughly the same distance apart. KNN works best on a modest number of well-chosen features (say, fewer than 20).

If you have many features, do feature selection or dimensionality reduction (like PCA) first.

### Imbalanced classes

If 95% of your training data is class A, then KNN will lean heavily toward A no matter what. Use stratified sampling, class weights, or balance your data before training.

### Choice of distance metric

KNN does not have to use Euclidean distance. It can use any of the metrics we learned in the previous tutorial: Manhattan, cosine, etc. Try them and see which works best on your data.

```python
KNeighborsClassifier(n_neighbors=5, metric="manhattan")
KNeighborsClassifier(n_neighbors=5, metric="cosine")
```

---

## Full Python demonstration

Let us see KNN in action on a classification problem.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Step 1. Load the data
data = load_iris()
X = data.data
y = data.target

# Step 2. Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Step 3. Scale the features (critical!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 4. Find the best K using grid search
param_grid = {
    "n_neighbors": [1, 3, 5, 7, 9, 11, 15],
    "weights": ["uniform", "distance"],
    "metric": ["euclidean", "manhattan"],
}
grid = GridSearchCV(
    KNeighborsClassifier(),
    param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
)
grid.fit(X_train_scaled, y_train)
print("Best parameters:", grid.best_params_)
print("Best CV score:", grid.best_score_)

# Step 5. Evaluate on the test set
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test_scaled)
print("\nTest accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification report:")
print(classification_report(y_test, y_pred, target_names=data.target_names))
```

What is happening here:

* We load the famous Iris dataset (3 flower species, 4 features).
* We split into 70% train and 30% test, stratified by class.
* We scale the features with StandardScaler.
* We do a grid search over different values of K, weighting schemes, and distance metrics.
* We evaluate the best model on the held-out test set.

You will typically get accuracy above 95% on this dataset with the right K. KNN is surprisingly effective.

### KNN for regression

The same workflow works for regression. Just swap the model:

```python
from sklearn.neighbors import KNeighborsRegressor

reg = KNeighborsRegressor(n_neighbors=5, weights="distance")
reg.fit(X_train_scaled, y_train)
predictions = reg.predict(X_test_scaled)
```

For each new point, the prediction is a weighted average of the K nearest training targets.

---

## When should you use KNN

KNN is a great choice when:

* Your dataset is small to medium (say, less than 100,000 rows).
* You have a modest number of features (say, less than 20).
* Your data is well-scaled or can be scaled.
* You want a quick, simple baseline before trying more complex models.
* Local patterns matter more than global ones.

KNN is a poor choice when:

* You have millions of rows (prediction becomes too slow).
* You have hundreds of features (curse of dimensionality).
* You need a model that handles missing values gracefully (KNN does not).
* You need a model that gives you interpretable feature importances (KNN does not).

For tabular classification problems, KNN with proper scaling and tuned K often performs surprisingly close to more sophisticated models like Random Forests. It is always worth trying as a baseline.

---

## Quick summary

KNN is the algorithm that does no real training but predicts by voting among the K most similar examples.

Five things to remember.

1. KNN looks up the K nearest neighbours of a new point and uses their labels to vote (classification) or their values to average (regression).
2. Weighted KNN gives closer neighbours more say. Use `weights="distance"`.
3. Always scale your features.
4. Pick K with cross validation. Odd numbers are safer for classification.
5. KNN struggles with very large datasets and very high dimensional data.

KNN is the perfect bookend to this section on unsupervised and distance-based methods. The same distance metrics we learned about earlier power both clustering and KNN. The difference is that clustering uses distances to **find groups** in unlabelled data, while KNN uses distances to **make predictions** on labelled data.

Together with everything from the earlier tutorials, you now have a solid foundation in classical machine learning. Linear models, regularisation, decision trees, ensembles, clustering, and nearest neighbours. That is most of the toolkit you need for any tabular dataset.

Good luck applying these ideas to real problems.
