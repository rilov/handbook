---
title: "Advanced Machine Learning: One-Liners"
category: Advanced Machine Learning
order: 1
permalink: /topics/advanced-machine-learning-one-liners/
tags:
  - machine-learning
  - one-liners
  - formulas
  - reference
summary: "Every key formula and concept in the Advanced Machine Learning module, reduced to one easy-to-scan line."
date: 2026-08-16
---

# Advanced Machine Learning: One-Liners

One concept, one line. Use this as a quick memory jog before an exam, an interview, or when you are trying to remember why something works.

---

## Core ideas

- **Bias:** your model is too simple and keeps missing the real pattern.
- **Variance:** your model is too complex and memorises the training noise.
- **Overfitting:** the model does great on training data but fails on new data.
- **Underfitting:** the model is too simple to capture the real pattern.
- **Support vectors:** the few training points that actually define the SVM boundary.
- **Parametric:** the model assumes a fixed mathematical shape (e.g. line, bell curve).
- **Non-parametric:** the model lets the data decide the shape (e.g. tree, nearest neighbours).

---

## Probability and Naive Bayes

- **Bayes' Theorem:** `P(class | data) = P(data | class) * P(class) / P(data)` — flip the question from "what does the data look like for this class?" to "which class is most likely given the data?".
- **Naive Bayes rule:** `predicted class = argmax P(class) * product of P(feature | class)` — pick the class whose features look most like the new sample.
- **Conditional independence assumption:** `P(x1, x2, ..., xn | class) = P(x1 | class) * P(x2 | class) * ... * P(xn | class)` — assume every feature is independent, which makes the math possible.
- **Log-space trick:** `log(P) + log(Q) = log(P * Q)` — add logs instead of multiplying tiny probabilities, so computers do not round to zero.
- **Laplace smoothing:** `(count + 1) / (total + number of categories)` — never let a never-seen word give zero probability.
- **Gaussian PDF:** `(1 / sqrt(2 * pi * sigma^2)) * exp(-(x - mu)^2 / (2 * sigma^2))` — the bell curve used for continuous features.
- **Multinomial likelihood for one word:** `P(word | class)^count` — the probability of a word raised to how many times it appears.
- **Bernoulli likelihood for one feature:** `P(feature | class)^x * (1 - P(feature | class))^(1 - x)` — one probability if the feature is present, another if it is absent.

---

## Support Vector Machines

- **Hyperplane equation:** `w · x + b = 0` — the flat decision surface that splits the data.
- **SVM decision rule:** `y = +1 if w · x + b > 0, else -1` — which side of the boundary is the point on?
- **Margin width:** `2 / ||w||` — the width of the empty "road" between the two classes.
- **SVM objective (soft margin):** `minimise (1/2) * ||w||^2 + C * sum(slack_i)` — keep the margin wide while punishing points on the wrong side.
- **Cost C:** a large `C` means "do not allow mistakes" (low bias, high variance); a small `C` means "allow some mistakes for a simpler boundary" (high bias, low variance).
- **Kernel trick:** `K(x, x') = phi(x) · phi(x')` — compute in high-dimensional space without ever building that space.
- **RBF kernel:** `K(x, x') = exp(-gamma * ||x - x'||^2)` — a flexible similarity measure based on distance between points.
- **Gamma:** a large `gamma` means each point has local influence (wiggly boundary); a small `gamma` means each point has global influence (smoother boundary).

---

## Distance and geometry

- **Dot product:** `a · b = sum(a_i * b_i)` — a measure of how much two vectors point in the same direction.
- **Euclidean distance:** `sqrt(sum((a_i - b_i)^2))` — the straight-line distance between two points.
- **L2 norm of a vector:** `||w|| = sqrt(sum(w_i^2))` — the length of the weight vector that defines the SVM margin.

---

## Practical rules

- **Naive Bayes for text:** use Bernoulli when presence matters, Multinomial when counts matter, Gaussian when the feature is a continuous number.
- **SVM kernel choice:** start with linear; use RBF when the boundary is curved; use polynomial for known curved relationships.
- **High C vs high gamma:** both make the SVM more flexible and more likely to overfit.
- **Smoother simpler model:** lower C, lower gamma, wider epsilon tube, smaller tree depth, fewer neighbours in KNN.
