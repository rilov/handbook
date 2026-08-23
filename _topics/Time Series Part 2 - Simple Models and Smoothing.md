---
title: "Time Series Part 2 - Simple Models and Smoothing"
category: Time Series
order: 1
permalink: /topics/time-series-simple-models-smoothing/
tags:
  - time-series
  - naive-forecast
  - exponential-smoothing
  - holt-winters
  - forecasting
summary: "A beginner-friendly guide to the simplest time-series forecasting models: naive, mean, drift, seasonal naive, simple exponential smoothing, Holt's method, and Holt-Winters. Plus how the parameters are chosen."
date: 2026-08-23
---

# Time Series Part 2 - Simple Models and Smoothing

This part of the time series module covers the simplest forecasting models. These models are the first things you try before moving to more advanced tools. They are surprisingly useful, and they help you understand why more complex models are needed.

---

## 1. Session overview

In this guide we will learn:

- Why forecasting is different from normal supervised learning
- How to split a time series honestly
- The simplest forecasting benchmarks: naive, mean, drift, and seasonal naive
- Simple exponential smoothing for level only
- Holt's method for trend
- Holt-Winters for trend and seasonality
- How the smoothing parameters are chosen

By the end, you will be able to look at a time series and pick a reasonable first model.

---

## 2. Modelling essentials for time series

### Forecasting is not like normal prediction

In normal machine learning, you might predict house prices from features. The rows are independent: one house does not depend on the next.

In time series, the value at the next step depends on the values before it. The order of the data matters. You cannot shuffle the rows.

```
Normal ML: shuffle rows, split randomly

Time series: keep order, split by time

Past                              Future
[-----------------------------------|-----]
 training                           test
```

### Train-test split for time series

For a time series, the **test set is always at the end**. You train on the past and try to predict the future. Shuffling would let the model see the future, which is not allowed in real forecasting.

```python
import pandas as pd

# df has a datetime index and a 'value' column
# use the first 80% for training, the last 20% for testing
cutoff = int(len(df) * 0.8)
train = df.iloc[:cutoff]
test = df.iloc[cutoff:]
```

### One-step-ahead vs multi-step-ahead

A **one-step-ahead** forecast predicts the next point only. A **multi-step-ahead** forecast predicts several points into the future. Simple models are usually easier to understand one step at a time.

### Goodness of fit

For time series, the most common error is the difference between the actual value and the forecast:

```
Error = Actual - Forecast
```

Common accuracy measures are:

- **MAE (Mean Absolute Error):** average of the absolute errors.
- **RMSE (Root Mean Squared Error):** square root of the average squared error.
- **MAPE (Mean Absolute Percentage Error):** average percentage error.

Smaller values mean a better forecast.

---

## 3. Simple time series models

These are the simplest possible forecasts. They are useful as baselines. If a fancy model cannot beat a simple model, the fancy model is not useful.

### Naive forecast

The forecast for the next period is just the last observed value.

```
Forecast for t+1 = value at t
```

Example:

```
Actual: 10, 12, 14, 13, ?
Forecast for the next point: 13
```

The naive method is good for data with no strong trend or seasonality. It says, "tomorrow will look like today."

### Mean forecast

The forecast for the next period is the mean of all past values.

```
Forecast for t+1 = average of all observed values so far
```

Example:

```
Actual: 10, 12, 14, 13
Mean = (10 + 12 + 14 + 13) / 4 = 12.25
Forecast for the next point: 12.25
```

The mean forecast is good when the data is roughly flat and has no trend. It can be bad if the data is changing over time.

### Drift forecast

The drift method assumes the trend continues. It connects the first and last points and extends the line.

```
Forecast for t+h = last value + h × (last value - first value) / (number of points - 1)
```

Example:

```
Actual: 10, 11, 13, 16, ?
The trend from 10 to 16 over 3 steps is +2 per step.
Forecast for the next point: 16 + 2 = 18
```

The drift method is good when the data has a clear, roughly straight trend.

### Seasonal naive forecast

For data with a repeating pattern, the forecast for the next period is the value from the same season last year.

```
Forecast for t+1 = value at t - m
```

where `m` is the length of the season. For monthly data with a yearly pattern, `m = 12`.

Example:

```
Sales in January 2023: 100
Sales in February 2023: 110
Sales in March 2023: 120
...
Sales in January 2024: ?
Seasonal naive forecast for January 2024: 100
```

The seasonal naive method is good when the data has strong seasonality and the level does not change much.

---

## 4. Simple exponential smoothing

### The idea

All the simple methods above treat every past observation equally. But the most recent values are usually more useful for forecasting than old values. Simple exponential smoothing weights the most recent observations more heavily.

### The formula

```
Forecast for t+1 = α × actual at t + (1 - α) × previous forecast
```

`α` (alpha) is the **smoothing parameter**. It is a number between 0 and 1.

- If `α` is close to **1**, the forecast mostly uses the most recent value. It reacts quickly.
- If `α` is close to **0**, the forecast mostly uses the previous forecast. It is slow and smooth.

Example with `α = 0.2`:

```
Actual:    10, 12, 14, 13, ?
Forecast:  10, 10, 10.4, 11.12, ...

Step 2: 0.2 × 10 + 0.8 × 10 = 10
Step 3: 0.2 × 12 + 0.8 × 10 = 10.4
Step 4: 0.2 × 14 + 0.8 × 10.4 = 11.12
Step 5: 0.2 × 13 + 0.8 × 11.12 = 11.496
```

Simple exponential smoothing is good for data with **no trend and no seasonality**, just a level that changes slowly.

---

## 5. Holt's exponential smoothing

### The problem with simple exponential smoothing

Simple exponential smoothing cannot handle a trend. If the data is going up, the forecast always lags behind.

Holt's method adds a second component: the **trend**.

### The formula

It keeps two smoothed values:

- `l_t` the level at time `t`
- `b_t` the trend at time `t`

```
Level:   l_t = α × y_t + (1 - α) × (l_{t-1} + b_{t-1})
Trend:   b_t = β × (l_t - l_{t-1}) + (1 - β) × b_{t-1}
Forecast for h steps ahead: l_t + h × b_t
```

`α` controls how fast the level updates. `β` (beta) controls how fast the trend updates.

### Example

```
Actual:  10, 12, 15, 17, ?

Holt's method sees the level is rising and the trend is about +2 per step.
Forecast for the next step: 17 + 2 = 19
```

Holt's method is good for data with a **trend but no seasonality**.

---

## 6. Holt-Winters' exponential smoothing

### Adding seasonality

Holt-Winters extends Holt's method by adding a third component: the **seasonal effect**.

It keeps three components:

- `l_t` the level
- `b_t` the trend
- `s_t` the seasonal factor

### Additive vs multiplicative seasonality

The seasonal effect can be combined in two ways:

**Additive** (the same size every year):

```
Forecast = (l_t + h × b_t) + s_{t+m}
```

**Multiplicative** (the size scales with the level):

```
Forecast = (l_t + h × b_t) × s_{t+m}
```

Use **additive** when the seasonal swings stay the same size. Use **multiplicative** when the swings grow as the series grows.

### The formula (additive version)

```
Level:    l_t = α × (y_t - s_{t-m}) + (1 - α) × (l_{t-1} + b_{t-1})
Trend:    b_t = β × (l_t - l_{t-1}) + (1 - β) × b_{t-1}
Seasonal: s_t = γ × (y_t - l_t) + (1 - γ) × s_{t-m}

Forecast h steps ahead: l_t + h × b_t + s_{t+h-m}
```

`γ` (gamma) is the seasonal smoothing parameter. It is also between 0 and 1.

Example with monthly sales and a yearly pattern (`m = 12`):

```
Current level: 1,000
Current trend: +50 per month
Seasonal factor for December: +200

Forecast for next December: 1,000 + (12 × 50) + 200 = 1,800
```

Holt-Winters is good for data with a **trend and a seasonal pattern**.

---

## 7. How the parameters are determined

For simple, Holt, and Holt-Winters methods, we need to choose the smoothing parameters `α`, `β`, and `γ`. The parameters are usually chosen by trying many values and picking the ones that give the smallest forecast error.

### Two common approaches

1. **Grid search:** try a fixed set of values, such as `0.1, 0.2, 0.3, ..., 0.9`, and pick the combination with the lowest error on a validation set.
2. **Optimisation:** use a numerical optimiser to find the values that minimise the error automatically.

### What error is minimised?

Usually the **sum of squared errors (SSE)** or the **mean squared error (MSE)** on the training or validation set. The idea is the same: find the parameters that make the model's one-step-ahead forecasts as close as possible to the actual values.

```
SSE = (actual_1 - forecast_1)^2 + (actual_2 - forecast_2)^2 + ... + (actual_n - forecast_n)^2
```

### The process

```
1. Start with initial guesses for α, β, γ
2. Run the model over the training data
3. Compute the forecast errors
4. Adjust the parameters to make the errors smaller
5. Repeat until the error cannot get much smaller
```

In Python, libraries like `statsmodels` do this automatically.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=12
)
fit = model.fit()
forecast = fit.forecast(12)
```

`fit()` automatically picks the `α`, `β`, and `γ` values that minimise the error.

---

## 8. One-sentence takeaway

**Start with the simplest model that matches your data: use the naive for flat data, Holt's for trend, and Holt-Winters for trend plus seasonality, and let the library fit the smoothing parameters for you.**
