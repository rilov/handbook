---
title: "Tensors and Tensor Operations - A Friendly Guide"
category: Deep Learning
order: 3
tags:
  - deep-learning
  - pytorch
  - tensors
  - tensor-operations
  - beginners
  - friendly
summary: Learn what tensors are, how to create them in PyTorch, and how to perform the operations that power every neural network — with memory tricks for shapes and broadcasting.
---

# Tensors and Tensor Operations — A Friendly Guide

Everything in PyTorch is a **tensor**. Inputs, weights, biases, and gradients are all tensors. If you understand tensors, you understand half of deep learning.

---

## 1. What Is a Tensor?

A tensor is just a multi-dimensional array of numbers.

| Tensor Type | Dimensions | Real-Life Example |
|-------------|------------|-------------------|
| **Scalar** | 0D | A single number: `5.0` |
| **Vector** | 1D | A list of numbers: `[2, 3, 5]` |
| **Matrix** | 2D | A table of numbers: spreadsheet rows and columns |
| **Tensor** | 3D+ | A stack of matrices, like a video (frames × height × width) |

> **Memory trick:** A tensor is a "numbered box" — 0D is a point, 1D is a line, 2D is a flat grid, 3D is a cube, and 4D+ is a cube of cubes.

---

## 2. Creating Tensors in PyTorch

```python
import torch

# Scalar
scalar = torch.tensor(5.0)
print(scalar, scalar.shape)

# Vector
vector = torch.tensor([1, 2, 3, 4])
print(vector, vector.shape)

# Matrix
matrix = torch.tensor([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print(matrix, matrix.shape)

# 3D tensor
tensor_3d = torch.tensor([
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
])
print(tensor_3d, tensor_3d.shape)
```

### Output

```
tensor(5.) torch.Size([])
tensor([1, 2, 3, 4]) torch.Size([4])
tensor([[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]) torch.Size([3, 3])
tensor([[[1, 2],
         [3, 4]],
        [[5, 6],
         [7, 8]]]) torch.Size([2, 2, 2])
```

---

## 3. Tensor Shapes and What They Mean

The shape of a tensor tells you how many dimensions it has and how big each one is.

```
shape = torch.Size([batch_size, channels, height, width])

For one colour image:
  [1, 3, 224, 224]
   │  │   │    └─ width in pixels
   │  │   └──── height in pixels
   │  └───────── RGB channels (3 for red, green, blue)
   └──────────── one image in this batch
```

> **Memory trick:** Read shape like a mailing address — biggest container first, smallest detail last.

---

## 4. Common Tensor Creation Helpers

```python
import torch

# Zeros
torch.zeros(3, 3)
# tensor([[0., 0., 0.],
#         [0., 0., 0.],
#         [0., 0., 0.]])

# Ones
torch.ones(2, 4)

# Random values between 0 and 1
torch.rand(3, 3)

# Random values from a normal distribution (mean=0, std=1)
torch.randn(3, 3)

# A range of numbers (like Python range)
torch.arange(0, 10)
# tensor([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# Linearly spaced values
torch.linspace(0, 1, 5)
# tensor([0.00, 0.25, 0.50, 0.75, 1.00])
```

---

## 5. Basic Tensor Operations

### Arithmetic

```python
import torch

a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])

print(a + b)       # tensor([5, 7, 9])
print(a - b)       # tensor([-3, -3, -3])
print(a * b)       # element-wise multiplication: tensor([4, 10, 18])
print(a / b)       # tensor([0.25, 0.40, 0.50])

# Scalar operations
print(a + 10)      # tensor([11, 12, 13])
print(a * 2)       # tensor([2, 4, 6])
```

### Matrix Multiplication

Matrix multiplication is the heart of neural networks.

```
For a layer:  output = input @ W + b

If input has shape (batch_size, in_features)
And W has shape (in_features, out_features)
Then output has shape (batch_size, out_features)
```

**Memory trick:** The inner dimensions must match, and the outer dimensions become the result.

```
(a, b) @ (b, c) → (a, c)
    ^     ^       ^
    └─────┘       └────── inner dimensions cancel
```

```python
A = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])      # shape (2, 3)

B = torch.tensor([[1, 2],
                  [3, 4],
                  [5, 6]])          # shape (3, 2)

C = A @ B  # or torch.matmul(A, B)
print(C)
# tensor([[22, 28],
#         [49, 64]])

# Check: (2, 3) @ (3, 2) → (2, 2)
print(C.shape)  # torch.Size([2, 2])
```

### Transpose

Transpose flips a matrix over its diagonal.

```python
A = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])

print(A.T)
# tensor([[1, 4],
#         [2, 5],
#         [3, 6]])
```

---

## 6. Reshaping Tensors

```python
import torch

x = torch.arange(12)
print(x)        # tensor([0, 1, 2, ..., 11])
print(x.shape)  # torch.Size([12])

# Reshape to 3 rows × 4 columns
x = x.reshape(3, 4)
print(x)
# tensor([[ 0,  1,  2,  3],
#         [ 4,  5,  6,  7],
#         [ 8,  9, 10, 11]])

# Reshape to 2 batches × 2 channels × 3 values
x = x.reshape(2, 2, 3)
print(x.shape)  # torch.Size([2, 2, 3])

# -1 means "infer this dimension"
x = torch.arange(12).reshape(3, -1)
print(x.shape)  # torch.Size([3, 4])
```

> **Memory trick:** Reshaping is like repacking the same marbles into a different box — the number of marbles stays the same.

---

## 7. Slicing and Indexing

```python
import torch

x = torch.tensor([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# First row
print(x[0])       # tensor([1, 2, 3])

# First column
print(x[:, 0])    # tensor([1, 4, 7])

# Element at row 1, column 2
print(x[1, 2])    # tensor(6)

# Last row
print(x[-1])      # tensor([7, 8, 9])

# Sub-matrix: rows 0-1, columns 1-2
print(x[0:2, 1:3])
# tensor([[2, 3],
#         [5, 6]])
```

---

## 8. Broadcasting

Broadcasting lets PyTorch work with tensors of different shapes without copying data.

**Simple rule:** If dimensions match, great. If one is 1, PyTorch "stretches" it to match.

```python
import torch

A = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])    # shape (2, 3)

b = torch.tensor([10, 20, 30])   # shape (3,) → broadcasted to (2, 3)

print(A + b)
# tensor([[11, 22, 33],
#         [14, 25, 36]])
```

> **Memory trick:** A shape of `1` is like an elastic band — it stretches to fit the larger shape.

---

## 9. Reduction Operations

Reductions collapse a dimension into a single number.

```python
import torch

x = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])

print(x.sum())      # tensor(21)
print(x.mean())     # tensor(3.5)
print(x.max())      # tensor(6)
print(x.min())      # tensor(1)

# Reduce along a specific dimension
print(x.sum(dim=0))   # sum each column: tensor([5, 7, 9])
print(x.sum(dim=1))   # sum each row:   tensor([ 6, 15])

# Keep the dimension for later broadcasting
print(x.sum(dim=1, keepdim=True))
# tensor([[ 6],
#         [15]])
```

---

## 10. Tensors in a Neural Network

Here is how tensors flow through a model:

```
Input tensor:      shape (batch_size, in_features)
Weight tensor:     shape (in_features, out_features)
Bias tensor:       shape (out_features,)
Output tensor:     shape (batch_size, out_features)
```

```python
import torch
import torch.nn as nn

# One batch of 4 samples, each with 3 features
x = torch.randn(4, 3)

# Linear layer: 3 inputs, 5 outputs
layer = nn.Linear(3, 5)

# Forward pass
output = layer(x)
print(output.shape)  # torch.Size([4, 5])

# Access the weights and biases
print(layer.weight.shape)  # torch.Size([5, 3])
print(layer.bias.shape)    # torch.Size([5])
```

Notice that `layer.weight` has shape `(5, 3)` even though the output is `(4, 5)` and the input is `(4, 3)`. PyTorch stores the weight transposed internally, so the math works out as:

```
output = x @ W^T + b
```

---

## 11. Moving Tensors to GPU

If you have a GPU, you can move tensors there for faster computation.

```python
import torch

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# Create tensor on GPU
x = torch.randn(3, 3).to(device)

# Or create directly on GPU
y = torch.randn(3, 3, device=device)

# Model on GPU
model = nn.Linear(10, 1).to(device)
```

---

## 12. Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|----------------|-----|
| Shape mismatch in matrix multiplication | Inner dimensions do not match | Use `.T` or reshape to align shapes |
| Forgetting `.item()` on a scalar tensor | PyTorch tensors do not print as plain numbers | Call `scalar.item()` |
| In-place operations break gradients | PyTorch cannot track in-place changes | Use out-of-place ops like `x = x + 1` |
| Mixing CPU and GPU tensors | Operations need both tensors on the same device | Move both to same device with `.to(device)` |
| Wrong `dim` for reduction | PyTorch `dim` is the dimension to *collapse* | Read `dim=0` as "collapse rows" |

---

## 13. Quick Review

| Term | Meaning | Example |
|------|---------|---------|
| **Scalar** | 0D tensor | `torch.tensor(5.0)` |
| **Vector** | 1D tensor | `torch.tensor([1, 2, 3])` |
| **Matrix** | 2D tensor | `torch.tensor([[1, 2], [3, 4]])` |
| **Shape** | Size of each dimension | `torch.Size([2, 3, 4])` |
| **Reshape** | Change dimensions without changing data | `x.reshape(2, -1)` |
| **Transpose** | Flip rows and columns | `A.T` |
| **Matrix multiplication** | `output = input @ W` | `(2, 3) @ (3, 4) → (2, 4)` |
| **Broadcasting** | Stretch a small tensor to match a bigger one | `[10, 20, 30]` added to a `(2, 3)` matrix |
| **Reduction** | Collapse a dimension into one number | `x.sum()`, `x.mean(dim=0)` |

---

## 14. Try It Yourself

```python
import torch

# 1. Create a 3×4 matrix of random numbers
A = torch.randn(3, 4)

# 2. Add 5 to every element
A = A + 5

# 3. Multiply by a column vector
b = torch.tensor([[1], [2], [3]])
print(A * b)  # broadcasting

# 4. Compute the mean of each column
print(A.mean(dim=0))

# 5. Reshape to 2×6
print(A.reshape(2, 6))

# 6. Matrix multiply with a 4×2 matrix
B = torch.randn(4, 2)
C = A @ B
print(C.shape)
```

---

## Summary

- A tensor is a multi-dimensional array of numbers.
- PyTorch tensors support GPU acceleration and automatic gradient tracking.
- Matrix multiplication is the core operation of neural networks.
- Broadcasting lets you combine tensors of different shapes cleanly.
- Reductions, reshaping, and slicing are the everyday tools you need.
- Always check tensor shapes before debugging anything else.
