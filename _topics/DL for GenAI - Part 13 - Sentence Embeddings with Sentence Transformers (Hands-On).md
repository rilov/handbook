---
layout: topic
title: "Deep Learning for Generative AI — Part 13: Sentence Embeddings with Sentence Transformers (Hands-On)"
category: Generative AI
order: 113
permalink: /topics/dl-genai-sentence-transformers/
tags:
  - generative-ai
  - deep-learning
  - transformer
  - sentence-transformers
  - embeddings
  - semantic-search
  - clustering
  - similarity
  - hands-on
  - beginners
  - friendly
summary: "A hands-on walkthrough of Sentence Transformers: turn whole sentences into fixed-length vectors with all-mpnet-base-v2, then reuse the same embeddings for semantic search, document-to-document similarity, and k-means clustering — with no extra training."
---

# Deep Learning for Generative AI — Part 13: Sentence Embeddings with Sentence Transformers (Hands-On)

[Part 12]({{ site.baseurl }}/topics/dl-genai-bert-sequence-classification/) reused a pre-trained BERT for classification. This part reuses a pre-trained model for something even more versatile: turning **whole sentences and documents into fixed-length vectors**.

Once text lives in vector space, three very different tasks become the *same* operation — measuring distance:

<div class="mermaid">
flowchart LR
    D["📄 Documents"] --> M["🤖 Sentence Transformer<br/>(all-mpnet-base-v2)"]
    M --> V["📍 One vector<br/>per document"]

    V --> S["🔍 Semantic search"]
    V --> C["🔗 Document similarity"]
    V --> K["🧩 Clustering"]

    style D fill:#fef3c7,stroke:#d97706
    style M fill:#dbeafe,stroke:#2563eb
    style V fill:#d1fae5,stroke:#059669
</div>

The key insight of this whole part: **we compute the embeddings once and reuse them for all three tasks. No model training happens anywhere.**

---

## 1. From word vectors to sentence vectors

[Part 1]({{ site.baseurl }}/topics/dl-genai-word-embeddings/) gave every **word** a vector. But most real questions are about **sentences and documents**:

- "Find the support ticket most similar to this one"
- "Which FAQ answers this customer's question?"
- "Group these 10,000 reviews by topic"

**Why not just average the word vectors?** Because averaging destroys meaning:

```text
"The movie was not good, it was terrible"
"The movie was not terrible, it was good"
```

Same words, opposite meanings — identical average. A sentence embedding model reads the whole sentence *in context* (using the bidirectional encoder from [Part 11]({{ site.baseurl }}/topics/dl-genai-transformer-variants/)) and produces **one vector that captures the sentence's meaning**.

### The model: all-mpnet-base-v2

We'll use [`all-mpnet-base-v2`](https://huggingface.co/sentence-transformers/all-mpnet-base-v2), the workhorse of the Sentence Transformers library:

| Property | Value | Meaning |
|---|---|---|
| Encoder | MPNet (a BERT-style Transformer) | The bidirectional "reader" from Part 11 |
| Output | 768 numbers per text | Fixed length, no matter how long the input |
| Training | Bi-encoder setup on 1+ billion sentence pairs | Trained so *similar sentences get nearby vectors* |
| Max input | 384 word pieces | Longer texts are truncated |

**What's a bi-encoder?** During training, pairs of related sentences (a question and its answer, a title and its article) were pushed **close together** in vector space, while unrelated pairs were pushed apart. That's the special sauce: raw BERT understands language, but a bi-encoder is *specifically tuned so that distance = semantic relatedness*.

**Analogy:** think of the embedding space as a giant library where the librarian shelves books by *meaning*, not alphabet. Books about pasta sit together; books about rockets sit in another aisle — even if one is titled "Fettuccine Forever" and the other "Noodles of Italy".

```bash
pip install sentence-transformers scikit-learn
```

---

## 2. Encode a small document collection

Nine short documents across three hidden topics — cooking, space, and football:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

documents = [
    "How to cook perfect pasta al dente",              # 0 cooking
    "A beginner's guide to baking sourdough bread",    # 1 cooking
    "Ten quick dinner recipes for busy weeknights",    # 2 cooking
    "NASA announces new mission to explore Europa",    # 3 space
    "The James Webb telescope captures distant galaxies", # 4 space
    "How rockets escape Earth's gravity",              # 5 space
    "Liverpool wins the Champions League final",       # 6 football
    "Transfer rumours: star striker heading to Madrid",# 7 football
    "Tactical analysis of the 4-3-3 formation",        # 8 football
]

embeddings = model.encode(documents)
print(embeddings.shape)
```

```text
(9, 768)
```

That's it. Nine documents, nine vectors, 768 numbers each. Short title or long paragraph — always 768 numbers, which is what makes everything downstream simple.

Each document is now **a point in a shared embedding space** where distance reflects semantic relatedness:

<div class="mermaid">
flowchart TB
    subgraph space["The embedding space (conceptually)"]
        subgraph c1["🍝 cooking corner"]
            P["pasta"] ~~~ B["sourdough"] ~~~ R["recipes"]
        end
        subgraph c2["🚀 space corner"]
            N["Europa"] ~~~ W["Webb"] ~~~ RK["rockets"]
        end
        subgraph c3["⚽ football corner"]
            L["Liverpool"] ~~~ T["transfers"] ~~~ F["4-3-3"]
        end
    end

    style c1 fill:#fef3c7,stroke:#d97706
    style c2 fill:#dbeafe,stroke:#2563eb
    style c3 fill:#dcfce7,stroke:#16a34a
</div>

---

## 3. Task 1: Semantic search

**Keyword search fails** when the words don't match: search "italian noodles" and a keyword engine finds nothing above — no document contains either word. Semantic search finds the pasta document anyway, because *meaning* matches.

The recipe:

1. Encode the query **with the same model** (critical — vectors from different models live in different spaces and can't be compared)
2. Compute similarity between the query vector and every document vector
3. Rank and return the top hits

```python
from sentence_transformers import util

query = "italian noodles"
query_embedding = model.encode(query)

scores = util.cos_sim(query_embedding, embeddings)[0]

for idx in scores.argsort(descending=True)[:3]:
    print(f"{scores[idx]:.3f}  {documents[idx]}")
```

```text
0.532  How to cook perfect pasta al dente
0.341  Ten quick dinner recipes for busy weeknights
0.286  A beginner's guide to baking sourdough bread
```

Not a single shared word with the query — pure meaning matching. Two more queries to build intuition:

```text
Query: "how do spaceships leave the planet"
0.647  How rockets escape Earth's gravity          ← "spaceships/leave/planet" ≈ "rockets/escape/Earth"
0.402  NASA announces new mission to explore Europa
0.311  The James Webb telescope captures distant galaxies

Query: "which team won the cup"
0.578  Liverpool wins the Champions League final   ← "team/won/cup" ≈ "Liverpool/wins/final"
0.334  Transfer rumours: star striker heading to Madrid
0.269  Tactical analysis of the 4-3-3 formation
```

**About the scores:** cosine similarity ranges from -1 to 1. In practice with this model, ~0.6+ is a strong match, ~0.3–0.5 is topically related, and below ~0.2 is mostly unrelated. The *ranking* matters more than the absolute numbers.

**Real-world uses:** FAQ bots ("customers phrase questions 100 different ways"), searching internal wikis, e-commerce search ("warm jacket for hiking" → finds "insulated trekking parka"), and the retrieval step of RAG — this is exactly what the vector store does in [RAG Basics]({{ site.baseurl }}/topics/langchain-rag-basics/).

---

## 4. Task 2: Document-to-document similarity

No query this time — we compare **every document against every other document** by building the full similarity matrix:

```python
sim_matrix = util.cos_sim(embeddings, embeddings)
print(sim_matrix.shape)   # (9, 9)
```

Conceptually (values rounded, 1.00 diagonal = each doc vs itself):

```text
            pasta  bread  recipes europa  webb  rocket  lpool  trans  tactic
pasta       1.00   0.45   0.51    0.05   0.03   0.08    0.02   0.04   0.06
bread       0.45   1.00   0.42    0.04   0.02   0.05    0.01   0.03   0.02
recipes     0.51   0.42   1.00    0.03   0.02   0.04    0.05   0.06   0.04
europa      0.05   0.04   0.03    1.00   0.48   0.44    0.03   0.05   0.02
webb        0.03   0.02   0.02    0.48   1.00   0.39    0.02   0.03   0.01
rocket      0.08   0.05   0.04    0.44   0.39   1.00    0.04   0.02   0.03
lpool       0.02   0.01   0.05    0.03   0.02   0.04    1.00   0.47   0.41
trans       0.04   0.03   0.06    0.05   0.03   0.02    0.47   1.00   0.36
tactic      0.06   0.02   0.04    0.02   0.01   0.03    0.41   0.36   1.00
```

Three bright blocks along the diagonal — the three topics — with near-zero everywhere else. The model discovered the topic structure without being told it exists.

To find the closest match for one selected document (say index 3, the Europa mission):

```python
doc_idx = 3
scores = sim_matrix[doc_idx].clone()
scores[doc_idx] = -1                      # exclude the document itself

best = scores.argmax()
print(f"Most similar to: {documents[doc_idx]}")
print(f"  → {documents[best]}  ({scores[best]:.3f})")
```

```text
Most similar to: NASA announces new mission to explore Europa
  → The James Webb telescope captures distant galaxies  (0.478)
```

**Real-world uses:** "related articles" widgets on news sites, detecting duplicate support tickets or bug reports, plagiarism and near-duplicate detection, "customers who viewed this also viewed" for content.

---

## 5. Task 3: Unsupervised clustering with k-means

We never labelled the documents — but the labels are already *implicit in the geometry*. Feed the embedding vectors straight into k-means (the algorithm itself is explained in [K-Means Clustering]({% link _topics/K-Means Clustering.md %})):

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_ids = kmeans.fit_predict(embeddings)

for cluster in range(3):
    print(f"\nCluster {cluster}:")
    for doc, cid in zip(documents, cluster_ids):
        if cid == cluster:
            print(f"  - {doc}")
```

```text
Cluster 0:
  - NASA announces new mission to explore Europa
  - The James Webb telescope captures distant galaxies
  - How rockets escape Earth's gravity

Cluster 1:
  - How to cook perfect pasta al dente
  - A beginner's guide to baking sourdough bread
  - Ten quick dinner recipes for busy weeknights

Cluster 2:
  - Liverpool wins the Champions League final
  - Transfer rumours: star striker heading to Madrid
  - Tactical analysis of the 4-3-3 formation
```

A perfect 3-way split into space, cooking, and football — with **zero labels and zero training**. K-means simply grouped points that sit near each other, and the embedding model had already placed same-topic documents nearby.

**Two practical notes:**

- **Choosing k:** here we knew there were 3 topics. In real projects you don't — use the elbow method or silhouette score (covered in the K-Means guide), or try a few values and inspect the clusters.
- **Inspect, always:** print a few documents per cluster like we did above. Clusters are only useful if a human can name them ("ah, this cluster is billing complaints").

**Real-world uses:** grouping thousands of open-ended survey answers into themes, organising support tickets before routing rules exist, discovering trending discussion topics, deduplicating a scraped dataset.

---

## 6. The big picture: one set of vectors, three tasks

Notice what we did **not** do in this entire part: we never trained anything. The workflow was:

<div class="mermaid">
flowchart LR
    A["Encode once<br/>model.encode(docs)"] --> B["Reuse everywhere"]
    B --> S["Search:<br/>query vs docs"]
    B --> C["Similarity:<br/>docs vs docs"]
    B --> K["Clustering:<br/>k-means on vectors"]

    style A fill:#dbeafe,stroke:#2563eb
    style B fill:#d1fae5,stroke:#059669
</div>

| Task | Operation on the vectors | Needs labels? | Needs training? |
|---|---|---|---|
| Semantic search | query vector vs all doc vectors, rank | ❌ | ❌ |
| Document similarity | all doc vectors vs each other (matrix) | ❌ | ❌ |
| Clustering | k-means on the doc vectors | ❌ | ❌ |

Compare with Part 12: BERT classification needed labelled examples and a fine-tuning loop. Sentence embeddings need **neither** — the bi-encoder pre-training already did the hard work of making distance meaningful.

---

## 7. Common pitfalls

| Pitfall | What goes wrong | Fix |
|---|---|---|
| Mixing models | Query encoded with model A, documents with model B — similarities are garbage | Always encode query and documents with the **same** model |
| Very long documents | Anything past ~384 word pieces is silently truncated | Split long documents into chunks and embed each chunk |
| Trusting absolute scores | "0.5 must mean 50% similar" — it doesn't | Use scores for *ranking*; calibrate thresholds on your own data |
| Wrong model for the job | `all-mpnet-base-v2` is English-focused | For other languages use a multilingual model like `paraphrase-multilingual-mpnet-base-v2` |
| Recomputing embeddings | Encoding the whole corpus on every query | Encode once, store the vectors (in production: a vector database) |

---

## 8. Summary

- A **Sentence Transformer** maps whole sentences/documents to **fixed-length vectors** (768 numbers for `all-mpnet-base-v2`), where **distance = semantic relatedness** thanks to bi-encoder training on a billion sentence pairs.
- **Semantic search:** encode the query with the same model, rank documents by cosine similarity — matches by meaning, not keywords.
- **Document similarity:** a full similarity matrix compares every pair of documents directly, no query needed.
- **Clustering:** k-means on the raw embedding vectors groups documents by topic with zero labels.
- The same embeddings are **computed once and reused** for all three tasks — no model training happens at any point.
- These are exactly the embeddings that power the vector store in [RAG]({{ site.baseurl }}/topics/langchain-rag-basics/) — this part is the "how does retrieval actually work" behind it.

**Next up:** see the whole Transformer again in one sitting, with zero math, in [The Transformer - A Friendly Guide]({{ site.baseurl }}/topics/transformer-friendly-guide/) — including how training works and what the "context limit" means inside each layer.
