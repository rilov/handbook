---
layout: topic
title: "Deep Learning for Generative AI — Part 19: Multimodal Models and Vision Transformers"
category: Generative AI
order: 119
permalink: /topics/dl-genai-multimodal-models/
tags:
  - generative-ai
  - deep-learning
  - multimodal
  - clip
  - vision-transformer
  - cross-attention
  - generative-models
  - hands-on
  - beginners
  - friendly
summary: "How text and images are aligned in a shared embedding space, how prompts guide generative models, and how Vision Transformers turn images into sequences of patch tokens."
---

# Deep Learning for Generative AI — Part 19: Multimodal Models and Vision Transformers

Generative models are no longer limited to one modality. Systems like Stable Diffusion, DALL-E, and GPT-4o can read a prompt, look at an image, or listen to audio, and produce a response that mixes these sources. This is possible because different kinds of data are mapped into a **shared geometric space**.

---

## 1. The core idea: one space, many modalities

A multimodal model learns a single embedding space where:

- an image of a cat,
- the sentence "a cat sitting on a chair", and
- perhaps the sound of a meow

all live near each other.

```text
cat image        ← close in the shared embedding space →   "cat sitting on a chair"
        ↑                                                        ↑
   image encoder                                          text encoder
```

Once this alignment exists, you can:

- search images with text,
- generate images from text prompts,
- answer questions about images,
- guide a diffusion model by pulling its latent codes toward the text direction.

---

## 2. CLIP: learning image-text alignment

CLIP (Contrastive Language-Image Pre-training) was one of the first broadly successful alignment models. It is trained on millions of image-caption pairs with a contrastive loss:

- The image encoder and text encoder each produce an embedding.
- For a matching pair, the embeddings are pulled together.
- For a non-matching pair, the embeddings are pushed apart.

After training, CLIP can do **zero-shot classification**: give it an image and a list of candidate labels written as sentences, rank which text embedding is closest to the image embedding, and pick the best one — with no task-specific training.

### A hands-on CLIP sketch

```python
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

image = Image.open("cat.jpg")
candidates = ["a cat", "a dog", "a car", "a bowl of fruit"]

inputs = processor(text=candidates, images=image, return_tensors="pt", padding=True)
outputs = model(**inputs)

logits_per_image = outputs.logits_per_image
probs = logits_per_image.softmax(dim=1)

for label, p in zip(candidates, probs[0]):
    print(f"{label}: {p:.2%}")
```

The model never saw a “cat vs dog” classifier head. It simply measures geometric distance between the image and each text description in the shared space.

---

## 3. Prompts as steering vectors

In text-to-image generation, a prompt is not a rigid instruction. It is converted into an embedding that acts as a **direction** in latent space.

```text
"a raccoon wearing an astronaut helmet"
        ↓
   text encoder  →  text embedding
        ↓
   diffusion U-Net pulls the denoising path toward this embedding
```

The diffusion model still starts from random noise, but each denoising step is biased by the prompt embedding. Negative prompts work the same way: they push generation away from unwanted concepts.

Because text and images share a space, you can also do arithmetic:

```text
"king" - "man" + "woman"  ≈  "queen"      (in text embeddings)
"photo of a forest in autumn" + "snowy"  ≈  "photo of a forest in winter"
```

The model did not learn these rules explicitly. It learned a geometry where related concepts cluster and meaningful directions exist.

---

## 4. Cross-attention: where modalities meet

How does a text prompt influence an image model? Usually through **cross-attention** inside the diffusion U-Net.

In self-attention, each token attends to every other token in the same sequence. In cross-attention, tokens from one modality attend to tokens from another:

```text
image patch tokens  ──cross-attention──→  text token embeddings
       ↓                                           ↓
   "this region                     "what should appear here?"
    should contain..."
```

Each region of the image model can query the prompt and update its own representation based on what the text says. This is the same mechanism that lets a Transformer decoder attend to encoder outputs in machine translation.

---

## 5. Vision Transformers: images as patch sequences

Before Vision Transformers (ViTs), the standard way to process images was with convolutional neural networks. ViTs instead cut an image into patches and treat the patches as a sequence of tokens — exactly like words in a sentence.

```text
Image:        224 × 224 pixels
Patch size:   16 × 16
Number of patches:  (224 / 16)² = 196

image  →  196 patch embeddings  +  [CLASS] token  +  position embeddings
              ↓
          Transformer encoder
              ↓
         image representation
```

Each patch is flattened and projected to an embedding vector. A special `[CLASS]` token is added for classification tasks, and position embeddings tell the model where each patch was in the original image.

After that, the same Transformer encoder from Parts 6–8 runs self-attention over the patches. No convolutions. Just attention, layer by layer.

### Why this matters

- It proves the Transformer architecture from NLP generalises directly to vision.
- It unifies the building blocks of language and vision models, making multimodal training simpler.
- It scales well with data and model size, which is why large vision-language models often use ViT backbones.

---

## 6. Putting it together: a multimodal generation stack

A modern text-to-image system like Stable Diffusion combines several ideas from this module:

| Component | From | Job |
|---|---|---|
| Text encoder | CLIP-style training | Turn the prompt into a steering vector |
| Image autoencoder | VAE-style | Compress images into a latent space |
| Diffusion U-Net | Diffusion models | Denoise in latent space, guided by text |
| Cross-attention | Transformer decoder | Let image regions attend to text tokens |
| Vision Transformer | ViT | Encode images for understanding tasks |

The result: type a sentence, and the model generates a brand-new image that matches the sentence.

---

## 7. Summary

- Multimodal models place text, images, and other data into a **shared embedding space** so they can be compared, searched, and combined.
- **CLIP** learns this alignment with a contrastive loss on image-caption pairs, enabling zero-shot image classification.
- **Prompts** are not commands — they are vectors that steer generation in latent space.
- **Cross-attention** lets a model in one modality query another, which is how image regions attend to text during generation.
- **Vision Transformers** treat image patches as tokens, unifying the architecture of language and vision models.

Generative models are converging on a small set of shared ideas: attention, latent spaces, probability, and alignment across modalities. The parts in this module — VAEs, GANs, diffusion, and multimodal alignment — are the tools that make modern text-to-image, image-to-text, and multimodal chat systems possible.

**This concludes the Generative AI model-building track.** For the practical side of building applications with these models — prompts, chains, retrieval, agents, and observability — see the [LangChain / LLM Application Development]({{ site.baseurl }}/categories/generative-ai/) series.