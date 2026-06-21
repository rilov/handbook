---
title: "NLP Cheat Sheet - Key Terms and Concepts"
category: Natural Language Processing
order: 11
tags:
  - nlp
  - cheat-sheet
  - reference
  - summary
  - glossary
summary: A quick-reference cheat sheet covering every important NLP term and concept from the full tutorial series. Organised by topic—from tokenisation to machine translation—with plain-English definitions and one-line memory aids.
---

# NLP Cheat Sheet — Key Terms and Concepts

A single-page reference for every important concept in the NLP series. Each term has a plain-English definition and a memory aid.

---

## 1. What Is NLP?

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **NLP** | Technology that helps computers understand, interpret, and respond to human language | "Teaching computers to read and talk" |
| **Natural Language** | Human language (messy, flexible, ambiguous) as opposed to programming languages (strict, precise) | "The way you actually speak" |
| **Corpus** | A large collection of text used to train NLP models | "The textbook the model studied" |
| **Token** | A single unit of text — usually a word or punctuation mark | "One piece of the puzzle" |
| **Pipeline** | The sequence of steps that transforms raw text into useful output | "An assembly line for text" |

### The 5 Linguistic Levels (in order)

| Level | Studies | Example |
|-------|---------|---------|
| **Phonetics / Phonology** | Sounds | "knight" and "night" sound identical |
| **Morphology** | Word structure | "un-happi-ness" = prefix + root + suffix |
| **Syntax** | Sentence structure | "Dog bites man" ≠ "Man bites dog" |
| **Semantics** | Meaning | "bank" = river edge OR financial institution |
| **Pragmatics** | Intent in context | "Oh great" after spilling coffee = sarcasm |

### Three Approaches to NLP

| Approach | How It Works | Best For |
|----------|-------------|----------|
| **Rule-Based** | Hand-written linguistic rules | Controlled domains, no training data |
| **Statistical / ML** | Learns patterns from labelled examples | Classification, spam detection |
| **Deep Learning** | Neural networks learn representations | Translation, complex QA, modern LLMs |

---

## 2. Lexical Processing

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **Tokenisation** | Splitting text into individual words or sentences | "Chopping a sentence into pieces" |
| **Word Tokenisation** | Splitting text into individual words | `"Hello world"` → `["Hello", "world"]` |
| **Sentence Tokenisation** | Splitting a paragraph into individual sentences | Handles "Dr. Smith went..." correctly |
| **Text Normalisation** | Making text consistent — lowercase, remove punctuation, expand contractions | "Tidying up before analysis" |
| **Stopwords** | Common words carrying little meaning (the, and, is, at) | "Background noise words" |
| **Morpheme** | The smallest meaningful unit of a word | "un" + "happy" + "ness" |
| **Stemming** | Chopping word endings using rules to get a root form | `running` → `run`, `easily` → `easili` |
| **Lemmatisation** | Converting a word to its dictionary form using vocabulary + grammar | `better` → `good`, `was` → `be` |
| **Lemma** | The dictionary/base form of a word | `ran` → lemma is `run` |
| **Porter Stemmer** | The most widely used stemming algorithm (5 phases of rules) | "The classic chopper" |
| **Spell Correction** | Fixing typos using edit distance and word frequency | "Autocorrect, but for NLP" |
| **Edit Distance (Levenshtein)** | Minimum single-character edits (insert, delete, substitute) to change one word to another | `kitten` → `sitting` = 3 edits |

### Stemming vs Lemmatisation

| | Stemming | Lemmatisation |
|--|----------|---------------|
| **Speed** | Fast | Slower |
| **Output** | May not be real words (`easili`) | Always real words (`good`) |
| **Needs context?** | No | Yes (needs POS tag) |
| **Use when** | Search engines, speed matters | Production NLP, meaning matters |

---

## 3. Syntactic Processing

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **Syntax** | The rules governing how words combine to form grammatical sentences | "Grammar rules for sentences" |
| **POS Tagging** | Labelling each word with its grammatical type (noun, verb, adjective...) | "Putting name tags on words" |
| **Penn Treebank Tags** | Standard tag set used in NLP: NN, VB, JJ, DT, RB, IN, PRP... | The industry standard tag system |
| **Shallow Parsing (Chunking)** | Grouping words into flat phrases (NP, VP, PP) without deep structure | "Sorting words into teams" |
| **Noun Phrase (NP)** | A chunk centred on a noun — "the quick brown fox" | Who/what |
| **Verb Phrase (VP)** | A chunk centred on a verb — "jumps over the fence" | The action |
| **Prepositional Phrase (PP)** | A chunk starting with a preposition — "over the moon" | The relationship |
| **Context-Free Grammar (CFG)** | A set of rules defining valid sentence structures using non-terminals and terminals | "A recipe book for valid sentences" |
| **Constituency Parsing** | Building a hierarchical tree showing phrases within phrases | "A tree of noun/verb boxes" |
| **Dependency Parsing** | Showing direct word-to-word relationships (who does what to whom) | "Drawing arrows between words" |
| **Parse Tree** | A visual tree structure representing grammatical relationships | "The family tree of a sentence" |
| **Root (dependency)** | The main verb — the word all others depend on | "The boss of the sentence" |
| **nsubj** | Nominal subject — who performs the action | `fox` in "the fox jumps" |
| **dobj** | Direct object — what receives the action | `ball` in "kicked the ball" |
| **amod** | Adjectival modifier — adjective modifying a noun | `quick` in "the quick fox" |
| **Grammatical Agreement** | Words matching each other in number, person, or gender | "The dog *runs*" not "The dog *run*" |
| **Subject-Verb Agreement** | Singular subjects take singular verbs; plural subjects take plural verbs | "He *runs* / They *run*" |
| **Ambiguity** | When a sentence has more than one valid parse tree | "I saw the man with the telescope" = 2 meanings |

### Common POS Tags

| Tag | Meaning | Example |
|-----|---------|---------|
| NN | Noun, singular | dog |
| NNS | Noun, plural | dogs |
| NNP | Proper noun | London |
| VB | Verb, base form | eat |
| VBD | Verb, past tense | ate |
| VBG | Verb, gerund | eating |
| JJ | Adjective | quick |
| RB | Adverb | quickly |
| DT | Determiner | the, a |
| IN | Preposition | in, on, at |
| PRP | Personal pronoun | I, he, she |

---

## 4. Semantic Processing

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **Semantics** | The study of meaning in language | "What it actually means" |
| **Lexical Semantics** | The meaning of individual words and how they relate | "The dictionary layer of meaning" |
| **Polysemy** | One word with multiple related meanings | `bank` = financial OR river edge |
| **Synonym** | Words with the same meaning | happy = joyful = glad |
| **Antonym** | Words with opposite meanings | hot ↔ cold |
| **Hyponym** | A more specific type of a broader category | Labrador is a hyponym of Dog |
| **Hypernym** | The broader category that contains more specific words | Animal is a hypernym of Dog |
| **Meronym** | A part of something | wheel is a meronym of car |
| **WordNet** | A large English lexical database grouping words into synsets by meaning | "The official word relationship map" |
| **Synset** | A group of synonymous words sharing the same meaning in WordNet | `{happy, glad, joyful}` |
| **Word Sense Disambiguation (WSD)** | Automatically determining which meaning of a polysemous word is intended | "Picking the right definition from context" |
| **Lesk Algorithm** | WSD method: count overlaps between sentence context words and dictionary definitions | "Match your surroundings to the dictionary" |
| **Distributional Semantics** | The idea that word meaning can be learned from patterns of word co-occurrence | "You know a word by its neighbours" |
| **Co-occurrence Matrix** | A table counting how often each word appears near each other word | "Who hangs out with whom" |
| **PMI (Pointwise Mutual Information)** | Measures whether two words appear together more than expected by chance | `PMI > 0` = genuinely associated |
| **PPMI** | PMI with negative values clipped to zero (more reliable with small data) | "PMI, but only the positives" |
| **Semantic Role Labelling (SRL)** | Identifying who did what to whom, with what, where, and when | "Answering the journalist's 5 Ws" |
| **Agent** | The entity performing an action | "The *chef* sliced the tomatoes" |
| **Patient / Theme** | The entity receiving or affected by an action | "The chef sliced *the tomatoes*" |
| **Instrument** | What was used to perform an action | "Sliced *with a knife*" |
| **Named Entity Recognition (NER)** | Identifying and classifying real-world named things (people, places, organisations) | "Spotting the proper nouns" |
| **IOB Tagging** | Labelling scheme for NER: B- (begins entity), I- (inside entity), O (outside) | "B starts, I continues, O is out" |
| **Conditional Random Field (CRF)** | A sequence model that considers the full label sequence, not just word-by-word | "Makes tag decisions as a team, not alone" |
| **Coreference Resolution** | Linking all mentions of the same entity across a text | "'She' = 'Marie Curie'" |
| **Antecedent** | The first, introducing mention of an entity | "Marie Curie" before "she" |
| **Anaphor** | A later reference that points back to an antecedent | "she", "her", "the scientist" |

### NER Entity Types

| Label | Meaning | Example |
|-------|---------|---------|
| PERSON | People's names | Tim Cook |
| ORG | Organisations | Apple, WHO |
| GPE | Countries, cities, states | London, India |
| DATE | Dates and periods | 14 June 2026 |
| MONEY | Monetary values | $4.5 billion |
| PRODUCT | Named products | iPhone 15 |

---

## 5. Text Representation

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **Bag-of-Words (BoW)** | Represent a document as word counts, ignoring order | "A bag of word counts" |
| **Vocabulary** | The complete set of unique words across all documents | "The master word list" |
| **Document Vector** | A list of numbers representing a document (one number per vocabulary word) | "A document's fingerprint" |
| **TF-IDF** | Weights words by frequency in a document × rarity across all documents | "Common everywhere = boring; rare here = important" |
| **TF (Term Frequency)** | How often a word appears in this specific document | `count / total_words_in_doc` |
| **IDF (Inverse Document Frequency)** | How rare a word is across all documents | `log(total_docs / docs_containing_word)` |
| **Word Embedding** | A dense vector representing a word's meaning, where similar words are close together | "Words as locations in meaning-space" |
| **Word2Vec** | Algorithm that trains embeddings by predicting words from context (or vice versa) | "Learn meaning from neighbours" |
| **CBOW** | Word2Vec variant: predict the centre word from surrounding context words | "Fill in the blank" |
| **Skip-gram** | Word2Vec variant: predict surrounding words from the centre word | "Guess the neighbours" |
| **GloVe** | Embedding method based on factorising the co-occurrence matrix directly | "Embeddings from counting" |
| **Cosine Similarity** | Measures the angle between two vectors — 1 = identical direction, 0 = unrelated | "How closely two vectors point the same way" |
| **Topic Modelling** | Unsupervised discovery of hidden themes in a document collection | "Finding the chapters nobody wrote" |
| **NMF (Non-negative Matrix Factorisation)** | Topic modelling method that decomposes TF-IDF matrix into topics × words | "Split the big table into topic tables" |
| **Topic** | In NMF/LDA: a probability distribution over words that tend to co-occur | "Football topic = {goal, match, player, team...}" |

### BoW vs TF-IDF vs Embeddings

| | BoW | TF-IDF | Embeddings |
|--|-----|--------|-----------|
| **Word order** | Ignored | Ignored | Ignored (basic) |
| **Word relationships** | None | None | Captured |
| **"cat" ≈ "kitten"?** | No | No | Yes |
| **Speed** | Fast | Fast | Slower |
| **Best for** | Simple classification | Search/retrieval | Semantic tasks |

---

## 6. Classical Text Generation

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **Language Model** | A model that assigns probability to a sequence of words | "How likely is this sentence?" |
| **N-gram** | A sequence of N consecutive words | Bigram = 2 words, Trigram = 3 words |
| **Unigram** | Single word, no context | P(cat) |
| **Bigram** | Two consecutive words | P(cat \| the) |
| **Trigram** | Three consecutive words | P(cat \| the, fluffy) |
| **Markov Property** | The next word depends only on the recent past, not the full history | "Only look back a few steps" |
| **Markov Chain** | A system where next state depends only on current state | The mathematical heart of N-gram models |
| **Sparsity Problem** | Most possible word combinations never appear in training data → zero probability | "Can't predict what you've never seen" |
| **Laplace Smoothing** | Add 1 to every N-gram count so nothing has zero probability | "Pretend you saw everything at least once" |
| **Backoff Smoothing** | If the trigram is unseen, try the bigram; if unseen, try the unigram | "Fall back to simpler when stuck" |
| **Interpolation Smoothing** | Mix trigram, bigram, and unigram probabilities with weights | "Blend all levels together" |
| **Perplexity** | How surprised the model is by new text — lower is better | "Average number of equally likely choices per word" |
| **Log Probability** | Log of probability — used to avoid numerical underflow when multiplying many small numbers | "Add instead of multiply" |
| **Greedy Decoding** | Always pick the most probable next word | Fast but gets stuck in loops |
| **Beam Search** | Keep the top K candidate sequences at each step; pick the best at the end | "Explore K paths, keep the winner" |
| **Temperature Sampling** | Control randomness: T < 1 = conservative, T > 1 = creative/random | "The creativity dial" |
| **Extractive Summarisation** | Select and return the most important existing sentences | "Highlight the key sentences" |
| **Abstractive Summarisation** | Generate new sentences capturing the meaning | "Rewrite in your own words" (needs neural networks) |
| **TextRank** | Graph-based summarisation using PageRank on sentence similarity | "The most central sentences win" |
| **BLEU Score** | Metric for machine translation quality — measures N-gram overlap with human reference | "How many phrases did we get right?" |
| **Rule-Based MT (RBMT)** | Translate using hand-written linguistic transfer rules | "Grammar rules as a dictionary" |
| **Statistical MT (SMT)** | Learn translations from parallel corpora; combine translation model + language model | "Learn from millions of translated docs" |
| **Translation Model** | In SMT: which words/phrases in source language map to which in target language | "The vocabulary of translation" |
| **Phrase Table** | In SMT: a lookup of multi-word translation units ("New York" → "Nueva York") | "Translation by phrases, not just words" |
| **Parallel Corpus** | The same document in two languages — used to train SMT | "The bilingual training bible" |

---

## 7. Quick Concept Comparisons

### When to Use What — Text Representation

| If you need... | Use |
|----------------|-----|
| A fast baseline classifier | Bag-of-Words |
| Document search or ranking | TF-IDF |
| Semantic similarity between sentences | Word Embeddings |
| Discover hidden themes with no labels | Topic Modelling (NMF) |

### When to Use What — Text Preprocessing

| If you need... | Use |
|----------------|-----|
| Speed, search engines | Stemming |
| Accurate word forms, production systems | Lemmatisation |
| Remove common uninformative words | Stopword removal |
| But be careful with stopwords for... | Sentiment analysis ("not good") |

### Parsing: Constituency vs Dependency

| | Constituency | Dependency |
|--|-------------|------------|
| **Shows** | Phrase structure (NP, VP) | Word-to-word relations |
| **Output** | Hierarchical tree | Directed graph |
| **Best for** | Grammar checking | Information extraction |

### Smoothing Quick Reference

| Method | How | When |
|--------|-----|------|
| **Laplace** | Add 1 to all counts | Simple baseline |
| **Backoff** | Use shorter N-gram when longer unseen | When most N-grams unseen |
| **Interpolation** | Weighted mix of all N-gram levels | Best general performance |

---

## 8. NLP Pipeline at a Glance

```
Raw Text
  ↓ Text Normalisation      (lowercase, remove punctuation, expand contractions)
  ↓ Tokenisation            (split into words and sentences)
  ↓ Stopword Removal        (filter common words — task dependent)
  ↓ Stemming/Lemmatisation  (reduce to root/dictionary form)
  ↓ POS Tagging             (label each word: noun, verb, adjective...)
  ↓ Parsing                 (understand sentence structure)
  ↓ Text Representation     (convert to numbers: BoW / TF-IDF / Embeddings)
  ↓ Modelling               (classify, generate, summarise, translate)
  ↓ Output
```

---

## 9. Common Python Libraries

| Library | What It Does | Key Uses |
|---------|-------------|----------|
| **NLTK** | Classic NLP toolkit | Tokenisation, POS tagging, stemming, lemmatisation, WordNet |
| **spaCy** | Fast, production-ready NLP | POS tagging, dependency parsing, NER, coreference |
| **scikit-learn** | Machine learning toolkit | BoW, TF-IDF, NMF topic modelling, classifiers |
| **gensim** | Topic modelling and embeddings | Word2Vec, LDA, document similarity |
| **TextBlob** | Simple NLP wrapper | Spell correction, sentiment, basic tagging |
| **sklearn-crfsuite** | CRF implementation | NER sequence labelling |

---

## 10. Ten Things to Remember

1. **Tokenisation is the foundation** — everything else builds on splitting text into tokens.
2. **Stemming is fast but crude; lemmatisation is slow but correct** — choose based on your task.
3. **Word order is lost in BoW and TF-IDF** — if order matters, use embeddings or sequence models.
4. **A word appearing in every document has TF-IDF score of zero** — it is not distinctive.
5. **Word embeddings encode meaning as geometry** — `king - man + woman ≈ queen`.
6. **Perplexity: lower is better** — it measures how surprised the model is.
7. **IOB tagging**: B = begins entity, I = continues entity, O = not an entity.
8. **CRFs beat word-by-word classifiers** because they consider the full label sequence.
9. **Coreference resolution links pronouns to their antecedents** — "she" → "Marie Curie".
10. **PMI > 0 means two words appear together more than chance** — they are genuinely associated.
