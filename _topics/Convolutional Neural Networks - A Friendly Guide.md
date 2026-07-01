---
title: "Part 9: Convolutional Neural Networks (CNNs) - A Friendly Guide"
category: Deep Learning
order: 9
tags:
  - deep-learning
  - cnn
  - computer-vision
  - convolution
  - pooling
  - feature-maps
  - image-classification
  - vgg16
  - beginners
  - friendly
summary: A zero-background introduction to Convolutional Neural Networks. Starts with a simple cat-vs-dog photo example and builds up, one idea at a time, through convolution, activation, feature maps, padding, and pooling — then goes further into the exact output-size and parameter-count formulas, finishing with a full layer-by-layer walkthrough of the real VGG16 architecture.
---

# Part 9: Convolutional Neural Networks (CNNs) — A Friendly Guide

Every earlier part of this series worked with a spam email turned into a short list of numbers — five features, one row. Images break that assumption. A single small photo is tens of thousands of numbers arranged in a grid, and *where* each number sits matters just as much as its value. This part starts from zero and builds up, one small idea at a time, to a real, working architecture: **VGG16**.

---

## 1. The problem: teaching a computer to recognize photos

Say you want to build something that looks at a photo and decides: "cat" or "dog." Easy for a person. Hard for a computer, because a computer never actually sees a cat — it sees a grid of numbers, one per pixel (or three per pixel for a color photo: one each for red, green, and blue brightness).

Your own visual system doesn't process a whole scene in one instant either. It works in stages:

| Stage | What it notices |
|---|---|
| Early | Simple edges, corners, contrast |
| Middle | Shapes and textures — curves, fur patterns |
| Later | Whole parts and objects — an ear, a whisker, a face |

A CNN is a computer program that copies this same layered idea: simple patterns first, combined into richer patterns, layer after layer, until the last layer can confidently say "cat."

<img src="{{ site.baseurl }}/assets/img/cnn-pipeline-overview.svg" alt="The CNN pipeline: photo, convolution, feature maps, pooling, flatten and dense, output" width="100%" />

> **Memory trick:** A CNN reads an image the way you read a page — letters first, then words, then sentences, then meaning.

---

## 2. Why a plain (fully connected) network struggles with images

Earlier in this series, a plain neural network worked fine on five hand-picked spam features. Why not just feed a photo's raw pixels into the same kind of network?

Two reasons that breaks down:

- **Parameter explosion.** A modest 224x224 color photo already has over 150,000 individual numbers. A fully connected layer would connect every single one of them to every neuron in the next layer — millions of weights before the network has learned anything at all.
- **No sense of "nearby."** A fully connected layer treats every pixel as a stranger to every other pixel. It has no built-in idea that the pixel at position (50, 50) and the pixel right next to it at (50, 51) are neighbors that jointly form part of an edge or a texture. It would have to rediscover that from scratch, purely from data — slow and wasteful.

<img src="{{ site.baseurl }}/assets/img/fc-vs-conv-connections.svg" alt="Side by side comparison: fully connected layer with dense mesh of connections versus a convolutional layer with a small local receptive field and shared weights" width="100%" />

A CNN's answer to both problems is the same trick: instead of connecting to the whole image, look at a small patch at a time, and reuse the same small set of weights everywhere in the picture. That trick is called **convolution**.

> **Memory trick:** Fully connected is "everyone talks to everyone." Convolutional is "a small window slides around, and the window's rules never change."

---

## 3. The convolution operation, step by step

Imagine standing in a dark room with a photo and a small flashlight. Instead of turning on the lights and seeing everything at once, you shine your flashlight on one small patch, note what you see, then slide it over, patch by patch, until you've covered the whole photo. That's a convolution: a small **kernel** (or **filter**) sliding across the image, checking each small **receptive field** for a specific pattern.

At every position, the kernel computes a **sum of products**: multiply each kernel weight by the pixel value underneath it, and add all the results into a single number.

<img src="{{ site.baseurl }}/assets/img/convolution-kernel-sliding.svg" alt="A 3x3 kernel scanning a 5x5 image, multiplying and summing values in the receptive field to produce one scalar in the feature map" width="100%" />

In the example above, a 3x3 kernel tuned to detect "dark on the left, light on the right" lines up with a patch of the image and produces a single scalar: `3`, a strong match. Slide the same kernel one step over, repeat the same multiply-and-add, and you get the next scalar — and so on, across the whole image, building up a full grid of output values called an **activation map** (or feature map).

In PyTorch, a single convolutional layer looks like this:

```python
import torch
import torch.nn as nn

# 1 input image, 3 color channels (RGB), 224x224 pixels
image = torch.randn(1, 3, 224, 224)

conv_layer = nn.Conv2d(
    in_channels=3,    # RGB input
    out_channels=64,  # 64 different filters/kernels
    kernel_size=3,    # each filter is 3x3
    padding=1,        # zero padding, explained in section 6
    stride=1
)

feature_maps = conv_layer(image)
print(feature_maps.shape)  # torch.Size([1, 64, 224, 224])
```

**One important detail:** for a color (RGB) image, a kernel isn't really 2D — it's 3D, matching the input's channel depth. A "3x3 kernel" over an RGB image is actually a 3x3x3 block of weights, and the sum-of-products at each position adds up all 27 multiplications into one scalar. No matter how many channels the input has, one kernel always produces one 2D feature map — if a layer uses many kernels (64 in the example above), you get one feature map per kernel, stacked together.

### Recap

| Term | Plain-English meaning |
|---|---|
| Kernel / Filter | A small pattern-detector, like a mini stencil |
| Receptive field | The small patch of the image the kernel is currently looking at |
| Sliding | Moving the kernel step by step across the whole image |
| Activation map / feature map | The full grid of output scalars produced by one kernel |

---

## 4. Activation functions: why we need ReLU

A convolution on its own is just a weighted sum — a linear operation. Stack any number of linear operations on top of each other and, mathematically, it's still just one big linear operation. That's not enough to learn genuinely complex patterns (edges combining into curves, curves into shapes, and so on).

So immediately after every convolution, an **activation function** is applied to every value in the feature map. The standard choice, used in VGG16 and almost every modern CNN, is **ReLU** (Rectified Linear Unit):

$$
\text{ReLU}(x) = \max(0, x)
$$

In words: keep positive values as they are, and clamp any negative value to zero.

```python
relu = nn.ReLU()
print(relu(torch.tensor([2.4, -0.7, 1.3])))
# tensor([2.4, 0.0, 1.3])
```

> **Memory trick:** ReLU is a bouncer at a club door — positive numbers walk straight through, negative numbers get turned away at zero.

---

## 5. Feature maps: what the computer "remembers"

Picture reading a long report with a yellow highlighter, marking every sentence about "budget." You don't memorize the whole report — you get a version showing exactly *where* the budget mentions are. A **feature map** is the CNN's version of that highlighted report: bright where a specific pattern was found, dark where it wasn't.

A real convolutional layer doesn't use just one kernel — it uses many (64 in the code example above, often hundreds in deeper layers), each hunting a different tiny pattern:

| This kernel hunts for... | Its feature map lights up where... |
|---|---|
| Vertical edges | Vertical lines appear in the photo |
| Horizontal edges | Horizontal lines appear |
| Orange blobs | Orange-colored regions appear (useful for, say, a cat's fur) |
| Rounded curves | Curved shapes appear (an ear, an eye) |

The *next* convolutional layer doesn't look at the raw photo anymore — it slides its own kernels across this whole stack of feature maps. This is how a CNN builds up from simple patterns (edges) to increasingly complex ones (fur texture, an ear shape, eventually a whole face), one layer at a time.

---

## 6. Padding: keeping control of the output size

Sliding a kernel across an image without any special handling shrinks the output slightly every time (the kernel can't center itself on the outermost pixels). **Padding** adds extra pixels around the border before convolving, to control that.

- **Zero padding** (the standard choice): surround the image with a border of zeros. This preserves the spatial size without inventing any real content — the padding carries no information.
- **Identity / replication padding**: repeats the edge pixels outward instead. Used less often, since it subtly introduces a duplicated pattern that wasn't really there.

VGG16 uses 1-pixel zero padding on every 3x3 convolution, specifically so the convolutions themselves never shrink the feature map — all of the shrinking in VGG16 comes from pooling (next section), not from convolution.

---

## 7. Pooling layers: shrinking while keeping the signal

Imagine condensing a detailed 500-word paragraph down to one punchy headline — you keep the single most important idea and drop the rest. That's what a **pooling layer** does to a feature map.

The most common version, **max pooling**, looks at small neighborhoods (2x2 is standard) and keeps only the highest number in each, discarding the rest:

<img src="{{ site.baseurl }}/assets/img/max-pooling-demo.svg" alt="A 4x4 feature map reduced to a 2x2 pooled map by taking the maximum value from each 2x2 block" width="100%" />

```python
pool_layer = nn.MaxPool2d(kernel_size=2, stride=2)

pooled = pool_layer(feature_maps)
print(pooled.shape)  # torch.Size([1, 64, 112, 112]) — half the width and height
```

Why shrink things on purpose?

- **Speed.** Fewer numbers to process in every layer that follows.
- **Tolerance to small shifts.** If a detected feature (an eye, an edge) moves slightly left or right in the photo, pooling makes it likely the same maximum value still gets picked up — the network cares that the feature was *roughly there*, not at one exact pixel.
- **Less memorizing.** Fewer numbers to track means the network is less likely to just memorize exact training photos instead of learning general patterns.

Pooling layers have no learnable weights and no bias term — they don't add anything to a CNN's parameter count.

---

## 8. From features to a decision: flatten + dense classifier

After several rounds of convolution, activation, and pooling, the CNN is holding a small stack of feature maps — think of it as a compact set of notes: "strong pointy-ear signal here," "strong whisker texture there." These notes are still shaped like small 2D grids. To make a final decision, the network needs all of this evidence side by side in one simple list.

**Flatten** unrolls every remaining feature map into one long 1D vector, with nothing lost — just rearranged:

```python
flatten = nn.Flatten()
flat_vector = flatten(pooled)  # shape: [1, 64*112*112]
```

A **dense (fully connected) layer** then acts like a detective laying every clue on the table and weighing them together — "strong ear signal, strong whisker signal, no snout signal... almost certainly a cat":

```python
classifier = nn.Sequential(
    nn.Linear(64 * 112 * 112, 128),
    nn.ReLU(),
    nn.Linear(128, 2),      # 2 classes: cat, dog
    nn.Softmax(dim=1)
)

output = classifier(flat_vector)
print(output)  # e.g. tensor([[0.92, 0.08]]) → 92% cat, 8% dog
```

**Softmax** turns the final raw scores into probabilities that sum to 1, and the highest-probability class becomes the network's answer.

---

## 9. Going further: the exact formulas

Everything so far has been intuition and worked examples. Now for the precise math behind every convolutional layer — useful once you start designing your own networks or reading someone else's architecture.

### Output size formula

Given an input of size $N \times N$, a kernel of size $F \times F$, padding $P$, and stride $S$ (how many pixels the kernel moves per step):

$$
\text{Output size} = \left\lfloor \frac{N - F + 2P}{S} \right\rfloor + 1
$$

**Worked example** — VGG16's standard conv layer: input $N=224$, kernel $F=3$, padding $P=1$, stride $S=1$:

$$
\frac{224 - 3 + 2(1)}{1} + 1 = \frac{223}{1} + 1 = 224
$$

Output stays 224x224 — exactly why VGG's convolutions never shrink the feature map on their own.

### Parameter count formula

$$
\text{Parameters} = (\text{filters}) \times (F \times F \times \text{channels}) + \text{filters}
$$

The final `+ filters` term is one learned bias value per filter.

**Worked example** — VGG16's first conv layer: 64 filters, 3x3, over a 3-channel input:

$$
64 \times (3 \times 3 \times 3) + 64 = 64 \times 27 + 64 = 1{,}728 + 64 = 1{,}792
$$

**A deeper layer** — 512 filters, 3x3, over a 512-channel input:

$$
512 \times (3 \times 3 \times 512) + 512 = 512 \times 4{,}608 + 512 = 2{,}359{,}808
$$

Notice how quickly this grows: the number of input channels directly multiplies the parameter count, which is why deep layers with many channels are far more expensive than shallow, early ones.

### Recap

| Concept | Formula |
|---|---|
| Output size | $\left\lfloor \dfrac{N-F+2P}{S} \right\rfloor + 1$ |
| Conv parameters | (filters) x (F x F x channels) + filters |
| Dense parameters | (inputs) x (outputs) + outputs |

---

## 10. A real architecture: the full VGG16 walkthrough

**VGG16** is one of the best-known CNNs, and a clean illustration of every idea above working together. It repeats the same building block — a few 3x3/stride-1/pad-1 convolutions, then one 2x2/stride-2 max-pool — five times, then finishes with three dense layers. Its 13 convolutional layers plus 3 dense layers give 16 learnable weight layers in total (hence "VGG16"); the 5 pooling layers have no weights and aren't counted.

<img src="{{ site.baseurl }}/assets/img/vgg16-architecture.svg" alt="VGG16 architecture diagram showing five convolutional blocks shrinking the spatial size from 224x224 down to 7x7 while growing channel depth, followed by flatten and three dense layers ending in a 1000-way softmax" width="100%" />

Every convolution below is 3x3/stride-1/pad-1 (so it never changes spatial size on its own); every pooling layer is 2x2/stride-2 (so it exactly halves width and height):

| # | Layer | Output shape | Parameters |
|---|---|---|---|
| 1 | Conv 3x3, 64 filters | 224 x 224 x 64 | 1,792 |
| 2 | Conv 3x3, 64 filters | 224 x 224 x 64 | 36,928 |
| — | MaxPool 2x2 | 112 x 112 x 64 | 0 |
| 3 | Conv 3x3, 128 filters | 112 x 112 x 128 | 73,856 |
| 4 | Conv 3x3, 128 filters | 112 x 112 x 128 | 147,584 |
| — | MaxPool 2x2 | 56 x 56 x 128 | 0 |
| 5 | Conv 3x3, 256 filters | 56 x 56 x 256 | 295,168 |
| 6 | Conv 3x3, 256 filters | 56 x 56 x 256 | 590,080 |
| 7 | Conv 3x3, 256 filters | 56 x 56 x 256 | 590,080 |
| — | MaxPool 2x2 | 28 x 28 x 256 | 0 |
| 8 | Conv 3x3, 512 filters | 28 x 28 x 512 | 1,180,160 |
| 9 | Conv 3x3, 512 filters | 28 x 28 x 512 | 2,359,808 |
| 10 | Conv 3x3, 512 filters | 28 x 28 x 512 | 2,359,808 |
| — | MaxPool 2x2 | 14 x 14 x 512 | 0 |
| 11 | Conv 3x3, 512 filters | 14 x 14 x 512 | 2,359,808 |
| 12 | Conv 3x3, 512 filters | 14 x 14 x 512 | 2,359,808 |
| 13 | Conv 3x3, 512 filters | 14 x 14 x 512 | 2,359,808 |
| — | MaxPool 2x2 | 7 x 7 x 512 | 0 |
| — | Flatten | 25,088 | 0 |
| 14 | Dense | 4,096 | 102,764,544 |
| 15 | Dense | 4,096 | 16,781,312 |
| 16 | Dense + Softmax | 1,000 | 4,097,000 |
| | **Total** | | **138,357,544** |

Two things stand out:

- **Convolutions are cheap, dense layers are expensive.** All 13 convolutional layers together account for roughly 14.7 million parameters — about 10% of the network. The 3 dense layers hold the remaining ~90%, because dense layers connect *every* input to *every* output with no weight sharing, unlike convolutions, which reuse the same small kernel everywhere.
- **Spatial size only changes at pooling layers.** Every convolution preserves width and height exactly, thanks to its zero padding; only the five max-pool layers actually shrink the feature map, each time cutting both dimensions in half.

---

## 11. Try it yourself: a mini CNN in PyTorch

Here's a small, runnable CNN that follows the exact same pattern as VGG16 — just far smaller — to classify tiny 32x32 images into 2 classes:

```python
import torch
import torch.nn as nn

class MiniCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2, 2),                          # 32x32 → 16x16
            nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2, 2),                          # 16x16 → 8x8
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 8 * 8, 64), nn.ReLU(),
            nn.Linear(64, 2),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

model = MiniCNN()
image = torch.randn(1, 3, 32, 32)   # 1 fake RGB image
prediction = model(image)
print(prediction)  # e.g. tensor([[0.63, 0.37]])
```

Swap in real cat and dog photos, train it with a loss function and optimizer exactly like the earlier parts in this series, and this same skeleton scales all the way up to VGG16.

---

## 12. Summary

- A CNN exists because plain fully connected networks don't scale to images: too many parameters, and no built-in sense that nearby pixels are related.
- **Convolution** slides a small kernel across the image, computing a sum-of-products at each receptive field to build a feature map.
- **ReLU** adds non-linearity right after each convolution, so the network can learn genuinely complex patterns, not just one big linear function.
- **Feature maps** show where a specific pattern was detected; stacking many filters, and stacking layers, lets a CNN build from simple edges up to whole objects.
- **Zero padding** keeps spatial size under control without inventing fake content.
- **Pooling** periodically shrinks the feature maps, adding speed and tolerance to small shifts, with zero learnable parameters.
- **Flatten + dense layers** turn the final features into a decision, with softmax converting raw scores into class probabilities.
- The output-size and parameter-count formulas let you calculate exactly how any convolutional layer behaves.
- **VGG16** ties all of this together: 13 conv layers + 3 dense layers = 16 weight layers, about 138 million parameters, going from a 224x224x3 photo to a 1,000-way classification.

## 13. Memory tricks recap

| Concept | Memory trick |
|---|---|
| Convolution | A flashlight scanning one small patch at a time |
| Kernel / filter | A mini stencil hunting for one pattern |
| ReLU | A bouncer that blocks negative numbers at the door |
| Feature map | A highlighted report showing where a pattern was found |
| Padding (zero) | A blank picture frame border, adds no fake content |
| Pooling | Turning a paragraph into a headline — keep the loudest point |
| Flatten | Unrolling a folded map into one straight strip |
| Dense layer | A detective weighing every clue before the verdict |
| Softmax | Turning raw scores into a normalized ranking that sums to 1 |

---
Previous: **[Part 8: Deep Learning Cheat Sheet]({{ site.baseurl }}/topics/deep-learning-cheat-sheet)**
