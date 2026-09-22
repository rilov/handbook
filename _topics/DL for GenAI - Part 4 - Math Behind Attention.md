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

## 7. The complete formula

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

## 8. Matrix form: doing it all at once

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

## 9. Additive attention (Bahdanau) — the alternative

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

## 10. PyTorch: scaled dot-product attention

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

## 11. Summary

- Attention uses three players: **Query** (what am I looking for?), **Key** (what does each word offer?), **Value** (the actual content).
- The **dot product** `Q · K` measures how similar a query is to each key.
- **Scaling** by `√d` prevents large dot products from making softmax too sharp.
- **Softmax** turns raw scores into weights that add up to 1.
- The **weighted sum** of values produces a context vector tuned to what the decoder needs right now.
- The complete formula: **Attention(Q, K, V) = softmax(Q · K^T / √d) · V**
- **Additive attention** (Bahdanau) uses a small network instead of a dot product — slower but more flexible.

**Next:** [Part 5: Drawbacks of Attention-Based Encoder-Decoder Architecture]({{ site.baseurl }}/topics/dl-genai-attention-drawbacks/)
