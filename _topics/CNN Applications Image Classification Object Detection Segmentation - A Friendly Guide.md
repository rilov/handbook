---
layout: topic
title: "Part 13: CNN Applications — Image Classification, Object Detection, Segmentation, Facial Recognition, and OCR"
category: Deep Learning
order: 13
tags:
  - deep-learning
  - cnn
  - computer-vision
  - image-classification
  - object-detection
  - image-segmentation
  - facial-recognition
  - ocr
  - beginners
  - friendly
summary: An overview of the main real-world applications of CNNs — image classification, object detection, image segmentation, facial recognition and analysis, and optical character recognition (OCR). Explains what each task is, how CNNs are used, key architectures, and real-world examples.
---

# Part 13: CNN Applications — Image Classification, Object Detection, Segmentation, Facial Recognition, and OCR

## What this guide covers

CNNs power almost every modern computer vision application.

This guide explains the five main application areas:

```text
1. Image classification   — what is in this image?
2. Object detection       — where is each object in this image?
3. Image segmentation     — which pixels belong to each object?
4. Facial recognition     — who is this person?
5. OCR                    — what text is in this image?
```

Each section explains the task, how a CNN solves it, key architectures, and real-world uses.

---

## 1. Image classification

### What is it?

Given an image, predict which class it belongs to.

```text
Input:  one image
Output: one label (e.g. "cat", "truck", "airplane")
```

This is the simplest CNN task and the one covered in previous guides.

### How a CNN solves it

```text
Image
→ convolution layers extract features (edges, textures, shapes)
→ pooling reduces spatial size
→ flatten
→ dense layers
→ softmax → probability for each class
```

### Real-world examples

| Use case | Classes |
|---|---|
| Medical image diagnosis | Tumor present / not present |
| Quality control in manufacturing | Defect / no defect |
| Plant disease detection | Healthy / diseased / which disease |
| Satellite image classification | Forest / water / urban / farmland |
| Food recognition | Pizza / salad / burger / ... |

### Key architectures

| Architecture | Year | Notes |
|---|---|---|
| AlexNet | 2012 | First deep CNN to win ImageNet |
| VGG16 | 2014 | Simple and deep, 16 weight layers |
| ResNet | 2015 | Residual connections, up to 152 layers |
| EfficientNet | 2019 | Scaled depth, width, resolution together |

### In PyTorch

```python
import torchvision.models as models

model = models.resnet50(pretrained=True)
model.fc = nn.Linear(2048, num_classes)
```

---

## 2. Object detection

### What is it?

Given an image, find every object in it and draw a bounding box around each one.

```text
Input:  one image
Output: list of (class label, bounding box coordinates, confidence score)
```

Example:

```text
Image of a street scene
→ [car at (120, 80, 200, 160), confidence 0.95]
   [person at (50, 30, 90, 180), confidence 0.88]
   [bicycle at (300, 100, 380, 200), confidence 0.72]
```

### How it differs from classification

Classification gives one label per image.

Detection gives many labels and locations per image.

```text
Classification: "there is a car in this image"
Detection:      "there is a car at these pixel coordinates"
```

### How a CNN solves it

Modern detectors use a CNN as a **backbone** to extract features, then add a **detection head** that predicts boxes and class scores.

```text
Image
→ CNN backbone (ResNet, VGG) → feature maps
→ detection head → bounding boxes + class scores
→ non-maximum suppression → remove duplicate boxes
→ final detections
```

### Key architectures

| Architecture | Notes |
|---|---|
| YOLO (You Only Look Once) | Very fast, good for real-time video |
| SSD (Single Shot Detector) | Fast single-pass detection |
| Faster R-CNN | Two-stage: propose regions then classify |
| DETR | Transformer-based detection, no anchor boxes |

### Real-world examples

- Self-driving cars detecting pedestrians, vehicles, traffic signs
- Security cameras detecting intruders
- Retail shelf monitoring detecting products
- Medical imaging detecting tumors or lesions in scans

### In PyTorch

```python
import torchvision.models.detection as detection

model = detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

with torch.no_grad():
    predictions = model([image_tensor])

# predictions[0] contains boxes, labels, scores
boxes  = predictions[0]['boxes']
labels = predictions[0]['labels']
scores = predictions[0]['scores']
```

---

## 3. Image segmentation

### What is it?

Given an image, assign a class label to **every single pixel**.

```text
Input:  one image (H × W × 3)
Output: one label map (H × W) where each pixel has a class
```

There are two main types:

| Type | What it does | Example |
|---|---|---|
| Semantic segmentation | Labels every pixel with its class | All cars are "car", all roads are "road" |
| Instance segmentation | Labels every pixel AND tells individual objects apart | Car 1, Car 2, Person 1, Person 2 |

### How a CNN solves it

Segmentation networks produce an output the **same size as the input**.

They use an **encoder-decoder** structure:

```text
Image
→ Encoder (CNN backbone): shrink spatial size, extract features
→ Decoder: expand back to original size, assign class per pixel
→ Output: H × W label map
```

The decoder uses **transposed convolutions** (also called upsampling or deconvolution) to grow the feature maps back to the original image size.

### Key architectures

| Architecture | Notes |
|---|---|
| FCN (Fully Convolutional Network) | First end-to-end segmentation network |
| U-Net | Encoder-decoder with skip connections; widely used in medical imaging |
| DeepLab | Uses dilated convolutions to capture context without shrinking resolution |
| Mask R-CNN | Adds segmentation mask output on top of Faster R-CNN detection |

### Real-world examples

- Autonomous driving: segment road, cars, pedestrians, sky
- Medical imaging: segment tumor boundaries in MRI scans
- Satellite imagery: segment land use (forest, water, buildings)
- Portrait mode photography: separate person from background

### Simple comparison: classification vs detection vs segmentation

```text
Classification: is there a cat? → YES
Detection:      where is the cat? → bounding box at (x1, y1, x2, y2)
Segmentation:   which pixels are the cat? → pixel-level mask
```

---

## 4. Facial recognition and analysis

### What is it?

Facial recognition identifies **who** a person is from their face.

Facial analysis extracts other attributes from a face: age, emotion, gender, gaze direction.

```text
Input:  image containing one or more faces
Output: identity / attribute predictions
```

### How it works

The pipeline typically has three stages:

```text
Stage 1: Face detection
→ find all face regions in the image (bounding boxes)
→ uses object detection CNN

Stage 2: Face alignment
→ normalize each face to a standard position and size
→ align eyes, nose, mouth to fixed landmarks

Stage 3: Feature extraction and recognition
→ CNN encodes the face into a compact feature vector (embedding)
→ compare embedding to database of known people
→ closest match = predicted identity
```

### Face embeddings

A face embedding is a fixed-length vector (e.g. 128 or 512 numbers) that represents the face.

```text
Photo of Alice → CNN → [0.2, -0.5, 0.8, ..., 0.3]  (128 numbers)
Photo of Alice (different angle) → CNN → [0.19, -0.48, 0.81, ..., 0.31]  (very similar)
Photo of Bob   → CNN → [0.9, 0.3, -0.2, ..., 0.7]   (very different)
```

Two photos of the same person produce similar embeddings. Different people produce distant embeddings.

Recognition: compare embeddings using a distance metric (cosine similarity or Euclidean distance).

### Key architectures

| Architecture | Notes |
|---|---|
| DeepFace (Meta) | One of the first deep CNNs for face recognition |
| FaceNet (Google) | Learns embeddings using triplet loss |
| ArcFace | State-of-the-art face recognition, angular margin loss |

### Facial analysis tasks

| Task | Output |
|---|---|
| Emotion recognition | Happy / sad / angry / surprised / neutral |
| Age estimation | Estimated age in years |
| Gaze estimation | Where the person is looking |
| Landmark detection | Positions of eyes, nose, mouth corners |

### Real-world examples

- Phone unlock using face ID
- Airport passport control
- Attendance tracking systems
- Emotion analysis for customer feedback
- Driver monitoring systems (detecting drowsiness)

---

## 5. Optical Character Recognition (OCR)

### What is it?

OCR converts images containing text into machine-readable text.

```text
Input:  image with text (photo, scan, screenshot)
Output: extracted text string
```

### How it works

OCR with CNNs typically has two stages:

```text
Stage 1: Text detection
→ CNN detects regions containing text
→ outputs bounding boxes around words or lines

Stage 2: Text recognition
→ CNN + sequence model reads each detected region
→ outputs the text string
```

The recognition stage uses a CNN to extract visual features from the text region, then a recurrent model (like LSTM) or a transformer to decode the character sequence.

```text
Detected text region image
→ CNN: extract column-by-column features
→ LSTM: decode sequence of characters
→ CTC loss: handle variable-length output
→ "Hello World"
```

### Key architectures

| Architecture | Notes |
|---|---|
| CRNN | CNN + RNN, standard for text recognition |
| EAST | Efficient text detection network |
| Tesseract | Classic OCR engine, now with deep learning backend |
| TrOCR (Microsoft) | Transformer-based OCR, state of the art |

### Real-world examples

- Scanning paper documents into editable text
- Reading license plates
- Extracting text from photos for translation
- Processing invoices and receipts automatically
- Digitizing historical books and newspapers
- Reading handwritten forms

---

## 6. Comparison: which task for which problem?

| You want to know... | Task | Output |
|---|---|---|
| What is in this image? | Classification | One label |
| Where are the objects? | Detection | Bounding boxes + labels |
| Which pixels belong to which object? | Segmentation | Pixel-level mask |
| Who is this person? | Facial recognition | Identity or embedding |
| What does the text say? | OCR | Text string |

---

## 7. Summary

All five applications are built on the same CNN foundation:

```text
Convolution layers extract features
→ pooling reduces size
→ task-specific head produces the output
```

What changes is the output format and the loss function:

| Application | Output | Loss |
|---|---|---|
| Classification | Class probabilities | CrossEntropyLoss |
| Detection | Boxes + class scores | Box regression + classification loss |
| Segmentation | Per-pixel class map | CrossEntropyLoss per pixel |
| Face recognition | Embedding vector | Triplet loss or ArcFace loss |
| OCR | Character sequence | CTC loss |

---

## What to read next

- [Part 12: Building a CNN End-to-End — CIFAR-10 with PyTorch]({{ site.baseurl }}/topics/building-a-cnn-end-to-end-cifar-10-with-pytorch) — hands-on implementation
- [Part 11: CNN Training Pipeline, Transfer Learning, and Visualization]({{ site.baseurl }}/topics/cnn-training-pipeline-transfer-learning-and-visualization) — training strategy and Grad-CAM
- [Part 10: Advanced Convolutional Neural Networks]({{ site.baseurl }}/topics/advanced-convolutional-neural-networks) — dropout, batch norm, residual connections
