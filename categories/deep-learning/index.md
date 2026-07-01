---
layout: category
title: Deep Learning
category: Deep Learning
---

Learn deep learning from scratch using one consistent, real-world example: a spam email classifier. Every tutorial below uses the same email features and the same PyTorch code style, so you can focus on the ideas without switching examples.

**Recommended Learning Path:**

1. **[Part 1: Understanding Neurons and Neural Networks]({{ site.baseurl }}/topics/understanding-neurons-and-neural-networks)** — Turn a real email into numbers, multiply by weights, add a bias, apply sigmoid, and produce a spam probability. Includes a neural network diagram.
2. **[Part 2: From Machine Learning to Deep Learning]({{ site.baseurl }}/topics/from-machine-learning-to-deep-learning)** — Compare hand-crafted spam features with learned features, and see why hidden layers and non-linearity matter.
3. **[Part 3: Tensors and Tensor Operations]({{ site.baseurl }}/topics/tensors-and-tensor-operations)** — The same email features as tensors: shapes, batches, matrix multiplication, broadcasting, and GPU movement.
4. **[Part 4: Data Handling with Dataset and DataLoader]({{ site.baseurl }}/topics/data-handling-with-dataset-and-dataloader)** — Build a spam `Dataset`, create batches, shuffle, split train/val/test, and normalise features.
5. **[Part 5: Parameters in PyTorch]({{ site.baseurl }}/topics/parameters-in-pytorch)** — Weights, biases, `requires_grad`, parameter counting, freezing, initialisation, saving, and loading using the spam model.
6. **[Part 6: Forward and Backward Propagation]({{ site.baseurl }}/topics/forward-and-backward-propagation)** — A worked numerical example showing exactly how forward prediction and backpropagation with the chain rule update a two-layer spam model.
7. **[Part 7: Cognitive Analogies — Brain-inspired Learning]({{ site.baseurl }}/topics/cognitive-analogies-brain-inspired-learning)** — How spam detection mirrors neurons, synapses, memory, attention, and generalisation in the brain.
8. **[Part 8: Deep Learning Cheat Sheet]({{ site.baseurl }}/topics/deep-learning-cheat-sheet)** — Formulas, memory tricks, and quick reference, all using the spam example.
9. **[Part 9: Convolutional Neural Networks (CNNs)]({{ site.baseurl }}/topics/convolutional-neural-networks)** — Moves from email features to images: convolution, activation, feature maps, padding, and pooling, explained from zero with diagrams, then a full layer-by-layer walkthrough of the real VGG16 architecture.
10. **[Part 10: Advanced Convolutional Neural Networks]({{ site.baseurl }}/topics/advanced-convolutional-neural-networks)** — A simple second CNN topic covering the degradation problem, data augmentation, dropout, batch normalization, residual connections, 1x1 bottleneck convolutions, global average pooling, CNN backpropagation through filters, feature maps, ReLU, and pooling, transfer learning, and freezing layers — with diagrams throughout.

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

All guides use friendly explanations, real-world examples, and working PyTorch code you can run yourself.
