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
  - wgan
  - dcgan
  - stylegan
  - beginners
  - friendly
summary: "How Generative Adversarial Networks turn generation into a two-player game, what the minimax objective really means, why training is unstable, how researchers stabilise it, and how conditional and cycle-consistent extensions guide the output."
---

# Deep Learning for Generative AI — Part 17: Generative Adversarial Networks

[Part 16]({{ site.baseurl }}/topics/dl-genai-autoencoders-and-vaes/) showed how Variational Autoencoders make generation possible by learning a smooth, probabilistic latent space. The price is often **blurriness**: VAEs average plausible alternatives because their loss encourages reconstruction plus a KL penalty.

GANs take a completely different route. They do not ask, “How likely is this data?” Instead they ask, **“Can you tell this sample is fake?”** Generation becomes a competition between two networks.

---

## 1. The players: forger and detective

A GAN has two neural networks:

- **Generator (G):** the forger. It takes random noise `z` and tries to create a fake sample that looks real.
- **Discriminator (D):** the detective. It receives both real training data and the generator's fakes, and tries to tell which is which.

```text
Noise z  →  Generator  →  Fake sample
                                  ↘
Real data  ─────────────────────→ Discriminator → "real" or "fake"
                                  ↗
```

The generator wants the discriminator to say “real.” The discriminator wants to avoid being fooled. They train together, each improving in response to the other.

---

## 2. The minimax objective in plain words

Training is a **minimax game**. The discriminator tries to maximise its own success; the generator tries to minimise the discriminator's success.

In symbols, the original GAN objective looks like this:

```text
min_G max_D  E[log D(real)] + E[log(1 - D(fake))]
```

Do not worry about the notation. It is just two rewards written together:

| Term | Who wants it high? | What it means |
|---|---|---|
| `E[log D(real)]` | Discriminator | Real data should get a score close to **1**. |
| `E[log(1 - D(fake))]` | Discriminator | Fake data should get a score close to **0**. |
| Same second term, from generator's view | Generator | Fakes should get a score close to **1**, so this term shrinks. |

So the discriminator is trained like a normal binary classifier on a mix of real and fake examples. The generator is trained to make the discriminator misclassify its fakes as real.

### Alternating updates

One training step looks like this:

```text
1. Freeze generator. Update discriminator on real + fake samples.
2. Freeze discriminator. Update generator using the discriminator's feedback.
```

Notice the asymmetry: the discriminator sees real data; the generator does not. The generator learns only through the discriminator's judgement.

---

## 3. Nash equilibrium: when neither player can win

In theory, training reaches a **Nash equilibrium**: the generator's distribution exactly matches the real data distribution, so the discriminator can do no better than random guessing.

```text
At equilibrium:
D(real) ≈ 0.5
D(fake) ≈ 0.5
```

At that point the discriminator is maximally confused, and the generator is producing samples that are, from the discriminator's point of view, indistinguishable from real data.

This equilibrium idea is elegant, but reaching it in practice is hard because the two networks are constantly changing each other's task.

---

## 4. Why GANs produce sharper images than VAEs

VAEs optimise a reconstruction loss plus a KL term. When several outputs are plausible, the model is pushed toward their average, which looks blurry.

GANs do not optimise pixel similarity. They optimise for **fooling a critic**. The discriminator cares about perceptual realism, so the generator is rewarded for sharp edges, textures, and details that make an image look real. This is why GAN outputs often look crisp and photographic.

The trade-off is that the game is harder to train.

---

## 5. Failure modes: when the game breaks

GAN failure modes are not bugs in the code; they come from the minimax setup itself.

### Mode collapse

The generator may find a small set of samples that reliably fool the discriminator and keep producing them. It gets high realism scores, but it ignores most of the data distribution.

```text
Bad behaviour:  noise_1 → face A
                noise_2 → face A (again)
                noise_3 → face A (again)
```

The model produces beautiful faces, but always the same face. The objective rewards realism, not diversity.

### Discriminator too strong

If the discriminator becomes perfect at spotting fakes, the generator receives almost no gradient signal and stops learning. There is no useful feedback telling it how to improve.

```text
D(fake) ≈ 0  →  gradient for generator ≈ 0  →  no progress
```

### Generator too strong

If the generator races ahead, the discriminator cannot provide meaningful direction either. Training oscillates or collapses.

### Non-stationary landscape

Unlike a normal supervised loss that steadily decreases, the GAN objective keeps changing because the opponent keeps changing. This makes learning rates, architectures, and regularisation especially important.

---

## 6. Stabilisation tricks

Researchers have developed several practical fixes that do not change the core game but make it more playable.

| Technique | What it does |
|---|---|
| **Feature matching** | The generator is rewarded for matching intermediate layer statistics of real data, not just final realism scores. This encourages broader coverage. |
| **Minibatch discrimination** | The discriminator looks at several samples at once, making it easier to spot mode collapse because all samples look identical. |
| **Historical averaging** | Parameter updates are smoothed with moving averages, reducing oscillations. |
| **One-sided label smoothing** | Real labels are slightly less than 1, so the discriminator does not become overconfident too quickly. |
| **Careful learning rates** | Usually the generator and discriminator use different update frequencies or learning rates so neither dominates. |

These interventions make GAN training more reliable without removing the adversarial pressure.

---

## 7. Important GAN variants

Several well-known variants improve stability, quality, or controllability.

| Variant | Key change | Why it helps |
|---|---|---|
| **DCGAN** | Convolutional layers, strided convolutions, batch normalisation, no fully connected layers | Gives stable architectural rules for image GANs. |
| **WGAN / WGAN-GP** | Replace the original loss with the Wasserstein distance; add a gradient penalty | Smoother gradients and a more meaningful training curve. |
| **LSGAN** | Use least-squares loss instead of cross-entropy | Less extreme gradients when the discriminator is very confident. |
| **StyleGAN** | Inject learned style vectors at multiple generator layers | Fine-grained control over pose, texture, lighting, etc.; very high-quality faces. |

These all keep the generator-vs-discriminator idea, but change the rules of the game or the architecture to make it easier to train.

---

## 8. Conditional GANs: steering the output

A plain GAN learns `p(x)` — the overall data distribution — and produces random samples. A **conditional GAN** learns `p(x | y)`, where `y` is extra information such as a class label, text, or another image.

```text
Unconditional:  z        → G → random face
Conditional:    z + y    → G → face of age y, wearing glasses y, etc.
```

Both networks receive the condition:

- `G(z, y)` generates a sample consistent with `y`.
- `D(x, y)` judges whether the sample is realistic **given** `y`.

This is how you can ask a GAN to generate “a handwritten digit 7” or “a photo of a sunset.”

### Paired data for image-to-image translation

Many conditional tasks use **paired** examples:

```text
grayscale image  →  colour image
low-resolution image  →  high-resolution image
sketch  →  photograph
```

The discriminator compares the generated output directly against the ground-truth target under the same input condition. This gives a strong supervised signal.

But paired data is not always available. That limitation leads to unpaired translation methods like CycleGAN.

---

## 9. CycleGAN: translating without paired examples

CycleGAN solves the problem: “I have a pile of horse photos and a pile of zebra photos, but no picture of the same horse as a zebra.”

It learns two generators:

- **G:** horse → zebra
- **F:** zebra → horse

The clever part is the **cycle consistency loss**: if you convert a horse to a zebra and back, you should land close to the original horse.

```text
horse  →  G  →  zebra  →  F  →  horse' ≈ horse
```

This stops the generator from ignoring the input and producing random zebras. The same loss runs in the opposite direction:

```text
zebra  →  F  →  horse  →  G  →  zebra' ≈ zebra
```

Together with the usual adversarial losses, CycleGAN learns a meaningful mapping between two unpaired collections of images.

---

## 10. A tiny code sketch

Here is a conceptual PyTorch snippet that shows the alternating update pattern. It is not a full runnable model, but it captures the loop clearly.

```python
for real_data in dataloader:
    noise = torch.randn(batch_size, latent_dim)
    fake_data = generator(noise)

    # --- Train discriminator ---
    d_real = discriminator(real_data)
    d_fake = discriminator(fake_data.detach())  # detach so generator is not trained here

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

The discriminator learns from real and fake data. The generator learns only through the discriminator's scores.

---

## 11. Summary

| Idea | In one sentence |
|---|---|
| **GAN** | Two networks play a game: a generator creates fakes, a discriminator detects them. |
| **Minimax** | Discriminator maximises realism scores for real data and minimises them for fakes; generator does the opposite. |
| **Equilibrium** | At the ideal point, the discriminator cannot tell real from fake. |
| **Sharpness** | GANs optimise for perceptual realism, not pixel-wise reconstruction, so they tend to produce crisp outputs. |
| **Failure modes** | Mode collapse, discriminator domination, and oscillation come from the game dynamics. |
| **Stabilisation** | Feature matching, minibatch discrimination, historical averaging, and architecture variants help keep training healthy. |
| **Conditional GAN** | Add a condition `y` to both networks so generation becomes controllable. |
| **CycleGAN** | Use two generators and cycle consistency to translate between unpaired domains. |

The original GAN paper: [Goodfellow et al., 2014](https://arxiv.org/pdf/1406.2661).

GANs were the dominant image-generation approach for years and remain central to editing, super-resolution, and domain translation. Their adversarial idea also inspired techniques used in diffusion models and other modern systems.

**Next up:** the third major generative family — models that learn by reversing a gradual noising process — in [Part 18: Diffusion Models and Stable Diffusion]({{ site.baseurl }}/topics/dl-genai-diffusion-models/).