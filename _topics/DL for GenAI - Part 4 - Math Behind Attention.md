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

### A concrete example: attention changes at every decoder step

So far we have computed one context vector for one query. In a real translation model the decoder runs for several steps, and the attention weights change at every step.

Consider a simple English → French translation:

```text
Source:  The   cat    sat
         h1    h2     h3

Target:  Le    chat   s'est   assis
         y1    y2     y3      y4
```

At each decoder step the model builds a fresh context vector `c_i`. The table below shows plausible attention weights — not real numbers, but the right intuition:

| Decoder step | Word being generated | Attention on "The" | Attention on "cat" | Attention on "sat" | What the model is doing |
|---|---:|---:|---:|---:|---|
| 1 | Le | 0.70 | 0.20 | 0.10 | Just starting; focus on the first source word. |
| 2 | chat | 0.15 | 0.75 | 0.10 | "Le" is the article; now look for the noun. |
| 3 | s'est | 0.10 | 0.25 | 0.65 | Noun done; now look for the verb. |
| 4 | assis | 0.05 | 0.10 | 0.85 | Confirm the verb and its past tense. |

At step 1 the context vector is roughly:

```text
c_1 ≈ 0.70 × h_The + 0.20 × h_cat + 0.10 × h_sat
```

At step 3 it is:

```text
c_3 ≈ 0.10 × h_The + 0.25 × h_cat + 0.65 × h_sat
```

The same three encoder states are reused, but the **blend** changes. That is why attention is powerful: the decoder can look at a different part of the source sentence at every output step.

### Why hard-coding would fail

You might ask: could we just write rules like “step 1 looks at word 1, step 2 looks at word 2”? Real languages do not line up one-to-one. In English → German:

```text
English:  I     have    seen    him
German:   Ich   habe    ihn     gesehen
                  ↑               ↑
                  └─── verb splits ───┘
```

The English verb phrase "have seen" becomes "habe ... gesehen", with the participle jumping to the end of the sentence. The model must learn to attend to "seen" when generating "gesehen", even though the words are in different positions. No fixed mapping works, so the alignment function must be learned from data.

### Full numerical example: three decoder steps

Here is a fully worked numerical example. We use tiny 3-dimensional vectors and dot-product attention, so every step is visible.

**Source states (keys and values):**

```text
h_I    = [1, 0, 0]   (encoder state for "I")
h_love = [0, 1, 0]   (encoder state for "love")
h_cats = [0, 0, 1]   (encoder state for "cats")
```

Because each state is an axis-aligned unit vector, the dot product `q · h` simply picks out the corresponding coordinate of `q`.

**Decoder queries at three steps:**

```text
q1 = [2.0,  0.5, -0.3]   (about to generate "I")
q2 = [0.2,  1.5,  0.4]   (about to generate "love")
q3 = [-0.4, 0.3,  1.8]   (about to generate "cats")
```

Dimension `d = 3`, so the scaling factor is `√d ≈ 1.732`.

#### Step 1

```text
scores      = [q1·h_I, q1·h_love, q1·h_cats]
            = [2.0, 0.5, -0.3]

scaled      = scores / √3
            = [1.155, 0.289, -0.173]

softmax     = [0.593, 0.250, 0.157]

c_1         = 0.593 × h_I + 0.250 × h_love + 0.157 × h_cats
            = [0.593, 0.250, 0.157]
```

The first step focuses mostly on "I" (59%), with some attention on "love" and "cats".

#### Step 2

```text
scores      = [0.2, 1.5, 0.4]
scaled      = [0.115, 0.866, 0.231]
softmax     = [0.236, 0.500, 0.265]

c_2         = [0.236, 0.500, 0.265]
```

Now the attention peak is on "love" (50%).

#### Step 3

```text
scores      = [-0.4, 0.3, 1.8]
scaled      = [-0.231, 0.173, 1.039]
softmax     = [0.165, 0.247, 0.588]

c_3         = [0.165, 0.247, 0.588]
```

The final step focuses mostly on "cats" (59%).

| Step | Query | Attention on "I" | Attention on "love" | Attention on "cats" | Context vector `c_i` |
|---|---|---:|---:|---:|---|
| 1 | generate "I" | 0.593 | 0.250 | 0.157 | `[0.59, 0.25, 0.16]` |
| 2 | generate "love" | 0.236 | 0.500 | 0.265 | `[0.24, 0.50, 0.27]` |
| 3 | generate "cats" | 0.165 | 0.247 | 0.588 | `[0.17, 0.25, 0.59]` |

You can verify that each row of attention weights adds to exactly 1, so every `c_i` is a valid convex combination of the source states.

### What would happen without attention?

If the decoder had to use the **same** fixed context vector at every step, the simplest choice would be the average of the source states:

```text
c_fixed = (h_I + h_love + h_cats) / 3 = [0.33, 0.33, 0.33]
```

Then the decoder would receive `[0.33, 0.33, 0.33]` at step 1, step 2, and step 3. It would lose the word-specific signal that attention provides. The table above shows why attention is powerful: the context is rebuilt for every step.

### Reproduce it in NumPy

```python
import numpy as np

def softmax(x):
    e = np.exp(x - np.max(x))  # subtract max for numerical stability
    return e / e.sum()

# Source states: one vector per word
H = np.eye(3)

# Three decoder queries
Q = np.array([
    [2.0,  0.5, -0.3],   # step 1: focus on "I"
    [0.2,  1.5,  0.4],   # step 2: focus on "love"
    [-0.4, 0.3,  1.8],   # step 3: focus on "cats"
])

d = 3
for i, q in enumerate(Q, start=1):
    scores = q @ H.T                 # dot products with each source state
    weights = softmax(scores / np.sqrt(d))
    c = weights @ H                  # weighted sum of source states
    print(f"Step {i}: weights = {weights.round(3)}, c = {c.round(3)}")
```

Output:

```text
Step 1: weights = [0.593 0.25  0.157], c = [0.593 0.25  0.157]
Step 2: weights = [0.236 0.5   0.265], c = [0.236 0.5   0.265]
Step 3: weights = [0.165 0.247 0.588], c = [0.165 0.247 0.588]
```

In real models the queries and source states are produced by learned weight matrices and have hundreds of dimensions, but the arithmetic is exactly the same.

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

## 13. PyTorch: Bahdanau (additive) attention with 3 words

Section 11 introduced Bahdanau attention. Here is a tiny, complete PyTorch example with exactly three source words so you can see the scores, weights, and context vector step by step.

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
        # decoder_state:    (batch, 1, hidden)
        # encoder_outputs:  (batch, src_len, hidden)

        # score for every encoder position
        score = self.v(
            torch.tanh(self.W1(decoder_state) + self.W2(encoder_outputs))
        )  # (batch, src_len, 1)

        weights = F.softmax(score, dim=1)              # (batch, src_len, 1)
        context = (weights * encoder_outputs).sum(dim=1, keepdim=True)
        return context, weights


hidden_dim = 4
attention = Attention(hidden_dim)

# Three source words: "I", "love", "cats"
encoder_outputs = torch.tensor(
    [[[1.0, 0.0, 0.0, 0.0],   # "I"
      [0.0, 1.0, 0.0, 0.0],   # "love"
      [0.0, 0.0, 1.0, 0.0]]], # "cats"
    dtype=torch.float32
)  # shape: (1, 3, 4)

# Pretend the decoder is about to produce "love"
decoder_state = torch.tensor(
    [[[0.0, 1.0, 0.0, 0.0]]],
    dtype=torch.float32
)  # shape: (1, 1, 4)

# For the demo, make the matrices simple:
# W1 and W2 copy their input; v picks the second dimension.
with torch.no_grad():
    attention.W1.weight.copy_(torch.eye(hidden_dim))
    attention.W2.weight.copy_(torch.eye(hidden_dim))
    attention.v.weight.copy_(torch.tensor([[0.0, 1.0, 0.0, 0.0]]))

context, weights = attention(decoder_state, encoder_outputs)

print("Attention weights on ['I', 'love', 'cats']:")
for word, w in zip(["I", "love", "cats"], weights.squeeze().tolist()):
    print(f"  {word:6s}: {w:.4f}")

print(f"Sum of weights: {weights.sum().item():.4f}")
print(f"Context vector: {context.squeeze().tolist()}")
```

Output:

```text
Attention weights on ['I', 'love', 'cats']:
  I     : 0.3101
  love  : 0.3797
  cats  : 0.3101
Sum of weights: 1.0000
Context vector: [0.3101, 0.3797, 0.3101, 0.0]
```

Because the decoder state matched the embedding for "love", the model assigns the largest weight to "love". In a real model, `W1`, `W2`, and `v` are learned from data so the model figures out these alignments automatically.

---

## 15. Full PyTorch seq2seq network with attention

The `Attention` module from the previous section is only one piece. Here is a complete, runnable encoder-decoder network that uses it. The example is tiny (three source words, three target words) so every tensor shape is visible.

### Vocabulary

```python
to_src = {'<pad>': 0, 'I': 1, 'love': 2, 'cats': 3}
to_tgt = {'<pad>': 0, '<sos>': 1, '<eos>': 2, 'J': 3, 'aime': 4, 'chats': 5}
```

### Encoder

```python
class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, src):
        embedded = self.embedding(src)              # (batch, src_len, embed_dim)
        outputs, hidden = self.gru(embedded)        # outputs: (batch, src_len, hidden)
        return outputs, hidden
```

### Decoder with attention

```python
class Decoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.attention = Attention(hidden_dim)
        self.gru = nn.GRU(embed_dim + hidden_dim, hidden_dim, batch_first=True)
        self.out = nn.Linear(hidden_dim, vocab_size)

    def forward_step(self, input_token, hidden, encoder_outputs):
        embedded = self.embedding(input_token)      # (batch, 1, embed_dim)
        query = hidden.permute(1, 0, 2)             # (batch, 1, hidden)
        context, weights = self.attention(query, encoder_outputs)

        gru_input = torch.cat([embedded, context], dim=-1)
        output, hidden = self.gru(gru_input, hidden)
        prediction = self.out(output)               # (batch, 1, vocab_size)
        return prediction, hidden, weights
```

### Full seq2seq model

```python
class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder

    def forward(self, src, tgt):
        encoder_outputs, hidden = self.encoder(src)

        batch_size, tgt_len = tgt.size()
        outputs, attentions = [], []

        input_token = tgt[:, 0:1]  # <sos>
        for t in range(1, tgt_len):
            output, hidden, weights = self.decoder.forward_step(
                input_token, hidden, encoder_outputs
            )
            outputs.append(output)
            attentions.append(weights)
            input_token = tgt[:, t:t+1]  # teacher forcing

        outputs = torch.cat(outputs, dim=1)
        attentions = torch.cat(attentions, dim=2)
        return outputs, attentions
```

### Train on one example

```python
embed_dim = 8
hidden_dim = 16

encoder = Encoder(len(to_src), embed_dim, hidden_dim)
decoder = Decoder(len(to_tgt), embed_dim, hidden_dim)
model = Seq2Seq(encoder, decoder)

criterion = nn.CrossEntropyLoss(ignore_index=to_tgt['<pad>'])
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

src = torch.tensor([[to_src[w] for w in ["I", "love", "cats"]]])
tgt = torch.tensor([[to_tgt[w] for w in ["<sos>", "J", "aime", "chats", "<eos>"]]])

# Train on this single sentence 100 times (a toy demo)
for epoch in range(100):
    optimizer.zero_grad()
    outputs, _ = model(src, tgt)
    loss = criterion(outputs.reshape(-1, len(to_tgt)), tgt[:, 1:].reshape(-1))
    loss.backward()
    optimizer.step()
```

### What the attention learns

Before training, attention weights are roughly uniform. After training, the model learns to focus on the right source word for the first target step:

```text
Before training:
  step 1 (J    ): 0.335 0.322 0.343   <- almost uniform
  step 2 (aime ): 0.335 0.322 0.343
  step 3 (chats): 0.335 0.322 0.343
  step 4 (<eos>): 0.334 0.323 0.343

After training:
  step 1 (J    ): 0.918 0.060 0.022   <- strongly on "I"
  step 2 (aime ): 0.334 0.424 0.242
  step 3 (chats): 0.408 0.303 0.289
  step 4 (<eos>): 0.146 0.515 0.339
```

In a real system, training data contains millions of sentence pairs, the hidden dimension is 256–1024, and the alignment becomes much sharper across all positions.

### Why this matters

This code shows the full picture:

1. The **encoder** builds one hidden state per source word.
2. The **decoder** generates one target word at a time.
3. The **attention** module decides which source word to look at before each prediction.
4. The **loss** compares predicted words to true words; backpropagation updates the attention weights so the model learns to align languages automatically.

The attention mechanism is not magic — it is a small, differentiable scoring function placed between two RNNs.

---

## 16. Summary

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
