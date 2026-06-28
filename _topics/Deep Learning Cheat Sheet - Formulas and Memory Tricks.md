---
title: "Part 8: Deep Learning Cheat Sheet - Formulas and Memory Tricks"
category: Deep Learning
order: 8
tags:
  - deep-learning
  - cheat-sheet
  - formulas
  - memory-tricks
  - pytorch
  - spam-detection
  - reference
summary: A one-page reference for every deep learning formula and concept from the tutorial series, all using the spam-detection example. Each formula has a memory trick.
---

# Part 8: Deep Learning Cheat Sheet — Formulas and Memory Tricks

A quick reference for everything in the Deep Learning series. Every formula and concept uses the spam-detection example.

---

## 1. From email to tensor

### Real email

> "Congratulations! Click here to claim your prize."

### Feature vector

| Suspicious words | Links | Known sender | Capitals | Length |
|------------------|-------|--------------|----------|--------|
| 3 | 1 | 0 | 0.20 | 47 |

### Tensor

```python
email = torch.tensor([3.0, 1.0, 0.0, 0.20, 47.0])
```

> **Memory trick:** A tensor is a lunchbox with labelled compartments. Each position has a fixed meaning.

---

## 2. The artificial neuron

### Formula

```
z = Σ (xᵢ × wᵢ) + b
output = activation(z)
```

### Memory trick

> **"Shopping basket + bouncer."** Throw all `x × w` items into a basket, add the bias as the tip, then the activation function decides who gets in.

### Worked example

```
x = [3, 1, 0, 0.20, 47]
w = [0.8, 0.6, -1.2, 2.0, 0.01]
b = -1.0

z = (3×0.8) + (1×0.6) + (0×-1.2) + (0.20×2.0) + (47×0.01) - 1.0
z = 2.4 + 0.6 + 0 + 0.4 + 0.47 - 1.0
z = 2.87
```

---

## 3. Activation functions

| Function | Formula | Output Range | Use | Memory trick |
|----------|---------|--------------|-----|--------------|
| **Sigmoid** | `1 / (1 + e^(-z))` | 0 to 1 | Binary output | Thermometer with a 0-to-1 scale |
| **Tanh** | `(e^z - e^(-z)) / (e^z + e^(-z))` | -1 to 1 | Older hidden layers | Sigmoid stretched to -1..1 |
| **ReLU** | `max(0, z)` | 0 to ∞ | Most hidden layers | Bouncer that blocks negatives |
| **Softmax** | `e^(zᵢ) / Σ e^(zⱼ)` | 0 to 1, sum = 1 | Multi-class output | Normalised ranking |

For spam detection, the final output uses sigmoid:

```python
probability = torch.sigmoid(z)
# z = 2.87 -> probability ≈ 0.946
```

---

## 4. Forward pass

```
Input features
    ↓
Hidden layer: z = x @ W + b, then ReLU
    ↓
Output layer: z = h @ W + b, then sigmoid
    ↓
Spam probability
```

### PyTorch version

```python
model = nn.Sequential(
    nn.Linear(5, 4),
    nn.ReLU(),
    nn.Linear(4, 1),
    nn.Sigmoid()
)

email = torch.tensor([[3.0, 1.0, 0.0, 0.20, 47.0]])
probability = model(email)
```

> **Memory trick:** `z` = raw score, `a` = activated score, `p` = probability.

---

## 5. Loss functions

| Task | Loss | Formula | Memory trick |
|------|------|---------|--------------|
| **Regression** | MSE | `mean((y - ŷ)²)` | Average squared mistake |
| **Binary classification** | Binary Cross-Entropy | `-mean(y log(ŷ) + (1-y) log(1-ŷ))` | Punish confident wrong answers |

For spam detection, use binary cross-entropy:

```python
criterion = nn.BCELoss()
loss = criterion(prediction, label)
```

---

## 6. Gradient descent

```
new_weight = old_weight - learning_rate × gradient

gradient = ∂loss / ∂weight
```

> **Memory trick:** Gradient = direction of downhill. Learning rate = step size.

---

## 7. Chain rule

For a path from weight `w` to loss `L`:

```
∂L/∂w = ∂L/∂p × ∂p/∂z2 × ∂z2/∂a1 × ∂a1/∂z1 × ∂z1/∂w
```

> **Memory trick:** Chain rule = dominoes. Push the first one, trace the effect to the last one.

---

## 8. Training loop

```
for each epoch:
    for each batch of emails:
        1. Forward pass      -> spam probabilities
        2. Compute loss      -> how far from true labels?
        3. Zero gradients    -> optimizer.zero_grad()
        4. Backward pass     -> loss.backward()
        5. Update weights    -> optimizer.step()
```

> **Memory trick:** Predict -> Measure -> Clear -> Calculate -> Move. Repeat.

---

## 9. Tensors and shapes

| Object | Shape | Example |
|--------|-------|---------|
| One email | `[5]` | `torch.tensor([3, 1, 0, 0.20, 47])` |
| Batch of 4 emails | `[4, 5]` | 4 rows × 5 columns |
| Weights for 5 -> 1 | `[1, 5]` | `nn.Linear(5, 1).weight` |
| Hidden layer 5 -> 3 | `[3, 5]` | `nn.Linear(5, 3).weight` |
| Bias for output | `[1]` | `nn.Linear(5, 1).bias` |
| Scalar | `[]` | `torch.tensor(-1.0)` |

> **Memory trick:** Shape = address. Rows = examples, columns = features.

---

## 10. Tensor operations

| Operation | PyTorch | Rule | Spam Example |
|-----------|---------|------|--------------|
| Matrix multiply | `a @ b` | Inner dims match | `(4, 5) @ (5, 1) -> (4, 1)` |
| Transpose | `a.T` | Flip rows/columns | `layer.weight.T` |
| Reshape | `a.reshape(m, n)` | Total elements same | `emails.reshape(-1)` |
| Slice | `a[:, 0]` | All rows, column 0 | All suspicious-word counts |
| Mean | `a.mean(dim=0)` | Collapse rows | Average feature values |
| Sum | `a.sum()` | All elements | Total across all emails |

---

## 11. Dataset and DataLoader

```python
from torch.utils.data import Dataset, DataLoader

class SpamDataset(Dataset):
    def __init__(self, emails, labels):
        self.emails = torch.tensor(emails, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.emails)

    def __getitem__(self, idx):
        return self.emails[idx], self.labels[idx]

loader = DataLoader(SpamDataset(emails, labels), batch_size=32, shuffle=True)
```

> **Memory trick:** Dataset = single apple. DataLoader = bag of apples.

---

## 12. PyTorch parameters

| What | Code | Shape |
|------|------|-------|
| All parameters | `model.parameters()` | Iterator |
| Named parameters | `model.named_parameters()` | Iterator with names |
| Number of elements | `p.numel()` | Scalar |
| Gradient tracking | `p.requires_grad` | Boolean |
| Save model | `torch.save(model.state_dict(), "spam_model.pth")` | File |
| Load model | `model.load_state_dict(torch.load("spam_model.pth"))` | File |

---

## 13. Common optimisers

| Optimiser | Best For | Memory trick |
|-----------|----------|--------------|
| **SGD** | Simple convex problems | Plain vanilla gradient descent |
| **SGD + momentum** | Faster escape from flat areas | Rolling ball keeps going |
| **Adam** | Most deep learning | Adapts learning rate per parameter |

For spam detection, start with Adam:

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

---

## 14. Overfitting vs underfitting

| | Underfitting | Good Fit | Overfitting |
|--|---------------|----------|-------------|
| **Training loss** | High | Low | Very low |
| **Validation loss** | High | Low | High |
| **Fix** | Bigger model, more features | Keep going | Regularisation, more data, early stopping |

> **Memory trick:** Underfitting = too dumb. Overfitting = too memorised. Good fit = just right.

---

## 15. Regularisation

| Method | How | Memory trick |
|--------|-----|--------------|
| **Dropout** | Randomly zero some neurons during training | Practise with one hand tied |
| **L2 (Weight decay)** | Penalise large weights | Keep weights small and humble |
| **Early stopping** | Stop when validation loss stops improving | Quit while you are ahead |
| **Data augmentation** | Generate modified training samples | Show more variations |

---

## 16. Key PyTorch imports

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset, random_split
```

---

## 17. Twenty memory tricks

1. **Tensor** = lunchbox with labelled compartments.
2. **Rows = examples, columns = features.**
3. **Weight** = volume knob.
4. **Bias** = starting mood.
5. **Raw score** = pre-decision number.
6. **Sigmoid** = thermometer with 0-to-1 scale.
7. **ReLU** = bouncer (positive in, negative out).
8. **Softmax** = normalised ranking.
9. **Weights** = synapses.
10. **Gradient** = direction of downhill.
11. **Learning rate** = step size.
12. **Epoch** = one full pass through the dataset.
13. **Batch** = one slice of emails.
14. **Forward pass** = prediction.
15. **Backward pass** = blame assignment.
16. **Loss** = how wrong you are.
17. **Optimiser** = the thing that moves weights.
18. **Matrix multiply** = inner dimensions must match.
19. **Broadcasting** = 1 stretches to fit.
20. **Dataset** = one apple; **DataLoader** = bag of apples.

---

## 18. Common mistakes

| Mistake | Fix |
|---------|-----|
| Shape mismatch in `matmul` | Check inner dimensions match |
| Forgetting `zero_grad()` | Call it every training step |
| Using sigmoid for multi-class output | Use softmax |
| Shuffling validation data | Set `shuffle=False` |
| Not moving tensors/model to GPU | Use `.to(device)` |
| Not normalising features | Scale inputs before training |
| Too large learning rate | Try 0.001 first |
| Not checking train vs val loss | Plot both to spot overfitting |
| Confusing raw score and probability | Apply sigmoid to raw score |
| Forgetting batch dimension | Use `[[3, 1, 0, 0.20, 47]]` not `[3, 1, 0, 0.20, 47]` |

---

## Summary

- The spam-detection example is the thread that runs through every tutorial.
- A neuron multiplies inputs by weights, adds a bias, and applies an activation.
- Sigmoid turns raw scores into probabilities. ReLU is the most common hidden activation.
- Training is a loop: predict, measure loss, clear gradients, calculate gradients, update weights.
- Tensors are multi-dimensional arrays. Shape is the most important thing to check.
- `Dataset` provides one sample; `DataLoader` provides batches.
- Parameters have `requires_grad=True` so PyTorch can update them.
- Deep learning mirrors brain ideas but is a mathematical pattern recogniser, not a mind.
