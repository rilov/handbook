---
title: "Mathematics 02: Counting for Probability — Permutations and Combinations"
category: Mathematics
order: 2
tags:
  - mathematics
  - probability
  - counting
  - permutations
  - combinations
summary: "Count possible outcomes using the multiplication rule, permutations, and combinations before calculating probability."
---

# Mathematics 02: Counting for Probability

Many probability questions become easy once you can count the possible outcomes.

---

## Question 1 — How many outfits can you make?

You have 3 shirts and 2 pairs of trousers. Choose one shirt and one pair of trousers.

### Multiplication rule

```text
number of complete choices = choices for step 1 × choices for step 2 × ...
```

### Answer

```text
3 shirts × 2 trousers = 6 outfits
```

This works because each shirt can be paired with each pair of trousers.

---

## Question 2 — How many ways can gold, silver, and bronze be assigned?

Five runners finish a race. We care about first, second, and third place.

Order matters: `Ada, Ben, Chen` is different from `Ben, Ada, Chen`.

### Permutation formula

```text
P(n, r) = n! / (n - r)!
```

| Symbol | Meaning |
|---|---|
| `n` | total available items |
| `r` | items selected |
| `!` | factorial: `5! = 5 × 4 × 3 × 2 × 1` |

### Answer

```text
P(5, 3) = 5! / (5 - 3)!
        = 5! / 2!
        = (5 × 4 × 3 × 2 × 1) / (2 × 1)
        = 5 × 4 × 3
        = 60
```

There are **60 ordered podiums**.

---

## Question 3 — How many groups of 3 can be chosen from 5 students?

Now we choose a committee of 3 students. The order does not matter. A committee containing Ada, Ben, and Chen is the same committee in every order.

### Combination formula

```text
C(n, r) = n! / (r! × (n - r)!)
```

`C(n, r)` is also written as `nCr` or `n choose r`.

### Answer

```text
C(5, 3) = 5! / (3! × 2!)
        = (5 × 4 × 3 × 2 × 1) / ((3 × 2 × 1) × (2 × 1))
        = 10
```

There are **10 possible committees**.

---

## Question 4 — What is the chance of exactly 2 heads in 3 fair coin flips?

The possible equally likely results are:

```text
HHH, HHT, HTH, THH, HTT, THT, TTH, TTT
```

Exactly two heads appears in `HHT`, `HTH`, and `THH`: 3 outcomes out of 8.

We can also use combinations.

### Formula

```text
P(exactly r successes in n fair trials) = C(n, r) × p^r × (1 - p)^(n-r)
```

For a fair coin, `p = 1/2`.

### Answer

```text
P(exactly 2 heads) = C(3, 2) × (1/2)^2 × (1/2)^1
                    = 3 × 1/8
                    = 3/8
                    = 0.375
```

This formula is called the **binomial formula**. You will study it in more detail later.

---

## How to choose the right formula

| Situation | Use |
|---|---|
| Choose in several independent steps | multiplication rule |
| Choose items and order matters | permutation `P(n, r)` |
| Choose items and order does not matter | combination `C(n, r)` |

## Practice

1. How many 4-digit PINs can be made if every digit may be 0–9?
2. How many ways can 2 class representatives be selected from 10 students if president and vice-president are different jobs?
3. How many ways can 2 class representatives be selected from 10 students if they have the same job?

### Answers

```text
1. 10 × 10 × 10 × 10 = 10,000
2. P(10, 2) = 10 × 9 = 90
3. C(10, 2) = 10! / (2! × 8!) = 45
```
