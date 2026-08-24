---
title: "Time Series Part 4 - ARMA, ARIMA and SARIMA"
category: Time Series
order: 3
permalink: /topics/time-series-arma-arima-sarima/
tags:
  - time-series
  - arma
  - arima
  - sarima
  - forecasting
  - stationarity
  - differencing
summary: "A beginner-friendly guide to Moving Average, ARMA, ARIMA, and SARIMA models, with a worked example using a simple synthetic sales dataset."
date: 2026-08-23
---

# Time Series Part 4 - ARMA, ARIMA and SARIMA

In Part 3, you learned how **AR** models use past values of the series to predict the next value. This part adds the missing pieces:

- **MA** models use past forecast errors.
- **ARMA** combines AR and MA.
- **ARIMA** adds differencing to handle trends.
- **SARIMA** adds seasonal differencing to handle repeating patterns.

By the end, you will be able to read the order `(p, d, q)(P, D, Q)m` and fit a model in Python.

---

## 1. Moving Average (MA) models

A **Moving Average** model does not use past values of the series. It uses past **shocks** (the unpredictable bits, also called errors or residuals).

An **MA(1)** model looks like this:

```
y_t = c + e_t + θ * e_{t-1}
```

- `y_t` is the value at time `t`
- `c` is a constant
- `e_t` is the random shock at time `t`
- `e_{t-1}` is the previous shock
- `θ` is the weight of the previous shock

### A tiny worked example

Imagine a lemonade stand. Sales are normally 50 cups a day. On Monday, there is an unexpected surprise: a school group visits and buys an extra 10 cups (`e_t = +10`). That shock also spills into Tuesday because the stand runs out of cups early and cannot serve a few customers.

Let `c = 50`, `θ = 0.4`, and the random shocks be:

| Day | Shock `e_t` |
|-----|-------------|
| 1   | 0           |
| 2   | 10          |
| 3   | 0           |

Then:

- `y_1 = 50 + 0 + 0.4 * 0 = 50`
- `y_2 = 50 + 10 + 0.4 * 0 = 60` (the shock on day 2 has not yet appeared in `e_{t-1}`)
- `y_3 = 50 + 0 + 0.4 * 10 = 54` (the old shock is still affecting sales one day later)

So an MA model has **short-term memory**: a shock affects the next few periods and then disappears.

### How to spot an MA(q) process

- The **ACF cuts off sharply** after lag `q`.
- The **PACF tails off gradually**.

That is the opposite of an AR(p) process. In AR, the PACF cuts off and the ACF tails off.

---

## 2. ARMA(p, q)

**ARMA(p, q)** simply combines the two ideas:

- `p` is the AR part: how many past values of the series are used.
- `q` is the MA part: how many past shocks are used.

A common shorthand is:

```
y_t = c + φ_1 y_{t-1} + ... + φ_p y_{t-p} + e_t + θ_1 e_{t-1} + ... + θ_q e_{t-q}
```

### Choosing p and q from the data

A practical recipe is:

1. Plot the series and the ACF/PACF.
2. If the series is already stationary:
   - `p` ≈ the last significant lag in the **PACF**.
   - `q` ≈ the last significant lag in the **ACF**.
3. Try a few nearby combinations and compare `AIC` or forecast error.

---

## 3. ARIMA(p, d, q)

Many real series are **not** stationary. They have a trend. **ARIMA** adds one more parameter, `d`, which stands for the number of times you need to **difference** the series to make it stationary.

- `p` = AR order
- `d` = number of differences
- `q` = MA order

If `d = 0`, ARIMA is the same as ARMA. If `d = 1`, you fit the model to `y_t - y_{t-1}`.

### A tiny worked example

A savings account grows like this:

```
Balance: 100, 105, 112, 118, 125, 131, ...
```

The balance itself has a trend, so it is not stationary. If you look at the weekly **changes** instead:

```
Differences: 5, 7, 6, 7, 6, ...
```

Those differences are roughly flat. So `d = 1` is a good starting point.

### Building an ARIMA model

1. Check stationarity with an ADF or KPSS test.
2. If the series is not stationary, apply differencing (`d = 1` or more).
3. On the differenced series, use ACF/PACF to pick `p` and `q`.
4. Fit the model and check residuals.
5. Forecast and transform the result back to the original scale if needed.

---

## 4. SARIMA(p,d,q)(P,D,Q)m

**SARIMA** adds a seasonal ARIMA model on top of the regular ARIMA model. The full order is written as `(p, d, q)(P, D, Q)m`.

| Letter | Meaning | Example |
|--------|---------|---------|
| `p` | non-seasonal AR order | `p = 1` uses `y_{t-1}` |
| `d` | non-seasonal differencing | `d = 1` removes trend |
| `q` | non-seasonal MA order | `q = 1` uses `e_{t-1}` |
| `P` | seasonal AR order | `P = 1` uses `y_{t-m}` |
| `D` | seasonal differencing | `D = 1` removes yearly pattern |
| `Q` | seasonal MA order | `Q = 1` uses `e_{t-m}` |
| `m` | number of periods per season | `m = 12` for monthly data |

### How to read it

`(1, 1, 1)(1, 1, 1)12` for monthly data means:

- The series is differenced once to remove trend (`d = 1`).
- It is also seasonally differenced once at lag 12 to remove the yearly pattern (`D = 1`, `m = 12`).
- We use one non-seasonal AR term (`p = 1`), one non-seasonal MA term (`q = 1`).
- We use one seasonal AR term at lag 12 (`P = 1`) and one seasonal MA term at lag 12 (`Q = 1`).

### Choosing the seasonal orders

1. Look at the ACF at seasonal lags: 12, 24, 36 for monthly data.
2. If a seasonal lag is significant, try `P` or `Q` at that lag.
3. Use seasonal differencing `D` if the seasonal pattern itself is changing over time.
4. Compare models using `AIC`, `BIC`, or forecast error.

---

## 5. Worked example: monthly hot-chocolate sales

We will build a SARIMA model for a small mountain café that sells hot chocolate. The café is busier in winter and grows a little each year.

### Step 1: make the data

You can generate a similar dataset in Python.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 4 years of monthly hot-chocolate sales
np.random.seed(42)
n = 48
time = np.arange(1, n + 1)

trend = 2 + 0.2 * time
seasonal = 30 * np.sin(2 * np.pi * time / 12) + 15 * np.cos(2 * np.pi * time / 12)
noise = np.random.normal(0, 4, n)

sales = 100 + trend + seasonal + noise

idx = pd.date_range('2020-01-01', periods=n, freq='MS')
df = pd.DataFrame({'sales': sales}, index=idx)

# Plot the series
df['sales'].plot(title='Monthly hot-chocolate sales')
plt.show()
```

This series has a trend and a yearly seasonal pattern, so SARIMA is a natural choice.

### Step 2: check stationarity

```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(df['sales'])
print('ADF p-value:', result[1])
```

If the p-value is large (for example, greater than 0.05), the series is not stationary. That is expected here because of the trend and the seasonality.

### Step 3: difference the series

We remove both the trend and the yearly pattern. For monthly data with season length `m = 12`:

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Optional: visualise the parts
decompose = seasonal_decompose(df['sales'], model='additive', period=12)
decompose.plot()
plt.show()
```

### Step 4: decide the orders from ACF and PACF

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings
warnings.filterwarnings('ignore')

fig, ax = plt.subplots(2, 1, figsize=(10, 8))
plot_acf(df['sales'], lags=24, ax=ax[0])
plot_pacf(df['sales'], lags=24, ax=ax[1], method='ywm')
plt.show()
```

In this synthetic example:

- The **ACF** decays slowly because the series is not stationary.
- After one non-seasonal difference and one seasonal difference, the ACF and PACF should show clearer cut-off points.

### Step 5: fit a SARIMA model

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Split into train and test
# Use the last 12 months as the test set
train = df.iloc[:-12]
test = df.iloc[-12:]

# Fit a SARIMA model with a reasonable starting order
model = SARIMAX(train['sales'],
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12))
results = model.fit(disp=False)

print(results.summary())
```

The summary has three parts:

- **coef** tells you the estimated weights for each term.
- **P>|z|** tells you the p-value. Values below 0.05 mean the term is useful.
- **AIC / BIC** are information criteria. Lower is better when comparing models for the same data.

### Step 6: forecast and evaluate

```python
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import math

# Forecast the same length as the test set
forecast = results.get_forecast(steps=12)
predicted = forecast.predicted_mean

rmse = math.sqrt(mean_squared_error(test['sales'], predicted))
mape = mean_absolute_percentage_error(test['sales'], predicted) * 100

print(f'RMSE: {rmse:.2f}')
print(f'MAPE: {mape:.2f}%')

# Plot actual vs forecast
plt.plot(train.index, train['sales'], label='train')
plt.plot(test.index, test['sales'], label='actual')
plt.plot(test.index, predicted, label='forecast')
plt.legend()
plt.show()
```

### Step 7: improve the model

If the first model is not good, try other values:

```python
orders_to_try = [
    (1, 1, 1, 1, 1, 1, 12),
    (1, 1, 0, 1, 1, 0, 12),
    (2, 1, 1, 1, 1, 1, 12),
    (1, 1, 1, 0, 1, 1, 12),
]

for p, d, q, P, D, Q, m in orders_to_try:
    model = SARIMAX(train['sales'],
                    order=(p, d, q),
                    seasonal_order=(P, D, Q, m))
    fitted = model.fit(disp=False)
    forecast = fitted.get_forecast(steps=12).predicted_mean
    rmse = math.sqrt(mean_squared_error(test['sales'], forecast))
    mape = mean_absolute_percentage_error(test['sales'], forecast) * 100
    print(f'({p},{d},{q})({P},{D},{Q}){m}  RMSE={rmse:.2f}  MAPE={mape:.2f}%')
```

Pick the order with the lowest `RMSE` or `MAPE` on the test set.

---

## 6. One-sentence takeaway

**SARIMA handles both trend and seasonality: use `p, q` and the ACF/PACF for the non-seasonal part, use `P, Q, m` for the repeating pattern, and use `d, D` to make the series stationary before you fit the model.**
