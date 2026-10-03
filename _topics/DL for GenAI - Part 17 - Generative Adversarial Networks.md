---
layout: topic
title: "Deep Learning for Generative AI — Part 17: Generative Adversarial Networks"
category: Generative AI
order: 117
permalink: /topics/dl-genai-gans/
tags:
  - generative-ai
  - deep-learning
  - gans
  - generative-models
  - conditional-gan
  - cyclegan
  - beginners
  - friendly
summary: "How Generative Adversarial Networks turn generation into a two-player game between a generator and a discriminator, and how conditional and cycle-consistent extensions guide the output."
---

# Deep Learning for Generative AI — Part 17: Generative Adversarial Networks

[Part 16]({{ site.baseurl }}/topics/dl-genai-autoencoders-and-vaes/) showed how Variational Autoencoders make generation possible by learning a probabilistic latent space. GANs take a very different route: instead of writing down a likelihood and optimising it, they turn generation into a **competition** between two networks.

---

## 1. The core idea: a forger and a detective

A GAN has two players:

- **Generator (G):** the forger. It takes random noise and tries to create fake samples that look real.
- **Discriminator (D):** the detective. It looks at both real data and the generator's fakes, and tries to tell them apart.

```text
Real data  ────────────────────────────────┐
                                           ├──→ Discriminator → "real" or "fake"
Noise  →  Generator  →  Fake sample  ──────┘
```

The generator wants to fool the discriminator. The discriminator wants to avoid being fooled. They train together.

---

## 2. The minimax game

Training is a minimax problem:

- The discriminator tries to **maximise** its accuracy at spotting fakes.
- The generator tries to **minimise** the discriminator's success — i.e., it tries to make the discriminator call its samples real.

In its simplest form the objective looks like:

```text
D wants:  high score for real data, low score for fake data
G wants:  high score for fake data
```

This is usually written with a binary cross-entropy loss. The discriminator is trained on a mix of real and fake samples, and the generator is trained to make the discriminator assign high “realness” scores to its outputs.

The two networks are locked in a race:

1. Better fakes force the discriminator to improve.
2. A better discriminator forces the generator to improve.
3. At equilibrium, the generator produces samples that the discriminator cannot distinguish from real data.

---

## 3. Why GANs produce sharper images than VAEs

VAEs learn a smooth distribution and sometimes pay for it with blur, because the KL term and the reconstruction loss encourage averaging. GANs do not directly optimise pixel-wise similarity. Instead, they optimise for “fooling a critic.” This often produces **sharper, more realistic-looking** images.

The trade-off is training stability. Because the two networks are competing, GAN training can be finicky:

- The generator may collapse and produce the same output over and over (**mode collapse**).
- One network may dominate, leaving the other with no useful gradient.
- Careful architecture choices (batch normalisation, proper learning rates, alternate update schedules) help keep the game balanced.

---

## 4. Conditional GANs: steering the generator

A plain GAN generates random samples. A **conditional GAN (cGAN)** gives the generator extra information so it produces samples of a particular kind.

```text
noise + label "cat"  →  Generator  →  image of a cat
```

The discriminator also receives the label, so its job becomes: “Is this a real image **of a cat**, or a fake image of a cat?”

This turns unconditional generation into a controllable process. Condition labels can be class labels, text embeddings, sketches, segmentation maps, or even another image.

---

## 5. CycleGAN: translating between domains without paired examples

CycleGAN solves a clever problem: convert images from one domain to another when you do **not** have paired examples.

For example, you might have a pile of horse photos and a pile of zebra photos, but no photo of the same horse as a zebra. CycleGAN learns:

- **G:** horse → zebra
- **F:** zebra → horse

The key idea is **cycle consistency**: if you turn a horse into a zebra and back again, you should get something close to the original horse.

```text
horse  →  G  →  zebra  →  F  →  horse-like image
```

This cycle loss stops the generator from ignoring the input and producing random zebras. Together with the usual adversarial losses, it learns a meaningful mapping between two unpaired collections of images.

---

## 6. A tiny code sketch

Here is a conceptual PyTorch snippet showing the training loop shape. It is not a full runnable model, but it captures the GAN idea clearly.

```python
for real_data in dataloader:
    # Sample random noise
    noise = torch.randn(batch_size, latent_dim)

    # Generator makes fakes
    fake_data = generator(noise)

    # --- Train discriminator ---
    d_real = discriminator(real_data)
    d_fake = discriminator(fake_data.detach())  # don't train generator here

    d_loss = binary_cross_entropy(d_real, real_labels) \
           + binary_cross_entropy(d_fake, fake_labels)

    d_loss.backward()
    optimizer_D.step()

    # --- Train generator ---
    d_fake = discriminator(fake_data)
    g_loss = binary_cross_entropy(d_fake, real_labels)  # wants to be called real

    g_loss.backward()
    optimizer_G.step()
```

Notice the asymmetry: the discriminator is trained on real and fake data, while the generator is trained only through the discriminator's feedback.

---

## 7. Strengths and limitations

| Strength | Limitation |
|---|---|
| Often produces sharp, realistic samples | Training can be unstable and requires tuning |
| No need to define an explicit likelihood | Hard to evaluate — “realistic” is subjective |
| Easy to condition on labels, text, or images | Mode collapse: generator may ignore parts of the data distribution |
| CycleGAN handles unpaired domain translation | Convergence is not guaranteed like VAE ELBO optimisation |

---

## 8. Summary

- GANs frame generation as a two-player game: a **generator** creates samples and a **discriminator** judges them.
- The discriminator maximises its ability to detect fakes; the generator minimises it.
- This adversarial pressure often leads to sharper samples than likelihood-based models like VAEs.
- **Conditional GANs** guide generation with extra inputs such as class labels or text.
- **CycleGAN** learns unpaired image-to-image translation by enforcing cycle consistency.

GANs were the dominant generative-image approach for several years. They remain influential, especially for image editing, style transfer, and domain translation. Later models such as StyleGAN pushed realism further, but diffusion models have recently taken over for high-quality text-to-image generation — the topic of the next part.

**Next up:** models that learn generation by reversing a gradual noising process — [Part 18: Diffusion Models and Stable Diffusion]({{ site.baseurl }}/topics/dl-genai-diffusion-models/).