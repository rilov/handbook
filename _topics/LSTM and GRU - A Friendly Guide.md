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

In Part 14, we learned how an RNN reads data step by step and keeps a hidden state — a small memory of what it has seen.

We also saw the two gradient problems:
- **Vanishing gradient** — the learning signal fades to zero going back through long sequences
- **Exploding gradient** — the learning signal grows out of control

In this part we focus on the deeper consequence of vanishing gradients: **RNNs cannot capture long-distance dependencies**. And we will learn how LSTM and GRU were designed to fix exactly this.

---

## 0. The core problem — long-distance dependencies

Imagine an RNN that has read 100 tokens (words or time steps). We are now at step 100 — we call it **h100**.

Ideally, h100 should carry a memory of **everything from step 1 to step 99**. It should know what happened at the very beginning of the sequence.

But in practice, that is **not what happens**.

The RNN memory at step 100 mostly remembers recent steps — steps 95, 96, 97, 98, 99. Anything from the early steps — step 1, 2, 3 — has been overwritten so many times it is effectively gone.

<div class="mermaid">
graph LR
    X1["Step 1\ntoken x1"] --> H1["h1"]
    H1 --> H2["h2"]
    H2 --> Dots["..."]
    Dots --> H98["h98"]
    H98 --> H99["h99"]
    H99 --> H100["h100\nfinal memory"]

    style X1 fill:#ffcccc
    style H100 fill:#4CAF50,color:#fff
</div>

At h100, the early tokens (shown in red) are almost forgotten. The later tokens (green) dominate the memory.

---

### Why this matters — a real example

Consider this sentence:

> "The **trophy** didn't fit in the suitcase because **it** was too big."

What does "it" refer to? The trophy. But "it" is far from "trophy" in the sentence. A basic RNN reading word by word will have mostly forgotten "trophy" by the time it reaches "it".

Or in a time series:

> Predicting this month's sales based on 12 months of history — the RNN mostly uses the last 2–3 months and ignores the pattern from a year ago.

This is called a **long-distance dependency** — a connection between two things that are far apart in a sequence. Basic RNNs struggle with these. They are designed to handle sequences but fail in practice when sequences are long.

---

### What we need

We need an architecture that can:
1. **Explicitly hold information** for a long time — not just a few steps
2. **Decide what to keep** — not all information is equally important
3. **Pass gradients cleanly** — so even early steps can learn

This is exactly what **LSTM** (Long Short-Term Memory) and **GRU** (Gated Recurrent Unit) provide. They give the network a way to **explicitly choose what to remember and what to forget**.

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

### Does LSTM fully solve the vanishing gradient problem?

**No — but it greatly reduces it.**

A basic RNN must multiply the gradient by the same weight at every single step. This causes the gradient to shrink to almost zero over long sequences.

LSTM does something clever: it keeps a **cell state** — a separate memory channel that runs straight through the sequence. Crucially, the gradient can flow **along the cell state** without being multiplied aggressively at every step. The gates add and remove information through addition (not multiplication), which keeps the gradient much healthier.

<div class="mermaid">
graph LR
    subgraph RNN["Basic RNN — gradient multiplied at every step"]
        direction LR
        R1["h1"] -->|"× weight\n× deriv"| R2["h2"]
        R2 -->|"× weight\n× deriv"| R3["h3"]
        R3 -->|"× weight\n× deriv → near zero"| R100["h100"]
        style R100 fill:#ffcccc
    end

    subgraph LSTM["LSTM — cell state is a gradient highway"]
        direction LR
        L1["c1"] -->|"add/forget"| L2["c2"]
        L2 -->|"add/forget"| L3["c3"]
        L3 -->|"add/forget → still alive"| L100["c100"]
        style L100 fill:#4CAF50,color:#fff
    end
</div>

> **Simple way to think about it:** A basic RNN is like a game of telephone — the message degrades at every person. LSTM is like passing a notebook — you can write new things, cross things out, but the notebook itself travels intact.

**The result:** LSTM can learn dependencies across hundreds of steps. A basic RNN struggles after 10–20 steps.

But LSTM does **not** completely eliminate the vanishing gradient. For extremely long sequences (thousands of steps), even LSTM can struggle. That is why Transformers (covered in a later part) were eventually developed — they use attention, which connects any two positions directly without passing through intermediate steps at all.

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

## 6. Why LSTM is a "heavy" model

LSTM works very well — but it has a cost.

Each of the three gates (forget, input, output) has its **own set of weights**. These weights are all trained separately during training. This means LSTM has a large number of parameters compared to a basic RNN.

Think of it like this: a basic RNN is a small notebook with one page. LSTM is a three-section binder — much more organised and powerful, but heavier and more expensive to carry.

| Model | Gates | Weight matrices | Relative size |
|-------|-------|----------------|--------------|
| Basic RNN | 0 | 2 (input + hidden) | Small |
| LSTM | 3 (forget, input, output) | 8 (4 for input, 4 for hidden) | Large |
| GRU | 2 (update, reset) | 6 (3 for input, 3 for hidden) | Medium |

Because LSTM has so many parameters, it needs **more training data** to learn properly. If you train LSTM on a small dataset, it may overfit — it memorises the training examples instead of learning general patterns.

> **Rule of thumb from research:** If you have a large dataset, LSTM tends to perform better. If you have a smaller dataset, GRU often works just as well and trains more reliably.

---

## 7. GRU — a simpler version of LSTM

Researchers asked: "Can we get the same long-term memory benefit as LSTM, but with fewer parameters?"

The answer was **GRU (Gated Recurrent Unit)**, introduced in 2014.

The key idea: instead of three separate gates (forget, input, output), combine the forget gate and input gate into a single gate called the **update gate**. And instead of two memory streams (cell state + hidden state), use just one.

### The two GRU gates

**Gate 1 — Update gate**

The update gate combines what LSTM's forget gate and input gate did separately.

It asks one question: **"How much of the old memory should I keep, and how much should I replace with new information?"**

- Close to 1 → keep most of the old memory, add very little new
- Close to 0 → mostly replace the old memory with new information

Think of it like a mixing knob on a music player — slide it left for more old, right for more new.

**Gate 2 — Reset gate**

The reset gate asks: **"When I am computing new information to possibly write into memory, how much of the current old memory should I look at?"**

- Close to 1 → look at all of the old memory when computing the new info
- Close to 0 → mostly ignore the old memory — start fresh

Think of it like a "clear history" button for computing new content — if the topic has completely changed, reset and compute the new info without being influenced by the old.

<div class="mermaid">
graph TD
    NewInput["New input arrives"] --> UG["Update Gate\nHow much old to keep\nvs new to add?"]
    NewInput --> RG["Reset Gate\nWhen computing new info\nhow much old memory to look at?"]
    OldMemory["Old hidden state h"] --> UG
    OldMemory --> RG
    RG --> NewCandidate["New candidate memory\ncomputed with reset gate"]
    UG --> NewCandidate
    UG -->|"blend old + new"| NewHidden["Updated hidden state h'"]
    NewCandidate --> NewHidden
</div>

### LSTM vs GRU — what gets combined

<div class="mermaid">
graph TD
    subgraph LSTM_Gates["LSTM — 3 gates"]
        FG["Forget gate\nerase old cell state"]
        IG["Input gate\nwrite to cell state"]
        OG["Output gate\nread from cell state to hidden"]
    end

    subgraph GRU_Gates["GRU — 2 gates"]
        UGate["Update gate\ncombines forget + input\ncontrols blend of old and new"]
        RGate["Reset gate\ncontrols how much old memory\ninfluences new candidate"]
    end
</div>

GRU does **exactly the same job** as LSTM — it can hold long-term dependencies — but it does it with fewer moving parts.

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

output, h_n = gru(x)   # only one hidden state — no cell state
print("Output shape:", output.shape)  # (1, 5, 16)
print("h_n shape:", h_n.shape)        # (1, 1, 16)
```

The only code change from LSTM: `nn.LSTM` → `nn.GRU`. Everything else stays the same.

Note: GRU returns only `h_n` (one hidden state). LSTM returns `(h_n, c_n)` (hidden state + cell state).

---

## 8. Choosing between LSTM and GRU

There is no single best answer. Both do the same job. Here is the practical guide:

| Situation | Recommendation |
|-----------|---------------|
| **Large dataset** (tens of thousands of examples or more) | Use LSTM — more parameters can learn richer patterns |
| **Small or medium dataset** | Use GRU — fewer parameters, less risk of overfitting |
| **Compute is limited** (small GPU, mobile device) | Use GRU — trains faster, uses less memory |
| **Very long sequences** (hundreds of steps) | Start with LSTM — slightly better at very long-range dependencies |
| **You are not sure** | Try GRU first. If it is not good enough, switch to LSTM |

<div class="mermaid">
graph TD
    Q1["How much data do you have?"]
    Q1 -->|"Large dataset\nmany examples"| LSTM_rec["Use LSTM\nmore parameters\nbetter on large data"]
    Q1 -->|"Small or medium\ndataset"| GRU_rec["Use GRU\nfewer parameters\neasier to train"]
    Q1 -->|"Not sure"| Try["Start with GRU\nswitch to LSTM\nif needed"]
    style LSTM_rec fill:#4CAF50,color:#fff
    style GRU_rec fill:#2196F3,color:#fff
</div>

> **Key insight from the syllabus:** The research community has not found definitive evidence that one is always better. The data-size rule of thumb is the most reliable guide in practice.

---

## 9. Stacked RNNs — making them deeper

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

## 10. Bidirectional RNNs

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

## 11. Padding, Masking, and Variable-Length Sequences

### Why is this a problem?

RNNs and LSTMs are designed to handle sequences of different lengths. A sentence can be 5 words. Another sentence can be 20 words. That is fine — the same RNN cell can process any number of steps.

But there is a problem when you train the model.

During training we use **mini-batches** — we pick, say, 32 sentences at a time and train on all 32 together. This is much faster than training one sentence at a time.

The problem: to process 32 sentences together, they must all be the **same length**. Computer hardware (GPU/CPU) processes data in rectangular grids — rows and columns. You cannot have one row with 5 columns and another row with 20 columns in the same grid.

<div class="mermaid">
graph TD
    subgraph Problem["The problem — sequences in a batch have different lengths"]
        S1["Sentence 1: The cat sat → 3 tokens"]
        S2["Sentence 2: I went to the shop yesterday → 6 tokens"]
        S3["Sentence 3: Hi → 1 token"]
        S1 --> BAD["Cannot fit in one\nrectangular grid ❌"]
        S2 --> BAD
        S3 --> BAD
    end
</div>

So how do we fix this? There are two main approaches: **padding** and **truncation**.

---

### Approach 1 — Padding

**Padding** means: find the longest sequence in the batch, then add zeros to all shorter sequences until they are the same length.

```
Sentence 1:  [the]  [cat]  [sat]  [0]    [0]    [0]    ← padded with 3 zeros
Sentence 2:  [I]    [went] [to]   [the]  [shop] [yest.] ← longest — no padding needed
Sentence 3:  [Hi]   [0]    [0]    [0]    [0]    [0]    ← padded with 5 zeros
```

Now all three sentences have length 6. They fit in a rectangular grid.

<div class="mermaid">
graph LR
    subgraph After["After padding — all same length"]
        R1["the | cat | sat | 0 | 0 | 0"]
        R2["I | went | to | the | shop | yest"]
        R3["Hi | 0 | 0 | 0 | 0 | 0"]
    end
</div>

The `0` values are called **padding tokens**. They carry no real information — they are just placeholders to make the shape rectangular.

---

### The problem with padding — wasted computation

Padding works, but it has a cost.

Imagine your dataset has 10,000 sentences. Most sentences are 50 tokens long. But one sentence is 200 tokens long.

If you pad to the maximum length, **every single sentence** gets padded to 200 tokens. That means 150 zeros added to 9,999 sentences — most of the data is now fake zeros.

```
Dataset of 10,000 sentences
Average length: 50 tokens
Longest sentence: 200 tokens

After padding:
  9,999 sentences × 150 fake zeros each = enormous amount of wasted computation
```

The LSTM will waste time processing all those zeros. Training becomes slow and memory usage grows.

---

### Approach 2 — Truncation

Instead of padding everything to the longest sequence, you can **truncate** the outlier long sequences down to a sensible length.

```
Maximum sentence you allow: 50 tokens
Sentence with 200 tokens → keep only the first 50 tokens, discard the rest
```

Yes — you lose some information from that one very long sentence. But you avoid padding 9,999 other sentences with 150 zeros each.

<div class="mermaid">
graph TD
    Q["One sentence: 200 tokens\nEveryone else: ~50 tokens"]
    Q -->|"Option A: Padding"| PA["Pad all 9999 sentences\nto 200 tokens\n→ huge waste"]
    Q -->|"Option B: Truncation"| PB["Cut the 200-token sentence\nto 50 tokens\n→ small information loss"]
    style PA fill:#ffcccc
    style PB fill:#4CAF50,color:#fff
</div>

**When to truncate:** When one or a few sequences are much longer than the rest. Losing 50% of one sentence is usually acceptable if it saves padding 10,000 other sentences.

---

### Approach 3 — Masking (tell the model to ignore the zeros)

Even with padding, there is another problem: the LSTM does not automatically know which positions are real data and which are padding zeros. It will process all the zeros and let them influence the memory — which we do not want.

**Masking** solves this. A mask is a list of `True`/`False` values that tells the model: "these positions are real, these positions are padding — ignore them."

```
Sequence:   [the]  [cat]  [sat]  [0]   [0]   [0]
Mask:       [True] [True] [True] [False][False][False]
```

The LSTM processes positions marked `True` normally. For positions marked `False` (padding), it stops updating the memory — the hidden state is frozen at the last real token.

---

### Putting it together — full PyTorch example

PyTorch provides three functions to handle this properly:

| Function | What it does |
|----------|-------------|
| `pad_sequence` | Pads a list of different-length tensors to the same length |
| `pack_padded_sequence` | Packs the padded data + tells LSTM which positions are real |
| `pad_packed_sequence` | Unpacks the output back to a regular padded tensor |

```python
import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence

# --- Three sentences of different lengths ---
# Each token is represented as a single number (in real NLP it would be an embedding)
sentence1 = torch.tensor([[1.0], [2.0], [3.0]])             # 3 tokens
sentence2 = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])  # 6 tokens
sentence3 = torch.tensor([[1.0]])                            # 1 token

print("Lengths before padding:", 3, 6, 1)

# --- Step 1: Pad to the same length ---
# pad_sequence pads all to the length of the longest (6)
padded = pad_sequence(
    [sentence1, sentence2, sentence3],
    batch_first=True,    # shape: (batch, seq_len, features)
    padding_value=0.0    # fill with zeros
)
lengths = torch.tensor([3, 6, 1])  # real length of each sequence

print("\nAfter padding:")
print(padded)
# tensor([[[1.], [2.], [3.], [0.], [0.], [0.]],   ← sentence1 padded
#         [[1.], [2.], [3.], [4.], [5.], [6.]],    ← sentence2 (longest, no padding)
#         [[1.], [0.], [0.], [0.], [0.], [0.]]])   ← sentence3 padded
print("Shape:", padded.shape)  # (3, 6, 1) — 3 sentences, length 6, 1 feature

# --- Step 2: Pack — tell LSTM which positions are real ---
# This creates a compact form that skips the padding during computation
packed = pack_padded_sequence(
    padded,
    lengths,
    batch_first=True,
    enforce_sorted=False  # sequences do not need to be sorted by length
)

# --- Step 3: Run through LSTM ---
lstm = nn.LSTM(input_size=1, hidden_size=8, batch_first=True)
packed_output, (h_n, c_n) = lstm(packed)

# h_n holds the final hidden state for each sequence
# Crucially: for sentence1, it is the state after token 3 (NOT after the zeros)
# For sentence3, it is the state after token 1 (NOT after the zeros)
print("\nh_n shape:", h_n.shape)  # (1, 3, 8) — 1 layer, 3 sequences, 8 hidden units

# --- Step 4: Unpack back to padded format (if you need per-step outputs) ---
output, output_lengths = pad_packed_sequence(packed_output, batch_first=True)
print("Output shape:", output.shape)  # (3, 6, 8) — padded positions have all zeros
```

The key benefit of packing: **the LSTM's final hidden state `h_n` correctly reflects only the real tokens**. Without packing, the LSTM would process the zeros too, and `h_n` would be corrupted by the padding.

---

### Summary — which approach to use

| Situation | Recommended approach |
|-----------|---------------------|
| All sequences are similar length | Simple padding — easy to implement |
| One or few very long outlier sequences | Truncate the outliers, then pad |
| Small differences in length | Padding + packing (standard approach) |
| Large differences in length | Truncate to a max length, then pad + pack |

```python
# Practical rule for text data
MAX_LENGTH = 100   # decide a max length based on your data

def prepare_sequence(tokens, max_length=MAX_LENGTH):
    if len(tokens) > max_length:
        tokens = tokens[:max_length]          # truncate
    return tokens
    # Then pad_sequence handles the rest
```

---

## 12. Common mistakes

| Mistake | Fix |
|---------|-----|
| Using RNN for very long sequences (100+ steps) | Use LSTM or GRU instead |
| Forgetting LSTM returns `(h_n, c_n)` not just `h_n` | Unpack correctly: `output, (h, c) = lstm(x)` |
| Not resetting hidden state between batches | Start each batch with `h = None` or a fresh zero tensor |
| Input shape wrong | Always check: `(batch_size, seq_length, input_size)` when `batch_first=True` |
| Forgetting to sort sequences by length for packing | Use `enforce_sorted=False` in `pack_padded_sequence` |

---

## Summary

| Concept | Simple meaning |
|---------|---------------|
| **Long-distance dependency** | A connection between two tokens that are far apart — basic RNNs cannot learn these |
| **h100 problem** | At step 100, the RNN barely remembers step 1 — memory gets overwritten at every step |
| **LSTM cell state** | A protected long-term memory channel — gradients can flow along it without shrinking |
| **LSTM forget gate** | Decides what to erase from long-term memory |
| **LSTM input gate** | Decides what new info to write into long-term memory |
| **LSTM output gate** | Decides what to output from long-term memory as short-term hidden state |
| **LSTM reduces vanishing gradient** | Yes — the cell state highway keeps gradients alive. But it does not fully eliminate the problem |
| **LSTM is heavy** | Three gates × own weight matrices = many parameters → needs more data to train well |
| **GRU update gate** | Combines forget + input: controls how much old memory to keep vs how much new info to add |
| **GRU reset gate** | Controls how much old memory to look at when computing new candidate information |
| **Data-size rule** | Large dataset → try LSTM. Small/medium dataset → try GRU first |

```
Basic RNN:  short sequences only — forgets long-ago information
LSTM:       long-distance dependencies — cell state + 3 gates — heavy, needs more data
GRU:        same capability — 2 gates — lighter, trains faster, good for smaller datasets
```
