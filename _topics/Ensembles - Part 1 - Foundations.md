---
title: "10. Ensembles - Part 1 - Foundations of Ensemble Learning"
category: Machine Learning
order: 10
tags:
  - machine-learning
  - ensembles
  - bagging
  - boosting
  - bias-variance
summary: A simple introduction to ensemble learning. Why combining many weak models beats relying on one strong model. The wisdom of crowds, bias and variance, and the two big families of ensembles.
---

# Ensembles - Part 1 - Foundations of Ensemble Learning

## Why many small models beat one big model

In Part 3 of the Decision Trees tutorial we said something important.

We said that a single decision tree is good for learning and easy to interpret, but in real production work you almost always get better results from an ensemble like Random Forest or Gradient Boosting.

This tutorial is about why that is true, and how those methods actually work.

This is Part 1 of a three part tutorial on ensembles.

* **Part 1.** What ensembles are, why they work, and the two big families.
* **Part 2.** Bagging and Random Forests, with full hyperparameter tuning.
* **Part 3.** Boosting, including AdaBoost, Gradient Boosting, and XGBoost.

By the end of Part 1 you will have a strong intuition for why combining many models is so powerful. We will not write code yet. The goal of this part is purely understanding.

Let us start with a story that captures the whole idea in one paragraph.

---

## A story about a county fair

In 1906 there was a small county fair in England. One of the events was guessing the weight of an ox after it had been slaughtered and prepared. Around 800 people each wrote down a guess on a piece of paper. The closest guess won a prize.

A statistician named Francis Galton looked at the slips afterwards. He expected the guesses to be all over the place, and he was right. Some people guessed way too high. Others guessed way too low. Almost no individual guess was very accurate.

But then he did something curious. He took the **average** of all 800 guesses.

The average came out to 1,197 pounds.

The actual weight of the ox was 1,198 pounds.

The crowd, taken as a whole, was off by one pound. Even though no single person was an expert, the combined wisdom of the crowd was nearly perfect.

That is the central idea behind ensemble learning.

You do not need one perfect model. You can combine many imperfect models, and as long as they are imperfect in different ways, the average of their predictions will be very close to the truth.

---

## What an ensemble actually is

An ensemble is just a collection of models that work together to make a single prediction.

Each model in the collection is called a **base model** or a **base learner**. The base models can be decision trees, but they do not have to be. They can be any model.

The ensemble makes its final prediction by combining the predictions of all the base models.

For classification, this combination is usually a vote. Each base model votes for a class, and the class with the most votes wins.

For regression, the combination is usually an average. Each base model produces a number, and the ensemble returns the average of those numbers.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    D["<b>New data point</b>"]
    D --> M1["<b>Model 1</b><br/>predicts: yes"]
    D --> M2["<b>Model 2</b><br/>predicts: yes"]
    D --> M3["<b>Model 3</b><br/>predicts: no"]
    D --> M4["<b>Model 4</b><br/>predicts: yes"]
    D --> M5["<b>Model 5</b><br/>predicts: no"]
    M1 --> V["<b>Combine the predictions</b><br/>(vote or average)"]
    M2 --> V
    M3 --> V
    M4 --> V
    M5 --> V
    V --> F["<b>Final prediction: yes</b><br/>(3 votes for yes, 2 for no)"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class M1,M2,M3,M4,M5 gray
    class D,V,F midgray
</div>

That is the whole structure. Many models, one combined prediction.

The interesting question is, why does this work better than a single big model?

---

## Why ensembles work, the two big reasons

There are two reasons ensembles tend to outperform single models.

### Reason 1. Errors cancel out

Imagine each base model is right 70 percent of the time and wrong 30 percent of the time. That is a fairly weak model on its own.

But suppose you have 5 such models, and they make their mistakes on **different** data points. So when one model is wrong, the others might still be right.

When you take a vote, the majority will be right more often than any single model.

Here is some basic intuition. With 5 independent models that are each 70 percent accurate, the chance that at least 3 of them get a given prediction right is around 84 percent. The vote is more accurate than any individual model.

The catch is in the word "independent." If all the models make exactly the same mistakes, voting gives you nothing. The models need to be different from each other in some way, so their errors point in different directions.

This is the core trick. **Combine many models that fail in different ways.**

### Reason 2. They balance bias and variance

This is the more technical reason, but the intuition is simple. Let me explain bias and variance first.

**Bias** is how wrong a model is on average. A model with high bias makes the same kinds of mistakes over and over because it is too simple to capture the real pattern.

**Variance** is how much a model's predictions change when you train it on slightly different data. A model with high variance is very sensitive to the training data. If you change a few rows, the model behaves completely differently.

Every model has some bias and some variance. The total error of a model is roughly bias plus variance. To get accurate predictions, you need both to be low.

Here is the problem. Most models force a tradeoff.

A simple model like linear regression has low variance (it does not change much when you change the data) but high bias (it cannot capture complex patterns).

A complex model like a deep decision tree has low bias (it can capture almost any pattern) but high variance (small changes in the data lead to wildly different trees).

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    A["<b>Simple model</b><br/>(linear regression,<br/>shallow tree)<br/><br/>High bias<br/>Low variance"]
    B["<b>Complex model</b><br/>(deep tree,<br/>deep neural net)<br/><br/>Low bias<br/>High variance"]
    C["<b>Ensemble</b><br/>(combines models)<br/><br/>Low bias<br/>Low variance"]
    A --> C
    B --> C
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class A,B gray
    class C midgray
</div>

Ensembles solve this tradeoff in two different ways depending on the family.

* **Bagging** takes complex high variance models and reduces their variance by averaging.
* **Boosting** takes simple high bias models and reduces their bias by combining them sequentially.

Both families end up with low bias and low variance, but they get there from different starting points.

That brings us to the two big families of ensembles.

---

## The two big families of ensembles

There are two main ways to build an ensemble. Almost every popular ensemble method is in one of these two families.

### Family 1. Bagging

Bagging stands for **Bootstrap Aggregating**.

The idea is simple. Train many copies of the same kind of model, but train each copy on a slightly different version of the training data. Then combine their predictions.

The "slightly different version" is created by random sampling with replacement. We will go into the details in Part 2.

Here is the key property of bagging. All the models are trained **in parallel**. They do not know about each other. They do not depend on each other. You could literally train them on different machines at the same time.

Examples of bagging methods:

* **Random Forest.** The most famous bagging method. Builds many decision trees on different bootstrap samples of the data. Each tree also picks a random subset of features at every split. We will study this in detail in Part 2.
* **Extra Trees.** Similar to Random Forest but adds even more randomness in the splits.

Bagging is especially good when the base model has high variance, like a deep decision tree.

### Family 2. Boosting

Boosting takes a different approach.

The idea is to train models **in sequence**. The first model tries to predict the target. The second model focuses on the mistakes of the first model. The third model focuses on the mistakes of the first two. And so on.

Each new model is built specifically to fix what the previous models got wrong.

The base models in boosting are usually weak. They are often simple shallow trees with just a few splits. The power comes from combining many weak models, each correcting the errors of the previous ones.

Examples of boosting methods:

* **AdaBoost.** The first famous boosting method. Each new model focuses on the data points that previous models got wrong.
* **Gradient Boosting.** A more general approach where each new model fits the residuals (errors) of the previous models.
* **XGBoost, LightGBM, CatBoost.** Modern, highly optimized versions of gradient boosting. These dominate most data science competitions and many production systems.

Boosting is especially good when the base model has high bias, like a shallow decision tree.

### Bagging vs Boosting at a glance

| Aspect | Bagging | Boosting |
|---|---|---|
| How models are trained | In parallel | In sequence |
| What each model sees | A random sample of data | The mistakes of previous models |
| Base model strength | Strong (deep trees) | Weak (shallow trees) |
| Reduces mostly | Variance | Bias |
| Sensitive to noisy data | Less | More |
| Famous examples | Random Forest, Extra Trees | AdaBoost, Gradient Boosting, XGBoost |
| Easy to parallelize | Yes | No |

Both families are powerful. Both have their place. Modern competitions and production systems use both, sometimes combined.

---

## Why decision trees are the most common base model

You will notice that almost every popular ensemble uses decision trees as the base model. There is a reason for that.

Decision trees have three properties that make them perfect raw material for ensembles.

**Property 1. They are unstable.** A small change in the training data leads to a very different tree. We mentioned this as a weakness of single trees. But for bagging, this is actually a strength. We need our base models to disagree with each other so the average has meaning. Trees disagree easily.

**Property 2. They are flexible.** A deep tree can fit almost any pattern. A shallow tree is a good weak learner. You can dial the strength up or down with a single hyperparameter, the depth.

**Property 3. They are fast.** Training a single tree is quick. That matters when you are training hundreds or thousands of them.

A linear regression model has none of these properties. It is stable. It is rigid. It does not benefit from ensembling much because all 100 copies look almost identical.

That is why nearly every ensemble book, library, and tutorial features trees front and center. Trees are made for ensembling.

---

## A simple way to picture the difference

Here is one image that summarizes the two families.

Imagine you are taking a test. You can ask your friends for help.

**Bagging is like getting answers from many friends in parallel and taking a majority vote.**

You ask 10 friends the same question. Each friend studied a different chapter of the textbook. Each friend gives you their answer independently. You go with whatever most of them say.

**Boosting is like getting help from friends one at a time, where each friend focuses on what the previous friends got wrong.**

You ask the first friend. They get some questions right and some wrong. You write down the mistakes. The next friend specifically studies the mistakes and tries to fix them. The next friend looks at what is still wrong, and so on.

Both strategies can lead to a good final answer. They just do it differently.

---

## What we have learned in Part 1

Let us recap.

We learned that an ensemble is a collection of models that work together to make a single prediction. The combination is usually a vote for classification or an average for regression.

We learned that ensembles work for two reasons. First, when models make different kinds of mistakes, those errors tend to cancel out when combined. Second, ensembles can reduce both bias and variance at the same time, which is hard for a single model to do.

We learned that there are two big families of ensembles. Bagging trains many models in parallel on random samples of the data. Boosting trains models in sequence, where each new model tries to fix the mistakes of the previous ones.

We learned why decision trees are the most popular base model. They are unstable, flexible, and fast, which makes them perfect raw material for ensembles.

In Part 2 we will go deep on bagging. We will explain bootstrap sampling carefully, build up to the Random Forest algorithm, and walk through the full hyperparameter tuning process step by step. We will also write Python code to train and tune a real Random Forest model.

In Part 3 we will go deep on boosting, including AdaBoost, Gradient Boosting, and the modern champions like XGBoost.

See you in Part 2.
