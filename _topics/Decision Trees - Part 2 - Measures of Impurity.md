---
title: "Decision Trees - Part 2 - Measures of Impurity"
category: Machine Learning
order: 7
tags:
  - machine-learning
  - decision-trees
  - gini-impurity
  - entropy
  - information-gain
summary: Part 2 of the decision trees tutorial. We explain in very simple terms what impurity means, how to measure it using Gini and entropy, and how the algorithm decides which question to ask using information gain.
---

# Decision Trees - Part 2 - Measures of Impurity

## How a decision tree decides what question to ask

In Part 1 we said something that needs more explanation.

We said the algorithm tries to split the data into groups that are "as pure as possible." We said purity is the key idea. But we never said exactly how to measure it.

That is what this part is about.

By the end of this part you will understand three things.

1. What impurity actually means with concrete numbers.
2. The two most common ways to measure it, Gini and entropy.
3. How to compare two possible splits and pick the better one, using information gain.

Everything in this part has some math, but the math is very gentle. If you can do basic arithmetic and squaring, you are ready.

Let us start with the most fundamental idea. What does pure or impure really mean.

---

## What does impurity mean

Take any group of data points that all have a label.

The labels might be things like "buyer" or "non buyer". They might be "spam" or "not spam". They might be "yes" or "no", "red" or "blue", or anything else.

A group is **pure** if all the points have the same label. There is no confusion. If you grabbed a random point from the group, you would know its label for sure.

A group is **impure** if the points have a mix of different labels. The more even the mix, the more impure the group.

Here is a visual way to think about it.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    A["<b>Perfectly pure</b><br/>10 buyers<br/>0 non buyers"]
    B["<b>Mostly pure</b><br/>9 buyers<br/>1 non buyer"]
    C["<b>Somewhat mixed</b><br/>7 buyers<br/>3 non buyers"]
    D["<b>Maximum impurity</b><br/>5 buyers<br/>5 non buyers"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    classDef dark fill:#9e9e9e,stroke:#000,stroke-width:1.5px,color:#000
    class A gray
    class B,C midgray
    class D dark
</div>

The first group has no impurity at all. Every point is a buyer.

The last group is as mixed as possible. Half buyers, half non buyers. There is no way to predict the label of a random point. You would just be guessing.

A decision tree wants to take impure groups and split them into purer groups. To do that, it needs a number that captures how pure a group is. That number is what Gini and entropy give us.

---

## Measure 1. Gini impurity

### The intuition behind Gini

Gini impurity is the most popular measure in practice. It is what scikit-learn uses by default. It is also the one most data scientists use most of the time.

Here is the intuition.

Suppose you reach into a group of points and grab one at random. Then you look at its label. Then you grab another random point and guess its label using the label distribution of the group.

The Gini impurity is the probability that you guess wrong.

If the group is perfectly pure, you can never guess wrong. Gini is zero.

If the group is perfectly mixed, you are essentially flipping a coin. Gini is the highest it can be.

That is it. Gini is just the chance of guessing wrong.

### The formula for Gini

The formula looks like this.

```
Gini = 1 - (p1 squared + p2 squared + ... + pk squared)
```

Where each `p` is the fraction of the group that belongs to one of the classes.

If there are only two classes, like "yes" and "no", the formula becomes:

```
Gini = 1 - (p_yes squared + p_no squared)
```

That is the whole formula. Square each fraction, add them up, subtract from 1.

### Let us actually compute it

Let us take three real examples.

#### Example 1. A pure group

Suppose a group has 10 points and all 10 are buyers.

The fraction of buyers is 10 out of 10, which is 1.

The fraction of non buyers is 0 out of 10, which is 0.

Plugging into the formula:

```
Gini = 1 - (1 squared + 0 squared)
Gini = 1 - (1 + 0)
Gini = 1 - 1
Gini = 0
```

A pure group has Gini equal to zero. That matches our intuition.

#### Example 2. A perfectly mixed group

Suppose a group has 10 points. 5 are buyers and 5 are non buyers.

The fraction of buyers is 5 out of 10, which is 0.5.

The fraction of non buyers is 5 out of 10, which is also 0.5.

Plugging in:

```
Gini = 1 - (0.5 squared + 0.5 squared)
Gini = 1 - (0.25 + 0.25)
Gini = 1 - 0.5
Gini = 0.5
```

A perfectly mixed group with two classes has Gini equal to 0.5. That is the maximum impurity for binary classification.

#### Example 3. A slightly mixed group

Suppose a group has 10 points. 9 are buyers and 1 is a non buyer.

The fraction of buyers is 9 out of 10, which is 0.9.

The fraction of non buyers is 1 out of 10, which is 0.1.

Plugging in:

```
Gini = 1 - (0.9 squared + 0.1 squared)
Gini = 1 - (0.81 + 0.01)
Gini = 1 - 0.82
Gini = 0.18
```

This group is much closer to pure, so Gini is small. Just 0.18.

### A summary table

| Group | Composition | Gini |
|------|-------------|------|
| Pure | 10 buyers, 0 non buyers | 0.00 |
| Almost pure | 9 buyers, 1 non buyer | 0.18 |
| Slightly mixed | 7 buyers, 3 non buyers | 0.42 |
| Very mixed | 6 buyers, 4 non buyers | 0.48 |
| Maximum mix | 5 buyers, 5 non buyers | 0.50 |

The pattern is clear. More mixed means higher Gini. Pure means zero. The highest possible value in binary classification is 0.5.

If you can compute Gini for any group, you can compare two possible splits by computing the Gini of the resulting groups. The split that produces lower Gini values is the better one. That is exactly what the algorithm does.

---

## Measure 2. Entropy

### The intuition behind entropy

Entropy is the other very popular measure of impurity. It comes from a field called information theory, which is about measuring information and uncertainty.

The intuition is simple.

If a group is very pure, you do not need much information to describe it. Saying "everyone here is a buyer" is enough. The group has low entropy.

If a group is very mixed, you need a lot of information to describe each point. There is a lot of uncertainty. The group has high entropy.

So entropy measures the amount of uncertainty in a group. The more uncertain the group, the higher the entropy.

### The formula for entropy

The formula uses logarithms, which look scary but are not really.

```
Entropy = -(p1 * log2(p1) + p2 * log2(p2) + ... + pk * log2(pk))
```

`log2` just means logarithm base 2. You can think of it as "how many times do I have to halve something to get this value". For example, `log2(0.5)` is `-1`, because halving 1 once gives 0.5.

For two classes, the formula becomes:

```
Entropy = -(p_yes * log2(p_yes) + p_no * log2(p_no))
```

By convention, if any `p` is zero, we treat `p * log2(p)` as zero. We do not actually evaluate `log2(0)`, which is undefined.

### Let us compute entropy too

#### Example 1. A pure group

Group with 10 buyers, 0 non buyers.

```
Entropy = -(1 * log2(1) + 0 * log2(0))
Entropy = -(1 * 0 + 0)
Entropy = 0
```

A pure group has entropy zero. Same as Gini.

#### Example 2. A perfectly mixed group

Group with 5 buyers, 5 non buyers.

```
Entropy = -(0.5 * log2(0.5) + 0.5 * log2(0.5))
Entropy = -(0.5 * -1 + 0.5 * -1)
Entropy = -(-1)
Entropy = 1
```

A perfectly mixed group with two classes has entropy equal to 1. That is the maximum entropy in binary classification.

#### Example 3. A slightly mixed group

Group with 9 buyers, 1 non buyer.

```
Entropy = -(0.9 * log2(0.9) + 0.1 * log2(0.1))
Entropy = -(0.9 * -0.152 + 0.1 * -3.322)
Entropy = -(-0.137 + -0.332)
Entropy = -(-0.469)
Entropy = 0.469
```

This group is close to pure, so entropy is low.

### Gini vs entropy, a comparison

| Group | Composition | Gini | Entropy |
|------|-------------|------|---------|
| Pure | 10 buyers, 0 non buyers | 0.00 | 0.00 |
| Almost pure | 9 buyers, 1 non buyer | 0.18 | 0.47 |
| Slightly mixed | 7 buyers, 3 non buyers | 0.42 | 0.88 |
| Very mixed | 6 buyers, 4 non buyers | 0.48 | 0.97 |
| Maximum mix | 5 buyers, 5 non buyers | 0.50 | 1.00 |

Notice they tell the same story. Both go up as the group gets more mixed. Both are zero when the group is pure. The numbers are different because they are on different scales, but they rank groups in the same order.

### Which one should you use

In practice, they almost always pick the same splits. It is rare to find a case where Gini and entropy disagree on what the best split is.

Most people use Gini because it is faster to compute. No logarithms are needed, just squares. When you are training a tree on a large dataset and considering thousands of possible splits, that speed difference can matter.

Entropy is sometimes preferred when you want theoretical guarantees or when you are following the original ID3 or C4.5 algorithms, which were the first famous decision tree algorithms.

For most beginners, the answer is just this. Use Gini by default. You will be fine.

---

## Measure 3. Information Gain

We now know how to measure how pure a single group is. But that alone is not enough to choose a split.

To choose a split, we need to compare the impurity **before** the split with the impurity **after** the split. That comparison is called information gain.

### The intuition

Imagine you have a group with Gini equal to 0.50. That is a very mixed group.

You consider splitting it in two ways.

**Split A.** You pick some question. The two resulting groups have Gini values of 0.45 and 0.45. That is not much better than before. This split barely helped.

**Split B.** You pick a different question. The two resulting groups have Gini values of 0.10 and 0.05. The resulting groups are much purer.

Clearly Split B is better. But we need a number that captures this.

Information gain does exactly that. It says, "by how much did the split reduce impurity."

### How to compute it

Here is the recipe.

1. Compute the impurity of the parent group. Call this `impurity_before`.
2. After the split, compute the impurity of each child group.
3. Take a weighted average of the child impurities. Weight each child by how many points it contains. Call this `weighted_impurity_after`.
4. Information gain equals `impurity_before` minus `weighted_impurity_after`.

The reason we take a weighted average is fairness. If one child contains 95 points and the other contains 5 points, the big child should count for more.

### A worked example

Suppose we have a parent group of 100 customers. 50 are buyers, 50 are not. Gini of the parent is 0.50.

We try splitting on age.

* Group A. Customers under 30. 80 customers total. 70 buyers, 10 non buyers.
* Group B. Customers 30 and over. 20 customers total. 0 buyers, 20 non buyers.

Compute Gini for each child.

Group A:
```
p_buyer = 70 / 80 = 0.875
p_non_buyer = 10 / 80 = 0.125
Gini = 1 - (0.875 squared + 0.125 squared)
Gini = 1 - (0.766 + 0.016)
Gini = 1 - 0.782
Gini = 0.218
```

Group B:
```
p_buyer = 0 / 20 = 0
p_non_buyer = 20 / 20 = 1
Gini = 1 - (0 + 1)
Gini = 0
```

Now take a weighted average:
```
weight_A = 80 / 100 = 0.8
weight_B = 20 / 100 = 0.2
weighted_impurity_after = 0.8 * 0.218 + 0.2 * 0 = 0.174
```

Information gain:
```
gain = 0.50 - 0.174 = 0.326
```

That is a big gain. The original group had impurity 0.50, and after splitting on age, the average impurity dropped to about 0.17. The algorithm would seriously consider this split.

### How splits get chosen

At every node, the algorithm does this.

1. List every possible question it could ask. For numeric features like age, this means trying many different threshold values. For categorical features like color, it tries each possible category.
2. For each question, compute the information gain it would produce.
3. Pick the question with the highest information gain.
4. Use that as the split.

That is the entire splitting logic, repeated at every node from the top down.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    A["<b>Current group</b><br/>compute impurity"]
    A --> B["<b>Try every possible split</b><br/>across every feature"]
    B --> C["<b>For each split,<br/>compute information gain</b>"]
    C --> D["<b>Pick the split<br/>with the highest gain</b>"]
    D --> E["<b>Use that question<br/>at this node</b>"]
    E --> F["<b>Repeat the process<br/>on each child group</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    class A,B,C,D,E,F gray
</div>

---

## One more useful idea, splits for numeric features

We have been talking about categorical features like color. But many real features are numbers, like age or income. How does the algorithm pick a threshold?

The trick is to try several reasonable thresholds.

Suppose we are splitting on age, and the ages in our group are 22, 28, 31, 35, 40, 45, 50.

The algorithm sorts them and tries threshold values between each pair of adjacent values. So it might try age less than 25, age less than 29.5, age less than 33, and so on.

For each threshold, it computes the information gain. Whichever threshold gives the highest gain wins.

That is why decision trees can handle numeric features so easily. They quietly try many thresholds and pick the best one.

---

## A complete mini example

Let us pull everything together with a small worked example.

Suppose we have 10 customers. 6 bought our product, 4 did not. Parent Gini is:

```
Gini_parent = 1 - (0.6 squared + 0.4 squared) = 1 - 0.52 = 0.48
```

We consider two splits.

**Split on age.**

* Left group, age under 35. 5 customers. 5 buyers, 0 non buyers.
* Right group, age 35 and over. 5 customers. 1 buyer, 4 non buyers.

```
Gini_left = 1 - (1 squared + 0 squared) = 0
Gini_right = 1 - (0.2 squared + 0.8 squared) = 1 - (0.04 + 0.64) = 0.32

weighted_after = 0.5 * 0 + 0.5 * 0.32 = 0.16
gain_age = 0.48 - 0.16 = 0.32
```

**Split on country.**

* Left group, country is USA. 6 customers. 4 buyers, 2 non buyers.
* Right group, country is not USA. 4 customers. 2 buyers, 2 non buyers.

```
Gini_left = 1 - ((4/6) squared + (2/6) squared) = 1 - (0.444 + 0.111) = 0.445
Gini_right = 1 - (0.5 squared + 0.5 squared) = 0.5

weighted_after = 0.6 * 0.445 + 0.4 * 0.5 = 0.267 + 0.2 = 0.467
gain_country = 0.48 - 0.467 = 0.013
```

**Comparison.**

Age has a gain of 0.32. Country has a gain of 0.013. Age is much better. The algorithm picks age as the question for this node.

That is exactly how every node in every decision tree is built, all the way down.

---

## What we have learned in this part

We learned what impurity means. A group is pure if all points have the same label. It is impure if the labels are mixed.

We learned two ways to measure impurity. Gini is fast and is the default in most tools. Entropy is from information theory and is also widely used. They almost always agree.

We learned how the algorithm picks splits. It computes the impurity before the split, computes the weighted impurity after the split, and the difference is called the information gain. The split with the highest information gain wins.

We learned that numeric features are handled by trying many possible thresholds and picking the best one.

In Part 3, we will pull all of this together. We will look at the complete training process, talk about how to stop the tree from overfitting, discuss the real world advantages and disadvantages, and finally write Python code to train and visualize a decision tree on a real dataset.

See you in Part 3.
