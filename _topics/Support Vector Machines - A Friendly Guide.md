---
title: "19. Support Vector Machines - A Friendly Guide"
category: Machine Learning
order: 19
tags:
  - machine-learning
  - svm
  - support-vector-machines
  - classification
  - kernel-trick
  - margin
  - beginners
  - friendly
summary: A complete beginner-friendly guide to Support Vector Machines. Learn how SVMs find the best boundary between classes, what the kernel trick does, and how to use SVMs in Python for real classification tasks.
---

# Support Vector Machines

## Finding the best possible boundary

Suppose you have two groups of points on a piece of paper — red dots and blue dots — and you want to draw a line that separates them. You could draw many different lines that work. But which one is *best*?

A **Support Vector Machine** (SVM) answers that question with a precise definition of "best": the line that has the largest possible gap between the two groups. This gap is called the **margin**, and maximising it is the entire goal of SVM.

This tutorial covers:

1. The intuition — what is a margin and why does it matter?
2. Support vectors — which points actually define the boundary?
3. Soft margin — handling data that is not perfectly separable.
4. The kernel trick — separating data that no straight line can divide.
5. Full Python demonstration.
6. When to use SVMs.

---

## 1. The intuition — margins matter

Imagine classifying emails as spam or not spam based on two features: number of suspicious words and number of links.

You could draw many lines to separate them:

```
Line A: passes very close to several spam emails
Line B: passes right through the middle of the gap between groups  ← SVM picks this
Line C: passes very close to several normal emails
```

Line B is the safest choice. If a new email arrives that is slightly ambiguous, Line B gives it the most room to be classified correctly. Lines A and C would misclassify borderline emails.

The **margin** is the width of the empty zone around the boundary line. SVM finds the line that maximises this margin.

> **Memory trick:** SVM is like drawing a road between two cities. You want the road as far from both cities as possible, so drivers have maximum safety margin on either side.

---

## 2. Support vectors — the critical points

Here is the key insight: **most training points don't matter**.

Only the points sitting right on the edge of each group — the ones closest to the boundary — determine where the boundary goes. These are the **support vectors**.

```
Normal emails:  ●  ●  ●  [●]  |    [■]  ■  ■  ■   :Spam emails
                              ↑    ↑
                         support vectors
                         (these define the boundary)
```

If you removed all other points and kept only the support vectors, the boundary would be exactly the same. This is why SVM is memory-efficient — after training, only the support vectors are stored.

---

## 3. Soft margin — real data is messy

In practice, data is rarely perfectly separable. A few spam emails will have no links and few suspicious words. A few normal emails will have several suspicious words.

A **hard margin** SVM requires perfect separation — impossible with noisy data. A **soft margin** SVM allows some points to be on the wrong side of the boundary, controlled by a parameter **C**:

- **Large C** — strict, tries hard to classify everything correctly → can overfit
- **Small C** — relaxed, allows more misclassifications → better generalisation

```python
from sklearn.svm import SVC

model_strict = SVC(C=100)   # large C — tight margin, few errors allowed
model_relaxed = SVC(C=0.1)  # small C — wide margin, some errors allowed
```

> **Memory trick:** C is the "cost of being wrong." High C = high cost = model tries very hard not to make mistakes.

---

## 4. The kernel trick — handling non-linear data

Sometimes no straight line can separate the two classes. Look at this:

```
          ●  ●  ●
       ●           ●
     ●    ■  ■  ■    ●
       ●           ●
          ●  ●  ●
```

The spam emails (■) are clustered in the centre, surrounded by normal emails (●). No straight line divides them.

The **kernel trick** solves this by mathematically transforming the data into a higher-dimensional space where a straight line *can* separate them — without ever explicitly computing that transformation.

Common kernels:

| Kernel | When to use |
|--------|-------------|
| `linear` | Data is roughly linearly separable, high-dimensional (e.g., text) |
| `rbf` (radial basis function) | Most common default — handles curved boundaries |
| `poly` | Polynomial boundaries — less common |

```python
# Linear kernel — for text classification, high-dimensional data
model = SVC(kernel='linear')

# RBF kernel — for most other problems (default)
model = SVC(kernel='rbf', C=1.0, gamma='scale')
```

> **Memory trick:** The kernel trick is like crumpling a piece of paper so two groups of dots that were mixed together now sit on different layers — then cutting between the layers.

---

## 5. Full Python demonstration

### Binary classification — spam detection

```python
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# Features: [suspicious_words, links, known_sender, capital_ratio, length]
X = np.array([
    [5, 3, 0, 0.40, 35],
    [4, 2, 0, 0.35, 42],
    [6, 4, 0, 0.50, 28],
    [3, 1, 0, 0.30, 55],
    [5, 5, 0, 0.45, 30],
    [4, 3, 0, 0.38, 40],
    [0, 0, 1, 0.02, 120],
    [1, 0, 1, 0.03, 95],
    [0, 1, 1, 0.05, 110],
    [0, 0, 1, 0.01, 140],
    [1, 1, 1, 0.04, 100],
    [0, 0, 1, 0.02, 130],
])
y = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]  # 1=spam, 0=not spam

# Step 1 — Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Step 2 — Scale features (IMPORTANT for SVM)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# Step 3 — Train SVM
model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
model.fit(X_train_scaled, y_train)

# Step 4 — Evaluate
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred, target_names=["not spam", "spam"]))

# Step 5 — Check support vectors
print(f"\nNumber of support vectors per class: {model.n_support_}")
print(f"Total support vectors: {sum(model.n_support_)}")

# Step 6 — Predict new email
new_email = np.array([[3, 2, 0, 0.25, 50]])
new_scaled = scaler.transform(new_email)
pred = model.predict(new_scaled)
prob = model.predict_proba(new_scaled)
print(f"\nNew email: {'SPAM' if pred[0]==1 else 'NOT SPAM'}")
print(f"Confidence: spam={prob[0][1]:.2f}, not spam={prob[0][0]:.2f}")
```

### Text classification with linear SVM

Linear SVMs work exceptionally well for text:

```python
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

emails = [
    "free prize win now click",
    "claim your reward today",
    "win iPhone limited offer free",
    "exclusive deal free gift",
    "meeting agenda tomorrow 3pm",
    "project deadline Friday report",
    "quarterly review attached",
    "please review the document",
]
labels = [1, 1, 1, 1, 0, 0, 0, 0]

# Pipeline: TF-IDF → Linear SVM
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('svm',   LinearSVC(C=1.0, max_iter=1000))
])

pipeline.fit(emails, labels)

test = ["free iPhone win prize now", "team meeting tomorrow agenda"]
predictions = pipeline.predict(test)
for email, pred in zip(test, predictions):
    print(f"'{email}' → {'SPAM' if pred==1 else 'NOT SPAM'}")
```

### Visualising the decision boundary (2D)

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

# Simple 2D example: suspicious words vs links
X = np.array([
    [5, 3], [4, 2], [6, 4], [3, 2], [5, 5],
    [0, 0], [1, 0], [0, 1], [1, 1], [0, 0]
])
y = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]

model = SVC(kernel='rbf', C=1.0, gamma='scale')
model.fit(X, y)

# Plot
xx, yy = np.meshgrid(np.linspace(-1, 8, 200), np.linspace(-1, 6, 200))
Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu')
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='RdBu', edgecolors='k')

# Highlight support vectors
sv = model.support_vectors_
plt.scatter(sv[:, 0], sv[:, 1], s=200, facecolors='none',
            edgecolors='k', linewidths=2, label='Support vectors')
plt.xlabel('Suspicious words')
plt.ylabel('Links')
plt.title('SVM Decision Boundary')
plt.legend()
plt.show()
```

---

## 6. Scaling is not optional

SVM is one of the few algorithms where **forgetting to scale your features will badly hurt performance**.

Why? The margin calculation uses distances. If feature A ranges from 0–1 and feature B ranges from 0–10,000, feature B will dominate the distance calculation and drown out feature A.

Always scale before training an SVM:

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)   # use fit from training set only
```

---

## 7. Tuning C and gamma

For RBF kernel, two parameters matter most:

| Parameter | Effect |
|---|---|
| **C** | How much to penalise misclassifications. High C = complex boundary. |
| **gamma** | How far each training point's influence reaches. High gamma = complex, localised boundary. |

Use grid search to find the best combination:

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C':     [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
}

grid = GridSearchCV(SVC(kernel='rbf'), param_grid, cv=5, scoring='accuracy')
grid.fit(X_train_scaled, y_train)

print(f"Best params: {grid.best_params_}")
print(f"Best CV score: {grid.best_score_:.3f}")
```

---

## 8. SVM vs other classifiers

| Algorithm | SVM advantage | SVM disadvantage |
|---|---|---|
| Logistic Regression | Better with non-linear boundaries (RBF) | Slower, harder to tune |
| Decision Trees | Less prone to overfitting | Not as interpretable |
| Naive Bayes | Better with continuous features | Slower to train |
| KNN | No need to store training data after fitting | KNN faster on small datasets |
| Neural Networks | Works well with small-medium datasets | Neural nets scale better to huge data |

**SVM sweet spot:** Medium-sized datasets (up to ~100k rows), high-dimensional data (text), or problems where the margin intuition fits naturally.

---

## 9. Common mistakes

| Mistake | Fix |
|---|---|
| Forgetting to scale features | Always use `StandardScaler` before SVM |
| Using RBF kernel on text | Use `LinearSVC` for text — much faster |
| Using `SVC` on large datasets (>100k rows) | Use `LinearSVC` or `SGDClassifier` instead |
| Not tuning C | Default C=1 is often suboptimal — try `GridSearchCV` |
| Expecting probability outputs from `LinearSVC` | Use `SVC(probability=True)` or `CalibratedClassifierCV` |

---

## 10. Try it yourself

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Generate a synthetic dataset
X, y = make_classification(
    n_samples=200, n_features=5, n_informative=3,
    n_redundant=1, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

for kernel in ['linear', 'rbf', 'poly']:
    model = SVC(kernel=kernel, C=1.0)
    model.fit(X_train_s, y_train)
    acc = accuracy_score(y_test, model.predict(X_test_s))
    print(f"Kernel={kernel:8s}  Accuracy={acc:.3f}  Support vectors={sum(model.n_support_)}")
```

Try different values of C (0.01, 1, 100) and see how the number of support vectors changes.

---

## Summary

- SVM finds the decision boundary that **maximises the margin** between classes.
- The boundary is determined only by the **support vectors** — the points closest to the boundary.
- **C** controls the trade-off between a wide margin and fewer misclassifications.
- The **kernel trick** maps data to higher dimensions where it becomes linearly separable.
- Always **scale your features** before training an SVM.
- **LinearSVC** for text and high-dimensional data. **SVC(kernel='rbf')** for everything else.
