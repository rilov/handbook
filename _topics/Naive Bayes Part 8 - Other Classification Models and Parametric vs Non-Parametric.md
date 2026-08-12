---
title: "Naive Bayes Part 8: Other Classification Models and Parametric vs Non-Parametric"
category: Advanced Machine Learning
order: 12
permalink: /topics/naive-bayes-other-classification-models/
tags:
  - machine-learning
  - naive-bayes
  - logistic-regression
  - decision-tree
  - knn
  - svm
  - parametric
  - non-parametric
  - model-selection
summary: "Part 8 of the Naive Bayes series: compare Naive Bayes with Logistic Regression, Decision Tree, KNN and SVM on the UCI Spambase dataset, then learn the conceptual distinction between parametric and non-parametric models."
date: 2026-08-12
---

# Naive Bayes Part 8: Other Classification Models and Parametric vs Non-Parametric

> Part 8 of the Naive Bayes series. We step back and compare Naive Bayes against four other well-known classifiers on the same spam dataset, then organize them by a crucial conceptual idea: parametric versus non-parametric models.

---

## 1. What this topic does

So far we have focused on the Naive Bayes family itself. This topic widens the lens. We run the same experiment on the UCI **Spambase** dataset with five different classifiers:

- **Naive Bayes (Gaussian)**
- **Logistic Regression**
- **Decision Tree**
- **K-Nearest Neighbors (KNN)**
- **Support Vector Machine (SVM, linear kernel)**

We look at two things for each model: **accuracy** and **training time**. The goal is not to crown a single winner, but to see how the models' different assumptions, flexibility and computational costs trade off on the same data.

---

## 2. The dataset: UCI Spambase

We use the real UCI Spambase data from OpenML. It has:

- 4,601 emails
- 57 numerical features (word frequencies and message statistics)
- 39.4% spam, 60.6% ham

```python
import numpy as np
from sklearn.datasets import fetch_openml

X, y = fetch_openml(data_id=44, parser='auto', as_frame=False, return_X_y=True)
y = (y == '1').astype(int)   # spam = 1
print("Shape:", X.shape, "class balance:", np.mean(y))
```

The 57 features are already numerical, but they are on very different scales. Many classifiers are sensitive to scale, so we standardize every feature to mean 0 and standard deviation 1.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(
    X.astype(float), y, test_size=0.3, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
```

---

## 3. Training and evaluating the five models

All five models are trained on the scaled training data and evaluated on the same held-out test set.

```python
import time
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

models = {
    "Naive Bayes (Gaussian)": GaussianNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "SVM (linear)": SVC(kernel="linear", random_state=42),
}

for name, model in models.items():
    t0 = time.perf_counter()
    model.fit(X_train_s, y_train)
    train_time = time.perf_counter() - t0
    acc = accuracy_score(y_test, model.predict(X_test_s))
    print(f"{name:25s} accuracy={acc:.4f}  train_time={train_time:.4f}s")
```

### Verified results

```
Naive Bayes (Gaussian)    accuracy=0.8197  train_time=0.0014s
Logistic Regression       accuracy=0.9290  train_time=0.0411s
Decision Tree             accuracy=0.8928  train_time=0.0577s
KNN (k=5)                 accuracy=0.8993  train_time=0.0011s
SVM (linear)              accuracy=0.9290  train_time=0.3218s
```

| Model | Accuracy | Training time |
|---|---|---|
| **Logistic Regression** | **92.9%** | 0.041s |
| **SVM (linear)** | **92.9%** | 0.322s |
| KNN (k=5) | 89.9% | 0.001s |
| Decision Tree | 89.3% | 0.058s |
| Naive Bayes (Gaussian) | 82.0% | 0.001s |

Two clear stories emerge:

- **Accuracy:** SVM and Logistic Regression tie at the top. KNN and Decision Tree are in the middle. Naive Bayes is the simplest but also the least accurate here.
- **Training speed:** Naive Bayes and KNN are essentially instantaneous at `fit()` time. Logistic Regression and Decision Tree are still fast. SVM is the slowest by a wide margin.

This is a classic accuracy-versus-speed tradeoff. There is no single "best" model — the right choice depends on which of these dimensions matters most for your project.

---

## 4. Parametric vs non-parametric models

A second, deeper way to compare these models is to ask: **does the model assume a fixed mathematical shape, or does it learn the shape from the data?**

### Parametric models

A parametric model assumes a specific functional form and then estimates a fixed set of parameters from the data. For example:

- **Naive Bayes** assumes each class follows a product of conditional probabilities and the continuous version assumes Gaussian distributions.
- **Logistic Regression** assumes a linear decision boundary in feature space (possibly after a transformation).
- **SVM (with a linear kernel)** also learns a linear boundary.

Because the form is fixed, training is usually fast and the model is easy to interpret. But if the true relationship is very different from the assumed form, the model will be wrong no matter how much data you feed it.

### Non-parametric models

A non-parametric model does **not** commit to a single equation ahead of time. It learns the relationship directly from the data:

- **Decision Tree** learns a series of if/then splits from the data.
- **KNN** simply remembers the training points and predicts by looking up the closest neighbors.
- **SVM with non-linear kernels** can also behave non-parametrically by mapping features into higher-dimensional spaces and adapting to the data's shape.

These models are more flexible, but that flexibility costs: they often need more data, more computation and more careful tuning to avoid overfitting.

### Classification of the five models

| Model | Parametric or non-parametric | Why? |
|---|---|---|
| Naive Bayes | **Parametric** | Assumes a specific probability distribution for each feature. |
| Logistic Regression | **Parametric** | Assumes a linear log-odds boundary. |
| SVM (linear) | **Parametric** | Learns a single linear separating hyperplane. |
| SVM (RBF) | **Non-parametric** (can be) | Adapts to complex shapes via the kernel. |
| Decision Tree | **Non-parametric** | Splits are learned from the data, not fixed. |
| KNN | **Non-parametric** | Predictions come from nearby training points, not from a fitted equation. |

So SVM is an interesting bridge: a **linear SVM is parametric**, but an **SVM with an RBF kernel behaves more like a non-parametric model**.

---

## 5. Model characteristics and when to use each

### Accuracy vs interpretability

- **Naive Bayes and Logistic Regression** are the most interpretable. Naive Bayes shows you class-conditional probabilities; Logistic Regression shows you feature weights.
- **SVM and KNN** are less transparent. SVM's support vectors matter, but the final boundary is not as easy to read as a probability table. KNN has no coefficients at all — its "model" is the entire training set.
- **Decision Tree** is somewhere in the middle. A small tree is easy to read; a deep tree is not.

### Training time

- **Naive Bayes and KNN** train almost instantly. Naive Bayes is literally counting; KNN is just storing data.
- **Logistic Regression and Decision Tree** are fast enough for most applications.
- **SVM** is the slowest, especially on larger datasets. This is why linear SVMs and approximate solvers are often preferred for large-scale work.

### Assumptions

- **Naive Bayes** assumes feature independence and, for Gaussian NB, normally distributed continuous features.
- **Logistic Regression** assumes a linearly separable problem in the feature space (or the space you transform into).
- **Decision Tree and KNN** make relatively few assumptions about the data distribution. That makes them more flexible but also more prone to overfitting if not regularized or tuned.
- **SVM (linear)** assumes a linear boundary. **SVM (kernel)** can fit more complex boundaries but needs kernel and `C` tuning.

### Parametric vs non-parametric: the rule of thumb

- **Use a parametric model** when:
  - You believe the data roughly matches a known distribution or shape.
  - You want speed, simplicity and interpretability.
  - You have limited data.

- **Use a non-parametric model** when:
  - The relationship between features and the target is complex or unknown.
  - You have enough data for the model to learn the complexity.
  - You are willing to trade some speed and interpretability for better fit.

---

## 6. Summary

- Naive Bayes is fast and simple, but on the UCI Spambase dataset it is outperformed by Logistic Regression and SVM.
- **Logistic Regression and linear SVM** achieved the highest accuracy (~92.9%) on this data, but SVM took much longer to train.
- **Decision Tree and KNN** sit in the middle in both accuracy and speed.
- A key conceptual distinction is **parametric vs non-parametric**: Naive Bayes, Logistic Regression and linear SVM assume a fixed form; Decision Trees and KNN learn the form from the data.
- SVM is a bridge: linear SVMs are parametric, while SVMs with non-linear kernels can act as non-parametric models.
- The best model is the one whose assumptions, speed and flexibility match your problem — not the one with the highest test accuracy in isolation.

**Series recap:** intuition (Part 1) → Bayes' theorem (Part 2) → the classifier (Part 3) → Gaussian (Part 4) → Multinomial (Part 5) → Bernoulli (Part 6) → choosing between variants (Part 7) → comparing Naive Bayes to other models (Part 8, this topic).
