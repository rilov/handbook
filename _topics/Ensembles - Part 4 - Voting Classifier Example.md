---
title: "14. Ensembles - Part 4 - Voting Classifier Example"
category: Machine Learning
order: 14
permalink: /topics/ensembles-voting-classifier-example/
tags:
  - machine-learning
  - ensembles
  - voting-classifier
  - logistic-regression
  - random-forest
  - gradient-boosting
  - scikit-learn
summary: "A complete worked example of a soft-voting ensemble on the breast cancer dataset using Logistic Regression, Random Forest and Gradient Boosting."
date: 2026-08-30
---

# Ensembles - Part 4 - Voting Classifier Example

In the previous three parts we learned why ensembles work, how bagging and Random Forest combine many similar models, and how boosting teaches models one after another.

This part is a short, practical worked example. We build three very different classifiers and then let them **vote** on the final answer.

## The idea in one sentence

Instead of trusting one model, train a few strong but different models and let them vote. `VotingClassifier` in scikit-learn does exactly that.

## What the code does

We will use the `load_breast_cancer` dataset from scikit-learn. It is a binary classification problem: predict whether a tumour is malignant or benign.

The ensemble contains:

- **Logistic Regression** (scaled with a `StandardScaler` inside a pipeline)
- **Random Forest** (a bagging ensemble of trees)
- **Gradient Boosting** (a boosting ensemble of trees)

We train each model, print its individual accuracy, then combine them with **soft voting**. Soft voting means the ensemble averages the predicted probabilities of each class.

## Full code

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier

from sklearn.metrics import accuracy_score


# ------------------------------------------------
# 1. Load a real dataset
# ------------------------------------------------

data = load_breast_cancer()

X = data.data
y = data.target


# ------------------------------------------------
# 2. Split into training and testing data
# ------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ------------------------------------------------
# 3. Create multiple models
# ------------------------------------------------

logistic_model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)

random_forest_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

gradient_boost_model = GradientBoostingClassifier(
    random_state=42
)


# ------------------------------------------------
# 4. Train each model separately
# ------------------------------------------------

logistic_model.fit(X_train, y_train)
random_forest_model.fit(X_train, y_train)
gradient_boost_model.fit(X_train, y_train)


# ------------------------------------------------
# 5. Check individual model performance
# ------------------------------------------------

models = {
    "Logistic Regression": logistic_model,
    "Random Forest": random_forest_model,
    "Gradient Boosting": gradient_boost_model
}


for name, model in models.items():

    prediction = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        prediction
    )

    print(name, accuracy)


# ------------------------------------------------
# 6. Create the Ensemble
# ------------------------------------------------

ensemble_model = VotingClassifier(
    estimators=[
        ("logistic", logistic_model),
        ("random_forest", random_forest_model),
        ("gradient_boost", gradient_boost_model)
    ],

    voting="soft"
)


# ------------------------------------------------
# 7. Train the ensemble
# ------------------------------------------------

ensemble_model.fit(
    X_train,
    y_train
)


# ------------------------------------------------
# 8. Predict using ensemble
# ------------------------------------------------

ensemble_prediction = ensemble_model.predict(
    X_test
)


ensemble_accuracy = accuracy_score(
    y_test,
    ensemble_prediction
)


print(
    "Ensemble Accuracy:",
    ensemble_accuracy
)
```

## Key points to remember

- The models should be **different** from each other. If every model makes the same mistakes, voting cannot fix them.
- **Soft voting** needs every base model to predict probabilities. It usually beats hard voting because probabilities contain more information than class labels.
- A `Pipeline` or `make_pipeline` is a clean way to keep scaling and modelling in one object. This is why `StandardScaler` is inside the logistic pipeline.
- `VotingClassifier` behaves like any other scikit-learn estimator: `fit`, `predict`, `predict_proba`, and `score` all work as usual.

## Typical output

You will see the accuracy of each model followed by the ensemble accuracy. Often the ensemble is slightly better than any single model, especially if the three models make different types of errors.

## When to use a voting classifier

Use it when you have:

- a few strong models that are different from each other
- enough data that training time is not a problem
- a task where small accuracy gains matter, such as medical diagnosis

For larger datasets and competitions, methods like Random Forest, XGBoost or LightGBM are usually the next step after this basic ensemble.
