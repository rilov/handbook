---
title: "Chapter 3: Introduction to Hypothesis Testing"
category: Data Science
order: 3
tags:
  - statistics
  - hypothesis-testing
  - p-value
  - significance
summary: "Master the fundamentals of hypothesis testing - learn the 5-step process, understand p-values, and avoid common errors in statistical testing."
---

# Chapter 3: Introduction to Hypothesis Testing

## Welcome to Hypothesis Testing! 🎯

**Hypothesis testing** is one of the most powerful tools in statistics. It provides a rigorous, mathematical framework for making decisions when we're uncertain about the truth.

**The Core Challenge:**

Every day, people make claims:
- "Our new app increases user engagement by 20%"
- "This teaching method improves test scores"
- "Men and women have different preferences for this product"
- "The average delivery time is under 30 minutes"

But how do we know if these claims are true or just random chance? That's where hypothesis testing comes in.

**The Detective Analogy:**

Imagine you're a detective investigating a case:
- **The Suspect:** A claim about the world (hypothesis)
- **Your Job:** Collect evidence (data) to determine if the claim is likely true or false
- **The Standard:** "Beyond reasonable doubt" (statistical significance)
- **The Verdict:** Reject the claim or fail to reject it based on evidence

Just like a detective doesn't "prove" guilt but shows evidence beyond reasonable doubt, we don't "prove" hypotheses - we determine if there's enough statistical evidence to support or reject them.

---

## Table of Contents
1. [What is Hypothesis Testing?](#what-is-hypothesis-testing)
2. [The Detective's Toolkit - Key Concepts](#key-concepts)
3. [The 5-Step Process](#five-step-process)
4. [Types of Errors](#types-of-errors)
5. [One-Tailed vs Two-Tailed Tests](#tailed-tests)
6. [Complete Python Example](#python-example)

---

## 1. What is Hypothesis Testing? {#what-is-hypothesis-testing}

### The Simple Explanation

**Hypothesis testing** is like being a judge in a courtroom:
- Someone makes a claim (like "This coin is fair")
- You collect evidence (flip the coin many times)
- You decide: Is there enough evidence to reject the claim?

### Real-Life Examples

**Example 1: The Coin Mystery** 🪙
- **Claim**: "This coin is fair (50% heads, 50% tails)"
- **Evidence**: You flip it 100 times and get 65 heads
- **Question**: Is the coin really fair, or is it biased?

**Example 2: The Medicine Mystery** 💊
- **Claim**: "This new medicine works better than the old one"
- **Evidence**: You test it on 200 patients
- **Question**: Does the new medicine really work better?

**Example 3: The Website Mystery** 🖱️
- **Claim**: "The new website design gets more clicks"
- **Evidence**: You track clicks for 1000 visitors
- **Question**: Is the new design really better?

---

## 2. The Detective's Toolkit - Key Concepts {#key-concepts}

### 🎯 The Two Hypotheses

Every hypothesis test has TWO competing claims:

#### **H₀ (Null Hypothesis)** - "The Boring Claim"
- This is what everyone currently believes
- It's the "nothing special is happening" claim
- We try to find evidence AGAINST this

**Examples:**
- "The coin is fair" (50% heads)
- "The new medicine is no better than the old one"
- "The average height is 170 cm"

#### **H₁ (Alternative Hypothesis)** - "The Interesting Claim"
- This is what we think might be true
- It's the "something special IS happening" claim
- We try to find evidence FOR this

**Examples:**
- "The coin is NOT fair" (not 50% heads)
- "The new medicine IS better"
- "The average height is NOT 170 cm"

### 📊 P-Value - "How Weird Is Your Evidence?"

The **p-value** is perhaps the most misunderstood concept in statistics. Let's break it down clearly.

**Formal Definition:**
> The p-value is the probability of observing data as extreme as (or more extreme than) what we actually observed, **assuming the null hypothesis is true**.

**What does this really mean?**

Imagine you flip a coin 100 times and get 65 heads. You wonder: "Is this coin fair?"
- If the coin IS fair (H₀ is true), what's the chance of getting 65+ heads just by luck?
- That probability is the p-value
- If it's very small (say, 0.01 or 1%), then either:
  - You witnessed a very rare event, OR
  - The coin isn't actually fair (more likely!)

**Interpreting P-Values:**

- **p < 0.01 (Very small):** "This is extremely unlikely to happen by chance. Strong evidence against H₀"
- **p < 0.05 (Small):** "This is unlikely to happen by chance. Moderate evidence against H₀"
- **p > 0.05 (Large):** "This could easily happen by chance. Weak evidence against H₀"
- **p > 0.10 (Very large):** "This is quite likely to happen by chance. No evidence against H₀"

**The Magic Number: 0.05 (5%)**

By convention, we use α = 0.05 as our threshold:
- **If p-value < 0.05:** Evidence is strong enough → **Reject H₀** (statistically significant)
- **If p-value ≥ 0.05:** Evidence is not strong enough → **Fail to reject H₀** (not significant)

**Important Misconceptions:**

❌ **WRONG:** "p-value is the probability that H₀ is true"
✅ **CORRECT:** "p-value is the probability of seeing this data if H₀ were true"

❌ **WRONG:** "p = 0.05 means there's a 5% chance we're wrong"
✅ **CORRECT:** "p = 0.05 means if H₀ is true, we'd see data this extreme 5% of the time"

❌ **WRONG:** "p < 0.05 proves H₁ is true"
✅ **CORRECT:** "p < 0.05 suggests H₀ is unlikely, so we reject it in favor of H₁"

### 🧮 How to Calculate P-Values - Step by Step

Now let's learn **how** p-values are actually calculated!

#### **Step 1: Calculate the Test Statistic**

The test statistic measures how far your sample result is from what H₀ claims, in units of standard error.

**General Formula:**
```
Test Statistic = (Observed Value - Expected Value) / Standard Error
```

**For different tests:**

**Z-test (proportions or means with known σ):**
```
z = (p̂ - p₀) / √[p₀(1-p₀)/n]        [For proportions]
z = (x̄ - μ₀) / (σ/√n)                [For means]

Where:
- p̂ = Sample proportion
- p₀ = Claimed proportion
- x̄ = Sample mean
- μ₀ = Claimed mean
- σ = Population standard deviation
- n = Sample size
```

**T-test (means with unknown σ):**
```
t = (x̄ - μ₀) / (s/√n)

Where:
- s = Sample standard deviation
```

**Example Calculation:**
```
Coin flip example:
- Flipped 100 times, got 65 heads
- H₀: p = 0.50 (fair coin)
- p̂ = 65/100 = 0.65

Calculate z:
z = (0.65 - 0.50) / √[0.50(1-0.50)/100]
z = 0.15 / √[0.25/100]
z = 0.15 / √0.0025
z = 0.15 / 0.05
z = 3.0
```

#### **Step 2: Convert Test Statistic to P-Value**

The p-value is the probability of getting a test statistic as extreme (or more extreme) than what you observed, if H₀ is true.

**Method 1: Using Z-Table or T-Table**

For **two-tailed test:**
1. Find the area in the tail beyond your test statistic
2. Multiply by 2 (because we check both tails)

**Example with z = 3.0:**
```
1. Look up z = 3.0 in standard normal table
2. Area beyond z = 3.0 is 0.0013
3. Two-tailed p-value = 2 × 0.0013 = 0.0026
```

For **one-tailed test:**
- Just use the area in one tail (don't multiply by 2)

**Method 2: Using Python/Calculator**

```python
from scipy import stats

# For z-test (two-tailed)
z_statistic = 3.0
p_value = 2 * (1 - stats.norm.cdf(abs(z_statistic)))
print(f"p-value = {p_value:.4f}")  # Output: 0.0027

# For t-test (two-tailed)
t_statistic = 2.5
df = 29  # degrees of freedom (n-1)
p_value = 2 * (1 - stats.t.cdf(abs(t_statistic), df))
print(f"p-value = {p_value:.4f}")
```

#### **Step 3: Interpret the P-Value**

**What the p-value tells you:**

If p-value = 0.0027 (like our coin example):
- "If the coin were truly fair (H₀ true), there's only a 0.27% chance of getting results as extreme as 65 heads out of 100 flips"
- This is very unlikely!
- Since 0.0027 < 0.05, we reject H₀

**Visual Understanding:**

```
Standard Normal Distribution (z-distribution)

                    |
                   /|\
                  / | \
                 /  |  \
                /   |   \
               /    |    \
              /     |     \
    ---------|-----|-----|----------
           -3.0    0    3.0
            ↑            ↑
         0.13%        0.13%
         
Total in both tails = 0.13% + 0.13% = 0.26% ≈ p-value
```

### 🎚️ Significance Level (α) - "How Sure Do We Need to Be?"

The **significance level** (alpha, α) is like setting the bar for how much evidence you need:
- Usually set to **0.05** (which means 95% confidence)
- Sometimes **0.01** (99% confidence - very strict!)
- Sometimes **0.10** (90% confidence - more lenient)

**What it means:**
- α = 0.05 means: "I'm willing to be wrong 5% of the time"
- It's the threshold for deciding if evidence is strong enough

#### **How α is Chosen**

The significance level is chosen **before** you collect data based on:

1. **Field Standards:**
   - Science/Medicine: α = 0.05 or 0.01 (strict)
   - Social Sciences: α = 0.05 (standard)
   - Exploratory Research: α = 0.10 (lenient)

2. **Consequences of Error:**
   - High cost of Type I error → Use smaller α (0.01)
   - Example: Approving a dangerous drug
   
   - Lower cost of Type I error → Use larger α (0.10)
   - Example: Preliminary screening test

3. **Trade-off:**
   - Smaller α (0.01) → Harder to reject H₀ → Fewer Type I errors, more Type II errors
   - Larger α (0.10) → Easier to reject H₀ → More Type I errors, fewer Type II errors

#### **Critical Values - The Decision Boundary**

Instead of calculating p-values, you can use **critical values** to make decisions.

**What is a critical value?**
- The test statistic value that marks the boundary of the rejection region
- If your test statistic is more extreme than the critical value → Reject H₀

**How to find critical values:**

**For Z-test:**
```
Two-tailed test (α = 0.05):
Critical values: z = ±1.96

One-tailed test (α = 0.05):
Right-tailed: z = +1.645
Left-tailed: z = -1.645
```

**Common Z critical values:**
| Confidence Level | α (two-tailed) | Critical Value |
|------------------|----------------|----------------|
| 90% | 0.10 | ±1.645 |
| 95% | 0.05 | ±1.96 |
| 99% | 0.01 | ±2.576 |

**For T-test:**
- Critical values depend on degrees of freedom (df = n - 1)
- Look up in t-table or use Python

```python
from scipy import stats

# Find critical t-value
alpha = 0.05
df = 29  # n - 1
critical_t = stats.t.ppf(1 - alpha/2, df)  # Two-tailed
print(f"Critical t-value: ±{critical_t:.3f}")
# Output: ±2.045
```

**Decision Rules:**

**Method 1: P-value approach**
```
If p-value < α → Reject H₀
If p-value ≥ α → Fail to reject H₀
```

**Method 2: Critical value approach**
```
Two-tailed:
If |test statistic| > critical value → Reject H₀
If |test statistic| ≤ critical value → Fail to reject H₀

One-tailed (right):
If test statistic > critical value → Reject H₀

One-tailed (left):
If test statistic < critical value → Reject H₀
```

**Example:**
```
Coin flip test: z = 3.0
Critical value (α = 0.05, two-tailed): ±1.96

Decision:
|3.0| > 1.96 → Reject H₀

This matches our p-value decision (p = 0.0027 < 0.05)
```

### 📏 Test Statistic - "The Evidence Score"

The **test statistic** is a single number that summarizes your evidence:
- Could be a Z-score, t-score, or other value
- Tells you "how far" your sample is from what's claimed
- Bigger numbers (positive or negative) = more unusual evidence

**Formula Pattern:**
```
Test Statistic = (What you observed - What was claimed) / Standard Error
```

---

## 3. The 5-Step Process {#five-step-process}

Every hypothesis test follows these steps:

### **Step 1: State Your Hypotheses** 📝

Write down H₀ and H₁ clearly.

**Example:**
```
H₀: The coin is fair (p = 0.50)
H₁: The coin is NOT fair (p ≠ 0.50)
α = 0.05
```

### **Step 2: Collect Your Data** 📊

Gather your sample and calculate statistics.

**Example:**
```
Flipped coin 100 times
Got 65 heads
Sample proportion = 65/100 = 0.65
```

### **Step 3: Calculate the Test Statistic** 🧮

Use the appropriate formula for your test.

**Example:**
```
Z = (0.65 - 0.50) / √(0.50 × 0.50 / 100)
Z = 0.15 / 0.05
Z = 3.0
```

### **Step 4: Find the P-Value** 🔍

Look up or calculate the p-value.

**Example:**
```
For Z = 3.0 (two-tailed)
p-value ≈ 0.003
```

### **Step 5: Make Your Decision** ⚖️

Compare p-value to α and conclude.

**Example:**
```
p-value (0.003) < α (0.05)
→ REJECT H₀
→ The coin is NOT fair!
```

---

## 4. Types of Errors {#types-of-errors}

Even with good evidence, we can make mistakes!

### 🚨 Type I Error - "False Alarm"

**What it is:** Rejecting H₀ when it's actually TRUE
- Like convicting an innocent person
- Probability = α (significance level)

**Example:**
- H₀: "The coin is fair" (and it really IS fair)
- But you reject it anyway because you got unlucky with your sample
- You cry "BIASED!" when it's actually fair

### 🚨 Type II Error - "Missed Detection"

**What it is:** Failing to reject H₀ when it's actually FALSE
- Like letting a guilty person go free
- Probability = β (beta)

**Example:**
- H₀: "The coin is fair" (but it's actually BIASED)
- But you fail to reject it because your sample wasn't extreme enough
- You say "It's fair!" when it's actually biased

### The Trade-Off Table

| Reality → | H₀ is TRUE | H₀ is FALSE |
|-----------|------------|-------------|
| **You Reject H₀** | ❌ Type I Error (α) | ✅ Correct! |
| **You Don't Reject H₀** | ✅ Correct! | ❌ Type II Error (β) |

**Memory Trick:**
- **Type I**: "I thought I saw something, but I was wrong" (false positive)
- **Type II**: "I missed it!" (false negative)

---

## 5. One-Tailed vs Two-Tailed Tests {#tailed-tests}

### 🎯 Two-Tailed Test - "Is it Different?"

You care if the value is different in EITHER direction (higher OR lower).

**H₁ uses:** ≠ (not equal to)

**Example:**
```
H₀: Average height = 170 cm
H₁: Average height ≠ 170 cm
(Could be taller OR shorter)
```

**Visual:**
```
        Reject H₀     Don't Reject H₀     Reject H₀
        (2.5%)           (95%)              (2.5%)
    |---------|========================|---------|
   -∞      -1.96         0            1.96      +∞
```

### 🎯 One-Tailed Test (Right) - "Is it Greater?"

You only care if the value is HIGHER.

**H₁ uses:** > (greater than)

**Example:**
```
H₀: Average height = 170 cm
H₁: Average height > 170 cm
(Only care if TALLER)
```

**Visual:**
```
        Don't Reject H₀              Reject H₀
             (95%)                      (5%)
    |========================|---------|
   -∞                      1.645      +∞
```

### 🎯 One-Tailed Test (Left) - "Is it Less?"

You only care if the value is LOWER.

**H₁ uses:** < (less than)

**Example:**
```
H₀: Average height = 170 cm
H₁: Average height < 170 cm
(Only care if SHORTER)
```

**Visual:**
```
        Reject H₀         Don't Reject H₀
          (5%)                 (95%)
    |---------|========================|
   -∞      -1.645                     +∞
```

### When to Use Which?

**Use Two-Tailed when:**
- You care about differences in BOTH directions
- You're asking "Is it different?"
- Most common in practice

**Use One-Tailed when:**
- You only care about ONE direction
- You're asking "Is it greater?" or "Is it less?"
- You have a specific directional hypothesis

---

## 6. Complete Manual Calculation Walkthrough {#manual-calculation}

Let's work through a complete example **by hand** to see exactly how everything is calculated!

### 📝 Problem Setup

**Scenario:** A coffee shop claims their average wait time is 5 minutes. You visit 36 times and record wait times. Your sample has:
- Sample mean (x̄) = 5.8 minutes
- Sample standard deviation (s) = 2.4 minutes
- Sample size (n) = 36

**Question:** Is the coffee shop's claim accurate? Use α = 0.05.

---

### **Step 1: State Hypotheses**

```
H₀: μ = 5 minutes (The claim is true)
H₁: μ ≠ 5 minutes (The claim is false)
α = 0.05
Test type: Two-tailed (we care if it's different in either direction)
```

---

### **Step 2: Choose the Test**

**Decision:** Use one-sample t-test because:
- ✅ We're comparing sample mean to a claimed value
- ✅ Population standard deviation (σ) is unknown
- ✅ We only have sample standard deviation (s)

---

### **Step 3: Calculate Test Statistic**

**Formula:**
```
t = (x̄ - μ₀) / (s / √n)
```

**Calculation:**

```
Step 3a: Calculate standard error (SE)
SE = s / √n
SE = 2.4 / √36
SE = 2.4 / 6
SE = 0.4 minutes

Step 3b: Calculate t-statistic
t = (x̄ - μ₀) / SE
t = (5.8 - 5.0) / 0.4
t = 0.8 / 0.4
t = 2.0
```

**Interpretation:** Our sample mean is 2.0 standard errors above the claimed mean.

---

### **Step 4: Find Degrees of Freedom**

```
df = n - 1
df = 36 - 1
df = 35
```

---

### **Step 5: Find P-Value**

**Method A: Using T-Table**

1. Look up t = 2.0 with df = 35 in t-table
2. Find the area in one tail
3. For t = 2.0, df = 35: one-tail area ≈ 0.027
4. Two-tailed p-value = 2 × 0.027 = 0.054

**Method B: Using Python (more accurate)**

```python
from scipy import stats
t_stat = 2.0
df = 35
p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
print(f"p-value = {p_value:.4f}")
# Output: p-value = 0.0530
```

---

### **Step 6: Find Critical Value (Alternative Method)**

Instead of p-value, we can use critical values:

```
For α = 0.05, two-tailed, df = 35:
Critical t-value = ±2.030 (from t-table)

Decision rule:
If |t| > 2.030 → Reject H₀
If |t| ≤ 2.030 → Fail to reject H₀

Our test statistic: |2.0| = 2.0
Comparison: 2.0 < 2.030
Decision: Fail to reject H₀
```

---

### **Step 7: Make Decision**

**Using p-value approach:**
```
p-value = 0.0530
α = 0.05

Since 0.0530 > 0.05:
→ Fail to reject H₀
```

**Using critical value approach:**
```
|t| = 2.0
Critical value = 2.030

Since 2.0 < 2.030:
→ Fail to reject H₀
```

**Both methods agree!**

---

### **Step 8: State Conclusion**

**Statistical conclusion:**
"At the 0.05 significance level, we do not have sufficient evidence to reject the claim that the average wait time is 5 minutes."

**Practical conclusion:**
"While our sample average (5.8 minutes) is higher than the claimed 5 minutes, this difference could reasonably occur by chance. The coffee shop's claim cannot be rejected based on this data."

**Note:** The p-value (0.053) is very close to α (0.05)! This is a borderline case. With a slightly larger sample or slightly higher sample mean, we might reject H₀.

---

### 📊 Visual Summary of Calculations

```
Given Data:
├─ x̄ = 5.8 minutes
├─ μ₀ = 5.0 minutes
├─ s = 2.4 minutes
├─ n = 36
└─ α = 0.05

Calculations:
├─ SE = s/√n = 2.4/6 = 0.4
├─ t = (x̄-μ₀)/SE = 0.8/0.4 = 2.0
├─ df = n-1 = 35
├─ p-value = 0.053
└─ Critical value = ±2.030

Decision:
├─ p-value (0.053) > α (0.05) ✓
├─ |t| (2.0) < critical (2.030) ✓
└─ Conclusion: Fail to reject H₀
```

---

## 7. Complete Python Example {#python-example}

Let's put it all together with a real example!

### Example: Testing a Coin for Fairness

**The Story:**
You suspect a coin might be biased. You flip it 100 times and get 65 heads. Is the coin fair?

```python
# Step 0: Import tools
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

print("🪙 COIN FAIRNESS TEST - COMPLETE WALKTHROUGH")
print("="*70)

# ============================================================
# STEP 1: STATE THE HYPOTHESES
# ============================================================
print("\n📝 STEP 1: STATE THE HYPOTHESES")
print("-"*70)
print("H₀ (Null): The coin is fair (p = 0.50)")
print("H₁ (Alternative): The coin is NOT fair (p ≠ 0.50)")
print("Significance level: α = 0.05")
print("Test type: Two-tailed (we care if it's biased in either direction)")

# ============================================================
# STEP 2: COLLECT THE DATA
# ============================================================
print("\n📊 STEP 2: COLLECT THE DATA")
print("-"*70)

n = 100                    # Number of flips
heads = 65                 # Number of heads observed
p_observed = heads / n     # Sample proportion
p_claimed = 0.50           # Claimed proportion (fair coin)

print(f"Number of flips: {n}")
print(f"Heads observed: {heads}")
print(f"Sample proportion: {p_observed:.2f} ({p_observed*100:.0f}%)")
print(f"Claimed proportion: {p_claimed:.2f} ({p_claimed*100:.0f}%)")
print(f"Difference: {(p_observed - p_claimed)*100:.0f} percentage points")

# ============================================================
# STEP 3: CALCULATE THE TEST STATISTIC
# ============================================================
print("\n🧮 STEP 3: CALCULATE THE TEST STATISTIC")
print("-"*70)

# Standard error for proportion
se = np.sqrt(p_claimed * (1 - p_claimed) / n)
print(f"Standard Error: {se:.4f}")

# Z-statistic
z_stat = (p_observed - p_claimed) / se
print(f"Z-statistic: {z_stat:.4f}")

print("\n💡 What does this mean?")
print(f"   Our sample proportion is {z_stat:.2f} standard errors")
print(f"   away from the claimed proportion.")
print(f"   That's {'pretty far' if abs(z_stat) > 2 else 'not too far'}!")

# ============================================================
# STEP 4: FIND THE P-VALUE
# ============================================================
print("\n🔍 STEP 4: FIND THE P-VALUE")
print("-"*70)

# Two-tailed p-value
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
print(f"P-value: {p_value:.4f}")

print("\n💡 What does this mean?")
print(f"   If the coin were really fair, there's only a")
print(f"   {p_value*100:.2f}% chance of getting results this extreme")
print(f"   or more extreme just by random luck.")

# ============================================================
# STEP 5: MAKE YOUR DECISION
# ============================================================
print("\n⚖️  STEP 5: MAKE YOUR DECISION")
print("-"*70)

alpha = 0.05
print(f"Significance level (α): {alpha}")
print(f"P-value: {p_value:.4f}")
print(f"Comparison: p-value {'<' if p_value < alpha else '>'} α")

print("\n" + "="*70)
print("🎯 FINAL DECISION:")
print("="*70)

if p_value < alpha:
    print("✅ REJECT H₀")
    print("\n📊 Conclusion:")
    print("   There IS sufficient evidence to conclude that the coin is biased.")
    print(f"   The probability of getting {heads} or more heads (or {100-heads} or fewer)")
    print(f"   in {n} flips of a fair coin is only {p_value*100:.2f}%.")
    print("   This is too unlikely to be just random chance!")
else:
    print("❌ FAIL TO REJECT H₀")
    print("\n📊 Conclusion:")
    print("   There is NOT sufficient evidence to conclude that the coin is biased.")
    print(f"   Getting {heads} heads in {n} flips could reasonably happen")
    print("   with a fair coin just by random chance.")

print("="*70)

# ============================================================
# BONUS: VISUALIZE THE RESULTS
# ============================================================
print("\n📈 Creating visualizations...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Plot 1: Pie chart of results
axes[0].pie([heads, n-heads], labels=['Heads', 'Tails'], 
            autopct='%1.0f%%', colors=['gold', 'silver'], startangle=90)
axes[0].set_title(f'Coin Flip Results\n({n} flips)', fontweight='bold')

# Plot 2: Comparison to expected
categories = ['Expected\n(Fair Coin)', 'Observed']
proportions = [p_claimed, p_observed]
colors = ['blue', 'red' if p_value < alpha else 'orange']

bars = axes[1].bar(categories, proportions, color=colors, alpha=0.7, edgecolor='black')
axes[1].axhline(p_claimed, color='blue', linestyle='--', linewidth=2, label='Fair coin (50%)')
axes[1].set_ylabel('Proportion of Heads')
axes[1].set_title('Expected vs Observed', fontweight='bold')
axes[1].set_ylim(0, 1)
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

# Add percentage labels on bars
for bar, prop in zip(bars, proportions):
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{prop*100:.0f}%', ha='center', va='bottom', fontweight='bold')

# Plot 3: Z-distribution with test statistic
x = np.linspace(-4, 4, 1000)
y = stats.norm.pdf(x)

axes[2].plot(x, y, 'b-', linewidth=2, label='Standard Normal Distribution')
axes[2].axvline(z_stat, color='red', linestyle='--', linewidth=2, 
                label=f'Our Z-score = {z_stat:.2f}')

# Critical values for two-tailed test
z_critical = stats.norm.ppf(1 - alpha/2)
axes[2].axvline(z_critical, color='green', linestyle='--', linewidth=1.5, 
                label=f'Critical values = ±{z_critical:.2f}')
axes[2].axvline(-z_critical, color='green', linestyle='--', linewidth=1.5)

# Shade rejection regions
x_left = np.linspace(-4, -z_critical, 100)
x_right = np.linspace(z_critical, 4, 100)
axes[2].fill_between(x_left, stats.norm.pdf(x_left), alpha=0.3, color='red', 
                     label='Rejection Regions')
axes[2].fill_between(x_right, stats.norm.pdf(x_right), alpha=0.3, color='red')

axes[2].set_xlabel('Z-score')
axes[2].set_ylabel('Probability Density')
axes[2].set_title('Hypothesis Test Visualization', fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n✅ Analysis complete!")
```

**Expected Output:**
```
🪙 COIN FAIRNESS TEST - COMPLETE WALKTHROUGH
======================================================================

📝 STEP 1: STATE THE HYPOTHESES
----------------------------------------------------------------------
H₀ (Null): The coin is fair (p = 0.50)
H₁ (Alternative): The coin is NOT fair (p ≠ 0.50)
Significance level: α = 0.05
Test type: Two-tailed (we care if it's biased in either direction)

📊 STEP 2: COLLECT THE DATA
----------------------------------------------------------------------
Number of flips: 100
Heads observed: 65
Sample proportion: 0.65 (65%)
Claimed proportion: 0.50 (50%)
Difference: 15 percentage points

🧮 STEP 3: CALCULATE THE TEST STATISTIC
----------------------------------------------------------------------
Standard Error: 0.0500
Z-statistic: 3.0000

💡 What does this mean?
   Our sample proportion is 3.00 standard errors
   away from the claimed proportion.
   That's pretty far!

🔍 STEP 4: FIND THE P-VALUE
----------------------------------------------------------------------
P-value: 0.0027

💡 What does this mean?
   If the coin were really fair, there's only a
   0.27% chance of getting results this extreme
   or more extreme just by random luck.

⚖️  STEP 5: MAKE YOUR DECISION
----------------------------------------------------------------------
Significance level (α): 0.05
P-value: 0.0027
Comparison: p-value < α

======================================================================
🎯 FINAL DECISION:
======================================================================
✅ REJECT H₀

📊 Conclusion:
   There IS sufficient evidence to conclude that the coin is biased.
   The probability of getting 65 or more heads (or 35 or fewer)
   in 100 flips of a fair coin is only 0.27%.
   This is too unlikely to be just random chance!
======================================================================
```

---

## 🎓 Summary - What You Learned

### **Key Concepts**

1. **Hypothesis Testing** = Making decisions about populations using sample data
2. **H₀ (Null)** = The boring claim we try to disprove
3. **H₁ (Alternative)** = The interesting claim we try to prove
4. **P-value** = "How weird is our evidence?" (< 0.05 = very weird!)
5. **α (Alpha)** = Our threshold for "weird enough" (usually 0.05)
6. **Test Statistic** = A score measuring how far our sample is from the claim

### **The 5-Step Process**

```
1. State hypotheses (H₀ and H₁)
2. Collect data
3. Calculate test statistic
4. Find p-value
5. Make decision (reject or don't reject H₀)
```

### **Decision Rule**

```
If p-value < α:  REJECT H₀ (found something interesting!)
If p-value ≥ α:  DON'T REJECT H₀ (not enough evidence)
```

### **Types of Errors**

- **Type I Error**: False alarm (reject H₀ when it's true)
- **Type II Error**: Missed detection (don't reject H₀ when it's false)

### **Test Types**

- **Two-tailed**: H₁ uses ≠ (different in either direction)
- **One-tailed (right)**: H₁ uses > (greater than)
- **One-tailed (left)**: H₁ uses < (less than)

---

## 🎯 What's Next?

Now that you understand the basics of hypothesis testing, you're ready to learn about specific tests!

**Continue to:**
- **Chapter 4.1**: Single Sample Tests (Z-test, T-test)
- **Chapter 4.2**: Two Sample Tests (Independent, Paired)
- **Chapter 4.3**: Proportion Tests

Each chapter will teach you WHEN to use each test and HOW to do it in Python!

---

## 💡 Practice Problems

### Problem 1: Quick Decision Practice

For each scenario, decide: Reject H₀ or Don't Reject H₀?

**a)** p-value = 0.03, α = 0.05
**b)** p-value = 0.08, α = 0.05
**c)** p-value = 0.001, α = 0.01
**d)** p-value = 0.06, α = 0.10

<details>
<summary>Click for answers</summary>

**a)** REJECT H₀ (0.03 < 0.05)
**b)** DON'T REJECT H₀ (0.08 > 0.05)
**c)** REJECT H₀ (0.001 < 0.01)
**d)** REJECT H₀ (0.06 < 0.10)
</details>

### Problem 2: Identify the Hypotheses

A company claims their light bulbs last 1000 hours on average. You think they last less. Write H₀ and H₁.

<details>
<summary>Click for answer</summary>

H₀: μ = 1000 hours (company's claim is true)
H₁: μ < 1000 hours (bulbs last less than claimed)
This is a **one-tailed (left)** test.
</details>

### Problem 3: Error Types

You test a new drug. The drug actually works (H₀ is false), but your test fails to reject H₀. What type of error is this?

<details>
<summary>Click for answer</summary>

**Type II Error** - You failed to detect something that was really there (missed detection).
</details>

---

**Remember:** Hypothesis testing is about making informed decisions with data. You're not looking for absolute proof - you're weighing evidence and making the best decision you can with the information available! 🎯

---

## 💻 Hands-On Practice

**Ready to practice hypothesis testing with real data?**

Check out the **[Jupyter Notebook with Hypothesis Testing Examples]({{ site.baseurl }}/notebooks/statistics/chapter3_hypothesis_testing_examples.ipynb)** using the Tips dataset!

**What's included:**
- ✅ Complete 5-step process examples
- ✅ Real dataset (restaurant tips)
- ✅ One-sample t-test (Is average tip $3.00?)
- ✅ Two-sample t-test (Do smokers tip differently?)
- ✅ Proportion test (Weekend vs weekday dining)
- ✅ p-value visualizations
- ✅ Decision-making examples

**To run the notebook:**
1. Install: `pip install pandas numpy matplotlib seaborn scipy statsmodels jupyter`
2. Download the notebook from the repository
3. Run: `jupyter notebook chapter3_hypothesis_testing_examples.ipynb`

📖 See the [notebooks README]({{ site.baseurl }}/notebooks/statistics/README.md) for full instructions!

**Ready to learn specific tests?** Head to Chapter 4! 🚀
