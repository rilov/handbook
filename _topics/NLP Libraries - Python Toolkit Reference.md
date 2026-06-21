---
title: "NLP Libraries - Python Toolkit Reference"
category: Natural Language Processing
order: 12
tags:
  - nlp
  - python
  - nltk
  - spacy
  - gensim
  - scikit-learn
  - libraries
  - reference
  - beginners
summary: A complete reference guide to every Python library used across the NLP tutorial series. Learn what each library does, how to install it, and which functions to use for each NLP task—with ready-to-run code examples.
---

# NLP Libraries — Python Toolkit Reference

Every code example in this series uses real Python libraries. This guide explains each one clearly — what it does, how to install it, and exactly which functions to use for which task.

---

## Quick Map: Library → Topic

| Task | Best Library | Alternative |
|------|-------------|-------------|
| Tokenisation | NLTK, spaCy | Python `split()` for basics |
| Stemming | NLTK | - |
| Lemmatisation | NLTK, spaCy | TextBlob |
| POS Tagging | spaCy, NLTK | TextBlob |
| Dependency Parsing | spaCy | StanfordNLP |
| Named Entity Recognition | spaCy | NLTK (basic) |
| Bag-of-Words / TF-IDF | scikit-learn | NLTK |
| Topic Modelling (NMF) | scikit-learn | gensim (LDA) |
| Word Embeddings | gensim | spaCy vectors |
| CRF (NER sequence model) | sklearn-crfsuite | - |
| Translation quality (BLEU) | NLTK | sacrebleu |
| Summarisation | sumy, gensim | - |

---

## Library 1: NLTK

### What Is It?

**NLTK (Natural Language Toolkit)** is the oldest and most widely taught Python NLP library. It was built for education and research, so it comes with built-in datasets, corpora, and every classical NLP algorithm. It is not the fastest, but it is the most comprehensive for learning.

### Install

```bash
pip install nltk
```

After installing, download the data packages you need:

```python
import nltk

# Download everything (safe for beginners — ~3.5GB)
nltk.download('all')

# Or download only what you need (recommended):
nltk.download('punkt')           # sentence and word tokeniser
nltk.download('punkt_tab')       # updated punkt data
nltk.download('averaged_perceptron_tagger')  # POS tagger
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')         # WordNet lexical database
nltk.download('omw-1.4')         # Open Multilingual Wordnet
nltk.download('stopwords')       # list of stopwords
nltk.download('maxent_ne_chunker')  # named entity chunker
nltk.download('words')           # English word list
```

---

### NLTK: Tokenisation

```python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

text = "Dr. Smith went to London. He attended the NLP conference on 14 June."

# Word tokenisation
words = word_tokenize(text)
print(words)
# ['Dr.', 'Smith', 'went', 'to', 'London', '.', 'He', 'attended',
#  'the', 'NLP', 'conference', 'on', '14', 'June', '.']

# Sentence tokenisation
sentences = sent_tokenize(text)
print(sentences)
# ['Dr. Smith went to London.', 'He attended the NLP conference on 14 June.']
# Note: correctly keeps "Dr. Smith" in one sentence
```

**Used in:** Lexical Processing guide

---

### NLTK: Stopwords

```python
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))
print(f"Total stopwords: {len(stop_words)}")
# Total stopwords: 179

text = "This is a simple example showing how to remove stopwords from text"
words = word_tokenize(text.lower())

filtered = [w for w in words if w not in stop_words and w.isalpha()]
print(filtered)
# ['simple', 'example', 'showing', 'remove', 'stopwords', 'text']
```

**Used in:** Lexical Processing guide

---

### NLTK: Stemming

```python
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer

porter = PorterStemmer()
lancaster = LancasterStemmer()
snowball = SnowballStemmer('english')

words = ['running', 'runs', 'easily', 'happiness', 'studies', 'beautiful']

print(f"{'Word':<15} {'Porter':<15} {'Lancaster':<15} {'Snowball'}")
print("-" * 55)
for word in words:
    print(f"{word:<15} {porter.stem(word):<15} {lancaster.stem(word):<15} {snowball.stem(word)}")
```

**Output:**
```
Word            Porter          Lancaster       Snowball
-------------------------------------------------------
running         run             run             run
runs            run             run             run
easily          easili          easy            easili
happiness       happi           happy           happi
studies         studi           study           studi
beautiful       beauti          beaut           beauti
```

**Used in:** Lexical Processing guide

---

### NLTK: Lemmatisation

```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Default: assumes noun
print(lemmatizer.lemmatize("running"))    # running (wrong — no POS)
print(lemmatizer.lemmatize("running", pos='v'))  # run (correct)
print(lemmatizer.lemmatize("better", pos='a'))   # good
print(lemmatizer.lemmatize("was", pos='v'))       # be
print(lemmatizer.lemmatize("mice"))               # mouse
print(lemmatizer.lemmatize("wolves"))             # wolf

# Always pass the POS tag for best results
pos_map = {'N': 'n', 'V': 'v', 'J': 'a', 'R': 'r'}  # map Penn tags to WordNet

from nltk import pos_tag, word_tokenize

def lemmatize_sentence(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    result = []
    for word, tag in tagged:
        wn_pos = pos_map.get(tag[0], 'n')
        result.append(lemmatizer.lemmatize(word, pos=wn_pos))
    return result

print(lemmatize_sentence("The dogs were running and the cats were sleeping"))
# ['The', 'dog', 'be', 'run', 'and', 'the', 'cat', 'be', 'sleep']
```

**Used in:** Lexical Processing guide

---

### NLTK: POS Tagging

```python
import nltk
from nltk import pos_tag, word_tokenize

text = "The quick brown fox jumps over the lazy dog"
tokens = word_tokenize(text)
tagged = pos_tag(tokens)

print(tagged)
# [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'),
#  ('jumps', 'VBZ'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN')]

# Look up what a tag means
print(nltk.help.upenn_tagset('JJ'))   # Adjective
print(nltk.help.upenn_tagset('VBZ'))  # Verb, 3rd person singular present
```

**Used in:** Syntactic Processing Part 1 guide

---

### NLTK: Chunking (Shallow Parsing)

```python
import nltk
from nltk import pos_tag, word_tokenize, RegexpParser

text = "The quick brown fox jumps over the lazy dog"
tokens = word_tokenize(text)
tagged = pos_tag(tokens)

# Define a grammar for noun phrases
grammar = """
    NP: {<DT>?<JJ>*<NN>}   # Optional determiner, any adjectives, then a noun
    VP: {<VBZ><IN>}         # Verb followed by preposition
"""

parser = RegexpParser(grammar)
tree = parser.parse(tagged)

print(tree)
# (S
#   (NP The/DT quick/JJ brown/JJ fox/NN)
#   (VP jumps/VBZ over/IN)
#   (NP the/DT lazy/JJ dog/NN))

# Visualise (opens a window — comment out if running headless)
# tree.draw()

# Iterate over chunks
for subtree in tree.subtrees():
    if subtree.label() in ['NP', 'VP']:
        print(f"{subtree.label()}: {' '.join(w for w, t in subtree.leaves())}")
```

**Used in:** Syntactic Processing Part 1 guide

---

### NLTK: WordNet

```python
from nltk.corpus import wordnet as wn

# Look up synsets for a word
synsets = wn.synsets('bank')
print(f"'bank' has {len(synsets)} senses:")
for syn in synsets[:4]:
    print(f"  {syn.name()}: {syn.definition()}")

# Get synonyms, antonyms
syn = wn.synset('happy.a.01')
print(f"\nDefinition: {syn.definition()}")
print(f"Synonyms: {[l.name() for l in syn.lemmas()]}")
print(f"Antonyms: {[l.name() for l in syn.lemmas()[0].antonyms()]}")

# Hypernyms and hyponyms
dog = wn.synset('dog.n.01')
print(f"\nHypernyms of dog: {[h.name() for h in dog.hypernyms()]}")
print(f"Hyponyms of dog: {[h.name() for h in dog.hyponyms()[:5]]}")

# Word similarity
cat = wn.synset('cat.n.01')
print(f"\nSimilarity (dog, cat): {dog.path_similarity(cat):.3f}")
print(f"Similarity (dog, car): {dog.path_similarity(wn.synset('car.n.01')):.3f}")
```

**Used in:** Semantic Processing Part 1 guide

---

### NLTK: Named Entity Recognition

```python
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk

text = "Apple CEO Tim Cook announced record profits in Cupertino last Tuesday."

tokens = word_tokenize(text)
tagged = pos_tag(tokens)
tree = ne_chunk(tagged)

print(tree)
# (S
#   (ORGANIZATION Apple/NNP)
#   CEO/NNP
#   (PERSON Tim/NNP Cook/NNP)
#   announced/VBD
#   ...
#   (GPE Cupertino/NNP)
#   last/JJ
#   Tuesday/NNP .)

# Extract named entities
for chunk in tree:
    if hasattr(chunk, 'label'):
        entity = ' '.join(w for w, t in chunk.leaves())
        print(f"{chunk.label()}: {entity}")
```

**Used in:** Semantic Processing Part 2 guide

---

### NLTK: BLEU Score

```python
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu, SmoothingFunction

# Single sentence BLEU
reference = [["the", "cat", "is", "on", "the", "mat"]]  # list of reference lists
candidate = ["the", "cat", "is", "on", "the", "mat"]

smooth = SmoothingFunction().method1

score = sentence_bleu(reference, candidate, smoothing_function=smooth)
print(f"Perfect match BLEU: {score:.3f}")    # 1.000

candidate2 = ["the", "cat", "sat", "on", "the", "mat"]
score2 = sentence_bleu(reference, candidate2, smoothing_function=smooth)
print(f"One word off BLEU:  {score2:.3f}")   # ~0.800

# Corpus BLEU (multiple sentences)
references = [[["the", "cat", "is", "on", "the", "mat"]],
              [["the", "dog", "ran", "in", "the", "park"]]]
hypotheses = [["the", "cat", "is", "on", "the", "mat"],
              ["the", "dog", "ran", "in", "the", "park"]]

print(f"Corpus BLEU: {corpus_bleu(references, hypotheses):.3f}")  # 1.000
```

**Used in:** Classical Text Generation Part 2 guide

---

## Library 2: spaCy

### What Is It?

**spaCy** is the industry-standard NLP library for production use. It is fast (written in Cython), accurate, and handles the full NLP pipeline in one call. While NLTK is educational, spaCy is what you use in real applications.

### Install

```bash
pip install spacy

# Download a language model (choose one):
python -m spacy download en_core_web_sm   # small — fast, less accurate (~12MB)
python -m spacy download en_core_web_md   # medium — includes word vectors (~43MB)
python -m spacy download en_core_web_lg   # large — best accuracy (~741MB)
```

---

### spaCy: The Full Pipeline in One Call

```python
import spacy

nlp = spacy.load("en_core_web_sm")

text = "Apple CEO Tim Cook announced $94.8 billion in revenue in Cupertino on Tuesday."
doc = nlp(text)  # Runs the FULL pipeline: tokenise → POS → parse → NER

# Everything is available on the doc object
for token in doc:
    print(f"{token.text:<15} POS: {token.pos_:<8} DEP: {token.dep_:<10} HEAD: {token.head.text}")
```

**Output:**
```
Apple           POS: PROPN    DEP: nsubj      HEAD: announced
CEO             POS: PROPN    DEP: appos      HEAD: Apple
Tim             POS: PROPN    DEP: compound   HEAD: Cook
Cook            POS: PROPN    DEP: appos      HEAD: CEO
announced       POS: VERB     DEP: ROOT       HEAD: announced
...
```

**Used across:** Syntactic Processing, Semantic Processing guides

---

### spaCy: Tokenisation and Sentence Detection

```python
import spacy
nlp = spacy.load("en_core_web_sm")

text = "Dr. Smith went to London. He loves NLP."
doc = nlp(text)

# Tokens
print("Tokens:", [token.text for token in doc])

# Sentences
print("Sentences:")
for sent in doc.sents:
    print(f"  '{sent.text}'")

# Token properties
for token in doc[:5]:
    print(f"{token.text:<12} lemma={token.lemma_:<12} is_stop={token.is_stop} is_punct={token.is_punct}")
```

**Used in:** Lexical Processing guide

---

### spaCy: POS Tagging

```python
import spacy
nlp = spacy.load("en_core_web_sm")

doc = nlp("The quick brown fox jumps over the lazy dog")

print(f"{'Token':<12} {'POS':<10} {'Fine-grained Tag':<15} {'Explanation'}")
print("-" * 60)
for token in doc:
    print(f"{token.text:<12} {token.pos_:<10} {token.tag_:<15} {spacy.explain(token.tag_)}")
```

**Output:**
```
Token        POS        Fine-grained Tag  Explanation
------------------------------------------------------------
The          DET        DT               determiner
quick        ADJ        JJ               adjective
brown        ADJ        JJ               adjective
fox          NOUN       NN               noun, singular or mass
jumps        VERB       VBZ              verb, 3rd person singular present
...
```

**Used in:** Syntactic Processing Part 1 guide

---

### spaCy: Dependency Parsing

```python
import spacy
nlp = spacy.load("en_core_web_sm")

doc = nlp("The chef sliced the tomatoes with a sharp knife")

print(f"{'Token':<12} {'Dep':<10} {'Head':<12} {'Meaning'}")
print("-" * 55)
for token in doc:
    print(f"{token.text:<12} {token.dep_:<10} {token.head.text:<12} {spacy.explain(token.dep_)}")

# Navigate the tree
root = [t for t in doc if t.dep_ == 'ROOT'][0]
print(f"\nRoot verb: {root.text}")
print(f"Subject:   {[t.text for t in root.lefts if t.dep_ == 'nsubj']}")
print(f"Object:    {[t.text for t in root.rights if t.dep_ == 'dobj']}")
```

**Used in:** Syntactic Processing Part 2 guide, Semantic Processing Part 2 guide

---

### spaCy: Named Entity Recognition

```python
import spacy
nlp = spacy.load("en_core_web_sm")

text = "Apple CEO Tim Cook announced $94.8 billion in revenue in Cupertino on Tuesday."
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
Cupertino                 GPE          Countries, cities, states
Tuesday                   DATE         Absolute or relative dates or periods
```

**Used in:** Semantic Processing Part 2 guide

---

### spaCy: IOB Tags

```python
import spacy
nlp = spacy.load("en_core_web_sm")

doc = nlp("Sundar Pichai joined Google in 2004.")

print(f"{'Token':<12} {'IOB':<10} {'Entity Type'}")
print("-" * 35)
for token in doc:
    iob = token.ent_iob_
    etype = token.ent_type_ or "-"
    label = f"{iob}-{etype}" if iob != "O" else "O"
    print(f"{token.text:<12} {label:<10} {etype}")
```

**Used in:** Semantic Processing Part 2 guide

---

### spaCy: Noun Phrases and Lemmatisation

```python
import spacy
nlp = spacy.load("en_core_web_sm")

doc = nlp("The running dogs were chasing the flying birds")

# Noun phrases (chunking)
print("Noun phrases:")
for chunk in doc.noun_chunks:
    print(f"  '{chunk.text}' (root: {chunk.root.text})")

# Lemmas
print("\nToken → Lemma:")
for token in doc:
    if not token.is_punct:
        print(f"  {token.text:<15} → {token.lemma_}")
```

**Used in:** Lexical Processing, Syntactic Processing Part 1 guides

---

## Library 3: scikit-learn

### What Is It?

**scikit-learn** is Python's general-purpose machine learning library. In NLP it handles text vectorisation (BoW, TF-IDF), unsupervised methods (NMF topic modelling), and all classifiers (Naive Bayes, SVM, Logistic Regression).

### Install

```bash
pip install scikit-learn
```

---

### scikit-learn: Bag-of-Words

```python
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

documents = [
    "I love cats and dogs",
    "Dogs love to run in the park",
    "Cats and dogs are great pets"
]

vectorizer = CountVectorizer()
bow_matrix = vectorizer.fit_transform(documents)

df = pd.DataFrame(
    bow_matrix.toarray(),
    columns=vectorizer.get_feature_names_out(),
    index=[f"Doc{i+1}" for i in range(len(documents))]
)
print(df)

# Useful parameters
vectorizer_custom = CountVectorizer(
    lowercase=True,          # convert to lowercase (default True)
    stop_words='english',    # remove English stopwords
    max_features=100,        # keep only top 100 words by frequency
    ngram_range=(1, 2),      # include both unigrams and bigrams
    min_df=2,                # ignore words appearing in fewer than 2 documents
)
```

**Used in:** Text Representation guide

---

### scikit-learn: TF-IDF

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

documents = [
    "the film was great the acting was superb",
    "the film was boring and slow",
    "superb acting and great direction"
]

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(documents)

df = pd.DataFrame(
    tfidf_matrix.toarray().round(3),
    columns=vectorizer.get_feature_names_out(),
    index=["Doc A", "Doc B", "Doc C"]
)
print(df)

# Find most important words for each document
feature_names = vectorizer.get_feature_names_out()
for i, doc in enumerate(["Doc A", "Doc B", "Doc C"]):
    scores = tfidf_matrix[i].toarray()[0]
    top_indices = scores.argsort()[-3:][::-1]
    top_words = [(feature_names[j], round(scores[j], 3)) for j in top_indices]
    print(f"{doc} top words: {top_words}")
```

**Used in:** Text Representation guide

---

### scikit-learn: NMF Topic Modelling

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import numpy as np

documents = [
    "The football team won the championship match last night",
    "The election results show the winning party gained seats in parliament",
    "Doctors recommend the new vaccine for all adults at the hospital",
    "The player scored three goals in the final match of the season",
    "Government policy on healthcare spending was debated in parliament",
    "The hospital launched a new treatment programme for patients",
]

# Step 1: TF-IDF
vectorizer = TfidfVectorizer(max_features=30, stop_words='english')
tfidf = vectorizer.fit_transform(documents)
words = vectorizer.get_feature_names_out()

# Step 2: NMF — discover 3 topics
nmf = NMF(n_components=3, random_state=42, max_iter=500)
doc_topics = nmf.fit_transform(tfidf)

# Step 3: Print top words per topic
print("Discovered Topics:")
for i, topic in enumerate(nmf.components_):
    top_words = [words[j] for j in topic.argsort()[-6:][::-1]]
    print(f"  Topic {i+1}: {', '.join(top_words)}")

# Step 4: Document → dominant topic
print("\nDocument assignments:")
for i, doc in enumerate(documents):
    topic_num = np.argmax(doc_topics[i]) + 1
    print(f"  Topic {topic_num}: {doc[:50]}...")
```

**Used in:** Text Representation guide

---

### scikit-learn: Text Classification Pipeline

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Example: sentiment classification
texts = [
    "I love this product it is amazing",
    "Terrible quality, waste of money",
    "Great value, would buy again",
    "Awful experience, never again",
    "Fantastic! Exceeded all expectations",
    "Broken on arrival, very disappointed",
]
labels = [1, 0, 1, 0, 1, 0]  # 1=positive, 0=negative

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.33, random_state=42
)

# Pipeline: TF-IDF → Classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LogisticRegression()),
])

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
print(classification_report(y_test, predictions, target_names=['negative', 'positive']))
```

---

## Library 4: gensim

### What Is It?

**gensim** specialises in topic modelling and word embeddings. It is the go-to library for Word2Vec, Doc2Vec, LDA (an alternative to NMF for topics), and document similarity.

### Install

```bash
pip install gensim
```

---

### gensim: Word2Vec — Training Your Own

```python
from gensim.models import Word2Vec

# Each sentence is a list of words
sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "cat", "ate", "the", "fish"],
    ["the", "dog", "chased", "the", "cat"],
    ["dogs", "and", "cats", "are", "pets"],
    ["the", "dog", "fetched", "the", "ball"],
    ["fish", "swim", "in", "the", "river"],
]

model = Word2Vec(
    sentences,
    vector_size=50,    # size of each word vector
    window=2,          # context window (words either side)
    min_count=1,       # minimum frequency to include word
    sg=0,              # 0=CBOW, 1=Skip-gram
    epochs=100,        # training passes
    seed=42,
)

# Most similar words
print("Similar to 'cat':", model.wv.most_similar("cat", topn=3))

# Word vector
print("Vector for 'cat':", model.wv["cat"][:5], "...")  # first 5 dims

# Cosine similarity
print(f"Similarity (cat, dog): {model.wv.similarity('cat', 'dog'):.3f}")
print(f"Similarity (cat, fish): {model.wv.similarity('cat', 'fish'):.3f}")

# Save and reload
model.save("word2vec.model")
loaded = Word2Vec.load("word2vec.model")
```

**Used in:** Text Representation guide

---

### gensim: Pre-trained Embeddings

```python
import gensim.downloader as api

# List available pre-trained models
# api.info()['models'].keys()

# Download a smaller model (word2vec trained on text8 corpus — ~33MB)
model = api.load("word2vec-google-news-300")  # 300-dim, trained on 3B words

# Or smaller options:
# model = api.load("glove-wiki-gigaword-50")    # GloVe 50-dim, ~66MB
# model = api.load("glove-twitter-25")          # GloVe Twitter 25-dim, ~47MB

# Vector arithmetic
print("king - man + woman:")
result = model.most_similar(positive=["king", "woman"], negative=["man"], topn=3)
for word, score in result:
    print(f"  {word}: {score:.3f}")

# Analogy: Paris is to France as Rome is to?
result = model.most_similar(positive=["Rome", "France"], negative=["Paris"], topn=1)
print(f"\nRome:France :: Paris:? → {result[0][0]}")  # Italy
```

**Used in:** Text Representation guide

---

### gensim: LDA Topic Modelling

```python
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import preprocess_string

# Preprocessing
documents = [
    "The football team won the championship match",
    "Parliament debated the election results",
    "Hospital launched a new vaccine programme",
    "The player scored goals in the final match",
    "Government healthcare policy debated in parliament",
    "Doctors treat patients with new medicine at the hospital",
]

processed = [preprocess_string(doc) for doc in documents]

# Build dictionary and corpus
dictionary = corpora.Dictionary(processed)
corpus = [dictionary.doc2bow(doc) for doc in processed]

# Train LDA
lda = LdaModel(
    corpus,
    num_topics=3,
    id2word=dictionary,
    passes=20,
    random_state=42,
)

# Print topics
for topic_id, topic in lda.print_topics(num_words=5):
    print(f"Topic {topic_id}: {topic}")

# Assign topics to a new document
new_doc = preprocess_string("The goalkeeper saved the match")
bow = dictionary.doc2bow(new_doc)
print("\nTopic distribution:", lda[bow])
```

---

## Library 5: sklearn-crfsuite

### What Is It?

**sklearn-crfsuite** is a wrapper around CRFsuite that follows the scikit-learn API. It is the standard library for training Conditional Random Field models for sequence labelling tasks like NER.

### Install

```bash
pip install sklearn-crfsuite
```

---

### sklearn-crfsuite: CRF for NER

```python
import sklearn_crfsuite
from sklearn_crfsuite import metrics

def word_features(sentence, i):
    """Extract features for the word at position i"""
    word = sentence[i][0]
    postag = sentence[i][1]

    features = {
        'word.lower': word.lower(),
        'word.isupper': word.isupper(),
        'word.istitle': word.istitle(),
        'word.isdigit': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
        'word[-3:]': word[-3:],   # suffix
        'word[-2:]': word[-2:],
    }

    if i > 0:
        prev_word = sentence[i-1][0]
        features['prev_word.lower'] = prev_word.lower()
        features['prev_word.istitle'] = prev_word.istitle()
    else:
        features['BOS'] = True  # beginning of sentence

    if i < len(sentence) - 1:
        next_word = sentence[i+1][0]
        features['next_word.lower'] = next_word.lower()
        features['next_word.istitle'] = next_word.istitle()
    else:
        features['EOS'] = True  # end of sentence

    return features

def sent_to_features(sent):
    return [word_features(sent, i) for i in range(len(sent))]

def sent_to_labels(sent):
    return [label for _, _, label in sent]

# Training data format: [(word, pos_tag, iob_label), ...]
train_sents = [
    [("Tim", "NNP", "B-PERSON"), ("Cook", "NNP", "I-PERSON"),
     ("joined", "VBD", "O"), ("Apple", "NNP", "B-ORG"), (".", ".", "O")],
    [("London", "NNP", "B-GPE"), ("is", "VBZ", "O"),
     ("the", "DT", "O"), ("capital", "NN", "O"), (".", ".", "O")],
]

X_train = [sent_to_features(s) for s in train_sents]
y_train = [sent_to_labels(s) for s in train_sents]

# Train CRF
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,            # L1 regularisation
    c2=0.1,            # L2 regularisation
    max_iterations=100,
    all_possible_transitions=True,
)
crf.fit(X_train, y_train)

# Predict
X_test = [sent_to_features(train_sents[0])]
pred = crf.predict(X_test)
print("Predicted labels:", pred[0])
```

**Used in:** Semantic Processing Part 2 guide

---

## Library 6: TextBlob

### What Is It?

**TextBlob** is a beginner-friendly wrapper around NLTK and Pattern. It trades flexibility for simplicity — great for quick prototyping, spell correction, and basic sentiment analysis.

### Install

```bash
pip install textblob
python -m textblob.download_corpora
```

---

### TextBlob: Basic NLP Tasks

```python
from textblob import TextBlob

text = "The quick brown fox jumps over the lazy dog. Natural language processing is fascinating."
blob = TextBlob(text)

# Tokenisation
print("Words:", blob.words[:6])
print("Sentences:", list(blob.sentences))

# POS Tagging
print("POS Tags:", blob.tags[:6])

# Noun phrases
print("Noun phrases:", blob.noun_phrases)

# Lemmatisation (word by word)
from textblob import Word
for word in ["running", "better", "geese", "was"]:
    print(f"  {word} → {Word(word).lemmatize()}")
```

---

### TextBlob: Spell Correction

```python
from textblob import TextBlob

mistakes = [
    "I havv goood speling",
    "Natrual langauge procesing is intresting",
    "The qiuck brwon fox"
]

for text in mistakes:
    blob = TextBlob(text)
    print(f"Original:  {text}")
    print(f"Corrected: {blob.correct()}")
    print()
```

**Used in:** Lexical Processing guide

---

### TextBlob: Sentiment Analysis

```python
from textblob import TextBlob

reviews = [
    "This product is absolutely amazing! Best purchase ever.",
    "Terrible quality. Broke after one day. Very disappointed.",
    "It's okay, nothing special but does the job.",
    "Fantastic value for money, highly recommend!",
]

print(f"{'Review':<50} {'Polarity':<10} {'Sentiment'}")
print("-" * 75)
for review in reviews:
    blob = TextBlob(review)
    polarity = blob.sentiment.polarity  # -1 (negative) to +1 (positive)
    label = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
    print(f"{review[:48]:<50} {polarity:>+.2f}     {label}")
```

---

## Library 7: sumy

### What Is It?

**sumy** provides classical extractive summarisation algorithms including TextRank, LexRank, LSA, and Luhn — all with a clean, consistent interface.

### Install

```bash
pip install sumy
python -c "import nltk; nltk.download('punkt')"
```

---

### sumy: TextRank Summarisation

```python
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer

article = """
The Amazon rainforest is the world's largest tropical rainforest, covering over 
five and a half million square kilometres. It is home to an estimated 10% of all 
species on Earth, including jaguars, anacondas, and hundreds of bird species. 
The forest plays a critical role in regulating the global climate by absorbing 
enormous amounts of carbon dioxide. Deforestation is the biggest threat to the 
Amazon, with cattle ranching and agriculture responsible for most land clearance. 
In recent years, the rate of deforestation has accelerated, alarming scientists 
and conservationists worldwide. Protecting the Amazon is considered essential 
for meeting global climate targets and preserving biodiversity.
"""

parser = PlaintextParser.from_string(article, Tokenizer("english"))

print("=== TextRank (2 sentences) ===")
summarizer = TextRankSummarizer()
for sentence in summarizer(parser.document, 2):
    print(f"  {sentence}")

print("\n=== LexRank (2 sentences) ===")
summarizer = LexRankSummarizer()
for sentence in summarizer(parser.document, 2):
    print(f"  {sentence}")
```

**Used in:** Classical Text Generation Part 2 guide

---

## Installation Summary

Copy and run this block to install everything at once:

```bash
# Core libraries
pip install nltk spacy scikit-learn gensim textblob sumy sklearn-crfsuite

# spaCy language models
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md   # optional, includes word vectors

# TextBlob corpora
python -m textblob.download_corpora

# NLTK data packages
python -c "
import nltk
packages = [
    'punkt', 'punkt_tab',
    'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng',
    'wordnet', 'omw-1.4',
    'stopwords',
    'maxent_ne_chunker', 'words'
]
for p in packages:
    nltk.download(p)
print('All NLTK packages downloaded.')
"
```

---

## Which Library for Which Guide

| Guide | Libraries Used |
|-------|---------------|
| Lexical Processing | `nltk` (tokenise, stem, lemmatise, stopwords), `spacy` (lemma, tokens), `textblob` (spell correction) |
| Syntactic Processing Part 1 | `nltk` (POS tag, chunking, RegexpParser), `spacy` (POS, noun_chunks) |
| Syntactic Processing Part 2 | `nltk` (CFG, ChartParser), `spacy` (dependency parse) |
| Syntactic Processing Part 3 | `nltk` (parse trees, tree drawing), `spacy` |
| Semantic Processing Part 1 | `nltk` (WordNet, Lesk algorithm), `spacy`, `numpy` |
| Semantic Processing Part 2 | `spacy` (NER, IOB, dep parse), `sklearn-crfsuite` (CRF) |
| Text Representation | `scikit-learn` (CountVectorizer, TfidfVectorizer, NMF), `gensim` (Word2Vec) |
| Classical Text Gen Part 1 | Pure Python, `collections`, `math`, `random` |
| Classical Text Gen Part 2 | Pure Python (beam search, temperature), `sklearn` (TF-IDF summarisation), `sumy` (TextRank), `nltk` (BLEU) |
