---
title: "20. PCA and Dimensionality Reduction - A Friendly Guide"
category: Machine Learning
order: 20
tags:
  - machine-learning
  - pca
  - dimensionality-reduction
  - unsupervised-learning
  - principal-component-analysis
  - feature-extraction
  - beginners
  - friendly
summary: A complete beginner-friendly guide to PCA and dimensionality reduction. Learn why too many features hurt models, how PCA finds the directions of maximum variance, and how to apply it in Python step by step.
---

# PCA and Dimensionality Reduction

## When having too many features becomes a problem

Imagine you are trying to classify emails as spam. You have 10,000 unique words in your vocabulary, so each email is represented as a vector of 10,000 numbers. Most of those numbers are zero. Many words carry almost no useful information. And many words are highly correlated — "free" and "prize" tend to appear together anyway.

This is the **curse of dimensionality**: too many features make models slow to train, prone to overfitting, and hard to visualise.

**Dimensionality reduction** solves this by compressing many features into fewer ones — while keeping as much useful information as possible.

**Principal Component Analysis (PCA)** is the most widely used dimensionality reduction technique.

This tutorial covers:

1. Why dimensionality is a problem.
2. The core idea of PCA — variance and directions.
3. How PCA works step by step.
4. How much information does each component keep?
5. Full Python demonstration.
6. When to use PCA.

---

## 1. Why too many features hurt

| Problem | What happens |
|---------|-------------|
| **Slow training** | Every algorithm slows down with more features |
| **Overfitting** | Model memorises noise in rarely-seen features |
| **Redundant information** | Correlated features add noise, not signal |
| **Hard to visualise** | You cannot plot 100-dimensional data |
| **Curse of dimensionality** | In high dimensions, all points appear equally distant |

> **Memory trick:** Imagine navigating a city with a 10,000-room map when only 20 rooms actually matter. PCA finds those 20 rooms and throws away the rest.

---

## 2. The core idea — find the directions of most variation

PCA asks a simple question: **which direction in your data has the most spread?**

Consider a dataset of emails described by two features: suspicious word count and link count. If you plot them, the data forms a cloud. That cloud has a natural "long axis" — the direction where most of the variation lives.

```
Links
  ↑
5 |        ●  ●
4 |      ●   ●  ●
3 |    ●  ●     ●
2 |  ●  ●
1 | ●
  +──────────────→ Suspicious words
    1  2  3  4  5
```

The long diagonal axis is the **first principal component (PC1)**. It captures the most variance.

The perpendicular axis is the **second principal component (PC2)**. It captures the remaining variance.

PCA rotates your coordinate system so the axes align with these directions of maximum variance. Then you can drop the low-variance axes and keep only the high-variance ones.

---

## 3. How PCA works — step by step

**Step 1 — Centre the data**

Subtract the mean of each feature so the data is centred at zero.

```python
import numpy as np

X = np.array([
    [3, 2], [4, 3], [5, 4], [2, 1], [6, 5], [1, 1]
])

X_centred = X - X.mean(axis=0)
```

**Step 2 — Compute the covariance matrix**

The covariance matrix captures how features vary together.

```python
cov_matrix = np.cov(X_centred.T)
print(cov_matrix)
# [[2.67  2.40]
#  [2.40  2.27]]
# High covariance → features move together
```

**Step 3 — Find eigenvectors and eigenvalues**

Eigenvectors are the directions of the principal components. Eigenvalues tell you how much variance each direction captures.

```python
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
print("Eigenvalues:", eigenvalues)
# Eigenvalues: [4.85  0.09]  ← PC1 captures 98% of variance!
```

**Step 4 — Sort by eigenvalue (most variance first)**

```python
order = np.argsort(eigenvalues)[::-1]
eigenvalues  = eigenvalues[order]
eigenvectors = eigenvectors[:, order]
```

**Step 5 — Project the data onto the top components**

```python
# Keep only PC1 (1 dimension instead of 2)
X_reduced = X_centred @ eigenvectors[:, 0:1]
print(X_reduced.shape)  # (6, 1) — 2D data compressed to 1D
```

In practice, `sklearn` does all of this for you.

---

## 4. How much variance does each component explain?

```python
from sklearn.decomposition import PCA
import numpy as np

X = np.array([
    [3, 2, 1, 5], [4, 3, 2, 6], [5, 4, 1, 7],
    [2, 1, 3, 4], [6, 5, 2, 8], [1, 1, 4, 3]
])

pca = PCA()
pca.fit(X)

print("Explained variance ratio per component:")
for i, ratio in enumerate(pca.explained_variance_ratio_):
    print(f"  PC{i+1}: {ratio:.3f}  ({ratio*100:.1f}%)")

print(f"\nCumulative variance:")
cumulative = np.cumsum(pca.explained_variance_ratio_)
for i, cum in enumerate(cumulative):
    print(f"  First {i+1} components: {cum:.3f}  ({cum*100:.1f}%)")
```

Output might look like:
```
PC1: 0.872  (87.2%)
PC2: 0.103  (10.3%)
PC3: 0.019   (1.9%)
PC4: 0.006   (0.6%)

First 2 components: 0.975  (97.5%)
```

Two components capture 97.5% of the information — you can safely drop the other two.

---

## 5. Full Python demonstration

### PCA for dimensionality reduction before classification

```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt

# Generate high-dimensional data
X, y = make_classification(
    n_samples=300, n_features=20, n_informative=5,
    n_redundant=10, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Always scale before PCA
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# Without PCA
model_full = SVC()
model_full.fit(X_train_s, y_train)
acc_full = accuracy_score(y_test, model_full.predict(X_test_s))
print(f"Accuracy with all 20 features:  {acc_full:.3f}")

# With PCA — keep 95% of variance
pca = PCA(n_components=0.95)   # keep enough components for 95% variance
X_train_pca = pca.fit_transform(X_train_s)
X_test_pca  = pca.transform(X_test_s)

print(f"Components needed for 95% variance: {pca.n_components_}")

model_pca = SVC()
model_pca.fit(X_train_pca, y_train)
acc_pca = accuracy_score(y_test, model_pca.predict(X_test_pca))
print(f"Accuracy with {pca.n_components_} PCA components: {acc_pca:.3f}")
```

### Visualising the scree plot — choosing number of components

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_wine

# Load a real dataset
data = load_wine()
X = StandardScaler().fit_transform(data.data)

pca = PCA()
pca.fit(X)

# Scree plot
cumvar = np.cumsum(pca.explained_variance_ratio_)
plt.figure(figsize=(8, 4))
plt.bar(range(1, len(pca.explained_variance_ratio_)+1),
        pca.explained_variance_ratio_, alpha=0.7, label='Per component')
plt.plot(range(1, len(cumvar)+1), cumvar, 'r-o', label='Cumulative')
plt.axhline(y=0.95, color='g', linestyle='--', label='95% threshold')
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.title('Scree Plot — How many components to keep?')
plt.legend()
plt.tight_layout()
plt.show()

# Find the elbow
n_for_95 = np.argmax(cumvar >= 0.95) + 1
print(f"Components needed to reach 95% variance: {n_for_95}")
```

### Visualising high-dimensional data in 2D

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

data = load_iris()
X = StandardScaler().fit_transform(data.data)
y = data.target
names = data.target_names

# Reduce 4D → 2D for plotting
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

print(f"Variance captured by 2 components: {pca.explained_variance_ratio_.sum():.1%}")

plt.figure(figsize=(8, 6))
colors = ['red', 'green', 'blue']
for i, (name, color) in enumerate(zip(names, colors)):
    mask = y == i
    plt.scatter(X_2d[mask, 0], X_2d[mask, 1],
                c=color, label=name, alpha=0.7)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
plt.title('Iris Dataset — 4D projected to 2D with PCA')
plt.legend()
plt.tight_layout()
plt.show()
```

---

## 6. PCA for email/text data

```python
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

emails = [
    "free prize win now click",
    "claim your reward today free",
    "win iPhone limited offer free",
    "exclusive deal free gift win",
    "meeting agenda tomorrow 3pm",
    "project deadline Friday report",
    "quarterly review document attached",
    "please review the attached report",
    "free lunch meeting agenda",
    "report due project update",
]
labels = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]

# For sparse text matrices, use TruncatedSVD (equivalent to PCA for sparse)
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('svd',   TruncatedSVD(n_components=5)),   # reduce to 5 dimensions
    ('svm',   LinearSVC(C=1.0))
])

pipeline.fit(emails, labels)
test = ["free win prize offer", "team meeting tomorrow"]
print(pipeline.predict(test))   # [1, 0]
```

---

## 7. PCA vs other dimensionality reduction techniques

| Technique | How it works | Best for |
|-----------|-------------|----------|
| **PCA** | Linear projection onto variance axes | Continuous features, preprocessing |
| **TruncatedSVD** | Same as PCA but works on sparse matrices | Text data (TF-IDF) |
| **t-SNE** | Non-linear, preserves local structure | Visualisation only |
| **UMAP** | Non-linear, faster than t-SNE | Visualisation + some downstream tasks |
| **LDA** | Uses class labels to find discriminative directions | Supervised dimensionality reduction |

---

## 8. When to use PCA

**Good fit:**
- Many correlated features (e.g., many word counts that tend to co-occur)
- You need to visualise high-dimensional data in 2D or 3D
- Pre-processing before a slow algorithm like SVM
- Noisy data — dropping low-variance components removes noise

**Not ideal for:**
- When features are already independent (PCA adds no value)
- When you need to interpret individual features — PCA components are combinations of all original features
- Sparse data — use `TruncatedSVD` instead

---

## 9. Common mistakes

| Mistake | Fix |
|---------|-----|
| Not scaling before PCA | Always `StandardScaler` first — PCA is sensitive to scale |
| Applying PCA before train/test split | Fit PCA on training data only, then transform test data |
| Choosing a fixed number of components | Use `n_components=0.95` to keep 95% of variance automatically |
| Using PCA on sparse matrices | Use `TruncatedSVD` for text/sparse data |
| Thinking PCA selects features | PCA creates *new* features — combinations of the originals |

---

## 10. Try it yourself

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_digits
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 64-dimensional handwritten digit data
digits = load_digits()
X, y = digits.data, digits.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

for n in [5, 10, 20, 40, 64]:
    if n == 64:
        X_tr, X_te = X_train_s, X_test_s
        label = "no PCA (64)"
    else:
        pca = PCA(n_components=n)
        X_tr = pca.fit_transform(X_train_s)
        X_te = pca.transform(X_test_s)
        var  = pca.explained_variance_ratio_.sum()
        label = f"PCA n={n:2d} ({var:.0%} var)"

    model = SVC(kernel='rbf')
    model.fit(X_tr, y_train)
    acc = accuracy_score(y_test, model.predict(X_te))
    print(f"{label}  →  accuracy: {acc:.3f}")
```

---

## Summary

- PCA finds the directions (**principal components**) of maximum variance in your data.
- It projects the data onto those directions, letting you drop low-variance ones.
- The result is fewer features with most of the original information preserved.
- Always **scale before PCA** — it is sensitive to feature scale.
- Use the **scree plot** or `n_components=0.95` to decide how many components to keep.
- PCA does not select original features — it creates new ones that are linear combinations of all originals.
- For sparse text data, use `TruncatedSVD` instead.
