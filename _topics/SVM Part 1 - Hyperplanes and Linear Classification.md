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

## 1.1 Wait — isn't a "line" what linear regression already uses?

If you've seen **linear regression** before (e.g. predicting house price from square footage), you already know a line can be fit through data:

```
price
  │                              ● ●
  │                        ●  ●
  │                  ● ●
  │            ●  ●
  │      ● ●
  │   ●
  └───────────────────────────────── square footage
```

Here, the line is the **prediction itself**. To predict the price of a 1,800 sq. ft. house, you find `x = 1800` on the horizontal axis and read off the `y` value where the line crosses it — that `y` value *is* your predicted price. The line's job is to tell you **where along it** a point should be.

SVM uses the same kind of equation, but gives the line a **completely different job**. In classification, we don't care where a point lands *on* the line — we don't even need it to touch the line at all. Instead, we only care **which side** of the line a point falls on:

```
x2 (word_freq_money)
  │      ● spam            ← this whole region = "spam"
  │    ●
  │  ────────────────       ← the line does not predict a value here —
  │        ■  not spam        it just divides the plane into two halves
  │      ■
  └──────────────────────── x1 (word_freq_technology)
```

So the same equation, `W0 + W1·x1 + W2·x2 = 0`, is doing two very different jobs depending on the problem:

| | Linear regression (house price) | SVM (spam classification) |
|---|---|---|
| What the line represents | The predicted output value itself | A **divider** between two regions |
| What you read off | The `y`-value where the line crosses your `x` | Which **side** of the line your point lands on |
| The number you compute | `W0 + W1·x1` is directly your prediction (e.g. price) | `W0 + W1·x1 + W2·x2` is only used for its **sign** (+/−), not its size |
| Points exactly on the line | Impossible unless the model is a perfect fit | Perfectly normal — that's the undecided boundary case |

This is the key mental shift for this whole topic: **stop thinking of the hyperplane as something whose height you read off, and start thinking of it purely as a wall that splits your feature space into two sides.** Everything from here on builds on that one idea.

> **So can SVM predict house prices too?** Yes — but not the *classification* SVM covered in this series. There's a sibling algorithm, **Support Vector Regression (SVR)**, that puts the hyperplane back to work as a value predictor (like the house-price line above), while still reusing the margin/slack/`C`/kernel machinery from this series. In scikit-learn it's `sklearn.svm.SVR` instead of `SVC`. This series focuses on classification (`SVC`); SVR is a different topic built on the same foundation.

---

## 1.5 The simplest possible version: one feature

Before jumping into lines and planes, consider the simplest case: **one single feature**, like an exam score. Suppose "pass" is `score ≥ 50`. You can write this as a rule:

```
score - 50 ≥ 0   →  pass
score - 50 < 0   →  fail
```

This is already a "hyperplane" — just in 1D, it's a single **point** (`score = 50`) that splits the number line into two sides:

```
fail  ────────────●──────────── pass
  0      20   40  50   60   80  100
```

Everything that follows is the exact same idea — compute a number, check whether it's positive or negative — just done using more than one feature at a time. A hyperplane is simply "a splitting point" generalized to more dimensions: a splitting **line** in 2D, a splitting **plane** in 3D, and a splitting **equation** beyond that.

---

## 2. Step 1: The hyperplane in 2D

Suppose you want to classify emails as spam or not spam. Every email gets converted into numbers first — this is a very common approach (used, for example, in the classic UCI Spambase dataset), where each feature is a **word frequency**: the percentage of words in the email that match a specific keyword. So:

- `x1` = word_freq_technology → e.g. if "technology" makes up 2% of the words in an email, `x1 = 2.0`
- `x2` = word_freq_money → e.g. if "money" makes up 5% of the words in an email, `x2 = 5.0`

The intuition is that legitimate technology-related emails tend to use words like "technology" a lot but rarely mention "money," while spam emails (offers, prizes, financial scams) tend to do the opposite — mention "money" heavily and "technology" rarely. So plotting every email as a point `(x1, x2)`, you'd expect spam and non-spam emails to cluster in different regions:

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

A **hyperplane** in 2D is just a line that separates the two classes. You've almost certainly seen the *slope-intercept* form of a line before:

```
y = m·x + c
```

This works fine for drawing lines, but it breaks down for a vertical line (where the slope `m` is undefined) and doesn't generalize cleanly to 3D or beyond. So instead, we use the more general **standard form** of a line, which has no such restriction:

```
a·x + b·y + c = 0
```

Any line — no matter its orientation — can be written this way. We now relabel the constants using weights (`W`) instead of `a, b, c`, and rename `x, y` to `x1, x2` (since we'll soon have far more than 2 features):

```
W0 + W1·x1 + W2·x2 = 0
```

Here, `x1` and `x2` are the **features** — the actual data values for one email. `W1` and `W2` are the **weights** (coefficients) that the SVM algorithm learns from the training data — they determine the line's orientation (which direction it tilts). `W0` is a constant, called the **bias** or **intercept** term — it determines how far the line is shifted away from the origin.

Put simply: **"training the SVM" means searching for the specific values of `W0`, `W1`, and `W2` that best separate the two classes.** Part 2 of this series explains exactly how those values are chosen; for now, assume they've already been found.

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

### A fully worked example with real sample data

Let's make this concrete with an actual small dataset of 6 emails, using `word_freq_technology` (`x1`) and `word_freq_money` (`x2`):

| Email | x1 (technology) | x2 (money) | Label |
|---|---|---|---|
| 1 | 5 | 1 | spam |
| 2 | 6 | 2 | spam |
| 3 | 7 | 1 | spam |
| 4 | 1 | 5 | not spam |
| 5 | 2 | 6 | not spam |
| 6 | 1 | 7 | not spam |

Notice: spam emails have **high** `x1` and **low** `x2`, while non-spam emails have the opposite. Plotted, the two classes fall cleanly on either side of a diagonal line running from the top-left to the bottom-right:

```
x2 (money)
 7 │                     ■ (email 6)
 6 │                  ■ (email 5)
 5 │               ■ (email 4)
 4 │            ╲
 3 │              ╲   ← the hyperplane sits somewhere in this gap
 2 │       ●          ╲ (email 2)
 1 │  ● (email 1)   ● (email 3)
 0 └──────────────────────────── x1 (technology)
     0  1  2  3  4  5  6  7
```

Fitting an SVM to this data (we'll properly explain *how* the best line is chosen in Part 2 — for now, just look at what comes out) gives the following hyperplane:

```
0.25·x1 − 0.25·x2 = 0
```

i.e. `W1 = 0.25`, `W2 = -0.25`, `W0 = 0`. Let's verify this classifies every training point correctly, and then use it on a brand-new email:

```python
import numpy as np
from sklearn.svm import SVC

X = np.array([
    [5, 1], [6, 2], [7, 1],   # spam
    [1, 5], [2, 6], [1, 7],   # not spam
])
y = np.array([1, 1, 1, -1, -1, -1])

model = SVC(kernel='linear', C=1000)
model.fit(X, y)
W, W0 = model.coef_[0], model.intercept_[0]
print("W:", W, "W0:", round(W0, 3))   # W: [0.25 -0.25]  W0: ~0.0

for point, label in zip(X, y):
    value = np.dot(W, point) + W0
    print(point, "label:", label, "→ value:", value, "→ predicted:", 1 if value > 0 else -1)

# A brand-new, never-seen email: technology=4, money=2
new_email = np.array([4, 2])
value = np.dot(W, new_email) + W0
print("New email value:", value, "→", "spam" if value > 0 else "not spam")
```

Running this: every training point's computed value matches its true label exactly (all six values come out `+1.0, +1.0, +1.5, -1.0, -1.0, -1.5`, matching `+1, +1, +1, -1, -1, -1`). The new email `[4, 2]` gives `0.25(4) - 0.25(2) = 0.5`, a **positive** value — so the model classifies it as **spam**, even though it never saw this exact point during training. This is the entire point of learning a hyperplane: it generalizes the boundary to any new point in the feature space, not just the training examples.

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

### A real 5-feature example, end to end

To prove this isn't just theory, let's generate a real dataset with 5 features, fit an SVM, and manually check the learned hyperplane's accuracy ourselves — with no visualization possible, since we can't draw a 5D picture:

```python
import numpy as np
from sklearn.svm import SVC
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=50, n_features=5, n_informative=5,
    n_redundant=0, n_clusters_per_class=1, random_state=1
)
y = np.where(y == 0, -1, 1)   # relabel classes as -1 / +1

model = SVC(kernel='linear', C=1000)
model.fit(X, y)
W, W0 = model.coef_[0], model.intercept_[0]
print("Learned W:", np.round(W, 3))
print("Learned W0:", round(W0, 3))

correct = 0
for point, label in zip(X, y):
    value = np.dot(W, point) + W0     # exact same rule as before, just with 5 features
    predicted = 1 if value > 0 else -1
    correct += (predicted == label)

print(f"Accuracy using the manual dot-product rule: {correct / len(y):.2%}")
```

This prints a learned weight vector like `[3.871, -2.053, 0.022, -3.099, -3.886]` and a bias `W0 ≈ 0.896`, and manually applying `∑(Wi·Xi) + W0` with these numbers gets **98% accuracy** on this dataset — using nothing but the same dot-product-and-check-the-sign rule from the 2D case. The dimensionality changed from 2 to 5, but the underlying math is identical.

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
5. Using the worked 2D example (`W1=0.25, W2=-0.25, W0=0`), what value does the point `(3, 3)` produce, and what does that tell you?

**Answers:**

1. `W0 + W1·x1 + W2·x2 = 0`
2. The point lies exactly on the hyperplane — it is on the boundary between the two classes.
3. Because the core boundary equation is always a linear (weighted sum) function. Curved boundaries come from transforming the *features* first (via kernels), not from changing the linear nature of the boundary equation itself.
4. 50 — one weight per feature, plus the separate `W0` bias term.
5. `0.25(3) - 0.25(3) = 0` — the point falls exactly on the hyperplane, meaning it's ambiguous/undecided between spam and not spam.

---

## 8. Summary

- A **hyperplane** is the boundary an SVM uses to separate classes: a line in 2D, a plane in 3D, and a linear equation in higher dimensions.
- The general form is `∑(Wi · Xi) + W0 = 0`.
- Plugging a point into this equation and checking the **sign** of the result tells you which class it belongs to.
- SVM is fundamentally a **linear model** — just like logistic regression.
- For a separable dataset, many different hyperplanes can work. The next topic explains how SVM picks the *best* one.

**Next topic:** [Maximal Margin Classifier]({{ site.baseurl }}/topics/svm-maximal-margin-classifier) — how SVM chooses the single best hyperplane out of infinitely many options.
