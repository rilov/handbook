---
title: "Lexical Processing - A Friendly Guide"
category: Natural Language Processing
order: 2
tags:
  - nlp
  - lexical-processing
  - tokenization
  - stemming
  - lemmatization
  - text-normalization
  - beginners
  - friendly
summary: A beginner-friendly guide to Lexical Processing in NLP. Learn how computers break down text through tokenization, text normalization, stopword removal, stemming, lemmatization, and spell correction—with simple explanations and Python examples.
---

# Lexical Processing - A Friendly Guide

## Why This Guide Exists

Before a computer can understand what you are saying, it needs to chop your text into manageable pieces. This is lexical processing—the first major stage of the NLP pipeline.

Think of it like preparing ingredients before cooking. You wouldn't dump a whole chicken into a pot and hope for the best. You chop, clean, and organize everything first.

This guide shows you how computers do exactly that with text—using friendly examples and real Python code you can run yourself.

---

## Segment 1: Session Overview

### What is Lexical Processing?

**Lexical processing** is the set of techniques that break down raw text into individual words (or tokens) and normalize them into standard forms.

**Why it matters:**
- Computers cannot work with paragraphs—they need individual units
- Words appear in different forms (run, running, ran) but mean the same thing
- Text is messy (typos, abbreviations, inconsistent formatting)

### What You Will Learn

1. **Text Normalisation** – Making text consistent and clean
2. **Tokenisation** – Splitting text into words and sentences
3. **Stopword Removal** – Filtering out common but unimportant words
4. **Morphological Analysis** – Understanding how words are built
5. **Spell Correction** – Fixing typos automatically
6. **Stemming** – Chopping words down to their roots
7. **Lemmatisation** – Converting words to their dictionary forms

### The Analogy: The Text Kitchen

Imagine you are a chef receiving a crate of random ingredients:

| Raw Delivery | Processing Step | Result |
|--------------|-----------------|--------|
| "HELLO world!!!" | Normalisation | "hello world" |
| "The quick brown fox jumps" | Tokenisation | ["The", "quick", "brown", "fox", "jumps"] |
| "running, runs, ran" | Stemming/Lemmatisation | "run" |
| "teh, recieve, seperate" | Spell Correction | "the, receive, separate" |

---

## Segment 2: Text Normalisation

### What is Text Normalisation?

Text normalisation makes text consistent. It is like tidying up a messy room before you can find anything.

### Common Normalisation Techniques

#### 1. Case Conversion
**What:** Convert everything to lowercase (or uppercase).

**Why:** "Apple" (company) and "apple" (fruit) should be treated the same for many tasks.

```python
# Example
text = "The QUICK Brown Fox"
normalized = text.lower()
# Result: "the quick brown fox"
```

**When to use:** Search, matching, most analysis tasks.

**When NOT to use:** Named entity recognition ("Washington" the place vs. "washington" a verb).

#### 2. Removing Extra Whitespace
**What:** Collapse multiple spaces, tabs, and newlines into single spaces.

```python
# Before
"Hello    world\n\n\tHow   are   you?"

# After
"Hello world How are you?"
```

#### 3. Removing Special Characters
**What:** Strip punctuation, emojis, or other non-text elements.

```python
# Before
"Hello!!! How are you??? 😊 #excited"

# After (keep only letters and spaces)
"Hello How are you"
```

**Caution:** Sometimes special characters matter. "@username" in tweets contains information.

#### 4. Handling Contractions
**What:** Expand shortened forms to full words.

| Contraction | Expanded |
|-------------|----------|
| don't | do not |
| I'm | I am |
| can't | cannot |
| won't | will not |
| it's | it is |

```python
# Example logic
contractions = {
    "don't": "do not",
    "I'm": "I am",
    "can't": "cannot"
}
```

**Why it matters:** "I don't like this" vs. "I do not like this"—without expansion, "don't" is treated as one unique word.

#### 5. Handling Accented Characters
**What:** Convert é, ñ, ü to e, n, u (or preserve them).

```python
# Before
"café, naïve, résumé"

# After (ASCII normalization)
"cafe, naive, resume"
```

### Real-World Example: Search Engine

When you search for "cafe" you want results for:
- "cafe"
- "café"
- "CAFE"
- "coffee shop" (maybe)

Normalisation makes this possible.

---

## Segment 3: Tokenisation

### What is Tokenisation?

**Tokenisation** is breaking text into smaller pieces called **tokens** (usually words or sentences).

It is the most fundamental step in NLP—everything else builds on this.

### Word Tokenisation

Splitting text into individual words.

```python
# Simple example
text = "The quick brown fox jumps"
tokens = ["The", "quick", "brown", "fox", "jumps"]
```

**But it is not always simple:**

| Challenge | Example | Decision |
|-----------|---------|----------|
| Contractions | "don't" | ["do", "n't"] or ["don't"]? |
| Hyphenated words | "state-of-the-art" | One token or ["state", "of", "the", "art"]? |
| Numbers | "3.14" | One token or ["3", ".", "14"]? |
| URLs | "https://example.com" | One token or separate? |
| Email | "user@email.com" | One token or separate? |

### Sentence Tokenisation

Splitting paragraphs into individual sentences.

**Challenges:**
- "Dr. Smith went to Washington." ("Dr." is not the end of a sentence)
- "The price is $3.50." (Period is not the end)
- "Mr. and Mrs. Jones arrived." (Multiple abbreviations)

```python
# Example sentences
text = "Hello! How are you? I'm fine. Thanks."
sentences = ["Hello!", "How are you?", "I'm fine.", "Thanks."]
```

### Tokenisation Strategies

#### 1. Whitespace Tokenisation
Split on spaces. Fast but crude.

```python
text = "Hello, world!"
# Result: ["Hello,", "world!"]  # Punctuation stuck to words
```

#### 2. Punctuation-Based Tokenisation
Split on punctuation too.

```python
text = "Hello, world!"
# Result: ["Hello", ",", "world", "!"]
```

#### 3. Treebank Tokenisation
Penn Treebank standard—handles contractions specially.

```python
text = "I'm happy."
# Result: ["I", "'m", "happy", "."]
```

#### 4. Subword Tokenisation (BPE, WordPiece)
Break rare words into smaller pieces.

```python
word = "unhappiness"
# Result: ["un", "##hap", "##pi", "##ness"]
# (Common in modern NLP like BERT)
```

### Python Example with NLTK

```python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required data
nltk.download('punkt')

# Word tokenisation
text = "Hello! I'm learning NLP. It's fascinating!"
words = word_tokenize(text)
print(words)
# ['Hello', '!', 'I', "'m", 'learning', 'NLP', '.', 'It', "'s", 'fascinating', '!']

# Sentence tokenisation
sentences = sent_tokenize(text)
print(sentences)
# ['Hello!', "I'm learning NLP.", "It's fascinating!"]
```

---

## Segment 4: Stopword Removal

### What are Stopwords?

**Stopwords** are common words that carry little meaning: the, and, is, at, which, on, a, an, in.

They appear in almost every sentence, so they do not help distinguish one document from another.

### Examples by Language

**English:** a, an, the, and, or, but, in, on, at, to, for, of, with, by
**Spanish:** el, la, de, que, y, a, los, del, se, las
**French:** le, la, de, et, à, un, il, être, et, avoir

### Why Remove Stopwords?

**Benefits:**
- Reduce dataset size (fewer unique words to process)
- Focus on meaningful words
- Improve processing speed
- Often improves accuracy for tasks like classification

**Example:**

| Original | After Stopword Removal |
|----------|------------------------|
| "The quick brown fox jumps over the lazy dog" | "quick brown fox jumps over lazy dog" |
| "I am running in the park" | "running park" |

### When NOT to Remove Stopwords

- **Sentiment analysis:** "not good" vs. "good"—removing "not" changes meaning
- **Question answering:** "Who is the president?"—removing "who" destroys the question
- **Machine translation:** Need all words to produce correct output
- **Grammar checking:** Need all words to check grammar

### Python Example

```python
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')

# Get English stopwords
stop_words = set(stopwords.words('english'))

text = "The quick brown fox jumps over the lazy dog"
words = word_tokenize(text.lower())

# Remove stopwords
filtered = [word for word in words if word not in stop_words]
print(filtered)
# ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog']
```

### Custom Stopword Lists

Sometimes the default list is not right for your task.

```python
# Add domain-specific stopwords
my_stopwords = stopwords.words('english')
my_stopwords.extend(['app', 'click', 'user', 'page'])  # For app reviews

# Or create your own
custom_stopwords = {'the', 'and', 'http', 'www', 'com'}
```

---

## Segment 5: Morphological Analysis

### What is Morphology?

**Morphology** is the study of how words are built from smaller meaningful units called **morphemes**.

**Example:** "Unhappiness"
- un- (prefix: not)
- happy (root word)
- -ness (suffix: state of being)

Understanding this structure helps computers recognize that "unhappiness" relates to "happy."

### Types of Morphemes

| Type | Description | Examples |
|------|-------------|----------|
| **Root/Stem** | Core meaning | run, happy, child |
| **Prefix** | Added before | un-, re-, pre-, dis- |
| **Suffix** | Added after | -ing, -ed, -ly, -ness |
| **Inflection** | Grammar changes | running, runs, ran (same word, different form) |
| **Derivation** | Creates new word | happy → happiness (different word class) |

### Why Morphology Matters in NLP

**Vocabulary reduction:**
- run, runs, running, ran → run
- 4 words become 1 concept

**Information extraction:**
- "unhappy" = "not happy" (prefix carries meaning)
- "teacher" = "teach" + "person who does" (suffix carries meaning)

**Language understanding:**
- Recognizing word relationships
- Handling unknown words by breaking them apart

### Example Analysis

| Word | Morphological Breakdown | Meaning |
|------|------------------------|---------|
| running | run + ing | action of run |
| impossible | im + possible | not possible |
| childhood | child + hood | state of being a child |
| nationalisation | nation + al + ise + ation | process of making national |

---

## Segment 6: Spell Correction

### Why Spell Correction Matters

Text is messy. People make typos, especially in:
- Social media posts
- Search queries
- Text messages
- User-generated content

A good NLP system needs to handle: "teh" → "the", "recieve" → "receive"

### Types of Spelling Errors

| Type | Example | Cause |
|------|---------|-------|
| **Non-word errors** | "teh" for "the" | Typing mistake |
| **Real-word errors** | "there" for "their" | Homophone confusion |
| **Insertion** | "happpy" (extra p) | Fat fingers |
| **Deletion** | "hapen" (missing p) | Fast typing |
| **Substitution** | "giod" for "good" | Adjacent keys |
| **Transposition** | "hte" for "the" | Finger order |

### How Spell Correction Works

#### 1. Detection
First, determine if a word is misspelled.

```
Check against dictionary:
- "the" → in dictionary ✓
- "teh" → not in dictionary ✗
```

#### 2. Candidate Generation
Create possible corrections.

For "teh":
- Edit distance 1: the, ten, tea, tech
- Edit distance 2: they, them, then

#### 3. Ranking
Choose the most likely correction.

Factors:
- Edit distance (fewer changes = better)
- Word frequency ("the" is more common than "tea")
- Context (surrounding words)

### Edit Distance (Levenshtein Distance)

The minimum number of single-character edits needed to change one word into another.

**Operations:**
- Insertion: "car" → "cart"
- Deletion: "cart" → "car"
- Substitution: "cat" → "cut"

**Example:**
```
kitten → sitting
kitten → sitten (substitute k→s)
sitten → sittin (substitute e→i)
sittin → sitting (insert g)
Distance = 3
```

### Python Example with TextBlob

```python
from textblob import TextBlob

# Simple spell correction
text = "I am lerning NLP and it is fascinting"
blob = TextBlob(text)
corrected = blob.correct()
print(corrected)
# "I am learning NLP and it is fascinating"
```

### Context-Aware Correction

Sometimes context matters more than edit distance:

```
"I am going to the markt"
Candidates: mark, market, mart
Best: "market" (context: "going to the...")
```

---

## Segment 7: Stemming

### What is Stemming?

**Stemming** chops off word endings to reduce words to their root form (stem). It uses simple rules and does not require a vocabulary.

**Crude but fast.**

### Examples

| Word | Stem | Rule Applied |
|------|------|--------------|
| running | run | Remove "ning" |
| runs | run | Remove "s" |
| runner | run | Remove "ner" |
| easily | easili | Remove "ly" |
| fairly | fairli | Remove "ly" |
| fishing | fish | Remove "ing" |

**Notice:** The stem is not always a real word ("easili" is not English).

### Common Stemming Algorithms

#### 1. Porter Stemmer (1980)
The most widely used. Five phases of word reductions.

```python
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

words = ["running", "runs", "runner", "easily", "fairly"]
stems = [stemmer.stem(w) for w in words]
print(stems)
# ['run', 'run', 'runner', 'easili', 'fairli']
```

**Porter rules example:**
- SSES → SS ("caresses" → "caress")
- IES → I ("ponies" → "poni")
- SS → SS ("caress" → "caress")
- S → "" ("cats" → "cat")

#### 2. Snowball Stemmer (Porter2)
Improved version, handles more cases.

```python
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer("english")
print(stemmer.stem("generously"))  # 'generous'
```

#### 3. Lancaster Stemmer
More aggressive—chops more, faster.

```python
from nltk.stem import LancasterStemmer

stemmer = LancasterStemmer()
print(stemmer.stem("maximum"))  # 'maxim'
print(stemmer.stem("multiply"))  # 'multiply'
```

### Comparison

| Stemmer | Speed | Aggressiveness | Use Case |
|---------|-------|----------------|----------|
| Porter | Medium | Moderate | General purpose |
| Snowball | Medium | Moderate | Better than Porter |
| Lancaster | Fast | Very aggressive | When you want maximum reduction |

### When to Use Stemming

**Good for:**
- Information retrieval (search engines)
- Basic text classification
- When speed matters more than precision

**Not good for:**
- Tasks needing real words
- Output shown to users
- When word meaning matters deeply

---

## Segment 8: Lemmatisation

### What is Lemmatisation?

**Lemmatisation** converts words to their dictionary form (**lemma**) using vocabulary and morphological analysis.

**Smarter but slower than stemming.**

**Key difference:** Lemmatisation produces real words.

### Examples

| Word | Lemma | Part of Speech |
|------|-------|----------------|
| running | run | verb |
| better | good | adjective |
| was | be | verb |
| mice | mouse | noun |
| are | be | verb |
| ate | eat | verb |

**Compare with stemming:**
- Stemming: "better" → "better" (unchanged, wrong)
- Lemmatisation: "better" → "good" (correct)

### Why Lemmatisation Needs Context

The same word can have different lemmas depending on its role:

| Word | Context | Lemma |
|------|---------|-------|
| saw | "I saw a movie" | see (verb) |
| saw | "Use a saw" | saw (noun) |
| leaves | "Leaves fall" | leaf (noun) |
| leaves | "She leaves" | leave (verb) |

This is why lemmatisers need **Part-of-Speech tags**.

### Python Example with NLTK

```python
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()

# Without POS tag (defaults to noun)
print(lemmatizer.lemmatize("running"))  # 'running' (treated as noun)

# With POS tag
print(lemmatizer.lemmatize("running", pos=wordnet.VERB))  # 'run'
print(lemmatizer.lemmatize("better", pos=wordnet.ADJ))  # 'good'
print(lemmatizer.lemmatize("was", pos=wordnet.VERB))  # 'wa' (be)
```

### POS Tag Mapping

NLTK and WordNet use different POS tag systems:

| NLTK Tag | WordNet POS | Description |
|----------|-------------|-------------|
| JJ | wordnet.ADJ | Adjective |
| NN | wordnet.NOUN | Noun |
| VB | wordnet.VERB | Verb |
| RB | wordnet.ADV | Adverb |

---

## Segment 9: Stemming vs Lemmatisation

### Quick Comparison

| Feature | Stemming | Lemmatisation |
|---------|----------|---------------|
| **Method** | Chop endings with rules | Use vocabulary and POS |
| **Speed** | Fast | Slower |
| **Output** | May not be real words | Always real words |
| **Accuracy** | Crude | Precise |
| **Context needed** | No | Yes (POS tags) |
| **Use case** | Search, basic NLP | High-quality NLP |

### Visual Example

```
Original: "The striped bats are hanging on their feet for best"

Stemming (Porter):
["the", "strip", "bat", "are", "hang", "on", "their", "feet", "for", "best"]

Lemmatisation:
["the", "striped", "bat", "be", "hang", "on", "their", "foot", "for", "good"]

Key differences:
- "striped" → "strip" (stemming loses meaning)
- "are" → "are" (stemming misses verb)
- "feet" → "foot" (lemmatisation knows plural)
- "best" → "good" (lemmatisation knows comparative)
```

### When to Use Which

**Use Stemming when:**
- Building a search engine (speed matters)
- Working with massive datasets
- You do not need human-readable output
- Doing basic exploratory analysis

**Use Lemmatisation when:**
- Building production NLP systems
- Output will be shown to users
- Doing sentiment analysis (word meaning matters)
- Working with machine learning models

### Real-World Analogy

| Method | Analogy | Result |
|--------|---------|--------|
| Stemming | Chopping vegetables with a big knife | Fast, but uneven pieces |
| Lemmatisation | Carefully cutting with a chef's knife | Precise, perfect pieces |

---

## Segment 10: Lexical Processing Python Demonstration

### Complete Pipeline Example

```python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet

# Download required resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Sample text
raw_text = """
The striped bats were hanging on their feet and ate best fishes.
After eating, they slept soundly while dreaming of flying.
"""

print("=" * 60)
print("LEXICAL PROCESSING PIPELINE DEMONSTRATION")
print("=" * 60)

# Step 1: Text Normalisation
print("\n1. TEXT NORMALISATION")
print("-" * 40)
normalized = raw_text.lower().strip()
print(f"Lowercase: {normalized[:60]}...")

# Step 2: Sentence Tokenisation
print("\n2. SENTENCE TOKENISATION")
print("-" * 40)
sentences = sent_tokenize(raw_text)
for i, sent in enumerate(sentences, 1):
    print(f"Sentence {i}: {sent}")

# Step 3: Word Tokenisation
print("\n3. WORD TOKENISATION")
print("-" * 40)
words = word_tokenize(raw_text)
print(f"Tokens: {words[:15]}...")
print(f"Total tokens: {len(words)}")

# Step 4: Stopword Removal
print("\n4. STOPWORD REMOVAL")
print("-" * 40)
stop_words = set(stopwords.words('english'))
filtered = [w for w in words if w.lower() not in stop_words and w.isalpha()]
print(f"Without stopwords: {filtered[:15]}...")
print(f"Removed {len(words) - len(filtered)} stopwords")

# Step 5: Stemming
print("\n5. STEMMING (Porter Stemmer)")
print("-" * 40)
porter = PorterStemmer()
stemmed = [porter.stem(w) for w in filtered]
print(f"Stemmed: {stemmed[:15]}...")

# Step 6: Lemmatisation
print("\n6. LEMMATISATION")
print("-" * 40)
lemmatizer = WordNetLemmatizer()

# Helper to convert POS tags
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

# Get POS tags
pos_tags = nltk.pos_tag(filtered)
print("POS Tags:", pos_tags[:10])

# Lemmatise with POS
lemmatized = []
for word, tag in pos_tags:
    wn_tag = get_wordnet_pos(tag)
    lemma = lemmatizer.lemmatize(word, pos=wn_tag)
    lemmatized.append(lemma)

print(f"Lemmatised: {lemmatized[:15]}...")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Original tokens: {len(words)}")
print(f"After stopword removal: {len(filtered)}")
print(f"Unique stems: {len(set(stemmed))}")
print(f"Unique lemmas: {len(set(lemmatized))}")
```

### Expected Output

```
============================================================
LEXICAL PROCESSING PIPELINE DEMONSTRATION
============================================================

1. TEXT NORMALISATION
----------------------------------------
Lowercase: the striped bats were hanging on their feet and...

2. SENTENCE TOKENISATION
----------------------------------------
Sentence 1: The striped bats were hanging on their feet and ate best fishes.
Sentence 2: After eating, they slept soundly while dreaming of flying.

3. WORD TOKENISATION
----------------------------------------
Tokens: ['The', 'striped', 'bats', 'were', 'hanging', 'on', 'their', ...]
Total tokens: 24

4. STOPWORD REMOVAL
----------------------------------------
Without stopwords: ['striped', 'bats', 'hanging', 'feet', 'ate', ...]
Removed 12 stopwords

5. STEMMING (Porter Stemmer)
----------------------------------------
Stemmed: ['stripe', 'bat', 'hang', 'feet', 'ate', 'best', 'fish', ...]

6. LEMMATISATION
----------------------------------------
POS Tags: [('striped', 'JJ'), ('bats', 'NNS'), ('hanging', 'VBG'), ...]
Lemmatised: ['striped', 'bat', 'hang', 'foot', 'eat', 'good', 'fish', ...]

============================================================
SUMMARY
============================================================
Original tokens: 24
After stopword removal: 12
Unique stems: 10
Unique lemmas: 11
```

---

## Segment 11: Session Summary

### What We Learned

1. **Text Normalisation** – Making text consistent (case, spacing, contractions, accents)

2. **Tokenisation** – Breaking text into words and sentences
   - Word tokenisation: Split into individual words
   - Sentence tokenisation: Split by sentence boundaries

3. **Stopword Removal** – Filtering common words (the, and, is)
   - Reduces data size
   - Focuses on meaningful words
   - But be careful with sentiment analysis

4. **Morphological Analysis** – Understanding word structure (prefixes, suffixes, roots)

5. **Spell Correction** – Fixing typos using edit distance and context

6. **Stemming** – Chopping word endings (fast, crude)
   - Porter, Snowball, Lancaster algorithms
   - Output may not be real words

7. **Lemmatisation** – Converting to dictionary forms (slow, precise)
   - Uses vocabulary and POS tags
   - Always produces real words

### Key Takeaways

- **Lexical processing prepares text for deeper analysis**
- **Tokenisation is the foundation**—everything builds on it
- **Choose stemming for speed, lemmatisation for accuracy**
- **Stopword removal is task-dependent**—not always helpful
- **These techniques often work together** in a pipeline

### The Pipeline Flow

```
Raw Text
    ↓
Text Normalisation (lowercase, clean)
    ↓
Tokenisation (split into words)
    ↓
Stopword Removal (filter common words)
    ↓
Stemming OR Lemmatisation (normalize forms)
    ↓
Clean Tokens Ready for Analysis
```

---

## Segment 12: Practice Questions

### Quick Check Questions

**1. What is the difference between tokenisation and normalisation?**
<details>
<summary>Answer</summary>
Normalisation makes text consistent (lowercase, remove spaces). Tokenisation splits text into individual units (words or sentences).
</details>

**2. Why might you choose stemming over lemmatisation?**
<details>
<summary>Answer</summary>
Stemming is faster and simpler. Good for search engines or when processing speed matters more than perfect accuracy.
</details>

**3. What are stopwords? Give three examples.**
<details>
<summary>Answer</summary>
Common words that carry little meaning: "the," "and," "is," "in," "at."
</details>

**4. What is the edit distance between "kitten" and "sitting"?**
<details>
<summary>Answer</summary>
3. (k→s, e→i, add g)
</details>

**5. Why does lemmatisation need Part-of-Speech tags?**
<details>
<summary>Answer</summary>
The same word can have different lemmas depending on its grammatical role (e.g., "saw" as verb = "see", as noun = "saw").
</details>

### Coding Questions

**6. Write code to tokenise and remove stopwords from this text:**
```python
text = "The quick brown fox jumps over the lazy dog!"
```
<details>
<summary>Answer</summary>

```python
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

words = word_tokenize(text.lower())
stop_words = set(stopwords.words('english'))
filtered = [w for w in words if w.isalpha() and w not in stop_words]
# Result: ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog']
```
</details>

**7. Compare stemming and lemmatisation results for:**
```python
words = ["better", "running", "geese", "was"]
```
<details>
<summary>Answer</summary>

```python
# Stemming: ['better', 'run', 'gees', 'wa']
# Lemmatisation: ['good', 'run', 'goose', 'be']
```
</details>

### Thought Questions

**8. Why might removing stopwords hurt sentiment analysis?**
<details>
<summary>Hint</summary>
Think about the phrase "not good."
</details>

**9. When would sentence tokenisation be more important than word tokenisation?**
<details>
<summary>Hint</summary>
Think about tasks that need to understand complete thoughts or document structure.
</details>

**10. Design a custom stopword list for analyzing customer reviews of a mobile app.**
<details>
<summary>Hint</summary>
What words are common in app reviews but do not help you understand if the review is positive or negative?
</details>

---

## What Comes Next?

Now that text is tokenised and normalised, the next step is understanding **structure**. The Syntactic Processing guide covers:

- **Part-of-Speech Tagging:** Labeling words as nouns, verbs, adjectives
- **Parsing:** Understanding how words relate to each other
- **Grammar:** Recognising sentence structure
- **Tree Structures:** Visualising sentence relationships

You have learned how to chop and prepare ingredients. Next, you will learn how to understand the recipe.
