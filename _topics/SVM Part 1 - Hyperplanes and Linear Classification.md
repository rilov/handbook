---
title: "SVM Part 1: Hyperplanes and Linear Classification"
category: Advanced Machine Learning
order: 2
permalink: /topics/svm-hyperplanes-and-linear-classification/
tags:
  - machine-learning
  - svm
  - support-vector-machines
  - hyperplane
  - linear-classification
  - beginners
  - friendly
summary: "Step one of the SVM series: what a hyperplane is in 2D, 3D, and beyond, and why SVM is considered a linear model. Builds the mathematical foundation needed for margins and kernels in the topics that follow."
date: 2026-08-09
---

# SVM Part 1: Hyperplanes and Linear Classification

> This is Part 1 of the SVM mini-series. If you have not read [Bias and Variance]({{ site.baseurl }}/topics/bias-and-variance) yet, start there first — it explains the tradeoff that SVM's `C` parameter controls, which we'll need in Part 3.

---

## 1. What problem is SVM trying to solve?

A **Support Vector Machine (SVM)** is a classification algorithm — it looks at labeled examples and learns to draw a boundary that separates one class from another.

What makes SVM special is *how it chooses that boundary*, and later, *how it handles data that no straight boundary can separate* (via kernels). We will build up to both ideas slowly. This first topic covers only the boundary itself: the **hyperplane**.

> **Important fact to remember:** SVM is a **linear model**. Just like linear regression or logistic regression, at its core it works with an equation of the form `weight × feature + weight × feature + ... = 0`. Everything else we learn later (margins, kernels) is built on top of this simple linear equation.

---

## 2. Step 1: The hyperplane in 2D

Suppose you want to classify emails as spam or not spam using two features:

- `x1` = word_freq_technology (how often the word "technology" appears)
- `x2` = word_freq_money (how often the word "money" appears)

A **hyperplane** in 2D is just a line that separates the two classes:

```
x2 (word_freq_money)
  │
  │      ● spam           ← above the line
  │    ●
  │  ────────────────       ← the hyperplane (the line itself)
  │        ■  not spam    ← below the line
  │      ■
  └──────────────────────── x1 (word_freq_technology)
```

The standard equation of a line is:

```
a·x + b·y + c = 0
```

We generalize this using weights (`W`) instead of `a, b, c`:

```
W0 + W1·x1 + W2·x2 = 0
```

Here, `x1` and `x2` are the features, and `W1`, `W2` are the coefficients the model learns. `W0` is a constant (the bias/intercept term).

### How the line classifies a point

Take any point `(x1, x2)` and plug it into the left-hand side of the equation:

- If the result is **positive** → the point is on one side (say, spam)
- If the result is **negative** → the point is on the other side (not spam)
- If the result is **exactly zero** → the point sits exactly on the line

This is the entire classification rule for a linear model: **compute a weighted sum, check its sign.**

```python
import numpy as np

# Example hyperplane: 2 - x1 + 3*x2 = 0  →  W0=2, W1=-1, W2=3
def classify_2d(x1, x2, W0=2, W1=-1, W2=3):
    value = W0 + W1 * x1 + W2 * x2
    if value > 0:
        return "spam", value
    elif value < 0:
        return "not spam", value
    else:
        return "on the boundary", value

print(classify_2d(1, 1))   # W0 + (-1)(1) + 3(1) = 2 - 1 + 3 = 4  → spam
print(classify_2d(5, 0))   # 2 - 5 + 0 = -3                       → not spam
```

---

## 3. Step 2: The hyperplane in 3D

Now add a third feature, `x3` (for example, `word_freq_free`). The hyperplane is no longer a line — it becomes a **flat plane** cutting through 3D space:

```
                z (x3)
                │      ● spam (above the plane)
                │   ╱‾‾‾‾‾‾╱
                │ ╱ plane ╱
                │╱_______╱
                │      ■ not spam (below the plane)
                └──────────────── y (x2)
               ╱
              x (x1)
```

The equation generalizes in exactly the same way:

```
a·x + b·y + c·z + d = 0
```

Points above the plane belong to one class; points below belong to the other. The math is unchanged — only the number of dimensions grew from 2 to 3.

---

## 4. Step 3: The hyperplane in d dimensions

Here is the powerful part: this idea keeps working no matter how many features (dimensions) you have. You can't draw a picture of a 20-dimensional hyperplane, but the equation is just a longer sum:

```
        d
        ∑ (Wi · Xi) + W0 = 0
       i=1
```

This is called a **linear discriminator** — a single equation that separates all your data points into two classes, no matter how many features you're using.

```python
import numpy as np

def classify_nd(x, W, W0):
    """
    x  : feature vector, e.g. [x1, x2, ..., xd]
    W  : weight vector,  e.g. [W1, W2, ..., Wd]
    W0 : bias/intercept term
    """
    value = np.dot(W, x) + W0
    return "class A" if value > 0 else "class B", value

# 5-dimensional example
x = np.array([1.2, 0.5, 3.0, 0.0, 2.1])
W = np.array([0.4, -1.1, 0.8, 2.0, -0.5])
W0 = -1.0

print(classify_nd(x, W, W0))
```

The rule never changes: **compute the dot product of weights and features, add the bias, check the sign.**

---

## 5. Step 4: Why "linear" matters

SVM belongs to the same family as **logistic regression** — both are linear models. In logistic regression, the log-odds of an outcome is a linear function of the inputs. In SVM, the hyperplane itself is a linear function of the inputs.

This matters because a purely linear boundary can only separate data that is arranged in a way a straight line (or flat plane) can divide. Some data isn't shaped like that at all:

```
        ●  ●  ●
      ●    ■  ■  ■    ●
        ●  ●  ●
   (■ points are surrounded by ● points — no straight line works)
```

We are not equipped to solve this yet — that requires the **kernel trick**, covered in Part 4. For now, remember: **SVM starts life as a linear model, and every advanced trick we add later is a way of making a linear model work on non-linear data, without abandoning the linear math underneath.**

---

## 6. Step 5: From "a" hyperplane to "the best" hyperplane

Notice something important: for a dataset that is separable by a straight line, there isn't just *one* possible hyperplane — there are infinitely many:

```
      ●  ●  ●
   ╲    ╲     ╲          ← three different valid separating lines
    ╲    ╲     ╲
      ■  ■  ■
```

All three lines above correctly separate the two classes on the training data. So which one should the model choose? This is exactly the question the next topic answers.

---

## 7. Practice questions

1. Write the equation of a hyperplane in 2D using weights `W0`, `W1`, `W2`.
2. A point plugged into a hyperplane equation gives a result of exactly 0. What does that mean?
3. Why is SVM called a "linear model" even though it can eventually create curved decision boundaries (as you'll see in Part 4)?
4. If you have 50 features in your dataset, how many weights (`Wi`) will your hyperplane equation need (not counting `W0`)?

**Answers:**

1. `W0 + W1·x1 + W2·x2 = 0`
2. The point lies exactly on the hyperplane — it is on the boundary between the two classes.
3. Because the core boundary equation is always a linear (weighted sum) function. Curved boundaries come from transforming the *features* first (via kernels), not from changing the linear nature of the boundary equation itself.
4. 50 — one weight per feature, plus the separate `W0` bias term.

---

## 8. Summary

- A **hyperplane** is the boundary an SVM uses to separate classes: a line in 2D, a plane in 3D, and a linear equation in higher dimensions.
- The general form is `∑(Wi · Xi) + W0 = 0`.
- Plugging a point into this equation and checking the **sign** of the result tells you which class it belongs to.
- SVM is fundamentally a **linear model** — just like logistic regression.
- For a separable dataset, many different hyperplanes can work. The next topic explains how SVM picks the *best* one.

**Next topic:** [Maximal Margin Classifier]({{ site.baseurl }}/topics/svm-maximal-margin-classifier) — how SVM chooses the single best hyperplane out of infinitely many options.
