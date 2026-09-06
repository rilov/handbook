---
layout: category
title: Computer Vision
category: Computer Vision
show_topic_list: false
---

Learn computer vision from the ground up: how images become numbers, what object detection and localisation mean, how bounding boxes are measured, and how modern detectors such as Faster R-CNN, YOLO, and SSD find objects in images.

**Recommended Learning Path:**

1. **[Part 1: Image Processing Fundamentals]({{ site.baseurl }}/topics/computer-vision-image-processing-fundamentals/)** — Pixels, colour models, image shapes, matrix operations, filters, convolution, and feature extraction — how a computer reads an image as numbers before it can understand it.
2. **[Part 2: Introduction]({{ site.baseurl }}/topics/computer-vision-introduction/)** — What computer vision is, why it is hard, the standard pipeline, and how it relates to deep learning.
3. **[Part 3: Object Detection Basics]({{ site.baseurl }}/topics/computer-vision-object-detection-basics/)** — Bounding boxes, coordinate formats, IoU, precision/recall, mAP, and the two-stage vs one-stage distinction.
4. **[Part 4: Loss in Object Localisation]({{ site.baseurl }}/topics/computer-vision-localisation-loss/)** — L1, L2, Smooth L1, IoU, GIoU, DIoU, and CIoU losses with formulas and code.
5. **[Part 5: Region-Based Detectors]({{ site.baseurl }}/topics/computer-vision-region-based-detectors/)** — R-CNN, Fast R-CNN, Faster R-CNN, the Region Proposal Network, and the limits of two-stage detectors.
6. **[Part 6: Anchor Boxes]({{ site.baseurl }}/topics/computer-vision-anchor-boxes/)** — What anchors are, how they are placed and matched to ground truth, and their role in RPN, YOLO, and SSD.
7. **[Part 7: One-Stage Detectors — YOLO and SSD]({{ site.baseurl }}/topics/computer-vision-yolo-ssd/)** — How YOLO and SSD work, how to decode YOLO output, and how non-maximum suppression produces final boxes.
8. **[Part 8: YOLO Evolution and YOLO11 Demo]({{ site.baseurl }}/topics/computer-vision-yolo11-demo/)** — The YOLO family from v1 to YOLO11, and a practical detection demo with `ultralytics`.

**Related Deep Learning topics:**

- [Part 9: Convolutional Neural Networks]({% link _topics/Convolutional Neural Networks - A Friendly Guide.md %}) — the backbone behind most vision models.
- [Part 13: CNN Applications]({% link _topics/CNN Applications Image Classification Object Detection Segmentation - A Friendly Guide.md %}) — broader computer-vision tasks including classification, segmentation, facial recognition, and OCR.
- [Part 14: Faster R-CNN and Region Proposal Networks]({% link _topics/Faster R-CNN and Region Proposal Networks - A Friendly Guide.md %}) — a deeper walk through the Faster R-CNN paper.
