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
  - vlm
  - cross-attention
  - alignment
  - generative-models
  - hands-on
  - beginners
  - friendly
summary: "A beginner-friendly guide to multimodal AI: how conditioning turns generation into p(x|c), why prompts are sensitive, how CLIP aligns images and text in a shared space, and how Vision-Language Models fuse vision and language for grounded reasoning."
---

# Deep Learning for Generative AI — Part 19: Multimodal Models and Vision Transformers

By [Part 18]({{ site.baseurl }}/topics/dl-genai-diffusion-models/) we had a powerful generator: start from noise, denoise step by step, and produce a realistic image. But a generator that only produces random images is only half useful. The real power comes when the model listens to a prompt, an image, a layout, or several signals at once.

This part is about two connected ideas:

1. **Conditioning** — how a generative model uses an external signal to guide its output.
2. **Multimodal alignment** — how text, images, and other data are placed into a shared geometric space so they can be compared, searched, and combined.

---

## 1. From unconditional to conditional generation

An unconditional model learns `p(x)`: “what does this kind of data look like?” A conditional model learns `p(x | c)`: “what does this kind of data look like, given this condition?”

```text
Unconditional:  z  →  Generator  →  random face
Conditional:  z + "a smiling child with a red hat"  →  Generator  →  matching image
```

The condition `c` can be:

- a text prompt,
- another image,
- a class label,
- a sketch or segmentation map,
- multiple signals combined.

The generator still produces data, but its path is steered by `c`.

---

## 2. How conditioning is injected

In modern systems the actual generation usually happens in a **latent space**, not in raw pixels. Conditioning is injected into that latent space so the external signal influences every refinement step.

### Step 1: encode the condition

A text prompt, for example, is turned into embeddings by a Transformer-based text encoder. The output can be:

- a **pooled sentence embedding** that captures the whole prompt, or
- a sequence of **token-level embeddings** that carry word-by-word meaning.

### Step 2: inject it into the generator

The most common mechanism is **cross-attention**:

```text
Image features  →  queries
Text embeddings →  keys + values

At each image location, the model asks: "which words are relevant here?"
```

This is the same cross-attention idea used in machine-translation decoders, but here one side is an image and the other side is text.

### Step 3: balance guidance and diversity

**Classifier-free guidance** lets us control how strictly the model follows the prompt. In diffusion models, it mixes a conditional prediction with an unconditional one:

```text
guided_noise = unconditional_noise + scale × (conditional_noise - unconditional_noise)
```

A larger `scale` makes the output more faithful to the prompt but can reduce variety.

---

## 3. Prompts are soft constraints, not orders

Conditioning gives control, but it is not as precise as a programming language.

### Prompt sensitivity

Generative models attend to individual tokens, not a single “meaning” of the sentence. Changing the wording, order, or emphasis changes the attention weights at every denoising step, so the final image shifts too.

```text
"a red car on a road"  →  emphasises "red" and "car"
"a car on a red road"  →  might put the redness on the road instead
```

### Ambiguity

If a prompt can mean several things, the model picks the most statistically common interpretation from its training data, which may not be the one you intended.

### Bias

The training data contains human stereotypes. Prompts like “a nurse” or “a CEO” may produce skewed demographics because the model learned those patterns from the internet.

### Compositionality

Models are good at individual concepts but weaker at combining many precise constraints:

```text
"three red spheres and two blue cubes, left to right"
```

Counting, exact spatial relationships, and multi-attribute binding remain hard because cross-attention distributes influence statistically rather than enforcing symbolic rules.

Understanding these limits matters in practice: prompts are a way of steering probability, not writing code.

---

## 4. Multimodal alignment: putting different worlds on the same map

Before vision and language can guide each other, they must be made comparable. Multimodal alignment places image and text representations into a **shared embedding space**.

```text
image of a dog  ──┐
                ├→  close together in embedding space
"a dog running" ──┘
```

In this space, **similarity is geometric**. You can measure distance, rank results, and even do arithmetic.

### Alignment is not equivalence

This is a crucial distinction.

- **Alignment** means related concepts are near each other.
- **Equivalence** would mean an image and its caption carry exactly the same information — they do not.

An image contains colour, texture, viewpoint, and background details that the caption may never mention. A caption contains abstract relationships and intentions that are not visible. Each modality compresses the world differently, so aligned embeddings are compatible, not identical.

### Explicit vs implicit alignment

| Type | How it is learned | Example |
|---|---|---|
| **Explicit alignment** | Directly optimise similarity between paired image–text samples. | CLIP |
| **Implicit alignment** | Correspondence emerges while solving another task, such as image captioning or text-to-image generation. | Stable Diffusion cross-attention |

Explicit alignment gives you a clean similarity score. Implicit alignment shapes behaviour without necessarily producing a shared comparison space.

---

## 5. Why image and text embeddings diverge

Even after alignment, the two encoders see different things:

- **Image encoder:** pixels, edges, colours, shapes, spatial layout.
- **Text encoder:** tokens, grammar, abstract concepts, relationships.

This creates several bottlenecks:

- **Global alignment.** Most contrastive objectives match whole images with whole captions. They do not learn which part of the image corresponds to which word.
- **Different omissions.** An image may show a sunset in the background; the caption might not mention it. A caption might say “happy family”; the image cannot directly show “happy.”
- **Dataset biases.** Visual style, lighting, and camera viewpoint affect image embeddings. Linguistic frequency and phrasing affect text embeddings.

These divergences mean retrieval and generation can produce matches that are semantically close but not exactly what you wanted.

---

## 6. CLIP: explicit alignment in practice

CLIP (Contrastive Language–Image Pre-training) is the classic explicit alignment model. It has two separate encoders:

- an **image encoder** (Vision Transformer or ResNet),
- a **text encoder** (Transformer language model).

Both produce vectors in the same space. During training, true image–caption pairs are pulled together and mismatched pairs are pushed apart.

```text
image ──image encoder──→ embedding ──┐
                                     ├→ cosine similarity
"a photo of a cat" ──text encoder──→ embedding ──┘
```

CLIP is not generative. It compares. But because it can compare, it enables:

- **zero-shot classification** — no task-specific training needed,
- **cross-modal retrieval** — find images for a caption or captions for an image,
- **prompt-based scoring** — rate how well a generated image matches a prompt.

### A hands-on CLIP zero-shot example

```python
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

image = Image.open("cat.jpg")
labels = ["a cat", "a dog", "a car", "a bowl of fruit"]

inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
outputs = model(**inputs)

probs = outputs.logits_per_image.softmax(dim=1)
for label, p in zip(labels, probs[0]):
    print(f"{label}: {p:.2%}")
```

The model never saw a “cat vs dog” classifier. It simply measures geometric distance between the image and each text description in the shared CLIP space, then turns those distances into probabilities.

CLIP paper: [Radford et al., 2021](https://arxiv.org/abs/2103.00020)

---

## 7. Vision-Language Models: beyond alignment to reasoning

CLIP aligns whole images with whole captions. Vision-Language Models (VLMs) go further: they allow **token-level interaction** between vision and language, which is needed for tasks like visual question answering, image captioning, and multimodal instruction following.

A typical VLM has three pieces:

1. **Vision encoder** — converts the image into visual tokens (often a Vision Transformer).
2. **Language backbone** — a large language model that reasons with text.
3. **Fusion mechanism** — how visual and text tokens talk to each other.

### Fusion mechanisms

| Mechanism | How it works |
|---|---|
| **Cross-attention** | Text tokens query visual tokens, attending to relevant image regions. |
| **Prefix / token injection** | Visual embeddings are projected and inserted into the language model’s input sequence as extra tokens. |
| **Unified multimodal transformer** | Visual and text tokens are concatenated into one sequence and processed by shared self-attention layers. |

### Fusion depth

| Depth | When fusion happens | Effect |
|---|---|---|
| **Early fusion** | From the first layers; modalities share a single sequence. | Strongest grounding, but computationally expensive. |
| **Intermediate fusion** | Each modality is encoded separately at low levels, then merged at chosen layers. | Balance between efficiency and interaction. |
| **Late fusion** | Streams stay separate until final scoring or generation. | Cheapest, but weaker cross-modal reasoning. |

### Training objectives

VLMs are trained with more than contrastive alignment:

- **Image-text matching:** predict whether an image and caption belong together.
- **Masked multimodal modelling:** predict missing visual or text tokens.
- **Generative captioning:** produce a caption given an image.
- **Instruction tuning:** follow multimodal instructions with human feedback.

These objectives force the model to actually **use visual evidence** when producing language, not just rely on text priors.

---

## 8. Vision Transformers: images as token sequences

Many of these systems use a **Vision Transformer (ViT)** as the image encoder. Instead of convolutions, a ViT splits the image into patches and treats each patch as a token.

```text
224 × 224 image
patch size 16 × 16
→ 14 × 14 = 196 patch tokens
→ each patch flattened and embedded
→ add a [CLASS] token and position embeddings
→ run a standard Transformer encoder
```

This unifies the building blocks of language and vision. Once images are tokens, the same attention machinery from Parts 6–10 can process them, making multimodal fusion much simpler.

---

## 9. Putting it together: a modern text-to-image system

A system like Stable Diffusion combines many ideas from this module:

| Component | From | Job |
|---|---|---|
| Text encoder | CLIP-style training | Turn the prompt into a steering vector. |
| Image autoencoder | VAE-style | Compress images into a latent space. |
| Diffusion U-Net | Diffusion models | Denoise in latent space. |
| Cross-attention | VLMs / Transformers | Let image regions attend to text tokens. |
| Classifier-free guidance | Conditional diffusion | Strengthen or loosen prompt adherence. |
| Vision Transformer | ViT | Encode images for understanding tasks. |

The result: type a sentence, and the model generates a brand-new image matching that sentence.

---

## 10. Summary

| Concept | One-sentence takeaway |
|---|---|
| **Conditional generation** | Learn `p(x \| c)` instead of `p(x)`, where `c` can be text, images, labels, or layouts. |
| **Cross-attention** | Image features ask text embeddings which words matter at each location. |
| **Prompt sensitivity** | Small wording changes alter token-level attention and the final output. |
| **Bias & ambiguity** | Models inherit training-data stereotypes and resolve ambiguous prompts statistically. |
| **Compositionality limits** | Cross-attention steers generation but cannot enforce precise symbolic rules. |
| **Multimodal alignment** | Place images and text in a shared embedding space so related concepts are close. |
| **Alignment ≠ equivalence** | Images and captions compress the world differently; they can be compatible without being identical. |
| **CLIP** | Dual-encoder contrastive model for explicit image–text alignment and zero-shot tasks. |
| **VLMs** | Allow token-level vision–language interaction for reasoning, captioning, and instruction following. |
| **Fusion depth** | Early, intermediate, or late fusion trades off grounding strength and computation. |
| **Vision Transformer** | Treat image patches as tokens so the same Transformer blocks handle vision and language. |

Multimodal systems are not one model; they are a stack of aligned representations, conditioning mechanisms, and fusion strategies. They connect the generative models from earlier parts with the real world of text, images, and other modalities.

This completes the core **Multimodal Generative Architectures** track. Next, see how the same ideas are implemented in code by building a Vision Transformer from scratch and running a pre-trained ViT in [Part 20: Vision Transformers in Code (Hands-On)]({{ site.baseurl }}/topics/dl-genai-vision-transformers-code/). After that, the [LangChain / LLM Application Development]({{ site.baseurl }}/categories/generative-ai/) series covers prompts, chains, retrieval, agents, and observability.