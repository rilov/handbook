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

#### Worked example: one-step-ahead

Imagine weekly sales:

```
Week:    1   2   3   4   5   6
Sales:  10  12  11  13  12   ?
```

A one-step-ahead forecast for week 6 uses the data up to week 5:

```
Forecast for week 6 = some function of (10, 12, 11, 13, 12)
```

Once week 6 is over and the real value is known, you update the model and forecast week 7.

A multi-step-ahead forecast for weeks 6, 7, and 8 uses the data up to week 5:

```
Forecast for week 6 = function of (10, 12, 11, 13, 12)
Forecast for week 7 = function of (10, 12, 11, 13, 12, forecast for week 6)
Forecast for week 8 = function of (10, 12, 11, 13, 12, forecast for week 6, forecast for week 7)
```

The further ahead you forecast, the more uncertainty you accumulate.

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

#### Worked example: all four simple forecasts on the same data

Weekly sales with a steady level:

```
Week:    1   2   3   4   5   6
Sales:  20  22  21  23  22   ?
```

- **Naive forecast for week 6:** 22 (last value)
- **Mean forecast for week 6:** (20 + 22 + 21 + 23 + 22) / 5 = 21.6
- **Drift forecast for week 6:** trend = (22 - 20) / 4 = +0.5 per week. Forecast = 22 + 0.5 = 22.5
- **Seasonal naive (season = 4 weeks) for week 6:** take the value from 4 weeks ago, week 2. Forecast = 22

These forecasts are close because the series is flat. The real value of each method shows up when the series has trend or seasonality.

#### Which simple model should you use?

| What the data looks like | Try this first |
|---|---|
| Flat, no pattern | Mean or naive |
| Flat with repeating season | Seasonal naive |
| Rising or falling trend | Drift |
| Trend plus season | Holt-Winters |

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

#### Worked example with a table

Daily demand:

```
Day:    1    2    3    4    5    ?
Actual: 100  105  103  108  107
```

Use `α = 0.3` and set the first forecast to the first actual value.

```
Day 1: Forecast = 100 (initialisation)
Day 2: Forecast = 0.3 × 100 + 0.7 × 100 = 100
       Actual = 105
       Error   = 105 - 100 = 5
Day 3: Forecast = 0.3 × 105 + 0.7 × 100 = 101.5
       Actual = 103
       Error   = 103 - 101.5 = 1.5
Day 4: Forecast = 0.3 × 103 + 0.7 × 101.5 = 101.95
       Actual = 108
       Error   = 108 - 101.95 = 6.05
Day 5: Forecast = 0.3 × 108 + 0.7 × 101.95 = 103.77
       Actual = 107
       Error   = 107 - 103.77 = 3.23
Day 6: Forecast = 0.3 × 107 + 0.7 × 103.77 = 104.74
```

The forecast is a smooth middle value. It never jumps all the way to the latest observation unless `α = 1`.

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

#### Worked example: Holt's method step by step

Monthly app downloads:

```
Month:     1    2    3    4    5    ?
Downloads: 100  120  140  160  180
```

Use `α = 0.4` and `β = 0.2`. Initialise the level to the first value, `100`, and the trend to the average difference between the first few points, `20`.

```
Month 1: l_1 = 100,  b_1 = 20

Month 2: l_2 = 0.4 × 120 + 0.6 × (100 + 20) = 48 + 72 = 120
         b_2 = 0.2 × (120 - 100) + 0.8 × 20 = 4 + 16 = 20

Month 3: l_3 = 0.4 × 140 + 0.6 × (120 + 20) = 56 + 84 = 140
         b_3 = 0.2 × (140 - 120) + 0.8 × 20 = 4 + 16 = 20

Month 4: l_4 = 0.4 × 160 + 0.6 × (140 + 20) = 64 + 96 = 160
         b_4 = 0.2 × (160 - 140) + 0.8 × 20 = 4 + 16 = 20

Month 5: l_5 = 0.4 × 180 + 0.6 × (160 + 20) = 72 + 108 = 180
         b_5 = 0.2 × (180 - 160) + 0.8 × 20 = 4 + 16 = 20

Forecast for month 6: l_5 + 1 × b_5 = 180 + 20 = 200
```

Because the data is a perfect straight line with `+20` per month, the model quickly learns the correct level and trend.

In real life the trend is not so clean, so `b_t` changes slightly each month.

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

#### Worked example: additive Holt-Winters

Quarterly sales show a trend of `+10` per quarter and a seasonal pattern that repeats every 4 quarters.

```
Quarter: 1   2   3   4   5   6   7   8
Sales:  110 125  95 140 125 140 110 155
```

The series has:

- an upward trend
- a clear seasonal spike in quarter 4

A simplified additive forecast for quarter 9 is:

```
Current level (after quarter 8): 155
Current trend: +10 per quarter
Seasonal factor for quarter 1 (same season as quarter 5 and 9): +0

Forecast for quarter 9 = 155 + 10 + 0 = 165

For quarter 12 (same season as quarter 4 and 8):
Seasonal factor for quarter 4: +25 (roughly, because quarter 4 is always the biggest)

Forecast for quarter 12 = 155 + (4 × 10) + 25 = 220
```

This is a hand-waved example. In practice, `statsmodels` estimates the level, trend, and all four seasonal factors automatically from the data.

#### Additive vs multiplicative: when to use each

| Data pattern | Use |
|---|---|
| Seasonal peaks stay the same absolute size | Additive |
| Seasonal peaks grow as the series grows | Multiplicative |

Example: ice-cream sales.

- A small shop sells 100 cones, summer adds 30 → additive seasonality of `+30`.
- Later the shop sells 1,000 cones. If summer still adds about 30% more, the seasonal effect is `×1.3` → multiplicative.

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

#### Worked example: choosing alpha by grid search

Imagine testing `α` for simple exponential smoothing on the daily demand series. You hold out the last three days and try different `α` values.

```
Training: 100, 105, 103, 108, 107
Test:     106, 104, 109
```

Try `α = 0.1`, `0.3`, and `0.7`:

| α | Forecasts for test | MAE on test |
|---|---|---|
| 0.1 | 102.6, 102.9, 103.0 | 5.2 |
| 0.3 | 104.7, 105.0, 104.6 | 2.9 |
| 0.7 | 107.0, 106.3, 106.0 | 2.0 |

`α = 0.7` gives the lowest MAE on the held-out test set. So that is the best value for this data.

This is the same idea `statsmodels.fit()` does, but automatically across all three parameters.

---

## 8. One-sentence takeaway

**Start with the simplest model that matches your data: use the naive for flat data, Holt's for trend, and Holt-Winters for trend plus seasonality, and let the library fit the smoothing parameters for you.**
