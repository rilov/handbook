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

[SVM series]({{ site.baseurl }}/topics/svm-hyperplanes-and-linear-classification)

- **SVM's goal:** find the best boundary between two groups of points.
- **Main trick:** draw the widest possible empty "street" (called the **margin**) between the two groups. A wide street gives a safer, more confident boundary.
- **Support vectors:** the few points that touch the edge of the street. They are the only points that matter for the final boundary.
- **Soft margin:** real data is messy, so SVM can allow a few points on the wrong side. The cost **C** controls how much we care about those mistakes.
- **Kernel trick:** when a straight line cannot separate the groups, SVM lifts the data into a higher-dimensional space where it can. Common kernels are **linear**, **polynomial** and **RBF**.

---

## Naive Bayes: the big idea

[Naive Bayes series]({{ site.baseurl }}/topics/naive-bayes-probabilistic-classification-intuition)

- **Naive Bayes's goal:** answer "given the evidence, which class is more likely?" It turns the question around using **Bayes' Theorem**.
- **The "naive" part:** it assumes all features are independent. This is usually wrong, but it makes the math fast and still works well for text and spam.
- **Gaussian variant:** for continuous numbers.
- **Multinomial variant:** for word counts.
- **Bernoulli variant:** for yes/no features.
- **Strength:** fast, simple, and good for high-dimensional text. **Weakness:** the independence assumption can hurt accuracy on problems where features interact strongly.

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
