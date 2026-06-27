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

A complete reference for every important concept in the NLP series. Each term has a plain-English definition, a memory aid, and where relevant — a formula, example, or common mistake to watch out for.

**How to use this:** Read it top to bottom once, then bookmark it as a lookup when working through the guides or writing code.

---

## 1. What Is NLP?

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **NLP** | Technology that helps computers understand, interpret, and respond to human language | "Teaching computers to read and talk" |
| **Natural Language** | Human language (messy, flexible, ambiguous) as opposed to programming languages (strict, precise) | "The way you actually speak" |
| **Corpus** | A large collection of text used to train NLP models | "The textbook the model studied" |
| **Token** | A single unit of text — usually a word or punctuation mark | "One piece of the puzzle" |
| **Vocabulary** | The set of all unique tokens in a corpus | "The dictionary the model knows" |
| **Pipeline** | The sequence of steps that transforms raw text into useful output | "An assembly line for text" |
| **Annotation** | Human-labelled data (e.g. POS tags, NER labels) used to train models | "The homework a human did for the model" |
| **Inference** | Using a trained model to make predictions on new data | "The model doing its job" |
| **Downstream Task** | The actual goal you care about (e.g. sentiment, translation) built on top of NLP preprocessing | "The final product" |

### Real-World NLP Applications

| Application | What NLP Does |
|-------------|---------------|
| **Spam filter** | Classify emails as spam or not using word patterns |
| **Autocomplete** | Predict the next word using a language model |
| **Spell checker** | Find words with low probability in context |
| **Chatbot** | Parse user intent and generate a response |
| **Sentiment analysis** | Classify reviews as positive, negative, or neutral |
| **Machine translation** | Convert text from one language to another |
| **Text summarisation** | Extract or generate a shorter version of a document |
| **Named entity recognition** | Find people, places, organisations in text |
| **Search engine** | Rank documents by relevance to a query |

### The 5 Linguistic Levels (in order)

| Level | Studies | Example |
|-------|---------|---------|
| **Phonetics / Phonology** | Sounds | "knight" and "night" sound identical |
| **Morphology** | Word structure | "un-happi-ness" = prefix + root + suffix |
| **Syntax** | Sentence structure | "Dog bites man" ≠ "Man bites dog" |
| **Semantics** | Meaning | "bank" = river edge OR financial institution |
| **Pragmatics** | Intent in context | "Oh great" after spilling coffee = sarcasm |

### Three Approaches to NLP

| Approach | How It Works | Pros | Cons | Best For |
|----------|-------------|------|------|----------|
| **Rule-Based** | Hand-written linguistic rules | Transparent, no data needed | Brittle, expensive to maintain | Controlled domains |
| **Statistical / ML** | Learns patterns from labelled data | Flexible, data-driven | Needs labelled examples | Classification, NER |
| **Deep Learning** | Neural networks learn representations automatically | State-of-the-art accuracy | Needs lots of data, slow to train | Translation, QA, generation |

---

## 2. Lexical Processing

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **Tokenisation** | Splitting text into individual words or sentences | "Chopping a sentence into pieces" |
| **Word Tokenisation** | Splitting text into individual words | `"Hello world"` → `["Hello", "world"]` |
| **Sentence Tokenisation** | Splitting a paragraph into individual sentences | Handles "Dr. Smith went..." correctly |
| **Text Normalisation** | Making text consistent — lowercase, remove punctuation, expand contractions | "Tidying up before analysis" |
| **Case Folding** | Converting all text to lowercase | `"Apple"` → `"apple"` |
| **Contraction Expansion** | Expanding shortened forms to full words | `"don't"` → `"do not"` |
| **Stopwords** | Common words carrying little meaning (the, and, is, at) | "Background noise words" |
| **Morpheme** | The smallest meaningful unit of a word | `"un"` + `"happy"` + `"ness"` |
| **Prefix** | A morpheme attached to the front of a word | `"un-"` in "unhappy", `"re-"` in "redo" |
| **Suffix** | A morpheme attached to the end of a word | `"-ness"` in "happiness", `"-ing"` in "running" |
| **Stemming** | Chopping word endings using rules to get a root form | `running` → `run`, `easily` → `easili` |
| **Lemmatisation** | Converting a word to its dictionary form using vocabulary + grammar | `better` → `good`, `was` → `be` |
| **Lemma** | The dictionary/base form of a word | `ran` → lemma is `run` |
| **Porter Stemmer** | The most widely used stemming algorithm (5 phases of rules) | "The classic chopper" |
| **Lancaster Stemmer** | More aggressive stemmer than Porter — shorter stems, more errors | "The heavy chopper" |
| **Snowball Stemmer** | Improved Porter stemmer, supports multiple languages | "The multilingual chopper" |
| **Spell Correction** | Fixing typos using edit distance and word frequency | "Autocorrect, but for NLP" |
| **Edit Distance (Levenshtein)** | Minimum single-character edits (insert, delete, substitute) to change one word to another | `kitten` → `sitting` = 3 edits |
| **Type** | A unique word in the vocabulary | "dog" is one type regardless of how often it appears |
| **Token** | Each individual occurrence of a word in text | "dog dog dog" = 3 tokens, 1 type |

### Edit Distance — Worked Example

`kitten` → `sitting` (3 edits):
```
kitten
→ sitten   (substitute k → s)      edit 1
→ sittin   (substitute e → i)      edit 2
→ sitting  (insert g at end)       edit 3
```

### Common Tokenisation Pitfalls

| Text | Naive Split | Correct Handling |
|------|------------|------------------|
| `"Dr. Smith"` | `["Dr.", "Smith"]` — fine | Sentence tokeniser must not split here |
| `"don't"` | `["don't"]` or `["don", "'t"]` | Depends on task |
| `"$4.5 million"` | `["$4.5", "million"]` | Keep as one token for NER |
| `"New York"` | `["New", "York"]` | May need to be one token |
| `"2023-06-14"` | `["2023", "-", "06", "-", "14"]` | Keep as date entity |

### Stemming vs Lemmatisation

| | Stemming | Lemmatisation |
|--|----------|---------------|
| **Speed** | Fast | Slower |
| **Output** | May not be real words (`easili`) | Always real words (`good`) |
| **Needs context?** | No | Yes (needs POS tag) |
| **Algorithm** | Rule-based suffix chopping | Dictionary lookup + grammar rules |
| **Example** | `studies` → `studi` | `studies` → `study` |
| **Use when** | Search engines, speed matters | Production NLP, meaning matters |

### Stopword Caution

> ⚠️ Do **not** remove stopwords blindly. "not good" → removing "not" → "good" completely flips the sentiment. Always check if your task needs stopwords.

| Task | Remove Stopwords? |
|------|------------------|
| Document classification | Yes — stopwords add noise |
| Sentiment analysis | Be careful — negations matter |
| Machine translation | No — every word matters |
| Information retrieval | Usually yes |

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
| **Adjective Phrase (ADJP)** | A chunk centred on an adjective — "very happy" | Description |
| **Adverb Phrase (ADVP)** | A chunk centred on an adverb — "quite quickly" | Manner |
| **Context-Free Grammar (CFG)** | A set of rules defining valid sentence structures using non-terminals and terminals | "A recipe book for valid sentences" |
| **Terminal** | An actual word in a CFG rule | `dog`, `runs`, `the` |
| **Non-terminal** | A label representing a phrase category in a CFG | `NP`, `VP`, `S` |
| **Production Rule** | One rule in a CFG, e.g. `S → NP VP` | "A sentence = noun phrase + verb phrase" |
| **Constituency Parsing** | Building a hierarchical tree showing phrases within phrases | "A tree of noun/verb boxes" |
| **Dependency Parsing** | Showing direct word-to-word relationships (who does what to whom) | "Drawing arrows between words" |
| **Parse Tree** | A visual tree structure representing grammatical relationships | "The family tree of a sentence" |
| **Head** | The main word of a phrase that determines its grammatical category | `fox` is the head of "the quick brown fox" |
| **Root (dependency)** | The main verb — the word all others depend on | "The boss of the sentence" |
| **nsubj** | Nominal subject — who performs the action | `fox` in "the fox jumps" |
| **dobj** | Direct object — what receives the action | `ball` in "kicked the ball" |
| **amod** | Adjectival modifier — adjective modifying a noun | `quick` in "the quick fox" |
| **prep** | Prepositional modifier | `in` in "sat in the park" |
| **det** | Determiner | `the` in "the dog" |
| **Grammatical Agreement** | Words matching each other in number, person, or gender | "The dog *runs*" not "The dog *run*" |
| **Subject-Verb Agreement** | Singular subjects take singular verbs; plural subjects take plural verbs | "He *runs* / They *run*" |
| **Structural Ambiguity** | When a sentence has more than one valid parse tree | "I saw the man with the telescope" = 2 meanings |
| **Attachment Ambiguity** | Uncertainty about which phrase a modifier attaches to | "She ate the salad with a fork" — fork modifies ate OR salad? |

### CFG Example

```
S  → NP VP              A sentence = noun phrase + verb phrase
NP → DT JJ* NN          Noun phrase = determiner + adjectives + noun
VP → VB NP              Verb phrase = verb + noun phrase
DT → "the" | "a"
NN → "cat" | "dog" | "fish"
VB → "chased" | "ate"
JJ → "quick" | "lazy"
```

### Dependency Labels — Full Reference

| Label | Meaning | Example |
|-------|---------|--------|
| `ROOT` | Main verb | "runs" in "The dog runs" |
| `nsubj` | Nominal subject | "dog" in "The dog runs" |
| `dobj` | Direct object | "ball" in "kicks the ball" |
| `iobj` | Indirect object | "him" in "gave him the ball" |
| `amod` | Adjectival modifier | "quick" in "quick fox" |
| `advmod` | Adverbial modifier | "quickly" in "ran quickly" |
| `det` | Determiner | "the" in "the dog" |
| `prep` | Prepositional modifier | "in" in "sat in the park" |
| `pobj` | Object of preposition | "park" in "in the park" |
| `compound` | Compound noun | "New" in "New York" |
| `aux` | Auxiliary verb | "was" in "was running" |

### Common POS Tags (Penn Treebank)

| Tag | Meaning | Example |
|-----|---------|---------|
| `NN` | Noun, singular | dog, city |
| `NNS` | Noun, plural | dogs, cities |
| `NNP` | Proper noun, singular | London, Apple |
| `NNPS` | Proper noun, plural | Vikings, Alps |
| `VB` | Verb, base form | eat, run |
| `VBD` | Verb, past tense | ate, ran |
| `VBG` | Verb, gerund / present participle | eating, running |
| `VBN` | Verb, past participle | eaten, run |
| `VBP` | Verb, non-3rd person singular present | eat (I eat) |
| `VBZ` | Verb, 3rd person singular present | eats, runs |
| `JJ` | Adjective | quick, happy |
| `JJR` | Adjective, comparative | quicker, happier |
| `JJS` | Adjective, superlative | quickest, happiest |
| `RB` | Adverb | quickly, very |
| `RBR` | Adverb, comparative | faster |
| `DT` | Determiner | the, a, an, this |
| `IN` | Preposition or subordinating conjunction | in, on, at, because |
| `PRP` | Personal pronoun | I, he, she, they |
| `PRP$` | Possessive pronoun | my, his, her, their |
| `CC` | Coordinating conjunction | and, but, or |
| `CD` | Cardinal number | one, 2, three |
| `MD` | Modal | can, will, should |

---

## 4. Semantic Processing

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **Semantics** | The study of meaning in language | "What it actually means" |
| **Lexical Semantics** | The meaning of individual words and how they relate | "The dictionary layer of meaning" |
| **Polysemy** | One word with multiple related meanings | `bank` = financial OR river edge |
| **Homonymy** | Two completely unrelated words that happen to be spelled/pronounced the same | `bat` (animal) vs `bat` (cricket bat) |
| **Synonym** | Words with the same (or very similar) meaning | happy = joyful = glad |
| **Antonym** | Words with opposite meanings | hot ↔ cold, fast ↔ slow |
| **Hyponym** | A more specific type of a broader category | Labrador is a hyponym of Dog |
| **Hypernym** | The broader category that contains more specific words | Animal is a hypernym of Dog |
| **Meronym** | A part of something | wheel is a meronym of car |
| **Holonym** | The whole that contains a part | car is a holonym of wheel |
| **WordNet** | A large English lexical database grouping words into synsets by meaning | "The official word relationship map" |
| **Synset** | A group of synonymous words sharing the same meaning in WordNet | `{happy.a.01: happy, glad, cheerful}` |
| **Sense** | One specific meaning of a polysemous word | `bank.n.01` = financial institution |
| **Word Sense Disambiguation (WSD)** | Automatically determining which meaning of a polysemous word is intended in context | "Picking the right definition" |
| **Lesk Algorithm** | WSD method: pick the sense whose WordNet definition overlaps most with the surrounding words | "Match your surroundings to the dictionary" |
| **Distributional Hypothesis** | Words that appear in similar contexts tend to have similar meanings | "You know a word by its neighbours" |
| **Distributional Semantics** | Representing word meaning using patterns of word co-occurrence in large corpora | "Learn meaning from statistics" |
| **Co-occurrence Matrix** | A table counting how often each word appears within a window of each other word | "Who hangs out with whom" |
| **Context Window** | The number of surrounding words considered when building co-occurrence statistics | Window=2 means 2 words left + 2 words right |
| **PMI (Pointwise Mutual Information)** | Measures whether two words appear together more than expected by chance | `PMI > 0` = genuinely associated |
| **PPMI** | PMI with negative values clipped to zero — more reliable with small data | "PMI, but only the positives" |
| **Semantic Role Labelling (SRL)** | Identifying who did what to whom, with what, where, and when | "Answering the journalist's 5 Ws" |
| **Agent** | The entity performing an action | "The *chef* sliced the tomatoes" |
| **Patient / Theme** | The entity receiving or affected by an action | "The chef sliced *the tomatoes*" |
| **Instrument** | What was used to perform an action | "Sliced *with a knife*" |
| **Location** | Where the action happened | "in the kitchen" |
| **Manner** | How the action was done | "carefully" |
| **Beneficiary** | Who benefited from the action | "for the guests" |
| **Named Entity Recognition (NER)** | Identifying and classifying real-world named things in text | "Spotting the proper nouns" |
| **IOB Tagging** | Labelling scheme for NER: B- begins entity, I- inside entity, O = not an entity | "B starts, I continues, O is out" |
| **Conditional Random Field (CRF)** | A sequence model that considers the full label sequence, not word-by-word | "Makes tag decisions as a team, not alone" |
| **Coreference Resolution** | Linking all mentions of the same entity across a text | "'She' = 'Marie Curie'" |
| **Mention** | Any reference to an entity — a name, pronoun, or description | "Marie Curie", "she", "the scientist" |
| **Coreference Cluster** | All mentions that refer to the same real-world entity | `{Marie Curie, she, her, the scientist}` |
| **Antecedent** | The first, introducing mention of an entity | "Marie Curie" before "she" |
| **Anaphor** | A later reference that points back to an antecedent | "she", "her", "the scientist" |

### PMI Formula

```
PMI(word_A, word_B) = log₂( P(A, B) / (P(A) × P(B)) )

P(A, B) = how often A and B appear together / total word pairs
P(A)    = how often A appears / total words
P(B)    = how often B appears / total words

PMI > 0  → A and B co-occur more than chance (associated)
PMI = 0  → exactly as expected by chance
PMI < 0  → A and B avoid each other (PPMI clips these to 0)
```

### IOB Tagging — Worked Example

```
Sentence: "Tim Cook announced Apple profits in Cupertino"

Tim        → B-PERSON   (begins a PERSON entity)
Cook       → I-PERSON   (continues the same PERSON entity)
announced  → O          (not an entity)
Apple      → B-ORG      (begins an ORG entity)
profits    → O
in         → O
Cupertino  → B-GPE      (begins a GPE entity — city)
```

### Semantic Roles — Full Sentence Example

```
"The chef carefully sliced the tomatoes with a sharp knife in the kitchen."

Agent:      the chef         (who did it)
Action:     sliced           (the event)
Patient:    the tomatoes     (what was acted on)
Manner:     carefully        (how)
Instrument: a sharp knife    (what tool)
Location:   in the kitchen   (where)
```

### NER Entity Types (spaCy / OntoNotes)

| Label | Meaning | Example |
|-------|---------|---------|
| `PERSON` | People's names | Tim Cook, Marie Curie |
| `ORG` | Organisations, companies, agencies | Apple, WHO, Oxford University |
| `GPE` | Countries, cities, states | London, India, California |
| `LOC` | Non-political locations | the Sahara, Mount Everest |
| `DATE` | Dates and time periods | 14 June 2026, last Tuesday |
| `TIME` | Times of day | 3pm, midnight |
| `MONEY` | Monetary values | $4.5 billion, £500 |
| `PERCENT` | Percentages | 45%, a third |
| `PRODUCT` | Named products | iPhone 15, Tesla Model S |
| `EVENT` | Named events | the World Cup, World War II |
| `WORK_OF_ART` | Titles of books, films, songs | Harry Potter, The Beatles |
| `LANGUAGE` | Named languages | English, Mandarin |

### Common NER Mistakes to Watch For

| Mistake | Example | Why It Happens |
|---------|---------|----------------|
| Split entity | `[Tim] [Cook]` instead of `[Tim Cook]` | Without IOB, multi-word names break apart |
| Wrong type | "Apple" tagged as `PRODUCT` not `ORG` | Ambiguous — same word, different context |
| Missing entity | "the company" not tagged | Pronoun/description coreference not resolved |
| Over-tagging | Common nouns tagged as entities | Model over-generalises from training data |

---

## 5. Text Representation

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **Bag-of-Words (BoW)** | Represent a document as word counts, ignoring order | "A bag of word counts" |
| **Vocabulary** | The complete set of unique words across all documents | "The master word list" |
| **Document Vector** | A list of numbers representing a document (one number per vocabulary word) | "A document's fingerprint" |
| **Sparse Vector** | A vector where most values are zero — typical of BoW with large vocabularies | "Mostly empty" |
| **Dense Vector** | A vector where most values are non-zero — typical of embeddings | "Fully packed with information" |
| **TF-IDF** | Weights words by how often they appear in a doc × how rare they are across all docs | "Rare here and common nowhere = important" |
| **TF (Term Frequency)** | How often a word appears in this specific document | `count / total_words_in_doc` |
| **IDF (Inverse Document Frequency)** | How rare a word is across all documents | `log(total_docs / docs_containing_word)` |
| **Word Embedding** | A dense vector representing a word's meaning, where similar words are close in space | "Words as locations in meaning-space" |
| **Embedding Dimension** | The size of the vector — typically 50, 100, 200, or 300 | "How many numbers describe each word" |
| **Word2Vec** | Google's algorithm that trains embeddings by predicting words from context | "Learn meaning from neighbours" |
| **CBOW** | Word2Vec variant: predict the centre word from surrounding context words | "Fill in the blank" |
| **Skip-gram** | Word2Vec variant: predict surrounding words from the centre word | "Guess the neighbours" |
| **GloVe** | Stanford's embedding method based on factorising the co-occurrence matrix | "Embeddings from counting" |
| **Cosine Similarity** | Measures the angle between two vectors — 1.0 = same direction, 0 = unrelated, -1 = opposite | "How closely two vectors point the same way" |
| **Dot Product** | Multiplying two vectors element-wise and summing — related to cosine similarity | "Raw closeness before normalising" |
| **Topic Modelling** | Unsupervised discovery of hidden themes in a document collection | "Finding the chapters nobody wrote" |
| **NMF (Non-negative Matrix Factorisation)** | Decomposes TF-IDF matrix into two smaller non-negative matrices: docs×topics and topics×words | "Split the big table into topic tables" |
| **LDA (Latent Dirichlet Allocation)** | Probabilistic topic model — each document is a mix of topics, each topic is a mix of words | "The Bayesian topic finder" |
| **Topic** | A probability distribution over words that tend to co-occur | `football topic = {goal: 0.3, match: 0.2, player: 0.15...}` |
| **Coherence Score** | Metric measuring how semantically related the top words in a topic are | "Do the topic words actually make sense together?" |

### TF-IDF Formula

```
TF-IDF(word, doc) = TF × IDF

TF  = (occurrences of word in doc) / (total words in doc)
IDF = log(total documents / documents containing word)

Example: word = "superb", appears in 2 of 100 documents, 3 times in doc A (50 words)
  TF  = 3 / 50 = 0.06
  IDF = log(100 / 2) = log(50) ≈ 3.91
  TF-IDF = 0.06 × 3.91 ≈ 0.235

Key insight: if word appears in ALL docs → IDF = log(1) = 0 → TF-IDF = 0
```

### Word Embedding Vector Arithmetic

```
king  - man  + woman  ≈  queen      (gender relationship)
Paris - France + Italy ≈  Rome       (capital city relationship)
doctor - man  + woman  ≈  nurse      (role + gender)

These relationships emerge from training on billions of sentences.
```

### CBOW vs Skip-gram

| | CBOW | Skip-gram |
|--|------|----------|
| **Predicts** | Centre word from context | Context words from centre |
| **Speed** | Faster | Slower |
| **Better for** | Frequent words | Rare words |
| **Training data** | Needs less | Needs more |

### BoW vs TF-IDF vs Embeddings

| | BoW | TF-IDF | Embeddings |
|--|-----|--------|-----------|
| **Word order** | Ignored | Ignored | Ignored (basic) |
| **Word relationships** | None | None | Captured |
| **"cat" ≈ "kitten"?** | No | No | Yes |
| **Common words** | Dominate | Downweighted | Not a problem |
| **Vector type** | Sparse | Sparse | Dense |
| **Vector size** | = vocabulary size | = vocabulary size | Fixed (e.g. 300) |
| **Speed** | Fast | Fast | Slower |
| **Best for** | Simple classification | Search/retrieval | Semantic tasks |

---

## 6. Classical Text Generation

| Term | Definition | Remember It As |
|------|-----------|----------------|
| **Language Model** | A model that assigns probability to a sequence of words | "How likely is this sentence?" |
| **N-gram** | A sequence of N consecutive words | Bigram = 2 words, Trigram = 3 words |
| **Unigram** | Single word, no context | `P(cat)` |
| **Bigram** | Two consecutive words | `P(cat | the)` |
| **Trigram** | Three consecutive words | `P(cat | the, fluffy)` |
| **Chain Rule** | The probability of a sentence = product of conditional word probabilities | `P(I love cats) = P(I) × P(love|I) × P(cats|I,love)` |
| **Markov Property** | The next word depends only on the recent past, not the full history | "Only look back a few steps" |
| **Markov Chain** | A system where next state depends only on current state — the heart of N-gram models | "Statistical word flow" |
| **Sparsity Problem** | Most possible word combinations never appear in training data → zero probability | "Can't predict what you've never seen" |
| **Zero Probability** | When an unseen N-gram causes the entire sentence probability to collapse to 0 | "One unknown word = the whole sentence fails" |
| **Laplace Smoothing** | Add 1 to every N-gram count so nothing has zero probability | "Pretend you saw everything at least once" |
| **Backoff Smoothing** | If the trigram is unseen, try the bigram; if unseen, try the unigram | "Fall back to simpler when stuck" |
| **Interpolation Smoothing** | Mix trigram, bigram, and unigram probabilities with learnable weights | "Blend all levels together" |
| **Perplexity** | How surprised the model is by new text — lower is better | "Average equally likely choices per word" |
| **Log Probability** | Log of probability — avoids numerical underflow when multiplying many small numbers | "Add instead of multiply" |
| **Greedy Decoding** | Always pick the single most probable next word | Fast but gets stuck in loops |
| **Beam Search** | Keep the top K candidate sequences alive; pick the globally best at the end | "Explore K paths, keep the winner" |
| **Beam Width** | The K in beam search — how many candidates to track | Larger K = better quality, slower speed |
| **Temperature Sampling** | Divide log probs by T before sampling: T<1 = conservative, T>1 = creative | "The creativity dial" |
| **Extractive Summarisation** | Select and return the most important existing sentences from the original | "Highlight the key sentences" |
| **Abstractive Summarisation** | Generate new sentences that capture the meaning — may use new vocabulary | "Rewrite in your own words" |
| **TextRank** | Graph-based summarisation: sentences are nodes, similarity = edge weight, PageRank picks top sentences | "The most central sentences win" |
| **BLEU Score** | Evaluates machine translation by measuring N-gram overlap with human reference translations | "How many phrases did we get right?" |
| **Rule-Based MT (RBMT)** | Translate using hand-written parse → transfer → generate pipeline | "Grammar rules as a bridge" |
| **Statistical MT (SMT)** | Learn translations from parallel corpora; argmax of translation model × language model | "Learn from millions of translated docs" |
| **Translation Model** | In SMT: P(source | target) — which source phrases map to which target phrases | "The bilingual dictionary" |
| **Language Model (in MT)** | In SMT: P(target) — ensures the output is fluent in the target language | "The fluency checker" |
| **Phrase Table** | In SMT: a lookup of multi-word translation units | `"New York" → "Nueva York"` |
| **Parallel Corpus** | The same document in two languages — used to train SMT | "The bilingual training bible" |

### Perplexity Formula

```
Perplexity = 2^(- average log₂ probability per word)

Or equivalently:
Perplexity = (1 / P(test text)) ^ (1/N)

N = number of words in test text

Intuition:
  Perplexity 10  → model considers ~10 equally likely options per word  (good)
  Perplexity 100 → model considers ~100 options per word  (mediocre)
  Perplexity 1   → perfect prediction (impossible in practice)
```

### N-gram Probability Formula

```
Bigram:   P(word | prev)         = C(prev, word) / C(prev)
Trigram:  P(word | prev2, prev1) = C(prev2, prev1, word) / C(prev2, prev1)

C(x) = count of x in training corpus

With Laplace smoothing:
P(word | prev) = (C(prev, word) + 1) / (C(prev) + |V|)
|V| = vocabulary size
```

### Decoding Strategies Compared

| Strategy | How | Quality | Speed | Use Case |
|----------|-----|---------|-------|----------|
| **Greedy** | Always pick top-1 word | Low (loops) | Fastest | Never recommended |
| **Beam Search** | Keep top K sequences | High | Medium | Translation, summarisation |
| **Random Sampling** | Sample from distribution | Variable | Fast | Creative generation |
| **Temperature (T<1)** | Sharpen distribution | More focused | Fast | Safe generation |
| **Temperature (T>1)** | Flatten distribution | More diverse | Fast | Creative, brainstorming |

---

## 7. Quick Concept Comparisons

### When to Use What — Text Representation

| If you need... | Use | Why |
|----------------|-----|-----|
| A fast baseline classifier | Bag-of-Words | Simple, fast, interpretable |
| Document search or ranking | TF-IDF | Rewards distinctive words |
| Semantic similarity between sentences | Word Embeddings | "excellent" ≈ "superb" |
| Discover hidden themes with no labels | Topic Modelling (NMF/LDA) | Fully unsupervised |
| Production text classification | TF-IDF + Logistic Regression | Fast, strong baseline |
| Deep semantic understanding | Pre-trained embeddings (GloVe/Word2Vec) | Captures word relationships |

### When to Use What — Text Preprocessing

| If you need... | Use | Watch Out For |
|----------------|-----|---------------|
| Speed, search engines | Stemming | Output may not be real words |
| Accurate word forms, production systems | Lemmatisation | Slower, needs POS tags |
| Remove common uninformative words | Stopword removal | Don't use for sentiment ("not good") |
| Normalise text | Lowercasing + punctuation removal | Loses capitalisation signals |

### Parsing: Constituency vs Dependency

| | Constituency | Dependency |
|--|-------------|------------|
| **Shows** | Phrase structure (NP, VP, PP) | Word-to-word grammatical relations |
| **Output** | Hierarchical tree | Directed arc graph |
| **Root** | S (sentence) | Main verb |
| **Best for** | Grammar checking, language teaching | Information extraction, SRL, QA |
| **Python library** | `nltk.RegexpParser`, `nltk.ChartParser` | `spacy` |

### Smoothing Quick Reference

| Method | Formula Change | Pros | Cons |
|--------|---------------|------|------|
| **Laplace** | Add 1 to all counts; add \|V\| to denominator | Simple, always works | Over-smooths — gives too much to unseen |
| **Backoff** | Use trigram if seen, else bigram, else unigram | Efficient | Discontinuous probabilities |
| **Interpolation** | λ₁×P_tri + λ₂×P_bi + λ₃×P_uni | Smooth, best performance | Needs λ tuning on held-out data |

### WSD Methods Compared

| Method | How | Needs | Accuracy |
|--------|-----|-------|----------|
| **Lesk Algorithm** | Dictionary definition overlap with context | WordNet | Low–Medium |
| **Supervised ML** | Trained on sense-labelled examples | Labelled data | High |
| **Most-frequent sense** | Always pick the most common sense | Frequency data | Surprisingly good baseline |
| **Neural (transformers)** | Context-aware representations (BERT) | Large corpus | Best |

---

## 8. NLP Pipeline at a Glance

```
Raw Text
  ↓ Text Normalisation      (lowercase, remove punctuation, expand contractions)
  ↓ Tokenisation            (split into words and sentences)
  ↓ Stopword Removal        (filter common words — task dependent!)
  ↓ Stemming/Lemmatisation  (reduce to root/dictionary form)
  ↓ POS Tagging             (label each word: noun, verb, adjective...)
  ↓ Parsing                 (understand sentence structure — syntactic)
  ↓ Semantic Analysis       (NER, SRL, WSD, coreference — meaning layer)
  ↓ Text Representation     (convert to numbers: BoW / TF-IDF / Embeddings)
  ↓ Modelling               (classify, generate, summarise, translate)
  ↓ Output
```

### Which Steps Are Optional?

| Step | Always needed? | Skip when... |
|------|---------------|--------------|
| Normalisation | Usually yes | Raw text already clean |
| Stopword removal | Task-dependent | Sentiment analysis, translation |
| Stemming/Lemmatisation | Often yes | Using character-level models |
| POS Tagging | For syntax tasks | BoW classification tasks |
| Parsing | For structure tasks | Simple text classification |
| NER/SRL | For semantic tasks | Topic modelling, sentiment |

### Full Worked Example Through the Pipeline

```
Input: "She's running quickly in New York."

Normalise: "she is running quickly in new york"
Tokenise:  ["she", "is", "running", "quickly", "in", "new", "york", "."]
Stopwords: ["running", "quickly", "new", "york"]  ← removed: she, is, in
Lemmatise: ["run", "quickly", "new", "york"]
POS tags:  run/VB, quickly/RB, new/JJ, york/NNP
NER:       [New York] → GPE
BoW vec:   {run: 1, quickly: 1, new: 1, york: 1}
TF-IDF:    {run: 0.3, quickly: 0.4, york: 0.6}  ← "york" more distinctive
```

---

## 9. Python Libraries — Quick Reference

| Library | Install | Best For | Key Classes / Functions |
|---------|---------|----------|--------------------------|
| **NLTK** | `pip install nltk` | Learning, research, WordNet | `word_tokenize`, `pos_tag`, `ne_chunk`, `PorterStemmer`, `WordNetLemmatizer` |
| **spaCy** | `pip install spacy` | Production NLP, speed | `nlp(text)`, `doc.ents`, `token.dep_`, `token.pos_`, `doc.noun_chunks` |
| **scikit-learn** | `pip install scikit-learn` | ML, vectorisation, classifiers | `CountVectorizer`, `TfidfVectorizer`, `NMF`, `Pipeline`, `LogisticRegression` |
| **gensim** | `pip install gensim` | Embeddings, topic models | `Word2Vec`, `LdaModel`, `corpora.Dictionary`, `api.load()` |
| **TextBlob** | `pip install textblob` | Quick prototyping, sentiment | `TextBlob(text)`, `.sentiment`, `.correct()`, `.tags` |
| **sklearn-crfsuite** | `pip install sklearn-crfsuite` | Sequence labelling (NER) | `CRF`, `.fit()`, `.predict()` |
| **sumy** | `pip install sumy` | Extractive summarisation | `TextRankSummarizer`, `LexRankSummarizer` |

### spaCy Pipeline Components

| Component | What It Adds | Access Via |
|-----------|-------------|------------|
| `tok2vec` | Token vectors (shared representations) | Internal |
| `tagger` | POS tags | `token.tag_`, `token.pos_` |
| `parser` | Dependency parse | `token.dep_`, `token.head` |
| `ner` | Named entities | `doc.ents`, `token.ent_type_` |
| `lemmatizer` | Lemmas | `token.lemma_` |

### NLTK Key Data Downloads

```python
import nltk
nltk.download('punkt')                        # Tokeniser
nltk.download('averaged_perceptron_tagger')   # POS tagger
nltk.download('wordnet')                      # WordNet database
nltk.download('stopwords')                    # Stopword lists
nltk.download('maxent_ne_chunker')            # NER chunker
nltk.download('words')                        # English word list
```

---

## 10. Twenty Things to Remember

**Lexical Processing**
1. **Tokenisation is the foundation** — everything else builds on splitting text into tokens.
2. **Stemming is fast but crude; lemmatisation is slow but correct** — choose based on your task.
3. **Do not remove stopwords blindly** — "not good" loses its meaning without "not".
4. **Edit distance measures how different two words are** — `kitten` → `sitting` = 3 edits.
5. **Lemmatisation needs the POS tag to be accurate** — `better` as adjective → `good`; as verb → `better`.

**Syntactic Processing**
6. **POS tags describe grammatical function, not meaning** — "bank" is NN whether it means a riverbank or a financial institution.
7. **Constituency parsing shows phrase hierarchy; dependency parsing shows word relationships** — both useful, for different tasks.
8. **The ROOT of a dependency parse is always the main verb** — everything hangs off it.
9. **Structural ambiguity is everywhere** — "I saw the man with the telescope" has 2 valid parse trees.
10. **Chunking (shallow parsing) is fast but does not give full sentence structure** — good enough for many tasks.

**Semantic Processing**
11. **Polysemy is the norm, not the exception** — most common English words have multiple senses.
12. **IOB tagging**: B = begins entity, I = continues entity, O = not an entity — never I without a preceding B.
13. **CRFs beat word-by-word classifiers** because they enforce valid label sequences (e.g. `I-PERSON` after `B-PERSON`).
14. **Coreference resolution links pronouns to their antecedents** — without it, "she" and "Marie Curie" are separate entities.
15. **PMI > 0 means two words appear together more than chance** — they are genuinely associated.

**Text Representation and Generation**
16. **A word appearing in every document has TF-IDF score of zero** — `log(N/N) = 0`.
17. **Word embeddings encode meaning as geometry** — `king - man + woman ≈ queen`.
18. **Perplexity: lower is better** — it measures how surprised the model is per word.
19. **Beam search with K=1 is identical to greedy decoding** — larger K = better quality but slower.
20. **Smoothing is essential for N-gram models** — a single unseen bigram collapses the entire sentence probability to zero without it.

---

## 11. Common Mistakes and How to Avoid Them

| Mistake | What Goes Wrong | Fix |
|---------|----------------|-----|
| Removing stopwords for sentiment | "not good" → "good" — flips meaning | Keep negations, check task first |
| Using stemming when accuracy matters | `"university"` → `"univers"` — breaks named entities | Use lemmatisation instead |
| Forgetting to pass POS to lemmatiser | `"better"` → `"better"` instead of `"good"` | Always tag POS first |
| Not downloading NLTK data | `LookupError` at runtime | Run `nltk.download()` in setup |
| Loading spaCy without a model | `OSError: [E050]` | Run `python -m spacy download en_core_web_sm` |
| Using raw counts in BoW | Common words dominate | Use TF-IDF or remove stopwords |
| Ignoring sparsity in N-gram models | Zero probability for unseen sequences | Always apply smoothing |
| Choosing too many/few topics in NMF | Topics are too broad or too granular | Try several values, inspect top words manually |
| Using BLEU alone to evaluate translation | BLEU does not measure fluency or meaning | Supplement with human evaluation |
| Treating IOB `I-` as standalone | `I-PERSON` without `B-PERSON` is invalid | Always start an entity with `B-` |
