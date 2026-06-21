---
title: "Semantic Processing Part 1 - Word Meaning and Disambiguation"
category: Natural Language Processing
order: 6
tags:
  - nlp
  - semantic-processing
  - lexical-semantics
  - word-sense-disambiguation
  - distributional-semantics
  - beginners
  - friendly
summary: A beginner-friendly guide to how computers understand word meaning. Covers lexical semantics, word sense disambiguation, co-occurrence models, and how to measure word similarity using statistics.
---

# Semantic Processing Part 1 - Word Meaning and Disambiguation

## Why This Guide Exists

You have learned how to break text into words (lexical processing) and understand sentence structure (syntactic processing). Now comes the hardest part: **what do those words actually mean?**

The word "bank" appears in:
- "I went to the bank to deposit my cheque."
- "We sat on the river bank watching the ducks."

Same word. Completely different meanings. A computer that cannot tell the difference will make embarrassing mistakes.

This guide explains how computers tackle meaning—starting with the dictionary of word senses, all the way to learning meaning from patterns in text.

---

## What Is Semantic Processing?

**Semantic processing** is the stage where we go from structure to meaning. Instead of asking "what is this word?" (POS tagging) or "how does the sentence fit together?" (parsing), we ask **"what does this actually mean?"**

Think of the three stages like reading a recipe:
- **Lexical:** Identify the ingredients listed
- **Syntactic:** Understand the order of steps
- **Semantic:** Grasp *what the dish is* and *why each step matters*

---

## Section 1: Lexical Semantics — The Meaning of Individual Words

### Words Are Not Just Strings of Letters

When you read the word "bright", your brain instantly connects it to concepts: light, intelligence, colour, cheerfulness. You know it relates to "shine" and "glow". You know it is the opposite of "dull" and "dark". None of that is obvious from the letters B-R-I-G-H-T.

**Lexical semantics** is the study of word meaning and how words relate to one another.

### Four Key Relationships Between Words

#### 1. Synonyms — Same Meaning
Words that mean roughly the same thing.

| Word | Synonyms |
|------|----------|
| happy | joyful, glad, content, pleased |
| fast | quick, rapid, swift, speedy |
| begin | start, commence, initiate |

**Why it matters in NLP:** A search for "fast cars" should also find "rapid vehicles." If you treat words as just strings, you miss this connection.

#### 2. Antonyms — Opposite Meaning
Words with opposite meanings.

| Word | Antonym |
|------|---------|
| hot | cold |
| increase | decrease |
| optimistic | pessimistic |

**Why it matters in NLP:** Sentiment analysis must understand that "not bad" is positive, not negative. Antonym relationships help.

#### 3. Hyponyms and Hypernyms — Specific vs General
A **hyponym** is a more specific version. A **hypernym** is the broader category.

```
Animal (hypernym)
   ├── Dog (hyponym of Animal)
   │     ├── Labrador (hyponym of Dog)
   │     └── Poodle   (hyponym of Dog)
   └── Bird (hyponym of Animal)
         ├── Robin    (hyponym of Bird)
         └── Eagle    (hyponym of Bird)
```

**Why it matters in NLP:** A question about "animals in Australia" should include answers about "kangaroos" even if the document never uses the word "animal."

#### 4. Meronyms — Part-Whole Relationships
A **meronym** is a part of something.

- "wheel" is a meronym of "car"
- "chapter" is a meronym of "book"
- "sleeve" is a meronym of "shirt"

**Why it matters in NLP:** If someone asks "what are the parts of an engine?", the system needs to understand part-whole relationships.

### WordNet: The Lexical Database

All of these relationships are captured in **WordNet**, a large English lexical database built at Princeton.

In WordNet, words are grouped into **synsets** (synonym sets)—groups of words that share the same meaning.

```python
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

# Find synsets for "bank"
synsets = wordnet.synsets("bank")
for s in synsets:
    print(f"{s.name()}: {s.definition()}")

# Output (abbreviated):
# bank.n.01: sloping land (especially the slope beside a body of water)
# bank.n.02: a financial institution that accepts deposits
# bank.v.01: tip laterally (as of an aircraft during a turn)
```

```python
# Find synonyms for "happy"
synonyms = []
for syn in wordnet.synsets("happy"):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())

print(set(synonyms))
# {'felicitous', 'glad', 'happy', 'well-chosen'}

# Find antonyms
for syn in wordnet.synsets("happy"):
    for lemma in syn.lemmas():
        if lemma.antonyms():
            print(f"Antonym of happy: {lemma.antonyms()[0].name()}")
# Antonym of happy: unhappy
```

---

## Section 2: Word Sense Disambiguation — Which Meaning Did You Mean?

### The Problem of Polysemy

**Polysemy** is when a single word has multiple related meanings. This is extremely common in English.

| Word | Meaning 1 | Meaning 2 | Meaning 3 |
|------|-----------|-----------|-----------|
| bank | financial institution | river edge | to tilt an aircraft |
| bat | cricket bat | flying mammal | to hit |
| cold | low temperature | illness | unfriendly |
| run | to move fast | a score in cricket | to manage (a business) |
| light | illumination | not heavy | pale in colour |

A machine translation system that does not handle this will produce comically wrong outputs.

> "I went to the bank" translated to French must decide: *la banque* (financial) or *la rive* (river)?

### Word Sense Disambiguation (WSD)

**WSD** is the task of automatically determining which sense of a word is being used, based on context.

#### Approach 1: Dictionary-Based (Knowledge Methods)

Use a dictionary (like WordNet) to figure out which sense fits best.

**The Lesk Algorithm** — the classic approach:

1. Take the word to be disambiguated and its context words
2. Look up all senses of that word in a dictionary
3. Count how many context words overlap with each sense's definition
4. Pick the sense with the most overlap

**Example:**

Sentence: *"I deposited money at the bank."*
Context words: deposited, money, at

```
Sense 1 (financial): "a financial institution that accepts deposits and channels money into lending activities"
Overlap with context: deposits ✓, money ✓ → score: 2

Sense 2 (river): "sloping land beside a body of water"
Overlap with context: none → score: 0

Winner: Sense 1 (financial institution)
```

```python
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

def simple_lesk(sentence, ambiguous_word):
    """Simplified Lesk algorithm"""
    context = set(word_tokenize(sentence.lower()))
    best_sense = None
    max_overlap = 0
    
    for synset in wordnet.synsets(ambiguous_word):
        # Get definition words
        definition = set(word_tokenize(synset.definition().lower()))
        # Count overlap with context
        overlap = len(context & definition)
        
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = synset
    
    return best_sense

# Test
sentence1 = "I went to the bank to deposit my money"
sense1 = simple_lesk(sentence1, "bank")
print(f"Sentence: '{sentence1}'")
print(f"Sense: {sense1.definition()}")

sentence2 = "We sat on the grassy bank by the river"
sense2 = simple_lesk(sentence2, "bank")
print(f"\nSentence: '{sentence2}'")
print(f"Sense: {sense2.definition()}")
```

#### Approach 2: Context-Based (Machine Learning)

Train a classifier that looks at surrounding words to predict the correct sense.

**Features used:**
- The 2-3 words immediately before/after the target word
- Part-of-speech tags of surrounding words
- Topic of the document

**Example:**

| Context | Label |
|---------|-------|
| "deposited money at the **bank**" | financial |
| "river **bank** was muddy" | geography |
| "sat beside the **bank** of flowers" | edge/side |

A trained classifier learns: when "money" or "deposit" appears nearby → financial sense.

#### Approach 3: Modern Neural Methods

Modern systems use **word embeddings in context** (like BERT). The key insight: the same word produces different numerical vectors depending on surrounding words.

```
"bank" in "river bank" → vector: [0.2, -0.8, 0.5, ...]
"bank" in "deposit money" → vector: [0.9, 0.1, -0.3, ...]
```

These different vectors are then matched to the correct sense.

---

## Section 3: How Words Travel Together — Distributional Semantics

### The Core Idea: You Are Known by the Company You Keep

Here is a fascinating insight from linguistics: **you can figure out what a word means by looking at what other words appear near it.**

Consider these two sentences:
- "The *wampimuk* climbed the tree and ate some berries."
- "The *wampimuk* growled and showed its teeth."

You have never seen "wampimuk" before. But from the context, you can guess it is probably an animal. The words around it (climbed, tree, berries, growled, teeth) tell you everything.

This is the core idea of **distributional semantics**: *a word's meaning is reflected by the words it appears alongside.*

### Co-Occurrence Models

**Co-occurrence** simply means: which words tend to appear near each other?

We can build a **co-occurrence matrix**—a table showing how often each word appears in the same sentence (or window) as every other word.

**Example corpus:**
- "I love ice cream"
- "I love coffee"
- "Dogs love bones"
- "Dogs love running"

**Co-occurrence matrix (window = whole sentence):**

|       | I | love | ice | cream | coffee | dogs | bones | running |
|-------|---|------|-----|-------|--------|------|-------|---------|
| love  | 2 | 0    | 1   | 1     | 1      | 1    | 1     | 1       |
| ice   | 1 | 1    | 0   | 1     | 0      | 0    | 0     | 0       |
| dogs  | 0 | 1    | 0   | 0     | 0      | 0    | 1     | 1       |

**What this tells us:**
- "ice" and "cream" co-occur a lot → they are related
- "dogs" and "bones" co-occur → they are related
- "ice" and "dogs" do not co-occur → they are unrelated

This lets us build a picture of word meaning purely from data, with no human-crafted dictionaries.

```python
from collections import defaultdict

def build_cooccurrence_matrix(sentences, window_size=2):
    """Build a simple co-occurrence matrix"""
    cooccurrence = defaultdict(lambda: defaultdict(int))
    
    for sentence in sentences:
        words = sentence.lower().split()
        for i, word in enumerate(words):
            start = max(0, i - window_size)
            end = min(len(words), i + window_size + 1)
            
            for j in range(start, end):
                if i != j:
                    cooccurrence[word][words[j]] += 1
    
    return cooccurrence

# Example usage
sentences = [
    "I love ice cream",
    "I love coffee",
    "dogs love bones",
    "dogs love running"
]

matrix = build_cooccurrence_matrix(sentences)
print("Words near 'love':", dict(matrix['love']))
print("Words near 'dogs':", dict(matrix['dogs']))
```

### Pointwise Mutual Information (PMI)

Raw counts have a problem: common words like "the" and "is" will co-occur with everything, so they appear highly related to everything—even unrelated words.

**PMI solves this** by asking: *"Does this pair of words appear together more than you would expect by chance?"*

The formula:

```
PMI(word1, word2) = log( P(word1, word2) / (P(word1) × P(word2)) )
```

**In plain English:**

```
PMI = log( how often they appear together / how often you'd expect them together by chance )
```

- **PMI > 0:** Words appear together more than expected → they are related
- **PMI ≈ 0:** Words appear together about as expected → unrelated
- **PMI < 0:** Words appear together less than expected → they avoid each other

**Example:**

In a large text corpus:
- "ice" and "cream" appear together far more than chance → high positive PMI
- "dog" and "justice" rarely appear together → low or negative PMI

```python
import math
from collections import Counter

def compute_pmi(corpus_sentences):
    """Compute PMI for word pairs"""
    word_counts = Counter()
    pair_counts = Counter()
    total_words = 0
    
    for sentence in corpus_sentences:
        words = sentence.lower().split()
        total_words += len(words)
        for word in words:
            word_counts[word] += 1
        for i, w1 in enumerate(words):
            for w2 in words[i+1:]:
                pair = tuple(sorted([w1, w2]))
                pair_counts[pair] += 1
    
    pmi_scores = {}
    for (w1, w2), pair_count in pair_counts.items():
        p_w1 = word_counts[w1] / total_words
        p_w2 = word_counts[w2] / total_words
        p_pair = pair_count / total_words
        
        if p_w1 > 0 and p_w2 > 0:
            pmi = math.log2(p_pair / (p_w1 * p_w2))
            pmi_scores[(w1, w2)] = round(pmi, 2)
    
    return pmi_scores

# Example
sentences = [
    "ice cream is delicious",
    "cream cheese is tasty",
    "dogs eat bones",
    "dogs love their owners",
    "I love ice cream"
]

pmi = compute_pmi(sentences)
# Sort by PMI score
top_pairs = sorted(pmi.items(), key=lambda x: x[1], reverse=True)[:10]
for pair, score in top_pairs:
    print(f"{pair[0]:10} + {pair[1]:10} | PMI: {score}")
```

**Positive PMI (PPMI):** A common improvement is to clip all negative values to 0 (since negative PMI is unreliable with small datasets):

```python
ppmi = {pair: max(0, score) for pair, score in pmi.items()}
```

---

## Section 4: Practice Questions

**1. What is polysemy? Give an example.**
<details><summary>Answer</summary>
Polysemy is when a single word has multiple related meanings. Example: "cold" can mean low temperature, a viral illness, or an unfriendly attitude.
</details>

**2. What does the Lesk algorithm do to pick a word sense?**
<details><summary>Answer</summary>
It counts how many context words from the sentence overlap with each dictionary definition of the word, then picks the sense with the most overlap.
</details>

**3. What does a high PMI score between two words tell you?**
<details><summary>Answer</summary>
Those two words appear together far more often than you would expect by chance, meaning they are strongly associated.
</details>

**4. What is the difference between a synonym and a hyponym?**
<details><summary>Answer</summary>
Synonyms share the same meaning (happy / joyful). A hyponym is a more specific type of a broader category (Labrador is a hyponym of Dog).
</details>

**5. Why is raw co-occurrence count not always enough? What does PMI fix?**
<details><summary>Answer</summary>
Frequent words like "the" co-occur with everything, making them look related to every word. PMI normalises by how often the words would co-occur by chance, so only genuinely associated pairs score highly.
</details>

---

## What Comes Next?

Part 2 moves from individual word meaning to identifying *who is doing what to whom* in a sentence—covering Semantic Role Labelling, Named Entity Recognition, IOB tagging, Conditional Random Fields, and Coreference Resolution.
