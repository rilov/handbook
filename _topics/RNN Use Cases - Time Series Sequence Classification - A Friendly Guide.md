---
title: "Part 16: RNN Use Cases - Time Series, Sequence Classification and Labelling - A Friendly Guide"
category: Deep Learning
order: 16
tags:
  - deep-learning
  - rnn
  - lstm
  - time-series
  - sequence-classification
  - sequence-labelling
  - pytorch
  - beginners
  - friendly
summary: A beginner-friendly guide to practical RNN applications. Learn how to use LSTM for time series forecasting, sequence classification, and sequence labelling with clear step-by-step Python examples.
---

# Part 16: RNN Use Cases — Time Series, Sequence Classification, and Labelling — A Friendly Guide

In Parts 14 and 15, you learned how RNNs and LSTMs work.

Now let us use them on real problems.

There are three main ways to use an RNN:

| Use | What you give it | What you get back |
|-----|-----------------|------------------|
| **Time series forecasting** | A sequence of past values | One predicted future value |
| **Sequence classification** | A whole sequence | One label for the whole thing |
| **Sequence labelling** | A whole sequence | One label **per step** |

Each one is slightly different in how you feed data in and how you read the output.

---

## 1. Time series forecasting — predicting what comes next

**The task:** Given past values (numbers over time), predict the next value.

**Examples:**
- Given last 7 days of temperature → predict tomorrow
- Given last 30 days of sales → predict next month's sales
- Given last 10 seconds of a patient's heart rate → predict the next value

### How it works

You feed the whole sequence in. The RNN reads it step by step and builds up a memory. At the end, you take the **final hidden state** and pass it through a linear layer to get your prediction.

```
x₁ → x₂ → x₃ → x₄ → x₅ → [final memory] → [Linear] → predicted x₆
```

### Step by step example — weekly sales forecasting

```python
import torch
import torch.nn as nn
import numpy as np

torch.manual_seed(0)

# Fake weekly sales data (units sold)
sales = [120, 135, 128, 142, 150, 145, 160, 155, 170, 165,
         180, 175, 190, 185, 200, 195, 210, 205, 220, 215]

# Step 1 — Create sequences
# Input: 4 weeks. Target: week 5.
SEQ_LEN = 4
X, y = [], []
for i in range(len(sales) - SEQ_LEN):
    X.append(sales[i : i + SEQ_LEN])
    y.append(sales[i + SEQ_LEN])

# Step 2 — Convert to tensors
# Normalise: divide by 200 so numbers are between 0 and 1
scale = 200.0
X = torch.tensor(X, dtype=torch.float32).unsqueeze(-1) / scale  # (N, 4, 1)
y = torch.tensor(y, dtype=torch.float32).unsqueeze(-1) / scale  # (N, 1)

print(f"Training samples: {len(X)}")
print(f"X shape: {X.shape}  y shape: {y.shape}")

# Step 3 — Build the model
class SalesForecaster(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm   = nn.LSTM(input_size=1, hidden_size=32, batch_first=True)
        self.linear = nn.Linear(32, 1)

    def forward(self, x):
        out, (h, c) = self.lstm(x)
        return self.linear(h.squeeze(0))  # use final hidden state

model     = SalesForecaster()
loss_fn   = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

# Step 4 — Train
for epoch in range(500):
    pred = model(X)
    loss = loss_fn(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 100 == 0:
        print(f"Epoch {epoch}  loss: {loss.item():.6f}")

# Step 5 — Predict next week
model.eval()
with torch.no_grad():
    last_4 = torch.tensor([[[205.0], [220.0], [215.0], [225.0]]]) / scale
    predicted = model(last_4).item() * scale
    print(f"\nGiven sales: 205, 220, 215, 225")
    print(f"Predicted next week: {predicted:.0f} units")
```

### Key decisions for time series

| Decision | Recommendation |
|----------|---------------|
| Sequence length | Start with 4–10 steps. Try longer if the model is bad. |
| Normalise data | Always divide by a scale factor. Values between 0 and 1 train much better. |
| Use LSTM not RNN | LSTM remembers longer patterns — almost always better. |
| Loss function | MSELoss for continuous values (temperature, sales, prices) |

---

## 2. Sequence classification — one label for the whole sequence

**The task:** Read a whole sequence and output **one single label**.

**Examples:**
- Read all words in an email → spam or not spam
- Read all words in a review → positive or negative
- Read all values in a sensor recording → fault or no fault
- Read all words in a support ticket → which department to route to

### How it works

Same as forecasting — the RNN reads the whole sequence. You take the **final hidden state** and classify it.

```
word₁ → word₂ → word₃ → ... → wordₙ → [final memory] → [Linear + Sigmoid] → label
```

### Step by step example — email routing

```python
import torch
import torch.nn as nn

# Simple vocabulary
vocab = {
    "invoice": 0, "payment": 1, "billing": 2, "charge": 3,
    "login": 4, "password": 5, "account": 6, "access": 7,
    "broken": 8, "error": 9, "not": 10, "working": 11,
    "the": 12, "my": 13, "is": 14, "i": 15, "cannot": 16,
    "<pad>": 17
}
VOCAB_SIZE = len(vocab)

# Department labels: 0=billing, 1=account, 2=technical
tickets = [
    (["my", "invoice", "is", "wrong"],                   0),  # billing
    (["i", "cannot", "access", "my", "account"],         1),  # account
    (["the", "login", "is", "not", "working"],           2),  # technical
    (["billing", "charge", "error"],                     0),  # billing
    (["password", "account", "access"],                  1),  # account
    (["broken", "error", "not", "working"],              2),  # technical
]

def encode(words):
    return torch.tensor([[vocab[w] for w in words]])

X = [encode(t[0]) for t in tickets]
y = torch.tensor([t[1] for t in tickets])

# Model
class TicketRouter(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(VOCAB_SIZE, 16)
        self.lstm      = nn.LSTM(input_size=16, hidden_size=32, batch_first=True)
        self.linear    = nn.Linear(32, 3)   # 3 departments

    def forward(self, x):
        emb = self.embedding(x)
        out, (h, c) = self.lstm(emb)
        return self.linear(h.squeeze(0))

model     = TicketRouter()
loss_fn   = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Train
for epoch in range(400):
    total_loss = 0
    for xi, yi in zip(X, y):
        pred = model(xi)
        loss = loss_fn(pred, yi.unsqueeze(0))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    if epoch % 100 == 0:
        print(f"Epoch {epoch}  loss: {total_loss/len(X):.4f}")

# Test
departments = ["Billing", "Account", "Technical"]
model.eval()
test_tickets = [
    ["my", "billing", "charge", "is", "wrong"],
    ["i", "cannot", "login", "account"],
]
with torch.no_grad():
    for words in test_tickets:
        # Filter to known words only
        known = [w for w in words if w in vocab]
        x = encode(known)
        logits = model(x)
        pred = logits.argmax().item()
        print(f"'{' '.join(words)}' → Route to: {departments[pred]}")
```

---

## 3. Sequence labelling — one label per step

**The task:** Read a sequence and output **one label at every position**.

**Examples:**
- Read each word in a sentence → label each word as Noun, Verb, Adjective, etc. (POS tagging)
- Read each word in a sentence → label each word as Person, Location, Organisation, or Other (Named Entity Recognition)
- Read each character in a DNA sequence → label each position as coding or non-coding
- Read each frame in a video → label each frame as "action" or "no action"

### How it works

For labelling, you do not take just the final hidden state. You take the **output at every step**.

```
word₁ → [LSTM] → output₁ → [Linear] → label₁
word₂ → [LSTM] → output₂ → [Linear] → label₂
word₃ → [LSTM] → output₃ → [Linear] → label₃
```

In PyTorch, `nn.LSTM` returns `output` — the hidden state at every step. Use this for sequence labelling.

### Step by step example — part-of-speech tagging

```python
import torch
import torch.nn as nn

# Vocabulary and tags
word_to_idx = {
    "the": 0, "cat": 1, "sat": 2, "on": 3, "mat": 4,
    "dog": 5, "ran": 6, "fast": 7, "a": 8, "big": 9,
    "<pad>": 10
}
tag_to_idx = {"DET": 0, "NOUN": 1, "VERB": 2, "PREP": 3, "ADJ": 4}
IDX_TO_TAG = {v: k for k, v in tag_to_idx.items()}

# Training data: (sentence, tags)  — one tag per word
training_data = [
    (["the", "cat", "sat", "on", "mat"],    ["DET", "NOUN", "VERB", "PREP", "NOUN"]),
    (["a", "dog", "ran", "fast"],           ["DET", "NOUN", "VERB", "ADJ"]),
    (["the", "big", "dog", "ran"],          ["DET", "ADJ", "NOUN", "VERB"]),
    (["a", "cat", "sat", "on", "mat"],      ["DET", "NOUN", "VERB", "PREP", "NOUN"]),
]

def encode_sentence(words):
    return torch.tensor([word_to_idx[w] for w in words])

def encode_tags(tags):
    return torch.tensor([tag_to_idx[t] for t in tags])

# Model
class POSTagger(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(len(word_to_idx), 16)
        self.lstm      = nn.LSTM(input_size=16, hidden_size=32, batch_first=True)
        self.linear    = nn.Linear(32, len(tag_to_idx))   # one score per tag

    def forward(self, x):
        emb = self.embedding(x.unsqueeze(0))  # (1, seq_len, 16)
        output, _ = self.lstm(emb)            # (1, seq_len, 32)
        return self.linear(output.squeeze(0)) # (seq_len, num_tags)

model     = POSTagger()
loss_fn   = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Train
for epoch in range(300):
    total_loss = 0
    for words, tags in training_data:
        x = encode_sentence(words)
        y = encode_tags(tags)
        pred = model(x)          # shape: (seq_len, num_tags)
        loss = loss_fn(pred, y)  # compare each position
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    if epoch % 100 == 0:
        print(f"Epoch {epoch}  loss: {total_loss/len(training_data):.4f}")

# Test — tag a new sentence
model.eval()
test_sentence = ["the", "big", "cat", "sat"]
with torch.no_grad():
    x = encode_sentence(test_sentence)
    pred = model(x)
    predicted_tags = pred.argmax(dim=1).tolist()
    print("\nWord-by-word tagging:")
    for word, tag_idx in zip(test_sentence, predicted_tags):
        print(f"  {word:10s} → {IDX_TO_TAG[tag_idx]}")
```

Output:
```
Word-by-word tagging:
  the        → DET
  big        → ADJ
  cat        → NOUN
  sat        → VERB
```

---

## 4. Which output to use — a clear guide

This is the most common source of confusion. Here is a simple rule:

```python
output, (h_n, c_n) = lstm(x)
```

| Task | Which output to use | Why |
|------|-------------------|-----|
| Time series forecasting | `h_n` — the final hidden state | You want one number at the end |
| Sequence classification | `h_n` — the final hidden state | You want one label at the end |
| Sequence labelling | `output` — hidden state at every step | You want one label at every position |

```python
# For forecasting or classification:
out, (h_n, c_n) = lstm(x)
result = linear(h_n.squeeze(0))    # use h_n → shape (batch, hidden)

# For labelling:
out, (h_n, c_n) = lstm(x)
result = linear(out)               # use output → shape (batch, seq_len, hidden)
```

---

## 5. Choosing the right sequence model — summary

| Problem | Model | Output used |
|---------|-------|------------|
| Predict next value | LSTM | Final hidden state → `h_n` |
| Classify whole sequence | LSTM or Bidirectional LSTM | Final hidden state → `h_n` |
| Label each step in sequence | LSTM or Bidirectional LSTM | All outputs → `output` |
| Very long sequences (1000+ steps) | Transformer (covered later) | Attention mechanism |

---

## 6. Common patterns in real projects

### Pattern 1 — Normalise your time series data

```python
# Always normalise time series before feeding to LSTM
mean = X.mean()
std  = X.std()
X_normalised = (X - mean) / std   # values centred around 0

# After predicting, scale back
prediction_real = prediction_normalised * std + mean
```

### Pattern 2 — Use a DataLoader for sequences

```python
from torch.utils.data import Dataset, DataLoader

class SequenceDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

dataset = SequenceDataset(X, y)
loader  = DataLoader(dataset, batch_size=16, shuffle=True)

for X_batch, y_batch in loader:
    pred = model(X_batch)
    # ...
```

### Pattern 3 — Add dropout to prevent overfitting

```python
lstm = nn.LSTM(
    input_size=1,
    hidden_size=64,
    num_layers=2,
    dropout=0.3,        # 30% dropout between layers
    batch_first=True
)
```

---

## Summary

Three main RNN use cases, each slightly different:

```
Time series forecasting:
  past values → LSTM → final hidden state → Linear → next value

Sequence classification:
  all words → LSTM → final hidden state → Linear → one label

Sequence labelling:
  all words → LSTM → output at every step → Linear → label per word
```

- Always **normalise** time series data before training.
- Use **`h_n`** (final hidden state) for forecasting and classification.
- Use **`output`** (all hidden states) for sequence labelling.
- For tasks where context from both directions matters, use **Bidirectional LSTM**.
- Stack 2 LSTM layers and add **dropout** for better generalisation on real datasets.
