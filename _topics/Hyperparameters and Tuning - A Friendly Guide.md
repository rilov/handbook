---
title: "Hyperparameters and Tuning - A Friendly Guide"
category: Model Evaluation
order: 1
permalink: /topics/hyperparameters-and-tuning/
tags:
  - machine-learning
  - hyperparameters
  - tuning
  - grid-search
  - random-search
summary: "A friendly guide to hyperparameters: what they are, how they differ from learned parameters, and how to tune them with grid search, random search, early stopping, and a careful eye on budget and leakage."
date: 2026-08-16
---

# Hyperparameters and Tuning - A Friendly Guide

Every machine learning model has two kinds of numbers:

- **Parameters:** the numbers the model learns from the data. In `y = w * x + b`, `w` and `b` are parameters.
- **Hyperparameters:** the settings you choose before training. They control *how* the model learns, not *what* it learns.

Picking the right hyperparameters can be the difference between a great model and a useless one. This guide explains what they are, how to search for them, and the common traps that make tuning go wrong.

---

## 1. Hyperparameters vs parameters

A **parameter** is something the training algorithm adjusts for you. A linear regression finds the best `w` and `b`. A neural network finds the best weights. You do not set these by hand.

A **hyperparameter** is something you set before the training begins. You tell the model how deep a tree can grow, how fast it should learn, or which optimisation algorithm to use. The model cannot learn these from the data.

```
Linear regression:  y = w * x + b
- Parameters: w, b           (learned)
- Hyperparameter: learning rate, regularisation strength
```

---

## 2. Examples of hyperparameters

Different models have different hyperparameters. Here are a few common ones:

| Model | Hyperparameters | What they control |
|---|---|---|
| **Decision tree** | `max_depth`, `min_samples_leaf` | How tall the tree can grow and when it stops splitting. |
| **Linear regression** | `learning_rate` | How big each update step is during training. |
| **Neural network** | `number_of_layers`, `neurons_per_layer`, `learning_rate`, `batch_size` | The size of the network and how fast it updates. |
| **Optimiser** | `SGD`, `Adam`, `RMSprop` | Which rule the model uses to update its weights. |
| **SVM** | `C`, `gamma`, `kernel` | The cost of mistakes and the shape of the decision boundary. |

Even non-parametric models such as KNN have hyperparameters (for example, the number of neighbours `k`).

---

## 3. Grid search

**Grid search** tries every combination from a fixed list you provide. If you give it three learning rates and two optimisers, it will train six models and pick the best one.

```
learning_rate: [0.001, 0.01, 0.1]
optimiser:     ["sgd", "adam"]

gives 3 × 2 = 6 combinations
```

It is exhaustive, so it is guaranteed to find the best combination inside the grid. The downside is that it can be very slow, especially when there are many hyperparameters or many values per hyperparameter.

```python
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

param_grid = {
    "C": [0.1, 1, 10],
    "gamma": [0.01, 0.001],
    "kernel": ["rbf", "linear"]
}

search = GridSearchCV(SVC(), param_grid, cv=5)
search.fit(X_train, y_train)
print("Best params:", search.best_params_)
print("Best CV score:", search.best_score_)
```

---

## 4. Random search

**Random search** does not try every combination. Instead, it samples random combinations from a range or distribution you define. It usually finds a good solution much faster than grid search.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform

param_distributions = {
    "C": loguniform(1e-2, 1e2),
    "gamma": loguniform(1e-4, 1e-1),
}

search = RandomizedSearchCV(
    SVC(),
    param_distributions,
    n_iter=20,
    cv=5,
    random_state=42
)
search.fit(X_train, y_train)
```

If one hyperparameter does not matter much, random search wastes very little time on it. This is why it often beats grid search in practice.

---

## 5. Search space, early stopping, and budget

### Search space

The **search space** is the set of hyperparameters and the ranges you consider. A huge search space can find better values, but it also means more trials. Keep the search space focused on values that make sense for your data and model.

### Early stopping

**Early stopping** stops training when the validation score stops improving. It is a cheap, effective way to prevent overfitting and save time. You do not have to wait for the full number of epochs if the model has already stopped getting better.

### Budget

In the real world, every trial costs money and time. A 1% accuracy gain might not be worth a week of extra compute. Decide up front how many trials or hours you are willing to spend. Good hyperparameter tuning means getting the best model you can within your budget, not chasing the absolute best score at any cost.

---

## 6. Common pitfalls

### Data leakage

The validation data must never influence the training data. Two classic mistakes:

- **Scaling before splitting:** if you fit the scaler on the whole dataset and then split, the validation set has already seen the training set's statistics. Always `fit` on the training set and `transform` the validation and test sets.
- **Tuning with the test set:** if you keep adjusting hyperparameters to improve the test score, the test score is no longer an honest measure.

### Target leakage

**Target leakage** happens when a feature would not actually be available at prediction time. For example, if you are predicting tomorrow's solar radiation, you cannot use tomorrow's relative humidity as a feature because that value will not be known until tomorrow. Always ask: *will this feature be available when the model is used?*

### Reusing the validation set too much

The validation set is for comparison, but if you test hundreds of ideas on it, the model effectively learns what the validation set looks like. Keep a final **test set** that is only used once at the end.

---

## 7. Hyperparameters in generative AI

Generative AI uses the same tuning principles, but the settings themselves are different. You are usually not choosing a tree depth or a kernel width; you are choosing how the model generates text, images, or other outputs.

### Inference-time hyperparameters

These are set when you call the model, not when you train it:

- **Temperature:** controls how random the output is. `0` means deterministic; higher values mean more creative and unpredictable.
- **Top-p (nucleus sampling):** limits the model to a small set of likely next tokens. A low `top-p` makes output focused and safe; a high `top-p` lets the model explore rare words.
- **Top-k:** limits the model to the `k` most likely next tokens.
- **Max output length:** the longest sequence the model is allowed to produce.
- **System prompt / prompt template:** the instructions you give the model before the user's question. This is one of the most powerful levers.
- **Number of in-context examples:** how many examples you show the model in the prompt for few-shot learning.

### Training-time hyperparameters for generative models

When you fine-tune a large language or image model, you still tune:

- **Learning rate and schedule**
- **Batch size and number of epochs**
- **LoRA rank and alpha** (when using parameter-efficient fine-tuning)
- **Warm-up steps**
- **Context window length**

### What makes tuning harder

- **Evaluation is expensive.** Generative output is open-ended, so you may need human review, an LLM-as-a-judge, or task-specific benchmarks.
- **Compute is expensive.** Large models take a long time to train, so you cannot run hundreds of grid-search trials.
- **Small gains may not be worth the cost.** Going from 92% to 93% quality might need ten times more compute. Domain knowledge and budget matter more than ever.

---

## 8. One-sentence takeaway

**Hyperparameters control how a model learns; grid search and random search help you find good values, but the best tuning is useless if you leak information from the validation or test set into the training process.**
