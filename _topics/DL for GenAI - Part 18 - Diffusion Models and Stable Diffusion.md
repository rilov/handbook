---
layout: topic
title: "Deep Learning for Generative AI — Part 18: Diffusion Models and Stable Diffusion"
category: Generative AI
order: 118
permalink: /topics/dl-genai-diffusion-models/
tags:
  - generative-ai
  - deep-learning
  - diffusion
  - stable-diffusion
  - latent-diffusion
  - generative-models
  - ddpm
  - ddim
  - classifier-free-guidance
  - pytorch
  - hands-on
  - beginners
  - friendly
summary: "A beginner-friendly tutorial on diffusion models: the forward Markov chain, the reverse denoising process, the simple noise-prediction objective, time-conditioned U-Nets, classifier-free guidance, latent diffusion, Stable Diffusion, and a minimal working 2D example."
---

# Deep Learning for Generative AI — Part 18: Diffusion Models and Stable Diffusion

GANs showed that sharp images can come from competition, but that competition can be unstable. [Part 17]({{ site.baseurl }}/topics/dl-genai-gans/) explained why.

Diffusion models take the opposite route: instead of a two-player game, they use a **fixed corruption process** and learn to undo it. The result is a generative model that is:

- **probabilistic and likelihood-based**,
- **stable to train** (no discriminator),
- **capable of state-of-the-art image quality**.

This part walks through the idea step by step, then builds a tiny working diffusion model in PyTorch on a 2D toy dataset so you can see the pieces move.

---

## 1. The big idea: destroy, then learn to restore

Imagine showing a photograph to a photocopier that adds a little static on every copy. After one copy the picture is almost fine. After a hundred copies it is pure noise.

A diffusion model learns the reverse job: starting from pure static, remove a little noise at a time until a clear picture appears.

```text
data  →  slightly noisy  →  very noisy  →  pure Gaussian noise
  ↑        ↑                 ↑
  └── learn to walk backwards ──┘
```

Generation is therefore **iterative refinement**, not a single step. This is the central difference between diffusion models and GANs or VAEs.

---

## 2. The forward process: a fixed chain of noise

The forward process is a **Markov chain**. Each step adds a small amount of Gaussian noise, and each step depends only on the previous one.

```text
x_0  →  x_1  →  x_2  →  ...  →  x_T
```

- `x_0` is the original data (e.g. an image).
- `x_T` is almost pure Gaussian noise.
- The amount of noise added at each step is set by a **noise schedule**, chosen before training.

Because each corruption step is small and Gaussian, we have a useful shortcut: we can jump straight from `x_0` to any noisy `x_t` without simulating all the intermediate steps.

```text
x_t = sqrt(α_bar_t) * x_0 + sqrt(1 - α_bar_t) * ε
```

In plain words:

- `α_bar_t` is how much of the original signal is left after `t` steps.
- `1 - α_bar_t` is how much noise has been added.
- `ε` is random Gaussian noise.

Early in the chain `α_bar_t` is close to 1, so `x_t` looks almost like `x_0`. Late in the chain `α_bar_t` is close to 0, so `x_t` looks almost like noise.

The forward process is **not learned**. It is just a recipe for corrupting data.

---

## 3. The reverse process: learn to denoise

The reverse process asks: given a noisy `x_t`, what does a slightly cleaner `x_{t-1}` look like?

Instead of predicting the clean image directly, modern diffusion models predict the **noise** that was added:

```text
input:   noisy image x_t  +  timestep t
output:  predicted noise ε_θ(x_t, t)
```

Once we have a noise estimate, we can remove it:

```text
x_{t-1}  ≈  (x_t - noise) / sqrt(α_t)  +  small random correction
```

The network is trained to estimate noise at every noise level. At sampling time, we start from pure Gaussian noise and repeat this denoising step many times.

---

## 4. Training: a simple regression on noise

Training is surprisingly simple and stable:

1. Pick a real data point `x_0`.
2. Pick a random timestep `t`.
3. Add noise to get `x_t` using the closed-form formula from section 2.
4. Ask the network to predict the noise.
5. Minimise the mean squared error between predicted and true noise.

```text
loss = || true_noise - predicted_noise ||²
```

That is it. No discriminator. No minimax game. Each training step is an independent denoising regression task.

Despite its simplicity, this objective corresponds to maximising a lower bound on the data likelihood, just like VAEs. The difference is that the forward process is fixed and well-behaved, so the optimisation landscape is much smoother.

---

## 5. The network: a time-conditioned U-Net

The same network has to denoise images at every noise level, from almost-clean to almost-pure-noise. It needs to know which level it is looking at.

### Timestep embedding

The timestep `t` is converted into a vector and injected into the network, like a tag that says: “this image has lots of noise” or “this image has almost no noise.”

### Why a U-Net?

A U-Net has:

- an **encoder** that compresses the image into broader features,
- a **decoder** that expands those features back to the image size,
- **skip connections** that carry fine detail from the encoder directly to the decoder.

This is a natural fit for denoising: the network must preserve structure while removing noise across many scales.

```text
noisy image  →  encoder  →  bottleneck  →  decoder  →  predicted noise
     ↑              ↓                        ↑
     └────────── skip connections ──────────┘
```

The timestep embedding is added at several layers so the network can behave differently for different noise levels.

---

## 6. Sampling: from noise to data

To generate a new sample:

1. Start with `x_T` drawn from Gaussian noise.
2. For `t = T, T-1, ..., 1`:
   - predict the noise in `x_t`,
   - subtract the right amount of noise to get `x_{t-1}`,
   - add a small random correction (except at the final step).
3. Return `x_0`.

The number of steps controls the trade-off between quality and speed:

| Steps | Quality | Speed |
|---|---|---|
| 1000 | Highest | Slowest |
| 100  | Very good | Reasonable |
| 20–50 | Good | Fast |
| <20  | Often acceptable | Real-time-ish |

The model can be trained with many steps but sampled with fewer because it learns to denoise across the whole noise range.

---

## 7. Faster sampling: DDIM

**DDPM** (Denoising Diffusion Probabilistic Models) sampling is stochastic: each run gives a different result because of the random corrections at every step.

**DDIM** (Denoising Diffusion Implicit Models) rewrites the reverse process so that it can take larger, deterministic jumps. It uses the same trained network, but skips many intermediate steps.

```text
DDPM:  noise  →  step 999  →  step 998  →  ...  →  image
DDIM:  noise  →  step 950  →  step 900  →  ...  →  image
```

DDIM is usually the default in production systems because it gives high-quality results with far fewer forward passes.

---

## 8. Conditional generation and classifier-free guidance

A plain diffusion model learns `p(x)` — the unconditional data distribution. To control generation, we add a condition `c` such as a class label or a text prompt. The network then predicts:

```text
noise = ε_θ(x_t, t, c)
```

The condition is embedded and fed into the U-Net, usually through cross-attention layers.

### Classifier-free guidance

This is the trick that makes text-to-image models follow prompts so strongly.

During training, the model sometimes sees the condition and sometimes sees nothing (an empty condition). It learns two predictions:

- `ε_cond` — prediction with the prompt.
- `ε_uncond` — prediction without the prompt.

At sampling time, the final prediction is pushed away from the unguided direction and toward the guided direction:

```text
guided_noise = ε_uncond + guidance_scale × (ε_cond - ε_uncond)
```

- `guidance_scale = 1` → no guidance (same as unconditional).
- `guidance_scale = 7` → strong guidance, the prompt dominates.

Higher values make the output more literal but can also make it oversaturated or repetitive.

---

## 9. Latent diffusion and Stable Diffusion

Running diffusion directly on high-resolution pixels is expensive. A 512×512 RGB image has 786,432 numbers. Denoising that many values step by step needs huge memory and time.

**Latent diffusion** solves this by moving the entire diffusion process into a compressed latent space.

```text
image  →  autoencoder encoder  →  small latent tensor
         (diffusion happens here)
latent →  autoencoder decoder  →  final image
```

The autoencoder is trained separately to compress images while preserving visual semantics. The diffusion U-Net then operates on the compact latent representation, which is much cheaper.

**Stable Diffusion** is a latent diffusion model with three pieces:

1. A **text encoder** (from CLIP) turns the prompt into an embedding.
2. A **U-Net diffusion model** denoises in latent space, conditioned on the text embedding through cross-attention.
3. A **decoder** maps the final latent representation back to pixels.

```text
prompt  →  text encoder  →  text embedding
                                ↓
noise in latent space  →  U-Net + cross-attention  →  clean latent
                                ↓
                        decoder  →  image
```

This modular design is why Stable Diffusion can generate high-quality 512×512 images on consumer GPUs.

---

## 10. A minimal diffusion tutorial in 2D

The same machinery works on any data. Below is a tiny PyTorch diffusion model trained on a 2D spiral. It shows the forward noising process, the noise-prediction objective, and the reverse sampling loop — all in a few dozen lines.

### Create a tiny spiral dataset

```python
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

def make_spiral(n=2000):
    theta = np.random.rand(n, 1) * 2 * np.pi
    r = theta + 1
    x = np.concatenate([r * np.cos(theta), r * np.sin(theta)], axis=1)
    return (x - x.mean(axis=0)) / x.std(axis=0)
```

### Forward diffusion setup

```python
T = 100                                   # number of timesteps
betas = torch.linspace(1e-4, 0.02, T)     # noise schedule
alphas = 1.0 - betas
alphas_bar = torch.cumprod(alphas, dim=0) # cumulative signal left

def q_sample(x0, t, noise=None):
    """Jump from clean x0 to noisy x_t in one step."""
    if noise is None:
        noise = torch.randn_like(x0)
    sqrt_ab = alphas_bar[t].sqrt()[:, None]
    sqrt_one_minus_ab = (1 - alphas_bar[t]).sqrt()[:, None]
    return sqrt_ab * x0 + sqrt_one_minus_ab * noise
```

### A tiny noise-prediction network

```python
class TinyDenoiser(nn.Module):
    def __init__(self, T):
        super().__init__()
        self.T = T
        self.net = nn.Sequential(
            nn.Linear(2 + 1, 64), nn.ReLU(),
            nn.Linear(64, 64), nn.ReLU(),
            nn.Linear(64, 2),
        )

    def forward(self, x, t):
        # normalise timestep into [0, 1] and append as a feature
        t_norm = t.float()[:, None] / self.T
        return self.net(torch.cat([x, t_norm], dim=1))

model = TinyDenoiser(T)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
```

### Training loop

```python
for epoch in range(3000):
    x0 = torch.tensor(make_spiral(256), dtype=torch.float32)
    t = torch.randint(0, T, (256,))
    noise = torch.randn_like(x0)
    xt = q_sample(x0, t, noise)

    pred_noise = model(xt, t)
    loss = nn.functional.mse_loss(pred_noise, noise)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 500 == 0:
        print(f"epoch {epoch}, loss {loss.item():.4f}")
```

The loss falls because the model learns to predict the noise added at each timestep. That is the entire training objective.

### Sampling: reverse the corruption

```python
@torch.no_grad()
def sample(model, n=1000):
    x = torch.randn(n, 2)  # start from pure noise
    for t in reversed(range(T)):
        t_batch = torch.full((n,), t, dtype=torch.long)
        pred_noise = model(x, t_batch)

        alpha_t = alphas[t]
        alpha_bar_t = alphas_bar[t]
        beta_t = betas[t]

        # DDPM reverse-step update
        x = (x - beta_t / (1 - alpha_bar_t).sqrt() * pred_noise) / alpha_t.sqrt()

        if t > 0:
            x = x + beta_t.sqrt() * torch.randn_like(x)
    return x

generated = sample(model).numpy()
plt.scatter(generated[:, 0], generated[:, 1], s=5)
plt.title("Samples from the tiny diffusion model")
plt.show()
```

After training, the model starts from random points and walks them back into a spiral shape, one denoising step at a time. The same idea scales to 28×28 images, 512×512 images, audio waveforms, or molecular structures.

---

## 11. Summary

| Concept | One-line explanation |
|---|---|
| **Forward diffusion** | Add Gaussian noise step by step in a fixed Markov chain. |
| **Closed-form sampling** | Jump straight to any noisy `x_t` without simulating every step. |
| **Reverse diffusion** | A neural network learns to predict and remove noise at each timestep. |
| **Training objective** | Mean squared error between predicted noise and true noise. |
| **Time conditioning** | The network needs the timestep to know how much noise is present. |
| **U-Net** | Encoder-decoder with skip connections; good for denoising across scales. |
| **DDPM sampling** | Stochastic, many steps, high quality. |
| **DDIM sampling** | Deterministic, fewer steps, much faster, same trained model. |
| **Classifier-free guidance** | Push the prediction toward the conditioned direction and away from the unconditional direction. |
| **Latent diffusion** | Run diffusion in a compressed latent space, then decode to pixels. |
| **Stable Diffusion** | Latent diffusion + text encoder + cross-attention = practical text-to-image generation. |

Key references:

- DDPM paper: [Ho et al., 2020](https://arxiv.org/pdf/2006.11239)
- DDIM paper: [Song et al., 2020](https://arxiv.org/abs/2010.02502)
- Stable Diffusion / latent diffusion paper: [Rombach et al., 2022](https://arxiv.org/abs/2112.10752)

Diffusion models bring the best of two worlds together: the probabilistic grounding of likelihood-based models and the high perceptual quality once associated mainly with GANs. They are the engine behind most modern text-to-image, image-editing, and video-generation systems.

**Next up:** how text, images, and other modalities are aligned so prompts can steer generation — [Part 19: Multimodal Models and Vision Transformers]({{ site.baseurl }}/topics/dl-genai-multimodal-models/).