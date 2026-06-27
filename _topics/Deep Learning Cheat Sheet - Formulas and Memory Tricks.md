---
title: "Deep Learning Cheat Sheet - Formulas and Memory Tricks"
category: Deep Learning
order: 7
tags:
  - deep-learning
  - cheat-sheet
  - formulas
  - memory-tricks
  - pytorch
  - reference
  - beginners
summary: A one-page reference for every deep learning formula, concept, and memory trick from the tutorial series. Covers neurons, tensors, activations, training, and PyTorch code snippets.
---

# Deep Learning Cheat Sheet — Formulas and Memory Tricks

A quick reference for everything in the Deep Learning series. Each formula has a memory trick to help you remember it.

---

## 1. The Artificial Neuron

### Formula

```
z = Σ (xᵢ × wᵢ) + b
output = activation(z)
```

### Memory Trick

> **"Shopping basket + bouncer"** — throw all `x × w` items into a basket, add the bias as the tip, then the activation function decides who gets in.

---

## 2. Activation Functions

| Function | Formula | Output Range | Use | Memory Trick |
|----------|---------|--------------|-----|--------------|
| **Sigmoid** | `σ(z) = 1 / (1 + e^(-z))` | 0 to 1 | Binary output | Letter `S` looks like the curve |
| **Tanh** | `(e^z - e^(-z)) / (e^z + e^(-z))` | -1 to 1 | Symmetric hidden | Sigmoid stretched to -1..1 |
| **ReLU** | `max(0, z)` | 0 to ∞ | Hidden layers | Bouncer: positive in, negative out |
| **Leaky ReLU** | `max(0.01z, z)` | -∞ to ∞ | ReLU fix | Let a little negative through |
| **Softmax** | `e^(zᵢ) / Σ e^(zⱼ)` | 0 to 1, sum = 1 | Multi-class output | Normalised ranking |

---

## 3. Forward Pass

```
Layer 1: z₁ = x · W₁ + b₁      a₁ = activation(z₁)
Layer 2: z₂ = a₁ · W₂ + b₂     a₂ = activation(z₂)
Output:  z₃ = a₂ · W₃ + b₃     ŷ = activation(z₃)
```

### Memory Trick

> **z = raw score, a = activated score.** z is "before", a is "after".

---

## 4. Loss Functions

| Task | Loss | Formula | Memory Trick |
|------|------|---------|--------------|
| **Regression** | MSE | `mean((y - ŷ)²)` | Average squared mistake |
| **Binary classification** | Binary Cross-Entropy | `-mean(y log(ŷ) + (1-y) log(1-ŷ))` | Punish confident wrong answers |
| **Multi-class classification** | Cross-Entropy | `-mean(log(ŷ[correct class]))` | Only penalise the true class probability |

---

## 5. Gradient Descent

```
new_weight = old_weight - learning_rate × gradient

gradient = ∂loss / ∂weight
```

### Memory Trick

> **Gradient = direction of downhill. Learning rate = step size.** Walk down the hill one step at a time.

---

## 6. Training Loop

```
for each epoch:
    for each batch:
        1. Forward pass      → ŷ
        2. Compute loss      → loss(y, ŷ)
        3. Zero gradients    → optimizer.zero_grad()
        4. Backward pass     → loss.backward()
        5. Update weights    → optimizer.step()
```

### Memory Trick

> **Predict → Measure → Clear → Calculate → Move.** Repeat.

---

## 7. Tensors

| Object | Dimensions | PyTorch Code |
|--------|------------|--------------|
| Scalar | 0D | `torch.tensor(5.0)` |
| Vector | 1D | `torch.tensor([1, 2, 3])` |
| Matrix | 2D | `torch.tensor([[1, 2], [3, 4]])` |
| 3D tensor | 3D | `torch.tensor([[[1, 2]]])` |

### Memory Trick

> **Shape = address.** Read from biggest container to smallest detail.

---

## 8. Tensor Operations

| Operation | PyTorch | Rule |
|-----------|---------|------|
| Addition | `a + b` | Shapes broadcast |
| Element-wise mult | `a * b` | Same shape |
| Matrix multiply | `a @ b` or `torch.matmul(a, b)` | `(a, b) @ (b, c) → (a, c)` |
| Transpose | `a.T` | Flip rows and columns |
| Reshape | `a.reshape(m, n)` | Total elements must match |
| Sum | `a.sum()` | Reduces all dims |
| Mean | `a.mean(dim=0)` | Reduce along dim |

---

## 9. Broadcasting Rule

> **Dimensions must match or one of them must be 1.** A 1 "stretches" to match the larger size.

```
(3, 3) + (3,) → (3, 3) + (3, 3) → (3, 3)
(2, 1) + (1, 3) → (2, 3)
```

---

## 10. Dataset and DataLoader

```python
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

dataset = MyDataset(X, y)
loader = DataLoader(dataset, batch_size=32, shuffle=True)
```

### Memory Trick

> **Dataset = single apple. DataLoader = bag of apples.**

---

## 11. PyTorch Parameters

| What | Code | Shape |
|------|------|-------|
| All parameters | `model.parameters()` | Iterator |
| Named parameters | `model.named_parameters()` | Iterator with names |
| Number of elements | `p.numel()` | Scalar |
| Gradient tracking | `p.requires_grad` | Boolean |
| Save model | `torch.save(model.state_dict(), "model.pth")` | File |
| Load model | `model.load_state_dict(torch.load("model.pth"))` | File |

---

## 12. Common Optimisers

| Optimiser | Best For | Memory Trick |
|-----------|----------|--------------|
| **SGD** | Simple convex problems | Plain vanilla gradient descent |
| **SGD + momentum** | Faster escape from flat areas | Rolling ball keeps going |
| **Adam** | Most deep learning | Adapts learning rate per parameter |
| **RMSprop** | Recurrent networks | Keeps moving average of squared gradients |

---

## 13. Overfitting vs Underfitting

| | Underfitting | Good Fit | Overfitting |
|--|---------------|----------|-------------|
| **Training loss** | High | Low | Very low |
| **Validation loss** | High | Low | High |
| **Fix** | Bigger model, more features | Keep going | Regularisation, more data, early stopping |

### Memory Trick

> **Underfitting = too dumb. Overfitting = too memorised. Good fit = just right.**

---

## 14. Regularisation

| Method | How | Memory Trick |
|--------|-----|--------------|
| **Dropout** | Randomly zero some neurons during training | Make the network practise with one hand tied |
| **L2 (Weight decay)** | Penalise large weights | Keep weights small and humble |
| **Early stopping** | Stop when validation loss stops improving | Quit while you are ahead |
| **Data augmentation** | Generate modified training samples | Show the model more variations |

---

## 15. Key PyTorch Imports

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset, random_split
```

---

## 16. Twenty Memory Tricks

1. **Neuron** = basket + bouncer.
2. **z** = raw score; **a** = activated score.
3. **Sigmoid** = S-shaped squasher.
4. **ReLU** = bouncer (positive in, negative out).
5. **Softmax** = turns scores into probabilities.
6. **Weights** = synapses.
7. **Bias** = starting mood.
8. **Gradient** = direction of downhill.
9. **Learning rate** = step size.
10. **Epoch** = one full pass through the data.
11. **Batch** = one slice of data.
12. **Forward pass** = prediction.
13. **Backward pass** = blame assignment.
14. **Loss** = how wrong you are.
15. **Optimizer** = the thing that moves weights.
16. **Tensor** = numbered box of data.
17. **Shape** = address from big to small.
18. **Broadcasting** = 1 stretches to fit.
19. **Dataset** = one apple; **DataLoader** = bag of apples.
20. **requires_grad=True** = still learning.

---

## 17. Common Mistakes

| Mistake | Fix |
|---------|-----|
| Shape mismatch in `matmul` | Check inner dimensions match |
| Forgetting `zero_grad()` | Call it every training step |
| Using `sigmoid` for multi-class output | Use `softmax` |
| Shuffling validation data | Set `shuffle=False` |
| Not moving tensors/model to GPU | Use `.to(device)` |
| Not normalising data | Scale inputs before training |
| Too large learning rate | Try 0.001 first |
| Not checking train vs val loss | Plot both to spot overfitting |

---

## Summary

- The neuron formula is `z = Σ xw + b`, then activation.
- Common activations: sigmoid (0..1), tanh (-1..1), ReLU (most popular), softmax (probabilities).
- Training is a loop: predict → measure → clear → calculate → move.
- Tensors are multi-dimensional arrays; shape is the most important thing to check.
- Dataset provides one sample; DataLoader provides batches.
- Parameters have `requires_grad=True` so PyTorch can update them.
- The brain analogy is helpful, but neural networks are mathematical tools.
