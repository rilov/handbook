---
title: "Advanced Machine Learning: SVM and Naive Bayes - A Friendly Guide"
category: Machine Learning
order: 35
tags:
  - machine-learning
  - advanced-machine-learning
  - svm
  - support-vector-machines
  - naive-bayes
  - classification
  - kernels
  - bayes-theorem
  - beginners
  - friendly
summary: "A step-by-step beginner-friendly guide to two powerful classifiers: Support Vector Machines (SVM) and Naive Bayes. Learn margins, kernels, Bayes' theorem, and when to use each algorithm."
---

# Advanced Machine Learning: SVM and Naive Bayes

This guide covers two classic machine learning algorithms used for classification:

- **Support Vector Machine (SVM)** — finds the best boundary between classes.
- **Naive Bayes** — classifies using probability and Bayes' theorem.

Both are simple to explain, powerful in practice, and still used in real applications today.

---

## 1. What is a margin classifier?

Imagine you have two groups of emails on a graph:

- **Not spam** emails: few suspicious words, few links
- **Spam** emails: many suspicious words, many links

You can draw a line that separates them. But many lines can work.

```text
Line A: very close to the spam emails
Line B: right in the middle of the gap           ← best choice
Line C: very close to the normal emails
```

**Line B** is best because it leaves the largest empty space on both sides. This empty space is called the **margin**.

A classifier that tries to maximise the margin is called a **margin classifier**.

> **Memory trick:** Think of the margin as a safety zone. A wider safety zone means fewer mistakes when new data arrives.

---

## 2. Support Vector Machines (SVM)

SVM is a margin classifier. It finds the boundary that has the biggest possible gap between the two classes.

### 2.1 Support vectors — the important points

Most training points do not affect the boundary. Only the points closest to the boundary matter. These special points are called **support vectors**.

```text
Normal:  ●  ●  [●]  |  [■]  ■  ■  : Spam
                    ↑    ↑
              support vectors
```

If you remove the other points and keep only the support vectors, the boundary stays the same.

> **Memory trick:** Support vectors are like the fence posts that hold the boundary line in place.

### 2.2 Soft margin — real life is messy

Real data is rarely perfectly separable. Some spam emails look normal, and some normal emails look spammy.

SVM handles this with a **soft margin**. The parameter `C` controls how strict the model is:

| C value | What happens |
|---|---|
| **Large C** | Tries hard to classify every training point correctly. Can overfit. |
| **Small C** | Allows some mistakes. Usually generalises better. |

```python
from sklearn.svm import SVC

strict = SVC(C=100)      # large C, tight margin
relaxed = SVC(C=0.1)     # small C, wide margin
```

> **Memory trick:** C is the cost of being wrong. A high C means mistakes are expensive, so the model becomes strict.

### 2.3 The kernel trick — when a straight line is not enough

Some data cannot be separated by a straight line. For example, imagine one class surrounded by another class in a circle.

```text
       ●  ●  ●
    ●           ●
  ●    ■  ■  ■    ●
  ●   ■  ■  ■  ■  ●
    ●           ●
       ●  ●  ●
```

No straight line separates the circles from the squares. But if we move the data into a higher-dimensional space, it becomes separable.

A **kernel** does this transformation without actually moving the data. It only changes the way distances are measured. This is called the **kernel trick**.

Common kernels:

| Kernel | Use case |
|---|---|
| **Linear** | Data can be separated by a straight line. Fast. |
| **Polynomial** | Data needs a curved boundary. |
| **RBF (Radial Basis Function)** | Complex boundaries. Most common non-linear choice. |

```python
from sklearn.svm import SVC

linear = SVC(kernel='linear')       # straight boundary
rbf = SVC(kernel='rbf')             # flexible boundary
poly = SVC(kernel='poly', degree=3)   # curved boundary
```

### 2.4 SVM demonstration in Python

```python
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

# Load data
iris = load_iris()
X = iris.data
y = iris.target

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train an SVM with RBF kernel
model = SVC(kernel='rbf', C=1.0)
model.fit(X_train, y_train)

# Predict and evaluate
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))
```

### 2.5 When to use SVM

- Small to medium datasets
- When the number of features is large
- When you need a clear decision boundary
- When you want control over overfitting through `C` and the kernel

SVMs are slower on very large datasets. For millions of rows, algorithms like Random Forest or Gradient Boosting are usually better.

---

## 3. Naive Bayes

Naive Bayes classifies by asking:

> Given the evidence I see, which class is most likely?

### 3.1 The intuition

You receive an email:

```text
"Congratulations! You won a free iPhone."
```

From past experience, you know:

- The word "free" appears in 80% of spam but only 5% of normal emails.
- The word "won" appears in 60% of spam but only 2% of normal emails.
- The word "Congratulations" appears in 55% of spam but 10% of normal emails.

Naive Bayes combines these clues to estimate the probability that the email is spam.

> **Memory trick:** Naive Bayes is like a detective who weighs each clue and reaches a verdict.

### 3.2 Bayes' theorem

Bayes' theorem tells us how to update a belief when we see new evidence.

```text
P(class | evidence) = P(evidence | class) × P(class)
                    ─────────────────────────────────
                              P(evidence)
```

Read it as:

> The probability of a class given the evidence depends on how likely the evidence is for that class, how common the class is overall, and how common the evidence is overall.

For spam detection:

```text
P(spam | words) = P(words | spam) × P(spam)
                  ───────────────────────────
                        P(words)
```

### 3.3 The "naive" assumption

The word **naive** means the model assumes each feature is independent of the others. In spam detection, it assumes the word "free" does not affect the word "won".

This assumption is usually wrong in real life. Words often appear together. But the model still works well because it only needs to pick the most likely class, not calculate exact probabilities.

> **Memory trick:** Naive Bayes pretends each clue is independent. It is a simple lie that makes the math easy and often gives the right answer.

### 3.4 Types of Naive Bayes

Different types exist for different kinds of data.

| Type | Best for | Example |
|---|---|---|
| **Multinomial** | Count data, especially text | Word counts in emails |
| **Bernoulli** | Binary features | Word present or absent in email |
| **Gaussian** | Continuous numerical features | Height, weight, temperature |

```python
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB

multinomial = MultinomialNB()   # word counts
bernoulli = BernoulliNB()       # word present / absent
gaussian = GaussianNB()         # continuous numbers
```

### 3.5 Numerical stability and log-space

When you multiply many small probabilities, computers can round them to zero. To avoid this, Naive Bayes works in **log space**.

Instead of multiplying probabilities:

```text
P(words | spam) = P(word1 | spam) × P(word2 | spam) × ...
```

It adds their logarithms:

```text
log P(words | spam) = log P(word1 | spam) + log P(word2 | spam) + ...
```

Adding small numbers is safer than multiplying tiny numbers. The class with the highest log score still wins.

> **Memory trick:** Logs turn multiplication into addition. It is the same answer, but the computer does not lose precision.

### 3.6 Choosing the right Naive Bayes model

| Data type | Choose |
|---|---|
| Text word counts | Multinomial Naive Bayes |
| Binary features | Bernoulli Naive Bayes |
| Continuous numbers | Gaussian Naive Bayes |
| Mixed data | Try Gaussian or preprocess first |

### 3.7 Advantages and disadvantages

**Advantages:**

- Very fast to train and predict
- Works well with many features, especially text
- Needs little training data to start
- Easy to understand and explain

**Disadvantages:**

- The independence assumption is rarely true
- Can give overconfident probabilities
- Struggles with features that are highly correlated

### 3.8 Naive Bayes demonstration in Python

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

emails = [
    "Win a free prize now",      # spam
    "Free offer for you",         # spam
    "Meeting tomorrow at 10",     # not spam
    "Lunch today?",               # not spam
    "Congratulations free gift",  # spam
    "Can you send the report?",   # not spam
]

labels = [1, 1, 0, 0, 1, 0]  # 1 = spam, 0 = not spam

# Convert text to word counts
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

# Split and train
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.3, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))
```

### 3.9 Comparison with other classification models

| Model | Best for | Notes |
|---|---|---|
| **Naive Bayes** | Text, fast baseline | Assumes features are independent |
| **Logistic Regression** | Linearly separable data | Gives calibrated probabilities |
| **SVM** | Medium datasets, clear margins | Good with kernels for complex boundaries |
| **Decision Tree** | Interpretable rules | Can overfit easily |
| **Random Forest** | General-purpose | Often strongest for tabular data |

---

## 4. SVM vs Naive Bayes — quick decision guide

| Question | Use SVM | Use Naive Bayes |
|---|---|---|
| Is the data mostly text? | Sometimes | Very often |
| Do you need probabilities? | Not directly | Yes |
| Is the dataset small? | Yes, great | Yes, works with little data |
| Is the dataset huge? | Maybe too slow | Fast |
| Is the boundary complex? | Use RBF kernel | Try a different model |
| Do you need an explainable result? | Less explainable | Easy to explain |

---

## 5. Summary

- **SVM** finds the boundary with the largest margin. It uses support vectors and can handle non-linear data with the kernel trick.
- **Naive Bayes** uses probability and Bayes' theorem. It assumes features are independent, which makes the math simple.
- **SVM** is strong for clear boundaries and medium datasets.
- **Naive Bayes** is fast and works especially well for text classification.

---

## 6. Practice questions

1. Why is Line B better than Line A or Line C in the margin example?
2. What are support vectors, and why do they matter?
3. What does a large `C` value do in an SVM?
4. When would you use an RBF kernel instead of a linear kernel?
5. What is the "naive" assumption in Naive Bayes?
6. Which type of Naive Bayes is best for text word counts?
7. Why does Naive Bayes use log probabilities instead of multiplying probabilities directly?

### Answers

```text
1. Line B has the largest margin, so it generalises better to new data.
2. Support vectors are the closest points to the boundary. They define the boundary.
3. A large C makes the model strict and tries to avoid training errors. It can overfit.
4. Use RBF when the classes cannot be separated by a straight line.
5. It assumes each feature is independent of the others.
6. Multinomial Naive Bayes is best for text word counts.
7. Multiplying many tiny probabilities can underflow to zero. Adding logs avoids this.
```
