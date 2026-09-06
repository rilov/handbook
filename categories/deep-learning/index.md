---
layout: category
title: Deep Learning
category: Deep Learning
show_topic_list: false
---

Learn deep learning from scratch using one consistent, real-world example: a spam email classifier. Every tutorial below uses the same email features and the same PyTorch code style, so you can focus on the ideas without switching examples.

**Recommended Learning Path:**

1. **[Part 1: Understanding Neurons and Neural Networks]({% link _topics/Understanding Neurons and Neural Networks - A Friendly Guide.md %})** — Turn a real email into numbers, multiply by weights, add a bias, apply sigmoid, and produce a spam probability. Includes a neural network diagram.
2. **[Part 2: From Machine Learning to Deep Learning]({% link _topics/From Machine Learning to Deep Learning - A Friendly Guide.md %})** — Compare hand-crafted spam features with learned features, and see why hidden layers and non-linearity matter.
3. **[Part 3: Tensors and Tensor Operations]({% link _topics/Tensors and Tensor Operations - A Friendly Guide.md %})** — The same email features as tensors: shapes, batches, matrix multiplication, broadcasting, and GPU movement.
4. **[Part 4: Data Handling with Dataset and DataLoader]({% link _topics/Data Handling with Dataset and DataLoader - A Friendly Guide.md %})** — Build a spam `Dataset`, create batches, shuffle, split train/val/test, and normalise features.
5. **[Part 5: Parameters in PyTorch]({% link _topics/Parameters in PyTorch - A Friendly Guide.md %})** — Weights, biases, `requires_grad`, parameter counting, freezing, initialisation, saving, and loading using the spam model.
6. **[Part 6: Forward and Backward Propagation]({% link _topics/Forward and Backward Propagation - A Friendly Guide.md %})** — A worked numerical example showing exactly how forward prediction and backpropagation with the chain rule update a two-layer spam model.
7. **[Part 7: Cognitive Analogies — Brain-inspired Learning]({% link _topics/Cognitive Analogies - Brain-inspired Learning.md %})** — How spam detection mirrors neurons, synapses, memory, attention, and generalisation in the brain.
8. **[Part 8: Deep Learning Cheat Sheet]({{ site.baseurl }}/topics/deep-learning-cheat-sheet)** — Formulas, memory tricks, and quick reference, all using the spam example.
9. **[Part 9: Convolutional Neural Networks (CNNs)]({% link _topics/Convolutional Neural Networks - A Friendly Guide.md %})** — Moves from email features to images: convolution, activation, feature maps, padding, and pooling, explained from zero with diagrams, then a full layer-by-layer walkthrough of the real VGG16 architecture.
10. **[Part 10: Advanced Convolutional Neural Networks]({% link _topics/Advanced Convolutional Neural Networks - A Friendly Guide.md %})** — A simple second CNN topic covering the degradation problem, data augmentation, dropout, batch normalization, residual connections, 1x1 bottleneck convolutions, global average pooling, CNN backpropagation through filters, feature maps, ReLU, and pooling, transfer learning, and freezing layers — with diagrams throughout.
11. **[Part 11: CNN Training Pipeline, Transfer Learning, and Visualization]({% link _topics/CNN Training Pipeline Transfer Learning and Visualization - A Friendly Guide.md %})** — The full CNN model design workflow: problem exploration, data collection and annotation, preprocessing (noise removal, resizing, normalization), augmentation, train/validation/test splits, training from scratch versus transfer learning versus fine-tuning, and CNN visualization with Grad-CAM to understand what the model actually learned.
12. **[Part 12: Building a CNN End-to-End — CIFAR-10 with PyTorch]({% link _topics/Building a CNN End-to-End CIFAR-10 with PyTorch - A Friendly Guide.md %})** — A complete hands-on walkthrough: load and preprocess CIFAR-10, define a CNN with batch normalization and dropout, write the training and validation loop, plot learning curves, and evaluate with accuracy, confusion matrix, and classification report.
13. **[Part 13: CNN Applications]({% link _topics/CNN Applications Image Classification Object Detection Segmentation - A Friendly Guide.md %})** — Overview of the five main CNN application areas: image classification, object detection (YOLO, Faster R-CNN), image segmentation (U-Net, Mask R-CNN), facial recognition (FaceNet, ArcFace), and optical character recognition (OCR/CRNN) — with real-world examples and key architectures for each.
14. **[Part 14: Faster R-CNN and Region Proposal Networks]({% link _topics/Faster R-CNN and Region Proposal Networks - A Friendly Guide.md %})** — A paper-style walkthrough of the R-CNN family: why region proposals are needed, how Fast R-CNN shared a feature map, and how Faster R-CNN's RPN makes proposals nearly free.
15. **[Part 15: RNN — Recurrent Neural Networks]({% link _topics/RNN Recurrent Neural Networks - A Friendly Guide.md %})** — Why normal networks fail on sequences, how hidden states carry memory, backpropagation through time, vanishing/exploding gradients, and gradient clipping.
16. **[Part 16: LSTM and GRU]({% link _topics/LSTM and GRU - A Friendly Guide.md %})** — Gated recurrent networks, the cell state highway, LSTM's three gates, GRU's update and reset gates, and how to choose between them.
17. **[Part 17: RNN Use Cases]({% link _topics/RNN Use Cases - Time Series Sequence Classification - A Friendly Guide.md %})** — Time-series forecasting, sequence classification, sequence labelling, language modelling, machine translation, padding, masking, and when to use `h_n` vs `output`.
18. **[Part 18: Activation and Output Functions]({% link _topics/Activation and Output Functions - A Friendly Guide.md %})** — Softmax, sigmoid, log-softmax, sparsemax, argmax, ReLU, and tanh: formulas, output ranges, and a decision table for choosing the right one.

**What You'll Learn:**

- How a real email becomes a tensor of numbers
- How a single neuron computes a weighted sum, adds a bias, and applies an activation
- How sigmoid turns a raw score into a spam probability
- Why hidden layers can learn feature combinations like "many links + unknown sender"
- The difference between traditional ML feature engineering and deep learning feature learning
- How tensors represent emails, weights, and biases in PyTorch
- How to batch, shuffle, split, and normalise data with `Dataset` and `DataLoader`
- How PyTorch creates, tracks, and updates parameters automatically
- How forward and backward propagation work step by step with the chain rule
- How deep learning mirrors brain concepts like memory, attention, and generalisation
- Memory tricks for every formula and concept
- Why images need convolution instead of fully connected layers, and how kernels, feature maps, padding, and pooling work
- The exact output-size and parameter-count formulas for convolutional layers, plus a full walkthrough of VGG16's 16 weight layers and ~138 million parameters
- How advanced CNNs improve training with augmentation, dropout, batch normalization, residual connections, global average pooling, 1x1 bottleneck convolutions, CNN backpropagation, and transfer learning
- How to build the full CNN training pipeline: data collection, annotation, preprocessing, normalization, augmentation, and splitting
- When to train from scratch, when to use transfer learning, and when to fine-tune
- How Grad-CAM visualizes where a CNN looks and why this matters for catching shortcut learning
- How to build and train a complete CNN on CIFAR-10 in PyTorch from data loading to evaluation
- The five main CNN application areas: classification, detection, segmentation, facial recognition, and OCR — what each task is, how CNNs solve it, and key architectures

All guides use friendly explanations, real-world examples, and working PyTorch code you can run yourself.
