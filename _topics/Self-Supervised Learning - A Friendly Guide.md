---
title: "22. Self-Supervised Learning - A Friendly Guide"
category: Machine Learning
order: 22
tags:
  - machine-learning
  - self-supervised-learning
  - pre-training
  - contrastive-learning
  - transformers
  - nlp
  - computer-vision
  - beginners
  - friendly
summary: A beginner-friendly guide to self-supervised learning — how models train themselves on unlabelled data by predicting parts of the input from other parts. Covers masked prediction, contrastive learning, and the role of SSL in GPT and BERT.
---

# Self-Supervised Learning

## Teaching a model without any human-provided labels

Training a large language model like GPT or a vision model like CLIP requires learning from billions of examples. Labelling billions of examples by hand is impossible. So how do these models learn?

The answer is **self-supervised learning (SSL)**: the model creates its own labels automatically from the raw data — no human annotation required.

This tutorial covers:

1. The core idea — generating labels from data itself.
2. Masked prediction — how BERT learns language.
3. Next token prediction — how GPT learns to generate text.
4. Contrastive learning — how vision models learn without labels.
5. The pre-train → fine-tune workflow.
6. Python examples.

---

## 1. The core idea — labels from the data itself

In supervised learning, a human labels each example:

```
Email text  →  "spam" or "not spam"   (human labelled)
```

In self-supervised learning, the data labels itself:

```
"The cat sat on the ___"  →  "mat"    (label comes from the sentence itself)
"___ cat sat on the mat"  →  "The"    (label comes from the sentence itself)
```

The model is trained to fill in missing or predicted parts. By solving millions of these automatic puzzles, the model develops deep understanding of language, images, or audio — without a single human label.

> **Memory trick:** Self-supervised learning is like a student who creates their own practice tests from a textbook. The textbook is the unlabelled data. The questions and answers are generated automatically from the text itself.

---

## 2. Masked prediction — how BERT works

**BERT** (Bidirectional Encoder Representations from Transformers) is pre-trained using **masked language modelling**:

1. Take a sentence: `"The spam email contained a free prize offer"`
2. Randomly mask 15% of the words: `"The spam email contained a [MASK] prize offer"`
3. Train the model to predict the masked word: `"free"`

The labels (`"free"`) come directly from the original text — no human needed.

After training on billions of sentences this way, BERT develops a rich understanding of language context. It can then be **fine-tuned** on a small labelled dataset (e.g., 1,000 spam/not-spam examples) for a specific task.

```python
# Using a pre-trained BERT model for masked prediction
from transformers import pipeline

# This model was pre-trained with masked language modelling
fill_mask = pipeline("fill-mask", model="bert-base-uncased")

result = fill_mask("The email contained a [MASK] offer.")
for r in result[:3]:
    print(f"  '{r['token_str']}' — score: {r['score']:.3f}")
# Output:
#   'special' — score: 0.142
#   'limited' — score: 0.098
#   'free'    — score: 0.087
```

---

## 3. Next token prediction — how GPT works

**GPT** uses **causal language modelling**: predict the next word given all previous words.

```
Input:  "The spam email contained a free"
Target: "prize"

Input:  "The spam email contained a free prize"
Target: "offer"
```

Again — the labels (`"prize"`, `"offer"`) come directly from the text. The model sees billions of sentences and learns to predict what comes next. This forces it to understand grammar, facts, reasoning, and context.

```python
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")
result = generator("The spam email contained", max_new_tokens=10)
print(result[0]['generated_text'])
```

---

## 4. Contrastive learning — self-supervised vision

For images there is no natural "next token." Instead, **contrastive learning** creates labels by comparing views of the same image:

1. Take one image (e.g., a cat photo).
2. Create two augmented views: rotate it, crop it, change brightness.
3. Train the model so the two views of the **same** image have similar representations, while views of **different** images have different representations.

```
Cat photo → Crop + flip  →  Representation A  ┐
                                                ├→ Pull together (same image)
Cat photo → Rotate + brighten → Representation B ┘

Cat photo vs Dog photo → Representations → Push apart (different images)
```

No human labels needed. The "label" is simply: these two views are of the same image.

```python
# Conceptual SimCLR-style contrastive learning structure
import torch
import torch.nn as nn
import torchvision.transforms as T

# Two random augmentations of the same image
augment = T.Compose([
    T.RandomResizedCrop(32),
    T.RandomHorizontalFlip(),
    T.ColorJitter(0.4, 0.4, 0.4),
    T.ToTensor(),
])

# For a batch of images, create two augmented views
def get_views(images):
    view1 = torch.stack([augment(img) for img in images])
    view2 = torch.stack([augment(img) for img in images])
    return view1, view2

# The contrastive loss (NT-Xent) pulls same-image pairs together
# and pushes different-image pairs apart in the embedding space.
# After pre-training, the encoder is fine-tuned with labels.
```

Popular contrastive methods:

| Method | Domain | Key idea |
|--------|--------|----------|
| SimCLR | Images | Two augmented views, NT-Xent loss |
| MoCo | Images | Momentum encoder for stable negatives |
| CLIP | Image + Text | Image and caption should be similar |
| wav2vec | Audio | Predict future audio representations |

---

## 5. The pre-train → fine-tune workflow

This is the defining pattern of modern machine learning:

```
Step 1 — Pre-train with SSL (no labels, massive data)
         ↓
   Model learns general representations
   (language structure, visual features, etc.)
         ↓
Step 2 — Fine-tune with supervised learning (small labelled dataset)
         ↓
   Model adapts to your specific task
   (spam detection, sentiment, image classification)
```

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer
import torch

# Step 1 — Load a model pre-trained with SSL (masked language modelling)
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Step 2 — Fine-tune on small labelled spam dataset
emails = [
    "free prize win now click here",
    "claim your reward today",
    "meeting agenda tomorrow 3pm",
    "project deadline report attached",
]
labels = [1, 1, 0, 0]   # 1=spam, 0=not spam

# Tokenise
encodings = tokenizer(emails, truncation=True, padding=True, return_tensors='pt')

class SpamDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __len__(self): return len(self.labels)
    def __getitem__(self, idx):
        item = {k: v[idx] for k, v in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

dataset = SpamDataset(encodings, labels)

# Fine-tune — only a few steps needed because BERT already understands language
args = TrainingArguments(output_dir='./spam_model', num_train_epochs=3,
                         per_device_train_batch_size=2, logging_steps=1)
trainer = Trainer(model=model, args=args, train_dataset=dataset)
trainer.train()
```

The key insight: **BERT already knows what "free prize win" means** from SSL pre-training. Fine-tuning with just 100 labelled spam examples can be enough for good performance.

---

## 6. SSL vs other learning types

| Aspect | Supervised | Unsupervised | Self-Supervised |
|--------|-----------|--------------|-----------------|
| Labels needed | Yes — all examples | No | No — labels from data |
| Data needed | Moderate | Large | Very large |
| Task | Specific | General patterns | General representations |
| Fine-tuning possible | N/A | Hard | Yes — easily |
| Examples | Spam classifier | K-Means clustering | GPT, BERT, CLIP |

---

## 7. Where self-supervised learning is used today

| Application | SSL method | Fine-tuned for |
|-------------|-----------|----------------|
| GPT-4 / ChatGPT | Next token prediction | Instruction following (SFT + RLHF) |
| BERT / RoBERTa | Masked token prediction | Classification, NER, QA |
| CLIP | Image-text contrastive | Zero-shot image classification |
| wav2vec 2.0 | Audio contrastive | Speech recognition |
| DINO / MAE | Masked image patches | Image classification, detection |

---

## Summary

- Self-supervised learning creates labels **automatically from the data itself** — no human annotation needed.
- **Masked prediction** (BERT): hide parts of the input and predict them.
- **Next token prediction** (GPT): predict what comes next in a sequence.
- **Contrastive learning** (SimCLR, CLIP): pull together representations of the same data, push apart different data.
- The **pre-train → fine-tune** workflow lets a model trained on billions of unlabelled examples be adapted to a specific task with just hundreds or thousands of labelled examples.
- SSL is the foundation of modern large language models and vision models.
