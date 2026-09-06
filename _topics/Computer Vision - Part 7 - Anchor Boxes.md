---
layout: topic
title: "Computer Vision - Part 7: Anchor Boxes"
category: Computer Vision
order: 7
permalink: /topics/computer-vision-anchor-boxes/
tags:
  - computer-vision
  - object-detection
  - anchor-boxes
  - region-proposal-network
  - yolo
  - ssd
  - beginners
  - friendly
summary: "A beginner-friendly guide to anchor boxes: why they exist, how they are placed and matched to ground truth, and how they are used in Faster R-CNN, YOLO, and SSD."
---

# Computer Vision — Part 7: Anchor Boxes

When an object detector looks at an image, it does not know where objects are, how big they are, or what shape they are. **Anchor boxes** are pre-defined guess shapes that let the detector start from sensible defaults instead of searching blindly.

This part explains what anchors are, how they are generated, how they are matched to real objects, and where they appear in modern detectors.

---

## 1. The problem anchors solve

Imagine you want to catch fish of different sizes and shapes in a lake. If you only throw one net, you will miss a lot of fish. A better plan is to throw several nets at each spot:

- a small round net for tiny fish
- a wide net for flat fish
- a long net for eels

At every location, you try several shapes and sizes. If the fish is there, at least one net will be a good fit.

Anchor boxes work the same way. At every spatial location on a feature map, the detector evaluates a set of **pre-defined boxes**. Each anchor is a guess about a possible object shape and size.

---

## 2. What is an anchor box?

An anchor box is a rectangle with a fixed width and height, defined ahead of time. It is not a prediction; it is a **starting template**.

A typical set of anchors might be:

| Anchor | Width | Height | Aspect ratio | Use for |
|---|---|---|---|---|
| A | 32 | 32 | 1:1 | Small square objects |
| B | 64 | 64 | 1:1 | Medium square objects |
| C | 128 | 128 | 1:1 | Large square objects |
| D | 32 | 64 | 1:2 | Tall objects like people |
| E | 64 | 32 | 2:1 | Wide objects like buses |

These anchors are placed at every location on the feature map, so the network can focus on saying:

- Is there an object near this anchor?
- If yes, how should the anchor be shifted or resized?
- What class is the object?

---

## 3. Anchor placement on a feature map

After a CNN processes an image, the feature map is smaller than the original image. Each cell in the feature map corresponds to a region in the original image.

For example, if the image is `800 × 600` and the CNN down-samples by a factor of 16, the feature map is `50 × 37`.

```text
Feature map cell (i, j)  →  original image region
width  = original_width / feature_map_width
height = original_height / feature_map_height
```

At each cell `(i, j)`, the anchor is placed at the centre of the corresponding image region. Then the anchor is resized to each width-height pair in the anchor set.

```text
For each feature-map cell:
  For each anchor shape:
    place one anchor box at the cell centre
```

If there are `50 × 37` cells and 9 anchors per cell, the total number of anchors is:

```text
50 × 37 × 9 = 16,650 anchors
```

Most of these anchors will not contain an object. The network learns to classify them as background.

---

## 4. Matching anchors to ground truth

During training, the detector knows the real boxes for each image. It must teach each anchor whether it should predict an object and, if so, which object.

The usual rule is based on **IoU**:

```text
For each ground-truth box:
  Find the anchor with the highest IoU → mark as positive (best match)

For each anchor:
  If IoU with any ground-truth box ≥ 0.7  → positive
  If IoU with all ground-truth boxes ≤ 0.3  → negative (background)
  Otherwise → ignore
```

A **positive** anchor is responsible for detecting that object. A **negative** anchor learns to say "this is just background".

Because positives are rare compared to negatives, detectors usually use strategies such as hard negative mining to balance training.

---

## 5. Anchor regression

An anchor almost never perfectly matches an object. The network predicts small adjustments.

If the anchor has centre `(x_a, y_a)` and width `w_a`, height `h_a`, and the ground truth has `(x, y, w, h)`, the target offsets are:

```text
t_x = (x - x_a) / w_a
t_y = (y - y_a) / h_a
t_w = log(w / w_a)
t_h = log(h / h_a)
```

These are called **anchor offsets** or **delta values**. They are usually small numbers, which makes learning easier.

At inference time, the predicted offsets are converted back:

```text
x = x_a + w_a * pred_x
y = y_a + h_a * pred_y
w = w_a * exp(pred_w)
h = h_a * exp(pred_h)
```

The `exp` ensures the width and height stay positive.

---

## 6. Anchor boxes in different detectors

### Faster R-CNN

In Faster R-CNN the **Region Proposal Network** uses 9 anchors at every feature-map cell (3 scales × 3 ratios). The RPN predicts objectness and anchor offsets, then passes the best anchors to the detection head.

### YOLO v2 and v3

YOLOv2 introduced **dimension clusters**: instead of hand-picking anchors, the authors ran k-means on the widths and heights of ground-truth boxes in the training set. This made anchors match the dataset better.

### SSD (Single Shot Detector)

SSD places anchors on several feature maps, not just the top one. Smaller feature maps use larger anchors to detect big objects. Larger feature maps use smaller anchors to detect small objects. This is how SSD handles objects of many sizes.

```text
Layer 1 (large feature map)  → small anchors → detect small objects
Layer 2 (medium feature map) → medium anchors
Layer 3 (small feature map)  → large anchors  → detect large objects
```

---

## 7. Problems with anchors

Anchors are powerful, but they come with challenges:

| Problem | Explanation |
|---|---|
| **Many anchors** | A single image can have tens of thousands of anchors, and most are background. This creates imbalance. |
| **Size tuning** | Anchor scales and ratios must be tuned to the dataset. Bad anchors miss objects that are unusual sizes. |
| **IoU threshold** | The cut-off between positive and negative is a hyperparameter that affects recall and precision. |
| **Overlapping objects** | If two objects overlap, one anchor may be assigned to only one of them. |

Because of these issues, modern detectors have explored **anchor-free** designs such as FCOS and CenterNet. Anchor-free models predict the distance from each feature point to the box edges directly, without pre-defined shapes.

---

## 8. Code: generate a grid of anchor boxes

```python
import numpy as np

def generate_anchors(feature_map_shape, image_shape, scales, ratios):
    """
    feature_map_shape: (H, W)
    image_shape: (img_h, img_w)
    scales: list of anchor areas in pixels (e.g. [32*32, 64*64, 128*128])
    ratios: list of width/height ratios (e.g. [0.5, 1.0, 2.0])
    Returns a list of [x1, y1, x2, y2] boxes.
    """
    fm_h, fm_w = feature_map_shape
    img_h, img_w = image_shape

    stride_h = img_h / fm_h
    stride_w = img_w / fm_w

    anchors = []
    for i in range(fm_h):
        for j in range(fm_w):
            cx = (j + 0.5) * stride_w
            cy = (i + 0.5) * stride_h

            for scale in scales:
                for ratio in ratios:
                    area = scale
                    w = np.sqrt(area * ratio)
                    h = np.sqrt(area / ratio)

                    x1 = cx - w / 2
                    y1 = cy - h / 2
                    x2 = cx + w / 2
                    y2 = cy + h / 2
                    anchors.append([x1, y1, x2, y2])

    return np.array(anchors)

anchors = generate_anchors(
    feature_map_shape=(10, 10),
    image_shape=(320, 320),
    scales=[32*32, 64*64],
    ratios=[0.5, 1.0, 2.0]
)
print("Number of anchors:", len(anchors))
print(anchors[:3])
```

---

## 9. Summary

- **Anchor boxes** are pre-defined templates of different sizes and aspect ratios placed across the image.
- They give the detector a set of starting guesses so it does not have to search every possible box blindly.
- Each anchor is matched to ground truth by **IoU** and then refined with small regression offsets.
- **Faster R-CNN** uses anchors in the RPN. **YOLO** uses dataset-specific anchor clusters. **SSD** uses anchors across multiple feature-map layers.
- Anchors are effective but require tuning, create class imbalance, and can struggle with overlapping objects. Modern anchor-free detectors address some of these issues.

**Next:** [Part 8: One-Stage Detectors — YOLO and SSD]({{ site.baseurl }}/topics/computer-vision-yolo-ssd/)
