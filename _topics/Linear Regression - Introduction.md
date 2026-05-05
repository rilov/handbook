---
title: "Linear Regression - Introduction"
category: Machine Learning
order: 2
tags:
  - machine-learning
  - linear-regression
  - supervised-learning
  - regression
summary: "Complete beginner's guide to Linear Regression - learn to predict continuous values with real-world examples and Python code."
---

# Linear Regression - Complete Beginner's Guide

## Welcome to Linear Regression! 📈

Linear Regression is one of the simplest and most important machine learning algorithms. It's the perfect starting point for your ML journey!

---

## What is Linear Regression?

### The Simple Explanation

**Linear Regression** is about finding the best straight line that fits your data.

Think of it like this:
- You have data points scattered on a graph
- You want to draw a straight line through them
- The line should be as close as possible to all points
- This line helps you predict future values

### Real-World Example: Predicting House Prices

**The Problem:**
You want to predict house prices based on size.

**The Data:**
| Size (sq ft) | Price ($1000s) |
|--------------|---------------|
| 1000 | 200 |
| 1500 | 300 |
| 2000 | 400 |
| 2500 | 500 |
| 3000 | 600 |

**What Linear Regression Does:**
It finds the best line through these points:
```
Price = 0.2 × Size
```

Now you can predict:
- 1800 sq ft house → 0.2 × 1800 = $360,000
- 3500 sq ft house → 0.2 × 3500 = $700,000

---

## The Mathematics (Made Simple!)

### The Line Equation

You probably remember this from school:

```
y = mx + b
```

In Linear Regression, we write it as:

```
ŷ = β₀ + β₁x
```

**What the symbols mean:**
- **ŷ (y-hat)** = Predicted value (what we're trying to guess)
- **x** = Input feature (what we know)
- **β₁ (beta-1)** = Slope (how much y changes when x changes)
- **β₀ (beta-0)** = Intercept (value when x = 0)

### Understanding Slope (β₁)

**What it means:** How much the output changes when the input increases by 1.

**Example:**
- If β₁ = 0.2 (house price example)
- Every additional square foot adds $0.2 thousand ($200)
- 1000 sq ft → $200,000
- 1001 sq ft → $200,200

**Visual:**
```
Price
  ↑
  │        /
  │      /
  │    /  (slope = 0.2)
  │  /
  │/
  └─────────→ Size
```

### Understanding Intercept (β₀)

**What it means:** The predicted value when x = 0.

**Example:**
- If β₀ = 50
- A house with 0 sq ft would cost $50,000
- This represents the "base price" (land, permits, etc.)

**Note:** Sometimes intercept doesn't make sense in reality (a 0 sq ft house), but it's still part of the equation.

---

## How Does It Work? (The Magic Behind It)

### The Goal: Minimize Errors

Linear Regression tries to find the line that minimizes the total error.

**What is Error?**

Error = Actual Value - Predicted Value

**Example:**
- Actual price: $320,000
- Predicted price: $300,000
- Error: $320,000 - $300,000 = $20,000

### The Cost Function (Sum of Squared Errors)

We square the errors for two reasons:
1. Make all errors positive (don't cancel out)
2. Penalize large errors more

**Formula:**
```
Cost = Σ(y - ŷ)²
```

**Visual:**
```
Actual point: ●
Predicted:     |
               |  ← Error
               |
```

**The line with the smallest cost is the best line!**

### How It Finds the Best Line

Now we know the model wants to **minimize the cost** (errors). But HOW does it actually find the best line? There are two main methods. Let's understand each one with simple examples!

---

## Method 1: Ordinary Least Squares (OLS) 📐

### 🎯 The Simple Idea

**OLS is like solving a math puzzle with a calculator.**

Instead of trying lots of different lines and picking the best one, OLS uses a **mathematical formula** to instantly calculate the perfect line in ONE step!

### 🍕 Pizza Analogy

Imagine you want to cut a pizza into exactly equal slices:

**Bad way (trial and error):**
- Cut a slice... too big!
- Cut another... too small!
- Try again... still wrong!
- Keep trying for hours

**OLS way (formula):**
- You know there are 8 people
- 360° ÷ 8 = 45° per slice
- Cut perfectly the FIRST time!

That's OLS! It uses a formula to find the answer **directly**.

### 📊 What It Actually Does

OLS finds the line that minimizes the **sum of squared errors**:

```
For each data point:
1. Find the error (actual - predicted)
2. Square the error (so negatives don't cancel positives)
3. Add up all squared errors
4. Find the line where this sum is SMALLEST
```

**Why "squared"?**

Imagine these errors: +5, -5, +3, -3
- Sum: 0 (looks perfect, but it's not!)
- Squared sum: 25+25+9+9 = 68 (shows real error)

Squaring makes all errors positive AND penalizes big errors more!

### 🧮 The Math (Simple Version)

For a simple line `y = β₀ + β₁x`, OLS calculates:

```
β₁ (slope) = Σ((x - x̄)(y - ȳ)) / Σ((x - x̄)²)

β₀ (intercept) = ȳ - β₁ × x̄

Where:
x̄ = average of x values
ȳ = average of y values
Σ = sum of all values
```

**Don't worry about memorizing this!** Python does it for you:

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()  # Uses OLS by default!
model.fit(X, y)
```

### ✅ When to Use OLS

| Use OLS When | Don't Use OLS When |
|--------------|-------------------|
| ✅ Small/medium dataset (< 100k rows) | ❌ Huge dataset (millions of rows) |
| ✅ Few features (< 1000) | ❌ Massive features (>10,000) |
| ✅ Want exact answer | ❌ Need to update model online |
| ✅ Memory is enough | ❌ Memory is limited |

### 🎯 OLS Pros and Cons

**Pros:**
- ✅ **Exact solution** - finds THE best answer
- ✅ **One-shot** - no iterations needed
- ✅ **Fast** for small data
- ✅ **No tuning** required

**Cons:**
- ❌ **Slow for big data** (matrix calculations)
- ❌ **Requires lots of memory** (stores entire matrix)
- ❌ **Doesn't work** for very complex models

---

## Method 2: Gradient Descent 🏔️

### 🎯 The Simple Idea

**Gradient Descent is like rolling a ball down a hill.**

Instead of solving with a formula, it **gradually adjusts** the line, making it better and better with each step until it reaches the bottom (minimum error).

### 🏔️ The Mountain Climber Analogy

Imagine you're a hiker stuck on a mountain in **dense fog**:

```
        You are here →  🧗
                        /\
                       /  \
                      /    \
                     /      \
                    /  Fog!  \
                   /          \
                  /            \
                 /     ⛰️       \
                /                \
        ──────  (Bottom = Goal)  ──────
```

**Your situation:**
- 🎯 **Goal:** Get to the bottom (minimum error)
- 🌫️ **Problem:** You can't see the bottom (fog!)
- 🦯 **Tool:** You can feel the slope under your feet

**Your strategy:**
1. **Feel the ground** - which way is downhill?
2. **Take a small step** in that direction
3. **Stop and check** - which way is downhill now?
4. **Take another small step** downhill
5. **Repeat** until the ground is flat (you're at the bottom!)

That's exactly how Gradient Descent works! 🎉

### 📊 Visual Step-by-Step

```
Step 0: Start somewhere (random)
        🧗
       ●
      /
     /
    /        ⛰️
   /
  /__________

Step 1: Check slope, take small step downhill
        
       \  
        ●→🧗
         \
          \      ⛰️
           \
  __________

Step 2: Continue downhill
        
        \
         \
          ●→🧗   ⛰️
            \
  __________

Step 3: Almost there!
        
        \
         \
          \
           ●→🧗⛰️
  __________

Step 4: Reached the bottom! 🎉
        
        \
         \
          \
           \
  ______●__🎯_____   You're at the minimum!
```

### 🧮 The Algorithm (Simple Version)

```python
# Gradient Descent in simple steps:

1. Start with random values for slope and intercept
   slope = random number
   intercept = random number

2. Calculate current error (cost)
   cost = sum of squared errors

3. Calculate the slope of the cost (gradient)
   "Which direction reduces error?"

4. Take a small step in that direction
   slope = slope - (learning_rate × gradient_slope)
   intercept = intercept - (learning_rate × gradient_intercept)

5. Repeat steps 2-4 until cost stops decreasing
```

### 🎚️ The Learning Rate (Step Size)

The **learning rate** is how big your steps are. This is **CRITICAL**!

**Too Small (tiny baby steps):**
```
🧗→●→●→●→●→●→●→●→●→●→●→●...🎯

Result: Takes forever to reach the bottom! 🐌
```

**Too Large (giant leaps):**
```
🧗──────●
        \
         \
          ●─────────🚀  Overshoot!
                   /
                  /
                 ●     Miss the target!
                /
              ●─────🚀

Result: Bounces around, never settles! 💥
```

**Just Right (Goldilocks):**
```
🧗
  ●
   ●
    ●
     ●
      ●
       🎯  Perfect! Reaches the bottom efficiently! ✅
```

**Common learning rates:** 0.001, 0.01, 0.1

```python
# Example with sklearn
from sklearn.linear_model import SGDRegressor

model = SGDRegressor(learning_rate='constant', eta0=0.01)
# eta0 = 0.01 means step size of 0.01
```

### 🎯 Three Types of Gradient Descent

#### **1. Batch Gradient Descent**
```
Use ALL data to calculate each step.

✅ Most accurate
❌ Slow for big data
❌ Uses lots of memory
```

#### **2. Stochastic Gradient Descent (SGD)**
```
Use ONE random data point per step.

✅ Very fast
✅ Works with huge data
❌ Noisy (zigzag path to bottom)
```

#### **3. Mini-Batch Gradient Descent (Most Common!)**
```
Use a small batch (e.g., 32 points) per step.

✅ Best of both worlds
✅ Fast AND stable
✅ Used in deep learning!
```

### 📊 Visual Comparison

```
Batch GD:        Stochastic GD:      Mini-Batch GD:
                 
🧗               🧗                   🧗
 ●                ●                    ●
  ●               ↘●                    ●
   ●                ●                    ●
    ●              ↗                      ●
     🎯            ●                       🎯
                  ↘●
Smooth path        🎯                Slightly noisy
                                     but smooth
                  Zigzag path
```

### ✅ When to Use Gradient Descent

| Use Gradient Descent When | Don't Use When |
|---------------------------|----------------|
| ✅ Huge dataset (millions of rows) | ❌ Small dataset |
| ✅ Many features (>10,000) | ❌ Want exact answer |
| ✅ Online/streaming data | ❌ Have time for OLS |
| ✅ Complex models (neural nets) | ❌ Simple problem |
| ✅ Limited memory | ❌ Plenty of memory |

### 🎯 Gradient Descent Pros and Cons

**Pros:**
- ✅ **Works with huge data** (millions of rows)
- ✅ **Less memory** required
- ✅ **Foundation** of deep learning
- ✅ **Online learning** possible

**Cons:**
- ❌ **Approximate** solution (very close, but not exact)
- ❌ **Need to tune** learning rate
- ❌ **May not converge** if learning rate is wrong
- ❌ **Slower per problem** (needs many iterations)

---

## 🥊 OLS vs Gradient Descent - Side by Side

| Feature | OLS | Gradient Descent |
|---------|-----|------------------|
| **How it works** | Math formula | Iterative steps |
| **Speed (small data)** | ⚡ Super fast | 🐢 Slower |
| **Speed (big data)** | 🐢 Very slow | ⚡ Fast |
| **Memory** | High | Low |
| **Accuracy** | Exact | Approximate |
| **Tuning needed** | None | Learning rate |
| **Real-world use** | Sklearn `LinearRegression` | Deep learning, big data |
| **Analogy** | Calculator | Hiking down mountain |

### 💡 Real-World Decision

**For most beginners:**
- Use sklearn's `LinearRegression` → It uses OLS automatically!
- Works perfectly for typical datasets

**For big data/complex models:**
- Use sklearn's `SGDRegressor` → Uses Gradient Descent
- Or move to deep learning frameworks

```python
# Beginner choice (OLS)
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)  # Done! ✅

# Big data choice (Gradient Descent)
from sklearn.linear_model import SGDRegressor
model = SGDRegressor(max_iter=1000, eta0=0.01)
model.fit(X, y)  # Iterates many times
```

### 🎓 Key Takeaway

**Both methods find the SAME answer!**
- **OLS**: Direct calculation (like using GPS)
- **Gradient Descent**: Step-by-step search (like asking for directions)

For learning, OLS is simpler. For real-world big data, Gradient Descent rules!

---

## Simple Linear Regression (One Feature)

### When to Use

- You have ONE input feature (x)
- You want to predict ONE output (y)
- The relationship appears linear

### Example: Study Hours vs Test Scores

**Data:**
| Hours Studied | Test Score |
|---------------|------------|
| 1 | 65 |
| 2 | 70 |
| 3 | 75 |
| 4 | 80 |
| 5 | 85 |

**Visual:**
```
Score
  ↑
100│         ●
  │       ●
  │     ●
  │   ●
  │ ●
50└────────────→ Hours
  0   5   10
```

**The Line:**
```
Score = 60 + 5 × Hours
```

**Interpretation:**
- β₀ = 60: Base score (even with 0 hours)
- β₁ = 5: Each hour adds 5 points
- Prediction: 7 hours → 60 + 5×7 = 95 points

---

## Multiple Linear Regression (Multiple Features)

### When to Use

- You have MULTIPLE input features (x₁, x₂, x₃, ...)
- You want to predict ONE output (y)
- Each feature contributes to the prediction

### Example: House Price Prediction

**Features:**
- Size (sq ft)
- Number of bedrooms
- Age of house
- Location score

**Equation:**
```
Price = β₀ + β₁(Size) + β₂(Bedrooms) + β₃(Age) + β₄(Location)
```

**Example Values:**
```
Price = 50 + 0.2(Size) + 30(Bedrooms) - 1(Age) + 20(Location)
```

**Interpretation:**
- β₁ = 0.2: Each sq ft adds $200
- β₂ = 30: Each bedroom adds $30,000
- β₃ = -1: Each year older subtracts $1,000
- β₄ = 20: Better location adds $20,000

**Prediction:**
```
House: 2000 sq ft, 3 bedrooms, 10 years old, location score 8
Price = 50 + 0.2(2000) + 30(3) - 1(10) + 20(8)
     = 50 + 400 + 90 - 10 + 160
     = $690,000
```

---

## Assumptions of Linear Regression

### 1. Linearity
**What it means:** The relationship between x and y should be linear.

**How to check:** Plot your data. If it looks curved, linear regression might not work well.

**What to do if violated:** Try polynomial regression or transform your data.

### 2. Independence
**What it means:** Each data point should be independent of others.

**Example violation:** Measuring the same person multiple times (not independent).

### 3. Homoscedasticity (Constant Variance)
**What it means:** The spread of errors should be consistent across all values.

**Visual check:** Plot errors vs predicted values. Should see random scatter, not a pattern.

### 4. Normality of Errors
**What it means:** Errors should be normally distributed.

**How to check:** Histogram of errors should look like a bell curve.

### 5. No Multicollinearity (for multiple regression)
**What it means:** Features shouldn't be highly correlated with each other.

**Example violation:** Using both "height in inches" and "height in cm" (they're the same thing!).

---

## Evaluating Your Model

### R-Squared (R²)

**What it is:** How well your line fits the data (0 to 1).

**Interpretation:**
- R² = 0: Model explains none of the variance (terrible)
- R² = 0.5: Model explains 50% of variance (okay)
- R² = 0.9: Model explains 90% of variance (excellent)
- R² = 1.0: Model explains all variance (perfect, but suspicious)

**Formula:**
```
R² = 1 - (Sum of squared errors / Total sum of squares)
```

**Simple interpretation:** "Percentage of variation explained by the model"

### Mean Squared Error (MSE)

**What it is:** Average of squared errors.

**Formula:**
```
MSE = Σ(y - ŷ)² / n
```

**Interpretation:** Lower is better. Hard to interpret directly (units are squared).

### Mean Absolute Error (MAE)

**What it is:** Average of absolute errors.

**Formula:**
```
MAE = Σ|y - ŷ| / n
```

**Interpretation:** "On average, my prediction is off by this amount"

**Example:** MAE = $20,000 means predictions are off by $20,000 on average.

---

## Common Problems and Solutions

### Problem 1: Overfitting

**What it is:** Model fits training data too well, performs poorly on new data.

**Symptoms:**
- Perfect R² on training data
- Terrible R² on test data
- Very complex model

**Solutions:**
- Use more training data
- Remove unnecessary features
- Use regularization (L1/L2)
- Try simpler model

### Problem 2: Underfitting

**What it is:** Model is too simple, doesn't capture patterns.

**Symptoms:**
- Poor R² on both training and test data
- Line doesn't fit the data well

**Solutions:**
- Add more features
- Try more complex model
- Add polynomial features
- Remove outliers

### Problem 3: Outliers

**What it is:** Extreme values that skew the line.

**Visual:**
```
y
│     ● ← outlier
│   ●
│ ●
│●
└─→ x
```

**Solutions:**
- Remove outliers (if they're errors)
- Use robust regression
- Transform data
- Keep them if they're real

---

## Complete Python Example (Notebook Style)

### Example 1: Simple Linear Regression

```python
# ============================================
# SIMPLE LINEAR REGRESSION
# Predict house prices based on size
# ============================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

print("🏠 HOUSE PRICE PREDICTION")
print("=" * 50)

# ============================================
# STEP 1: CREATE SAMPLE DATA
# ============================================
print("\n📊 Step 1: Creating sample data")

# House sizes (in sq ft)
X = np.array([1000, 1500, 2000, 2500, 3000, 3500, 4000]).reshape(-1, 1)

# House prices (in $1000s)
y = np.array([200, 300, 400, 500, 600, 700, 800])

print(f"Number of houses: {len(X)}")
print(f"Size range: {X.min()} - {X.max()} sq ft")
print(f"Price range: ${y.min()}k - ${y.max()}k")

# ============================================
# STEP 2: VISUALIZE THE DATA
# ============================================
print("\n📈 Step 2: Visualizing the data")

plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', s=100, alpha=0.7)
plt.xlabel('House Size (sq ft)')
plt.ylabel('Price ($1000s)')
plt.title('House Size vs Price')
plt.grid(True, alpha=0.3)
plt.show()

print("✅ Data plotted - can you see the linear pattern?")

# ============================================
# STEP 3: TRAIN THE MODEL
# ============================================
print("\n🤖 Step 3: Training the model")

model = LinearRegression()
model.fit(X, y)

print("✅ Model trained!")

# ============================================
# STEP 4: GET MODEL PARAMETERS
# ============================================
print("\n📋 Step 4: Model parameters")

slope = model.coef_[0]
intercept = model.intercept_

print(f"Slope (β₁): ${slope:.2f} per sq ft")
print(f"Intercept (β₀): ${intercept:.2f}")
print(f"\nEquation: Price = {intercept:.2f} + {slope:.2f} × Size")

print("\n💡 What this means:")
print(f"- A house with 0 sq ft would cost ${intercept:.2f}k (base price)")
print(f"- Each additional sq ft adds ${slope:.2f}k")

# ============================================
# STEP 5: MAKE PREDICTIONS
# ============================================
print("\n🔮 Step 5: Making predictions")

# Predict prices for our training data
y_pred = model.predict(X)

# Predict for new houses
new_sizes = np.array([1800, 2800, 3800]).reshape(-1, 1)
new_predictions = model.predict(new_sizes)

print("\nTraining data predictions:")
for i in range(len(X)):
    actual = y[i]
    predicted = y_pred[i]
    error = actual - predicted
    print(f"  {X[i][0]:.0f} sq ft: ${predicted:.0f}k (actual: ${actual:.0f}k, error: ${error:.0f}k)")

print("\nNew house predictions:")
for i in range(len(new_sizes)):
    size = new_sizes[i][0]
    price = new_predictions[i]
    print(f"  {size:.0f} sq ft → ${price:.0f}k")

# ============================================
# STEP 6: EVALUATE THE MODEL
# ============================================
print("\n📊 Step 6: Model evaluation")

r2 = r2_score(y, y_pred)
mse = mean_squared_error(y, y_pred)
mae = mean_absolute_error(y, y_pred)

print(f"R² Score: {r2:.4f}")
print(f"Mean Squared Error: {mse:.2f}")
print(f"Mean Absolute Error: ${mae:.2f}k")

print("\n💡 Interpretation:")
print(f"- R² = {r2:.1%} means the model explains {r2:.1%} of the variance")
print(f"- MAE = ${mae:.0f}k means predictions are off by ${mae:.0f}k on average")

# ============================================
# STEP 7: PLOT THE REGRESSION LINE
# ============================================
print("\n📈 Step 7: Plotting the regression line")

plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', s=100, alpha=0.7, label='Actual data')
plt.plot(X, y_pred, color='red', linewidth=2, label='Regression line')
plt.xlabel('House Size (sq ft)')
plt.ylabel('Price ($1000s)')
plt.title('Linear Regression: House Size vs Price')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("✅ Regression line plotted!")

# ============================================
# STEP 8: PREDICT FOR USER INPUT
# ============================================
print("\n🎯 Step 8: Interactive prediction")

def predict_price(size):
    price = model.predict([[size]])[0]
    print(f"\n🏠 House size: {size} sq ft")
    print(f"💰 Predicted price: ${price:.0f}k (${price*1000:.0f})")
    return price

# Try it!
predict_price(2200)
predict_price(3200)
```

### Example 2: Multiple Linear Regression

```python
# ============================================
# MULTIPLE LINEAR REGRESSION
# Predict house prices using multiple features
# ============================================

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

print("🏠 MULTIPLE LINEAR REGRESSION")
print("=" * 50)

# ============================================
# STEP 1: CREATE SAMPLE DATA
# ============================================
print("\n📊 Step 1: Creating sample data")

# Features: Size, Bedrooms, Age, Location
X = np.array([
    [1000, 2, 10, 5],
    [1500, 3, 5, 7],
    [2000, 3, 2, 8],
    [2500, 4, 15, 6],
    [3000, 4, 1, 9],
    [3500, 5, 8, 8],
    [4000, 5, 3, 10]
])

# Prices
y = np.array([200, 300, 400, 450, 600, 650, 800])

feature_names = ['Size (sq ft)', 'Bedrooms', 'Age (years)', 'Location (1-10)']

print(f"Number of houses: {len(X)}")
print(f"Number of features: {len(feature_names)}")
print(f"\nFeatures: {feature_names}")

# ============================================
# STEP 2: TRAIN THE MODEL
# ============================================
print("\n🤖 Step 2: Training the model")

model = LinearRegression()
model.fit(X, y)

print("✅ Model trained!")

# ============================================
# STEP 3: GET MODEL PARAMETERS
# ============================================
print("\n📋 Step 3: Model parameters")

intercept = model.intercept_
coefficients = model.coef_

print(f"Intercept (β₀): ${intercept:.2f}k")
print("\nCoefficients (β₁, β₂, β₃, β₄):")
for i, (name, coef) in enumerate(zip(feature_names, coefficients)):
    print(f"  {name}: ${coef:.2f}k")

print(f"\nEquation:")
print(f"Price = {intercept:.2f}", end="")
for name, coef in zip(feature_names, coefficients):
    print(f" + {coef:.2f}×{name}", end="")
print()

# ============================================
# STEP 4: INTERPRET THE COEFFICIENTS
# ============================================
print("\n💡 Step 4: Interpreting coefficients")

print("What each coefficient means:")
for name, coef in zip(feature_names, coefficients):
    if coef > 0:
        print(f"  ✓ {name}: Each unit increase adds ${abs(coef):.0f}k")
    else:
        print(f"  ✗ {name}: Each unit increase subtracts ${abs(coef):.0f}k")

# ============================================
# STEP 5: MAKE PREDICTIONS
# ============================================
print("\n🔮 Step 5: Making predictions")

# Predict for training data
y_pred = model.predict(X)

print("\nTraining data predictions:")
for i in range(len(X)):
    actual = y[i]
    predicted = y_pred[i]
    error = actual - predicted
    print(f"  House {i+1}: ${predicted:.0f}k (actual: ${actual:.0f}k, error: ${error:.0f}k)")

# Predict for new house
new_house = np.array([[2200, 3, 5, 7]])
new_prediction = model.predict(new_house)[0]

print(f"\n🏠 New house prediction:")
print(f"  Size: 2200 sq ft")
print(f"  Bedrooms: 3")
print(f"  Age: 5 years")
print(f"  Location: 7/10")
print(f"  💰 Predicted price: ${new_prediction:.0f}k")

# ============================================
# STEP 6: EVALUATE THE MODEL
# ============================================
print("\n📊 Step 6: Model evaluation")

r2 = r2_score(y, y_pred)
print(f"R² Score: {r2:.4f}")
print(f"The model explains {r2:.1%} of the variance in house prices")
```

---

## Quick Reference

### Key Formulas

**Simple Linear Regression:**
```
ŷ = β₀ + β₁x
```

**Multiple Linear Regression:**
```
ŷ = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
```

**Cost Function:**
```
Cost = Σ(y - ŷ)²
```

**R-Squared:**
```
R² = 1 - (SS_residual / SS_total)
```

### Common Scikit-Learn Functions

```python
from sklearn.linear_model import LinearRegression

# Create model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Get parameters
intercept = model.intercept_
coefficients = model.coef_

# Evaluate
from sklearn.metrics import r2_score, mean_squared_error
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
```

---

## When to Use Linear Regression

### ✅ Good For:
- Predicting continuous values (prices, temperatures, scores)
- When relationship appears linear
- When you want interpretable results
- When you have enough data (50+ points preferred)
- When assumptions are met

### ❌ Not Good For:
- Classifying into categories (use classification)
- When relationship is clearly non-linear
- When you have very little data (< 20 points)
- When features are highly correlated
- When you need perfect accuracy

---

## Next Steps

### Practice Ideas:
1. Predict car prices from mileage, age, brand
2. Predict student grades from study hours, attendance
3. Predict salary from experience, education, location
4. Predict sales from advertising spend, season, price

### Advanced Topics:
- Polynomial Regression (for curved relationships)
- Ridge/Lasso Regression (for regularization)
- Logistic Regression (for classification)
- Generalized Linear Models

---

## Summary

**Linear Regression** is:
- ✅ Simple and interpretable
- ✅ Fast to train
- ✅ Good baseline model
- ✅ Great for understanding relationships
- ✅ Foundation for more complex models

**Key Takeaways:**
1. Find the best line through your data
2. Use slope and intercept to make predictions
3. Evaluate with R², MSE, MAE
4. Check assumptions
5. Start simple, then improve

**Remember:** Linear Regression is the "Hello World" of machine learning. Master it first, then move to more complex algorithms! 🚀

---

**Happy Learning!** 📚
