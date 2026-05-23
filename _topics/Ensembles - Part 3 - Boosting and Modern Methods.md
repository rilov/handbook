---
title: "Ensembles - Part 3 - Boosting and Modern Methods"
category: Machine Learning
order: 11
tags:
  - machine-learning
  - boosting
  - adaboost
  - gradient-boosting
  - xgboost
  - lightgbm
summary: Part 3 of the ensembles tutorial. We explain boosting from the ground up, walk through AdaBoost and Gradient Boosting in plain language, meet the modern champions like XGBoost and LightGBM, and finish with practical advice on when to use each method.
---

# Ensembles - Part 3 - Boosting and Modern Methods

## Many weak models, taught one at a time, become strong

In Part 1 we introduced the two big families of ensembles. In Part 2 we did a deep dive on bagging and Random Forests.

Now we look at the second family. **Boosting.**

Boosting is, in many real world tasks, the single most powerful classical machine learning method available today. Modern boosting algorithms like XGBoost, LightGBM, and CatBoost win most data science competitions and power countless production systems at companies of every size.

This part will teach you how boosting actually works.

We will cover four things.

1. The big idea behind boosting and why it is different from bagging.
2. AdaBoost, the original boosting algorithm.
3. Gradient Boosting, the more general and more powerful version.
4. Modern champions: XGBoost, LightGBM, CatBoost. When to use each.

We will keep the math gentle and focus on intuition first, code second.

---

## The big idea behind boosting

Bagging trains many models in parallel and averages them. The models do not know about each other.

Boosting is the opposite. Models are trained **one at a time, in sequence**, and each new model focuses on the examples that the previous models got wrong.

Here is the central idea in one sentence.

> Train a weak model. Find the data points it got wrong. Train a new model that focuses on fixing those mistakes. Combine the two. Repeat.

That is the entire game.

Each individual model is allowed to be weak. It just needs to be slightly better than random guessing. As long as each new model fixes at least some of the previous mistakes, the combined model gets better and better.

After many rounds, you have a sequence of weak models that, taken together, perform extremely well.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    D["<b>Training data</b>"]
    D --> M1["<b>Model 1</b><br/>(weak learner)"]
    M1 --> E1["<b>Mistakes 1</b>"]
    E1 --> M2["<b>Model 2</b><br/>focuses on Mistakes 1"]
    M2 --> E2["<b>Mistakes 2</b>"]
    E2 --> M3["<b>Model 3</b><br/>focuses on Mistakes 2"]
    M3 --> ED["<b>... continue<br/>for N rounds</b>"]
    ED --> F["<b>Combined model</b><br/>weighted sum of all"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class M1,M2,M3,E1,E2,ED gray
    class D,F midgray
</div>

Three things to notice.

The models depend on each other. Model 2 cannot be trained until Model 1 is done. So unlike Random Forest, you cannot train all the models in parallel.

The models are usually weak. Often they are decision trees with depth 3 or 4, sometimes called **decision stumps** when they are even smaller.

The combined prediction is a weighted sum of the individual predictions. Better models get bigger weights.

Now let us see how this idea is actually implemented. There are two big approaches. AdaBoost and Gradient Boosting.

---

## AdaBoost, the original boosting algorithm

AdaBoost stands for **Adaptive Boosting**. It was the first famous boosting algorithm, introduced in 1995. It is still useful today and is a good way to build intuition.

### How AdaBoost works

The trick in AdaBoost is to give every training example a **weight**. Every example starts with the same weight. After each round, examples that were misclassified get their weights increased. Examples that were classified correctly get their weights decreased.

The next model is trained on the same data, but with the new weights. So it pays more attention to the harder examples.

Here is the algorithm in plain words.

Step 1. Give every training example equal weight.

Step 2. Train a weak model on the weighted data.

Step 3. See which examples the model got right and which it got wrong.

Step 4. Increase the weights of the misclassified examples. Decrease the weights of the correctly classified examples.

Step 5. Compute a score for this model based on its accuracy. Better models get higher scores.

Step 6. Go back to step 2 and train a new model. The new training pays more attention to the harder examples.

Step 7. After N rounds, combine all the models. Each model contributes to the final prediction in proportion to its score.

The intuition is simple. The first model picks up the easy patterns. The second model focuses on the points where the first failed. The third focuses on the points where the first two failed. And so on. By the end, the ensemble has learned how to handle even the trickiest examples.

### A concrete picture

Imagine you have 10 training points, all with weight 1.

You train a stump (a tree with one split). It correctly classifies 7 points and misclassifies 3.

You bump up the weights of those 3 misclassified points to maybe 2 each. The 7 correct ones go down to maybe 0.5 each.

You train a new stump on this re-weighted data. Because the 3 hard points now contribute more, the new stump will try harder to get those right, even at the cost of getting one of the easy ones wrong.

You keep going. After 50 rounds, you have 50 stumps. The final prediction takes a weighted vote across all of them.

### When to use AdaBoost

AdaBoost is a fine starting point, but it has been mostly replaced by Gradient Boosting in modern practice. It is still useful as a teaching tool and works well on clean datasets.

The biggest weakness of AdaBoost is that it is sensitive to noise. If your dataset has mislabeled rows, AdaBoost will keep boosting their weight and eventually overfit to them.

That weakness is one of the reasons Gradient Boosting was invented.

---

## Gradient Boosting, the more general approach

Gradient Boosting takes the same core idea (models in sequence, each fixing the previous one's mistakes) but uses a more flexible mathematical framework.

### The key insight

Instead of re-weighting the training examples like AdaBoost does, Gradient Boosting trains each new model to predict the **residuals** of the previous models.

A residual is just the difference between the true value and the predicted value.

Suppose you are predicting house prices.

* True price of a house is 500,000.
* Model 1 predicts 450,000.
* Residual is 500,000 minus 450,000 equals 50,000.

Model 1 was off by 50,000. Now you train Model 2 to predict that error of 50,000. If Model 2 predicts 30,000, your combined prediction becomes 450,000 plus 30,000 equals 480,000. You are now off by only 20,000.

Train Model 3 to predict that 20,000. And so on.

Each new model picks up where the last one left off. The errors get smaller and smaller.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    A["<b>True value: 500</b>"]
    A --> B["<b>Model 1 predicts: 450</b><br/>residual = 50"]
    B --> C["<b>Model 2 predicts<br/>the residual: 30</b><br/>combined = 480<br/>residual = 20"]
    C --> D["<b>Model 3 predicts<br/>the residual: 15</b><br/>combined = 495<br/>residual = 5"]
    D --> E["<b>Continue until<br/>residuals are small</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class A,E midgray
    class B,C,D gray
</div>

That is the whole idea. Train each new model to predict what the previous models could not explain.

For classification problems, the math is slightly different (we use log loss residuals instead of straight differences) but the spirit is the same.

### Why it is called gradient

The name comes from the fact that residuals are mathematically related to the gradient of the loss function. The algorithm essentially performs gradient descent in function space.

You do not need to understand that to use it. The mental model of "fit the next model to the residuals of the previous" is enough for almost all practical purposes.

### Important hyperparameters in Gradient Boosting

Gradient Boosting has more knobs than Random Forest, and they really matter. The big ones are these.

**n_estimators.** Number of trees. Unlike Random Forest, more is not always better here. Too many trees in Gradient Boosting can overfit.

**learning_rate.** This is new. It controls how much each new tree contributes to the combined prediction. A smaller learning rate makes each tree contribute less, which means you need more trees overall but you usually get better generalization.

**max_depth.** How deep each tree can go. Gradient Boosting trees are usually shallow. Common values are 3 to 6. Much deeper than that and they tend to overfit.

**subsample.** Fraction of training data to use for each tree. Setting this to less than 1.0 (like 0.8) introduces randomness similar to bagging and helps prevent overfitting. This is sometimes called **stochastic gradient boosting**.

The interplay between **n_estimators** and **learning_rate** is the most important one to understand.

A common pattern. Set learning_rate to something small like 0.05 or 0.1, then crank up n_estimators until validation performance stops improving. The smaller the learning rate, the more trees you need, but the better the final model.

---

## The modern champions, XGBoost, LightGBM, CatBoost

Plain Gradient Boosting was great, but starting around 2014, three optimized libraries took the world by storm. They are essentially highly engineered versions of Gradient Boosting with clever tricks for speed and accuracy.

### XGBoost

XGBoost stands for **Extreme Gradient Boosting**. Released in 2014, it became the dominant algorithm in Kaggle competitions almost overnight.

What makes it different.

* It uses smarter regularization to fight overfitting.
* It handles missing values automatically.
* It uses second order information from the loss function (not just gradients but also curvature) for more accurate fits.
* It is heavily parallelized for speed, even though boosting is inherently sequential.
* It supports GPU training for very large datasets.

If you do not know which tool to reach for on a tabular dataset, XGBoost is almost always a safe choice.

### LightGBM

Released by Microsoft in 2017. Designed to be even faster and more memory efficient than XGBoost.

What makes it different.

* It grows trees leaf-wise instead of level-wise. That sounds technical but the practical effect is that it builds trees faster and often more accurately on big datasets.
* It uses a clever sampling trick (Gradient-based One-Side Sampling) to focus on the most informative examples.
* It bins continuous features for speed.

LightGBM tends to be the fastest of the three on large datasets. On small or medium datasets, the difference may not matter much.

### CatBoost

Released by Yandex in 2017. Designed to handle categorical features especially well.

What makes it different.

* It deals with categorical features without requiring you to do one hot encoding manually. It uses a clever statistical encoding internally.
* It has built in protections against a subtle problem called target leakage that affects naive categorical encodings.
* It often produces good results with minimal tuning.

CatBoost is a great choice when your data has lots of categorical columns or when you do not want to spend much time preprocessing.

### How to choose between them

A simple rule of thumb.

* **Small or medium dataset, mostly numeric.** XGBoost is fine. LightGBM also fine.
* **Big dataset, want it fast.** LightGBM.
* **Lots of categorical columns.** CatBoost.
* **Just starting out.** XGBoost. It is the most popular and has the most learning material.

In real practice, many practitioners try two or three of them and pick whichever works best on their specific problem.

---

## A simple Python example with Gradient Boosting

Let us train a Gradient Boosting model the same way we trained a Random Forest in Part 2.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score

# Load data
data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.3, random_state=123, stratify=y
)

# Train a baseline gradient boosting model
gb = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=3,
    random_state=123,
)
gb.fit(X_train, y_train)

proba_val = gb.predict_proba(X_val)[:, 1]
print("Validation ROC AUC:", roc_auc_score(y_val, proba_val))
```

Notice how similar the code is to Random Forest. Same scikit-learn pattern: create a model, fit, predict. The only difference is the model class and the hyperparameters.

### Tuning Gradient Boosting

The same grid search workflow from Part 2 works for Gradient Boosting.

```python
parameters_grid = {
    "n_estimators": [100, 200, 500],
    "learning_rate": [0.01, 0.05, 0.1],
    "max_depth": [3, 5, 7],
}

grid = GridSearchCV(
    estimator=GradientBoostingClassifier(random_state=123),
    param_grid=parameters_grid,
    scoring="roc_auc",
    cv=5,
    verbose=2,
    n_jobs=-1,
)

grid.fit(X_train, y_train)

print("Best parameters:", grid.best_params_)
print("Best CV ROC AUC:", grid.best_score_)
```

This searches 3 times 3 times 3 equals 27 combinations across 5 cross validation folds, so 135 fits total. Be patient on large datasets.

### Using XGBoost instead

If you want to use XGBoost, install it first.

```bash
pip install xgboost
```

Then the code is almost the same as scikit-learn.

```python
from xgboost import XGBClassifier

xgb = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=4,
    random_state=123,
    use_label_encoder=False,
    eval_metric="logloss",
)
xgb.fit(X_train, y_train)

proba_val = xgb.predict_proba(X_val)[:, 1]
print("XGBoost Validation ROC AUC:", roc_auc_score(y_val, proba_val))
```

XGBoost usually gives a small but real improvement over scikit-learn's GradientBoostingClassifier on most datasets, plus it is much faster on big data.

---

## Bagging vs Boosting, when to use which

Now that we have seen both families, here is a practical guide for choosing.

| When you want this | Reach for this |
|---|---|
| Maximum accuracy on tabular data | Boosting (XGBoost, LightGBM, CatBoost) |
| A quick robust baseline | Random Forest |
| Easy to tune, hard to break | Random Forest |
| Highly parallelizable training | Random Forest |
| Sensitive to noisy labels | Random Forest |
| Tons of categorical features | CatBoost |
| Massive dataset, fast training | LightGBM |
| Built in handling of missing values | XGBoost or LightGBM |
| Maximum interpretability | Single decision tree |

A useful workflow.

Step 1. Train a Random Forest with default settings. This gives you a baseline.

Step 2. Train an XGBoost or LightGBM with default settings. Compare to baseline.

Step 3. Tune the better of the two using grid search or randomized search.

Step 4. Compare to your business requirements. Decide if more tuning is worth the effort.

This workflow handles most real world tabular data problems very well.

---

## Common pitfalls with boosting

Boosting is powerful but it has some traps. Watch out for these.

### Overfitting silently

Unlike Random Forest, boosting can absolutely overfit. If you train too many trees with too high a learning rate and too deep individual trees, you can fit the noise perfectly while doing poorly on new data.

Always use a validation set or cross validation to check generalization.

### Sensitivity to hyperparameters

Boosting has more knobs than Random Forest, and they interact in subtle ways. Spend time tuning learning_rate and n_estimators together.

A useful trick. Use **early stopping**. Train a model with many trees, but stop adding trees as soon as validation performance stops improving. Most modern boosting libraries support this directly.

### Slow training without parallelism

Boosting is inherently sequential. You cannot just throw more cores at it the way you can with Random Forest. The smart libraries (XGBoost, LightGBM) parallelize the work within each tree, but they cannot parallelize across trees.

For huge datasets, choose libraries that support GPU training (XGBoost and LightGBM both do).

### Sensitivity to noisy labels

Boosting will keep boosting the weight of misclassified examples. If those examples are misclassified because they are mislabeled in the data (not because they are genuinely hard), boosting will fit the noise.

This is one of the few situations where Random Forest is actually more robust than boosting.

---

## What we have learned across the whole tutorial

Three parts. Let us bring it all together.

**From Part 1.** An ensemble combines many models into a single prediction. They work because errors cancel out when models disagree, and because they can lower bias and variance at the same time. There are two main families. Bagging trains models in parallel on bootstrap samples. Boosting trains models in sequence, each one fixing the previous one's mistakes.

**From Part 2.** Bagging is built on bootstrap sampling, which is sampling with replacement. Random Forest extends bagging by also randomizing which features each split considers. Tuning Random Forest mainly involves n_estimators and max_depth. Grid search with cross validation is the standard way to tune combinations of hyperparameters.

**From Part 3.** Boosting trains weak models in sequence. AdaBoost re-weights the training data to focus on hard examples. Gradient Boosting trains each new tree on the residuals of the previous ones. Modern champions like XGBoost, LightGBM, and CatBoost dominate most data competitions. They can overfit if not tuned carefully, but they almost always give the best results on tabular data.

---

## Where to go from here

You now have the foundation to use the most powerful classical machine learning tools available today.

A natural learning sequence from here.

* Try XGBoost, LightGBM, and CatBoost on the same dataset and compare them.
* Learn about **early stopping** to automatically pick the right number of trees.
* Learn about **feature importance** in tree ensembles.
* Learn about **SHAP values** for explaining individual predictions of complex tree models.
* Learn about **stacking**, which is yet another ensemble technique that combines models from completely different families.

But the single most useful thing you can do right now is to grab a tabular dataset you care about and try a Random Forest, a Gradient Boosting, and an XGBoost on it. Tune them. Compare them. The intuition you build from running real models is worth ten more tutorials.

That is the end of the ensembles tutorial.

Decision Trees in three parts. Ensembles in three parts. Together, these six tutorials cover almost everything you need to dominate classical machine learning on tabular data.

Good luck and have fun.
