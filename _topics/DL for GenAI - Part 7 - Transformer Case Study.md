---
layout: topic
title: "Deep Learning for Generative AI — Part 7: Transformer Case Study — Python Program"
category: Generative AI
order: 107
permalink: /topics/dl-genai-transformer-case-study/
tags:
  - generative-ai
  - deep-learning
  - transformer
  - attention
  - query-key-value
  - self-attention
  - beginners
  - friendly
summary: "A simple walk-through of the Transformer encoder on one sentence — 'Python program to print Hello World' — showing how each word attends to the others."
---

# Deep Learning for Generative AI — Part 7: Transformer Case Study — Python Program

In Part 6 we met the Transformer and the group project analogy. Now let's watch it work on one real example.

Still **no math** here. We only want a high-level glimpse of what the encoder does.

---

## 1. The task

The input sentence has 6 words:

| Position | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Word | Python | program | to | print | Hello | World |

The goal: translate this English sentence into actual Python code.

```text
"Python program to print Hello World"   →   print("Hello World")
```

Let's focus on the **encoder** first.

---

## 2. The encoder's job: 6 words in, 6 rich vectors out

The encoder takes the 6 words and gives back **6 vectors**, one per word:

```text
Python   program   to   print   Hello   World
  ↓         ↓       ↓     ↓       ↓       ↓
  z1        z2      z3    z4      z5      z6
```

Each `z` is a **richer representation** of its word. It captures what the word means *in this sentence*, not just on its own. These rich vectors are what help the decoder produce the right code later.

---

## 3. Every word builds its Query, Key, Value

Back to the group project: the 6 words are the team members. The team's goal is to understand itself better.

Step one: each word comes up with its own Query, Key and Value.

```text
Python  → Q1, K1, V1
program → Q2, K2, V2
to      → Q3, K3, V3
print   → Q4, K4, V4
Hello   → Q5, K5, V5
World   → Q6, K6, V6
```

| Item | Simple meaning |
|---|---|
| Query (Q) | "What am I looking for?" |
| Key (K) | "What can I offer others?" |
| Value (V) | "Here is my information." |

(Just a quick recap — the full group project analogy is in [Part 6, section 4]({{ site.baseurl }}/topics/dl-genai-transformer-intro/).) *How* each word computes these three comes in [Part 9]({{ site.baseurl }}/topics/dl-genai-self-attention-math/). For now, let's see what happens with them.

---

## 4. Example: what does "program" pay attention to?

On its own, the word **program** is unclear. It could mean:

- a TV show or an event
- a celebration schedule
- computer code ✅

So the query of "program" is basically: *"What kind of program am I?"*

The word that answers this best is **Python**. Its key matches program's query strongly, so **program pays a lot of attention to Python**.

| "program" looks at… | Attention | Why |
|---|---|---|
| Python | 🔴 Very high | Tells it what kind of program it is |
| program (itself) | 🔴 High | Its own meaning still matters |
| print | 🟡 Some | Hints at code |
| Hello | 🟡 Some | Part of the task |
| World | 🟡 Some | Part of the task |
| to | ⚪ Very low | Adds almost no meaning |

In the group project, "to" is the friend who doesn't answer many of your questions, so you barely listen to them.

The same thing happens in the other direction. **Python** could also mean a snake, so it pays attention to **program** and **print** to learn that it means the programming language.

---

## 5. Building the new representation

The new vector for "program", `z2`, is a weighted mix of every word's value:

```text
z2 = α1·V1 + α2·V2 + α3·V3 + α4·V4 + α5·V5 + α6·V6
```

- The `α` values are the **attention weights**.
- They always **add up to 1**: `α1 + α2 + ... + α6 = 1`. This makes it a **convex combination**, as in Part 4.
- So if `α1` (Python) and `α2` (program) are big, the others must be small.

Every word does this at the same time, in parallel, which gives `z1` to `z6`.

---

## 6. Summary

- The encoder turns 6 plain words into 6 **rich vectors** `z1...z6`, each aware of its context.
- Each word builds its own **Query, Key and Value**.
- A word pays more attention to the words whose **keys match its query**. "program" listens most to "Python" and hardly at all to "to".
- Its new vector is a **weighted mix of all values**, and the weights add up to 1.

**Next up:** the full Transformer blueprint, box by box, in [Part 8: The Transformer Architecture]({{ site.baseurl }}/topics/dl-genai-transformer-architecture/). After that, [Part 9]({{ site.baseurl }}/topics/dl-genai-self-attention-math/) shows how Q, K, V and the attention weights `α` are actually calculated.
