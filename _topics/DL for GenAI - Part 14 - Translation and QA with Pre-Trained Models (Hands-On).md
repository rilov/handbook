---
layout: topic
title: "Deep Learning for Generative AI — Part 14: Translation and Question Answering with Pre-Trained Models (Hands-On)"
category: Generative AI
order: 114
permalink: /topics/dl-genai-translation-qa-pretrained/
tags:
  - generative-ai
  - deep-learning
  - transformer
  - seq2seq
  - translation
  - question-answering
  - hugging-face
  - t5
  - marianmt
  - hands-on
  - beginners
  - friendly
summary: "Use pre-trained encoder-decoder Transformers for two transformation tasks: machine translation with MarianMT and question answering with T5, without training from scratch."
---

# Deep Learning for Generative AI — Part 14: Translation and Question Answering with Pre-Trained Models (Hands-On)

[Part 11]({{ site.baseurl }}/topics/dl-genai-transformer-variants/) introduced three Transformer families. [Part 12]({{ site.baseurl }}/topics/dl-genai-bert-sequence-classification/) showed how to put an encoder-only model to work by fine-tuning BERT. Now we will put the full **encoder-decoder** family to work — without any training at all.

Two classic transformation tasks are perfect for this architecture:

1. **Machine translation:** one language → another language.
2. **Question answering (extractive/generative):** a question + a passage → an answer.

We will use Hugging Face pre-trained models. The models already know a lot about language; we just load them and feed them text.

---

## 1. Why pre-trained encoder-decoder models?

Training a Transformer from scratch needs huge datasets and serious compute. Most practical work today reuses a pre-trained model:

```text
Pre-training  (weeks, huge parallel text)  →  the model already knows language
Using it      (seconds, your sentence)    →  it translates or answers immediately
```

You can fine-tune later if you have a specialised domain, but for many tasks the pre-trained version is already good enough.

---

## 2. What you need

```bash
pip install transformers torch sentencepiece
```

- `transformers` — the model and tokenizer zoo.
- `torch` — runs the computations.
- `sentencepiece` — many seq2seq tokenizers need it under the hood.

---

## 3. Task A: machine translation with MarianMT

MarianMT models are specialised: each checkpoint handles one language pair. They are encoder-decoder Transformers trained on parallel text.

Here we translate English → Spanish.

```python
from transformers import MarianTokenizer, MarianMTModel

model_name = "Helsinki-NLP/opus-mt-en-es"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
```

```python
text = "The library is quiet today, and the coffee is excellent."

inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
translated_ids = model.generate(**inputs, max_new_tokens=40)
translation = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

print(translation)
```

```text
La biblioteca está tranquila hoy, y el café es excelente.
```

What just happened?

1. The tokenizer split the English sentence into subword tokens and added special markers.
2. The **encoder** read the whole English sentence.
3. The **decoder** generated Spanish tokens one at a time, using cross-attention to look back at the English encoder outputs.
4. `skip_special_tokens=True` strips the padding and end-of-sequence markers so we get readable text.

### A reusable translation function

```python
def translate_en_to_es(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=40)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

for sentence in [
    "Where is the nearest train station?",
    "She finished the report before lunch.",
]:
    print(f"EN: {sentence}")
    print(f"ES: {translate_en_to_es(sentence)}\n")
```

MarianMT models are fast and small because they are task-specific: one model, one language pair.

---

## 4. Task B: question answering with T5

T5 is an encoder-decoder model trained with a text-to-text objective: every task is rewritten as "input text → output text". For question answering, the input is a formatted string that combines the question and a context passage.

```python
from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
```

```python
context = (
    "Marie Curie was a Polish-born physicist and chemist. "
    "She won the Nobel Prize in Physics in 1903 for her work on radioactivity, "
    "and the Nobel Prize in Chemistry in 1911 for the discovery of radium and polonium."
)
question = "Which two elements did Marie Curie discover?"

input_text = f"question: {question} context: {context}"

inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
answer_ids = model.generate(**inputs, max_new_tokens=30)
answer = tokenizer.decode(answer_ids[0], skip_special_tokens=True)

print(answer)
```

```text
radium and polonium
```

Notice the format:

```text
question: Which two elements did Marie Curie discover? context: Marie Curie was...
```

T5 was trained with this style of prefix, so the model recognises that it should answer the question using the context. The encoder reads the combined text bidirectionally; the decoder writes the answer one token at a time.

### A reusable QA function

```python
def answer_question(question, context):
    prompt = f"question: {question} context: {context}"
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=30)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

context = (
    "The Pacific Ocean is the largest ocean on Earth, covering more than "
    "one-third of its surface. The Mariana Trench, the deepest part of the world, "
    "lies in the western Pacific."
)
print(answer_question("Where is the Mariana Trench?", context))
```

```text
western Pacific
```

---

## 5. MarianMT vs T5: specialised vs multi-task

| | MarianMT | T5 |
|---|---|---|
| Architecture | Encoder-decoder Transformer | Encoder-decoder Transformer |
| Specialisation | One language pair per model | Many tasks with one model |
| How you ask it | Plain sentence in source language | Prefixed task string, e.g. `question: ... context: ...` |
| Strength | Fast, high-quality translation | Flexible: translation, summarisation, QA, classification |
| When to pick it | You know the language pair up front | You want one model to do several text-to-text tasks |

Both use the same underlying idea from Parts 6–8: an encoder builds a rich representation of the input, a decoder generates the output word by word, and cross-attention lets the decoder focus on the right parts of the input.

---

## 6. Practical details to watch

### Tokenizer and model must match

Always load the tokenizer from the same checkpoint as the model. The tokenizer owns the vocabulary; the model expects exactly those token IDs.

```python
# Good: same checkpoint
tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")
model     = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-es")
```

### Use `torch.no_grad()` in production

During inference you are not training, so you do not need gradients. Wrapping generation in `torch.no_grad()` saves memory and speeds things up:

```python
import torch

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=40)
```

### Control generation with a few knobs

- `max_new_tokens` — how many new tokens the decoder may produce.
- `num_beams` — beam search; larger values usually give better but slower outputs.
- `early_stopping` — stop once the model emits the end-of-sequence token.

### Truncation matters

Long inputs are silently cut off at `max_length` or `max_position_embeddings`. For QA, if your document is longer than the model can read, split it into chunks and run the model on each chunk.

---

## 7. Summary

| Step | Translation | Question Answering |
|---|---|---|
| Load tokenizer | `MarianTokenizer` | `T5Tokenizer` |
| Load model | `MarianMTModel` | `T5ForConditionalGeneration` |
| Prepare input | Plain source sentence | `question: ... context: ...` |
| Generate | `model.generate(**inputs)` | `model.generate(**inputs)` |
| Decode | `tokenizer.decode(..., skip_special_tokens=True)` | `tokenizer.decode(..., skip_special_tokens=True)` |

- **MarianMT** is a specialist: one checkpoint per language pair, excellent at that one job.
- **T5** is a generalist: the same architecture handles many tasks once you phrase them as text-to-text.
- Both reuse the encoder-decoder machinery from Parts 6–8: read the input, then write the output one token at a time with cross-attention to the input.

**Next up:** the Generative AI track continues with generative models beyond Transformers — starting with the difference between prediction, transformation, and true generation in [Part 15: Introduction to Multimodal Generative Architectures]({{ site.baseurl }}/topics/dl-genai-multimodal-generative-intro/).