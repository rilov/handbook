---
title: "Mathematics 03: Conditional Probability — Questions, Formulas, and Python"
category: Mathematics
order: 3
tags:
  - mathematics
  - probability
  - conditional-probability
  - python
  - beginners
summary: "Learn conditional probability using simple class examples, complete formulas, input validation, and a Python solution."
---

# Mathematics 03: Conditional Probability

Conditional probability means:

> **What is the chance of A when we already know B happened?**

The words **given that** are the most important clue.

---

## The class question

You receive a tuple in this order:

```text
(total students, passed Math, passed both Math and Science)
```

Write a Python program that finds:

> What is the probability that a student passed Science **given that** the student passed Math?

The output must be rounded to two decimal places. Invalid inputs must print `Invalid input`.

### Example input

```text
(20, 5, 5)
```

### Example output

```text
1
```

---

## 1. Name the values first

Let:

| Symbol | Meaning |
|---|---|
| `T` | total number of students |
| `M` | students who passed Math |
| `S` | students who passed Science |
| `B` | students who passed both Math and Science |

The input tuple is `(T, M, B)`.

For `(20, 5, 5)`:

```text
T = 20
M = 5
B = 5
```

---

## 2. Basic probability formula

### Question — What is the chance that a randomly chosen student passed Math?

### Formula

```text
P(A) = number of favourable outcomes / total number of outcomes
```

For Math:

```text
P(M) = M / T
```

For `(20, 5, 5)`:

```text
P(M) = 5 / 20 = 0.25
```

So 25% of all students passed Math.

---

## 3. Intersection probability

The symbol `∩` means **and** or **both**.

```text
M ∩ S = passed Math and Science
```

### Formula

```text
P(M ∩ S) = B / T
```

For `(20, 5, 5)`:

```text
P(M ∩ S) = 5 / 20 = 0.25
```

So 25% of all students passed both subjects.

---

## 4. Conditional probability

We do not ask about every student in the class anymore. We narrow the group to only students who passed Math.

The question is:

```text
P(S | M)
```

Read this as:

> Probability of passing Science **given** that the student passed Math.

### Conditional probability formula

```text
P(A | B) = P(A ∩ B) / P(B), where P(B) > 0
```

For this question:

```text
P(S | M) = P(S ∩ M) / P(M)
```

Substitute the formulas from the previous sections:

```text
P(S | M) = (B / T) / (M / T)
```

Dividing by a fraction means multiplying by its reciprocal:

```text
P(S | M) = (B / T) × (T / M)
```

`T` cancels:

```text
P(S | M) = B / M
```

### Final program formula

```text
P(Science | Math) = passed both Math and Science / passed Math
                   = B / M
```

In plain English:

> From the students who passed Math, find the fraction who also passed Science.

The total `T` is not needed for the final division. It is still important for validating that the input describes a possible class.

---

## Worked example 1 — `(20, 5, 5)`

```text
M = 5
B = 5

P(S | M) = B / M
         = 5 / 5
         = 1
```

Output:

```text
1
```

Every student who passed Math also passed Science. `1` means 100%.

---

## Worked example 2 — `(20, 5, 2)`

```text
M = 5
B = 2

P(S | M) = 2 / 5
         = 0.4
```

Output:

```text
0.4
```

Among Math-passing students, 40% also passed Science.

---

## Worked example 3 — `(20, 8, 3)`

```text
P(S | M) = 3 / 8
         = 0.375
```

Rounded to two decimal places:

```text
0.38
```

---

## 5. Why `(20, 5, 10)` is invalid

This input says:

```text
5 students passed Math
10 students passed both Math and Science
```

This is impossible. Everyone who passed both subjects must be included in the students who passed Math.

```text
B ≤ M
```

But here:

```text
10 > 5
```

So the correct output is:

```text
Invalid input
```

---

## 6. Input validation equations

A valid input must satisfy all of these rules:

```text
T > 0
0 < M ≤ T
0 ≤ B ≤ M
```

| Rule | Why it matters |
|---|---|
| `T > 0` | A class must contain at least one student. |
| `M > 0` | We cannot calculate `B / M` when `M` is zero. |
| `M ≤ T` | More students cannot pass Math than exist in the class. |
| `B ≥ 0` | A student count cannot be negative. |
| `B ≤ M` | Students passing both must also have passed Math. |

---

## 7. Python solution

```python
import ast

try:
    data = ast.literal_eval(input())

    if not isinstance(data, tuple) or len(data) != 3:
        print("Invalid input")
    else:
        total, math_passed, both_passed = data

        valid_counts = all(isinstance(value, int) and not isinstance(value, bool) for value in data)
        valid_relationships = (
            total > 0
            and math_passed > 0
            and math_passed <= total
            and both_passed >= 0
            and both_passed <= math_passed
        )

        if not valid_counts or not valid_relationships:
            print("Invalid input")
        else:
            probability = both_passed / math_passed
            result = f"{probability:.2f}".rstrip("0").rstrip(".")
            print(result)
except (SyntaxError, ValueError):
    print("Invalid input")
```

### Why use `ast.literal_eval`?

The input looks like a Python tuple: `(20, 5, 5)`.

`ast.literal_eval` safely converts simple literal values such as tuples and integers. Do **not** use `eval` for user input because it can execute arbitrary Python code.

---

## 8. Trace the program

Input:

```text
(20, 8, 3)
```

The program does this:

```text
1. Reads T=20, M=8, B=3.
2. Checks 20 > 0: valid.
3. Checks 0 < 8 ≤ 20: valid.
4. Checks 0 ≤ 3 ≤ 8: valid.
5. Calculates B / M = 3 / 8 = 0.375.
6. Rounds to two decimal places: 0.38.
```

Output:

```text
0.38
```

## Formula summary

```text
Basic probability:         P(M) = M / T
Intersection probability:  P(M ∩ S) = B / T
Conditional probability:   P(A | B) = P(A ∩ B) / P(B)
This question:             P(S | M) = (B / T) / (M / T) = B / M
Validation:                T > 0, 0 < M ≤ T, 0 ≤ B ≤ M
```

## Practice

1. What should the program print for `(50, 20, 15)`?
2. Why is `(30, 0, 0)` invalid for this specific question?
3. Why is `(10, 11, 2)` invalid?

### Answers

```text
1. 15 / 20 = 0.75
2. It would require dividing by zero; there are no Math-passing students to condition on.
3. 11 Math-passing students cannot come from a class of only 10 students.
```
