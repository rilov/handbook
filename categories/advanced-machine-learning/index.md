---
layout: category
title: Advanced Machine Learning
category: Advanced Machine Learning
---

Learn advanced machine learning algorithms through clear, step-by-step explanations and practical Python examples. This module builds Support Vector Machines from the ground up — one small idea at a time — starting from the bias-variance tradeoff that motivates every design choice that follows.

**Recommended Learning Path:**

0. **[Bias and Variance]({{ site.baseurl }}/topics/bias-and-variance)** — The two ways any model can go wrong: underfitting (bias) vs overfitting (variance). Read this first — every later topic refers back to it.
1. **[SVM Part 1: Hyperplanes and Linear Classification]({{ site.baseurl }}/topics/svm-hyperplanes-and-linear-classification)** — What a hyperplane is in 2D, 3D, and d-dimensions, and why SVM is a linear model.
2. **[SVM Part 2: Maximal Margin Classifier]({{ site.baseurl }}/topics/svm-maximal-margin-classifier)** — Why SVM picks the widest-margin hyperplane, the dot-product and distance-formula refreshers, and support vectors.
3. **[SVM Part 3: Soft Margin Classifier and the Cost Parameter (C)]({{ site.baseurl }}/topics/svm-soft-margin-and-cost)** — Slack variables, why the Maximal Margin Classifier is fragile, and how `C` controls the bias-variance tradeoff.
4. **[SVM Part 4: Kernels and the Kernel Trick]({{ site.baseurl }}/topics/svm-kernels-and-kernel-trick)** — Mapping non-linear data to linear data, feature transformation, the kernel trick, and the `gamma` parameter.

**Complementary classification algorithm:**

- **[Naive Bayes — A Friendly Guide]({{ site.baseurl }}{% link _topics/Naive Bayes - A Friendly Guide.md %})** — A probabilistic classifier often compared with SVM. Covers Bayes' theorem, the naive independence assumption, and Multinomial/Bernoulli/Gaussian variants.

**What You'll Learn:**

- The bias-variance tradeoff and how to diagnose underfitting vs overfitting
- What a hyperplane is, from 2D lines to d-dimensional linear discriminators
- Why maximising the margin leads to better classifiers
- How support vectors define the SVM decision boundary
- Slack variables and the role of the `C` (cost) parameter
- The kernel trick and when to use linear, polynomial, and RBF kernels
- The `gamma` parameter and how it controls boundary flexibility
- How each SVM concept maps back to the bias-variance tradeoff
- Bayes' theorem and how it drives Naive Bayes classification
- When to use SVM vs Naive Bayes vs other classifiers
