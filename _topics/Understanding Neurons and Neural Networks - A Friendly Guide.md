---
title: "Understanding Neurons and Neural Networks - A Friendly Guide"
category: Deep Learning
order: 1
tags:
  - deep-learning
  - neural-networks
  - neurons
  - activation-functions
  - sigmoid
  - relu
  - beginners
  - friendly
  - pytorch
summary: Learn how biological neurons inspired artificial neurons, how a single neuron computes a weighted sum with bias and activation, and how single neurons stack into deep networks. Includes memory tricks for every formula.
---

# Understanding Neurons and Neural Networks — A Friendly Guide

Deep learning starts with one simple idea: a computer can learn by imitating how brain cells work. In this guide, we will build that idea from the ground up.

---

## 1. The Big Picture

A **neural network** is a stack of tiny calculators called **neurons**. Each neuron looks at some inputs, multiplies them by numbers called **weights**, adds a small shift called a **bias**, and then applies a non-linearity called an **activation function**.

The magic is that the network learns the weights and biases from data.

---

## 2. The Biological Inspiration

Your brain contains about 86 billion **neurons**. Each neuron has:

- **Dendrites** — branches that receive signals from other neurons
- **Soma** — the cell body that combines those signals
- **Axon** — a long fibre that sends out a signal if the combined input is strong enough

A neuron fires when the incoming signals are strong enough. This "all-or-nothing" behaviour inspired the artificial neuron.

---

## 3. The Artificial Neuron

Imagine a neuron that decides whether to buy a house based on three inputs:

| Input | Value | Meaning |
|-------|-------|---------|
| `x₁` | 1200 | size in square feet |
| `x₂` | 3 | number of bedrooms |
| `x₃` | 2 | distance to city centre in km |

Each input gets a **weight** that tells the neuron how important it is:

| Weight | Value | Meaning |
|--------|-------|---------|
| `w₁` | 0.5 | size matters a lot |
| `w₂` | 0.2 | bedrooms matter a little |
| `w₃` | -0.4 | distance hurts the score |

The neuron computes a **weighted sum** and then adds a **bias**.

---

## 4. The Formula

### Weighted Sum

```
z = (x₁ × w₁) + (x₂ × w₂) + (x₃ × w₃) + b
```

In short form:

```
z = Σ (xᵢ × wᵢ) + b
```

> **Memory trick:** Think of `Σ` as a "shopping basket" — you throw all the `x × w` items in, then add the bias as the tip.

### Worked Example

Using the house example:

```
z = (1200 × 0.5) + (3 × 0.2) + (2 × -0.4) + 10
z = 600 + 0.6 - 0.8 + 10
z = 609.8
```

The raw score `z = 609.8` is not yet useful. We pass it through an **activation function**.

---

## 5. Activation Functions

An activation function decides whether the neuron "fires" and how strongly.

### Sigmoid — The Squeezes-Everything-To-0-1 Function

```
σ(z) = 1 / (1 + e^(-z))
```

- Output is always between 0 and 1
- Useful for probabilities

**Memory trick:** The letter `S` looks like the sigmoid curve — a smooth "S" that squashes everything.

```python
import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

print(sigmoid(0))    # 0.5 — exactly the middle
print(sigmoid(10))   # close to 1.0
print(sigmoid(-10))  # close to 0.0
```

### ReLU — The "If Negative, Zero" Function

```
ReLU(z) = max(0, z)
```

- If input is positive, leave it alone
- If input is negative, make it zero
- Most popular activation in modern deep learning

**Memory trick:** ReLU is like a bouncer at a club — positive numbers get in, negative numbers are blocked.

```python
def relu(z):
    return max(0, z)

print(relu(5))   # 5
print(relu(-3))  # 0
```

### Tanh — The Squeezes-Everything-To-Minus-1-1 Function

```
tanh(z) = (e^z - e^(-z)) / (e^z + e^(-z))
```

- Output is between -1 and 1
- Useful when negative values are meaningful

**Memory trick:** `tanh` is sigmoid stretched to go from -1 to 1 instead of 0 to 1.

```python
import math

def tanh(z):
    return math.tanh(z)

print(tanh(0))    # 0.0
print(tanh(2))    # 0.96
print(tanh(-2))   # -0.96
```

### Activation Function Cheat Sheet

| Function | Formula | Output Range | When to Use |
|----------|---------|--------------|-------------|
| **Sigmoid** | `1 / (1 + e^(-z))` | 0 to 1 | Binary classification output |
| **Tanh** | `(e^z - e^(-z)) / (e^z + e^(-z))` | -1 to 1 | Hidden layers in older networks |
| **ReLU** | `max(0, z)` | 0 to ∞ | Most modern hidden layers |
| **Softmax** | `e^(zᵢ) / Σ e^(zⱼ)` | 0 to 1 (sums to 1) | Multi-class classification output |

> **Memory trick for Softmax:** It turns a list of scores into probabilities that add up to 1 — like a normalised "ranking".

---

## 6. From One Neuron to a Network

A single neuron is just a linear model. To learn complex patterns, we connect many neurons together.

### Layers

- **Input layer** — receives the raw data
- **Hidden layer** — neurons that transform the input
- **Output layer** — produces the final prediction

```
Input Layer    Hidden Layer    Output Layer

   x₁ ───────────→ ● ───────────────→ ●
                   ↑                   ↑
   x₂ ───────────→ ● ───────────────→ ●
                   ↑                   ↑
   x₃ ───────────→ ● ───────────────→ ●
```

**Why "deep"?** Because we stack many hidden layers. A network with 3+ hidden layers is usually called "deep".

### Why Depth Matters

Think of recognising a face:

- Layer 1: detects edges
- Layer 2: combines edges into eyes, noses, mouths
- Layer 3: combines features into full faces

Each layer builds a slightly more complex representation. Early layers see simple patterns; deeper layers see concepts.

---

## 7. The Forward Pass

The forward pass is what happens when data flows through the network to produce a prediction.

```
Layer 1:  z₁ = x · W₁ + b₁        a₁ = activation(z₁)
Layer 2:  z₂ = a₁ · W₂ + b₂       a₂ = activation(z₂)
Output:   z₃ = a₂ · W₃ + b₃        y_hat = activation(z₃)
```

> **Memory trick:** `z` is the "raw score" (before activation), and `a` is the "activated" value (after activation).

### Python Example with NumPy

```python
import numpy as np

# Inputs: 1 sample, 3 features
x = np.array([1200, 3, 2])

# One hidden layer with 2 neurons
W1 = np.array([[0.5, 0.2],     # weights for hidden neuron 1
               [-0.4, 0.1],    # weights for hidden neuron 2
               [0.0, 0.3]])    # weights for hidden neuron 3
b1 = np.array([10, -5])

# Output layer: 1 neuron
W2 = np.array([[0.7],
               [-0.7]])
b2 = np.array([2])

# Forward pass
z1 = np.dot(x, W1) + b1
a1 = np.maximum(0, z1)   # ReLU

z2 = np.dot(a1, W2) + b2
output = 1 / (1 + np.exp(-z2))  # sigmoid

print(f"Raw hidden scores: {z1}")
print(f"Activated hidden:  {a1}")
print(f"Final prediction:  {output}")
```

---

## 8. What the Network Learns

The network learns two things:

1. **Weights** — how strongly each input should influence each neuron
2. **Biases** — the baseline tendency of each neuron to fire

During training, we compare the network's prediction `ŷ` to the true answer `y`, compute an error, and use an algorithm called **backpropagation** to update every weight and bias slightly.

We will cover backpropagation in a later guide. For now, remember:

> **Learning = changing weights and biases to make the error smaller.**

---

## 9. Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|----------------|-----|
| Forgetting the bias | Bias lets the neuron shift its decision boundary | Always include `+ b` |
| Using sigmoid in hidden layers | Sigmoid can cause vanishing gradients | Use ReLU instead |
| Thinking one neuron is enough | A single neuron is just a linear classifier | Use hidden layers for complex tasks |
| Using wrong activation for output | Regression needs no activation; classification needs sigmoid/softmax | Match activation to task |

---

## 10. Quick Review

| Term | What It Is | Formula / Memory Trick |
|------|-----------|------------------------|
| **Neuron** | A tiny computing unit | Inputs → weights → bias → activation |
| **Weighted sum** | Adds up the influence of all inputs | `z = Σ xᵢwᵢ + b` — "shopping basket" |
| **Bias** | A constant shift | `+ b` — the neuron's starting mood |
| **Activation** | Decides how strongly the neuron fires | Sigmoid = S-curve; ReLU = bouncer |
| **Layer** | A group of neurons | Input → Hidden → Output |
| **Deep network** | A network with many hidden layers | Each layer learns a richer feature |
| **Forward pass** | Data flowing through the network | `z = xW + b`, then `a = activation(z)` |

---

## 11. Try It Yourself

```python
import numpy as np

# A tiny network: 2 inputs, 1 hidden neuron, 1 output neuron

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def relu(z):
    return np.maximum(0, z)

# Inputs: temperature (°C) and humidity (%)
x = np.array([25.0, 60.0])

# Hidden neuron: weights + bias
W1 = np.array([0.3, -0.2])
b1 = 5.0

# Output neuron: weight + bias
W2 = np.array([0.8])
b2 = -3.0

# Forward pass
hidden = relu(np.dot(x, W1) + b1)
output = sigmoid(np.dot(hidden, W2) + b2)

print(f"Will it rain? Probability: {output[0]:.3f}")
```

---

## Summary

- A neural network is a stack of artificial neurons.
- Each neuron computes `z = Σ xᵢwᵢ + b` and then applies an activation function.
- Sigmoid outputs probabilities between 0 and 1; ReLU is the most common hidden-layer activation.
- Depth lets the network learn increasingly complex features.
- During training, the network learns weights and biases to reduce prediction error.
