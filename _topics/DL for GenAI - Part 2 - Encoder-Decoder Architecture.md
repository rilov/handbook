---
layout: topic
title: "Deep Learning for Generative AI — Part 2: Encoder-Decoder Architecture"
category: Generative AI
order: 102
permalink: /topics/dl-genai-encoder-decoder/
tags:
  - generative-ai
  - deep-learning
  - encoder-decoder
  - seq2seq
  - rnn
  - machine-translation
  - beginners
  - friendly
summary: "A beginner-friendly guide to the encoder-decoder (seq2seq) architecture — the foundation behind machine translation, text summarisation, and chatbots."
---

# Deep Learning for Generative AI — Part 2: Encoder-Decoder Architecture

In Part 1 we turned words into numbers (embeddings). Now we need a network that can read a **whole sentence** and produce a **different sentence** — for example, translating English to French or summarising a paragraph.

The architecture that does this is called **encoder-decoder**, also known as **sequence-to-sequence (seq2seq)**.

---

## 1. The problem: variable-length input → variable-length output

A normal neural network takes a fixed-size input and gives a fixed-size output. But sentences come in all sizes:

```text
Input:  "How are you?"          (3 words)
Output: "Comment allez-vous ?"  (3 words, but could be 2 or 5)
```

We need a model that can handle **any length** on both sides.

---

## 2. The big idea: compress, then generate

The encoder-decoder solves this in two steps:

```text
Step 1 — Encoder: read the input sentence and compress it into a single vector
Step 2 — Decoder: use that vector to generate the output sentence, one word at a time
```

### Analogy: the interpreter

Imagine an interpreter at the United Nations. A delegate speaks a full sentence in English, and the interpreter must repeat it in French.

The interpreter works in two phases:

1. **Listening phase (encoder):** The interpreter listens to the **entire** English sentence from start to finish. While listening, they do not speak — they just build up an understanding of what was said. By the end of the sentence, the interpreter holds the full meaning in their head.

2. **Speaking phase (decoder):** Now the interpreter opens their mouth and produces the French translation, one word at a time. They are no longer listening to the original English — they are working entirely from the understanding they built during the listening phase.

The key point is what happens **between** these two phases. After listening and before speaking, the interpreter holds a mental summary — they know *what* the sentence means, even though they have not started translating yet. In the neural network, this mental summary is called the **context vector**. It is a list of numbers (e.g. 256 or 512 numbers) that represents the meaning of the entire input sentence.

```text
English sentence → [interpreter listens] → mental summary → [interpreter speaks] → French sentence
English sentence → [encoder processes]   → context vector → [decoder generates]  → French sentence
```

The context vector is the **only connection** between the encoder and the decoder. The decoder never sees the original English words — it only gets this one vector. So the context vector must contain everything the decoder needs to produce the correct output.

---

## 3. First step: every word becomes a vector

Before the encoder can process anything, each word must be turned into a vector of numbers. This is the **embedding** step we covered in Part 1.

Here is what happens to the sentence "I love cats":

```text
Step 1 — Tokenise:  split the sentence into words
  "I love cats"  →  ["I", "love", "cats"]

Step 2 — Look up index:  each word has a position in the vocabulary
  "I"    → index 5
  "love" → index 312
  "cats" → index 87

Step 3 — Look up embedding:  use the index to grab a row from the embedding matrix
  index 5   → [0.12, -0.45, 0.78, 0.33, ...]   (e.g. 256 numbers)
  index 312 → [0.91,  0.02, -0.64, 0.17, ...]
  index 87  → [0.34,  0.88,  0.21, -0.55, ...]
```

So the sentence is now a **sequence of vectors** — one vector per word:

```text
"I love cats"
      ↓
[ [0.12, -0.45, 0.78, ...],    ← vector for "I"
  [0.91,  0.02, -0.64, ...],   ← vector for "love"
  [0.34,  0.88,  0.21, ...] ]  ← vector for "cats"
```

These embedding vectors are what the encoder actually receives. It never sees the raw words — it only sees numbers.

**Where does the embedding matrix come from?** It can be pre-trained (like Word2Vec or GloVe from Part 1), or it can start with random numbers and be trained along with the rest of the network. Either way, the embedding matrix is updated during training so the vectors become more meaningful over time.

---

## 4. The encoder

The encoder's job is to read the word vectors from section 3, **one at a time**, and build up a single summary of the whole sentence. The encoder is typically an **RNN** (Recurrent Neural Network), **LSTM**, or **GRU** — all of which work in the same general way described below.

### What is a hidden state?

The hidden state is just a **list of numbers** (e.g. 256 numbers) that acts as the encoder's **memory**. It starts as all zeros — the encoder knows nothing yet. Every time it reads a new word, it updates this memory.

Think of it like taking notes while listening to someone speak:

- Before they start → your notepad is blank (hidden state = all zeros)
- After hearing the first word → you jot down a rough note (hidden state h1)
- After hearing the second word → you update your notes with the new information (hidden state h2)
- After the last word → your notes now summarise everything that was said (final hidden state = context vector)

The key idea: **the hidden state always has the same size** (e.g. always 256 numbers), no matter how many words you have read. It is a fixed-size notepad that keeps getting rewritten.

### Walking through "I love cats"

Let's say our hidden state has 4 numbers (real models use 256–512, but 4 is easier to follow).

**Before starting:** the hidden state is zeros.

```text
h0 = [0, 0, 0, 0]   (encoder knows nothing)
```

**Step 1 — Read "I":**

The encoder takes two inputs: the word vector for "I" and the current hidden state h0. It mixes them together (using learned weights) and produces a new hidden state:

```text
Input:   word vector for "I" = [0.12, -0.45, 0.78, 0.33]
         previous state  h0  = [0, 0, 0, 0]

Output:  new state  h1 = [0.31, -0.12, 0.55, 0.08]
```

h1 now contains the encoder's understanding after reading just "I" — it knows *someone* is the subject.

**Step 2 — Read "love":**

```text
Input:   word vector for "love" = [0.91, 0.02, -0.64, 0.17]
         previous state  h1     = [0.31, -0.12, 0.55, 0.08]

Output:  new state  h2 = [0.68, 0.24, -0.11, 0.42]
```

h2 now captures "I love" — the encoder knows *someone loves something*.

**Step 3 — Read "cats":**

```text
Input:   word vector for "cats" = [0.34, 0.88, 0.21, -0.55]
         previous state  h2     = [0.68, 0.24, -0.11, 0.42]

Output:  new state  h3 = [0.52, 0.71, 0.33, -0.19]
```

h3 now captures the meaning of the entire sentence "I love cats." This final hidden state **is** the context vector.

```text
context vector = h3 = [0.52, 0.71, 0.33, -0.19]
```

### How does the encoder "mix" the word vector with the hidden state?

At each step, the encoder does a simple calculation:

```text
h_t = tanh(W_h × h_{t-1}  +  W_x × x_t  +  b)
```

Here is what each piece means:

| Symbol | What it is | Plain English |
|--------|-----------|---------------|
| `x_t` | The embedding vector of the current word | The new word the encoder is reading right now |
| `h_{t-1}` | The previous hidden state | The encoder's memory from all previous words |
| `W_x` | A weight matrix for the word | "How much should I pay attention to this new word?" |
| `W_h` | A weight matrix for the memory | "How much should I keep from my previous memory?" |
| `b` | A bias term | A small adjustment (like a default starting point) |
| `tanh` | An activation function | Squashes the result to stay between −1 and +1 |
| `h_t` | The new hidden state | The encoder's updated memory after reading this word |

The weight matrices `W_x` and `W_h` are **learned during training**. The network figures out for itself how to best combine new words with existing memory.

### Analogy: mixing paint

Think of each word vector as a new colour of paint. The hidden state is the colour in your bucket:

1. Bucket starts empty (clear).
2. Pour in "I" (blue) → bucket is now blue.
3. Pour in "love" (red) → bucket is now purple (a mix of blue and red).
4. Pour in "cats" (yellow) → bucket is now a brownish mix of all three.

The final colour represents the whole sentence. You cannot separate the individual colours out again — they are blended. This is both the strength (compact summary) and the weakness (you lose individual word detail) of this approach.

After the last word, the hidden state contains a compressed representation of the entire sentence. This is the **context vector** that gets passed to the decoder.

---

## 5. The context vector

The context vector is the bridge between the encoder and decoder. It is a single vector (e.g. 256 or 512 numbers) that must summarise the entire input.

```text
"I love cats" → context vector c = [0.42, -0.18, 0.91, ...]
```

This is both the power and the weakness of this design. We will see the weakness in Part 5.

---

## 6. The decoder

The decoder is another RNN. It starts with the context vector as its initial hidden state and generates the output sentence one word at a time.

```text
Initial state: context vector c

Step 1: Input <START> token → predict "J'"     → hidden state s1
Step 2: Input "J'"          → predict "aime"   → hidden state s2
Step 3: Input "aime"        → predict "les"    → hidden state s3
Step 4: Input "les"         → predict "chats"  → hidden state s4
Step 5: Input "chats"       → predict <END>    → stop
```

At each step the decoder:
1. Takes the previous word (or `<START>` at the beginning)
2. Updates its hidden state
3. Predicts the next word using a softmax over the vocabulary

### Training vs inference

| | Training (teacher forcing) | Inference |
|---|---|---|
| Input to each step | The **correct** previous word from the training data | The word the model **actually predicted** at the previous step |
| Speed | Faster, more stable | Slower, errors can compound |

**Teacher forcing** is like a teacher who always tells the student the right answer before asking the next question. It speeds up training but means the model never practises recovering from its own mistakes during training.

---

## 7. Putting it all together

```text
┌──────────────────────────┐      ┌──────────────────────────────┐
│         ENCODER          │      │           DECODER            │
│                          │      │                              │
│  "I" → h1               │      │  <START> → "J'"              │
│  "love" → h2             │  c   │  "J'"    → "aime"           │
│  "cats" → h3 ──────────────────→│  "aime"  → "les"            │
│                          │      │  "les"   → "chats"          │
│  (read whole input)      │      │  "chats" → <END>            │
│                          │      │                              │
│                          │      │  (generate one word at a    │
│                          │      │   time until <END>)          │
└──────────────────────────┘      └──────────────────────────────┘
```

---

## 8. A concrete example: English → French

Let's walk through translating "I love cats" to "J'aime les chats."

### Encoder

```text
Word       Embedding          Hidden state
─────────  ─────────────────  ──────────────
"I"        [0.1, 0.3, ...]   h1 = tanh(W_h·h0 + W_x·emb("I") + b)
"love"     [0.8, -0.2, ...]  h2 = tanh(W_h·h1 + W_x·emb("love") + b)
"cats"     [0.4, 0.7, ...]   h3 = tanh(W_h·h2 + W_x·emb("cats") + b)

Context vector c = h3
```

### Decoder

```text
Input token    Hidden state               Softmax output     Predicted word
─────────────  ─────────────────────────  ─────────────────  ──────────────
<START>        s1 = tanh(W·c + W·emb(<START>) + b)          "J'"
"J'"           s2 = tanh(W·s1 + W·emb("J'") + b)           "aime"
"aime"         s3 = tanh(W·s2 + W·emb("aime") + b)         "les"
"les"          s4 = tanh(W·s3 + W·emb("les") + b)          "chats"
"chats"        s5 = tanh(W·s4 + W·emb("chats") + b)        <END>
```

---

## 9. Loss function: cross-entropy

At each decoder step, the network predicts a probability distribution over the entire vocabulary. The loss measures how far that distribution is from the correct word.

```text
At step 2, the correct word is "aime".
The model predicts: P("aime") = 0.7, P("adore") = 0.15, P("chat") = 0.05, ...

Cross-entropy loss = -log(0.7) = 0.36
```

The total loss for the sentence is the sum (or average) of the losses at each step. Backpropagation flows through the decoder, through the context vector, and back into the encoder — so both halves learn together.

---

## 10. Common applications

| Task | Input | Output |
|------|-------|--------|
| Machine translation | "I love cats" | "J'aime les chats" |
| Text summarisation | A long article | A short summary |
| Chatbot | User message | Bot reply |
| Text-to-SQL | "Show me all users over 30" | `SELECT * FROM users WHERE age > 30` |
| Image captioning | An image (CNN features) | "A dog running on a beach" |

In image captioning, the encoder is a **CNN** instead of an RNN — it compresses the image into a vector. The decoder is still an RNN that generates text.

---

## 11. PyTorch sketch

```python
import torch
import torch.nn as nn

class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, x):
        embedded = self.embedding(x)          # (batch, seq_len, embed_dim)
        outputs, hidden = self.rnn(embedded)  # hidden = context vector
        return hidden                         # (1, batch, hidden_dim)

class Decoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden):
        embedded = self.embedding(x)          # (batch, 1, embed_dim)
        output, hidden = self.rnn(embedded, hidden)
        prediction = self.fc(output)          # (batch, 1, vocab_size)
        return prediction, hidden
```

The encoder reads the full input and returns a hidden state. The decoder takes that hidden state and generates one word per call.

---

## 12. Summary

- The **encoder** reads the input sequence and compresses it into a **context vector**.
- The **decoder** starts from the context vector and generates the output sequence one word at a time.
- During training, **teacher forcing** feeds the correct previous word to the decoder; during inference, the model uses its own predictions.
- The loss is **cross-entropy** at each output step, and backpropagation trains both encoder and decoder together.
- This architecture powers translation, summarisation, chatbots, and more.
- The main weakness is that the entire input is squeezed into **one fixed-size vector** — long sentences lose information. The next part shows how **attention** fixes this.

**Next:** [Part 3: Attention-Based Encoder-Decoder Architecture]({{ site.baseurl }}/topics/dl-genai-attention-encoder-decoder/)
