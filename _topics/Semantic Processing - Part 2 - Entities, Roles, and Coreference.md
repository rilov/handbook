---
title: "Semantic Processing Part 2 - Entities, Roles, and Coreference"
category: Natural Language Processing
order: 7
tags:
  - nlp
  - semantic-processing
  - named-entity-recognition
  - semantic-role-labelling
  - coreference-resolution
  - iob-labelling
  - conditional-random-fields
  - beginners
  - friendly
summary: Learn how computers identify who is doing what to whom in a sentence. Covers Semantic Role Labelling, Named Entity Recognition, IOB tagging, Conditional Random Fields, and Coreference Resolution—with simple explanations and Python examples.
---

# Semantic Processing Part 2 - Entities, Roles, and Coreference

## Where We Left Off

Part 1 explained how computers understand the meaning of individual words—through lexical semantics, word sense disambiguation, and co-occurrence patterns.

Now we zoom out to the full sentence. The question changes from *"what does this word mean?"* to:

- **Who or what is mentioned?** → Named Entity Recognition
- **Who did what to whom?** → Semantic Role Labelling
- **When two words refer to the same thing?** → Coreference Resolution

These are the tools that turn raw text into structured, queryable knowledge.

---

## Section 1: Semantic Role Labelling — Who Did What to Whom?

### The Core Question

Read this sentence:

> *"The chef carefully sliced the tomatoes with a sharp knife in the kitchen."*

As a human you instantly know:
- **Who performed the action?** The chef
- **What action was performed?** sliced
- **What was acted upon?** the tomatoes
- **How was it done?** carefully, with a sharp knife
- **Where did it happen?** in the kitchen

Computers need to learn this too. **Semantic Role Labelling (SRL)** is the task of automatically identifying these roles.

### Semantic Roles Explained Simply

Each participant in an event plays a **role**. The key roles are:

| Role | Plain English | Example from above |
|------|---------------|--------------------|
| **Agent** | Who/what did the action | the chef |
| **Patient / Theme** | Who/what received the action | the tomatoes |
| **Instrument** | What was used to do it | a sharp knife |
| **Location** | Where it happened | in the kitchen |
| **Manner** | How it was done | carefully |
| **Time** | When it happened | (not in this sentence) |
| **Beneficiary** | Who benefited | (e.g. "for the guests") |

### Why SRL Matters

Without SRL, a computer cannot tell the difference between:

> *"The dog bit the man."*
> *"The man bit the dog."*

Both sentences contain the same three entities. SRL tells you **which one is the biter (Agent) and which is the bitten (Patient)**—which completely changes the meaning.

**Real-world uses:**
- **Question answering:** "Who made the decision?" → find the Agent of "decided"
- **Information extraction:** Pull structured facts from news articles
- **Machine translation:** Preserve *who does what* across languages

### Python Example with spaCy

```python
import spacy

nlp = spacy.load("en_core_web_sm")

sentence = "The chef sliced the tomatoes with a sharp knife."
doc = nlp(sentence)

print(f"{'Token':<15} {'Dep Label':<15} {'Head':<15} {'Role Hint'}")
print("-" * 65)

role_hints = {
    "nsubj": "→ likely Agent",
    "dobj":  "→ likely Patient/Theme",
    "pobj":  "→ Instrument / Location",
    "ROOT":  "→ Main verb (the event)",
    "advmod":"→ Manner",
}

for token in doc:
    hint = role_hints.get(token.dep_, "")
    print(f"{token.text:<15} {token.dep_:<15} {token.head.text:<15} {hint}")
```

**Output:**
```
Token           Dep Label       Head            Role Hint
-----------------------------------------------------------------
The             det             chef
chef            nsubj           sliced          → likely Agent
sliced          ROOT            sliced          → Main verb (the event)
the             det             tomatoes
tomatoes        dobj            sliced          → likely Patient/Theme
with            prep            sliced
a               det             knife
sharp           amod            knife
knife           pobj            with            → Instrument / Location
.               punct           sliced
```

---

## Section 2: Named Entity Recognition — Spotting the Important Nouns

### What Is a Named Entity?

A **named entity** is a real-world object with a proper name: a person, a place, a company, a date, a currency amount. Not just any noun—specifically the ones that refer to something specific and identifiable.

| Not a Named Entity | Named Entity |
|-------------------|--------------|
| "the city" | "London" |
| "the CEO" | "Elon Musk" |
| "a bank" | "Barclays" |
| "last year" | "2023" |
| "a large sum" | "$4.5 billion" |

### Entity Types

The standard set of entity types used in most NLP systems:

| Label | Meaning | Examples |
|-------|---------|----------|
| **PERSON** | People's names | Tim Cook, Marie Curie |
| **ORG** | Organisations | Apple, WHO, Oxford University |
| **GPE** | Countries, cities, states | India, New York, California |
| **LOC** | Non-political locations | the Sahara, Mount Everest |
| **DATE** | Dates and periods | 14 June 2026, last Tuesday |
| **TIME** | Times of day | 3pm, midnight |
| **MONEY** | Monetary values | $500, £1.2 million |
| **PERCENT** | Percentages | 45%, a third |
| **PRODUCT** | Products | iPhone 15, Tesla Model S |
| **EVENT** | Named events | the World Cup, World War II |

### A Real Example

> *"Apple CEO Tim Cook announced that the company earned $94.8 billion in revenue during Q4 2023 at an event in Cupertino."*

```
Tim Cook     → PERSON
Apple        → ORG
$94.8 billion → MONEY
Q4 2023      → DATE
Cupertino    → GPE
```

This is the kind of structured information you can extract automatically from thousands of news articles—building knowledge databases without any human reading.

### Python Example with spaCy

```python
import spacy

nlp = spacy.load("en_core_web_sm")

text = """
Apple CEO Tim Cook announced that the company earned $94.8 billion 
in revenue during Q4 2023 at an event in Cupertino, California.
"""

doc = nlp(text)

print(f"{'Entity':<25} {'Label':<12} {'Explanation'}")
print("-" * 60)
for ent in doc.ents:
    print(f"{ent.text:<25} {ent.label_:<12} {spacy.explain(ent.label_)}")
```

**Output:**
```
Entity                    Label        Explanation
------------------------------------------------------------
Apple                     ORG          Companies, agencies, institutions
Tim Cook                  PERSON       People, including fictional
$94.8 billion             MONEY        Monetary values, including unit
Q4 2023                   DATE         Absolute or relative dates or periods
Cupertino                 GPE          Countries, cities, states
California                GPE          Countries, cities, states
```

---

## Section 3: IOB Labelling — How NER Tags Words in Sequence

### The Problem with Simple Tagging

Imagine you have this sentence and you want to tag "Tim Cook" as a PERSON:

```
Tim    Cook    announced    the    results
```

If you just label each word, you get:

```
Tim=PERSON    Cook=PERSON    announced=O    the=O    results=O
```

But this does not tell you whether "Tim" and "Cook" are **one entity** (a full name) or **two separate entities**. What if you had "Tim Cook and Sundar Pichai"?

```
Tim=PERSON    Cook=PERSON    and=O    Sundar=PERSON    Pichai=PERSON
```

You cannot tell which words group together.

### IOB Tagging Solves This

**IOB** stands for **Inside, Outside, Beginning**.

Each word gets one of three prefixes:
- **B-** (Beginning): This word **starts** a named entity
- **I-** (Inside): This word is **inside** (continues) a named entity
- **O** (Outside): This word is **not** part of any named entity

**Example:**

```
Tim       → B-PERSON   (Begins a PERSON entity)
Cook      → I-PERSON   (Inside the same PERSON entity)
announced → O          (Not an entity)
the       → O
results   → O
from      → O
Apple     → B-ORG      (Begins an ORG entity)
```

Now it is crystal clear: "Tim Cook" is one entity, "Apple" is another.

### A More Complex Example

> *"Sundar Pichai joined Google in 2004 and became CEO in August 2015."*

```
Sundar    → B-PERSON
Pichai    → I-PERSON
joined    → O
Google    → B-ORG
in        → O
2004      → B-DATE
and       → O
became    → O
CEO       → O
in        → O
August    → B-DATE
2015      → I-DATE
```

Notice "August 2015" is correctly identified as one DATE entity (B then I), while "2004" is a standalone DATE (just B, no I follows).

### Python: Applying IOB Tags

```python
import spacy

nlp = spacy.load("en_core_web_sm")

text = "Sundar Pichai joined Google in 2004 and became CEO in August 2015."
doc = nlp(text)

print(f"{'Token':<12} {'IOB Tag':<10} {'Entity Type'}")
print("-" * 40)

for token in doc:
    iob = token.ent_iob_   # 'B', 'I', or 'O'
    etype = token.ent_type_ or "-"
    label = f"{iob}-{etype}" if iob != "O" else "O"
    print(f"{token.text:<12} {label:<10} {etype}")
```

**Output:**
```
Token        IOB Tag    Entity Type
----------------------------------------
Sundar       B-PERSON   PERSON
Pichai       I-PERSON   PERSON
joined       O          -
Google       B-ORG      ORG
in           O          -
2004         B-DATE     DATE
and          O          -
became       O          -
CEO          O          -
in           O          -
August       B-DATE     DATE
2015         I-DATE     DATE
.            O          -
```

---

## Section 4: Conditional Random Fields — Teaching the Sequence

### Why Word-by-Word Classification Is Not Enough

You could train a simple classifier that looks at each word in isolation and decides its IOB tag. But this ignores something crucial: **the tags of neighbouring words constrain each other**.

Think about these rules that a good tagger should follow:
- An `I-PERSON` tag should only follow a `B-PERSON` or another `I-PERSON`, never an `O` or `B-ORG`
- After a `B-DATE`, you would expect either `I-DATE` or `O`, not `B-DATE` again
- Two consecutive `B-` tags of the same type usually means two separate entities

A word-by-word classifier has no way to enforce these constraints. **Conditional Random Fields (CRFs)** solve this.

### CRFs in Plain English

A **Conditional Random Field** is a model that considers the entire sequence of labels at once, rather than labelling each word independently.

Think of it like this:

**Simple classifier (word-by-word):**
> "I see the word 'Cook'. Based on this word alone, is it PERSON, ORG, or O?"

**CRF (sequence-aware):**
> "I see the word 'Cook'. The previous word 'Tim' was tagged B-PERSON. What is the most likely tag for 'Cook' given both the word itself AND the previous tag?"

The CRF learns transition probabilities:
- `P(I-PERSON | previous=B-PERSON)` is very high
- `P(B-ORG | previous=B-PERSON)` is very low

### Features a CRF Uses

A CRF does not just look at the raw word—it uses carefully crafted features:

| Feature | Example for word "Apple" |
|---------|--------------------------|
| The word itself | "Apple" |
| Is it capitalised? | Yes |
| Previous word | "bought" |
| Next word | "shares" |
| Does it end in common suffix? | No (-ing, -ed, -ly) |
| Is it in a company name list? | Yes |
| Part-of-speech tag | NN (noun) |

The CRF combines all these features to make a decision about the full tag sequence.

### Python: CRF for NER with sklearn-crfsuite

```python
# pip install sklearn-crfsuite

import sklearn_crfsuite
from sklearn_crfsuite import metrics

def word_features(sentence, i):
    """Extract features for word at position i"""
    word = sentence[i][0]   # the word
    postag = sentence[i][1] # its POS tag
    
    features = {
        'word.lower': word.lower(),
        'word.isupper': word.isupper(),
        'word.istitle': word.istitle(),  # Is it capitalised?
        'word.isdigit': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],        # First 2 chars of POS tag
        'word[-3:]': word[-3:],          # Last 3 chars (suffix)
        'word[-2:]': word[-2:],          # Last 2 chars
    }
    
    # Features from previous word
    if i > 0:
        prev_word = sentence[i-1][0]
        features['prev_word.lower'] = prev_word.lower()
        features['prev_word.istitle'] = prev_word.istitle()
    else:
        features['BOS'] = True  # Beginning of sentence
    
    # Features from next word
    if i < len(sentence) - 1:
        next_word = sentence[i+1][0]
        features['next_word.lower'] = next_word.lower()
        features['next_word.istitle'] = next_word.istitle()
    else:
        features['EOS'] = True  # End of sentence
    
    return features

def sentence_features(sentence):
    return [word_features(sentence, i) for i in range(len(sentence))]

def sentence_labels(sentence):
    return [label for _, _, label in sentence]

# Example training data: (word, pos_tag, iob_label)
train_sentences = [
    [("Tim", "NNP", "B-PERSON"), ("Cook", "NNP", "I-PERSON"),
     ("joined", "VBD", "O"), ("Apple", "NNP", "B-ORG")],
    [("London", "NNP", "B-GPE"), ("is", "VBZ", "O"),
     ("a", "DT", "O"), ("city", "NN", "O")],
]

X_train = [sentence_features(s) for s in train_sentences]
y_train = [sentence_labels(s) for s in train_sentences]

# Train CRF
crf = sklearn_crfsuite.CRF(algorithm='lbfgs', max_iterations=100)
crf.fit(X_train, y_train)
```

---

## Section 5: Coreference Resolution — When Two Words Mean the Same Thing

### The Problem

Read this paragraph:

> *"Marie Curie was a physicist. **She** conducted research in Paris. **Her** work on radioactivity won **her** two Nobel Prizes. **The scientist** changed science forever."*

As a human, you instantly know:
- "She" = Marie Curie
- "Her" = Marie Curie
- "The scientist" = Marie Curie

A computer reading this paragraph in chunks would treat "Marie Curie", "She", "Her", and "The scientist" as four separate entities—and fail to connect them into a unified picture.

**Coreference resolution** is the task of finding all mentions that refer to the same real-world entity and linking them together.

### Key Terms

| Term | Meaning | Example |
|------|---------|---------|
| **Mention** | Any reference to an entity | "Marie Curie", "she", "the scientist" |
| **Coreference cluster** | All mentions of the same entity | {Marie Curie, she, her, the scientist} |
| **Antecedent** | The main, introducing mention | "Marie Curie" |
| **Anaphor** | A later reference back to it | "she", "her" |

### Why It Matters

Without coreference resolution:

**Question:** "What did Marie Curie win?"

**Computer sees:** "She won two Nobel Prizes" — but "she" is not connected to "Marie Curie" in the computer's memory, so it cannot answer correctly.

**With coreference resolution:**

All mentions are linked → the computer knows "she" = "Marie Curie" → can answer: "two Nobel Prizes."

**Other applications:**
- Summarisation: Avoid repeating full names repeatedly
- Information extraction: Build complete profiles of entities
- Chatbots: Remember that "it" in a follow-up question refers to the product mentioned earlier

### Types of References

| Type | Description | Example |
|------|-------------|---------|
| **Pronoun** | Personal pronouns | she, he, it, they |
| **Definite description** | "the + noun" | "the scientist", "the company" |
| **Proper name repetition** | Repeating the name | "Curie" after "Marie Curie" |
| **Demonstrative** | this, that, these | "This discovery proved..." |

### How Coreference Resolution Works

**Step 1: Mention detection**
Find all noun phrases that could be entity references.

```
Mentions: [Marie Curie], [a physicist], [She], [Paris], [Her work], 
          [radioactivity], [her], [two Nobel Prizes], [The scientist]
```

**Step 2: Coreference clustering**
Group mentions that refer to the same entity.

```
Cluster 1 (Marie Curie): {Marie Curie, a physicist, She, her, The scientist}
Cluster 2 (Paris):       {Paris}
Cluster 3 (Nobel Prizes):{two Nobel Prizes}
```

**Step 3: Resolution**
For downstream tasks, replace all mentions in a cluster with the canonical name.

### Python Example with spaCy

```python
# pip install spacy
# python -m spacy download en_core_web_sm
# Note: full coreference requires neuralcoref or spacy-experimental

import spacy

# Simple example using spaCy's built-in token references
nlp = spacy.load("en_core_web_sm")

text = "Marie Curie was a physicist. She worked in Paris. Her research was groundbreaking."
doc = nlp(text)

# Print all noun phrases (candidate mentions)
print("Candidate mentions (noun phrases):")
for chunk in doc.noun_chunks:
    print(f"  '{chunk.text}' — root: {chunk.root.text}, dep: {chunk.root.dep_}")

# Print pronouns (likely anaphors)
print("\nPronouns (likely referring back to something):")
for token in doc:
    if token.pos_ == "PRON":
        print(f"  '{token.text}' at position {token.i}")
```

### A Simple Rule-Based Approach

```python
def simple_coref_resolve(text):
    """
    Very simple rule-based coreference:
    Replace pronouns with the most recent named entity of matching gender.
    (Simplified - real systems are far more sophisticated)
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    last_person = None
    resolved = []
    
    for token in doc:
        if token.ent_type_ == "PERSON":
            last_person = token.text
            resolved.append(token.text)
        elif token.text.lower() in ["she", "her", "he", "his", "him"] and last_person:
            resolved.append(f"{token.text}[={last_person}]")
        else:
            resolved.append(token.text)
    
    return " ".join(resolved)

text = "Marie Curie was a physicist. She worked tirelessly. Her research changed science."
print(simple_coref_resolve(text))
# Marie Curie was a physicist. She[=Curie] worked tirelessly. Her[=Curie] research changed science.
```

---

## Section 6: Putting It All Together

Here is how the semantic layer builds up across a single sentence:

> *"Apple CEO Tim Cook announced record profits in Cupertino last Tuesday, and he said the company would invest in AI."*

**Named Entity Recognition:**
```
Tim Cook  → PERSON
Apple     → ORG
Cupertino → GPE
last Tuesday → DATE
```

**IOB Tagging:**
```
Apple/B-ORG  CEO/O  Tim/B-PERSON  Cook/I-PERSON  announced/O 
record/O  profits/O  in/O  Cupertino/B-GPE  last/B-DATE  Tuesday/I-DATE
```

**Semantic Role Labelling:**
```
Agent:    Tim Cook  (who announced)
Action:   announced
Theme:    record profits  (what was announced)
Location: Cupertino
Time:     last Tuesday
```

**Coreference Resolution:**
```
"he"      → Tim Cook
"the company" → Apple
```

**Result:** A structured, queryable fact:
> WHO: Tim Cook (Agent, from Apple)  
> DID WHAT: announced  
> WHAT: record profits  
> WHERE: Cupertino  
> WHEN: last Tuesday  
> FOLLOW-UP: Tim Cook said Apple would invest in AI  

This is how modern systems turn raw news text into structured knowledge databases.

---

## Section 7: Practice Questions

**1. What is the difference between an Agent and a Patient in semantic roles?**
<details><summary>Answer</summary>
The Agent performs the action (the doer). The Patient receives or is affected by the action (the target). In "The chef sliced the tomatoes," the chef is the Agent and the tomatoes are the Patient.
</details>

**2. What do B-, I-, and O- mean in IOB tagging?**
<details><summary>Answer</summary>
B- = Beginning of a named entity. I- = Inside (continuation of) the same entity. O = Outside (not part of any entity).
</details>

**3. Why do CRFs outperform word-by-word classifiers for NER?**
<details><summary>Answer</summary>
CRFs consider the full sequence of labels, learning which tag transitions are valid (e.g. I-PERSON should follow B-PERSON) instead of treating each word independently.
</details>

**4. What is coreference resolution? Why does it matter for question answering?**
<details><summary>Answer</summary>
Coreference resolution links all mentions of the same entity (e.g. "Marie Curie", "she", "the scientist"). Without it, a QA system cannot connect "What did she win?" to "Marie Curie won two Nobel Prizes."
</details>

**5. In the sentence "Amazon fired 9,000 workers. The company cited economic pressures.", what is the coreference cluster?**
<details><summary>Answer</summary>
{Amazon, The company} — both refer to the same organisation.
</details>

---

## Summary

| Technique | Question It Answers | Output |
|-----------|---------------------|--------|
| Semantic Role Labelling | Who did what to whom, how, where, when? | Agent, Patient, Instrument, Location, Time labels |
| Named Entity Recognition | What real-world things are mentioned? | PERSON, ORG, GPE, DATE, MONEY labels |
| IOB Tagging | Which words belong to the same entity? | B-/I-/O prefix labels |
| Conditional Random Fields | What is the best tag sequence overall? | Full IOB tag sequence |
| Coreference Resolution | Which mentions refer to the same entity? | Coreference clusters |

---

## What Comes Next?

Now you understand how computers extract meaning from text. The next guide covers **Classical Text Generation**—how computers produce new text using statistical methods like N-gram language models and Markov chains, before the era of neural networks.
