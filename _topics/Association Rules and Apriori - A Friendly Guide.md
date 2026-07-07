---
title: "25. Association Rules and Apriori - A Friendly Guide"
category: Machine Learning
order: 25
tags:
  - machine-learning
  - association-rules
  - apriori
  - market-basket-analysis
  - unsupervised-learning
  - support
  - confidence
  - lift
  - beginners
  - friendly
summary: A beginner-friendly guide to association rules and the Apriori algorithm. Learn how to find "customers who bought X also bought Y" patterns in transaction data, with support, confidence, lift explained and full Python examples.
---

# Association Rules and Apriori

## Discovering "also bought" patterns in data

When you shop on Amazon, the website shows "Customers who bought this also bought…". When Netflix shows "Because you watched X, you might like Y." These recommendations come from **association rule mining** — finding patterns in large collections of transactions.

This tutorial covers:

1. What association rules are.
2. The three key metrics: support, confidence, lift.
3. The Apriori algorithm — how it finds rules efficiently.
4. Full Python demonstration.
5. Real-world applications beyond shopping.

---

## 1. What is an association rule?

An association rule has the form:

```
{bread, butter} → {milk}
```

"If a customer buys bread and butter, they also tend to buy milk."

The left side is the **antecedent** (if…). The right side is the **consequent** (then…).

The data is a collection of **transactions** — each transaction is a set of items purchased together:

| Transaction | Items |
|-------------|-------|
| T1 | bread, butter, milk |
| T2 | bread, butter |
| T3 | milk, eggs |
| T4 | bread, milk, eggs |
| T5 | butter, milk, eggs |

From this data we want to find rules like `{bread, butter} → {milk}` that hold frequently.

---

## 2. The three key metrics

### Support — how common is this combination?

```
Support({bread, butter}) = transactions containing bread AND butter
                           ─────────────────────────────────────────
                                    total transactions

= 3/5 = 0.60  (60% of transactions contain both)
```

Low support means the rule rarely applies. Typically you set a **minimum support threshold** to filter out rare patterns.

### Confidence — how reliable is the rule?

```
Confidence({bread, butter} → {milk}) = Support({bread, butter, milk})
                                        ──────────────────────────────
                                          Support({bread, butter})

= (2/5) / (3/5) = 0.67
```

"In 67% of transactions where bread and butter appear, milk also appears."

### Lift — is the rule better than chance?

```
Lift({bread, butter} → {milk}) = Confidence({bread, butter} → {milk})
                                  ──────────────────────────────────────
                                            Support({milk})

= 0.67 / (4/5) = 0.67 / 0.80 = 0.84
```

| Lift value | Meaning |
|-----------|---------|
| Lift > 1 | The items appear together more than by chance — genuine association |
| Lift = 1 | Items are independent — the rule adds no value |
| Lift < 1 | Items appear together less than by chance — negative association |

**Lift is the most important metric.** High support and confidence with low lift just means both items are popular — there is no real connection.

> **Memory trick:** Support = how often. Confidence = how reliable. Lift = how much better than random.

---

## 3. The Apriori algorithm

With 10,000 products, there are billions of possible item combinations. Checking all of them is impossible.

**Apriori** uses one key insight: **if a set is infrequent, all its supersets are also infrequent**.

If `{bread, caviar}` is rare, then `{bread, caviar, milk}` is also rare — no need to check it.

This lets Apriori prune the search space dramatically:

```
Step 1: Find all individual items with support ≥ min_support
        {bread: 0.80, butter: 0.60, milk: 0.80, eggs: 0.60}  ← all pass

Step 2: Find all pairs with support ≥ min_support
        {bread, butter}: 0.60 ✓
        {bread, milk}:   0.60 ✓
        {butter, milk}:  0.60 ✓
        {bread, eggs}:   0.20 ✗  ← removed, and all larger sets with bread+eggs too

Step 3: Find all triples from the surviving pairs
        {bread, butter, milk}: check support
        ...

Step 4: Generate rules from frequent itemsets
        {bread, butter} → {milk}  confidence=0.67, lift=0.84
        {milk, butter}  → {eggs}  confidence=...
        ...
```

---

## 4. Full Python demonstration

```python
# Install: pip install mlxtend
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Transaction dataset
transactions = [
    ['bread', 'butter', 'milk'],
    ['bread', 'butter'],
    ['milk', 'eggs'],
    ['bread', 'milk', 'eggs'],
    ['butter', 'milk', 'eggs'],
    ['bread', 'butter', 'milk', 'eggs'],
    ['bread', 'milk'],
    ['butter', 'eggs'],
    ['bread', 'eggs'],
    ['milk', 'butter', 'bread'],
]

# Step 1 — Encode transactions as a binary matrix
te = TransactionEncoder()
te_array = te.fit_transform(transactions)
df = pd.DataFrame(te_array, columns=te.columns_)
print(df.head())
#    bread  butter   eggs   milk
# 0   True    True  False   True
# 1   True    True  False  False
# ...

# Step 2 — Find frequent itemsets (support >= 50%)
frequent_itemsets = apriori(df, min_support=0.5, use_colnames=True)
print("\nFrequent itemsets:")
print(frequent_itemsets.sort_values('support', ascending=False))

# Step 3 — Generate association rules (confidence >= 60%)
rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.6)
rules = rules.sort_values('lift', ascending=False)

print("\nTop association rules by lift:")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_string())
```

### Filtering the best rules

```python
# Keep only rules with high lift AND high confidence
strong_rules = rules[
    (rules['lift'] > 1.2) &
    (rules['confidence'] > 0.7)
]
print("\nStrong rules (lift > 1.2 AND confidence > 0.7):")
print(strong_rules[['antecedents', 'consequents', 'confidence', 'lift']])
```

### Visualising rules

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.scatter(rules['support'], rules['confidence'],
            c=rules['lift'], cmap='RdYlGn', s=100, alpha=0.7)
plt.colorbar(label='Lift')
plt.xlabel('Support')
plt.ylabel('Confidence')
plt.title('Association Rules — Support vs Confidence (colour = Lift)')
plt.tight_layout()
plt.show()
```

---

## 5. Real-world applications

| Application | What the "items" are | What a rule looks like |
|-------------|---------------------|----------------------|
| **Retail basket analysis** | Products purchased | `{nappies} → {beer}` (famous example) |
| **Netflix / Spotify** | Movies or songs watched | `{Inception} → {Interstellar}` |
| **Medical diagnosis** | Symptoms or diagnoses | `{fever, cough} → {flu}` |
| **Web navigation** | Pages visited in a session | `{homepage, pricing} → {signup}` |
| **Cross-selling** | Customer purchases | `{laptop} → {mouse, keyboard}` |
| **Fraud detection** | Transaction patterns | `{foreign_ATM, large_withdrawal} → {fraud}` |

---

## 6. Choosing thresholds

| Parameter | Typical range | Effect of too low | Effect of too high |
|-----------|--------------|------------------|-------------------|
| `min_support` | 0.01 – 0.10 | Millions of rules, slow | Misses rare but valuable patterns |
| `min_confidence` | 0.50 – 0.80 | Unreliable rules included | Too few rules |
| `min_lift` | 1.0 – 2.0 | Obvious rules included | Misses moderate associations |

For large e-commerce datasets, `min_support=0.01` (1%) is typical. For small datasets, 5–10% is more appropriate.

---

## Summary

- Association rules find "if A then B" patterns in transaction data.
- **Support** = how often the combination appears. **Confidence** = how reliable the rule is. **Lift** = how much better than chance.
- **Apriori** prunes the search space using the principle that subsets of infrequent sets are also infrequent.
- Filter rules by **lift > 1** to keep only genuine associations, not just popular items.
- Applications go far beyond shopping: recommendations, medical patterns, fraud, web analytics.
- Use `mlxtend` in Python for a complete Apriori implementation.
