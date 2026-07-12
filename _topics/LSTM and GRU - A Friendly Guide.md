---
title: "Part 15: LSTM and GRU - Solving the Memory Problem - A Friendly Guide"
category: Deep Learning
order: 15
tags:
  - deep-learning
  - lstm
  - gru
  - rnn
  - vanishing-gradient
  - sequential-data
  - pytorch
  - beginners
  - friendly
summary: A beginner-friendly guide to LSTM and GRU — the improved versions of RNN that can remember things from much longer ago. Learn why basic RNNs forget, how LSTM gates solve this, and how to use both in PyTorch.
---

# Part 15: LSTM and GRU — Solving the Memory Problem — A Friendly Guide

In Part 14, we learned that an RNN reads data step by step and keeps a memory (the hidden state).

But we also saw one big problem: **RNNs forget things from long ago**.

Imagine you are reading a detective story. The important clue was mentioned on page 3. By page 50, you still remember it — because your brain knows it was important and held onto it.

A basic RNN cannot do this. Every step, the memory is overwritten a little. After many steps, early information is almost gone.

**LSTM** (Long Short-Term Memory) and **GRU** (Gated Recurrent Unit) fix this. They give the network a way to **choose what to remember and what to forget**.

---

## 1. The problem — vanishing gradients

When we train an RNN using backpropagation through time (BPTT), we go backwards through the chain:

```
x₁ → [RNN] → h₁ → [RNN] → h₂ → [RNN] → h₃ → ... → h₅₀ → output → loss
     ←─────────────────────────────────────────────────────────────── gradients flow back
```

At each step going backwards, the gradient is multiplied by the same weights. If those weights are slightly less than 1 (which they often are), the gradient shrinks at every step:

```
0.9 × 0.9 × 0.9 × 0.9 × 0.9 × ... (50 times) = almost zero
```

By the time the gradient reaches step 1, it is so small the weights barely update. The network cannot learn from early parts of the sequence.

This is the **vanishing gradient problem**.

> **Simple analogy:** Imagine passing a whisper along a line of 50 people. Each person hears it slightly quieter. By the 50th person, they hear almost nothing. That is what happens to gradients in a long RNN.

---

## 2. The solution — gates

LSTM solves this by adding **gates** — small switches that control what information passes through.

There are three gates:

| Gate | What it does |
|------|-------------|
| **Forget gate** | Decides what to erase from memory |
| **Input gate** | Decides what new information to add to memory |
| **Output gate** | Decides what part of memory to use as output |

Each gate is a number between 0 and 1 (produced by a sigmoid function):
- **0** means "block this completely — forget it"
- **1** means "let this through completely — remember it"
- **0.7** means "keep 70% of this"

The gates are themselves learned during training. The network learns *when* to remember and *when* to forget.

---

## 3. LSTM — two memory streams

LSTM has **two separate memory streams**:

| Stream | Name | Purpose |
|--------|------|---------|
| `h_t` | Hidden state | Short-term working memory (same as basic RNN) |
| `c_t` | Cell state | Long-term memory — can carry information across many steps |

The cell state is the key innovation. It flows through the network like a conveyor belt, and the gates decide what to add or remove from it.

```
Long-term memory (cell state):
──────────────────────────────────────────────────────►
        ↑ add new info        ↑ add new info
    [forget some]         [forget some]
        ↓ use for output      ↓ use for output

Short-term memory (hidden state):
h₀ → [LSTM] → h₁ → [LSTM] → h₂ → [LSTM] → h₃
```

### How one LSTM step works (conceptually)

```
1. Forget gate:  look at (current input + old hidden state) → decide what to erase from cell state
2. Input gate:   look at (current input + old hidden state) → decide what new info to write to cell state
3. Update cell:  erase the old info, write the new info
4. Output gate:  look at (current input + old hidden state) → decide what to output as new hidden state
```

You do not need to implement this yourself — PyTorch does all of it inside `nn.LSTM`.

---

## 4. LSTM in PyTorch

```python
import torch
import torch.nn as nn

lstm = nn.LSTM(
    input_size=1,    # one number per time step
    hidden_size=16,  # size of hidden state AND cell state
    num_layers=1,
    batch_first=True
)

# Input: 1 sequence, 5 time steps, 1 feature
x = torch.tensor([[[20.0], [22.0], [24.0], [23.0], [25.0]]])

# LSTM returns: output, (hidden_state, cell_state)
output, (h_n, c_n) = lstm(x)

print("Output shape:", output.shape)  # (1, 5, 16) — hidden state at every step
print("h_n shape:", h_n.shape)        # (1, 1, 16) — final hidden state
print("c_n shape:", c_n.shape)        # (1, 1, 16) — final cell state (long-term memory)
```

The main difference from `nn.RNN`: LSTM returns **two** hidden states — `h_n` (short-term) and `c_n` (long-term cell state).

---

## 5. Full LSTM example — sentiment analysis

We read a sentence word by word and predict if it is positive or negative.

```python
import torch
import torch.nn as nn

# Simple vocabulary
word_to_idx = {
    "the": 0, "food": 1, "was": 2, "good": 3, "bad": 4,
    "not": 5, "really": 6, "very": 7, "service": 8, "great": 9,
    "<pad>": 10
}
VOCAB_SIZE = len(word_to_idx)

# Training sentences and labels
sentences = [
    ["the", "food", "was", "good"],       # positive = 1
    ["the", "food", "was", "bad"],        # negative = 0
    ["the", "food", "was", "not", "bad"], # positive = 1  (tricky!)
    ["the", "service", "was", "great"],   # positive = 1
    ["the", "service", "was", "not", "good"], # negative = 0 (tricky!)
]
labels = [1, 0, 1, 1, 0]

# Convert words to numbers
def encode(sentence):
    return torch.tensor([[word_to_idx[w] for w in sentence]])

X = [encode(s) for s in sentences]
y = torch.tensor(labels, dtype=torch.float32)

# Model
class SentimentLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(VOCAB_SIZE, 8)  # each word → 8 numbers
        self.lstm      = nn.LSTM(input_size=8, hidden_size=16, batch_first=True)
        self.linear    = nn.Linear(16, 1)
        self.sigmoid   = nn.Sigmoid()

    def forward(self, x):
        embedded = self.embedding(x)           # words → vectors
        out, (h, c) = self.lstm(embedded)      # process sequence
        last_h = h.squeeze(0)                  # final hidden state
        return self.sigmoid(self.linear(last_h)).squeeze()

model     = SentimentLSTM()
loss_fn   = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Train
for epoch in range(300):
    total_loss = 0
    for xi, yi in zip(X, y):
        pred = model(xi)
        loss = loss_fn(pred, yi)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    if epoch % 100 == 0:
        print(f"Epoch {epoch}  loss: {total_loss/len(X):.4f}")

# Test
model.eval()
test_sentences = [
    ["the", "food", "was", "not", "bad"],
    ["the", "service", "was", "bad"],
]
with torch.no_grad():
    for s in test_sentences:
        x = encode(s)
        prob = model(x).item()
        label = "POSITIVE" if prob >= 0.5 else "NEGATIVE"
        print(f"'{' '.join(s)}' → {label} ({prob:.2f})")
```

Notice the tricky sentences: "not bad" should be positive. LSTM can learn this because it remembers the word "not" when it reaches "bad".

---

## 6. GRU — a simpler version of LSTM

GRU (Gated Recurrent Unit) was invented in 2014 as a **simpler** version of LSTM. It has **two gates** instead of three, and only **one memory stream** instead of two.

| | LSTM | GRU |
|---|------|-----|
| Gates | 3 (forget, input, output) | 2 (reset, update) |
| Memory streams | 2 (hidden state + cell state) | 1 (hidden state only) |
| Parameters | More | Fewer |
| Training speed | Slower | Faster |
| Performance | Often slightly better on long sequences | Often similar, sometimes better on smaller data |

### GRU in PyTorch

```python
import torch
import torch.nn as nn

gru = nn.GRU(
    input_size=1,
    hidden_size=16,
    batch_first=True
)

x = torch.tensor([[[20.0], [22.0], [24.0], [23.0], [25.0]]])

output, h_n = gru(x)   # only one hidden state — simpler than LSTM
print("Output shape:", output.shape)  # (1, 5, 16)
print("h_n shape:", h_n.shape)        # (1, 1, 16)
```

The only difference from `nn.RNN`: replace `nn.RNN` with `nn.GRU`. The rest of your code stays exactly the same.

### Which should you use?

- **Try GRU first** — fewer parameters, trains faster, often similar accuracy
- **Use LSTM** if your sequences are very long (hundreds of steps) or GRU is not good enough
- In practice, the difference is often small — experiment with both

---

## 7. Stacked RNNs — making them deeper

Just like CNNs stack many convolutional layers, you can stack multiple LSTM or GRU layers:

```python
lstm_stacked = nn.LSTM(
    input_size=1,
    hidden_size=32,
    num_layers=2,      # two LSTM layers stacked
    batch_first=True,
    dropout=0.2        # dropout between layers to prevent overfitting
)

x = torch.tensor([[[20.0], [22.0], [24.0], [23.0], [25.0]]])
output, (h_n, c_n) = lstm_stacked(x)

# h_n shape: (2, 1, 32) — one hidden state per layer
print("h_n shape:", h_n.shape)
```

Layer 1 learns low-level patterns. Layer 2 learns higher-level patterns from layer 1's output. More layers = more capacity, but also more data and compute needed.

---

## 8. Bidirectional RNNs

A normal RNN reads left to right. But for tasks like understanding a whole sentence, reading in **both directions** helps:

```
"The food was not bad at all."

Forward:   The → food → was → not → bad → at → all → [summary]
Backward:  all → at  → bad → not → was → food → The → [summary]

Combined:  [forward summary + backward summary] → final answer
```

```python
lstm_bi = nn.LSTM(
    input_size=1,
    hidden_size=16,
    batch_first=True,
    bidirectional=True   # reads forward AND backward
)

x = torch.tensor([[[20.0], [22.0], [24.0]]])
output, (h_n, c_n) = lstm_bi(x)

# output shape: (1, 3, 32) — 32 because 16 forward + 16 backward
print("Output shape:", output.shape)
```

Bidirectional LSTMs are very common in NLP tasks like named entity recognition, where knowing what comes after a word is as important as what came before.

---

## 9. Handling variable-length sequences

Real datasets have sequences of different lengths. A padding token fills the shorter sequences:

```python
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence

# Sequences of different lengths
seq1 = torch.tensor([[1.0], [2.0], [3.0]])          # length 3
seq2 = torch.tensor([[1.0], [2.0], [3.0], [4.0]])   # length 4
seq3 = torch.tensor([[1.0], [2.0]])                  # length 2

# Pad to the same length
padded = pad_sequence([seq1, seq2, seq3], batch_first=True, padding_value=0.0)
lengths = torch.tensor([3, 4, 2])

print("Padded shape:", padded.shape)  # (3, 4, 1) — 3 sequences, max length 4

# Pack — tells LSTM to ignore the padding
packed = pack_padded_sequence(padded, lengths, batch_first=True, enforce_sorted=False)

lstm = nn.LSTM(input_size=1, hidden_size=8, batch_first=True)
packed_output, (h_n, c_n) = lstm(packed)

# Unpack back to padded format
output, lengths_out = pad_packed_sequence(packed_output, batch_first=True)
print("Output shape:", output.shape)
```

---

## 10. Common mistakes

| Mistake | Fix |
|---------|-----|
| Using RNN for very long sequences (100+ steps) | Use LSTM or GRU instead |
| Forgetting LSTM returns `(h_n, c_n)` not just `h_n` | Unpack correctly: `output, (h, c) = lstm(x)` |
| Not resetting hidden state between batches | Start each batch with `h = None` or a fresh zero tensor |
| Input shape wrong | Always check: `(batch_size, seq_length, input_size)` when `batch_first=True` |
| Forgetting to sort sequences by length for packing | Use `enforce_sorted=False` in `pack_padded_sequence` |

---

## Summary

- Basic RNNs **forget** information from long ago — the vanishing gradient problem.
- **LSTM** fixes this with three gates (forget, input, output) and two memory streams (hidden state + cell state).
- **GRU** is a simpler version with two gates and one memory stream — faster to train, similar performance.
- Both use `nn.LSTM` and `nn.GRU` in PyTorch — just swap the class name.
- **Bidirectional** versions read both forward and backward — useful for understanding whole sentences.
- For variable-length sequences, use `pad_sequence` and `pack_padded_sequence`.

```
Basic RNN:  good for short sequences, forgets long-ago information
LSTM:       remembers much longer, three gates control what to keep
GRU:        simpler than LSTM, two gates, usually similar performance
```
