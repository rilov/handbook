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
summary: "A simple, step-by-step walkthrough of the math behind attention — what Query, Key, and Value mean, how dot products and softmax turn a question into a weighted blend, and how the decoder uses this blend at every step."
---

# Deep Learning for Generative AI — Part 4: Math Behind Attention Mechanism

[Part 3]({{ site.baseurl }}/topics/dl-genai-attention-encoder-decoder/) showed the idea: the decoder looks back at the encoder states and focuses on the most relevant ones. This part shows the math that makes it work — one small step at a time.

> **Where this fits:** this is the math of **decoder-to-encoder attention**. The same ingredients (dot products, softmax, Query/Key/Value) appear again in [Part 9]({{ site.baseurl }}/topics/dl-genai-self-attention-math/) for self-attention inside a Transformer.

---

## 1. Attention in one sentence

**Attention lets the decoder ask every encoder state, “How useful are you to what I need right now?” and then take a weighted average of the answers.**

The weights are not fixed. They are recomputed at every decoder step.

---

## 2. Three roles: Query, Key, Value

Think of a library search:

| Role | Meaning | Library analogy |
|---|---|---|
| **Query (Q)** | What the decoder is looking for right now | Your search query |
| **Key (K)** | A label for each encoder state | The title of each book |
| **Value (V)** | The actual content of each encoder state | The content of each book |

The decoder writes a query. It compares the query to every key. The better the match, the more of that value it keeps.

---

## 3. The three-step recipe

```text
1. Compare the query with every key → raw scores
2. Turn the scores into percentages (weights) with softmax
3. Blend the values using those weights → context vector
```

That is the whole attention mechanism. Everything else is just details.

---

## 4. A concrete example with small numbers

We will use 3-dimensional vectors and three source words:

```text
h1 = [1, 0, 0]  → encoder state for "I"
h2 = [0, 1, 0]  → encoder state for "love"
h3 = [0, 0, 1]  → encoder state for "cats"
```

In this example, the keys are the encoder states and the values are also the encoder states:

```text
K1 = V1 = h1 = [1, 0, 0]
K2 = V2 = h2 = [0, 1, 0]
K3 = V3 = h3 = [0, 0, 1]
```

Suppose the decoder query is:

```text
Q = [2, 0, 1]
```

### Step 1: raw scores

The score is the dot product:

```text
Q · K1 = 2×1 + 0×0 + 1×0 = 2
Q · K2 = 2×0 + 0×1 + 1×0 = 0
Q · K3 = 2×0 + 0×0 + 1×1 = 1

scores = [2, 0, 1]
```

The query matches `"I"` best, then `"cats"`, then `"love"`.

### Step 2: scale

The vectors have dimension `d = 3`, so we divide by `√d ≈ 1.732`:

```text
scaled scores = [2/1.732, 0/1.732, 1/1.732]
              = [1.155, 0.000, 0.577]
```

Scaling keeps the numbers from growing too large when we use long vectors.

### Step 3: softmax turns scores into weights

Softmax converts any list of numbers into percentages that add up to 1:

```text
softmax([1.155, 0.000, 0.577])
```

```text
e^1.155 ≈ 3.174
 e^0    = 1.000
e^0.577 ≈ 1.781

sum = 3.174 + 1.000 + 1.781 = 5.955

weights = [3.174/5.955, 1.000/5.955, 1.781/5.955]
        = [0.533, 0.168, 0.299]
```

Check: `0.533 + 0.168 + 0.299 = 1.000`.

### Step 4: weighted sum of values

```text
c = 0.533 × V1 + 0.168 × V2 + 0.299 × V3
  = 0.533 × [1, 0, 0] + 0.168 × [0, 1, 0] + 0.299 × [0, 0, 1]
  = [0.533, 0.168, 0.299]
```

The final **context vector** is `[0.533, 0.168, 0.299]`. It is a blend of all three source words, with most weight on `"I"`.

---

## 5. Why do we need softmax?

Without softmax, the weights could be negative or not add up to 1. Softmax guarantees two useful things:

- every weight is between 0 and 1,
- all weights add up to exactly 1.

That makes the context vector a true **blend** of the values, not a random sum.

---

## 6. Why do we scale by √d?

When vectors are long (for example, 512 dimensions), dot products can become huge. Huge numbers make softmax push one weight close to 1 and all others close to 0. The gradients then become very small and learning slows down.

Dividing by `√d` keeps the scores in a comfortable range.

```text
score(Q, K) = (Q · K) / √d
```

That is all the scaling does.

---

## 7. The full attention formula

Putting the three steps into one line gives the famous scaled dot-product attention:

```text
Attention(Q, K, V) = softmax( (Q · K^T) / √d ) · V
```

Read it from left to right:

1. `Q · K^T` — compare the query with every key.
2. `/ √d` — scale the scores down.
3. `softmax(...)` — turn scores into weights.
4. `· V` — blend the values with those weights.

The output is the context vector `c`.

---

## 8. What changes in the decoder?

In [Part 2]({{ site.baseurl }}/topics/dl-genai-encoder-decoder/) the decoder updated its state using a fixed context vector:

```text
s_i = f(s_{i-1}, y_{i-1}, c)
```

With attention, the only change is that `c` becomes `c_i` — a fresh context vector at every step:

```text
s_i = f(s_{i-1}, y_{i-1}, c_i)
                          ↑
                 recomputed at every decoder step
```

The previous decoder state `s_{i-1}` and the previous output word `y_{i-1}` stay the same. The context is rebuilt each time because the query changes.

---

## 9. A real-language example

Consider translating English → French:

```text
Source: The   cat    sat
Target: Le    chat   s'est   assis
```

At each decoder step the model looks at the source words with different weights:

| Target step | Word | Attention on "The" | Attention on "cat" | Attention on "sat" |
|---|---|---:|---:|---:|
| 1 | Le | 0.70 | 0.20 | 0.10 |
| 2 | chat | 0.15 | 0.75 | 0.10 |
| 3 | s'est | 0.10 | 0.25 | 0.65 |
| 4 | assis | 0.05 | 0.10 | 0.85 |

At step 1 the decoder mostly reads "The". At step 2 it shifts to "cat". At step 4 it focuses on "sat". The same encoder states are reused, but the blend is different every time.

### What if the word order changes?

English → German:

```text
English: I     have    seen    him
German:  Ich   habe    ihn     gesehen
```

The English verb phrase "have seen" becomes "habe ... gesehen", with the second half jumping to the end. A fixed word-to-word mapping would fail. Attention learns to look at "seen" when generating "gesehen", even though the positions differ.

---

## 10. Where do the scores come from?

The scores are not hand-coded. They come from a small learnable function:

```text
score(decoder_state, encoder_state) = a(s_{i-1}, h_j)
```

The function `a` has weights that are updated during training. If the model focuses on the wrong word and produces a bad translation, the loss pushes the weights to focus better next time. Over millions of sentences, the model learns where to look.

The simplest version uses a dot product. A richer version, called **Bahdanau (additive) attention**, uses a tiny neural network instead. In modern Transformers, the dot-product version is used because it is fast and works well.

---

## 11. A tiny PyTorch check

Here is the whole recipe in code:

```python
import torch
import torch.nn.functional as F
import math

def attention(query, key, value):
    d = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d)
    weights = F.softmax(scores, dim=-1)
    context = torch.matmul(weights, value)
    return context, weights

# one query, three keys/values of dimension 3
Q = torch.tensor([[2.0, 0.0, 1.0]])
K = torch.tensor([[1.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0],
                  [0.0, 0.0, 1.0]])
V = K.clone()

context, weights = attention(Q, K, V)
print("weights:", weights)   # tensor([[0.533, 0.168, 0.299]])
print("context:", context)   # tensor([[0.533, 0.168, 0.299]])
```

The numbers match the hand calculation from section 4.

---

## 12. Summary

| Idea | In plain words |
|---|---|
| **Query** | What the decoder is currently looking for. |
| **Key** | A label for each encoder state. |
| **Value** | The actual content of each encoder state. |
| **Dot product** | Measures how well a query matches a key. |
| **Scaling** | Divides by `√d` to keep scores from exploding. |
| **Softmax** | Turns scores into weights that add to 1. |
| **Weighted sum** | Blends values into one context vector `c_i`. |
| **Per-step context** | The decoder gets a fresh `c_i` at every step. |
| **Learnable scoring** | The model learns where to focus from training data. |

The full formula, worth remembering, is:

```text
Attention(Q, K, V) = softmax( (Q · K^T) / √d ) · V
```

**Next:** [Part 5: Drawbacks of Attention-Based Encoder-Decoder Architecture]({{ site.baseurl }}/topics/dl-genai-attention-drawbacks/)