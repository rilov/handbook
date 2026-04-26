---
title: "Chapter 4.3: Proportion Tests"
category: Data Science
order: 7
tags:
  - statistics
  - hypothesis-testing
  - proportion-test
  - z-test
  - percentages
summary: "Learn proportion tests for testing percentages and proportions - one-sample and two-sample proportion tests with practical examples and Python code."
---

# Chapter 4.3: Proportion Tests

## Overview

**Proportion tests** are used when your data consists of categories or yes/no outcomes, and you want to test claims about percentages or success rates. Unlike t-tests which compare means, proportion tests compare percentages.

**The Core Question:**

"Is this percentage/success rate significantly different from what we expected or from another group?"

**Real-World Applications:**

- **Marketing & A/B Testing:** Did the new ad campaign increase conversion rates?
- **Quality Control:** Is the defect rate below 5%?
- **Medical Research:** Is the cure rate for Treatment A higher than Treatment B?
- **Politics:** Do different demographics support a candidate at different rates?
- **Product Testing:** Do users prefer Feature A over Feature B?

**When to Use Proportion Tests:**

Use proportion tests when your data is:
- **Binary/Categorical:** Yes/No, Success/Failure, Click/No Click, Pass/Fail
- **Count-based:** Number of successes out of total trials
- **Percentage-based:** Conversion rates, success rates, approval ratings

**Examples:**
- ✅ "60 out of 100 customers were satisfied" → Proportion = 0.60
- ✅ "15% of products were defective" → Proportion = 0.15
- ✅ "450 out of 1000 clicked the ad" → Proportion = 0.45

**NOT for proportion tests:**
- ❌ Average customer spending ($45.50) → Use t-test
- ❌ Mean test score (78.5) → Use t-test
- ❌ Average delivery time (23.4 minutes) → Use t-test

**Two Types of Proportion Tests:**

### **1. One-Sample Proportion Test**
Compare your sample proportion to a claimed or expected value.

**Example:** "A company claims 90% customer satisfaction. You survey 200 customers and find 85% are satisfied. Is the company's claim accurate?"

### **2. Two-Sample Proportion Test**
Compare proportions between two independent groups.

**Example:** "Do men (20% click rate) and women (30% click rate) click on ads at different rates?"

**Key Differences from T-Tests:**

| Aspect | T-Test | Proportion Test |
|--------|--------|-----------------|
| **Data Type** | Continuous (means) | Categorical (percentages) |
| **Example** | Average height: 170 cm | 60% are tall |
| **Test Statistic** | t-statistic | z-statistic |
| **Distribution** | t-distribution | Normal distribution |
| **Sample Size** | Works with small samples | Needs larger samples (np ≥ 10) |

**What You'll Learn:**

1. **One-sample proportion test:** Test if a percentage matches a claimed value
2. **Two-sample proportion test:** Compare percentages between two groups
3. **Sample size requirements:** When proportion tests are valid
4. **Practical interpretation:** What the results mean for decision-making

## Table of Contents
1. [Introduction - Testing Percentages](#introduction)
2. [One-Sample Proportion Test](#one-sample)
3. [Two-Sample Proportion Test](#two-sample)
4. [Python Implementation - Let's Code It!](#python-implementation)
5. [Practice Exercises - Your Turn!](#practice-exercises)

---

## 1. Introduction - Testing Percentages {#introduction}

### The Big Picture (Explained Simply)

So far, we've been testing **averages** (means):
- Chapter 4.1: Is the average chocolate bar weight 100g?
- Chapter 4.2: Do men and women have different average salaries?

Now we're going to test **percentages** (proportions):
- Is the success rate really 50%?
- Do more women than men prefer product A?
- Has customer satisfaction improved from 60% to 75%?

### What's a Proportion?

A **proportion** is just a fancy word for a percentage expressed as a decimal:
- 50% = 0.50
- 75% = 0.75
- 23% = 0.23

**Examples of proportions:**
- 🎯 60% of customers are satisfied (proportion = 0.60)
- 🗳️ 45% of voters support Candidate A (proportion = 0.45)
- 🎓 80% of students passed the exam (proportion = 0.80)
- 🏥 15% of patients experienced side effects (proportion = 0.15)

### Two Types of Proportion Tests

#### **Type 1: One-Sample Proportion Test**
Compare ONE sample proportion to a claimed value.

**Example:** A coin should land on heads 50% of the time. You flip it 100 times and get 60 heads. Is the coin fair?
- Claimed proportion: 50% (0.50)
- Your sample: 60% (0.60)
- Question: Is this difference just random luck, or is the coin biased?

#### **Type 2: Two-Sample Proportion Test**
Compare TWO sample proportions to each other.

**Example:** Do men and women click on ads at different rates?
- Men: 100 out of 500 clicked (20%)
- Women: 150 out of 500 clicked (30%)
- Question: Is this difference real, or just random variation?

### Real-Life Examples

**One-Sample:**
- 🎲 Is this die fair? (Should be 1/6 = 16.67% for each number)
- 📊 Is our conversion rate really 10%?
- 🏥 Is the cure rate at least 80%?

**Two-Sample:**
- 👨👩 Do men and women have different click-through rates?
- 💊 Is Drug A more effective than Drug B?
- 🎯 Did our marketing campaign improve conversion rates?

---

## 2. One-Sample Proportion Test {#one-sample}

### What is a One-Sample Proportion Test? (Simple Explanation)

Imagine you're a quality control manager at a factory. The company claims that only 5% of products are defective. You inspect 200 random products and find 15 defective ones (7.5%). 

**The Question:** Is the defect rate really 5%, or is it higher?

This is a **one-sample proportion test** because you're comparing your sample proportion (7.5%) to a claimed proportion (5%).

### When to Use One-Sample Proportion Test

**Use it when:**
- ✅ You have ONE sample
- ✅ You're counting successes/failures (yes/no, pass/fail, click/no-click)
- ✅ You want to compare your sample proportion to a claimed value
- ✅ Sample size is large enough (np ≥ 10 and n(1-p) ≥ 10)

**Examples:**
- 🎯 Testing if a coin is fair (claimed: 50% heads)
- 📊 Testing if conversion rate meets target (claimed: 10%)
- 🗳️ Testing if candidate has majority support (claimed: 50%)
- 🏥 Testing if cure rate meets standard (claimed: 80%)

### The Formula (Don't Panic!)

The test statistic for proportions is called a **Z-score**:

$$Z = \frac{\hat{p} - p_0}{\sqrt{\frac{p_0(1-p_0)}{n}}}$$

**What each symbol means:**
- $\hat{p}$ (p-hat) = Your sample proportion (like 0.075 or 7.5%)
- $p_0$ (p-zero) = The claimed proportion (like 0.05 or 5%)
- $n$ = Sample size (like 200 products)

**In plain English:** "How far is my sample proportion from the claimed proportion, considering sample size?"

### Example: Defective Products

**The Story:**
A factory claims only 5% of products are defective. You inspect 200 products and find 15 defective.

**The Data:**
- Sample size: n = 200
- Defective found: 15
- Sample proportion: $\hat{p}$ = 15/200 = 0.075 (7.5%)
- Claimed proportion: $p_0$ = 0.05 (5%)

**The Question:** Is the defect rate higher than claimed?

---

**Step 1: Set Up Your Claims**

🔵 **Boring Claim (H₀)**: "The defect rate is 5%"
- In math: p = 0.05

🔴 **Interesting Claim (H₁)**: "The defect rate is HIGHER than 5%"
- In math: p > 0.05
- Note: One-tailed test (we only care if it's higher)

🎯 **How sure do we need to be?** α = 0.05 (95% confidence)

---

**Step 2: Check if We Can Use This Test**

We need to check if our sample is large enough:
- np₀ = 200 × 0.05 = 10 ✅ (≥ 10)
- n(1-p₀) = 200 × 0.95 = 190 ✅ (≥ 10)

Both conditions met! We can proceed.

---

**Step 3: Calculate the Z-Score**

$$Z = \frac{0.075 - 0.05}{\sqrt{\frac{0.05 \times 0.95}{200}}} = \frac{0.025}{\sqrt{0.0002375}} = \frac{0.025}{0.0154} = 1.62$$

**Breaking it down:**
- Top part: 0.075 - 0.05 = 0.025 (2.5% higher than claimed)
- Bottom part: √(0.05 × 0.95 / 200) = 0.0154 (standard error)
- Final Z-score: 0.025 / 0.0154 = **1.62**

---

**Step 4: Find the P-Value**

For Z = 1.62 (one-tailed, right side):
- P-value ≈ 0.053

---

**Step 5: Make Your Decision**

- P-value = 0.053
- Alpha = 0.05
- Since 0.053 > 0.05, we're just barely outside the "weird zone"

**Conclusion (in plain English):**
"We found 7.5% defective products instead of the claimed 5%. This is higher, but not quite high enough to be statistically significant at the 95% confidence level. It's borderline - we might want to keep monitoring!"

**Technical way to say it:**
"We fail to reject H₀. There is insufficient evidence at α = 0.05 that the defect rate exceeds 5% (p = 0.053)."

---

### Python Implementation - One-Sample Proportion Test

Let's code this step by step!

```python
# Step 1: Import the tools we need
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Step 2: Enter your data
n = 200                    # Sample size (products inspected)
x = 15                     # Number of successes (defective products)
p_hat = x / n              # Sample proportion
p_0 = 0.05                 # Claimed proportion
alpha = 0.05               # Significance level

print("🏭 DEFECTIVE PRODUCTS TEST")
print("="*60)
print(f"Sample size: {n} products")
print(f"Defective found: {x} products")
print(f"Sample proportion: {p_hat:.4f} ({p_hat*100:.2f}%)")
print(f"Claimed proportion: {p_0:.4f} ({p_0*100:.2f}%)")
print("="*60)

# Step 3: Check assumptions
np_0 = n * p_0
n_1_p_0 = n * (1 - p_0)

print(f"\n🔍 CHECKING ASSUMPTIONS:")
print(f"np₀ = {np_0:.1f} (need ≥ 10) {'✅' if np_0 >= 10 else '❌'}")
print(f"n(1-p₀) = {n_1_p_0:.1f} (need ≥ 10) {'✅' if n_1_p_0 >= 10 else '❌'}")

if np_0 >= 10 and n_1_p_0 >= 10:
    print("✅ Sample size is large enough! We can proceed.")
else:
    print("❌ Sample size too small! Results may not be reliable.")

# Step 4: Calculate Z-score
se = np.sqrt(p_0 * (1 - p_0) / n)  # Standard error
z_score = (p_hat - p_0) / se

print(f"\n📊 TEST RESULTS:")
print(f"Standard error: {se:.4f}")
print(f"Z-score: {z_score:.4f}")

# Step 5: Calculate p-value (one-tailed, right side)
p_value = 1 - stats.norm.cdf(z_score)
print(f"P-value (one-tailed): {p_value:.4f}")

# Step 6: Find critical value
z_critical = stats.norm.ppf(1 - alpha)
print(f"Critical value: {z_critical:.4f}")

# Step 7: Make a decision
print("\n🎯 DECISION:")
if p_value < alpha:
    print(f"✅ REJECT H₀: Defect rate IS higher than {p_0*100:.0f}%!")
    print(f"   (p-value {p_value:.4f} < {alpha})")
    print(f"   We found {p_hat*100:.1f}% defective, significantly higher than claimed")
else:
    print(f"❌ FAIL TO REJECT H₀: Not enough evidence")
    print(f"   (p-value {p_value:.4f} > {alpha})")
    print(f"   The {p_hat*100:.1f}% defect rate could be due to random variation")

# Step 8: Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Bar chart comparing proportions
axes[0].bar(['Claimed', 'Observed'], [p_0, p_hat], color=['blue', 'red'], alpha=0.7)
axes[0].axhline(p_0, color='blue', linestyle='--', linewidth=2, label='Claimed rate')
axes[0].set_ylabel('Proportion Defective')
axes[0].set_title('Defect Rate Comparison')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

# Add percentage labels on bars
for i, (label, value) in enumerate([('Claimed', p_0), ('Observed', p_hat)]):
    axes[0].text(i, value + 0.005, f'{value*100:.1f}%', ha='center', fontweight='bold')

# Plot 2: Z-score distribution
x = np.linspace(-4, 4, 1000)
y = stats.norm.pdf(x)

axes[1].plot(x, y, 'b-', linewidth=2, label='Standard Normal')
axes[1].axvline(z_score, color='r', linestyle='--', linewidth=2, 
                label=f'Our Z-score = {z_score:.2f}')
axes[1].axvline(z_critical, color='g', linestyle='--', linewidth=1.5, 
                label=f'Critical value = {z_critical:.2f}')

# Shade rejection region
x_reject = np.linspace(z_critical, 4, 100)
axes[1].fill_between(x_reject, stats.norm.pdf(x_reject), alpha=0.3, color='red',
                     label='Rejection Region')

axes[1].set_xlabel('Z-score')
axes[1].set_ylabel('Probability Density')
axes[1].set_title('One-Sample Proportion Test (One-Tailed)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n📊 The graph shows our Z-score is just below the critical value!")
```

---

### Using statsmodels for Proportion Test

Python has a built-in function that makes this even easier!

```python
from statsmodels.stats.proportion import proportions_ztest

# Your data
count = 15        # Number of defective products
nobs = 200        # Total products inspected
value = 0.05      # Claimed proportion

# Perform one-sample proportion test
z_stat, p_value = proportions_ztest(count, nobs, value, alternative='larger')

print("🏭 QUICK PROPORTION TEST")
print("="*60)
print(f"Defective: {count} out of {nobs} ({count/nobs*100:.1f}%)")
print(f"Claimed: {value*100:.0f}%")
print(f"\nZ-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("\n✅ Significant! Defect rate is higher than claimed.")
else:
    print("\n❌ Not significant. Could be random variation.")
print("="*60)
```

---

## 3. Two-Sample Proportion Test {#two-sample}

### What is a Two-Sample Proportion Test? (Simple Explanation)

Imagine you're running an A/B test for a website:
- **Version A (Control):** 50 out of 500 visitors clicked the button (10%)
- **Version B (New design):** 80 out of 500 visitors clicked the button (16%)

**The Question:** Is Version B really better, or could this difference be just random luck?

This is a **two-sample proportion test** because you're comparing two proportions to each other.

### When to Use Two-Sample Proportion Test

**Use it when:**
- ✅ You have TWO independent groups
- ✅ Each group has successes/failures (yes/no, click/no-click)
- ✅ You want to compare the two proportions
- ✅ Sample sizes are large enough

**Examples:**
- 🎯 A/B testing: Version A vs Version B click rates
- 👨👩 Gender differences: Male vs Female success rates
- 💊 Drug comparison: Drug A vs Drug B cure rates
- 🗳️ Political polls: Support for Candidate A in State 1 vs State 2

### The Formula (Don't Panic!)

$$Z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}(1-\hat{p})(\frac{1}{n_1} + \frac{1}{n_2})}}$$

Where $\hat{p}$ is the **pooled proportion**:

$$\hat{p} = \frac{x_1 + x_2}{n_1 + n_2}$$

**What each symbol means:**
- $\hat{p}_1$ = Proportion in Group 1 (like 10% click rate)
- $\hat{p}_2$ = Proportion in Group 2 (like 16% click rate)
- $\hat{p}$ = Combined proportion from both groups
- $n_1$, $n_2$ = Sample sizes of each group

**In plain English:** "How different are the two proportions, considering both sample sizes?"

### Example: A/B Testing Website Design

**The Story:**
You're testing two website designs to see which gets more clicks:
- **Version A:** 50 clicks out of 500 visitors (10%)
- **Version B:** 80 clicks out of 500 visitors (16%)

**The Question:** Is Version B significantly better?

---

**Step 1: Set Up Your Claims**

🔵 **Boring Claim (H₀)**: "Both versions have the same click rate"
- In math: p₁ = p₂ (or p₁ - p₂ = 0)

🔴 **Interesting Claim (H₁)**: "The versions have different click rates"
- In math: p₁ ≠ p₂
- Note: Two-tailed test (we're open to either being better)

🎯 **How sure do we need to be?** α = 0.05 (95% confidence)

---

**Step 2: Calculate the Proportions**

- Version A: $\hat{p}_1$ = 50/500 = 0.10 (10%)
- Version B: $\hat{p}_2$ = 80/500 = 0.16 (16%)
- Pooled: $\hat{p}$ = (50+80)/(500+500) = 130/1000 = 0.13 (13%)

---

**Step 3: Calculate the Z-Score**

$$Z = \frac{0.10 - 0.16}{\sqrt{0.13 \times 0.87 \times (\frac{1}{500} + \frac{1}{500})}} = \frac{-0.06}{\sqrt{0.1131 \times 0.004}} = \frac{-0.06}{0.0213} = -2.82$$

---

**Step 4: Find the P-Value**

For Z = -2.82 (two-tailed):
- P-value ≈ 0.005

---

**Step 5: Make Your Decision**

- P-value = 0.005
- Alpha = 0.05
- Since 0.005 < 0.05, we're in the "weird zone"!

**Conclusion (in plain English):**
"Version B got 16% clicks compared to Version A's 10%. That's a 6 percentage point difference, and it's too big to be just random luck. Version B is genuinely better!"

**Technical way to say it:**
"We reject H₀. There is significant evidence that the two versions have different click rates (p = 0.005)."

---

### Python Implementation - Two-Sample Proportion Test

Let's code this!

```python
# Step 1: Import tools
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Step 2: Enter your data
# Version A
n1 = 500          # Visitors to Version A
x1 = 50           # Clicks on Version A
p1_hat = x1 / n1  # Click rate for Version A

# Version B
n2 = 500          # Visitors to Version B
x2 = 80           # Clicks on Version B
p2_hat = x2 / n2  # Click rate for Version B

alpha = 0.05      # Significance level

print("🖱️ A/B TESTING: WEBSITE CLICK RATES")
print("="*60)
print(f"Version A:")
print(f"  Visitors: {n1}")
print(f"  Clicks: {x1}")
print(f"  Click rate: {p1_hat:.4f} ({p1_hat*100:.1f}%)")
print(f"\nVersion B:")
print(f"  Visitors: {n2}")
print(f"  Clicks: {x2}")
print(f"  Click rate: {p2_hat:.4f} ({p2_hat*100:.1f}%)")
print(f"\nDifference: {(p2_hat - p1_hat)*100:.1f} percentage points")
print("="*60)

# Step 3: Calculate pooled proportion
p_pooled = (x1 + x2) / (n1 + n2)
print(f"\n📊 Pooled proportion: {p_pooled:.4f} ({p_pooled*100:.1f}%)")

# Step 4: Calculate standard error
se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
print(f"Standard error: {se:.4f}")

# Step 5: Calculate Z-score
z_score = (p1_hat - p2_hat) / se
print(f"Z-score: {z_score:.4f}")

# Step 6: Calculate p-value (two-tailed)
p_value = 2 * stats.norm.cdf(z_score)  # Two-tailed (z_score is negative)
print(f"P-value (two-tailed): {p_value:.4f}")

# Step 7: Make a decision
print("\n🎯 DECISION:")
if p_value < alpha:
    print(f"✅ REJECT H₀: The versions ARE different!")
    print(f"   (p-value {p_value:.4f} < {alpha})")
    if p2_hat > p1_hat:
        print(f"   Version B is BETTER! ({p2_hat*100:.1f}% vs {p1_hat*100:.1f}%)")
        improvement = ((p2_hat - p1_hat) / p1_hat) * 100
        print(f"   That's a {improvement:.1f}% relative improvement!")
    else:
        print(f"   Version A is BETTER! ({p1_hat*100:.1f}% vs {p2_hat*100:.1f}%)")
else:
    print(f"❌ FAIL TO REJECT H₀: No significant difference")
    print(f"   (p-value {p_value:.4f} > {alpha})")
    print(f"   The difference could be random variation")

# Step 8: Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Bar chart comparing proportions
versions = ['Version A', 'Version B']
click_rates = [p1_hat, p2_hat]
colors = ['blue', 'green']

bars = axes[0].bar(versions, click_rates, color=colors, alpha=0.7, edgecolor='black')
axes[0].set_ylabel('Click Rate')
axes[0].set_title('Click Rate Comparison')
axes[0].grid(True, alpha=0.3, axis='y')

# Add percentage labels on bars
for bar, rate in zip(bars, click_rates):
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{rate*100:.1f}%', ha='center', va='bottom', fontweight='bold')

# Plot 2: Sample sizes and success rates
x_pos = np.arange(2)
successes = [x1, x2]
failures = [n1-x1, n2-x2]

axes[1].bar(x_pos, successes, label='Clicks', color='green', alpha=0.7)
axes[1].bar(x_pos, failures, bottom=successes, label='No Clicks', color='gray', alpha=0.7)
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(versions)
axes[1].set_ylabel('Number of Visitors')
axes[1].set_title('Clicks vs No Clicks')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n📊 The graphs show Version B has a higher click rate!")
```

---

### Using statsmodels for Two-Sample Proportion Test

The easy way:

```python
from statsmodels.stats.proportion import proportions_ztest

# Your data
count = np.array([50, 80])      # Clicks for each version
nobs = np.array([500, 500])     # Visitors for each version

# Perform two-sample proportion test
z_stat, p_value = proportions_ztest(count, nobs)

print("🖱️ QUICK A/B TEST")
print("="*60)
print(f"Version A: {count[0]} clicks out of {nobs[0]} ({count[0]/nobs[0]*100:.1f}%)")
print(f"Version B: {count[1]} clicks out of {nobs[1]} ({count[1]/nobs[1]*100:.1f}%)")
print(f"\nZ-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("\n✅ Significant difference! The versions perform differently.")
    if count[1]/nobs[1] > count[0]/nobs[0]:
        print("   Version B is the winner! 🎉")
    else:
        print("   Version A is the winner! 🎉")
else:
    print("\n❌ No significant difference. Keep testing or stick with current version.")
print("="*60)
```

---

## 4. Putting It All Together - Real Examples! {#python-implementation}

### Example 1: Coin Fairness Test (One-Sample)

**The Situation:**
You suspect a coin might be biased. You flip it 100 times and get 60 heads.

```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

# Data
n = 100           # Number of flips
heads = 60        # Number of heads
p_hat = heads / n # Sample proportion
p_0 = 0.5         # Fair coin proportion

print("🪙 COIN FAIRNESS TEST")
print("="*60)
print(f"Flips: {n}")
print(f"Heads: {heads} ({p_hat*100:.0f}%)")
print(f"Expected (fair coin): {p_0*100:.0f}%")
print("="*60)

# Perform test
z_stat, p_value = proportions_ztest(heads, n, p_0)

print(f"\n📊 TEST RESULTS:")
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value (two-tailed): {p_value:.4f}")

print("\n🎯 DECISION:")
if p_value < 0.05:
    print(f"✅ REJECT H₀: The coin IS biased!")
    print(f"   (p-value {p_value:.4f} < 0.05)")
    if p_hat > 0.5:
        print(f"   It favors HEADS ({p_hat*100:.0f}%)")
    else:
        print(f"   It favors TAILS ({(1-p_hat)*100:.0f}%)")
else:
    print(f"❌ FAIL TO REJECT H₀: The coin appears fair")
    print(f"   (p-value {p_value:.4f} > 0.05)")
    print(f"   The {p_hat*100:.0f}% heads could be random variation")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Pie chart of results
axes[0].pie([heads, n-heads], labels=['Heads', 'Tails'], autopct='%1.0f%%',
            colors=['gold', 'silver'], startangle=90)
axes[0].set_title(f'Coin Flip Results (n={n})')

# Plot 2: Bar chart comparing to fair coin
axes[1].bar(['Expected\n(Fair Coin)', 'Observed'], [0.5, p_hat], 
            color=['blue', 'red'], alpha=0.7, edgecolor='black')
axes[1].axhline(0.5, color='blue', linestyle='--', linewidth=2, label='Fair coin (50%)')
axes[1].set_ylabel('Proportion of Heads')
axes[1].set_title('Expected vs Observed')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

---

### Example 2: Gender Differences in Product Preference (Two-Sample)

**The Situation:**
A company wants to know if men and women prefer their product at different rates.
- Men: 120 out of 400 prefer it (30%)
- Women: 160 out of 400 prefer it (40%)

```python
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

# Data
n_men = 400
prefer_men = 120
p_men = prefer_men / n_men

n_women = 400
prefer_women = 160
p_women = prefer_women / n_women

print("👨👩 GENDER PREFERENCE ANALYSIS")
print("="*60)
print(f"Men:")
print(f"  Sample size: {n_men}")
print(f"  Prefer product: {prefer_men} ({p_men*100:.1f}%)")
print(f"\nWomen:")
print(f"  Sample size: {n_women}")
print(f"  Prefer product: {prefer_women} ({p_women*100:.1f}%)")
print(f"\nDifference: {(p_women - p_men)*100:.1f} percentage points")
print("="*60)

# Perform test
count = np.array([prefer_men, prefer_women])
nobs = np.array([n_men, n_women])
z_stat, p_value = proportions_ztest(count, nobs)

print(f"\n📊 TEST RESULTS:")
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value (two-tailed): {p_value:.4f}")

print("\n🎯 DECISION:")
if p_value < 0.05:
    print(f"✅ REJECT H₀: There IS a gender difference!")
    print(f"   (p-value {p_value:.4f} < 0.05)")
    if p_women > p_men:
        print(f"   Women prefer it MORE ({p_women*100:.1f}% vs {p_men*100:.1f}%)")
    else:
        print(f"   Men prefer it MORE ({p_men*100:.1f}% vs {p_women*100:.1f}%)")
else:
    print(f"❌ FAIL TO REJECT H₀: No significant gender difference")
    print(f"   (p-value {p_value:.4f} > 0.05)")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Grouped bar chart
x = np.arange(2)
width = 0.35

prefer = [prefer_men, prefer_women]
not_prefer = [n_men - prefer_men, n_women - prefer_women]

axes[0].bar(x - width/2, prefer, width, label='Prefer', color='green', alpha=0.7)
axes[0].bar(x + width/2, not_prefer, width, label='Don\'t Prefer', color='red', alpha=0.7)
axes[0].set_xticks(x)
axes[0].set_xticklabels(['Men', 'Women'])
axes[0].set_ylabel('Number of People')
axes[0].set_title('Product Preference by Gender')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

# Plot 2: Proportion comparison
axes[1].bar(['Men', 'Women'], [p_men, p_women], color=['blue', 'pink'], 
            alpha=0.7, edgecolor='black')
axes[1].set_ylabel('Proportion Who Prefer Product')
axes[1].set_title('Preference Rate Comparison')
axes[1].grid(True, alpha=0.3, axis='y')

# Add percentage labels
for i, (label, value) in enumerate([('Men', p_men), ('Women', p_women)]):
    axes[1].text(i, value + 0.01, f'{value*100:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.show()
```

---

### Example 3: Before/After Marketing Campaign (Two-Sample)

**The Situation:**
A company runs a marketing campaign and wants to see if conversion rates improved.
- Before campaign: 80 out of 1000 visitors converted (8%)
- After campaign: 120 out of 1000 visitors converted (12%)

```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

# Data
n_before = 1000
convert_before = 80
p_before = convert_before / n_before

n_after = 1000
convert_after = 120
p_after = convert_after / n_after

print("📈 MARKETING CAMPAIGN EFFECTIVENESS")
print("="*60)
print(f"Before Campaign:")
print(f"  Visitors: {n_before}")
print(f"  Conversions: {convert_before} ({p_before*100:.1f}%)")
print(f"\nAfter Campaign:")
print(f"  Visitors: {n_after}")
print(f"  Conversions: {convert_after} ({p_after*100:.1f}%)")
print(f"\nImprovement: {(p_after - p_before)*100:.1f} percentage points")

# Calculate relative improvement
relative_improvement = ((p_after - p_before) / p_before) * 100
print(f"Relative improvement: {relative_improvement:.1f}%")
print("="*60)

# Perform test (one-tailed: we only care if it improved)
count = np.array([convert_before, convert_after])
nobs = np.array([n_before, n_after])
z_stat, p_value_two = proportions_ztest(count, nobs)
p_value_one = p_value_two / 2  # One-tailed

print(f"\n📊 TEST RESULTS:")
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value (one-tailed): {p_value_one:.4f}")

print("\n🎯 DECISION:")
if p_value_one < 0.05 and z_stat < 0:  # z_stat negative means after > before
    print(f"✅ REJECT H₀: Campaign WORKED!")
    print(f"   (p-value {p_value_one:.4f} < 0.05)")
    print(f"   Conversion rate improved from {p_before*100:.1f}% to {p_after*100:.1f}%")
    print(f"   That's a {relative_improvement:.1f}% relative improvement! 🎉")
else:
    print(f"❌ FAIL TO REJECT H₀: No significant improvement")
    print(f"   (p-value {p_value_one:.4f} > 0.05)")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Conversion rates
axes[0].bar(['Before', 'After'], [p_before, p_after], 
            color=['red', 'green'], alpha=0.7, edgecolor='black')
axes[0].set_ylabel('Conversion Rate')
axes[0].set_title('Conversion Rate: Before vs After Campaign')
axes[0].grid(True, alpha=0.3, axis='y')

# Add percentage labels and arrow
for i, (label, value) in enumerate([('Before', p_before), ('After', p_after)]):
    axes[0].text(i, value + 0.005, f'{value*100:.1f}%', ha='center', fontweight='bold')

# Add improvement arrow
axes[0].annotate('', xy=(1, p_after), xytext=(0, p_before),
                arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
axes[0].text(0.5, (p_before + p_after)/2, f'+{(p_after-p_before)*100:.1f}pp',
            ha='center', fontweight='bold', color='blue', fontsize=12)

# Plot 2: Stacked bar showing conversions
periods = ['Before', 'After']
conversions = [convert_before, convert_after]
non_conversions = [n_before - convert_before, n_after - convert_after]

axes[1].bar(periods, conversions, label='Converted', color='green', alpha=0.7)
axes[1].bar(periods, non_conversions, bottom=conversions, 
            label='Did Not Convert', color='gray', alpha=0.7)
axes[1].set_ylabel('Number of Visitors')
axes[1].set_title('Conversions: Before vs After')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

---

## 5. Practice Exercises - Your Turn! {#practice-exercises}

### Exercise 1: Dice Fairness (One-Sample - Easy)

**The Problem:**
You roll a die 120 times and get the number 6 exactly 25 times. A fair die should show 6 about 1/6 of the time (16.67%). Is this die fair?

**Your Tasks:**
1. What's the claimed proportion?
2. What's your sample proportion?
3. Set up H₀ and H₁
4. Run the test in Python
5. What's your conclusion?

```python
# Write your code here!
# Hint: Claimed proportion = 1/6 ≈ 0.1667
```

<details>
<summary>💡 Click to see solution</summary>

```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

print("🎲 DICE FAIRNESS TEST")
print("="*60)

# Given information
n = 120                    # Number of rolls
sixes = 25                 # Number of times we got 6
p_hat = sixes / n          # Sample proportion
p_0 = 1/6                  # Fair die proportion (16.67%)

# Question 1 & 2
print("Q1 & Q2: Proportions")
print(f"   Claimed proportion (fair die): {p_0:.4f} ({p_0*100:.2f}%)")
print(f"   Sample proportion: {p_hat:.4f} ({p_hat*100:.2f}%)\n")

# Question 3: Hypotheses
print("Q3: Set up hypotheses:")
print("   H₀: p = 1/6 (die is fair)")
print("   H₁: p ≠ 1/6 (die is NOT fair)")
print("   α = 0.05 (95% confidence)\n")

# Question 4: Run the test
z_stat, p_value = proportions_ztest(sixes, n, p_0)

print("Q4: Test Results:")
print(f"   Z-statistic: {z_stat:.4f}")
print(f"   P-value (two-tailed): {p_value:.4f}\n")

# Question 5: Conclusion
print("Q5: Conclusion:")
if p_value < 0.05:
    print(f"   ✅ REJECT H₀!")
    print(f"   The die IS biased!")
    print(f"   (p-value {p_value:.4f} < 0.05)")
    if p_hat > p_0:
        print(f"   It shows 6 TOO OFTEN ({p_hat*100:.1f}% vs expected {p_0*100:.1f}%)")
    else:
        print(f"   It shows 6 TOO RARELY ({p_hat*100:.1f}% vs expected {p_0*100:.1f}%)")
else:
    print(f"   ❌ FAIL TO REJECT H₀")
    print(f"   The die appears fair")
    print(f"   (p-value {p_value:.4f} > 0.05)")
    print(f"   Getting {sixes} sixes in {n} rolls is within normal variation")

print("\n📊 In Plain English:")
print(f"   We got 6 on {sixes} out of {n} rolls ({p_hat*100:.1f}%).")
print(f"   A fair die should show 6 about {p_0*100:.1f}% of the time.")
if p_value < 0.05:
    print("   This difference is too big to be just luck!")
    print("   The die is probably loaded! 🎲")
else:
    print("   This difference could easily happen by chance.")
    print("   The die seems fair! ✅")

print("="*60)
```
</details>

---

### Exercise 2: Drug Effectiveness Comparison (Two-Sample - Medium)

**The Problem:**
Two drugs are being tested for effectiveness:
- **Drug A:** 180 out of 250 patients recovered (72%)
- **Drug B:** 200 out of 250 patients recovered (80%)

**Your Tasks:**
1. Which test should you use?
2. Set up H₀ and H₁
3. Run the test in Python
4. Calculate the difference in recovery rates
5. What's your conclusion? Which drug is better?

```python
# Write your code here!
```

<details>
<summary>💡 Click to see solution</summary>

```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

print("💊 DRUG EFFECTIVENESS COMPARISON")
print("="*60)

# Given information
n_a = 250
recovered_a = 180
p_a = recovered_a / n_a

n_b = 250
recovered_b = 200
p_b = recovered_b / n_b

# Question 1: Which test?
print("Q1: Which test should we use?")
print("   • Two different groups (Drug A patients vs Drug B patients)")
print("   ➡️  Answer: TWO-SAMPLE PROPORTION TEST\n")

# Question 2: Hypotheses
print("Q2: Set up hypotheses:")
print("   H₀: p_A = p_B (both drugs equally effective)")
print("   H₁: p_A ≠ p_B (drugs have different effectiveness)")
print("   α = 0.05 (95% confidence)\n")

# Question 3: Run the test
count = np.array([recovered_a, recovered_b])
nobs = np.array([n_a, n_b])
z_stat, p_value = proportions_ztest(count, nobs)

print("Q3: Test Results:")
print(f"   Drug A: {recovered_a}/{n_a} recovered ({p_a*100:.1f}%)")
print(f"   Drug B: {recovered_b}/{n_b} recovered ({p_b*100:.1f}%)")
print(f"   Z-statistic: {z_stat:.4f}")
print(f"   P-value (two-tailed): {p_value:.4f}\n")

# Question 4: Difference
difference = (p_b - p_a) * 100
print("Q4: Difference in recovery rates:")
print(f"   Drug B - Drug A = {difference:.1f} percentage points")
print(f"   Relative improvement: {(difference/p_a/100)*100:.1f}%\n")

# Question 5: Conclusion
print("Q5: Conclusion:")
if p_value < 0.05:
    print(f"   ✅ REJECT H₀!")
    print(f"   The drugs ARE significantly different!")
    print(f"   (p-value {p_value:.4f} < 0.05)")
    if p_b > p_a:
        print(f"   Drug B is BETTER! ({p_b*100:.1f}% vs {p_a*100:.1f}%)")
        print(f"   Drug B has {difference:.1f} percentage points higher recovery rate")
    else:
        print(f"   Drug A is BETTER! ({p_a*100:.1f}% vs {p_b*100:.1f}%)")
else:
    print(f"   ❌ FAIL TO REJECT H₀")
    print(f"   No significant difference found")
    print(f"   (p-value {p_value:.4f} > 0.05)")
    print(f"   Both drugs appear equally effective")

print("\n📊 In Plain English:")
print(f"   Drug A helped {p_a*100:.0f}% of patients recover.")
print(f"   Drug B helped {p_b*100:.0f}% of patients recover.")
if p_value < 0.05:
    print(f"   This {difference:.0f} percentage point difference is real!")
    print(f"   Drug B is the clear winner! 💊✨")
else:
    print(f"   The {difference:.0f} percentage point difference could be random.")
    print(f"   Both drugs work about the same.")

print("="*60)

# Visualize
plt.figure(figsize=(12, 5))

# Plot 1: Recovery rates
plt.subplot(1, 2, 1)
plt.bar(['Drug A', 'Drug B'], [p_a, p_b], color=['blue', 'green'], 
        alpha=0.7, edgecolor='black')
plt.ylabel('Recovery Rate')
plt.title('Drug Effectiveness Comparison')
plt.grid(True, alpha=0.3, axis='y')

# Add percentage labels
for i, (drug, rate) in enumerate([('Drug A', p_a), ('Drug B', p_b)]):
    plt.text(i, rate + 0.02, f'{rate*100:.1f}%', ha='center', fontweight='bold')

# Plot 2: Stacked bars
plt.subplot(1, 2, 2)
drugs = ['Drug A', 'Drug B']
recovered = [recovered_a, recovered_b]
not_recovered = [n_a - recovered_a, n_b - recovered_b]

plt.bar(drugs, recovered, label='Recovered', color='green', alpha=0.7)
plt.bar(drugs, not_recovered, bottom=recovered, label='Not Recovered', 
        color='red', alpha=0.7)
plt.ylabel('Number of Patients')
plt.title('Recovery Outcomes')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```
</details>

---

### Exercise 3: Your Own Example! (Challenge)

Create your own proportion test scenario!

**Option A: One-Sample Proportion Test**
```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Example: Test if success rate meets target
print("MY ONE-SAMPLE PROPORTION TEST")
print("="*60)
print("Scenario: [Describe your situation]")
print("Claimed proportion: [e.g., 50%]")
print("="*60)

# Your data
# n = ...           # Sample size
# successes = ...   # Number of successes
# p_0 = ...         # Claimed proportion

# Run test
# z_stat, p_value = proportions_ztest(successes, n, p_0)

# Make conclusion
```

**Option B: Two-Sample Proportion Test**
```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Example: Compare two groups
print("MY TWO-SAMPLE PROPORTION TEST")
print("="*60)
print("Scenario: [Describe your comparison]")
print("="*60)

# Your data
# count = np.array([successes_group1, successes_group2])
# nobs = np.array([n_group1, n_group2])

# Run test
# z_stat, p_value = proportions_ztest(count, nobs)

# Make conclusion
```

**Ideas for scenarios:**
- 🎯 Click-through rates: Email A vs Email B
- 🎮 Win rates: Player 1 vs Player 2
- 🏥 Side effect rates: Old drug vs New drug
- 🗳️ Poll results: Support in State A vs State B
- 📱 App crash rates: iOS vs Android
- 🎓 Pass rates: Online course vs In-person course

---

## Summary - What You Learned! 🎓

### Key Concepts

**1. What Are Proportions?**
- Proportions are percentages expressed as decimals (0 to 1)
- Used for yes/no, success/failure, click/no-click data
- Examples: 60% = 0.60, 25% = 0.25

**2. One-Sample Proportion Test**
- Compare ONE sample proportion to a claimed value
- Example: Is the coin fair? (claimed: 50%)
- Formula: $Z = \frac{\hat{p} - p_0}{\sqrt{\frac{p_0(1-p_0)}{n}}}$
- Python: `proportions_ztest(count, nobs, value)`

**3. Two-Sample Proportion Test**
- Compare TWO sample proportions to each other
- Example: Do men and women have different click rates?
- Uses pooled proportion for standard error
- Python: `proportions_ztest(count_array, nobs_array)`

**4. Sample Size Requirements**
- Need: np ≥ 10 AND n(1-p) ≥ 10
- This ensures the normal approximation works
- If not met, results may be unreliable

### Quick Decision Tree

```
What are you comparing?
│
├─ One proportion to a claimed value?
│  └─ Use ONE-SAMPLE PROPORTION TEST
│     proportions_ztest(count, nobs, value)
│
└─ Two proportions to each other?
   └─ Use TWO-SAMPLE PROPORTION TEST
      proportions_ztest(count_array, nobs_array)
```

### Python Cheat Sheet

```python
from statsmodels.stats.proportion import proportions_ztest
import numpy as np

# One-Sample Proportion Test
count = 60        # Number of successes
nobs = 100        # Sample size
value = 0.5       # Claimed proportion
z_stat, p_value = proportions_ztest(count, nobs, value)

# Two-Sample Proportion Test
count = np.array([50, 80])      # Successes in each group
nobs = np.array([500, 500])     # Sample sizes
z_stat, p_value = proportions_ztest(count, nobs)

# One-tailed test (add alternative parameter)
z_stat, p_value = proportions_ztest(count, nobs, value, 
                                    alternative='larger')  # or 'smaller'

# Decision
if p_value < 0.05:
    print("Significant difference found!")
else:
    print("No significant difference")
```

### Common Mistakes to Avoid ⚠️

1. **Using proportion tests for averages** → Use t-tests instead!
2. **Forgetting to check sample size requirements** → Need np ≥ 10 and n(1-p) ≥ 10
3. **Confusing proportions with counts** → Use proportions (0-1), not percentages (0-100)
4. **Using two-sample test for before/after** → If same subjects, consider paired t-test
5. **Ignoring practical significance** → Small p-value doesn't always mean important difference

### Proportion vs Mean Tests

**Use Proportion Tests when:**
- ✅ Data is yes/no, success/failure, click/no-click
- ✅ You're comparing percentages
- ✅ Example: "60% of customers are satisfied"

**Use Mean Tests (t-tests) when:**
- ✅ Data is continuous numbers
- ✅ You're comparing averages
- ✅ Example: "Average customer satisfaction score is 7.5/10"

### Real-World Applications

**Marketing & Business:**
- A/B testing website designs
- Comparing conversion rates
- Customer satisfaction surveys
- Click-through rate analysis

**Healthcare:**
- Drug effectiveness (cure rates)
- Side effect rates
- Patient recovery rates
- Treatment success rates

**Quality Control:**
- Defect rates
- Product failure rates
- Compliance rates
- Error rates

**Politics & Social Science:**
- Poll results and voter preferences
- Survey response rates
- Demographic comparisons
- Public opinion changes

---

## What's Next?

Congratulations! You've completed the Hypothesis Testing Methods series! 🎉

**You now know:**
- ✅ **Chapter 4.1**: Single Sample Tests (Z-test, T-test)
- ✅ **Chapter 4.2**: Two Sample Tests (Independent, Paired)
- ✅ **Chapter 4.3**: Proportion Tests (One-sample, Two-sample)

**Next topics to explore:**
- **Chi-Square Tests**: Testing relationships between categorical variables
- **ANOVA**: Comparing more than two groups
- **Regression Analysis**: Predicting outcomes and finding relationships
- **Non-Parametric Tests**: When your data doesn't meet assumptions

Keep practicing! The more you use these tests, the more intuitive they become! 🚀

---

**Remember:** Statistics is about making informed decisions with data. Always ask yourself:
1. What question am I trying to answer?
2. What type of data do I have?
3. Which test is appropriate?
4. What do my results mean in the real world?

You're not just calculating p-values - you're solving real problems! 💡
