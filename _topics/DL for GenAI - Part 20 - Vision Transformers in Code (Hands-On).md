---
layout: topic
title: "Deep Learning for Generative AI — Part 20: Vision Transformers in Code (Hands-On)"
category: Generative AI
order: 120
permalink: /topics/dl-genai-vision-transformers-code/
tags:
  - generative-ai
  - deep-learning
  - vision-transformer
  - vit
  - tensorflow
  - hugging-face
  - hands-on
  - beginners
  - friendly
summary: "A hands-on walkthrough of Vision Transformers: build the patch extraction, encoding, transformer block, and full ViT classifier in TensorFlow/Keras, then run a pre-trained ViT from Hugging Face for zero-setup image classification."
---

# Deep Learning for Generative AI — Part 20: Vision Transformers in Code (Hands-On)

[Part 19]({{ site.baseurl }}/topics/dl-genai-multimodal-models/) explained the idea: a Vision Transformer (ViT) turns an image into a sequence of patch tokens and processes them with a standard Transformer encoder. This part puts that idea into code.

We will build a small ViT from scratch in TensorFlow/Keras to see how every block works, then use Google’s pre-trained ViT from Hugging Face for real-world inference.

---

## 1. What we are building

For an input image of size `224 × 224 × 3` and patch size `16 × 16`:

```text
224 × 224 image
→ split into 16 × 16 patches
→ 14 × 14 = 196 patches
→ flatten each patch: 16 × 16 × 3 = 768 numbers
→ add 1 class (CLS) token
→ 197 tokens of 768 dimensions each
→ run through Transformer encoder layers
→ classify using the pooled representation
```

The pipeline is exactly the same as a language Transformer, except the input tokens come from image patches instead of words.

---

## 2. Building a ViT from scratch in TensorFlow/Keras

The model has four custom pieces:

1. `PatchExtractor` — cuts the image into patches.
2. `PatchEncoder` — projects patches to vectors, adds a class token, and adds positional embeddings.
3. `TransformerBlock` — self-attention + feed-forward network with residual connections.
4. `TransformerEncoder` — a stack of Transformer blocks.

### Patch extraction

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class PatchExtractor(layers.Layer):
    def __init__(self, patch_size=16):
        super().__init__()
        self.patch_size = patch_size

    def call(self, images):
        batch_size = tf.shape(images)[0]
        patches = tf.image.extract_patches(
            images=images,
            sizes=[1, self.patch_size, self.patch_size, 1],
            strides=[1, self.patch_size, self.patch_size, 1],
            rates=[1, 1, 1, 1],
            padding="VALID",
        )
        patch_dims = patches.shape[-1]
        patches = tf.reshape(patches, [batch_size, -1, patch_dims])
        return patches
```

For a `224 × 224 × 3` image with `16 × 16` patches, this returns a tensor of shape `(batch_size, 196, 768)`.

### Patch encoding

```python
class PatchEncoder(layers.Layer):
    def __init__(self, num_patches=196, projection_dim=768):
        super().__init__()
        self.num_patches = num_patches
        self.projection = layers.Dense(projection_dim)

        # learnable class token
        w_init = tf.random_normal_initializer()
        self.class_token = tf.Variable(
            initial_value=w_init(shape=(1, projection_dim), dtype="float32"),
            trainable=True,
            name="class_token",
        )

        # learnable positional embeddings
        self.position_embedding = layers.Embedding(
            input_dim=num_patches + 1, output_dim=projection_dim
        )

    def call(self, patches):
        batch_size = tf.shape(patches)[0]

        # project patches
        patches_embed = self.projection(patches)  # (batch, 196, dim)

        # prepend the class token to every sample in the batch
        class_tokens = tf.tile(self.class_token, [batch_size, 1])
        class_tokens = tf.reshape(class_tokens, [batch_size, 1, -1])
        patches_embed = tf.concat([class_tokens, patches_embed], axis=1)

        # add positional embeddings
        positions = tf.range(start=0, limit=self.num_patches + 1, delta=1)
        positions_embed = self.position_embedding(positions)
        encoded = patches_embed + positions_embed

        return encoded
```

The output has shape `(batch_size, 197, 768)`: one class token plus 196 patch tokens.

### MLP and Transformer block

```python
class MLP(layers.Layer):
    def __init__(self, hidden_features, out_features, dropout_rate=0.1):
        super().__init__()
        self.dense1 = layers.Dense(hidden_features, activation=tf.nn.gelu)
        self.dense2 = layers.Dense(out_features)
        self.dropout = layers.Dropout(dropout_rate)

    def call(self, x):
        x = self.dense1(x)
        x = self.dropout(x)
        x = self.dense2(x)
        return self.dropout(x)


class TransformerBlock(layers.Layer):
    def __init__(self, projection_dim, num_heads=8, dropout_rate=0.1):
        super().__init__()
        self.norm1 = layers.LayerNormalization(epsilon=1e-6)
        self.attn = layers.MultiHeadAttention(
            num_heads=num_heads,
            key_dim=projection_dim // num_heads,
            dropout=dropout_rate,
        )
        self.norm2 = layers.LayerNormalization(epsilon=1e-6)
        self.mlp = MLP(projection_dim * 2, projection_dim, dropout_rate)

    def call(self, x):
        x1 = self.norm1(x)
        attn_output = self.attn(x1, x1)  # self-attention
        x2 = layers.Add()([attn_output, x])
        x3 = self.norm2(x2)
        x3 = self.mlp(x3)
        return layers.Add()([x3, x2])
```

Each block is the same pattern used in language Transformers: normalise, attend, add a residual, normalise again, apply an MLP, add another residual.

### Transformer encoder and full ViT

```python
class TransformerEncoder(layers.Layer):
    def __init__(self, projection_dim, num_heads=8, num_blocks=12, dropout_rate=0.1):
        super().__init__()
        self.blocks = [
            TransformerBlock(projection_dim, num_heads, dropout_rate)
            for _ in range(num_blocks)
        ]
        self.norm = layers.LayerNormalization(epsilon=1e-6)

    def call(self, x):
        for block in self.blocks:
            x = block(x)
        return self.norm(x)


def create_vit(
    num_classes,
    num_patches=196,
    projection_dim=768,
    num_heads=8,
    num_blocks=12,
    input_shape=(224, 224, 3),
):
    inputs = keras.Input(shape=input_shape)

    patches = PatchExtractor()(inputs)
    encoded = PatchEncoder(num_patches, projection_dim)(patches)
    representation = TransformerEncoder(
        projection_dim, num_heads, num_blocks
    )(encoded)
    representation = layers.GlobalAveragePooling1D()(representation)
    logits = MLP(projection_dim, num_classes, dropout_rate=0.5)(representation)

    return keras.Model(inputs=inputs, outputs=logits)
```

You can create the model without training it just to inspect the architecture:

```python
vit = create_vit(num_classes=10, num_blocks=4)
vit.summary()
```

Training a full ViT from scratch on ImageNet requires large data and compute. In practice, most people use a pre-trained ViT and fine-tune it.

---

## 3. Visualising patches

Here is a quick way to see what the `PatchExtractor` is doing. The example uses a dog image instead of a flower, so it does not copy the original transcript.

```python
import matplotlib.pyplot as plt
import numpy as np

# Download a small demo image
url = "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=224&q=80"
image_path = keras.utils.get_file("demo_dog.jpg", url)
image = plt.imread(image_path)
image = tf.image.resize(tf.convert_to_tensor(image), size=(224, 224))

batch = tf.expand_dims(image, axis=0)
patches = PatchExtractor()(batch)
print(patches.shape)  # (1, 196, 768)

# Plot the 14 x 14 grid of patches
n = int(np.sqrt(patches.shape[1]))
fig, axes = plt.subplots(n, n, figsize=(8, 8))
for i, ax in enumerate(axes.flat):
    patch_img = tf.reshape(patches[0, i], (16, 16, 3))
    ax.imshow(patch_img.numpy().astype("uint8"))
    ax.axis("off")
plt.show()
```

You will see 196 tiny squares, each a `16 × 16` region of the original image. The Transformer processes these squares as if they were words in a sentence.

---

## 4. Using a pre-trained ViT from Hugging Face

Training a ViT from scratch is expensive. Google released `google/vit-base-patch16-224`, pre-trained on ImageNet-21k, which you can use immediately for image classification.

This example uses a different image from the original transcript:

```python
import torch
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import requests

model_name = "google/vit-base-patch16-224"
model = ViTForImageClassification.from_pretrained(model_name)
processor = ViTImageProcessor.from_pretrained(model_name)

# Use a dog image from Unsplash instead of the COCO cat image
url = "https://images.unsplash.com/photo-1587300003388-5920800f913a?auto=format&fit=crop&w=224&q=80"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)

predicted_class_idx = outputs.logits.argmax(-1).item()
print("Predicted class:", model.config.id2label[predicted_class_idx])
```

`google/vit-base-patch16-224` expects `224 × 224` inputs and splits them into `16 × 16` patches — exactly the setup we built from scratch. The difference is that the weights were learned from 14 million images.

Model card: <https://huggingface.co/google/vit-base-patch16-224>

---

## 5. ViT vs CNN: a practical note

As you saw in the original discussion, ViTs are data-hungry:

- On small datasets like ImageNet-1k from scratch, a CNN is usually better.
- On very large datasets like ImageNet-21k or JFT-300M, ViTs match or beat CNNs.
- In practice, the easiest way to use a ViT is to fine-tune a pre-trained checkpoint on your own task, rather than training from scratch.

---

## 6. Summary

| Component | What it does |
|---|---|
| **PatchExtractor** | Splits an image into non-overlapping patches. |
| **PatchEncoder** | Projects patches to vectors, prepends a class token, and adds positional embeddings. |
| **TransformerBlock** | Self-attention + MLP with layer normalisation and residuals. |
| **TransformerEncoder** | Stacks many Transformer blocks. |
| **MLP head** | Converts the pooled representation into class logits. |
| **Pre-trained ViT** | Use Google's checkpoint via Hugging Face for real tasks. |

Key references:

- ViT paper: [An Image is Worth 16x16 Words (Dosovitskiy et al., 2020)](https://arxiv.org/abs/2010.11929)
- Pre-trained model: <https://huggingface.co/google/vit-base-patch16-224>

This concludes the model-building part of the Multimodal Generative Architectures track. From here, you can apply these building blocks to your own images, fine-tune pre-trained vision models, or connect them with language models for multimodal applications.

**Next up:** for the practical side of building generative applications — prompts, chains, retrieval, agents, and observability — see the [LangChain / LLM Application Development]({{ site.baseurl }}/categories/generative-ai/) series.