---
layout: topic
title: "Deep Learning for Generative AI — Part 9: The Math Behind Self-Attention (The Magic Is a Matrix)"
category: Generative AI
order: 109
permalink: /topics/dl-genai-self-attention-math/
tags:
  - generative-ai
  - deep-learning
  - transformer
  - self-attention
  - query-key-value
  - softmax
  - matrix-multiplication
  - beginners
  - friendly
summary: "How the group project intuition turns into a few matrix multiplications: the input matrix X, the learned matrices W_Q, W_K, W_V, and softmax(QKᵀ/√d)V, with a fully worked 3-word example."
---

# Deep Learning for Generative AI — Part 9: The Math Behind Self-Attention (The Magic Is a Matrix)

People often call GPT and Transformers "magic". Here's a better word: **matrix**.

Everything we described with the group project analogy (queries, keys, values, "who listens to whom") comes down to **a few matrix multiplications**. In this part we'll write them down and then work through a tiny example by hand, so you can see every number.

If you need a refresher on dot products or softmax, Part 4 covers them. Here we only use what we need.

---

## 1. Setting up the notation

Take a sentence with **N** words. We'll use a new, tiny example:

```text
"cats chase mice"      →   N = 3 words
```

We need two sizes:

| Symbol | Meaning | In our example |
|---|---|---|
| **N** | Number of words in the input | 3 |
| **D1** | Length of each word's **starting** vector (its plain embedding) | 4 |
| **D2** | Length of each word's **rich** vector `z` (the model size we want) | 2 |

The starting vectors `x1, x2, x3` are plain, "static" descriptions of each word. They are the same no matter what sentence the word is in. The whole point of attention is to turn them into **rich** vectors `z1, z2, z3` that know about their neighbours.

(Real models use sizes like D1 = D2 = 512. We use tiny sizes so you can check the arithmetic.)

---

## 2. Stack the words into one matrix, X

Instead of handling words one at a time, we stack them as **rows** of one matrix:

```text
            ← D1 = 4 columns →
X =  cats   [ 1   0   1   0 ]      row 1 = x1
     chase  [ 0   2   0   1 ]      row 2 = x2
     mice   [ 1   1   0   0 ]      row 3 = x3

size: N × D1 = 3 × 4
```

**One row per word.** That's all X is. The numbers here are made up to keep things simple.

---

## 3. The three learnable matrices: W_Q, W_K, W_V

Where do queries, keys and values come from? From three matrices the Transformer **learns during training**:

| Matrix | Size | Produces |
|---|---|---|
| **W_Q** (query weights) | D1 × D2 | Queries: what each word is looking for |
| **W_K** (key weights) | D1 × D2 | Keys: what each word can offer |
| **W_V** (value weights) | D1 × D2 | Values: what each word actually knows |

"Learnable" means they start as random numbers and get adjusted, bit by bit, during training. Here's the chain that makes them so important:

```text
good W_Q, W_K, W_V
   → good queries, keys and values
      → good attention weights
         → good rich representations
            → good translations / answers
```

Training a Transformer's attention is essentially the search for the best W_Q, W_K and W_V.

---

## 4. Step 1: get Q, K, V with one multiplication each

<img src="{{ site.baseurl }}/assets/img/self-attention-matrix-flow.svg" alt="Step 1: the input matrix X of size N by D1 is multiplied by the learned matrix W_Q of size D1 by D2 to give Q of size N by D2, one query per word. Likewise K equals X times W_K and V equals X times W_V. Step 2: Q times K transpose gives an N by N matrix of match scores; dividing by the square root of D2 and applying softmax gives the weights A, whose rows add to 1; A times V gives Z, of size N by D2, the rich vectors. The whole of self-attention in one line: Z equals softmax of Q K transpose over root D2, times V." style="width:100%;max-width:900px;">

```text
Q = X × W_Q        (N × D1) × (D1 × D2)  =  N × D2
K = X × W_K        same shape
V = X × W_V        same shape
```

One multiplication gives the queries of **all** words at once, with row 1 for cats, row 2 for chase, row 3 for mice. No loop over words. This is why Transformers are so fast on GPUs.

Let's use these small learned matrices (again, made-up numbers):

```text
W_Q = [ 1 0 ]     W_K = [ 0 1 ]     W_V = [ 1 0 ]
      [ 0 1 ]           [ 1 0 ]           [ 0 1 ]
      [ 1 0 ]           [ 1 0 ]           [ 1 1 ]
      [ 0 1 ]           [ 0 1 ]           [ 0 0 ]
```

Multiply X by each one (each entry is "row of X" · "column of W"):

```text
            Q            K            V
cats    [ 2  0 ]     [ 1  1 ]     [ 2  1 ]
chase   [ 0  3 ]     [ 2  1 ]     [ 0  2 ]
mice    [ 1  1 ]     [ 1  1 ]     [ 1  1 ]
```

Check one: the query of **cats** = `[1 0 1 0] × W_Q` → first column: 1·1 + 0·0 + 1·1 + 0·0 = **2**, second column: 1·0 + 0·1 + 1·0 + 0·1 = **0**. So `q_cats = [2, 0]`. ✓

---

## 5. Step 2: queries meet keys with QKᵀ

In the group project, you listen most to the friend whose **key matches your query**. "Match" in math is the **dot product**: bigger when two vectors point the same way.

To match every query with every key in one go, multiply Q by the **transpose** of K (Kᵀ: flip rows into columns):

```text
Q × Kᵀ    (N × D2) × (D2 × N)  =  N × N
```

The result is an **N × N table of scores**. Row i, column j = how well word i's query matches word j's key.

```text
                    keys of →   cats   chase   mice
scores = Q Kᵀ =   cats query  [  2      4      2  ]
                  chase query [  3      3      3  ]
                  mice query  [  2      3      2  ]
```

Check one: cats' query `[2, 0]` · chase's key `[2, 1]` = 2·2 + 0·1 = **4**. That's the highest score in the cats row, so **cats wants to listen to chase the most**.

---

## 6. Step 3: scale, then softmax to get weights

Two small steps turn scores into attention weights.

**Scale by √D2.** Divide every score by √D2 (here √2 ≈ 1.41). With big vectors, dot products get very large and softmax becomes too "extreme" (one word gets everything). Scaling keeps things calm. The original paper uses exactly this.

```text
scores ÷ √2 =  [ 1.41  2.83  1.41 ]
               [ 2.12  2.12  2.12 ]
               [ 1.41  2.12  1.41 ]
```

**Softmax each row.** We want weights that are positive and **add up to 1** (a convex combination, as in Part 4). Softmax does exactly this:

```text
softmax(z)_i = e^(z_i) / (e^(z_1) + e^(z_2) + ... + e^(z_n))
```

Quick example with the numbers 1, 2, 3:

```text
e^1 = 2.72    e^2 = 7.39    e^3 = 20.09     total = 30.20

weights = 2.72/30.20, 7.39/30.20, 20.09/30.20  =  0.09, 0.24, 0.67   (adds to 1 ✓)
```

Because `e^x` is always positive, softmax works even when scores are negative, and the biggest score always gets the biggest share.

Applying softmax to each row of our scaled scores gives the **attention weights A**:

```text
                  cats   chase   mice
A =   cats     [ 0.16   0.67   0.16 ]     ← cats listens mostly to chase
      chase    [ 0.33   0.33   0.33 ]     ← chase listens to everyone equally
      mice     [ 0.25   0.50   0.25 ]     ← mice leans towards chase

(each row adds to 1, allowing for rounding)
```

Notice the **chase** row: its query matched every key equally (all scores were 3), so it splits its attention evenly. In a trained model, W_Q and W_K would be tuned so the useful words stand out.

---

## 7. Step 4: blend the values with A × V

Last step, the "collective knowledge" from the group project. Each word's new vector is a **weighted blend of everyone's values**, using its row of A:

```text
Z = A × V     (N × N) × (N × D2)  =  N × D2
```

For **cats**:

```text
z_cats = 0.16 × v_cats + 0.67 × v_chase + 0.16 × v_mice
       = 0.16 × [2, 1]  + 0.67 × [0, 2]  + 0.16 × [1, 1]
       = [0.49, 1.67]
```

Doing all three rows at once:

```text
            Z
cats    [ 0.49  1.67 ]
chase   [ 1.00  1.33 ]
mice    [ 0.74  1.50 ]
```

We started with plain `3 × 4` word vectors and ended with **rich `3 × 2` vectors**, one per word. Each is built from the whole sentence. "cats" now carries a lot of "chase" in it: it's no longer just *cats*, it's *cats that are doing the chasing*.

---

## 8. The whole thing in one line

Every step above fits in one famous formula:

```text
Z = softmax( Q Kᵀ / √D2 ) × V        where  Q = X W_Q,  K = X W_K,  V = X W_V
```

Read it right to left with the group project in mind:

| Piece | Math | Group project meaning |
|---|---|---|
| `X W_Q`, `X W_K`, `X W_V` | Three matrix multiplications | Everyone reads alone and forms questions, insights, understanding |
| `Q Kᵀ` | Dot product of every query with every key | Whose insights answer whose questions? |
| `/ √D2` | Scaling | Keep the discussion calm |
| `softmax(...)` | Rows become weights that add to 1 | How much you listen to each friend |
| `× V` | Weighted sum of values | Walk away with the group's collective knowledge |

And the shapes:

```text
X (N × D1)  →  Q, K, V (N × D2)  →  scores and A (N × N)  →  Z (N × D2)
```

**Multi-head attention** (Part 8) simply runs this whole recipe several times in parallel, each head with its own W_Q, W_K and W_V, and then joins the results.

---

## 9. Summary

- The "magic" of Transformers is **matrix multiplication**.
- Stack the N word vectors as rows of **X** (N × D1).
- Three **learned** matrices W_Q, W_K, W_V (D1 × D2) turn X into **Q, K, V** (N × D2) in one multiplication each.
- **Q Kᵀ** gives an N × N table of how well each word's query matches each word's key.
- Divide by **√D2**, then **softmax** each row so the weights are positive and add to 1.
- **A × V** blends everyone's values into rich vectors **Z** (N × D2).
- Training is the search for W_Q, W_K, W_V that make these blends as useful as possible.

**Next up:** run all of this yourself in about 15 lines of Python in [Part 10: Self-Attention in Code with NumPy]({{ site.baseurl }}/topics/dl-genai-self-attention-numpy/).
