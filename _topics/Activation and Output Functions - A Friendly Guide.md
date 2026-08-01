---
title: "Part 17: Activation and Output Functions — A Friendly Guide"
category: Deep Learning
order: 17
tags:
  - deep-learning
  - activation-functions
  - softmax
  - sigmoid
  - relu
  - tanh
  - beginners
summary: "A beginner-friendly guide to the most common activation and output functions in deep learning, with formulas, use cases, and a decision table."
---

# Part 17: Activation and Output Functions — A Friendly Guide

A neural network is just a long chain of calculations. At the end of each part, we need a function that turns numbers into useful outputs.

These functions are called **activation functions**.

Some are used inside the network to help it learn complicated patterns. Others are used at the very end to produce the final answer: a class, a probability, or a class index.

This lesson shows the most common functions you will meet in PyTorch and other deep learning libraries.

---

## 1. Common output and activation functions

| Function | Formula | Output range | Adds to 1? | Main use | Example output |
|---|---|---|---|---|---|
| **Softmax** | `P_i = e^(z_i) / Σ_j e^(z_j)` | 0 to 1 | Yes | Multiclass classification where only one class is correct | `[0.10, 0.75, 0.15]` |
| **Sigmoid** | `σ(z) = 1 / (1 + e^(-z))` | 0 to 1 | No | Binary classification and multi-label classification | `[0.80, 0.70, 0.10]` |
| **Log-Softmax** | `log(P_i) = z_i - log(Σ_j e^(z_j))` | Usually negative | No | Stable multiclass training | `[-0.36, -1.61, -2.30]` |
| **Sparsemax** | `sparsemax(z)_i = max(z_i - τ, 0)` | 0 to 1 | Yes | Produces probabilities with exact zeros | `[0.85, 0.15, 0]` |
| **Argmax** | `argmax_i(z_i)` | Class index | Not applicable | Selects the position with the largest value | `[0.1, 0.7, 0.2] → class 2` |
| **ReLU** | `f(z) = max(0, z)` | 0 to infinity | No | Hidden layers | `[-2, 3, 5] → [0, 3, 5]` |
| **Tanh** | `tanh(z) = (e^z - e^(-z)) / (e^z + e^(-z))` | -1 to 1 | No | Hidden layers and recurrent networks | `tanh(2) ≈ 0.96` |

---

## 2. What each function does

### Softmax

Softmax turns a list of raw scores into a list of probabilities that add to 1.

**Formula:**

```text
P_i = e^(z_i) / (e^(z_1) + e^(z_2) + ... + e^(z_K))
```

**Simple example:**

Your model gives three scores: `z = [2.0, 1.0, 0.1]`.

Softmax turns this into probabilities:

```text
P ≈ [0.70, 0.26, 0.04]
```

These add to 1, and the largest score becomes the largest probability.

### Sigmoid

Sigmoid takes one number and squeezes it between 0 and 1.

**Formula:**

```text
σ(z) = 1 / (1 + e^(-z))
```

For a very large positive `z`, the result is close to 1. For a very large negative `z`, the result is close to 0.

Each output is separate. If you have three classes, you can have three separate sigmoid outputs: `[0.80, 0.70, 0.10]`. This is useful when one item can belong to more than one class at the same time.

### Log-Softmax

Log-Softmax is simply the logarithm of the Softmax result.

**Formula:**

```text
log(P_i) = z_i - log(e^(z_1) + e^(z_2) + ... + e^(z_K))
```

It is used during training because the math is more stable and more accurate than writing Softmax followed by `log`. In PyTorch, `nn.CrossEntropyLoss` expects raw scores, but `nn.NLLLoss` expects log-softmax outputs.

### Sparsemax

Sparsemax is like Softmax, but it can produce exact zeros.

**Formula:**

```text
sparsemax(z)_i = max(z_i - τ, 0)
```

The value `τ` is chosen so the non-zero results add to 1. This means some classes can receive probability 0 while others share the full probability.

Useful when you want the model to clearly ignore some classes.

### Argmax

Argmax does not produce a probability. It only tells you which position has the biggest value.

```text
argmax([0.1, 0.7, 0.2]) = 1
```

The answer is `1` because the largest value `0.7` is at index 1.

Argmax is used at prediction time. After the model produces probabilities, you pick the class with the highest score.

### ReLU

ReLU is the most common activation for hidden layers.

**Formula:**

```text
f(z) = max(0, z)
```

If the input is positive, pass it through. If the input is negative, replace it with 0.

```text
[-2, 3, 5] → [0, 3, 5]
```

It is fast, simple, and helps the network learn quickly.

### Tanh

Tanh squeezes a number between -1 and 1.

**Formula:**

```text
tanh(z) = (e^z - e^(-z)) / (e^z + e^(-z))
```

Values near 0 stay near 0. Large positive numbers become close to 1. Large negative numbers become close to -1.

Tanh is used in hidden layers and in older recurrent networks because its output is centered around 0, which can help training.

---

## 3. Which one should you use?

| Problem | Output function | Formula |
|---|---|---|
| Spam or not spam | **Sigmoid** | `σ(z) = 1 / (1 + e^(-z))` |
| Cat, dog, or horse — exactly one | **Softmax** | `P_i = e^(z_i) / Σ_j e^(z_j)` |
| Image may contain both cat and dog | **Sigmoid for each class** | `σ(z_i) = 1 / (1 + e^(-z_i))` for each class separately |
| Choose the class with highest probability | **Argmax** | `argmax_i(P_i)` |
| Hidden-layer activation | **ReLU** | `f(z) = max(0, z)` |

---

## 4. Important symbols

| Symbol | Meaning |
|---|---|
| `z_i` | Raw score, or logit, for class `i` |
| `e` | Exponential number, approximately `2.718` |
| `K` | Total number of classes |
| `P_i` | Probability of class `i` |
| `Σ` | Add all the values together |
| `i` | Current class being calculated |
| `j` | Used to go through all classes |

---

## 5. Softmax example for three classes

For three classes, Softmax takes raw scores and turns them into three probabilities:

```text
[z_1, z_2, z_3] → [P_1, P_2, P_3]
```

Where:

```text
P_1 = e^(z_1) / (e^(z_1) + e^(z_2) + e^(z_3))
P_2 = e^(z_2) / (e^(z_1) + e^(z_2) + e^(z_3))
P_3 = e^(z_3) / (e^(z_1) + e^(z_2) + e^(z_3))
```

Because they are all divided by the same total, they always add to 1:

```text
P_1 + P_2 + P_3 = 1
```

### Worked example

Raw scores: `z = [2.0, 1.0, 0.1]`

Step 1: Calculate `e^(z_i)` for each class:

```text
e^2.0  ≈ 7.39
e^1.0  ≈ 2.72
e^0.1  ≈ 1.11
```

Step 2: Add them up:

```text
total = 7.39 + 2.72 + 1.11 = 11.22
```

Step 3: Divide each by the total:

```text
P_1 = 7.39 / 11.22 ≈ 0.66
P_2 = 2.72 / 11.22 ≈ 0.24
P_3 = 1.11 / 11.22 ≈ 0.10
```

Result:

```text
[0.66, 0.24, 0.10]
```

This adds to exactly 1. The class with the biggest raw score becomes the most likely class.

In PyTorch, this is one line:

```python
import torch
import torch.nn as nn

scores = torch.tensor([2.0, 1.0, 0.1])
softmax = nn.Softmax(dim=0)
probabilities = softmax(scores)

print(probabilities)
# tensor([0.6590, 0.2424, 0.0986])
```

---

## 6. A simple memory rule

- **Inside the network** — use ReLU or Tanh.
- **At the end, one correct class** — use Softmax.
- **At the end, yes/no or multiple labels per item** — use Sigmoid.
- **At prediction time, pick a class** — use Argmax.

---

## Summary

| Function | Where to use it | Output adds to 1? |
|---|---|---|
| Softmax | Last layer for multiclass (cat, dog, horse) | Yes |
| Sigmoid | Binary or multi-label problems | No |
| Log-Softmax | Training with `NLLLoss` | No |
| Sparsemax | When some classes should be exactly 0 | Yes |
| Argmax | Pick the most likely class | Not a probability |
| ReLU | Hidden layers | No |
| Tanh | Hidden layers and RNNs | No |
