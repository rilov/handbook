---
title: "NumPy Cheat Sheet - Print Reference"
category: Python
tags:
  - numpy
  - python
  - data-science
  - arrays
summary: Print-friendly NumPy quick reference guide for fast lookup
---

# NumPy Cheat Sheet

`import numpy as np`

---

## ARRAY CREATION

| Code | Description |
|------|-------------|
| `np.array([1,2,3])` | From list |
| `np.zeros(5)` | Array of zeros |
| `np.zeros((3,4))` | 3×4 matrix of zeros |
| `np.ones(5)` | Array of ones |
| `np.ones((2,3))` | 2×3 matrix of ones |
| `np.arange(10)` | 0 to 9 |
| `np.arange(5,15)` | 5 to 14 |
| `np.arange(0,10,2)` | 0,2,4,6,8 (step=2) |
| `np.linspace(0,1,5)` | 5 values from 0 to 1 |
| `np.eye(3)` | 3×3 identity matrix |
| `np.full((2,3), 7)` | 2×3 filled with 7 |
| `np.random.rand(3,4)` | 3×4 random [0,1) |
| `np.random.randn(3,4)` | 3×4 normal dist |
| `np.random.randint(0,10,5)` | 5 random ints [0,10) |

## ARRAY PROPERTIES

| Code | Returns |
|------|---------|
| `arr.shape` | Dimensions (3,4) |
| `arr.size` | Total elements |
| `arr.ndim` | Number of dimensions |
| `arr.dtype` | Data type |
| `arr.itemsize` | Bytes per element |
| `len(arr)` | Length of 1st dimension |

## INDEXING & SLICING

| Code | Description |
|------|-------------|
| `arr[0]` | First element |
| `arr[-1]` | Last element |
| `arr[1:4]` | Elements 1,2,3 |
| `arr[::2]` | Every 2nd element |
| `arr[::-1]` | Reverse |
| `arr[1,2]` | Row 1, col 2 |
| `arr[0]` | First row |
| `arr[:,0]` | First column |
| `arr[0:2, 1:3]` | Submatrix |
| `arr[arr > 5]` | Boolean indexing |
| `arr[[0,2,4]]` | Fancy indexing |

## MATH OPERATIONS

| Code | Description |
|------|-------------|
| `a + b` | Element-wise add |
| `a - b` | Element-wise subtract |
| `a * b` | Element-wise multiply |
| `a / b` | Element-wise divide |
| `a ** 2` | Square |
| `a + 10` | Add scalar |
| `a * 2` | Multiply scalar |
| `np.sqrt(a)` | Square root |
| `np.exp(a)` | Exponential |
| `np.log(a)` | Natural log |
| `np.log10(a)` | Base-10 log |
| `np.sin(a)` | Sine |
| `np.cos(a)` | Cosine |
| `np.abs(a)` | Absolute value |
| `np.dot(a,b)` | Dot product |
| `a @ b` | Matrix multiply |

## AGGREGATION

| Code | Description |
|------|-------------|
| `arr.sum()` | Sum all |
| `arr.sum(axis=0)` | Sum columns |
| `arr.sum(axis=1)` | Sum rows |
| `arr.mean()` | Mean |
| `arr.std()` | Std deviation |
| `arr.var()` | Variance |
| `arr.min()` | Minimum |
| `arr.max()` | Maximum |
| `arr.argmin()` | Index of min |
| `arr.argmax()` | Index of max |
| `np.median(arr)` | Median |
| `np.percentile(arr,25)` | 25th percentile |

## RESHAPING

| Code | Description |
|------|-------------|
| `arr.reshape(3,4)` | Change to 3×4 |
| `arr.reshape(-1,3)` | Auto-calc rows |
| `arr.flatten()` | To 1D (copy) |
| `arr.ravel()` | To 1D (view) |
| `arr.T` | Transpose |
| `arr.transpose()` | Transpose |

## STACKING & SPLITTING

| Code | Description |
|------|-------------|
| `np.vstack([a,b])` | Vertical stack |
| `np.hstack([a,b])` | Horizontal stack |
| `np.concatenate([a,b])` | Concatenate |
| `np.split(arr, 3)` | Split into 3 |
| `np.append(arr, 6)` | Append element |
| `np.insert(arr, 2, 99)` | Insert at index |
| `np.delete(arr, 2)` | Delete at index |

## COMPARISON & LOGIC

| Code | Description |
|------|-------------|
| `a == b` | Element-wise equal |
| `a > b` | Element-wise greater |
| `a < 5` | Compare to scalar |
| `(a>2) & (a<5)` | AND condition |
| `(a<2) \| (a>5)` | OR condition |
| `~(a>3)` | NOT condition |
| `np.any(a>5)` | Any element > 5? |
| `np.all(a>0)` | All elements > 0? |
| `np.where(a>5)` | Indices where true |
| `np.where(a>5, 0, a)` | Replace >5 with 0 |

## SORTING & SEARCHING

| Code | Description |
|------|-------------|
| `np.sort(arr)` | Sort array |
| `arr.sort()` | Sort in-place |
| `np.argsort(arr)` | Indices to sort |
| `np.unique(arr)` | Unique values |
| `np.clip(arr, 2, 8)` | Clip values [2,8] |

## LINEAR ALGEBRA

| Code | Description |
|------|-------------|
| `np.dot(A,B)` | Matrix multiply |
| `A @ B` | Matrix multiply |
| `np.linalg.inv(A)` | Inverse |
| `np.linalg.det(A)` | Determinant |
| `np.linalg.eig(A)` | Eigenvalues |
| `np.linalg.solve(A,b)` | Solve Ax=b |

## STATISTICS

| Code | Description |
|------|-------------|
| `np.mean(arr)` | Mean |
| `np.median(arr)` | Median |
| `np.std(arr)` | Std deviation |
| `np.var(arr)` | Variance |
| `np.corrcoef(arr)` | Correlation |
| `np.percentile(arr,25)` | Percentile |

## RANDOM

| Code | Description |
|------|-------------|
| `np.random.seed(42)` | Set seed |
| `np.random.rand(3,4)` | Uniform [0,1) |
| `np.random.randn(3,4)` | Normal (μ=0,σ=1) |
| `np.random.randint(0,10,5)` | Random ints |
| `np.random.normal(5,2,100)` | Normal (μ=5,σ=2) |
| `np.random.uniform(0,10,5)` | Uniform [0,10) |
| `np.random.choice([1,2,3],3)` | Random choice |
| `np.random.shuffle(arr)` | Shuffle in-place |

## FILE I/O

| Code | Description |
|------|-------------|
| `np.save('f.npy', arr)` | Save binary |
| `np.load('f.npy')` | Load binary |
| `np.savetxt('f.txt', arr)` | Save text |
| `np.loadtxt('f.txt')` | Load text |
| `np.savez('f.npz', a=arr1, b=arr2)` | Save multiple |

## BROADCASTING RULES

1. Arrays with different dimensions: pad smaller shape with 1s on left
2. Arrays compatible if dimensions equal or one is 1
3. After broadcasting, each array behaves as if it had larger shape

Example:
```
arr (3,4) + scalar → (3,4) + (1,1) → (3,4)
arr (3,4) + row (4,) → (3,4) + (1,4) → (3,4)
arr (3,4) + col (3,1) → (3,4) + (3,1) → (3,4)
```

## COMMON PATTERNS

**Normalize:** `(data - data.mean()) / data.std()`

**One-hot encode:**
```python
labels = np.array([0,1,2,1,0])
one_hot = np.zeros((labels.size, labels.max()+1))
one_hot[np.arange(labels.size), labels] = 1
```

**Meshgrid:**
```python
x, y = np.arange(5), np.arange(3)
xx, yy = np.meshgrid(x, y)
```

**Distance matrix:**
```python
points = np.array([[0,0], [1,1], [2,2]])
dist = np.sqrt(((points[:,None] - points)**2).sum(axis=2))
```

## PERFORMANCE TIPS

✅ **DO:** Use vectorized operations
```python
result = arr * 2  # Fast
```

❌ **DON'T:** Use Python loops
```python
result = [x * 2 for x in arr]  # Slow
```

✅ **DO:** Use NumPy functions
```python
np.sum(arr)  # Fast
```

❌ **DON'T:** Use Python built-ins
```python
sum(arr)  # Slow
```

**Memory:** `.copy()` creates copy, slicing creates view

### From Lists

```python
# 1D array
arr = np.array([1, 2, 3, 4, 5])
# Output: array([1, 2, 3, 4, 5])

# 2D array (matrix)
matrix = np.array([[1, 2, 3], [4, 5, 6]])
# Output: array([[1, 2, 3],
#                [4, 5, 6]])

# 3D array
arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
```

### Built-in Array Creation Functions

```python
# Array of zeros
np.zeros(5)                    # array([0., 0., 0., 0., 0.])
np.zeros((3, 4))               # 3x4 matrix of zeros

# Array of ones
np.ones(5)                     # array([1., 1., 1., 1., 1.])
np.ones((2, 3))                # 2x3 matrix of ones

# Array with a range of values
np.arange(10)                  # array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
np.arange(5, 15)               # array([5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
np.arange(0, 10, 2)            # array([0, 2, 4, 6, 8]) - step of 2

# Evenly spaced values
np.linspace(0, 1, 5)           # array([0., 0.25, 0.5, 0.75, 1.])

# Identity matrix
np.eye(3)                      # 3x3 identity matrix

# Empty array (uninitialized)
np.empty((2, 3))               # 2x3 array with random values

# Array filled with a constant
np.full((2, 3), 7)             # 2x3 array filled with 7

# Random arrays
np.random.rand(3, 4)           # 3x4 array with random values [0, 1)
np.random.randn(3, 4)          # 3x4 array with normal distribution
np.random.randint(0, 10, (3, 4))  # 3x4 array with random integers [0, 10)
```

---

## 2. Array Properties

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

arr.shape        # (2, 3) - dimensions
arr.size         # 6 - total number of elements
arr.ndim         # 2 - number of dimensions
arr.dtype        # dtype('int64') - data type
arr.itemsize     # 8 - size of each element in bytes
arr.nbytes       # 48 - total bytes consumed
```

---

## 3. Array Indexing & Slicing

### Basic Indexing

```python
arr = np.array([10, 20, 30, 40, 50])

arr[0]           # 10 - first element
arr[-1]          # 50 - last element
arr[1:4]         # array([20, 30, 40]) - slice
arr[::2]         # array([10, 30, 50]) - every 2nd element
arr[::-1]        # array([50, 40, 30, 20, 10]) - reverse
```

### 2D Array Indexing

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

matrix[0, 0]     # 1 - element at row 0, col 0
matrix[1, 2]     # 6 - element at row 1, col 2
matrix[0]        # array([1, 2, 3]) - first row
matrix[:, 0]     # array([1, 4, 7]) - first column
matrix[0:2, 1:3] # array([[2, 3], [5, 6]]) - submatrix
```

### Boolean Indexing

```python
arr = np.array([1, 2, 3, 4, 5, 6])

arr[arr > 3]     # array([4, 5, 6]) - elements > 3
arr[arr % 2 == 0]  # array([2, 4, 6]) - even numbers
arr[(arr > 2) & (arr < 5)]  # array([3, 4]) - AND condition
```

### Fancy Indexing

```python
arr = np.array([10, 20, 30, 40, 50])

arr[[0, 2, 4]]   # array([10, 30, 50]) - specific indices
arr[[1, 1, 3]]   # array([20, 20, 40]) - can repeat indices
```

---

## 4. Array Operations

### Arithmetic Operations

```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# Element-wise operations
a + b            # array([11, 22, 33, 44])
a - b            # array([-9, -18, -27, -36])
a * b            # array([10, 40, 90, 160])
a / b            # array([0.1, 0.1, 0.1, 0.1])
a ** 2           # array([1, 4, 9, 16]) - square
np.sqrt(a)       # array([1., 1.41421356, 1.73205081, 2.])

# Scalar operations
a + 10           # array([11, 12, 13, 14])
a * 2            # array([2, 4, 6, 8])
```

### Universal Functions (ufuncs)

```python
arr = np.array([1, 2, 3, 4])

np.exp(arr)      # Exponential
np.log(arr)      # Natural logarithm
np.log10(arr)    # Base-10 logarithm
np.sin(arr)      # Sine
np.cos(arr)      # Cosine
np.abs(arr)      # Absolute value
```

### Aggregation Functions

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

arr.sum()        # 21 - sum of all elements
arr.min()        # 1 - minimum value
arr.max()        # 6 - maximum value
arr.mean()       # 3.5 - mean
arr.std()        # 1.707... - standard deviation
arr.var()        # 2.916... - variance

# Axis-specific operations
arr.sum(axis=0)  # array([5, 7, 9]) - sum along columns
arr.sum(axis=1)  # array([6, 15]) - sum along rows
arr.min(axis=0)  # array([1, 2, 3]) - min of each column
arr.max(axis=1)  # array([3, 6]) - max of each row
```

---

## 5. Array Manipulation

### Reshaping

```python
arr = np.arange(12)  # array([0, 1, 2, ..., 11])

arr.reshape(3, 4)    # 3x4 matrix
arr.reshape(2, 6)    # 2x6 matrix
arr.reshape(4, 3)    # 4x3 matrix
arr.reshape(-1, 3)   # Auto-calculate rows: 4x3

# Flatten
arr.reshape(3, 4).flatten()  # Back to 1D array
arr.reshape(3, 4).ravel()    # Also flattens (returns view)
```

### Transposing

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])

matrix.T         # Transpose: array([[1, 4],
                 #                   [2, 5],
                 #                   [3, 6]])

matrix.transpose()  # Same as .T
```

### Stacking & Splitting

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Vertical stack (rows)
np.vstack([a, b])    # array([[1, 2, 3],
                     #        [4, 5, 6]])

# Horizontal stack (columns)
np.hstack([a, b])    # array([1, 2, 3, 4, 5, 6])

# Concatenate
np.concatenate([a, b])  # array([1, 2, 3, 4, 5, 6])

# Split
arr = np.arange(9)
np.split(arr, 3)     # [array([0, 1, 2]), array([3, 4, 5]), array([6, 7, 8])]
```

### Adding/Removing Elements

```python
arr = np.array([1, 2, 3, 4, 5])

np.append(arr, 6)        # array([1, 2, 3, 4, 5, 6])
np.insert(arr, 2, 99)    # array([1, 2, 99, 3, 4, 5])
np.delete(arr, 2)        # array([1, 2, 4, 5])
```

---

## 6. Broadcasting

**Broadcasting** allows NumPy to perform operations on arrays of different shapes.

```python
# Scalar broadcasting
arr = np.array([1, 2, 3, 4])
arr + 10         # array([11, 12, 13, 14])

# 1D to 2D broadcasting
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
row = np.array([10, 20, 30])

matrix + row     # array([[11, 22, 33],
                 #        [14, 25, 36]])

# Column broadcasting
col = np.array([[10], [20]])
matrix + col     # array([[11, 12, 13],
                 #        [24, 25, 26]])
```

### Broadcasting Rules

1. If arrays have different dimensions, pad the smaller shape with ones on the left
2. Arrays are compatible if dimensions are equal or one of them is 1
3. After broadcasting, each array behaves as if it had the larger shape

---

## 7. Linear Algebra

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix multiplication
np.dot(A, B)     # array([[19, 22], [43, 50]])
A @ B            # Same as np.dot (Python 3.5+)

# Element-wise multiplication
A * B            # array([[5, 12], [21, 32]])

# Matrix inverse
np.linalg.inv(A)

# Determinant
np.linalg.det(A)  # -2.0

# Eigenvalues and eigenvectors
np.linalg.eig(A)

# Solve linear system Ax = b
b = np.array([1, 2])
x = np.linalg.solve(A, b)
```

---

## 8. Statistics

```python
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

np.mean(data)        # 5.5 - mean
np.median(data)      # 5.5 - median
np.std(data)         # 2.872... - standard deviation
np.var(data)         # 8.25 - variance
np.percentile(data, 25)  # 3.25 - 25th percentile
np.corrcoef(data)    # Correlation coefficient

# Min/Max with indices
np.argmin(data)      # 0 - index of minimum
np.argmax(data)      # 9 - index of maximum
```

---

## 9. Random Numbers

```python
# Set seed for reproducibility
np.random.seed(42)

# Random float [0, 1)
np.random.rand(3, 4)         # 3x4 array

# Random integers
np.random.randint(0, 10, 5)  # 5 random integers [0, 10)

# Normal distribution
np.random.randn(3, 4)        # Mean=0, Std=1
np.random.normal(5, 2, 100)  # Mean=5, Std=2, 100 samples

# Uniform distribution
np.random.uniform(0, 10, 5)  # 5 values between 0 and 10

# Random choice
np.random.choice([1, 2, 3, 4, 5], 3)  # Pick 3 random elements

# Shuffle
arr = np.array([1, 2, 3, 4, 5])
np.random.shuffle(arr)       # Shuffles in-place
```

---

## 10. Comparison & Logic

```python
a = np.array([1, 2, 3, 4, 5])
b = np.array([5, 4, 3, 2, 1])

# Element-wise comparison
a == b           # array([False, False, True, False, False])
a > b            # array([False, False, False, True, True])
a < 3            # array([True, True, False, False, False])

# Logical operations
np.logical_and(a > 2, a < 5)  # array([False, False, True, True, False])
np.logical_or(a < 2, a > 4)   # array([True, False, False, False, True])
np.logical_not(a > 3)         # array([True, True, True, False, False])

# Any/All
np.any(a > 3)    # True - at least one element > 3
np.all(a > 0)    # True - all elements > 0
```

---

## 11. Sorting & Searching

```python
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# Sort
np.sort(arr)         # array([1, 1, 2, 3, 4, 5, 6, 9])
arr.sort()           # Sorts in-place

# Argsort (indices that would sort the array)
np.argsort(arr)      # array([1, 3, 6, 0, 2, 4, 7, 5])

# Find unique values
np.unique(arr)       # array([1, 2, 3, 4, 5, 6, 9])

# Where (find indices)
np.where(arr > 4)    # (array([4, 5, 7]),)
```

---

## 12. File I/O

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# Save to binary file
np.save('array.npy', arr)

# Load from binary file
loaded = np.load('array.npy')

# Save to text file
np.savetxt('array.txt', arr)

# Load from text file
loaded = np.loadtxt('array.txt')

# Save/load multiple arrays
np.savez('arrays.npz', a=arr, b=arr*2)
data = np.load('arrays.npz')
data['a']  # Access saved arrays
```

---

## 13. Common Patterns & Tips

### Creating Coordinate Grids

```python
x = np.arange(0, 5)
y = np.arange(0, 3)
xx, yy = np.meshgrid(x, y)
# xx: array([[0, 1, 2, 3, 4],
#            [0, 1, 2, 3, 4],
#            [0, 1, 2, 3, 4]])
# yy: array([[0, 0, 0, 0, 0],
#            [1, 1, 1, 1, 1],
#            [2, 2, 2, 2, 2]])
```

### Clipping Values

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
np.clip(arr, 3, 7)  # array([3, 3, 3, 4, 5, 6, 7, 7, 7])
```

### Replacing Values

```python
arr = np.array([1, 2, 3, 4, 5])
arr[arr > 3] = 0    # array([1, 2, 3, 0, 0])

# Using where
np.where(arr > 3, 0, arr)  # Replace >3 with 0, else keep value
```

### Memory Views vs Copies

```python
arr = np.array([1, 2, 3, 4, 5])

# View (shares memory)
view = arr[1:4]
view[0] = 99        # Changes original arr too!

# Copy (independent)
copy = arr[1:4].copy()
copy[0] = 99        # Does NOT change original arr
```

---

## 14. Performance Tips

```python
# ✅ GOOD: Vectorized operations
arr = np.arange(1000000)
result = arr * 2

# ❌ BAD: Python loops
result = []
for x in arr:
    result.append(x * 2)

# ✅ GOOD: Use NumPy functions
np.sum(arr)

# ❌ BAD: Python sum
sum(arr)

# ✅ GOOD: Boolean indexing
arr[arr > 500000]

# ❌ BAD: List comprehension
[x for x in arr if x > 500000]
```

---

## 15. Common Use Cases

### Normalize Data

```python
data = np.array([1, 2, 3, 4, 5])
normalized = (data - data.mean()) / data.std()
```

### One-Hot Encoding

```python
labels = np.array([0, 1, 2, 1, 0])
one_hot = np.zeros((labels.size, labels.max() + 1))
one_hot[np.arange(labels.size), labels] = 1
# array([[1., 0., 0.],
#        [0., 1., 0.],
#        [0., 0., 1.],
#        [0., 1., 0.],
#        [1., 0., 0.]])
```

### Moving Average

```python
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
window = 3
moving_avg = np.convolve(data, np.ones(window)/window, mode='valid')
```

### Distance Matrix

```python
points = np.array([[0, 0], [1, 1], [2, 2]])
distances = np.sqrt(((points[:, None] - points) ** 2).sum(axis=2))
```

---

## Quick Reference Table

| Operation | Code | Result |
|-----------|------|--------|
| Create array | `np.array([1,2,3])` | `[1 2 3]` |
| Zeros | `np.zeros(5)` | `[0. 0. 0. 0. 0.]` |
| Ones | `np.ones(5)` | `[1. 1. 1. 1. 1.]` |
| Range | `np.arange(5)` | `[0 1 2 3 4]` |
| Shape | `arr.shape` | `(3, 4)` |
| Reshape | `arr.reshape(2, 3)` | 2×3 array |
| Transpose | `arr.T` | Transposed |
| Sum | `arr.sum()` | Total sum |
| Mean | `arr.mean()` | Average |
| Max | `arr.max()` | Maximum |
| Slice | `arr[1:4]` | Elements 1-3 |
| Boolean | `arr[arr > 5]` | Elements > 5 |
| Dot product | `np.dot(a, b)` | Matrix mult |

---

## Resources

- **Official Documentation**: [numpy.org/doc](https://numpy.org/doc/)
- **NumPy Tutorial**: [numpy.org/learn](https://numpy.org/learn/)
- **Visual Guide**: [NumPy Illustrated](https://betterprogramming.pub/numpy-illustrated-the-visual-guide-to-numpy-3b1d4976de1d)

---

## Summary

NumPy is essential for:
- ✅ Fast numerical computations
- ✅ Working with arrays and matrices
- ✅ Scientific computing and data analysis
- ✅ Machine learning preprocessing
- ✅ Image processing
- ✅ Signal processing

**Key takeaway**: Always use NumPy's vectorized operations instead of Python loops for better performance!
