---
title: "Statistics Formulas Cheat Sheet"
category: Data Science
order: 8
tags:
  - statistics
  - formulas
  - reference
  - cheat-sheet
summary: "Complete reference guide with all statistical formulas, explanations, and when to use them - your go-to resource for hypothesis testing, confidence intervals, and more."
---

# 📊 Statistics Formulas Cheat Sheet

## Quick Reference Guide

This cheat sheet contains all the essential statistical formulas you need, organized by topic with clear explanations and usage guidelines.

---

## 📐 Table of Contents

1. [Descriptive Statistics](#descriptive-statistics)
2. [Probability & Distributions](#probability-distributions)
3. [Sampling & Central Limit Theorem](#sampling-clt)
4. [Confidence Intervals](#confidence-intervals)
5. [Hypothesis Testing Basics](#hypothesis-testing-basics)
6. [Single Sample Tests](#single-sample-tests)
7. [Two Sample Tests](#two-sample-tests)
8. [Proportion Tests](#proportion-tests)
9. [Effect Sizes](#effect-sizes)
10. [Quick Decision Tree](#decision-tree)

---

## 1. Descriptive Statistics {#descriptive-statistics}

### Measures of Central Tendency

#### **Mean (Average)**
```
μ = (Σx) / N          [Population mean]
x̄ = (Σx) / n          [Sample mean]

Where:
- Σx = Sum of all values
- N = Population size
- n = Sample size
```

**When to use:** Most common measure, use when data is roughly symmetric without extreme outliers.

#### **Median (Middle Value)**
```
1. Sort data from smallest to largest
2. If n is odd: Median = middle value
3. If n is even: Median = average of two middle values
```

**When to use:** Better than mean when data has outliers or is skewed.

#### **Mode (Most Frequent)**
```
Mode = Value that appears most often
```

**When to use:** For categorical data or to find most common value.

### Measures of Spread

#### **Range**
```
Range = Maximum - Minimum
```

**When to use:** Quick measure of spread, but sensitive to outliers.

#### **Variance**
```
σ² = Σ(x - μ)² / N     [Population variance]
s² = Σ(x - x̄)² / (n-1) [Sample variance]

Where:
- σ² (sigma squared) = Population variance
- s² = Sample variance
- (n-1) = Degrees of freedom (Bessel's correction)
```

**When to use:** Measure of spread, but in squared units.

#### **Standard Deviation**
```
σ = √[Σ(x - μ)² / N]      [Population std dev]
s = √[Σ(x - x̄)² / (n-1)]  [Sample std dev]
```

**When to use:** Most common measure of spread, in original units.

#### **Coefficient of Variation**
```
CV = (s / x̄) × 100%

Where:
- CV = Coefficient of Variation
- s = Standard deviation
- x̄ = Mean
```

**When to use:** Compare variability between datasets with different units or scales.

### Measures of Position

#### **Percentile**
```
Percentile rank = (Number of values below x / Total values) × 100
```

**When to use:** Understand relative position in a distribution.

#### **Quartiles**
```
Q1 = 25th percentile (1st quartile)
Q2 = 50th percentile (median)
Q3 = 75th percentile (3rd quartile)
IQR = Q3 - Q1 (Interquartile Range)
```

**When to use:** Identify spread and detect outliers.

#### **Z-Score (Standardization)**
```
z = (x - μ) / σ        [Population]
z = (x - x̄) / s        [Sample]

Where:
- z = Standard score
- x = Individual value
- μ or x̄ = Mean
- σ or s = Standard deviation
```

**Interpretation:**
- z = 0: Value is at the mean
- z = 1: Value is 1 std dev above mean
- z = -1: Value is 1 std dev below mean
- |z| > 3: Likely an outlier

**When to use:** Standardize values, compare across different scales, detect outliers.

### Correlation

#### **Pearson Correlation Coefficient**
```
r = Σ[(x - x̄)(y - ȳ)] / √[Σ(x - x̄)² × Σ(y - ȳ)²]

Alternative formula:
r = [nΣxy - (Σx)(Σy)] / √{[nΣx² - (Σx)²][nΣy² - (Σy)²]}

Where:
- r = Correlation coefficient (-1 to +1)
- x, y = Individual values
- x̄, ȳ = Means
- n = Sample size
```

**Interpretation:**
- r = +1: Perfect positive correlation
- r = +0.7 to +1: Strong positive
- r = +0.3 to +0.7: Moderate positive
- r = 0: No correlation
- r = -0.3 to -0.7: Moderate negative
- r = -0.7 to -1: Strong negative
- r = -1: Perfect negative correlation

**When to use:** Measure linear relationship between two continuous variables.

---

## 2. Probability & Distributions {#probability-distributions}

### Basic Probability

#### **Probability Formula**
```
P(A) = (Number of favorable outcomes) / (Total number of outcomes)

Where:
- P(A) = Probability of event A
- 0 ≤ P(A) ≤ 1
```

#### **Complement Rule**
```
P(not A) = 1 - P(A)
```

#### **Addition Rule (OR)**
```
P(A or B) = P(A) + P(B) - P(A and B)

If mutually exclusive:
P(A or B) = P(A) + P(B)
```

#### **Multiplication Rule (AND)**
```
P(A and B) = P(A) × P(B|A)

If independent:
P(A and B) = P(A) × P(B)
```

### Normal Distribution

#### **Standard Normal Distribution**
```
Z ~ N(0, 1)

Where:
- Mean (μ) = 0
- Standard deviation (σ) = 1
```

**Key Properties:**
- 68% of data within ±1σ
- 95% of data within ±1.96σ
- 99% of data within ±2.58σ

#### **Converting to Standard Normal**
```
Z = (X - μ) / σ

Where:
- Z = Standard normal variable
- X = Original variable
- μ = Mean
- σ = Standard deviation
```

**When to use:** Find probabilities, compare values across different distributions.

---

## 3. Sampling & Central Limit Theorem {#sampling-clt}

### Sampling Distribution

#### **Mean of Sampling Distribution**
```
μx̄ = μ

Where:
- μx̄ = Mean of sample means
- μ = Population mean
```

**Interpretation:** The average of all sample means equals the population mean.

#### **Standard Error (SE)**
```
SE = σ / √n

Where:
- SE = Standard error (std dev of sampling distribution)
- σ = Population standard deviation
- n = Sample size
```

**When to use:** Measure variability of sample means, calculate confidence intervals.

**Key insight:** Larger sample size → Smaller standard error → More precise estimates

### Central Limit Theorem

#### **CLT Statement**
```
For n ≥ 30:
x̄ ~ N(μ, σ/√n)

Where:
- x̄ = Sample mean
- N = Normal distribution
- μ = Population mean
- σ/√n = Standard error
```

**What it means:** Sample means are approximately normally distributed, regardless of the population's distribution, when sample size is large enough.

**Requirements:**
- Random sampling
- Sample size n ≥ 30 (or population is already normal)
- Independent observations

---

## 4. Confidence Intervals {#confidence-intervals}

### Confidence Interval for Mean (σ known)

#### **Z-Interval Formula**
```
CI = x̄ ± Z* × (σ / √n)

Where:
- CI = Confidence interval
- x̄ = Sample mean
- Z* = Critical z-value
- σ = Population standard deviation
- n = Sample size
```

**Common Z* values:**
- 90% confidence: Z* = 1.645
- 95% confidence: Z* = 1.96
- 99% confidence: Z* = 2.576

**When to use:** Population standard deviation is known (rare in practice).

### Confidence Interval for Mean (σ unknown)

#### **T-Interval Formula**
```
CI = x̄ ± t* × (s / √n)

Where:
- t* = Critical t-value (from t-table)
- s = Sample standard deviation
- df = n - 1 (degrees of freedom)
```

**When to use:** Population standard deviation is unknown (most common case).

### Confidence Interval for Proportion

#### **Proportion CI Formula**
```
CI = p̂ ± Z* × √[p̂(1 - p̂) / n]

Where:
- p̂ = Sample proportion
- Z* = Critical z-value
- n = Sample size
```

**Requirements:**
- np̂ ≥ 10
- n(1 - p̂) ≥ 10

**When to use:** Estimate population proportion from sample proportion.

### Margin of Error

#### **Margin of Error Formula**
```
ME = Z* × (σ / √n)     [Known σ]
ME = t* × (s / √n)     [Unknown σ]

Where:
- ME = Margin of error
- Larger ME = Less precise estimate
- Smaller ME = More precise estimate
```

**How to reduce margin of error:**
- Increase sample size (n)
- Accept lower confidence level
- Reduce population variability (can't control)

---

## 5. Hypothesis Testing Basics {#hypothesis-testing-basics}

### Hypotheses Setup

#### **Null Hypothesis (H₀)**
```
H₀: μ = μ₀     [No difference/change]
H₀: μ₁ = μ₂    [Two groups are equal]
H₀: p = p₀     [Proportion equals claimed value]
```

**Interpretation:** Status quo, no effect, no difference.

#### **Alternative Hypothesis (H₁)**
```
Two-tailed:  H₁: μ ≠ μ₀   [Different from]
Right-tailed: H₁: μ > μ₀   [Greater than]
Left-tailed:  H₁: μ < μ₀   [Less than]
```

### Significance Level (α)

```
α = Probability of Type I Error

Common values:
- α = 0.05 (5%) - Most common
- α = 0.01 (1%) - More strict
- α = 0.10 (10%) - More lenient
```

**Interpretation:** Maximum acceptable probability of rejecting H₀ when it's actually true.

### P-Value

#### **P-Value Definition**
```
p-value = P(observing data this extreme | H₀ is true)
```

**Decision Rule:**
- If p-value < α: Reject H₀ (statistically significant)
- If p-value ≥ α: Fail to reject H₀ (not significant)

**Interpretation:**
- p < 0.01: Very strong evidence against H₀
- p < 0.05: Strong evidence against H₀
- p < 0.10: Moderate evidence against H₀
- p ≥ 0.10: Weak or no evidence against H₀

### Type I and Type II Errors

```
Type I Error (α):
- Reject H₀ when H₀ is true
- "False Positive"
- Probability = α

Type II Error (β):
- Fail to reject H₀ when H₀ is false
- "False Negative"
- Probability = β

Power = 1 - β
- Probability of correctly rejecting false H₀
```

---

## 6. Single Sample Tests {#single-sample-tests}

### One-Sample Z-Test (σ known)

#### **Test Statistic**
```
z = (x̄ - μ₀) / (σ / √n)

Where:
- x̄ = Sample mean
- μ₀ = Claimed population mean
- σ = Population standard deviation
- n = Sample size
```

**Requirements:**
- Population standard deviation (σ) is known
- n ≥ 30, OR population is normally distributed
- Random sample

**When to use:** Testing if sample mean differs from claimed value, σ known.

### One-Sample T-Test (σ unknown)

#### **Test Statistic**
```
t = (x̄ - μ₀) / (s / √n)

Where:
- s = Sample standard deviation
- df = n - 1 (degrees of freedom)
```

**Requirements:**
- Population standard deviation (σ) is unknown
- n ≥ 30, OR population is normally distributed
- Random sample

**When to use:** Testing if sample mean differs from claimed value, σ unknown (most common).

**Decision:**
- Compare |t| to critical value t* from t-table
- OR compare p-value to α

---

## 7. Two Sample Tests {#two-sample-tests}

### Independent Two-Sample T-Test

#### **Test Statistic (Equal Variances)**
```
t = (x̄₁ - x̄₂) / √[s²ₚ(1/n₁ + 1/n₂)]

Where:
Pooled variance:
s²ₚ = [(n₁-1)s₁² + (n₂-1)s₂²] / (n₁ + n₂ - 2)

Degrees of freedom:
df = n₁ + n₂ - 2
```

**Requirements:**
- Two independent groups
- Both groups approximately normally distributed
- Equal variances (test with F-test or Levene's test)

#### **Test Statistic (Unequal Variances - Welch's t-test)**
```
t = (x̄₁ - x̄₂) / √[(s₁²/n₁) + (s₂²/n₂)]

Degrees of freedom (Welch-Satterthwaite):
df = [(s₁²/n₁ + s₂²/n₂)²] / [(s₁²/n₁)²/(n₁-1) + (s₂²/n₂)²/(n₂-1)]
```

**When to use:** Comparing means of two independent groups.

### Paired T-Test

#### **Test Statistic**
```
t = d̄ / (sᵈ / √n)

Where:
- d̄ = Mean of differences
- sᵈ = Standard deviation of differences
- n = Number of pairs
- df = n - 1
```

**Steps:**
1. Calculate differences: d = x₁ - x₂ for each pair
2. Calculate mean of differences: d̄
3. Calculate standard deviation of differences: sᵈ
4. Compute t-statistic

**Requirements:**
- Same subjects measured twice (paired data)
- Differences are approximately normally distributed
- Random sample

**When to use:** Before/after comparisons, matched pairs.

---

## 8. Proportion Tests {#proportion-tests}

### One-Sample Proportion Test

#### **Test Statistic**
```
z = (p̂ - p₀) / √[p₀(1 - p₀) / n]

Where:
- p̂ = Sample proportion (x/n)
- p₀ = Claimed population proportion
- x = Number of successes
- n = Sample size
```

**Requirements:**
- np₀ ≥ 10
- n(1 - p₀) ≥ 10
- Random sample

**When to use:** Testing if sample proportion differs from claimed proportion.

### Two-Sample Proportion Test

#### **Test Statistic**
```
z = (p̂₁ - p̂₂) / √[p̂(1 - p̂)(1/n₁ + 1/n₂)]

Where:
Pooled proportion:
p̂ = (x₁ + x₂) / (n₁ + n₂)

- p̂₁ = x₁/n₁ (proportion in group 1)
- p̂₂ = x₂/n₂ (proportion in group 2)
```

**Requirements:**
- n₁p̂₁ ≥ 10, n₁(1-p̂₁) ≥ 10
- n₂p̂₂ ≥ 10, n₂(1-p̂₂) ≥ 10
- Independent groups
- Random samples

**When to use:** Comparing proportions between two independent groups.

---

## 9. Effect Sizes {#effect-sizes}

### Cohen's d (Standardized Mean Difference)

#### **For Independent Samples**
```
d = (x̄₁ - x̄₂) / sₚₒₒₗₑᵈ

Where:
sₚₒₒₗₑᵈ = √[(s₁² + s₂²) / 2]
```

**Interpretation:**
- |d| = 0.2: Small effect
- |d| = 0.5: Medium effect
- |d| = 0.8: Large effect

#### **For Paired Samples**
```
d = d̄ / sᵈ

Where:
- d̄ = Mean of differences
- sᵈ = Standard deviation of differences
```

**When to use:** Measure practical significance (how big is the difference?).

### R² (Coefficient of Determination)

```
R² = r²

Where:
- r = Correlation coefficient
- R² = Proportion of variance explained
```

**Interpretation:**
- R² = 0.01: Small effect (1% variance explained)
- R² = 0.09: Medium effect (9% variance explained)
- R² = 0.25: Large effect (25% variance explained)

**When to use:** Measure strength of relationship in correlation/regression.

---

## 10. Quick Decision Tree {#decision-tree}

### Which Test Should I Use?

```
START: What are you comparing?

├─ ONE sample to a claimed value
│  ├─ Data type: MEAN (continuous)
│  │  ├─ σ known? → Z-test
│  │  └─ σ unknown? → One-sample t-test
│  └─ Data type: PROPORTION (categorical)
│     └─ One-sample proportion test (z-test)
│
├─ TWO groups
│  ├─ Data type: MEANS (continuous)
│  │  ├─ Independent groups? → Independent t-test
│  │  └─ Paired/matched? → Paired t-test
│  └─ Data type: PROPORTIONS (categorical)
│     └─ Two-sample proportion test (z-test)
│
└─ RELATIONSHIP between two variables
   └─ Both continuous? → Pearson correlation (r)
```

### Sample Size Requirements

```
Test Type          | Minimum Sample Size
-------------------|--------------------
Z-test             | n ≥ 30
T-test             | n ≥ 30 (or normal population)
Proportion test    | np ≥ 10 AND n(1-p) ≥ 10
Paired t-test      | n ≥ 30 pairs (or normal differences)
Independent t-test | n₁, n₂ ≥ 30 (or both normal)
```

---

## 📝 Common Symbols Reference

| Symbol | Meaning |
|--------|---------|
| μ (mu) | Population mean |
| x̄ (x-bar) | Sample mean |
| σ (sigma) | Population standard deviation |
| s | Sample standard deviation |
| σ² | Population variance |
| s² | Sample variance |
| n | Sample size |
| N | Population size |
| α (alpha) | Significance level |
| β (beta) | Type II error probability |
| p̂ (p-hat) | Sample proportion |
| p | Population proportion |
| df | Degrees of freedom |
| SE | Standard error |
| CI | Confidence interval |
| ME | Margin of error |
| H₀ | Null hypothesis |
| H₁ | Alternative hypothesis |
| r | Correlation coefficient |
| t | t-statistic |
| z | z-statistic |
| Σ (sigma) | Sum of |

---

## 🎯 Quick Tips

### Choosing Confidence Level
- **90%:** Quick estimates, exploratory analysis
- **95%:** Standard for most research (most common)
- **99%:** High-stakes decisions, need more certainty

### Interpreting Results
1. **Check assumptions first** (normality, sample size, independence)
2. **Look at p-value** (is it < α?)
3. **Check effect size** (is the difference meaningful?)
4. **Consider practical significance** (does it matter in real life?)

### Common Mistakes to Avoid
- ❌ Using z-test when σ is unknown (use t-test instead)
- ❌ Using independent t-test for paired data (use paired t-test)
- ❌ Confusing statistical significance with practical importance
- ❌ Interpreting p-value as probability that H₀ is true
- ❌ Accepting H₀ (we "fail to reject," not "accept")
- ❌ Using proportion test for means or vice versa

---

## 📚 Related Resources

- **Chapter 1:** Exploratory Data Analysis
- **Chapter 2:** Inferential Statistics and Hypothesis Testing
- **Chapter 3:** Introduction to Hypothesis Testing
- **Chapter 4.1:** Single Sample Tests
- **Chapter 4.2:** Two Sample Tests
- **Chapter 4.3:** Proportion Tests

---

**Print this page and keep it handy for quick reference!** 📄

*Last updated: 2026*
