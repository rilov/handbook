---
title: "Syntactic Processing Part 3 - Tree Structures and Grammatical Agreement"
category: Natural Language Processing
order: 5
tags:
  - nlp
  - syntactic-processing
  - tree-structures
  - parse-trees
  - grammatical-agreement
  - beginners
  - friendly
summary: Learn how to visualize sentence structure with parse trees and ensure grammatical correctness through agreement checking. The final part of our syntactic processing series.
---

# Syntactic Processing Part 3 - Tree Structures and Grammatical Agreement

## Why This Guide Exists

Understanding sentence structure is one thing. Visualizing it and ensuring it follows grammar rules is another. This guide covers parse trees (visual representations of syntax) and grammatical agreement (ensuring words match correctly).

---

## Segment 1: Tree Structures

### What are Parse Trees?

**Parse trees** are visual representations of sentence structure, showing how words group into phrases and relate to each other.

### Tree Components

```
        S                    ← Root node (Sentence)
      /   \
    NP      VP              ← Non-terminal nodes (phrases)
   /  \     /  \
 DET   N   V    NP          ← Pre-terminal nodes (POS tags)
 |     |   |   /  \
the   cat sleeps DET  N     ← Terminal nodes (actual words)
               |     |
              the  mat
```

| Node Type | Description | Example |
|-----------|-------------|---------|
| **Root** | Top of tree | S (Sentence) |
| **Non-terminals** | Categories | NP, VP, PP |
| **Pre-terminals** | POS tags | DET, N, V |
| **Terminals** | Actual words | the, cat, sleeps |

### Treebank Format

Computers store trees in bracket notation:
```
(S (NP (DET the) (N cat)) (VP (V sleeps) (PP (PREP on) (NP (DET the) (N mat)))))
```

### Why Tree Structures Matter

**Resolving ambiguity:**
```
"Flying planes can be dangerous"

Tree 1: [Flying planes] can be dangerous (planes that are flying)
Tree 2: Flying [planes can be dangerous] (act of flying planes)
```

**Information extraction:**
- Find all noun phrases (who/what)
- Find verb phrases (what happened)
- Find prepositional phrases (when/where)

---

## Segment 2: Python Tree Operations

```python
from nltk.tree import Tree

# Create tree from bracket notation
tree_string = "(S (NP (DT The) (NN cat)) (VP (VBD slept) (PP (IN on) (NP (DT the) (NN mat)))))"
tree = Tree.fromstring(tree_string)

# Tree properties
print(f"Tree: {tree}")
print(f"Height: {tree.height()}")  # 4
print(f"Leaves: {tree.leaves()}")  # ['The', 'cat', 'slept', 'on', 'the', 'mat']

# Navigate the tree
for subtree in tree.subtrees():
    print(f"Label: {subtree.label()}, Leaves: {subtree.leaves()}")

# Draw tree (opens window)
tree.draw()
```

---

## Segment 3: Grammatical Agreement

### What is Grammatical Agreement?

**Grammatical agreement** ensures words match in grammatical features:
- **Number:** singular vs plural
- **Person:** first, second, third
- **Gender:** masculine, feminine, neuter (in some languages)

### Types of Agreement

#### 1. Subject-Verb Agreement
Verb must match subject in number.

| Correct | Incorrect |
|---------|-----------|
| The dog **runs** | The dog **run** |
| The dogs **run** | The dogs **runs** |

**Tricky case:**
```
"The group of students are arguing" ← Incorrect!
Subject = "group" (singular), so verb should be "is"
```

#### 2. Noun-Determiner Agreement
Determiners must match noun number.

| Correct | Incorrect |
|---------|-----------|
| **a** dog / **the** dog | **a** dogs |
| **many** dogs / **the** dogs | **many** dog |
| **this** book / **these** books | **this** books |

#### 3. Pronoun-Antecedent Agreement
Pronouns must match the noun they refer to.

| Correct | Incorrect (formal) |
|---------|-------------------|
| The student finished **his/her** work | The student finished **their** work |
| Each student finished **his/her** exam | Each student finished **their** exam |

### Agreement in Other Languages

**Spanish example:**
- el gato **blanco** (masculine singular)
- la casa **blanca** (feminine singular)
- los gatos **blancos** (masculine plural)
- las casas **blancas** (feminine plural)

---

## Segment 4: Agreement Checking in Python

```python
def check_subject_verb_agreement(subject, verb):
    """Simple check for subject-verb agreement"""
    singular_subjects = ['dog', 'cat', 'student', 'person', 'man', 'woman']
    singular_verbs = ['runs', 'eats', 'sleeps', 'is', 'was']
    plural_verbs = ['run', 'eat', 'sleep', 'are', 'were']
    
    # Determine subject number
    if subject.endswith('s') or subject in ['they', 'we']:
        subj_number = 'plural'
    else:
        subj_number = 'singular'
    
    # Determine verb number
    if verb in singular_verbs:
        verb_number = 'singular'
    elif verb in plural_verbs:
        verb_number = 'plural'
    else:
        return "Cannot determine verb number"
    
    if subj_number != verb_number:
        return f"Error: '{subject}' ({subj_number}) does not agree with '{verb}' ({verb_number})"
    return "Agreement OK"

# Test examples
print(check_subject_verb_agreement("dog", "runs"))   # OK
print(check_subject_verb_agreement("dogs", "run"))   # OK
print(check_subject_verb_agreement("dog", "run"))      # Error
print(check_subject_verb_agreement("dogs", "runs"))    # Error
```

### Why Agreement Matters in NLP

| Application | Why Agreement Matters |
|-------------|----------------------|
| **Grammar checking** | Flag errors in writing |
| **Text generation** | Ensure output is grammatical |
| **Machine translation** | Preserve grammatical features |
| **Speech recognition** | Disambiguate similar sounds |

---

## Segment 5: Complete Syntactic Pipeline Example

```python
import nltk
from nltk import pos_tag, word_tokenize, RegexpParser
from nltk.tree import Tree

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

text = "The quick brown fox jumps over the lazy dog."
print(f"Original: {text}\n")

# Step 1: Tokenise
tokens = word_tokenize(text)
print(f"1. Tokens: {tokens}\n")

# Step 2: POS Tag
tags = pos_tag(tokens)
print("2. POS Tags:")
for word, tag in tags:
    print(f"   {word:12} {tag}")

# Step 3: Chunk
gamma = r"NP: {<DT>?<JJ>*<NN>+}"
parser = RegexpParser(gamma)
tree = parser.parse(tags)
print(f"\n3. Chunks: {tree}")

# Summary
print("\n" + "="*50)
print("SUMMARY")
print("="*50)
print(f"• Main subject: 'fox'")
print(f"• Main verb: 'jumps'")
print(f"• Noun phrases: 'The quick brown fox', 'the lazy dog'")
print(f"• Grammatical check: Subject (fox/singular) + Verb (jumps/singular) = OK")
```

---

## Segment 6: Session Summary

### Key Takeaways

1. **Parse trees** visualize sentence structure hierarchically
2. **Treebank format** uses bracket notation to store trees
3. **Grammatical agreement** ensures words match in number, person, and gender
4. **Subject-verb agreement** is the most critical type
5. **Agreement checking** is essential for grammar checking and text generation

### Practice Questions

**1. What are the four types of nodes in a parse tree?**
<details><summary>Answer</summary>Root, non-terminals, pre-terminals, terminals.</details>

**2. What is the subject-verb agreement rule?**
<details><summary>Answer</summary>Singular subjects take singular verbs, plural subjects take plural verbs.</details>

**3. Why is "The group of students are arguing" grammatically incorrect?**
<details><summary>Answer</summary>The subject is "group" (singular), so the verb should be "is" not "are."</details>

**4. Write the treebank notation for: "The cat sleeps."**
<details><summary>Answer</summary>(S (NP (DT The) (NN cat)) (VP (VBZ sleeps)))</details>

---

## Complete Syntactic Processing Series Summary

You have now learned:

**Part 1:** POS Tagging and Shallow Parsing
- Labeling words with grammatical types
- Grouping words into phrases

**Part 2:** Context-Free Grammar and Parsing
- Grammar rules for valid sentences
- Constituency and dependency parsing

**Part 3:** Tree Structures and Grammatical Agreement
- Visualizing sentence structure
- Ensuring grammatical correctness

**What Comes Next?** Semantic Processing—understanding what sentences actually mean.
