---
layout: topic
title: "Computer Vision - Part 2: Introduction"
category: Computer Vision
order: 2
permalink: /topics/computer-vision-introduction/
tags:
  - computer-vision
  - image-processing
  - cnn
  - beginners
  - friendly
summary: "A beginner-friendly introduction to computer vision: what it is, why it is hard, the standard pipeline, and how it connects to deep learning and image processing."
---

# Computer Vision — Part 2: Introduction

Computer vision is the part of artificial intelligence that teaches computers to understand images and videos the way humans understand what they see.

When you look at a photo, you instantly recognise objects, their positions, depth, motion, and even mood. For a computer, the same photo is just a giant table of numbers. Computer vision is the collection of techniques that turn those numbers into useful meaning.

---

## 1. What is computer vision?

A simple definition:

> **Computer vision** = giving a machine the ability to extract useful information from visual data.

That information can be:

| Task | Question the computer answers |
|---|---|
| **Image classification** | What is in this image? |
| **Object detection** | What objects are in the image and where are they? |
| **Object localisation** | Where is the single main object? |
| **Image segmentation** | Which pixels belong to each object? |
| **Face recognition** | Who is this person? |
| **Optical character recognition (OCR)** | What text is in this image? |
| **Motion analysis** | Which way are things moving? |
| **Image generation** | Can you create a new image from a description? |

---

## 2. Human vision vs computer vision

Your eyes are not cameras that simply record pixels. Your brain uses a lifetime of experience to recognise patterns, ignore clutter, and fill in missing information.

For example, you can recognise a dog in a photo even if:

- the dog is far away or very close
- the lighting is dim or very bright
- part of the dog is hidden behind a chair
- the photo is black-and-white
- the dog is upside down

A computer does none of this automatically. It sees a grid of colour values and must learn, from many examples, that a particular pattern of numbers means "dog".

```text
Human:  "That is a cat."
Computer: "I see a 224 × 224 × 3 tensor of integers."
```

---

## 3. Why is computer vision difficult?

The same object can produce very different pixel patterns. The main challenges are:

| Challenge | What it means |
|---|---|
| **Viewpoint changes** | An object looks different from the front, side, or top. |
| **Scale changes** | A car can fill the image or be a tiny dot. |
| **Illumination** | Bright sunlight, shadows, and night photos change colours. |
| **Occlusion** | Objects hide behind each other. |
| **Background clutter** | The object blends into the background. |
| **Deformation** | A person can sit, run, or stretch. |
| **Intra-class variation** | Not all chairs, dogs, or cars look the same. |

A good computer vision system must be robust to all of these.

---

## 4. Images as numbers

Before any algorithm can work, an image must become numbers.

- A greyscale image is a 2-D grid of values. Each value is a pixel intensity, usually from 0 (black) to 255 (white).
- A colour image is a 3-D grid: height × width × channels, where the channels are red, green, and blue.

```text
Grayscale:   image[y, x] = one number (brightness)
Colour:      image[y, x, c] = three numbers (R, G, B)
```

For a detailed look at pixels, colour models, and basic image arithmetic, see [Part 1: Image Processing Fundamentals]({{ site.baseurl }}/topics/computer-vision-image-processing-fundamentals/).

---

## 5. The computer vision pipeline

Most real-world vision systems follow the same broad steps:

```text
1. Capture     → camera, scanner, video file, medical device
2. Preprocess  → resize, crop, rotate, denoise, normalise
3. Augment     → random flips, colour changes (training only)
4. Model       → extract features and make a prediction
5. Postprocess → convert raw outputs to human-readable results
6. Act         → display, alert, store, or control another system
```

**Preprocessing** makes sure every input has the same size and range so the model sees consistent data. **Augmentation** artificially creates more training examples by slightly changing existing images. **Postprocessing** turns model outputs, such as tensors, into bounding boxes, masks, or labels.

---

## 6. The two big eras of computer vision

### Era 1 — hand-crafted features

Before deep learning, engineers manually designed features such as:

- **SIFT** and **SURF** for finding interesting keypoints
- **HOG** (Histogram of Oriented Gradients) for describing object shapes
- **Haar cascades** for face detection

These methods worked well for specific, controlled problems, but they did not generalise. A feature designed for faces usually failed for cars.

### Era 2 — learned features with deep learning

Convolutional neural networks (CNNs) learn their own features from data. Instead of a human writing rules, the network discovers edges, textures, shapes, and object parts by looking at thousands of examples.

```text
Pixels → edges → textures → shapes → object parts → whole objects → prediction
```

This is the foundation of modern computer vision. CNNs are covered in detail in the Deep Learning section under [Part 9: Convolutional Neural Networks]({% link _topics/Convolutional Neural Networks - A Friendly Guide.md %}).

---

## 7. Common applications

Computer vision is used in many places you already interact with:

| Area | Example |
|---|---|
| **Medical imaging** | Detecting tumours in X-rays and MRI scans |
| **Self-driving cars** | Identifying pedestrians, lanes, traffic signs |
| **Manufacturing** | Finding defects on production lines |
| **Retail** | Self-checkout cameras and inventory counting |
| **Security** | Face unlock, intrusion detection |
| **Agriculture** | Crop-health monitoring from drone images |
| **Entertainment** | Snapchat filters, game motion capture |
| **Accessibility** | Describing photos for visually impaired users |

---

## 8. How computer vision relates to other topics

| Field | How it connects |
|---|---|
| **Image processing** | Low-level operations on pixels: filters, resizing, noise removal. |
| **Deep learning** | The main engine that learns features and predictions. |
| **Natural language processing** | Combining vision with text for image captioning or visual question answering. |
| **Robotics** | Cameras give robots information about the world around them. |
| **Generative AI** | Models that create or edit images, such as diffusion models and GANs. |

---

## 9. Summary

- **Computer vision** turns images and videos into useful information.
- The same object can look very different because of viewpoint, lighting, scale, and occlusion, which makes vision hard.
- A typical pipeline is: capture → preprocess → augment → model → postprocess → act.
- Modern computer vision is dominated by **deep learning**, especially CNNs.
- Vision connects to image processing, NLP, robotics, and generative AI.

**Next:** [Part 3: Object Detection Basics]({{ site.baseurl }}/topics/computer-vision-object-detection-basics/)
