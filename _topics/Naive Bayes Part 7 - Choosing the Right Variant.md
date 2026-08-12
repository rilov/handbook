---
title: "Naive Bayes Part 7: Choosing the Right Variant"
category: Advanced Machine Learning
order: 11
permalink: /topics/naive-bayes-choosing-the-right-variant/
tags:
  - machine-learning
  - naive-bayes
  - gaussian
  - multinomial
  - bernoulli
  - model-selection
summary: "Part 7 of the Naive Bayes series: compare Gaussian, Multinomial, and Bernoulli Naive Bayes on the same spam dataset, and learn why the best variant depends on how the feature distribution aligns with each model's assumption."
date: 2026-08-11
---

# Naive Bayes Part 7: Choosing the Right Variant

> Part 7 of the Naive Bayes series. We run all three variants — Gaussian, Multinomial, and Bernoulli — on the same spam dataset and discover that the winner depends entirely on how the features are represented.

---

## 1. Three variants, one decision

You now know all three Naive Bayes variants:

| Variant | Feature type | Distribution assumption |
|---|---|---|
| **Gaussian NB** | Continuous numbers | Each feature is normally distributed per class |
| **Multinomial NB** | Counts / frequencies | Word counts follow a multinomial distribution |
| **Bernoulli NB** | Binary present/absent | Each feature is a Bernoulli (yes/no) trial |

Selecting the correct variant is critical for performance. The rest of this topic is one experiment that makes this concrete: the **same spam dataset, three feature representations, three very different results**.

---

## 2. The experiment setup

We use a spam-like dataset with 4,601 samples and 57 word-frequency features. Like real spam data, the features are **zero-inflated and skewed**: most word frequencies are exactly 0 (the word does not appear), and when a word does appear, its frequency is noisy. The class signal lives mostly in *which* words appear, not *how often*.

```python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB

# Zero-inflated, skewed word-frequency features (spam-like)
rng = np.random.default_rng(42)
n_samples, n_features = 4601, 57
y = (rng.random(n_samples) < 0.4).astype(int)  # ~40% spam

p_ham = rng.uniform(0.05, 0.45, n_features)
p_spam = np.clip(
    p_ham + rng.uniform(0.1, 0.4, n_features) * rng.choice([-1, 1], n_features),
    0.02, 0.95
)

presence_prob = np.where(y[:, None] == 1, p_spam, p_ham)
present = (rng.random((n_samples, n_features)) < presence_prob).astype(float)
magnitude = rng.exponential(0.35, (n_samples, n_features))  # small percentages, mostly < 0.5
X = present * magnitude

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
```

---

## 3. Gaussian NB on the raw continuous features

```python
gnb = GaussianNB()
gnb.fit(X_train, y_train)
acc_g = accuracy_score(y_test, gnb.predict(X_test))
print("GaussianNB accuracy:", round(acc_g, 4))   # 0.8327
print(classification_report(y_test, gnb.predict(X_test), target_names=["ham", "spam"]))
```

Verified result: **83.3% accuracy**, with this classification report:

```
              precision    recall  f1-score
         ham       0.93      0.77      0.84
        spam       0.75      0.92      0.82
```

Note the pattern: ham has **high precision but lower recall**, while spam has **lower precision but very high recall**. Gaussian NB is good at catching spam but sometimes flags ham as spam — a common trade-off in spam filtering.

Why isn't it better? Gaussian NB assumes each feature follows a bell curve within each class. Zero-inflated, skewed frequencies are nothing like a bell curve, so the model's assumption is badly violated.

---

## 4. Multinomial NB on rounded counts

Multinomial NB needs non-negative counts, so we round the continuous frequencies to integers:

```python
X_train_counts = np.round(X_train).astype(int)
X_test_counts = np.round(X_test).astype(int)

mnb = MultinomialNB()
mnb.fit(X_train_counts, y_train)
acc_m = accuracy_score(y_test, mnb.predict(X_test_counts))
print("MultinomialNB accuracy:", round(acc_m, 4))   # 0.8161
```

Verified result: **81.6% accuracy** — the worst of the three. This performance drop is expected: the original features are continuous percentages, and most of them are below 0.5, so **rounding to integers collapses them to 0** — destroying the very presence information that carries the class signal. Rounding and integer conversion lose valuable information.

This does not mean Multinomial NB is a weak algorithm. It demonstrates how to prepare data for it — and with **genuine raw word counts** from a text corpus, Multinomial NB would be operating exactly in its comfort zone and typically performs excellently.

---

## 5. Bernoulli NB on binarized features

Bernoulli NB wants pure presence/absence. We binarize with the rule *present if the value is greater than 0*:

```python
X_train_bin = (X_train > 0).astype(int)
X_test_bin = (X_test > 0).astype(int)

bnb = BernoulliNB()
bnb.fit(X_train_bin, y_train)
acc_b = accuracy_score(y_test, bnb.predict(X_test_bin))
print("BernoulliNB accuracy:", round(acc_b, 4))   # 0.9848
```

Verified result: **98.5% accuracy** — surprisingly, the highest of all three, with strong precision and recall for both classes.

This is a striking outcome: throwing away all the magnitude information and keeping only *does the word appear at all* produced the **best** classifier. For this dataset, presence or absence of certain words is a more powerful spam indicator than their exact frequencies.

---

## 6. The comparison table and the crucial insight

| Model | Feature representation | Accuracy |
|---|---|---|
| **Bernoulli NB** | **binary presence/absence** | **98.5%** |
| Gaussian NB | raw continuous values | 83.3% |
| Multinomial NB | rounded integer counts | 81.6% |

The ranking is: **Bernoulli first, Gaussian second, Multinomial last** — the same ordering observed on the real Spambase dataset.

> **The crucial insight:** the best variant depends on how the feature distribution aligns with the model's assumption — **not** on which algorithm is "better."

Bernoulli won *here* because this dataset's signal lives in word presence. On a different dataset the ranking can flip completely:

- Truly normal continuous measurements (heights, sensor readings) → **Gaussian NB** shines.
- Genuine word counts from a text corpus, where repetition matters → **Multinomial NB** shines.
- Binary indicators or short binarized text → **Bernoulli NB** shines.

There is no universally best variant. Match the model's distribution assumption to your data.

---

## 7. A quick decision guide

```
What type are your features?
│
├── Continuous numbers (height, temperature, measurements)
│     └── Gaussian NB   (assumes normal distribution per class)
│
├── Counts / frequencies (word counts, event counts)
│     └── Multinomial NB   (assumes multinomial distribution)
│
└── Binary yes/no (word present, symptom present)
      └── Bernoulli NB   (assumes Bernoulli distribution)
```

When in doubt — especially with text data — try both Multinomial (on counts) and Bernoulli (on binarized features) and compare with cross-validation. The experiment above shows the difference can be large.

---

## 8. Practice questions

1. Why did Multinomial NB perform worst on this spam-like dataset despite being the standard choice for text?
2. Why did binarizing the features (losing all magnitude information) *improve* accuracy?
3. Your dataset has genuine word counts from long documents. Which variant would you try first, and why?
4. What is the single most important principle when choosing a Naive Bayes variant?

**Answers:**

1. The features were continuous percentages, not raw counts. Rounding them to integers collapsed most values (below 0.5) to 0, destroying the presence signal. Multinomial NB shines on genuine word counts, not on force-converted continuous data.
2. Because the class signal in this data lives in *which* words appear, not how often. Binarizing matched the data to Bernoulli NB's assumption exactly, and Bernoulli also uses absent words as evidence.
3. Multinomial NB — genuine counts from long documents match the multinomial distribution assumption, and word repetition carries real signal in longer texts.
4. Match the feature distribution to the model's assumption. The winner is determined by alignment between data and assumption, not by any inherent superiority of one algorithm.

---

## 9. Summary

- The three variants make different distribution assumptions: Gaussian (normal), Multinomial (counts), Bernoulli (binary).
- On the same spam-like dataset: **Bernoulli 98.5% > Gaussian 83.3% > Multinomial 81.6%**.
- Bernoulli won because the signal was in word presence/absence — its assumption matched the data.
- Multinomial lost because rounding continuous percentages to integers destroyed information — it needs genuine counts.
- No variant is universally best; the right choice depends on your dataset's feature type and distribution.
- When unsure with text data, benchmark Multinomial vs Bernoulli with cross-validation.

**Series recap:** intuition (Part 1) → Bayes' theorem (Part 2) → the classifier (Part 3) → Gaussian (Part 4) → Multinomial (Part 5) → Bernoulli (Part 6) → choosing between them (Part 7, this topic).
