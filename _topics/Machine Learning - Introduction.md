---
title: "01. Machine Learning - Introduction"
category: Machine Learning
order: 1
tags:
  - machine-learning
  - introduction
  - getting-started
summary: A friendly, story-style introduction to Machine Learning. What it is, how it differs from regular programming, the three big types, the full ML pipeline, and the key ideas every beginner should know. With diagrams.
---

# Machine Learning - Introduction

## A short story to start with

Imagine you want to teach a child to recognize cats.

You could try writing down rules. "Cats have four legs. They have whiskers. They have pointy ears. They are usually small. They have a tail."

The child quickly runs into trouble. A dog has four legs too. A rabbit has whiskers. A fox has pointy ears. Your rules keep breaking, and every time they break you have to add a new rule. "Cats have a tail, but not the kind a fox has." After a while you have a giant pile of rules, and the child still gets confused.

Now try a different approach. Just show the child hundreds of pictures of cats. Then show them hundreds of pictures that are not cats. After a while, the child can spot a cat in a picture they have never seen before. They cannot tell you exactly what rules they used. They just know.

That second approach is **machine learning**.

We do not write rules. We show the computer examples, and the computer figures out the patterns on its own.

This page is your friendly introduction to that idea. We will keep it simple, use diagrams, and stay focused on the big picture. By the end you will know what ML is, how it differs from regular programming, the three big flavours of ML, and the steps to actually do it.

---

## Traditional Programming vs Machine Learning

The clearest way to understand ML is to compare it to normal programming.

In **traditional programming**, you write the rules. The computer follows them.

In **machine learning**, you provide the data and the answers. The computer writes the rules for you.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    subgraph T["Traditional Programming"]
        TR["<b>Rules</b><br/>(written by you)"]
        TD["<b>Data</b>"]
        TR --> TC["<b>Computer</b>"]
        TD --> TC
        TC --> TA["<b>Answers</b>"]
    end

    subgraph M["Machine Learning"]
        MD["<b>Data</b>"]
        MA["<b>Answers</b>"]
        MD --> MC["<b>Computer</b>"]
        MA --> MC
        MC --> MR["<b>Rules</b><br/>(learned by the<br/>computer)"]
    end
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class TR,TD,MD,MA gray
    class TC,TA,MC,MR midgray
</div>

Notice how the arrows flip. In traditional programming, rules and data go in, answers come out. In ML, data and answers go in, rules come out. Once you have those learned rules, you can use them on new data.

### A concrete example

Say you want to filter spam emails.

**Traditional way.** You write rules. "If the subject contains FREE in all caps, mark it spam. If the sender is on this blacklist, mark it spam. If there are more than 5 dollar signs, mark it spam." Spammers adapt. You add more rules. Forever.

**ML way.** You collect 50,000 emails, each labelled as spam or not spam. You hand them to an algorithm. It learns the patterns. Now any new email can be classified automatically, and when spammers change their tactics, you just retrain the model with newer examples.

---

## Real-world ML you already use every day

Machine learning is not some far-off technology. You probably touched five different ML systems before breakfast.

* **Email spam filters** learn what spam looks like from billions of examples.
* **Netflix and YouTube recommendations** learn what you might like based on what you and similar viewers watched.
* **Phone face unlock** learns your face from a handful of training photos.
* **Map navigation apps** learn typical traffic patterns to estimate arrival times.
* **Photo search** lets you type "beach" and finds all your beach photos by learning what beaches look like.
* **Voice assistants** learn to convert speech into text from millions of voice samples.
* **Bank fraud alerts** learn what your normal spending looks like, then flag anything weird.
* **ChatGPT and Claude** learn language patterns from huge amounts of text.

Every one of these started with someone collecting examples and letting an algorithm figure out the patterns.

---

## The Three Big Types of Machine Learning

Almost every ML technique falls into one of three families. Let us meet them.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    ML["<b>Machine Learning</b>"]
    ML --> S["<b>Supervised</b><br/>learns from labelled<br/>examples"]
    ML --> U["<b>Unsupervised</b><br/>finds patterns in<br/>unlabelled data"]
    ML --> R["<b>Reinforcement</b><br/>learns by trial,<br/>reward, error"]
    S --> SE["spam filter,<br/>house prices,<br/>medical diagnosis"]
    U --> UE["customer groups,<br/>anomaly detection,<br/>topic discovery"]
    R --> RE["game playing,<br/>robot control,<br/>self-driving"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class SE,UE,RE gray
    class ML,S,U,R midgray
</div>

### 1. Supervised Learning, the most common one

Think of it as learning with a teacher. Every training example has both a question and the right answer. The algorithm learns to map questions to answers.

* Question: "Here is an email. Is it spam?" Answer: yes or no.
* Question: "Here are the features of a house. What is its price?" Answer: a number.
* Question: "Here is an image. What animal is in it?" Answer: cat, dog, or bird.

Most of what you see in business and industry is supervised learning. It is the workhorse.

### 2. Unsupervised Learning, finding hidden structure

There is no teacher. You just have data, and you want the computer to find structure in it. The output is not "predict this answer" but rather "tell me what is in this data."

* Group my customers into natural categories without me telling you what the categories are.
* Spot transactions that look unusual compared to the rest.
* Organize a million news articles into related topics.

Unsupervised learning is great for exploring data you do not understand yet.

### 3. Reinforcement Learning, learning by trying

The algorithm tries things. Good outcomes give it a reward. Bad outcomes give it a punishment. Over time it figures out which actions lead to rewards.

* A robot learning to walk falls over thousands of times, gradually figuring out how to balance.
* A chess engine plays millions of games against itself and learns winning strategies.
* A self-driving car simulator runs millions of driving scenarios to learn good behaviour.

Reinforcement learning is the most "alive" of the three. It is also the most data-hungry and hardest to do well.

---

## The Machine Learning Pipeline

When you actually do an ML project, you go through a series of steps. Almost every real project, big or small, follows the same pipeline.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    A["<b>1. Collect<br/>data</b>"] --> B["<b>2. Clean<br/>and prepare</b>"]
    B --> C["<b>3. Pick a<br/>model</b>"]
    C --> D["<b>4. Train</b>"]
    D --> E["<b>5. Evaluate</b>"]
    E --> F{"<b>Good<br/>enough?</b>"}
    F -->|no| G["<b>6. Improve</b>"]
    G --> C
    F -->|yes| H["<b>7. Deploy</b>"]
    H --> I["<b>Monitor<br/>in production</b>"]
    I -->|drift over time| A
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class B,C,D,E,G,H gray
    class A,F,I midgray
</div>

Let us walk through each step.

### Step 1. Collect Data

Get the raw material. If you want to predict house prices, you need a list of past house sales with their features and final prices. If you want to detect fraud, you need historical transactions with fraud labels.

This is usually the hardest, slowest, and most expensive step. Real datasets are messy, scattered across systems, full of holes, and sometimes need to be created from scratch.

### Step 2. Clean and Prepare Data

Real data is almost always dirty. You will spend most of your project here.

* Fill in or drop missing values.
* Remove duplicates.
* Convert text categories into numbers.
* Scale features that live on very different ranges.
* Engineer new features that capture useful patterns.

The saying goes, "garbage in, garbage out." If your data is bad, no algorithm in the world will save you.

### Step 3. Pick a Model

Pick the right tool for the job.

* Predicting a number? Use a **regression** algorithm.
* Predicting a category? Use a **classification** algorithm.
* Finding groups? Use a **clustering** algorithm.

For your first project, pick something simple. A linear regression or a logistic regression is almost always the right starting point.

### Step 4. Train the Model

Show the algorithm your training data and let it figure out the patterns. In Python this is usually a single line of code.

```python
model.fit(X_train, y_train)
```

That is it. The algorithm crunches the numbers and produces a trained model.

### Step 5. Evaluate

Now check how good your model actually is. You test it on data it has never seen, called the **test set**. You measure metrics like accuracy, error rate, precision, or recall depending on the problem.

The score you get on test data is the only score that matters. Training accuracy tells you whether the model memorized. Test accuracy tells you whether it actually learned.

### Step 6. Improve

Almost no model is great on the first try. You iterate.

* Try a different algorithm.
* Tune the hyperparameters.
* Add more or better features.
* Get more data if you can.

This loop is where the real craft of ML happens.

### Step 7. Deploy and Monitor

Once your model is good enough, ship it. Put it behind an API, embed it in your app, or run it in a batch pipeline. But the job is not done.

Real-world data changes over time. Customer behaviour shifts. New fraud tactics appear. Your model will slowly become less accurate as the world drifts away from your training data. You have to monitor performance and retrain regularly.

---

## Key Ideas You Need to Know

A few terms come up constantly in ML. Let us make them stick.

### Features and Labels

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    F["<b>Features (X)</b><br/>What you know<br/>(inputs)"]
    F --> M["<b>Model</b>"]
    M --> L["<b>Label (y)</b><br/>What you want<br/>(output)"]

    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class M gray
    class F,L midgray
</div>

**Features** are the inputs. They are what you know about each example. For houses, the features could be size, bedrooms, age, and location.

**Labels** are the outputs. They are what you want to predict. For houses, the label is the price.

In code you will see features called `X` and labels called `y`. That is a convention from math, and it stuck.

### Training Data and Test Data

You never train and evaluate on the same data. That would be like writing your own exam and then bragging that you scored 100%. You have to split the data.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    D["<b>All your data</b>"]
    D --> TR["<b>Training set</b><br/>~80%<br/>used to teach<br/>the model"]
    D --> TE["<b>Test set</b><br/>~20%<br/>used to honestly<br/>evaluate"]
    TR --> M["<b>Model learns<br/>patterns</b>"]
    M --> SC["<b>Score on test set</b><br/>this is the<br/>real performance"]
    TE --> SC
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class TR,TE gray
    class D,M,SC midgray
</div>

A common split is 80% for training, 20% for testing. The model only sees the training set. The test set is kept hidden until the end, and the score on it is the only one that counts.

### Overfitting and Underfitting

This is the most important concept in ML. Get this right and most things make sense.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    U["<b>Underfitting</b><br/>Model too simple<br/>Misses the pattern<br/>Bad on training<br/>Bad on test"]
    G["<b>Just right</b><br/>Captures the pattern<br/>Generalizes well<br/>Good on training<br/>Good on test"]
    O["<b>Overfitting</b><br/>Model too complex<br/>Memorizes the noise<br/>Great on training<br/>Bad on test"]
    U -.->|more complex| G
    G -.->|even more complex| O
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class U,O gray
    class G midgray
</div>

**Underfitting** is when your model is too simple to capture the real patterns. Like trying to draw a curving river with a single straight line. It fails on both training and test data.

**Overfitting** is when your model is too complex and memorizes every random quirk in the training data, including the noise. It scores brilliantly on training data and miserably on anything new. Like a student who memorized every word of the textbook but cannot answer a slightly different question.

**The sweet spot** is in the middle. The model is just complex enough to capture the real patterns but not so complex that it memorizes noise. Most of ML is about finding this sweet spot.

---

## Should You Use Machine Learning?

ML is not the answer to every problem. Sometimes a simple rule is better. Here is a quick guide to know when ML is worth it.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    Q{"<b>Do you have<br/>lots of data?</b><br/>(thousands+ examples)"}
    Q -->|no| NO1["<b>Skip ML</b><br/>use simple rules<br/>or just analysis"]
    Q -->|yes| Q2{"<b>Are the patterns<br/>complex?</b>"}
    Q2 -->|no| NO2["<b>Skip ML</b><br/>write the rules<br/>directly"]
    Q2 -->|yes| Q3{"<b>Is approximate<br/>OK?</b>"}
    Q3 -->|no| NO3["<b>Careful</b><br/>ML is probabilistic,<br/>never 100% accurate"]
    Q3 -->|yes| Q4{"<b>Can you tolerate<br/>some opaqueness?</b>"}
    Q4 -->|no| NO4["<b>Use simple ML</b><br/>like linear / logistic<br/>regression for clarity"]
    Q4 -->|yes| YES["<b>Use ML!</b><br/>this is what it's<br/>built for"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class NO1,NO2,NO3,NO4,YES gray
    class Q,Q2,Q3,Q4 midgray
</div>

### ML is a great fit when:

* You have lots of historical data (thousands of examples or more).
* The patterns are too complex to write rules for by hand.
* The patterns change over time and you need a model that can adapt.
* Approximate is fine. Most ML systems aim for high accuracy, not perfect accuracy.

### ML is the wrong choice when:

* You only have a few dozen examples.
* The rules are simple and well known. Just write them.
* You need 100% accuracy or perfect explanations every time.
* It is a one-off decision, not a repeating task.

If you are unsure, try a quick experiment. Build the simplest possible model with the data you have and see how it scores. If a simple model already does well, you know ML is the right path. If a simple model fails badly, more ML probably will not save you.

---

## Getting Started in Practice

Ready to do something hands on? Here is the minimum setup.

### What you need

* **A laptop.** Almost any modern computer works for learning.
* **Basic algebra.** Just the idea of `y = mx + b`. Nothing fancy.
* **Some Python.** You do not need to be a Python expert. Knowing variables, lists, and functions is enough.

### Install the tools

These are the libraries that everyone uses. One command installs all of them.

```bash
pip install numpy pandas scikit-learn matplotlib seaborn
```

* **numpy** for numbers and arrays.
* **pandas** for working with tables of data.
* **scikit-learn** for the ML algorithms.
* **matplotlib and seaborn** for plotting.

### Your first project ideas

Pick something small and finish it. Almost any of these is a perfect first project.

* Predict house prices using a public housing dataset.
* Build a simple spam filter on the SMS Spam Collection.
* Group customers into segments using K-Means.
* Predict whether a passenger survived the Titanic.
* Classify iris flowers by species.

You will learn ten times more by completing one small project than by reading ten tutorials.

---

## Common Beginner Mistakes

A few traps catch almost every beginner. Knowing them now saves you weeks later.

* **Training on test data.** Never. The test set must stay sealed until the end.
* **Skipping data cleaning.** Bad data destroys good algorithms. Spend the time.
* **Starting too complex.** Begin with linear regression, not neural networks.
* **Trusting training accuracy.** A 99% training score with a 60% test score means you overfit.
* **Forgetting to scale features.** Many algorithms (KNN, K-Means, SVM, linear models with regularization) need scaled features.
* **Ignoring imbalanced data.** If 99% of your data is class A, a model that always says "A" gets 99% accuracy without learning anything.

---

## Where to go from here

You now have the big picture. From here, follow the numbered tutorials in this section in order.

* **02. ML in Plain English - A Friendly Tour** gives you the story-style overview of every technique.
* **03 to 05. Linear Regression** teaches the foundation algorithm for predicting numbers.
* **06. Logistic Regression** teaches the foundation algorithm for yes-or-no predictions.
* **07. Regularization** teaches how to keep your models from overfitting.
* **08 to 10. Decision Trees** teaches the most intuitive class of models.
* **11 to 13. Ensembles** teaches the most powerful classical algorithms: Random Forests and Gradient Boosting.
* **14. Similarity and Distance Metrics** sets up the unsupervised section.
* **15 to 16. Clustering** teaches K-Means and Hierarchical Clustering.
* **17. K-Nearest Neighbours** rounds out the classical toolkit.

Take your time. ML is not a race. The people who learn it well are the ones who slow down on the basics until those basics feel obvious.

---

## One last thing to remember

Machine learning is not magic. It is just a clever way to find patterns in data. Every algorithm you will meet, from linear regression to gradient boosting to neural networks, is a tool for the same basic job. Look at the examples. Find the patterns. Make predictions on new examples.

Once you internalize that idea, everything else is detail.

Welcome aboard.
