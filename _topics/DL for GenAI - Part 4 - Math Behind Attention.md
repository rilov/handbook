---
layout: topic
title: "Deep Learning for Generative AI — Part 4: Math Behind Attention Mechanism"
category: Generative AI
order: 104
permalink: /topics/dl-genai-attention-math/
tags:
  - generative-ai
  - deep-learning
  - attention
  - scaled-dot-product
  - softmax
  - query-key-value
  - beginners
  - friendly
summary: "A beginner-friendly walkthrough of the math behind attention — dot products, scaling, softmax, and the Query-Key-Value framework, with worked numerical examples."
---

# Deep Learning for Generative AI — Part 4: Math Behind Attention Mechanism

Part 3 showed the intuition: the decoder looks back at all encoder states and focuses on the most relevant ones. This part shows the **math** that makes it work — step by step, with real numbers.

> **Where this fits:** this is the math of **attention v1** — the decoder of an RNN encoder-decoder attending to encoder states (Bahdanau/Luong style). The Transformer's **self-attention** reuses the same ingredients (dot products, scaling, softmax, Q/K/V) but applies them differently — that version is covered in [Part 9]({{ site.baseurl }}/topics/dl-genai-self-attention-math/). Learn the ingredients here once, and Part 9 becomes easy.

---

## 1. The three players: Query, Key, Value

Attention can be described with three simple concepts:

| Role | What it is | Analogy |
|------|-----------|---------|
| **Query (Q)** | What the decoder is looking for right now | A search query you type into Google |
| **Key (K)** | A label for each encoder state | The title of each web page |
| **Value (V)** | The actual content of each encoder state | The content of each web page |

The decoder sends a **query**. It compares the query against every **key** to get a relevance score. Then it uses those scores to take a weighted sum of the **values**.

```text
1. Compare Q with every K  →  scores
2. Softmax(scores)          →  weights (add up to 1)
3. Weighted sum of V        →  context vector
```

---

## 2. Where do Q, K, V come from?

In a typical encoder-decoder with attention:

```text
Q = decoder hidden state (what am I looking for?)
K = encoder hidden states (what does each input word represent?)
V = encoder hidden states (same as K in basic attention)
```

In the Transformer (which we will see later), Q, K, and V are created by multiplying the input by three different weight matrices.

---

## 3. Dot-product attention — the simplest version

The score between a query and a key is their **dot product**:

```text
score(Q, K_i) = Q · K_i = sum of element-wise products
```

### Worked example

Suppose the decoder state (query) and three encoder states (keys) are 4-dimensional vectors:

```text
Q  = [1, 0, 1, 0]

K1 = [1, 1, 0, 0]   (encoder state for "I")
K2 = [0, 1, 1, 0]   (encoder state for "love")
K3 = [1, 0, 1, 1]   (encoder state for "cats")
```

Compute the dot products:

```text
score(Q, K1) = 1×1 + 0×1 + 1×0 + 0×0 = 1
score(Q, K2) = 1×0 + 0×1 + 1×1 + 0×0 = 1
score(Q, K3) = 1×1 + 0×0 + 1×1 + 0×1 = 2
```

The query is most similar to K3 ("cats") because their dot product is highest.

---

## 4. Why we scale: the √d trick

When vectors are long (e.g. 512 dimensions), dot products become very large numbers. Large inputs to softmax push the output toward 0 or 1 — the gradients become tiny and learning slows down.

The fix is simple: **divide by the square root of the dimension**.

```text
scaled_score(Q, K_i) = (Q · K_i) / √d
```

For `d = 4`:

```text
√4 = 2

scaled scores = [1/2, 1/2, 2/2] = [0.5, 0.5, 1.0]
```

This keeps the numbers in a reasonable range for softmax.

---

## 5. Softmax: turning scores into weights

Softmax converts raw scores into probabilities that add up to 1:

```text
softmax(z_i) = e^(z_i) / Σ e^(z_j)
```

### Worked example

Using our scaled scores `[0.5, 0.5, 1.0]`:

```text
e^0.5 = 1.65
e^0.5 = 1.65
e^1.0 = 2.72

sum = 1.65 + 1.65 + 2.72 = 6.02

weights:
  w1 = 1.65 / 6.02 = 0.27
  w2 = 1.65 / 6.02 = 0.27
  w3 = 2.72 / 6.02 = 0.45
```

The decoder pays 45% attention to "cats", 27% to "I", and 27% to "love."

---

## 6. Weighted sum: the context vector

Now use the weights to blend the **values**. In basic attention, the values are the same as the keys:

```text
V1 = K1 = [1, 1, 0, 0]
V2 = K2 = [0, 1, 1, 0]
V3 = K3 = [1, 0, 1, 1]

context = 0.27 × V1 + 0.27 × V2 + 0.45 × V3
```

Element by element:

```text
context[0] = 0.27×1 + 0.27×0 + 0.45×1 = 0.72
context[1] = 0.27×1 + 0.27×1 + 0.45×0 = 0.54
context[2] = 0.27×0 + 0.27×1 + 0.45×1 = 0.72
context[3] = 0.27×0 + 0.27×0 + 0.45×1 = 0.45

context = [0.72, 0.54, 0.72, 0.45]
```

This vector is a blend of all encoder states, leaning toward "cats."

---

## 7. What actually changes in the decoder: c becomes c_i

The encoder has done its job — it produced a hidden state for every input word. **All the changes happen in the decoder.** Let's see exactly what changed compared to Part 2.

### The three basic tenets of decoding

In Part 2, the decoder updated its state at every step using three ingredients:

```text
s_i = f( s_{i-1},   y_{i-1},   c )
         │          │          │
         │          │          └─ context from the encoder
         │          └─ previous output word (what I just generated)
         └─ previous decoder state (my own memory)
```

### Spot the difference

Here is the decoder with attention. Compare the two formulas — what changed?

```text
Without attention (Part 2):   s_i = f( s_{i-1},  y_{i-1},  c   )
With attention:               s_i = f( s_{i-1},  y_{i-1},  c_i )
                                                            ↑
                                             the ONLY difference
```

The first two ingredients are untouched: the decoder still uses its **previous state** and the **previous output word**. The only change is the third ingredient:

- **Before:** `c` — one fixed context vector, computed once, reused at every step.
- **After:** `c_i` — a **fresh context vector for step i**, rebuilt at every step. At step 1 the decoder uses c₁, at step 2 it uses c₂, and so on.

The word "context" gets a new **interpretation**: it is no longer "the summary of the whole sentence" but "**the summary of what I need right now**." Since the context is now enriched, the decoder state s_i that absorbs it becomes enriched too — a better context at every step leads to a better memory at every step, which leads to better predictions.

### The formula for c_i

And how is c_i computed? Exactly what we did in sections 3–6, written as one formula:

```text
        n
c_i  =  Σ  α_ij × h_j
       j=1

where:
  h_j   = encoder hidden state for input word j       (sections 3: the keys/values)
  α_ij  = attention weight of word j at decoder step i (sections 4–5: scored, scaled, softmaxed)
  n     = number of input words
```

In words: **the context at step i is the weighted sum of all encoder hidden states, where the weights α_ij are computed fresh at every step i.** Using our worked example from section 6:

```text
c_i = 0.27 × h1 + 0.27 × h2 + 0.45 × h3 = [0.72, 0.54, 0.72, 0.45]
```

At the next decoder step, the query changes, so the weights α change, so c changes — that is the whole trick.

### This is called a "convex combination"

The fancy math name for this weighted sum is a **convex combination**: a blend where all the weights are **between 0 and 1** and they **sum to exactly 1**.

```text
c_i = α_i1 × h1 + α_i2 × h2 + α_i3 × h3

with:  0 ≤ α_ij ≤ 1   and   α_i1 + α_i2 + α_i3 = 1
```

Why does this matter? Because it makes the result a true **percentage-based blend** — like a recipe: "27% of h1, 27% of h2, 45% of h3." The context can never be bigger or wilder than the ingredients; it always stays inside the "space" spanned by the encoder states. This is exactly why we need **softmax** in the pipeline — it is the tool that guarantees both conditions (all weights in [0,1], summing to 1).

### Getting the notation straight: e_ij vs α_ij

Two symbols that are easy to confuse:

```text
e_ij  =  raw attention SCORE   (any number — can be negative, can be large)
α_ij  =  attention WEIGHT      (between 0 and 1, all weights sum to 1)

              softmax
  e_ij  ────────────────→  α_ij
```

Both carry two subscripts, read the same way: **at decoder step i, for encoder word j**. Softmax converts scores into weights:

```text
           exp(e_ij)
α_ij = ───────────────────
        Σ_k exp(e_ik)
```

Two things the exponential does for us:

- **Negative scores become positive.** `exp(-2) = 0.14` — still a valid (small) weight. Without this, a negative score would break the "weights between 0 and 1" requirement.
- **The denominator normalises.** Dividing by the sum of all exponentials guarantees the weights add up to exactly 1.

---

## 8. Where do the scores come from? A learnable alignment function

One question remains: how is the raw score `e_ij` computed? Could we just hard-code the rules — "at step 1 focus on word 1, at step 2 focus on word 2"?

**No — and this is the most important point.** Where to focus changes with every sentence:

```text
English → French:   "I love cats"     → "J'aime les chats"      (roughly in order)
English → German:   "I have seen him" → "Ich habe ihn gesehen"  (verb jumps to the end!)
English → Japanese: subject-verb-object → subject-object-verb    (order changes completely)
```

No human could sit and label, for every possible sentence, which word to focus on at every step. So **what to focus on must itself be learned** by the model during training — just like every other weight.

### The alignment function

The score is produced by a small **learnable function** `a`, called the **alignment function**:

```text
e_ij = a(s_{i-1}, h_j)
```

Read it as: *"to score encoder word j at my step i, compare **my current context** (the decoder's previous state s_{i-1}) against **that word's encoder state** h_j."*

What the decoder has at step i:

```text
  s_{i-1}   — the decoder's own state so far  ("here is what I have generated and what I need next")
  h1 ... hn — all the encoder states           ("here is what each input word means")

  e_i1 = a(s_{i-1}, h1)     score for word 1
  e_i2 = a(s_{i-1}, h2)     score for word 2
  e_i3 = a(s_{i-1}, h3)     score for word 3
```

The function `a` contains **learnable weight matrices** (like every other part of the network). During training, backpropagation adjusts them: whenever the model focuses on the wrong words and produces a bad translation, the loss pushes the alignment weights toward better focusing. Over millions of examples, the model **learns where to look** — nobody tells it.

The dot product from section 3 is the simplest possible alignment function (no extra weights). The **additive (Bahdanau) attention** in section 11 is a richer one, with learned matrices `W1`, `W2` and vector `v`:

```text
Dot product:   a(s, h) = s · h                          (no parameters)
Bahdanau:      a(s, h) = vᵀ · tanh(W1·s + W2·h)         (learned parameters)
```

---

## 9. The complete formula

Putting it all together in one line:

```text
Attention(Q, K, V) = softmax(Q · K^T / √d) · V
```

Where:
- `Q · K^T` computes all dot products at once (matrix multiplication)
- `/ √d` scales them down
- `softmax` turns them into weights
- `· V` takes the weighted sum

This is the **scaled dot-product attention** formula from the famous "Attention Is All You Need" paper (Vaswani et al., 2017).

---

## 10. Matrix form: doing it all at once

In practice, we process all decoder steps and all encoder states in parallel using matrices:

```text
Q shape = (seq_len_decoder, d)
K shape = (seq_len_encoder, d)
V shape = (seq_len_encoder, d)

Step 1: Q · K^T  →  (seq_len_decoder, seq_len_encoder)   scores
Step 2: / √d     →  (seq_len_decoder, seq_len_encoder)   scaled scores
Step 3: softmax  →  (seq_len_decoder, seq_len_encoder)   weights
Step 4: · V      →  (seq_len_decoder, d)                 context vectors
```

Each row of the output is the context vector for one decoder step.

---

## 11. Additive attention (Bahdanau) — the alternative

Before scaled dot-product, **Bahdanau (2014)** proposed additive attention:

```text
score(s_t, h_i) = v^T · tanh(W1 · s_t + W2 · h_i)
```

- `W1` and `W2` are learned weight matrices
- `v` is a learned vector
- `tanh` squashes the result

### How is it different?

| | Dot-product | Additive |
|---|---|---|
| Score function | Simple dot product | Small neural network |
| Speed | Faster (just matrix multiply) | Slower (extra layers) |
| Flexibility | Less flexible | More flexible (learned scoring) |
| Used in | Transformer, modern models | Original seq2seq with attention |

In practice, scaled dot-product is used almost everywhere today because it is fast and works well.

---

## 12. PyTorch: scaled dot-product attention

```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(Q, K, V):
    d = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d)
    weights = F.softmax(scores, dim=-1)
    context = torch.matmul(weights, V)
    return context, weights

# Example
Q = torch.tensor([[1.0, 0.0, 1.0, 0.0]])       # (1, 4)
K = torch.tensor([[1, 1, 0, 0],
                   [0, 1, 1, 0],
                   [1, 0, 1, 1]], dtype=torch.float)  # (3, 4)
V = K.clone()

context, weights = scaled_dot_product_attention(Q, K, V)
print("Weights:", weights)    # tensor([[0.27, 0.27, 0.45]])
print("Context:", context)    # tensor([[0.72, 0.54, 0.72, 0.45]])
```

---

## 13. Summary

- Attention uses three players: **Query** (what am I looking for?), **Key** (what does each word offer?), **Value** (the actual content).
- The **dot product** `Q · K` measures how similar a query is to each key.
- **Scaling** by `√d` prevents large dot products from making softmax too sharp.
- **Softmax** turns raw scores into weights that add up to 1.
- The **weighted sum** of values produces a context vector tuned to what the decoder needs right now: **c_i = Σ α_ij × h_j** — a **convex combination** (weights in [0,1], summing to 1).
- Raw scores `e_ij` come from a **learnable alignment function** `e_ij = a(s_{i-1}, h_j)` — where to focus is learned during training, never hand-coded.
- In the decoder, the **only change** from Part 2 is that the fixed context `c` becomes a per-step context `c_i`: `s_i = f(s_{i-1}, y_{i-1}, c_i)`. The previous state and previous output stay the same.
- The complete formula: **Attention(Q, K, V) = softmax(Q · K^T / √d) · V**
- **Additive attention** (Bahdanau) uses a small network instead of a dot product — slower but more flexible.

**Next:** [Part 5: Drawbacks of Attention-Based Encoder-Decoder Architecture]({{ site.baseurl }}/topics/dl-genai-attention-drawbacks/)
