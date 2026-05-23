---
title: "Ensembles - Part 2 - Bagging and Random Forests"
category: Machine Learning
order: 10
tags:
  - machine-learning
  - random-forest
  - bagging
  - bootstrap
  - hyperparameter-tuning
  - grid-search
summary: Part 2 of the ensembles tutorial. We explain bootstrap sampling, build up to the Random Forest algorithm step by step, and walk through full hyperparameter tuning using number of trees, maximum depth, and grid search with cross validation.
---

# Ensembles - Part 2 - Bagging and Random Forests

## How many trees become a forest

In Part 1 we introduced the two big families of ensembles, bagging and boosting. We also met the most famous member of the bagging family, the Random Forest.

Now we go deep on bagging.

By the end of this part you will understand three things in real depth.

1. What bootstrap sampling actually is and why it matters.
2. How a Random Forest works step by step from the inside.
3. How to tune the hyperparameters of a Random Forest, including number of trees, maximum depth, and combinations using grid search.

This part has the most code in the whole tutorial. We will build a Random Forest classifier on a real dataset and tune it the way you would in real work.

Let us start with the foundation of bagging, which is something called bootstrap sampling.

---

## Bootstrap sampling, the foundation of bagging

The word bagging stands for **bootstrap aggregating**.

Bootstrap is the sampling method. Aggregating is what we do at the end with the predictions.

Let us explain bootstrap sampling carefully because it is the heart of how bagging works.

### What bootstrap sampling means

Suppose your training set has 1,000 rows. You want to create a slightly different version of this dataset to train one base model on.

Here is what bootstrap sampling does.

You draw a row at random from the original 1,000. You write it down. You **put it back** into the pool. You draw another row. You write it down. You put it back. You keep doing this 1,000 times.

At the end you have a new dataset of 1,000 rows. But because you put each row back after picking it, some rows from the original got picked more than once, and some rows did not get picked at all.

That is bootstrap sampling. It is sampling with replacement, of the same size as the original dataset.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    O["<b>Original data</b><br/>1000 rows"]
    O -->|"sample with<br/>replacement"| B1["<b>Bootstrap 1</b><br/>1000 rows<br/>(some duplicated,<br/>some missing)"]
    O -->|"sample with<br/>replacement"| B2["<b>Bootstrap 2</b><br/>1000 rows"]
    O -->|"sample with<br/>replacement"| B3["<b>Bootstrap 3</b><br/>1000 rows"]
    O -->|"..."| BN["<b>Bootstrap N</b><br/>1000 rows"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class B1,B2,B3,BN gray
    class O midgray
</div>

### Why bootstrap sampling is useful

Each bootstrap sample looks **almost** like the original dataset, but is a little different. Some rows are missing. Others appear multiple times. That small variation is exactly what we want.

When you train a decision tree on each bootstrap sample, the trees will be slightly different from each other. They will pick different splits at different places. They will make different mistakes.

That is the secret. Bootstrap sampling is a cheap and clever way to create models that disagree with each other.

And as we learned in Part 1, models that disagree with each other are exactly what an ensemble needs.

### One more useful detail, out of bag samples

When you draw 1,000 rows with replacement from 1,000 rows, statistically about 63 percent of the original rows end up in the bootstrap. The other 37 percent are left out.

Those left out rows are called **out of bag** samples, or OOB samples.

This turns out to be very useful. Each tree was never trained on its own out of bag rows. So those rows can be used as a free validation set for that tree. Average the predictions across all trees on their out of bag rows, and you get something called the **out of bag score**, which is a good estimate of the model's accuracy without needing a separate test set.

Random Forest libraries like scikit-learn give you this score for free if you ask for it.

---

## What bagging does, step by step

Now we can describe bagging clearly.

Step 1. Take your original training data.

Step 2. Create N different bootstrap samples from it.

Step 3. Train one base model on each bootstrap sample. Usually the base model is a decision tree.

Step 4. To make a prediction on a new data point, run that point through every model. For classification, take the majority vote. For regression, take the average.

That is the entire bagging algorithm.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    O["<b>Original training data</b>"]
    O --> S1["<b>Bootstrap sample 1</b>"]
    O --> S2["<b>Bootstrap sample 2</b>"]
    O --> SN["<b>Bootstrap sample N</b>"]
    S1 --> T1["<b>Tree 1</b>"]
    S2 --> T2["<b>Tree 2</b>"]
    SN --> TN["<b>Tree N</b>"]
    T1 --> V["<b>Combine predictions</b><br/>vote or average"]
    T2 --> V
    TN --> V
    V --> P["<b>Final prediction</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class S1,S2,SN,T1,T2,TN gray
    class O,V,P midgray
</div>

The result is a model that is much more stable and accurate than any single tree. Variance goes down. Bias stays about the same. That is the magic of bagging.

---

## From bagging to Random Forests

Plain bagging with decision trees is already pretty good. But Random Forest adds one more clever twist that makes it even better.

Here is the problem with plain bagging.

Even when you give each tree a different bootstrap sample, the trees still tend to look similar. Why? Because if there is one feature that is very strong, every tree will pick that feature first. Most trees end up looking like variations of the same shape.

Similar trees mean their errors are correlated. Correlated errors do not cancel each other out as well. The benefit of averaging is reduced.

Random Forest solves this with one extra rule.

### The extra random forest rule

> At every split, do not consider all the features. Consider only a random subset of them.

That is it. That one rule changes everything.

For example, suppose your dataset has 20 features. At each split, instead of looking at all 20 to find the best one, the tree might look at only 5 randomly chosen features and pick the best one out of those.

The result is that different trees end up using different features at different places. The strong feature does not dominate every tree. The trees become more diverse, their errors become less correlated, and the average gets more accurate.

This is the only difference between plain bagging with trees and Random Forest. But it is a huge difference in practice.

### How many features at each split

A common rule of thumb for classification is to use the square root of the total number of features. So if you have 25 features, each split tries about 5 of them. If you have 100 features, each split tries about 10 of them.

For regression, the common rule is to use one third of the features.

These are defaults. You can tune them. But they are good starting points.

---

## A complete picture of Random Forest

Putting everything together, here is what Random Forest does.

Step 1. Take the original training data.

Step 2. Create N bootstrap samples.

Step 3. For each bootstrap sample, grow a decision tree. But every time the tree needs to split, pick a random subset of features to consider, and only look at those.

Step 4. Let each tree grow deep, with little or no pruning. Single trees overfit, but the average of many overfit trees still generalizes well.

Step 5. To predict on a new data point, run it through every tree. Take a majority vote for classification or an average for regression.

That is Random Forest.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    O["<b>Original data</b><br/>n rows, p features"]
    O --> R1["<b>Bootstrap +<br/>random feature subset<br/>at each split</b>"]
    R1 --> T1["<b>Deep Tree 1</b>"]
    R1 --> T2["<b>Deep Tree 2</b>"]
    R1 --> T3["<b>Deep Tree 3</b>"]
    R1 --> TN["<b>Deep Tree N</b>"]
    T1 --> V["<b>Vote / Average</b>"]
    T2 --> V
    T3 --> V
    TN --> V
    V --> P["<b>Final prediction</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class T1,T2,T3,TN gray
    class O,R1,V,P midgray
</div>

This is one of the most successful and widely used machine learning algorithms in history. Banks, insurance companies, healthcare systems, and tech companies all rely on Random Forests for real production predictions every day.

---

## The hyperparameters that matter

Random Forest has several knobs you can turn. Most people only need to know about three or four of them. Here are the important ones.

### Number of estimators (n_estimators)

This is the number of trees in the forest.

More trees usually means better and more stable predictions, up to a point. After enough trees, adding more does not help much but takes longer to train.

Typical values: 100, 200, 500, 1000.

### Maximum tree depth (max_depth)

This controls how deep each individual tree is allowed to grow.

In a single decision tree, deeper trees overfit. In a Random Forest, this is less of a problem because averaging across many trees reduces overfitting. Still, very deep trees take longer to train and can sometimes hurt performance.

Typical values: 5, 7, 10, 15, or None (no limit).

### Maximum features at each split (max_features)

How many features to consider at each split. We talked about this earlier.

Typical values: "sqrt" (square root of total features) for classification, "log2", or a specific number.

### Minimum samples per split (min_samples_split)

The smallest group size that the tree is still allowed to split. Bigger values mean less splitting and shallower trees.

Typical values: 2 (default), 5, 10, 20.

### Minimum samples per leaf (min_samples_leaf)

The smallest size a leaf is allowed to be. Bigger values mean smoother decisions.

Typical values: 1 (default), 5, 10.

### Class weight (class_weight)

Useful when the classes are imbalanced. Setting this to "balanced" tells the algorithm to give more weight to the minority class.

Typical values: None (default), "balanced".

For most beginners, the two most important hyperparameters to tune are **n_estimators** and **max_depth**. Let us see how to do that.

---

## Hyperparameter tuning, step by step

Now we get to the practical part. We will tune a Random Forest classifier the way you would tune one in real work. We will go through it in three stages.

Stage 1. Tune the number of estimators alone.

Stage 2. Tune the maximum depth alone.

Stage 3. Tune both together using grid search with cross validation.

This is exactly the workflow you want to know. Let us walk through it slowly.

### Setting up

We will use the famous breast cancer dataset that comes with scikit-learn. It has 569 rows and 30 features. The task is to predict whether a tumor is malignant or benign.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

# Split into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.3, random_state=123, stratify=y
)

print("Training rows:", X_train.shape[0])
print("Validation rows:", X_val.shape[0])
```

This gives us roughly 400 rows for training and 170 rows for validation. We will use the validation set to measure how each model performs.

### Stage 1. Tune the number of estimators alone

We will try several values of n_estimators while keeping everything else fixed. For each value, we train a model and record both the accuracy and the ROC AUC score on the training and validation sets.

```python
# Create a list of values to tune over.
# np.arange(50, 501, 50) gives 50, 100, 150, ..., 500
num_estimators = np.arange(50, 501, 50)

# Empty dataframe to record performance
results_n = pd.DataFrame()

for n in num_estimators:
    # Build a Random Forest with the current value of n_estimators
    current_rf = RandomForestClassifier(
        n_estimators=n,
        max_depth=5,
        class_weight="balanced",
        random_state=123,
    )
    current_rf.fit(X_train, y_train)
    print(f"Done training with n_estimators = {n}")

    # Predictions for accuracy
    y_pred_train = current_rf.predict(X_train)
    y_pred_val = current_rf.predict(X_val)

    # Predicted probabilities for ROC AUC
    proba_train = current_rf.predict_proba(X_train)[:, 1]
    proba_val = current_rf.predict_proba(X_val)[:, 1]

    # Store everything in the dataframe
    results_n.loc[n, "train_accuracy"] = accuracy_score(y_train, y_pred_train)
    results_n.loc[n, "val_accuracy"] = accuracy_score(y_val, y_pred_val)
    results_n.loc[n, "train_roc_auc"] = roc_auc_score(y_train, proba_train)
    results_n.loc[n, "val_roc_auc"] = roc_auc_score(y_val, proba_val)

print(results_n)
```

What is happening here, in plain words.

We made a list of 10 values from 50 to 500 in steps of 50. For each value we built a Random Forest with that many trees, with maximum depth fixed at 5 for now. We trained the model on the training data. We measured how well it did on both the training and validation data, using both accuracy and ROC AUC.

The print statement after the fit gives you visual feedback so you can see the loop progressing.

### Visualizing the results

Once we have the dataframe, we can plot it.

```python
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(results_n.index, results_n["val_accuracy"], marker="o")
plt.title("Validation Accuracy vs Number of Estimators")
plt.xlabel("n_estimators")
plt.ylabel("Validation Accuracy")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(results_n.index, results_n["val_roc_auc"], marker="o")
plt.title("Validation ROC AUC vs Number of Estimators")
plt.xlabel("n_estimators")
plt.ylabel("Validation ROC AUC")
plt.grid(True)

plt.tight_layout()
plt.show()
```

You will typically see that the metric jumps up quickly with the first few hundred trees and then flattens out. There may be a small spike or dip somewhere because validation scores are noisy on small datasets. The general pattern is that more trees help, then the help levels off.

The key insight is that the metric does not keep climbing forever. After some point, adding more trees just costs you training time without giving you better predictions.

### Stage 2. Tune the maximum depth alone

Now we fix the number of estimators and tune the depth instead.

```python
max_depths = np.arange(1, 11)

results_d = pd.DataFrame()

for d in max_depths:
    current_rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=d,
        class_weight="balanced",
        random_state=123,
    )
    current_rf.fit(X_train, y_train)
    print(f"Done training with max_depth = {d}")

    y_pred_train = current_rf.predict(X_train)
    y_pred_val = current_rf.predict(X_val)
    proba_train = current_rf.predict_proba(X_train)[:, 1]
    proba_val = current_rf.predict_proba(X_val)[:, 1]

    results_d.loc[d, "train_accuracy"] = accuracy_score(y_train, y_pred_train)
    results_d.loc[d, "val_accuracy"] = accuracy_score(y_val, y_pred_val)
    results_d.loc[d, "train_roc_auc"] = roc_auc_score(y_train, proba_train)
    results_d.loc[d, "val_roc_auc"] = roc_auc_score(y_val, proba_val)

print(results_d)
```

The shape is identical to the n_estimators loop, just tuning a different parameter.

```python
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(results_d.index, results_d["val_accuracy"], marker="o")
plt.title("Validation Accuracy vs Max Depth")
plt.xlabel("max_depth")
plt.ylabel("Validation Accuracy")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(results_d.index, results_d["val_roc_auc"], marker="o")
plt.title("Validation ROC AUC vs Max Depth")
plt.xlabel("max_depth")
plt.ylabel("Validation ROC AUC")
plt.grid(True)

plt.tight_layout()
plt.show()
```

The typical pattern looks like this. Performance starts low at depth 1 because the trees are too simple. It climbs steeply as depth increases. Around depth 5 to 8 it starts to flatten out. Past that, more depth does not help much and in some cases starts to hurt.

You can use this curve to spot the sweet spot. For this dataset, depth 7 or 8 is usually a good choice.

### Why tuning one at a time can mislead you

You might be tempted to pick the best n_estimators from Stage 1 and the best max_depth from Stage 2 and assume the combination is best.

Unfortunately, hyperparameters interact. The best max_depth for n_estimators = 100 might be different from the best max_depth for n_estimators = 500.

To find the best **combination**, we need to try combinations directly. That is what grid search is for.

---

## Stage 3. Grid search with cross validation

Grid search is the standard way to tune multiple hyperparameters together.

Here is the idea.

Step 1. Define a grid. The grid is a list of values for each hyperparameter you want to tune.

Step 2. Try every possible combination of values from the grid. For each combination, train a model and evaluate it.

Step 3. Pick the combination that gave the best score.

Cross validation is a way to make the evaluation more reliable. Instead of measuring on a single validation set, we split the training data into K parts (often 5). For each combination, we train on K minus 1 parts and evaluate on the remaining part. We do this K times so every part gets used for evaluation once. We average the K scores to get a single, more reliable estimate.

Scikit-learn provides `GridSearchCV` which does all of this automatically.

### The code

```python
from sklearn.model_selection import GridSearchCV

# Base model with the fixed settings that are not part of the search
base_grid_model = RandomForestClassifier(
    class_weight="balanced",
    random_state=123,
)

# The grid of values to search over.
# In real work you would use larger lists. We keep it small for demonstration.
parameters_grid = {
    "n_estimators": [100, 200],
    "max_depth": [5, 7],
}

# Set up grid search with 5 fold cross validation
grid = GridSearchCV(
    estimator=base_grid_model,
    param_grid=parameters_grid,
    scoring="roc_auc",
    cv=5,
    verbose=4,
)

# Fit on the training data
grid.fit(X_train, y_train)

# Report the best combination
print("Best parameters:", grid.best_params_)
print("Best CV ROC AUC score:", grid.best_score_)
```

Walk through the code in plain words.

We created a base model with the settings that we are not searching over, like class_weight and random_state.

We defined a grid with two values for n_estimators and two values for max_depth. That gives 2 times 2 equals 4 candidate combinations.

We set up GridSearchCV with 5 fold cross validation. So we will train and evaluate 5 times for each of the 4 combinations, totaling 20 model fits.

We told it to score using ROC AUC.

The verbose=4 setting prints helpful progress messages as it runs.

When it finishes, `grid.best_params_` tells you the winning combination.

A typical output for this dataset might look like this.

```
Best parameters: {'max_depth': 7, 'n_estimators': 200}
Best CV ROC AUC score: 0.987
```

Translation. The optimal model in this small grid uses 200 trees and a maximum depth of 7. Its average ROC AUC across the 5 cross validation folds is about 0.987.

### Reading verbose output

When you run grid search with verbose set high, you will see lines like this.

```
Fitting 5 folds for each of 4 candidates, totalling 20 fits
[CV 1/5; 1/4] START max_depth=5, n_estimators=100..............
[CV 1/5; 1/4] END   max_depth=5, n_estimators=100, score=0.984 total time=0.5s
[CV 2/5; 1/4] START max_depth=5, n_estimators=100..............
...
```

The numbers like `1/5` mean fold 1 of 5. The numbers like `1/4` mean candidate 1 of 4. So you can see exactly where in the search you are.

### Larger grids in real work

For demonstration we used a tiny grid with 4 combinations. In real work, your grid would be much bigger. Here is a more realistic grid.

```python
parameters_grid = {
    "n_estimators": [100, 200, 300, 500],
    "max_depth": [5, 7, 10, 15, None],
    "min_samples_split": [2, 5, 10],
    "max_features": ["sqrt", "log2"],
}
```

This grid has 4 times 5 times 3 times 2 equals 120 combinations. With 5 fold cross validation, that is 600 model fits. On a moderate dataset this can take many minutes or hours.

If your grid gets too big, switch to **RandomizedSearchCV**. It samples a fixed number of random combinations from the grid instead of trying all of them. You usually find a near optimal combination much faster.

---

## Other hyperparameters worth experimenting with

We focused on n_estimators and max_depth because those are the most impactful. But there are several others worth trying once you have those dialed in.

* **max_features.** Controls how many features each split considers. Try "sqrt", "log2", or specific numbers.
* **min_samples_split.** Controls how big a node has to be before it can split.
* **min_samples_leaf.** Controls how small a leaf is allowed to be.
* **bootstrap.** Whether to use bootstrap sampling. Default is True. If you set this to False, every tree sees the full training data and you get something called Extra Trees.
* **class_weight.** Critical when the classes are imbalanced.

The general advice is to tune the most impactful parameters first (n_estimators and max_depth), then see if the others make a noticeable difference.

---

## A note on training time

Random Forests are computationally expensive.

Training one tree is fast. But you are training hundreds of them, and each cross validation fold trains all of them again. With grid search, you multiply by the number of combinations.

Be aware of three things when doing this in practice.

First, training time grows linearly with n_estimators. Going from 100 trees to 500 trees takes about 5 times as long.

Second, training time grows with max_depth. Deeper trees are more expensive.

Third, scikit-learn's Random Forest can use multiple CPU cores in parallel. Set `n_jobs = -1` in your model and grid search to use all cores. This can speed things up dramatically.

```python
RandomForestClassifier(..., n_jobs=-1)
GridSearchCV(..., n_jobs=-1)
```

This is one of those small settings that gives you a 4x or 8x speedup for free. Always use it on real datasets.

---

## What we have learned in Part 2

Let us recap.

We learned what bootstrap sampling is. It is sampling with replacement, of the same size as the original dataset. About 63 percent of unique rows end up in any bootstrap. The remaining 37 percent are out of bag samples.

We learned what bagging does. It creates many bootstrap samples, trains one model per sample, and combines them by voting or averaging.

We learned what makes Random Forest different from plain bagging. At every split, it considers only a random subset of features. This makes the trees more diverse and reduces correlated errors.

We learned the most important hyperparameters of Random Forest, especially n_estimators and max_depth.

We walked through full hyperparameter tuning in three stages. We tuned n_estimators alone, max_depth alone, and then both together using grid search with cross validation.

We saw the typical patterns. More trees help up to a point, then plateau. Deeper trees help up to a point, then plateau or hurt. Tuning hyperparameters one at a time can mislead, so grid search over combinations is the right tool when you have time and compute.

In Part 3 we move to the other family of ensembles. We will learn how boosting works, why it is so different from bagging, and meet the modern champions like XGBoost, LightGBM, and CatBoost that win most data competitions today.

See you in Part 3.
