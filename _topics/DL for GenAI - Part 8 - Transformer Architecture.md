---
layout: topic
title: "Deep Learning for Generative AI — Part 8: The Transformer Architecture, Explained Simply"
category: Generative AI
order: 108
permalink: /topics/dl-genai-transformer-architecture/
tags:
  - generative-ai
  - deep-learning
  - transformer
  - attention
  - multi-head-attention
  - positional-encoding
  - encoder-decoder
  - beginners
  - friendly
summary: "The full Transformer blueprint, box by box: embeddings, positional encoding, multi-head attention, add & norm, feed-forward, masked attention, cross-attention, and how the output is generated one word at a time."
---

# Deep Learning for Generative AI — Part 8: The Transformer Architecture, Explained Simply

In Part 6 we learned the big idea (Query, Key, Value and the group project). In Part 7 we watched the encoder enrich the words of one sentence.

Now let's open the whole machine and look at **every box** in it. Still no heavy math. By the end you should be able to look at the famous Transformer diagram and explain each part to a friend.

We'll use the same example as Part 7:

```text
Input  (English):  Python program to print Hello World
Output (code):     print ( "Hello World" )
```

---

## 1. The full blueprint

<img src="{{ site.baseurl }}/assets/img/transformer-architecture-overview.svg" alt="The Transformer blueprint. On the left, the encoder: the input sentence goes through input embedding, positional encoding, then an encoder layer made of multi-head self-attention, add and norm, feed-forward network, add and norm, repeated six times, producing rich vectors z1 to z6. On the right, the decoder: the output so far goes through output embedding and positional encoding, then a decoder layer made of masked self-attention, cross-attention that looks at the encoder output, and a feed-forward network, each followed by add and norm, repeated six times. Finally a linear and softmax layer scores every possible next word, and the chosen word is fed back into the decoder input." style="width:100%;max-width:900px;">

Think of it as a company with **two departments**:

| Department | Job | Analogy |
|---|---|---|
| **Encoder** (left, blue) | Read and understand the input | The reading team that studies the request |
| **Decoder** (right, green) | Write the output, one word at a time | The writing team that drafts the answer, checking the reading team's notes as it goes |

The numbered boxes are the seven pieces we'll walk through. Once you know those seven, you know the Transformer.

---

## 2. Box 1: Input Embedding (words become numbers)

Computers can't read words, only numbers. So each word is first turned into a vector, exactly as in Part 1 (Word Embeddings).

```text
"Python"  → [0.21, -0.40, 0.88, ...]
"program" → [0.19, -0.35, 0.72, ...]
...
```

In the original Transformer each vector has **512 numbers**. Words with similar meanings get similar vectors.

**Problem:** these starting vectors describe each word **alone**. "program" gets the same vector whether it means code or a TV show. Fixing that is the job of everything that follows.

---

## 3. Box 2: Positional Encoding (giving every word a seat number)

Here's a surprise. Attention looks at all the words **at the same time**. That's what makes it fast, but it also means it has **no idea of word order**. To plain attention, these two sentences look the same:

<img src="{{ site.baseurl }}/assets/img/transformer-positional-encoding.svg" alt="Without positions, 'dog bites man' and 'man bites dog' look like the same bag of three words, so the two sentences look identical. With positional encoding, each word gets a seat number: in sentence A dog is seat 1 and man is seat 3, in sentence B man is seat 1 and dog is seat 3, so the model knows who bit whom. The input to the Transformer is the word embedding plus a position vector." style="width:100%;max-width:900px;">

The fix is simple: **add a position vector to every word vector**.

```text
input to the Transformer = word embedding (what it means) + position vector (where it sits)
```

**Analogy:** a cinema ticket. The ticket says *who* you are and *which seat* you're in. Two people with the same name in different seats are clearly different.

The original paper builds these position vectors from sine and cosine waves of different speeds, so every position gets a unique pattern. You don't need the formula yet. Just remember: **meaning + position goes in**.

---

## 4. The encoder layer

Every encoder layer has the same two main parts: **multi-head self-attention**, then a **feed-forward network**. After each part comes a small **Add & Norm** step.

### Box 3: Multi-Head Self-Attention (several discussions at once)

This is the group project from [Part 6]({{ site.baseurl }}/topics/dl-genai-transformer-intro/) and [Part 7]({{ site.baseurl }}/topics/dl-genai-transformer-case-study/): every word makes a Query, Key and Value, and each word ends up with a weighted blend of the other words' values. (No re-explanation needed here — if Q, K, V feel fuzzy, revisit Part 6 first.)

**Multi-head** just means the team holds **several discussions at the same time**, each with a different focus:

<img src="{{ site.baseurl }}/assets/img/transformer-multi-head-attention.svg" alt="Three attention heads for the word 'program'. Head 1, meaning, asks what kind of program it is and listens mostly to Python (0.55). Head 2, action, asks what the program does and listens mostly to print (0.50). Head 3, content, asks what the program will print and listens mostly to Hello and World (0.30 each). The heads' answers are joined together into one richer vector. The original Transformer uses 8 heads." style="width:100%;max-width:900px;">

- Head 1 might learn "what kind of thing is this?" (program → Python).
- Head 2 might learn "what action is involved?" (program → print).
- Head 3 might learn "what is the content?" (program → Hello, World).

Each head produces its own answer. The answers are joined side by side and mixed into one vector. One discussion can only focus on one thing, but eight discussions can cover grammar, meaning, and more, all at once.

> The heads above are illustrative. In a real model **nobody assigns the topics**. Each head discovers its own focus during training.

### Add & Norm (keep your notes, then tidy up)

After attention, two small housekeeping steps happen:

- **Add** (a *residual connection*): add the word's original vector back to the attention result. *Analogy:* after a group discussion, you don't throw away your own notes. You keep them and add what you learned. This also helps training on very deep networks (the same trick ResNet uses in vision).
- **Norm** (*layer normalisation*): rescale the numbers so they stay in a steady, sensible range. *Analogy:* adjusting the volume so nobody is shouting or whispering.

### Box 4: Feed-Forward Network (think it over alone)

After the discussion, each word goes through a small ordinary neural network **by itself**, with no looking at other words.

*Analogy:* after the team meeting, everyone goes home and thinks quietly about what they heard. The discussion is where words **share**. The feed-forward step is where each word **processes**.

In the original paper this network widens each vector from 512 to 2048 numbers and then squeezes it back to 512.

### Stacked six times

One encoder layer = attention → add & norm → feed-forward → add & norm. The original Transformer **stacks six** of these, one after another.

*Analogy:* reading a hard book several times. First pass: who's who. Later passes: deeper meaning. Each layer builds on the understanding of the one below.

The encoder's final output is `z1 … z6`, one rich vector per input word, exactly what Part 7 described.

---

## 5. The decoder layer

The decoder looks almost the same, with **one extra attention** and **one rule**.

### Box 5: Masked Self-Attention (no peeking at future words)

The decoder first lets the words it has **written so far** discuss with each other. But there's a rule: a word may only look at itself and the words **before** it.

<img src="{{ site.baseurl }}/assets/img/transformer-masked-attention.svg" alt="A five by five grid for the output words start, print, open bracket, Hello World, close bracket. Each word can look at itself and the words before it (green ticks, forming a lower triangle) but not the words after it (grey crosses). The mask exists because during training the whole correct answer is given at once, and without it a word could copy the next word. Exam analogy: you may re-read what you have written, but not the answer key." style="width:100%;max-width:900px;">

Why? During training the decoder is shown the whole correct answer at once, so it can learn from all positions in parallel. Without the mask, the position after "print" could simply peek at "(" and copy it. It would learn nothing.

*Analogy:* an exam. You can re-read your own earlier answers, but you can't look at the answer key.

### Box 6: Cross-Attention (checking the reading team's notes)

Next, the decoder asks the encoder for help. In cross-attention:

- the **Queries** come from the decoder ("what do I need to write next?")
- the **Keys and Values** come from the encoder's `z1 … z6` ("here is what the input says")

So when the decoder is about to write the text inside the brackets, its query matches the keys of **Hello** and **World**, and it pulls in their meaning.

*Analogy:* the writing team glancing back at the reading team's notes before writing each word.

This is the same "decoder looks back at the encoder" idea from Part 3, now built entirely from Query, Key and Value.

### Then: Feed-Forward, Add & Norm, stacked six times

Exactly as in the encoder. One decoder layer = masked self-attention → cross-attention → feed-forward, each followed by add & norm, and six layers stacked.

---

## 6. Box 7: Linear + Softmax (picking the next word)

At the top, the decoder has one vector for the current position. It must turn that into an actual word.

1. **Linear:** give a score to **every word in the vocabulary** (tens of thousands of possible words).
2. **Softmax:** turn those scores into probabilities that add up to 1.

```text
After "<start> print (" the model might say:

  "Hello World"   0.82   ← pick this one
  "Hi"            0.06
  )               0.04
  ...everything else shares the remaining 0.08
```

*Analogy:* a multiple-choice question with thousands of options, where the model writes down how confident it is in each.

> Real models split text into **tokens**, which are often pieces of words. Treating `"Hello World"` as one token here just keeps the example tidy.

---

## 7. Putting it all together: writing the code

The encoder reads the input **once**. The decoder then runs in a loop, adding one word per step, until it produces a special `<end>` word:

<img src="{{ site.baseurl }}/assets/img/transformer-generation-steps.svg" alt="Five generation steps. Step 1: input start, the Transformer predicts print. Step 2: input start print, predicts open bracket. Step 3: input start print open bracket, predicts Hello World. Step 4: adds Hello World, predicts close bracket. Step 5: the full line, predicts end, so it stops. The encoder reads the input once; the decoder runs once per new word with everything written so far." style="width:100%;max-width:900px;">

Final output:

```python
print("Hello World")
```

Here is the whole journey in one list:

1. **Embed** the input words and **add positions**.
2. **Encoder** × 6: words discuss (multi-head self-attention), then think alone (feed-forward). Result: `z1 … z6`.
3. **Decoder** starts with `<start>`, embeds it and adds positions.
4. **Decoder** × 6: look at what's been written (masked), check the encoder's notes (cross-attention), then think alone (feed-forward).
5. **Linear + Softmax** picks the next word.
6. Add that word to the output and go back to step 3, until `<end>`.

---

## 8. The original numbers

From the 2017 paper *Attention Is All You Need* (base model):

| Setting | Value | What it means |
|---|---|---|
| Encoder layers | 6 | Six stacked encoder layers |
| Decoder layers | 6 | Six stacked decoder layers |
| Vector size (d_model) | 512 | Numbers per word vector |
| Attention heads | 8 | Eight discussions at once |
| Size per head | 64 | 512 ÷ 8 |
| Feed-forward size | 2048 | Temporary width inside the feed-forward network |
| Parameters | ~65 million | Tiny next to today's large language models |

---

## 9. Where you meet this today

The same building blocks power modern AI. Different models keep different halves:

| Type | Keeps | Good at | Examples |
|---|---|---|---|
| Encoder–decoder | Both halves | Turning one sequence into another | Original Transformer, T5 (translation, summarisation) |
| Encoder-only | Just the encoder | Understanding text | BERT (search, classification) |
| Decoder-only | Just the decoder (without cross-attention) | Generating text | GPT-style chatbots and most modern LLMs |

A chatbot that writes an answer word by word is doing the loop from section 7. There's just no separate encoder: your question simply becomes the start of the "output so far".

These three families — why they exist and how to pick between them — get a full part of their own: [Part 11: Transformer Variants]({{ site.baseurl }}/topics/dl-genai-transformer-variants/).

---

## 10. Summary

| Box | Name | One-line job | Analogy |
|---|---|---|---|
| 1 | Input Embedding | Words → vectors | A dictionary of number codes |
| 2 | Positional Encoding | Add word order | A seat number on a cinema ticket |
| 3 | Multi-Head Self-Attention | Words share information | Several group discussions at once |
| — | Add & Norm | Keep the original, tidy the numbers | Keep your notes; adjust the volume |
| 4 | Feed-Forward | Each word processes alone | Thinking it over at home |
| 5 | Masked Self-Attention | Look only at words written so far | No peeking at the answer key |
| 6 | Cross-Attention | Decoder checks the input | Glancing at the reading team's notes |
| 7 | Linear + Softmax | Choose the next word | A multiple-choice answer with confidences |

**Next up:** the math. How are Q, K and V actually computed, and how does attention turn into a few matrix multiplications? See [Part 9: The Math Behind Self-Attention]({{ site.baseurl }}/topics/dl-genai-self-attention-math/).
