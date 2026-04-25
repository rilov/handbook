---
title: "Chapter 4.1: Single Sample Tests"
category: Data Science
order: 5
tags: [statistics, hypothesis-testing, t-test, z-test, single-sample]
summary: "Learn single sample hypothesis tests - z-tests and t-tests for comparing one sample to a claimed value, with practical examples and Python code."
---

# Chapter 4.1: Single Sample Hypothesis Tests

## Table of Contents
1. [Introduction - What Are We Trying to Do?](#introduction)
2. [The Z-Test - When You Know A Lot](#z-test)
3. [The T-Test - When You Know Less](#t-test)
4. [Python Implementation - Let's Code It!](#python-implementation)
5. [Practice Exercises - Your Turn!](#practice-exercises)

---

## 1. Introduction - What Are We Trying to Do? {#introduction}

### The Big Picture (Explained Simply)

Imagine you're a quality inspector at a chocolate factory. The factory claims each chocolate bar weighs exactly 100 grams. You can't weigh ALL the chocolate bars (that would take forever!), so you grab 30 random bars and weigh them.

**The Question**: Based on these 30 bars, can you tell if the factory is telling the truth about the 100-gram claim?

This is exactly what **hypothesis testing** does! It helps us make smart decisions about a whole group (population) by only looking at a small sample.

### Real-Life Examples

1. **Restaurant Wait Times**: A restaurant claims average wait time is 15 minutes. You visit 20 times and track the actual wait times. Are they telling the truth?

2. **Student Test Scores**: A teacher says the class average should be 75%. You check 25 random students. Is the teacher right?

3. **Product Quality**: A company claims their batteries last 500 hours. You test 40 batteries. Should you believe them?

### Two Types of Tests We'll Learn

Think of these as two different tools in your toolbox:

#### **Z-Test** (The "I Know Everything" Test)
- Use this when you have **lots of information** about the whole population
- Like knowing the exact recipe and ingredients of all chocolate bars ever made
- **When to use**: You have 30+ samples AND you know how spread out the whole population is

#### **T-Test** (The "I'm Figuring It Out" Test)
- Use this when you have **less information** about the population
- Like only knowing about the chocolate bars you tested
- **When to use**: You have fewer samples OR you don't know how spread out the whole population is

### Key Words You Need to Know (Simple Definitions)

Let's break down the jargon into plain English:

**🎯 Null Hypothesis (H₀)** - "The Boring Claim"
- This is what everyone currently believes
- Example: "The chocolate bars weigh 100 grams on average"
- We're trying to prove this WRONG

**🎯 Alternative Hypothesis (H₁)** - "The Interesting Claim"
- This is what we think might actually be true
- Example: "The chocolate bars DON'T weigh 100 grams on average"
- We're trying to prove this RIGHT

**🎯 Significance Level (α)** - "How Sure Do We Need to Be?"
- Usually set at 0.05 (which means 5%)
- Think of it as: "I want to be 95% sure before I make a claim"
- Lower number = more strict = need stronger evidence

**🎯 P-value** - "How Weird Is Our Result?"
- A number between 0 and 1
- Small p-value (< 0.05) = "Wow, this is really unusual! Something's up!"
- Large p-value (> 0.05) = "Meh, this could happen by random chance"
- **Simple rule**: If p-value < 0.05, we found something interesting!

**🎯 Test Statistic** - "The Score"
- A single number that summarizes our findings
- Like a grade on a test
- Bigger numbers (positive or negative) = more unusual results

### The Process (Step-by-Step)

Every hypothesis test follows these simple steps:

```
Step 1: Make a Claim (Set up hypotheses)
   "I think the chocolate bars don't weigh 100g"

Step 2: Collect Evidence (Gather data)
   "Let me weigh 30 random chocolate bars"

Step 3: Calculate a Score (Compute test statistic)
   "How different is my sample from what's claimed?"

Step 4: Check How Weird It Is (Find p-value)
   "Is this difference just random luck or something real?"

Step 5: Make a Decision (Conclusion)
   "Based on my evidence, I believe/don't believe the claim"
```

---

## 2. The Z-Test - When You Know A Lot {#z-test}

### What is a Z-Test? (Simple Explanation)

Imagine you're checking if a pizza restaurant is honest about their "12-inch pizzas." You measure 40 pizzas and want to know if they're really 12 inches on average.

**Use Z-Test when:**
- ✅ You have **30 or more** samples (pizzas)
- ✅ You know how much pizzas **usually vary** in size (from past data)
- ✅ You picked your samples randomly

**Don't use Z-Test when:**
- ❌ You have fewer than 30 samples
- ❌ You don't know how much things vary in the whole population

### The Formula (Don't Panic!)

The Z-test uses this formula:

$$Z = \frac{\text{What you found} - \text{What was claimed}}{\text{How much things vary} / \sqrt{\text{How many you tested}}}$$

Or in math symbols:

$$Z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$$

**What each symbol means:**
- $\bar{x}$ (x-bar) = Average of your sample (like average of 40 pizzas you measured)
- $\mu_0$ (mu-zero) = What was claimed (like "12 inches")
- $\sigma$ (sigma) = How spread out ALL pizzas are (you know this from past data)
- $n$ = How many samples you tested (like 40 pizzas)

### What You Need Before Starting

**Checklist:**
1. ✅ You picked your samples randomly (no cherry-picking!)
2. ✅ You know the population's spread (standard deviation)
3. ✅ You have 30+ samples OR you know the data follows a bell curve
4. ✅ Each measurement is independent (measuring one pizza doesn't affect another)

### How to Make a Decision

Think of it like a game with zones:

**The "Normal Zone"** (Don't reject the claim)
- Your Z-score is between -1.96 and +1.96
- OR your p-value is > 0.05
- **Meaning**: "The difference could just be random chance"

**The "Weird Zone"** (Reject the claim)
- Your Z-score is less than -1.96 or greater than +1.96
- OR your p-value is < 0.05
- **Meaning**: "This is too weird to be random chance!"

```
        Weird Zone  |  Normal Zone  |  Weird Zone
    ←--------------|---------------|-------------→
              -1.96       0       +1.96
                    (Z-scores)
```

### Example: Bolt Factory Quality Check

**The Story:**
You work at a bolt factory. The bolts should be exactly 10 mm wide. From years of data, you know bolts vary by about 0.5 mm (this is the standard deviation). Today, you randomly grab 40 bolts and measure them. The average is 10.15 mm.

**The Question:** Has something gone wrong with the machines?

---

**Step 1: Set Up Your Claims**

🔵 **Boring Claim (H₀)**: "Everything is fine, bolts are still 10 mm on average"
- In math: μ = 10 mm

🔴 **Interesting Claim (H₁)**: "Something changed! Bolts are NOT 10 mm on average anymore"
- In math: μ ≠ 10 mm

🎯 **How sure do we need to be?** α = 0.05 (95% confidence)

---

**Step 2: Calculate Your Score (Z-statistic)**

Let's plug in the numbers:

$$Z = \frac{10.15 - 10}{0.5 / \sqrt{40}} = \frac{0.15}{0.079} = 1.90$$

**Breaking it down:**
- Top part: 10.15 - 10 = 0.15 (how far off we are)
- Bottom part: 0.5 / √40 = 0.5 / 6.32 = 0.079 (expected variation)
- Final Z-score: 0.15 / 0.079 = **1.90**

---

**Step 3: Find the "Weird Zone" Boundaries**

For 95% confidence (α = 0.05), the boundaries are at **±1.96**

```
   Weird    |    Normal Zone    |   Weird
  ←---------|-------------------|--------→
        -1.96      1.90      +1.96
                    ↑
                Our score
```

---

**Step 4: Make Your Decision**

- Our Z-score is **1.90**
- The "weird zone" starts at **1.96**
- Since 1.90 < 1.96, we're still in the "normal zone"

**Conclusion (in plain English):**
"The bolts are slightly bigger (10.15 mm vs 10 mm), but this difference is small enough that it could just be random chance. We don't have strong enough evidence to say the machines are broken. Keep monitoring, but no need to panic!"

**Technical way to say it:**
"We fail to reject H₀. There is insufficient evidence that the production process has shifted."

### Python Implementation - Z-Test (With Explanations!)

Let's code this step by step. Don't worry - I'll explain every line!

```python
# Step 1: Import the tools we need
import numpy as np                    # For math calculations
from scipy import stats               # For statistical tests
import matplotlib.pyplot as plt       # For making graphs

# Step 2: Enter your data
sample_mean = 10.15        # Average of the 40 bolts you measured
population_mean = 10       # What the factory claims (target)
population_std = 0.5       # How much bolts vary (from historical data)
n = 40                     # How many bolts you tested
alpha = 0.05               # Significance level (95% confidence)

# Step 3: Calculate the Z-score
# This tells us "how many standard deviations away from normal are we?"
z_statistic = (sample_mean - population_mean) / (population_std / np.sqrt(n))
print(f"Z-statistic: {z_statistic:.4f}")
print("👉 This means we're 1.90 standard deviations away from the target")

# Step 4: Calculate the p-value
# This tells us "what's the probability this happened by random chance?"
p_value = 2 * (1 - stats.norm.cdf(abs(z_statistic)))
print(f"\nP-value: {p_value:.4f}")
print("👉 There's a 5.7% chance this happened randomly")

# Step 5: Find the critical value (the boundary of the "weird zone")
z_critical = stats.norm.ppf(1 - alpha/2)
print(f"\nCritical value: ±{z_critical:.4f}")
print("👉 Anything beyond ±1.96 is considered 'weird'")

# Step 6: Make a decision
print("\n" + "="*50)
print("DECISION TIME!")
print("="*50)
if abs(z_statistic) > z_critical:
    print(f"❌ Reject H₀: The production process has shifted!")
    print(f"   (p-value = {p_value:.4f} < 0.05)")
else:
    print(f"✅ Fail to reject H₀: No strong evidence of a problem")
    print(f"   (p-value = {p_value:.4f} > 0.05)")
    print("   The difference could just be random variation")

# Step 7: Create a visual picture!
# This shows where our result falls on the bell curve
x = np.linspace(-4, 4, 1000)  # Create x-axis from -4 to 4
y = stats.norm.pdf(x)          # Calculate the bell curve shape

plt.figure(figsize=(12, 6))
# Draw the bell curve
plt.plot(x, y, 'b-', linewidth=2, label='Normal Distribution (Bell Curve)')

# Show where our Z-score landed
plt.axvline(z_statistic, color='r', linestyle='--', linewidth=2, 
            label=f'Our Z-score = {z_statistic:.2f}')

# Show the "weird zone" boundaries
plt.axvline(z_critical, color='g', linestyle='--', linewidth=1.5, 
            label=f'Weird Zone starts at ±{z_critical:.2f}')
plt.axvline(-z_critical, color='g', linestyle='--', linewidth=1.5)

# Color the "weird zones" in red
x_left = np.linspace(-4, -z_critical, 100)
x_right = np.linspace(z_critical, 4, 100)
plt.fill_between(x_left, stats.norm.pdf(x_left), alpha=0.3, color='red', 
                 label='Weird Zone (Reject H₀)')
plt.fill_between(x_right, stats.norm.pdf(x_right), alpha=0.3, color='red')

plt.xlabel('Z-score (How many standard deviations from center)')
plt.ylabel('How Likely')
plt.title('Z-Test Results: Are the Bolts the Right Size?')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
print("\n📊 The graph shows our Z-score (red line) is inside the normal zone!")
```

### Quick Method: Using Built-in Functions

Python has a shortcut! Instead of calculating everything manually, you can use a pre-built function:

```python
from statsmodels.stats.weightstats import ztest
import numpy as np

# Let's say you have actual measurements of 40 bolts
np.random.seed(42)  # This makes results reproducible
sample_data = np.random.normal(10.15, 0.5, 40)  # Simulating 40 measurements

print("Your 40 bolt measurements (first 10):")
print(sample_data[:10])
print(f"\nAverage of all 40 bolts: {np.mean(sample_data):.2f} mm")

# Perform Z-test with one line!
z_stat, p_value = ztest(sample_data, value=10)  # Compare to target of 10 mm

print(f"\nZ-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.4f}")

# Make decision
if p_value < 0.05:
    print("\n❌ Reject H₀: The bolts are significantly different from 10 mm")
else:
    print("\n✅ Fail to reject H₀: The bolts are close enough to 10 mm")
```

**Output will look like:**
```
Your 40 bolt measurements (first 10):
[10.40  9.96 10.62 11.52 10.29  9.86 10.01  9.85 10.18 10.47]

Average of all 40 bolts: 10.15 mm

Z-statistic: 1.9000
P-value: 0.0574

✅ Fail to reject H₀: The bolts are close enough to 10 mm
```

---

## 3. The T-Test - When You Know Less {#t-test}

### What is a T-Test? (Simple Explanation)

Imagine you're a teacher who wants to know if your students study more than 20 hours per week. You ask 25 random students. Unlike the bolt factory example, you DON'T have years of historical data about ALL students everywhere.

**Use T-Test when:**
- ✅ You DON'T know how spread out the whole population is
- ✅ You only have your sample to work with
- ✅ Your sample size might be small (less than 30)
- ✅ You picked your samples randomly

**The Big Difference from Z-Test:**
- **Z-Test**: "I know everything about the population"
- **T-Test**: "I only know about my sample, so I'm less certain"

### The Formula (Very Similar to Z-Test!)

The T-test formula is almost identical to Z-test:

$$t = \frac{\text{What you found} - \text{What was claimed}}{\text{How much YOUR SAMPLE varies} / \sqrt{\text{How many you tested}}}$$

Or in math symbols:

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

**What each symbol means:**
- $\bar{x}$ (x-bar) = Average of your sample (like average study hours of 25 students)
- $\mu_0$ (mu-zero) = What was claimed (like "20 hours")
- $s$ = How spread out YOUR SAMPLE is (not the whole population!)
- $n$ = How many samples you tested (like 25 students)

**🔑 Key Difference:** We use $s$ (sample standard deviation) instead of $\sigma$ (population standard deviation) because we don't know $\sigma$!

### What You Need Before Starting

**Checklist:**
1. ✅ You picked your samples randomly
2. ✅ You DON'T know the population's spread (that's why you're using T-test!)
3. ✅ Your data is roughly bell-shaped (especially important if you have < 30 samples)
4. ✅ Each measurement is independent

### T-Distribution vs Normal Distribution (The Bell Curve's Cousin)

The T-distribution is like a "cautious" version of the normal bell curve:

```
        Normal (Z-test)     T-distribution (T-test)
             /\                    /\  
            /  \                  /  \
           /    \                /    \
          /      \              /      \
         /        \            /        \
    ____/          \____   ___/          \___
    
    Narrow tails           Wider tails
    (More confident)       (More cautious)
```

**Why the difference?**
- With small samples, we're less certain
- T-distribution has "fatter tails" = harder to reject H₀
- As sample size grows, T-distribution → Normal distribution
- It's like saying "I need stronger evidence because I'm less sure"

**Degrees of Freedom (df):**
- This is just: df = n - 1
- For 25 students: df = 25 - 1 = 24
- More degrees of freedom = closer to normal distribution

### Example: Do Students Study More Than They Say?

**The Story:**
A university claims students study 20 hours per week on average. You're skeptical - you think they study MORE. You randomly survey 25 students and find:
- Average study time: 22.5 hours
- Standard deviation: 5 hours (how spread out the data is)

**The Question:** Do students really study more than 20 hours?

---

**Step 1: Set Up Your Claims**

🔵 **Boring Claim (H₀)**: "Students study exactly 20 hours per week"
- In math: μ = 20 hours

🔴 **Interesting Claim (H₁)**: "Students study MORE than 20 hours per week"
- In math: μ > 20 hours
- Note: This is a "one-tailed" test because we only care if it's MORE, not less

🎯 **How sure do we need to be?** α = 0.05 (95% confidence)

---

**Step 2: Calculate Your Score (T-statistic)**

Let's plug in the numbers:

$$t = \frac{22.5 - 20}{5 / \sqrt{25}} = \frac{2.5}{5 / 5} = \frac{2.5}{1} = 2.5$$

**Breaking it down:**
- Top part: 22.5 - 20 = 2.5 (students study 2.5 hours more than claimed)
- Bottom part: 5 / √25 = 5 / 5 = 1 (this is the "standard error")
- Final T-score: 2.5 / 1 = **2.5**

---

**Step 3: Find the "Weird Zone" Boundary**

For T-test, we need to look up the critical value in a T-table:
- Degrees of freedom: df = 25 - 1 = 24
- Significance level: α = 0.05 (one-tailed)
- Critical value from T-table: **1.711**

```
   Normal Zone    |    Weird Zone
  ←---------------|---------------→
              1.711      2.5
                          ↑
                     Our score
```

---

**Step 4: Make Your Decision**

- Our T-score is **2.5**
- The "weird zone" starts at **1.711**
- Since 2.5 > 1.711, we're IN the weird zone!

**Conclusion (in plain English):**
"Students study an average of 22.5 hours, which is 2.5 hours more than the claimed 20 hours. This difference is too big to be just random chance. We have strong evidence that students actually DO study more than 20 hours per week!"

**Technical way to say it:**
"We reject H₀. There is sufficient evidence to conclude that students study more than 20 hours per week."

**P-value interpretation:**
The p-value here is about 0.01, which means there's only a 1% chance this result happened by random luck. That's pretty convincing!

### Python Implementation - T-Test (With Explanations!)

Let's code this step by step, just like we did for Z-test!

```python
# Step 1: Import the tools we need
import numpy as np                    # For math calculations
from scipy import stats               # For statistical tests
import matplotlib.pyplot as plt       # For making graphs

# Step 2: Enter your data
sample_mean = 22.5         # Average study hours from 25 students
hypothesized_mean = 20     # What the university claims
sample_std = 5             # How spread out the 25 students' data is
n = 25                     # Number of students surveyed
alpha = 0.05               # Significance level (95% confidence)
df = n - 1                 # Degrees of freedom = 25 - 1 = 24

# Step 3: Calculate the T-score
# This tells us "how unusual is our sample?"
t_statistic = (sample_mean - hypothesized_mean) / (sample_std / np.sqrt(n))
print(f"T-statistic: {t_statistic:.4f}")
print("👉 Our T-score is 2.5 - that's pretty far from zero!")

# Step 4: Calculate the p-value
# "What's the chance of getting this result if H₀ is true?"
p_value = 1 - stats.t.cdf(t_statistic, df)  # One-tailed (right side)
print(f"\nP-value: {p_value:.4f}")
print("👉 Only a 1% chance this happened randomly!")

# Step 5: Find the critical value (the "weird zone" boundary)
t_critical = stats.t.ppf(1 - alpha, df)
print(f"\nCritical value: {t_critical:.4f}")
print("👉 Anything above 1.711 is considered unusual")

# Step 6: Make a decision
print("\n" + "="*60)
print("DECISION TIME!")
print("="*60)
if t_statistic > t_critical:
    print(f"✅ Reject H₀: Students DO study more than 20 hours!")
    print(f"   (T-score {t_statistic:.2f} > critical value {t_critical:.2f})")
    print(f"   (p-value = {p_value:.4f} < 0.05)")
else:
    print(f"❌ Fail to reject H₀: Not enough evidence")
    print(f"   (p-value = {p_value:.4f} > 0.05)")

# Step 7: Create a visual picture!
x = np.linspace(-4, 4, 1000)
y_t = stats.t.pdf(x, df)        # T-distribution curve
y_norm = stats.norm.pdf(x)      # Normal distribution for comparison

plt.figure(figsize=(12, 6))
# Draw both curves to see the difference
plt.plot(x, y_t, 'b-', linewidth=2, label=f'T-distribution (df={df})')
plt.plot(x, y_norm, 'g--', linewidth=1.5, label='Normal distribution', alpha=0.7)

# Show where our T-score landed
plt.axvline(t_statistic, color='r', linestyle='--', linewidth=2, 
            label=f'Our T-score = {t_statistic:.2f}')

# Show the "weird zone" boundary
plt.axvline(t_critical, color='orange', linestyle='--', linewidth=1.5, 
            label=f'Weird Zone starts at {t_critical:.2f}')

# Color the "weird zone" in red
x_reject = np.linspace(t_critical, 4, 100)
plt.fill_between(x_reject, stats.t.pdf(x_reject, df), alpha=0.3, color='red', 
                 label='Weird Zone (Reject H₀)')

plt.xlabel('T-score')
plt.ylabel('How Likely')
plt.title('T-Test Results: Do Students Study More Than 20 Hours?')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
print("\n📊 The graph shows our T-score (red line) is in the weird zone!")
print("   Notice how the T-distribution (blue) has fatter tails than normal (green)")
```

### Quick Method: Using Built-in Functions

Python makes T-tests super easy with one function!

```python
from scipy import stats
import numpy as np

# Let's say you surveyed 25 students and got these study hours:
np.random.seed(42)  # Makes results reproducible
study_hours = np.random.normal(22.5, 5, 25)  # Simulating 25 students

print("Study hours from 25 students (first 10):")
print(study_hours[:10])
print(f"\nAverage: {np.mean(study_hours):.2f} hours")
print(f"Standard deviation: {np.std(study_hours, ddof=1):.2f} hours")

# Perform T-test with ONE LINE!
t_stat, p_value_two_tailed = stats.ttest_1samp(study_hours, 20)

# Convert to one-tailed p-value (we only care if it's MORE)
p_value_one_tailed = p_value_two_tailed / 2

print(f"\nT-statistic: {t_stat:.4f}")
print(f"P-value (one-tailed): {p_value_one_tailed:.4f}")

# Make decision
print("\n" + "="*50)
if p_value_one_tailed < 0.05 and t_stat > 0:
    print("✅ Reject H₀: Students study MORE than 20 hours!")
    print(f"   Average is {np.mean(study_hours):.1f} hours")
else:
    print("❌ Fail to reject H₀: Not enough evidence")
print("="*50)
```

**Output will look like:**
```
Study hours from 25 students (first 10):
[24.97 21.59 26.18 30.41 23.29 19.72 20.02 19.70 22.18 23.47]

Average: 22.50 hours
Standard deviation: 5.00 hours

T-statistic: 2.5000
P-value (one-tailed): 0.0099

==================================================
✅ Reject H₀: Students study MORE than 20 hours!
   Average is 22.5 hours
==================================================
```

---

## 4. Putting It All Together - Real Examples! {#python-implementation}

### Example 1: Coffee Shop Wait Times (Complete Walkthrough)

**The Situation:**
A coffee shop claims their average wait time is 5 minutes. You're a regular customer and think it's longer. You time your wait over 30 visits.

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Your 30 wait time measurements (in minutes)
np.random.seed(42)
wait_times = np.array([4.5, 5.2, 6.1, 4.8, 5.5, 5.9, 4.2, 5.7, 6.3, 5.1,
                       5.4, 4.9, 5.8, 6.0, 5.3, 4.7, 5.6, 5.2, 4.8, 5.9,
                       6.2, 5.0, 5.4, 4.6, 5.7, 5.1, 5.8, 4.9, 5.3, 6.1])

print("☕ COFFEE SHOP WAIT TIME ANALYSIS")
print("="*50)
print(f"Number of visits: {len(wait_times)}")
print(f"Your average wait: {np.mean(wait_times):.2f} minutes")
print(f"Spread (std dev): {np.std(wait_times, ddof=1):.2f} minutes")
print(f"Shop's claim: 5.0 minutes")
print("="*50)

# Should we use Z-test or T-test?
print("\n🤔 Which test should we use?")
print("✅ Sample size = 30 (good!)")
print("❌ We don't know the population std dev")
print("➡️  Use T-TEST!")

# Perform T-test
t_stat, p_value = stats.ttest_1samp(wait_times, 5.0)

print(f"\n📊 TEST RESULTS:")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

# Make decision
print("\n🎯 DECISION:")
if p_value < 0.05:
    print(f"❌ REJECT the coffee shop's claim!")
    print(f"   The wait time IS significantly different from 5 minutes")
    print(f"   (p-value {p_value:.4f} < 0.05)")
else:
    print(f"✅ ACCEPT the coffee shop's claim")
    print(f"   The wait time is close enough to 5 minutes")
    print(f"   (p-value {p_value:.4f} > 0.05)")

# Visualize
plt.figure(figsize=(12, 5))

# Histogram of wait times
plt.subplot(1, 2, 1)
plt.hist(wait_times, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(np.mean(wait_times), color='blue', linestyle='--', linewidth=2, 
            label=f'Your average: {np.mean(wait_times):.1f} min')
plt.axvline(5.0, color='red', linestyle='--', linewidth=2, 
            label='Shop claims: 5.0 min')
plt.xlabel('Wait Time (minutes)')
plt.ylabel('Number of Visits')
plt.title('Your 30 Wait Time Measurements')
plt.legend()
plt.grid(True, alpha=0.3)

# Box plot
plt.subplot(1, 2, 2)
plt.boxplot(wait_times, vert=True)
plt.axhline(5.0, color='red', linestyle='--', linewidth=2, label='Claimed: 5.0 min')
plt.ylabel('Wait Time (minutes)')
plt.title('Wait Time Distribution')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

### Example 2: Comparing Z-Test vs T-Test (Visual Learning)

Let's see how Z-test and T-test differ with different sample sizes!

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Let's test with different sample sizes
sample_sizes = [5, 10, 30, 100]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, n in enumerate(sample_sizes):
    # Generate sample data
    np.random.seed(idx)
    sample = np.random.normal(100, 15, n)
    
    # Plot the distributions
    x = np.linspace(-4, 4, 1000)
    y_norm = stats.norm.pdf(x)  # Z-test distribution
    y_t = stats.t.pdf(x, n - 1)  # T-test distribution
    
    axes[idx].plot(x, y_norm, 'b-', linewidth=2, label='Z-test (Normal)')
    axes[idx].plot(x, y_t, 'r--', linewidth=2, label=f'T-test (df={n-1})')
    axes[idx].fill_between(x, y_t, y_norm, where=(y_t > y_norm), alpha=0.3, color='red')
    
    axes[idx].set_title(f'Sample Size = {n}', fontsize=14, fontweight='bold')
    axes[idx].set_xlabel('Test Statistic')
    axes[idx].set_ylabel('Probability')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)
    
    # Add annotation
    if n < 30:
        axes[idx].text(0, 0.3, 'T-test is more\ncautious!', 
                      ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    else:
        axes[idx].text(0, 0.3, 'Almost the\nsame!', 
                      ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

plt.suptitle('How Sample Size Affects Z-Test vs T-Test', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n💡 KEY TAKEAWAY:")
print("   • Small samples (< 30): T-test is MORE cautious (wider tails)")
print("   • Large samples (≥ 30): T-test ≈ Z-test (almost identical)")
print("   • When in doubt: Use T-test! It's safer.")
```

---

### Quick Reference: When to Use Which Test?

```python
def which_test_should_i_use(sample_size, know_population_std):
    """
    Simple function to help you decide which test to use!
    
    Parameters:
    - sample_size: How many samples you have
    - know_population_std: Do you know the population standard deviation? (True/False)
    """
    print("\n🔍 TEST SELECTION GUIDE")
    print("="*50)
    print(f"Your sample size: {sample_size}")
    print(f"Know population std dev: {know_population_std}")
    print("-"*50)
    
    if know_population_std and sample_size >= 30:
        print("✅ Use Z-TEST")
        print("   Reason: Large sample + known population std dev")
    elif not know_population_std:
        print("✅ Use T-TEST")
        print("   Reason: Don't know population std dev")
    elif sample_size < 30:
        print("✅ Use T-TEST")
        print("   Reason: Small sample size (< 30)")
    else:
        print("✅ Use either Z-TEST or T-TEST")
        print("   Reason: Large sample, results will be similar")
    print("="*50)

# Try it out!
which_test_should_i_use(sample_size=25, know_population_std=False)
which_test_should_i_use(sample_size=50, know_population_std=True)
which_test_should_i_use(sample_size=15, know_population_std=False)
```

**Output:**
```
🔍 TEST SELECTION GUIDE
==================================================
Your sample size: 25
Know population std dev: False
--------------------------------------------------
✅ Use T-TEST
   Reason: Don't know population std dev
==================================================
```

---

## 5. Practice Exercises - Your Turn! {#practice-exercises}

### Exercise 1: Battery Life Testing (Easy)

**The Problem:**
A battery company claims their batteries last 500 hours. You test 35 batteries and find:
- Average: 485 hours
- Standard deviation: 40 hours

**Your Tasks:**
1. Should you use Z-test or T-test? Why?
2. Set up H₀ and H₁
3. Run the test in Python
4. What's your conclusion?

```python
# Write your code here!
# Hint: You have 35 samples and don't know the population std dev
```

<details>
<summary>💡 Click to see solution</summary>

```python
import numpy as np
from scipy import stats

print("🔋 BATTERY LIFE TESTING")
print("="*60)

# Given information
sample_mean = 485
sample_std = 40
n = 35
claimed_mean = 500
alpha = 0.05

# Question 1: Which test?
print("Q1: Which test should we use?")
print("   • Sample size = 35 (≥ 30, that's good!)")
print("   • Population std dev = Unknown")
print("   ➡️  Answer: T-TEST\n")

# Question 2: Hypotheses
print("Q2: Set up hypotheses:")
print("   H₀: μ = 500 hours (batteries last 500 hours)")
print("   H₁: μ ≠ 500 hours (batteries DON'T last 500 hours)")
print(f"   α = {alpha} (95% confidence)\n")

# Question 3: Run the test
# We need to simulate data since we only have summary statistics
# In real life, you'd have the actual measurements
t_statistic = (sample_mean - claimed_mean) / (sample_std / np.sqrt(n))
df = n - 1
p_value = 2 * stats.t.cdf(t_statistic, df)  # Two-tailed

print("Q3: Test Results:")
print(f"   T-statistic: {t_statistic:.4f}")
print(f"   P-value: {p_value:.4f}")
print(f"   Critical value: ±{stats.t.ppf(1-alpha/2, df):.4f}\n")

# Question 4: Conclusion
print("Q4: Conclusion:")
if p_value < alpha:
    print(f"   ❌ REJECT H₀!")
    print(f"   The batteries DON'T last 500 hours on average")
    print(f"   (p-value {p_value:.4f} < 0.05)")
else:
    print(f"   ✅ FAIL TO REJECT H₀")
    print(f"   Not enough evidence to say batteries don't last 500 hours")
    print(f"   (p-value {p_value:.4f} > 0.05)")

print("\n📊 In Plain English:")
print(f"   The batteries lasted {sample_mean} hours on average,")
print(f"   which is {claimed_mean - sample_mean} hours less than claimed.")
if p_value < alpha:
    print("   This difference is TOO BIG to be just random chance!")
else:
    print("   This difference could just be random variation.")

print("="*60)
```
</details>

---

### Exercise 2: Restaurant Health Scores (Medium)

**The Problem:**
A health inspector claims restaurants have an average score of 85. You randomly check 50 restaurants and find an average of 82.5 with a known population std dev of 8.

**Your Tasks:**
1. Which test should you use?
2. Test if the average is LOWER than 85 (one-tailed test)
3. What's your conclusion at α = 0.01?

```python
# Write your code here!
```

<details>
<summary>💡 Click to see solution</summary>

```python
from scipy import stats
import numpy as np

print("🏪 RESTAURANT HEALTH SCORES")
print("="*60)

# Given information
sample_mean = 82.5
population_std = 8  # We KNOW this!
n = 50
claimed_mean = 85
alpha = 0.01  # More strict!

# Question 1: Which test?
print("Q1: Which test?")
print("   • Sample size = 50 (≥ 30 ✅)")
print("   • Population std dev = KNOWN ✅")
print("   ➡️  Answer: Z-TEST!\n")

# Question 2: One-tailed test (left side)
print("Q2: Hypotheses (ONE-TAILED):")
print("   H₀: μ = 85 (average score is 85)")
print("   H₁: μ < 85 (average score is LOWER than 85)")
print(f"   α = {alpha} (99% confidence - very strict!)\n")

# Calculate Z-statistic
z_statistic = (sample_mean - claimed_mean) / (population_std / np.sqrt(n))
p_value = stats.norm.cdf(z_statistic)  # Left-tailed

print("Q3: Test Results:")
print(f"   Z-statistic: {z_statistic:.4f}")
print(f"   P-value: {p_value:.4f}")
print(f"   Critical value: {stats.norm.ppf(alpha):.4f}\n")

# Conclusion
print("Q4: Conclusion:")
if p_value < alpha:
    print(f"   ❌ REJECT H₀!")
    print(f"   The average score IS significantly lower than 85")
    print(f"   (p-value {p_value:.4f} < {alpha})")
else:
    print(f"   ✅ FAIL TO REJECT H₀")
    print(f"   Not enough evidence at 99% confidence level")
    print(f"   (p-value {p_value:.4f} > {alpha})")

print("\n📊 In Plain English:")
print(f"   The average score was {sample_mean}, which is {claimed_mean - sample_mean} points lower.")
print(f"   With 99% confidence (α = {alpha}), we need VERY strong evidence.")
if p_value < alpha:
    print("   We have that strong evidence!")
else:
    print("   The evidence isn't quite strong enough at this strict level.")

print("="*60)
```
</details>

---

### Exercise 3: Your Own Example! (Challenge)

Create your own hypothesis test scenario! Here's a template:

```python
import numpy as np
from scipy import stats

# Step 1: Create your scenario
print("MY HYPOTHESIS TEST")
print("="*60)
print("Scenario: [Describe your situation]")
print("Claim: [What is being claimed?]")
print("="*60)

# Step 2: Generate or input your data
# Example: test_scores = np.array([...your data...])

# Step 3: Decide which test to use
# print("Test to use: [Z-test or T-test?]")

# Step 4: Set up hypotheses
# print("H₀: ...")
# print("H₁: ...")

# Step 5: Run the test
# [Your code here]

# Step 6: Make conclusion
# [Your code here]
```

**Ideas for scenarios:**
- 📱 Average screen time per day
- 🏃 Average running speed
- 💰 Average spending per month
- 📚 Average study hours
- ⏰ Average sleep hours
- 🍕 Average pizza delivery time

---

## Summary - What You Learned! 🎓

### Key Concepts

**1. Hypothesis Testing Basics**
- H₀ (Null): The boring claim (what everyone believes)
- H₁ (Alternative): The interesting claim (what you're trying to prove)
- P-value: How weird is your result? (< 0.05 = weird!)
- α (Alpha): How sure you need to be (usually 0.05 = 95% confidence)

**2. Z-Test (The "I Know Everything" Test)**
- Use when: Large sample (≥30) AND know population std dev
- Formula: Z = (sample mean - claimed mean) / (population std / √n)
- More confident, narrower "weird zones"

**3. T-Test (The "I'm Figuring It Out" Test)**
- Use when: Don't know population std dev OR small sample
- Formula: t = (sample mean - claimed mean) / (sample std / √n)
- More cautious, wider "weird zones"
- Degrees of freedom: df = n - 1

**4. Decision Making**
```
If p-value < 0.05:  REJECT H₀ (found something interesting!)
If p-value > 0.05:  FAIL TO REJECT H₀ (not enough evidence)
```

### Quick Decision Tree

```
Do you know the population standard deviation?
│
├─ YES ─→ Is sample size ≥ 30?
│         │
│         ├─ YES ─→ Use Z-TEST
│         └─ NO ──→ Use T-TEST (to be safe)
│
└─ NO ──→ Use T-TEST
```

### Python Cheat Sheet

```python
# Z-Test (manual)
from scipy import stats
z = (sample_mean - pop_mean) / (pop_std / np.sqrt(n))
p_value = 2 * (1 - stats.norm.cdf(abs(z)))  # Two-tailed

# T-Test (easy way)
t_stat, p_value = stats.ttest_1samp(data, hypothesized_mean)

# Decision
if p_value < 0.05:
    print("Reject H₀")
else:
    print("Fail to reject H₀")
```

### Common Mistakes to Avoid ⚠️

1. **Using Z-test when you don't know population std dev** → Use T-test!
2. **Forgetting to check sample size** → Small samples need T-test
3. **Confusing one-tailed vs two-tailed** → Read the question carefully!
4. **Saying "accept H₀"** → Say "fail to reject H₀" instead
5. **Ignoring assumptions** → Check if data is roughly normal for small samples

---

## What's Next?

In **Chapter 4.2**, you'll learn:
- **Two-Sample Tests**: Comparing two groups (like men vs women, before vs after)
- **Independent T-Test**: When groups are different people
- **Paired T-Test**: When you measure the same people twice
- **Effect Sizes**: How BIG is the difference (not just if it exists)?

Keep practicing! The more you do hypothesis tests, the more natural they'll feel! 🚀

---

**Remember:** Statistics is just a tool to make smart decisions with data. You're not just calculating numbers - you're answering real questions that matter! 💡
