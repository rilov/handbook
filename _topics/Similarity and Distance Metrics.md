---
title: "13. Similarity and Distance Metrics"
category: Machine Learning
order: 13
tags:
  - machine-learning
  - distance-metrics
  - similarity
  - euclidean
  - cosine
  - jaccard
  - correlation
summary: A complete beginner friendly guide to the metrics machine learning uses to decide whether two points are similar or different. We cover distance-based, angle-based, correlation-based, and set-based metrics with simple examples and Python code.
---

# Similarity and Distance Metrics

## How do we decide if two things are similar

Before we can talk about clustering or nearest neighbour algorithms, we have to answer one simple question.

> Given two data points, how do we measure how similar or different they are?

This sounds easy but it has many answers, and the answer you pick changes everything downstream. Different metrics give very different results. Choosing the right one is one of the most important decisions in unsupervised learning.

In this tutorial we cover the four big families of metrics that you will see again and again.

1. **Distance-based metrics.** How far apart are two points?
2. **Angle-based metrics.** How aligned are two vectors?
3. **Correlation-based metrics.** Do two series move together?
4. **Set-based metrics.** How much do two collections overlap?

By the end you will know which metric to use in which situation, and how each one is calculated.

---

## Distance-based metrics

These are the most intuitive. They measure how far apart two points are in some space.

### Euclidean distance

This is the straight line distance between two points. It is what a ruler measures.

For two points `A = (a1, a2, ..., an)` and `B = (b1, b2, ..., bn)`, the Euclidean distance is

```
d(A, B) = sqrt( (a1 - b1)^2 + (a2 - b2)^2 + ... + (an - bn)^2 )
```

Simple example. If A = (1, 2) and B = (4, 6), then
- difference in x is 4 - 1 = 3
- difference in y is 6 - 2 = 4
- squared sum is 9 + 16 = 25
- square root is 5

So A and B are 5 units apart.

```python
import numpy as np
A = np.array([1, 2])
B = np.array([4, 6])
euclidean = np.sqrt(np.sum((A - B) ** 2))
print(euclidean)   # 5.0
```

**When to use Euclidean.** Continuous numeric features that all live on similar scales. Always scale your features (StandardScaler) before using Euclidean distance, because otherwise large-valued features dominate.

### Manhattan distance (also called L1 or city block)

This measures distance like a taxi driving on a grid of city streets. You add up the absolute differences along each axis instead of using a straight line.

```
d(A, B) = |a1 - b1| + |a2 - b2| + ... + |an - bn|
```

For A = (1, 2) and B = (4, 6), the Manhattan distance is |1 - 4| + |2 - 6| = 3 + 4 = 7.

```python
manhattan = np.sum(np.abs(A - B))
print(manhattan)   # 7
```

**When to use Manhattan.** When your features represent things that genuinely cannot move diagonally (like grid positions). Also more robust to outliers than Euclidean.

### Minkowski distance

A general formula that includes both Euclidean and Manhattan as special cases.

```
d(A, B) = ( sum |ai - bi|^p ) ^ (1/p)
```

When p = 1, you get Manhattan. When p = 2, you get Euclidean. Larger p gives more weight to large differences.

### Chebyshev distance

The biggest difference along any single axis. It is what a chess king uses (one step in any direction).

```
d(A, B) = max( |a1 - b1|, |a2 - b2|, ..., |an - bn| )
```

For A = (1, 2) and B = (4, 6), Chebyshev distance is max(3, 4) = 4.

---

## Angle-based metrics

Sometimes you do not care about magnitude, only about direction. Two vectors pointing the same way are similar even if one is much longer than the other.

### Cosine similarity

Cosine similarity measures the angle between two vectors.

```
cosine_similarity(A, B) = (A . B) / (|A| * |B|)
```

The numerator is the dot product. The denominator is the product of the lengths of the two vectors.

The value ranges from -1 to 1.
- 1 means the vectors point the exact same way
- 0 means they are perpendicular (no relationship)
- -1 means they point in opposite directions

Concrete example. Suppose customer A bought 2 books and 4 movies, and customer B bought 4 books and 8 movies. They have very different totals but they bought books and movies in the same ratio. Euclidean distance would say they are far apart. Cosine similarity would say they are identical (similarity = 1) because their preferences point the same way.

```python
A = np.array([2, 4])
B = np.array([4, 8])
cosine = np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))
print(cosine)   # 1.0
```

You can also turn it into a distance by computing `1 - cosine_similarity`.

**When to use cosine.** Text documents (bag of words vectors), high-dimensional sparse data, recommendation systems, embeddings from neural networks. Essentially any time direction matters more than magnitude.

---

## Correlation-based metrics

These ask: do two series move together?

### Pearson correlation

Pearson correlation measures how strongly two variables move in a linear relationship. It ranges from -1 to +1.

- +1 means they move perfectly together
- 0 means no linear relationship
- -1 means they move perfectly in opposite directions

It is essentially cosine similarity after subtracting the mean from each vector.

```
pearson(A, B) = cov(A, B) / (std(A) * std(B))
```

Example. Suppose stock A goes up 5% on days that stock B goes up 5%, and down 3% on days B is down 3%. Their correlation is close to +1. If they move randomly with respect to each other, correlation is close to 0.

```python
A = np.array([1, 2, 3, 4, 5])
B = np.array([2, 4, 6, 8, 10])
pearson = np.corrcoef(A, B)[0, 1]
print(pearson)   # 1.0
```

To turn correlation into a distance, use `1 - correlation`.

**When to use Pearson.** Time series, sensor readings, financial data, gene expression data. Anywhere you care whether series rise and fall together.

### Spearman correlation

Same idea as Pearson but works on ranks instead of raw values. So it captures any monotonic relationship, not just linear ones. Useful when the relationship is "the bigger one goes up, the other goes up" but not necessarily proportionally.

---

## Set-based metrics

When your data is a collection of items (set membership), distance metrics no longer make sense. You use set-based metrics instead.

### Jaccard similarity

Jaccard measures the overlap between two sets. It is the size of the intersection divided by the size of the union.

```
jaccard(A, B) = |A intersection B| / |A union B|
```

The result ranges from 0 (no overlap) to 1 (identical sets).

Example. Customer A bought {bread, milk, eggs}. Customer B bought {milk, eggs, butter}.
- Intersection is {milk, eggs}, size 2.
- Union is {bread, milk, eggs, butter}, size 4.
- Jaccard similarity is 2 / 4 = 0.5.

```python
A = set(["bread", "milk", "eggs"])
B = set(["milk", "eggs", "butter"])
jaccard = len(A & B) / len(A | B)
print(jaccard)   # 0.5
```

To turn it into a distance, use `1 - jaccard_similarity`.

**When to use Jaccard.** Categorical data, document tag sets, market basket analysis, document similarity using shingles, image segmentation evaluation.

### Hamming distance

For two strings or binary vectors of equal length, Hamming distance counts how many positions differ.

Example. The strings "karolin" and "kathrin" differ in 3 positions (o vs t, l vs h, n vs n... wait, actually karolin → kathrin: k=k, a=a, r=t, o=h, l=r, i=i, n=n, so 3 differences).

```python
s1 = "karolin"
s2 = "kathrin"
hamming = sum(c1 != c2 for c1, c2 in zip(s1, s2))
print(hamming)   # 3
```

**When to use Hamming.** Comparing binary vectors, error detection codes, comparing DNA sequences of equal length.

---

## How to choose the right metric

Here is a simple cheat sheet.

| Your data looks like | Use this |
|---|---|
| Numeric, similar scales, magnitude matters | Euclidean |
| Numeric, you want robustness to outliers | Manhattan |
| Numeric, very high dimensional or sparse | Cosine |
| Time series, sensor data, anything moving together | Pearson correlation |
| Sets of items (purchases, tags, words) | Jaccard |
| Binary vectors or strings of equal length | Hamming |

The most common mistake is using Euclidean on raw unscaled data with mixed scales. Always scale numeric features before using Euclidean.

The second most common mistake is using Euclidean on high-dimensional sparse data (like text). In high dimensions, all points end up roughly the same Euclidean distance apart (this is the "curse of dimensionality"). Cosine similarity works much better there.

---

## Quick summary

We have seen four families of metrics.

* **Distance-based** (Euclidean, Manhattan, Chebyshev) measure how far apart points are. Sensitive to scale, so always scale your features first.
* **Angle-based** (Cosine) measure direction, not magnitude. Great for sparse and high-dimensional data.
* **Correlation-based** (Pearson, Spearman) measure whether two series move together. Great for time series.
* **Set-based** (Jaccard, Hamming) measure overlap. Great for categorical and binary data.

You will see all of these again when we tackle clustering and nearest neighbour algorithms in the next tutorials. The metric you choose is part of the model.
