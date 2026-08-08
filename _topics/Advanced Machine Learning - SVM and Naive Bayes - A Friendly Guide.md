---
title: "Advanced Machine Learning: SVM and Naive Bayes"
category: Advanced Machine Learning
order: 1
tags:
  - advanced-machine-learning
  - svm
  - support-vector-machines
  - naive-bayes
  - kernels
  - margin-classifiers
  - bayes-theorem
  - classification
  - python
  - sklearn
summary: "A complete step-by-step guide to Support Vector Machines and Naive Bayes. Covers margin classifiers, kernels, email and letter recognition demonstrations, Bayes' theorem, types of Naive Bayes, and how to choose between models."
---

# Advanced Machine Learning: SVM and Naive Bayes

This module covers two classic but powerful machine learning algorithms used for classification:

- **Support Vector Machines (SVM)** — find the best boundary between classes.
- **Naive Bayes** — classify using probability and Bayes' theorem.

Both algorithms are still widely used today. They are simple to explain, fast to train, and often surprisingly effective.

---

## Module 0: Course and module overview

By the end of this module you will be able to:

1. Explain what a margin classifier is and why it matters.
2. Train an SVM and choose the right kernel for the data.
3. Classify emails and handwritten characters using non-linear SVMs.
4. Use Bayes' theorem to update beliefs based on evidence.
5. Build a Naive Bayes classifier for text and other data.
6. Choose between Multinomial, Bernoulli, and Gaussian Naive Bayes.
7. Compare SVM and Naive Bayes with other classification models.

Each section is written in plain English and includes runnable Python code.

---

## Session 1: Margin classifiers

### 1.1 The idea of a margin

Imagine you are a teacher separating two groups of students on a playground: Team A and Team B. You can draw a line down the middle. Many lines work, but the best line is the one that keeps the largest empty space between the two teams.

```text
Team A       gap       Team B
  ●   ●     |     ■   ■
     ●      |       ■
            |        ← best boundary
```

That empty space is called the **margin**. A classifier that tries to make the margin as wide as possible is called a **margin classifier**.

A wide margin is safer because new points that are slightly ambiguous are less likely to be classified wrong.

> **Memory trick:** The margin is a safety lane. The wider the lane, the safer the classifier.

### 1.2 Why the middle line is best

You could draw a line very close to Team A. That line would classify all Team A members correctly, but it might misclassify a new Team B member who stands slightly inside the gap.

The same problem happens if you draw the line too close to Team B.

The best line is the one that is **farthest from both groups**. This is the core idea behind every margin classifier.

---

## Session 2: Support Vector Machines and Kernels

### 2.1 Session overview

A **Support Vector Machine (SVM)** is a margin classifier. It finds the boundary that maximises the distance between the two closest points from each class.

Those closest points are called **support vectors**. They are the only points that matter for the boundary. Every other point could be removed without changing the result.

SVMs can use straight lines, but they can also use curved boundaries through a clever idea called the **kernel trick**.

### 2.2 Support vectors

Most training points are not important. Only the points that sit right on the edge of the margin matter.

```text
Normal:  ●  ●  [●]  |  [■]  ■  ■  : Spam
                    ↑    ↑
              support vectors
```

The boundary is fully determined by the support vectors. This is why SVMs can be memory-efficient after training.

> **Memory trick:** Support vectors are the fence posts that hold the boundary line in place.

### 2.3 Soft margin — real data is messy

In real life, data is rarely perfectly separable. A few points will be on the wrong side.

SVMs handle this with a **soft margin**. The parameter `C` controls how much the model is allowed to misclassify training points:

| C value | What happens |
|---|---|
| **Large C** | Strict. Few training errors allowed. Can overfit. |
| **Small C** | Relaxed. More errors allowed. Often generalises better. |

```python
from sklearn.svm import SVC

strict = SVC(C=100)
relaxed = SVC(C=0.1)
```

> **Memory trick:** C is the cost of being wrong. High C means mistakes are expensive.

### 2.4 Motivation for kernels and feature transformations

Some datasets cannot be separated by a straight line.

```text
       ●  ●  ●
    ●           ●
  ●    ■  ■  ■    ●
  ●   ■  ■  ■  ■  ●
    ●           ●
       ●  ●  ●
```

Here the circles surround the squares. No straight line can separate them.

One way to solve this is to transform the data into a higher-dimensional space. In that space, the classes may become separable.

For example, if your original features are `x` and `y`, you could add a new feature `z = x² + y²`. In 3D space, the circles might be lifted above the squares, making a flat plane a good boundary.

A **kernel** does this transformation without actually computing the new coordinates. It only changes the way distances are measured. This is the **kernel trick**.

### 2.5 Working of kernels

A kernel is a function that takes two points and returns a similarity score. It answers the question: *how close are these two points after the hidden transformation?*

Common kernels:

| Kernel | When to use |
|---|---|
| **Linear** | The classes can be separated by a straight line. Fast and interpretable. |
| **Polynomial** | You expect curved boundaries of a certain degree. |
| **RBF (Radial Basis Function)** | Complex boundaries. Often the default non-linear choice. |

```python
from sklearn.svm import SVC

linear = SVC(kernel='linear')
rbf = SVC(kernel='rbf')
poly = SVC(kernel='poly', degree=3)
```

The RBF kernel measures similarity as a function of distance. Nearby points are very similar; far away points are very different. This lets the boundary bend around the data.

> **Memory trick:** A kernel is a magic lens that bends the data into a shape where a straight line can separate the classes.

### 2.6 SVM demonstration — email classification using non-linear SVMs

Email classification is a classic text problem. Words are converted into numbers, and then an SVM separates spam from normal emails.

Because email data is rarely linearly separable, we use an RBF kernel.

```python
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

emails = [
    # Spam
    "Win a free prize now",
    "Free offer just for you",
    "Claim your free reward today",
    "Get a free iPhone now",
    "You won a free vacation",
    "Buy cheap products free shipping",
    "Congratulations you won a free gift",
    "Act now free money prize",
    "Limited time free reward",
    "Call now to claim your prize",
    "Free entry to win cash",
    "You are selected for a free prize",
    # Not spam
    "Meeting tomorrow at 10",
    "Lunch today?",
    "Can you send the report?",
    "Project update attached",
    "See you at the standup",
    "Please review the document",
    "Schedule a call for next week",
    "Thanks for the update today",
    "Let me know if you need help",
    "The report is ready for review",
    "Happy to discuss this tomorrow",
    "Can we reschedule the meeting?",
]

labels = [1]*12 + [0]*12  # 1 = spam, 0 = not spam

# Convert text into TF-IDF features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(emails)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.25, random_state=42
)

# Non-linear SVM with RBF kernel
model = SVC(kernel='rbf', C=1.0)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Email SVM accuracy:", accuracy_score(y_test, predictions))
```

The `TfidfVectorizer` turns each email into a vector of word importance scores. The RBF kernel then finds a non-linear boundary between spam and normal emails.

### 2.7 SVM demonstration — letter recognition using non-linear SVMs

Letter recognition means deciding which letter a handwritten or printed character is. We can practise this idea using the digits dataset from scikit-learn, where each image is a small grid of numbers.

```python
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Load character images (8x8 pixels each)
digits = load_digits()
X = digits.data
y = digits.target

# Scale the pixel values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Non-linear SVM with RBF kernel
model = SVC(kernel='rbf', C=1.0)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Letter/digit SVM accuracy:", accuracy_score(y_test, predictions))
```

The RBF kernel handles the complex shapes of different characters. Each pixel is a feature, and the SVM learns which combinations of pixels belong to which character.

### 2.8 When to use SVM

- Small to medium datasets
- High-dimensional data, like text
- When you need a clear decision boundary
- When you can afford some training time for better accuracy

SVMs can be slow on very large datasets. For millions of rows, tree-based models are often faster.

---

## Session 3: Naive Bayes

### 3.1 Session overview

Naive Bayes is a probabilistic classifier. It asks:

> Given the evidence I see, which class is most likely?

It is built entirely on one rule from probability: **Bayes' theorem**. The "naive" part is a simplifying assumption that makes the math easy.

Despite the simple assumption, Naive Bayes works very well for many real problems, especially text classification.

### 3.2 Intuition behind probabilistic classification

You receive an email with the subject:

```text
"Congratulations! You won a free iPhone."
```

From past experience, you know:

- "free" appears in 80% of spam but only 5% of normal emails.
- "won" appears in 60% of spam but only 2% of normal emails.
- "Congratulations" appears in 55% of spam but 10% of normal emails.

Naive Bayes combines these individual clues into a single probability:

```text
What is the probability this email is spam, given these words?
```

> **Memory trick:** Naive Bayes is like a detective collecting clues and weighing the evidence.

### 3.3 Deriving Bayes' theorem from conditional probability

Conditional probability is the probability of one event given that another event has happened.

```text
P(A | B) = probability of A given B
```

The definition of conditional probability is:

```text
P(A | B) = P(A and B) / P(B)
```

If we swap A and B, we also get:

```text
P(B | A) = P(A and B) / P(A)
```

Since both expressions contain `P(A and B)`, we can rearrange them to get Bayes' theorem:

```text
P(A | B) = P(B | A) × P(A)
          ─────────────────────
                 P(B)
```

In plain English:

> How likely is A after seeing B? It depends on how likely B is when A is true, how likely A was before seeing B, and how likely B is overall.

### 3.4 From Bayes' theorem to the Naive Bayes classifier

For spam detection, we want:

```text
P(spam | words) = P(words | spam) × P(spam)
                 ───────────────────────────
                        P(words)
```

The tricky part is `P(words | spam)`. A sentence can contain many words, and computing their combined probability is hard.

Naive Bayes makes the **naive assumption**: each word is independent of the others.

This means:

```text
P(words | spam) = P(word1 | spam) × P(word2 | spam) × ...
```

The assumption is usually wrong. Words like "free" and "won" often appear together in spam. But the model still works because it only needs to choose the most likely class, not produce perfect probabilities.

For each class, Naive Bayes computes a score:

```text
score(class) = P(class) × P(feature1 | class) × P(feature2 | class) × ...
```

The class with the highest score wins.

> **Memory trick:** Naive Bayes pretends every clue is independent. It is a simple lie that makes the math fast and usually gives the right answer.

### 3.5 Naive Bayes: Python demonstration

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

emails = [
    # Spam
    "Win a free prize now",
    "Free offer just for you",
    "Claim your free reward today",
    "Get a free iPhone now",
    "You won a free vacation",
    "Buy cheap products free shipping",
    "Congratulations you won a free gift",
    "Act now free money prize",
    "Limited time free reward",
    "Call now to claim your prize",
    "Free entry to win cash",
    "You are selected for a free prize",
    # Not spam
    "Meeting tomorrow at 10",
    "Lunch today?",
    "Can you send the report?",
    "Project update attached",
    "See you at the standup",
    "Please review the document",
    "Schedule a call for next week",
    "Thanks for the update today",
    "Let me know if you need help",
    "The report is ready for review",
    "Happy to discuss this tomorrow",
    "Can we reschedule the meeting?",
]

labels = [1]*12 + [0]*12  # 1 = spam, 0 = not spam

# Convert text to word counts
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(emails)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.25, random_state=42
)

# Train Multinomial Naive Bayes
model = MultinomialNB()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Naive Bayes accuracy:", accuracy_score(y_test, predictions))
```

### 3.6 Multinomial Naive Bayes

Multinomial Naive Bayes is designed for count data, especially word counts in text.

It assumes each feature is a count, such as how many times a word appears in a document.

Use it when:

- Your features are counts.
- You are working with text.
- The order of words does not matter, only their presence and frequency.

```python
from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB()
```

### 3.7 Bernoulli Naive Bayes

Bernoulli Naive Bayes is designed for binary features.

Instead of counting how many times a word appears, it only cares whether the word is present or absent.

Use it when:

- Your features are 0 or 1.
- You only care about whether a word appears in a document, not how many times.

```python
from sklearn.naive_bayes import BernoulliNB

model = BernoulliNB()
```

### 3.8 Gaussian Naive Bayes

Gaussian Naive Bayes is designed for continuous numerical features.

It assumes each feature follows a **normal distribution** (a bell curve) for each class. It uses the mean and variance of the feature to estimate probabilities.

Use it when:

- Your features are continuous numbers, like height, weight, or temperature.

```python
from sklearn.naive_bayes import GaussianNB

model = GaussianNB()
```

### 3.9 Numerical stability and log-space computation

When you multiply many small probabilities, the result can become so small that the computer rounds it to zero. This is called **underflow**.

Naive Bayes avoids this by working in **log space**.

Instead of multiplying probabilities:

```text
P(words | spam) = P(word1 | spam) × P(word2 | spam) × ...
```

It adds the logarithms of the probabilities:

```text
log P(words | spam) = log P(word1 | spam) + log P(word2 | spam) + ...
```

Adding small numbers is safe. The class with the highest log-score is still the most likely class.

> **Memory trick:** Logs turn multiplication into addition. The answer is the same, but the computer does not lose precision.

### 3.10 Choosing the right Naive Bayes model

| Data type | Choose |
|---|---|
| Word counts or term frequencies | Multinomial Naive Bayes |
| Binary features (present / absent) | Bernoulli Naive Bayes |
| Continuous numerical features | Gaussian Naive Bayes |
| Mixed data | Try Gaussian or preprocess the data first |

### 3.11 Advantages and disadvantages of Naive Bayes

**Advantages:**

- Extremely fast to train and predict
- Works well with many features
- Needs little training data to be useful
- Easy to understand and implement
- Performs well for text classification

**Disadvantages:**

- The independence assumption is rarely true
- Probabilities can be overconfident
- Struggles when features are highly correlated
- Not the best choice when relationships between features are important

### 3.12 Comparison of Naive Bayes with other classification models

| Model | Best for | Key idea |
|---|---|---|
| **Naive Bayes** | Text, fast baseline | Probability with independence assumption |
| **Logistic Regression** | Linearly separable data | Learns a linear decision boundary |
| **SVM** | Medium datasets, complex boundaries | Maximises the margin, uses kernels |
| **Decision Tree** | Interpretable rules | Splits data based on feature questions |
| **Random Forest** | General tabular data | Ensemble of many decision trees |

Naive Bayes is often the best first model for text because it is fast and surprisingly accurate. SVM is often better when the dataset is small and the boundary is complex. Random Forest is usually the strongest for mixed tabular data.

### 3.13 Session summary

- Naive Bayes classifies by computing the probability of each class given the evidence.
- Bayes' theorem tells us how to update beliefs when we see new evidence.
- The naive assumption makes the math fast and simple.
- Multinomial Naive Bayes is for text counts.
- Bernoulli Naive Bayes is for binary features.
- Gaussian Naive Bayes is for continuous numbers.
- Log-space computation prevents numerical underflow.

---

## 4. SVM vs Naive Bayes: which one should you use?

| Question | Use SVM | Use Naive Bayes |
|---|---|---|
| Mostly text data? | Sometimes | Very often |
| Need probabilities? | Not directly | Yes |
| Small dataset? | Great | Great |
| Huge dataset? | May be too slow | Very fast |
| Complex boundary? | Use RBF kernel | Try another model |
| Need explainability? | Less explainable | Easy to explain |

Both are excellent classifiers. Start with Naive Bayes for a quick baseline, then try SVM if you need a more flexible boundary.

---

## 5. Practice questions

1. Why is the middle separating line better than a line close to one class?
2. What are support vectors, and why do they matter?
3. What does a large `C` value do in an SVM?
4. When would you use an RBF kernel instead of a linear kernel?
5. What is the kernel trick, and why is it useful?
6. What does the "naive" assumption mean in Naive Bayes?
7. Which type of Naive Bayes is best for text word counts?
8. Why does Naive Bayes use log probabilities instead of multiplying probabilities?
9. Which model would you try first for a large text-classification problem?
10. Which model would you try if you have a small dataset with a complex boundary?

### Answers

```text
1. The middle line has the largest margin, so it generalises better.
2. Support vectors are the closest points to the boundary. They define the boundary.
3. A large C makes the model strict and tries hard to avoid training errors.
4. Use RBF when the classes cannot be separated by a straight line.
5. The kernel trick transforms data into a higher-dimensional space without actually computing the new coordinates. It lets SVMs find curved boundaries.
6. It assumes each feature is independent of the others.
7. Multinomial Naive Bayes is best for text word counts.
8. Multiplying many tiny probabilities can underflow to zero. Adding logs avoids this.
9. Naive Bayes is a great first model for large text problems.
10. SVM with an RBF kernel is a good choice for a small dataset with a complex boundary.
```
