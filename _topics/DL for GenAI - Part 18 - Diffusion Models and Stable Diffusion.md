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
  - beginners
  - friendly
summary: "How diffusion models learn generation by reversing a gradual noising process, and how Stable Diffusion scales the idea with latent spaces, time conditioning, and text guidance."
---

# Deep Learning for Generative AI — Part 18: Diffusion Models and Stable Diffusion

VAEs learn a latent distribution and sample from it. GANs train a generator by pitting it against a critic. Diffusion models take a third path: they learn to **undo noise**, one small step at a time.

This approach has become the foundation of modern image generation systems such as Stable Diffusion, DALL-E 2/3, and Imagen.

---

## 1. The big picture: destruction and reconstruction

Imagine taking a photograph and adding a little Gaussian noise. Then adding a little more. Then more. After enough steps, the image becomes pure static — mathematically close to Gaussian noise.

A diffusion model learns the reverse: given a noisy image at step `t`, predict the noise that was added. If it can do that reliably, it can start from pure noise and remove noise step by step until a clear image emerges.

```text
real image  →  noisy image  →  noisier image  →  ...  →  pure noise
     ↑            ↑              ↑                           ↑
     └── model learns to walk backwards ────────────────────┘
```

Generation is therefore an iterative denoising process.

---

## 2. Forward process: add noise in fixed steps

The forward process is predefined. At each step we add a small amount of Gaussian noise. Because each step is simple and known, we can jump directly from a clean image to a heavily noised version without simulating every intermediate step.

```text
x_0  →  x_1  →  x_2  →  ...  →  x_T
```

- `x_0` is the original image.
- `x_T` is nearly pure Gaussian noise.
- The schedule of noise levels is fixed before training.

There is nothing to learn in the forward direction; it is just a recipe for corrupting data.

---

## 3. Reverse process: a neural network learns to denoise

The model is a neural network — usually a U-Net — that takes two inputs:

1. The noisy image at step `t`.
2. The timestep `t` itself (encoded as an embedding).

Its job is to predict the noise, or equivalently the slightly cleaner image. The timestep tells the network how far along the corruption process it is, so the same network can handle every level of noise.

```text
input:  noisy image at step t  +  t
        ↓
    neural network (U-Net)
        ↓
output: predicted noise
```

Training is surprisingly simple: take a clean image, add noise at a random timestep, ask the network to predict the noise, and minimise the mean squared error between predicted and actual noise.

---

## 4. Sampling: start from noise and walk backwards

To generate a new image:

```text
x_T  ~  pure Gaussian noise
repeat:
    x_{t-1}  =  denoise(x_t, t)
until x_0 is a clean image
```

Each step removes a small amount of noise. After many steps — typically 20 to 1000, depending on the sampler — the result is a plausible new image.

The randomness in the initial noise means each run produces a different sample.

---

## 5. Why diffusion works well

| Advantage | Why it matters |
|---|---|
| **Stable training** | There is no adversarial game; the loss is a simple supervised regression on noise. |
| **Strong likelihood** | The model can be written as a proper probabilistic model, so likelihoods and probabilities make sense. |
| **Mode coverage** | Unlike GANs, diffusion models tend to cover many modes of the data distribution rather than collapsing. |
| **Iterative refinement** | Each step is small and local, so the model can fix mistakes gradually. |
| **Conditioning is natural** | Class labels, text prompts, or images can be fed into the U-Net alongside the noisy input. |

The main downside is speed: generating one sample requires many forward passes. Much recent research — improved samplers, consistency models, and distillation — is aimed at reducing that cost.

---

## 6. Classifier-free guidance: making the prompt stick

Text-to-image models need the generated image to match a prompt. They use a technique called **classifier-free guidance**.

During training, the model sometimes sees a text prompt and sometimes sees no prompt (or an empty prompt). It learns to denoise both with and without conditioning.

At generation time, the model is pushed away from the unconditioned prediction and toward the conditioned prediction:

```text
guided prediction = unconditioned prediction
                    + guidance_scale × (conditioned prediction - unconditioned prediction)
```

A higher `guidance_scale` makes the output follow the prompt more strongly. Too high and the image becomes oversaturated or repetitive; too low and the prompt is ignored.

---

## 7. Stable Diffusion and latent diffusion

Raw images are huge. Running a diffusion model directly on a 512×512 RGB image would be very expensive. **Stable Diffusion** solves this by applying diffusion in a **latent space** instead of pixel space.

The recipe is:

1. Use a pre-trained autoencoder to compress the image into a much smaller latent tensor.
2. Train the diffusion model to denoise in this compressed space.
3. Decode the final latent tensor back into an image with the autoencoder's decoder.

```text
text prompt  →  text encoder  →  conditioning
                                ↓
noise in latent space  →  U-Net denoiser (many steps)  →  clean latent
                                                            ↓
                                                     decoder  →  image
```

This is called a **latent diffusion model (LDM)**. It is the architecture behind Stable Diffusion. The diffusion U-Net still operates step by step, but each step is much cheaper because it works on a compact representation.

---

## 8. Summary

- Diffusion models learn to reverse a fixed noising process.
- Training predicts noise at random timesteps; sampling starts from pure noise and denoises step by step.
- Time conditioning lets one network handle every level of noise.
- **Classifier-free guidance** pushes generation toward a text prompt or other condition.
- **Latent diffusion** runs diffusion in a compressed space so high-resolution generation becomes practical.

Diffusion models combine many of the strengths of VAEs (a structured latent space) and GANs (high-quality samples) while avoiding the adversarial training instability. That is why they now dominate image, video, and audio generation.

**Next up:** how text and images are aligned so that prompts can steer generation, and how Transformers can process images too — [Part 19: Multimodal Models and Vision Transformers]({{ site.baseurl }}/topics/dl-genai-multimodal-models/).