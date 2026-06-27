---
title: "Data Handling with Dataset and DataLoader - A Friendly Guide"
category: Deep Learning
order: 4
tags:
  - deep-learning
  - pytorch
  - dataset
  - dataloader
  - batching
  - data-pipeline
  - beginners
  - friendly
summary: Learn how to load, batch, shuffle, and iterate over your own data in PyTorch using torch.utils.data.Dataset and DataLoader. Includes custom dataset examples and memory tricks.
---

# Data Handling with Dataset and DataLoader — A Friendly Guide

Before a neural network can learn, it needs clean, organised batches of data. In PyTorch, `Dataset` and `DataLoader` handle this for you.

---

## 1. The Big Idea

A neural network rarely trains on the entire dataset at once. Instead, it sees **mini-batches** — small chunks of data, shuffled, fed one at a time.

```
Full Dataset
  ├── Mini-batch 1 (32 samples)
  ├── Mini-batch 2 (32 samples)
  ├── Mini-batch 3 (32 samples)
  └── ...
```

> **Memory trick:** Training on the whole dataset at once is like trying to eat a whole cake. Mini-batches are like sensible slices.

---

## 2. Dataset and DataLoader

| Class | Job | What You Provide |
|-------|-----|------------------|
| **Dataset** | Knows how to fetch one sample | File paths, labels, transforms |
| **DataLoader** | Wraps the Dataset and creates batches | Batch size, shuffle, workers |

---

## 3. Built-in TensorDataset

If your data is already in tensors, use `TensorDataset`.

```python
import torch
from torch.utils.data import TensorDataset, DataLoader

# Features and labels
X = torch.randn(100, 3)      # 100 samples, 3 features each
y = torch.randint(0, 2, (100,))  # 100 binary labels

# Wrap in a Dataset
dataset = TensorDataset(X, y)

# Wrap in a DataLoader
loader = DataLoader(dataset, batch_size=8, shuffle=True)

# Iterate through batches
for batch_idx, (features, labels) in enumerate(loader):
    print(f"Batch {batch_idx}: features shape = {features.shape}, labels shape = {labels.shape}")
    if batch_idx == 2:
        break
```

### Output

```
Batch 0: features shape = torch.Size([8, 3]), labels shape = torch.Size([8])
Batch 1: features shape = torch.Size([8, 3]), labels shape = torch.Size([8])
Batch 2: features shape = torch.Size([8, 3]), labels shape = torch.Size([8])
```

---

## 4. Writing a Custom Dataset

Most real projects need a custom `Dataset`. You must implement three methods:

| Method | Purpose |
|--------|---------|
| `__init__` | Set up paths, labels, transforms |
| `__len__` | Return the total number of samples |
| `__getitem__` | Return one sample and its label by index |

```python
import torch
from torch.utils.data import Dataset

class HousePriceDataset(Dataset):
    def __init__(self, sizes, bedrooms, prices):
        # Store data as tensors
        self.X = torch.tensor([[s, b] for s, b in zip(sizes, bedrooms)], dtype=torch.float32)
        self.y = torch.tensor(prices, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Sample data
sizes = [1200, 1500, 800, 2000, 950]
bedrooms = [3, 4, 2, 5, 2]
prices = [250000, 320000, 180000, 410000, 210000]

dataset = HousePriceDataset(sizes, bedrooms, prices)

print(f"Dataset size: {len(dataset)}")
print(f"Sample 0: {dataset[0]}")
```

---

## 5. Loading Data from CSV

Real datasets usually live in CSV files. Here is how to load one.

```python
import pandas as pd
import torch
from torch.utils.data import Dataset

class CSVDataset(Dataset):
    def __init__(self, csv_path, feature_columns, target_column):
        # Load the CSV
        self.df = pd.read_csv(csv_path)

        # Extract features and target
        self.X = torch.tensor(self.df[feature_columns].values, dtype=torch.float32)
        self.y = torch.tensor(self.df[target_column].values, dtype=torch.float32)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Use it
dataset = CSVDataset(
    csv_path="houses.csv",
    feature_columns=["size", "bedrooms"],
    target_column="price"
)
```

---

## 6. Transforms in a Dataset

A transform is a function that modifies the data before returning it. Common transforms include:

- Normalising values
- Converting to tensors
- Augmenting images

```python
import torch
from torch.utils.data import Dataset

class NormalisedDataset(Dataset):
    def __init__(self, X, y, mean=None, std=None):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

        # Compute mean and std if not provided
        if mean is None:
            mean = self.X.mean(dim=0)
        if std is None:
            std = self.X.std(dim=0)

        self.mean = mean
        self.std = std

        # Apply normalisation
        self.X = (self.X - self.mean) / self.std

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Example
X = [[1200, 3], [1500, 4], [800, 2], [2000, 5]]
y = [250, 320, 180, 410]

dataset = NormalisedDataset(X, y)
print(dataset[0])
```

---

## 7. DataLoader Options

The `DataLoader` has many useful options.

```python
from torch.utils.data import DataLoader

loader = DataLoader(
    dataset,
    batch_size=32,       # samples per batch
    shuffle=True,        # randomise order each epoch
    num_workers=4,       # load data in parallel processes
    drop_last=True,      # drop last incomplete batch
    pin_memory=True      # speed up GPU transfer
)
```

| Option | What It Does | When to Use |
|--------|--------------|-------------|
| `batch_size` | Number of samples per batch | Larger = faster training, more memory |
| `shuffle` | Randomise order each epoch | Use for training, not for validation/testing |
| `num_workers` | Parallel loading | Use when data loading is slow |
| `drop_last` | Drop incomplete final batch | When batch size must be exact |
| `pin_memory` | Faster CPU → GPU transfer | Use with GPU training |

---

## 8. Train / Validation / Test Split

Never evaluate on training data. Split into three parts:

```
Dataset
  ├── Training set (70%) — used to learn weights
  ├── Validation set (15%) — used to tune hyperparameters
  └── Test set (15%) — used once at the end
```

```python
import torch
from torch.utils.data import random_split, DataLoader

# Create a dataset
full_dataset = TensorDataset(torch.randn(1000, 3), torch.randint(0, 2, (1000,)))

# Split sizes
train_size = int(0.7 * len(full_dataset))
val_size = int(0.15 * len(full_dataset))
test_size = len(full_dataset) - train_size - val_size

train_set, val_set, test_set = random_split(full_dataset, [train_size, val_size, test_size])

# Create loaders
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
val_loader = DataLoader(val_set, batch_size=32, shuffle=False)
test_loader = DataLoader(test_set, batch_size=32, shuffle=False)

print(f"Train: {len(train_set)}, Val: {len(val_set)}, Test: {len(test_set)}")
```

---

## 9. A Complete Training Loop with DataLoader

```python
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

# Fake data
X = torch.randn(1000, 3)
y = torch.randint(0, 2, (1000, 1), dtype=torch.float32)

# Dataset and loader
dataset = TensorDataset(X, y)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Model
model = nn.Sequential(
    nn.Linear(3, 10),
    nn.ReLU(),
    nn.Linear(10, 1),
    nn.Sigmoid()
)

# Loss and optimizer
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training loop
for epoch in range(5):
    total_loss = 0
    for batch_x, batch_y in train_loader:
        # Forward pass
        predictions = model(batch_x)
        loss = criterion(predictions, batch_y)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch + 1}, Average Loss: {total_loss / len(train_loader):.4f}")
```

---

## 10. Image Dataset Example

Here is a custom dataset for images:

```python
import os
from PIL import Image
import torch
from torch.utils.data import Dataset

class ImageDataset(Dataset):
    def __init__(self, image_dir, transform=None):
        self.image_dir = image_dir
        self.image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg'))]
        self.transform = transform

        # Labels from filenames: cat_01.jpg → label "cat"
        self.labels = [f.split('_')[0] for f in self.image_files]
        self.label_map = {label: idx for idx, label in enumerate(set(self.labels))}

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        filename = self.image_files[idx]
        image_path = os.path.join(self.image_dir, filename)
        image = Image.open(image_path).convert("RGB")

        label = self.label_map[self.labels[idx]]
        label = torch.tensor(label, dtype=torch.long)

        if self.transform:
            image = self.transform(image)

        return image, label
```

---

## 11. Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|----------------|-----|
| Forgetting to set `shuffle=True` for training | Model sees the same order every epoch | Always shuffle training data |
| Shuffling validation/test data | Order does not matter for evaluation, but can be confusing | Set `shuffle=False` for val/test |
| Forgetting to call `optimizer.zero_grad()` | Gradients accumulate | Clear gradients each batch |
| Not using `num_workers` on large datasets | Data loading becomes the bottleneck | Use 2–4 workers |
| Returning wrong data types | PyTorch expects tensors | Convert features and labels to tensors |
| Data leakage between splits | Samples overlap between train and test | Split before any preprocessing |

---

## 12. Quick Review

| Class | Job | Must Implement |
|-------|-----|---------------|
| **Dataset** | Fetch one sample | `__init__`, `__len__`, `__getitem__` |
| **DataLoader** | Create batches | `batch_size`, `shuffle`, `num_workers` |
| **TensorDataset** | Wrap tensors | Nothing — just pass tensors |
| **random_split** | Split dataset into parts | Dataset and split sizes |

---

## 13. Try It Yourself

```python
import torch
from torch.utils.data import Dataset, DataLoader

# 1. Create a custom dataset that returns numbers and their squares
class SquareDataset(Dataset):
    def __init__(self, n):
        self.numbers = torch.arange(n, dtype=torch.float32)
        self.squares = self.numbers ** 2

    def __len__(self):
        return len(self.numbers)

    def __getitem__(self, idx):
        return self.numbers[idx], self.squares[idx]

# 2. Create DataLoader
 dataset = SquareDataset(100)
loader = DataLoader(dataset, batch_size=10, shuffle=True)

# 3. Print one batch
for x, y in loader:
    print(f"Inputs: {x[:5]}")
    print(f"Squares: {y[:5]}")
    break
```

---

## Summary

- `Dataset` defines how to access one sample.
- `DataLoader` creates batches and can shuffle, parallel-load, and drop partial batches.
- Always split data into train/validation/test sets.
- Use `TensorDataset` for simple tensor data and write custom `Dataset` classes for real files.
- Transforms are applied inside `__getitem__` to prepare data for the model.
- Data handling is the foundation of every training pipeline — get it right early.
