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

## 1. The problem — RNNs forget things from long ago

Let us start with a simple story before any technical terms.

---

### The telephone game

You have played the telephone game, maybe as a child.

Ten people stand in a line. Person 1 whispers a message to Person 2. Person 2 whispers it to Person 3. And so on.

By the time the message reaches Person 10, it has changed. Some words are lost. Some words are wrong. The further down the line, the worse it gets.

<div class="mermaid">
graph LR
    P1["Person 1\n Original message"] -->|whispers| P2["Person 2\n Slightly changed"]
    P2 -->|whispers| P3["Person 3\n More changed"]
    P3 -->|whispers| P4["Person 4\n Even more changed"]
    P4 -->|whispers| P10["Person 10\n Almost nothing left"]
</div>

A basic RNN has exactly the same problem.

---

### How an RNN reads a long sentence

Imagine this sentence:

> "The cat, which was sitting quietly on the old wooden chair next to the window in the kitchen, **was hungry**."

The important connection is: **"The cat"** at the beginning → **"was hungry"** at the end.

An RNN reads this word by word:

<div class="mermaid">
graph LR
    W1["The"] --> M1["memory 1"]
    M1 --> W2["cat"]
    W2 --> M2["memory 2"]
    M2 --> W3["which"]
    W3 --> M3["memory 3"]
    M3 --> W4["was"]
    W4 --> M4["memory 4"]
    M4 --> Dots["... 10 more words ..."]
    Dots --> Mlast["memory 15"]
    Mlast --> Wlast["was hungry"]
</div>

Each step, the RNN updates its memory. But the update **always mixes in new information**. Old information slowly gets pushed out.

By the time the RNN reaches "was hungry" at step 15, the memory of "The cat" from step 1 has been overwritten many times. It is very faint — or completely gone.

---

### Why does this happen? — the shrinking signal

When we train any neural network, we use a process called **backpropagation**. This is how the model learns from its mistakes.

In simple terms:
1. The model makes a prediction
2. We check how wrong it was — this is the **error**
3. We send that error signal **backwards** through the model
4. Every layer uses that signal to adjust its weights

For an RNN, "sending the error backwards" means going **backwards through every time step**.

Here is the key problem. At each step backwards, the error signal gets **multiplied** by a number. In most RNNs, that number is less than 1 — for example, 0.8.

```
Start:           error = 1.0
After 1 step:    1.0 × 0.8 = 0.80
After 2 steps:   0.8 × 0.8 = 0.64
After 3 steps:   0.64 × 0.8 = 0.51
After 5 steps:   0.32
After 10 steps:  0.11
After 20 steps:  0.012
After 50 steps:  0.000001  ← almost zero
```

<div class="mermaid">
graph LR
    E0["Error: 1.0\nstep 50"] -->|"× 0.8"| E1["Error: 0.8\nstep 49"]
    E1 -->|"× 0.8"| E2["Error: 0.64\nstep 48"]
    E2 -->|"× 0.8"| E3["Error: 0.51\nstep 47"]
    E3 -->|"× 0.8"| E4["Error: 0.11\nstep 40"]
    E4 -->|"× 0.8"| E5["Error: 0.000001\nstep 1"]
</div>

By the time this signal reaches the **first time steps**, it is so tiny that the weights there barely change at all. Those early time steps never learn anything useful.

This is called the **vanishing gradient problem**.

> **In plain English:** The RNN cannot learn connections between words or events that are far apart. It only learns from what happened very recently.

---

### Why does this matter?

For short sequences (5–10 steps), basic RNNs work fine.

For longer sequences, they fail on exactly the cases that matter most:

| Task | What the RNN misses |
|------|-------------------|
| Long sentence sentiment | Forgets the subject by the end |
| Paragraph summarisation | Forgets the topic sentence |
| Long time series | Forgets patterns from weeks ago |
| Dialogue | Forgets what was said at the start of the conversation |

---

### The fix — give the RNN a proper memory

The solution is to give the network a **separate, protected memory channel** that does not get overwritten at every step.

Instead of one stream of memory that gets mixed at every step, we add a second stream — one that flows through mostly unchanged unless the model explicitly decides to update it.

This is what **LSTM** does. It adds **gates** — small switches that control what goes into the memory, what stays, and what gets erased.

Think of it like upgrading from a whiteboard (erased every step) to a notebook (you choose what to write, what to keep, and what to cross out).

---

## 2. The solution — gates

### Think of a gate like a water tap

A tap (faucet) can be fully open, fully closed, or anywhere in between.

- **Fully open** → water flows through freely
- **Fully closed** → no water gets through
- **Half open** → some water gets through

LSTM adds three of these taps — called **gates** — to control memory.

Each gate produces a number between **0** and **1**:
- **0** = completely closed → block this information, erase it
- **1** = completely open → let all of this through, keep it
- **0.7** = 70% open → keep 70%, erase 30%

The three gates and what each one does:

| Gate | Simple meaning | Real-life analogy |
|------|---------------|------------------|
| **Forget gate** | "Should I erase something from memory?" | Crossing out old notes in a notebook |
| **Input gate** | "Should I write something new into memory?" | Writing a new note in a notebook |
| **Output gate** | "What part of my memory should I say out loud right now?" | Reading out the relevant part of your notes |

<div class="mermaid">
graph TD
    Input["New word arrives"] --> FG["Forget Gate\nShould I erase anything?"]
    Input --> IG["Input Gate\nShould I write anything new?"]
    Memory["Long-term memory"] --> FG
    FG -->|"erase some"| NewMemory["Updated memory"]
    IG -->|"add new info"| NewMemory
    NewMemory --> OG["Output Gate\nWhat do I say now?"]
    OG --> Hidden["Hidden state output\nused for prediction"]
</div>

The important thing: **the gates are learned**. The model figures out, during training, when to open and close each gate. You do not have to tell it. It learns this automatically from the data.

For example, in a sentiment analysis task ("The food was not bad"), the model learns to:
- Keep the word "not" in memory (input gate stays open)
- Remember "not" is still relevant when it sees "bad" later (forget gate stays closed)
- Reverse the meaning when it sees "bad" (output gate uses the stored "not")

---

## 3. LSTM — two types of memory

Think about how you remember things as a person.

You have two types of memory:

- **Working memory** — what you are thinking about right now. Very short. Changes every second. If someone tells you a phone number, you hold it in your head just long enough to dial it.
- **Long-term memory** — things you remember for a long time. Your name. Your address. Important events. This does not get erased easily.

LSTM gives a neural network exactly these two types:

| Name in LSTM | What it is | Real-life equivalent |
|-------------|-----------|---------------------|
| **Hidden state** (`h`) | Short-term working memory | What you are thinking right now |
| **Cell state** (`c`) | Long-term protected memory | Important things you remember for a long time |

The **cell state** is the key invention of LSTM. It is a separate channel of memory that travels through every step. The gates carefully decide what to add to it, what to erase from it, and what to read from it.

<div class="mermaid">
graph LR
    subgraph Step1["Step 1 - word: The"]
        C0["Long-term memory\nbefore step 1"] --> FG1["Forget gate\nErase?"]
        FG1 --> C1["Long-term memory\nafter step 1"]
        IG1["Input gate\nWrite?"] --> C1
        C1 --> OG1["Output gate\nSpeak?"]
        OG1 --> H1["Short-term memory h1"]
    end

    subgraph Step2["Step 2 - word: cat"]
        C1 --> FG2["Forget gate\nErase?"]
        FG2 --> C2["Long-term memory\nafter step 2"]
        IG2["Input gate\nWrite?"] --> C2
        C2 --> OG2["Output gate\nSpeak?"]
        OG2 --> H2["Short-term memory h2"]
    end
</div>

### What happens at each step — in plain English

Every time a new word arrives, LSTM does four things in order:

**Step 1 — Forget gate asks: "Should I erase anything from long-term memory?"**
> Example: The model just read "he" after a story about a woman. The forget gate erases "woman" from memory, because "he" changes the subject.

**Step 2 — Input gate asks: "Should I write anything new into long-term memory?"**
> Example: The model just read "not". The input gate writes "negation active" into long-term memory.

**Step 3 — Update long-term memory**
> Erase what the forget gate said to erase. Write what the input gate said to write.

**Step 4 — Output gate asks: "What should I output right now?"**
> Read the relevant part of long-term memory and produce the short-term memory `h` that goes to the next layer.

You do not need to code any of this. PyTorch does all four steps automatically when you use `nn.LSTM`.

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
