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

To understand this, we need to think about **what the training process actually does** to the vectors.

#### Step 1: Training creates clusters

Recall from section 3 that words appearing in similar contexts get similar vectors. So the training data naturally creates clusters:

```text
Cluster of "male person" words   → man, boy, he, him, father, king, prince ...
Cluster of "female person" words → woman, girl, she, her, mother, queen, princess ...
```

Within each cluster, the words are close to each other. But the model also notices something deeper.

#### Step 2: Training preserves parallel relationships

Think about how "man" and "woman" appear in text. They show up in **exactly the same patterns**, just swapped:

```text
"He is the king of England."     ↔  "She is the queen of England."
"The man wore a crown."          ↔  "The woman wore a crown."
"He became a prince at birth."   ↔  "She became a princess at birth."
```

Because these pairs always appear in mirror-image sentences, the model learns that the **difference** between each male word and its female counterpart is **the same**. In vector terms:

```text
woman - man  ≈  queen - king  ≈  princess - prince  ≈  she - he
```

All of these give roughly the same vector — a direction we can call **"gender."**

The same thing happens for other relationships:

```text
king - man  ≈  queen - woman       → the "royalty" direction
Paris - France  ≈  Tokyo - Japan   → the "capital city" direction
walked - walk  ≈  swam - swim      → the "past tense" direction
```

#### Step 3: Parallel relationships form a grid

Because these differences are consistent, the words arrange themselves into a **grid-like pattern** in vector space:

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

The arrow from "man" to "king" and the arrow from "woman" to "queen" point in the **same direction** and have the **same length** (royalty). The arrow from "man" to "woman" and from "king" to "queen" also point in the same direction and have the same length (gender).

This grid is not designed — it **emerges** from the training data. The model finds that organising words this way is the most efficient way to predict context, because it can reuse the same "gender" offset and the same "royalty" offset across many word pairs.

#### Analogy: a spreadsheet

Think of it like a spreadsheet where each row is a person:

| Person | Royalty score | Gender score |
|--------|--------------|--------------|
| man    | 1            | 0            |
| woman  | 1            | 1            |
| king   | 5            | 0            |
| queen  | 5            | 1            |

If you want to go from "man" to "king," you add 4 to the royalty column. If you want to go from "man" to "woman," you add 1 to the gender column. These transformations work for **any** row — that is why the arithmetic works.

#### Why "≈" and not "="?

In practice, the result is **approximate** — `king - man + woman` gives a vector close to "queen" but not exactly equal. This is because:

- Real embeddings have 300 dimensions, not 2, and the relationships are spread across many dimensions.
- Words have multiple meanings and associations that create noise.
- The training data is not perfectly balanced.

So we find the word whose vector is **closest** (by cosine similarity) to the result, and that word is usually "queen."

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

### More examples (all verified on real Word2Vec embeddings)

These are real results people have gotten using Google's pre-trained Word2Vec model:

**Example 1: king − man + woman ≈ queen**

You already know this one. We remove "maleness" from "king" and add "femaleness." The closest word to the result is "queen."

**Example 2: doctor − man + woman ≈ nurse**

This one is interesting — and controversial. The model learned from news and web text where "doctor" appeared more often with "he" and "nurse" appeared more often with "she." The arithmetic picks up that bias from the data. It shows that embeddings reflect the **real patterns in the training text**, including societal biases.

**Example 3: Japan − Tokyo + Paris ≈ France**

Here the logic is: remove the capital city of Japan from Japan, and add the capital city of France. What is left is the country — France. The model learned this because sentences like "Tokyo is the capital of Japan" and "Paris is the capital of France" appear in similar patterns.

**Example 4: eating − eat + drink ≈ drinking**

Remove the base verb from the "-ing" form, and add a different base verb. The result is that verb's "-ing" form. This works because the model sees "I am eating" and "I am drinking" in the same sentence patterns, so the offset from "eat" to "eating" is the same as from "drink" to "drinking."

**How to read any word arithmetic**

Every example follows the same pattern:

```text
A - B + C ≈ D

Meaning: "A is to B as D is to C"
   or:   "Take the relationship between A and B, apply it to C"
```

For example:
- king is to man as **queen** is to woman
- eating is to eat as **drinking** is to drink
- Japan is to Tokyo as **France** is to Paris

### The key insight

Nobody programmed these relationships. The network discovered them **on its own** by reading billions of words and learning which words appear in similar contexts. The fact that simple vector arithmetic recovers human-like analogies is what makes word embeddings so powerful — and it also means they inherit whatever biases exist in the training data.

---

## 6. Measuring similarity: cosine similarity

We said similar words have similar vectors — but how do we measure "similar"? The standard answer is **cosine similarity**.

### The intuition: direction, not length

Imagine two arrows starting from the same point. Cosine similarity measures the **angle** between them:

```text
Small angle  → arrows point the same way  → words are similar
Right angle  → arrows point in unrelated directions  → words are unrelated
Opposite     → arrows point in opposite directions
```

It only cares about **direction**, not how long the arrows are. This is important because during training some words might end up with larger vectors than others (common words tend to have longer vectors). We do not want "cat" and "dog" to look different just because one vector happens to be longer — we care about whether they point in the same direction.

### The formula

```text
cos(A, B) = (A · B) / (|A| × |B|)
```

Let's unpack each piece:

- **A · B** is the **dot product** — multiply each pair of numbers and add them up.
- **|A|** is the **length** of vector A — how far the arrow reaches from the origin.
- Dividing by both lengths **normalises** the result so it always falls between −1 and +1.

The result means:

| Cosine similarity | Meaning |
|-------------------|---------|
| **1.0** | Vectors point in exactly the same direction — very similar |
| **0.0** | Vectors are perpendicular — no relationship |
| **−1.0** | Vectors point in opposite directions |

### Worked example with simple numbers

Suppose we have two 3-dimensional word vectors:

```text
A = "cat"  = [1, 2, 3]
B = "dog"  = [2, 3, 4]
```

**Step 1: Dot product (A · B)**

Multiply each pair and add:

```text
A · B = (1×2) + (2×3) + (3×4)
      = 2 + 6 + 12
      = 20
```

**Step 2: Length of each vector**

```text
|A| = √(1² + 2² + 3²) = √(1 + 4 + 9) = √14 ≈ 3.74
|B| = √(2² + 3² + 4²) = √(4 + 9 + 16) = √29 ≈ 5.39
```

**Step 3: Divide**

```text
cos(A, B) = 20 / (3.74 × 5.39)
          = 20 / 20.15
          ≈ 0.99
```

A cosine similarity of **0.99** means "cat" and "dog" point in almost exactly the same direction — very similar. (These are made-up numbers, but the process is the same with real 300-dimensional embeddings.)

### Now compare with an unrelated word

```text
C = "car" = [5, -1, 0]

A · C = (1×5) + (2×-1) + (3×0) = 5 - 2 + 0 = 3

|C| = √(25 + 1 + 0) = √26 ≈ 5.10

cos(A, C) = 3 / (3.74 × 5.10)
          = 3 / 19.07
          ≈ 0.16
```

Only **0.16** — almost perpendicular. "Cat" and "car" have very little in common.

### Real-world cosine similarity values

These are approximate values from Google's pre-trained Word2Vec model:

```text
cos("cat", "dog")    = 0.76   ← both are pets, very similar
cos("cat", "kitten") = 0.79   ← a kitten is a baby cat
cos("cat", "car")    = 0.15   ← unrelated, just similar spelling
cos("king", "queen") = 0.73   ← both royalty
cos("good", "bad")   = 0.47   ← related (both describe quality) but different meaning
cos("good", "table") = 0.08   ← almost no connection
```

Notice that "good" and "bad" are somewhat similar (0.47) even though they are opposites. This is because they appear in **the same kinds of sentences** — "the food was good" and "the food was bad." Cosine similarity measures whether words appear in similar contexts, not whether they mean the same thing.

### Why not just use Euclidean distance?

You might wonder: why not just measure the straight-line distance between two vectors instead?

```text
Euclidean distance = √((a1-b1)² + (a2-b2)² + ...)
```

The problem is that Euclidean distance is affected by **vector length**. A word that appears very frequently (like "the") might have a longer vector than a rare word (like "platypus"). Euclidean distance would say they are far apart even if they point in a similar direction. Cosine similarity ignores length and focuses purely on direction, which is a better measure of meaning.

```text
A = [1, 2]       (short vector)
B = [100, 200]   (long vector, but same direction)

Euclidean distance = very large (they look far apart)
Cosine similarity  = 1.0 (they point the same way — identical meaning)
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
