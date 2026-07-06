---
title: "Part 5: Parameters in PyTorch - A Friendly Guide"
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
  - spam-detection
  - beginners
  - friendly
summary: Learn how PyTorch creates, tracks, and updates learnable parameters for a spam-detection model. Understand weights, biases, requires_grad, and how to inspect and manage model parameters.
---

# Part 5: Parameters in PyTorch — A Friendly Guide

By Part 4 you have a complete data pipeline: a `Dataset`, a `DataLoader` producing batches, and the training loop calling `loss.backward()` and `optimizer.step()` on each batch.

But what exactly is `optimizer.step()` changing? The answer is **parameters** — the weights and biases stored inside each layer. Every time `optimizer.step()` runs, it nudges those numbers slightly to reduce the loss.

Part 5 opens up the model and shows you exactly what parameters exist, how PyTorch tracks them, and how you can inspect, freeze, save, and load them. This is the foundation you need before Part 6 shows you how backpropagation computes which direction to nudge each one.

When you build a spam-detection model, the things that learn are called **parameters**. In PyTorch, parameters are automatically created, tracked, and updated. This guide explains how that works using the same email example.

---

## 1. What are parameters?

A **parameter** is a number that the model learns during training. In a neural network, the main parameters are:

- **Weights** — how strongly each email feature connects to each neuron
- **Biases** — the baseline tendency of each neuron to fire

> **Memory trick:** Weights are like volume knobs; biases are like starting positions.

---

## 2. Parameters versus inputs

| | Parameter | Input |
|--|-----------|-------|
| **Created by** | PyTorch (or you) | Your data |
| **Updated during training?** | Yes | No |
| **Has gradients?** | Yes | Usually no |
| **Purpose** | Learn the pattern | Provide the pattern |

For spam detection, the inputs are the email features. The parameters are the weights and biases that turn those features into a spam score.

---

## 3. How PyTorch creates parameters for spam detection

When you define a layer, PyTorch automatically creates the weight and bias tensors.

```python
import torch.nn as nn

# 5 email features -> 1 spam probability
layer = nn.Linear(5, 1)

print(layer.weight)
print(layer.bias)
```

Output (values will be random):

```
Parameter containing:
tensor([[ 0.1234, -0.5678,  0.9012, -0.3456,  0.7890]], requires_grad=True)
Parameter containing:
tensor([-0.1234], requires_grad=True)
```

Notice the `requires_grad=True`. That tells PyTorch to track gradients for these tensors so they can be updated during training.

> **Memory trick:** `requires_grad=True` means "this number is still being decided."

---

## 4. The `requires_grad` flag

`requires_grad` is the switch that says "this tensor should be updated during training."

```python
import torch

# A normal input tensor
email = torch.tensor([3.0, 1.0, 0.0, 0.20, 47.0])
print(email.requires_grad)  # False

# A parameter tensor
weight = torch.tensor([0.8, 0.6, -1.2, 2.0, 0.01], requires_grad=True)
print(weight.requires_grad)  # True

# You can turn it on later
email.requires_grad_()
print(email.requires_grad)  # True
```

By default, inputs do not need gradients. Weights do.

---

## 5. Building a spam model with parameters

Here is a small spam model with one hidden layer:

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(5, 4),  # 5 features -> 4 hidden neurons
    nn.ReLU(),         # remove negative hidden signals
    nn.Linear(4, 1),  # 4 hidden values -> 1 spam score
    nn.Sigmoid()       # spam score -> probability
)
```

Let's count the parameters:

- First layer: 5 features × 4 neurons = 20 weights, plus 4 biases
- Second layer: 4 hidden values × 1 output = 4 weights, plus 1 bias
- Total: 24 weights + 5 biases = 29 parameters

```python
total = sum(p.numel() for p in model.parameters())
print(f"Total parameters: {total}")
# Output: 29
```

> **Memory trick:** `numel()` = "number of elements" = how many numbers are in the tensor.

---

## 6. Listing all parameters

Every `nn.Module` has a `parameters()` method that returns all parameters.

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(5, 4),
    nn.ReLU(),
    nn.Linear(4, 1)
)

print("All parameters:")
for name, param in model.named_parameters():
    print(f"  {name}: {param.shape}")
```

Output:

```
All parameters:
  0.weight: torch.Size([4, 5])
  0.bias: torch.Size([4])
  2.weight: torch.Size([1, 4])
  2.bias: torch.Size([1])
```

The numbers `0` and `2` refer to the positions in `nn.Sequential`. Position `1` is `ReLU`, which has no parameters.

---

## 7. Weight initialisation

The starting values of weights matter. PyTorch has several common initialisation methods.

```python
import torch.nn as nn

layer = nn.Linear(5, 1)

# Reset weights from a normal distribution
nn.init.normal_(layer.weight, mean=0, std=0.01)

# Reset weights using Xavier/Glorot initialisation
nn.init.xavier_uniform_(layer.weight)

# Reset biases to zero
nn.init.zeros_(layer.bias)

print(layer.weight)
```

### Common initialisation methods

| Method | Use case | Memory trick |
|--------|----------|--------------|
| **Random normal** | Simple baseline | Bell curve of weights |
| **Xavier/Glorot** | Symmetric activations (tanh, sigmoid) | Keeps variance stable |
| **He/Kaiming** | ReLU activations | Named for the ReLU hero |
| **Zeros** | Biases only | Start from neutral |

For our spam model with ReLU hidden layers, **He initialisation** is the most common choice.

---

## 8. Freezing and unfreezing parameters

Sometimes you do not want to update certain parameters. You can freeze them by setting `requires_grad=False`.

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(5, 4),
    nn.ReLU(),
    nn.Linear(4, 1)
)

# Freeze the first layer
for param in model[0].parameters():
    param.requires_grad = False

# Only the second layer will train
for name, param in model.named_parameters():
    print(f"{name}: trainable = {param.requires_grad}")
```

This is useful for **transfer learning**, where you reuse a pretrained model and only train the last layer.

For spam detection, you might freeze the first layer if you believe it already extracts good features, and only fine-tune the output layer.

---

## 9. Gradients and the optimiser

The optimiser is the thing that updates parameters. You tell it which parameters to manage.

```python
import torch
import torch.nn as nn

model = nn.Linear(5, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# One training step
email = torch.tensor([[3.0, 1.0, 0.0, 0.20, 47.0]])
label = torch.tensor([[1.0]])

prediction = model(email)
loss = ((prediction - label) ** 2).mean()

optimizer.zero_grad()
loss.backward()
optimizer.step()
```

What happened behind the scenes:

1. `loss.backward()` computed `∂loss/∂w` for every parameter.
2. `optimizer.step()` changed each parameter by `w = w - lr * gradient`.

> **Memory trick:** Gradient = "direction to move to reduce loss". Optimiser = "take the step".

---

## 10. The learning rate

The learning rate controls how big each update is.

```
new_weight = old_weight - learning_rate * gradient
```

| Learning rate | Effect | Risk |
|---------------|--------|------|
| Too small | Very slow learning | Takes forever |
| Too large | Bounces around | Never converges |
| Just right | Steady improvement | Happy training |

**Common starting values:** 0.01, 0.001, 0.0001

For spam detection, a good starting point is usually `lr=0.001` with the Adam optimiser.

---

## 11. Saving and loading a spam model

A trained spam model has two parts:

1. **Architecture** — the code that defines the layers
2. **Learned state** — the weights and biases

```python
import torch
import torch.nn as nn

# Build the model
model = nn.Sequential(
    nn.Linear(5, 4),
    nn.ReLU(),
    nn.Linear(4, 1),
    nn.Sigmoid()
)

# Save the learned parameters
torch.save(model.state_dict(), "spam_model.pth")

# Load into a new model with the same architecture
new_model = nn.Sequential(
    nn.Linear(5, 4),
    nn.ReLU(),
    nn.Linear(4, 1),
    nn.Sigmoid()
)
new_model.load_state_dict(torch.load("spam_model.pth"))
```

`state_dict()` is a dictionary that maps parameter names to their tensors. It is the standard way to save a trained model.

> **Memory trick:** Think of the architecture as the recipe and the weights as the trained taste. The recipe is code; the taste is the learned state.

---

## 12. Common mistakes

| Mistake | Why it happens | Fix |
|---------|----------------|-----|
| Forgetting `requires_grad=True` | PyTorch cannot track gradients | Use `nn.Parameter` or `nn.Linear` |
| Updating parameters manually without `torch.no_grad()` | Breaks the computation graph | Use `with torch.no_grad()` or let the optimiser handle it |
| Passing wrong parameters to the optimiser | Some layers do not train | Use `model.parameters()` |
| Freezing everything by accident | Model never learns | Check `requires_grad` for each parameter |
| Not zeroing gradients | Gradients accumulate across batches | Call `optimizer.zero_grad()` every step |
| Saving the whole model instead of `state_dict()` | Can break if code changes | Save `state_dict()` separately |

---

## 13. Quick review

| Term | What it is | Example for spam detection |
|------|-----------|----------------------------|
| **Weight** | Connects inputs to neurons | `nn.Linear(5, 4).weight` |
| **Bias** | Shifts the neuron's output | `nn.Linear(5, 4).bias` |
| **Parameter** | A tensor that PyTorch learns | `nn.Parameter(torch.randn(5, 1))` |
| **`requires_grad`** | Whether PyTorch tracks gradients | `True` for weights, `False` for inputs |
| **`parameters()`** | Iterator over all parameters | `model.parameters()` |
| **`named_parameters()`** | Iterator over parameters with names | `model.named_parameters()` |
| **`state_dict()`** | Dictionary of all parameters | `torch.save(model.state_dict(), "spam_model.pth")` |
| **Learning rate** | Step size during gradient descent | `0.001` |
| **Gradient** | Direction to reduce loss | `loss.backward()` computes it |
| **Optimiser** | Updates parameters using gradients | `torch.optim.SGD`, `Adam` |

---

## 14. Try it yourself

```python
import torch
import torch.nn as nn

# 1. Build a spam model
model = nn.Sequential(
    nn.Linear(5, 4),
    nn.ReLU(),
    nn.Linear(4, 1)
)

# 2. Count trainable parameters
print("Total parameters:", sum(p.numel() for p in model.parameters() if p.requires_grad))

# 3. Print parameter names
for name, param in model.named_parameters():
    print(f"{name}: {param.shape}")

# 4. Freeze the first layer
for param in model[0].parameters():
    param.requires_grad = False

# 5. Verify only the second layer trains
print("\nAfter freezing:")
for name, param in model.named_parameters():
    print(f"{name}: trainable = {param.requires_grad}")

# 6. Use an optimiser on only trainable parameters
optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=0.001
)

# 7. One fake training step
email = torch.tensor([[3.0, 1.0, 0.0, 0.20, 47.0]])
label = torch.tensor([[1.0]])

prediction = torch.sigmoid(model(email))
loss = nn.BCELoss()(prediction, label)

optimizer.zero_grad()
loss.backward()
optimizer.step()

print("\nLoss:", loss.item())
```

---

## Summary

- Parameters are the learnable numbers in a neural network: weights and biases.
- PyTorch creates them automatically when you use `nn.Linear` and other layers.
- `requires_grad=True` tells PyTorch to track gradients for a tensor.
- The optimiser updates parameters using gradients from backpropagation.
- You can freeze parameters by setting `requires_grad=False`.
- Saving `state_dict()` is the standard way to store a model's learned weights.
- For spam detection, the model learns weights that make suspicious features increase the spam score and trusted features decrease it.
