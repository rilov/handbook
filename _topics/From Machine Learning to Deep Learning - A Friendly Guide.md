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
summary: The direct continuation of Part 1. Part 1 built the spam model with handcoded weights. Part 2 answers the natural next question — how does a model actually learn those weights? Covers labels, loss, backpropagation, and the complete training loop using the same spam example.
---

# Part 2: From Machine Learning to Deep Learning — A Friendly Guide

In Part 1 we built this model:

```python
model = nn.Sequential(
    nn.Linear(5, 3),
    nn.ReLU(),
    nn.Linear(3, 1),
    nn.Sigmoid()
)
```

And we used **handcoded weights** like `[0.8, 0.6, -1.2, 2.0, 0.01]` to show how the calculation works.

But that raises the obvious question:

> **In a real model, nobody writes those numbers by hand. So where do the weights actually come from?**

Part 2 answers that. We will take the exact same spam model from Part 1 and **train it** — starting from random weights and teaching it to improve by looking at labelled examples.

---

## 1. Step 1 — Give the model labelled examples

In Part 1, the model received one email and predicted a probability. But it could not learn anything because we never told it whether its prediction was right or wrong.

To train a model, every email needs a **label** — the correct answer:

| Email | Features | Label |
|-------|----------|-------|
| "Congratulations! Claim your prize now." | `[3, 1, 0, 0.20, 47]` | `1` — spam |
| "Hi, your meeting is confirmed for 3pm." | `[0, 0, 1, 0.02, 82]` | `0` — not spam |
| "Win a free iPhone — click here now!" | `[5, 4, 0, 0.40, 31]` | `1` — spam |
| "Your invoice for March is attached." | `[0, 1, 1, 0.01, 110]` | `0` — not spam |

`1` means spam. `0` means not spam. These are called **labels**, and a human assigns them by reading each email and deciding.

In PyTorch, the features and labels become two tensors:

```python
import torch

# Features: [suspicious_words, links, known_sender, capitals, length]
X = torch.tensor([
    [3.0, 1.0, 0.0, 0.20,  47.0],
    [0.0, 0.0, 1.0, 0.02,  82.0],
    [5.0, 4.0, 0.0, 0.40,  31.0],
    [0.0, 1.0, 1.0, 0.01, 110.0]
])

# Labels: 1 = spam, 0 = not spam
y = torch.tensor([[1.0], [0.0], [1.0], [0.0]])
```

The model will process `X` and try to produce predictions that match `y`.

> **Memory trick:** Labels are the answer key. Without the answer key, the model cannot know if it got a question right or wrong.

---

## 2. Step 2 — Start with random weights

In Part 1 we wrote the weights by hand. In a real model, PyTorch assigns **random weights** at the start:

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(5, 4),   # same structure as Part 1
    nn.ReLU(),
    nn.Linear(4, 1),
    nn.Sigmoid()
)

# Predict before any training — weights are random
with torch.no_grad():
    raw_predictions = model(X)
    print(raw_predictions)
# Output: something like [[0.47], [0.51], [0.49], [0.52]] — basically guessing
```

The model starts knowing nothing. All four emails get roughly 50% spam probability — essentially a coin flip. Training is the process of improving those weights until predictions match the labels.

---

## 3. Step 3 — Measure the mistake with a loss function

After the model predicts, we need a way to measure how wrong it was. That measure is called the **loss**.

For spam detection (binary classification), the standard loss is **Binary Cross-Entropy (BCE)**:

```python
loss_fn = nn.BCELoss()
```

It compares each prediction to its label:

```python
prediction = torch.tensor([[0.47]])   # model said 47% spam
label      = torch.tensor([[1.0]])    # correct answer: this IS spam

loss = loss_fn(prediction, label)
print(loss.item())   # ~0.75 — prediction was quite wrong
```

| Prediction | Label | Loss |
|---|---|---|
| `0.95` | `1.0` (spam) | small — almost correct |
| `0.47` | `1.0` (spam) | large — quite wrong |
| `0.05` | `0.0` (not spam) | small — almost correct |
| `0.60` | `0.0` (not spam) | large — quite wrong |

The higher the loss, the more the model needs to change. Training is just the process of driving this number down.

> **Memory trick:** Loss is the score on a test. Training is studying to improve that score.

---

## 4. Step 4 — Backpropagation finds which weights caused the mistake

The model has many weights spread across two layers. After computing the loss, we need to know: **which weights were most responsible for the mistake?**

This is what **backpropagation** does. It works backwards through the model, calculating how much each weight contributed to the error. PyTorch does this automatically with one line:

```python
loss.backward()
```

After this call, every weight in the model has a **gradient** — a number that says "increase this weight to reduce the loss" or "decrease this weight to reduce the loss."

You do not need to write backpropagation yourself. PyTorch computes it automatically because it has been tracking every calculation since the input arrived.

> **Memory trick:** Backpropagation is like tracing a domino chain backwards — you look at which domino caused the final one to fall.

---

## 5. Step 5 — The optimizer adjusts the weights

Now that we know which direction to move each weight, the **optimizer** makes the actual adjustment:

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
optimizer.step()
```

`lr=0.01` is the **learning rate** — how large a step to take. A large learning rate changes weights aggressively and can overshoot. A small learning rate changes them cautiously and can be slow. `0.01` is a common starting point.

After `optimizer.step()`, every weight has been nudged slightly in the direction that reduces the loss. The model is now marginally better at distinguishing spam from normal email.

---

## 6. Step 6 — Repeat across many emails and many epochs

One pass through the training data is called an **epoch**. We repeat the loop many times until the loss stops decreasing:

```python
for epoch in range(200):
    prediction = model(X)               # forward pass
    loss = loss_fn(prediction, y)       # how wrong?

    optimizer.zero_grad()               # clear previous gradients
    loss.backward()                     # backprop: who caused the mistake?
    optimizer.step()                    # update weights

    if epoch % 50 == 0:
        print(f"Epoch {epoch}  loss: {loss.item():.4f}")
```

`optimizer.zero_grad()` clears the gradients before each pass — if you skip it, PyTorch accumulates gradients from previous steps, which gives wrong results.

After 200 epochs you will see the loss decreasing:

```
Epoch 0    loss: 0.7431
Epoch 50   loss: 0.4812
Epoch 100  loss: 0.2903
Epoch 150  loss: 0.1644
Epoch 200  loss: 0.0951
```

---

## 7. The complete training loop

Putting all six steps together:

```python
import torch
import torch.nn as nn

# Step 1 — labelled data
X = torch.tensor([
    [3.0, 1.0, 0.0, 0.20,  47.0],
    [0.0, 0.0, 1.0, 0.02,  82.0],
    [5.0, 4.0, 0.0, 0.40,  31.0],
    [0.0, 1.0, 1.0, 0.01, 110.0]
])
y = torch.tensor([[1.0], [0.0], [1.0], [0.0]])

# Step 2 — model with random weights
model     = nn.Sequential(nn.Linear(5, 4), nn.ReLU(), nn.Linear(4, 1), nn.Sigmoid())
loss_fn   = nn.BCELoss()                       # Step 3 — loss function
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)  # Step 5 — optimizer

# Steps 4, 5, 6 — train
for epoch in range(300):
    prediction = model(X)
    loss = loss_fn(prediction, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Check the result
with torch.no_grad():
    final = model(X)
    for i, prob in enumerate(final):
        result = "spam" if prob.item() >= 0.5 else "not spam"
        print(f"Email {i+1}: {prob.item():.3f}  →  {result}")
```

Expected output:

```
Email 1: 0.923  →  spam
Email 2: 0.071  →  not spam
Email 3: 0.981  →  spam
Email 4: 0.064  →  not spam
```

The model learned — starting from random weights — to correctly classify all four emails.

---

## 8. What "from machine learning to deep learning" actually means

Both traditional machine learning (like logistic regression) and deep learning follow the exact same training loop above:

```
predict → measure loss → backprop → update weights → repeat
```

The difference is not the training loop. The difference is **what you give the model as input**:

| | What goes into the model | What the model learns |
|---|---|---|
| **Traditional ML** | Features you extracted: `[3, 1, 0, 0.20, 47]` | Weights for those 5 features |
| **Deep learning** | Raw text tokens: `[1842, 95, 721, 4031, ...]` | Which words and phrases signal spam |

In our tutorial, we have been giving the model **hand-crafted features** (suspicious word count, link count, etc.). That is traditional ML, even though we are using PyTorch.

Deep learning starts when you remove the human feature extraction step and feed the raw email text directly. The model then needs to learn what to look for from scratch — which requires far more data and compute, but can discover patterns a human would never think to hand-code.

The rest of this series builds toward that. Part 3 covers tensors in more depth, Part 4 covers data loading at scale, and from there we progress to real text and image models.

---

## 9. Summary

| Step | What happens | PyTorch |
|---|---|---|
| 1 | Provide features + labels | `X`, `y` tensors |
| 2 | Model starts with random weights | `nn.Sequential(...)` |
| 3 | Predict and measure loss | `loss_fn(prediction, y)` |
| 4 | Backprop finds responsible weights | `loss.backward()` |
| 5 | Optimizer adjusts weights | `optimizer.step()` |
| 6 | Repeat until loss is low | `for epoch in range(...)` |

- Labels are the correct answers — required for the loss calculation to work.
- Loss measures how wrong the model is. Lower is better.
- Backpropagation traces the error back through the model to find which weights to adjust.
- The optimizer makes the actual weight update, one small step at a time.
- Traditional ML and deep learning use the same loop — the difference is whether a human or the model decides what features to look at.

---

## 10. Try it yourself

Run the complete training loop above. Then experiment:

1. Change `lr=0.01` to `lr=0.5` — does the model learn faster or does loss jump around?
2. Change `range(300)` to `range(10)` — how accurate are the predictions after just 10 epochs?
3. Add a fifth email `[2.0, 0.0, 0.0, 0.15, 60.0]` with label `1.0` — does the model classify it correctly after training?

---

## Final mental model

```
Part 1:  email → features → neuron calculates → probability
                                                    ↑
                                         weights were handcoded

Part 2:  Same model, but now with labelled data the model learns those weights itself:

         random weights
              ↓
         predict → loss → backprop → optimizer → better weights
              ↑___________________________________________|
                         repeat until loss is low
```

