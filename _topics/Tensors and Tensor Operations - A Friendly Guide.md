---
title: "Part 3: Tensors and Tensor Operations - A Friendly Guide"
category: Deep Learning
order: 3
tags:
  - deep-learning
  - pytorch
  - tensors
  - tensor-operations
  - spam-detection
  - beginners
  - friendly
summary: Learn tensors and tensor operations using the same spam-detection example. Covers feature vectors, batches of emails, weights, matrix multiplication, broadcasting, and reshaping.
---

# Part 3: Tensors and Tensor Operations — A Friendly Guide

Everything in a spam-detection model is a tensor. The email features are a tensor, the weights are a tensor, the bias is a tensor, and even the final probability is a tensor. In this guide, we will see exactly how those tensors work.

---

## 1. What is a tensor?

A tensor is a multi-dimensional array of numbers. The same idea appears at different scales.

| Tensor Type | Dimensions | Spam Example |
|-------------|------------|--------------|
| **Scalar** | 0D | One number, such as the bias `-1.0` |
| **Vector** | 1D | One email's features: `[3, 1, 0, 0.20, 47]` |
| **Matrix** | 2D | A batch of emails: 4 rows × 5 columns |
| **3D tensor** | 3D+ | A collection of email batches over several training steps |

> **Memory trick:** A tensor is a numbered box. 0D is a single number, 1D is a list, 2D is a table, 3D is a stack of tables.

---

## 2. One email as a tensor

Recall our spam email features:

| Suspicious words | Links | Known sender | Capitals | Length |
|------------------|-------|--------------|----------|--------|
| 3 | 1 | 0 | 0.20 | 47 |

In PyTorch:

```python
import torch

email = torch.tensor([
    3.0,    # suspicious words
    1.0,    # links
    0.0,    # known sender
    0.20,   # capitals
    47.0    # length
])

print(email)
print(email.shape)  # torch.Size([5])
```

Output:

```
tensor([ 3.0000,  1.0000,  0.0000,  0.2000, 47.0000])
torch.Size([5])
```

This tensor has **one dimension** and **five elements**. The shape tells us how many numbers live along each dimension.

> **Memory trick:** Shape is like a mailing address. It answers "how many?" at each level.

---

## 3. Many emails as a 2D tensor

During training, we do not process one email at a time. We process a **batch** of emails. Each row is one email, and each column is one feature.

```python
emails = torch.tensor([
    # susp, link, known, caps, len
    [3.0,  1.0,  0.0,  0.20, 47.0],  # spammy
    [0.0,  0.0,  1.0,  0.02, 82.0],  # normal
    [5.0,  4.0,  0.0,  0.45, 31.0],  # very spammy
    [1.0,  0.0,  1.0,  0.05, 120.0]  # normal
])

print(emails.shape)  # torch.Size([4, 5])
```

The shape `[4, 5]` means:

```
4 emails (rows)
5 features (columns)
```

> **Memory rule:** Rows = examples, columns = features.

---

## 4. Weights and bias as tensors

The weights for our single-neuron spam model are also a tensor:

```python
weights = torch.tensor([
    0.8,    # suspicious words
    0.6,    # links
   -1.2,    # known sender
    2.0,    # capitals
    0.01    # length
])

print(weights.shape)  # torch.Size([5])

bias = torch.tensor(-1.0)
print(bias.shape)  # torch.Size([])
```

The weights are a 1D tensor with five elements. The bias is a scalar tensor with an empty shape, meaning it has no dimensions.

---

## 5. Common tensor creation helpers

PyTorch provides helpers to create common tensors. These are useful when building models or initialising data.

```python
import torch

# Zeros: sometimes used for initialising bias
zeros = torch.zeros(5)

# Ones
ones = torch.ones(4, 5)

# Random values between 0 and 1
random_values = torch.rand(4, 5)

# Random values from a normal distribution (bell curve)
# Most weights in a new model start like this
weights = torch.randn(5, 3)

# Numbers from 0 to 9
steps = torch.arange(10)

# Numbers evenly spaced between 0 and 1
levels = torch.linspace(0, 1, 5)
# tensor([0.00, 0.25, 0.50, 0.75, 1.00])
```

---

## 6. Matrix multiplication: one email at a time

When we compute the raw spam score for one email, we multiply the email vector by the weight vector and add the bias:

```python
email = torch.tensor([3.0, 1.0, 0.0, 0.20, 47.0])
weights = torch.tensor([0.8, 0.6, -1.2, 2.0, 0.01])
bias = torch.tensor(-1.0)

raw_score = email @ weights + bias
print(raw_score)  # tensor(2.8700)
```

The `@` operator performs **matrix multiplication**. For two 1D tensors of the same length, it is the same as a dot product: multiply matching positions and add the results.

| Position | email | weights | product |
|----------|-------|---------|---------|
| 0 | 3.0 | 0.8 | 2.4 |
| 1 | 1.0 | 0.6 | 0.6 |
| 2 | 0.0 | -1.2 | 0.0 |
| 3 | 0.20 | 2.0 | 0.4 |
| 4 | 47.0 | 0.01 | 0.47 |

Sum of products: `2.4 + 0.6 + 0.0 + 0.4 + 0.47 = 3.87`

Add bias: `3.87 - 1.0 = 2.87`

> **Memory trick:** Matrix multiplication is a row of waiters each carrying one plate. Each plate is a feature multiplied by its weight. The total bill is the sum.

---

## 7. Matrix multiplication: a batch of emails at once

The real power comes from processing many emails at once. If the emails tensor has shape `(4, 5)` and the weights tensor has shape `(5,)`, then:

```
(4, 5) @ (5,) -> (4,)
```

PyTorch multiplies each of the four rows by the weight vector, producing four raw scores.

```python
emails = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0],
    [5.0, 4.0, 0.0, 0.45, 31.0],
    [1.0, 0.0, 1.0, 0.05, 120.0]
])

weights = torch.tensor([0.8, 0.6, -1.2, 2.0, 0.01])
bias = torch.tensor(-1.0)

raw_scores = emails @ weights + bias
print(raw_scores)
# tensor([ 2.8700, -2.1800,  6.5600, -2.9500])

print(raw_scores.shape)  # torch.Size([4])
```

Each number is the raw score for one email. The first email scored `2.87`, the second scored `-2.18`, and so on.

> **Memory trick:** The inner dimensions must match. Here the inner dimension is `5` (features), so `(4, 5) @ (5,)` becomes `(4,)`.

---

## 8. Why PyTorch layers use a 2D weight tensor

In practice, PyTorch stores weights for a layer in a 2D tensor. For a layer with 5 inputs and 1 output, the weight tensor has shape `(1, 5)`:

```python
import torch.nn as nn

layer = nn.Linear(5, 1)
print(layer.weight.shape)  # torch.Size([1, 5])
print(layer.bias.shape)    # torch.Size([1])
```

To compute the output, PyTorch effectively does:

```python
output = emails @ layer.weight.T + layer.bias
```

The transpose `.T` flips the weight tensor from `(1, 5)` to `(5, 1)`, so the multiplication works:

```
(4, 5) @ (5, 1) -> (4, 1)
```

This is why the output shape is `(4, 1)` instead of `(4,)`.

> **Memory trick:** PyTorch stores weights as rows. To multiply, we turn the rows into columns with `.T`.

---

## 9. The shape of a hidden layer

Suppose we add a hidden layer with 3 neurons to our spam model. The first layer turns 5 features into 3 hidden values. The weight tensor has shape `(3, 5)`:

```python
hidden_layer = nn.Linear(5, 3)
print(hidden_layer.weight.shape)  # torch.Size([3, 5])
print(hidden_layer.bias.shape)    # torch.Size([3])

emails = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0]
])

hidden_scores = hidden_layer(emails)
print(hidden_scores.shape)  # torch.Size([2, 3])
```

The input shape is `(2, 5)`. The layer computes `(2, 5) @ (5, 3) -> (2, 3)`. Each of the two emails now has three hidden scores.

> **Memory trick:** A linear layer is a shape transformer. The number of columns going in becomes the number of columns coming out.

---

## 10. Broadcasting with the bias

Notice that the bias tensor has shape `(1,)`, but PyTorch adds it to every row of the output. This is **broadcasting**. PyTorch automatically stretches the small tensor to match the big one.

```python
emails = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0],
    [5.0, 4.0, 0.0, 0.45, 31.0],
    [1.0, 0.0, 1.0, 0.05, 120.0]
])

weights = torch.tensor([
    [0.8],
    [0.6],
    [-1.2],
    [2.0],
    [0.01]
])

bias = torch.tensor([[-1.0]])

scores = emails @ weights + bias
print(scores)
# tensor([[ 2.8700],
#         [-2.1800],
#         [ 6.5600],
#         [-2.9500]])
```

The bias `[[-1.0]]` was broadcast to all four rows. This is a common pattern in neural networks: the same bias is added to every example.

> **Memory trick:** A shape of `1` is an elastic band. It stretches to fit the larger shape.

---

## 11. Reshaping tensors

Sometimes the shape of a tensor is not what a layer expects. For example, a spam model might need the input in a different format. We can reshape without changing the data.

```python
emails = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0]
])

print(emails.shape)  # torch.Size([2, 5])

# Flatten into one long vector
flat = emails.reshape(-1)
print(flat.shape)    # torch.Size([10])
print(flat)
# tensor([3.0, 1.0, 0.0, 0.20, 47.0, 0.0, 0.0, 1.0, 0.02, 82.0])

# Reshape back, but with one batch dimension and one feature dimension
back = flat.reshape(2, 5)
print(back.shape)    # torch.Size([2, 5])
```

The `-1` tells PyTorch to infer the size of that dimension. The total number of elements must stay the same.

> **Memory trick:** Reshaping is like repacking the same marbles into a different box. The marbles do not change; only the box changes.

---

## 12. Slicing and indexing emails

We often need to look at a subset of the data. Slicing lets us do that.

```python
emails = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],  # email 0
    [0.0, 0.0, 1.0, 0.02, 82.0],  # email 1
    [5.0, 4.0, 0.0, 0.45, 31.0],  # email 2
    [1.0, 0.0, 1.0, 0.05, 120.0]  # email 3
])

# Get the first email
print(emails[0])
# tensor([3.0, 1.0, 0.0, 0.20, 47.0])

# Get the suspicious-word count for all emails
print(emails[:, 0])
# tensor([3.0, 0.0, 5.0, 1.0])

# Get the first two emails and the first two features
print(emails[0:2, 0:2])
# tensor([[3.0, 1.0],
#         [0.0, 0.0]])

# Get the last email
print(emails[-1])
# tensor([1.0, 0.0, 1.0, 0.05, 120.0])
```

> **Memory trick:** `emails[:, 0]` means "all rows, column 0." The colon is like a wildcard.

---

## 13. Reduction operations

Reductions collapse a dimension into a single number. For example, we might want the average number of suspicious words across all emails.

```python
emails = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0],
    [5.0, 4.0, 0.0, 0.45, 31.0],
    [1.0, 0.0, 1.0, 0.05, 120.0]
])

# Average across all emails and all features
print(emails.mean())  # tensor(1.3680)

# Average number of suspicious words (column 0)
print(emails[:, 0].mean())  # tensor(2.25)

# Average of each feature across all emails
print(emails.mean(dim=0))
# tensor([2.2500, 1.2500, 0.5000, 0.1800, 70.0000])
```

`dim=0` means "collapse the rows" — in other words, compute the average feature value across all emails.

> **Memory trick:** `dim=0` means vertical collapse. `dim=1` means horizontal collapse.

---

## 14. Moving tensors to GPU

If you have a GPU, you can move tensors there for faster computation. This is especially useful for large batches of emails or big models.

```python
# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# Move emails to GPU
emails = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0]
]).to(device)

# Create a model on GPU
model = nn.Linear(5, 1).to(device)

# Forward pass happens on GPU
probabilities = torch.sigmoid(model(emails))
print(probabilities)
```

> **Memory trick:** GPU is like a fast factory. CPU is like a hand workshop. For big jobs, use the factory.

---

## 15. Common mistakes

| Mistake | Why it happens | Fix |
|---------|----------------|-----|
| Shape mismatch in matrix multiplication | Inner dimensions do not match | Check shapes with `.shape` before multiplying |
| Forgetting the batch dimension | `nn.Linear` expects `(batch, features)` | Add a leading dimension: `[[...]]` |
| Confusing `*` and `@` | `*` is element-wise; `@` is matrix multiplication | Use `@` for neural network layers |
| Wrong `dim` in reduction | `dim=0` collapses rows; `dim=1` collapses columns | Think about which dimension you want to remove |
| Reshaping into incompatible sizes | Total number of elements must stay the same | Use `-1` to let PyTorch infer one dimension |
| Mixing CPU and GPU tensors | Operations need both tensors on the same device | Move both to the same device with `.to(device)` |

---

## 16. Quick review

| Term | Meaning | Spam Example |
|------|---------|--------------|
| **Tensor** | A container of numbers | Email features, weights, probabilities |
| **Shape** | Size of each dimension | `(4, 5)` means 4 emails, 5 features |
| **Scalar** | 0D tensor | The bias `-1.0` |
| **Vector** | 1D tensor | One email: `[3, 1, 0, 0.20, 47]` |
| **Matrix** | 2D tensor | A batch of emails |
| **Matrix multiplication** | Multiply rows by columns and sum | `(4, 5) @ (5, 1) -> (4, 1)` |
| **Transpose** | Flip rows and columns | `layer.weight.T` |
| **Broadcasting** | Stretch a small tensor to match a bigger one | Adding a bias to every row |
| **Reshape** | Change dimensions without changing data | `emails.reshape(-1)` |
| **Slicing** | Select a subset | `emails[:, 0]` for all suspicious-word counts |
| **Reduction** | Collapse a dimension | `emails.mean(dim=0)` for average feature values |

---

## 17. Try it yourself

```python
import torch
import torch.nn as nn

# 1. Create a batch of 4 emails with 5 features
emails = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0],
    [5.0, 4.0, 0.0, 0.45, 31.0],
    [1.0, 0.0, 1.0, 0.05, 120.0]
])

# 2. Create a linear layer: 5 inputs -> 1 output
layer = nn.Linear(5, 1)

# 3. Compute raw scores for all emails at once
scores = layer(emails)
print("Scores shape:", scores.shape)
print(scores)

# 4. Apply sigmoid to get probabilities
probabilities = torch.sigmoid(scores)
print("Probabilities:")
print(probabilities)

# 5. Average probability across all emails
print("Average probability:", probabilities.mean().item())

# 6. Get the suspicious-word count for all emails
print("Suspicious-word counts:", emails[:, 0])
```

---

## Summary

- A tensor is a multi-dimensional array of numbers. Spam emails, weights, and biases are all tensors.
- Shape tells you how many dimensions the tensor has and how big each one is.
- Matrix multiplication is the core operation of neural networks. Inner dimensions must match.
- PyTorch stores layer weights as `(out_features, in_features)` and transposes them during multiplication.
- Broadcasting automatically stretches a small tensor, such as a bias, to match a larger one.
- Reshaping, slicing, and reductions are everyday tools for working with data.
- Always check tensor shapes before debugging anything else.
