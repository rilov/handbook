---
title: "21. Semi-Supervised Learning - A Friendly Guide"
category: Machine Learning
order: 21
tags:
  - machine-learning
  - semi-supervised-learning
  - label-propagation
  - self-training
  - gan
  - beginners
  - friendly
summary: A beginner-friendly guide to semi-supervised learning — the technique that uses a small amount of labelled data and a large amount of unlabelled data together. Covers self-training, label propagation, and GANs with Python examples.
---

# Semi-Supervised Learning

## Making the most of data you haven't labelled yet

Labelling data is expensive. Training a spam classifier requires someone to read thousands of emails and mark each one spam or not spam. Building a medical image classifier requires doctors to examine thousands of scans. This takes enormous time and money.

But you almost always have far more *unlabelled* data than labelled data. Your inbox has millions of emails. Hospitals have millions of scans. Can the model learn something useful from the unlabelled data, guided by the small labelled set?

Yes — and that is exactly what **semi-supervised learning** does.

> **Definition:** Semi-supervised learning trains on a **small labelled dataset** and a **large unlabelled dataset** together, using the unlabelled data to improve the model.

This tutorial covers:

1. When you need semi-supervised learning.
2. Self-training — the simplest approach.
3. Label propagation — spreading labels through a graph.
4. GANs — generating unlabelled data as a semi-supervised tool.
5. Full Python demonstrations.
6. When to use each approach.

---

## 1. The problem — labels are rare, data is abundant

Typical real-world situation:

| Dataset | Labelled | Unlabelled |
|---------|----------|------------|
| Email spam | 500 labelled | 50,000 unlabelled |
| Medical images | 200 labelled | 10,000 unlabelled |
| Product reviews | 1,000 labelled | 500,000 unlabelled |

Options:

- **Pure supervised learning** — use only the 500 labelled examples. Simple but wastes 50,000 data points.
- **Pure unsupervised learning** — use all 50,500 but ignore the labels entirely. Loses the useful signal.
- **Semi-supervised learning** — use all 50,500, with the 500 labels guiding the learning. Best of both worlds.

> **Memory trick:** Imagine teaching a child to recognise cats. You show 10 labelled pictures of cats and non-cats. Then you let them look at 1,000 unlabelled photos and tell you which ones look similar to the labelled cats. They learn much faster than from 10 pictures alone.

---

## 2. Self-training — the simplest approach

Self-training is the most intuitive semi-supervised method:

1. Train a model on the small labelled dataset.
2. Use the model to predict labels on the unlabelled data.
3. Add the highest-confidence predictions to the labelled set.
4. Re-train the model on the expanded labelled set.
5. Repeat until no high-confidence unlabelled points remain.

```python
import numpy as np
from sklearn.semi_supervised import SelfTrainingClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Generate data
X, y = make_classification(n_samples=1000, n_features=10,
                            n_informative=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Simulate having only 50 labelled examples out of 800
y_train_partial = y_train.copy()
unlabelled_idx = np.random.choice(len(y_train), size=750, replace=False)
y_train_partial[unlabelled_idx] = -1   # -1 = unlabelled in sklearn

# Compare: supervised only (50 labels) vs self-training (50 labels + 750 unlabelled)
base_model = SVC(kernel='rbf', probability=True, C=1.0)

# Supervised only — ignore unlabelled points
labelled_mask = y_train_partial != -1
sup_model = SVC(kernel='rbf')
sup_model.fit(X_train[labelled_mask], y_train[labelled_mask])
acc_sup = accuracy_score(y_test, sup_model.predict(X_test))

# Self-training — uses unlabelled points too
self_trainer = SelfTrainingClassifier(base_estimator=SVC(kernel='rbf', probability=True))
self_trainer.fit(X_train, y_train_partial)
acc_semi = accuracy_score(y_test, self_trainer.predict(X_test))

print(f"Supervised only (50 labels):          {acc_sup:.3f}")
print(f"Self-training  (50 labels + 750 more): {acc_semi:.3f}")
```

### How confidence threshold works

```python
# threshold=0.9 means: only add predictions the model is 90%+ confident about
self_trainer = SelfTrainingClassifier(
    base_estimator=SVC(kernel='rbf', probability=True),
    threshold=0.9,       # minimum confidence to accept a pseudo-label
    max_iter=10          # maximum rounds of self-training
)
```

---

## 3. Label propagation — spreading labels through similarity

Label propagation treats data points as a graph. Labelled points are sources. Their labels spread to similar unlabelled points like ink spreading through paper.

```python
from sklearn.semi_supervised import LabelPropagation, LabelSpreading
import numpy as np
from sklearn.datasets import make_moons
import matplotlib.pyplot as plt

# Two-moon dataset — classic semi-supervised benchmark
X, y = make_moons(n_samples=300, noise=0.1, random_state=42)

# Keep only 10% of labels
y_partial = y.copy()
unlabelled = np.random.choice(len(y), size=270, replace=False)
y_partial[unlabelled] = -1   # -1 = unlabelled

# Label Propagation
lp = LabelPropagation(kernel='rbf', gamma=20)
lp.fit(X, y_partial)

acc = (lp.predict(X[unlabelled]) == y[unlabelled]).mean()
print(f"Label Propagation accuracy on unlabelled: {acc:.3f}")

# Label Spreading (more robust to noise)
ls = LabelSpreading(kernel='rbf', alpha=0.2)
ls.fit(X, y_partial)
acc_ls = (ls.predict(X[unlabelled]) == y[unlabelled]).mean()
print(f"Label Spreading accuracy on unlabelled:   {acc_ls:.3f}")
```

### Label Propagation vs Label Spreading

| | Label Propagation | Label Spreading |
|---|---|---|
| Labelled points | Kept fixed | Can be updated slightly |
| Noise handling | Can overfit to noisy labels | More robust |
| Parameter | `gamma` (kernel width) | `alpha` (how much labels spread) |

---

## 4. GANs — learning from unlabelled data via generation

A **Generative Adversarial Network (GAN)** trains two neural networks against each other:

- **Generator** — creates fake examples that look like real data
- **Discriminator** — tries to tell real examples from fake ones

The discriminator learns the structure of the data without needing labels. This learned structure can then be fine-tuned with a small labelled dataset — a powerful form of semi-supervised learning.

```python
import torch
import torch.nn as nn

# Simple GAN structure (conceptual — full training loop omitted for brevity)
class Generator(nn.Module):
    def __init__(self, noise_dim=10, output_dim=5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(noise_dim, 16),
            nn.ReLU(),
            nn.Linear(16, output_dim),
        )
    def forward(self, z):
        return self.net(z)

class Discriminator(nn.Module):
    def __init__(self, input_dim=5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)

# The discriminator learns the data distribution from unlabelled examples.
# Its internal representations (features) can then be used for classification
# with only a small labelled set — the semi-supervised GAN approach.
```

---

## 5. Choosing the right approach

| Situation | Best approach |
|-----------|--------------|
| Any sklearn-compatible model, few labels | **Self-training** |
| Data has clear clusters or manifold structure | **Label Propagation / Spreading** |
| Image or text data, large unlabelled set | **GAN-based or pre-trained models** |
| Labels are noisy | **Label Spreading** (more robust than Propagation) |

---

## 6. When semi-supervised learning helps most

**Works well when:**
- Labelled data is very small (< 5–10% of total data)
- Unlabelled data is abundant and from the same distribution
- The data has natural cluster structure

**Works poorly when:**
- Unlabelled data is from a different distribution than labelled data
- The model's early predictions (in self-training) are very wrong — errors compound
- The dataset is already large and fully labelled

---

## Summary

- Semi-supervised learning bridges the gap between supervised and unsupervised learning.
- It uses a **small labelled set** to guide learning from a **large unlabelled set**.
- **Self-training**: train on labels → predict unlabelled → add confident predictions → retrain.
- **Label propagation**: labels spread from labelled to similar unlabelled points.
- **GANs**: the discriminator learns data structure from unlabelled examples, then fine-tuned with labels.
- Most powerful when labelled data is scarce and unlabelled data is plentiful.
