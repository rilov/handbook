---
layout: category
title: Advanced Machine Learning
category: Advanced Machine Learning
---

Learn advanced machine learning algorithms through clear, step-by-step explanations and practical Python examples. This module builds Support Vector Machines from the ground up — one small idea at a time — starting from the bias-variance tradeoff that motivates every design choice that follows.

**Start here:**

- **[Advanced Machine Learning: The One-Pager]({{ site.baseurl }}/topics/advanced-machine-learning-one-pager)** — The simplest, one-page summary of every topic in this module. Read this first if you want the big picture.

**Recommended Learning Path:**

0. **[Bias and Variance]({{ site.baseurl }}/topics/bias-and-variance)** — The two ways any model can go wrong: underfitting (bias) vs overfitting (variance). Read this first — every later topic refers back to it.
1. **[SVM Part 1: Hyperplanes and Linear Classification]({{ site.baseurl }}/topics/svm-hyperplanes-and-linear-classification)** — What a hyperplane is in 2D, 3D, and d-dimensions, and why SVM is a linear model.
2. **[SVM Part 2: Maximal Margin Classifier]({{ site.baseurl }}/topics/svm-maximal-margin-classifier)** — Why SVM picks the widest-margin hyperplane, the dot-product and distance-formula refreshers, and support vectors.
3. **[SVM Part 3: Soft Margin Classifier and the Cost Parameter (C)]({{ site.baseurl }}/topics/svm-soft-margin-and-cost)** — Slack variables, why the Maximal Margin Classifier is fragile, and how `C` controls the bias-variance tradeoff.
4. **[SVM Part 4: Kernels and the Kernel Trick]({{ site.baseurl }}/topics/svm-kernels-and-kernel-trick)** — Mapping non-linear data to linear data, feature transformation, the kernel trick, and the `gamma` parameter.

**Naive Bayes series — probabilistic classification from first principles:**

5. **[Naive Bayes Part 1: Probabilistic Classification Intuition]({{ site.baseurl }}/topics/naive-bayes-probabilistic-classification-intuition)** — Classification as a probability question, priors and likelihoods, the curse of dimensionality, and why the "naive" assumption saves everything.
6. **[Naive Bayes Part 2: Deriving Bayes' Theorem]({{ site.baseurl }}/topics/naive-bayes-deriving-bayes-theorem)** — Conditional probability, the full derivation of Bayes' theorem, and what posterior, likelihood, prior, and evidence mean.
7. **[Naive Bayes Part 3: From Bayes' Theorem to the Classifier]({{ site.baseurl }}/topics/naive-bayes-from-bayes-theorem-to-classifier)** — Extending to multiple features, conditional independence, the argmax decision rule, numerical underflow, and log-space.
8. **[Naive Bayes Part 4: Gaussian Naive Bayes from Scratch]({{ site.baseurl }}/topics/naive-bayes-gaussian-from-scratch)** — Continuous features, the Gaussian PDF, a hand-worked male/female example, and a full from-scratch implementation compared to scikit-learn.
9. **[Naive Bayes Part 5: Multinomial Naive Bayes]({{ site.baseurl }}/topics/naive-bayes-multinomial)** — Count data, the multinomial likelihood, Laplace smoothing, and a fully worked spam example.
10. **[Naive Bayes Part 6: Bernoulli Naive Bayes]({{ site.baseurl }}/topics/naive-bayes-bernoulli)** — Binary features, the Bernoulli likelihood, and a fully worked mammal vs non-mammal example.
11. **[Naive Bayes Part 7: Choosing the Right Variant]({{ site.baseurl }}/topics/naive-bayes-choosing-the-right-variant)** — All three variants compared on the same spam dataset, and why the winner depends on how the feature distribution aligns with each model's assumption.
12. **[Naive Bayes Part 8: Other Classification Models and Parametric vs Non-Parametric]({{ site.baseurl }}/topics/naive-bayes-other-classification-models)** — Compare Naive Bayes with Logistic Regression, Decision Tree, KNN and SVM on the UCI Spambase dataset, and learn the parametric vs non-parametric distinction.

**Quick reference:**

- **[Advanced Machine Learning: The One-Pager]({{ site.baseurl }}/topics/advanced-machine-learning-one-pager)** — The simplest, big-picture summary of the whole module.
- **[Advanced Machine Learning: One-Liners]({{ site.baseurl }}/topics/advanced-machine-learning-one-liners)** — Every key formula and concept in one easy-to-scan line.
- **[Naive Bayes — A Friendly Guide]({{ site.baseurl }}{% link _topics/Naive Bayes - A Friendly Guide.md %})** — Original single-page overview of Naive Bayes, useful as a quick refresher after the series.

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
