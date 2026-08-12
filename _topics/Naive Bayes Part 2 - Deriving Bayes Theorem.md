---
title: "Naive Bayes Part 2: Deriving Bayes' Theorem from Conditional Probability"
category: Advanced Machine Learning
order: 6
permalink: /topics/naive-bayes-deriving-bayes-theorem/
tags:
  - machine-learning
  - naive-bayes
  - bayes-theorem
  - probability
  - conditional-probability
summary: "Part 2 of the Naive Bayes series: derive Bayes' theorem from the definition of conditional probability, and understand what each term means."
date: 2026-08-11
---

# Naive Bayes Part 2: Deriving Bayes' Theorem from Conditional Probability

> Part 2 of the Naive Bayes series. We derive Bayes' theorem from the definition of conditional probability and explain each term in plain English.

---

## 1. Conditional probability

Conditional probability is the probability of one event happening **given that another event has already happened**. We write it as:

```
P(A | B)
```

Read as: "the probability of A, given B."

### Example with a deck of cards

In a standard 52-card deck, the probability of drawing a heart is `13/52 = 0.25`. But if someone already tells you the card is red, the probability becomes:

```
P(heart | red) = 13 / 26 = 0.5
```

Because knowing the card is red eliminates all the black cards. The "condition" narrows the sample space.

---

## 2. The definition of conditional probability

For any two events A and B, with `P(B) > 0`:

```
P(A | B) = P(A and B) / P(B)
```

Equivalently:

```
P(A and B) = P(A | B) × P(B)
```

This is the foundation of everything that follows. It says: the probability that both A and B happen equals the probability of B happening, multiplied by the probability of A happening once B is known.

---

## 3. Deriving Bayes' theorem

We can also write the joint probability the other way around:

```
P(A and B) = P(B | A) × P(A)
```

Both expressions equal the same thing, so we can set them equal to each other:

```
P(A | B) × P(B) = P(B | A) × P(A)
```

Now divide both sides by `P(B)`:

```
             P(B | A) × P(A)
P(A | B) =  ─────────────────
                   P(B)
```

This is **Bayes' theorem**. It lets us "flip" the conditioning: we start with `P(B | A)` (how likely the evidence is if the class is true) and end up with `P(A | B)` (how likely the class is, given the evidence).

---

## 4. What each term means in classification

Map Bayes' theorem to a classification problem where `C` is the class and `X` is the observed evidence:

```
             P(X | C) × P(C)
P(C | X) =  ─────────────────
                  P(X)
```

| Term | Name | Meaning |
|---|---|---|
| `P(C \| X)` | **Posterior** | What we want: the probability of the class given the evidence. |
| `P(X \| C)` | **Likelihood** | How likely the evidence is, if the class is true. Learned from training data. |
| `P(C)` | **Prior** | How common the class is overall. |
| `P(X)` | **Evidence** | Overall probability of seeing this evidence. Same for all classes, so we can ignore it when comparing classes. |

Because `P(X)` is the same in every class comparison, we can drop the denominator and just compare the numerators:

```
P(C | X) ∝ P(X | C) × P(C)
```

The class with the larger numerator wins.

---

## 5. A worked numerical example

Suppose a medical test for a disease has these properties:

- 1% of the population has the disease: `P(Disease) = 0.01`
- If you have the disease, the test is positive 99% of the time: `P(Positive | Disease) = 0.99`
- If you do not have the disease, the test is positive 5% of the time: `P(Positive | No Disease) = 0.05`

You tested positive. What is the probability you actually have the disease?

Using Bayes' theorem:

```
P(Disease | Positive) = P(Positive | Disease) × P(Disease) / P(Positive)
```

First compute `P(Positive)` — the total probability of a positive test result:

```
P(Positive) = P(Positive | Disease) × P(Disease)
            + P(Positive | No Disease) × P(No Disease)

            = 0.99 × 0.01 + 0.05 × 0.99
            = 0.0099 + 0.0495
            = 0.0594
```

Now plug in:

```
P(Disease | Positive) = 0.99 × 0.01 / 0.0594
                      = 0.0099 / 0.0594
                      ≈ 0.1667
```

So even after a positive test, the actual probability of having the disease is only about **16.7%**. This is why the prior matters: the disease is rare, and false positives from healthy people add up.

---

## 6. Why the denominator can be ignored in classification

When we classify a new sample, we compare the posterior for every class. The denominator `P(X)` is identical in every comparison, so it does not change which class wins. We can write:

```
P(C1 | X) ∝ P(X | C1) × P(C1)
P(C2 | X) ∝ P(X | C2) × P(C2)
```

Predicted class = whichever is larger. This is the exact reason Naive Bayes can skip the expensive computation of the full evidence term.

---

## 7. Practice questions

1. Write Bayes' theorem using `A` and `B`, and identify which part is the posterior.
2. Why can we ignore the denominator `P(X)` when comparing classes in Naive Bayes?
3. In the medical test example, why is the probability of disease after a positive test only ~16.7% despite the test being 99% accurate on sick people?
4. What is the difference between the prior `P(C)` and the likelihood `P(X | C)`?

**Answers:**

1. `P(A | B) = P(B | A) × P(A) / P(B)`. The posterior is `P(A | B)`.
2. Because `P(X)` is the same for every class being compared. It scales both scores equally, so the class with the larger numerator still wins.
3. The disease is rare (only 1% prior), and there are many more healthy people than sick people. Even with a low false-positive rate, the sheer number of healthy people produces enough false positives to outnumber true positives.
4. The prior is how common the class is before seeing any evidence. The likelihood is how likely the observed evidence is if that class were true.

---

## 8. Summary

- Conditional probability: `P(A | B) = P(A and B) / P(B)`.
- Bayes' theorem follows by writing the joint probability two ways and solving for the flipped conditional.
- In classification: `P(C | X) ∝ P(X | C) × P(C)`.
- The posterior, likelihood, and prior each have a clear meaning.
- We can ignore the evidence `P(X)` when comparing classes, which is what makes Naive Bayes efficient.

**Next topic:** [From Bayes' Theorem to the Naive Bayes Classifier]({{ site.baseurl }}/topics/naive-bayes-from-bayes-theorem-to-classifier)
