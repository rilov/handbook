---
layout: topic
title: "Deep Learning for Generative AI — Part 3: Attention-Based Encoder-Decoder Architecture"
category: Generative AI
order: 103
permalink: /topics/dl-genai-attention-encoder-decoder/
tags:
  - generative-ai
  - deep-learning
  - attention
  - encoder-decoder
  - seq2seq
  - bahdanau
  - beginners
  - friendly
summary: "A beginner-friendly guide to the attention mechanism — how it lets the decoder look back at every encoder word instead of relying on a single context vector."
---

# Deep Learning for Generative AI — Part 3: Attention-Based Encoder-Decoder Architecture

In Part 2 we saw the basic encoder-decoder model. Its biggest weakness is the **context vector bottleneck**: the entire input sentence is squeezed into one fixed-size vector. For long sentences, the decoder forgets what was said at the beginning.

**Attention** fixes this by letting the decoder look back at **all** encoder hidden states and focus on the most relevant ones at each step.

---

## 1. The bottleneck problem

Imagine you are translating a 50-word English paragraph into French. With the basic encoder-decoder, you must first read all 50 words, memorise everything in a single vector, and then start translating from memory.

For short sentences this works fine. For long ones, important details get lost — like trying to memorise a whole page before writing the translation.

```text
Short sentence  → context vector captures most information  ✓
Long sentence   → context vector loses early details        ✗
```

---

## 2. The attention idea: look back at every word

Instead of relying on one summary vector, the decoder can **peek back** at every encoder hidden state and decide which words are important right now.

### Analogy: reading while translating

A human translator does not memorise the whole paragraph first. They translate one phrase, then glance back at the source text to check what comes next. Attention does the same thing — it lets the decoder glance back at the entire input at every step.

---

## 3. How attention works — step by step

At each decoder step, attention answers: **"Which input words should I pay attention to right now?"**

### Setup

The encoder produces a hidden state for every input word:

```text
Input: "I love cats"

Encoder hidden states:
  h1 (for "I")
  h2 (for "love")
  h3 (for "cats")
```

The decoder is about to generate the next output word. Its current hidden state is `s_t`.

### Step 1: Compute alignment scores

Compare the decoder state `s_t` with each encoder hidden state:

```text
score(s_t, h1) = how relevant is "I" right now?       → e.g. 0.3
score(s_t, h2) = how relevant is "love" right now?     → e.g. 2.1
score(s_t, h3) = how relevant is "cats" right now?     → e.g. 4.5
```

Higher score = more relevant. The score function can be a dot product, a small neural network, or other methods (more on this in Part 4).

### Step 2: Turn scores into weights with softmax

```text
weights = softmax([0.3, 2.1, 4.5])
       = [0.01, 0.11, 0.88]
```

The weights add up to 1. In this example, the decoder is paying 88% attention to "cats."

### Step 3: Compute the context vector (weighted sum)

```text
context = 0.01 × h1 + 0.11 × h2 + 0.88 × h3
```

This **attention context vector** is a blend of all encoder states, weighted by relevance. Unlike the basic model's fixed context vector, this one **changes at every decoder step**.

### Step 4: Use the context vector to predict

The decoder combines the attention context with its own hidden state to predict the next word:

```text
output = f(s_t, context)  →  "chats"
```

---

## 4. A full translation example with attention

Translating "I love cats" → "J'aime les chats":

```text
Decoder step 1: generate "J'"
  - Attention weights: I=0.60, love=0.25, cats=0.15
  - The decoder focuses on "I" because it's generating the subject

Decoder step 2: generate "aime"
  - Attention weights: I=0.10, love=0.80, cats=0.10
  - The decoder focuses on "love" because it's generating the verb

Decoder step 3: generate "les"
  - Attention weights: I=0.05, love=0.05, cats=0.90
  - The decoder focuses on "cats" because it's generating the article for the object

Decoder step 4: generate "chats"
  - Attention weights: I=0.02, love=0.08, cats=0.90
  - Still focused on "cats" — generating the noun itself
```

The attention weights shift naturally as the decoder moves through the output.

---

## 5. Visualising attention

You can plot the attention weights as a heatmap:

```text
              Encoder words
              I     love   cats
Decoder  J'   ██░░  ░░░░  ░░░░    (focuses on "I")
words    aime ░░░░  ██░░  ░░░░    (focuses on "love")
         les  ░░░░  ░░░░  ██░░    (focuses on "cats")
         chats░░░░  ░░░░  ██░░    (focuses on "cats")
```

The dark squares show where the decoder is looking. For well-trained models, the pattern roughly follows the diagonal — each output word aligns with one or two input words.

---

## 6. Comparing basic vs attention encoder-decoder

| Feature | Basic encoder-decoder | With attention |
|---|---|---|
| Context vector | One fixed vector for the whole input | A different weighted vector at every step |
| Long sentences | Loses information | Handles them well |
| Interpretability | Black box | Attention weights show what the model focuses on |
| Speed | Slightly faster | Slightly slower (computes weights at each step) |
| Translation quality | Good for short sentences | Much better for long sentences |

---

## 7. Types of attention (preview)

There are several ways to compute the alignment score in Step 1. The most common:

| Name | Formula | Introduced by |
|------|---------|---------------|
| **Dot product** | `score = s_t · h_i` | Luong (2015) |
| **Scaled dot product** | `score = (s_t · h_i) / √d` | Vaswani (2017) |
| **Additive (concat)** | `score = v · tanh(W₁·s_t + W₂·h_i)` | Bahdanau (2014) |
| **General** | `score = s_t · W · h_i` | Luong (2015) |

Part 4 dives into the math behind these.

---

## 8. PyTorch sketch: additive attention

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.W1 = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W2 = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.v = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, decoder_state, encoder_outputs):
        # decoder_state:  (batch, 1, hidden)
        # encoder_outputs: (batch, src_len, hidden)

        score = self.v(
            torch.tanh(self.W1(decoder_state) + self.W2(encoder_outputs))
        )  # (batch, src_len, 1)

        weights = F.softmax(score, dim=1)         # (batch, src_len, 1)
        context = (weights * encoder_outputs).sum(dim=1, keepdim=True)
        return context, weights
```

This is the **Bahdanau (additive) attention**. The decoder calls this module at every step to get a fresh context vector.

---

## 9. Summary

- The basic encoder-decoder squeezes the whole input into **one vector** — a bottleneck.
- **Attention** lets the decoder look at **all** encoder hidden states and focus on the most relevant ones at each step.
- Attention computes **alignment scores**, turns them into **weights** with softmax, and creates a **weighted context vector**.
- The context vector changes at every decoder step, so the model can handle long sentences without losing information.
- Attention weights can be visualised as a heatmap, making the model more interpretable.
- There are several score functions (dot product, additive, general) — the next part covers the math.

**Next:** [Part 4: Math Behind Attention Mechanism]({{ site.baseurl }}/topics/dl-genai-attention-math/)
