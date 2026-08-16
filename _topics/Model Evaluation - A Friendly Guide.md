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

### Why training accuracy is not enough

**Training accuracy** is how well the model does on the data it already saw. A model that simply memorises the training set can score 99% on training data and still fail on real-world data. Training score alone cannot tell you whether the model has learned a useful pattern or just memorised the answers.

- **Training error:** how well the model does on the data it learned from.
- **Validation error:** how well the model does on a held-out set used to tune and compare options.
- **Test error:** how well the model does on data it has never seen.

A model with low training error but high test error has **overfitted** — it memorised noise instead of the pattern. A model with high training error and high test error has **underfitted** — it is too simple to capture the pattern.

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

Think of the validation set as an early warning system. It gives the model a chance to prove itself on unseen data before the final test. If the validation score is much worse than the training score, the model is overfitting and you need to simplify it, collect more data, or add regularisation. Repeating this check stops you from accidentally optimising for the test set.

---

## 4. Cross-validation

There are two common ways to create a validation set:

- **Holdout validation:** split the data once into train and validation. Fast, but the score can be unlucky if the validation slice is small or unusual.
- **Cross-validation:** split the data into `k` folds and train/test `k` times, rotating which fold is the validation set. Slower, but uses more data for training and gives a more stable, less variable score.

For very large datasets (millions of rows), a holdout set is usually enough because the validation set is already large and representative. For smaller datasets, cross-validation is better because every data point gets used for both training and validation across different folds.

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

**Common choices:** `k=5` for speed, `k=10` for small datasets.

### Stratified k-fold

In normal k-fold, the folds are random. With imbalanced classes, one fold might accidentally contain only the majority class and give a misleading score. **Stratified k-fold** keeps the same class proportions in every fold. If 90% of the data is class A and 10% is class B, every fold also has that 90/10 split. This is the default choice for classification problems because it prevents a lucky or unlucky fold from fooling you.

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(LogisticRegression(max_iter=200), X, y, cv=skf)
```

### Leave-one-out cross-validation

**Leave-one-out (LOO)** is k-fold taken to the extreme: each fold is a single sample, so the model is trained on every sample except one and tested on that one. It uses almost all the data for training and gives a very unbiased estimate, but it is extremely slow on large datasets. Use it only for very small datasets where you cannot afford to hold out a bigger chunk.

### Time series cross-validation

For time-ordered data, you cannot shuffle the rows randomly because the future depends on the past. **Time series cross-validation** respects the order.

**Expanding window:** use the first T1, T2, T3 to predict T4; then T1..T4 to predict T5; then T1..T5 to predict T6. The training set grows over time.

```
Train: T1 T2 T3           → Test: T4
Train: T1 T2 T3 T4        → Test: T5
Train: T1 T2 T3 T4 T5     → Test: T6
```

**Rolling window:** use a fixed window that slides forward. For example, T1, T2, T3 to predict T4; then T2, T3, T4 to predict T5; then T3, T4, T5 to predict T6.

```
Train: T1 T2 T3   → Test: T4
Train: T2 T3 T4   → Test: T5
Train: T3 T4 T5   → Test: T6
```

Choose expanding window when you want to use all historical data; choose rolling window when you only care about the most recent window and want the training set size to stay constant.

### Benefits and costs

- **Benefit:** cross-validation gives a more reliable score because every data point gets to be in the validation set once, and the average is less sensitive to one unlucky split.
- **Cost:** it trains the model multiple times, so it can be slow on large datasets or complex models.
- **Rule of thumb:** use holdout for large data, k-fold for medium data, stratified k-fold for imbalanced classification, LOO for tiny data, and time-series splits for ordered data.

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

### Which mistakes are more expensive?

The right metric depends on what the model is used for. A high score on the wrong metric can still be a bad model.

- **Fraud detection:** a false negative (a real fraud marked as safe) is usually much more expensive than a false positive (a safe transaction marked as fraud). Maximise **recall** so you catch as much fraud as possible.
- **Credit scoring:** the goal is to maximise expected profit. The metric should reflect the financial gain or loss of each kind of decision, not just accuracy.
- **Medical screening:** a false negative (sick patient told they are healthy) can cost a life. Minimise false negatives even if it means more false positives, which lead to extra tests but not harm.

Always ask: *What does a wrong prediction cost in the real world?* Then pick the metric that matches that cost.

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
