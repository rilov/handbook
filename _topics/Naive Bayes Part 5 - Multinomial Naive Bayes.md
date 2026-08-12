---
title: "Naive Bayes Part 5: Multinomial Naive Bayes"
category: Advanced Machine Learning
order: 9
permalink: /topics/naive-bayes-multinomial/
tags:
  - machine-learning
  - naive-bayes
  - multinomial
  - text-classification
  - laplace-smoothing
summary: "Part 5 of the Naive Bayes series: the Multinomial variant for count data, the multinomial likelihood formula, Laplace smoothing, and a fully worked spam example."
date: 2026-08-11
---

# Naive Bayes Part 5: Multinomial Naive Bayes

> Part 5 of the Naive Bayes series. Multinomial Naive Bayes is the standard variant for count data — most famously, word counts in text classification.

---

## 1. The three variants of Naive Bayes

The Naive Bayes family has different variants based on the **type of features**:

| Variant | Feature type | Example |
|---|---|---|
| **Multinomial NB** | Counts / frequencies | Number of times a word appears in a document |
| **Bernoulli NB** | Binary (present/absent) | Whether a word appears at all; symptom yes/no |
| **Gaussian NB** | Continuous values | Height, weight, temperature |

This topic covers Multinomial NB. Bernoulli NB is covered in [Part 6]({{ site.baseurl }}/topics/naive-bayes-bernoulli), and Gaussian NB was covered in [Part 4]({{ site.baseurl }}/topics/naive-bayes-gaussian-from-scratch).

---

## 2. The multinomial likelihood

Multinomial NB models word counts using the probability mass function of the multinomial distribution. For a document with word counts `x1, x2, ..., xn`:

```
                    N!
P(X | C) = ──────────────────── × ∏ P(wi | C)^xi
           x1! × x2! × ... × xn!   i
```

where:

- `N` is the total number of words in the document
- `xi` is the count of word `i`
- `P(wi | C)` is the probability of word `i` appearing in class `C`

For **classification**, the factorial term is a constant that does not depend on the class, so we drop it:

```
P(X | C) ∝ ∏ P(wi | C)^xi
```

The posterior becomes:

```
P(C | X) ∝ P(C) × ∏ P(wi | C)^xi
```

Each word's class probability is raised to the power of how many times the word appears.

---

## 3. Laplace smoothing

Word probabilities are estimated from training counts:

```
                 count of word w in class C + 1
P(w | C) = ───────────────────────────────────────
           total words in class C + vocabulary size
```

The `+1` in the numerator and `+ V` in the denominator is **Laplace smoothing**. Without it, a word that never appeared in a class's training data would have probability exactly 0 — and since the score is a product, one zero would wipe out all the other evidence and pull the entire score to zero. Smoothing guarantees every word has a small non-zero probability.

---

## 4. Fully worked example: spam detection

### Training data

| Message | Text | Class |
|---|---|---|
| M1 | "buy limited items" | spam |
| M2 | "special offer sale" | spam |
| M3 | "let us meet tomorrow" | not spam |
| M4 | "see you" | not spam |

**New incoming email:** "buy items buy items" — spam or not spam?

### Step 1 — Vocabulary

All unique words across training data: buy, limited, items, special, offer, sale, let, us, meet, tomorrow, see, you.

```
Vocabulary size V = 12
```

Total words in spam messages = 6 (buy, limited, items, special, offer, sale).
Total words in not-spam messages = 6 (let, us, meet, tomorrow, see, you).

### Step 2 — Priors

```
P(spam)     = 2/4 = 0.5
P(not spam) = 2/4 = 0.5
```

### Step 3 — Word probabilities with Laplace smoothing

For spam (word count + 1, divided by total words in class + V):

```
P("buy"   | spam) = (1 + 1) / (6 + 12) = 2/18
P("items" | spam) = (1 + 1) / (6 + 12) = 2/18
```

For not spam ("buy" and "items" never appear in not-spam messages):

```
P("buy"   | not spam) = (0 + 1) / (6 + 12) = 1/18
P("items" | not spam) = (0 + 1) / (6 + 12) = 1/18
```

Notice how smoothing saved us: without the `+1`, both not-spam probabilities would be `0/18 = 0` and the entire not-spam score would collapse to zero.

### Step 4 — Posteriors

The new email "buy items buy items" has counts: buy = 2, items = 2. Each word's probability is raised to its count:

```
posterior(spam)     ∝ 0.5 × (2/18)² × (2/18)² = 0.5 × (2/18)⁴ ≈ 7.6 × 10⁻⁵

posterior(not spam) ∝ 0.5 × (1/18)² × (1/18)² = 0.5 × (1/18)⁴ ≈ 4.8 × 10⁻⁶
```

### Step 5 — Decision

```
posterior(spam) > posterior(not spam)
```

The predicted class is **spam** — the score for spam is about 16× larger.

---

## 5. Python verification

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

messages = [
    "buy limited items",
    "special offer sale",
    "let us meet tomorrow",
    "see you",
]
labels = [1, 1, 0, 0]  # 1 = spam, 0 = not spam

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(messages)

model = MultinomialNB(alpha=1.0)  # alpha=1.0 is Laplace smoothing
model.fit(X, labels)

new_email = vectorizer.transform(["buy items buy items"])
print(model.predict(new_email))        # [1] → spam
print(model.predict_proba(new_email))  # spam probability dominates
```

`alpha=1.0` (the default) is exactly the Laplace smoothing from the hand calculation.

---

## 6. When to use Multinomial NB

**Good fit:**
- Text classification with word counts or TF-IDF (spam filtering, topic labeling, sentiment)
- Any feature vector of non-negative counts or frequencies
- Large vocabularies — it scales effortlessly

**Not a fit:**
- Continuous measurements → use Gaussian NB
- Pure presence/absence features → Bernoulli NB is often a better model
- Negative feature values → Multinomial NB requires non-negative input

---

## 7. Practice questions

1. Why can we drop the factorial term from the multinomial likelihood during classification?
2. In the worked example, what would happen without Laplace smoothing?
3. Why is each word's probability raised to the power of its count?
4. What does the `alpha` parameter of `MultinomialNB` control?

**Answers:**

1. The factorial term depends only on the word counts of the document, not on the class. It scales every class score equally, so it does not affect which class wins.
2. `P("buy" | not spam)` and `P("items" | not spam)` would be 0, making the entire not-spam score 0 regardless of any other evidence. Smoothing keeps every probability non-zero.
3. Because the multinomial model treats each occurrence of a word as independent evidence. A word appearing twice contributes its probability twice — i.e. squared.
4. The smoothing strength. `alpha=1.0` is Laplace (add-one) smoothing; smaller values smooth less, larger values smooth more.

---

## 8. Summary

- Multinomial NB is used when features are **counts or frequencies**, most commonly word counts.
- Likelihood: `P(X | C) ∝ ∏ P(wi | C)^xi` — each word's probability raised to its count.
- Word probabilities use **Laplace smoothing** to avoid zero probabilities.
- The worked example shows "buy items buy items" scored ≈ 7.6e-5 for spam vs ≈ 4.8e-6 for not spam → predicted spam.
- `sklearn.naive_bayes.MultinomialNB` with `alpha=1.0` reproduces the hand calculation.

**Next topic:** [Bernoulli Naive Bayes]({{ site.baseurl }}/topics/naive-bayes-bernoulli)
