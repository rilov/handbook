---
title: "Mathematics 01: Probability Foundations — Questions, Formulas, and Answers"
category: Mathematics
order: 1
tags:
  - mathematics
  - probability
  - beginners
  - formulas
  - questions
summary: "Learn probability from zero using simple questions, formulas, plain-English explanations, and worked answers."
---

# Mathematics 01: Probability Foundations

Probability answers one question:

> **How likely is an event to happen?**

A probability is always between `0` and `1`.

- `0` means impossible.
- `1` means certain.
- `0.5` means a 50% chance.

---

## 1. The words you need

| Word | Simple meaning | Example: rolling a die |
|---|---|---|
| **Outcome** | One possible result | rolling a 4 |
| **Sample space** (`Ω`) | Every possible outcome | `{1, 2, 3, 4, 5, 6}` |
| **Event** (`A`) | A group of outcomes we care about | roll an even number: `{2, 4, 6}` |

---

## Question 1 — What is the chance of rolling an even number?

A fair die has six equally likely outcomes: `{1, 2, 3, 4, 5, 6}`.

The favourable outcomes for an even number are `{2, 4, 6}`. There are three.

### Formula

```text
P(A) = number of favourable outcomes / total number of equally likely outcomes
```

### Answer

```text
P(even) = 3 / 6 = 1 / 2 = 0.5
```

There is a **50% chance** of rolling an even number.

> This simple fraction formula works only when every outcome has the same chance. A fair die and a well-shuffled deck are common examples.

---

## 2. The three basic probability rules

### Rule 1 — Range rule

```text
0 ≤ P(A) ≤ 1
```

A probability cannot be negative and cannot be greater than 1.

### Rule 2 — Certain event rule

```text
P(Ω) = 1
```

Something in the full sample space must happen. When rolling a die, you must get one of `{1, 2, 3, 4, 5, 6}`.

### Rule 3 — Impossible event rule

```text
P(∅) = 0
```

`∅` means an empty event. Rolling a 7 on an ordinary six-sided die is impossible.

---

## Question 2 — What is the chance of *not* rolling a 6?

Let `A` mean “roll a 6.” Its complement, written `Aᶜ`, means “do not roll a 6.”

### Complement formula

```text
P(Aᶜ) = 1 - P(A)
```

### Answer

```text
P(roll 6) = 1 / 6
P(not 6) = 1 - 1 / 6 = 5 / 6 ≈ 0.83
```

There is an **83% chance** of not rolling a 6.

---

## Question 3 — What is the chance of drawing a heart or a king?

A standard deck has 52 cards.

- 13 cards are hearts.
- 4 cards are kings.
- 1 card is both a heart and a king: the king of hearts.

If we simply add `13 + 4`, we count the king of hearts twice. We must subtract it once.

### Addition rule

```text
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
```

| Symbol | Meaning |
|---|---|
| `A ∪ B` | A or B or both |
| `A ∩ B` | A and B together |

### Answer

```text
P(heart or king) = 13/52 + 4/52 - 1/52
                  = 16/52
                  = 4/13 ≈ 0.31
```

There is about a **31% chance** of drawing a heart or a king.

---

## Key formula summary

```text
Basic probability:     P(A) = favourable / total
Complement:            P(Aᶜ) = 1 - P(A)
Addition rule:         P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
Range:                 0 ≤ P(A) ≤ 1
Certain event:         P(Ω) = 1
Impossible event:      P(∅) = 0
```

## Practice

1. A bag has 3 red and 7 blue balls. What is `P(red)`?
2. For the same bag, what is `P(not red)`?
3. In a deck, what is `P(queen or spade)`? Remember the queen of spades belongs to both groups.

### Answers

```text
1. 3/10 = 0.30
2. 7/10 = 0.70
3. 4/52 + 13/52 - 1/52 = 16/52 = 4/13
```
