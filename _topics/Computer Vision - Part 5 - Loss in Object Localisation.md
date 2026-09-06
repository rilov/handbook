---
layout: topic
title: "Computer Vision - Part 5: Loss in Object Localisation"
category: Computer Vision
order: 5
permalink: /topics/computer-vision-localisation-loss/
tags:
  - computer-vision
  - object-detection
  - loss-functions
  - iou
  - smooth-l1
  - giou
  - diou
  - ciou
  - beginners
  - friendly
summary: "A simple guide to loss functions used for bounding-box regression, from L1/L2 and Smooth L1 to IoU, GIoU, DIoU, and CIoU, with formulas and code examples."
---

# Computer Vision — Part 5: Loss in Object Localisation

Object detection has two jobs: classify the object and place a box around it. The loss function tells the model how wrong it is and which way to improve.

This part focuses on the **localisation loss**: the part of the total loss that measures how well the predicted bounding box matches the ground-truth box.

---

## 1. What is a localisation loss?

A localisation loss takes two boxes and returns one number:

- **0** means the predicted box is exactly on top of the real box.
- A **large number** means the box is far away, the wrong size, or the wrong shape.

The model tries to make this number as small as possible during training.

The total loss for an object detector usually combines several pieces:

```text
total loss = classification loss + localisation loss (+ confidence loss)
```

This part is about the **localisation** piece.

---

## 2. L2 loss (Mean Squared Error)

The simplest idea is to treat the four box numbers as plain coordinates and use the squared difference:

```text
L2 = (x_true - x_pred)² + (y_true - y_pred)² + (w_true - w_pred)² + (h_true - h_pred)²
```

MSE is easy to compute but has problems for bounding boxes.

### Drawbacks

| Problem | Why it matters |
|---|---|
| **Not scale-invariant** | A 10-pixel error on a small box is the same as a 10-pixel error on a large box. |
| **Ignores geometry** | It treats `(x, y, w, h)` as four unrelated numbers. |
| **Very sensitive to outliers** | A single large mistake is punished heavily because of the square. |

For these reasons, MSE alone is rarely used for boxes in modern detectors.

---

## 3. L1 loss (Mean Absolute Error)

L1 uses the absolute difference instead of the square:

```text
L1 = |x_true - x_pred| + |y_true - y_pred| + |w_true - w_pred| + |h_true - h_pred|
```

It is less sensitive to outliers than L2, but it is still not scale-invariant and still ignores geometry.

---

## 4. Smooth L1 loss (Huber loss)

**Smooth L1** is the most common baseline for bounding-box regression. It behaves like L2 for small errors and L1 for large errors.

```text
           ⎧ 0.5 * (error)²            if |error| < δ
SmoothL1 = ⎨
           ⎩ δ * |error| - 0.5 * δ²   if |error| ≥ δ
```

When `δ = 1.0`:

```text
           ⎧ 0.5 * e²    if |e| < 1
SmoothL1 = ⎨
           ⎩ |e| - 0.5   if |e| ≥ 1
```

### Why it is useful

- Small errors get the gentle quadratic treatment, which helps training stability.
- Large errors get the linear treatment, so a single bad prediction does not explode the gradient.
- It is the default choice for Faster R-CNN and many two-stage detectors.

```python
import torch
import torch.nn as nn

smooth_l1 = nn.SmoothL1Loss()

pred   = torch.tensor([50.0, 30.0, 150.0, 150.0])
 target = torch.tensor([55.0, 35.0, 145.0, 155.0])

loss = smooth_l1(pred, target)
print(loss.item())
```

---

## 5. IoU loss

A loss based directly on **Intersection over Union** is much more natural for bounding boxes because it uses the geometry of the boxes.

```text
L_IoU = 1 - IoU(pred, true)
```

If the boxes perfectly overlap, IoU is `1` and the loss is `0`. If they do not overlap, IoU is `0` and the loss is `1`.

### Advantages

- Scale-invariant: a 10-pixel error matters more for a small box.
- Coupled: it measures the full box, not four separate numbers.
- Matches the evaluation metric (mAP uses IoU).

### Limitation

If two boxes do **not overlap at all**, the gradient of IoU with respect to the box parameters becomes `0`. The model gets no signal telling it which direction to move. Modern losses fix this.

---

## 6. Generalised IoU (GIoU)

**GIoU** solves the zero-overlap problem by comparing the area of the smallest enclosing rectangle with the union.

```text
            A ∪ B
C = smallest box that contains both A and B

            |A ∩ B|     |C - (A ∪ B)|
GIoU = ───────────── - ───────────────
          |A ∪ B|            |C|

L_GIoU = 1 - GIoU
```

In plain English:

- If the boxes overlap, the first term is IoU.
- If they do not overlap, the second term pushes the boxes closer by measuring how much empty space is between them inside the enclosing box `C`.

Even with no overlap, GIoU still gives a gradient and tells the model which way to move.

---

## 7. Distance IoU (DIoU)

GIoU can be slow to converge because it only cares about area, not the distance between box centres. **DIoU** adds a centre-distance penalty.

```text
              ρ²(b, b_gt)
DIoU = IoU - ─────────────
                 c²

L_DIou = 1 - DIoU
```

Where:

- `b` and `b_gt` are the centre points of the predicted and ground-truth boxes.
- `ρ` is the Euclidean distance between the two centre points.
- `c` is the diagonal length of the smallest enclosing box.

DIoU penalises the distance between centres directly, so boxes that are the right size but far apart still get a strong training signal.

---

## 8. Complete IoU (CIoU)

**CIoU** adds three terms: overlap, centre distance, and aspect ratio.

```text
                     ρ²(b, b_gt)        α * v
CIoU = IoU - ───────────────────── - ─────────
                    c²                 (1 - IoU) + α

L_CIoU = 1 - CIoU
```

Where `v` measures how different the aspect ratios are:

```text
              4   ⎛        w_gt          h_gt      ⎞²
v = ─────────── * ⎜ arctan ──── - arctan ──── ⎟
       π²          ⎝        h_gt          h       ⎠
```

And `α` is a positive weighting term.

CIoU is the most complete of the IoU-based losses and is often used in YOLOv4 and later.

---

## 9. Comparison table

| Loss | What it optimises | Best for |
|---|---|---|
| **L2 / MSE** | Point distance | Not recommended for boxes |
| **L1** | Point distance | Not recommended for boxes |
| **Smooth L1** | Stable regression of box parameters | Two-stage detectors (Faster R-CNN) |
| **IoU** | Direct overlap | When IoU is non-zero |
| **GIoU** | Overlap + enclosure | Handling no-overlap cases |
| **DIoU** | Overlap + centre distance | Faster convergence |
| **CIoU** | Overlap + centre distance + aspect ratio | Best overall bounding-box loss (YOLOv4+) |

---

## 10. Multi-task loss example

A detector like Faster R-CNN has a combined loss:

```text
L = L_cls   +   λ * L_loc
```

Where:

- `L_cls` is the classification loss (often cross-entropy).
- `L_loc` is the box regression loss (Smooth L1 for Faster R-CNN).
- `λ` is a weight that balances the two terms, often set to `1` or tuned.

For one-stage detectors such as YOLO:

```text
L = λ_coord * L_loc + λ_obj * L_conf + L_cls
```

- `L_coord` is localisation loss (CIoU in newer YOLO versions, MSE in YOLOv1-v3).
- `L_conf` is objectness confidence loss.
- `L_cls` is classification loss.

---

## 11. Code: compute IoU-based losses

```python
import torch

def box_iou(box_a, box_b):
    """
    box = [x1, y1, x2, y2]
    Returns IoU for one pair of boxes.
    """
    inter_x1 = max(box_a[0], box_b[0])
    inter_y1 = max(box_a[1], box_b[1])
    inter_x2 = min(box_a[2], box_b[2])
    inter_y2 = min(box_a[3], box_b[3])

    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])

    union_area = area_a + area_b - inter_area
    return inter_area / union_area if union_area > 0 else 0.0

def giou_loss(pred, true):
    """
    pred, true: [x1, y1, x2, y2]
    """
    inter_x1 = max(pred[0], true[0])
    inter_y1 = max(pred[1], true[1])
    inter_x2 = min(pred[2], true[2])
    inter_y2 = min(pred[3], true[3])

    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    area_p = (pred[2] - pred[0]) * (pred[3] - pred[1])
    area_t = (true[2] - true[0]) * (true[3] - true[1])

    union_area = area_p + area_t - inter_area
    iou = inter_area / union_area if union_area > 0 else 0.0

    # Smallest enclosing box
    c_x1 = min(pred[0], true[0])
    c_y1 = min(pred[1], true[1])
    c_x2 = max(pred[2], true[2])
    c_y2 = max(pred[3], true[3])
    c_area = (c_x2 - c_x1) * (c_y2 - c_y1)

    giou = iou - (c_area - union_area) / c_area
    return 1 - giou

pred  = [10, 10, 60, 60]
true  = [30, 30, 80, 80]

print("IoU loss:", 1 - box_iou(pred, true))
print("GIoU loss:", giou_loss(pred, true))
```

---

## 12. Summary

- A **localisation loss** measures the difference between a predicted box and the ground-truth box.
- **Smooth L1** is robust and commonly used in two-stage detectors.
- **IoU loss** is geometric and matches the evaluation metric, but has no gradient when boxes do not overlap.
- **GIoU** handles the no-overlap case by using the enclosing box.
- **DIoU** adds a centre-distance term for faster convergence.
- **CIoU** also penalises aspect-ratio differences and is used in modern YOLO.
- Real detectors combine localisation, classification, and confidence losses with weights.

**Next:** [Part 6: Region-Based Object Detectors]({{ site.baseurl }}/topics/computer-vision-region-based-detectors/)
