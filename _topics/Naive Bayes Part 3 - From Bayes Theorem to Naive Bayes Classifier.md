---
title: "Naive Bayes Part 3: From Bayes' Theorem to the Naive Bayes Classifier"
category: Advanced Machine Learning
order: 7
permalink: /topics/naive-bayes-from-bayes-theorem-to-classifier/
tags:
  - machine-learning
  - naive-bayes
  - bayes-theorem
  - conditional-independence
  - classification
summary: "Part 3 of the Naive Bayes series: extend Bayes' theorem to multiple features, add the conditional independence assumption, and derive the final Naive Bayes decision rule with argmax."
date: 2026-08-11
---

# Naive Bayes Part 3: From Bayes' Theorem to the Naive Bayes Classifier

> Part 3 of the Naive Bayes series. We extend Bayes' theorem to many features, make the conditional independence assumption, and arrive at the final Naive Bayes decision rule.

---

## 1. Bayes' theorem with a single feature

From Part 2, for one feature `x` and class `C`:

```
             P(x | C) × P(C)
P(C | x) =  ─────────────────
                  P(x)
```

The class with the highest posterior wins. For now, we ignore the denominator because it is the same for every class.

---

## 2. Extending to multiple features

Real samples have many features:

```
X = [x1, x2, ..., xn]
```

Bayes' theorem becomes:

```
             P(x1, x2, ..., xn | C) × P(C)
P(C | X) =  ───────────────────────────────
                     P(x1, x2, ..., xn)
```

The term `P(x1, x2, ..., xn | C)` is the **joint likelihood** — the probability of seeing this exact combination of features, given the class. This is the hard part. With many features, estimating the joint distribution directly is impractical because the feature space is too large and too sparse.

---
## 3. Conditional independence assumption

Naive Bayes assumes that, once the class is known, every feature is independent of the others:

```
P(x1, x2, ..., xn | C) ≈ P(x1 | C) × P(x2 | C) × ... × P(xn | C)
```

In compact product notation:

```
            n
P(X | C) ≈ ∏ P(xi | C)
           i=1
```

This is the core assumption. It says we can estimate each feature's likelihood separately, then multiply them together. Instead of one impossible high-dimensional joint distribution, we have `n` simple one-dimensional distributions.

---

## 4. The Naive Bayes posterior

Substitute the assumption into Bayes' theorem and drop the constant denominator:

```
                  n
P(C | X) ∝ P(C) × ∏ P(xi | C)
                 i=1
```

This is the score Naive Bayes computes for every class. The class with the highest score is the prediction.

---

## 5. The decision rule: argmax

For a sample with features `X`, compute the score for each possible class `C`:

```
score(C) = P(C) × P(x1 | C) × P(x2 | C) × ... × P(xn | C)
```

Then pick the class with the maximum score:

```
ŷ = argmax_C  score(C)
```

`argmax_C` means: "the value of `C` that gives the largest score." If `C` can be `spam` or `not spam`, we compute both scores and choose the larger one.

---

## 6. Numerical underflow — and why log-space is used in practice

### The problem

Naive Bayes multiplies many probabilities:

```
score(C) = P(C) × P(x1 | C) × P(x2 | C) × ... × P(xn | C)
```

Every term is between 0 and 1, so the product **shrinks rapidly** toward zero as more features are multiplied in. With hundreds or thousands of features (like words in a document), the product can reach values like `1e-420` — smaller than what a computer's floating-point numbers can represent. The computer rounds it to exactly **0**.

This is called **numerical underflow**. The model's math is still correct — the issue is purely computational. When it happens, *all* class scores underflow to zero, they all look identical, and the classifier can no longer tell the classes apart.

### The fix: take logarithms

Instead of multiplying probabilities, we take their logarithms and add them. The key identity is `log(a × b) = log(a) + log(b)`, so the product becomes a sum:

```
log score(C) = log P(C) + Σ log P(xi | C)
```

For example, if the individual word likelihoods are small numbers like `0.07`, their logs are moderate negative numbers like `-2.66`. Summing hundreds of values around `-2.66` gives something like `-266` — a perfectly representable number, no underflow.

### Why the logs are negative

A logarithm answers: "to what power must I raise the base to get this number?"

```
log10(100) = 2     because 10² = 100
log10(0.1) = -1    because 10⁻¹ = 0.1
```

Since probabilities are between 0 and 1, their logs are always **negative**. That is fine — we only care about which class's sum is *highest* (least negative).

### Why this doesn't change the answer

The logarithm is a **monotonically increasing** function: if `a > b` then `log(a) > log(b)`. So the class with the highest log-score is exactly the class that would have had the highest raw score. We can safely replace the product with a sum, avoid underflow, and get the same prediction.

---

## 7. A tiny worked example

Training data: 4 emails, each with 3 words.

| Email | Words | Label |
|---|---|---|
| "free prize win" | free, prize, win | spam |
| "free offer claim" | free, offer, claim | spam |
| "meeting tomorrow agenda" | meeting, tomorrow, agenda | not spam |
| "project update tomorrow" | project, update, tomorrow | not spam |

**Priors:**

```
P(spam) = 2/4 = 0.5
P(not spam) = 2/4 = 0.5
```

**Likelihoods with Laplace smoothing (smoothing value = 1):**

Vocabulary size = 8 words (free, prize, win, offer, claim, meeting, tomorrow, agenda, project, update) → actually 10 words. Counting carefully: free, prize, win, offer, claim, meeting, tomorrow, agenda, project, update = 10.

Spam word count = 6. Not spam word count = 6.

```
P("free" | spam) = (2 + 1) / (6 + 10) = 3/16 = 0.1875
P("win"  | spam) = (1 + 1) / (6 + 10) = 2/16 = 0.125
P("tomorrow" | spam) = (0 + 1) / (6 + 10) = 1/16 = 0.0625

P("free" | not spam) = (0 + 1) / (6 + 10) = 1/16 = 0.0625
P("win"  | not spam) = (0 + 1) / (6 + 10) = 1/16 = 0.0625
P("tomorrow" | not spam) = (2 + 1) / (6 + 10) = 3/16 = 0.1875
```

**Classify new email: "free win tomorrow"**

```
score(spam)     ∝ 0.5 × 0.1875 × 0.125 × 0.0625 = 0.000732
score(not spam) ∝ 0.5 × 0.0625 × 0.0625 × 0.1875 = 0.000366
```

`score(spam)` > `score(not spam)`, so the prediction is **spam**. The word "tomorrow" pulls toward not spam, but "free" and "win" pull harder toward spam.

---

## 8. Practice questions

1. Write the Naive Bayes score formula for a sample with `n` features.
2. What problem does working in log-space solve?
3. In the worked example above, why does "free win tomorrow" get classified as spam even though "tomorrow" is more common in not-spam emails?
4. What does `argmax_C` mean in the Naive Bayes decision rule?

**Answers:**

1. `score(C) = P(C) × ∏ P(xi | C)` or, equivalently, `log score(C) = log P(C) + Σ log P(xi | C)`.
2. Multiplying many small probabilities can underflow to zero. Log-space turns products into sums, avoiding this numerical issue.
3. Classification depends on the combined evidence. "free" and "win" are much stronger spam indicators than "tomorrow" is a not-spam indicator, so the product favors spam overall.
4. It means "the class `C` that produces the highest score." We compute the score for every class and pick the winner.

---

## 9. Summary

- Start with Bayes' theorem for many features: `P(C | X) ∝ P(X | C) × P(C)`.
- The joint likelihood `P(X | C)` is hard to estimate directly.
- Naive Bayes assumes conditional independence: `P(X | C) ≈ ∏ P(xi | C)`.
- The classifier becomes: `ŷ = argmax_C P(C) × ∏ P(xi | C)`.
- In practice, use log-space: `log score(C) = log P(C) + Σ log P(xi | C)`.
- Laplace smoothing prevents zero probabilities from destroying the product.

**Next topic:** [Gaussian Naive Bayes from Scratch in Python]({{ site.baseurl }}/topics/naive-bayes-gaussian-from-scratch)
