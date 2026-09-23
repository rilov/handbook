---
layout: topic
title: "Deep Learning for Generative AI — Part 1: Word Embeddings"
category: Generative AI
order: 101
permalink: /topics/dl-genai-word-embeddings/
tags:
  - generative-ai
  - deep-learning
  - word-embeddings
  - word2vec
  - nlp
  - beginners
  - friendly
summary: "A beginner-friendly guide to word embeddings — how computers turn words into numbers so they can understand meaning, similarity, and relationships."
---

# Deep Learning for Generative AI — Part 1: Word Embeddings

Before a neural network can work with text, it needs to turn every word into a list of numbers. That list is called a **word embedding**. This part explains why we need them, how they work, and how they capture meaning.

---

## 1. The problem: computers don't understand words

A neural network only works with numbers. If you give it the sentence:

```text
"The cat sat on the mat"
```

It has no idea what "cat" or "mat" means. We need a way to convert each word into numbers.

---

## 2. The simplest approach: one-hot encoding

One-hot encoding gives each word a unique index in a long vector of zeros.

**Example** — suppose our vocabulary has only four words:

| Word | Index | One-hot vector |
|------|-------|----------------|
| cat  | 0     | [1, 0, 0, 0]  |
| sat  | 1     | [0, 1, 0, 0]  |
| on   | 2     | [0, 0, 1, 0]  |
| mat  | 3     | [0, 0, 0, 1]  |

### Why one-hot is bad

- **No meaning.** "cat" and "dog" are equally far apart as "cat" and "spaceship." The vectors tell us nothing about similarity.
- **Huge vectors.** Real vocabularies have 30,000–100,000 words. Each vector would be that long, mostly zeros.
- **No relationships.** There is no way to know that "king" is to "queen" as "man" is to "woman."

Think of it like giving every student in a school a locker number. The number tells you *which* locker, but nothing about the student.

---

## 3. Word embeddings: dense, meaningful vectors

A word embedding replaces the long one-hot vector with a short, dense vector — typically 50 to 300 numbers. These numbers are **learned** from data, so words that appear in similar contexts end up with similar vectors.

```text
One-hot  "cat" = [1, 0, 0, 0, 0, ..., 0]    # 30,000 numbers, almost all zero
Embedding "cat" = [0.25, -0.71, 0.33, 0.82]  # 4 numbers (in practice 50–300)
```

### But how does the model know "cat" and "dog" are similar?

The model never sees a dictionary or a picture. It learns from **context** — the words that appear around a word in real sentences. Consider these sentences from a training corpus:

```text
"The cat sat on the mat."
"I took my cat to the vet."
"She feeds her cat every morning."

"The dog sat on the mat."
"I took my dog to the vet."
"She feeds her dog every morning."
```

Notice that "cat" and "dog" appear in almost **identical surroundings** — next to "sat," "vet," "feeds," "morning," "mat." The model's job during training is to predict a word from its neighbours (or vice versa). Because "cat" and "dog" have the **same neighbours**, the model is forced to give them **similar vectors** — otherwise it could not make good predictions for both.

Now compare with the word "car":

```text
"The car drove down the highway."
"I parked my car in the garage."
"She washed her car on Sunday."
```

"Car" appears next to "drove," "highway," "parked," "garage" — completely different neighbours. So the model gives "car" a **very different vector** from "cat" or "dog."

**In short:** words that keep the same company get similar vectors. Words that keep different company get different vectors. The model does not understand meaning — it just notices patterns in who appears next to whom, and that is enough to capture meaning.

### Each number captures something

The 50–300 numbers in an embedding are not random. During training, each dimension ends up loosely representing some property. For example, one dimension might roughly capture "is it alive?", another might capture "is it big or small?", another "is it a positive or negative word?"

```text
             is-alive?   size   positivity   ...
"cat"     →  [ 0.9,      -0.3,    0.5,      ...]
"dog"     →  [ 0.8,      -0.1,    0.6,      ...]   ← similar to cat
"car"     →  [-0.7,       0.6,    0.2,      ...]   ← very different
"truck"   →  [-0.8,       0.9,    0.1,      ...]   ← similar to car
```

Nobody labels these dimensions — the model discovers them on its own. The exact meaning of each dimension is not always clean or interpretable, but the overall pattern is: **similar words → similar numbers**.

### Analogy: GPS coordinates

Think of each word as a city on a map. The embedding is like the latitude and longitude of that city. Cities that are close in meaning are close on the map:

```text
"cat"     → (2.1, 3.5)
"dog"     → (2.3, 3.4)     ← close to cat
"car"     → (8.7, 1.2)     ← far from cat
"truck"   → (8.5, 1.4)     ← close to car
```

Just as GPS coordinates tell you which cities are near each other without needing a picture, embeddings tell you which words are related without needing a dictionary.

---

## 4. How are embeddings learned? The Word2Vec idea

The most famous method is **Word2Vec** (Google, 2013). The key insight is:

> **"A word is known by the company it keeps."**

Word2Vec trains a small neural network to predict a word from its neighbours (or neighbours from a word). As it learns, the hidden layer weights become the embeddings.

### Two flavours

| Method | Task | Example |
|--------|------|---------|
| **CBOW** (Continuous Bag of Words) | Predict the centre word from surrounding words | "The ___ sat on the mat" → predict "cat" |
| **Skip-gram** | Predict surrounding words from the centre word | Given "cat" → predict "The," "sat," "on" |

### Skip-gram step by step

```text
Sentence: "The cat sat on the mat"

Window size = 2 (two words on each side)

For the word "sat":
  Input:   "sat"
  Targets: "The", "cat", "on", "the"

Training pairs:
  (sat, The)
  (sat, cat)
  (sat, on)
  (sat, the)
```

The network has one hidden layer. After training on millions of sentences, the hidden-layer weights for each word become its embedding.

---

## 5. The magic of word arithmetic

Once you have good embeddings, you can do arithmetic with words. The most famous example is:

```text
king - man + woman ≈ queen
```

That looks like magic, but it is really just vector addition and subtraction. Let's break it down.

### Why does it work?

During training, the network learns that certain **directions** in the vector space correspond to certain **concepts**. For example:

- There is a direction that means **"gender"** — moving along it turns "man" into "woman" or "king" into "queen."
- There is a direction that means **"royalty"** — moving along it turns "man" into "king" or "woman" into "queen."

Think of it as a 2D map:

```text
                  royalty →
                ┌─────────────────────┐
                │                     │
     gender ↓   │  man ─────→ king    │
                │   │           │     │
                │   ↓           ↓     │
                │  woman ────→ queen  │
                │                     │
                └─────────────────────┘
```

The arrow from "man" to "king" and the arrow from "woman" to "queen" point in the **same direction** (royalty). The arrow from "man" to "woman" and from "king" to "queen" also point in the same direction (gender).

### Worked example with simple numbers

Suppose our embeddings are just 2 numbers — one for "royalty" and one for "gender":

```text
man   = [1, 0]     (not royal, male)
woman = [1, 1]     (not royal, female)
king  = [5, 0]     (royal, male)
queen = [5, 1]     (royal, female)
```

Now do the arithmetic:

```text
king - man + woman
= [5, 0] - [1, 0] + [1, 1]
= [4, 0] + [1, 1]
= [5, 1]
= queen  ✓
```

Step by step, what happened:

1. **king − man = [4, 0]** — we removed the "man" part from "king," leaving behind the pure concept of "royalty."
2. **[4, 0] + woman = [5, 1]** — we added that royalty concept to "woman," giving us a royal woman — "queen."

### What does "subtract" really mean here?

Subtracting one word vector from another isolates the **difference** between them. That difference is a concept:

```text
king - man    = the "royalty" concept    [4, 0]
woman - man   = the "gender" concept     [0, 1]
Paris - France = the "capital" concept
walked - walk  = the "past tense" concept
```

When you add that concept to another word, you apply the same transformation:

```text
man   + (king - man)     = king     (make it royal)
walk  + (walked - walk)  = walked   (make it past tense)
France + (Paris - France) = Paris   (find the capital)
```

### More examples

| Question you are asking | Arithmetic | Result |
|------------------------|------------|--------|
| What is the capital of Italy? | Paris − France + Italy | ≈ Rome |
| What is the opposite of "big" for "small"? | bigger − big + small | ≈ smaller |
| What is the past tense of "swim"? | walked − walk + swim | ≈ swam |

### The key insight

Nobody programmed these relationships. The network discovered them **on its own** by reading billions of words and learning which words appear in similar contexts. The fact that simple vector arithmetic recovers human-like analogies is what makes word embeddings so powerful.

---

## 6. Measuring similarity: cosine similarity

To compare two word vectors, we use **cosine similarity** — the cosine of the angle between them.

```text
cos(A, B) = (A · B) / (|A| × |B|)
```

- **1.0** = identical direction (very similar)
- **0.0** = perpendicular (unrelated)
- **-1.0** = opposite direction

**Example:**

```text
cos("cat", "dog")   = 0.92   ← very similar
cos("cat", "car")   = 0.15   ← not similar
cos("king", "queen") = 0.87  ← similar (both royalty)
```

---

## 7. The embedding layer in a neural network

In practice, the embedding is just a **lookup table** stored as a matrix.

```text
Vocabulary size = V (e.g. 30,000 words)
Embedding size  = D (e.g. 300 dimensions)

Embedding matrix E has shape (V, D)
```

When the network sees word index `i`, it grabs row `i` from the matrix:

```text
word "cat" → index 42 → E[42] = [0.25, -0.71, 0.33, ...]
```

During training, the numbers in `E` are updated by backpropagation, just like any other weights.

### PyTorch example

```python
import torch
import torch.nn as nn

vocab_size = 10000
embed_dim = 300

embedding = nn.Embedding(vocab_size, embed_dim)

# Look up the embedding for word index 42
word_index = torch.tensor([42])
word_vector = embedding(word_index)

print(word_vector.shape)  # torch.Size([1, 300])
```

---

## 8. Pre-trained embeddings

Training embeddings from scratch needs a lot of data. Instead, you can use **pre-trained** embeddings that someone else trained on billions of words:

| Name | Creator | Dimensions | Trained on |
|------|---------|------------|------------|
| **Word2Vec** | Google | 300 | Google News (100 B words) |
| **GloVe** | Stanford | 50–300 | Wikipedia + CommonCrawl |
| **FastText** | Facebook | 300 | Wikipedia + CommonCrawl |

You load these vectors and plug them into your neural network. The network starts with good word representations instead of random numbers.

---

## 9. Limitations of static embeddings

Word2Vec and GloVe give each word **one** vector, no matter the context. But many words have multiple meanings:

```text
"bank" in "river bank"    → nature
"bank" in "bank account"  → finance
```

Both get the same vector. This is a big problem. Later models like **ELMo**, **BERT**, and **GPT** solve this by producing **contextual embeddings** — a different vector for the same word depending on the sentence. We will see these in later parts.

---

## 10. Summary

- Computers need words as numbers. **One-hot encoding** is simple but wasteful and meaningless.
- **Word embeddings** are short, dense vectors that capture meaning. Similar words have similar vectors.
- **Word2Vec** learns embeddings by predicting words from context (Skip-gram) or context from words (CBOW).
- Embeddings enable **word arithmetic**: king − man + woman ≈ queen.
- **Cosine similarity** measures how similar two word vectors are.
- An **embedding layer** is a simple lookup table that is trained with the rest of the network.
- Static embeddings give one vector per word regardless of context — a limitation solved by contextual models (coming next).

**Next:** [Part 2: Encoder-Decoder Architecture]({{ site.baseurl }}/topics/dl-genai-encoder-decoder/)
