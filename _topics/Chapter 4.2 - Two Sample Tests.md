---
title: "Chapter 4.2: Two Sample Tests"
category: Data Science
order: 6
tags:
  - statistics
  - hypothesis-testing
  - t-test
  - two-sample
  - paired-test
summary: "Master two sample hypothesis tests - independent and paired t-tests for comparing two groups, with real-world examples and Python implementations."
---

# Chapter 4.2: Two Sample Hypothesis Tests

## Table of Contents
1. [Introduction - Comparing Two Groups](#introduction)
2. [Independent T-Test - Different Groups](#independent-test)
3. [Paired T-Test - Same Group, Two Times](#paired-test)
4. [Python Implementation - Let's Code It!](#python-implementation)
5. [Practice Exercises - Your Turn!](#practice-exercises)

---

## 1. Introduction - Comparing Two Groups {#introduction}

### The Big Picture (Explained Simply)

In Chapter 4.1, we compared ONE sample to a claimed value (like "Are these chocolate bars really 100g?"). Now we're going to compare TWO samples to each other!

**Real-Life Questions:**
- 💊 Does a new medicine work better than the old one?
- 👨👩 Do men and women have different average salaries?
- 📚 Did students improve after taking a course?
- ☕ Which coffee shop is faster - Starbucks or Dunkin'?

### Two Types of Comparisons

Think of it like comparing heights:

#### **Type 1: Independent Samples** (Different People)
- Compare men's heights vs women's heights
- Two completely different groups
- Like comparing apples to oranges (but both are fruits!)

#### **Type 2: Paired Samples** (Same People, Measured Twice)
- Measure people's weight before and after a diet
- Same group, measured at two different times
- Like comparing your height at age 10 vs age 20

```
Independent Samples:
Group A: 👨👨👨👨👨  (Men)
Group B: 👩👩👩👩👩  (Women)
Different people!

Paired Samples:
Before: 😊😊😊😊😊  (Same people before diet)
After:  😃😃😃😃😃  (Same people after diet)
Same people, different times!
```

### Key Concepts (Simple Definitions)

**🎯 Independent T-Test** - "Comparing Different Groups"
- Use when: Two separate groups of people/things
- Example: Test scores of Class A vs Class B
- Question: "Are these two groups different?"

**🎯 Paired T-Test** - "Comparing Before and After"
- Use when: Same group measured twice
- Example: Blood pressure before and after medication
- Question: "Did something change?"

**🎯 Effect Size** - "How BIG is the Difference?"
- P-value tells us IF there's a difference
- Effect size tells us HOW BIG the difference is
- Small difference: "Meh, who cares?"
- Large difference: "Wow, that's huge!"

---

## 2. Independent T-Test - Different Groups {#independent-test}

### What is an Independent T-Test? (Simple Explanation)

Imagine you want to know if coffee makes people more productive. You split 50 people into two groups:
- **Group A (25 people)**: Drink coffee every morning
- **Group B (25 people)**: No coffee (drink water instead)

After a month, you measure how many tasks each person completed. Are the coffee drinkers more productive?

**This is an INDEPENDENT T-TEST** because the two groups are completely different people!

### When to Use Independent T-Test

**Use it when:**
- ✅ You have TWO separate groups
- ✅ Each person/thing is in only ONE group
- ✅ The groups are independent (one doesn't affect the other)
- ✅ You want to compare their averages

**Examples:**
- 🏥 Treatment group vs Control group (different patients)
- 🎓 Online learning vs In-person learning (different students)
- 📱 iPhone users vs Android users (different people)
- 🏃 Runners vs Cyclists (different athletes)

### The Formula (Don't Panic!)

The independent t-test formula looks scary, but it's just asking:

$$t = \frac{\text{Difference between group averages}}{\text{How much the data varies}}$$

More specifically:

$$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$

**What each symbol means:**
- $\bar{x}_1$ = Average of Group 1 (like average tasks by coffee drinkers)
- $\bar{x}_2$ = Average of Group 2 (like average tasks by non-coffee drinkers)
- $s_1$ = How spread out Group 1 is (standard deviation)
- $s_2$ = How spread out Group 2 is (standard deviation)
- $n_1$ = Number of people in Group 1
- $n_2$ = Number of people in Group 2

**In plain English:** "How different are the groups compared to how much they vary?"

### What You Need Before Starting

**Checklist:**
1. ✅ Two independent groups (different people/things)
2. ✅ Data is roughly bell-shaped (normal distribution)
3. ✅ Samples are randomly selected
4. ✅ Variances are roughly equal (we'll test this!)

### Example: Coffee vs No Coffee Productivity

**The Story:**
You run an experiment with 50 office workers:
- **Coffee Group (25 people)**: Average 12 tasks/day, std dev = 3
- **No Coffee Group (25 people)**: Average 10 tasks/day, std dev = 2.5

**The Question:** Does coffee really make people more productive?

---

**Step 1: Set Up Your Claims**

🔵 **Boring Claim (H₀)**: "Coffee makes no difference"
- In math: μ₁ = μ₂ (both groups have the same average)

🔴 **Interesting Claim (H₁)**: "Coffee DOES make a difference"
- In math: μ₁ ≠ μ₂ (groups have different averages)

🎯 **How sure do we need to be?** α = 0.05 (95% confidence)

---

**Step 2: Calculate the T-Score**

Let's plug in the numbers:

$$t = \frac{12 - 10}{\sqrt{\frac{3^2}{25} + \frac{2.5^2}{25}}} = \frac{2}{\sqrt{\frac{9}{25} + \frac{6.25}{25}}} = \frac{2}{\sqrt{0.61}} = \frac{2}{0.78} = 2.56$$

**Breaking it down:**
- Top part: 12 - 10 = 2 (coffee group did 2 more tasks)
- Bottom part: √0.61 = 0.78 (combined variation)
- Final T-score: 2 / 0.78 = **2.56**

---

**Step 3: Find the P-Value**

With degrees of freedom = 48 (25 + 25 - 2), we look up the p-value:
- T-score = 2.56
- P-value ≈ 0.013

---

**Step 4: Make Your Decision**

- P-value = 0.013
- Alpha = 0.05
- Since 0.013 < 0.05, we're in the "weird zone"!

**Conclusion (in plain English):**
"Coffee drinkers completed 2 more tasks per day on average. This difference is too big to be just random chance. Coffee DOES seem to make people more productive!"

**Technical way to say it:**
"We reject H₀. There is significant evidence that coffee consumption affects productivity (p = 0.013)."

---

### Python Implementation - Independent T-Test

Let's code this step by step!

```python
# Step 1: Import the tools we need
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Step 2: Create our data
# Coffee group: 25 people
np.random.seed(42)
coffee_group = np.random.normal(12, 3, 25)  # Average 12 tasks, std dev 3

# No coffee group: 25 people
no_coffee_group = np.random.normal(10, 2.5, 25)  # Average 10 tasks, std dev 2.5

print("☕ COFFEE PRODUCTIVITY EXPERIMENT")
print("="*60)
print(f"Coffee Group (n={len(coffee_group)}):")
print(f"  Average tasks: {np.mean(coffee_group):.2f}")
print(f"  Std deviation: {np.std(coffee_group, ddof=1):.2f}")
print(f"\nNo Coffee Group (n={len(no_coffee_group)}):")
print(f"  Average tasks: {np.mean(no_coffee_group):.2f}")
print(f"  Std deviation: {np.std(no_coffee_group, ddof=1):.2f}")
print(f"\nDifference: {np.mean(coffee_group) - np.mean(no_coffee_group):.2f} tasks")
print("="*60)

# Step 3: Perform Independent T-Test (ONE LINE!)
t_stat, p_value = stats.ttest_ind(coffee_group, no_coffee_group)

print(f"\n📊 TEST RESULTS:")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

# Step 4: Make a decision
print("\n🎯 DECISION:")
if p_value < 0.05:
    print(f"✅ REJECT H₀: Coffee DOES make a difference!")
    print(f"   (p-value {p_value:.4f} < 0.05)")
    print(f"   Coffee drinkers completed {np.mean(coffee_group) - np.mean(no_coffee_group):.1f} more tasks")
else:
    print(f"❌ FAIL TO REJECT H₀: No significant difference")
    print(f"   (p-value {p_value:.4f} > 0.05)")

# Step 5: Calculate Effect Size (Cohen's d)
# This tells us HOW BIG the difference is
pooled_std = np.sqrt((np.std(coffee_group, ddof=1)**2 + np.std(no_coffee_group, ddof=1)**2) / 2)
cohens_d = (np.mean(coffee_group) - np.mean(no_coffee_group)) / pooled_std

print(f"\n📏 EFFECT SIZE (Cohen's d): {cohens_d:.3f}")
if abs(cohens_d) < 0.2:
    print("   → Small effect (barely noticeable)")
elif abs(cohens_d) < 0.5:
    print("   → Medium effect (noticeable)")
else:
    print("   → Large effect (very noticeable!)")

# Step 6: Visualize the results
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Box plots comparing groups
axes[0].boxplot([coffee_group, no_coffee_group], labels=['Coffee', 'No Coffee'])
axes[0].set_ylabel('Tasks Completed per Day')
axes[0].set_title('Productivity Comparison')
axes[0].grid(True, alpha=0.3)

# Add mean markers
means = [np.mean(coffee_group), np.mean(no_coffee_group)]
axes[0].plot([1, 2], means, 'ro-', linewidth=2, markersize=10, label='Group Means')
axes[0].legend()

# Plot 2: Histograms overlaid
axes[1].hist(coffee_group, bins=10, alpha=0.6, color='brown', label='Coffee', edgecolor='black')
axes[1].hist(no_coffee_group, bins=10, alpha=0.6, color='blue', label='No Coffee', edgecolor='black')
axes[1].axvline(np.mean(coffee_group), color='brown', linestyle='--', linewidth=2)
axes[1].axvline(np.mean(no_coffee_group), color='blue', linestyle='--', linewidth=2)
axes[1].set_xlabel('Tasks Completed per Day')
axes[1].set_ylabel('Number of People')
axes[1].set_title('Distribution of Productivity')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n📊 The graphs show the coffee group is shifted to the right (higher productivity)!")
```

---

### Checking Assumptions: Equal Variances Test

Before running an independent t-test, we should check if the two groups have similar spreads (variances). This is called **Levene's Test**.

```python
from scipy import stats

# Levene's Test for Equal Variances
stat, p_value_levene = stats.levene(coffee_group, no_coffee_group)

print("\n🔍 CHECKING ASSUMPTIONS:")
print("="*60)
print("Levene's Test for Equal Variances:")
print(f"  Test statistic: {stat:.4f}")
print(f"  P-value: {p_value_levene:.4f}")

if p_value_levene > 0.05:
    print("  ✅ Variances are equal (good!)")
    print("  → Use standard independent t-test")
else:
    print("  ⚠️  Variances are NOT equal")
    print("  → Use Welch's t-test instead")
    
    # Welch's t-test (doesn't assume equal variances)
    t_stat_welch, p_value_welch = stats.ttest_ind(coffee_group, no_coffee_group, equal_var=False)
    print(f"\n  Welch's T-test results:")
    print(f"    T-statistic: {t_stat_welch:.4f}")
    print(f"    P-value: {p_value_welch:.4f}")
```

**What this means:**
- **Equal variances (p > 0.05)**: Both groups vary about the same → Use regular t-test
- **Unequal variances (p < 0.05)**: Groups vary differently → Use Welch's t-test

---

## 3. Paired T-Test - Same Group, Two Times {#paired-test}

### What is a Paired T-Test? (Simple Explanation)

Imagine you want to know if a new study technique helps students. You:
1. Test 30 students BEFORE teaching them the technique
2. Test the SAME 30 students AFTER teaching them the technique

You're measuring the **same people twice** - this is a PAIRED T-TEST!

**Why "paired"?** Because each person has TWO measurements that are "paired" together:
- Student 1: Before score + After score
- Student 2: Before score + After score
- And so on...

### When to Use Paired T-Test

**Use it when:**
- ✅ Same subjects measured twice (before/after)
- ✅ Each measurement is paired with another
- ✅ You want to see if there's a CHANGE

**Examples:**
- 💊 Blood pressure before and after medication (same patients)
- 🏋️ Weight before and after a diet (same people)
- 📚 Test scores before and after tutoring (same students)
- 😴 Sleep quality before and after using a sleep app (same users)

### The Formula (Simpler Than Independent!)

The paired t-test is actually SIMPLER because we just look at the differences:

$$t = \frac{\bar{d}}{s_d / \sqrt{n}}$$

**What each symbol means:**
- $\bar{d}$ = Average of the differences (After - Before)
- $s_d$ = Standard deviation of the differences
- $n$ = Number of pairs

**In plain English:** "Is the average change big enough to matter?"

### Example: Study Technique Effectiveness

**The Story:**
You teach 30 students a new study technique. You test them before and after:

| Student | Before | After | Difference |
|---------|--------|-------|------------|
| 1       | 65     | 72    | +7         |
| 2       | 70     | 75    | +5         |
| 3       | 60     | 68    | +8         |
| ...     | ...    | ...   | ...        |
| 30      | 75     | 80    | +5         |

**Average difference:** +6.5 points

**The Question:** Did the study technique really help?

---

**Step 1: Set Up Your Claims**

🔵 **Boring Claim (H₀)**: "The technique makes no difference"
- In math: μ_difference = 0 (average change is zero)

🔴 **Interesting Claim (H₁)**: "The technique DOES help"
- In math: μ_difference > 0 (scores improved)
- Note: One-tailed test (we only care if it's better, not worse)

🎯 **How sure do we need to be?** α = 0.05 (95% confidence)

---

**Step 2: Calculate the Differences**

For each student: Difference = After - Before

If most differences are positive, students improved!

---

**Step 3: Run the Test**

We'll use Python to calculate the t-statistic and p-value.

---

**Step 4: Make Your Decision**

If p-value < 0.05, the technique works!

---

### Python Implementation - Paired T-Test

Let's code this!

```python
# Step 1: Import tools
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Step 2: Create our data (30 students)
np.random.seed(42)
n_students = 30

# Before scores (average 70, std dev 8)
before_scores = np.random.normal(70, 8, n_students)

# After scores (average 76.5, std dev 8) - improved by ~6.5 points
after_scores = before_scores + np.random.normal(6.5, 3, n_students)

# Calculate differences
differences = after_scores - before_scores

print("📚 STUDY TECHNIQUE EFFECTIVENESS")
print("="*60)
print(f"Number of students: {n_students}")
print(f"\nBefore technique:")
print(f"  Average score: {np.mean(before_scores):.2f}")
print(f"  Std deviation: {np.std(before_scores, ddof=1):.2f}")
print(f"\nAfter technique:")
print(f"  Average score: {np.mean(after_scores):.2f}")
print(f"  Std deviation: {np.std(after_scores, ddof=1):.2f}")
print(f"\nAverage improvement: {np.mean(differences):.2f} points")
print(f"Std dev of improvements: {np.std(differences, ddof=1):.2f}")
print("="*60)

# Step 3: Perform Paired T-Test (ONE LINE!)
t_stat, p_value = stats.ttest_rel(after_scores, before_scores)

# For one-tailed test (we only care if it improved)
p_value_one_tailed = p_value / 2 if t_stat > 0 else 1 - p_value / 2

print(f"\n📊 TEST RESULTS:")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value (one-tailed): {p_value_one_tailed:.4f}")

# Step 4: Make a decision
print("\n🎯 DECISION:")
if p_value_one_tailed < 0.05:
    print(f"✅ REJECT H₀: The technique WORKS!")
    print(f"   (p-value {p_value_one_tailed:.4f} < 0.05)")
    print(f"   Students improved by {np.mean(differences):.1f} points on average")
else:
    print(f"❌ FAIL TO REJECT H₀: No significant improvement")
    print(f"   (p-value {p_value_one_tailed:.4f} > 0.05)")

# Step 5: Calculate Effect Size (Cohen's d for paired data)
cohens_d = np.mean(differences) / np.std(differences, ddof=1)

print(f"\n📏 EFFECT SIZE (Cohen's d): {cohens_d:.3f}")
if abs(cohens_d) < 0.2:
    print("   → Small effect (barely noticeable)")
elif abs(cohens_d) < 0.5:
    print("   → Medium effect (noticeable)")
else:
    print("   → Large effect (very noticeable!)")

# Step 6: Visualize the results
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Plot 1: Before vs After (connected lines)
axes[0].plot([1, 2], [before_scores, after_scores], 'o-', alpha=0.3, color='gray')
axes[0].plot([1, 2], [np.mean(before_scores), np.mean(after_scores)], 
             'ro-', linewidth=3, markersize=12, label='Average')
axes[0].set_xticks([1, 2])
axes[0].set_xticklabels(['Before', 'After'])
axes[0].set_ylabel('Test Score')
axes[0].set_title('Individual Student Changes')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Distribution of differences
axes[1].hist(differences, bins=12, color='green', alpha=0.7, edgecolor='black')
axes[1].axvline(0, color='red', linestyle='--', linewidth=2, label='No change')
axes[1].axvline(np.mean(differences), color='blue', linestyle='--', linewidth=2, 
                label=f'Avg change: {np.mean(differences):.1f}')
axes[1].set_xlabel('Score Improvement (After - Before)')
axes[1].set_ylabel('Number of Students')
axes[1].set_title('Distribution of Improvements')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Plot 3: Box plot of differences
axes[2].boxplot(differences, vert=True)
axes[2].axhline(0, color='red', linestyle='--', linewidth=2, label='No change')
axes[2].set_ylabel('Score Improvement')
axes[2].set_title('Summary of Improvements')
axes[2].set_xticklabels(['Difference'])
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n📊 The graphs show most students improved (differences are mostly positive)!")

# Bonus: Show some individual students
print("\n👥 Sample of Individual Students:")
print("="*60)
print("Student | Before | After | Improvement")
print("-"*60)
for i in range(5):  # Show first 5 students
    print(f"   {i+1:2d}   |  {before_scores[i]:5.1f} | {after_scores[i]:5.1f} |    {differences[i]:+5.1f}")
print("  ...  |   ...  |  ...  |     ...")
print("="*60)
```

---

### Independent vs Paired: Which One to Use?

Here's a simple decision tree:

```
Are you measuring the SAME people/things twice?
│
├─ YES ─→ Use PAIRED T-TEST
│         Examples:
│         • Before/After measurements
│         • Pre-test/Post-test
│         • Treatment/Control on same subjects
│
└─ NO ──→ Use INDEPENDENT T-TEST
          Examples:
          • Men vs Women
          • Group A vs Group B
          • Treatment vs Control (different subjects)
```

**Key Difference:**
- **Independent**: Two separate groups, no connection between them
- **Paired**: Same group measured twice, each pair is connected

---

## 4. Putting It All Together - Real Examples! {#python-implementation}

### Example 1: Salary Comparison (Independent T-Test)

**The Situation:**
A company wants to know if there's a gender pay gap. They randomly sample:
- 40 male employees
- 40 female employees

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Generate salary data
np.random.seed(42)
male_salaries = np.random.normal(75000, 15000, 40)    # Average $75k
female_salaries = np.random.normal(70000, 14000, 40)  # Average $70k

print("💰 GENDER PAY GAP ANALYSIS")
print("="*60)
print(f"Male employees (n={len(male_salaries)}):")
print(f"  Average salary: ${np.mean(male_salaries):,.2f}")
print(f"  Std deviation: ${np.std(male_salaries, ddof=1):,.2f}")
print(f"\nFemale employees (n={len(female_salaries)}):")
print(f"  Average salary: ${np.mean(female_salaries):,.2f}")
print(f"  Std deviation: ${np.std(female_salaries, ddof=1):,.2f}")
print(f"\nDifference: ${np.mean(male_salaries) - np.mean(female_salaries):,.2f}")
print("="*60)

# Perform independent t-test
t_stat, p_value = stats.ttest_ind(male_salaries, female_salaries)

print(f"\n📊 INDEPENDENT T-TEST RESULTS:")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print(f"\n✅ Significant difference found!")
    print(f"   There IS a gender pay gap (p = {p_value:.4f})")
    diff = np.mean(male_salaries) - np.mean(female_salaries)
    print(f"   Men earn ${diff:,.2f} more on average")
else:
    print(f"\n❌ No significant difference")
    print(f"   No evidence of a pay gap (p = {p_value:.4f})")

# Visualize
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.boxplot([male_salaries, female_salaries], labels=['Male', 'Female'])
plt.ylabel('Salary ($)')
plt.title('Salary Distribution by Gender')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.hist(male_salaries, bins=15, alpha=0.6, color='blue', label='Male', edgecolor='black')
plt.hist(female_salaries, bins=15, alpha=0.6, color='pink', label='Female', edgecolor='black')
plt.xlabel('Salary ($)')
plt.ylabel('Number of Employees')
plt.title('Salary Distributions')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

### Example 2: Weight Loss Program (Paired T-Test)

**The Situation:**
A gym wants to test their new weight loss program. They weigh 25 people before and after 3 months.

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Generate weight data
np.random.seed(123)
n_people = 25

# Before weights (average 180 lbs, std dev 20)
before_weight = np.random.normal(180, 20, n_people)

# After weights (lost 8 lbs on average, with some variation)
weight_loss = np.random.normal(8, 4, n_people)  # Average loss 8 lbs
after_weight = before_weight - weight_loss

print("🏋️ WEIGHT LOSS PROGRAM EVALUATION")
print("="*60)
print(f"Number of participants: {n_people}")
print(f"\nBefore program:")
print(f"  Average weight: {np.mean(before_weight):.1f} lbs")
print(f"\nAfter program:")
print(f"  Average weight: {np.mean(after_weight):.1f} lbs")
print(f"\nAverage weight loss: {np.mean(weight_loss):.1f} lbs")
print("="*60)

# Perform paired t-test
t_stat, p_value = stats.ttest_rel(before_weight, after_weight)

print(f"\n📊 PAIRED T-TEST RESULTS:")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print(f"\n✅ Program WORKS!")
    print(f"   Significant weight loss detected (p = {p_value:.4f})")
    print(f"   Average loss: {np.mean(weight_loss):.1f} lbs")
else:
    print(f"\n❌ Program doesn't show significant results")
    print(f"   (p = {p_value:.4f})")

# Calculate percentage who lost weight
percent_lost = (weight_loss > 0).sum() / n_people * 100
print(f"\n📈 {percent_lost:.0f}% of participants lost weight")

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Plot 1: Before vs After
axes[0].scatter(range(n_people), before_weight, color='red', label='Before', s=100, alpha=0.6)
axes[0].scatter(range(n_people), after_weight, color='green', label='After', s=100, alpha=0.6)
for i in range(n_people):
    axes[0].plot([i, i], [before_weight[i], after_weight[i]], 'k-', alpha=0.3)
axes[0].set_xlabel('Participant')
axes[0].set_ylabel('Weight (lbs)')
axes[0].set_title('Individual Weight Changes')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Distribution of weight loss
axes[1].hist(weight_loss, bins=12, color='purple', alpha=0.7, edgecolor='black')
axes[1].axvline(0, color='red', linestyle='--', linewidth=2, label='No change')
axes[1].axvline(np.mean(weight_loss), color='blue', linestyle='--', linewidth=2,
                label=f'Avg: {np.mean(weight_loss):.1f} lbs')
axes[1].set_xlabel('Weight Loss (lbs)')
axes[1].set_ylabel('Number of People')
axes[1].set_title('Distribution of Weight Loss')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Plot 3: Paired comparison
axes[2].boxplot([before_weight, after_weight], labels=['Before', 'After'])
axes[2].set_ylabel('Weight (lbs)')
axes[2].set_title('Weight Before and After Program')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

### Quick Reference Function: Which Test Should I Use?

```python
def which_two_sample_test(same_subjects_measured_twice):
    """
    Simple function to help you decide which test to use!
    
    Parameters:
    - same_subjects_measured_twice: Are you measuring the same people/things twice? (True/False)
    """
    print("\n🔍 TWO-SAMPLE TEST SELECTION GUIDE")
    print("="*60)
    
    if same_subjects_measured_twice:
        print("✅ Use PAIRED T-TEST")
        print("\nReason: Same subjects measured twice")
        print("\nExamples:")
        print("  • Before/After treatment")
        print("  • Pre-test/Post-test")
        print("  • Repeated measurements on same subjects")
        print("\nPython code:")
        print("  t_stat, p_value = stats.ttest_rel(after, before)")
    else:
        print("✅ Use INDEPENDENT T-TEST")
        print("\nReason: Two different groups")
        print("\nExamples:")
        print("  • Men vs Women")
        print("  • Treatment group vs Control group")
        print("  • Product A vs Product B")
        print("\nPython code:")
        print("  t_stat, p_value = stats.ttest_ind(group1, group2)")
    
    print("="*60)

# Try it out!
which_two_sample_test(same_subjects_measured_twice=True)
which_two_sample_test(same_subjects_measured_twice=False)
```

---

## 5. Practice Exercises - Your Turn! {#practice-exercises}

### Exercise 1: Sleep App Effectiveness (Paired T-Test - Easy)

**The Problem:**
A sleep tracking app claims it helps people sleep better. You track 20 people's sleep for a week before and after using the app:

- **Before app:** Average 6.2 hours/night
- **After app:** Average 7.1 hours/night
- **Standard deviation of differences:** 1.2 hours

**Your Tasks:**
1. Should you use independent or paired t-test? Why?
2. Set up H₀ and H₁
3. Run the test in Python
4. What's your conclusion?

```python
# Write your code here!
# Hint: Same people measured twice = Paired test
```

<details>
<summary>💡 Click to see solution</summary>

```python
import numpy as np
from scipy import stats

print("😴 SLEEP APP EFFECTIVENESS TEST")
print("="*60)

# Given information
n = 20
avg_before = 6.2
avg_after = 7.1
avg_difference = avg_after - avg_before  # 0.9 hours improvement
std_difference = 1.2

# Question 1: Which test?
print("Q1: Which test should we use?")
print("   • Same 20 people measured twice (before & after)")
print("   ➡️  Answer: PAIRED T-TEST\n")

# Question 2: Hypotheses
print("Q2: Set up hypotheses:")
print("   H₀: μ_diff = 0 (app makes no difference)")
print("   H₁: μ_diff > 0 (app improves sleep)")
print("   α = 0.05 (95% confidence)\n")

# Question 3: Run the test
# Calculate t-statistic manually
t_statistic = avg_difference / (std_difference / np.sqrt(n))
df = n - 1
p_value = 1 - stats.t.cdf(t_statistic, df)  # One-tailed

print("Q3: Test Results:")
print(f"   T-statistic: {t_statistic:.4f}")
print(f"   Degrees of freedom: {df}")
print(f"   P-value (one-tailed): {p_value:.4f}\n")

# Question 4: Conclusion
print("Q4: Conclusion:")
if p_value < 0.05:
    print(f"   ✅ REJECT H₀!")
    print(f"   The app DOES improve sleep!")
    print(f"   (p-value {p_value:.4f} < 0.05)")
    print(f"   Average improvement: {avg_difference:.1f} hours per night")
else:
    print(f"   ❌ FAIL TO REJECT H₀")
    print(f"   Not enough evidence that the app helps")
    print(f"   (p-value {p_value:.4f} > 0.05)")

print("\n📊 In Plain English:")
print(f"   People slept {avg_difference:.1f} hours more after using the app.")
if p_value < 0.05:
    print("   This improvement is too big to be just random chance!")
    print("   The app really works! 😴💤")
else:
    print("   This could just be random variation.")

print("="*60)
```
</details>

---

### Exercise 2: Online vs In-Person Learning (Independent T-Test - Medium)

**The Problem:**
A university wants to compare online vs in-person learning. They randomly assign:
- 35 students to online classes
- 35 students to in-person classes

Final exam scores:
- **Online:** Average 78, std dev 12
- **In-person:** Average 82, std dev 10

**Your Tasks:**
1. Which test should you use?
2. Test if there's a significant difference (two-tailed test)
3. Calculate the effect size
4. What's your conclusion?

```python
# Write your code here!
```

<details>
<summary>💡 Click to see solution</summary>

```python
import numpy as np
from scipy import stats

print("🎓 ONLINE VS IN-PERSON LEARNING COMPARISON")
print("="*60)

# Given information
n1 = 35  # Online
n2 = 35  # In-person
mean_online = 78
std_online = 12
mean_inperson = 82
std_inperson = 10
alpha = 0.05

# Question 1: Which test?
print("Q1: Which test should we use?")
print("   • Two different groups of students")
print("   • Online group ≠ In-person group")
print("   ➡️  Answer: INDEPENDENT T-TEST\n")

# Question 2: Hypotheses
print("Q2: Set up hypotheses (two-tailed):")
print("   H₀: μ_online = μ_inperson (no difference)")
print("   H₁: μ_online ≠ μ_inperson (there is a difference)")
print(f"   α = {alpha} (95% confidence)\n")

# Question 3: Calculate t-statistic manually
pooled_se = np.sqrt((std_online**2 / n1) + (std_inperson**2 / n2))
t_statistic = (mean_online - mean_inperson) / pooled_se
df = n1 + n2 - 2
p_value = 2 * stats.t.cdf(t_statistic, df)  # Two-tailed (negative t)

print("Q3: Test Results:")
print(f"   T-statistic: {t_statistic:.4f}")
print(f"   Degrees of freedom: {df}")
print(f"   P-value (two-tailed): {p_value:.4f}\n")

# Question 4: Effect Size (Cohen's d)
pooled_std = np.sqrt(((n1-1)*std_online**2 + (n2-1)*std_inperson**2) / (n1 + n2 - 2))
cohens_d = (mean_online - mean_inperson) / pooled_std

print("Q4: Effect Size:")
print(f"   Cohen's d: {cohens_d:.3f}")
if abs(cohens_d) < 0.2:
    effect_desc = "Small (barely noticeable)"
elif abs(cohens_d) < 0.5:
    effect_desc = "Medium (noticeable)"
else:
    effect_desc = "Large (very noticeable)"
print(f"   → {effect_desc}\n")

# Conclusion
print("Q5: Conclusion:")
if p_value < alpha:
    print(f"   ✅ REJECT H₀!")
    print(f"   There IS a significant difference!")
    print(f"   (p-value {p_value:.4f} < {alpha})")
    diff = abs(mean_online - mean_inperson)
    winner = "In-person" if mean_inperson > mean_online else "Online"
    print(f"   {winner} learning scored {diff:.1f} points higher")
else:
    print(f"   ❌ FAIL TO REJECT H₀")
    print(f"   No significant difference found")
    print(f"   (p-value {p_value:.4f} > {alpha})")

print("\n📊 In Plain English:")
print(f"   In-person students scored {mean_inperson - mean_online:.1f} points higher.")
if p_value < alpha:
    print("   This difference is statistically significant!")
    if abs(cohens_d) < 0.5:
        print("   But the effect size is small-to-medium.")
        print("   The difference exists, but it's not huge.")
    else:
        print("   And the effect size is large!")
        print("   This is a meaningful difference!")
else:
    print("   But this could just be random variation.")
    print("   Both methods seem equally effective.")

print("="*60)
```
</details>

---

### Exercise 3: Your Own Example! (Challenge)

Create your own two-sample test scenario! Choose one:

**Option A: Independent T-Test**
```python
import numpy as np
from scipy import stats

# Example: Compare two products, two groups, etc.
print("MY INDEPENDENT T-TEST")
print("="*60)
print("Scenario: [Describe your comparison]")
print("Group 1: [Description]")
print("Group 2: [Description]")
print("="*60)

# Generate or input your data
# group1 = np.array([...])
# group2 = np.array([...])

# Run independent t-test
# t_stat, p_value = stats.ttest_ind(group1, group2)

# Make conclusion
```

**Option B: Paired T-Test**
```python
import numpy as np
from scipy import stats

# Example: Before/after comparison
print("MY PAIRED T-TEST")
print("="*60)
print("Scenario: [Describe your before/after situation]")
print("="*60)

# Generate or input your data
# before = np.array([...])
# after = np.array([...])

# Run paired t-test
# t_stat, p_value = stats.ttest_rel(after, before)

# Make conclusion
```

**Ideas for scenarios:**
- 📱 iPhone vs Android battery life
- 🏃 Running speed: morning vs evening
- 💰 Spending: weekday vs weekend
- 📚 Study time: with music vs without music
- ☕ Coffee shop wait times: Starbucks vs Dunkin'
- 🎮 Gaming performance: before vs after practice

---

## Summary - What You Learned! 🎓

### Key Concepts

**1. Two Types of Two-Sample Tests**

**Independent T-Test:**
- Compares TWO different groups
- Example: Men vs Women, Group A vs Group B
- Formula focuses on difference between group means
- Python: `stats.ttest_ind(group1, group2)`

**Paired T-Test:**
- Compares SAME group measured twice
- Example: Before vs After, Pre-test vs Post-test
- Formula focuses on average of differences
- Python: `stats.ttest_rel(after, before)`

**2. Effect Size (Cohen's d)**
- P-value tells you IF there's a difference
- Effect size tells you HOW BIG the difference is
- Small (< 0.2): "Meh, barely noticeable"
- Medium (0.2-0.5): "Yeah, I can see that"
- Large (> 0.5): "Wow, that's huge!"

**3. Assumptions to Check**
- Data should be roughly normal (bell-shaped)
- For independent t-test: Check equal variances (Levene's test)
- For paired t-test: Differences should be roughly normal

### Quick Decision Tree

```
Are you comparing two groups?
│
├─ Same people measured twice?
│  │
│  ├─ YES ─→ PAIRED T-TEST
│  │         stats.ttest_rel(after, before)
│  │
│  └─ NO ──→ INDEPENDENT T-TEST
│            stats.ttest_ind(group1, group2)
│
└─ Only one group?
   └─ Go back to Chapter 4.1 (One-sample tests)
```

### Python Cheat Sheet

```python
from scipy import stats
import numpy as np

# Independent T-Test (two different groups)
t_stat, p_value = stats.ttest_ind(group1, group2)

# Paired T-Test (same group, two measurements)
t_stat, p_value = stats.ttest_rel(after, before)

# Check equal variances (for independent t-test)
stat, p_val = stats.levene(group1, group2)
if p_val < 0.05:
    # Use Welch's t-test instead
    t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

# Calculate Effect Size (Cohen's d)
# For independent:
pooled_std = np.sqrt((std1**2 + std2**2) / 2)
cohens_d = (mean1 - mean2) / pooled_std

# For paired:
cohens_d = np.mean(differences) / np.std(differences, ddof=1)

# Decision
if p_value < 0.05:
    print("Significant difference found!")
else:
    print("No significant difference")
```

### Common Mistakes to Avoid ⚠️

1. **Using independent t-test for paired data** → Use paired t-test!
2. **Using paired t-test for independent groups** → Use independent t-test!
3. **Ignoring effect size** → Small p-value doesn't mean big difference!
4. **Not checking assumptions** → Check normality and equal variances
5. **One-tailed vs two-tailed confusion** → Read the question carefully!

### Real-World Interpretation Tips

**When p-value < 0.05:**
- ✅ "We found a statistically significant difference"
- ✅ "The difference is unlikely to be due to chance"
- ❌ Don't say: "We proved X causes Y" (correlation ≠ causation!)

**When p-value > 0.05:**
- ✅ "We didn't find enough evidence of a difference"
- ✅ "The groups appear similar"
- ❌ Don't say: "The groups are definitely the same"

**Always consider effect size:**
- Small p-value + Small effect size = "Significant but not important"
- Small p-value + Large effect size = "Significant AND important!"

---

## What's Next?

In **Chapter 4.3**, you'll learn:
- **Proportion Tests**: Comparing percentages (like 60% vs 70%)
- **One-Sample Proportion Test**: Is the success rate really 50%?
- **Two-Sample Proportion Test**: Do men and women have different success rates?
- **Chi-Square Tests**: Testing relationships between categories

Keep practicing! You're building a powerful toolkit for data analysis! 🚀

---

**Remember:** The goal isn't just to get a p-value - it's to answer real questions and make informed decisions! Always think about what your results mean in the real world. 💡
