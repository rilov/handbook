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
  - spam-detection
  - beginners
  - friendly
summary: Learn how to load, batch, shuffle, and iterate over spam-detection data in PyTorch using torch.utils.data.Dataset and DataLoader. Uses the same email example throughout.
---

# Data Handling with Dataset and DataLoader — A Friendly Guide

Before a neural network can learn, it needs clean, organised batches of data. In PyTorch, `Dataset` and `DataLoader` handle this for you. We will use the same spam-detection example throughout.

---

## 1. Why not feed the whole dataset at once?

A neural network rarely trains on the entire dataset at once. Instead, it sees **mini-batches** — small chunks of data, shuffled, fed one at a time.

```
Full spam dataset
  ├── Mini-batch 1 (32 emails)
  ├── Mini-batch 2 (32 emails)
  ├── Mini-batch 3 (32 emails)
  └── ...
```

> **Memory trick:** Training on the whole dataset at once is like trying to eat a whole cake. Mini-batches are like sensible slices.

There are three good reasons for mini-batches:

1. **Memory:** A large dataset may not fit in RAM or GPU memory.
2. **Speed:** Matrix operations are faster when done on many examples at once.
3. **Learning:** Seeing many small random samples helps the model generalise better.

---

## 2. Dataset and DataLoader

| Class | Job | What you provide |
|-------|-----|------------------|
| **Dataset** | Knows how to fetch one email and its label | Features, labels, transforms |
| **DataLoader** | Wraps the Dataset and creates batches | Batch size, shuffle, workers |

> **Memory trick:** Dataset = one apple. DataLoader = bag of apples.

---

## 3. A simple spam dataset with TensorDataset

If your email features and labels are already in tensors, use `TensorDataset`.

```python
import torch
from torch.utils.data import TensorDataset, DataLoader

# Features: 100 emails, 5 features each
emails = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],   # spammy
    [0.0, 0.0, 1.0, 0.02, 82.0],   # normal
    [5.0, 4.0, 0.0, 0.45, 31.0],   # spammy
    [1.0, 0.0, 1.0, 0.05, 120.0],  # normal
    # ... many more emails
])

# Labels: 1 = spam, 0 = not spam
labels = torch.tensor([
    [1.0],
    [0.0],
    [1.0],
    [0.0]
])

# Wrap in a Dataset
dataset = TensorDataset(emails, labels)

# Wrap in a DataLoader
loader = DataLoader(dataset, batch_size=2, shuffle=True)

# Iterate through batches
for batch_emails, batch_labels in loader:
    print("Batch emails shape:", batch_emails.shape)
    print("Batch labels shape:", batch_labels.shape)
    break
```

Output:

```
Batch emails shape: torch.Size([2, 5])
Batch labels shape: torch.Size([2, 1])
```

Each batch contains 2 emails, each with 5 features, and 2 matching labels.

---

## 4. Writing a custom Dataset for spam emails

Most real projects need a custom `Dataset`. You must implement three methods:

| Method | Purpose |
|--------|---------|
| `__init__` | Set up features, labels, transforms |
| `__len__` | Return the total number of emails |
| `__getitem__` | Return one email and its label by index |

```python
import torch
from torch.utils.data import Dataset

class SpamDataset(Dataset):
    def __init__(self, emails, labels):
        # Store data as tensors
        self.emails = torch.tensor(emails, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.emails)

    def __getitem__(self, idx):
        return self.emails[idx], self.labels[idx]

# Example data
emails = [
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0],
    [5.0, 4.0, 0.0, 0.45, 31.0],
    [1.0, 0.0, 1.0, 0.05, 120.0]
]
labels = [1.0, 0.0, 1.0, 0.0]

dataset = SpamDataset(emails, labels)
print("Dataset size:", len(dataset))
print("Email 0:", dataset[0])
```

Output:

```
Dataset size: 4
Email 0: (tensor([3.0, 1.0, 0.0, 0.20, 47.0]), tensor(1.0))
```

---

## 5. Loading spam data from a CSV file

Real datasets usually live in CSV files. Here is how to load one.

```python
import pandas as pd
import torch
from torch.utils.data import Dataset

class SpamCSVDataset(Dataset):
    def __init__(self, csv_path):
        # Load the CSV
        self.df = pd.read_csv(csv_path)

        # Extract features and target
        feature_columns = [
            'suspicious_words',
            'links',
            'known_sender',
            'capitals',
            'length'
        ]
        self.emails = torch.tensor(
            self.df[feature_columns].values,
            dtype=torch.float32
        )
        self.labels = torch.tensor(
            self.df['is_spam'].values,
            dtype=torch.float32
        )

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        return self.emails[idx], self.labels[idx]

# Use it
dataset = SpamCSVDataset("emails.csv")
```

Example `emails.csv`:

```csv
suspicious_words,links,known_sender,capitals,length,is_spam
5,4,0,0.40,31,1
0,0,1,0.02,85,0
3,2,0,0.25,42,1
0,1,1,0.01,110,0
```

---

## 6. Transforms: normalising email features

A transform is a function that modifies the data before returning it. For spam emails, we often normalise the features so that no single feature dominates.

For example, message length might be 120 while capital percentage is 0.20. If we do not normalise, the length value could overwhelm the other features.

```python
import torch
from torch.utils.data import Dataset

class NormalisedSpamDataset(Dataset):
    def __init__(self, emails, labels):
        emails = torch.tensor(emails, dtype=torch.float32)
        labels = torch.tensor(labels, dtype=torch.float32)

        # Compute mean and standard deviation for each feature
        self.mean = emails.mean(dim=0)
        self.std = emails.std(dim=0)

        # Normalise: (value - mean) / std
        self.emails = (emails - self.mean) / self.std
        self.labels = labels

    def __len__(self):
        return len(self.emails)

    def __getitem__(self, idx):
        return self.emails[idx], self.labels[idx]

emails = [
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0],
    [5.0, 4.0, 0.0, 0.45, 31.0],
    [1.0, 0.0, 1.0, 0.05, 120.0]
]
labels = [1.0, 0.0, 1.0, 0.0]

dataset = NormalisedSpamDataset(emails, labels)
print(dataset[0])
```

> **Memory trick:** Normalisation is like giving every feature the same size ruler. Without it, the model listens mostly to the loudest feature.

---

## 7. DataLoader options

The `DataLoader` has many useful options.

```python
from torch.utils.data import DataLoader

loader = DataLoader(
    dataset,
    batch_size=32,       # emails per batch
    shuffle=True,        # randomise order each epoch
    num_workers=4,       # load data in parallel processes
    drop_last=True,      # drop last incomplete batch
    pin_memory=True      # speed up GPU transfer
)
```

| Option | What it does | When to use |
|--------|--------------|-------------|
| `batch_size` | Number of emails per batch | Larger = faster training, more memory |
| `shuffle` | Randomise order each epoch | Use for training, not for validation/testing |
| `num_workers` | Parallel loading | Use when data loading is slow |
| `drop_last` | Drop incomplete final batch | When batch size must be exact |
| `pin_memory` | Faster CPU → GPU transfer | Use with GPU training |

---

## 8. Train / validation / test split

Never evaluate on training data. Split into three parts:

```
Spam dataset
  ├── Training set (70%) — used to learn weights
  ├── Validation set (15%) — used to tune hyperparameters
  └── Test set (15%) — used once at the end
```

```python
import torch
from torch.utils.data import random_split, DataLoader

# Full dataset
emails = torch.randn(1000, 5)  # 1000 emails, 5 features
labels = torch.randint(0, 2, (1000, 1), dtype=torch.float32)
full_dataset = torch.utils.data.TensorDataset(emails, labels)

# Split sizes
train_size = int(0.7 * len(full_dataset))
val_size = int(0.15 * len(full_dataset))
test_size = len(full_dataset) - train_size - val_size

train_set, val_set, test_set = random_split(
    full_dataset,
    [train_size, val_size, test_size]
)

# Create loaders
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
val_loader = DataLoader(val_set, batch_size=32, shuffle=False)
test_loader = DataLoader(test_set, batch_size=32, shuffle=False)

print(f"Train: {len(train_set)}, Val: {len(val_set)}, Test: {len(test_set)}")
```

> **Memory trick:** Training set is the textbook. Validation set is the practice exam. Test set is the final exam.

---

## 9. A complete training loop with spam data

Here is how a full training loop looks with `Dataset` and `DataLoader`.

```python
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

# Fake spam data: 1000 emails, 5 features each
emails = torch.randn(1000, 5)
labels = torch.randint(0, 2, (1000, 1), dtype=torch.float32)

# Dataset and loader
dataset = TensorDataset(emails, labels)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Model: 5 features -> 4 hidden -> 1 output
model = nn.Sequential(
    nn.Linear(5, 4),
    nn.ReLU(),
    nn.Linear(4, 1),
    nn.Sigmoid()
)

# Loss and optimizer
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training loop
for epoch in range(5):
    total_loss = 0
    for batch_emails, batch_labels in train_loader:
        # Forward pass
        predictions = model(batch_emails)
        loss = criterion(predictions, batch_labels)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch + 1}, Average Loss: {total_loss / len(train_loader):.4f}")
```

The loop runs through the entire dataset five times. Each time, the emails are shuffled and split into batches of 32.

---

## 10. Common mistakes

| Mistake | Why it happens | Fix |
|---------|----------------|-----|
| Forgetting to set `shuffle=True` for training | Model sees the same order every epoch | Always shuffle training data |
| Shuffling validation/test data | Order does not matter for evaluation, but can be confusing | Set `shuffle=False` for val/test |
| Forgetting to call `optimizer.zero_grad()` | Gradients accumulate | Clear gradients each batch |
| Not using `num_workers` on large datasets | Data loading becomes the bottleneck | Use 2–4 workers |
| Returning wrong data types | PyTorch expects tensors | Convert features and labels to tensors |
| Data leakage between splits | Emails overlap between train and test | Split before any preprocessing |
| Not normalising features | One feature dominates the others | Normalise to zero mean and unit variance |

---

## 11. Quick review

| Class | Job | Must implement |
|-------|-----|---------------|
| **Dataset** | Fetch one email and its label | `__init__`, `__len__`, `__getitem__` |
| **DataLoader** | Create batches | `batch_size`, `shuffle`, `num_workers` |
| **TensorDataset** | Wrap tensors | Nothing — just pass tensors |
| **random_split** | Split dataset into parts | Dataset and split sizes |

---

## 12. Try it yourself

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

# 4. Try with a spam-style dataset
spam_emails = [
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0],
    [5.0, 4.0, 0.0, 0.45, 31.0]
]
spam_labels = [1.0, 0.0, 1.0]

spam_dataset = SpamDataset(spam_emails, spam_labels)
spam_loader = DataLoader(spam_dataset, batch_size=2, shuffle=True)

for batch_x, batch_y in spam_loader:
    print(batch_x.shape, batch_y.shape)
    break
```

---

## Summary

- `Dataset` defines how to access one email and its label.
- `DataLoader` creates batches and can shuffle, parallel-load, and drop partial batches.
- Always split data into train/validation/test sets.
- Use `TensorDataset` for simple tensor data and write custom `Dataset` classes for real files.
- Transforms are applied inside `__getitem__` to prepare data for the model.
- Normalisation helps prevent one feature from dominating the others.
- Data handling is the foundation of every training pipeline — get it right early.
