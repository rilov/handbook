---
title: "04. Linear Regression - Advanced Topics"
category: Machine Learning
order: 4
tags:
  - machine-learning
  - linear-regression
  - assumptions
  - scaling
  - multicollinearity
  - regularization
summary: "Deep dive into Linear Regression assumptions, challenges, and advanced techniques - scaling, feature engineering, handling violations, and regularization explained simply."
---

# Linear Regression - Advanced Topics

## Welcome! 🚀

You've learned the basics of Linear Regression. Now let's dive deeper into the **assumptions**, **challenges**, and **advanced techniques** that will make you a Linear Regression expert!

---

## Table of Contents

1. [Assumptions of Linear Regression](#assumptions)
2. [Challenges and How to Fix Them](#challenges)
3. [Scaling and Interpretability](#scaling)
4. [Understanding Coefficients](#coefficients)
5. [Feature Engineering](#feature-engineering)
6. [Regularization (Ridge, Lasso, Elastic Net)](#regularization)
7. [Complete Python Examples](#python-examples)

---

## 1. Assumptions of Linear Regression {#assumptions}

Linear Regression is simple and powerful, but it **only works well** when certain assumptions are met. Let's understand each one!

### 🎯 Assumption 1: Linearity

**What it means:** The relationship between features (X) and target (y) should be **linear** (a straight line).

**Simple explanation:** If you plot X vs y, it should look like a straight line, not a curve.

**Example of LINEAR relationship:**
```
Temperature (°C)  →  Energy Consumption (kWh)
10                →  50
20                →  100
30                →  150
40                →  200

As temperature increases by 10°C, energy increases by 50 kWh consistently.
This is LINEAR! ✅
```

**Visual:**
```
Energy
  │     ●
  │   ●
  │ ●
  │●
  └─────→ Temperature
  
Perfect straight line = Linear relationship
```

**Example of NON-LINEAR relationship:**
```
Temperature (°C)  →  Energy Consumption (kWh)
10                →  50
20                →  80   (smaller increase)
30                →  120  (bigger increase)
40                →  180  (even bigger increase)

The rate of change is NOT constant.
This is NON-LINEAR! ❌
```

**Visual:**
```
Energy
  │         ●
  │      ●
  │   ●
  │ ●
  └─────→ Temperature
  
Curved line = Non-linear relationship
```

**Real-world example:**

**Linear:** House size vs price
- 1000 sq ft → $200k
- 2000 sq ft → $400k
- 3000 sq ft → $600k
- Each additional 1000 sq ft adds $200k (constant rate)

**Non-linear:** Population growth over time
- Year 1: 100 people
- Year 2: 110 people (+10)
- Year 3: 121 people (+11)
- Year 4: 133 people (+12)
- Growth rate is accelerating (exponential, not linear)

**How to check:**
```python
import matplotlib.pyplot as plt

# Plot X vs y
plt.scatter(X, y)
plt.xlabel('Feature')
plt.ylabel('Target')
plt.title('Check for Linearity')
plt.show()

# Look for: straight line pattern ✅
# Watch out for: curved pattern ❌
```

**What to do if violated:**
1. **Transform the data** (log, square root, polynomial)
2. **Use polynomial regression** (we'll cover this later)
3. **Try a different algorithm** (decision trees, neural networks)

---

### 🎯 Assumption 2: Independence of Data Points

**What it means:** Each data point should be **independent** - one observation shouldn't influence another.

**Simple explanation:** Measuring one house shouldn't affect the measurement of another house.

**Example of INDEPENDENT data:**
```
Measuring different houses in different neighborhoods:
House 1: 1500 sq ft, $300k
House 2: 2000 sq ft, $400k
House 3: 1800 sq ft, $350k

Each house is separate. ✅
```

**Example of DEPENDENT data:**
```
Measuring the same person's weight over time:
Day 1: 70 kg
Day 2: 70.5 kg
Day 3: 71 kg

Today's weight depends on yesterday's weight! ❌
This is called "autocorrelation" or "time series data"
```

**Real-world violations:**

**Time Series Data:**
- Stock prices (today's price depends on yesterday's)
- Temperature readings (today's temp related to yesterday's)
- Sales data (this month influenced by last month)

**Spatial Data:**
- House prices in same neighborhood (similar prices)
- Pollution levels in nearby cities (correlated)

**Repeated Measurements:**
- Same person measured multiple times
- Same patient before/after treatment

**How to check:**
```python
# For time series: Plot residuals over time
plt.plot(residuals)
plt.xlabel('Time')
plt.ylabel('Residuals')
plt.title('Check for Autocorrelation')
plt.show()

# Look for: random scatter ✅
# Watch out for: patterns or trends ❌
```

**What to do if violated:**
1. **Use time series models** (ARIMA, SARIMA)
2. **Add time-based features** (day, month, season)
3. **Use specialized methods** (GLS, mixed models)

---

### 🎯 Assumption 3: Homoscedasticity (Constant Variance)

**What it means:** The spread of errors should be **constant** across all values.

**Simple explanation:** Your predictions should be equally accurate for small and large values.

**Example of HOMOSCEDASTICITY (Good!):**
```
Predicted Price  →  Error (Actual - Predicted)
$100k            →  ±$10k
$200k            →  ±$10k
$300k            →  ±$10k
$400k            →  ±$10k

Error spread is constant (±$10k) ✅
```

**Visual:**
```
Residuals
    │  ●  ●  ●  ●
    │ ● ● ● ● ● ●
  0 ├─────────────
    │ ● ● ● ● ● ●
    │  ●  ●  ●  ●
    └─────────────→ Predicted
    
Even spread at all levels = Homoscedasticity ✅
```

**Example of HETEROSCEDASTICITY (Bad!):**
```
Predicted Price  →  Error (Actual - Predicted)
$100k            →  ±$5k   (small error)
$200k            →  ±$10k  (medium error)
$300k            →  ±$20k  (large error)
$400k            →  ±$40k  (very large error)

Error spread increases with price! ❌
```

**Visual:**
```
Residuals
    │          ● ●
    │        ● ● ●
    │      ● ● ● ●
  0 ├─────────────
    │      ● ● ● ●
    │        ● ● ●
    │          ● ●
    └─────────────→ Predicted
    
Spread increases = Heteroscedasticity ❌
```

**Real-world example:**

Predicting house prices:
- Small houses ($100k): Errors are small (±$5k)
- Large houses ($1M): Errors are large (±$100k)

This makes sense! Expensive houses have more variability in price.

**How to check:**
```python
# Plot residuals vs predicted values
plt.scatter(y_pred, residuals)
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.axhline(y=0, color='r', linestyle='--')
plt.title('Residuals vs Predicted')
plt.show()

# Look for: even spread (rectangle shape) ✅
# Watch out for: funnel shape (cone) ❌
```

**What to do if violated:**
1. **Transform the target variable** (log, square root)
2. **Use weighted least squares**
3. **Use robust standard errors**

---

### 🎯 Assumption 4: Normality of Residuals

**What it means:** The errors (residuals) should follow a **normal distribution** (bell curve).

**Simple explanation:** Most errors should be small, with fewer large errors in both directions.

**Example of NORMAL residuals:**
```
Error Distribution:
-$20k: ●
-$15k: ●●
-$10k: ●●●●
 -$5k: ●●●●●●●●
   $0: ●●●●●●●●●●●●  (most common)
  $5k: ●●●●●●●●
 $10k: ●●●●
 $15k: ●●
 $20k: ●

Bell curve shape! ✅
```

**Visual:**
```
Frequency
    │     ╱╲
    │    ╱  ╲
    │   ╱    ╲
    │  ╱      ╲
    │ ╱        ╲
    └────────────→ Residuals
   -20  0  +20
   
Bell curve = Normal distribution ✅
```

**Example of NON-NORMAL residuals:**
```
Error Distribution:
-$50k: ●●●●●●●●●●  (many large negative errors)
-$25k: ●●●●
   $0: ●●●●●●●●●●●●
 $25k: ●●
 $50k: ●

Skewed to the left! ❌
```

**How to check:**
```python
import scipy.stats as stats

# Method 1: Histogram
plt.hist(residuals, bins=30, edgecolor='black')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Distribution of Residuals')
plt.show()

# Method 2: Q-Q Plot (Quantile-Quantile)
stats.probplot(residuals, dist="norm", plot=plt)
plt.title('Q-Q Plot')
plt.show()

# Look for: bell curve in histogram ✅
# Look for: points on diagonal line in Q-Q plot ✅
```

**What to do if violated:**
1. **Transform the target variable** (log, Box-Cox)
2. **Remove outliers** (if they're errors)
3. **Use robust regression methods**
4. **Note:** Violation is less critical with large sample sizes (Central Limit Theorem)

---

### 🎯 Assumption 5: No Multicollinearity

**What it means:** Features should **not be highly correlated** with each other.

**Simple explanation:** Don't use features that measure the same thing in different ways.

**Example of MULTICOLLINEARITY (Bad!):**
```
Features for predicting house price:
- Size in square feet: 2000
- Size in square meters: 185.8
- Number of rooms: 8

Problem: Square feet and square meters are the SAME thing!
They're perfectly correlated. ❌
```

**Another example:**
```
Predicting salary:
- Years of experience: 10
- Age: 35
- Years since graduation: 12

Problem: These are highly correlated!
Older people usually have more experience. ❌
```

**Why is this bad?**

1. **Unstable coefficients:** Small changes in data cause big changes in coefficients
2. **Hard to interpret:** Can't tell which feature is actually important
3. **Inflated standard errors:** Coefficients seem less significant than they are

**Real-world example:**

```python
# Bad model:
Price = 100 + 0.2×(sq_ft) + 0.5×(sq_meters)

# If you increase house size:
# - sq_ft goes up
# - sq_meters also goes up (they're the same!)
# - Model gets confused about which one matters

# Good model (remove one):
Price = 100 + 0.2×(sq_ft)
```

**How to check:**

**Method 1: Correlation Matrix**
```python
import seaborn as sns

# Calculate correlations
corr_matrix = X.corr()

# Visualize
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlation Matrix')
plt.show()

# Look for: values close to ±1 (high correlation) ❌
# Good: values close to 0 (low correlation) ✅
```

**Method 2: Variance Inflation Factor (VIF)**
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Calculate VIF for each feature
vif_data = pd.DataFrame()
vif_data["Feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

print(vif_data)

# VIF < 5: Low multicollinearity ✅
# VIF 5-10: Moderate multicollinearity ⚠️
# VIF > 10: High multicollinearity ❌
```

**What to do if violated:**
1. **Remove one of the correlated features**
2. **Combine correlated features** (average them)
3. **Use PCA** (Principal Component Analysis)
4. **Use regularization** (Ridge, Lasso - we'll cover this!)

---

## 2. Challenges and How to Fix Them {#challenges}

### 🔧 Challenge 1: Scaling and Interpretability

**The Problem:**

When features are on **different scales**, it's hard to compare their importance.

**Example:**
```
Predicting house price:
- Size: 2000 sq ft (large numbers)
- Bedrooms: 3 (small numbers)
- Age: 15 years (medium numbers)

Model:
Price = 50 + 0.2×Size + 30×Bedrooms - 1×Age
```

**Question:** Which feature is most important?

**You might think:** Bedrooms (coefficient = 30) is most important!

**But wait!**
- Size varies from 1000 to 4000 (range = 3000)
- Bedrooms vary from 1 to 5 (range = 4)
- Age varies from 0 to 50 (range = 50)

**The truth:**
```
Size impact: 0.2 × 3000 = $600k variation
Bedrooms impact: 30 × 4 = $120k variation
Age impact: 1 × 50 = $50k variation

Size is actually most important!
```

**The Solution: Scaling**

**Method 1: Standardization (Z-score normalization)**

**What it does:** Transforms features to have mean=0 and std=1

**Formula:**
```
X_scaled = (X - mean) / std
```

**Example:**
```
Original sizes: [1000, 2000, 3000, 4000]
Mean: 2500
Std: 1118

Scaled sizes:
1000 → (1000-2500)/1118 = -1.34
2000 → (2000-2500)/1118 = -0.45
3000 → (3000-2500)/1118 = +0.45
4000 → (4000-2500)/1118 = +1.34

Now all features are on the same scale!
```

**Python code:**
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Now coefficients are directly comparable!
```

**Method 2: Min-Max Scaling**

**What it does:** Scales features to range [0, 1]

**Formula:**
```
X_scaled = (X - min) / (max - min)
```

**Example:**
```
Original sizes: [1000, 2000, 3000, 4000]
Min: 1000
Max: 4000

Scaled sizes:
1000 → (1000-1000)/(4000-1000) = 0.0
2000 → (2000-1000)/(4000-1000) = 0.33
3000 → (3000-1000)/(4000-1000) = 0.67
4000 → (4000-1000)/(4000-1000) = 1.0
```

**Python code:**
```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

**When to use which?**

| Method | Use When | Pros | Cons |
|--------|----------|------|------|
| **Standardization** | Features have different units | Handles outliers better | Values can be outside [0,1] |
| **Min-Max** | Want bounded range [0,1] | Easy to interpret | Sensitive to outliers |

**Important Note:**

After scaling, you **cannot directly interpret** the coefficients in the original units!

**Example:**
```python
# Before scaling:
Price = 50 + 0.2×Size
# Interpretation: Each sq ft adds $200

# After scaling:
Price = 300 + 150×Size_scaled
# Interpretation: Each 1 std increase in size adds $150k
```

---

### 🔧 Challenge 2: Overfitting

**The Problem:**

Model learns the training data **too well**, including the noise and errors.

**Simple analogy:**

Imagine studying for a test:
- **Underfitting:** You barely study, don't understand the concepts
- **Good fit:** You understand the concepts, can apply to new problems
- **Overfitting:** You memorize every practice problem exactly, but can't solve new problems

**Example:**
```
Training data:
Size: 2000 sq ft → Price: $400k
Size: 2001 sq ft → Price: $350k (unusual, maybe a fixer-upper)

Overfit model learns:
"2000 sq ft = $400k, 2001 sq ft = $350k"

New data:
Size: 2001 sq ft → Predicts $350k (wrong! Should be ~$400k)

The model memorized the outlier instead of learning the pattern!
```

**How to detect:**
```python
# Train model
model.fit(X_train, y_train)

# Evaluate on both sets
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Training R²: {train_score:.3f}")
print(f"Test R²: {test_score:.3f}")

# Signs of overfitting:
# Training R² = 0.99 (excellent)
# Test R² = 0.60 (poor)
# Big gap = Overfitting! ❌
```

**Solutions:**

1. **Get more training data**
2. **Remove unnecessary features**
3. **Use regularization** (Ridge, Lasso - coming up!)
4. **Cross-validation**

---

### 🔧 Challenge 3: Outliers

**The Problem:**

Extreme values can **pull the regression line** away from the true pattern.

**Visual example:**
```
Without outlier:
Price
  │   ●
  │  ●
  │ ●
  │●
  └────→ Size
  
Good fit! ✅

With outlier:
Price
  │        ●  ← Outlier pulls line up!
  │   ●  /
  │  ● /
  │ ●/
  │●
  └────→ Size
  
Line is distorted! ❌
```

**Real example:**
```
House prices:
1000 sq ft: $200k
1500 sq ft: $300k
2000 sq ft: $400k
2500 sq ft: $500k
3000 sq ft: $2M  ← Outlier! (Maybe a mansion with ocean view)

The $2M house pulls the line up, making all predictions too high!
```

**How to detect:**
```python
# Method 1: Box plot
plt.boxplot(y)
plt.title('Detect Outliers in Target')
plt.show()

# Method 2: Z-score
from scipy import stats
z_scores = np.abs(stats.zscore(y))
outliers = np.where(z_scores > 3)[0]
print(f"Outliers at indices: {outliers}")

# Method 3: IQR method
Q1 = y.quantile(0.25)
Q3 = y.quantile(0.75)
IQR = Q3 - Q1
outliers = (y < Q1 - 1.5*IQR) | (y > Q3 + 1.5*IQR)
```

**Solutions:**

1. **Investigate:** Is it a data error or real?
2. **Remove:** If it's an error
3. **Transform:** Use log transformation to reduce impact
4. **Robust regression:** Use algorithms less sensitive to outliers
5. **Keep:** If it's real and important (like the mansion!)

---

## 3. Understanding Coefficients {#coefficients}

### 📊 What Do Coefficients Really Mean?

Coefficients tell you **how much the target changes** when a feature increases by 1 unit.

**Simple Linear Regression:**
```
Price = 50 + 0.2×Size

Intercept (β₀ = 50):
- When Size = 0, Price = $50k
- This is the "base price" (land, permits, etc.)

Slope (β₁ = 0.2):
- Each additional sq ft adds $0.2k ($200)
- 1000 sq ft → $50k + 0.2×1000 = $250k
- 2000 sq ft → $50k + 0.2×2000 = $450k
```

**Multiple Linear Regression:**
```
Price = 50 + 0.2×Size + 30×Bedrooms - 1×Age

β₀ = 50: Base price
β₁ = 0.2: Each sq ft adds $200 (holding bedrooms and age constant)
β₂ = 30: Each bedroom adds $30k (holding size and age constant)
β₃ = -1: Each year older subtracts $1k (holding size and bedrooms constant)
```

**Key phrase:** "Holding other features constant"

This means: When you change one feature, you keep all others the same.

**Example:**

Two houses:
```
House A: 2000 sq ft, 3 bedrooms, 10 years old
House B: 2000 sq ft, 4 bedrooms, 10 years old

Difference: Only bedrooms changed (3 → 4)
Price difference: $30k (the coefficient for bedrooms!)

Price_A = 50 + 0.2×2000 + 30×3 - 1×10 = 50 + 400 + 90 - 10 = $530k
Price_B = 50 + 0.2×2000 + 30×4 - 1×10 = 50 + 400 + 120 - 10 = $560k
Difference = $560k - $530k = $30k ✅
```

### 🎯 Interpreting Different Types of Features

**Continuous Features (Size, Age, Income):**
```
Coefficient = 0.2
Interpretation: "Each 1-unit increase in X leads to 0.2-unit increase in y"

Example: Each additional sq ft adds $200 to house price
```

**Binary Features (Has_Pool: 0 or 1):**
```
Coefficient = 50
Interpretation: "Having this feature adds 50 units to y"

Example: Having a pool adds $50k to house price
```

**Categorical Features (Location: Urban, Suburban, Rural):**
```
After one-hot encoding:
Is_Urban: coefficient = 100
Is_Suburban: coefficient = 50
Is_Rural: (reference category, coefficient = 0)

Interpretation:
- Urban houses cost $100k more than Rural (reference)
- Suburban houses cost $50k more than Rural
- Urban houses cost $50k more than Suburban ($100k - $50k)
```

---

## 4. Feature Engineering {#feature-engineering}

### 🛠️ Creating Better Features

Sometimes the raw features aren't enough. We need to **create new features** to capture patterns!

### Polynomial Features

**When to use:** When the relationship is curved, not straight.

**Example:**

Temperature vs Ice Cream Sales:
```
Temperature: 10°C → Sales: 100
Temperature: 20°C → Sales: 150
Temperature: 30°C → Sales: 250
Temperature: 40°C → Sales: 400

This is NOT linear! Sales accelerate as it gets hotter.
```

**Solution: Add polynomial features**

```python
from sklearn.preprocessing import PolynomialFeatures

# Original features: [Temperature]
# Polynomial features: [Temperature, Temperature²]

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Now model can learn:
# Sales = β₀ + β₁×Temp + β₂×Temp²
# Sales = 50 + 2×Temp + 0.1×Temp²
```

**Visual:**
```
Sales
  │         ●
  │      ●
  │   ●
  │ ●
  │●
  └─────→ Temperature

Curved relationship captured by polynomial!
```

### Interaction Features

**When to use:** When the effect of one feature **depends on** another feature.

**Example:**

Advertising effectiveness:
```
TV ads alone: Small effect
Online ads alone: Small effect
TV + Online together: HUGE effect! (synergy)
```

**Solution: Create interaction term**

```python
# Create interaction
X['TV_x_Online'] = X['TV_ads'] * X['Online_ads']

# Model:
Sales = β₀ + β₁×TV + β₂×Online + β₃×(TV × Online)
```

**Real example:**

House price:
```
Size effect depends on location!

Rural area:
- 1000 sq ft: $100k
- 2000 sq ft: $150k (only $50k more)

Urban area:
- 1000 sq ft: $300k
- 2000 sq ft: $500k ($200k more!)

Create interaction: Size × Is_Urban
```

### Log Transformations

**When to use:** When data is skewed or has exponential growth.

**Example:**

Income distribution:
```
Original income:
$30k, $40k, $50k, $60k, $100k, $500k, $1M

Very skewed! Most people earn $30-60k, few earn millions.
```

**Solution: Log transform**

```python
X['log_income'] = np.log(X['income'])

# Now more normally distributed:
# log($30k) = 10.3
# log($40k) = 10.6
# log($50k) = 10.8
# log($1M) = 13.8

# More evenly spaced!
```

**Interpretation after log:**
```
Model: Price = 100 + 50×log(Income)

Interpretation:
"A 1% increase in income leads to 0.5% increase in price"
(This is called elasticity in economics!)
```

---

## 5. Regularization {#regularization}

### 🎯 What is Regularization?

**The Problem:**

Complex models with many features can **overfit** - they memorize training data instead of learning patterns.

**The Solution:**

**Regularization** adds a **penalty** for having large coefficients. This forces the model to be simpler.

**Analogy:**

Imagine packing a suitcase:
- **No regularization:** Pack everything! (overfitting)
- **Regularization:** You have a weight limit, so pack only essentials (better generalization)

---

### 🔵 Ridge Regression (L2 Regularization)

**What it does:** Shrinks all coefficients toward zero, but doesn't eliminate any.

**Formula:**
```
Cost = Σ(y - ŷ)² + α×Σ(β²)
        ↑            ↑
   Fit the data   Penalty for large coefficients
```

**Key parameter: α (alpha)**
- α = 0: No penalty (regular linear regression)
- α = small: Light penalty
- α = large: Heavy penalty (coefficients shrink more)

**Example:**

```python
from sklearn.linear_model import Ridge

# Try different alpha values
alphas = [0.01, 0.1, 1, 10, 100]

for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train, y_train)
    
    print(f"Alpha = {alpha}")
    print(f"Coefficients: {ridge.coef_}")
    print(f"Test R²: {ridge.score(X_test, y_test):.3f}\n")

# Output:
# Alpha = 0.01: Coef = [0.20, 30.5, -1.2], R² = 0.75
# Alpha = 1:    Coef = [0.18, 25.0, -0.9], R² = 0.78 ← Better!
# Alpha = 100:  Coef = [0.05, 5.0, -0.1],  R² = 0.60 ← Too much!
```

**When to use Ridge:**
- Many correlated features
- Want to keep all features
- Prevent overfitting

**Pros:**
- ✅ Handles multicollinearity well
- ✅ Keeps all features
- ✅ Stable coefficients

**Cons:**
- ❌ Doesn't eliminate features (all stay in model)
- ❌ Less interpretable with many features

---

### 🔴 Lasso Regression (L1 Regularization)

**What it does:** Shrinks coefficients AND can set some to **exactly zero** (feature selection!).

**Formula:**
```
Cost = Σ(y - ŷ)² + α×Σ|β|
        ↑            ↑
   Fit the data   Penalty for large coefficients
```

**Key difference from Ridge:** Uses absolute value |β| instead of β²

**Example:**

```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=1)
lasso.fit(X_train, y_train)

print(f"Coefficients: {lasso.coef_}")
# Output: [0.15, 0, -0.8, 25.0, 0, 0, 18.5]
#              ↑         ↑  ↑
#         These features were eliminated!
```

**Feature Selection:**

Lasso automatically removes unimportant features by setting their coefficients to 0!

```python
# See which features were kept
feature_names = X.columns
important_features = feature_names[lasso.coef_ != 0]

print(f"Important features: {important_features}")
# Output: ['size', 'age', 'bedrooms', 'location_score']
```

**When to use Lasso:**
- Many features, want to select important ones
- Want a simpler, more interpretable model
- Suspect many features are irrelevant

**Pros:**
- ✅ Automatic feature selection
- ✅ More interpretable (fewer features)
- ✅ Prevents overfitting

**Cons:**
- ❌ Can be unstable with correlated features
- ❌ Might remove useful features

---

### 🟣 Elastic Net (Combination of Ridge + Lasso)

**What it does:** Combines both L1 and L2 penalties - gets benefits of both!

**Formula:**
```
Cost = Σ(y - ŷ)² + α×[r×Σ|β| + (1-r)×Σ(β²)]
                      ↑           ↑
                   Lasso      Ridge
```

**Two parameters:**
- **α (alpha):** Overall strength of regularization
- **r (l1_ratio):** Balance between Lasso and Ridge
  - r = 0: Pure Ridge
  - r = 1: Pure Lasso
  - r = 0.5: Equal mix

**Example:**

```python
from sklearn.linear_model import ElasticNet

elastic = ElasticNet(alpha=1, l1_ratio=0.5)
elastic.fit(X_train, y_train)

print(f"Coefficients: {elastic.coef_}")
print(f"Test R²: {elastic.score(X_test, y_test):.3f}")
```

**When to use Elastic Net:**
- Many correlated features
- Want some feature selection
- Best of both worlds!

---

### 📊 Comparing Regularization Methods

| Method | Penalty | Feature Selection | Best For |
|--------|---------|-------------------|----------|
| **Ridge** | L2 (β²) | No | Correlated features, keep all |
| **Lasso** | L1 (\|β\|) | Yes | Feature selection, sparse models |
| **Elastic Net** | L1 + L2 | Yes | Correlated features + selection |

**Visual comparison:**

```
Coefficients without regularization:
Feature 1: ████████████ 12.0
Feature 2: ██████████ 10.0
Feature 3: ████████ 8.0
Feature 4: ██ 2.0
Feature 5: █ 1.0

Ridge (α=1):
Feature 1: ████████ 8.0  (shrunk)
Feature 2: ██████ 6.0    (shrunk)
Feature 3: █████ 5.0     (shrunk)
Feature 4: █ 1.5         (shrunk)
Feature 5: █ 0.8         (shrunk)

Lasso (α=1):
Feature 1: ██████ 6.0    (shrunk)
Feature 2: ████ 4.0      (shrunk)
Feature 3: ██ 2.0        (shrunk)
Feature 4: 0             (eliminated!)
Feature 5: 0             (eliminated!)

Elastic Net (α=1, r=0.5):
Feature 1: ███████ 7.0   (shrunk)
Feature 2: █████ 5.0     (shrunk)
Feature 3: ███ 3.0       (shrunk)
Feature 4: █ 0.5         (shrunk)
Feature 5: 0             (eliminated!)
```

---

## 6. Complete Python Examples {#python-examples}

### Example 1: Checking Assumptions

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from scipy import stats

print("=" * 70)
print("LINEAR REGRESSION ASSUMPTIONS CHECK")
print("=" * 70)

# ============================================
# STEP 1: CREATE SAMPLE DATA
# ============================================
print("\n📊 Step 1: Creating sample data")

np.random.seed(42)
n_samples = 100

# Features
size = np.random.uniform(1000, 4000, n_samples)
bedrooms = np.random.randint(1, 6, n_samples)
age = np.random.uniform(0, 50, n_samples)

# Target (with some noise)
price = 50 + 0.2*size + 30*bedrooms - 1*age + np.random.normal(0, 20, n_samples)

# Create DataFrame
df = pd.DataFrame({
    'size': size,
    'bedrooms': bedrooms,
    'age': age,
    'price': price
})

print(f"Dataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())

# ============================================
# STEP 2: TRAIN MODEL
# ============================================
print("\n🤖 Step 2: Training model")

X = df[['size', 'bedrooms', 'age']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

print("✅ Model trained!")
print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_:.2f}")

# ============================================
# STEP 3: CHECK ASSUMPTION 1 - LINEARITY
# ============================================
print("\n📈 Step 3: Checking Linearity")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for i, col in enumerate(['size', 'bedrooms', 'age']):
    axes[i].scatter(X[col], y, alpha=0.5)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('price')
    axes[i].set_title(f'Price vs {col}')
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✅ Check: Do the relationships look linear?")
print("   If you see curves, consider polynomial features!")

# ============================================
# STEP 4: CHECK ASSUMPTION 3 - HOMOSCEDASTICITY
# ============================================
print("\n📊 Step 4: Checking Homoscedasticity")

y_pred = model.predict(X)
residuals = y - y_pred

plt.figure(figsize=(10, 6))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--', linewidth=2)
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot - Check for Homoscedasticity')
plt.grid(True, alpha=0.3)
plt.show()

print("✅ Check: Is the spread constant across all predicted values?")
print("   Look for: Even spread (rectangle) ✅")
print("   Watch out for: Funnel shape (cone) ❌")

# ============================================
# STEP 5: CHECK ASSUMPTION 4 - NORMALITY
# ============================================
print("\n📊 Step 5: Checking Normality of Residuals")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Histogram
axes[0].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Residuals')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Residuals')
axes[0].grid(True, alpha=0.3)

# Q-Q Plot
stats.probplot(residuals, dist="norm", plot=axes[1])
axes[1].set_title('Q-Q Plot')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("✅ Check: Do residuals follow a normal distribution?")
print("   Histogram should look like a bell curve")
print("   Q-Q plot points should be on the diagonal line")

# ============================================
# STEP 6: CHECK ASSUMPTION 5 - MULTICOLLINEARITY
# ============================================
print("\n📊 Step 6: Checking Multicollinearity")

# Correlation matrix
corr_matrix = X.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1)
plt.title('Feature Correlation Matrix')
plt.show()

print("\nCorrelation Matrix:")
print(corr_matrix)

print("\n✅ Check: Are features highly correlated?")
print("   Values close to ±1 indicate high correlation ❌")
print("   Values close to 0 indicate low correlation ✅")

# VIF
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data["Feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) 
                   for i in range(len(X.columns))]

print("\nVariance Inflation Factor (VIF):")
print(vif_data)
print("\nVIF Interpretation:")
print("  VIF < 5: Low multicollinearity ✅")
print("  VIF 5-10: Moderate multicollinearity ⚠️")
print("  VIF > 10: High multicollinearity ❌")

# ============================================
# STEP 7: MODEL EVALUATION
# ============================================
print("\n📊 Step 7: Model Evaluation")

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Training R²: {train_score:.3f}")
print(f"Test R²: {test_score:.3f}")
print(f"Difference: {abs(train_score - test_score):.3f}")

if abs(train_score - test_score) > 0.1:
    print("⚠️  Large gap between train and test scores!")
    print("   This suggests overfitting.")
else:
    print("✅ Train and test scores are similar - good generalization!")
```

### Example 2: Scaling and Regularization

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

print("=" * 70)
print("SCALING AND REGULARIZATION EXAMPLE")
print("=" * 70)

# ============================================
# STEP 1: CREATE DATA WITH DIFFERENT SCALES
# ============================================
print("\n📊 Step 1: Creating data with different scales")

np.random.seed(42)
n_samples = 200

# Features on VERY different scales
size = np.random.uniform(1000, 4000, n_samples)        # 1000-4000
bedrooms = np.random.randint(1, 6, n_samples)          # 1-5
age = np.random.uniform(0, 50, n_samples)              # 0-50
income = np.random.uniform(30000, 200000, n_samples)   # 30k-200k

# Target
price = (50 + 0.2*size + 30*bedrooms - 1*age + 0.001*income 
         + np.random.normal(0, 20, n_samples))

df = pd.DataFrame({
    'size': size,
    'bedrooms': bedrooms,
    'age': age,
    'income': income,
    'price': price
})

print("Feature scales:")
print(df.describe())

# ============================================
# STEP 2: TRAIN WITHOUT SCALING
# ============================================
print("\n🤖 Step 2: Training WITHOUT scaling")

X = df[['size', 'bedrooms', 'age', 'income']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model_unscaled = LinearRegression()
model_unscaled.fit(X_train, y_train)

print("\nCoefficients (unscaled):")
for feature, coef in zip(X.columns, model_unscaled.coef_):
    print(f"  {feature:12s}: {coef:10.4f}")

print("\n⚠️  Hard to compare! Features are on different scales.")

# ============================================
# STEP 3: TRAIN WITH SCALING
# ============================================
print("\n🤖 Step 3: Training WITH scaling")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_scaled = LinearRegression()
model_scaled.fit(X_train_scaled, y_train)

print("\nCoefficients (scaled):")
for feature, coef in zip(X.columns, model_scaled.coef_):
    print(f"  {feature:12s}: {coef:10.2f}")

print("\n✅ Now coefficients are directly comparable!")
print("   Larger absolute value = more important feature")

# Find most important feature
most_important_idx = np.argmax(np.abs(model_scaled.coef_))
most_important_feature = X.columns[most_important_idx]
print(f"\nMost important feature: {most_important_feature}")

# ============================================
# STEP 4: RIDGE REGRESSION
# ============================================
print("\n🔵 Step 4: Ridge Regression")

alphas = [0.01, 0.1, 1, 10, 100]
ridge_scores = []

print("\nTrying different alpha values:")
for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train_scaled, y_train)
    
    train_score = ridge.score(X_train_scaled, y_train)
    test_score = ridge.score(X_test_scaled, y_test)
    ridge_scores.append(test_score)
    
    print(f"\nAlpha = {alpha:6.2f}")
    print(f"  Train R²: {train_score:.3f}")
    print(f"  Test R²:  {test_score:.3f}")
    print(f"  Coefficients: {ridge.coef_.round(2)}")

# Plot alpha vs performance
plt.figure(figsize=(10, 6))
plt.semilogx(alphas, ridge_scores, 'o-', linewidth=2, markersize=8)
plt.xlabel('Alpha (Regularization Strength)')
plt.ylabel('Test R² Score')
plt.title('Ridge Regression: Alpha vs Performance')
plt.grid(True, alpha=0.3)
plt.show()

best_alpha_idx = np.argmax(ridge_scores)
best_alpha = alphas[best_alpha_idx]
print(f"\n✅ Best alpha: {best_alpha} (Test R² = {ridge_scores[best_alpha_idx]:.3f})")

# ============================================
# STEP 5: LASSO REGRESSION
# ============================================
print("\n🔴 Step 5: Lasso Regression (Feature Selection)")

lasso = Lasso(alpha=1)
lasso.fit(X_train_scaled, y_train)

print("\nLasso Coefficients:")
for feature, coef in zip(X.columns, lasso.coef_):
    status = "✅ KEPT" if coef != 0 else "❌ ELIMINATED"
    print(f"  {feature:12s}: {coef:10.4f}  {status}")

# Count features
n_features_kept = np.sum(lasso.coef_ != 0)
print(f"\nFeatures kept: {n_features_kept}/{len(X.columns)}")

test_score = lasso.score(X_test_scaled, y_test)
print(f"Test R²: {test_score:.3f}")

# ============================================
# STEP 6: ELASTIC NET
# ============================================
print("\n🟣 Step 6: Elastic Net (Best of Both)")

elastic = ElasticNet(alpha=1, l1_ratio=0.5)
elastic.fit(X_train_scaled, y_train)

print("\nElastic Net Coefficients:")
for feature, coef in zip(X.columns, elastic.coef_):
    status = "✅ KEPT" if coef != 0 else "❌ ELIMINATED"
    print(f"  {feature:12s}: {coef:10.4f}  {status}")

test_score = elastic.score(X_test_scaled, y_test)
print(f"Test R²: {test_score:.3f}")

# ============================================
# STEP 7: COMPARE ALL METHODS
# ============================================
print("\n📊 Step 7: Comparing All Methods")

models = {
    'Linear (unscaled)': model_unscaled,
    'Linear (scaled)': model_scaled,
    'Ridge': Ridge(alpha=best_alpha).fit(X_train_scaled, y_train),
    'Lasso': lasso,
    'Elastic Net': elastic
}

results = []
for name, model in models.items():
    if 'unscaled' in name:
        score = model.score(X_test, y_test)
    else:
        score = model.score(X_test_scaled, y_test)
    results.append({'Model': name, 'Test R²': score})

results_df = pd.DataFrame(results)
print("\nModel Comparison:")
print(results_df.to_string(index=False))

# Visualize
plt.figure(figsize=(10, 6))
plt.barh(results_df['Model'], results_df['Test R²'])
plt.xlabel('Test R² Score')
plt.title('Model Comparison')
plt.xlim(0, 1)
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()

print("\n✅ Analysis complete!")
```

---

## Summary

### Key Takeaways

**Assumptions:**
1. ✅ **Linearity:** Relationship should be linear (straight line)
2. ✅ **Independence:** Data points should be independent
3. ✅ **Homoscedasticity:** Constant variance of errors
4. ✅ **Normality:** Errors should be normally distributed
5. ✅ **No Multicollinearity:** Features shouldn't be highly correlated

**Challenges:**
- **Scaling:** Use StandardScaler or MinMaxScaler
- **Overfitting:** Use regularization or more data
- **Outliers:** Detect and handle appropriately

**Regularization:**
- **Ridge:** Shrinks coefficients, keeps all features
- **Lasso:** Shrinks coefficients, eliminates some features
- **Elastic Net:** Combination of Ridge and Lasso

**Best Practices:**
1. Always check assumptions first
2. Scale features when they're on different scales
3. Use regularization to prevent overfitting
4. Cross-validate to find best hyperparameters
5. Interpret coefficients carefully

---

**You're now a Linear Regression expert!** 🎉

Ready for more? Try these next:
- Polynomial Regression
- Logistic Regression (for classification)
- Decision Trees
- Random Forests

Happy learning! 📚🚀
