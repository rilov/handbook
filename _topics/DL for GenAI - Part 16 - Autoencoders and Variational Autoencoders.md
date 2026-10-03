---
layout: topic
title: "Deep Learning for Generative AI — Part 16: Autoencoders and Variational Autoencoders"
category: Generative AI
order: 116
permalink: /topics/dl-genai-autoencoders-and-vaes/
tags:
  - generative-ai
  - deep-learning
  - vae
  - autoencoders
  - generative-models
  - tensorflow
  - fashion-mnist
  - hands-on
  - beginners
  - friendly
summary: "Why deterministic autoencoders reconstruct but cannot generate, and how Variational Autoencoders add probability, the reparameterisation trick, and the ELBO objective to make smooth, sample-able latent spaces."
---

# Deep Learning for Generative AI — Part 16: Autoencoders and Variational Autoencoders

In [Part 15]({{ site.baseurl }}/topics/dl-genai-multimodal-generative-intro/) we said that autoencoders **compress and reconstruct**, but they are not true generative models. This part explains why, and introduces **Variational Autoencoders (VAEs)** — the first practical way to turn an encoder-decoder into a model that can generate new data.

---

## 1. The autoencoder review

An autoencoder has two parts:

```text
x  →  encoder  →  z  →  decoder  →  x̂
```

- **Encoder** squeezes the input `x` into a smaller latent vector `z`.
- **Decoder** tries to reconstruct `x` from `z`, producing `x̂`.
- Training minimises reconstruction loss (usually mean squared error): `||x - x̂||²`.

This works well for denoising, compression, and learning useful features. But it is a **transformation**, not a generator.

---

## 2. Why autoencoders cannot generate

### Problem 1: each input becomes one point

A standard autoencoder maps every training example to a **single deterministic point** in latent space. There is no notion of probability, density, or uncertainty.

```text
Training image 1  →  z = [-0.4,  0.7]
Training image 2  →  z = [ 1.2, -0.3]
Training image 3  →  z = [ 0.1,  0.1]
```

The latent space ends up as a scattered, irregular collection of training points. If you pick a random latent point and decode it, the decoder has never seen anything like it and usually produces nonsense.

### Problem 2: the decoder only sees encoder-produced points

During training, the decoder learns to reconstruct only from latent codes that came from the encoder. It has no experience with the rest of the space. Generation requires decoding from **new** points, but the decoder has not learned how.

### Problem 3: reconstruction loss averages plausible outputs

Mean squared error tells the model: “produce one best answer.” If several reconstructions are equally plausible, the model learns their **average**, which is blurry. It never learns to represent the fact that multiple good answers exist.

---

## 3. The VAE idea: encode a distribution, not a point

A Variational Autoencoder changes one key thing: instead of mapping each input to a single point `z`, the encoder outputs the **parameters of a probability distribution** over `z`.

Usually it predicts:

```text
mean       μ(x)
log-variance log σ²(x)
```

So each input becomes a Gaussian in latent space:

```text
z ~ N(μ(x), σ²(x)I)
```

To get a concrete code, we **sample** from that Gaussian. The sampled `z` is then passed to the decoder.

```text
x  →  encoder  →  μ, log σ²  →  sample z  →  decoder  →  x̂
```

Now nearby latent points are related, and the decoder learns to reconstruct from many different points drawn from each distribution.

---

## 4. The reparameterisation trick

Sampling is random, so how do we backpropagate? The reparameterisation trick moves the randomness outside the gradient path:

```text
ε ~ N(0, 1)    (random noise, sampled fresh each forward pass)
z = μ + σ * ε
```

During backpropagation, `μ` and `σ` are adjusted so the distribution moves and shapes itself. The noise `ε` is treated as a constant input, so gradients flow through `μ` and `σ` normally.

Think of it as drawing a random direction and distance from a standard normal, then stretching and shifting that sample by the encoder's parameters.

---

## 5. The ELBO objective: two competing pressures

A VAE is trained to maximise the **Evidence Lower Bound (ELBO)**, a lower bound on the log-likelihood of the data. In practice it has two terms:

### Reconstruction term

Measures how well the decoder reconstructs the input from a sampled `z`.

```text
E[ log p(x | z) ]
```

For images this is usually binary cross-entropy or mean squared error.

### KL divergence term

Measures how far the learned posterior `q(z|x)` is from a simple prior `p(z)`, usually a standard normal `N(0, I)`.

```text
KL( q(z|x) || p(z) )
```

This forces every encoded distribution to stay close to a common, smooth, centred distribution. The latent space becomes continuous and dense, which makes sampling possible.

### Full objective

```text
ELBO = reconstruction loss - KL divergence
```

Maximise ELBO = reconstruct accurately *and* keep latent codes close to a standard normal.

The two terms compete:

- If reconstruction dominates, the model memorises training points and the latent space stays irregular.
- If KL dominates, every code collapses to the prior and the decoder ignores the input.

Good VAE training finds a balance.

---

## 6. What a VAE buys you

| | Standard autoencoder | VAE |
|---|---|---|
| Latent representation | single point | probability distribution |
| Latent space | sparse and irregular | smooth and dense |
| Can sample new data? | no | yes |
| Handles uncertainty? | no | yes |
| Outputs | often blurry if multiple reconstructions plausible | can interpolate and generate |

Because the latent space is regularised toward a known prior, you can:

- sample `z ~ N(0, I)` and decode it,
- interpolate between two images by moving between their latent means,
- explore the learned data manifold by walking through latent space.

---

## 7. Hands-on: a small VAE on Fashion MNIST

The following code builds a minimal VAE in TensorFlow/Keras. It uses a 2D latent space so the learned manifold can be visualised easily.

### Install and load data

```python
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

(x_train, _), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()

x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32") / 255.0

x_train = np.expand_dims(x_train, -1)
x_test  = np.expand_dims(x_test, -1)
```

### Sampling layer

```python
class Sampling(layers.Layer):
    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.random.normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon
```

### Encoder

```python
latent_dim = 2

inputs = keras.Input(shape=(28, 28, 1))
x = layers.Conv2D(32, 3, activation="relu", strides=2, padding="same")(inputs)
x = layers.Conv2D(64, 3, activation="relu", strides=2, padding="same")(x)
x = layers.Flatten()(x)
x = layers.Dense(16, activation="relu")(x)

z_mean = layers.Dense(latent_dim)(x)
z_log_var = layers.Dense(latent_dim)(x)
z = Sampling()([z_mean, z_log_var])

encoder = keras.Model(inputs, [z_mean, z_log_var, z], name="encoder")
```

### Decoder

```python
latent_inputs = keras.Input(shape=(latent_dim,))
x = layers.Dense(7 * 7 * 64, activation="relu")(latent_inputs)
x = layers.Reshape((7, 7, 64))(x)
x = layers.Conv2DTranspose(64, 3, activation="relu", strides=2, padding="same")(x)
x = layers.Conv2DTranspose(32, 3, activation="relu", strides=2, padding="same")(x)
outputs = layers.Conv2DTranspose(1, 3, activation="sigmoid", padding="same")(x)

decoder = keras.Model(latent_inputs, outputs, name="decoder")
```

### VAE model with the ELBO as a custom loss

```python
class VAE(keras.Model):
    def __init__(self, encoder, decoder, **kwargs):
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder

    def call(self, inputs):
        z_mean, z_log_var, z = self.encoder(inputs)
        reconstruction = self.decoder(z)

        # Reconstruction loss: binary cross-entropy per pixel
        reconstruction_loss = tf.reduce_mean(
            tf.reduce_sum(
                keras.losses.binary_crossentropy(inputs, reconstruction), axis=(1, 2)
            )
        )

        # KL divergence to a standard normal
        kl_loss = -0.5 * tf.reduce_mean(
            tf.reduce_sum(
                1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var), axis=1
            )
        )

        total_loss = reconstruction_loss + kl_loss
        self.add_loss(total_loss)
        return reconstruction

vae = VAE(encoder, decoder)
vae.compile(optimizer=keras.optimizers.Adam())
```

### Train

```python
vae.fit(x_train, x_train, epochs=20, batch_size=128, validation_split=0.1)
```

### Generate new images

```python
import matplotlib.pyplot as plt

# Sample 20 points from the prior
grid = np.random.normal(size=(20, 2))
generated = decoder.predict(grid)

fig, axes = plt.subplots(2, 10, figsize=(12, 3))
for i, ax in enumerate(axes.flat):
    ax.imshow(generated[i].squeeze(), cmap="gray")
    ax.axis("off")
plt.show()
```

Because the latent space was regularised, random samples decode into recognisable clothing-like shapes instead of random blots.

---

## 8. What the latent space looks like

After training, you can encode the test set and colour each point by its true clothing class. In a well-trained 2D VAE, similar items cluster together:

```text
T-shirts in one corner, boots in another, bags in another, with gradual transitions between them.
```

Walking smoothly from one cluster to another morphs one item into another — something a deterministic autoencoder usually cannot do.

---

## 9. Summary

- Autoencoders compress and reconstruct, but their latent spaces are sparse and irregular, so they cannot generate reliably.
- VAEs encode each input as a **distribution** over latent codes rather than a single point.
- The **reparameterisation trick** makes sampling differentiable, so the model can be trained end-to-end with backpropagation.
- The **ELBO** objective balances reconstruction accuracy against a KL penalty that keeps the latent space close to a standard normal.
- A trained VAE can sample from its prior, interpolate between examples, and explore the data manifold.

The original VAE paper: [Auto-Encoding Variational Bayes (Kingma & Welling, 2013)](https://arxiv.org/pdf/1312.6114). A step-by-step TensorFlow tutorial is also available [here](https://www.tensorflow.org/tutorials/generative/cvae).

**Next up:** the second major generative family — adversarial training — in [Part 17: Generative Adversarial Networks]({{ site.baseurl }}/topics/dl-genai-gans/).