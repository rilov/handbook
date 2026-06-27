---
title: "From Machine Learning to Deep Learning - A Friendly Guide"
category: Deep Learning
order: 2
tags:
  - deep-learning
  - machine-learning
  - neural-networks
  - hidden-layers
  - perceptron
  - activation-functions
  - beginners
  - friendly
summary: Learn exactly what changes when you move from traditional machine learning to deep learning, why hidden layers matter, and how the perceptron algorithm connects to modern neural networks.
---

# From Machine Learning to Deep Learning — A Friendly Guide

If you already know machine learning, deep learning is not a huge leap — it is a shift in *how* we represent features. In this guide, we will see what stays the same, what changes, and why adding hidden layers unlocks so much power.

---

## 1. What Stays the Same

Traditional ML and deep learning share the same core idea:

> **Feed data into a model, measure the error, and update the model to reduce the error.**

| Step | Traditional ML | Deep Learning |
|------|----------------|---------------|
| Input data | Features like height, age, word counts | Same — but often rawer (pixels, text) |
| Model | Linear regression, decision tree, SVM | Neural network |
| Loss function | MSE, cross-entropy, log loss | MSE, cross-entropy |
| Optimisation | Gradient descent | Gradient descent / Adam |
| Goal | Minimise error on unseen data | Same |

---

## 2. What Changes

### Feature Engineering vs Feature Learning

In traditional ML, humans often hand-craft features:

- For spam detection: count of spammy words, presence of links
- For house prices: price per square foot, number of rooms

In deep learning, the network learns the features itself. The hidden layers automatically discover what matters.

```
Traditional ML:   Raw Data → Human Features → Model → Prediction
Deep Learning:    Raw Data → Neural Network → Learned Features → Prediction
```

> **Memory trick:** In ML, you tell the model what to look at. In DL, you give it the raw data and it figures out what to look at.

### Linear vs Non-Linear

Most traditional ML models are either linear or have limited non-linearity. A single neuron without activation is a **linear model**:

```
ŷ = w₁x₁ + w₂x₂ + ... + b
```

This is basically **linear regression** or **logistic regression** (if we add sigmoid).

Deep learning becomes powerful when we stack multiple neurons with non-linear activations. The network can then learn curved, complex decision boundaries.

---

## 3. The Perceptron — Where It All Started

The **perceptron** is the simplest neural network: one neuron with a step function.

### Perceptron Rule

```
ŷ = 1 if Σ (xᵢ × wᵢ) + b ≥ 0
ŷ = 0 otherwise
```

It is a binary classifier. The perceptron can learn things like:

- Is an email spam or not spam?
- Is a tumour malignant or benign?

But it cannot solve problems that are not linearly separable, like XOR.

### XOR Problem

| x₁ | x₂ | XOR |
|----|----|-----|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

There is no single straight line that separates the two output classes. A single perceptron fails.

This is why we need **hidden layers**.

---

## 4. Why Hidden Layers Matter

A hidden layer is just a layer of neurons between the input and the output. Each hidden neuron combines the inputs, and the output neuron combines the hidden neurons.

With one hidden layer, the network can learn XOR.

### Why Hidden Layers Work

Imagine trying to draw a circle around a group of points on a piece of paper:

- A single neuron can only draw a straight line.
- A hidden layer can draw curves by combining many straight-line decisions.
- More hidden layers can draw more complex shapes.

> **Memory trick:** A single neuron is like a straight-edge ruler. A hidden layer is like having many rulers that combine into a flexible curve.

### The Universal Approximation Theorem

This theorem says that a neural network with enough hidden neurons can approximate **any** continuous function.

In plain English: **a big enough neural network can learn almost any pattern you give it.**

---

## 5. Deep Learning vs Shallow Learning

| | Shallow Network | Deep Network |
|--|-----------------|--------------|
| **Hidden layers** | 0 or 1 | 3 or more |
| **Features** | Hand-crafted or simple | Learned automatically |
| **Data needed** | Less | More |
| **Compute needed** | Less | More |
| **Can learn complex patterns** | Limited | Yes |
| **Examples** | Logistic regression, SVM | CNNs, transformers, deep MLPs |

---

## 6. The Role of Non-Linearity

Without activation functions, a deep network would just be one giant linear model.

Here is why:

```
Layer 1: z = xW₁ + b₁
Layer 2: z = zW₂ + b₂ = (xW₁ + b₁)W₂ + b₂ = x(W₁W₂) + (b₁W₂ + b₂)
```

If we remove the activation, two layers collapse into one. The activation function stops this from happening.

> **Memory trick:** Activation functions are the "wrinkles" that stop the network from being a flat piece of paper.

---

## 7. Common Activation Functions in Detail

### Sigmoid

```
σ(z) = 1 / (1 + e^(-z))
```

- Smooth, differentiable
- Output between 0 and 1
- Problem: gradients become very small for extreme inputs (vanishing gradient)

### Tanh

```
tanh(z) = 2σ(2z) - 1
```

- Output between -1 and 1
- Stronger gradients than sigmoid
- Still has vanishing gradient problem

### ReLU

```
ReLU(z) = max(0, z)
```

- No vanishing gradient for positive inputs
- Very fast
- Problem: neurons can "die" if they always get negative input

### Leaky ReLU

```
LeakyReLU(z) = max(0.01z, z)
```

- Small slope for negative inputs
- Prevents dying neurons

### Softmax

```
softmax(zᵢ) = e^(zᵢ) / Σ e^(zⱼ)
```

- Turns scores into probabilities
- Used for multi-class classification

---

## 8. Python: Build a Simple Deep Network

```python
import torch
import torch.nn as nn

class TinyNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # Input: 2 features, Hidden: 4 neurons, Output: 1 neuron
        self.layer1 = nn.Linear(2, 4)
        self.activation = nn.ReLU()
        self.layer2 = nn.Linear(4, 1)
        self.output = nn.Sigmoid()

    def forward(self, x):
        x = self.layer1(x)
        x = self.activation(x)
        x = self.layer2(x)
        x = self.output(x)
        return x

# Create the model
model = TinyNetwork()

# Sample input: temperature and humidity
sample = torch.tensor([[25.0, 60.0]])
prediction = model(sample)

print(f"Prediction: {prediction.item():.4f}")
print("\nModel architecture:")
print(model)
```

### What `nn.Linear` Does

`nn.Linear(in_features, out_features)` creates a layer that computes:

```
output = input · W^T + b
```

PyTorch automatically creates the weight matrix `W` and the bias vector `b` for you.

---

## 9. The Learning Loop

All deep learning training follows the same loop:

```
1. Forward pass:   predict ŷ
2. Compute loss:    how far is ŷ from y?
3. Backward pass:   compute gradients
4. Update weights:  move a small step in the direction that reduces loss
5. Repeat
```

We will cover the loss function and backpropagation in later guides.

---

## 10. Quick Comparison: ML vs DL

| Question | Traditional ML | Deep Learning |
|----------|----------------|---------------|
| **Who designs features?** | Human | Network |
| **Best for small data?** | Yes | No |
| **Best for images/text/audio?** | Often needs preprocessing | Works well on raw data |
| **Interpretability?** | Higher | Lower (black box) |
| **Training time?** | Faster | Slower |
| **Hardware?** | CPU | GPU recommended |
| **When to use?** | Structured data, small datasets | Unstructured data, large datasets |

---

## 11. When to Use Deep Learning

Use deep learning when:

- You have a lot of data
- The data is unstructured (images, audio, text, video)
- You do not know exactly which features matter
- You have enough compute power

Use traditional ML when:

- Data is small or structured
- You need to understand why the model made a decision
- Training time and compute are limited

---

## 12. Summary

- Deep learning is a type of machine learning that uses many-layered neural networks.
- The key difference is that deep learning learns features automatically.
- A single neuron is a linear model; hidden layers add non-linearity and power.
- The perceptron can solve linearly separable problems but fails on XOR.
- Activation functions like ReLU, sigmoid, and softmax let the network learn complex patterns.
- More layers = more capacity, but also more data and compute needed.

---

## Try It Yourself

```python
import torch
import torch.nn as nn

# Build a network that can solve XOR
class XORNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(2, 4)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(4, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.sigmoid(self.layer2(x))
        return x

model = XORNetwork()

# Test on all four XOR inputs
X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
with torch.no_grad():
    predictions = model(X)
    print("Before training:")
    for i, pred in enumerate(predictions):
        print(f"  {X[i].tolist()} → {pred.item():.4f}")

# Training loop
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
y = torch.tensor([[0.0], [1.0], [1.0], [0.0]])

for epoch in range(1000):
    pred = model(X)
    loss = loss_fn(pred, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

with torch.no_grad():
    final_predictions = model(X)
    print("\nAfter training:")
    for i, pred in enumerate(final_predictions):
        print(f"  {X[i].tolist()} → {pred.item():.4f}")
```
