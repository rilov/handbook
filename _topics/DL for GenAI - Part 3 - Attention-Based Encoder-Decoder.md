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

## 1. Quick recap of Part 2 — and the problem we left with

In Part 2 we built this pipeline. The encoder reads the sentence one word at a time, producing a hidden state after each word:

```text
"I"    → h1   (understanding after "I")
"love" → h2   (understanding after "I love")
"cats" → h3   (understanding after "I love cats")
```

Then we did something wasteful: we **kept only h3** (calling it the context vector) and **threw away h1 and h2**. The decoder had to generate the entire French sentence from that single vector.

```text
Basic encoder-decoder:

  h1 → thrown away  ✗
  h2 → thrown away  ✗
  h3 → the only thing the decoder gets
```

Remember the paint-mixing analogy from Part 2: by the end, all the words are blended into one colour, and you cannot recover the individual words. For a 3-word sentence this is fine. For a 50-word sentence, the early words fade away — like trying to memorise a whole page before writing the translation.

```text
Short sentence  → context vector captures most information  ✓
Long sentence   → context vector loses early details        ✗
```

---

## 2. The attention idea: stop throwing away h1 and h2

Here is the key insight, and it is surprisingly simple:

> The encoder **already produced** a hidden state for every word — h1, h2, h3. Instead of keeping only the last one, **keep them all** and let the decoder look at any of them whenever it wants.

```text
With attention:

  h1 (for "I")    → kept  ✓
  h2 (for "love") → kept  ✓     the decoder can look at
  h3 (for "cats") → kept  ✓     any of these, at any step
```

### But which one should the decoder look at?

That depends on **what the decoder is doing right now**. Think about translating "I love cats" → "J'aime les chats":

- When generating **"J'"** (= "I"), the decoder should look mostly at **h1** ("I")
- When generating **"aime"** (= "love"), it should look mostly at **h2** ("love")
- When generating **"chats"** (= "cats"), it should look mostly at **h3** ("cats")

So the decoder needs a way to decide, at every step, **how much to look at each encoder hidden state**. That deciding mechanism is what we call **attention**. That's all attention is: a scoring system for "which input words matter to me right now?"

### Analogy: reading while translating

A human translator does not memorise the whole paragraph first and then write blind. They translate one phrase, then **glance back at the source text** to check what comes next. Attention gives the decoder that same ability — to glance back at the entire input at every step, focusing on the relevant part.

---

## 3. How attention works — step by step

At each decoder step, attention answers one question: **"Which input words should I pay attention to right now?"** It does this in 4 steps. Let's walk through them slowly, with real numbers.

### Setup: what we have to work with

Two ingredients, both of which you already know from Part 2:

1. **The encoder hidden states** — one per input word (we keep all of them now):

```text
Input: "I love cats"

  h1 = [0.31, -0.12]    (encoder's understanding at "I")
  h2 = [0.68,  0.24]    (encoder's understanding at "I love")
  h3 = [0.52,  0.71]    (encoder's understanding at "I love cats")

(2 numbers each to keep the math small — real models use 256–512)
```

2. **The decoder's current hidden state** `s_t` — the decoder's own memory of what it has generated so far. Say the decoder has just generated "J'aime les" and is about to generate the next word:

```text
  s_t = [0.45, 0.80]    (decoder's memory: "I've said J'aime les,
                          next I need the object noun")
```

### Step 1: Score each encoder state — "how relevant are you to me right now?"

The decoder compares its own state `s_t` with **each** encoder hidden state. The simplest comparison is the **dot product** (multiply matching positions, add up) — the same similarity idea as cosine similarity in Part 1:

```text
score(s_t, h1) = 0.45 × 0.31 + 0.80 × (-0.12) = 0.14 - 0.10 = 0.04   ("I" — not relevant)
score(s_t, h2) = 0.45 × 0.68 + 0.80 × 0.24    = 0.31 + 0.19 = 0.50   ("love" — a little)
score(s_t, h3) = 0.45 × 0.52 + 0.80 × 0.71    = 0.23 + 0.57 = 0.80   ("cats" — very relevant!)
```

Higher score = more relevant. Intuitively: the decoder needs an object noun next, and h3 ("cats") points in the most similar direction to what it is looking for.

(The score can also be computed by a small neural network instead of a dot product — Part 4 covers the variations. The idea is the same.)

### Step 2: Turn scores into percentages with softmax

The raw scores `[0.04, 0.50, 0.80]` are useful, but we want them as clean **percentages that add up to 1**. That is exactly what softmax does (same softmax as the decoder's word prediction in Part 2):

```text
weights = softmax([0.04, 0.50, 0.80]) = [0.21, 0.33, 0.46]

Meaning:  pay 21% attention to "I"
          pay 33% attention to "love"
          pay 46% attention to "cats"   ← the winner
```

These percentages are called **attention weights**.

### Step 3: Build a custom context vector — a weighted blend

Now mix the encoder states together **according to the attention weights**. Each h is multiplied by its percentage, then everything is added up:

```text
context = 0.21 × h1           + 0.33 × h2           + 0.46 × h3
        = 0.21 × [0.31,-0.12] + 0.33 × [0.68, 0.24] + 0.46 × [0.52, 0.71]
        = [0.07, -0.03]       + [0.22, 0.08]        + [0.24, 0.33]
        = [0.53, 0.38]
```

This is the **attention context vector**. It is mostly made of h3 ("cats") because that got the biggest weight — but it still carries a little of the other words.

**The crucial difference from Part 2:** in the basic model, the context vector was computed **once** and never changed. Here, a **fresh context vector is built at every decoder step**, custom-blended for whatever the decoder needs right now.

### Step 4: Use it to predict the next word

The decoder combines this custom context vector with its own hidden state and predicts the next word through softmax (exactly like in Part 2):

```text
combine(s_t = [0.45, 0.80],  context = [0.53, 0.38])  →  softmax  →  "chats"
```

Then the decoder moves to the next step, its hidden state updates, and the whole attention process (steps 1–4) **runs again from scratch** — producing new scores, new weights, and a new context vector.

### The 4 steps in one picture

```text
                 h1        h2        h3        (all encoder states, kept)
                  │         │         │
Step 1 (score):  0.04      0.50      0.80      "how relevant is each to me now?"
                  │         │         │
Step 2 (softmax): 21%       33%       46%      turn into percentages
                  │         │         │
Step 3 (blend):   └────────┼────────┘
                            ↓
                  context = [0.53, 0.38]       custom blend for this step
                            ↓
Step 4 (predict): decoder + context → "chats"
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
