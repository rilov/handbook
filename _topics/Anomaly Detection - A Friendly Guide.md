---
title: "26. Anomaly Detection - A Friendly Guide"
category: Machine Learning
order: 26
tags:
  - machine-learning
  - anomaly-detection
  - outlier-detection
  - isolation-forest
  - one-class-svm
  - unsupervised-learning
  - fraud-detection
  - beginners
  - friendly
summary: A beginner-friendly guide to anomaly detection. Learn how to find unusual data points using isolation forest, one-class SVM, and statistical methods. Covers fraud detection, network intrusion, and quality control with full Python examples.
---

# Anomaly Detection

## Finding the needle in the haystack

Most credit card transactions are normal. A few are fraudulent. Most machines in a factory work correctly. A few are about to fail. Most network packets are legitimate. Some are intrusion attempts.

**Anomaly detection** — also called **outlier detection** — is the task of finding the rare, unusual points that don't fit the pattern of normal data.

The challenge: you often have thousands of normal examples but very few (or zero) examples of anomalies to train on.

This tutorial covers:

1. What makes something an anomaly?
2. Statistical methods — Z-score and IQR.
3. Isolation Forest — the most popular algorithm.
4. One-Class SVM.
5. Autoencoder-based detection.
6. Full Python demonstration.
7. Choosing the right method.

---

## 1. What makes something an anomaly?

Three types:

| Type | Description | Example |
|------|-------------|---------|
| **Point anomaly** | A single unusual data point | A £50,000 credit card transaction when typical is £50 |
| **Contextual anomaly** | Unusual in context, normal elsewhere | 25°C in December (unusual), 25°C in July (normal) |
| **Collective anomaly** | A group of points is unusual together | 100 small transactions in 5 minutes from the same card |

> **Memory trick:** An anomaly is not just a rare event. It's a point that looks different from the bulk of the data.

---

## 2. Statistical methods — simple baselines

### Z-score (standard deviations from the mean)

```python
import numpy as np

# Transaction amounts (£)
amounts = np.array([45, 52, 48, 55, 51, 47, 49, 1500, 53, 46, 50, 48])

mean = amounts.mean()
std  = amounts.std()
z_scores = (amounts - mean) / std

print("Z-scores:", z_scores.round(2))
# [−0.45, 0.08, −0.27, 0.35, −0.01, −0.36, −0.18, 9.43, 0.17, −0.45, −0.09, −0.27]

# Flag anything beyond 3 standard deviations
anomalies = amounts[np.abs(z_scores) > 3]
print("Anomalies:", anomalies)   # [1500]
```

### IQR (Interquartile Range) — robust to extreme values

```python
Q1 = np.percentile(amounts, 25)
Q3 = np.percentile(amounts, 75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

anomalies = amounts[(amounts < lower) | (amounts > upper)]
print(f"IQR bounds: {lower:.1f} to {upper:.1f}")
print("Anomalies:", anomalies)   # [1500]
```

These work well for simple, single-feature data. For multi-dimensional data (many features), machine learning methods are needed.

---

## 3. Isolation Forest — the most popular algorithm

**Isolation Forest** works on a clever insight: **anomalies are easy to isolate**.

Think of it like a guessing game: "I'm thinking of a data point. Ask yes/no questions about features to find it."

- Normal points: need many questions (they blend in with the crowd)
- Anomalous points: need very few questions (they are isolated from the rest)

```
Normal transaction: 
  "Amount > £100?" No → "Amount > £50?" No → "Amount > £45?" Yes → Found (5 questions needed)

Fraudulent transaction (£50,000):
  "Amount > £100?" Yes → "Amount > £1000?" Yes → "Amount > £10000?" Yes → Found (3 questions needed)
```

The fewer questions needed, the more anomalous the point.

```python
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Simulate credit card transactions: [amount, hour_of_day]
np.random.seed(42)
normal = np.column_stack([
    np.random.normal(50, 15, 500),     # typical amounts £50 ± £15
    np.random.normal(13, 4, 500),      # typical hour: 1pm ± 4 hours
])

# Inject anomalies
anomalies_true = np.array([
    [5000, 3],   # large amount at 3am
    [4500, 2],   # large amount at 2am
    [8000, 4],   # huge amount at 4am
    [50, 2],     # normal amount but at 2am
])

X = np.vstack([normal, anomalies_true])

# Fit Isolation Forest
iso_forest = IsolationForest(
    n_estimators=100,      # number of trees
    contamination=0.01,    # expected fraction of anomalies (1%)
    random_state=42
)
iso_forest.fit(X)

predictions = iso_forest.predict(X)   # 1 = normal, -1 = anomaly
scores = iso_forest.score_samples(X)  # lower = more anomalous

n_anomalies = (predictions == -1).sum()
print(f"Detected {n_anomalies} anomalies")

# Visualise
normal_mask   = predictions ==  1
anomaly_mask  = predictions == -1

plt.figure(figsize=(8, 5))
plt.scatter(X[normal_mask, 0],  X[normal_mask, 1],  c='blue', alpha=0.3, label='Normal')
plt.scatter(X[anomaly_mask, 0], X[anomaly_mask, 1], c='red',  s=100,    label='Anomaly', marker='X')
plt.xlabel('Transaction amount (£)')
plt.ylabel('Hour of day')
plt.title('Isolation Forest — Anomaly Detection')
plt.legend()
plt.tight_layout()
plt.show()
```

---

## 4. One-Class SVM

One-Class SVM learns a tight boundary around the normal data. Anything outside the boundary is an anomaly.

```python
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler

# Scale first (important for SVM)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit One-Class SVM — nu is the expected fraction of anomalies
oc_svm = OneClassSVM(kernel='rbf', nu=0.05, gamma='scale')
oc_svm.fit(X_scaled)

predictions_svm = oc_svm.predict(X_scaled)   # 1 = normal, -1 = anomaly
n_anomalies_svm = (predictions_svm == -1).sum()
print(f"One-Class SVM detected {n_anomalies_svm} anomalies")
```

---

## 5. Local Outlier Factor (LOF)

LOF compares the density of each point's neighbourhood to its neighbours' neighbourhoods. Points in sparse regions relative to their neighbours are anomalies.

```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.01)
predictions_lof = lof.fit_predict(X)

n_lof = (predictions_lof == -1).sum()
print(f"LOF detected {n_lof} anomalies")
```

---

## 6. Comparing all three methods

```python
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
X_normal = np.random.multivariate_normal([0, 0], [[1, 0.5],[0.5, 1]], 500)
X_anomaly = np.random.uniform(-5, 5, (20, 2))
X = np.vstack([X_normal, X_anomaly])
true_labels = np.array([1]*500 + [-1]*20)

scaler = StandardScaler()
X_s = scaler.fit_transform(X)

methods = {
    'Isolation Forest': IsolationForest(contamination=0.04, random_state=42),
    'One-Class SVM':    OneClassSVM(nu=0.04, kernel='rbf', gamma='scale'),
    'LOF':             LocalOutlierFactor(contamination=0.04),
}

for name, model in methods.items():
    preds = model.fit_predict(X_s)
    correct = (preds == true_labels).sum()
    print(f"{name:20s}  Accuracy: {correct/len(X):.3f}")
```

---

## 7. Choosing the right method

| Method | Best for | Limitation |
|--------|----------|-----------|
| **Z-score / IQR** | Single feature, quick check | Only works for simple univariate data |
| **Isolation Forest** | General purpose, large datasets, many features | Needs `contamination` estimate |
| **One-Class SVM** | When normal data has a clear boundary | Slow on large datasets, needs scaling |
| **LOF** | Local density differences | Slow on very large datasets |
| **Autoencoder** | Complex patterns, image/text data | Needs deep learning setup |

---

## 8. The contamination parameter

Most sklearn anomaly detectors need `contamination` — your estimate of what fraction of the data is anomalous.

If you have no idea: start with `0.01` to `0.05` (1–5%). Tune using:
- Domain knowledge ("we know about 2% of transactions are fraudulent")
- Validation on labelled anomaly examples if you have them

```python
# If you have some labelled anomalies, evaluate precision/recall
from sklearn.metrics import classification_report

# Convert sklearn's 1/-1 to 1/0 for classification report
y_true = (true_labels == -1).astype(int)
y_pred = (preds == -1).astype(int)
print(classification_report(y_true, y_pred, target_names=['normal', 'anomaly']))
```

---

## 9. Real-world applications

| Domain | What is "normal" | What is anomalous |
|--------|-----------------|------------------|
| **Credit card fraud** | Typical spending patterns | Large amounts, unusual locations, odd hours |
| **Network security** | Normal traffic patterns | Port scans, DDoS, unusual data volumes |
| **Manufacturing** | Sensor readings from working machines | Readings from a machine about to fail |
| **Healthcare** | Typical patient vital signs | Readings indicating a medical event |
| **E-commerce** | Normal user browsing behaviour | Bot traffic, account takeover attempts |

---

## Summary

- Anomaly detection finds data points that don't fit the pattern of normal data.
- **Z-score and IQR** are simple statistical methods for single-feature data.
- **Isolation Forest** is the go-to algorithm — fast, scalable, works on many features.
- **One-Class SVM** learns a tight boundary around normal data.
- **LOF** compares local densities to find locally unusual points.
- All methods need a `contamination` estimate — how many anomalies you expect.
- In most real applications anomalies are rare (< 5%), so focus on **recall** (catching real anomalies) over accuracy.
