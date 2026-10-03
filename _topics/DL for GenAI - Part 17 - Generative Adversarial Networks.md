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

### Paired image-to-image translation: pix2pix

When you have **paired** input–output examples, the conditional GAN idea becomes image-to-image translation. The classic model for this is **pix2pix**.

```text
grayscale image  →  colour image
street map       →  aerial satellite photo
sketch           →  realistic photo
low-resolution image  →  high-resolution image
```

pix2pix uses:

- a **U-Net generator**, so the input structure is preserved while the output style is changed;
- a **PatchGAN discriminator**, which classifies each small patch as real or fake instead of judging the whole image at once. This encourages local realism and sharper edges.

Because the training data already contains matching pairs, the generator gets direct feedback: “given this input, your output should look like the known target.”

---

### Unpaired image-to-image translation

Many interesting translations do **not** have paired examples:

```text
horse  ↔  zebra          (the same animal cannot be both at once)
summer scene  ↔  winter scene
photograph  ↔  Monet painting
sunny day  ↔  foggy day
```

For these cases we only have two separate collections of images. The challenge is to learn a mapping without knowing which image in domain A corresponds to which image in domain B.

This is where CycleGAN comes in.

---

## 9. CycleGAN: two generators, two discriminators, and three losses

CycleGAN learns two mappings at the same time:

- **G_AB:** domain A → domain B (e.g. horse → zebra)
- **G_BA:** domain B → domain A (e.g. zebra → horse)

Each domain has its own discriminator:

- **D_A:** tells real A images from translated A images.
- **D_B:** tells real B images from translated B images.

### 1. Adversarial loss

Each generator–discriminator pair plays a normal GAN game:

```text
real A images  →  D_A says "real"
G_BA(fake B)   →  D_A says "fake"
real B images  →  D_B says "real"
G_AB(fake A)   →  D_B says "fake"
```

This ensures that translated images look realistic in the target domain.

### 2. Cycle consistency loss

The adversarial loss alone is not enough. A generator could ignore the input and produce any plausible target image, as long as it fools the discriminator. The cycle loss fixes this.

If you translate a horse to a zebra and back, you should end up close to the original horse:

```text
horse  →  G_AB  →  zebra  →  G_BA  →  horse' ≈ horse
```

The same must work in the other direction:

```text
zebra  →  G_BA  →  horse  →  G_AB  →  zebra' ≈ zebra
```

This is a **self-supervised** constraint: the model does not need paired labels, only the requirement that round-trip translations preserve structure.

### 3. Identity loss

The identity loss is a regulariser. If you feed an image that already belongs to the target domain into the generator, it should change very little:

```text
zebra  →  G_AB  →  zebra   (G_AB maps A→B, so a B input should stay a B input)
```

This prevents the model from unnecessarily altering colours and textures, and helps preserve the input's overall look.

### Why patch-level discriminators?

CycleGAN discriminators often operate on small image patches. This has the same effect as pix2pix's PatchGAN: it focuses on local texture and structure rather than memorising the whole image, which matters when the overall layout must stay the same and only the style should change.

### Limitations

CycleGAN assumes both domains share the same geometry and content. If you ask it to turn a horse into a zebra, it assumes the horse shape is preserved and only the texture changes. When domains differ in shape or semantics, it can distort objects or hallucinate details.

- CycleGAN project page: <https://junyanz.github.io/CycleGAN/>
- Original paper: [Zhu et al., 2017](https://arxiv.org/pdf/1703.10593)

---

## 10. Latent-space arithmetic with DCGAN

A well-trained GAN learns a meaningful latent space. You can treat latent vectors like word vectors and do arithmetic on them.

A classic face-GAN example:

```text
smiling_woman  -  neutral_woman  +  neutral_man  ≈  smiling_man
```

How does this work?

1. Find latent vectors that the generator turns into images in each category.
2. Average several examples per category to get a stable centre.
3. Subtract the “woman” direction and add the “man” direction to the “smiling woman” direction.
4. Feed the result into the generator.

The generator has disentangled concepts like “smiling” and “gender” into different directions in latent space. This shows that the model has learned semantic structure, not just memorised training images.

---

## 11. A simple GAN on Fashion MNIST

Here is a compact TensorFlow/Keras sketch that trains a simple GAN on the Fashion MNIST dataset. The goal is not production code; it is to see the generator and discriminator shapes and the alternating update pattern.

### Generator

```python
latent_dim = 100

generator = keras.Sequential([
    layers.Dense(7 * 7 * 128, input_shape=(latent_dim,)),
    layers.Reshape((7, 7, 128)),
    layers.BatchNormalization(),
    layers.Conv2DTranspose(64, 5, strides=2, padding="same", activation="relu"),
    layers.BatchNormalization(),
    layers.Conv2DTranspose(1, 5, strides=2, padding="same", activation="sigmoid"),
], name="generator")
```

The generator turns a 100-dimensional noise vector into a 28×28 grayscale image.

### Discriminator

```python
discriminator = keras.Sequential([
    layers.Conv2D(64, 5, strides=2, padding="same", input_shape=[28, 28, 1]),
    layers.LeakyReLU(0.2),
    layers.Conv2D(128, 5, strides=2, padding="same"),
    layers.LeakyReLU(0.2),
    layers.Flatten(),
    layers.Dense(1, activation="sigmoid"),
], name="discriminator")
```

The discriminator receives either a real Fashion MNIST image or a generated image, and outputs a single probability.

### Training loop

```python
g_optimizer = keras.optimizers.Adam(1e-4)
d_optimizer = keras.optimizers.Adam(1e-4)
cross_entropy = keras.losses.BinaryCrossentropy()

@tf.function
def train_step(real_images):
    noise = tf.random.normal([batch_size, latent_dim])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(noise, training=True)

        real_output = discriminator(real_images, training=True)
        fake_output = discriminator(generated_images, training=True)

        # Generator wants discriminator to think fakes are real
        gen_loss = cross_entropy(tf.ones_like(fake_output), fake_output)

        # Discriminator wants to label real as 1 and fake as 0
        real_loss = cross_entropy(tf.ones_like(real_output), real_output)
        fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
        disc_loss = real_loss + fake_loss

    gen_gradients = gen_tape.gradient(gen_loss, generator.trainable_variables)
    disc_gradients = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    g_optimizer.apply_gradients(zip(gen_gradients, generator.trainable_variables))
    d_optimizer.apply_gradients(zip(disc_gradients, discriminator.trainable_variables))
```

After many epochs, random noise fed into the generator starts producing recognisable clothing-like shapes.

### A note on DCGAN

The demonstration above uses transposed convolutions and batch normalisation, which are the core ideas of **DCGAN**. Replacing the dense layers at the start with a fully convolutional architecture and following DCGAN guidelines usually makes image GANs more stable.

---

## 12. Summary

| Idea | In one sentence |
|---|---|
| **GAN** | Two networks play a game: a generator creates fakes, a discriminator detects them. |
| **Minimax** | Discriminator maximises realism scores for real data and minimises them for fakes; generator does the opposite. |
| **Equilibrium** | At the ideal point, the discriminator cannot tell real from fake. |
| **Sharpness** | GANs optimise for perceptual realism, not pixel-wise reconstruction, so they tend to produce crisp outputs. |
| **Failure modes** | Mode collapse, discriminator domination, and oscillation come from the game dynamics. |
| **Stabilisation** | Feature matching, minibatch discrimination, historical averaging, and architecture variants help keep training healthy. |
| **Conditional GAN** | Add a condition `y` to both networks so generation becomes controllable. |
| **pix2pix** | Paired image-to-image translation with a U-Net generator and PatchGAN discriminator. |
| **CycleGAN** | Unpaired image-to-image translation using two generators, two discriminators, cycle consistency, and identity loss. |
| **Latent arithmetic** | In a trained GAN, semantic concepts become directions in the noise space. |

The original GAN paper: [Goodfellow et al., 2014](https://arxiv.org/pdf/1406.2661).

GANs were the dominant image-generation approach for years and remain central to editing, super-resolution, and domain translation. Their adversarial idea also inspired techniques used in diffusion models and other modern systems.

**Next up:** the third major generative family — models that learn by reversing a gradual noising process — in [Part 18: Diffusion Models and Stable Diffusion]({{ site.baseurl }}/topics/dl-genai-diffusion-models/).