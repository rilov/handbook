---
layout: topic
title: "Deep Learning for Generative AI — Part 11: Transformer Variants — Encoder-Only, Decoder-Only, Encoder-Decoder"
category: Generative AI
order: 111
permalink: /topics/dl-genai-transformer-variants/
tags:
  - generative-ai
  - deep-learning
  - transformer
  - bert
  - gpt
  - t5
  - encoder-only
  - decoder-only
  - beginners
  - friendly
summary: "Why the industry split the Transformer into three families — encoder-only (BERT) for understanding, decoder-only (GPT) for generating, and encoder-decoder (T5) for transforming — and how to pick the right one for a task."
---

# Deep Learning for Generative AI — Part 11: Transformer Variants — Encoder-Only, Decoder-Only, Encoder-Decoder

In Parts 6–10 we built up the full Transformer: an encoder that reads and a decoder that writes. But look at the models making headlines today and you'll notice something odd — most of them **threw half of the machine away**.

This part explains why, and introduces the three families every modern model belongs to.

---

## 1. Different tasks need different ways of reading

A single one-size-fits-all architecture is often computationally inefficient. Different NLP tasks need **different patterns of information access**:

| The task feels like... | What it needs | Example |
|---|---|---|
| **Understanding** | See every word at once — the whole sentence, both directions | "Is this review positive?" — you need the full sentence before judging |
| **Creating** | Write one word at a time, like a human speaking or writing a story | "Continue this story..." |
| **Transforming** | Read one full sequence, then map it to an entirely different one | English sentence → French translation |

So the industry branched the Transformer into **three distinct variants**, each keeping only the parts its task needs:

<div class="mermaid">
flowchart TB
    T["🤖 The full Transformer<br/>(encoder + decoder)"]

    T --> E["📖 Encoder-only<br/>(auto-encoding)<br/><b>BERT</b>"]
    T --> D["✍️ Decoder-only<br/>(autoregressive)<br/><b>GPT</b>"]
    T --> ED["🔄 Encoder-decoder<br/>(sequence-to-sequence)<br/><b>T5</b>"]

    E --> EU["Understanding:<br/>classification, search, NER"]
    D --> DU["Generating:<br/>chatbots, stories, code"]
    ED --> EDU["Transforming:<br/>translation, summarisation"]

    style T fill:#dbeafe,stroke:#2563eb
    style E fill:#dcfce7,stroke:#16a34a
    style D fill:#fef3c7,stroke:#d97706
    style ED fill:#f3e8ff,stroke:#9333ea
</div>

---

## 2. Encoder-only models (auto-encoding): BERT, the reader

**Keep:** the encoder stack. **Throw away:** the decoder.

An encoder-only model (also called an **auto-encoding** model) is just stacked encoder layers. Its hallmark is **fully bidirectional self-attention**: every word can attend to every other word — past *and* future — at the same time.

If the model is looking at the 5th word of a 10-word sentence, it simultaneously sees words 1–4 (the past) **and** words 6–10 (the future). It has a **global view** of the input.

```text
Sentence:  The bank will not [word 5] the loan application
                              ↑
              word 5 sees everything on BOTH sides at once
```

This makes it incredibly powerful at building **rich contextual representations**. Instead of a word having one fixed meaning, the model refines its understanding of each word using the complete sentence context — this is exactly the contextual embedding idea promised back in [Part 1]({{ site.baseurl }}/topics/dl-genai-word-embeddings/): "bank" near "loan" gets a money-vector, "bank" near "river" gets a geography-vector.

**The trade-off:** there is no mechanism for generating new tokens. A pure encoder-only model **cannot write a story for you**. Its outputs are contextual embeddings — dense vectors, perfectly aligned with the input positions, one per input token. These models are **the readers of the table**.

### How BERT is trained: masked language modelling

BERT (**B**idirectional **E**ncoder **R**epresentations from **T**ransformers) changed the game by changing *how* we train. Instead of predicting the next word, it plays **fill in the blanks**:

```text
Original:  I drink hot coffee every morning
Masked:    I drink [MASK] coffee every [MASK]
Model:     guess the blanked words using BOTH sides
```

Roughly 15% of the words are blanked out, and the model's job is to use the words on the left **and** the right to guess what fits. If you only looked in one direction, you'd lose half the context — this forces the model to learn **deep bidirectional relationships**.

BERT was additionally trained with **next sentence prediction**: show it two sentences and ask whether sentence B logically follows sentence A.

> This "learn by filling blanks on unlabelled text" trick is a form of **self-supervised learning** — covered in depth in [Self-Supervised Learning - A Friendly Guide]({% link _topics/Self-Supervised Learning - A Friendly Guide.md %}), including runnable BERT and GPT examples.

**Best at:** sentiment classification, semantic search, named entity recognition, question answering — anything where the whole input is available up front and the job is to *understand* it.

---

## 3. Decoder-only models (autoregressive): GPT, the writer

**Keep:** the decoder stack (minus cross-attention — there's no encoder to look at). **Throw away:** the encoder.

An **autoregressive** model generates text **one token at a time**, each new token conditioned on everything written so far — exactly the masked self-attention from [Part 8]({{ site.baseurl }}/topics/dl-genai-transformer-architecture/): look back as much as you like, never peek ahead.

```text
The cat sat on the ___        → "mat"  (97%)
The cat sat on the mat and ___ → "purred" (61%)
```

**Training is beautifully simple:** take any text on the internet, hide the next word, ask the model to predict it. No labels needed, infinite training data. Repeat over trillions of words.

**The trade-off:** it only ever sees the past, never the future — so its understanding of a full sentence is less naturally bidirectional than BERT's. But it can **generate**, and that turned out to be the killer feature.

**Best at:** chatbots, story and code generation, and — with enough scale — nearly everything. GPT-style decoder-only models are what power most modern LLMs (ChatGPT, Claude, Gemini). Your question isn't fed to a separate encoder; it simply becomes the beginning of the "text so far".

---

## 4. Encoder-decoder models (sequence-to-sequence): T5, the translator

**Keep:** everything. This is the original Transformer from Parts 6–10.

Use it when you take one full sequence and map it to an **entirely different sequence**: English sentence → French translation, long article → short summary, English request → Python code.

The encoder gets the bidirectional global view of the input (like BERT); the decoder writes autoregressively (like GPT), glancing at the encoder's notes through cross-attention. Best of both — at the cost of running both.

**Best at:** translation, summarisation, and structured transformation tasks. Examples: the original Transformer, T5, BART.

---

## 5. The three families side by side

| | Encoder-only | Decoder-only | Encoder-decoder |
|---|---|---|---|
| Also called | Auto-encoding | Autoregressive | Sequence-to-sequence |
| Attention | Bidirectional (sees both sides) | Causal / masked (past only) | Bidirectional in, causal out |
| Output | Contextual embeddings (one per input token) | New tokens, one at a time | New tokens, one at a time |
| Can generate text? | ❌ | ✅ | ✅ |
| Trained by | Fill in the blanks (masked LM) | Predict the next word | Map input pairs to outputs |
| Famous example | BERT | GPT | T5, original Transformer |
| Analogy | The reader who understands every nuance | The storyteller who never stops | The translator with a notepad |

<div class="mermaid">
flowchart LR
    subgraph tasks["Pick by task"]
        U["Understand text?<br/>→ Encoder-only"]
        G["Generate text?<br/>→ Decoder-only"]
        X["Transform text?<br/>→ Encoder-decoder"]
    end

    style U fill:#dcfce7,stroke:#16a34a
    style G fill:#fef3c7,stroke:#d97706
    style X fill:#f3e8ff,stroke:#9333ea
</div>

---

## 6. Summary

- One size doesn't fit all: **understanding**, **creating**, and **transforming** need different patterns of information access, so the Transformer split into three families.
- **Encoder-only (BERT):** fully bidirectional, outputs contextual embeddings, cannot generate — the reader. Trained by masking words and guessing them from both sides.
- **Decoder-only (GPT):** autoregressive, writes one token at a time using only the past — the writer. Trained by next-word prediction on unlabelled text. Powers most modern LLMs.
- **Encoder-decoder (T5):** the full original machine — bidirectional reading plus autoregressive writing — the translator.
- These also deliver the **contextual embeddings** promised in Part 1: the same word finally gets a different vector in different sentences.

**Next up:** put the encoder-only reader to work — load a pre-trained BERT from Hugging Face and fine-tune it for sentiment classification in [Part 12: Sequence Classification with BERT (Hands-On)]({{ site.baseurl }}/topics/dl-genai-bert-sequence-classification/).
