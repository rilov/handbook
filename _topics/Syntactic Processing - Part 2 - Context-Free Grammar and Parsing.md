---
title: "Syntactic Processing Part 2 - Context-Free Grammar and Parsing"
category: Natural Language Processing
order: 4
tags:
  - nlp
  - syntactic-processing
  - grammar
  - cfg
  - parsing
  - constituency
  - dependency
  - beginners
  - friendly
summary: Learn how computers understand sentence structure through grammar rules, constituency parsing, and dependency parsing. A beginner-friendly guide to analyzing how words relate to each other.
---

# Syntactic Processing Part 2 - Context-Free Grammar and Parsing

## Why This Guide Exists

Words and phrases are not enough. To truly understand language, we need to know how words connect to form complete thoughts. This guide explains grammar rules and parsing—the process of analyzing sentence structure.

---

## Segment 1: Context-Free Grammar (CFG)

### What is CFG?

**Context-Free Grammar** is a set of rules that define which sentences are grammatically valid.

### Grammar Components

1. **Terminal symbols:** Actual words (the, dog, runs)
2. **Non-terminal symbols:** Categories (Sentence, Noun Phrase, Verb)
3. **Production rules:** How to expand non-terminals
4. **Start symbol:** Where to begin (usually S for Sentence)

### Simple English Grammar

```
S → NP VP                    (Sentence = Noun Phrase + Verb Phrase)
NP → DET N                   (Noun Phrase = Determiner + Noun)
NP → DET ADJ N               (Noun Phrase = Determiner + Adjective + Noun)
VP → V NP                    (Verb Phrase = Verb + Noun Phrase)
VP → V                       (Verb Phrase = just a Verb)
DET → "the" | "a" | "an"     (Determiner options)
ADJ → "quick" | "brown"      (Adjective options)
N → "fox" | "dog" | "cat"    (Noun options)
V → "jumps" | "runs" | "eats" (Verb options)
```

### Deriving a Sentence

Start with **S**:
```
S → NP VP → DET N VP → "the" N VP → "the" "fox" VP 
  → "the" "fox" V NP → "the" "fox" "jumps" NP
  → "the" "fox" "jumps" DET N → "the" "fox" "jumps" "the" "dog"
```

**Result:** "the fox jumps the dog"

**Note:** This is grammatically valid but semantically odd. CFG checks grammar, not meaning!

---

## Segment 2: Types of Parsing

### Constituency Parsing

Builds a **hierarchical tree** showing phrases within phrases.

**Example:** "The cat sleeps"
```
        S
      /   \
    NP      VP
   /  \     /  \
 DET    N  V
 |      |  |
the   cat sleeps
```

**Key concept:** Constituents can move together
- "The cat" → "It sleeps"
- "sleeps" → "The cat does so"

### Dependency Parsing

Shows **direct relationships** between words.

**Example:** "The cat sleeps"
```
    sleeps (root)
     /    \
   cat    . (punctuation)
   |
  the
```

**Key labels:**
- **nsubj:** nominal subject (who is doing the action)
- **dobj:** direct object (what receives the action)
- **prep:** preposition
- **amod:** adjectival modifier
- **det:** determiner

### Constituency vs Dependency

| Feature | Constituency | Dependency |
|---------|-------------|------------|
| **Structure** | Hierarchical phrases | Word-to-word links |
| **Focus** | Phrase structure | Grammatical relations |
| **Best for** | Grammar checking | Information extraction |

---

## Segment 3: Ambiguity in Parsing

Some sentences have multiple valid interpretations:

**"I saw the man with the telescope"**

**Interpretation 1:** I used a telescope to see the man.
```
VP: saw [the man] [with the telescope]  ← "with telescope" modifies "saw"
```

**Interpretation 2:** I saw a man who had a telescope.
```
VP: saw [the man with the telescope]  ← "with telescope" modifies "man"
```

This is why parsing is challenging—computers must choose between valid interpretations.

---

## Segment 4: Python Examples

### Dependency Parsing with spaCy

```python
import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp("The quick brown fox jumps over the lazy dog")

for token in doc:
    print(f"{token.text:12} | {token.dep_:12} | {token.head.text:12}")
```

**Output:**
```
The          | det          | fox          
quick        | amod         | fox          
brown        | amod         | fox          
fox          | nsubj        | jumps        
jumps        | ROOT         | jumps        
over         | prep         | jumps        
the          | det          | dog          
lazy         | amod         | dog          
dog          | pobj         | over         
```

### Creating Parse Trees

```python
from nltk.tree import Tree

# Create tree from bracket notation
tree_string = "(S (NP (DT The) (NN cat)) (VP (VBD slept)))"
tree = Tree.fromstring(tree_string)
print(tree)
tree.draw()  # Opens visualization window
```

---

## Segment 5: Session Summary

### Key Takeaways

1. **Context-Free Grammar** defines valid sentence structures using rules
2. **Constituency parsing** builds hierarchical phrase trees
3. **Dependency parsing** shows direct word relationships
4. **Ambiguity** is common—sentences can have multiple valid parses
5. **Different parsers serve different purposes**—choose based on your task

### Practice Questions

**1. What does S → NP VP mean in CFG?**
<details><summary>Answer</summary>A Sentence consists of a Noun Phrase followed by a Verb Phrase.</details>

**2. What is the difference between constituency and dependency parsing?**
<details><summary>Answer</summary>Constituency builds phrase hierarchies (NP, VP). Dependency shows word-to-word relationships (subject, object).</details>

**3. What does "nsubj" mean in dependency parsing?**
<details><summary>Answer</summary>Nominal subject—the word performing the action of the verb.</details>

---

## What Comes Next?

Part 3 covers **Tree Structures and Grammatical Agreement**—visual representations of syntax and ensuring grammatical correctness.
