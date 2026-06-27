---
title: "Parameters in PyTorch - A Friendly Guide"
category: Deep Learning
order: 5
tags:
  - deep-learning
  - pytorch
  - parameters
  - weights
  - biases
  - nn-module
  - autograd
  - beginners
  - friendly
summary: Learn how PyTorch creates, tracks, and updates learnable parameters automatically. Understand weights, biases, requires_grad, and how to inspect and manage model parameters.
---

# Parameters in PyTorch — A Friendly Guide

When you build a neural network, the things that learn are called **parameters**. In PyTorch, parameters are automatically created, tracked, and updated. This guide explains how that works.

---

## 1. What Are Parameters?

A **parameter** is a number that the model learns during training. In a neural network, the main parameters are:

- **Weights** — how strongly each input connects to each neuron
- **Biases** — the baseline tendency of each neuron to fire

> **Memory trick:** Weights are like volume knobs; biases are like starting positions.

---

## 2. Parameters vs Inputs

| | Parameter | Input |
|--|-----------|-------|
| **Created by** | PyTorch (or you) | Your data |
| **Updated during training?** | Yes | No |
| **Has gradients?** | Yes | Usually no |
| **Purpose** | Learn the pattern | Provide the pattern |

---

## 3. How PyTorch Creates Parameters

When you define a layer, PyTorch automatically creates the weight and bias tensors.

```python
import torch.nn as nn

layer = nn.Linear(3, 2)

print(layer.weight)
print(layer.bias)
```

### Output

```
Parameter containing:
tensor([[ 0.1234, -0.5678,  0.9012],
        [-0.3456,  0.7890, -0.2345]], requires_grad=True)
Parameter containing:
tensor([-0.1234,  0.5678], requires_grad=True)
```

Notice the `requires_grad=True`. That tells PyTorch to track gradients for these tensors.

---

## 4. The `requires_grad` Flag

`requires_grad` is the switch that says "this tensor should be updated during training".

```python
import torch

# A normal tensor
x = torch.tensor([1.0, 2.0, 3.0])
print(x.requires_grad)  # False

# A parameter
w = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
print(w.requires_grad)  # True

# You can turn it on later
x.requires_grad_()
print(x.requires_grad)  # True
```

> **Memory trick:** `requires_grad=True` means "this number is still being decided".

---

## 5. Parameters in a Custom Model

Here is a custom model with manually defined parameters.

```python
import torch
import torch.nn as nn

class ManualModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Manually create a parameter
        self.weight = nn.Parameter(torch.randn(3, 1))
        self.bias = nn.Parameter(torch.zeros(1))

    def forward(self, x):
        return x @ self.weight + self.bias

model = ManualModel()
for name, param in model.named_parameters():
    print(f"{name}: shape {param.shape}")
```

### Output

```
weight: shape torch.Size([3, 1])
bias: shape torch.Size([1])
```

`nn.Parameter` wraps a tensor so PyTorch knows it is a learnable parameter.

---

## 6. Listing All Parameters

Every `nn.Module` has a `parameters()` method that returns all parameters.

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(3, 5),
    nn.ReLU(),
    nn.Linear(5, 1)
)

print("All parameters:")
for name, param in model.named_parameters():
    print(f"  {name}: {param.shape}")

# Count total parameters
total = sum(p.numel() for p in model.parameters())
print(f"\nTotal parameters: {total}")
```

### Output

```
All parameters:
  0.weight: torch.Size([5, 3])
  0.bias: torch.Size([5])
  2.weight: torch.Size([1, 5])
  2.bias: torch.Size([1])

Total parameters: 21
```

> **Memory trick:** `numel()` = "number of elements" = how many numbers are in the tensor.

---

## 7. Weight Initialisation

The starting values of weights matter. PyTorch has several common initialisation methods.

```python
import torch.nn as nn

layer = nn.Linear(3, 2)

# Reset weights from a normal distribution
nn.init.normal_(layer.weight, mean=0, std=0.01)

# Reset weights using Xavier/Glorot initialisation
nn.init.xavier_uniform_(layer.weight)

# Reset biases to zero
nn.init.zeros_(layer.bias)

print(layer.weight)
```

### Common Initialisation Methods

| Method | Use Case | Memory Trick |
|--------|----------|--------------|
| **Random normal** | Simple baseline | Bell curve of weights |
| **Xavier/Glorot** | Symmetric activations (tanh, sigmoid) | Keeps variance stable |
| **He/Kaiming** | ReLU activations | Named for the ReLU hero |
| **Zeros** | Biases only | Start from neutral |

---

## 8. Freezing and Unfreezing Parameters

Sometimes you do not want to update certain parameters. You can freeze them by setting `requires_grad=False`.

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(3, 5),
    nn.ReLU(),
    nn.Linear(5, 1)
)

# Freeze the first layer
for param in model[0].parameters():
    param.requires_grad = False

# Only the second layer will train
for name, param in model.named_parameters():
    print(f"{name}: trainable = {param.requires_grad}")
```

This is useful for **transfer learning**, where you reuse a pretrained model and only train the last layer.

---

## 9. Gradients and the Optimiser

The optimiser is the thing that updates parameters. You tell it which parameters to manage.

```python
import torch
import torch.nn as nn

model = nn.Linear(2, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# One training step
x = torch.tensor([[1.0, 2.0]])
y_true = torch.tensor([[1.0]])

y_pred = model(x)
loss = ((y_pred - y_true) ** 2).mean()

optimizer.zero_grad()
loss.backward()
optimizer.step()
```

What happened behind the scenes:

1. `loss.backward()` computed `∂loss/∂w` for every parameter.
2. `optimizer.step()` changed each parameter by `w = w - lr * gradient`.

> **Memory trick:** Gradient = "direction to move to reduce loss". Optimiser = "take the step".

---

## 10. The Learning Rate

The learning rate controls how big each update is.

```
new_weight = old_weight - learning_rate * gradient
```

| Learning Rate | Effect | Risk |
|---------------|--------|------|
| Too small | Very slow learning | Takes forever |
| Too large | Bounces around | Never converges |
| Just right | Steady improvement | Happy training |

**Common starting values:** 0.01, 0.001, 0.0001

---

## 11. Inspecting Parameter Values

```python
import torch.nn as nn

model = nn.Linear(2, 1)

# Before training
print("Before:", model.weight)

# After a fake training step
with torch.no_grad():
    model.weight += 0.01

print("After:", model.weight)
```

Better: use an optimiser. But if you ever need to manually change values, wrap it in `torch.no_grad()` so you do not mess up the gradient tracking.

---

## 12. Saving and Loading Parameters

```python
import torch

# Save model parameters
torch.save(model.state_dict(), "model.pth")

# Load into a new model with the same architecture
new_model = nn.Linear(2, 1)
new_model.load_state_dict(torch.load("model.pth"))
```

`state_dict()` is a dictionary that maps parameter names to their tensors.

---

## 13. Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|----------------|-----|
| Forgetting `requires_grad=True` | PyTorch cannot track gradients | Use `nn.Parameter` or `nn.Linear` |
| Updating parameters manually without `torch.no_grad()` | Breaks the computation graph | Use `with torch.no_grad()` or let the optimiser handle it |
| Passing wrong parameters to the optimiser | Some layers do not train | Use `model.parameters()` |
| Freezing everything by accident | Model never learns | Check `requires_grad` for each parameter |
| Not zeroing gradients | Gradients accumulate across batches | Call `optimizer.zero_grad()` every step |

---

## 14. Quick Review

| Term | Meaning | Example |
|------|---------|---------|
| **Weight** | Connects inputs to neurons | `nn.Linear(3, 5).weight` |
| **Bias** | Shifts the neuron's output | `nn.Linear(3, 5).bias` |
| **Parameter** | A tensor that PyTorch learns | `nn.Parameter(torch.randn(3, 1))` |
| **`requires_grad`** | Whether PyTorch tracks gradients | `True` for weights, `False` for inputs |
| **`parameters()`** | Iterator over all parameters | `model.parameters()` |
| **`named_parameters()`** | Iterator over parameters with names | `model.named_parameters()` |
| **`state_dict()`** | Dictionary of all parameters | `torch.save(model.state_dict(), "model.pth")` |
| **Learning rate** | Step size during gradient descent | `0.01` |
| **Gradient** | Direction to reduce loss | `loss.backward()` computes it |
| **Optimiser** | Updates parameters using gradients | `torch.optim.SGD`, `Adam` |

---

## 15. Try It Yourself

```python
import torch
import torch.nn as nn

# Build a model
model = nn.Sequential(
    nn.Linear(2, 4),
    nn.ReLU(),
    nn.Linear(4, 1)
)

# 1. Count trainable parameters
print("Total parameters:", sum(p.numel() for p in model.parameters() if p.requires_grad))

# 2. Print parameter names
for name, param in model.named_parameters():
    print(f"{name}: {param.shape}")

# 3. Freeze the first layer
for param in model[0].parameters():
    param.requires_grad = False

# 4. Verify only the second layer trains
print("\nAfter freezing:")
for name, param in model.named_parameters():
    print(f"{name}: trainable = {param.requires_grad}")

# 5. Use an optimiser on only trainable parameters
optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.001)
```

---

## Summary

- Parameters are the learnable numbers in a neural network: weights and biases.
- PyTorch creates them automatically when you use `nn.Linear` and other layers.
- `requires_grad=True` tells PyTorch to track gradients for a tensor.
- `nn.Parameter` wraps tensors so PyTorch treats them as model parameters.
- The optimiser updates parameters using gradients from backpropagation.
- You can freeze parameters by setting `requires_grad=False`.
- Saving `state_dict()` is the standard way to store a model's learned weights.
