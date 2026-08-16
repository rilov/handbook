---
title: "Advanced Machine Learning: The One-Pager"
category: Advanced Machine Learning
order: 0
permalink: /topics/advanced-machine-learning-one-pager/
tags:
  - machine-learning
  - summary
  - one-pager
  - advanced-machine-learning
summary: "The simplest one-page guide to every topic in the Advanced Machine Learning module: bias and variance, SVM, and the full Naive Bayes series."
date: 2026-08-16
---

# Advanced Machine Learning: The One-Pager

This page is a bird's-eye view of the whole module. Each topic below is reduced to one or two plain sentences. Read this first, or use it as a quick reference when you are lost.

---

## 0. Bias and Variance

[Bias and Variance]({{ site.baseurl }}/topics/bias-and-variance)

- **Bias** means the model is too simple and keeps making the same kind of mistake. It has underfitted the data.
- **Variance** means the model is too complex and memorises the training data. It has overfitted.
- The goal is to find the middle: a model that is simple enough to generalise and complex enough to fit the real pattern.

---

## SVM: the big idea

[SVM Part 1]({{ site.baseurl }}/topics/svm-hyperplanes-and-linear-classification) | [SVM Part 2]({{ site.baseurl }}/topics/svm-maximal-margin-classifier) | [SVM Part 3]({{ site.baseurl }}/topics/svm-soft-margin-and-cost) | [SVM Part 4]({{ site.baseurl }}/topics/svm-kernels-and-kernel-trick)

- **SVM's goal:** find the best boundary between two groups of points.
- **Main trick:** draw the widest possible empty "street" (called the **margin**) between the two groups. A wide street gives a safer, more confident boundary.
- **Support vectors:** the few points that touch the edge of the street. They are the only points that matter for the final boundary.
- **Soft margin:** real data is messy, so SVM can allow a few points on the wrong side. The cost **C** controls how much we care about those mistakes.
- **Kernel trick:** when a straight line cannot separate the groups, SVM lifts the data into a higher-dimensional space where it can. The **linear**, **polynomial** and **RBF** kernels are the most common.

The four sections below walk through these steps one at a time.

---

## 1. SVM Part 1: Hyperplanes and Linear Classification

[SVM Part 1]({{ site.baseurl }}/topics/svm-hyperplanes-and-linear-classification)

- A **hyperplane** is just a flat line (in 2D), a flat plane (in 3D), or a flat decision surface (in higher dimensions) that splits data into two groups.
- SVM finds the best flat boundary for classifying things, such as spam vs not spam.

---

## 2. SVM Part 2: Maximal Margin Classifier

[SVM Part 2]({{ site.baseurl }}/topics/svm-maximal-margin-classifier)

- SVM wants the widest possible empty "road" between the two classes. That road is called the **margin**.
- The points that touch the edge of the road are the **support vectors**; they are the only points that matter for the final boundary.

---

## 3. SVM Part 3: Soft Margin and the Cost Parameter C

[SVM Part 3]({{ site.baseurl }}/topics/svm-soft-margin-and-cost)

- Real data is messy, so SVM allows some points to be on the wrong side of the margin using **slack variables**.
- **C** is the cost of making a mistake: a big C means "do not allow mistakes" (low bias, high variance); a small C means "allow some mistakes to keep the boundary simpler" (high bias, low variance).

---

## 4. SVM Part 4: Kernels and the Kernel Trick

[SVM Part 4]({{ site.baseurl }}/topics/svm-kernels-and-kernel-trick)

- When data is not linearly separable, SVM can lift it into a higher-dimensional space where it becomes separable. This is the **kernel trick**.
- Common kernels are **linear** (simple), **polynomial** (curved boundaries) and **RBF** (very flexible local curves). **gamma** controls how tight the RBF curve is.

---

## 5. Naive Bayes Part 1: Probabilistic Classification

[Naive Bayes Part 1]({{ site.baseurl }}/topics/naive-bayes-probabilistic-classification-intuition)

- Classification means "given the evidence, which class is more likely?" Naive Bayes answers this using probabilities.
- The "naive" part is the assumption that every feature is independent, which makes the math possible even with many features.

---

## 6. Naive Bayes Part 2: Bayes' Theorem

[Naive Bayes Part 2]({{ site.baseurl }}/topics/naive-bayes-deriving-bayes-theorem)

- **Bayes' Theorem** lets you flip a probability: you can go from "what is the evidence given the class?" to "what is the class given the evidence?"

---

## 7. Naive Bayes Part 3: From Bayes' Theorem to the Classifier

[Naive Bayes Part 3]({{ site.baseurl }}/topics/naive-bayes-from-bayes-theorem-to-classifier)

- Multiply the probabilities of all the features, then pick the class with the highest product. We use **log probabilities** so the numbers do not vanish.

---

## 8. Naive Bayes Part 4: Gaussian Naive Bayes

[Naive Bayes Part 4]({{ site.baseurl }}/topics/naive-bayes-gaussian-from-scratch)

- For continuous numbers, Gaussian Naive Bayes assumes each feature looks like a bell curve for each class.
- It then picks the class whose bell curve is most likely to produce the new value.

---

## 9. Naive Bayes Part 5: Multinomial Naive Bayes

[Naive Bayes Part 5]({{ site.baseurl }}/topics/naive-bayes-multinomial)

- For counting words, tags or categories, **Multinomial Naive Bayes** counts how often each word appears in each class.
- **Laplace smoothing** stops the model from giving zero probability to words it has not seen before.

---

## 10. Naive Bayes Part 6: Bernoulli Naive Bayes

[Naive Bayes Part 6]({{ site.baseurl }}/topics/naive-bayes-bernoulli)

- For yes/no features, **Bernoulli Naive Bayes** only cares whether each feature is present or absent, not how many times it appears.

---

## 11. Naive Bayes Part 7: Choosing the Right Variant

[Naive Bayes Part 7]({{ site.baseurl }}/topics/naive-bayes-choosing-the-right-variant)

- **Gaussian** is for numbers, **Multinomial** is for word counts, **Bernoulli** is for yes/no features. The best one depends on the shape of the data.

---

## 12. Naive Bayes Part 8: Other Classifiers

[Naive Bayes Part 8]({{ site.baseurl }}/topics/naive-bayes-other-classification-models)

- Naive Bayes is fast and simple, but it is not always the most accurate. It is compared with Logistic Regression, Decision Tree, KNN and SVM on the same spam dataset.
- **Parametric** models assume a fixed shape; **non-parametric** models learn the shape from the data.

---

## Quick cheat sheet: which tool for which job?

| You want... | Try this |
|---|---|
| A fast, simple text classifier | Naive Bayes (Bernoulli or Multinomial) |
| A fast classifier with probabilities | Logistic Regression |
| The best possible flat boundary | SVM with a linear kernel |
| A non-linear boundary with few knobs | SVM with an RBF kernel |
| An easy-to-read decision flow | Decision Tree |
| A flexible boundary with little training | KNN |
| To understand why a model fails | Bias and Variance |

---

## One-sentence takeaway

All machine learning is a tradeoff: make the model too simple and it misses the pattern; make it too complex and it memorises noise. The topics in this module give you the tools to find the right balance.
