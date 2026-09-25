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

The architecture that does this is called **encoder-decoder**, also known as **sequence-to-sequence (seq2seq)**. The important thing to know upfront: the encoder and decoder are **two separate neural networks**, each with its own weights. They are trained together but they do different jobs.

---

## 1. The foundation: translation is done by neural networks

Our goal in this article is to translate a sentence — say, English to French:

```text
"I love cats"  →  "J'aime les chats"
```

The machine that does this is built from **neural networks**. So before we look at the architecture, let's understand what a neural network does *in the context of translation*.

### A neural network only works with numbers

A neural network cannot read words. It takes **numbers in** and produces **numbers out**. So the entire translation pipeline is about numbers:

```text
"I love cats"                                    "J'aime les chats"
      ↓                                                  ↑
convert words to numbers                    convert numbers back to words
      ↓                                                  ↑
[0.12, -0.45, ...]  →  [neural networks]  →  [0.87, 0.03, ...]
```

- **Going in:** each word becomes a vector of numbers (the embeddings from Part 1).
- **Inside:** the networks transform these numbers step by step.
- **Coming out:** the final numbers are converted back into words (by picking the most likely word from the vocabulary).

### How does the network transform numbers? Weights.

Inside the network are **weights** — grids of numbers (matrices). Every transformation is a matrix multiplication: the input numbers get multiplied by the weights to produce output numbers.

Here is a tiny example. Say the word vector for "I" is `[0.8, 0.2]` and the network has this weight matrix:

```text
       input for "I"    weights           output
       [0.8]            [[0.6, 0.1],      [?]
       [0.2]             [0.2, 0.7]]      [?]

output[0] = 0.6 × 0.8 + 0.1 × 0.2 = 0.50
output[1] = 0.2 × 0.8 + 0.7 × 0.2 = 0.30

output = [0.50, 0.30]
```

The weights decide **what the network pays attention to** in the word vector. Different weights would produce a completely different output from the same word.

### Where do the weights come from? Training.

The weights start as **random numbers** — at that point the network produces garbage translations. Then we train it:

1. **Show it an example:** Feed in "I love cats" and let the network produce a translation attempt — maybe "Le chien mange" (garbage at first).
2. **Measure the error:** Compare the attempt with the correct answer "J'aime les chats." The difference is called the **loss**.
3. **Adjust the weights:** A process called **backpropagation** figures out which weights caused the error and nudges each one slightly in the direction that reduces it.
4. **Repeat** with millions of sentence pairs. Gradually the weights shift from random values to values that produce correct translations.

```text
                  ┌──────────────────────────────────────────────┐
                  │  Feed in "I love cats" → get attempt          │
  Training loop:  │  Compare with "J'aime les chats" → loss       │
                  │  Backpropagation → nudge all weights slightly │
                  │  Repeat with the next sentence pair           │
                  └──────────────────────────────────────────────┘
```

**Nobody programs the translation rules by hand.** The network discovers them by seeing millions of translated sentence pairs and slowly adjusting its weights.

### Keep this in mind for the rest of the article

Everything that follows builds on these three facts:

1. The translator is made of **neural networks** that only handle numbers.
2. The transformations happen through **weight matrices** (like `W_h`, `W_x`, and `b` you will see later).
3. Those weights are **learned from training data**, not written by a person.

---

## 2. The problem: variable-length input → variable-length output

Now that we know translation is done by neural networks, here is the first obstacle. The network from section 1 takes a **fixed-size** input and gives a **fixed-size** output. But sentences come in all sizes:

```text
Input:  "How are you?"          (3 words)
Output: "Comment allez-vous ?"  (3 words, but could be 2 or 5)
```

We need a model that can handle **any length** on both sides. The solution is the encoder-decoder architecture.

---

## 3. The big idea: two networks working together

The encoder-decoder uses **two separate neural networks** that work as a team:

```text
┌─────────────────────────┐         ┌─────────────────────────┐
│    ENCODER (network 1)  │         │    DECODER (network 2)  │
│                         │         │                         │
│  Has its own weights    │ context │  Has its own weights    │
│  Job: read the input    │ vector  │  Job: generate output   │
│  sentence and compress  │────────→│  sentence, one word at  │
│  it into a single vector│         │  a time                 │
└─────────────────────────┘         └─────────────────────────┘
```

- **Network 1 (encoder):** reads the input sentence and compresses it into a single vector.
- **Network 2 (decoder):** takes that vector and generates the output sentence, one word at a time.

They have **separate weight matrices** — the encoder has its own `W_h` and `W_x`, and the decoder has its own different `W_h` and `W_x`. But they are trained **together** as one system: the loss from the decoder's output flows back through both networks, so both sets of weights are updated at the same time.

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

That is the big picture. Now let's follow the pipeline step by step, starting with how words get into the encoder in the first place.

---

## 4. First step: every word becomes a vector

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

We now have a sequence of word vectors. The next step is to feed them to the first of our two networks: the encoder.

---

## 5. The encoder

The encoder's job is to read the word vectors from section 4, **one at a time**, and build up a single summary of the whole sentence.

### The problem: a normal network has no memory

Recall the neural network from section 1: numbers go in, math happens, numbers come out. Each input is processed **independently** — the network has no idea what it saw before.

```text
Normal network:

  input 1 → [network] → output 1     (forgets everything)
  input 2 → [network] → output 2     (forgets everything)
  input 3 → [network] → output 3     (forgets everything)
```

That is a problem for sentences, because **word order and history matter**. "The dog bit the man" and "The man bit the dog" contain the same words — the only difference is the sequence. To understand a sentence, the network must remember what came before.

### The solution: give the network a memory (this is the RNN)

How do we fix a network that forgets? Simple idea: **whatever the network produced for the previous word, hand it back to the network along with the next word.**

Compare the two side by side:

```text
Normal network — each word processed alone:

  "I"    → [network] → result       (result is thrown away)
  "love" → [network] → result       (knows nothing about "I")
  "cats" → [network] → result       (knows nothing about "I love")


RNN — each word processed together with the previous result:

  "I"    + (blank memory)        → [network] → memory after "I"
                                                    │
                                     ┌──────────────┘
                                     ↓
  "love" + memory after "I"      → [network] → memory after "I love"
                                                    │
                                     ┌──────────────┘
                                     ↓
  "cats" + memory after "I love" → [network] → memory after "I love cats"
```

Notice what changed: the network now takes **two inputs at every step** instead of one:

1. The **new word** (as a vector, from section 4)
2. The **memory from the previous step** (what the network produced last time)

And it produces **one output**: an updated memory that now includes the new word.

**Important:** it is the **same network with the same weights** used at every step — not three different networks. The network is simply applied again and again, once per word, each time carrying its previous output forward.

### Analogy: reading with a sticky note

Imagine you can only see **one word at a time** through a small window, but you have a sticky note:

1. You see "I" — you write on the note: *"someone is talking about themselves."*
2. The window moves to "love" — you read your note, see the new word, and rewrite the note: *"this person loves something."*
3. The window moves to "cats" — you read the note, see the new word, and rewrite: *"this person loves cats."*

You never saw the whole sentence at once — but by always combining the **note (memory)** with the **current word**, you ended up understanding the full sentence. The RNN does exactly this.

This is why it is called *recurrent* — "recurrent" means "happening repeatedly." The same operation repeats for every word, and the output of one step feeds back in as the input of the next.

### Where exactly does this loop live inside the network?

A neural network has three parts: an **input layer**, one or more **middle (hidden) layers**, and an **output layer**. The loop is **not** at the output layer — it happens at the **middle layer**.

Here is a normal feed-forward network first:

```text
Normal network (no memory):

   input layer      middle layer      output layer
   ┌─────────┐      ┌───────────┐     ┌──────────┐
   │  word   │ ───→ │  neurons  │ ──→ │  result  │
   │ vector  │      │ (compute) │     │          │
   └─────────┘      └───────────┘     └──────────┘

   Data flows straight through, left to right. Nothing is kept.
```

And here is the RNN — one added connection makes all the difference:

```text
RNN (with memory):

   input layer      middle layer      output layer
   ┌─────────┐      ┌───────────┐     ┌──────────┐
   │  word   │ ───→ │  neurons  │ ──→ │  result  │
   │ vector  │      │ (compute) │     │(optional)│
   └─────────┘      └─────┬─────┘     └──────────┘
                      ↑    │
                      │    │  the middle layer's values
                      └────┘  loop back into itself
                              at the next time step
```

The values sitting in the middle layer after processing a word — those **are the hidden state**. At the next time step, they are fed back into the same middle layer along with the new word.

Unrolled over time, it looks like this:

```text
              "I"              "love"            "cats"
               │                 │                 │
               ↓                 ↓                 ↓
          ┌─────────┐       ┌─────────┐       ┌─────────┐
  h0 ───→ │ middle  │ ─h1─→ │ middle  │ ─h2─→ │ middle  │ ─h3─→ context
 (zeros)  │  layer  │       │  layer  │       │  layer  │       vector
          └─────────┘       └─────────┘       └─────────┘
          (same layer, same weights, applied 3 times)
```

Two things to notice:

- **The hidden state h is the middle layer's activations** — not a separate storage box. "Passing the hidden state forward" literally means: take the middle layer's numbers from this step and feed them into the middle layer at the next step.
- **The output layer is optional for the encoder.** The encoder does not need to produce a word at every step — we only care about its final hidden state (the context vector). The decoder, on the other hand, *does* use its output layer at every step to predict the next word.

**What about stacked layers?** If the encoder has 3 stacked layers (as shown later in this section), **each layer has its own loop and its own hidden state**. Layer 1's hidden state feeds back into layer 1, layer 2's into layer 2, and so on.

```text
Stacked RNN — every layer has its own loop:

   word vector
        ↓
   ┌─────────┐ ←──┐
   │ layer 1 │────┘   h¹ loops back into layer 1
   └────┬────┘
        ↓
   ┌─────────┐ ←──┐
   │ layer 2 │────┘   h² loops back into layer 2
   └────┬────┘
        ↓
   ┌─────────┐ ←──┐
   │ layer 3 │────┘   h³ loops back into layer 3
   └────┬────┘
        ↓
     output
```

### But wait — for images, the whole image goes in at once. Why not the whole sentence?

If you have seen image networks (like CNNs), you know the **entire image** is fed into the first layer in one go, and there is **one forward pass**:

```text
Image network — ONE forward pass, whole input at once:

  entire image (e.g. 224×224 pixels, all at once)
        ↓
   [layer 1] → [layer 2] → [layer 3] → "cat"

  Run once. Done.
```

An RNN is different: the network runs **once per word** — a 3-word sentence means **3 forward passes** through the same network:

```text
RNN — THREE forward passes, one word each:

  Pass 1:  "I"    + h0 → [network] → h1
  Pass 2:  "love" + h1 → [network] → h2
  Pass 3:  "cats" + h2 → [network] → h3

  Run 3 times. The hidden state carries information between runs.
```

Why the difference?

| | Image | Sentence |
|---|---|---|
| Size | Fixed (e.g. always 224×224 pixels) | Variable (3 words, 8 words, 50 words...) |
| Input strategy | Whole input in one pass | One word per pass, repeated |
| Memory between passes | Not needed — there is only one pass | The hidden state connects the passes |

An image always has the same number of pixels, so you can build a network whose input layer exactly fits it. A sentence has no fixed size — you cannot build an input layer that fits "any number of words." The RNN's trick is to keep the network small (one word at a time) and run it repeatedly, using the hidden state to accumulate meaning across the runs.

**In short:** an image network is *one big bite*; an RNN is *many small bites with a memory of what it has chewed so far*.

> Fun fact: the Transformer architecture (coming in later parts) actually *does* take the whole sentence at once, more like an image network — that is one of the reasons it replaced RNNs. But it needs special tricks (positional encoding, attention) to handle variable lengths and word order.

### That memory has a name: the hidden state

The memory that gets passed from step to step is called the **hidden state**. Concretely, it is just a **list of numbers** (e.g. 256 numbers):

- It is called *hidden* because it is internal to the network — it is not the input and not the final output; it lives "hidden" in the middle.
- It is called a *state* because it represents the network's current state of understanding — everything it has absorbed from the sentence so far.

It starts as all zeros — the encoder knows nothing yet. Every time it reads a new word, it updates this memory.

Think of it like taking notes while listening to someone speak:

- Before they start → your notepad is blank (hidden state = all zeros)
- After hearing the first word → you jot down a rough note (hidden state h1)
- After hearing the second word → you update your notes with the new information (hidden state h2)
- After the last word → your notes now summarise everything that was said (final hidden state = context vector)

The key idea: **the hidden state always has the same size** (e.g. always 256 numbers), no matter how many words you have read. It is a fixed-size notepad that keeps getting rewritten.

> **Note:** In practice the encoder is usually an **LSTM** or **GRU** rather than a plain RNN. These are improved versions of the RNN that are better at remembering things over long sentences, but the core idea — a hidden state updated word by word — is exactly the same.

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

It is **not** simple vector addition. The encoder uses three operations: **matrix multiplication**, **addition**, and **squashing**. Here is the formula:

```text
h_t = tanh(W_h × h_{t-1}  +  W_x × x_t  +  b)
```

That looks dense, so let's break it into three clear sub-steps:

```text
Sub-step 1:  Transform the memory      →  W_h × h_{t-1}      (matrix multiply)
Sub-step 2:  Transform the new word     →  W_x × x_t          (matrix multiply)
Sub-step 3:  Add them together + bias   →  result + b          (addition)
Sub-step 4:  Squash to [-1, +1]         →  tanh(result)        (activation)
```

#### Why matrix multiplication and not just addition?

Plain addition would just pile numbers on top of each other — the encoder would have no control over **which parts** of the word or memory matter. Matrix multiplication is like a set of **knobs and dials**: each weight in the matrix controls how much one input number influences one output number. This lets the encoder learn things like "pay a lot of attention to verbs but less to articles."

#### Worked example with real numbers

Let's use tiny 2-dimensional vectors so you can follow every number. In a real model these would be 256 or 512 dimensions — the math is identical, just bigger.

**Important: where does each number come from?**

| Value | Where it comes from | In this example |
|-------|-------------------|-----------------|
| `h0` (previous hidden state) | The output of the **previous step**. At the very start of a sentence, it is initialised to all zeros. Here we use `[0.5, -0.3]` to show a mid-sentence step where the encoder already has some memory. | `[0.5, -0.3]` |
| `x1` (word vector) | Looked up from the **embedding matrix** (section 4). The word "I" has an index in the vocabulary, and that index picks a row from the embedding table. | `[0.8, 0.2]` |
| `W_h` (weight matrix for memory) | **Initialised randomly** before training, then **learned** by backpropagation. The network adjusts these numbers over thousands of training examples until they produce good translations. | `[[0.1, 0.4], [0.3, 0.2]]` |
| `W_x` (weight matrix for word) | Same as W_h — **randomly initialised**, then **learned** during training. | `[[0.6, 0.1], [0.2, 0.7]]` |
| `b` (bias) | Also **learned** during training. We set it to zero here to keep the example simple. | `[0.0, 0.0]` |

So: `h0` comes from the previous step, `x1` comes from the embedding table, and `W_h`, `W_x`, `b` are all **learned parameters** that the network discovers during training. Nobody chooses these numbers by hand — the training process finds values that work.

**Given (made-up numbers for illustration):**

```text
Previous hidden state:  h0     = [0.5, -0.3]
New word vector:        x1     = [0.8,  0.2]    (the word "I")

Weight matrix for memory:  W_h = [[0.1, 0.4],
                                   [0.3, 0.2]]

Weight matrix for word:    W_x = [[0.6, 0.1],
                                   [0.2, 0.7]]

Bias:                      b   = [0.0, 0.0]     (zero for simplicity)
```

**Sub-step 1 — Transform the memory (W_h × h0):**

This is matrix-vector multiplication. Each output number is a dot product of one row of W_h with h0:

```text
row 1:  0.1 × 0.5  +  0.4 × (-0.3)  =  0.05 + (-0.12)  =  -0.07
row 2:  0.3 × 0.5  +  0.2 × (-0.3)  =  0.15 + (-0.06)  =   0.09

W_h × h0 = [-0.07, 0.09]
```

**Sub-step 2 — Transform the new word (W_x × x1):**

```text
row 1:  0.6 × 0.8  +  0.1 × 0.2  =  0.48 + 0.02  =  0.50
row 2:  0.2 × 0.8  +  0.7 × 0.2  =  0.16 + 0.14  =  0.30

W_x × x1 = [0.50, 0.30]
```

**Sub-step 3 — Add them together (+ bias):**

```text
[-0.07, 0.09]  +  [0.50, 0.30]  +  [0.0, 0.0]  =  [0.43, 0.39]
```

This is the only step that uses plain addition — and it is adding two **transformed** vectors, not the raw inputs.

**Sub-step 4 — Squash with tanh:**

tanh pushes every number into the range [−1, +1]:

```text
tanh(0.43) = 0.41
tanh(0.39) = 0.37

h1 = [0.41, 0.37]   ← the new hidden state
```

**Summary of what happened:**

```text
h0 = [0.5, -0.3]    (old memory)
x1 = [0.8, 0.2]     (new word "I")
        ↓
   matrix multiply each with learned weights
        ↓
   add the two transformed results
        ↓
   squash with tanh
        ↓
h1 = [0.41, 0.37]   (updated memory)
```

The weight matrices decide **how much** of the old memory to keep and **how much** of the new word to absorb. During training, the network adjusts these weights so that the final hidden state captures the most useful information from the sentence.

#### Quick reference table

| Symbol | What it is | Plain English |
|--------|-----------|---------------|
| `x_t` | The embedding vector of the current word | The new word the encoder is reading right now |
| `h_{t-1}` | The previous hidden state | The encoder's memory from all previous words |
| `W_x` | A weight matrix for the word | Controls how the new word is transformed |
| `W_h` | A weight matrix for the memory | Controls how the old memory is transformed |
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

### How many layers do the encoder and decoder have?

So far we showed a **single-layer** RNN — one set of weights processes the word vectors. But in practice, encoder-decoders stack **multiple layers** on top of each other. This is called a **stacked** or **deep** RNN.

#### Single layer (what we showed above)

```text
word vectors:   x1 → x2 → x3
                 ↓     ↓     ↓
Layer 1:        h1 → h2 → h3  → context vector
```

One layer reads the words left to right and produces one hidden state per word.

#### Stacked layers (what real models use)

```text
word vectors:    x1  →  x2  →  x3
                  ↓      ↓      ↓
Layer 1:        h1¹ → h2¹ → h3¹        (captures basic patterns)
                  ↓      ↓      ↓
Layer 2:        h1² → h2² → h3²        (captures deeper patterns)
                  ↓      ↓      ↓
Layer 3:        h1³ → h2³ → h3³        (captures even deeper patterns)
                                 ↓
                          context vector = h3³
```

Each layer takes the outputs of the layer below as its input. The bottom layer sees the raw word vectors. The next layer sees the hidden states from below, and learns **higher-level patterns** from them — like understanding phrase structure or sentence meaning rather than just individual words.

#### Typical numbers

| Model | Encoder layers | Decoder layers | Hidden size |
|-------|---------------|----------------|-------------|
| Simple seq2seq (tutorial) | 1 | 1 | 256 |
| Google's original NMT (2016) | 4 | 4 | 1,024 |
| Larger production models | 4–8 | 4–8 | 512–1,024 |

**More layers = more capacity to learn complex patterns**, but also slower to train and more likely to overfit on small datasets. The encoder and decoder usually have the **same number of layers** so the hidden states match in size when passing the context vector.

The decoder works the same way — if it has 3 layers, each decoder step runs through all 3 layers before predicting the next word.

---

## 6. The context vector

Let's zoom in on the hand-off between the two networks. From the walkthrough in section 5, the encoder's final hidden state was:

```text
"I love cats" → context vector c = h3 = [0.52, 0.71, 0.33, -0.19]
```

This single vector (in real models 256 or 512 numbers) is the bridge between the encoder and decoder. It must summarise the **entire input sentence**, because it is the only thing the decoder receives.

This is both the power and the weakness of this design:

- **Power:** any input length gets compressed to the same fixed size, so the decoder always knows what to expect.
- **Weakness:** a 50-word sentence must squeeze into the same space as a 3-word sentence — information gets lost. (This is the paint-mixing problem from section 5, and it is the main motivation for **attention** in Part 3.)

---

## 7. The decoder

Now for the second network. The decoder is another RNN — it works with a hidden state just like the encoder, but its job is reversed: instead of reading words to build a summary, it **starts from the summary** (the context vector) and unfolds it into words, one at a time.

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
2. Updates its hidden state — same mixing operation as the encoder, but with the decoder's own weights
3. Predicts the next word using a **softmax** over the vocabulary

**What is softmax?** The decoder's final layer produces one score for every word in the vocabulary (e.g. 30,000 scores). Softmax converts these scores into **probabilities** that add up to 1. The word with the highest probability is picked as the next output word:

```text
Decoder scores  →  softmax  →  P("J'") = 0.72, P("Je") = 0.15, P("Le") = 0.04, ...
                                        ↓
                              pick "J'" (highest probability)
```

### Training vs inference

The decoder behaves **differently** depending on whether it is being trained or being used. First, the two terms:

- **Training:** the model is learning. We have the correct translation ("J'aime les chats") and we are adjusting the weights.
- **Inference:** the model is being used for real. There is no correct answer available — the model is on its own.

The difference is in **what we feed into each decoder step as the "previous word."**

#### During inference: the model uses its own predictions

There is no other choice — we do not know the correct answer. Whatever the model predicted at step 1 becomes the input for step 2:

```text
Step 1: <START>          → predicts "J'"
Step 2: "J'" (own guess) → predicts "aime"
Step 3: "aime"           → predicts "les"
...
```

The danger: if the model makes a mistake early, that mistake is fed into the next step, which can cause another mistake — **errors compound**:

```text
Step 1: <START>            → predicts "Le"  ✗ (wrong! should be "J'")
Step 2: "Le" (wrong input) → predicts "chat" ✗ (now even more off track)
Step 3: "chat"             → predicts "est"  ✗ (the sentence is derailed)
```

#### During training: we feed in the correct word instead (teacher forcing)

During training, we **know** the correct translation. So even if the model predicts the wrong word, we ignore its prediction and feed in the **correct** word for the next step:

```text
Step 1: <START>              → predicts "Le"  ✗ (wrong — the loss records this mistake)
Step 2: "J'" (correct word,  → predicts "aime" ✓ (back on track, because
        not the model's guess)                     the input was corrected)
Step 3: "aime" (correct)     → predicts "les"  ✓
...
```

This is called **teacher forcing**. The model's wrong prediction at step 1 still counts against it in the loss (so it learns from the mistake), but the mistake is **not allowed to poison the following steps**.

**Why do this?** Without teacher forcing, one early error would derail the whole sentence, and the model would waste time learning from garbage inputs at steps 2, 3, 4... With teacher forcing, every step trains on a sensible input, so learning is faster and more stable.

**The trade-off:** during training, the model always receives perfect inputs — it never practises recovering from its own mistakes. Then at inference time it suddenly has to live with its own (sometimes wrong) predictions. This mismatch is a known weakness called **exposure bias**.

#### Summary

| | Training (teacher forcing) | Inference |
|---|---|---|
| Do we know the correct answer? | Yes — it is in the training data | No |
| Input to each step | The **correct** previous word from the training data | The word the model **actually predicted** at the previous step |
| What happens after a wrong prediction? | The mistake is recorded in the loss, but the next step still gets the correct word | The mistake is fed into the next step — errors compound |
| Speed and stability | Faster, more stable | Slower, errors can compound |

**Analogy:** teacher forcing is like a teacher who always tells the student the right answer before asking the next question. The student learns each question well, but never practises recovering after getting one wrong — which is exactly what they must do in the real exam (inference).

---

## 8. Putting it all together

Here is the whole pipeline in one picture — embeddings feed the encoder, the encoder compresses to a context vector, and the decoder unfolds it into the output sentence:

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

## 9. A concrete example: English → French

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

## 10. Loss function: cross-entropy

At each decoder step, the network predicts a probability distribution over the entire vocabulary. The loss measures how far that distribution is from the correct word.

```text
At step 2, the correct word is "aime".
The model predicts: P("aime") = 0.7, P("adore") = 0.15, P("chat") = 0.05, ...

Cross-entropy loss = -log(0.7) = 0.36
```

The total loss for the sentence is the sum (or average) of the losses at each step. Backpropagation flows through the decoder, through the context vector, and back into the encoder — so both halves learn together.

---

## 11. Common applications

| Task | Input | Output |
|------|-------|--------|
| Machine translation | "I love cats" | "J'aime les chats" |
| Text summarisation | A long article | A short summary |
| Chatbot | User message | Bot reply |
| Text-to-SQL | "Show me all users over 30" | `SELECT * FROM users WHERE age > 30` |
| Image captioning | An image (CNN features) | "A dog running on a beach" |

In image captioning, the encoder is a **CNN** instead of an RNN — it compresses the image into a vector. The decoder is still an RNN that generates text.

---

## 12. PyTorch sketch

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

## 13. Summary

- The **encoder** reads the input sequence and compresses it into a **context vector**.
- The **decoder** starts from the context vector and generates the output sequence one word at a time.
- During training, **teacher forcing** feeds the correct previous word to the decoder; during inference, the model uses its own predictions.
- The loss is **cross-entropy** at each output step, and backpropagation trains both encoder and decoder together.
- This architecture powers translation, summarisation, chatbots, and more.
- The main weakness is that the entire input is squeezed into **one fixed-size vector** — long sentences lose information. The next part shows how **attention** fixes this.

**Next:** [Part 3: Attention-Based Encoder-Decoder Architecture]({{ site.baseurl }}/topics/dl-genai-attention-encoder-decoder/)
