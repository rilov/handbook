---
title: "Part 2: From Machine Learning to Deep Learning - A Friendly Guide"
category: Deep Learning
order: 2
tags:
  - deep-learning
  - machine-learning
  - neural-networks
  - hidden-layers
  - feature-engineering
  - feature-learning
  - spam-detection
  - beginners
  - friendly
summary: Understand how a model actually learns — what labels are, why they are required for spam detection, what loss means, and the exact difference between traditional machine learning and deep learning. Builds directly on Part 1.
---

# Part 2: From Machine Learning to Deep Learning — A Friendly Guide

## What Part 1 covered — and what it left out

Part 1 showed you the **mechanics** of a neuron:

- How an email becomes a feature vector of numbers
- How a neuron multiplies inputs by weights, adds a bias, and applies sigmoid
- What a hidden layer is structurally
- What weights and biases are stored in the model

But Part 1 left one big question unanswered:

> **Where did those weights come from? How does the model actually learn them?**

Part 1 used manually written weights like `[0.8, 0.6, -1.2, 2.0, 0.01]` to demonstrate the calculation. A real model does not start with useful weights. It starts with random ones, and **learns** better values by repeatedly looking at labelled examples and correcting its mistakes.

That is what Part 2 is about: **the learning process itself**, and how traditional machine learning and deep learning differ in *what* they ask the model to learn.

---

## 1. Do you need labels? Yes — and here is exactly why

This is the most common confusion in this topic.

**For spam detection, labels are required.** Without them, the model has no way to know when it is wrong.

A label is simply the correct answer for each example:

| Email | Features | Label |
|-------|----------|-------|
| "Congratulations! Claim your prize now." | `[3, 1, 0, 0.20, 47]` | `1` (spam) |
| "Hi, your meeting is confirmed for 3pm." | `[0, 0, 1, 0.02, 82]` | `0` (not spam) |
| "Win a free iPhone — click here now!" | `[5, 4, 0, 0.40, 31]` | `1` (spam) |
| "Your invoice for March is attached." | `[0, 1, 1, 0.01, 110]` | `0` (not spam) |

In PyTorch, these labels become a tensor:

```python
labels = torch.tensor([[1.0], [0.0], [1.0], [0.0]])
```

The model predicts a probability for each email. The label tells the model what the probability *should have been*. The gap between the prediction and the label is the **loss** — and reducing the loss is the entire goal of training.

> **Memory trick:** Labels are the answer key. Without the answer key, the model cannot know if it got the question right.

### Why labels are required for classification

The training loop works like this:

```
1. Model predicts: email [3, 1, 0, 0.20, 47] → probability 0.30
2. Label says:     correct answer is 1.0 (spam)
3. Loss measures:  how far is 0.30 from 1.0?  → loss is large
4. Backprop finds: which weights caused the mistake?
5. Optimizer:      nudge those weights to reduce the loss
6. Repeat across all emails until loss is small
```

Without the label `1.0` in step 2, there is nothing to compare against. The loop cannot run.

### When labels are not required

Labels are only required for **supervised learning** — tasks where each example has a known correct answer.

Some tasks do not need labels:

| Learning type | Labels? | Example |
|---|---|---|
| Supervised (spam classifier) | **Yes** | Human labels each email spam / not spam |
| Unsupervised (clustering) | No | Group emails by similarity, no pre-defined answers |
| Self-supervised (language model pre-training) | No — labels come from the data itself | Predict the next word in an email |

Everything in this series — spam classification, PyTorch training loops, cross-entropy loss — is supervised learning. **Labels are required.**

---

## 2. What loss is and why it matters

The model's prediction is a probability between 0 and 1. The label is either 0 or 1. The **loss function** measures how wrong the prediction is.

For binary classification like spam detection, the standard loss function is **Binary Cross-Entropy (BCE)**:

```python
import torch.nn as nn

loss_fn = nn.BCELoss()

prediction = torch.tensor([[0.30]])   # model said 30% spam
label      = torch.tensor([[1.0]])    # correct answer: spam

loss = loss_fn(prediction, label)
print(loss.item())   # large number — prediction was very wrong
```

If the model predicts `0.95` for a spam email (label `1.0`), the loss is small. If it predicts `0.10` for a spam email, the loss is large. Training is just the process of repeatedly reducing this loss across thousands of emails.

> **Memory trick:** Loss is the score on a test. Training is studying to improve that score.

---

## 3. Traditional ML vs deep learning — the real difference

Part 1 showed you *how* a model computes. Now the question is: **what does the model actually learn to do?**

Both traditional ML and deep learning follow the same training loop:

```
Predict → measure loss against labels → update weights → repeat
```

The difference is in **what the model is asked to learn from**.

### Traditional machine learning — you design the features

In traditional ML, a human decides which features to extract from the raw email *before* feeding it to the model:

```
Raw email
    ↓
Human writes code to count suspicious words, links, capitals, etc.
    ↓
Model receives: [3, 1, 0, 0.20, 47]
    ↓
Model learns: 5 weights + 1 bias
    ↓
Spam probability
```

The model only learns **how much weight to give each human-chosen feature**. It does not discover new features. This is called **feature engineering** — the human does the hard thinking about what matters.

```python
from sklearn.linear_model import LogisticRegression

# Features chosen by a human
features = [
    [3, 1, 0, 0.20, 47],
    [0, 0, 1, 0.02, 82],
    [5, 4, 0, 0.40, 31],
    [0, 1, 1, 0.01, 110]
]
labels = [1, 0, 1, 0]   # ← labels required here too

model = LogisticRegression()
model.fit(features, labels)
```

### Deep learning — the model discovers its own features

In deep learning, you give the model raw or lightly processed input. The hidden layers learn their own internal representations:

```
Raw email
    ↓
Convert words to token IDs: [1842, 95, 721, 4031, ...]
    ↓
Embedding layer learns a vector per word
    ↓
Hidden layers learn combinations: "claim your prize" = strong spam signal
    ↓
Output layer produces spam probability
```

The model does not just learn weights for human-chosen features. It learns **what to look for in the first place**. This is called **feature learning**.

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Embedding(num_embeddings=10000, embedding_dim=32),  # learns word vectors
    nn.Linear(32, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
    nn.Sigmoid()
)
```

> **Memory trick:** Traditional ML is like giving a detective a checklist you wrote. Deep learning is like hiring a detective who writes their own checklist by studying thousands of cases.

---

## 4. Why Part 1's model is traditional ML — not deep learning

This is the exact confusion the article title creates.

Part 1 built this model:

```python
model = nn.Sequential(
    nn.Linear(5, 3),   # 5 hand-chosen features → 3 hidden values
    nn.ReLU(),
    nn.Linear(3, 1),
    nn.Sigmoid()
)
```

Even though this uses PyTorch and has a hidden layer, it is **traditional machine learning in deep learning clothing**. Why?

Because the five input features (`suspicious_words`, `links`, `known_sender`, `capitals`, `length`) were **chosen by a human**. The model only learns how to combine those five numbers — it does not discover what to look for in the raw email text.

| What the model receives | What the model learns | Type |
|---|---|---|
| Human-chosen features `[3, 1, 0, 0.20, 47]` | Weights for those features | Traditional ML |
| Raw token IDs `[1842, 95, 721, ...]` | What patterns in words predict spam | Deep Learning |

Adding hidden layers to a model that receives hand-crafted features makes it a **deeper traditional ML model**, not deep learning in the true sense. The power of deep learning comes from learning features, not from having more layers.

---

## 5. Why deep learning needs more data and compute

Because deep learning asks the model to discover features from scratch, it needs to see far more examples:

| Situation | Traditional ML | Deep Learning |
|---|---|---|
| 500 labelled emails | Works well | Likely overfit or underfit |
| 100,000 labelled emails | Possibly overkill | Starts to shine |
| 10,000,000 emails | Cannot improve much | Can learn subtle language patterns |
| Need to explain every decision | Good — weights are readable | Harder — patterns are buried in layers |
| Input is raw text, images, or audio | Requires manual feature design | Handles naturally |

The tradeoff is: deep learning requires **labelled data at scale** and **significantly more compute**, but it can learn things that no human would think to hand-code as a feature.

---

## 6. The complete picture — putting Part 1 and Part 2 together

Here is how the two parts connect:

| Concept | Where it lives |
|---|---|
| Neuron calculation (weights × inputs + bias) | Part 1 |
| Sigmoid turns score into probability | Part 1 |
| Hidden layers as structure | Part 1 |
| What weights and biases are stored | Part 1 |
| **What labels are and why they are required** | **Part 2** |
| **What loss is and how it drives training** | **Part 2** |
| **Feature engineering vs feature learning** | **Part 2** |
| **Why Part 1's model is traditional ML, not deep learning** | **Part 2** |
| **When to use traditional ML vs deep learning** | **Part 2** |

---

## 7. The training loop in full — with labels

Here is the complete supervised training loop using Part 1's five-feature model:

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Features: [suspicious_words, links, known_sender, capitals, length]
X = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0],
    [5.0, 4.0, 0.0, 0.40, 31.0],
    [0.0, 1.0, 1.0, 0.01, 110.0]
])

# Labels: 1 = spam, 0 = not spam  ← required
y = torch.tensor([[1.0], [0.0], [1.0], [0.0]])

dataset = TensorDataset(X, y)
loader  = DataLoader(dataset, batch_size=2, shuffle=True)

model     = nn.Sequential(nn.Linear(5, 4), nn.ReLU(), nn.Linear(4, 1), nn.Sigmoid())
loss_fn   = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    for batch_x, batch_y in loader:
        prediction = model(batch_x)
        loss = loss_fn(prediction, batch_y)   # compares prediction to label

        optimizer.zero_grad()
        loss.backward()    # finds which weights caused the error
        optimizer.step()   # nudges weights to reduce error
```

Every line that involves `batch_y` — `loss_fn(prediction, batch_y)` — is the point where labels are used. Remove `y` and the training loop breaks immediately.

---

## 8. Summary

- **Labels are required** for supervised learning. The model learns by comparing its predictions to labels and adjusting weights to reduce the error.
- **Loss** measures how wrong the model is. Training is the process of reducing loss over many labelled examples.
- **Traditional ML**: a human extracts features from raw data, then the model learns weights for those features.
- **Deep learning**: the model receives raw or lightly processed input and learns what features to look for by itself.
- **Part 1's model is traditional ML** because it receives hand-chosen features. The presence of hidden layers does not make it deep learning — the *source of the features* does.
- Deep learning needs significantly more labelled data and compute in exchange for not requiring manual feature design.

---

## 9. Try it yourself

```python
import torch
import torch.nn as nn

# Four emails: [suspicious_words, links, known_sender, capitals, length]
X = torch.tensor([
    [3.0, 1.0, 0.0, 0.20, 47.0],
    [0.0, 0.0, 1.0, 0.02, 82.0],
    [5.0, 4.0, 0.0, 0.40, 31.0],
    [1.0, 0.0, 1.0, 0.05, 120.0]
])

# Labels are required — 1 = spam, 0 = not spam
y = torch.tensor([[1.0], [0.0], [1.0], [0.0]])

model     = nn.Sequential(nn.Linear(5, 4), nn.ReLU(), nn.Linear(4, 1), nn.Sigmoid())
loss_fn   = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.05)

for epoch in range(300):
    pred = model(X)
    loss = loss_fn(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

with torch.no_grad():
    final = model(X)
    for i, prob in enumerate(final):
        label = "spam" if prob.item() >= 0.5 else "not spam"
        print(f"Email {i+1}: {prob.item():.3f} → {label}")
```

Try removing the `y` labels and see what breaks. Try replacing the five hand-chosen features with raw token counts — that is the first step toward true deep learning.

---

## Final mental model

```
Part 1 answered:  How does a neuron compute a prediction?
Part 2 answers:   How does a model learn — and what is it learning from?

Traditional ML:   Human extracts features  →  model learns weights for them
Deep Learning:    Model receives raw input  →  model learns what features matter

Both need labels. Both use loss. Both use gradient descent.
The difference is who decides what the model looks at.
```

