---
layout: topic
title: "Deep Learning for Generative AI — Part 5: Drawbacks of Attention-Based Encoder-Decoder Architecture"
category: Generative AI
order: 105
permalink: /topics/dl-genai-attention-drawbacks/
tags:
  - generative-ai
  - deep-learning
  - attention
  - encoder-decoder
  - rnn
  - transformer
  - beginners
  - friendly
summary: "A beginner-friendly look at the remaining problems with attention-based encoder-decoders — sequential processing, long-range dependencies, and why the Transformer was invented."
---

# Deep Learning for Generative AI — Part 5: Drawbacks of Attention-Based Encoder-Decoder Architecture

Attention made encoder-decoders much better (Part 3). But several problems remain. Understanding these problems is important because they are **exactly the reasons** the Transformer architecture was invented.

---

## 1. Quick recap: what attention gave us

| Before attention | After attention |
|---|---|
| One fixed context vector | A different context vector at every step |
| Forgets early words in long sentences | Can look back at any word |
| Black-box decisions | Attention weights show what the model focuses on |

Attention was a huge improvement. But the **underlying architecture** — the RNN — still has fundamental limits.

---

## 2. Problem 1: sequential processing (slow training)

An RNN processes words **one at a time**, left to right. Each step depends on the previous one:

```text
h1 = f(x1, h0)
h2 = f(x2, h1)    ← must wait for h1
h3 = f(x3, h2)    ← must wait for h2
...
```

You cannot compute `h3` until `h2` is ready, and `h2` cannot start until `h1` is done. This means:

- **No parallelism.** Modern GPUs are designed to do thousands of operations at once, but RNNs force them to work step by step.
- **Training is slow.** A sentence with 100 words needs 100 sequential steps in the encoder alone, plus 100 more in the decoder.

### Analogy: the assembly line

Imagine a factory where each worker must wait for the previous worker to finish before starting. Even if you have 100 workers, only one is active at any time. That is how an RNN uses a GPU.

A Transformer, by contrast, is like giving every worker their own copy of the product — they all work at the same time.

---

## 3. Problem 2: long-range dependencies

Even with attention, the encoder is still an RNN. Information from early words must travel through many hidden states to reach the end:

```text
Word 1 → h1 → h2 → h3 → ... → h50
```

With each step, the signal from word 1 gets weaker — like a game of telephone. This is the **vanishing gradient** problem.

### What does this mean in practice?

Consider the sentence:

```text
"The cat, which was sitting on the mat near the window
 overlooking the garden where the birds were singing, purred."
```

The subject ("cat") and the verb ("purred") are far apart. The RNN must carry the information about "cat" through dozens of steps. Even with LSTM or GRU gates, long-distance connections are hard to maintain.

Attention helps because the decoder can look directly at word 1. But the **encoder itself** still processes sequentially, so the hidden states at the end are still biased toward recent words.

---

## 4. Problem 3: fixed-length hidden state

At each time step, the RNN compresses everything it has seen into a **single hidden state vector** of fixed size (e.g. 512 dimensions).

```text
After 5 words:  512 numbers must encode 5 words of context
After 50 words: 512 numbers must encode 50 words of context
```

The vector does not grow with the sentence. More information is crammed into the same space, and something has to be forgotten.

Attention partially solves this by letting the decoder access all individual hidden states. But the quality of each hidden state is still limited by this compression.

---

## 5. Problem 4: difficulty with bidirectional context

A standard RNN reads left to right. Word 5 does not know about word 10 yet:

```text
"The bank of the river was muddy."
                          ^
                          "muddy" helps you know "bank" means river bank,
                          but a left-to-right RNN has not seen "muddy" when
                          it encodes "bank."
```

**Bidirectional RNNs** help by running a second RNN right to left and concatenating the states. But this doubles the computation and still has the sequential bottleneck.

---

## 6. Problem 5: attention itself adds cost

Attention computes a score between the decoder state and **every** encoder state at **every** decoder step.

For a sentence of length `n` on both sides:

```text
Number of attention scores = n × n = n²
```

| Sentence length | Attention scores |
|-----------------|------------------|
| 10 words        | 100              |
| 100 words       | 10,000           |
| 1,000 words     | 1,000,000        |

For very long texts, this quadratic cost becomes expensive. (The Transformer has the same quadratic attention cost, but compensates by removing the sequential bottleneck.)

---

## 7. Summary of all drawbacks

| Drawback | Cause | Impact |
|----------|-------|--------|
| **Sequential processing** | RNN processes one word at a time | Cannot use GPU parallelism; slow training |
| **Long-range dependencies** | Information must travel through many steps | Vanishing gradients; forgets distant words |
| **Fixed-length hidden state** | Same-size vector for any sentence length | Compression loss for long sentences |
| **Limited bidirectional context** | Standard RNN is left-to-right only | Cannot use future words to understand current word |
| **Quadratic attention cost** | Score every encoder state at every decoder step | Expensive for long sequences |

---

## 8. What came next: the Transformer

In 2017, the paper **"Attention Is All You Need"** (Vaswani et al.) introduced the **Transformer**. It removed the RNN entirely and used only attention:

```text
RNN encoder-decoder with attention
  → still sequential, still has vanishing gradients

Transformer
  → processes all words in parallel
  → uses self-attention (each word attends to every other word)
  → no recurrence at all
```

The Transformer solves all five problems listed above:

| Problem | Transformer solution |
|---------|---------------------|
| Sequential processing | All positions processed in parallel |
| Long-range dependencies | Direct connection between any two words (no chain of hidden states) |
| Fixed hidden state | Each word keeps its own representation |
| Bidirectional context | Self-attention sees all words at once |
| Quadratic cost | Still quadratic, but very fast on GPUs because of parallelism |

The Transformer is the foundation of **GPT**, **BERT**, **T5**, and every modern large language model. We will cover it in the next series.

---

## 9. A quick comparison table

| Feature | Basic encoder-decoder | + Attention | Transformer |
|---------|----------------------|-------------|-------------|
| Context vector | Single, fixed | Different per step | Self-attention across all words |
| Parallelism | None (sequential) | None (still RNN) | Full parallelism |
| Long sentences | Poor | Better | Best |
| Training speed | Slow | Slow | Fast |
| Modern usage | Rarely used | Some legacy systems | Standard for LLMs |

---

## 10. Summary

- Attention improved the encoder-decoder but did not fix the **RNN bottleneck**.
- The five key drawbacks are: sequential processing, long-range dependencies, fixed hidden state, limited bidirectional context, and quadratic attention cost.
- These problems motivated the **Transformer** architecture, which removed recurrence entirely and relies only on attention.
- Understanding these drawbacks explains **why** Transformers were needed and **why** they work so well.

This concludes the "Context Behind Transformers" series. You now have the background to understand how and why the Transformer was designed.
