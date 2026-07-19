---
title: "Mathematics 05: Random Variables and Distributions — Questions, Formulas, and Answers"
category: Mathematics
order: 5
tags:
  - mathematics
  - probability
  - random-variables
  - distributions
  - expected-value
summary: "Understand random variables, probability distributions, expected value, variance, and standard deviation through simple questions."
---

# Mathematics 05: Random Variables and Distributions

A **random variable** gives a number to each random outcome.

For one die roll, let `X` be the number rolled. Then `X` can be `1, 2, 3, 4, 5, 6`.

---

## Question 1 — What is a probability distribution?

A distribution lists every value a random variable can take and its probability.

For a fair die:

| `x` | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| `P(X = x)` | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 | 1/6 |

All probabilities in a distribution must add to 1.

```text
Σ P(X = x) = 1
```

`Σ` means “add all values.”

---

## Question 2 — What is expected value?

Expected value is the long-run average if you repeat an experiment many times.

### Formula

```text
E[X] = Σ x × P(X = x)
```

### Answer for a fair die

```text
E[X] = 1(1/6) + 2(1/6) + 3(1/6) + 4(1/6) + 5(1/6) + 6(1/6)
     = 21/6
     = 3.5
```

You cannot roll 3.5, but after many rolls the average approaches 3.5.

---

## Question 3 — How spread out are the results?

Variance measures how far values tend to be from the expected value.

### Variance formula

```text
Var(X) = E[(X - μ)²]
```

For a discrete distribution, calculate it as:

```text
Var(X) = Σ (x - μ)² × P(X = x)
```

Here `μ = E[X]` is the mean.

### Standard deviation

```text
σ = √Var(X)
```

Variance uses squared units. Standard deviation returns to the original units, which is usually easier to interpret.

---

## Question 4 — What distribution counts successes?

The **binomial distribution** describes the number of successes in a fixed number of independent yes/no trials.

Examples:

- number of heads in 10 coin flips
- number of customers who click an advert out of 100 visitors

### Binomial formula

```text
P(X = k) = C(n, k) × p^k × (1 - p)^(n-k)
```

| Symbol | Meaning |
|---|---|
| `n` | number of trials |
| `k` | wanted number of successes |
| `p` | chance of success in one trial |

For a binomial random variable:

```text
E[X] = np
Var(X) = np(1 - p)
```

---

## Worked question — exactly 3 heads in 5 flips

```text
n = 5
k = 3
p = 1/2

P(X = 3) = C(5, 3) × (1/2)^3 × (1/2)^2
         = 10 × 1/32
         = 0.3125
```

There is a **31.25% chance** of exactly three heads.

## Practice

A fair die is rolled once. Find its expected value. Then explain why it is not one of the possible die values.

### Answer

```text
E[X] = 3.5
```

Expected value is a long-run average, not a prediction of the next single roll.
