---
title: "Time Series Part 3 - Autoregressive Models and Stationarity"
category: Time Series
order: 2
permalink: /topics/time-series-autoregressive-stationarity/
tags:
  - time-series
  - autoregressive
  - stationarity
  - adf
  - kpss
  - acf
  - pacf
  - differencing
summary: "A beginner-friendly guide to autoregressive models, stationarity tests, handling non-stationarity, and autocorrelation measures (ACF and PACF)."
date: 2026-08-23
---

# Time Series Part 3 - Autoregressive Models and Stationarity

This part of the time series module moves from smoothing to models that use the past to predict the future. We will learn what an autoregressive model is, why stationarity matters, how to test for it, how to fix non-stationary data, and how to read ACF and PACF plots.

---

## 1. Session overview

In this guide we will learn:

- What an autoregressive (AR) model is
- Why AR models need stationary data
- How to test for stationarity visually and with statistical tests
- How to make a non-stationary series stationary
- What autocorrelation, ACF, and PACF are
- How to use ACF and PACF to choose the right AR model

---

## 2. Introduction to autoregressive models

### The basic idea

An **autoregressive** model uses past values of the series to predict the next value. The word "regressive" comes from regression, and "auto" means on itself. So the model **regresses the series on its own past**.

### AR(1)

The simplest model is AR(1): the value today depends on the value yesterday plus some noise.

```
y_t = c + φ × y_{t-1} + ε_t
```

- `y_t` is the value at time `t`
- `c` is a constant (the baseline level)
- `φ` (phi) is a parameter that says how much yesterday matters
- `y_{t-1}` is the value one step ago
- `ε_t` is random noise

Example:

```
y_t = 2 + 0.8 × y_{t-1} + noise
```

If yesterday's value was 10, the model predicts roughly `2 + 0.8 × 10 = 10` today, plus a small random wiggle.

#### Worked example: generating an AR(1) series

Imagine the process is:

```
y_t = 5 + 0.6 × y_{t-1} + ε_t
```

The noise `ε_t` is small random numbers with mean 0.

Start with `y_0 = 12`. The next values are:

```
y_1 = 5 + 0.6 × 12 + ε_1 = 12.2 + small noise
y_2 = 5 + 0.6 × y_1 + ε_2
y_3 = 5 + 0.6 × y_2 + ε_3
```

```
Time:    0    1     2      3      4      5
Value:  12  12.2  12.3   12.4   12.4   12.4
```

Because `0.6` is less than 1, the effect of the starting value `12` dies out and the series settles around its long-run mean of about `12.5`.

The long-run mean is:

```
mean = c / (1 - φ) = 5 / (1 - 0.6) = 12.5
```

This is why the condition `|φ| < 1` is important. If `φ = 1`, the series has a unit root and is non-stationary. If `φ > 1`, the series explodes.

### AR(p)

An **AR(p)** model uses the last `p` values:

```
y_t = c + φ_1 × y_{t-1} + φ_2 × y_{t-2} + ... + φ_p × y_{t-p} + ε_t
```

For example, AR(2) uses yesterday and the day before:

```
y_t = c + φ_1 × y_{t-1} + φ_2 × y_{t-2} + ε_t
```

The number `p` is called the **order** of the model. AR(1), AR(2), and AR(3) are just AR models with different orders.

### When can we use an AR model?

AR models work well when:

- The data is **stationary** (mean and variance are constant over time)
- The relationship between today and the past is roughly linear
- You have enough historical data to estimate the parameters

If the data is not stationary, the AR model can give strange or useless results.

#### An intuitive example

Consider two versions of the same daily temperature series.

**Version A is stationary:**

```
Day:   1   2   3   4   5   6   7
Temp: 20  22  19  21  20  23  21
```

The mean is about 21. The relationship between today's temperature and yesterday's temperature is the same everywhere.

**Version B is non-stationary:**

```
Day:   1   2   3   4   5   6   7
Temp: 20  25  31  38  46  55  65
```

Each day is warmer. A single AR(1) parameter cannot describe today-to-tomorrow for the whole series because the relationship changes as the level rises.

You must remove the trend before fitting an AR model.

---

## 3. Stationarity tests

### Why stationarity matters

An AR model assumes that the relationship between `y_t` and `y_{t-1}` is the same everywhere in the series. If the mean is changing, the relationship is changing. The model cannot learn a single set of parameters that works for the whole series.

```
Non-stationary: the mean is rising
   /
  /
 /
/

Here, y_t depends on y_{t-1} differently at the start than at the end.

Stationary: the mean is flat
  /\  /\  /\  /\  /\  
 /  \/  \/  \/  \/  \

Here, the relationship between y_t and y_{t-1} is the same everywhere.
```

### Visual check

The simplest test is to look at the plot:

- Is the **center** roughly flat?
- Is the **spread** roughly the same?
- Are the **waves** the same size?

If the answer to all three is yes, the series is probably stationary.

### Statistical tests

#### Augmented Dickey-Fuller (ADF) test

The ADF test checks whether a unit root is present. A unit root usually means the series is non-stationary.

```
Null hypothesis: the series has a unit root (non-stationary)
Alternative hypothesis: the series is stationary
```

If the **p-value is small** (for example, less than 0.05), we reject the null hypothesis and say the series is stationary.

```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(df["value"])
print("p-value:", result[1])
```

#### KPSS test

The KPSS test has the opposite logic:

```
Null hypothesis: the series is stationary
Alternative hypothesis: the series is non-stationary
```

If the **p-value is small**, we reject the null hypothesis and say the series is non-stationary.

```python
from statsmodels.tsa.stattools import kpss

result = kpss(df["value"])
print("p-value:", result[1])
```

It is good practice to use both tests. If they disagree, you need to look more carefully at the plot.

#### Worked example: interpreting the tests

A stock price series gives:

- **ADF p-value = 0.02**
- **KPSS p-value = 0.04**

What do we conclude?

- ADF: small p-value → reject the null of a unit root → the series looks stationary.
- KPSS: small p-value → reject the null of stationarity → the series looks non-stationary.

This is a contradiction. The series might be close to the borderline, or there might be a slow trend. Look at the plot before deciding. If a plot shows a wandering pattern, treat the series as non-stationary and try differencing.

If both tests agreed:

- ADF p-value < 0.05 and KPSS p-value > 0.05 → stationary.
- ADF p-value > 0.05 and KPSS p-value < 0.05 → non-stationary.

---

## 4. Dealing with non-stationarity

If a series is not stationary, you can transform it. The goal is to remove the trend or stabilise the variance.

### Differencing

**Differencing** replaces each value with the difference between it and the previous value.

```
y'_t = y_t - y_{t-1}
```

Example:

```
Original:  10, 12, 15, 17, 20, 22
Differenced: 2, 3, 2, 3, 2
```

If the data has a trend, differencing often makes it stationary. If one round of differencing is not enough, you can difference again.

#### Worked example: first differencing

```
Day:     1   2   3   4   5   6   7
Sales:  10  12  15  17  20  22  25

Differenced:
Day 2: 12 - 10 = 2
Day 3: 15 - 12 = 3
Day 4: 17 - 15 = 2
Day 5: 20 - 17 = 3
Day 6: 22 - 20 = 2
Day 7: 25 - 22 = 3
```

The differenced series is `2, 3, 2, 3, 2, 3`. It is now flat around `2.5`.

#### Worked example: second differencing

If the first difference is itself trending, difference again.

```
Day:     1   2   3   4   5   6   7
Sales:   2   5   9  14  20  27  35

First difference:
Day 2: 5 - 2 = 3
Day 3: 9 - 5 = 4
Day 4: 14 - 9 = 5
Day 5: 20 - 14 = 6
Day 6: 27 - 20 = 7
Day 7: 35 - 27 = 8

First difference: 3, 4, 5, 6, 7, 8  (still increasing)

Second difference:
4 - 3 = 1
5 - 4 = 1
6 - 5 = 1
7 - 6 = 1
8 - 7 = 1

Second difference: 1, 1, 1, 1, 1 (flat and stationary)
```

A second difference means you are looking at the change of the change. You rarely need more than two rounds.

```python
df["diff"] = df["value"].diff().dropna()
```

### Log transform

If the **variance** is growing with the level, take the **log** of the values. This compresses large values and stabilises the spread.

```python
import numpy as np

df["log_value"] = np.log(df["value"])
```

### Detrending

If the data has a clear straight or smooth trend, you can fit a trend line and subtract it.

```
y'_t = y_t - trend_t
```

### Deseasonalising

If the data has a strong repeating pattern, you can estimate the seasonal effect for each season and subtract it.

```
y'_t = y_t - seasonal_t
```

### Summary of fixes

| Problem | Fix |
|---|---|
| Trend | Differencing or detrending |
| Growing variance | Log or square-root transform |
| Seasonality | Seasonal differencing or deseasonalising |

---

## 5. Autocorrelation measures

### What is autocorrelation?

**Autocorrelation** is the correlation of a series with itself at different time lags. It tells you how much today's value is related to yesterday's value, the day before's, and so on.

```
Lag 1 autocorrelation: correlation of y_t with y_{t-1}
Lag 2 autocorrelation: correlation of y_t with y_{t-2}
```

If lag 1 autocorrelation is high, yesterday is a good predictor of today.

### ACF: Autocorrelation Function

The **ACF** shows the autocorrelation for many lags.

```
ACF plot:

lag 1:  ***
lag 2:  **
lag 3:  *
lag 4:  .
lag 5:  .
```

For a stationary AR(1) process, the ACF usually decays gradually:

```
lag 1: ******
lag 2: *****
lag 3: ****
lag 4: ***
lag 5: **
lag 6: *
```

For seasonal data, the ACF has spikes at the seasonal lag (for example, lag 12 for monthly data with a yearly pattern).

```
spikes at lag 12, 24, 36...

lag 12:  ******
lag 24:  *****
lag 36:  ****
```

### PACF: Partial Autocorrelation Function

The **PACF** is the correlation at a particular lag after removing the effect of the lags in between. It tells you whether that specific lag adds any new information.

For an AR(1) process, the PACF usually has a single significant spike at lag 1:

```
lag 1: ******
lag 2: .
lag 3: .
lag 4: .
```

For an AR(2) process, the PACF has significant spikes at lag 1 and lag 2, then drops to zero.

```
lag 1: ******
lag 2: *****
lag 3: .
lag 4: .
```

### How to use ACF and PACF to choose the AR order

A simple rule of thumb:

- Look at the **PACF** to choose the order `p` of an AR model.
- The number of significant spikes in the PACF often tells you what `p` should be.
- If the PACF drops to zero after lag 2, try AR(2).

#### Worked example: reading ACF and PACF

Daily temperature with a one-day memory pattern:

```
Day:  1   2   3   4   5   6   7
Temp: 20  22  19  21  20  23  21
```

Imagine the ACF and PACF plots look like this:

```
ACF:
Lag 1: 0.85  (high)
Lag 2: 0.70  (still high)
Lag 3: 0.55
Lag 4: 0.40
Lag 5: 0.30

PACF:
Lag 1: 0.85  (high)
Lag 2: 0.05  (near zero)
Lag 3: 0.00
Lag 4: 0.00
Lag 5: 0.00
```

What does this mean?

- The **ACF** decays slowly, which is typical for an AR(1) process. Today's temperature is related to yesterday, yesterday's to the day before, and so on.
- The **PACF** has one big spike at lag 1 and then drops. That means only the previous day has a direct effect. The relationship at lag 2 is just a knock-on from lag 1.

The pattern "ACF decays, PACF cuts off after lag 1" suggests an **AR(1)** model.

For an AR(2), you would see:

```
ACF:
Lag 1: 0.80
Lag 2: 0.65
Lag 3: 0.50
Lag 4: 0.35
Lag 5: 0.25

PACF:
Lag 1: 0.80
Lag 2: 0.40
Lag 3: 0.02
Lag 4: 0.00
```

The PACF cuts off after lag 2, so try AR(2).

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plot_acf(df["value"])
plot_pacf(df["value"])
```

---

## 6. Building an AR model in Python

Once the series is stationary and you have chosen the order `p`, you can fit the model.

```python
from statsmodels.tsa.ar_model import AutoReg

# Fit an AR(2) model
model = AutoReg(train, lags=2)
fit = model.fit()
print(fit.summary())

# Forecast the next 12 steps
forecast = fit.predict(start=len(train), end=len(train) + 11)
```

The `summary` shows the estimated `φ` values, the constant `c`, and the p-values. If the p-values are small, the lags are useful predictors.

---

## 7. Session summary

- An **autoregressive** model uses past values of the series to predict the future.
- AR models need the data to be **stationary**.
- Use **visual checks** and tests like **ADF** and **KPSS** to decide whether a series is stationary.
- If the data is not stationary, use **differencing**, **log transforms**, **detrending**, or **deseasonalising**.
- **ACF** shows how the series correlates with itself at different lags.
- **PACF** shows the direct relationship at a particular lag.
- Use the **PACF** to choose the order `p` of an AR model.

---

## 8. One-sentence takeaway

**An AR model predicts the future from the past, but only after you have made the series stationary and used ACF/PACF to choose how many past values to include.**
