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
summary: Learn what changes when you move from traditional machine learning to deep learning, using the same spam-detection example throughout. Covers feature engineering, feature learning, hidden layers, and why non-linearity matters.
---

# Part 2: From Machine Learning to Deep Learning — A Friendly Guide

Let us continue with the spam email example. We already saw that a single neuron can take five numbers and produce a spam probability. Now we will ask: what changes if we switch from traditional machine learning to deep learning?

---

## 1. The same problem, two different approaches

Imagine you work at an email company and you must build a spam detector.

In **traditional machine learning**, a human might decide which features matter:

| Feature | How to get it |
|---------|---------------|
| Number of suspicious words | Count words like “free”, “win”, “prize” |
| Number of links | Count `http://` or `<a>` tags |
| Sender known or unknown | Check against an address book |
| Percentage of capital letters | Count uppercase letters ÷ total letters |
| Message length | Count words |

You then feed these features into a model like logistic regression or a decision tree. The model learns weights, but the features themselves are designed by a person. This is called **feature engineering**.

In **deep learning**, you might give the model raw text instead:

> “Congratulations! Click here to claim your prize.”

The model learns which words, phrases, and patterns matter. It might discover that “claim your prize” is a strong spam signal without anyone telling it explicitly. This is called **feature learning**.

> **Memory trick:** In traditional ML, you hand-pick the clues. In deep learning, the detective learns which clues to look for.

---

## 2. What stays the same

Both approaches share the same high-level goal:

> **Feed data into a model, measure the error, and update the model to reduce the error.**

| Step | Traditional ML | Deep Learning |
|------|----------------|---------------|
| Input | Features designed by humans | Raw or lightly processed data |
| Model | Logistic regression, SVM, decision tree | Neural network |
| Loss function | Cross-entropy, MSE | Cross-entropy, MSE |
| Optimisation | Gradient descent or similar | Gradient descent / Adam |
| Goal | Generalise to unseen emails | Same |

The difference is not the goal. The difference is **who decides what the model looks at**.

---

## 3. A single neuron is just traditional ML

Recall our simple spam model:

```python
email = torch.tensor([3.0, 1.0, 0.0, 0.20, 47.0])
weights = torch.tensor([0.8, 0.6, -1.2, 2.0, 0.01])
bias = torch.tensor(-1.0)

raw_score = email @ weights + bias
probability = torch.sigmoid(raw_score)
```

This is almost the same as **logistic regression**:

- Multiply each feature by a weight.
- Add them up.
- Add a bias.
- Squash with sigmoid to get a probability.

So a single neuron with five hand-chosen features is a traditional machine-learning model wearing a neural-network costume. It is useful, but it cannot learn new combinations of features.

---

## 4. Why a single neuron is limited

A single neuron can only learn patterns that look like a straight line in feature space. For example, it can learn:

> If `(0.8 × suspicious_words) + (0.6 × links) + ... + bias` is large enough, it is spam.

But it cannot easily learn combinations such as:

> “An email is spam only if it has many links AND an unknown sender, OR if it has many suspicious words AND many capitals.”

Those combinations are not simple straight-line rules. They need a way to mix features together before making the final decision.

---

## 5. Hidden layers add combinations

A hidden layer is a group of neurons between the input and the output. Each hidden neuron looks at the same five features but learns a different combination.

For spam detection, one hidden neuron might learn:

```
neuron_1 = links × 0.7 + unknown_sender × 1.5 + bias
```

This neuron fires when an email has many links and an unknown sender.

Another hidden neuron might learn:

```
neuron_2 = suspicious_words × 1.1 + capitals × 0.9 + bias
```

This neuron fires when an email has many suspicious words and many capital letters.

The output neuron then combines these hidden neurons:

```
spam_score = neuron_1 × 0.8 + neuron_2 × 0.6 + bias
```

So the model can now say: “This email is spam because it triggered both the suspicious-words neuron and the unknown-sender neuron.”

> **Memory trick:** A single neuron is like one judge. A hidden layer is like a panel of judges, each scoring a different aspect, before the final decision.

---

## 6. Why depth matters

Each hidden layer builds on the previous one. With spam text, this might look like:

| Layer | What it learns |
|-------|----------------|
| Input | Raw words or hand features |
| Hidden layer 1 | Word combinations like “claim your” or “free prize” |
| Hidden layer 2 | Phrase patterns like “click here to claim” |
| Output | Spam probability |

Early layers see simple patterns. Deeper layers see richer patterns. This is why deep networks are powerful for text, images, and audio.

> **Memory trick:** Deep learning is like reading a book. First you recognise letters, then words, then sentences, then meaning.

---

## 7. The role of non-linearity

Without activation functions, a deep network would just be a long chain of multiplications and additions. In fact, it would collapse into one single multiplication and addition.

Here is why:

```
Layer 1: z = xW₁ + b₁
Layer 2: z = zW₂ + b₂ = (xW₁ + b₁)W₂ + b₂ = x(W₁W₂) + (b₁W₂ + b₂)
```

If there is no activation between the layers, the two layers are mathematically the same as one layer. The activation function breaks the linearity.

ReLU, for example, simply turns negative values to zero:

```python
ReLU([2.4, -0.7, 1.3]) = [2.4, 0.0, 1.3]
```

This small change is what allows the network to learn complex shapes and combinations. It is like adding a small switch between layers.

> **Memory trick:** Activation functions are the wrinkles that stop the network from being a flat piece of paper.

---

## 8. Common activation functions in detail

| Function | What it does | Where it is used | Memory trick |
|----------|--------------|------------------|--------------|
| **Sigmoid** | Squishes any number to 0..1 | Output layer for binary classification | Thermometer with a 0-to-1 scale |
| **Tanh** | Squishes any number to -1..1 | Older hidden layers | Sigmoid stretched to -1..1 |
| **ReLU** | Turns negatives to zero | Most modern hidden layers | Bouncer that blocks negatives |
| **Leaky ReLU** | Lets a small negative through | ReLU replacement | Slightly open door for negatives |
| **Softmax** | Turns scores into probabilities that sum to 1 | Output layer for multi-class classification | Normalised ranking |

For spam detection, the final output is one probability, so sigmoid is the right choice. The hidden layers use ReLU because it is fast and avoids the vanishing gradient problem.

---

## 9. Feature engineering vs feature learning for spam

### Traditional ML spam detector

```
Raw email
    ↓
Human writes rules to extract 5 features
    ↓
Logistic regression learns 5 weights + bias
    ↓
Spam probability
```

```python
from sklearn.linear_model import LogisticRegression

# Features designed by a human
features = [
    [3, 1, 0, 0.20, 47],
    [0, 0, 1, 0.02, 82],
    [5, 4, 0, 0.40, 31]
]
labels = [1, 0, 1]

model = LogisticRegression()
model.fit(features, labels)
```

### Deep learning spam detector

```
Raw email
    ↓
Convert words to token IDs
    ↓
Embedding layer learns vectors
    ↓
Hidden layers learn word and phrase patterns
    ↓
Output layer produces spam probability
```

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Embedding(num_embeddings=10000, embedding_dim=32),
    nn.Linear(32, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
    nn.Sigmoid()
)
```

In this simple example, the embedding layer learns a vector for each word. The hidden layers learn to combine those vectors into a spam score.

> **Memory trick:** Traditional ML is a recipe with ingredients you choose. Deep learning is a kitchen that discovers its own ingredients.

---

## 10. When to use which approach for spam

| Situation | Use Traditional ML | Use Deep Learning |
|-----------|-------------------|-------------------|
| Small dataset of 1,000 emails | Yes | No — not enough data |
| Dataset has clear, measurable features | Yes | Maybe overkill |
| Need to explain why an email was flagged | Yes | Harder |
| Dataset has 1,000,000 emails | No | Yes |
| Need to understand subtle language | No | Yes |
| Need to handle many languages and typos | No | Yes |

---

## 11. A deep learning spam model with hand features

Even if we keep the same five hand features, adding a hidden layer can improve the model because it learns combinations.

```python
import torch
import torch.nn as nn

# One email: suspicious_words, links, known_sender, capitals, length
email = torch.tensor([[3.0, 1.0, 0.0, 0.20, 47.0]])

model = nn.Sequential(
    nn.Linear(5, 4),   # 5 features → 4 hidden combinations
    nn.ReLU(),          # remove negative hidden signals
    nn.Linear(4, 1),    # 4 hidden combinations → 1 spam score
    nn.Sigmoid()        # spam score → probability
)

probability = model(email)
print("Spam probability:", probability.item())
```

The first layer creates four hidden combinations. ReLU removes the negative ones. The second layer combines the remaining positive signals into a final score. Sigmoid turns that score into a probability.

---

## 12. What the hidden neurons might learn

We do not get to read the neurons' minds, but we can imagine what they might represent:

| Hidden neuron | Might learn |
|---------------|-------------|
| 1 | High links + unknown sender = suspicious |
| 2 | High capitals + suspicious words = suspicious |
| 3 | Known sender + long message = normal |
| 4 | Short message + no links = normal |

These are not programmed. They emerge during training as the network tries to reduce its mistakes.

---

## 13. The training loop is the same in both worlds

Whether you use traditional ML or deep learning, the training process is similar:

```
1. Forward pass:   predict spam probability for each email
2. Compute loss:    how far is the prediction from the true label?
3. Backward pass:   find which weights caused the mistake
4. Update weights:  move a small step in the direction that reduces loss
5. Repeat
```

The only difference is that deep learning has more weights to update, including weights inside the hidden layers.

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(5, 4),
    nn.ReLU(),
    nn.Linear(4, 1),
    nn.Sigmoid()
)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training loop
for batch_x, batch_y in train_loader:
    prediction = model(batch_x)
    loss = criterion(prediction, batch_y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

---

## 14. From shallow to deep

| Network | Hidden layers | What it can learn |
|---------|---------------|-------------------|
| **No hidden layer** | 0 | Linear spam rule (like logistic regression) |
| **Shallow network** | 1 | Simple feature combinations |
| **Deep network** | 3 or more | Rich patterns in text, images, or audio |

Most modern spam filters use deep learning because spam evolves. Spammers change wording, use images, and add noise. A deep model can adapt to new patterns if it is retrained on fresh data.

---

## 15. Summary

- Traditional ML asks a human to design features. Deep learning asks the network to learn features.
- A single neuron with hand features is basically logistic regression.
- Hidden layers let the model learn combinations of features, such as “many links + unknown sender.”
- Activation functions like ReLU add non-linearity, which is why deep networks can learn complex patterns.
- Deep learning needs more data and compute, but it can handle raw text, images, and audio better than traditional ML.
- For spam detection, deep learning shines when the dataset is large and the language is subtle.

---

## 16. Try it yourself

```python
import torch
import torch.nn as nn

# Two simple hand-crafted features for four emails
emails = torch.tensor([
    [3.0, 1.0],   # 3 suspicious words, 1 link
    [0.0, 0.0],   # clean email
    [5.0, 4.0],   # very spammy
    [1.0, 0.0]    # slightly suspicious
])

labels = torch.tensor([[1.0], [0.0], [1.0], [0.0]])

# Build a model with one hidden layer
model = nn.Sequential(
    nn.Linear(2, 3),
    nn.ReLU(),
    nn.Linear(3, 1),
    nn.Sigmoid()
)

loss_fn = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

# Train for a few epochs
for epoch in range(200):
    pred = model(emails)
    loss = loss_fn(pred, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Check predictions
with torch.no_grad():
    final = model(emails)
    for i, prob in enumerate(final):
        label = "spam" if prob.item() >= 0.5 else "not spam"
        print(f"Email {i}: probability {prob.item():.3f} → {label}")
```

---

## Final mental model

```
Traditional ML:   Email → human features → simple model → spam probability
Deep learning:    Email → raw tokens → learned embeddings → hidden layers → spam probability
```

The real shift is from **hand-written features** to **learned representations**. Everything else — loss, optimisation, and evaluation — stays largely the same.

<img src="{{ site.baseurl }}/assets/img/NeuralNetwork.png" alt="A neural network showing how input features pass through hidden layers to an output probability" width="60%" />
