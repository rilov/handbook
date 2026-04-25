---
title: "Chapter 2: Inferential Statistics and Hypothesis Testing"
category: Data Science
order: 2
tags:
  - statistics
  - inferential-statistics
  - hypothesis-testing
  - sampling
summary: "Learn how to make predictions about populations from samples, understand confidence intervals, and test hypotheses using statistical methods."
---

# 🎯 Inferential Statistics - Making Smart Predictions!

## 📚 What is Inferential Statistics?

Imagine you want to know the average height of all students in your country, but you can't measure everyone! **Inferential Statistics** helps you make smart guesses about a big group (population) by studying a smaller group (sample).

**Think of it like this:**
- 🍪 You taste ONE cookie from a batch to know if ALL cookies are good
- 🎮 You play a few levels of a game to decide if you'll like the WHOLE game
- 📊 You survey 100 students to understand what ALL students think

<div class="mermaid">
flowchart TD
    A[🌍 Population<br/>Everyone/Everything] --> B[📦 Take a Sample<br/>Small group]
    B --> C[📊 Analyze Sample<br/>Calculate statistics]
    C --> D[🎯 Make Inference<br/>Predict about population]
    D --> E[✅ Test if prediction<br/>is reliable]
    
    style A fill:#E74C3C,stroke:#A93226,stroke-width:3px,color:#fff
    style B fill:#3498DB,stroke:#1F618D,stroke-width:3px,color:#fff
    style C fill:#2ECC71,stroke:#1E8449,stroke-width:3px,color:#fff
    style D fill:#F39C12,stroke:#B9770E,stroke-width:3px,color:#fff
    style E fill:#9B59B6,stroke:#6C3483,stroke-width:3px,color:#fff
</div>

---

## 🎯 The Learning Journey

<div class="mermaid">
mindmap
  root((Inferential<br/>Statistics))
    Central Limit Theorem
      Sampling Distribution
      Normal Distribution
      Standard Error
    Hypothesis Testing I
      Null Hypothesis
      Alternative Hypothesis
      Critical Values
    Hypothesis Testing II
      p-value Method
      Type I Error
      Type II Error
</div>

---

## 🐍 Python Setup for Inferential Statistics

```python
# Import essential libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import scipy.stats as st

# Set up nice visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
```

---

## 📖 Chapter 1: Understanding Populations and Samples

### 🌍 Key Terms (Simple Explanations)

<div class="mermaid">
graph TD
    A[Statistical Terms] --> B[Population]
    A --> C[Sample]
    
    B --> D[Population Size N<br/>Total count of everyone]
    B --> E[Population Mean μ<br/>Average of everyone]
    B --> F[Population Variance σ²<br/>How spread out data is]
    
    C --> G[Sample Size n<br/>Count in your sample]
    C --> H[Sample Mean X̄<br/>Average of sample]
    C --> I[Sample Variance s²<br/>Spread in sample]
    
    style A fill:#E74C3C,stroke:#A93226,stroke-width:3px,color:#fff
    style B fill:#3498DB,stroke:#1F618D,stroke-width:3px,color:#fff
    style C fill:#2ECC71,stroke:#1E8449,stroke-width:3px,color:#fff
    style D fill:#9B59B6,stroke:#6C3483,stroke-width:3px,color:#fff
    style E fill:#E67E22,stroke:#A04000,stroke-width:3px,color:#fff
    style F fill:#1ABC9C,stroke:#117A65,stroke-width:3px,color:#fff
    style G fill:#F39C12,stroke:#B9770E,stroke-width:3px,color:#fff
    style H fill:#27AE60,stroke:#186A3B,stroke-width:3px,color:#fff
    style I fill:#C0392B,stroke:#7B241C,stroke-width:3px,color:#fff
</div>

**Simple Definitions:**

| Symbol | Name | What it means | Example |
|--------|------|---------------|---------|
| **N** | Population Size | Total number of everyone | All 1000 students in school |
| **μ** (mu) | Population Mean | Average of everyone | Average height of all students |
| **σ²** (sigma squared) | Population Variance | How different everyone is | How heights vary across all students |
| **n** | Sample Size | Number in your sample | 50 students you measured |
| **X̄** (x-bar) | Sample Mean | Average of your sample | Average height of 50 students |
| **s²** | Sample Variance | How different sample is | How heights vary in your 50 students |

### 🎮 Real-World Example: Facebook Feature Test

**Scenario:** Facebook wants to add a fact-checking feature but doesn't want to test it on ALL 2 billion users!

```python
import numpy as np
import matplotlib.pyplot as plt

# Simulate Facebook's approach
np.random.seed(42)

# Population: All Facebook users' preferences (unknown to Facebook)
# Let's say 52% actually prefer the new feature
population_preference = 0.52

# Facebook samples 10,000 users
sample_size = 10000
sample_results = np.random.binomial(1, population_preference, sample_size)
sample_preference = sample_results.mean()

print(f"🌍 True population preference: {population_preference*100}%")
print(f"📊 Sample preference (10,000 users): {sample_preference*100:.2f}%")
print(f"📏 Difference: {abs(population_preference - sample_preference)*100:.2f}%")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Sample results
axes[0].bar(['Prefer Old', 'Prefer New'], 
            [1-sample_preference, sample_preference],
            color=['#E74C3C', '#2ECC71'], edgecolor='black', linewidth=2)
axes[0].set_ylabel('Proportion', fontweight='bold')
axes[0].set_title(f'Sample Results (n={sample_size})', fontweight='bold', fontsize=13)
axes[0].set_ylim(0, 1)
for i, v in enumerate([1-sample_preference, sample_preference]):
    axes[0].text(i, v + 0.02, f'{v*100:.1f}%', ha='center', fontweight='bold')

# Plot 2: Comparison
categories = ['True\nPopulation', 'Sample\nEstimate']
values = [population_preference, sample_preference]
axes[1].bar(categories, values, color=['#3498DB', '#F39C12'], 
            edgecolor='black', linewidth=2)
axes[1].set_ylabel('Preference for New Feature', fontweight='bold')
axes[1].set_title('Population vs Sample', fontweight='bold', fontsize=13)
axes[1].set_ylim(0, 1)
for i, v in enumerate(values):
    axes[1].text(i, v + 0.02, f'{v*100:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.show()
```

**Why Sample Instead of Everyone?**
- ⏰ **Saves Time**: Testing 10,000 users vs 2 billion users
- 💰 **Saves Money**: Cheaper to run small tests
- 🛡️ **Reduces Risk**: If feature fails, only affects small group
- 📊 **Still Accurate**: With proper sampling, results are reliable!

---

## 📊 Chapter 2: Central Limit Theorem (CLT)

### 🎪 The Magic of CLT

**The Central Limit Theorem is like magic!** It says:

> "If you take many samples and calculate their averages, those averages will form a bell curve (normal distribution), even if your original data isn't bell-shaped!"

<div class="mermaid">
flowchart LR
    A[🎲 Any Population<br/>Any shape!] --> B[📦 Take many<br/>samples]
    B --> C[📊 Calculate each<br/>sample mean]
    C --> D[🔔 Sample means form<br/>NORMAL distribution!]
    
    style A fill:#E74C3C,stroke:#A93226,stroke-width:3px,color:#fff
    style B fill:#3498DB,stroke:#1F618D,stroke-width:3px,color:#fff
    style C fill:#2ECC71,stroke:#1E8449,stroke-width:3px,color:#fff
    style D fill:#F39C12,stroke:#B9770E,stroke-width:3px,color:#fff
</div>

### 📐 CLT Formulas

**Properties of Sampling Distribution:**

```
1. Mean of sampling distribution = Population mean
   μₓ̄ = μ

2. Standard Error (SE) = Population std dev / √sample size
   SE = σ / √n
   
3. For n > 30, distribution becomes normal (bell curve)
```

**Confidence Interval Formula:**
```
Confidence Interval = X̄ ± Z* × (S/√n)

Where:
- X̄ = sample mean
- Z* = Z-score for confidence level
- S = sample standard deviation
- n = sample size
- S/√n = Standard Error (SE)
```

**Common Z* values:**
- 90% confidence: Z* = 1.645
- 95% confidence: Z* = 1.96
- 99% confidence: Z* = 2.576

### 🐍 Python Example: CLT in Action!

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Let's prove CLT with dice rolls!
np.random.seed(42)

# Population: Rolling a die (uniform distribution, NOT normal!)
population = np.arange(1, 7)  # [1, 2, 3, 4, 5, 6]
population_mean = population.mean()
population_std = population.std()

print(f"🎲 Population (Die): {population}")
print(f"📊 Population Mean: {population_mean}")
print(f"📏 Population Std Dev: {population_std:.3f}\n")

# Take many samples and calculate their means
sample_size = 30
num_samples = 1000
sample_means = []

for i in range(num_samples):
    sample = np.random.choice(population, size=sample_size, replace=True)
    sample_means.append(sample.mean())

sample_means = np.array(sample_means)

# Calculate statistics of sample means
mean_of_means = sample_means.mean()
std_of_means = sample_means.std()
theoretical_se = population_std / np.sqrt(sample_size)

print(f"📊 Mean of sample means: {mean_of_means:.3f}")
print(f"📏 Std of sample means: {std_of_means:.3f}")
print(f"🎯 Theoretical SE (σ/√n): {theoretical_se:.3f}")

# Visualize CLT
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Original population (uniform)
axes[0].hist(population, bins=6, color='#E74C3C', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Die Value', fontweight='bold')
axes[0].set_ylabel('Frequency', fontweight='bold')
axes[0].set_title('Original Population\n(Uniform Distribution)', fontweight='bold')
axes[0].axvline(population_mean, color='blue', linestyle='--', linewidth=2, 
                label=f'Mean = {population_mean}')
axes[0].legend()

# Plot 2: Sampling distribution (normal!)
axes[1].hist(sample_means, bins=30, color='#2ECC71', edgecolor='black', 
             alpha=0.7, density=True)
axes[1].set_xlabel('Sample Mean', fontweight='bold')
axes[1].set_ylabel('Density', fontweight='bold')
axes[1].set_title(f'Sampling Distribution of Means\n(n={sample_size}, samples={num_samples})', 
                  fontweight='bold')

# Overlay normal curve
x = np.linspace(sample_means.min(), sample_means.max(), 100)
axes[1].plot(x, stats.norm.pdf(x, mean_of_means, std_of_means), 
             'r-', linewidth=2, label='Normal curve')
axes[1].axvline(mean_of_means, color='blue', linestyle='--', linewidth=2,
                label=f'Mean = {mean_of_means:.2f}')
axes[1].legend()

plt.tight_layout()
plt.show()

print("\n✨ CLT Magic: Even though dice rolls are uniform,")
print("   the sample means form a beautiful bell curve!")
```

### 🎯 Confidence Interval Example

```python
# Calculate 95% confidence interval for student heights
np.random.seed(42)

# Sample of 50 student heights (in cm)
sample_heights = np.random.normal(165, 10, 50)
n = len(sample_heights)
sample_mean = sample_heights.mean()
sample_std = sample_heights.std(ddof=1)  # ddof=1 for sample std
se = sample_std / np.sqrt(n)

# 95% confidence interval
confidence_level = 0.95
z_star = stats.norm.ppf((1 + confidence_level) / 2)
margin_of_error = z_star * se

ci_lower = sample_mean - margin_of_error
ci_upper = sample_mean + margin_of_error

print(f"📊 Sample Statistics:")
print(f"   Sample size (n): {n}")
print(f"   Sample mean (X̄): {sample_mean:.2f} cm")
print(f"   Sample std (S): {sample_std:.2f} cm")
print(f"   Standard Error (SE): {se:.2f} cm")
print(f"\n🎯 95% Confidence Interval:")
print(f"   Z* = {z_star:.3f}")
print(f"   Margin of Error = {margin_of_error:.2f} cm")
print(f"   CI = ({ci_lower:.2f}, {ci_upper:.2f}) cm")
print(f"\n💡 Interpretation:")
print(f"   We are 95% confident that the true average height")
print(f"   of ALL students is between {ci_lower:.2f} cm and {ci_upper:.2f} cm")

# Visualize
plt.figure(figsize=(10, 6))
plt.hist(sample_heights, bins=15, color='#3498DB', edgecolor='black', alpha=0.7)
plt.axvline(sample_mean, color='red', linestyle='--', linewidth=2, 
            label=f'Sample Mean = {sample_mean:.2f}')
plt.axvline(ci_lower, color='green', linestyle='--', linewidth=2, 
            label=f'95% CI Lower = {ci_lower:.2f}')
plt.axvline(ci_upper, color='green', linestyle='--', linewidth=2, 
            label=f'95% CI Upper = {ci_upper:.2f}')
plt.xlabel('Height (cm)', fontweight='bold')
plt.ylabel('Frequency', fontweight='bold')
plt.title('Student Heights with 95% Confidence Interval', fontweight='bold', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 🧪 Chapter 3: Hypothesis Testing - Part I

### 🎯 What is Hypothesis Testing?

**Hypothesis Testing** is like being a detective! You have a claim, and you need to find evidence to prove or disprove it.

<div class="mermaid">
flowchart TD
    A[🤔 Start with a Claim] --> B[📝 Write Hypotheses<br/>H₀ and H₁]
    B --> C[📊 Collect Sample Data]
    C --> D[🧮 Calculate Test Statistic]
    D --> E{Is evidence<br/>strong enough?}
    E -->|Yes| F[❌ Reject H₀<br/>Accept H₁]
    E -->|No| G[✅ Fail to Reject H₀<br/>Stick with status quo]
    
    style A fill:#E74C3C,stroke:#A93226,stroke-width:3px,color:#fff
    style B fill:#3498DB,stroke:#1F618D,stroke-width:3px,color:#fff
    style C fill:#2ECC71,stroke:#1E8449,stroke-width:3px,color:#fff
    style D fill:#F39C12,stroke:#B9770E,stroke-width:3px,color:#fff
    style E fill:#9B59B6,stroke:#6C3483,stroke-width:3px,color:#fff
    style F fill:#E67E22,stroke:#A04000,stroke-width:3px,color:#fff
    style G fill:#1ABC9C,stroke:#117A65,stroke-width:3px,color:#fff
</div>

### 📋 The Two Hypotheses

<div class="mermaid">
graph TD
    A[Hypotheses] --> B[Null Hypothesis H₀<br/>Status Quo]
    A --> C[Alternative Hypothesis H₁<br/>What we want to prove]
    
    B --> D[Uses: =, ≤, ≥<br/>Assumes no change]
    C --> E[Uses: ≠, <, ><br/>Claims a change]
    
    style A fill:#E74C3C,stroke:#A93226,stroke-width:3px,color:#fff
    style B fill:#3498DB,stroke:#1F618D,stroke-width:3px,color:#fff
    style C fill:#2ECC71,stroke:#1E8449,stroke-width:3px,color:#fff
    style D fill:#F39C12,stroke:#B9770E,stroke-width:3px,color:#fff
    style E fill:#9B59B6,stroke:#6C3483,stroke-width:3px,color:#fff
</div>

**Simple Explanation:**

- **H₀ (Null Hypothesis)**: "Nothing special is happening" or "Things are normal"
  - Example: "The average test score is 75"
  
- **H₁ (Alternative Hypothesis)**: "Something interesting is happening!"
  - Example: "The average test score is NOT 75" or "higher than 75" or "lower than 75"

### 🎯 Types of Tests

<div class="mermaid">
graph TD
    A[Type of Test] --> B[Two-Tailed<br/>H₁: μ ≠ value]
    A --> C[Right-Tailed<br/>H₁: μ > value]
    A --> D[Left-Tailed<br/>H₁: μ < value]
    
    B --> E[Reject regions<br/>on BOTH sides]
    C --> F[Reject region<br/>on RIGHT side]
    D --> G[Reject region<br/>on LEFT side]
    
    style A fill:#E74C3C,stroke:#A93226,stroke-width:3px,color:#fff
    style B fill:#3498DB,stroke:#1F618D,stroke-width:3px,color:#fff
    style C fill:#2ECC71,stroke:#1E8449,stroke-width:3px,color:#fff
    style D fill:#F39C12,stroke:#B9770E,stroke-width:3px,color:#fff
    style E fill:#9B59B6,stroke:#6C3483,stroke-width:3px,color:#fff
    style F fill:#E67E22,stroke:#A04000,stroke-width:3px,color:#fff
    style G fill:#1ABC9C,stroke:#117A65,stroke-width:3px,color:#fff
</div>

### 📐 Critical Value Method - Step by Step

**Steps:**
1. **Set up hypotheses** (H₀ and H₁)
2. **Choose significance level** α (usually 0.05 = 5%)
3. **Find critical value(s)** from Z-table
4. **Calculate test statistic** from sample
5. **Make decision**: Compare test statistic with critical value

**Formula for Test Statistic:**
```
Z = (X̄ - μ₀) / (S / √n)

Where:
- X̄ = sample mean
- μ₀ = hypothesized population mean
- S = sample standard deviation
- n = sample size
```

### 🐍 Python Example: Testing Average Score

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Problem: A teacher claims the average test score is 75
# A sample of 40 students has mean = 78 and std = 10
# Test at α = 0.05 if the average is different from 75

# Step 1: Set up hypotheses
print("📝 Step 1: Hypotheses")
print("H₀: μ = 75 (average score is 75)")
print("H₁: μ ≠ 75 (average score is NOT 75)")
print("This is a TWO-TAILED test\n")

# Step 2: Given data
sample_mean = 78
hypothesized_mean = 75
sample_std = 10
n = 40
alpha = 0.05

print(f"📊 Step 2: Given Data")
print(f"Sample mean (X̄) = {sample_mean}")
print(f"Hypothesized mean (μ₀) = {hypothesized_mean}")
print(f"Sample std (S) = {sample_std}")
print(f"Sample size (n) = {n}")
print(f"Significance level (α) = {alpha}\n")

# Step 3: Calculate critical values
z_critical = stats.norm.ppf(1 - alpha/2)  # Two-tailed
print(f"🎯 Step 3: Critical Values")
print(f"Z_critical = ±{z_critical:.3f}")
print(f"Reject H₀ if Z < -{z_critical:.3f} or Z > {z_critical:.3f}\n")

# Step 4: Calculate test statistic
se = sample_std / np.sqrt(n)
z_statistic = (sample_mean - hypothesized_mean) / se

print(f"🧮 Step 4: Calculate Test Statistic")
print(f"Standard Error (SE) = {se:.3f}")
print(f"Z = (X̄ - μ₀) / SE = ({sample_mean} - {hypothesized_mean}) / {se:.3f}")
print(f"Z = {z_statistic:.3f}\n")

# Step 5: Make decision
print(f"✅ Step 5: Decision")
if abs(z_statistic) > z_critical:
    print(f"Since |{z_statistic:.3f}| > {z_critical:.3f}")
    print("❌ REJECT H₀")
    print("📊 Conclusion: There is significant evidence that the average")
    print("   score is different from 75")
else:
    print(f"Since |{z_statistic:.3f}| ≤ {z_critical:.3f}")
    print("✅ FAIL TO REJECT H₀")
    print("📊 Conclusion: Not enough evidence to say average is different from 75")

# Visualize
x = np.linspace(-4, 4, 1000)
y = stats.norm.pdf(x)

plt.figure(figsize=(12, 6))
plt.plot(x, y, 'b-', linewidth=2, label='Standard Normal Distribution')

# Shade rejection regions
plt.fill_between(x[x < -z_critical], y[x < -z_critical], alpha=0.3, color='red', 
                 label=f'Rejection Region (α/2 = {alpha/2})')
plt.fill_between(x[x > z_critical], y[x > z_critical], alpha=0.3, color='red')

# Mark critical values
plt.axvline(-z_critical, color='red', linestyle='--', linewidth=2, 
            label=f'Critical values: ±{z_critical:.3f}')
plt.axvline(z_critical, color='red', linestyle='--', linewidth=2)

# Mark test statistic
plt.axvline(z_statistic, color='green', linestyle='-', linewidth=3, 
            label=f'Test statistic: {z_statistic:.3f}')

plt.xlabel('Z-score', fontweight='bold', fontsize=12)
plt.ylabel('Probability Density', fontweight='bold', fontsize=12)
plt.title('Hypothesis Test: Two-Tailed Test', fontweight='bold', fontsize=14)
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 🔬 Chapter 4: Hypothesis Testing - Part II (p-value Method)

### 💡 What is a p-value?

**p-value** = "How surprising is our result if H₀ is true?"

- **Low p-value** (< 0.05): Very surprising! Reject H₀
- **High p-value** (≥ 0.05): Not surprising. Don't reject H₀

<div class="mermaid">
flowchart LR
    A[Calculate<br/>p-value] --> B{p-value < α?}
    B -->|Yes| C[❌ Reject H₀<br/>Result is significant]
    B -->|No| D[✅ Fail to Reject H₀<br/>Result not significant]
    
    style A fill:#3498DB,stroke:#1F618D,stroke-width:3px,color:#fff
    style B fill:#F39C12,stroke:#B9770E,stroke-width:3px,color:#fff
    style C fill:#E74C3C,stroke:#A93226,stroke-width:3px,color:#fff
    style D fill:#2ECC71,stroke:#1E8449,stroke-width:3px,color:#fff
</div>

### 📐 p-value Method Steps

**Steps:**
1. Calculate Z-score from sample
2. Find p-value from Z-score
3. Compare p-value with α
4. Make decision

**p-value Calculation:**
```
For two-tailed test: p-value = 2 × P(Z > |z|)
For right-tailed test: p-value = P(Z > z)
For left-tailed test: p-value = P(Z < z)
```

### 🐍 Python Example: p-value Method

```python
# Same problem as before, but using p-value method
print("📝 Hypothesis Test using p-value Method\n")

# Given data (same as before)
sample_mean = 78
hypothesized_mean = 75
sample_std = 10
n = 40
alpha = 0.05

# Calculate test statistic
se = sample_std / np.sqrt(n)
z_statistic = (sample_mean - hypothesized_mean) / se

print(f"📊 Test Statistic: Z = {z_statistic:.3f}\n")

# Calculate p-value (two-tailed)
p_value = 2 * (1 - stats.norm.cdf(abs(z_statistic)))

print(f"💡 p-value Calculation:")
print(f"p-value = 2 × P(Z > |{z_statistic:.3f}|)")
print(f"p-value = {p_value:.4f}\n")

# Make decision
print(f"✅ Decision:")
print(f"α = {alpha}")
if p_value < alpha:
    print(f"Since p-value ({p_value:.4f}) < α ({alpha})")
    print("❌ REJECT H₀")
    print("📊 The result is statistically significant!")
else:
    print(f"Since p-value ({p_value:.4f}) ≥ α ({alpha})")
    print("✅ FAIL TO REJECT H₀")
    print("📊 The result is NOT statistically significant")

print(f"\n💭 Interpretation:")
print(f"There is only a {p_value*100:.2f}% chance of getting this result")
print(f"if the true mean were actually 75.")

# Visualize p-value
x = np.linspace(-4, 4, 1000)
y = stats.norm.pdf(x)

plt.figure(figsize=(12, 6))
plt.plot(x, y, 'b-', linewidth=2, label='Standard Normal Distribution')

# Shade p-value regions
plt.fill_between(x[x < -abs(z_statistic)], y[x < -abs(z_statistic)], 
                 alpha=0.5, color='orange', label=f'p-value = {p_value:.4f}')
plt.fill_between(x[x > abs(z_statistic)], y[x > abs(z_statistic)], 
                 alpha=0.5, color='orange')

# Mark test statistic
plt.axvline(z_statistic, color='red', linestyle='-', linewidth=3, 
            label=f'Test statistic: {z_statistic:.3f}')
plt.axvline(-z_statistic, color='red', linestyle='--', linewidth=2)

plt.xlabel('Z-score', fontweight='bold', fontsize=12)
plt.ylabel('Probability Density', fontweight='bold', fontsize=12)
plt.title('p-value Visualization (Two-Tailed Test)', fontweight='bold', fontsize=14)
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## ⚠️ Chapter 5: Types of Errors

### 🎯 Understanding Type I and Type II Errors

<div class="mermaid">
graph TD
    A[Reality vs Decision] --> B[Type I Error α<br/>False Positive]
    A --> C[Type II Error β<br/>False Negative]
    
    B --> D[Reject TRUE H₀<br/>False Alarm!]
    C --> E[Fail to reject FALSE H₀<br/>Missed Detection!]
    
    D --> F[Example: Innocent person<br/>declared guilty]
    E --> G[Example: Guilty person<br/>declared innocent]
    
    style A fill:#E74C3C,stroke:#A93226,stroke-width:3px,color:#fff
    style B fill:#E67E22,stroke:#A04000,stroke-width:3px,color:#fff
    style C fill:#3498DB,stroke:#1F618D,stroke-width:3px,color:#fff
    style D fill:#F39C12,stroke:#B9770E,stroke-width:3px,color:#fff
    style E fill:#9B59B6,stroke:#6C3483,stroke-width:3px,color:#fff
    style F fill:#C0392B,stroke:#7B241C,stroke-width:3px,color:#fff
    style G fill:#2980B9,stroke:#1A5276,stroke-width:3px,color:#fff
</div>

### 📊 Error Types Table

| | **H₀ is TRUE** | **H₀ is FALSE** |
|---|---|---|
| **Reject H₀** | ❌ Type I Error (α)<br/>False Positive | ✅ Correct Decision<br/>True Positive |
| **Fail to Reject H₀** | ✅ Correct Decision<br/>True Negative | ❌ Type II Error (β)<br/>False Negative |

### 🏥 Real-World Example: COVID-19 Test

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# COVID-19 Testing Example
print("🏥 COVID-19 Testing Errors\n")
print("H₀: Person does NOT have COVID-19")
print("H₁: Person HAS COVID-19\n")

# Create confusion matrix
errors_data = {
    'Reality': ['No COVID', 'No COVID', 'Has COVID', 'Has COVID'],
    'Test Result': ['Negative', 'Positive', 'Negative', 'Positive'],
    'Outcome': ['✅ Correct\n(True Negative)', 
                '❌ Type I Error\n(False Positive)', 
                '❌ Type II Error\n(False Negative)', 
                '✅ Correct\n(True Positive)'],
    'Consequence': ['Person is healthy\nand test says healthy',
                   'Person is healthy\nbut test says sick',
                   'Person is sick\nbut test says healthy',
                   'Person is sick\nand test says sick']
}

df_errors = pd.DataFrame(errors_data)

print("📊 Error Types:")
print("\n🔴 Type I Error (α) - False Positive:")
print("   Test says: Person HAS COVID")
print("   Reality: Person does NOT have COVID")
print("   Consequence: Unnecessary quarantine, anxiety, treatment\n")

print("🔵 Type II Error (β) - False Negative:")
print("   Test says: Person does NOT have COVID")
print("   Reality: Person HAS COVID")
print("   Consequence: Spreads infection, no treatment\n")

# Visualize with a table
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('tight')
ax.axis('off')

table_data = [
    ['', 'H₀ TRUE\n(No COVID)', 'H₀ FALSE\n(Has COVID)'],
    ['Reject H₀\n(Test Positive)', 
     '❌ Type I Error (α)\nFalse Positive\nHealthy → Quarantine', 
     '✅ Correct\nTrue Positive\nSick → Treatment'],
    ['Fail to Reject H₀\n(Test Negative)', 
     '✅ Correct\nTrue Negative\nHealthy → Free', 
     '❌ Type II Error (β)\nFalse Negative\nSick → Spreads virus']
]

table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.25, 0.375, 0.375])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 3)

# Color cells
for i in range(len(table_data)):
    for j in range(len(table_data[0])):
        cell = table[(i, j)]
        if i == 0 or j == 0:
            cell.set_facecolor('#3498DB')
            cell.set_text_props(weight='bold', color='white')
        elif '❌' in table_data[i][j]:
            cell.set_facecolor('#FFE5E5')
        else:
            cell.set_facecolor('#E5FFE5')

plt.title('Type I and Type II Errors in COVID-19 Testing', 
          fontweight='bold', fontsize=14, pad=20)
plt.tight_layout()
plt.show()

# Simulate error rates
np.random.seed(42)
n_tests = 1000
true_positive_rate = 0.95  # Sensitivity (1 - β)
true_negative_rate = 0.90  # Specificity (1 - α)

# 30% of people actually have COVID
has_covid = np.random.binomial(1, 0.3, n_tests)

# Test results
test_results = []
for person_has_covid in has_covid:
    if person_has_covid:
        # Person has COVID: test positive with 95% probability
        test_positive = np.random.binomial(1, true_positive_rate)
    else:
        # Person doesn't have COVID: test positive with 10% probability (Type I error)
        test_positive = np.random.binomial(1, 1 - true_negative_rate)
    test_results.append(test_positive)

test_results = np.array(test_results)

# Calculate errors
true_positives = np.sum((has_covid == 1) & (test_results == 1))
false_positives = np.sum((has_covid == 0) & (test_results == 1))  # Type I
true_negatives = np.sum((has_covid == 0) & (test_results == 0))
false_negatives = np.sum((has_covid == 1) & (test_results == 0))  # Type II

print(f"\n📊 Simulation Results (n={n_tests}):")
print(f"✅ True Positives: {true_positives}")
print(f"❌ False Positives (Type I): {false_positives}")
print(f"✅ True Negatives: {true_negatives}")
print(f"❌ False Negatives (Type II): {false_negatives}")
print(f"\nType I Error Rate (α): {false_positives/(false_positives + true_negatives):.3f}")
print(f"Type II Error Rate (β): {false_negatives/(false_negatives + true_positives):.3f}")
```

---

## 🎮 Practice Exercises

### 📝 Exercise 1: Confidence Interval

**Problem:** A coffee shop wants to estimate the average amount customers spend. They sample 50 customers and find:
- Sample mean = $8.50
- Sample std = $2.00

Calculate the 95% confidence interval for the population mean.

<details>
<summary>💡 Click for solution</summary>

```python
n = 50
sample_mean = 8.50
sample_std = 2.00
confidence = 0.95

z_star = stats.norm.ppf((1 + confidence) / 2)
se = sample_std / np.sqrt(n)
margin_error = z_star * se

ci_lower = sample_mean - margin_error
ci_upper = sample_mean + margin_error

print(f"95% CI: (${ci_lower:.2f}, ${ci_upper:.2f})")
```
</details>

---

### 📝 Exercise 2: Hypothesis Test (Critical Value)

**Problem:** A factory claims light bulbs last 1000 hours on average. You test 36 bulbs:
- Sample mean = 980 hours
- Sample std = 60 hours

Test at α = 0.05 if the claim is false.

<details>
<summary>💡 Click for solution</summary>

```python
# H₀: μ = 1000
# H₁: μ ≠ 1000 (two-tailed)

mu_0 = 1000
x_bar = 980
s = 60
n = 36
alpha = 0.05

z_critical = stats.norm.ppf(1 - alpha/2)
se = s / np.sqrt(n)
z_stat = (x_bar - mu_0) / se

print(f"Z-statistic: {z_stat:.3f}")
print(f"Critical value: ±{z_critical:.3f}")

if abs(z_stat) > z_critical:
    print("Reject H₀: Bulbs don't last 1000 hours")
else:
    print("Fail to reject H₀")
```
</details>

---

### 📝 Exercise 3: p-value Method

**Problem:** A school claims average SAT score is 1200. Sample of 40 students shows mean = 1230, std = 100. Test at α = 0.05.

<details>
<summary>💡 Click for solution</summary>

```python
mu_0 = 1200
x_bar = 1230
s = 100
n = 40
alpha = 0.05

se = s / np.sqrt(n)
z_stat = (x_bar - mu_0) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

print(f"Z-statistic: {z_stat:.3f}")
print(f"p-value: {p_value:.4f}")

if p_value < alpha:
    print("Reject H₀: Average is different from 1200")
else:
    print("Fail to reject H₀")
```
</details>

---

## 🌟 Key Takeaways

<div class="mermaid">
mindmap
  root((Inferential<br/>Statistics))
    Sampling
      Represents population
      Saves time & money
      Must be random
    CLT
      Sample means → Normal
      Works for n > 30
      Enables predictions
    Confidence Intervals
      Range for true value
      95% most common
      Wider = more confident
    Hypothesis Testing
      Test claims
      Two methods available
      Control error rates
    Errors
      Type I: False alarm
      Type II: Missed detection
      Trade-off exists
</div>

### 🎊 Remember

1. **Samples represent populations** - Choose wisely!
2. **CLT is magic** - Sample means become normal
3. **Confidence intervals** - Give range, not exact value
4. **p-value < 0.05** - Usually means significant
5. **Errors happen** - Understand Type I and Type II
6. **Context matters** - Always interpret results practically!

---

## 📚 Glossary

- **Population (N)**: Everyone or everything we're studying
- **Sample (n)**: Subset we actually measure
- **μ (mu)**: Population mean (true average)
- **X̄ (x-bar)**: Sample mean (our estimate)
- **σ (sigma)**: Population standard deviation
- **s**: Sample standard deviation
- **SE**: Standard Error = σ/√n
- **α (alpha)**: Significance level (usually 0.05)
- **β (beta)**: Type II error rate
- **p-value**: Probability of result if H₀ is true
- **CI**: Confidence Interval
- **H₀**: Null hypothesis (status quo)
- **H₁**: Alternative hypothesis (what we test)

---

## 💻 Hands-On Practice

**Ready to see inferential statistics in action with real data?**

Check out the **[Jupyter Notebook with Inferential Statistics Examples]({{ site.baseurl }}/notebooks/statistics/chapter2_inferential_statistics_examples.ipynb)** using the Penguins dataset!

**What's included:**
- ✅ Population vs sample demonstrations
- ✅ Real dataset (333 Antarctic penguins)
- ✅ Central Limit Theorem visualization
- ✅ Confidence interval calculations (multiple sample sizes)
- ✅ Standard error and margin of error examples
- ✅ Species comparison (Adelie vs Gentoo)
- ✅ Effect of sample size on precision

**To run the notebook:**
1. Install: `pip install pandas numpy matplotlib seaborn scipy jupyter`
2. Download the notebook from the repository
3. Run: `jupyter notebook chapter2_inferential_statistics_examples.ipynb`

📖 See the [notebooks README]({{ site.baseurl }}/notebooks/statistics/README.md) for full instructions!

---

*Made with ❤️ for curious learners who want to make smart decisions with data!*
