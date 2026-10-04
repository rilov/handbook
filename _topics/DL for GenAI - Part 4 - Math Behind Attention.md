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

## 2. The three roles and how they work together

Think of a library search:

| Role | Meaning | Library analogy |
|---|---|---|
| **Query (Q)** | What the decoder is looking for right now | Your search query |
| **Key (K)** | A label for each encoder state | The title of each book |
| **Value (V)** | The actual content of each encoder state | The content of each book |

The decoder writes a query. It compares the query to every key. The better the match, the more of that value it keeps.

### Step 1: the encoder turns each source word into a memory

Before the decoder can use attention, the **encoder** must read the source sentence.

Take the source sentence:

```text
I    love   cats
```

Each word is first turned into an embedding vector:

```text
"I"    →  e1
"love" →  e2
"cats" →  e3
```

The encoder then processes these vectors one by one. In a simple recurrent encoder, this looks like:

```text
hidden_0 = zero vector
hidden_1 = RNN(e1, hidden_0) = h1   (memory of "I")
hidden_2 = RNN(e2, hidden_1) = h2   (memory of "I love")
hidden_3 = RNN(e3, hidden_2) = h3   (memory of "I love cats")
```

After reading the whole sentence, the encoder has produced three hidden states:

```text
h1 = memory of "I"
h2 = memory of "I love"
h3 = memory of "I love cats"
```

These hidden states are the **Keys** and **Values** for attention. Each one is a compact summary of what the encoder has read up to that point.

### Step 2: the decoder asks a question

Now the decoder starts generating the translation. Imagine we are translating:

```text
Source: I    love   cats
Target: J'aime chats
```

When the decoder is about to produce the first target word, it asks itself: *"What do I need from the source sentence right now?"*

Its current hidden state becomes the **Query**:

```text
Query = "I am looking for the subject of the sentence"
```

It compares this query with every source-word memory:

```text
Key 1 = "I"          → matches well
Key 2 = "love"       → matches a little
Key 3 = "cats"       → matches less
```

After softmax, the weights might look like:

```text
weights on ["I", "love", "cats"] = [0.75, 0.15, 0.10]
```

The decoder builds a custom summary:

```text
context = 0.75 × Value("I")
        + 0.15 × Value("love")
        + 0.10 × Value("cats")
```

It uses this summary to predict the first word: `J'`.

For the next word, the decoder updates its hidden state and asks a new question:

```text
Query = "I am looking for the verb now"
```

This time the weights might shift to `[0.10, 0.80, 0.10]`, so the context focuses on `"love"`. The decoder predicts `aime`.

### The attention call

So the decoder is calling a function like this at every step:

```text
context_i = attention(
    query  = decoder_state_i,
    keys   = [encoder_state_1, encoder_state_2, encoder_state_3],
    values = [encoder_state_1, encoder_state_2, encoder_state_3]
)
```

The query changes at every step, so the answer changes too.

### Where the vectors come from

- **Keys and Values** come from the **encoder** hidden states.
- **Query** comes from the **decoder** hidden state at the current step.

In a Transformer, Q/K/V are produced by learned weight matrices (`W_Q`, `W_K`, `W_V`), but the idea is the same: keys and values describe the source, and the query describes what the decoder currently needs. We cover that in [Part 9]({{ site.baseurl }}/topics/dl-genai-self-attention-math/).

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

The keys and values are the same as the encoder states:

```text
K1 = V1 = h1 = [1, 0, 0]
K2 = V2 = h2 = [0, 1, 0]
K3 = V3 = h3 = [0, 0, 1]
```

Suppose the decoder query is:

```text
Q = [2, 0, 1]
```

This query is like the decoder saying: *"I am interested in the first and third source words right now."*

### Step 1: raw scores — ask each memory how relevant it is

The score is the dot product:

```text
Q · K1 = 2×1 + 0×0 + 1×0 = 2
Q · K2 = 2×0 + 0×1 + 1×0 = 0
Q · K3 = 2×0 + 0×0 + 1×1 = 1

scores = [2, 0, 1]
```

The query matches `"I"` best, then `"cats"`, then `"love"`.

### Step 2: scale — keep the numbers friendly

The vectors have dimension `d = 3`, so we divide by `√d ≈ 1.732`:

```text
scaled scores = [2/1.732, 0/1.732, 1/1.732]
              = [1.155, 0.000, 0.577]
```

Scaling keeps the numbers from growing too large when we use long vectors.

### Step 3: softmax — turn scores into weights

Softmax converts any list of numbers into percentages that add up to 1:

```text
e^1.155 ≈ 3.174
 e^0    = 1.000
e^0.577 ≈ 1.781

sum = 3.174 + 1.000 + 1.781 = 5.955

weights = [3.174/5.955, 1.000/5.955, 1.781/5.955]
        = [0.533, 0.168, 0.299]
```

Check: `0.533 + 0.168 + 0.299 = 1.000`.

### Step 4: weighted sum — build the final answer

```text
c = 0.533 × V1 + 0.168 × V2 + 0.299 × V3
  = 0.533 × [1, 0, 0] + 0.168 × [0, 1, 0] + 0.299 × [0, 0, 1]
  = [0.533, 0.168, 0.299]
```

The final **context vector** is `[0.533, 0.168, 0.299]`. It is a blend of all three source words, with most weight on `"I"`.

### What happens for the next word?

After producing one word, the decoder updates its hidden state and creates a new query. Then it runs the same four steps again. Because the query is different, the weights are different, and the decoder gets a fresh context vector for the next word.

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

### A concrete walkthrough

Translating English → French:

```text
Source: The   cat    sat
Target: Le    chat   s'est   assis
```

Here is what happens inside the decoder:

| Step | Target word so far | What the decoder does | Context vector focus |
|---|---|---|---|
| 1 | (nothing) | Uses its initial hidden state as the query. Asks attention, "which source word helps me produce `Le`?" | Mostly on "The" |
| 2 | Le | Updates its hidden state after producing `Le`. New query asks, "which source word helps me produce `chat`?" | Mostly on "cat" |
| 3 | Le chat | Updates again. New query asks, "which source word helps me produce `s'est`?" | Mostly on "sat" |
| 4 | Le chat s'est | Updates again. New query asks, "which source word helps me produce `assis`?" | Mostly on "sat" |

Each row is the same four-step recipe: **query → scores → softmax → weighted sum**. Only the query changes, so the context vector changes with it.

The full picture:

```text
Source words → Encoder → hidden states h1, h2, h3 (keys + values)
                                          ↓
Decoder step 1:  Q1 = s0  →  attention  →  c1  →  "Le"
Decoder step 2:  Q2 = s1  →  attention  →  c2  →  "chat"
Decoder step 3:  Q3 = s2  →  attention  →  c3  →  "s'est"
Decoder step 4:  Q4 = s3  →  attention  →  c4  →  "assis"
```

### How does the decoder know how many words to produce?

It does **not** know in advance. The decoder generates one word at a time and stops when it predicts a special **end-of-sentence token**, usually written `<eos>`.

During training, the target sentence is already known:

```text
Target: Le    chat   s'est   assis   <eos>
```

The decoder is fed the true previous word at every step (this is called **teacher forcing**). It produces one output for each position in the target, including `<eos>`. The loss is computed at every position, so the model learns to predict the right word and, eventually, when to emit `<eos>`.

At inference time, when there is no target sentence available, the process looks like this:

```text
Input:  <sos>
Output: "Le"

Input:  "Le"
Output: "chat"

Input:  "chat"
Output: "s'est"

Input:  "s'est"
Output: "assis"

Input:  "assis"
Output: "<eos>"   ← stop here
```

The previous output becomes the next input. The decoder keeps going until it either produces `<eos>` or reaches a maximum length limit.

So the decoder decides the sentence length itself. It does not get a fixed number of words from the encoder.

### What if the word order changes?

English → German:

```text
English: I     have    seen    him
German:  Ich   habe    ihn     gesehen
```

The English verb phrase "have seen" becomes "habe ... gesehen", with the second half jumping to the end. A fixed word-to-word mapping would fail. Attention learns to look at "seen" when generating "gesehen", even though the positions differ.

---

## 9. Where do the scores come from?

The scores are not hand-coded. They come from a small learnable function:

```text
score(decoder_state, encoder_state) = a(s_{i-1}, h_j)
```

The function `a` has weights that are updated during training. If the model focuses on the wrong word and produces a bad translation, the loss pushes the weights to focus better next time. Over millions of sentences, the model learns where to look.

The simplest version uses a dot product. A richer version, called **Bahdanau (additive) attention**, uses a tiny neural network instead. In modern Transformers, the dot-product version is used because it is fast and works well.

---

## 10. A tiny PyTorch check

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

## 11. Summary

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