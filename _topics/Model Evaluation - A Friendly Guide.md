---
title: "Model Evaluation - A Friendly Guide"
category: Model Evaluation
order: 0
permalink: /topics/model-evaluation/
tags:
  - machine-learning
  - model-evaluation
  - cross-validation
  - overfitting
  - metrics
summary: "A friendly guide to evaluating machine learning models: train-test split, validation sets, cross-validation, metrics, and how to avoid common traps."
date: 2026-08-16
---

# Model Evaluation - A Friendly Guide

The fanciest model in the world is useless if it cannot make good predictions on data it has not seen yet. **Model evaluation** is the set of tools we use to answer one question: *how will this model actually perform in the real world?*

This guide covers the practical ideas behind splitting data, choosing the right metric, and comparing models fairly. It assumes you already know the basics of machine learning; if you want a deeper look at the bias-variance tradeoff, see the [Bias and Variance]({{ site.baseurl }}/topics/bias-and-variance) topic first.

---

## 1. The whole point: generalisation

A model's job is to learn a pattern that also works on **new** data.

- **Training error:** how well the model does on the data it learned from.
- **Test error:** how well the model does on data it has never seen.
- A model with low training error but high test error has **overfitted**.
- A model with high training error and high test error has **underfitted**.

The only score that really matters is the score on data the model has not seen.

---

## 2. The train-test split

The simplest way to estimate real-world performance is to hide some data before training.

```
100% of data
│
├── training set  (e.g. 80%)  → used to train the model
└── test set      (e.g. 20%)  → used only at the very end
```

A common split is **80% train / 20% test**. For imbalanced classes, use **stratification** so the test set has the same class proportions as the full set.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("Test accuracy:", accuracy_score(y_test, predictions))
```

The test set should be touched **once**. If you keep tuning the model to improve the test score, the test set becomes just another training set.

---

## 3. The validation set

A **validation set** is a second held-out split used to make decisions *during* the project:

- picking between different models,
- choosing hyperparameters,
- deciding when to stop training.

```
100% of data
│
├── training set      (e.g. 70%)
├── validation set    (e.g. 15%)  → used to compare options
└── test set          (e.g. 15%)  → used only for final score
```

The rule is simple: **train on the training set, tune on the validation set, report on the test set**.

---

## 4. Cross-validation

When the dataset is small, a single train-test split can be unlucky: the test fold might happen to contain only easy or only hard examples. **Cross-validation** trains and tests the model multiple times on different slices of the data, then averages the scores.

### k-fold cross-validation

```
Fold 1:  [Test][Train][Train][Train][Train]
Fold 2:  [Train][Test][Train][Train][Train]
Fold 3:  [Train][Train][Test][Train][Train]
Fold 4:  [Train][Train][Train][Test][Train]
Fold 5:  [Train][Train][Train][Train][Test]
```

The data is split into `k` equal chunks. The model is trained `k` times, each time holding out one chunk as the test set. The final score is the average of all `k` scores.

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(LogisticRegression(max_iter=200), X, y, cv=5)
print("Cross-validation scores:", scores)
print("Average:", scores.mean())
```

**Common choices:** `k=5` or `k=10`. Use `k=5` for speed, `k=10` for small datasets. Leave-one-out cross-validation (`k` equals the number of samples) is the most thorough but the slowest.

---

## 5. Classification metrics

**Accuracy** is the simplest classification metric:

```
accuracy = correct predictions / total predictions
```

It is easy to understand, but it can be misleading when the classes are imbalanced. If 99% of emails are not spam, a model that always says "not spam" gets 99% accuracy.

For imbalanced problems, use **precision**, **recall**, and the **F1-score**.

- **Precision:** of all the positives the model predicted, how many were actually positive?
- **Recall:** of all the actual positives, how many did the model find?

```
precision = true positives / (true positives + false positives)
recall    = true positives / (true positives + false negatives)
```

The **F1-score** is the balanced average of precision and recall:

```
F1 = 2 * (precision * recall) / (precision + recall)
```

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

predictions = model.predict(X_test)
print("accuracy:", accuracy_score(y_test, predictions))
print("precision:", precision_score(y_test, predictions, average="macro"))
print("recall:", recall_score(y_test, predictions, average="macro"))
print("F1:", f1_score(y_test, predictions, average="macro"))
```

A **confusion matrix** shows exactly which classes get confused with which. It is the most honest view of a classifier's mistakes.

---

## 6. Regression metrics

For numerical predictions, the most common metrics are:

- **MSE (Mean Squared Error):** the average of the squared errors. It punishes large mistakes heavily.

```
MSE = average of (actual - predicted)^2
```

- **RMSE (Root Mean Squared Error):** the square root of MSE. It has the same units as the target, so it is easier to interpret.

```
RMSE = sqrt(MSE)
```

- **MAE (Mean Absolute Error):** the average of the absolute errors. It treats all mistakes equally.

```
MAE = average of |actual - predicted|
```

- **R^2 (coefficient of determination):** how much of the variance in the target is explained by the model. 1.0 is a perfect fit; negative values mean the model is worse than predicting the mean.

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

# replace y_test and predictions with regression values
# print("RMSE:", np.sqrt(mean_squared_error(y_test, predictions)))
# print("MAE:", mean_absolute_error(y_test, predictions))
# print("R^2:", r2_score(y_test, predictions))
```

---

## 7. Hyperparameter search

**Hyperparameters** are the settings you choose before training, such as `C` for an SVM, `k` for KNN, or `max_depth` for a decision tree. They are not learned from the data, so we have to try different values and see what works best.

Two simple strategies are:

- **Grid search:** try every combination from a fixed list. Exhaustive, but slow.
- **Random search:** try random combinations. Often faster and almost as good.

In both cases, use a **validation set** or **cross-validation** to score each combination. Never pick hyperparameters by looking at the final test score.

```python
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

param_grid = {
    "C": [0.1, 1, 10],
    "gamma": ["scale", 0.01, 0.001],
    "kernel": ["rbf", "linear"]
}

search = GridSearchCV(SVC(), param_grid, cv=5)
search.fit(X_train, y_train)
print("Best params:", search.best_params_)
print("Best CV score:", search.best_score_)
```

---

## 8. The most common traps

- **Data leakage:** any information from the test set reaches the training process. Always split before scaling, feature engineering, or any transformation.
- **Optimising for the wrong metric:** accuracy is not enough for imbalanced data; mean accuracy is not enough if some mistakes are more expensive than others.
- **Overfitting the test set:** if you tune, re-tune, and re-tune again using the test score, your final score is no longer an honest estimate.
- **Ignoring the validation set:** the test set is for the final report. The validation set is for all decisions before that.

---

## 9. Summary: which tool for which job?

| Situation | Use this |
|---|---|
| Lots of data and one model to check | Train-test split |
| Small dataset or comparing models | k-fold cross-validation |
| Choosing hyperparameters or models | Validation set or cross-validation |
| Imbalanced classes | Precision, recall, F1 |
| Numerical predictions | RMSE, MAE, R^2 |
| Final report on unseen data | Test set (used once) |

---

## 10. One-sentence takeaway

**Treat the test set like an exam paper you only get to see once:** use the training and validation sets to practise, and only measure real performance on the final test set.
