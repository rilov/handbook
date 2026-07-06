---
layout: topic
title: "Part 12: Building a CNN End-to-End — CIFAR-10 with PyTorch"
category: Deep Learning
order: 12
tags:
  - deep-learning
  - cnn
  - computer-vision
  - cifar-10
  - pytorch
  - image-classification
  - training-loop
  - evaluation
  - beginners
  - friendly
summary: A complete hands-on walkthrough of building, training, and evaluating a CNN on the CIFAR-10 dataset using PyTorch. Covers loading and preprocessing the dataset, defining a CNN architecture, writing the training loop with validation, and evaluating with accuracy, confusion matrix, and classification report.
---

# Part 12: Building a CNN End-to-End — CIFAR-10 with PyTorch

## What this guide covers

The previous guides explained how CNNs work and how to design the training pipeline.

This guide puts it all together in one working PyTorch project using **CIFAR-10** — the standard beginner CNN benchmark dataset.

By the end you will have:

```text
✓ Loaded and preprocessed CIFAR-10
✓ Defined a CNN model
✓ Trained it with a validation loop
✓ Evaluated it with accuracy, confusion matrix, and classification report
```

---

## 1. What is CIFAR-10?

**CIFAR-10** is a dataset of 60,000 small color images across 10 classes.

| Property | Value |
|---|---|
| Total images | 60,000 |
| Training images | 50,000 |
| Test images | 10,000 |
| Image size | 32 × 32 pixels |
| Channels | 3 (RGB color) |
| Classes | 10 |

The 10 classes are:

```text
0: airplane    1: automobile  2: bird    3: cat   4: deer
5: dog         6: frog        7: horse   8: ship  9: truck
```

Each class has exactly 6,000 images, so the dataset is **balanced**.

CIFAR-10 is small enough to train quickly on a laptop but complex enough to need a real CNN — simple fully connected networks do not work well on it.

---

## 2. Setup

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
```

Check if a GPU is available:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
```

---

## 3. Load and preprocess CIFAR-10

### Transforms

Training images get augmentation. Validation and test images get only normalization.

The normalization values are the CIFAR-10 channel means and standard deviations:

```python
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.4914, 0.4822, 0.4465],
        std=[0.2470, 0.2435, 0.2616]
    ),
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.4914, 0.4822, 0.4465],
        std=[0.2470, 0.2435, 0.2616]
    ),
])
```

### Download and split

```python
full_train = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=train_transform
)
test_set = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=test_transform
)

# Split training into train (45,000) and validation (5,000)
train_size = 45000
val_size   = 5000
train_set, val_set = random_split(full_train, [train_size, val_size])

# Apply test transform to validation set
val_set.dataset.transform = test_transform
```

### DataLoaders

```python
train_loader = DataLoader(train_set, batch_size=64, shuffle=True,  num_workers=2)
val_loader   = DataLoader(val_set,   batch_size=64, shuffle=False, num_workers=2)
test_loader  = DataLoader(test_set,  batch_size=64, shuffle=False, num_workers=2)

classes = ['airplane','automobile','bird','cat','deer',
           'dog','frog','horse','ship','truck']
```

---

## 4. Define the CNN model

This is a simple CNN with three convolution blocks followed by a small classifier.

```python
class CIFAR10CNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),       # 32x32 → 16x16
            nn.Dropout(0.25),

            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),       # 16x16 → 8x8
            nn.Dropout(0.25),

            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),       # 8x8 → 4x4
            nn.Dropout(0.25),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 10),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
```

### Why this shape?

```text
Input:      3 × 32 × 32
Block 1:   32 × 16 × 16  (after MaxPool)
Block 2:   64 ×  8 ×  8  (after MaxPool)
Block 3:  128 ×  4 ×  4  (after MaxPool)
Flatten:  128 × 4 × 4 = 2048
Dense:    256
Output:   10
```

Count the trainable parameters:

```python
model = CIFAR10CNN().to(device)
total = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Trainable parameters: {total:,}")
```

---

## 5. Loss function and optimizer

```python
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)
```

- **CrossEntropyLoss** — standard for multiclass classification. Combines softmax and log loss.
- **Adam** — adaptive optimizer, works well as a default.
- **StepLR** — halves the learning rate every 10 epochs to fine-tune later.

---

## 6. Training loop

```python
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, total = 0, 0, 0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
        total += labels.size(0)

    avg_loss = total_loss / len(loader)
    accuracy = 100.0 * correct / total
    return avg_loss, accuracy


def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss, correct, total = 0, 0, 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()
            total += labels.size(0)

    avg_loss = total_loss / len(loader)
    accuracy = 100.0 * correct / total
    return avg_loss, accuracy
```

### Run training

```python
num_epochs = 30
train_losses, val_losses = [], []
train_accs, val_accs = [], []

for epoch in range(1, num_epochs + 1):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    val_loss,   val_acc   = evaluate(model, val_loader, criterion, device)
    scheduler.step()

    train_losses.append(train_loss)
    val_losses.append(val_loss)
    train_accs.append(train_acc)
    val_accs.append(val_acc)

    print(f"Epoch {epoch:2d}/{num_epochs} | "
          f"Train loss: {train_loss:.4f}, acc: {train_acc:.1f}% | "
          f"Val loss: {val_loss:.4f}, acc: {val_acc:.1f}%")
```

---

## 7. Plot training curves

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(train_losses, label='Train')
ax1.plot(val_losses,   label='Validation')
ax1.set_title('Loss')
ax1.set_xlabel('Epoch')
ax1.legend()

ax2.plot(train_accs, label='Train')
ax2.plot(val_accs,   label='Validation')
ax2.set_title('Accuracy (%)')
ax2.set_xlabel('Epoch')
ax2.legend()

plt.tight_layout()
plt.show()
```

What to look for:

```text
Good: train loss ↓, val loss ↓ together
Overfitting: train loss ↓, val loss ↑ (gap opens up)
Underfitting: both losses stay high
```

---

## 8. Evaluate on the test set

```python
test_loss, test_acc = evaluate(model, test_loader, criterion, device)
print(f"\nTest accuracy: {test_acc:.1f}%")
```

### Full classification report

```python
all_preds, all_labels = [], []

model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        outputs = model(images)
        _, predicted = outputs.max(1)
        all_preds.extend(predicted.cpu().numpy())
        all_labels.extend(labels.numpy())

print(classification_report(all_labels, all_preds, target_names=classes))
```

This prints precision, recall, and F1 for every class.

### Confusion matrix

```python
cm = confusion_matrix(all_labels, all_preds)
print(cm)
```

Reading the confusion matrix:

```text
Row = actual class
Column = predicted class
Diagonal = correct predictions
Off-diagonal = mistakes
```

If the model confuses cats and dogs often, you will see high values in that off-diagonal cell.

---

## 9. Save and load the model

```python
# Save
torch.save(model.state_dict(), 'cifar10_cnn.pth')

# Load
model_loaded = CIFAR10CNN().to(device)
model_loaded.load_state_dict(torch.load('cifar10_cnn.pth'))
model_loaded.eval()
```

---

## 10. Predict on a single image

```python
import PIL.Image

def predict(model, image_path, transform, classes, device):
    img = PIL.Image.open(image_path).convert('RGB')
    tensor = transform(img).unsqueeze(0).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)
        conf, pred = probs.max(1)

    print(f"Predicted: {classes[pred.item()]}  ({conf.item()*100:.1f}% confidence)")
```

---

## 11. Expected results

With this architecture and 30 epochs:

| Metric | Typical value |
|---|---|
| Test accuracy | ~80–85% |
| Training time (CPU) | ~30–60 min |
| Training time (GPU) | ~3–5 min |

Accuracy above 90% requires deeper networks, more augmentation, or techniques like ResNet or learning rate warm-up.

---

## 12. Summary

```text
Load CIFAR-10
→ apply augmentation to training set only
→ split into train / validation / test
→ define CNN (conv blocks + classifier)
→ train with CrossEntropyLoss and Adam
→ monitor val loss each epoch
→ evaluate on test set
→ check confusion matrix per class
```

| Step | Code |
|---|---|
| Download dataset | `torchvision.datasets.CIFAR10` |
| Augment training | `transforms.RandomHorizontalFlip`, `RandomCrop` |
| Normalize | `transforms.Normalize` with CIFAR-10 stats |
| Define model | `nn.Conv2d`, `nn.BatchNorm2d`, `nn.MaxPool2d`, `nn.Dropout` |
| Train | `loss.backward()`, `optimizer.step()` |
| Evaluate | `torch.no_grad()`, `classification_report` |

---

## What to read next

- [Part 11: CNN Training Pipeline, Transfer Learning, and Visualization]({{ site.baseurl }}/topics/cnn-training-pipeline-transfer-learning-and-visualization) — the full pipeline explained conceptually
- [Part 13: CNN Applications]({{ site.baseurl }}/topics/cnn-applications-image-classification-object-detection-segmentation) — image classification, object detection, segmentation, facial recognition, OCR
