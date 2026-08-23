---
title: "Time Series - A Friendly Guide"
category: Time Series
order: 0
permalink: /topics/time-series-friendly-guide/
tags:
  - time-series
  - machine-learning
  - stationarity
  - decomposition
  - trend
  - seasonality
summary: "A beginner-friendly guide to time series: what it is, how to spot changing mean and variance, what stationarity means, and how to decompose a series into trend, seasonality, and residuals."
date: 2026-08-23
---

# Time Series - A Friendly Guide

A **time series** is just a set of observations collected over time. Daily temperatures, monthly sales, hourly website traffic, and yearly stock prices are all time series.

Because the observations are ordered, we cannot treat them like normal rows in a spreadsheet. A row at time `t` is often connected to the row at time `t-1`. This guide explains the first things you look at when you get a time series: its center, its spread, its trend, and its repeating patterns.

---

## 1. Two quick questions: where is the center? how wide is the spread?

Whenever you see a time-series plot, ask two things:

- **Where is the middle of the data?** That is the **mean**.
- **How far do the points move away from the middle?** That is the **variance**.

```
Same center, small spread            Same center, larger spread

  .                                    .        .
    .                              .        .        .
.        .                       .        .        .        .
--------                        ---------------------------
 ^ mean                          ^ mean
```

The center tells you where the series lives. The spread tells you how noisy it is.

---

## 2. Constant mean vs changing mean

A **constant mean** means the center of the data does not drift over time. The values go up and down, but they stay around the same level.

```
Constant mean: the middle line is flat

  /\      /\      /\      /\      /\      /\
 /  \    /  \    /  \    /  \    /  \    /  \
/    \__/    \__/    \__/    \__/    \__/    \__
----------------- mean -------------------------
```

Example of values with a constant mean:

```
8, 11, 12, 9, 10, 8, 12, 11, 9, 10
```

The center is around 10, even though individual values jump around.

A **variable mean** means the center itself is moving. This is often called a **trend**.

```
Variable mean: the middle line is rising

                                /\
                              /  \
                            /    \
          /\              /        \              /\
        /  \            /            \            /  \
      /    \          /                \          /    \
    /        \      /                    \      /        \
  /            \  /                        \  /            \
```

Example of values with a variable mean:

```
10, 11, 12, 13, 14, 15, 16, 17, 18, 19
```

The whole series is shifting upward.

---

## 3. Constant variance vs changing variance

**Variance** describes how far the points move away from the center.

**Constant variance** means the size of the waves stays the same over time:

```
Same-sized waves:

  /\      /\      /\      /\      /\      /\
 /  \    /  \    /  \    /  \    /  \    /  \
/    \__/    \__/    \__/    \__/    \__/    \__
```

Example:

```
9, 11, 10, 9, 11, 10, 9, 11, 10, 9
```

The spread stays small and stable.

**Changing variance** means the waves get bigger or smaller over time:

```
Waves getting bigger:

              /\                    /\\
            /  \                  /   \\
      /\  /    \            /\  /      \\
____/  \/      \____/\____/  \/         \\
```

Example:

```
2, 18, 5, 16, 1, 20, 30, 45, 50, 80
```

The fluctuations become much larger as time goes on.

---

## 4. The four common plot types

When you are asked to classify a plot, draw an imaginary line through the middle and check the size of the waves.

| Plot | Mean | Variance | Visual clue |
|---|---|---|---|
| **1** | Constant | Constant | Same center, same-sized waves |
| **2** | Variable | Constant | Upward trend, similar-sized fluctuations |
| **3** | Variable | Approximately constant | Strong upward trend |
| **4** | Variable | Variable | Level and fluctuations both grow |

A simple visual trick:

1. Draw a line through the middle of the data.
   - Flat → constant mean
   - Sloped → variable mean
2. Look at the distance between the high and low points.
   - Same-sized waves → constant variance
   - Growing or shrinking waves → variable variance

---

## 5. Stationarity

A **stationary** time series has constant mean, constant variance, and constant autocorrelation over time. In other words, the statistical properties do not depend on when you look.

Why does this matter? Many classic time-series models assume the series is stationary. If the mean or variance is changing, the model can be confused and make poor forecasts.

```
Stationary:            Non-stationary:

Same level, same waves  Trend + growing waves

  /\  /\  /\  /\         /\\
 /  \/  \/  \/  \       /   \\
/                \_____/      \\
```

If a series is not stationary, you often need to transform it before modeling. Common fixes include:

- **Removing a trend** by differencing.
- **Stabilizing variance** with a log or square-root transform.
- **Removing seasonality** by deseasonalising the data.

---

## 6. Trend, seasonality, and residuals

Most time series can be broken into three pieces:

- **Trend:** the long-term direction (going up, going down, or staying flat).
- **Seasonality:** a repeating pattern at fixed intervals (daily, weekly, yearly).
- **Residuals / noise:** the leftover random variation after the trend and seasonality are removed.

```
Sales data:

Actual series = Trend + Seasonality + Residual

         /\                /\                  /\      .
        /  \    /\        /  \    /\          /  \    /|  random
_______/    \__/  \______/    \__/  \________/    \__/      wiggle
    rising trend      repeating winter spike        noise
```

---

## 7. Additive vs multiplicative decomposition

Both additive and multiplicative decomposition split a series into the same three parts: trend, seasonality, and residual. The difference is how those parts combine.

### Additive

```
Time series = Trend + Seasonality + Residual
```

In an **additive** series, the seasonal effect stays the same size over time.

Example: ice-cream sales with a summer boost of 20 extra units.

```
Normal sales = 100 units
Summer boost = +20 units
Total summer sales = 120

Later, business grows:
Normal sales = 500 units
Summer boost = +20 units
Total summer sales = 520
```

The seasonal effect is a fixed number, no matter how big the business gets.

### Multiplicative

```
Time series = Trend × Seasonality × Residual
```

In a **multiplicative** series, the seasonal effect grows with the level of the series.

Example: ice-cream sales in summer are 20% higher than normal.

```
Normal sales = 100 units
Summer boost = 20% higher
Total summer sales = 100 × 1.2 = 120

Later, business grows:
Normal sales = 500 units
Summer boost = 20% higher
Total summer sales = 500 × 1.2 = 600
```

The seasonal effect scales with the trend.

### How to tell them apart

Look at the waves again:

```
Additive: same-sized waves over time

    /\      /\      /\      /\      /\      /\      
   /  \    /  \    /  \    /  \    /  \    /  \
__/    \__/    \__/    \__/    \__/    \__/    \__

Multiplicative: waves get bigger as the series grows

                                /\
                          /\   /  \      
                    /\   /  \ /    \
              /\   /  \ /              
        /\   /  \ /                    
  /\   /  \ /                          
 /  \ /                                
/                                      
```

- **Same-sized waves** → additive.
- **Waves that grow with the trend** → multiplicative.

---

## 8. A quick decomposition example

In Python, `statsmodels` can decompose a series for you.

```python
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# df is a DataFrame with a datetime index and a 'value' column
result = seasonal_decompose(df["value"], model="additive", period=12)

result.plot()
plt.show()
```

Use `model="additive"` when the seasonal swings look the same everywhere. Use `model="multiplicative"` when the seasonal swings grow with the trend.

---

## 9. One-sentence takeaway

**A time series is ordered data over time; to understand it, check whether the mean and variance stay the same, and whether the repeating pattern is additive or multiplicative.**
