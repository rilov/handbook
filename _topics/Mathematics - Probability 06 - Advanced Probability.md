---
title: "Mathematics 06: Advanced Probability — Joint Distributions, Covariance, LLN, and CLT"
category: Mathematics
order: 6
tags:
  - mathematics
  - probability
  - covariance
  - central-limit-theorem
  - law-of-large-numbers
summary: "Connect probability ideas using joint distributions, covariance, conditional expectation, the law of large numbers, and the central limit theorem."
---

# Mathematics 06: Advanced Probability

This lesson connects the earlier ideas and explains why probability is so useful in statistics and machine learning.

---

## Question 1 — What is a joint probability?

A joint probability asks for two events together.

```text
P(A ∩ B)
```

Example: in a class, what is the probability that a randomly chosen student passed both Math and Science?

If 5 out of 20 students passed both:

```text
P(Math ∩ Science) = 5/20 = 0.25
```

---

## Question 2 — How do we get a marginal probability?

A **marginal probability** ignores one variable by adding over all its possible values.

```text
P(A) = Σᵦ P(A ∩ B)
```

Plain English: to find the chance of A, add the chance of A happening with every possible version of B.

---

## Question 3 — What is covariance?

Covariance measures whether two numeric variables tend to move together.

### Formula

```text
Cov(X, Y) = E[(X - E[X])(Y - E[Y])]
```

- Positive covariance: both tend to rise together.
- Negative covariance: one tends to rise while the other falls.
- Near-zero covariance: no linear relationship is visible.

Correlation scales covariance to always sit between `-1` and `1`.

```text
Corr(X, Y) = Cov(X, Y) / (σₓσᵧ)
```

Correlation does not prove that one variable causes the other.

---

## Question 4 — Why do averages become stable?

The **Law of Large Numbers (LLN)** says that as we repeat an experiment more times, the sample average tends to get closer to the true expected value.

```text
sample mean = (x₁ + x₂ + ... + xₙ) / n
```

If you flip a fair coin 10 times, heads might be 70%. After 100,000 flips, the percentage of heads will usually be much closer to 50%.

---

## Question 5 — Why is the normal distribution everywhere?

The **Central Limit Theorem (CLT)** says that the average of many independent observations tends to look normally distributed when the sample is large enough, even if the original data is not normal.

For a population with mean `μ` and standard deviation `σ`:

```text
mean of sample means = μ
standard deviation of sample means = σ / √n
```

`σ / √n` is called the **standard error**. Larger samples make it smaller, so estimates become more precise.

---

## Worked question — why does a larger survey help?

Suppose individual customer ratings have standard deviation `σ = 12`.

Compare a survey of 36 customers with one of 144 customers.

```text
SE for n = 36  = 12 / √36  = 12 / 6  = 2
SE for n = 144 = 12 / √144 = 12 / 12 = 1
```

The larger survey has half the standard error. Its average rating is usually more stable.

## Formula summary

```text
Joint probability:       P(A ∩ B)
Marginal probability:    P(A) = Σᵦ P(A ∩ B)
Covariance:              Cov(X, Y) = E[(X - E[X])(Y - E[Y])]
Correlation:             Corr(X, Y) = Cov(X, Y) / (σₓσᵧ)
Sample mean:             x̄ = Σxᵢ / n
Standard error:          SE = σ / √n
```

## Practice

A population has standard deviation 20. What is the standard error for samples of size 25 and 100?

### Answer

```text
n = 25:  SE = 20 / √25 = 4
n = 100: SE = 20 / √100 = 2
```

Increasing the sample size by four makes the standard error half as large.
