---
title: "09. Decision Trees - Part 3 - Training and Demonstration"
category: Machine Learning
order: 9
tags:
  - machine-learning
  - decision-trees
  - overfitting
  - pruning
  - python
  - scikit-learn
summary: Part 3 of the decision trees tutorial. We walk through the full training process, talk about overfitting and pruning, discuss real world advantages and disadvantages, and then build a working decision tree in Python on a real dataset.
---

# Decision Trees - Part 3 - Training and Demonstration

## Putting it all together with real code

Welcome to the final part of the decision trees tutorial.

In Part 1 we learned what decision trees are and why people use them.

In Part 2 we learned how the algorithm measures impurity and chooses splits using Gini, entropy, and information gain.

Now we are going to put everything together.

Here is what we will cover in this part.

1. The full training process, end to end.
2. The biggest danger with decision trees, which is overfitting, and how to prevent it.
3. The advantages and disadvantages you should know before using decision trees in real work.
4. A complete Python demonstration, where we train, visualize, and evaluate a decision tree on a real dataset.

Let us start by zooming out and looking at the full training process.

---

## Segment 4. The decision tree training process

We have seen pieces of the training process in earlier parts. Let us now describe it as one full procedure.

### The full algorithm in plain words

Step 1. Start with the entire training dataset at the root.

Step 2. Compute the impurity of the current group, using Gini or entropy.

Step 3. Try every possible question you could ask. For numeric features, try several thresholds. For categorical features, try each category. For each candidate question, compute the information gain.

Step 4. Pick the question with the highest information gain. That becomes the split at this node.

Step 5. Split the data into the resulting child groups, one group per branch.

Step 6. For each child group, repeat steps 2 through 5. This is recursion. Each child becomes its own little problem.

Step 7. At every step, check whether you should stop. If yes, turn the current node into a leaf and assign it a final label.

### Choosing the label at a leaf

When the algorithm stops at a leaf, it needs to assign a final prediction.

For classification, the rule is simple. Look at all the training points that ended up at this leaf. Whichever class is the majority becomes the prediction.

For example, if a leaf contains 8 buyers and 2 non buyers, the leaf predicts "buyer". When a new data point lands on this leaf, the prediction will be "buyer".

For regression, where the answer is a number, the leaf takes the average of the training points that landed there.

### Stopping rules in more detail

We mentioned stopping rules in Part 1. Let us look at them more carefully because they really matter.

There are four common stopping rules. You can use them alone or together.

**Maximum depth.** Stop splitting once the tree has reached a certain depth. Depth means how many levels of questions the tree has. A depth of 1 is a single question. A depth of 5 is five levels of questions stacked up.

**Minimum samples to split.** Refuse to split a group if it has too few examples. For instance, do not split any group that has fewer than 20 points.

**Minimum samples per leaf.** Do not create a leaf that would have fewer than some minimum number of training points. For instance, every leaf must contain at least 5 points.

**Minimum information gain.** Do not bother splitting if the best possible split barely improves purity. For instance, if the gain is less than 0.001, just stop.

Each of these rules is a way of saying, "do not try too hard to fit every tiny detail of the training data." That brings us to the most important concept in this part.

### A note about how the algorithm picks the best split

The algorithm is greedy. That means at each node, it picks whatever split looks best right now. It does not plan ahead.

This is sometimes a weakness. The split that looks best at the top might force bad choices at the bottom. A truly optimal tree would consider the whole structure together, but that is far too expensive to compute.

In practice, greedy splitting works well. Most decision tree algorithms you will ever use are greedy.

---

## The biggest danger, overfitting

Overfitting is the single most important problem you need to understand about decision trees.

It is also the reason a lot of beginners get burned the first time they use them.

### What overfitting actually means

Suppose you let a decision tree grow without any stopping rules. It will keep splitting until every leaf contains exactly one training point. The tree will get perfect accuracy on the training data.

That sounds great. But it is actually terrible.

A tree that has memorized every training point has not learned the underlying pattern. It has learned the random noise. When you give it a new data point that it has not seen before, it will probably make a bad prediction, because the leaf rules are too narrow and oddly shaped to match new examples.

This is overfitting. The model performs amazingly on training data and poorly on new data.

A simple picture.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    A["<b>Underfit tree</b><br/>(too simple)<br/>misses real patterns"]
    B["<b>Just right tree</b><br/>captures the pattern<br/>ignores the noise"]
    C["<b>Overfit tree</b><br/>(too complex)<br/>memorizes noise"]
    A --> B
    B --> C
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class A,C gray
    class B midgray
</div>

We want the middle one. The tree should be just deep enough to capture the real signal in the data, but not so deep that it captures random noise.

### How to fight overfitting

There are two main strategies. The first is to stop the tree from growing too big in the first place. The second is to let it grow and then trim it back.

#### Strategy 1. Pre pruning

Pre pruning means setting stopping rules so the tree never gets too big.

This is the same as the stopping rules we just discussed. Limit the maximum depth. Require a minimum number of samples per leaf. Require a minimum information gain. These all act as guardrails.

Pre pruning is easy to understand and easy to implement. It is the most common approach in practice.

#### Strategy 2. Post pruning

Post pruning means letting the tree grow fully, then trimming branches that do not seem useful.

The idea is to take each subtree and ask, "if I replace this whole subtree with a single leaf, does the model get worse on a validation set?" If it does not get worse, remove the subtree.

Post pruning can produce slightly better trees than pre pruning, but it is more work to implement.

Both strategies have the same goal. Make the tree simple enough that it generalizes well to new data, but rich enough that it captures the real patterns.

### The single most useful hyperparameter to tune

Out of all the knobs you can turn, the single most useful one for a decision tree is **maximum depth**.

Start by trying values like 3, 5, 7, and 10. Train the tree at each depth. Measure performance on a separate validation set. Pick the depth that gives the best validation score.

This one step alone usually solves most overfitting problems.

---

## Segment 5. Advantages and disadvantages

Now that we understand how decision trees are trained, let us be honest about where they shine and where they struggle.

### Advantages

**They are easy to interpret.** You can literally draw the tree and explain it to anyone. This is rare in machine learning and very valuable.

**They need very little data preparation.** No scaling, no normalization, no one hot encoding of categorical features (with some libraries). Compared to most other algorithms, decision trees are very forgiving.

**They handle mixed data types.** Numeric and categorical features can sit side by side. The algorithm does not care.

**They handle non linear relationships naturally.** As we saw in Part 1, the tree can build different rules for different parts of the data without any special effort.

**They are fast to predict with.** Walking down a tree is just a series of comparisons. Even a large tree predicts in microseconds.

**They show feature importance.** After training, you can ask the tree which features contributed the most to the splits. This gives you a free ranking of which features actually mattered.

**They are the foundation for ensemble methods.** Once you understand a single tree, you are most of the way to understanding Random Forests, Gradient Boosting, XGBoost, LightGBM, and CatBoost.

### Disadvantages

**They overfit easily.** This is by far the biggest weakness. A single decision tree, left unchecked, will memorize the training data. We covered this in detail above.

**They are unstable.** A small change in the training data can lead to a completely different tree structure. This makes single trees feel fragile.

**They are biased toward features with more possible splits.** A feature that can take on many values gets more chances to be picked as a split point. This can sometimes make less informative features look more important than they really are.

**They struggle with linear relationships.** If the true relationship between two features is a clean straight line, a decision tree has to approximate it using many tiny axis aligned splits. A linear model would do this in one line of code.

**A single tree is rarely state of the art.** For most real world tasks, you will get better performance from an ensemble like Random Forest or Gradient Boosting. The single decision tree is great for learning and for interpretability, but it usually gets beaten by the team versions.

### A simple rule of thumb

Use a single decision tree when:

* You need to explain the model to humans.
* You have a small dataset.
* You want a quick baseline.
* You need fast predictions on simple data.

Move to an ensemble like Random Forest or XGBoost when:

* You want maximum accuracy.
* The dataset is medium or large.
* You can afford slightly less interpretability.

In real production work, ensembles win most of the time. But understanding the single tree comes first.

---

## Segment 6. Decision trees, a Python demonstration

Time to make this real with actual code. We will use scikit-learn, the most popular machine learning library in Python.

If you want to follow along, install it with this command in your terminal:

```bash
pip install scikit-learn matplotlib pandas
```

We will use a famous beginner dataset called the Iris dataset. It contains measurements of 150 iris flowers from three different species. Our job is to predict the species from four measurements: sepal length, sepal width, petal length, and petal width.

### Step 1. Load the data

```python
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target, name="species")

print("Shape of X:", X.shape)
print("First few rows:")
print(X.head())
print("Class labels:", iris.target_names)
```

X is a table with 150 rows and 4 columns. Each row is one flower. Each column is one measurement. y is the label, a number from 0 to 2 representing the species.

### Step 2. Split into training and test sets

We never train and evaluate on the same data. We want to measure how well the tree handles new flowers it has never seen.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print("Training size:", X_train.shape[0])
print("Test size:", X_test.shape[0])
```

We keep 70 percent for training and 30 percent for testing. The `stratify` argument makes sure both sets have the same proportion of each species.

### Step 3. Train a decision tree

```python
from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(
    criterion="gini",
    max_depth=3,
    random_state=42
)

tree.fit(X_train, y_train)
print("Training complete.")
```

We set `max_depth` to 3. That means the tree can have at most 3 levels of questions. This is one of the most important hyperparameters to control overfitting.

We set `criterion` to "gini" so the tree uses Gini impurity. We could also use "entropy" if we preferred.

### Step 4. Evaluate the tree

```python
from sklearn.metrics import accuracy_score, classification_report

train_pred = tree.predict(X_train)
test_pred = tree.predict(X_test)

print("Training accuracy:", accuracy_score(y_train, train_pred))
print("Test accuracy:", accuracy_score(y_test, test_pred))

print("\nDetailed test report:")
print(classification_report(y_test, test_pred, target_names=iris.target_names))
```

A typical result is something like 97 percent training accuracy and 95 percent test accuracy. The two numbers are close, which is a good sign. It means the tree is not severely overfitting.

If you saw 100 percent training accuracy but only 70 percent test accuracy, you would suspect overfitting and try a smaller `max_depth`.

### Step 5. Visualize the tree

This is where decision trees really shine. We can literally draw the tree we just trained.

```python
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 8))
plot_tree(
    tree,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    rounded=True
)
plt.title("Decision Tree on the Iris Dataset")
plt.show()
```

When you run this, you get a picture of the actual tree. You can see every question, every split, and every leaf. You can follow any data point from the top to the bottom and see exactly why the tree made its prediction.

Try this yourself. Pick a single test flower, walk through the tree by hand, and see if your manual walk matches what `tree.predict` returned.

### Step 6. See which features mattered most

Decision trees give us a free ranking of feature importance based on how much each feature was used for splits.

```python
import pandas as pd

importances = pd.Series(
    tree.feature_importances_,
    index=iris.feature_names
).sort_values(ascending=False)

print("Feature importance:")
print(importances)
```

You will likely see that petal length and petal width carry most of the predictive power. Sepal measurements are useful but less so. This kind of insight is hard to get from many other algorithms.

### Step 7. Tune the depth using a loop

We picked `max_depth = 3` somewhat arbitrarily. Let us try a few values and see which one works best.

```python
for depth in [1, 2, 3, 4, 5, 6, 10, None]:
    t = DecisionTreeClassifier(max_depth=depth, random_state=42)
    t.fit(X_train, y_train)
    train_acc = t.score(X_train, y_train)
    test_acc = t.score(X_test, y_test)
    print(f"Depth={depth!s:<5}  train_acc={train_acc:.3f}  test_acc={test_acc:.3f}")
```

A typical output:

```
Depth=1      train_acc=0.667  test_acc=0.622
Depth=2      train_acc=0.952  test_acc=0.933
Depth=3      train_acc=0.971  test_acc=0.956
Depth=4      train_acc=0.990  test_acc=0.956
Depth=5      train_acc=1.000  test_acc=0.956
Depth=6      train_acc=1.000  test_acc=0.933
Depth=10     train_acc=1.000  test_acc=0.933
Depth=None   train_acc=1.000  test_acc=0.933
```

Notice what is happening. At very low depth, the tree is too simple and both accuracies are low. As depth grows, training accuracy keeps climbing toward 1.0, but test accuracy stops improving and may even drop a little.

That is overfitting in action.

The sweet spot in this example is around depth 3 to 4. Going deeper makes the tree memorize the training data without helping on the test data.

This loop is the single most useful piece of code in this tutorial. Whenever you train a decision tree, run something like this to find a good depth.

### Step 8. Make a prediction on a new flower

```python
new_flower = [[5.1, 3.5, 1.4, 0.2]]
predicted_class = tree.predict(new_flower)[0]
predicted_probs = tree.predict_proba(new_flower)[0]

print("Predicted species:", iris.target_names[predicted_class])
print("Class probabilities:", dict(zip(iris.target_names, predicted_probs)))
```

The tree returns both a class and a probability distribution. The probabilities come from the proportions at the leaf where this flower landed. If a leaf contains 19 setosa and 1 versicolor, the tree returns probabilities of about 0.95 and 0.05.

---

## A quick summary of everything we have learned

Let us bring it all together with a final summary of the three parts.

**From Part 1.** A decision tree is a flowchart of yes or no questions that ends in a prediction. The top question is the root, middle questions are internal nodes, and the bottom predictions are the leaves. Decision trees are popular because they look like human reasoning, they handle messy data well, they can capture non linear patterns, and they are easy to explain.

**From Part 2.** A group is pure if all its labels are the same. The algorithm measures impurity using Gini or entropy. To choose a split, it compares the impurity before and after, and picks the question that produces the highest information gain.

**From Part 3.** The full training process repeats split selection from the top down until a stopping rule fires. The biggest danger is overfitting, which we control with stopping rules like maximum depth. Decision trees have many strengths and a few weaknesses. In real Python code, training a tree is just a few lines, and the resulting model is one of the most interpretable in all of machine learning.

---

## Where to go next

Decision trees alone are powerful, but they are usually the first stop, not the last.

Once you are comfortable with single trees, the natural next topics are:

* **Random Forests.** Train many decision trees on random samples of the data and average their predictions. This usually gives a much more accurate and stable model.
* **Gradient Boosting.** Train decision trees in sequence, where each new tree tries to correct the mistakes of the previous ones. Modern libraries like XGBoost, LightGBM, and CatBoost are based on this idea and dominate many data competitions.
* **Pruning techniques.** Learn about cost complexity pruning, which is the standard way to post prune a tree.
* **Handling missing values and categorical features.** Different libraries handle these in different ways. Knowing the details makes you a more confident practitioner.

If you understand decision trees deeply, all of these become much easier to learn.

That is the end of the tutorial.

The best thing you can do right now is open a notebook, load a dataset, train a decision tree, visualize it, and play with the depth. The intuition you build by actually running this code is worth more than any amount of reading.

Good luck and have fun.
