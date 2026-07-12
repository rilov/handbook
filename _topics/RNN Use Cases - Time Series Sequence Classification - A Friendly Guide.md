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

But before we dive into specific tasks, we need to understand something important: **there are different patterns for how sequences can go in and come out of an RNN**.

---

## 0. Sequence modeling patterns — what goes in, what comes out

An RNN takes a sequence as input. But what it outputs can be very different depending on the task.

There are three main patterns:

| Pattern | Input | Output | Example tasks |
|---------|-------|--------|--------------|
| **Many-to-One** | Many tokens | One answer | Sentiment analysis, spam detection, time series forecast |
| **Many-to-Many** | Many tokens | Many tokens | POS tagging, NER, summarization, translation |
| **One-to-Many** | One input | Many tokens | Image captioning, music generation |

---

### Pattern 1 — Many to One

**Input:** a sequence of many tokens (many steps)
**Output:** a single answer for the whole sequence

The RNN reads every step and builds memory. At the very last step, you take the final memory (the final hidden state) and pass it through a linear layer to get **one answer**.

<div class="mermaid">
graph LR
    X1["token 1"] --> RNN1["RNN step 1"]
    RNN1 --> RNN2["RNN step 2"]
    X2["token 2"] --> RNN2
    RNN2 --> RNN3["RNN step 3"]
    X3["token 3"] --> RNN3
    RNN3 --> RNN4["RNN step 4"]
    X4["token 4"] --> RNN4
    RNN4 -->|"final hidden state"| LIN["Linear layer"]
    LIN --> OUT["One output\ne.g. Positive / Negative"]
</div>

**Real examples:**

- **Sentiment analysis** — input: "The food was not bad at all" (7 words) → output: Positive
- **Spam detection** — input: email words → output: Spam or Not Spam
- **Time series forecasting** — input: last 7 days of temperature → output: tomorrow's temperature
- **Document classification** — input: article → output: Sports / Politics / Tech

> All **classification tasks** where you want one label for the whole sequence fall into Many-to-One.

---

### Pattern 2 — Many to Many

**Input:** a sequence of many tokens
**Output:** a sequence of many tokens (one per input step, or a different-length output sequence)

There are two sub-types:

**Sub-type A — Same length output (one tag per input token)**

The RNN produces an output at **every step**, not just the last one. You take the hidden state at each step and pass it through a linear layer to get a tag for that position.

<div class="mermaid">
graph LR
    X1["The"] --> RNN1["step 1"]
    X2["cat"] --> RNN2["step 2"]
    X3["sat"] --> RNN3["step 3"]
    RNN1 --> RNN2
    RNN2 --> RNN3
    RNN1 --> T1["DET"]
    RNN2 --> T2["NOUN"]
    RNN3 --> T3["VERB"]
</div>

**Real examples (same-length):**

- **Part-of-speech (POS) tagging** — input: "The cat sat" → output: "DET NOUN VERB" (one tag per word)
- **Named entity recognition (NER)** — input: "Barack Obama visited Paris" → output: "PERSON PERSON O LOCATION"
- **Sequence labelling** — any task where every input token gets its own label

**Sub-type B — Different length output (encoder-decoder / seq2seq)**

The input sequence and output sequence can be **different lengths**. You encode the whole input into a final memory vector, then use a separate decoder RNN to generate the output sequence one token at a time.

<div class="mermaid">
graph LR
    subgraph Encoder["Encoder RNN — reads input"]
        E1["Bonjour"] --> E2["le"] --> E3["monde"]
        E3 --> MEM["Memory\nvector"]
    end

    subgraph Decoder["Decoder RNN — generates output"]
        MEM --> D1["Hello"]
        D1 --> D2["world"]
    end
</div>

**Real examples (different-length):**

- **Machine translation** — input: "Bonjour le monde" (French, 3 words) → output: "Hello world" (English, 2 words)
- **Text summarization** — input: long document (500 words) → output: summary (50 words)
- **Dialogue generation** — input: "How are you?" → output: "I am doing well, thank you."

> Both sub-types fall into **Many-to-Many**. The difference is whether output length equals input length or not.

---

### Pattern 3 — One to Many

**Input:** a single item (not a sequence)
**Output:** a sequence of many tokens generated one at a time

There is no sequence coming in — just one thing (an image, a number, a label). The decoder RNN generates output step by step, using its own previous output as input to the next step.

<div class="mermaid">
graph LR
    IMG["One input\ne.g. an image"] --> H0["Initial hidden state"]
    H0 --> D1["a"]
    D1 --> D2["cat"]
    D2 --> D3["sitting"]
    D3 --> D4["on"]
    D4 --> D5["a chair"]
</div>

**Real examples:**

- **Image captioning** — input: one photo → output: "A cat sitting on a wooden chair" (many words)
- **Music generation** — input: one starting note → output: a sequence of notes
- **Story generation** — input: one prompt word → output: many sentences

> The key: **the input is not a sequence**. The model generates the output sequence from scratch, conditioned on just one thing.

---

### All three patterns at a glance

<div class="mermaid">
graph TD
    subgraph M1["Many-to-One"]
        direction LR
        A1["x1 → x2 → x3 → x4"] --> B1["one answer"]
    end

    subgraph M2["Many-to-Many (same length)"]
        direction LR
        A2["x1 → x2 → x3 → x4"] --> B2["y1   y2   y3   y4"]
    end

    subgraph M3["Many-to-Many (different length)"]
        direction LR
        A3["x1 → x2 → x3"] --> B3["y1 → y2 → y3 → y4 → y5"]
    end

    subgraph M4["One-to-Many"]
        direction LR
        A4["one input"] --> B4["y1 → y2 → y3 → y4"]
    end
</div>

---

Now let us look at how to implement each pattern in PyTorch, starting with the most common ones.

---

## 1. Time series forecasting — predicting what comes next (Many-to-One)

### What is time series forecasting?

**Time series forecasting** means predicting future values based on data collected over time.

Unlike regular data — where each row is independent — time series data is **sequential**. Each value depends on what came before. The order matters.

Examples of time series data:

| Data | Time step | What you want to predict |
|------|-----------|------------------------|
| Daily stock prices | One day | Tomorrow's price |
| Hourly temperatures | One hour | Next hour's temperature |
| Monthly sales | One month | Next month's sales |
| Website traffic | One day | Tomorrow's visitor count |
| Patient heart rate | One second | Next second's reading |

### Why sequential order matters

Imagine you shuffle the daily temperatures for the past month randomly. The numbers are still there — but the pattern is destroyed. You can no longer tell if temperatures are rising, falling, or cycling. A model trained on shuffled data would learn nothing useful.

This is exactly why a normal neural network cannot do time series forecasting well — it sees all inputs at once without any sense of order. An RNN reads values **one at a time, in order**, building memory as it goes. That is what makes it suitable.

---

### What patterns does a time series contain?

Good forecasting comes from recognising the patterns hidden in past data. There are four main types:

**1 — Trend**: a long-term direction, either rising or falling.
> Example: Monthly sales slowly increasing over a year as the business grows.

**2 — Seasonality**: a repeating pattern at regular intervals.
> Example: Electricity usage spikes every summer (air conditioning) and every winter (heating). It repeats at the same time every year.

**3 — Cycles and fluctuations**: irregular rises and falls caused by external factors.
> Example: Sales jumping unexpectedly after a news story, or dipping during an economic downturn. Less regular than seasonality.

**4 — Anomalies**: unusual values that do not fit the pattern at all.
> Example: A sudden spike in server traffic that indicates a security incident or a viral post.

<div class="mermaid">
graph LR
    subgraph Trend["Trend — steady upward direction"]
        T1["Jan\n100"] --> T2["Feb\n110"] --> T3["Mar\n122"] --> T4["Apr\n135"]
    end
    subgraph Season["Seasonality — repeating pattern"]
        S1["Jan\nlow"] --> S2["Jul\nhigh"] --> S3["Jan\nlow"] --> S4["Jul\nhigh"]
    end
    subgraph Anomaly["Anomaly — sudden unexpected spike"]
        A1["Mon\n50"] --> A2["Tue\n52"] --> A3["Wed\n200 ⚠️"] --> A4["Thu\n51"]
        style A3 fill:#ff4444,color:#fff
    end
</div>

An RNN can learn to recognise all four of these patterns from the sequence of past values — because it processes them in order and remembers what it has seen.

---

### Why RNNs are good at this

A simple model (like linear regression) can follow a straight trend. But it cannot capture:
- Patterns that depend on what happened 7 steps ago (weekly seasonality)
- Patterns that change over time (an upward trend that accelerates)
- Interactions between trend and anomaly

An RNN remembers past steps. Its hidden state at step 30 contains information about steps 1–29. This lets it capture complex, time-dependent relationships that simpler models miss.

---

### The task in one line

> Given the last N values in a sequence, predict the next value.

```
x₁ → x₂ → x₃ → x₄ → x₅ → [final hidden state] → [Linear] → predicted x₆
```

This is a **Many-to-One** pattern: many input steps, one output prediction.

---

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

## 2. Sequence classification — one label for the whole sequence (Many-to-One)

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

## 3. Sequence labelling — one label per step (Many-to-Many, same length)

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
