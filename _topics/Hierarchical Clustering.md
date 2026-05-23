---
title: "16. Hierarchical Clustering"
category: Machine Learning
order: 16
tags:
  - machine-learning
  - clustering
  - hierarchical
  - agglomerative
  - dendrogram
  - linkage
summary: A complete beginner friendly guide to hierarchical clustering. We cover the agglomerative algorithm step by step, the different linkage methods, how to read a dendrogram, practical considerations, and a full Python demonstration.
---

# Hierarchical Clustering

## A different way to find groups in data

In the previous tutorial we used K-Means to group data points. K-Means asks you to pick a number of clusters K up front, and it gives you that many flat groups as output.

Hierarchical clustering takes a completely different approach. It does not ask you for K. Instead it builds a **tree of clusters**, from individual points all the way up to one giant cluster containing everything. You can then cut the tree at whatever level gives you the right number of groups.

This tutorial covers everything you need to know.

1. What hierarchical clustering is and how it differs from K-Means.
2. The different linkage methods (how we measure distance between clusters).
3. The agglomerative clustering algorithm step by step.
4. How to read and use a dendrogram.
5. Practical considerations.
6. A full Python demonstration.

Let us begin.

---

## What is hierarchical clustering

There are two flavours of hierarchical clustering.

**Agglomerative (bottom up).** Start with every point as its own cluster. Repeatedly merge the two closest clusters until only one cluster remains. This is by far the most common version.

**Divisive (top down).** Start with one big cluster containing everything. Repeatedly split it until every point is its own cluster. Less common, more expensive.

We focus on agglomerative clustering for the rest of this tutorial because it is what you will use 99% of the time.

### How is it different from K-Means

| K-Means | Hierarchical |
|---|---|
| Pick K up front | No K needed |
| Output: flat groups | Output: tree of clusters |
| Reassigns points each iteration | Once merged, points stay together |
| Fast on big data | Slow on big data (O(n^3)) |
| Works on huge datasets | Best for small to medium datasets |
| Hard to visualise the structure | Beautiful dendrogram visualisation |

Hierarchical clustering shines when you want to see the **structure** of your data, not just labels.

---

## The key question, how do you measure distance between clusters

In K-Means, distance between a point and a centroid is straightforward. But in hierarchical clustering you have to measure distance between two **clusters**, each containing many points.

How do you do that? You pick a rule called a **linkage method**. There are four common ones.

### Single linkage (minimum)

The distance between two clusters is the distance between their **two closest points**.

```
d(A, B) = min over a in A, b in B [ d(a, b) ]
```

Tends to produce long, snake-like clusters. Can chain points together through narrow bridges. Sensitive to noise.

### Complete linkage (maximum)

The distance between two clusters is the distance between their **two farthest points**.

```
d(A, B) = max over a in A, b in B [ d(a, b) ]
```

Tends to produce compact, round clusters. More robust to noise than single linkage.

### Average linkage

The distance between two clusters is the **average** of all pairwise distances between points in one cluster and points in the other.

```
d(A, B) = mean over a in A, b in B [ d(a, b) ]
```

A middle ground between single and complete. Often a sensible default.

### Ward linkage

This one is different. Ward linkage merges the two clusters that cause the smallest **increase in total within-cluster variance**. It tries to keep clusters as tight as possible.

Ward is the default in scikit-learn and works extremely well in practice. It also has a nice property: it minimises the same objective as K-Means but in a hierarchical way.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    S["<b>Single</b><br/>closest pair<br/>chain-like clusters"]
    C["<b>Complete</b><br/>farthest pair<br/>compact clusters"]
    A["<b>Average</b><br/>mean of all pairs<br/>balanced choice"]
    W["<b>Ward</b><br/>min variance increase<br/>often best in practice"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    class S,C,A,W gray
</div>

**Which to choose?** Start with Ward. If your clusters should be elongated or chain-like, try single. If you suspect outliers, try complete or average.

---

## The agglomerative clustering algorithm

Now we put it together. Here is the algorithm.

**Step 1. Start with every data point as its own cluster.** If you have N points, you start with N clusters of size 1.

**Step 2. Compute distances between every pair of clusters.** Use the linkage method you chose (single, complete, average, or Ward).

**Step 3. Merge the two closest clusters into one new cluster.**

**Step 4. Recompute distances** between the new cluster and all the others.

**Step 5. Repeat steps 3 and 4** until only one cluster remains.

Throughout this process, every merge is recorded. The record of all merges is the **dendrogram** (the tree).

### A small worked example

Suppose you have 5 points in 1D: 1, 2, 5, 10, 11.

Iteration 0. Five clusters: {1}, {2}, {5}, {10}, {11}.

Iteration 1. Two closest are {1} and {2} (distance 1). Merge them. Clusters now: {1, 2}, {5}, {10}, {11}.

Iteration 2. Two closest are {10} and {11} (distance 1). Merge them. Clusters now: {1, 2}, {5}, {10, 11}.

Iteration 3. The closest pair is {5} and {1, 2}, depending on linkage:
* With single linkage, distance from 5 to {1, 2} is min(|5-1|, |5-2|) = 3.
* Distance from 5 to {10, 11} is min(|5-10|, |5-11|) = 5.
* So merge {5} into {1, 2}. Clusters now: {1, 2, 5}, {10, 11}.

Iteration 4. Only two clusters left. Merge them. Final: {1, 2, 5, 10, 11}.

The dendrogram records each merge with its height equal to the distance at which it happened.

---

## Interpreting the dendrogram

The dendrogram is the killer feature of hierarchical clustering. It shows you the full structure of how points group together at every level.

Reading a dendrogram:

* The x-axis lists individual data points.
* The y-axis is the distance (or dissimilarity) at which two clusters merged.
* Two points connected by a low horizontal line merged early and are similar.
* Two points connected by a high horizontal line merged late and are very different.

To get a flat clustering, you draw a horizontal line across the dendrogram at some height. The number of vertical lines your horizontal line crosses is the number of clusters.

### How to pick where to cut

A common heuristic is to cut at a height where there is a **large vertical gap** between merges. Big gaps mean that merging at the next level forces together clusters that are quite different.

For example, if you see merges at heights 1, 1.2, 1.5, 3.0, 3.1, the jump from 1.5 to 3.0 is a natural place to cut. Below the cut, you get the groups that formed easily. Above the cut, the algorithm started forcing together groups that did not really want to merge.

---

## Practical considerations and applications

Hierarchical clustering is great, but it has limitations.

### It is slow

The standard algorithm is O(n^3) in time and O(n^2) in memory. On 10,000 points this is fine. On 1,000,000 points it is impossible. Use K-Means or BIRCH on huge datasets.

### Once merged, always merged

Unlike K-Means, hierarchical clustering never undoes a decision. If two points get merged early by mistake, they stay together forever. This makes it sensitive to early choices.

### Scale your features

Like K-Means, hierarchical clustering uses distances. Always scale your features first.

### Where it really shines

* Genetics and biology, where you actually want a tree (the tree of life is a giant hierarchical clustering).
* Document and topic organization.
* Customer segmentation where you want to see how groups nest inside larger groups.
* Any time you want to **explore** the data structure, not just label points.

---

## Full Python demonstration

Let us run hierarchical clustering on a real example.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Step 1. Generate data with 4 natural clusters
X, _ = make_blobs(n_samples=50, centers=4, cluster_std=0.7, random_state=42)

# Step 2. Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3. Compute the linkage matrix using Ward
Z = linkage(X_scaled, method="ward")

# Step 4. Plot the dendrogram
plt.figure(figsize=(12, 5))
dendrogram(Z, color_threshold=4)
plt.title("Hierarchical Clustering Dendrogram (Ward Linkage)")
plt.xlabel("Data point index")
plt.ylabel("Distance")
plt.axhline(y=4, color="gray", linestyle="--", label="Cut here for 4 clusters")
plt.legend()
plt.show()

# Step 5. Cut the tree to get 4 flat clusters
model = AgglomerativeClustering(n_clusters=4, linkage="ward")
labels = model.fit_predict(X_scaled)

# Step 6. Visualise the resulting flat clusters
plt.figure(figsize=(8, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap="viridis", s=60, edgecolor="k")
plt.title("Hierarchical Clustering Result (4 clusters)")
plt.xlabel("Feature 1 (scaled)")
plt.ylabel("Feature 2 (scaled)")
plt.grid(True)
plt.show()

# Step 7. See how many points fell into each cluster
print(pd.Series(labels).value_counts().sort_index())
```

What is happening here.

* We generate 50 points in 4 true clusters and scale them.
* We use scipy's `linkage` function to compute the merge sequence using Ward linkage.
* We plot the dendrogram. Look at it and find a big vertical gap. That gap tells you where to cut.
* We use scikit-learn's `AgglomerativeClustering` to actually produce flat cluster labels by cutting at the level that gives 4 clusters.
* We visualise the result.

### Trying different linkage methods

You can compare linkage methods easily by changing the `method` parameter in `linkage()`.

```python
for method in ["single", "complete", "average", "ward"]:
    Z = linkage(X_scaled, method=method)
    plt.figure(figsize=(10, 4))
    dendrogram(Z)
    plt.title(f"Dendrogram with {method} linkage")
    plt.show()
```

You will notice that single linkage produces chain-like dendrograms, while Ward gives the cleanest, most balanced trees.

---

## Quick summary

Hierarchical clustering builds a full tree of merges from individual points up to one giant cluster.

The four big things to remember.

1. Agglomerative clustering merges the two closest clusters at each step, recorded as a dendrogram.
2. The linkage method (single, complete, average, Ward) defines how distance between clusters is measured. Ward is a great default.
3. The dendrogram visualises the entire structure. You cut it at a height to get flat clusters.
4. It is slow on huge datasets but excellent for exploring structure on small to medium ones.

Use it when you want to **see how your data is organised**, not just put labels on it.

In the next tutorial we look at K-Nearest Neighbours, an algorithm that uses the same distance metrics but for classification rather than clustering.
