---
title: "Classical Text Generation Part 2 - Summarisation and Translation"
category: Natural Language Processing
order: 10
tags:
  - nlp
  - text-generation
  - sentence-generation
  - summarisation
  - machine-translation
  - classical-nlp
  - beginners
  - friendly
summary: Learn how classical NLP systems generate sentences, automatically summarise documents, and translate between languages—before neural networks. Covers controlled sentence generation, extractive summarisation, and rule-based and statistical machine translation.
---

# Classical Text Generation Part 2 - Summarisation and Translation

## Where We Left Off

Part 1 covered N-gram language models, perplexity, smoothing, and Markov chains — the statistical foundations of language generation.

Now we put those foundations to work. This guide answers three practical questions:

1. **Sentence Generation:** How do you generate text that sounds intentional, not random?
2. **Classical Summarisation:** How do you automatically shorten a long document to its key points?
3. **Machine Translation:** How did computers translate between languages before neural networks?

---

## Section 1: Sentence Generation — Beyond Random Sampling

### The Problem with Pure Random Sampling

In Part 1, you built a Markov text generator that randomly followed transitions. The output was vaguely English-shaped but often nonsensical:

```
"the cat ate the floor the dog sat on the fish"
```

Words and transitions follow the training distribution — but there is no goal, no coherence, no control.

Real applications need better strategies for choosing the next word at each step.

### Strategy 1: Greedy Decoding

At every step, always pick the **most probable** next word.

```python
def greedy_generate(model, start_word, length=15):
    """Always pick the most likely next word"""
    current = start_word
    output = [current]
    
    for _ in range(length - 1):
        if current not in model:
            break
        next_counts = model[current]
        # Pick the word with highest count
        best_word = max(next_counts, key=next_counts.get)
        output.append(best_word)
        current = best_word
        
        if best_word in ['.', '<END>']:
            break
    
    return ' '.join(output)
```

**Problem:** Greedy decoding gets stuck in loops.

```
Input: "the"
Output: "the cat sat on the mat on the mat on the mat..."
```

Because "the" → "cat" → "sat" → "on" → "the" is the most probable path, the model keeps circling.

### Strategy 2: Beam Search

Instead of committing to the single best word at each step, beam search keeps the **top K candidates** (the "beam") alive at each step.

```
Beam width = 3

Step 1 — Start with "I":
  Keep top 3 next words: [love (0.6), hate (0.2), like (0.15)]

Step 2 — Expand each:
  "I love" → [cats (0.4), dogs (0.4), pizza (0.2)]
  "I hate" → [rain (0.5), mondays (0.3), traffic (0.2)]
  "I like" → [coffee (0.5), running (0.3), reading (0.2)]
  
  Keep top 3 full sequences so far:
    "I love cats"   (score: 0.6 × 0.4 = 0.24)
    "I love dogs"   (score: 0.6 × 0.4 = 0.24)
    "I hate rain"   (score: 0.2 × 0.5 = 0.10)

Step 3 — Keep expanding the survivors...
```

At the end, pick the sequence with the highest total probability score.

```python
import heapq
from collections import defaultdict, Counter

def beam_search(model, start_word, beam_width=3, max_length=10):
    """
    Beam search text generation.
    model: dict of {word: Counter of next words}
    """
    import math
    
    # Beam: list of (log_prob, word_sequence)
    beam = [(0.0, [start_word])]
    completed = []
    
    for _ in range(max_length):
        candidates = []
        
        for log_prob, sequence in beam:
            current_word = sequence[-1]
            
            if current_word == '<END>' or current_word == '.':
                completed.append((log_prob, sequence))
                continue
            
            if current_word not in model:
                completed.append((log_prob, sequence))
                continue
            
            total = sum(model[current_word].values())
            
            # Expand: try every possible next word
            for next_word, count in model[current_word].items():
                prob = count / total
                new_log_prob = log_prob + math.log(prob + 1e-10)
                candidates.append((new_log_prob, sequence + [next_word]))
        
        if not candidates:
            break
        
        # Keep only top beam_width candidates
        beam = heapq.nlargest(beam_width, candidates, key=lambda x: x[0])
    
    completed.extend(beam)
    
    # Return the best sequence
    best_log_prob, best_sequence = max(completed, key=lambda x: x[0])
    return ' '.join(best_sequence), best_log_prob

# Example usage
from collections import defaultdict, Counter
import random

# Build a small bigram model
corpus = """
i love cats and dogs . 
i love pizza and pasta .
cats love fish and milk .
dogs love bones and running .
the cat sat on the mat .
the dog ran in the park .
"""

model = defaultdict(Counter)
words = corpus.split()
for i in range(len(words) - 1):
    model[words[i]][words[i+1]] += 1

# Generate with beam search
result, score = beam_search(model, "i", beam_width=3, max_length=8)
print(f"Beam search output: {result}")
print(f"Log probability: {score:.2f}")
```

**Beam search produces more coherent text** than greedy or random sampling, which is why it is used in machine translation and text summarisation systems.

### Strategy 3: Temperature Sampling

Instead of always picking the most probable word (greedy) or randomly sampling from the raw distribution (flat), temperature sampling lets you control how "adventurous" the model is.

```
Temperature T:
  T = 1.0   → sample from the original distribution
  T < 1.0   → more conservative, likely words dominate (towards greedy)
  T > 1.0   → more adventurous, unlikely words get a chance (more random)
```

```python
import numpy as np

def temperature_sample(word_counts, temperature=1.0):
    """
    Sample next word with temperature control.
    """
    words = list(word_counts.keys())
    counts = np.array(list(word_counts.values()), dtype=float)
    
    # Apply temperature: divide log probabilities by T
    scaled = counts ** (1.0 / temperature)
    probs = scaled / scaled.sum()
    
    return np.random.choice(words, p=probs)

# Compare temperatures on "love" → next word
from collections import Counter
love_follows = Counter({'cats': 10, 'dogs': 8, 'pizza': 3, 'running': 1, 'jazz': 1})

print("Next word after 'love':")
print("\nT=0.3 (conservative, repeats top words):")
for _ in range(5):
    print(" ", temperature_sample(love_follows, temperature=0.3))

print("\nT=1.0 (normal sampling):")
for _ in range(5):
    print(" ", temperature_sample(love_follows, temperature=1.0))

print("\nT=2.0 (adventurous, rare words appear more):")
for _ in range(5):
    print(" ", temperature_sample(love_follows, temperature=2.0))
```

Temperature is used everywhere — including modern GPT-style models. When you see a "creativity" slider in an AI writing tool, it is usually adjusting temperature.

---

## Section 2: Classical Summarisation — Keeping What Matters

### What Is Automatic Summarisation?

Automatic summarisation compresses a document down to its key points. Two fundamentally different approaches:

| Approach | Method | Output |
|----------|--------|--------|
| **Extractive** | Pick the most important existing sentences | Original sentences, rearranged/selected |
| **Abstractive** | Generate new sentences that capture the meaning | New text, may not appear in original |

Classical methods are almost entirely **extractive** — they identify and select the best sentences rather than generating new ones. Abstractive summarisation required neural networks to become practical.

### How Extractive Summarisation Works

The core task: **rank every sentence by importance, then pick the top N**.

The challenge: what makes a sentence "important"?

#### Signal 1: TF-IDF Score

Sentences containing words with high TF-IDF scores are likely important — they contain the distinctive vocabulary of the document.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def tfidf_summarise(text, num_sentences=3):
    """Extractive summarisation using TF-IDF sentence scoring"""
    
    # Split into sentences
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    if len(sentences) <= num_sentences:
        return text
    
    # Build TF-IDF over sentences (treating each sentence as a document)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # Score each sentence: sum of its word TF-IDF scores
    sentence_scores = np.asarray(tfidf_matrix.sum(axis=1)).flatten()
    
    # Pick top N sentences (preserve original order)
    top_indices = sorted(
        np.argsort(sentence_scores)[-num_sentences:].tolist()
    )
    
    summary = ' '.join(sentences[i] for i in top_indices)
    return summary

# Test
article = """
The Amazon rainforest is the world's largest tropical rainforest, covering over 
five and a half million square kilometres. It is home to an estimated 10% of all 
species on Earth, including jaguars, anacondas, and hundreds of bird species. 
The forest plays a critical role in regulating the global climate by absorbing 
enormous amounts of carbon dioxide. Deforestation is the biggest threat to the 
Amazon, with cattle ranching and agriculture responsible for most land clearance. 
In recent years, the rate of deforestation has accelerated, alarming scientists 
and conservationists worldwide. Protecting the Amazon is considered essential 
for meeting global climate targets and preserving biodiversity. Several 
international agreements aim to reduce deforestation, but enforcement remains 
a significant challenge.
"""

summary = tfidf_summarise(article, num_sentences=3)
print("SUMMARY:")
print(summary)
```

#### Signal 2: Sentence Position

Position in a document is a strong signal:
- **First sentence of each paragraph** → usually a topic sentence
- **First and last sentences of the whole document** → introduction and conclusion
- **Sentences in early paragraphs** → typically more important

```python
def position_score(sentence_index, total_sentences):
    """
    Sentences at the beginning score higher.
    Simple linear decay.
    """
    return 1.0 - (sentence_index / total_sentences) * 0.5
```

#### Signal 3: Keyword Frequency

Sentences that contain words which appear frequently throughout the document are likely about the central topic.

```python
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def keyword_score(sentence, document_word_freq, stop_words):
    """Score a sentence by the frequency of its content words"""
    words = word_tokenize(sentence.lower())
    content_words = [w for w in words if w.isalpha() and w not in stop_words]
    
    if not content_words:
        return 0
    
    return sum(document_word_freq.get(w, 0) for w in content_words) / len(content_words)
```

### TextRank — Graph-Based Summarisation

**TextRank** is one of the most popular classical summarisation algorithms. It adapts Google's PageRank — the algorithm that ranks web pages — to rank sentences.

The idea: **sentences that are similar to many other sentences are central to the document and therefore important**.

```
Step 1: Represent every sentence as a TF-IDF vector
Step 2: Build a graph where sentences are nodes
Step 3: Add edges between sentences weighted by their cosine similarity
Step 4: Run PageRank — important sentences have many strong connections
Step 5: Pick top N sentences by PageRank score
```

```python
# pip install sumy  (implements TextRank and other summarisers)
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def textrank_summarise(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return ' '.join(str(sentence) for sentence in summary)

# Or using the popular gensim implementation
from gensim.summarization import summarize  # gensim < 4.0

summary = summarize(article, ratio=0.3)  # Keep 30% of original
```

### Limitations of Classical Summarisation

| Limitation | Why It Happens |
|------------|---------------|
| Cannot merge information from multiple sentences | Only selects, never generates |
| May miss implicit key points | Does not understand meaning |
| Repetition between selected sentences | No awareness of redundancy |
| Cannot infer or abstract | Purely statistical |

These limitations are why **abstractive summarisation** with neural networks (transformers) became so important. Classical summarisation is still used today when speed and interpretability matter.

---

## Section 3: Machine Translation — Crossing the Language Barrier

### The Challenge

Translating between languages is deceptively hard. It is not just swapping words. Languages differ in:

| Difference | Example |
|-----------|---------|
| **Word order** | English: "I love you" → Japanese: "I you love" |
| **Grammatical gender** | French: "le soleil" (masculine sun), "la lune" (feminine moon) |
| **No direct equivalent** | German "Schadenfreude" has no English single word |
| **Idiomatic expressions** | "It's raining cats and dogs" → cannot translate literally |
| **Morphology** | Finnish has 15 grammatical cases; English has almost none |

Classical systems tackled this with two approaches: rule-based and statistical.

### Approach 1: Rule-Based Machine Translation (RBMT)

Linguists hand-write rules to convert one language to another:

```
Rule: In Spanish, adjectives follow nouns (usually)
English: "red car"
Spanish: "coche rojo"  (car red)

Rule: Spanish verbs encode subject in conjugation
English: "I speak / you speak / he speaks"
Spanish: "hablo / hablas / habla"  (no separate pronoun needed)
```

**How RBMT works:**
1. **Parse** the source sentence (get its structure)
2. **Transfer** the structure to the target language structure using rules
3. **Generate** the target language sentence

```
English input: "The old man walks slowly"
    ↓ Parse
[NP: the old man] [VP: walks slowly]
[DET: the] [ADJ: old] [N: man] [V: walks] [ADV: slowly]
    ↓ Transfer rules (EN → ES)
[DET: el] [N: hombre] [ADJ: viejo] [V: camina] [ADV: lentamente]
    ↓ Generate
Spanish output: "El hombre viejo camina lentamente"
```

**Pros:** Predictable, no training data needed, transparent
**Cons:** Thousands of rules to write, brittle for irregular language, enormous maintenance cost

### Approach 2: Statistical Machine Translation (SMT)

Instead of rules, SMT learns translation patterns from **large collections of parallel texts** — the same document in two languages (like EU parliament proceedings translated into all EU languages).

SMT combines two models:

**Translation Model:** What word/phrase in Language B matches what in Language A?

Learned from aligned parallel corpora:
```
"cat" ↔ "gato" (many times in Spanish data)
"dog" ↔ "perro"
"I love" ↔ "yo amo" or "me gusta"
"running water" ↔ "agua corriente" (phrase-level alignment)
```

**Language Model:** Does this output actually sound like natural Language B?

This is the N-gram model from Part 1! The language model ensures the translation is fluent in the target language, not just word-for-word.

**The SMT formula:**

```
Best translation = argmax P(target | source)
                 = argmax P(source | target) × P(target)
                           ↑ translation model  ↑ language model
```

In plain English: find the target sentence that is both a likely translation of the source AND sounds natural in the target language.

### Phrase-Based SMT

A major improvement was moving from word-by-word translation to **phrase-based** translation. The system learns whole phrases as translation units:

```
"New York"      → "Nueva York"   (not "Nueva" + "York" separately)
"by the way"    → "por cierto"   (idiom: translate as unit)
"looking for"   → "buscando"     (verb phrase)
"United States" → "Estados Unidos"
```

```python
# Simplified illustration of phrase-based translation lookup
phrase_table = {
    "the cat": "el gato",
    "the dog": "el perro",
    "is running": "está corriendo",
    "in the park": "en el parque",
    "the cat is running": "el gato está corriendo",
    "in the garden": "en el jardín"
}

def simple_phrase_translate(sentence, phrase_table):
    """
    Very simplified phrase-based translation.
    Tries to match longest phrase first (greedy).
    """
    words = sentence.lower().split()
    result = []
    i = 0
    
    while i < len(words):
        # Try to match longest phrase starting at position i
        matched = False
        for length in range(len(words) - i, 0, -1):
            phrase = ' '.join(words[i:i+length])
            if phrase in phrase_table:
                result.append(phrase_table[phrase])
                i += length
                matched = True
                break
        
        if not matched:
            result.append(f"[{words[i]}?]")  # unknown word
            i += 1
    
    return ' '.join(result)

print(simple_phrase_translate("the cat is running in the park", phrase_table))
# "el gato está corriendo en el parque"
```

### The BLEU Score — Evaluating Translation Quality

How do you measure if a translation is good? **BLEU (Bilingual Evaluation Understudy)** is the standard metric.

The idea: compare the machine translation to one or more **human reference translations**, measuring how many N-grams overlap.

```
Reference: "The cat is on the mat"
Candidate: "The cat is on the mat"        BLEU ≈ 1.0 (perfect)
Candidate: "The cat sat on the mat"       BLEU ≈ 0.8 (one word different)
Candidate: "A feline rests upon the rug"  BLEU ≈ 0.1 (no N-gram overlap)
```

**The maths (simplified):**
```
BLEU = brevity penalty × geometric mean of n-gram precisions for n=1,2,3,4
```

```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

reference = [["the", "cat", "is", "on", "the", "mat"]]
candidate1 = ["the", "cat", "is", "on", "the", "mat"]
candidate2 = ["the", "cat", "sat", "on", "the", "mat"]
candidate3 = ["a", "feline", "rests", "upon", "the", "rug"]

smooth = SmoothingFunction().method1

print(f"Perfect match BLEU:  {sentence_bleu(reference, candidate1, smoothing_function=smooth):.3f}")
print(f"One word off BLEU:   {sentence_bleu(reference, candidate2, smoothing_function=smooth):.3f}")
print(f"Different vocab BLEU:{sentence_bleu(reference, candidate3, smoothing_function=smooth):.3f}")
```

### Why Classical Translation Was Eventually Replaced

Statistical MT dominated the 2000s but had fundamental ceilings:

| Limitation | Why It Matters |
|------------|---------------|
| **No global context** | Translates phrases locally, misses document-level context |
| **Fixed phrase table** | Cannot translate new phrases or terminology |
| **Language model is shallow** | N-gram models cannot capture long-range agreement |
| **Cannot reorder flexibly** | Some language pairs need massive structural reordering |

In 2016-2017, **neural machine translation** (encoder-decoder with attention) overtook all statistical systems, and by 2018 the transformer architecture made it even better. Google Translate switched from phrase-based SMT to neural MT in 2016.

---

## Section 4: The Complete Classical NLP Generation Toolkit

Here is a summary of everything covered across both text generation guides:

```
TASK: Generate text
  ├── Build an N-gram language model (learn from corpus)
  ├── Apply smoothing (Laplace, backoff, interpolation)
  ├── Evaluate quality with perplexity
  └── Generate using:
        ├── Greedy decoding (fast, gets stuck in loops)
        ├── Beam search (best quality, explores K paths)
        └── Temperature sampling (control creativity)

TASK: Summarise a document
  ├── Score sentences by TF-IDF content words
  ├── Score by position in document
  ├── Score by keyword frequency
  ├── Use TextRank (graph-based PageRank on sentence similarity)
  └── Select top N sentences (extractive — no generation needed)

TASK: Translate between languages
  ├── Rule-based: hand-write linguistic transfer rules
  └── Statistical (SMT):
        ├── Learn translation model from parallel corpora
        ├── Learn language model from target language text
        ├── Combine with phrase tables for multi-word units
        └── Evaluate with BLEU score
```

---

## Section 5: Practice Questions

**1. What is the difference between greedy decoding and beam search?**
<details><summary>Answer</summary>
Greedy decoding always picks the single most probable next word at each step. Beam search keeps the top K candidate sequences alive and explores them all, picking the globally best path at the end. Beam search produces better results but is slower.
</details>

**2. What does temperature > 1.0 do to text generation?**
<details><summary>Answer</summary>
It makes the probability distribution flatter, giving unlikely words more chance of being chosen. The output becomes more diverse and creative but also more likely to be incoherent.
</details>

**3. What is the difference between extractive and abstractive summarisation?**
<details><summary>Answer</summary>
Extractive summarisation selects and returns existing sentences from the original document. Abstractive summarisation generates new sentences that capture the meaning, potentially using vocabulary not in the original.
</details>

**4. In TextRank, what does it mean for a sentence to have a high PageRank score?**
<details><summary>Answer</summary>
The sentence is similar to many other sentences in the document, meaning it covers ideas that are central and recurring throughout the text — so it is a good representative of the document's main content.
</details>

**5. In Statistical MT, what role does the language model play?**
<details><summary>Answer</summary>
The translation model picks candidate translations based on word/phrase alignments from parallel data. The language model ensures the output actually sounds fluent and natural in the target language — it filters out grammatically awkward translations.
</details>

**6. What does a BLEU score of 1.0 mean?**
<details><summary>Answer</summary>
The machine translation exactly matches the human reference translation — a perfect score. In practice, scores above 0.4 are considered good for most language pairs.
</details>

**7. Why did phrase-based SMT outperform word-by-word SMT?**
<details><summary>Answer</summary>
Many words change their meaning or form when combined into phrases ("by the way", "New York"). Translating whole phrases as units captures these multi-word patterns, producing more accurate and natural-sounding translations.
</details>
