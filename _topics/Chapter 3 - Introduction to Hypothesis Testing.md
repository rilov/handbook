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

Imagine you're a detective trying to solve a mystery. You have a hunch (a hypothesis), and you need to collect evidence (data) to see if your hunch is right or wrong. That's exactly what hypothesis testing is!

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

The **p-value** is a number between 0 and 1 that tells you:
> "If the null hypothesis were true, what's the probability of getting evidence as extreme as (or more extreme than) what we observed?"

**Think of it like this:**
- **Small p-value (< 0.05)**: "Wow, this is really unusual! Something's going on!"
- **Large p-value (> 0.05)**: "Meh, this could easily happen by random chance"

**The Magic Number: 0.05**
- If p-value < 0.05 → Evidence is strong → Reject H₀
- If p-value > 0.05 → Evidence is weak → Don't reject H₀

### 🎚️ Significance Level (α) - "How Sure Do We Need to Be?"

The **significance level** (alpha, α) is like setting the bar for how much evidence you need:
- Usually set to **0.05** (which means 95% confidence)
- Sometimes **0.01** (99% confidence - very strict!)
- Sometimes **0.10** (90% confidence - more lenient)

**What it means:**
- α = 0.05 means: "I'm willing to be wrong 5% of the time"
- It's the threshold for deciding if evidence is strong enough

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

## 6. Complete Python Example {#python-example}

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
