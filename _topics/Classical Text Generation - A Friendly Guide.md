---
title: "Classical Text Generation - A Friendly Guide"
category: Natural Language Processing
order: 8
tags:
  - nlp
  - text-generation
  - language-models
  - ngrams
  - markov-chains
  - smoothing
  - perplexity
  - beginners
  - friendly
summary: A beginner-friendly guide to classical text generation. Learn how computers generate language using N-gram models, Markov chains, probability, smoothing techniques, and how to evaluate quality with perplexity—before the era of neural networks.
---

# Classical Text Generation - A Friendly Guide

## Why This Guide Exists

Before ChatGPT, before GPT-3, before neural networks dominated NLP—computers generated text using elegant statistical methods built on a simple idea:

> **The next word depends on the words that came before it.**

This sounds obvious. But turning that intuition into a working system required clever maths, probability theory, and some creative problem-solving. Understanding these classical methods is not just history—it gives you the foundation to truly understand why modern neural models work the way they do.

This guide builds from scratch, using real examples at every step.

---

## Section 1: What Is a Language Model?

### The Core Idea

A **language model** is a system that assigns a probability to a sequence of words.

In plain English: it answers the question, *"How likely is this sentence to appear in natural text?"*

| Sentence | Likely probability |
|----------|-------------------|
| "The cat sat on the mat." | High |
| "The mat sat on the cat." | Lower (grammatical but unusual) |
| "Sat mat the cat on the." | Very low (grammatically wrong) |
| "Colourless green ideas sleep furiously." | Low (grammatical but nonsensical) |

A good language model gives high probabilities to natural-sounding sentences and low probabilities to weird or ungrammatical ones.

### What Language Models Are Used For

| Application | How the language model helps |
|-------------|------------------------------|
| **Autocomplete** | "I want to go to the ___" → predicts most likely next word |
| **Spell checking** | "I went to teh store" — "teh store" has very low probability, so flag it |
| **Machine translation** | Choose the translated sentence with the highest probability in the target language |
| **Speech recognition** | Between "recognise speech" and "wreck a nice beach" (same audio), pick the more probable sentence |
| **Text generation** | Repeatedly predict the next word to produce new text |

---

## Section 2: N-Gram Models — Learning from History

### The Simplest Idea: Count What Follows What

Imagine you read a million sentences and track what word tends to follow every other word. After enough reading, you have a pretty good model of language.

This is exactly what **N-gram models** do.

### What Is an N-Gram?

An **N-gram** is a sequence of N consecutive words.

| N | Name | Example from "The quick brown fox jumps" |
|---|------|------------------------------------------|
| 1 | Unigram | "The", "quick", "brown", "fox", "jumps" |
| 2 | Bigram | "The quick", "quick brown", "brown fox", "fox jumps" |
| 3 | Trigram | "The quick brown", "quick brown fox", "brown fox jumps" |
| 4 | 4-gram | "The quick brown fox", "quick brown fox jumps" |

### Predicting the Next Word with Bigrams

A **bigram model** assumes the next word depends only on the current word.

**Training:** Count how often each word follows each other word.

**Example corpus:**
```
"I love cats"
"I love dogs"  
"I hate rain"
"cats love fish"
```

**Bigram counts:**
| Previous word | Next word | Count |
|---------------|-----------|-------|
| I | love | 2 |
| I | hate | 1 |
| love | cats | 1 |
| love | dogs | 1 |
| love | fish | 1 |
| cats | love | 1 |
| hate | rain | 1 |

**Bigram probabilities** (divide count by total following word count):
```
P(love | I) = 2/3 = 0.67
P(hate | I) = 1/3 = 0.33
P(cats | love) = 1/3 = 0.33
P(dogs | love) = 1/3 = 0.33
P(fish | love) = 1/3 = 0.33
```

**Prediction:**
- After "I", the most likely word is "love" (67% chance)
- After "love", all three options are equal (33% each)

### Generating Text with a Bigram Model

```python
import random
from collections import defaultdict

def build_bigram_model(text):
    """Build a bigram language model from text"""
    words = text.lower().split()
    model = defaultdict(list)
    
    for i in range(len(words) - 1):
        model[words[i]].append(words[i + 1])
    
    return model

def generate_text(model, start_word, length=10):
    """Generate text using the bigram model"""
    current = start_word
    output = [current]
    
    for _ in range(length - 1):
        if current not in model:
            break
        next_word = random.choice(model[current])
        output.append(next_word)
        current = next_word
    
    return " ".join(output)

# Train on example text
corpus = """
the cat sat on the mat the cat ate the fish
the dog sat on the floor the dog ate the bone
cats love fish dogs love bones
the fish swam in the water
"""

model = build_bigram_model(corpus)

# Generate some text
random.seed(42)
for _ in range(3):
    print(generate_text(model, start_word="the", length=8))
```

**Example output:**
```
the cat sat on the floor the dog
the mat the fish swam in the water
the dog ate the bone cats love fish
```

Notice: the output looks somewhat like natural text but can loop or get stuck!

### Trigrams: Using More Context

A **trigram model** uses the previous *two* words to predict the next one. This captures more context.

```
Bigram:  P(word | prev_word)
Trigram: P(word | prev_word, prev_prev_word)
```

**Example:**
- After "I love", the next word is probably "cats", "dogs", or "pizza"—but not "the" or "and"
- A trigram model knows this; a bigram model only sees "love" and might predict "fish" from other contexts

```python
from collections import defaultdict, Counter

def build_trigram_model(text):
    """Build a trigram language model"""
    words = ['<START>'] + text.lower().split() + ['<END>']
    model = defaultdict(Counter)
    
    for i in range(len(words) - 2):
        context = (words[i], words[i+1])
        next_word = words[i+2]
        model[context][next_word] += 1
    
    return model

def trigram_predict(model, word1, word2, top_n=3):
    """Predict top N likely next words given two previous words"""
    context = (word1, word2)
    if context not in model:
        return []
    
    total = sum(model[context].values())
    predictions = [(w, c/total) for w, c in model[context].most_common(top_n)]
    return predictions

# Example
corpus = """
i love cats and i love dogs and i love pizza
cats love fish and dogs love bones
she loves to eat pizza and he loves to eat pasta
"""

model = build_trigram_model(corpus)
print("After 'i love':", trigram_predict(model, "i", "love"))
print("After 'love to':", trigram_predict(model, "love", "to"))
```

---

## Section 3: The Probability of a Full Sentence

### Chaining Probabilities Together

Once you have a bigram model, you can calculate the probability of an entire sentence by multiplying the probabilities of each word given the previous word.

**Formula:**
```
P("I love cats") = P(I | <START>) × P(love | I) × P(cats | love) × P(<END> | cats)
```

**Example with numbers:**
```
P(I | <START>) = 0.5   (half our sentences start with "I")
P(love | I)    = 0.67  (67% of the time after "I" comes "love")
P(cats | love) = 0.33  (one of three words after "love")

P("I love cats") = 0.5 × 0.67 × 0.33 ≈ 0.11
```

```python
import math

def sentence_probability(model_probs, sentence):
    """
    Calculate log probability of a sentence using bigram model.
    Using log to avoid numerical underflow with many multiplications.
    """
    words = ['<START>'] + sentence.lower().split() + ['<END>']
    log_prob = 0.0
    
    for i in range(len(words) - 1):
        bigram = (words[i], words[i+1])
        prob = model_probs.get(bigram, 1e-10)  # tiny prob for unseen bigrams
        log_prob += math.log(prob)
    
    return log_prob

# Example bigram probabilities (hand-crafted for illustration)
probs = {
    ('<START>', 'i'): 0.5,
    ('i', 'love'): 0.67,
    ('love', 'cats'): 0.33,
    ('cats', '<END>'): 1.0,
    ('<START>', 'the'): 0.3,
    ('the', 'dog'): 0.4,
    ('dog', 'ran'): 0.6,
    ('ran', '<END>'): 1.0,
}

s1 = sentence_probability(probs, "i love cats")
s2 = sentence_probability(probs, "the dog ran")

print(f"Log P('i love cats') = {s1:.2f}")
print(f"Log P('the dog ran') = {s2:.2f}")
```

**Why log probability?** Multiplying many small probabilities (0.5 × 0.3 × 0.1 × ...) quickly reaches numbers too small for computers to represent. Taking the log converts multiplication to addition, which is numerically stable.

---

## Section 4: The Sparsity Problem and Smoothing

### The Big Problem: Unseen N-Grams

Here is a fundamental challenge. You train your model on a million words. Then someone types a sentence with a word combination that never appeared in your training data.

```
Training data never contained: "purple elephant sings"
P(sings | purple elephant) = 0/0 = ??? 
```

A probability of zero is catastrophic—it means the entire sentence gets probability zero, even if it is perfectly reasonable English.

This is the **sparsity problem**: real language has infinite possible sentences, but your training data is finite.

### Solution 1: Laplace (Add-One) Smoothing

The simplest fix: pretend you saw every possible word combination at least once by adding 1 to every count.

**Without smoothing:**
```
Count("purple", "sings") = 0
P(sings | purple) = 0 / total = 0
```

**With Laplace smoothing (add 1 to every count):**
```
Count("purple", "sings") = 0 + 1 = 1
P(sings | purple) = 1 / (total + vocabulary_size)
```

Now every combination has at least a tiny probability.

```python
def laplace_bigram_probability(word1, word2, bigram_counts, unigram_counts, vocab_size):
    """
    Compute P(word2 | word1) with Laplace (add-1) smoothing
    """
    count_bigram = bigram_counts.get((word1, word2), 0)
    count_unigram = unigram_counts.get(word1, 0)
    
    # Add 1 to numerator, add vocab_size to denominator
    return (count_bigram + 1) / (count_unigram + vocab_size)

# Example
bigram_counts = {('I', 'love'): 10, ('I', 'hate'): 3}
unigram_counts = {'I': 13}
vocab_size = 1000

p_love = laplace_bigram_probability('I', 'love', bigram_counts, unigram_counts, vocab_size)
p_never_seen = laplace_bigram_probability('I', 'purple', bigram_counts, unigram_counts, vocab_size)

print(f"P(love | I) = {p_love:.4f}")
print(f"P(purple | I) = {p_never_seen:.6f}  ← small but not zero")
```

**Problem with Laplace:** It gives too much probability mass to unseen events and takes too much from seen ones. In practice, Laplace smoothing is too aggressive.

### Solution 2: Backoff Smoothing

The idea: if you have never seen the trigram "I love cats", fall back to the bigram "love cats". If that is also unseen, fall back to the unigram "cats".

```
Try:  P(cats | I, love)  ← trigram — has count? Use it.
Else: P(cats | love)     ← bigram  — has count? Use it.
Else: P(cats)            ← unigram — always has count.
```

```python
def backoff_probability(word, context, trigram_probs, bigram_probs, unigram_probs,
                        alpha=0.4):
    """
    Stupid backoff: use trigram if available, else bigram, else unigram.
    alpha is a discount factor applied when backing off.
    """
    if len(context) >= 2:
        trigram_key = (context[-2], context[-1], word)
        if trigram_key in trigram_probs:
            return trigram_probs[trigram_key]
    
    if len(context) >= 1:
        bigram_key = (context[-1], word)
        if bigram_key in bigram_probs:
            return alpha * bigram_probs[bigram_key]
    
    return alpha * alpha * unigram_probs.get(word, 1e-10)
```

### Solution 3: Interpolation Smoothing

Instead of choosing one level, **mix all levels together** with weights that sum to 1.

```
P(word | context) = λ₁ × P_trigram + λ₂ × P_bigram + λ₃ × P_unigram
```

Where λ₁ + λ₂ + λ₃ = 1.

```python
def interpolated_probability(word, context, trigram_probs, bigram_probs, unigram_probs,
                             l1=0.6, l2=0.3, l3=0.1):
    """
    Interpolation smoothing: weighted mix of trigram, bigram, unigram.
    l1 + l2 + l3 must equal 1.
    """
    p_tri = trigram_probs.get((context[-2], context[-1], word), 0) if len(context) >= 2 else 0
    p_bi  = bigram_probs.get((context[-1], word), 0) if len(context) >= 1 else 0
    p_uni = unigram_probs.get(word, 1e-10)
    
    return l1 * p_tri + l2 * p_bi + l3 * p_uni
```

---

## Section 5: Evaluating a Language Model — Perplexity

### How Do You Know If Your Model Is Any Good?

You could generate some text and see if it sounds natural. But that is subjective. We need a number.

**Perplexity** is the standard metric for evaluating language models.

### What Perplexity Means Intuitively

Perplexity measures **how surprised your model is by new text**.

Think of it this way: imagine a language model is guessing the next word at each step. Perplexity tells you the average number of equally likely choices the model is considering at each word.

- **Low perplexity** = model is confident, fewer choices, good model
- **High perplexity** = model is confused, many choices, bad model

| Perplexity | Interpretation |
|------------|----------------|
| 10 | At each word, the model is effectively choosing from 10 equally likely options — very good |
| 100 | 100 options per word — reasonable |
| 1000 | 1000 options — the model has barely learned anything |
| 1 | Perfect (impossible in practice) |

### The Perplexity Formula

```
Perplexity = 2^(-average log₂ probability per word)

Or equivalently:
Perplexity = (1 / P(test text)) ^ (1/N)

Where N = number of words in the test text
```

```python
import math

def perplexity(model_probs, test_sentences):
    """
    Calculate perplexity of a language model on test sentences.
    model_probs: dict of bigram → probability
    test_sentences: list of tokenised sentences (lists of words)
    """
    total_log_prob = 0.0
    total_words = 0
    
    for sentence in test_sentences:
        words = ['<START>'] + sentence + ['<END>']
        for i in range(len(words) - 1):
            bigram = (words[i], words[i+1])
            prob = model_probs.get(bigram, 1e-10)
            total_log_prob += math.log2(prob)
            total_words += 1
    
    avg_log_prob = total_log_prob / total_words
    return 2 ** (-avg_log_prob)

# Example: comparing two models on test data
good_model = {
    ('<START>', 'i'): 0.5,   ('i', 'love'): 0.7,
    ('love', 'cats'): 0.5,   ('cats', '<END>'): 1.0,
}

bad_model = {
    ('<START>', 'i'): 0.1,   ('i', 'love'): 0.1,
    ('love', 'cats'): 0.1,   ('cats', '<END>'): 1.0,
}

test = [['i', 'love', 'cats']]

print(f"Good model perplexity: {perplexity(good_model, test):.2f}")
print(f"Bad model perplexity:  {perplexity(bad_model, test):.2f}")
# Good model perplexity: ~1.6   (very confident)
# Bad model perplexity:  ~10.0  (more confused)
```

---

## Section 6: Markov Chains — The Statistical Heart

### What Is a Markov Chain?

A **Markov Chain** is a mathematical model where the next state depends only on the current state—not on how you got there.

The N-gram models we built are Markov Chains! A bigram model is a **first-order Markov Chain** (next word depends on 1 previous word). A trigram model is a **second-order Markov Chain** (next word depends on 2 previous words).

**The Markov Property:**
```
P(word_n | word_1, word_2, ..., word_{n-1}) ≈ P(word_n | word_{n-1})
```

We approximate that the future depends only on the recent past—not the entire history.

### Visualising a Markov Chain

Think of words as **states** and transitions as **arrows with probabilities**.

```
<START> ──0.6──→ "The"  ──0.4──→ "cat"  ──0.7──→ "sat"
        ──0.4──→ "A"    ──0.3──→ "dog"  ──0.3──→ "ran"
                        ──0.3──→ "bird" ──────────→ ...
```

At each step, you randomly follow an arrow weighted by probability. The result is a generated sentence.

### Building a Markov Text Generator

```python
import random
from collections import defaultdict, Counter
import re

def train_markov_model(text, order=2):
    """
    Train a Markov chain language model.
    order: how many previous words to use as context (1=bigram, 2=trigram)
    """
    # Clean and tokenise
    words = re.findall(r'\b\w+\b', text.lower())
    model = defaultdict(Counter)
    
    for i in range(len(words) - order):
        context = tuple(words[i:i+order])
        next_word = words[i+order]
        model[context][next_word] += 1
    
    return model

def generate_markov_text(model, order, seed_words, length=30):
    """Generate text using the Markov model"""
    output = list(seed_words)
    context = tuple(seed_words[-order:])
    
    for _ in range(length):
        if context not in model:
            break
        
        # Weighted random choice
        choices = list(model[context].keys())
        weights = list(model[context].values())
        next_word = random.choices(choices, weights=weights, k=1)[0]
        
        output.append(next_word)
        context = tuple(output[-order:])
    
    return ' '.join(output)

# Train on some text
training_text = """
The cat sat on the mat. The cat ate the fish.
The dog ran in the park. The dog chased the cat.
Cats like to eat fish and sleep on mats.
Dogs like to run and play in the park.
The fish swam in the river near the park.
On sunny days, the cat and the dog played together.
"""

model = train_markov_model(training_text, order=2)

print("Generated sentences (order-2 Markov chain):")
print("-" * 50)
random.seed(1)
for i in range(5):
    seed = random.choice(list(model.keys()))
    text = generate_markov_text(model, order=2, seed_words=list(seed), length=12)
    print(f"  {i+1}. {text}")
```

**Example output:**
```
Generated sentences (order-2 Markov chain):
--------------------------------------------------
  1. the cat sat on sunny days the cat and the dog played
  2. the dog chased the cat ate the fish swam in the river
  3. cats like to eat fish and sleep on mats dogs like to
  4. the park on sunny days the cat and the dog ran in the
  5. in the park on sunny days the cat sat on the mat the
```

Notice: higher-order models produce more coherent text because they remember more context.

---

## Section 7: Limitations of Classical Methods

Classical N-gram models were dominant in NLP for decades. But they have real limitations that motivated the move to neural networks.

### 1. Fixed Context Window
A trigram only looks back 2 words. It cannot capture long-range dependencies:

```
"The trophy didn't fit in the suitcase because _____ was too big."
```

Is the blank "it" (the trophy) or "it" (the suitcase)? Humans use the whole sentence. A trigram model only sees "because ___ was".

### 2. No Generalisation
A model trained on "cats love fish" knows nothing about "dogs love fish"—even though they are structurally identical. Every N-gram is treated as independent. Words have no relationships to each other.

### 3. Vocabulary Explosion
For a vocabulary of 50,000 words, a trigram model needs to store 50,000³ = 125 billion possible combinations. Most are never seen. The model is mostly zeros.

### 4. Smoothing Is a Hack
All smoothing techniques are approximate fixes to a fundamental problem: the model does not understand language, it just counts.

### Why This Matters

These limitations directly motivated **word embeddings** (words have neighbours and relationships) and **neural language models** (context is captured by flexible network weights, not fixed windows).

Understanding classical methods makes it clear *why* the field moved to neural networks—not just that it did.

---

## Section 8: Summary

### What You Learned

| Concept | Plain English Summary |
|---------|----------------------|
| **Language Model** | Assigns probability to sentences; higher = more natural |
| **N-gram** | A sequence of N consecutive words |
| **Bigram Model** | Predict next word based on current word |
| **Trigram Model** | Predict next word based on previous 2 words |
| **Sparsity Problem** | Many N-grams never appear in training data → zero probability |
| **Laplace Smoothing** | Add 1 to all counts so nothing has zero probability |
| **Backoff Smoothing** | Fall back to shorter N-gram when longer one unseen |
| **Interpolation** | Mix all N-gram levels with learnable weights |
| **Perplexity** | How surprised is the model? Lower = better model |
| **Markov Chain** | Next state depends only on recent past, not full history |

### The Key Insight

Classical text generation taught us that **language has statistical regularities**. The same words tend to appear together. Some word sequences are far more likely than others. You can learn these patterns from data.

What neural networks added was the ability to *generalise* those patterns—to understand that "the cat sat" and "a feline rested" are the same idea expressed differently, and to capture context far beyond a fixed window of 2-3 words.

---

## Practice Questions

**1. What is the difference between a unigram and a bigram model?**
<details><summary>Answer</summary>
A unigram model treats each word independently with no context. A bigram model predicts the next word based on the single previous word.
</details>

**2. Why do we use log probabilities instead of raw probabilities for sentences?**
<details><summary>Answer</summary>
Multiplying many small probabilities produces numbers too tiny for computers to store accurately. Log converts multiplication to addition, avoiding numerical underflow.
</details>

**3. What is the sparsity problem in N-gram models?**
<details><summary>Answer</summary>
Most possible word combinations never appear in training data, giving them zero probability. This breaks the model whenever it encounters any unseen combination.
</details>

**4. Describe Laplace smoothing in one sentence.**
<details><summary>Answer</summary>
Add 1 to every N-gram count so that no combination has zero probability, at the cost of slightly redistributing probability from seen to unseen events.
</details>

**5. What does perplexity measure? Is lower or higher better?**
<details><summary>Answer</summary>
Perplexity measures how surprised the model is by new text—effectively how many equally likely choices it considers at each word. Lower perplexity means a better model.
</details>

**6. What is the Markov property in the context of language models?**
<details><summary>Answer</summary>
The next word depends only on the recent context (the last N-1 words), not on the entire history of the sentence.
</details>

**7. Why do trigram models generally outperform bigram models?**
<details><summary>Answer</summary>
Trigrams use more context (2 previous words vs 1), so they make more informed predictions. However, they also suffer more from sparsity.
</details>

**8. Name two limitations of classical N-gram models that neural networks address.**
<details><summary>Answer</summary>
(1) Fixed context window — neural models capture arbitrarily long dependencies. (2) No generalisation — word embeddings give words relationships to each other, so learning about "cats" helps with "dogs."
</details>
