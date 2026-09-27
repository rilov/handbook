---
layout: topic
title: "Deep Learning for Generative AI — Part 12: Sequence Classification with BERT (Hands-On)"
category: Generative AI
order: 112
permalink: /topics/dl-genai-bert-sequence-classification/
tags:
  - generative-ai
  - deep-learning
  - transformer
  - bert
  - hugging-face
  - fine-tuning
  - sentiment-analysis
  - sequence-classification
  - hands-on
  - beginners
  - friendly
summary: "A hands-on walkthrough of sentiment classification with BERT: load a pre-trained model from Hugging Face, tokenize text properly, fine-tune on a few labelled sentences with a plain PyTorch loop, and interpret the outputs."
---

# Deep Learning for Generative AI — Part 12: Sequence Classification with BERT (Hands-On)

[Part 11]({{ site.baseurl }}/topics/dl-genai-transformer-variants/) introduced BERT as the encoder-only "reader": bidirectional attention, rich contextual embeddings, brilliant at understanding — unable to generate.

In this part we put the reader to work. We'll take a **pre-trained** BERT model, teach it **sentiment classification** with just a few labelled sentences, and run it on text it has never seen. All in plain Python you can paste into any notebook.

---

## 1. Why reuse a pre-trained model?

BERT is one of the most influential models in modern NLP — and one reason is that you almost never train it from scratch. Google already did that, on billions of words, using masked language modelling ([how that works]({% link _topics/Self-Supervised Learning - A Friendly Guide.md %})).

Instead, we **fine-tune**: take the pre-trained model, which already understands English deeply, and adapt it to a *downstream task* — here, sentiment classification.

**Analogy:** you don't teach a literature professor the English language before asking them to sort book reviews into "liked it" and "hated it". You give them ten examples of each and they get the idea immediately. Fine-tuning is exactly that: a tiny bit of task-specific training on top of a mountain of general knowledge.

```text
Pre-training  (Google, weeks, billions of words)  →  understands language
Fine-tuning   (you, minutes, a few examples)      →  understands YOUR task
```

---

## 2. Why Hugging Face?

[Hugging Face](https://huggingface.co/) is the standard place to get pre-trained NLP models. We use it because:

- **Thousands of pre-trained models**, one line to download
- **Easy, consistent APIs** — the same code works for BERT, RoBERTa, DistilBERT...
- **Production-ready tools** — tokenizers, training utilities, model hosting

Install the two packages we need (`transformers` for the model and tokenizer, `torch` for running it):

```bash
pip install transformers torch
```

---

## 3. Load pre-trained BERT with a classification head

The `transformers` package gives us BERT **with a classification head already attached** — a small linear layer sitting on top of the encoder that maps BERT's understanding to our labels:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "bert-base-uncased"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2,          # 0 = negative, 1 = positive
)
```

Two things happen here:

1. The **encoder stack** (12 layers, 110M parameters) downloads with all its pre-trained weights — the mountain of language knowledge.
2. A fresh **classification head** is bolted on top with **random weights**. You'll even see a warning saying some weights were "newly initialized" and that you should train the model on a downstream task — that's expected, and it's exactly what we're about to do.

```text
[CLS] token's rich vector  →  classification head  →  2 scores (neg, pos)
```

BERT reads the whole sentence bidirectionally, and the special `[CLS]` token's final vector acts as a summary of the entire sequence — the classification head reads just that.

---

## 4. Tokenize the text properly

BERT can't take raw strings. Its tokenizer does three jobs:

1. **Split words into WordPiece tokens** — common words stay whole, rare words split into pieces ("unbelievable" → `un`, `##believ`, `##able`), so no word is ever "unknown"
2. **Add special tokens** — `[CLS]` at the start (the summary slot) and `[SEP]` at the end
3. **Build the attention mask** — 1 for real tokens, 0 for padding, so attention ignores the padding

```python
inputs = tokenizer(
    "I absolutely loved this movie!",
    return_tensors="pt",     # PyTorch tensors
    padding=True,
    truncation=True,
)

print(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]))
```

```text
['[CLS]', 'i', 'absolutely', 'loved', 'this', 'movie', '!', '[SEP]']
```

The tokenizer and the model **must come from the same checkpoint** — the token IDs are the vocabulary the model was pre-trained with. That's why we load both with the same `model_name`.

---

## 5. Fine-tune on a few labelled sentences

Real projects use thousands of examples, but the mechanics are identical with six — and six is enough to watch it work. A plain PyTorch training loop:

```python
import torch

texts = [
    "I absolutely loved this movie!",          # positive
    "What a fantastic experience.",            # positive
    "Best purchase I have made all year.",     # positive
    "This was a complete waste of time.",      # negative
    "Terrible acting and a boring plot.",      # negative
    "I want my money back.",                   # negative
]
labels = torch.tensor([1, 1, 1, 0, 0, 0])

batch = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

model.train()
for epoch in range(5):
    optimizer.zero_grad()
    outputs = model(**batch, labels=labels)
    outputs.loss.backward()      # cross-entropy loss, computed for us
    optimizer.step()
    print(f"epoch {epoch + 1}: loss = {outputs.loss.item():.4f}")
```

```text
epoch 1: loss = 0.7123
epoch 2: loss = 0.5241
epoch 3: loss = 0.3187
epoch 4: loss = 0.1904
epoch 5: loss = 0.0982
```

Notes on what just happened:

- Passing `labels=` makes the model compute the **cross-entropy loss** for us — the same "wanted vs got" measure from [the friendly guide]({{ site.baseurl }}/topics/transformer-friendly-guide/)
- The tiny learning rate (`2e-5`) is deliberate: we want to *gently nudge* the pre-trained weights, not bulldoze the language knowledge
- The loss falling epoch after epoch is the classification head (and, gently, the encoder) learning what "positive" and "negative" look like

---

## 6. Run inference and interpret the outputs

Now feed the model sentences it has never seen:

```python
model.eval()

new_texts = [
    "An unforgettable, brilliant film.",
    "I fell asleep halfway through.",
]

batch = tokenizer(new_texts, return_tensors="pt", padding=True, truncation=True)

with torch.no_grad():
    logits = model(**batch).logits

probs = torch.softmax(logits, dim=-1)
preds = probs.argmax(dim=-1)

for text, p, pred in zip(new_texts, probs, preds):
    label = "positive" if pred == 1 else "negative"
    print(f"{label:8s} ({p[pred]:.0%})  {text}")
```

```text
positive (97%)  An unforgettable, brilliant film.
negative (94%)  I fell asleep halfway through.
```

Reading the output chain:

```text
logits    raw scores, one per label          [-2.1,  1.4]
softmax   turn scores into probabilities     [0.03,  0.97]
argmax    pick the biggest                   1  →  "positive"
```

That's the same **linear + softmax** confidence vote from [Part 8]({{ site.baseurl }}/topics/dl-genai-transformer-architecture/) — just voting over 2 labels instead of a whole vocabulary.

---

## 7. Summary

| Step | Tool | One-line job |
|---|---|---|
| Load model | `AutoModelForSequenceClassification` | Pre-trained encoder + fresh classification head |
| Load tokenizer | `AutoTokenizer` | Same checkpoint as the model, always |
| Tokenize | `tokenizer(...)` | WordPiece + `[CLS]`/`[SEP]` + attention mask |
| Fine-tune | plain PyTorch loop, `lr=2e-5` | Gently adapt to the downstream task |
| Predict | `logits → softmax → argmax` | Scores → probabilities → label |

- **Don't train from scratch** — fine-tune a pre-trained model and inherit billions of words of language understanding for free.
- BERT is the **encoder-only reader** from Part 11 put to work: bidirectional understanding in, one classification out.
- The whole downstream task lives in a **small classification head** reading the `[CLS]` summary vector.
- With more data, the loop scales unchanged — or switch to Hugging Face's `Trainer` API, which wraps the same steps with batching, evaluation, and checkpointing.

**Next up:** classification needed labels — but the same pre-trained encoders can power search, similarity, and clustering with *no* labels and *no* training at all. See [Part 13: Sentence Embeddings with Sentence Transformers]({{ site.baseurl }}/topics/dl-genai-sentence-transformers/).
