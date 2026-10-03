---
layout: topic
title: "Deep Learning for Generative AI — Part 15: Introduction to Multimodal Generative Architectures"
category: Generative AI
order: 115
permalink: /topics/dl-genai-multimodal-generative-intro/
tags:
  - generative-ai
  - deep-learning
  - generative-models
  - autoencoders
  - vae
  - gans
  - diffusion
  - multimodal
  - beginners
  - friendly
summary: "The big-picture start of the generative-modeling track: the difference between discriminative prediction, deterministic transformation, and probabilistic generation; why autoencoders reconstruct but do not generate; and a roadmap to VAEs, GANs, diffusion models, and multimodal architectures."
---

# Deep Learning for Generative AI — Part 15: Introduction to Multimodal Generative Architectures

So far in this track we have seen how Transformers learn to **transform** one sequence into another: English → French, text → code, questions → answers. Those are powerful models, but they are still trained as deterministic input–output mappings.

This part shifts the focus to models that learn the **data distribution itself**. Once a model knows how data is produced, it can generate new, realistic samples, reason about uncertainty, and blend information from more than one modality — text, images, audio, or structured data.

---

## 1. Three kinds of models

Machine-learning tasks are usually described in one of three ways:

| Type | Question it answers | Input → output | Examples |
|---|---|---|---|
| **Prediction** | "Given x, what is y?" | email → spam/not spam | classification, regression |
| **Transformation** | "What is the structured counterpart of x?" | English sentence → French sentence | translation, denoising, speech-to-text |
| **Generation** | "What does this kind of data look like?" | noise or prompt → new sample | images, music, text, molecules |

Prediction and transformation are about **boundaries** or **mappings**. Generation is about **probability distributions**: the model learns what values, structures, and combinations are likely, then samples from that distribution.

```text
Prediction:     P(y | x)      → a label
Transformation: P(y | x)    → a paired output
Generation:     P(data)     → a brand-new sample
```

---

## 2. Discriminative vs generative models

A **discriminative** model learns the boundary between classes. It is great at saying “this is a cat” but it cannot draw a cat.

A **generative** model learns what cats look like. It can:

- generate a new cat image,
- tell you whether a new image looks like a cat,
- fill in missing parts of a cat photo,
- smoothly morph between a cat and a dog.

```text
Discriminative:  "Does this look like a cat?"  → decision boundary
Generative:      "What do cats look like?"     → probability distribution over images
```

The same idea applies to text, audio, tabular data, or anything with structure.

---

## 3. Conditional and unconditional generation

Generation can be free-form or guided:

| | Unconditional | Conditional |
|---|---|---|
| Input | None (or random noise) | A class label, text prompt, partial image, etc. |
| Output | A random plausible sample | A sample matching the condition |
| Example | Random face | “A photo of a raccoon wearing an astronaut helmet” |

Modern systems like Stable Diffusion or DALL-E are **conditional** image generators: they learn the distribution of images *given a text prompt*.

---

## 4. The autoencoder trap

An autoencoder looks like a generative model at first glance:

```text
input → encoder → latent code → decoder → reconstructed input
```

It learns to compress and reconstruct data, and the latent code often captures meaningful structure. But a standard autoencoder is **not a true generative model**.

Why?

- Each input becomes **one deterministic point** in latent space.
- The model learns to decode only the points the encoder actually produced.
- Random points in the latent space usually decode into **garbage** because the latent space is sparse and irregular.
- A reconstruction loss like mean squared error averages plausible alternatives, producing **blurry** outputs.

In short: autoencoders **compress** and **reconstruct**, but they do not learn a smooth, probabilistic distribution they can safely sample from.

---

## 5. What makes a model truly generative?

A generative model needs two things:

1. **A structured, probabilistic latent space** — nearby points should decode to similar, realistic outputs.
2. **A way to sample from it** — starting from noise or a prior distribution, the model should produce new, high-quality data.

The next few parts introduce the main families that achieve this:

| Family | Core idea | Strength | Classic example |
|---|---|---|---|
| **VAE** | Encode each input as a distribution, regularise it toward a simple prior | Smooth latent space, principled probability | Kingma & Welling VAE |
| **GAN** | Train a generator and a discriminator in a two-player game | Sharp, realistic samples | DCGAN, StyleGAN |
| **Diffusion** | Learn to reverse a gradual noising process | Stable training, strong likelihoods | DDPM, Stable Diffusion |
| **Autoregressive** | Predict one piece at a time | Exact likelihood, flexible | GPT, PixelCNN |

Transformers like GPT are autoregressive generative models over sequences. The next parts focus on the visual side — images — but the same principles show up everywhere.

---

## 6. Roadmap for the next parts

1. **Part 16** — Autoencoders vs VAEs: why the latent space must become probabilistic.
2. **Part 17** — Generative Adversarial Networks: generator vs discriminator.
3. **Part 18** — Diffusion models and Stable Diffusion: reversing noise step by step.
4. **Part 19** — Multimodal models, CLIP-style alignment, and Vision Transformers.

Along the way we will keep one idea in mind: generative models do not memorise training examples. They learn the **statistical rules** behind the data, then use those rules to create things that never existed before.

**Next up:** dive into the autoencoder trap and how Variational Autoencoders escape it in [Part 16: Autoencoders and Variational Autoencoders]({{ site.baseurl }}/topics/dl-genai-autoencoders-and-vaes/).