---
title: "Part 14: RNN - Recurrent Neural Networks - A Friendly Guide"
category: Deep Learning
order: 14
tags:
  - deep-learning
  - rnn
  - recurrent-neural-networks
  - sequential-data
  - time-series
  - pytorch
  - beginners
  - friendly
summary: A beginner-friendly introduction to Recurrent Neural Networks. Learn why normal neural networks cannot handle sequences, how an RNN reads data step by step, and how to build one in PyTorch using simple everyday examples.
---

# Part 14: RNN — Recurrent Neural Networks — A Friendly Guide

In Parts 1 to 13, every model we built read the **whole input at once**.

You gave it 5 numbers — it gave back one answer. You gave it a 32×32 image — it gave back a label. The order of the input did not matter. You could shuffle the pixels and the model would still try to process them.

But some data is different. Some data has **order** — and the order is the whole point.

- "The food was **not** bad." → positive or negative?
- "The food was bad, **not** good." → positive or negative?

The same words. Very different meaning — because of **order**.

A normal neural network cannot tell the difference. An **RNN** can.

---

## 1. What is sequential data?

Sequential data is data where **position matters**. Each piece depends on what came before.

Here are real examples:

| Data | Why order matters |
|------|------------------|
| A sentence | Word 3 changes meaning based on word 1 and 2 |
| Daily temperatures | Today's temperature depends on yesterday's |
| Stock prices | Tomorrow's price depends on today and last week |
| Audio | Each sound depends on the sounds just before it |
| Video | Each frame depends on the frames before it |

Think of reading a book. You read word by word, left to right. Each word you read changes your understanding of what comes next. If you read the words in random order, the story makes no sense.

A normal neural network reads all words at once, like taking a photo of the whole page and looking at it without reading order. An RNN reads **one word at a time, left to right, remembering what it read before**.

---

## 2. Why normal neural networks struggle with sequences

Let us use a simple example. You want to predict the **next temperature** given the last 3 days:

```
Day 1: 20°C
Day 2: 22°C
Day 3: 24°C
→ Predict Day 4
```

A normal neural network (MLP) takes all three numbers and tries to find the answer:

```python
import torch
import torch.nn as nn

# Normal network — takes all 3 days at once
mlp = nn.Sequential(
    nn.Linear(3, 8),
    nn.ReLU(),
    nn.Linear(8, 1)
)

x = torch.tensor([[20.0, 22.0, 24.0]])
print(mlp(x))   # some prediction
```

This works for 3 days. But what if sometimes you have 3 days of data and sometimes 7 days? The network has a fixed input size — it cannot handle different length sequences.

More importantly: a normal network **does not know that day 3 comes after day 2**. It just sees three numbers. It has no concept of "earlier" or "later".

> **Simple way to think about it:** A normal network is like looking at 3 numbers on a piece of paper all at once. An RNN is like reading a diary — one entry at a time, remembering what you read on the previous page.

---

## 3. The key idea of RNN — memory

An RNN processes data **one step at a time**. After each step, it keeps a small memory called the **hidden state**.

```
Step 1: Read "20°C" → update memory → memory now holds info about day 1
Step 2: Read "22°C" → update memory (using old memory + new input) → memory now holds info about days 1 and 2
Step 3: Read "24°C" → update memory → memory now holds info about all 3 days
Step 4: Use memory to predict day 4
```

The hidden state is just a small list of numbers — but those numbers carry a summary of everything the RNN has seen so far.

```
hidden state = memory of the past
```

---

## 4. How one RNN step works

At each step, the RNN does a very simple calculation:

```
new memory = tanh( (input × weight_input) + (old memory × weight_memory) + bias )
```

In plain English:
- Take the **current input** (e.g. today's temperature)
- Take the **old memory** (what we remember from previous steps)
- Multiply each by their own weights
- Add them together
- Pass through `tanh` (squashes the result between -1 and +1)
- This gives the **new memory**

```python
import torch
import torch.nn as nn

# One RNN cell — manual version to understand it
input_size  = 1    # one number per step (temperature)
hidden_size = 4    # memory has 4 numbers

# Weights
W_input  = nn.Linear(input_size,  hidden_size, bias=False)
W_hidden = nn.Linear(hidden_size, hidden_size, bias=True)

# One step
def rnn_step(x_t, h_prev):
    return torch.tanh(W_input(x_t) + W_hidden(h_prev))

# Starting memory = all zeros (no memory yet)
h = torch.zeros(1, hidden_size)

# Process 3 days one step at a time
for temp in [20.0, 22.0, 24.0]:
    x = torch.tensor([[temp]])
    h = rnn_step(x, h)
    print(f"After {temp}°C → memory: {h.detach().numpy().round(3)}")
```

Output:
```
After 20.0°C → memory: [[ 0.999  0.891 -0.723  0.445]]
After 22.0°C → memory: [[ 1.000  0.997 -0.912  0.781]]
After 24.0°C → memory: [[ 1.000  0.999 -0.961  0.893]]
```

The memory updates at every step. By the end, it holds a compressed summary of all three days.

---

## 5. The same weights at every step

This is very important: **the RNN uses the exact same weights at every single step**.

Whether you are processing step 1, step 5, or step 100 — the same `W_input` and `W_hidden` are used.

This is why RNNs can handle sequences of **any length**. You do not need different weights for different positions. The same small set of weights is applied over and over.

```
Step 1:  x₁ + h₀  →  [same weights]  →  h₁
Step 2:  x₂ + h₁  →  [same weights]  →  h₂
Step 3:  x₃ + h₂  →  [same weights]  →  h₃
...
Step N:  xₙ + hₙ₋₁ → [same weights]  →  hₙ
```

> **Memory trick:** Think of a person reading a book. They use the same brain (same weights) to understand every word. The brain does not change for page 1 vs page 100. What changes is their memory of what they have read so far.

---

## 6. Unfolding — seeing the RNN across time

When we draw an RNN "unfolded" across time steps, it looks like a chain:

```
x₁ → [RNN] → h₁ → [RNN] → h₂ → [RNN] → h₃ → output
        ↑               ↑               ↑
    same weights    same weights    same weights
```

Each box in the chain is the **same RNN cell** applied again. The hidden state `h` flows from left to right, carrying memory forward.

This unfolded view is also how PyTorch trains the RNN — it calculates gradients by going backwards through the chain (called **Backpropagation Through Time** or BPTT).

---

## 7. Using PyTorch's built-in RNN

You do not need to write the step function yourself. PyTorch has `nn.RNN`:

```python
import torch
import torch.nn as nn

# Build a simple RNN
rnn = nn.RNN(
    input_size=1,    # one number per time step
    hidden_size=8,   # memory has 8 numbers
    num_layers=1,    # one layer of RNN cells
    batch_first=True # input shape: (batch, time_steps, features)
)

# Simulate a sequence: batch of 1, 5 time steps, 1 feature per step
x = torch.tensor([[[20.0], [22.0], [24.0], [23.0], [25.0]]])
# Shape: (1, 5, 1) — 1 sequence, 5 steps, 1 number per step

# Run through RNN
output, h_final = rnn(x)

print("Output shape:", output.shape)    # (1, 5, 8) — 8 hidden values at every step
print("Final hidden shape:", h_final.shape)  # (1, 1, 8) — final memory
print("Final memory:", h_final.detach().numpy().round(3))
```

- `output` — the hidden state at **every** time step (useful for sequence labelling)
- `h_final` — the hidden state at the **last** step only (useful for classification)

---

## 8. Full example — temperature prediction

```python
import torch
import torch.nn as nn
import numpy as np

# Make fake temperature data
# Input: 3 days. Output: next day's temperature.
torch.manual_seed(42)

temperatures = [20, 22, 24, 23, 25, 26, 24, 22, 21, 23, 25, 27]

# Create sequences of length 3
X, y = [], []
for i in range(len(temperatures) - 3):
    X.append(temperatures[i:i+3])
    y.append(temperatures[i+3])

X = torch.tensor(X, dtype=torch.float32).unsqueeze(-1)  # (N, 3, 1)
y = torch.tensor(y, dtype=torch.float32).unsqueeze(-1)  # (N, 1)

# Model: RNN → Linear layer to predict one number
class TempPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.rnn    = nn.RNN(input_size=1, hidden_size=16, batch_first=True)
        self.linear = nn.Linear(16, 1)

    def forward(self, x):
        output, h = self.rnn(x)
        last_hidden = h.squeeze(0)   # take the final memory
        return self.linear(last_hidden)

model     = TempPredictor()
loss_fn   = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Train
for epoch in range(200):
    pred = model(X)
    loss = loss_fn(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 50 == 0:
        print(f"Epoch {epoch}  loss: {loss.item():.4f}")

# Predict
with torch.no_grad():
    test = torch.tensor([[[23.0], [25.0], [27.0]]])
    print(f"\nGiven: 23, 25, 27°C → Predicted next: {model(test).item():.1f}°C")
```

---

## 9. Practical applications of RNNs

| Application | What the sequence is | What the RNN predicts |
|-------------|---------------------|----------------------|
| **Weather forecasting** | Past temperatures | Next day's temperature |
| **Spam detection** | Words in an email, one by one | Spam or not spam |
| **Stock price prediction** | Daily prices | Tomorrow's price |
| **Speech recognition** | Audio frames | Words being spoken |
| **Text generation** | Previous words | Next word |
| **Sentiment analysis** | Words in a review | Positive or negative |
| **Music generation** | Previous notes | Next note |

---

## 10. What RNNs are not good at

RNNs have one big weakness: **they forget things that happened a long time ago**.

Imagine reading a very long book. By chapter 20, you may have forgotten a small detail from chapter 1. An RNN has the same problem — its memory fades as the sequence gets longer.

For example:

```
"The cat, which was sitting on the old wooden chair by the window, was hungry."
```

By the time the RNN reaches "was hungry", it may have partly forgotten "The cat" from the beginning.

This is called the **vanishing gradient problem**. It is why LSTM and GRU were invented — and that is exactly what Part 15 covers.

---

## 11. Quick recap quiz

Before moving on, check your understanding:

**Q1:** You have weather data for 10 days. Each day has one temperature reading. What is the input shape for an RNN?
- Answer: `(1, 10, 1)` — 1 sequence, 10 time steps, 1 feature per step

**Q2:** Does an RNN use different weights for step 1 and step 10?
- Answer: No — the same weights are used at every step

**Q3:** What does the hidden state hold?
- Answer: A memory summary of everything the RNN has seen so far

**Q4:** Why can RNNs handle sequences of any length?
- Answer: Because the same weights are reused at every step — there is no fixed input size

---

## Summary

- Some data has **order** — changing the order changes the meaning. Normal networks cannot handle this.
- An RNN reads data **one step at a time** and keeps a **hidden state** (memory) that is updated at every step.
- The **same weights** are used at every time step — this is why RNNs work on sequences of any length.
- After processing all steps, the final hidden state holds a summary of the whole sequence.
- RNNs struggle with **long sequences** because memory fades — this is fixed by LSTM and GRU in Part 15.

```
Normal network:  [x₁, x₂, x₃] → model → answer
                  (all at once, no order)

RNN:             x₁ → memory → x₂ → memory → x₃ → memory → answer
                  (one at a time, order matters, memory carries forward)
```
