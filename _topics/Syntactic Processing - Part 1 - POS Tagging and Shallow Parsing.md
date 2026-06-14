---
title: "Syntactic Processing Part 1 - POS Tagging and Shallow Parsing"
category: Natural Language Processing
order: 3
tags:
  - nlp
  - syntactic-processing
  - pos-tagging
  - chunking
  - shallow-parsing
  - beginners
  - friendly
summary: Learn how computers identify word types (nouns, verbs, adjectives) and group them into meaningful phrases. A beginner-friendly guide to Part-of-Speech tagging and shallow parsing with Python examples.
---

# Syntactic Processing Part 1 - POS Tagging and Shallow Parsing

## Why This Guide Exists

You now know how to break text into words. But words alone do not tell the whole story.

Consider: "The dog bit the man" vs "The man bit the dog." Same words, different meanings. The difference is **structure**—the grammatical relationships between words.

This guide covers the first layer of syntactic processing: identifying what type each word is, and grouping them into meaningful chunks.

---

## Segment 1: Session Overview

### What You Will Learn

1. **Part-of-Speech Tagging** – Labeling words as nouns, verbs, adjectives, etc.
2. **Shallow Parsing (Chunking)** – Grouping words into phrases like "noun phrases" and "verb phrases"

### The Analogy: Sentence Architecture

Think of a sentence like a building:
- **Foundation:** Main verb (holds everything together)
- **Load-bearing walls:** Subject, object (core participants)
- **Support beams:** Prepositions, conjunctions (connect parts)
- **Decorations:** Adjectives, adverbs (add detail)

Lexical processing gave you the building materials (words). Syntactic processing creates the structure.

---

## Segment 2: Part-of-Speech Tagging

### What is POS Tagging?

**Part-of-Speech (POS) tagging** is labeling each word with its grammatical role.

### The 8 Primary Parts of Speech

| POS | Description | Examples |
|-----|-------------|----------|
| **Noun (N)** | Person, place, thing, idea | dog, city, happiness |
| **Pronoun (PRP)** | Replaces a noun | he, she, it, they |
| **Verb (V)** | Action or state | run, is, think |
| **Adjective (ADJ)** | Modifies a noun | quick, happy, blue |
| **Adverb (ADV)** | Modifies a verb/adjective | quickly, very, well |
| **Preposition (PREP)** | Shows relationship | in, on, at, with |
| **Conjunction (CONJ)** | Connects words/clauses | and, but, because |
| **Determiner (DET)** | Specifies a noun | the, a, an, this |

### Why POS Tagging is Hard

Many words can be multiple parts of speech:

| Word | One Meaning | Another Meaning |
|------|-------------|-----------------|
| **book** | "I read a book" (noun) | "Book a flight" (verb) |
| **back** | "My back hurts" (noun) | "Go back home" (adverb) |
| **well** | "Drink from the well" (noun) | "She sings well" (adverb) |

**Context determines the correct tag.**

### Penn Treebank Tags (NLTK)

| Tag | Meaning | Example |
|-----|---------|---------|
| NN | Noun, singular | dog |
| NNS | Noun, plural | dogs |
| NNP | Proper noun | London |
| VB | Verb, base form | eat |
| VBD | Verb, past tense | ate |
| VBG | Verb, gerund | eating |
| VBN | Verb, past participle | eaten |
| JJ | Adjective | quick |
| RB | Adverb | quickly |
| IN | Preposition | in, on |
| DT | Determiner | the, a |
| PRP | Personal pronoun | I, you, he |

### Python Example

```python
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

text = "The quick brown fox jumps over the lazy dog"
tokens = word_tokenize(text)
tags = nltk.pos_tag(tokens)
print(tags)
# [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'), 
#  ('jumps', 'VBZ'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN')]
```

---

## Segment 3: Shallow Parsing (Chunking)

### What is Shallow Parsing?

**Shallow parsing** (chunking) groups words into phrases without analyzing deep grammatical relationships. Think of it as finding "chunks" of meaning.

### Types of Phrases

| Phrase Type | Contains | Example |
|-------------|----------|---------|
| **Noun Phrase (NP)** | Noun + modifiers | "the quick brown fox" |
| **Verb Phrase (VP)** | Verb + helpers/objects | "jumps over the fence" |
| **Prepositional Phrase (PP)** | Preposition + object | "over the moon" |

### Example

**Sentence:** "The quick brown fox jumps over the lazy dog"

**Noun phrases identified:**
- "The quick brown fox" (NP)
- "the lazy dog" (NP)

### Python Chunking Example

```python
from nltk.chunk import RegexpParser

# Define chunking grammar
grammar = r"""
    NP: {<DT>?<JJ>*<NN>}    # Determiner + adjectives + noun
        {<NNP>+}            # Proper nouns
    VP: {<VB.*><NP|PP>*}    # Verb + noun phrase or prepositional phrase
    PP: {<IN><NP>}          # Preposition + noun phrase
"""

chunk_parser = RegexpParser(grammar)
sentence = [("The", "DT"), ("quick", "JJ"), ("brown", "JJ"), 
            ("fox", "NN"), ("jumps", "VBZ"), ("over", "IN"),
            ("the", "DT"), ("lazy", "JJ"), ("dog", "NN")]

tree = chunk_parser.parse(sentence)
# Visualizes as: (S (NP The/DT quick/JJ brown/JJ fox/NN) 
#                 (VP jumps/VBZ (PP over/IN (NP the/DT lazy/JJ dog/NN))))
```

### Shallow vs Deep Parsing

| Aspect | Shallow Parsing | Deep Parsing |
|--------|-----------------|--------------|
| **Speed** | Fast | Slower |
| **Output** | Flat chunks | Full tree structure |
| **Relationships** | Limited | Comprehensive |
| **Use case** | Information extraction | Complete understanding |

---

## Segment 4: Session Summary

### Key Takeaways

1. **POS Tagging** labels each word with its grammatical type
   - Context matters: "book" can be noun or verb
   - Penn Treebank tags are standard in NLP

2. **Shallow Parsing** groups words into phrases
   - Noun phrases, verb phrases, prepositional phrases
   - Fast and useful for information extraction

3. **These techniques work together:**
   - First tokenise, then tag, then chunk

### Practice Questions

**1. What is the POS tag for "quickly"?**
<details><summary>Answer</summary>RB (Adverb)</details>

**2. What phrase type is "the lazy dog"?**
<details><summary>Answer</summary>Noun Phrase (NP)</details>

**3. Why is POS tagging challenging?**
<details><summary>Answer</summary>Many words can be different parts of speech depending on context.</details>

---

## What Comes Next?

Part 2 covers **Context-Free Grammar and Parsing**—understanding complete sentence structures and building parse trees.
