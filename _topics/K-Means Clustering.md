---
title: "14. K-Means Clustering"
category: Machine Learning
order: 14
tags:
  - machine-learning
  - clustering
  - kmeans
  - unsupervised-learning
  - elbow-method
summary: A complete beginner friendly guide to K-Means Clustering. We cover unsupervised learning, how K-Means actually works step by step, picking the right number of clusters, common pitfalls, and a full Python demonstration.
---

# K-Means Clustering

## Finding groups in data without any labels

Up to now every tutorial has been about **supervised learning**. We had labelled data, where every training example came with the right answer attached, and the model learned to predict that answer.

But what if you do not have labels? What if you just have a pile of data and want to know whether there are natural groups hiding inside it?

That is **unsupervised learning**, and the most famous unsupervised algorithm of all is **K-Means Clustering**.

This tutorial covers everything you need to know.

1. What unsupervised learning is and how it differs from supervised learning.
2. The intuition behind clustering.
3. How K-Means actually works, step by step.
4. The math (kept gentle) for the distances and centroid updates.
5. How to pick the right number of clusters using the elbow method.
6. Practical considerations and common pitfalls.
7. A full Python demonstration.

Let us get started.

---

## What is unsupervised learning

In supervised learning, every row in your training data looks like this:

```
features      ->  label
(age, income) ->  bought_product (yes/no)
```

In unsupervised learning, there is no label column. You just have features:

```
features
(age, income)
(age, income)
...
```

Your job is to discover something about the structure of the data without anyone telling you what to look for.

Clustering is the most common unsupervised task. The goal is to group similar rows together. Same group = similar data points. Different group = different data points.

### Real world examples of clustering

* A retailer groups customers by buying behaviour to design marketing campaigns.
* A streaming service groups viewers by viewing habits to recommend content.
* A bank groups credit card transactions to spot anomalies that look unlike normal groups.
* A biologist groups gene expression patterns to discover possible cell types.
* A photo app groups your photos by who appears in them, without you tagging anyone.

In every case, no one tells the model what the groups should be. The model discovers them from the data itself.

---

## The big idea behind clustering

Imagine you have a scatter plot of 200 customer profiles, each plotted by two features: age and yearly spending.

When you look at the plot, you might see three obvious blobs. Young low spenders in the bottom left. Middle-aged big spenders in the upper right. Older medium spenders in the middle.

A clustering algorithm is just a formal way to tell a computer to find those blobs.

The key idea behind K-Means in particular is that each blob can be summarised by a single point at its center, called a **centroid**.

If you know the centroids, you can assign every data point to whichever centroid is closest. And if you know the assignments, you can find the centroids by taking the average of all points in each group.

This sounds like a chicken-and-egg problem. K-Means solves it by alternating between the two.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    A["<b>Start</b><br/>pick K random<br/>centroids"]
    A --> B["<b>Assign</b><br/>each point to<br/>nearest centroid"]
    B --> C["<b>Update</b><br/>move each centroid to<br/>the mean of its points"]
    C --> D{"<b>Did anything<br/>change?</b>"}
    D -->|yes| B
    D -->|no| E["<b>Done</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class B,C gray
    class A,D,E midgray
</div>

That is the entire algorithm. Let us look at it more carefully.

---

## Metrics and logic for K-Means

K-Means needs two ingredients.

1. A way to measure how close two points are. By default, this is Euclidean distance (see the previous tutorial on Similarity and Distance Metrics).
2. A way to summarise a group of points. By default, this is the mean (the arithmetic average), which is where the "Means" in K-Means comes from.

The K in K-Means is the number of clusters you want to find. You have to tell the algorithm what K is before it starts. We will see later how to pick a sensible K.

### The objective K-Means is trying to minimise

K-Means tries to minimise something called the **within-cluster sum of squares**, or **WCSS** for short. It is also called inertia.

For each cluster, you compute the sum of squared distances from every point in that cluster to the centroid of that cluster. Then you add up those sums across all clusters.

```
WCSS = sum over clusters [ sum over points in cluster ( distance to centroid )^2 ]
```

A smaller WCSS means tighter, more compact clusters. K-Means tries to make WCSS as small as possible.

The reason squared distances are used (instead of just distances) is because the math works out cleanly. When you minimise the sum of squared distances, the optimal "center" of a group of points is exactly their mean.

---

## The K-Means algorithm, step by step

Here is the full algorithm.

**Step 1. Pick K.** Decide how many clusters you want.

**Step 2. Initialise centroids.** Pick K starting positions for the centroids. The simplest method is to pick K random points from your dataset. A smarter method called **K-Means++** spreads the initial centroids out, which usually gives better results. Most libraries use K-Means++ by default.

**Step 3. Assignment step.** For every data point, compute its distance to each of the K centroids. Assign the point to whichever centroid is closest.

**Step 4. Update step.** For each cluster, compute the mean of all points assigned to it. Move that cluster's centroid to the new mean.

**Step 5. Repeat.** Go back to Step 3 and reassign points based on the new centroids. Then update again. Then reassign. Keep going.

**Step 6. Stop.** When the centroids stop moving (or move by very little), the algorithm has converged. The current assignments are the final clusters.

That is it. Five steps, simple, and very effective.

### A small worked example

Suppose you have just 6 points in 1D, and you want K = 2 clusters.

Data: 1, 2, 3, 10, 11, 12.

Step 1. K = 2.

Step 2. Random initial centroids: pick points 1 and 12.

Step 3. Assign each point to its nearest centroid.
- Point 1: closer to 1. Cluster A.
- Point 2: closer to 1. Cluster A.
- Point 3: closer to 1 (distance 2) than 12 (distance 9). Cluster A.
- Point 10: closer to 12. Cluster B.
- Point 11: closer to 12. Cluster B.
- Point 12: closer to 12. Cluster B.

Cluster A = {1, 2, 3}, Cluster B = {10, 11, 12}.

Step 4. Update centroids.
- New centroid A = mean(1, 2, 3) = 2.
- New centroid B = mean(10, 11, 12) = 11.

Step 5. Reassign with new centroids 2 and 11.
- Every point in A is still closer to 2 than 11.
- Every point in B is still closer to 11 than 2.

No assignments changed. K-Means has converged. Final clusters are {1, 2, 3} and {10, 11, 12}, with centroids at 2 and 11.

This is a toy example, but the algorithm works the same way in any number of dimensions.

---

## Picking the right number of clusters

K-Means asks you to pick K up front. But how do you know what K should be?

If you knew there were exactly 3 customer types ahead of time, you would set K = 3. But usually you do not know. So you have to discover K from the data.

The most common method is the **elbow method**.

### The elbow method

Here is the idea. Run K-Means for several values of K, like K = 1, 2, 3, ..., 10. For each K, record the WCSS (inertia).

WCSS always decreases as K grows. With K = 1 cluster, every point is far from the center, so WCSS is huge. With K = N (one cluster per point), WCSS is zero.

But the rate at which WCSS drops changes. Adding the first few clusters helps a lot. Beyond a certain K, adding more clusters gives only tiny improvements.

If you plot WCSS against K, you usually see a curve that looks like an arm bending. The point where the curve sharply bends is called the **elbow**, and that K is a good choice.

```python
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

wcss = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X)
    wcss.append(km.inertia_)

plt.plot(range(1, 11), wcss, marker="o")
plt.xlabel("Number of clusters K")
plt.ylabel("WCSS (inertia)")
plt.title("Elbow Method")
plt.grid(True)
plt.show()
```

If the elbow is at K = 3, then K = 3 is a good number of clusters.

### Silhouette score

A more rigorous alternative is the **silhouette score**. For each point, it measures how close that point is to its own cluster compared to the next nearest cluster. The score ranges from -1 to 1. Higher is better.

```python
from sklearn.metrics import silhouette_score

for k in range(2, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    score = silhouette_score(X, km.labels_)
    print(f"K = {k}, silhouette = {score:.3f}")
```

Pick the K with the highest silhouette score.

In practice, looking at both the elbow plot and the silhouette score together is the safest approach.

---

## Practical considerations

K-Means is powerful but it has several quirks you need to know.

### Always scale your features

K-Means uses Euclidean distance. If one feature ranges from 0 to 1 and another from 0 to 1,000,000, the large feature will completely dominate the distance calculation. You have to scale your features first, usually with StandardScaler.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

Then run K-Means on `X_scaled`, not on raw `X`. This is the single most common mistake people make with K-Means.

### K-Means assumes spherical clusters of similar size

K-Means works best when clusters are roughly round blobs of similar size. It struggles with elongated clusters, very different sized clusters, or clusters with complex shapes. If your data has those shapes, consider DBSCAN, GMM, or hierarchical clustering instead.

### Initialisation matters

Different random initialisations can lead to different final clusters. To handle this, libraries run K-Means many times with different starting points and keep the best result. Always set `n_init` to at least 10.

### K-Means cannot find outliers

Every point gets assigned to some cluster, even points that do not belong with any group. If you need outlier detection, use DBSCAN instead.

### K-Means does not work well with categorical features

Means do not make sense for categorical data. For categorical features, consider K-Modes or K-Prototypes instead.

---

## Full Python demonstration

Let us put everything together with a real example. We will generate synthetic customer data and find the clusters.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs

# Step 1. Generate synthetic data with 4 true clusters
X, y_true = make_blobs(
    n_samples=400,
    centers=4,
    cluster_std=0.8,
    random_state=42,
)

# Step 2. Always scale your data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3. Use the elbow method to pick K
wcss = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X_scaled)
    wcss.append(km.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(range(1, 11), wcss, marker="o")
plt.xlabel("K")
plt.ylabel("WCSS")
plt.title("Elbow Method")
plt.grid(True)
plt.show()

# The elbow should appear around K = 4

# Step 4. Train final K-Means with K = 4
final_km = KMeans(n_clusters=4, n_init=10, random_state=42)
final_km.fit(X_scaled)
labels = final_km.labels_
centroids = final_km.cluster_centers_

# Step 5. Visualise the result
plt.figure(figsize=(8, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap="viridis", s=30, alpha=0.7)
plt.scatter(centroids[:, 0], centroids[:, 1], c="red", marker="X", s=250, label="Centroids")
plt.title("K-Means Clustering (K = 4)")
plt.xlabel("Feature 1 (scaled)")
plt.ylabel("Feature 2 (scaled)")
plt.legend()
plt.grid(True)
plt.show()

# Step 6. Inspect the cluster sizes
print(pd.Series(labels).value_counts().sort_index())
```

What is happening:

* We generate 400 synthetic points in 4 true clusters.
* We standardise them so each feature has zero mean and unit variance.
* We run the elbow method for K = 1 through 10. The elbow appears at K = 4.
* We train the final model with K = 4 and look at the assignments.
* We visualise the clusters and centroids.

You can apply this exact workflow to any real dataset. Just replace the `make_blobs` call with `pd.read_csv("your_data.csv")` and select the numeric columns.

---

## Quick summary

K-Means is the most popular clustering algorithm in the world for a reason. It is simple, fast, and works well on a huge variety of problems.

The five things to remember.

1. K-Means alternates between assigning points to nearest centroids and moving centroids to the mean of assigned points.
2. It minimises the within-cluster sum of squares (WCSS).
3. You pick K using the elbow method or silhouette score.
4. Always scale your features first.
5. It assumes spherical, similarly sized clusters. For weird shapes, use DBSCAN or GMM.

In the next tutorial we look at **hierarchical clustering**, a completely different approach that does not require you to pick K up front and produces a tree of clusters you can cut at any depth.
