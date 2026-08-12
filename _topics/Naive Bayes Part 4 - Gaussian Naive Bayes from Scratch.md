---
title: "Naive Bayes Part 4: Gaussian Naive Bayes from Scratch"
category: Advanced Machine Learning
order: 8
permalink: /topics/naive-bayes-gaussian-from-scratch/
tags:
  - machine-learning
  - naive-bayes
  - gaussian
  - classification
  - python
summary: "Part 4 of the Naive Bayes series: build a Gaussian Naive Bayes classifier from scratch, compare it to scikit-learn, and interpret priors, likelihoods, and posteriors."
date: 2026-08-11
---

# Naive Bayes Part 4: Gaussian Naive Bayes from Scratch

> Part 4 of the Naive Bayes series. We implement Gaussian Naive Bayes from first principles, compare it to scikit-learn, and inspect how each feature contributes to the final decision.

---

## 1. When features are continuous, use Gaussian Naive Bayes

So far we have talked about discrete features like word counts. But many real datasets contain continuous numerical measurements — for example, the percentage of times a particular word appears in an email, the length of a message, or sensor readings.

**Gaussian Naive Bayes** assumes each continuous feature follows a bell curve (a normal distribution) inside each class. The model learns two numbers per feature per class:

- the **mean** `μ` — the center of the bell curve
- the **variance** `σ²` — how spread out the values are

Then, for a new sample, it asks: "How likely is this feature value under the class's bell curve?"

---

## 2. The Gaussian probability density function

The likelihood of a continuous value `x` under a Gaussian with mean `μ` and variance `σ²` is:

```
                1                (x - μ)²
P(x | μ, σ²) = ──────── × exp(- ───────────)
               √(2πσ²)              2σ²
```

In practice, we almost always work in **log-space** to avoid multiplying tiny numbers:

```
log P(x | μ, σ²) = -0.5 log(2πσ²) - (x - μ)² / (2σ²)
```

This is the building block of Gaussian Naive Bayes.

> **Important: this is a density, not a probability.** The Gaussian PDF gives a probability *density*, not an actual class probability. For continuous variables, the probability of any exact value is technically zero — what matters is which class's distribution gives a **higher density** at the observed value. Gaussian Naive Bayes chooses the class whose distribution assigns the higher density to the sample. You can also think of the exponent term as a **z-score**: `(x - μ) / σ` measures how many standard deviations the value is from the class mean — values close to the class mean get high density, values far away get low density.

---

## 3. A worked example by hand: male or female?

Before writing any code, let's do one full prediction by hand. We have 8 training samples with three continuous features: height (feet), weight (lbs), and foot size (inches).

| Height | Weight | Foot size | Class |
|---|---|---|---|
| 6.00 | 180 | 12 | male |
| 5.92 | 190 | 11 | male |
| 5.58 | 170 | 12 | male |
| 5.92 | 165 | 10 | male |
| 5.00 | 100 | 6 | female |
| 5.50 | 150 | 8 | female |
| 5.42 | 130 | 7 | female |
| 5.75 | 150 | 9 | female |

**New unseen sample:** height = 6.00, weight = 130, foot size = 8. Male or female?

**Step 1 — Priors.** 4 males and 4 females out of 8 samples:

```
P(male)   = 4/8 = 0.5
P(female) = 4/8 = 0.5
```

**Step 2 — Class-wise mean and variance for each feature.**

| | Height mean/var | Weight mean/var | Foot mean/var |
|---|---|---|---|
| male | 5.855 / 0.0350 | 176.25 / 122.92 | 11.25 / 0.9167 |
| female | 5.4175 / 0.0972 | 132.5 / 558.33 | 7.5 / 1.6667 |

**Step 3 — Gaussian likelihood of each feature value under each class.** Plug each value into the Gaussian PDF with that class's mean and variance:

```
P(height=6.00 | male)   ≈ 1.5789     P(height=6.00 | female) ≈ 0.2235
P(weight=130  | male)   ≈ 5.99e-06   P(weight=130  | female) ≈ 0.0168
P(foot=8      | male)   ≈ 0.0013     P(foot=8      | female) ≈ 0.2867
```

(Note: a density can exceed 1 — like 1.5789 for height — because it is a density, not a probability.)

**Step 4 — Posteriors (prior × product of likelihoods).**

```
posterior(male)   = 0.5 × 1.5789 × 5.99e-06 × 0.0013 ≈ 6.2e-09
posterior(female) = 0.5 × 0.2235 × 0.0168 × 0.2867  ≈ 5.4e-04
```

**Step 5 — argmax.** `posterior(female)` is about 100,000× larger than `posterior(male)`, so the **predicted class is female**. Even though the height (6.00) looks male, the weight (130) and foot size (8) are far more typical of the female class, and their likelihoods dominate the product.

---

## 4. Custom implementation from scratch

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.naive_bayes import GaussianNB

class CustomGaussianNB:
    def __init__(self, var_smoothing=1e-9):
        self.var_smoothing = var_smoothing
        self.classes_ = None
        self.priors_ = {}
        self.means_ = {}
        self.variances_ = {}

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        for c in self.classes_:
            X_c = X[y == c]
            self.priors_[c] = len(X_c) / len(X)
            self.means_[c] = X_c.mean(axis=0)
            self.variances_[c] = X_c.var(axis=0) + self.var_smoothing
        return self

    def _log_gaussian_pdf(self, x, mean, var):
        return -0.5 * np.log(2 * np.pi * var) - 0.5 * ((x - mean) ** 2) / var

    def predict_log_proba(self, X):
        log_probs = np.zeros((X.shape[0], len(self.classes_)))
        for i, c in enumerate(self.classes_):
            log_likelihood = np.sum(
                self._log_gaussian_pdf(X, self.means_[c], self.variances_[c]),
                axis=1
            )
            log_probs[:, i] = np.log(self.priors_[c]) + log_likelihood
        return log_probs

    def predict(self, X):
        log_probs = self.predict_log_proba(X)
        return self.classes_[np.argmax(log_probs, axis=1)]

    def predict_proba(self, X):
        log_probs = self.predict_log_proba(X)
        log_probs -= np.max(log_probs, axis=1, keepdims=True)
        probs = np.exp(log_probs)
        probs /= np.sum(probs, axis=1, keepdims=True)
        return probs
```

### What each part does

- **`fit`**: separates the training data by class, then computes the prior, mean, and variance for each class.
- **`var_smoothing`**: adds a tiny value to every variance to prevent division by zero when a feature has zero variance in a class.
- **`_log_gaussian_pdf`**: computes the log-likelihood of a feature value under the learned Gaussian.
- **`predict_log_proba`**: applies the Naive Bayes assumption — sums the log-likelihoods across all features and adds the log-prior.
- **`predict`**: returns the class with the highest log-score (the `argmax` decision rule).
- **`predict_proba`**: converts log-scores back to proper probabilities that sum to 1.

---

## 5. Training and evaluating on a continuous spam-like dataset

```python
# Generate a continuous dataset resembling the classic Spambase dataset
X, y = make_classification(
    n_samples=4601, n_features=57, n_informative=40, n_redundant=0,
    n_clusters_per_class=1, class_sep=1.2, flip_y=0.03, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Custom model
custom_model = CustomGaussianNB(var_smoothing=1e-9)
custom_model.fit(X_train, y_train)
custom_pred = custom_model.predict(X_test)

print("Custom GaussianNB accuracy:", accuracy_score(y_test, custom_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, custom_pred))
print(classification_report(y_test, custom_pred, target_names=["ham", "spam"]))

# Scikit-learn model
sk_model = GaussianNB(var_smoothing=1e-9)
sk_model.fit(X_train, y_train)
sk_pred = sk_model.predict(X_test)

print("Scikit-learn GaussianNB accuracy:", accuracy_score(y_test, sk_pred))
print("Disagreement count:", np.sum(custom_pred != sk_pred))
```

Running this gives accuracy of **94.06%** for both models, with **zero disagreements** between the custom implementation and scikit-learn. That confirms the custom implementation matches the library's behavior exactly.

---

## 6. Interpreting one sample

```python
sample_idx = 0
sample = X_test[sample_idx].reshape(1, -1)
true_label = y_test[sample_idx]
log_post = custom_model.predict_log_proba(sample)[0]
probs = custom_model.predict_proba(sample)[0]

print(f"Sample {sample_idx}: true label={true_label}")
for i, c in enumerate(custom_model.classes_):
    print(f"  class {c}: log-posterior={log_post[i]:.4f}, probability={probs[i]:.4f}")
print("Predicted:", custom_model.predict(sample)[0])
```

Verified output for the first test sample (true label = ham):

```
Sample 0: true label=0
  class 0: log-posterior=-134.7445, probability=0.9604
  class 1: log-posterior=-137.9327, probability=0.0396
Predicted: 0
```

The log-posterior for class 0 is less negative than for class 1, so the model predicts ham with 96% confidence. Note that the raw log-posteriors are *unnormalized* — `predict_proba` normalizes them (via a softmax-style exponentiation) so they sum to 1.

---

## 7. Which features matter most?

We can inspect the most discriminative features by looking at how much each feature's log-likelihood differs between the two classes:

```python
# Log-likelihood contribution of each feature for this sample
feature_ll_ham = custom_model._log_gaussian_pdf(
    sample, custom_model.means_[0], custom_model.variances_[0]
)[0]
feature_ll_spam = custom_model._log_gaussian_pdf(
    sample, custom_model.means_[1], custom_model.variances_[1]
)[0]

diff = feature_ll_spam - feature_ll_ham

# Top 10 features pushing toward spam (positive diff) or ham (negative diff)
top_indices = np.argsort(np.abs(diff))[-10:]
for idx in reversed(top_indices):
    direction = "spam" if diff[idx] > 0 else "ham"
    print(f"Feature {idx}: diff={diff[idx]:.4f} → pushes toward {direction}")
```

A large positive difference means the feature's value is much more likely under the spam class; a large negative difference means it is much more likely under ham. This is exactly how Naive Bayes arrives at its final classification: each feature contributes a small log-likelihood, and the sum determines the winner.

---

## 8. Practice questions

1. Why does Gaussian Naive Bayes need to learn a mean and variance for every feature in every class?
2. What is `var_smoothing` for, and what happens if you set it to 0?
3. Why do we sum log-likelihoods instead of multiplying raw probabilities?
4. How can you tell which features are most responsible for a particular prediction?

**Answers:**

1. Because the Gaussian assumption says each feature follows a bell curve inside each class. The mean and variance define that bell curve, which is needed to compute the likelihood of any new feature value.
2. It adds a tiny value to every variance to prevent division by zero. Without it, if a feature has zero variance in a class (all values identical), the likelihood formula divides by zero.
3. Multiplying many small probabilities causes numerical underflow. Log-space turns the product into a sum, which is numerically stable and gives the same class ranking.
4. Compare the per-feature log-likelihoods under each class. The features with the largest absolute difference between classes are the most discriminative.

---

## 9. Summary

- Gaussian Naive Bayes is used when features are continuous (height, weight, temperature, measurements).
- It assumes each feature follows a normal distribution within each class.
- The Gaussian PDF gives a density, not a probability — the class with the higher density at the observed value wins.
- The model learns a mean and variance per feature per class.
- Prediction is done in log-space to avoid underflow.
- A custom implementation can closely match scikit-learn's `GaussianNB`.
- Per-feature log-likelihood differences reveal which features drive the decision.

**Next topic:** [Multinomial Naive Bayes]({{ site.baseurl }}/topics/naive-bayes-multinomial)
