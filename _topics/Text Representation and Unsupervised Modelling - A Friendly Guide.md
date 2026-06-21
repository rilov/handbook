---
title: "Text Representation and Unsupervised Modelling - A Friendly Guide"
category: Natural Language Processing
order: 8
tags:
  - nlp
  - text-representation
  - bag-of-words
  - tf-idf
  - word-embeddings
  - topic-modelling
  - nmf
  - unsupervised
  - beginners
  - friendly
summary: Learn how computers turn raw text into numbers, and how to discover hidden topics in large collections of documents—without any labelled data. Covers Bag-of-Words, TF-IDF, Word Embeddings, and Topic Modelling with NMF.
---

# Text Representation and Unsupervised Modelling - A Friendly Guide

## Why This Guide Exists

Every machine learning algorithm works with numbers. Not words. So before you can do anything interesting with text, you need to answer one fundamental question: **how do you turn a sentence into numbers?**

The answer you choose has a massive impact on everything downstream. Get it wrong, and even a perfect model cannot save you. Get it right, and remarkably simple models can produce excellent results.

This guide walks through the main approaches—from the crude-but-surprisingly-effective Bag of Words, to TF-IDF, to modern Word Embeddings that capture meaning. Then it shows how these representations unlock powerful **unsupervised** techniques like Topic Modelling—where you discover the hidden themes in thousands of documents without any labelling.

---

## Section 1: The Problem — Computers Cannot Read

### Why "Banana" Means Nothing to a Computer

To you, "banana" immediately brings to mind a yellow fruit, a specific taste, something you find in a fruit bowl. To a computer, "banana" is just the character sequence b-a-n-a-n-a. It has no idea that "banana" is similar to "mango" or related to "fruit".

Machine learning algorithms need numbers. Specifically, they need vectors—lists of numbers where similar things produce similar vectors.

```
Human understanding:
  banana ≈ mango ≈ fruit  (semantically similar)
  banana ≠ justice        (semantically unrelated)

What the computer needs:
  banana → [0.2, 0.8, 0.1, ...]
  mango  → [0.3, 0.7, 0.1, ...]   ← close to banana!
  justice→ [-0.5, 0.1, 0.9, ...]  ← far from banana
```

The question is: how do we build this mapping from words to numbers?

---

## Section 2: Bag-of-Words — The Simple Starting Point

### The Core Idea

Imagine you have a bag. You read a document, and for every word you find, you throw a copy of that word into the bag. At the end, you count how many times each word appears.

That count vector **is** your document representation. You have thrown away:
- Word order ("I love cats" and "cats love I" look the same)
- Grammar
- Context

But you have kept the most important thing: **which words appear and how often**.

### Building a Bag-of-Words Step by Step

**Step 1: Build the vocabulary**

Collect all unique words across all documents.

```
Documents:
  Doc 1: "I love cats"
  Doc 2: "I love dogs"
  Doc 3: "dogs chase cats"

Vocabulary: [cats, chase, dogs, I, love]  ← sorted alphabetically
```

**Step 2: Represent each document as a count vector**

Each position corresponds to a vocabulary word.

| Document | cats | chase | dogs | I | love |
|----------|------|-------|------|---|------|
| Doc 1: "I love cats" | 1 | 0 | 0 | 1 | 1 |
| Doc 2: "I love dogs" | 0 | 0 | 1 | 1 | 1 |
| Doc 3: "dogs chase cats" | 1 | 1 | 1 | 0 | 0 |

**Step 3: Use these vectors in a machine learning model**

Now Doc 1 = `[1, 0, 0, 1, 1]` — a vector of numbers that any algorithm can work with.

### Python Example

```python
from sklearn.feature_extraction.text import CountVectorizer

documents = [
    "I love cats",
    "I love dogs",
    "dogs chase cats",
    "cats and dogs are pets"
]

# Build BoW model
vectorizer = CountVectorizer()
bow_matrix = vectorizer.fit_transform(documents)

# Show vocabulary
print("Vocabulary:", vectorizer.get_feature_names_out())
# ['and', 'are', 'cats', 'chase', 'dogs', 'love', 'pets']

# Show document vectors
import pandas as pd
df = pd.DataFrame(
    bow_matrix.toarray(),
    columns=vectorizer.get_feature_names_out(),
    index=[f"Doc{i+1}" for i in range(len(documents))]
)
print(df)
```

**Output:**
```
      and  are  cats  chase  dogs  love  pets
Doc1    0    0     1      0     0     1     0
Doc2    0    0     0      0     1     1     0
Doc3    0    0     1      1     1     0     0
Doc4    1    1     1      0     1     0     1
```

### The Problem with Raw Counts

Raw counts have a fundamental flaw: **common words dominate**.

In a collection of news articles, "the", "and", "said", "was" appear thousands of times. They swamp the signal from meaningful words like "parliament", "vaccine", or "earthquake".

Two ways to fix this:
1. Remove stopwords (already covered in Lexical Processing)
2. Use TF-IDF to weight words by how distinctive they are

---

## Section 3: TF-IDF — Rewarding the Distinctive Words

### The Intuition

TF-IDF answers one question: **how important is this word to this particular document, relative to the whole collection?**

A word is important to a document if:
1. It appears **frequently** in that document (TF — Term Frequency)
2. It appears **rarely** across all documents (IDF — Inverse Document Frequency)

Words that are common everywhere (the, and, is) score low on IDF because they appear in every document — they are not distinctive. Words that only appear in a few documents score high because they signal something specific.

### The Formula

```
TF-IDF(word, document) = TF(word, document) × IDF(word)
```

**Term Frequency (TF):**
```
TF = (number of times word appears in document) / (total words in document)
```

**Inverse Document Frequency (IDF):**
```
IDF = log(total documents / number of documents containing word)
```

The `log` is important — it dampens the effect so that a word appearing in 10 documents does not score 10x a word appearing in 1 document.

### Worked Example

**Corpus: 3 movie reviews**
```
Doc A: "the film was great the acting was superb"
Doc B: "the film was boring and slow"
Doc C: "superb acting and great direction"
```

**Compute TF for "superb" in Doc A:**
```
TF = 1 occurrence / 8 total words = 0.125
```

**Compute IDF for "superb":**
```
Total docs = 3
Docs containing "superb" = 2 (Doc A and Doc C)
IDF = log(3/2) = log(1.5) ≈ 0.18
```

**TF-IDF for "superb" in Doc A:**
```
TF-IDF = 0.125 × 0.18 ≈ 0.022
```

**Compute TF-IDF for "the" in Doc A:**
```
TF = 2/8 = 0.25
IDF = log(3/3) = log(1) = 0      ← "the" appears in all docs
TF-IDF = 0.25 × 0 = 0            ← zero! "the" is not distinctive
```

The word "the" gets zero importance, even though it is the most frequent word. "Superb" gets a meaningful score because it is distinctive.

### Python Example

```python
from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
    "the film was great the acting was superb",
    "the film was boring and slow",
    "superb acting and great direction"
]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

import pandas as pd
df = pd.DataFrame(
    tfidf_matrix.toarray().round(3),
    columns=vectorizer.get_feature_names_out(),
    index=["Doc A", "Doc B", "Doc C"]
)
print(df)
```

**Output (abbreviated):**
```
         acting  and  boring  direction  film  great  slow  superb   the   was
Doc A     0.337  0.0   0.000      0.000 0.254  0.254   0.0   0.254 0.508 0.508
Doc B     0.000  0.0   0.482      0.000 0.365  0.000   0.482 0.000 0.365 0.365
Doc C     0.337  0.0   0.000      0.482 0.000  0.337   0.0   0.337 0.000 0.000
```

Notice: "the" and "was" have high scores in Doc A just because they repeat — but in a real use case you would remove stopwords first. "boring" and "slow" strongly identify Doc B as unique. "direction" uniquely identifies Doc C.

### BoW vs TF-IDF: When to Use Each

| Situation | Better Choice |
|-----------|--------------|
| Short texts, simple classification | BoW |
| Document search / retrieval | TF-IDF |
| Comparing long documents | TF-IDF |
| Spam detection | Either works well |
| Fast baseline | BoW |
| Meaningful word weighting | TF-IDF |

---

## Section 4: Word Embeddings — Words as Locations in Space

### Why BoW and TF-IDF Are Still Limited

Both BoW and TF-IDF treat every word as completely independent. They have no idea that:
- "cat" and "kitten" are related
- "great" and "excellent" mean similar things
- "Paris" and "France" are connected (city + country)

This means two documents saying "the film was excellent" and "the movie was superb" would look very different to a BoW model — different vocabulary, low similarity score — even though they express the same opinion.

**Word embeddings** fix this.

### The Core Idea: Words Have Neighbours

The insight behind embeddings comes from linguistics: **you can learn a word's meaning from the company it keeps.**

If "kitten" and "cat" tend to appear near the same words ("fluffy", "meowed", "fur", "purring"), they probably mean similar things. If "king" and "queen" share many neighbours ("royal", "crown", "throne"), they are related.

By training a neural network to predict a word from its neighbours (or vice versa), each word ends up with a dense vector of numbers — its **embedding** — where words with similar meanings are close together in space.

### Famous Vector Arithmetic

Word embeddings encode semantic relationships as geometric directions in the vector space:

```
king - man + woman ≈ queen

Paris - France + Italy ≈ Rome

doctor - man + woman ≈ nurse   ← (reflects training data biases)
```

This is not magic — it emerges from the statistical patterns in how words co-occur in billions of sentences.

### Two Key Algorithms

#### Word2Vec (Google, 2013)

Two architectures for training:

**CBOW (Continuous Bag of Words):** Given surrounding words, predict the centre word.
```
"The ___ sat on the mat" → predict "cat"
Context: [The, sat, on, the, mat] → Target: cat
```

**Skip-gram:** Given the centre word, predict surrounding words.
```
"cat" → predict [The, sat, on, the, mat]
```

Skip-gram works better for rare words. CBOW is faster.

#### GloVe (Stanford, 2014)

GloVe (Global Vectors) works differently — instead of a neural network predicting words, it directly factorises the co-occurrence matrix. The result is similar high-quality embeddings with a cleaner mathematical story.

### Python Example: Using Pre-trained Word2Vec

```python
# pip install gensim
import gensim.downloader as api

# Download pre-trained embeddings (trained on Google News, 3 billion words)
print("Loading model... (this downloads ~1.6GB the first time)")
model = api.load("word2vec-google-news-300")

# Find similar words
print("Words similar to 'cat':")
for word, score in model.most_similar("cat", topn=5):
    print(f"  {word:<15} similarity: {score:.3f}")

print("\nWords similar to 'london':")
for word, score in model.most_similar("london", topn=5):
    print(f"  {word:<15} similarity: {score:.3f}")

# Vector arithmetic
print("\nking - man + woman =")
result = model.most_similar(positive=["king", "woman"], negative=["man"], topn=3)
for word, score in result:
    print(f"  {word:<15} score: {score:.3f}")

# Similarity between words
print(f"\nSimilarity (cat, dog):    {model.similarity('cat', 'dog'):.3f}")
print(f"Similarity (cat, banana): {model.similarity('cat', 'banana'):.3f}")
```

**Expected output:**
```
Words similar to 'cat':
  cats            similarity: 0.822
  dog             similarity: 0.760
  kitten          similarity: 0.726
  feline          similarity: 0.720
  puppy           similarity: 0.709

king - man + woman =
  queen           score: 0.711
  monarch         score: 0.636
  princess        score: 0.628

Similarity (cat, dog):    0.760
Similarity (cat, banana): 0.192
```

### Smaller Example: Training Your Own Embeddings

```python
from gensim.models import Word2Vec

# Small training corpus
sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "cat", "ate", "the", "fish"],
    ["the", "dog", "chased", "the", "cat"],
    ["dogs", "and", "cats", "are", "pets"],
    ["the", "dog", "fetched", "the", "ball"],
    ["fish", "swim", "in", "the", "river"],
]

# Train Word2Vec
model = Word2Vec(
    sentences,
    vector_size=50,   # embedding dimensions
    window=2,         # context window size
    min_count=1,      # minimum word frequency
    workers=4,
    epochs=100
)

# Find similar words
print("Most similar to 'cat':", model.wv.most_similar("cat", topn=3))
print("Most similar to 'dog':", model.wv.most_similar("dog", topn=3))
print(f"Similarity (cat, dog): {model.wv.similarity('cat', 'dog'):.3f}")
```

---

## Section 5: Topic Modelling — Finding Hidden Themes

### The Problem: You Have 100,000 Documents

Imagine you work at a newspaper archive. You have 100,000 articles spanning 20 years, and no one has ever tagged or categorised them. A new journalist asks: "What were the main topics covered?"

You cannot read them all. You cannot label them manually — there are too many and you do not know the categories in advance.

**Topic modelling** is the answer. It automatically discovers the hidden thematic structure of a document collection — with no labelled data at all.

### What Is a Topic?

In topic modelling, a **topic** is a probability distribution over words. The model discovers that certain words tend to appear together, and groups them into a theme.

For example, in a news archive, the model might discover:

**Topic 1 (Sport):** football, goal, player, match, stadium, team, score, league
**Topic 2 (Politics):** election, parliament, vote, minister, party, government, policy
**Topic 3 (Health):** hospital, doctor, vaccine, patient, treatment, disease, NHS

Nobody told the model these categories existed. It found them purely by noticing which words co-occur.

Each document is then described as a **mixture of topics**:
- "England won the match but the prime minister missed it" → 60% sport, 40% politics
- "The hospital trialled a new vaccine" → 100% health

### NMF: The Method Behind the Magic

**Non-negative Matrix Factorisation (NMF)** is a particularly intuitive approach to topic modelling.

The core idea: take your TF-IDF matrix (documents × words) and factorise it into two smaller matrices.

```
Documents × Words  ≈  Documents × Topics  ×  Topics × Words
    (big matrix)         (how much         (which words
                          each doc          define each
                          belongs to        topic)
                          each topic)
```

**Why "non-negative"?** Because negative values in a topic make no sense — you cannot have -0.3 of "football" in a topic. NMF forces all values to be ≥ 0, which makes the topics interpretable.

### Step-by-Step Example

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np

# Sample documents
documents = [
    "The football team won the championship match last night",
    "The election results show the winning party gained seats in parliament",
    "Doctors recommend the new vaccine for all adults at the hospital",
    "The player scored three goals in the final match of the season",
    "Government policy on healthcare spending was debated in parliament",
    "The hospital launched a new treatment programme for patients",
    "The football league announced the fixtures for next season",
    "The prime minister addressed parliament after the election",
    "Clinical trials for the new vaccine showed positive results",
    "The team's manager praised the players after their championship win",
]

# Step 1: Convert to TF-IDF
vectorizer = TfidfVectorizer(
    max_features=30,     # keep only top 30 words
    stop_words='english' # remove stopwords
)
tfidf_matrix = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()

# Step 2: Apply NMF to discover 3 topics
nmf_model = NMF(n_components=3, random_state=42, max_iter=500)
doc_topics = nmf_model.fit_transform(tfidf_matrix)  # how much each doc = each topic
topic_words = nmf_model.components_                  # which words define each topic

# Step 3: Display top words for each topic
print("DISCOVERED TOPICS")
print("=" * 50)
topic_labels = ["Topic A", "Topic B", "Topic C"]

for i, (topic, label) in enumerate(zip(topic_words, topic_labels)):
    top_word_indices = topic.argsort()[-8:][::-1]  # top 8 words
    top_words = [feature_names[j] for j in top_word_indices]
    print(f"\n{label}: {', '.join(top_words)}")

# Step 4: Show dominant topic for each document
print("\n\nDOCUMENT → TOPIC ASSIGNMENTS")
print("=" * 50)
for i, doc in enumerate(documents):
    dominant_topic = np.argmax(doc_topics[i])
    confidence = doc_topics[i][dominant_topic]
    print(f"Doc {i+1}: [{topic_labels[dominant_topic]}] (score: {confidence:.2f})")
    print(f"  '{doc[:55]}...'")
```

**Expected output:**
```
DISCOVERED TOPICS
==================================================

Topic A: football, match, team, season, player, championship, goals, league
Topic B: election, parliament, minister, party, government, policy, seats
Topic C: hospital, vaccine, treatment, patients, doctors, clinical, healthcare

DOCUMENT → TOPIC ASSIGNMENTS
==================================================
Doc 1: [Topic A] (score: 0.89)  'The football team won the championship...'
Doc 2: [Topic B] (score: 0.91)  'The election results show the winning...'
Doc 3: [Topic C] (score: 0.87)  'Doctors recommend the new vaccine...'
Doc 5: [Topic B] (score: 0.73)  'Government policy on healthcare...'  ← mixed
```

Notice Doc 5 (government policy on healthcare) is assigned to politics but with lower confidence — it mixes both politics and health vocabulary.

### Choosing the Number of Topics

One challenge with topic modelling: you have to decide how many topics to look for in advance.

**Too few topics** → overly broad, unmeaningful themes
**Too many topics** → overly specific, redundant themes

Common approaches:
- **Coherence score:** Measures how semantically similar the top words in each topic are. Higher = more coherent topics.
- **Try several values** and inspect results qualitatively

```python
from gensim.models import CoherenceModel
import gensim.corpora as corpora

# Tip: gensim's LDA also does topic modelling with coherence scoring
# For NMF, visually inspect topics for n=3,5,10,20 and pick the most interpretable
```

### Real-World Applications

| Use Case | How Topic Modelling Helps |
|----------|--------------------------|
| **Customer feedback** | Automatically surface top complaint themes from thousands of reviews |
| **News aggregation** | Tag articles by topic without manual labelling |
| **Research papers** | Discover research trends across thousands of papers over decades |
| **Legal documents** | Find the key subjects across contracts in a data room |
| **Social media monitoring** | Identify emerging conversation themes in real-time |
| **Support tickets** | Route tickets by discovered topic, not keyword rules |

---

## Section 6: How It All Fits Together

Here is how the three representation methods relate to each other:

```
Raw Text
    ↓
Preprocessing (tokenise, lowercase, remove stopwords, lemmatise)
    ↓
Choose representation:

┌─────────────┬──────────────────────────────────────────────────────┐
│ Bag-of-Words│ Fast, simple. Each word is independent. Good baseline│
├─────────────┼──────────────────────────────────────────────────────┤
│ TF-IDF      │ Downweights common words, upweights distinctive ones │
│             │ Better for search and document comparison            │
├─────────────┼──────────────────────────────────────────────────────┤
│ Embeddings  │ Words have relationships. "cat" ≈ "kitten".          │
│             │ Best for tasks needing semantic understanding        │
└─────────────┴──────────────────────────────────────────────────────┘
    ↓
Feed vectors into:
  - Supervised model → classification, sentiment, NER
  - Unsupervised model → topic modelling, clustering, search
```

---

## Section 7: Practice Questions

**1. Why does Bag-of-Words lose word order, and when does that not matter?**
<details><summary>Answer</summary>
BoW counts word occurrences without caring about position. This does not matter much for document classification (a review containing "terrible" and "slow" is negative regardless of order) but matters for sentiment nuance ("not good" vs "good not").
</details>

**2. A word appears in every document in your corpus. What is its IDF score?**
<details><summary>Answer</summary>
log(N/N) = log(1) = 0. Its TF-IDF score is zero — it is not distinctive to any document.
</details>

**3. What does a word embedding vector represent?**
<details><summary>Answer</summary>
A dense list of numbers (typically 100–300 dimensions) that positions the word in a semantic space where similar words are close together. The values are learned from patterns of word co-occurrence in large text corpora.
</details>

**4. What does NMF produce when applied to a TF-IDF matrix?**
<details><summary>Answer</summary>
Two matrices: one describing how much each document belongs to each topic, and one describing which words define each topic. Together they approximate the original TF-IDF matrix.
</details>

**5. You have 50,000 customer reviews and want to understand what people are complaining about — without any pre-defined categories. Which approach would you use?**
<details><summary>Answer</summary>
Topic modelling (e.g. NMF on a TF-IDF matrix). It is unsupervised — it discovers the complaint themes automatically from the data without needing labelled examples.
</details>

**6. Why do word embeddings outperform TF-IDF for semantic similarity tasks?**
<details><summary>Answer</summary>
TF-IDF treats every word as independent — "excellent" and "superb" look completely different. Word embeddings place semantically similar words close together in vector space, so documents with similar meaning get high similarity scores even if they use different vocabulary.
</details>

---

## Summary

| Technique | What It Does | Best For |
|-----------|-------------|----------|
| **Bag-of-Words** | Counts word occurrences in a document | Simple classification, fast baselines |
| **TF-IDF** | Weights words by how distinctive they are | Document search, comparison, retrieval |
| **Word Embeddings** | Places words in semantic space by meaning | Semantic similarity, modern NLP models |
| **Topic Modelling (NMF)** | Discovers hidden themes in document collections | Unsupervised analysis, content categorisation |

The journey from raw text to machine learning is: **clean → tokenise → represent → model**. This guide covered the representation step — the bridge that makes everything else possible.
