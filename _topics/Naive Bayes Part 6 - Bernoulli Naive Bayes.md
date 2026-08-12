---
title: "Naive Bayes Part 6: Bernoulli Naive Bayes"
category: Advanced Machine Learning
order: 10
permalink: /topics/naive-bayes-bernoulli/
tags:
  - machine-learning
  - naive-bayes
  - bernoulli
  - binary-features
  - classification
summary: "Part 6 of the Naive Bayes series: the Bernoulli variant for binary yes/no features, its likelihood formula, and a fully worked mammal vs non-mammal example."
date: 2026-08-11
---

# Naive Bayes Part 6: Bernoulli Naive Bayes

> Part 6 of the Naive Bayes series. Bernoulli Naive Bayes handles binary features — each attribute is either present (1) or absent (0) — and predicts the class based on how likely that combination of yes/no attributes is under each class.

---

## 1. When features are binary

Many datasets have features that are purely yes/no:

- Does this word appear in the email at all? (present/absent, ignoring the count)
- Does the patient have this symptom? (yes/no)
- Does this animal give birth? Can it fly? (yes/no)

For these, **Bernoulli Naive Bayes** is the natural variant. It is built on the Bernoulli distribution — the distribution of a single yes/no trial.

---

## 2. The Bernoulli likelihood

For binary features `xi ∈ {0, 1}`, the likelihood of feature `i` given class `C` is:

```
P(xi | C) = pᵢ^xi × (1 - pᵢ)^(1-xi)
```

where `pᵢ = P(feature i is present | C)`.

This compact formula covers both cases:

- If `xi = 1` (present): the term becomes `pᵢ` — the probability that feature `i` appears in class `C`.
- If `xi = 0` (absent): the term becomes `1 - pᵢ` — the probability that feature `i` does **not** appear in class `C`.

The full posterior follows the usual Naive Bayes pattern:

```
P(C | X) ∝ P(C) × ∏ pᵢ^xi × (1 - pᵢ)^(1-xi)
                  i
```

**Key difference from Multinomial NB:** Bernoulli NB explicitly penalizes *absent* features through the `(1 - pᵢ)` terms. Multinomial NB only counts what is present; Bernoulli NB also uses what is missing as evidence.

---

## 3. Fully worked example: mammal or non-mammal?

We want to classify animals as **mammal (M)** or **non-mammal (N)** from four binary attributes: gives birth, can fly, lives in water, has legs.

### Training data summary

Out of 20 animals: 7 are mammals and 13 are non-mammals.

Counting attribute occurrences within each class gives these conditional probabilities:

| Attribute (= yes) | P(attr = 1 \| M) | P(attr = 1 \| N) |
|---|---|---|
| gives birth | 6/7 | 1/13 |
| can fly | 1/7 | 3/13 |
| lives in water | 2/7 | 3/13 |
| has legs | 5/7 | 9/13 |

For example, `P(gives birth = 1 | M) = 6/7` means: of the 7 mammals in the training data, 6 give birth.

### The new sample to classify

```
gives birth = yes (1)
can fly = no (0)
lives in water = yes (1)
has legs = no (0)
```

### Step 1 — Priors

```
P(M) = 7/20  = 0.35
P(N) = 13/20 = 0.65
```

### Step 2 — Likelihood for mammal

Apply the Bernoulli formula per feature. Present features use `pᵢ`, absent features use `(1 - pᵢ)`:

```
P(X | M) = P(gb=1|M) × (1 - P(fly=1|M)) × P(water=1|M) × (1 - P(legs=1|M))
         = (6/7) × (1 - 1/7) × (2/7) × (1 - 5/7)
         = 0.857 × 0.857 × 0.286 × 0.286
         ≈ 0.06
```

### Step 3 — Likelihood for non-mammal

```
P(X | N) = P(gb=1|N) × (1 - P(fly=1|N)) × P(water=1|N) × (1 - P(legs=1|N))
         = (1/13) × (1 - 3/13) × (3/13) × (1 - 9/13)
         = 0.077 × 0.769 × 0.231 × 0.308
         ≈ 0.0042
```

### Step 4 — Posteriors (likelihood × prior)

```
posterior(M) = 0.06   × 0.35 ≈ 0.021
posterior(N) = 0.0042 × 0.65 ≈ 0.0027
```

### Step 5 — Decision

```
posterior(M) = 0.021 > posterior(N) = 0.0027
```

The predicted class is **Mammal**. Even though non-mammals are almost twice as common (prior 0.65 vs 0.35), the evidence — especially "gives birth = yes," which is very rare among non-mammals (1/13) — overwhelmingly favors mammal.

---

## 4. Python verification

```python
import numpy as np
from sklearn.naive_bayes import BernoulliNB

# Features: [gives_birth, can_fly, lives_in_water, has_legs]
# A training set matching the probability table above
X = np.array([
    # 7 mammals
    [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 0, 1],
    [1, 1, 0, 1], [1, 0, 1, 1], [0, 0, 0, 0],
    # 13 non-mammals
    [1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 0],
    [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1],
    [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0],
    [0, 0, 0, 0],
])
y = np.array([1]*7 + [0]*13)  # 1 = mammal, 0 = non-mammal

model = BernoulliNB(alpha=0)  # no smoothing, to match the hand calculation
model.fit(X, y)

new_animal = np.array([[1, 0, 1, 0]])  # gives birth, doesn't fly, lives in water, no legs
print(model.predict(new_animal))        # [1] → mammal
print(model.predict_proba(new_animal))  # mammal probability dominates
```

In practice you would keep the default `alpha=1.0` (Laplace smoothing) to protect against zero probabilities, just like in Multinomial NB.

---

## 5. Bernoulli vs Multinomial for text

Both variants are used for text, but they model it differently:

| | Multinomial NB | Bernoulli NB |
|---|---|---|
| Feature | word **count** | word **present or absent** |
| "free free free" vs "free" | different (count 3 vs 1) | identical (both present) |
| Absent words | ignored | actively used as evidence via `(1 - pᵢ)` |
| Best for | longer documents | short texts (SMS, tweets, headlines) |

For short texts, word repetition is rare, so presence/absence captures most of the signal — and Bernoulli's use of absent words as evidence often helps.

---

## 6. Practice questions

1. Write the Bernoulli likelihood formula for one feature and explain how it behaves for `xi = 1` vs `xi = 0`.
2. In the mammal example, the non-mammal prior (0.65) was almost double the mammal prior (0.35). Why did the model still predict mammal?
3. What is the main modeling difference between Bernoulli NB and Multinomial NB for text?
4. Why might Bernoulli NB outperform Multinomial NB on very short texts?

**Answers:**

1. `P(xi | C) = pᵢ^xi × (1 - pᵢ)^(1-xi)`. When `xi = 1` it evaluates to `pᵢ` (probability the feature is present in class C); when `xi = 0` it evaluates to `1 - pᵢ` (probability it is absent).
2. The likelihood ratio dominated the prior. `P(X | M) ≈ 0.06` vs `P(X | N) ≈ 0.0042` — a 14× difference in evidence, far larger than the ~2× prior advantage of non-mammals.
3. Multinomial models word counts; Bernoulli models only presence/absence and additionally uses absent words as evidence through the `(1 - pᵢ)` terms.
4. In short texts words rarely repeat, so counts add little information beyond presence. Bernoulli's explicit modeling of absent words provides extra signal that Multinomial ignores.

---

## 7. Summary

- Bernoulli NB is for **binary features** — each attribute is present (1) or absent (0).
- Likelihood per feature: `pᵢ^xi × (1 - pᵢ)^(1-xi)` — present features contribute `pᵢ`, absent features contribute `1 - pᵢ`.
- Posterior: `P(C | X) ∝ P(C) × ∏ pᵢ^xi (1 - pᵢ)^(1-xi)`.
- Worked example: posterior(mammal) ≈ 0.021 vs posterior(non-mammal) ≈ 0.0027 → predicted **mammal**, despite the smaller prior.
- Bernoulli NB uses absent features as evidence, which makes it especially effective on short texts.

**Next topic:** [Choosing the Right Variant]({{ site.baseurl }}/topics/naive-bayes-choosing-the-right-variant) — all three variants compared head-to-head on the same dataset.
