---
title: "Computer Vision - Part 3: CNNs for Computer Vision"
category: Computer Vision
order: 3
permalink: /topics/computer-vision-cnn-primer/
tags:
  - computer-vision
  - cnn
  - convolutional-neural-networks
  - feature-maps
  - backbone
  - transfer-learning
  - beginners
  - friendly
summary: "A short, focused primer on convolutional neural networks written specifically for computer vision: learned filters, feature maps, pooling, the hierarchy of features, and the idea of a pretrained CNN backbone — just enough to understand the object detectors covered later in this series."
date: 2026-09-07
---

# Computer Vision — Part 3: CNNs for Computer Vision

[Part 1]({{ site.baseurl }}/topics/computer-vision-image-processing-fundamentals/) showed you how to build filters by hand: a Sobel filter for edges, a Gaussian filter for blur, a median filter for noise. Every one of those filters had numbers a human chose in advance.

That works for edges and blur. It does not work for "is this a cat." Nobody can hand-write a filter for "cat-ness." A **convolutional neural network (CNN)** solves this by keeping the exact same convolution operation from Part 1, but no longer choosing the filter numbers by hand. Instead, the network **learns** them from thousands of example photos.

This part is a focused primer: just enough about how a CNN works to make sense of the detectors in the rest of this series (Region-Based Detectors, Anchor Boxes, YOLO, and SSD all lean on the ideas here). For the full depth — exact formulas, backpropagation through filters, and a real architecture walked through layer by layer — see the Deep Learning section's [Part 9: Convolutional Neural Networks]({% link _topics/Convolutional Neural Networks - A Friendly Guide.md %}).

---

## 1. A convolutional layer is a learned filter

Recall from Part 1: convolution slides a small grid of numbers (a kernel) over an image, multiplying and summing as it goes. In a CNN, that kernel's numbers are **parameters** — values the network adjusts during training, the same way it adjusts any other weight.

At the start of training, a filter's numbers are random. After seeing many labelled photos and being corrected when it gets things wrong, the filter settles into numbers that respond strongly to some visual pattern — maybe a vertical edge, maybe a patch of orange-brown fur, maybe a curve. Nobody wrote that filter. The network found it because it was useful for telling the training photos apart.

A single convolutional layer doesn't use just one filter — it uses many, often 32, 64, or more, all learned side by side. Each one looks for a different pattern in the same image.

## 2. Feature maps

Running one filter over an image produces one new grid of numbers, the same way Part 1's Sobel filter produced an edge map. In CNN terms, that output grid is called a **feature map** — it shows, at every position in the image, how strongly that one filter's pattern was detected there.

Since a convolutional layer runs many filters, it produces many feature maps, stacked together. If a layer has 64 filters, its output is 64 feature maps deep, one per filter, each one a map of "where did this particular pattern show up."

```text
image → [filter 1] → feature map 1  (found: vertical edges)
      → [filter 2] → feature map 2  (found: orange-ish patches)
      → [filter 3] → feature map 3  (found: rounded curves)
      → ...
```

## 3. Stacking layers builds a hierarchy

A single layer of filters can only detect simple, local patterns like edges and colour patches. The real power of a CNN comes from **stacking many convolutional layers** one after another. Each new layer takes the previous layer's feature maps as its input, so it isn't looking at raw pixels anymore — it's looking at combinations of "edges" and "colour patches."

This produces a hierarchy, the same one introduced in the Deep Learning CNN guide:

```text
Layer 1: pixels     → edges, colours
Layer 2: edges      → textures, corners
Layer 3: textures    → parts (an eye, a wheel, a leaf)
Layer 4: parts       → whole objects (a face, a car, a tree)
```

Early layers learn generic, reusable patterns. Deeper layers learn increasingly specific, task-relevant combinations of those patterns. This is exactly why a CNN trained on one large photo collection can be reused for a completely different task — the early layers' edges and textures are useful almost everywhere.

## 4. Pooling: shrinking the feature maps

Between convolutional layers, CNNs typically shrink the feature maps down, usually by keeping only the strongest value in each small neighbourhood (called **max pooling**). A 2×2 max-pooling step turns a 100×100 feature map into a 50×50 one, keeping the loudest signal from each 2×2 patch and throwing the rest away.

This does two useful things at once: it makes the network faster (smaller grids are cheaper to process), and it makes detections more tolerant to small shifts — if the interesting pattern moves a few pixels, it usually still survives inside the same pooled cell.

## 5. Putting it together: a CNN backbone

Stack enough (convolution → activation → pooling) blocks and you get a pipeline that takes a photo in one end, and produces a small, deep stack of feature maps out the other end — a compact numerical summary of "what patterns are present, and roughly where."

```text
image (e.g. 224×224×3)
  → conv block 1 → pool  (edges, colours)
  → conv block 2 → pool  (textures)
  → conv block 3 → pool  (object parts)
  → conv block 4 → pool  (whole-object patterns)
  → final feature map (e.g. 7×7×512)
```

That stack of convolution and pooling blocks, on its own, is often called the **backbone**. On its own it doesn't say "cat" or "dog" — for a classifier, you'd add one more piece on top (a small set of fully connected layers, covered in the Deep Learning guide) that turns the final feature map into a decision.

This "backbone" framing matters a lot for the rest of this series. Object detectors don't usually train a CNN backbone from scratch. Instead, they take a CNN that was already trained as an image classifier on a huge, general photo collection (commonly **ImageNet**, over a million photos across a thousand categories), throw away its final decision layer, and reuse everything before it purely as a feature extractor. This is why you'll keep seeing phrases like "a CNN pretrained on ImageNet" in the Region-Based Detectors and One-Stage Detectors parts that follow — they mean exactly this: someone else's backbone, already good at noticing edges, textures, and object parts, repurposed as the first stage of a detector.

## 6. Summary

- A convolutional layer is the same sliding-kernel operation from Part 1, except the kernel's numbers are **learned**, not hand-chosen.
- Each filter's output is a **feature map**: where in the image that filter's pattern was found.
- Stacking layers builds a **hierarchy**: edges → textures → parts → whole objects.
- **Pooling** shrinks feature maps between layers, for speed and for tolerance to small shifts.
- The stack of convolution and pooling layers, without a final decision layer, is a **backbone** — a reusable feature extractor.
- Detectors almost always start from a backbone **pretrained** on a large general dataset like ImageNet, rather than training one from scratch.

For the full mathematical depth behind all of this — exact output-size and parameter-count formulas, how backpropagation flows through a filter, and a complete layer-by-layer walkthrough of a real architecture (VGG16) — see [Part 9: Convolutional Neural Networks]({% link _topics/Convolutional Neural Networks - A Friendly Guide.md %}) in the Deep Learning section.

**Next:** [Part 4: Object Detection Basics]({{ site.baseurl }}/topics/computer-vision-object-detection-basics/)
