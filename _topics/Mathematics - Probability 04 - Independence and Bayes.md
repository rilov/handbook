---
title: "Mathematics 04: Independence and Bayes' Theorem — Questions, Formulas, and Answers"
category: Mathematics
order: 4
tags:
  - mathematics
  - probability
  - independence
  - bayes-theorem
summary: "Learn whether events affect each other and use Bayes' theorem to update probability after new evidence."
---

# Mathematics 04: Independence and Bayes' Theorem

## Question 1 — Are two coin flips independent?

Flip a fair coin twice. Does the first result change the chance of heads on the second flip?

No. The second coin flip does not remember the first one.

### Independence formula

```text
A and B are independent when:
P(A ∩ B) = P(A) × P(B)
```

For two heads:

```text
P(first head ∩ second head) = 1/2 × 1/2 = 1/4
```

The chance is 25%.

---

## Question 2 — Are drawing two aces without replacement independent?

Draw one card from a standard deck. Keep it out. Then draw another card.

The first result changes the deck for the second result, so the events are **not independent**.

```text
P(first ace) = 4/52
P(second ace given first ace) = 3/51
P(two aces) = 4/52 × 3/51 = 1/221
```

This uses the multiplication rule for dependent events:

```text
P(A ∩ B) = P(A) × P(B | A)
```

`P(B | A)` means “the probability of B, given that A already happened.”

---

## Question 3 — What is Bayes' theorem?

A medical test can be positive or negative. A positive result is evidence, but it is not automatically proof that a person has the disease.

Bayes' theorem tells us how to update a probability when we receive evidence.

### Bayes' theorem

```text
P(A | B) = P(B | A) × P(A) / P(B)
```

| Symbol | Meaning |
|---|---|
| `A` | the claim we want to know about |
| `B` | the evidence we observed |
| `P(A)` | probability of A before new evidence: prior |
| `P(A | B)` | probability of A after evidence B: posterior |

---

## Worked question — a positive medical test

Suppose:

- 1% of people have a disease: `P(disease) = 0.01`
- The test correctly finds the disease 99% of the time: `P(positive | disease) = 0.99`
- It incorrectly gives a positive result to 5% of healthy people: `P(positive | healthy) = 0.05`

**Question:** If a test is positive, what is the chance the person has the disease?

First find the chance of any positive result. This is the total probability rule:

```text
P(positive) = P(positive | disease) × P(disease)
            + P(positive | healthy) × P(healthy)

P(positive) = 0.99 × 0.01 + 0.05 × 0.99
            = 0.0594
```

Now use Bayes:

```text
P(disease | positive) = 0.99 × 0.01 / 0.0594
                      = 0.1667
```

A positive result means about a **16.67% chance** of disease in this example. The probability is not 99% because the disease is rare and false positives exist.

## Formula summary

```text
Independent events:  P(A ∩ B) = P(A)P(B)
Dependent events:    P(A ∩ B) = P(A)P(B | A)
Bayes' theorem:      P(A | B) = P(B | A)P(A) / P(B)
Total probability:   P(B) = Σ P(B | Aᵢ)P(Aᵢ)
```

## Practice

A website detects fraud. 2% of transactions are fraudulent. The detector catches 90% of fraud and incorrectly flags 4% of legitimate transactions. Find `P(fraud | flagged)`.

### Answer

```text
P(flagged) = 0.90 × 0.02 + 0.04 × 0.98 = 0.0572
P(fraud | flagged) = (0.90 × 0.02) / 0.0572 ≈ 0.3147
```

About **31.47%** of flagged transactions are actually fraudulent.
