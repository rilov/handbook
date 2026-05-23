---
title: "07. Decision Trees - Part 1 - Foundations"
category: Machine Learning
order: 7
tags:
  - machine-learning
  - decision-trees
  - classification
  - regression
  - supervised-learning
summary: A simple beginner friendly guide to decision trees. Part 1 covers what they are, why we use them, and how they actually work step by step using real life examples.
---

# Decision Trees - Part 1 - Foundations

## A simple guide to one of the most loved algorithms in machine learning

If you have ever played the game "20 questions", you already understand decision trees.

That game works like this. One person thinks of an object. The other person asks yes or no questions. Each answer narrows down what the object could be. After enough questions, the guesser can figure it out.

A decision tree does exactly the same thing. It asks a series of simple questions about the data, and each answer leads it closer to a final prediction.

This is the first part of a three part tutorial. We will go from "I have never heard of decision trees" to "I can explain how they work to my friend" by the end of this part.

Here is what we will cover in Part 1.

1. Overview, what is a decision tree
2. Why anyone uses them at all
3. How a decision tree actually works, step by step

Let us start at the beginning.

---

## Segment 1. Overview

### What is a decision tree

A decision tree is a model that makes predictions by asking a sequence of yes or no questions.

You start at the top. You ask one question. Depending on the answer, you go left or right. At that next spot, you ask another question. You keep going down the tree until you reach the bottom, where you have a final answer.

That is really all there is to it.

Here is the simplest possible example.

Suppose you want to decide whether to play tennis today. You can ask a few simple questions about the weather.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    A["<b>Is it raining?</b>"]
    A -->|"yes"| B["<b>Do not play</b>"]
    A -->|"no"| C["<b>Is it very hot?</b>"]
    C -->|"yes"| D["<b>Do not play</b>"]
    C -->|"no"| E["<b>Is it windy?</b>"]
    E -->|"yes"| F["<b>Do not play</b>"]
    E -->|"no"| G["<b>Play tennis</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class B,D,F,G gray
    class A,C,E midgray
</div>

That is a decision tree.

It is just a flowchart of questions, with a prediction at the end of every path.

### Some words you will hear a lot

Three words come up over and over when people talk about decision trees. Let us define them right now so the rest of the tutorial is clear.

**Root node.** This is the very first question at the top of the tree. In our tennis example, "Is it raining" is the root node. Every prediction starts from here.

**Internal node.** Any question that is not at the top and not at the bottom. "Is it very hot" and "Is it windy" are internal nodes. They split the data further.

**Leaf node.** The boxes at the very bottom that have the final answer in them. "Play tennis" and "Do not play" are leaf nodes. They are the end of the road.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    A["<b>Root node</b><br/>(the first question)"]
    A --> B["<b>Internal node</b><br/>(another question)"]
    A --> C["<b>Leaf node</b><br/>(final answer)"]
    B --> D["<b>Leaf node</b><br/>(final answer)"]
    B --> E["<b>Leaf node</b><br/>(final answer)"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class C,D,E gray
    class A,B midgray
</div>

That is the whole vocabulary. Root, internal, leaf. Most of decision tree theory is built on top of these three ideas.

### What kinds of problems can decision trees solve

Decision trees can solve two types of problems.

**Classification.** When the answer at the leaf is a category. Like spam or not spam. Like sick or healthy. Like will buy or will not buy.

**Regression.** When the answer at the leaf is a number. Like the price of a house. Like the temperature tomorrow. Like the salary of an employee.

Most of this tutorial will focus on classification because it is easier to picture. But almost everything we learn also applies to regression with small changes.

---

## Segment 2. Motivation for Decision Trees

Now that we know what a decision tree is, let us talk about why anyone uses them.

There are five real reasons. Let us go through them one by one.

### Reason 1. They look exactly like how humans think

When a doctor diagnoses a patient, they do not pull out a fancy equation. They ask questions.

Do you have a fever? Yes.

How high? Around 102.

Any cough? Yes.

How long has this been going on? Three days.

Each answer leads to the next question, and eventually to a diagnosis. That is a decision tree, drawn out loud.

This is one of the biggest reasons decision trees are loved. Other machine learning models work like a magic black box that spits out an answer. A decision tree shows you exactly how it got to its answer, in a way any human can follow.

This matters a lot in fields like medicine, banking, and law, where you legally have to explain why a decision was made.

### Reason 2. They handle messy real world data without complaining

Most machine learning algorithms are picky.

Linear regression wants all your data scaled to similar ranges. Neural networks want everything normalized. Many algorithms cannot deal with missing values at all and will simply crash.

Decision trees are way more forgiving.

* They do not need you to scale the features.
* They do not care if one column is age in years and another is salary in dollars.
* They handle both numbers and categories.
* They can work even when some values are missing.

You can throw fairly raw data at a decision tree and it will still produce something useful.

### Reason 3. They can find non linear patterns

This is a technical sounding phrase but the idea is simple.

A linear model assumes the world is like a straight line. As one thing goes up, another thing goes up or down in a steady proportion.

But the real world is rarely like that.

For example, a baby weighing 10 pounds is normal. A grown adult weighing 10 pounds would be very alarming. The meaning of "10 pounds" changes depending on the age of the person.

Decision trees handle this naturally. They can ask "is the age above 18" first, and then ask "is the weight below 30 pounds" only on one side. They can build different rules for different parts of the data.

This is called capturing non linear interactions, and decision trees do it almost for free.

### Reason 4. They are easy to explain to non technical people

Imagine you build a model to decide which customers are likely to cancel their subscription.

If your model is a deep neural network, explaining it to the marketing team is hard. You either have to skip the details or wave your hands.

If your model is a decision tree, you can literally print it out and show it on a slide. The marketing team can read it like a flowchart. They can argue with the questions. They can suggest improvements. They are now part of the conversation.

That alone is sometimes worth using a slightly less accurate model.

### Reason 5. They are the building block for the most powerful algorithms

Here is something most beginners do not realize.

The most popular and most powerful classical machine learning algorithms in the world today, things like Random Forest, XGBoost, LightGBM, and CatBoost, are all based on decision trees.

They are basically many decision trees working together in clever ways.

So learning how a single decision tree works is not just academic. It is the foundation for understanding the algorithms that win most data science competitions and power most production systems.

If you understand this tutorial, you are already most of the way to understanding those advanced models.

---

## Segment 3. Working of Decision Trees

Now we get to the heart of it. How does a decision tree actually work.

We will walk through this in two stages.

First, how the tree makes a prediction once it is built.

Second, how the tree gets built in the first place.

### Stage 1. How the tree makes a prediction

Suppose someone hands you a fully built decision tree. They also give you a new data point. You want to use the tree to predict what category this data point belongs to.

Here is exactly what happens.

You take the new data point. You start at the root node, which is the top question of the tree. You look at that question. You check the value in your new data point. Based on the answer, you go down the left branch or the right branch.

You arrive at a new node. You ask that question. You go down again.

You keep doing this until you arrive at a leaf node. The leaf has a final answer written on it. That is your prediction.

That is the entire process. Walk from the top, follow the answers, end at a leaf.

Let me show this with a concrete example.

#### Example. Will a customer buy our product

Suppose we have a tree that predicts whether a customer will buy our product. It looks like this.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    A["<b>Is age less than 30?</b>"]
    A -->|"yes"| B["<b>Is income above 50K?</b>"]
    A -->|"no"| C["<b>Has visited 3+ times?</b>"]
    B -->|"yes"| D["<b>Will buy</b>"]
    B -->|"no"| E["<b>Will not buy</b>"]
    C -->|"yes"| F["<b>Will buy</b>"]
    C -->|"no"| G["<b>Will not buy</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class D,E,F,G gray
    class A,B,C midgray
</div>

Now suppose a new customer arrives. They are 25 years old, earn 60,000 per year, and have visited 2 times.

How does the tree predict?

Step 1. Start at the root. The question is "Is age less than 30". The customer is 25. That is yes. Go left.

Step 2. We arrive at "Is income above 50K". The customer earns 60,000. That is yes. Go left.

Step 3. We reach the leaf "Will buy". That is our prediction.

Done.

Notice that we did not even use the "visits" feature for this customer. The tree only asks about features that matter at each decision point. That is one of the elegant things about decision trees.

### Stage 2. How the tree gets built

This is the more interesting question. How does the algorithm decide what question to ask first, what to ask next, and when to stop.

The whole game can be summarized in one sentence.

> At every step, the algorithm looks at all the possible questions it could ask, and picks the one that does the best job of separating the data into groups that are as pure as possible.

The word "pure" is important. Let me explain what it means.

#### What does pure mean

Imagine you have 100 customers. 50 of them bought your product and 50 did not. That group is mixed. It is impure.

Now suppose you split the group based on age. You end up with two groups.

Group A. Customers under 30. 80 of them bought, 5 did not.

Group B. Customers over 30. 0 of them bought, 15 did.

Group A is mostly buyers. Group B is entirely non buyers. Both groups are much more pure than the original mixed group.

That is a good split.

A decision tree builds itself by repeatedly finding splits that make the resulting groups as pure as possible.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    A["<b>Mixed group</b><br/>50 buyers<br/>50 non buyers"]
    A -->|"age &lt; 30"| B["<b>Mostly buyers</b><br/>80 buyers<br/>5 non buyers"]
    A -->|"age &gt;= 30"| C["<b>Mostly non buyers</b><br/>0 buyers<br/>15 non buyers"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class B,C gray
    class A midgray
</div>

The numbers in this example do not add up because I made them up for clarity, but the idea is what matters. Each split should make the children purer than the parent.

#### The full building process

Here is what the algorithm does, in plain English.

Step 1. Start with all the training data at the root.

Step 2. Look at every feature in the data. For each feature, look at every possible threshold or split point. For each possible split, calculate how much purer the resulting groups would be.

Step 3. Pick the single best split. That becomes the question at this node.

Step 4. Divide the data into the two child groups based on that split.

Step 5. Repeat the whole process on each child group, finding the best split inside that smaller group.

Step 6. Keep going recursively until you decide to stop.

The result is a tree.

We will get into how to measure "purer" in much more detail in Part 2. That is where we will meet Gini impurity, entropy, and information gain. For now, just hold on to the intuition. A split is good if the groups it creates are more uniform than the group it started with.

#### When does the algorithm stop

If we just let the algorithm split forever, it would keep going until every leaf contained exactly one training example. The tree would be enormous and would have memorized the training data.

That is bad. A tree that has memorized everything will not work well on new data.

So we tell the algorithm when to stop. The common stopping rules are these.

* Stop when a group is already pure, meaning all examples in it belong to the same class.
* Stop when a group has fewer than some minimum number of examples, like 20.
* Stop when the tree has reached some maximum depth, like 10 levels.
* Stop when the best possible split would not improve purity by much.

These rules are called the stopping criteria. We will see them again when we look at training in Part 3.

---

## A quick visual recap

Let me put it all together into one picture.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    A["<b>Step 1.</b><br/>Start with all training data"]
    A --> B["<b>Step 2.</b><br/>Find the question that<br/>splits the data into the<br/>purest possible groups"]
    B --> C["<b>Step 3.</b><br/>Split the data using<br/>that question"]
    C --> D["<b>Step 4.</b><br/>Repeat for each<br/>smaller group"]
    D --> E["<b>Step 5.</b><br/>Stop when groups<br/>are pure enough or<br/>too small to split"]
    E --> F["<b>Step 6.</b><br/>The result is a tree<br/>of questions ending<br/>in predictions"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    class A,B,C,D,E,F gray
</div>

---

## Putting it all together with a longer example

Let us go through one full example to make sure all the ideas stick.

Suppose we want to predict whether someone will play golf today. We have collected data on 14 days. Each day we recorded the weather and whether the person played.

| Day | Outlook | Temperature | Humidity | Windy | Played |
|----|---------|-------------|----------|-------|--------|
| 1 | Sunny | Hot | High | False | No |
| 2 | Sunny | Hot | High | True | No |
| 3 | Overcast | Hot | High | False | Yes |
| 4 | Rainy | Mild | High | False | Yes |
| 5 | Rainy | Cool | Normal | False | Yes |
| 6 | Rainy | Cool | Normal | True | No |
| 7 | Overcast | Cool | Normal | True | Yes |
| 8 | Sunny | Mild | High | False | No |
| 9 | Sunny | Cool | Normal | False | Yes |
| 10 | Rainy | Mild | Normal | False | Yes |
| 11 | Sunny | Mild | Normal | True | Yes |
| 12 | Overcast | Mild | High | True | Yes |
| 13 | Overcast | Hot | Normal | False | Yes |
| 14 | Rainy | Mild | High | True | No |

We have 9 days where the person played and 5 days where they did not. The overall group is mixed.

Now the algorithm looks at the features and asks, "which feature, if I split on it, gives me the cleanest groups?"

Suppose it tries splitting on Outlook first. The data splits into three groups.

* Sunny days. 5 days total. 2 played, 3 did not. Still mixed.
* Overcast days. 4 days total. 4 played, 0 did not. Pure.
* Rainy days. 5 days total. 3 played, 2 did not. Mixed.

That is a useful split because one of the three branches, the overcast branch, is already completely pure. We can stop on that branch.

For Sunny and Rainy, the algorithm needs to ask another question to clean them up further. Maybe it splits Sunny on Humidity. Maybe it splits Rainy on Windy. Each split makes the resulting groups purer.

Eventually we end up with a tree like this.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    A["<b>Outlook?</b>"]
    A -->|"Sunny"| B["<b>Humidity?</b>"]
    A -->|"Overcast"| C["<b>Play</b>"]
    A -->|"Rainy"| D["<b>Windy?</b>"]
    B -->|"High"| E["<b>Do not play</b>"]
    B -->|"Normal"| F["<b>Play</b>"]
    D -->|"True"| G["<b>Do not play</b>"]
    D -->|"False"| H["<b>Play</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class C,E,F,G,H gray
    class A,B,D midgray
</div>

Take a moment to walk through this tree with a new example. Imagine the weather today is sunny, humid, and not windy. Start at the top. Outlook is sunny, go left. Humidity is high, go left. The leaf says do not play. That is the prediction.

Notice how natural this tree feels. It is something a human could have written down by hand. That is the magic of decision trees.

---

## What we have learned so far

In this part we covered three big ideas.

We learned what a decision tree is. It is a flowchart of yes or no questions ending in a prediction. The first question is the root, the questions in the middle are internal nodes, and the final predictions are the leaves.

We learned why people use decision trees. They look like human reasoning, they handle messy data, they capture non linear patterns, they are easy to explain, and they are the foundation for the most powerful algorithms in classical machine learning.

We learned how a decision tree works. It makes predictions by walking from the root to a leaf. It gets built by repeatedly finding the question that best separates the data into pure groups, and stopping when the groups are clean enough or small enough.

We mentioned the word "pure" many times without saying how to measure it. That is the topic of Part 2.

In Part 2 we will meet three very important measures.

* Gini impurity, which is the most common one in practice.
* Entropy, which comes from information theory and feels very natural once you understand it.
* Information gain, which is how we measure if a split is actually worth making.

Once we understand these measures, we will be ready to look at the full training algorithm in Part 3, and finally write some real Python code that builds a decision tree from scratch on a real dataset.

See you in Part 2.
