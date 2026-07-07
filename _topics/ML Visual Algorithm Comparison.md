---
title: "32. ML Visual Algorithm Comparison"
category: Machine Learning
order: 32
tags:
  - machine-learning
  - comparison
  - decision-boundaries
  - visualization
summary: A side-by-side visual tour of how every classifier carves up the same 2D dataset. See exactly why linear models draw straight lines, decision trees make boxes, KNN makes wavy regions, and ensembles smooth things out.
---

# ML Visual Algorithm Comparison

The fastest way to understand the difference between algorithms is to **see** them all on the same data. This page describes (and gives you the code to generate) the decision boundary each classifier draws.

Run the code at the end of this page and you will see all the visualizations at once.

---

## The setup

We will use a synthetic 2D dataset called "moons" (two interleaving half-circles). It is small enough to plot, complex enough to be interesting, and nonlinear enough to separate the simple from the powerful classifiers.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    D["<b>2D moons dataset</b><br/>two interleaving<br/>half-circles"]
    D --> M["<b>Every classifier</b><br/>predicts every point<br/>on a fine grid"]
    M --> V["<b>Decision boundary</b><br/>visualized as<br/>colored regions"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class M gray
    class D,V midgray
</div>

---

## How each algorithm looks

### Logistic Regression

> **Boundary shape:** A single straight line (or smooth curve with polynomial features).
>
> **Why it looks that way:** Logistic regression is fundamentally linear. The decision is "above the line = class 1, below = class 0."
>
> **On moons:** Fails. The two half-circles cannot be separated by a straight line. Accuracy hovers around 85%.

### KNN (K = 1)

> **Boundary shape:** Wavy and jagged, hugging every training point.
>
> **Why it looks that way:** Each test point copies the label of its single nearest training point.
>
> **On moons:** Captures the shape but looks like a torn paper edge. Will overfit on noisy data.

### KNN (K = 15)

> **Boundary shape:** Smooth and curving, follows the data shape gently.
>
> **Why it looks that way:** Each test point votes among 15 neighbours, so the boundary is the smooth majority surface.
>
> **On moons:** Excellent. Smoothly separates the two moons. Generally a great default.

### Decision Tree (max_depth=3)

> **Boundary shape:** Axis-aligned rectangles. Hard vertical and horizontal cuts.
>
> **Why it looks that way:** Each node splits on one feature at one threshold, producing right-angle boundaries.
>
> **On moons:** Captures the rough shape but with blocky, unnatural edges.

### Decision Tree (max_depth=None)

> **Boundary shape:** Many tiny rectangles, often one per training point.
>
> **Why it looks that way:** The tree grew deep enough to memorize every point.
>
> **On moons:** Classic overfit. Looks great on training, will fail on slightly different data.

### Random Forest

> **Boundary shape:** Smoother than a single tree, still vaguely blocky but with rounded edges.
>
> **Why it looks that way:** Many trees vote, so the hard rectangle edges of individual trees get averaged out.
>
> **On moons:** Very good. Smoother and more accurate than a single tree.

### Gradient Boosting

> **Boundary shape:** Very smooth, follows the data shape closely, can wrap around complex regions.
>
> **Why it looks that way:** Many shallow trees, each adding a small correction. The result is a finely tuned surface.
>
> **On moons:** Near-perfect. Often the best classical model.

### Naive Bayes

> **Boundary shape:** A smooth curve, often elliptical.
>
> **Why it looks that way:** Naive Bayes assumes each feature follows a simple distribution and combines them probabilistically.
>
> **On moons:** Decent but limited. Not as flexible as KNN or trees.

### SVM with RBF Kernel

> **Boundary shape:** Smooth and curving, often the cleanest looking boundary.
>
> **Why it looks that way:** SVM with an RBF kernel implicitly maps points into a higher-dimensional space where a hyperplane can separate them, which projects back as a smooth curve.
>
> **On moons:** Excellent. One of the best on small low-dimensional problems.

### Neural Network (small)

> **Boundary shape:** Smooth and curving, similar to SVM.
>
> **Why it looks that way:** Each layer of the network bends the input space, producing a smooth nonlinear boundary.
>
> **On moons:** Very good with proper tuning. Overkill for this size of problem.

---

## What each pattern teaches you

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    BS["<b>Boundary shape</b>"]
    BS --> S["<b>Straight line</b><br/>Linear / Logistic"]
    BS --> R["<b>Rectangles</b><br/>Decision Tree"]
    BS --> SR["<b>Smoothed rectangles</b><br/>Random Forest"]
    BS --> SM["<b>Smooth curves</b><br/>SVM (RBF), Neural Net,<br/>Gradient Boosting"]
    BS --> J["<b>Jagged hugging</b><br/>KNN (small K)"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class S,R,SR,SM,J gray
    class BS midgray
</div>

Once you have seen these patterns, you can almost guess what an unseen classifier will do just by knowing what family it belongs to.

---

## The code to generate all of them

Save this in a file and run it. You will see all 9 classifiers side by side on the moons dataset.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

# 1. Create the dataset
X, y = make_moons(n_samples=300, noise=0.25, random_state=42)
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 2. Models to compare
classifiers = {
    "Logistic Regression":   LogisticRegression(),
    "KNN (k=1)":             KNeighborsClassifier(n_neighbors=1),
    "KNN (k=15)":            KNeighborsClassifier(n_neighbors=15),
    "Decision Tree (d=3)":   DecisionTreeClassifier(max_depth=3, random_state=42),
    "Decision Tree (full)":  DecisionTreeClassifier(random_state=42),
    "Random Forest":         RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting":     GradientBoostingClassifier(random_state=42),
    "Naive Bayes":           GaussianNB(),
    "SVM (RBF)":             SVC(kernel="rbf", gamma=2, C=1),
    "Neural Net":            MLPClassifier(hidden_layer_sizes=(20, 20), max_iter=2000, random_state=42),
}

# 3. Set up the grid for plotting decision boundaries
x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))

cm = plt.cm.RdBu
cm_bright = ListedColormap(["#FF0000", "#0000FF"])

# 4. Plot each classifier
fig, axes = plt.subplots(2, 5, figsize=(20, 8))
axes = axes.ravel()

for ax, (name, clf) in zip(axes, classifiers.items()):
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)

    # Decision boundary
    if hasattr(clf, "decision_function"):
        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    else:
        Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    Z = Z.reshape(xx.shape)

    ax.contourf(xx, yy, Z, cmap=cm, alpha=0.6)
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors="k", s=25)
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, edgecolors="k", s=25, marker="x")
    ax.set_title(f"{name}\nTest acc = {score:.2f}")
    ax.set_xticks(())
    ax.set_yticks(())

plt.tight_layout()
plt.show()
```

When you run this you will see, in a single picture, the exact differences between every classical algorithm. Look at the boundaries:

* Logistic regression draws one line. Bad for moons.
* Single trees draw boxes. Decent but blocky.
* Random Forest smooths the boxes.
* KNN at K=1 is jagged and overfits. KNN at K=15 is smooth.
* SVM with RBF and Gradient Boosting draw nearly perfect smooth curves.

This single plot teaches more about algorithm differences than reading any text. Run it once and the patterns will stick with you.

---

## How to apply this insight

When you face a real problem, ask:

1. **Is my data linearly separable?** If yes, logistic regression and linear SVM will work.
2. **Are the classes in irregular shapes?** Use tree ensembles, KNN, RBF SVM, or neural nets.
3. **Do I need interpretability?** Logistic regression or a shallow decision tree.
4. **Is my data noisy?** Avoid deep decision trees and KNN with small K (they overfit noise).
5. **Do I have lots of data and want top accuracy?** Gradient boosting.

The boundary shape an algorithm produces tells you what kinds of problems it is good at. Linear boundaries for linear problems. Box boundaries for stepwise problems. Smooth curves for complex nonlinear problems.

Internalize this and you will rarely pick the wrong algorithm for a problem again.
