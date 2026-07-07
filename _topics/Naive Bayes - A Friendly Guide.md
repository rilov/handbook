---
title: "18. Naive Bayes - A Friendly Guide"
category: Machine Learning
order: 18
tags:
  - machine-learning
  - naive-bayes
  - classification
  - probability
  - text-classification
  - spam-detection
  - beginners
  - friendly
summary: A complete beginner-friendly guide to Naive Bayes. Learn how probability drives classification, why the "naive" assumption works in practice, and build a spam detector step by step in Python.
---

# Naive Bayes

## The algorithm that reads your email

Every time your email client moves a message to the spam folder, there is a good chance Naive Bayes is involved. It is one of the oldest, simplest, and most battle-tested classification algorithms in machine learning — and it is built entirely on one idea from high school probability.

This tutorial covers:

1. The intuition — what does "probability of spam" actually mean?
2. Bayes' Theorem in plain English.
3. The "naive" assumption and why it works.
4. Types of Naive Bayes.
5. Step-by-step worked example.
6. Full Python demonstration.
7. When to use it and when not to.

---

## 1. The intuition

Imagine you receive an email with the subject line: *"Congratulations! You have won a free iPhone."*

You have seen thousands of emails before. You know that:

- The word "free" appears in 80% of spam emails but only 5% of normal emails.
- The word "won" appears in 60% of spam but only 2% of normal emails.
- The word "Congratulations" appears in 55% of spam but 10% of normal emails.

Given these observations, what is the probability this new email is spam?

Naive Bayes answers exactly this question — systematically, using probability.

> **Memory trick:** Naive Bayes is like a detective who looks at individual clues (words) and combines the evidence to reach a verdict (spam or not spam).

---

## 2. Bayes' Theorem — the engine

Bayes' Theorem tells us how to update our belief about something when we see new evidence.

```
P(spam | words) = P(words | spam) × P(spam)
                  ─────────────────────────
                         P(words)
```

In plain English:

- **P(spam | words)** — probability this email is spam, given the words we see. This is what we want.
- **P(words | spam)** — how likely these words are if the email IS spam. Learned from training data.
- **P(spam)** — how common spam is overall. Also learned from training data.
- **P(words)** — overall probability of seeing these words. The same for all classes, so we can ignore it when comparing.

We do not need to calculate the bottom. We just compare:

```
P(spam | words)     vs     P(not spam | words)
```

Whichever is higher wins.

---

## 3. The "naive" assumption

Here is where the "naive" part comes in.

Computing `P(words | spam)` for a whole sentence is hard — you would need to have seen that exact combination of words before. Instead, Naive Bayes makes a simplifying assumption:

> **Each word is independent of every other word.**

So instead of `P("free won Congratulations" | spam)`, we compute:

```
P("free" | spam) × P("won" | spam) × P("Congratulations" | spam)
```

This is "naive" because words are obviously not independent — "New York" is much more likely as a pair than as two random words. But in practice, this assumption rarely hurts much and makes the algorithm incredibly fast.

> **Memory trick:** Naive Bayes treats each word like a separate witness testifying independently. Even if the witnesses are related, their combined testimony still points to the right answer most of the time.

---

## 4. Types of Naive Bayes

| Type | Use case | Input |
|------|----------|-------|
| **Multinomial NB** | Text classification — word counts | Word frequencies |
| **Bernoulli NB** | Short text, binary features — word present or not | 0 or 1 per word |
| **Gaussian NB** | Continuous features like height, temperature | Real numbers |

For spam detection with word counts, **Multinomial NB** is the standard choice.

---

## 5. Step-by-step worked example

### Training data

| Email | Words | Label |
|-------|-------|-------|
| "free prize win" | free, prize, win | spam |
| "free offer claim" | free, offer, claim | spam |
| "meeting tomorrow agenda" | meeting, tomorrow, agenda | not spam |
| "project update tomorrow" | project, update, tomorrow | not spam |

**Step 1 — Calculate prior probabilities**

```
P(spam)     = 2/4 = 0.5
P(not spam) = 2/4 = 0.5
```

**Step 2 — Calculate word likelihoods from training data**

Total words in spam emails: free, prize, win, free, offer, claim = 6 words

```
P("free"  | spam) = 2/6 = 0.33
P("prize" | spam) = 1/6 = 0.17
P("win"   | spam) = 1/6 = 0.17
P("offer" | spam) = 1/6 = 0.17
P("claim" | spam) = 1/6 = 0.17
```

Total words in not-spam emails: 6 words

```
P("free"     | not spam) = 0/6 ≈ 0.0  (we add smoothing — see below)
P("tomorrow" | not spam) = 2/6 = 0.33
P("meeting"  | not spam) = 1/6 = 0.17
```

**Step 3 — Predict a new email: "free win tomorrow"**

```
Score(spam)     = P(spam) × P("free"|spam) × P("win"|spam) × P("tomorrow"|spam)
                = 0.5 × 0.33 × 0.17 × ~0.01   (tomorrow rarely appears in spam)
                = very small positive number

Score(not spam) = P(not spam) × P("free"|not spam) × P("win"|not spam) × P("tomorrow"|not spam)
                = 0.5 × ~0.01 × ~0.01 × 0.33
                = also very small
```

We compare which score is higher and assign that class.

### Laplace smoothing — fixing zero probabilities

If a word never appeared in training spam emails, `P(word | spam) = 0`, which would make the entire product zero no matter what other words say. That is too harsh.

**Laplace smoothing** adds 1 to every word count:

```
P(word | class) = (count of word in class + 1)
                  ─────────────────────────────
                  (total words in class + vocabulary size)
```

This ensures no probability is ever exactly zero.

---

## 6. Full Python demonstration

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Training data
emails = [
    "free prize win now",
    "claim your free offer today",
    "win a free iPhone click here",
    "limited offer free gift",
    "meeting at 3pm tomorrow",
    "project update attached please review",
    "agenda for tomorrow meeting",
    "quarterly report due Friday",
    "free lunch meeting agenda",
    "please review the attached report",
]
labels = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
# 1 = spam, 0 = not spam

# Step 1 — Convert text to word count vectors
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

# Step 2 — Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.3, random_state=42
)

# Step 3 — Train Naive Bayes
model = MultinomialNB()
model.fit(X_train, y_train)

# Step 4 — Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=["not spam", "spam"]))

# Step 5 — Predict new emails
new_emails = [
    "free offer win prize now",
    "meeting notes from today attached",
]
X_new = vectorizer.transform(new_emails)
predictions = model.predict(X_new)
probs = model.predict_proba(X_new)

for email, pred, prob in zip(new_emails, predictions, probs):
    label = "SPAM" if pred == 1 else "NOT SPAM"
    print(f"\n'{email}'")
    print(f"  → {label}  (spam prob: {prob[1]:.2f})")
```

### Understanding word importance

```python
import numpy as np

# Which words are most associated with spam?
feature_names = vectorizer.get_feature_names_out()
spam_log_probs = model.feature_log_prob_[1]   # class 1 = spam

top_spam_words = np.argsort(spam_log_probs)[-10:]
print("Top words for spam:")
for idx in reversed(top_spam_words):
    print(f"  '{feature_names[idx]}': log-prob {spam_log_probs[idx]:.2f}")
```

---

## 7. Gaussian Naive Bayes — for continuous features

When features are continuous numbers (like email length, number of links), use Gaussian NB, which assumes each feature follows a bell curve within each class:

```python
from sklearn.naive_bayes import GaussianNB
import numpy as np

# Features: [suspicious_word_count, link_count, message_length]
X = np.array([
    [5, 3, 42],   # spam
    [4, 2, 35],   # spam
    [6, 4, 28],   # spam
    [0, 0, 120],  # not spam
    [1, 0, 95],   # not spam
    [0, 1, 110],  # not spam
])
y = [1, 1, 1, 0, 0, 0]

model = GaussianNB()
model.fit(X, y)

# Predict a new email
new = np.array([[3, 2, 50]])
print(model.predict(new))          # [1] → spam
print(model.predict_proba(new))    # [[0.12, 0.88]] → 88% spam
```

---

## 8. When to use Naive Bayes

**Good fit:**
- Text classification (spam, sentiment, topic labelling)
- Large vocabulary with many features
- You need a fast baseline before trying complex models
- Small training datasets — NB generalises well with little data
- Real-time prediction — NB is extremely fast to score

**Not ideal for:**
- Features with strong dependencies (e.g., word order matters — "not good" vs "good not")
- Continuous features with complex distributions
- Tasks where the independence assumption is badly violated

| Compared to | Naive Bayes advantage |
|---|---|
| Logistic Regression | Faster training, works with tiny datasets |
| Decision Trees | Less prone to overfitting on small data |
| SVM | Much faster, easier to interpret |
| Deep Learning | Tiny model, instant training, explainable |

---

## 9. Common mistakes

| Mistake | Fix |
|---|---|
| Forgetting to apply `CountVectorizer` or `TfidfVectorizer` | Text must be converted to numbers first |
| Using `MultinomialNB` with negative values | Use `GaussianNB` for raw continuous features |
| Not applying Laplace smoothing | `MultinomialNB` applies it by default via `alpha=1.0` |
| Treating NB as your final model | Use it as a fast baseline, then try stronger models |

---

## 10. Try it yourself

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

# Try TF-IDF instead of raw counts
vectorizer = TfidfVectorizer(stop_words='english')

emails = [
    "free prize win now click here",
    "claim your reward today free",
    "win iPhone limited time offer",
    "schedule meeting tomorrow agenda",
    "project deadline Friday report",
    "review attached document please",
]
labels = [1, 1, 1, 0, 0, 0]

X = vectorizer.fit_transform(emails)
model = MultinomialNB(alpha=1.0)
model.fit(X, labels)

test = vectorizer.transform(["free iPhone win prize"])
print(model.predict(test))         # [1] → spam
print(model.predict_proba(test))   # confidence scores
```

Experiment: change `alpha` (the smoothing parameter) from `0.01` to `10.0` and see how it affects confidence scores on borderline emails.

---

## Summary

- Naive Bayes uses probability to classify. For each class it asks: "how likely is this input, given what we know about this class?"
- The "naive" assumption is that features are independent. It is wrong but it works surprisingly well.
- **Multinomial NB** — word counts in text. **Gaussian NB** — continuous numbers. **Bernoulli NB** — word present/absent.
- Laplace smoothing prevents zero probabilities from destroying the calculation.
- It is fast, interpretable, and works well even with small datasets.
- Use it as a strong baseline before investing in more complex models.
