---
title: "Pandas Series Cheat Sheet - Quick Reference"
category: Python
tags:
  - pandas
  - series
  - data-analysis
  - python
summary: Print-friendly quick reference for Pandas Series - creation, indexing, operations, and essential methods.
---

# Pandas Series Cheat Sheet

**Pandas Series** - One-dimensional labeled array capable of holding any data type

---

## NUMPY ARRAY VS PANDAS SERIES

### Key Differences

| **Feature** | **NumPy Array** | **Pandas Series** |
|-------------|-----------------|-------------------|
| **Index** | Integer position only | Labeled index (any type) |
| **Data types** | Homogeneous (single dtype) | Homogeneous (single dtype) |
| **Missing data** | No built-in support | Native NaN handling |
| **Alignment** | Manual alignment needed | Automatic index alignment |
| **Operations** | Element-wise by position | Element-wise by label |
| **Slicing** | Position-based only | Label-based or position-based |
| **Memory** | More efficient | Slightly more overhead |
| **Speed** | Faster for numeric ops | Slightly slower, more features |

### When to Use What

| **Use NumPy Array** | **Use Pandas Series** |
|---------------------|----------------------|
| Pure numerical computation | Data with meaningful labels |
| Maximum performance needed | Need to handle missing data |
| Working with matrices | Working with time series |
| Scientific computing | Data analysis & exploration |
| No need for labels | Need automatic alignment |
| Memory-constrained | Need rich functionality |

### Code Comparison

| **Task** | **NumPy** | **Pandas** |
|----------|-----------|------------|
| Create | `np.array([1, 2, 3])` | `pd.Series([1, 2, 3])` |
| With labels | Not supported | `pd.Series([1, 2, 3], index=['a', 'b', 'c'])` |
| Access by position | `arr[0]` | `s.iloc[0]` or `s[0]` |
| Access by label | Not supported | `s.loc['a']` or `s['a']` |
| Slice | `arr[0:2]` | `s.iloc[0:2]` or `s[0:2]` |
| Missing data | `np.nan` (no special handling) | `s.isna()`, `s.fillna()`, `s.dropna()` |
| Operations | `arr1 + arr2` (position-based) | `s1 + s2` (index-aligned) |
| Statistics | `arr.mean()` | `s.mean()` (skips NaN) |
| Filtering | `arr[arr > 5]` | `s[s > 5]` |
| Type conversion | `arr.astype(float)` | `s.astype(float)` |

### Index Alignment Example

```python
# NumPy - No alignment, just position-based
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr1 + arr2  # [5, 7, 9] - adds by position

# Pandas - Automatic index alignment
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([4, 5, 6], index=['b', 'c', 'd'])
s1 + s2  # a: NaN, b: 6, c: 8, d: NaN - aligns by label
```

### Conversion Between NumPy and Pandas

| **Conversion** | **Code** |
|----------------|----------|
| NumPy → Series | `pd.Series(numpy_array)` |
| NumPy → Series (with index) | `pd.Series(numpy_array, index=labels)` |
| Series → NumPy | `series.values` or `series.to_numpy()` |
| Keep index | `series.index.to_numpy()` (separate) |

### Performance Considerations

```python
# NumPy - Fastest for pure numeric operations
arr = np.array([1, 2, 3, 4, 5])
arr * 2  # Very fast

# Pandas - Slightly slower but more features
s = pd.Series([1, 2, 3, 4, 5])
s * 2  # Fast, plus handles NaN, alignment, etc.

# For large datasets with numeric operations only → NumPy
# For data analysis with labels/missing data → Pandas
```

---

## QUICK REFERENCE

### Import & Creation

| **Method** | **Code** | **Result** |
|------------|----------|------------|
| Import | `import pandas as pd` | - |
| From list | `pd.Series([1, 2, 3])` | Series with default index |
| With index | `pd.Series([1, 2, 3], index=['a', 'b', 'c'])` | Custom index labels |
| From dict | `pd.Series({'a': 1, 'b': 2, 'c': 3})` | Keys become index |
| From scalar | `pd.Series(5, index=['a', 'b', 'c'])` | Broadcast value |
| From ndarray | `pd.Series(np.array([1, 2, 3]))` | NumPy array to Series |
| With name | `pd.Series([1, 2, 3], name='numbers')` | Named Series |

### Basic Properties

| **Property** | **Returns** | **Example** |
|--------------|-------------|-------------|
| `.values` | NumPy array | `s.values` → `array([1, 2, 3])` |
| `.index` | Index object | `s.index` → `Index(['a', 'b', 'c'])` |
| `.dtype` | Data type | `s.dtype` → `dtype('int64')` |
| `.shape` | Tuple of dimensions | `s.shape` → `(3,)` |
| `.size` | Number of elements | `s.size` → `3` |
| `.name` | Series name | `s.name` → `'numbers'` |
| `.empty` | True if empty | `s.empty` → `False` |
| `.ndim` | Number of dimensions | `s.ndim` → `1` |

---

## INDEXING & SELECTION

### Basic Indexing

| **Method** | **Example** | **Description** |
|------------|-------------|-----------------|
| Label-based | `s['a']` | Access by label |
| Position-based | `s[0]` | Access by position |
| `.loc[]` | `s.loc['a']` | Label-based (explicit) |
| `.iloc[]` | `s.iloc[0]` | Position-based (explicit) |
| Slice labels | `s['a':'c']` | Inclusive slice |
| Slice positions | `s[0:2]` | Exclusive slice |
| Multiple labels | `s[['a', 'c']]` | Fancy indexing |
| Boolean mask | `s[s > 2]` | Conditional selection |

### Advanced Selection

| **Method** | **Example** | **Description** |
|------------|-------------|-----------------|
| `.at[]` | `s.at['a']` | Fast scalar access (label) |
| `.iat[]` | `s.iat[0]` | Fast scalar access (position) |
| `.get()` | `s.get('a', default=0)` | Safe access with default |
| `.where()` | `s.where(s > 2, 0)` | Replace values where False |
| `.mask()` | `s.mask(s > 2, 0)` | Replace values where True |
| `.isin()` | `s.isin([1, 3])` | Check membership |
| `.between()` | `s.between(1, 3)` | Check range |

---

## OPERATIONS

### Arithmetic Operations

| **Operation** | **Example** | **Description** |
|---------------|-------------|-----------------|
| Addition | `s + 10` or `s.add(10)` | Element-wise addition |
| Subtraction | `s - 5` or `s.sub(5)` | Element-wise subtraction |
| Multiplication | `s * 2` or `s.mul(2)` | Element-wise multiplication |
| Division | `s / 2` or `s.div(2)` | Element-wise division |
| Floor division | `s // 2` or `s.floordiv(2)` | Integer division |
| Modulo | `s % 2` or `s.mod(2)` | Remainder |
| Power | `s ** 2` or `s.pow(2)` | Exponentiation |
| Absolute | `abs(s)` or `s.abs()` | Absolute values |

### Comparison Operations

| **Operation** | **Example** | **Returns** |
|---------------|-------------|-------------|
| Equal | `s == 5` or `s.eq(5)` | Boolean Series |
| Not equal | `s != 5` or `s.ne(5)` | Boolean Series |
| Greater than | `s > 5` or `s.gt(5)` | Boolean Series |
| Less than | `s < 5` or `s.lt(5)` | Boolean Series |
| Greater or equal | `s >= 5` or `s.ge(5)` | Boolean Series |
| Less or equal | `s <= 5` or `s.le(5)` | Boolean Series |

### Logical Operations

| **Operation** | **Example** | **Description** |
|---------------|-------------|-----------------|
| AND | `(s > 1) & (s < 5)` | Element-wise AND |
| OR | `(s < 2) \| (s > 4)` | Element-wise OR |
| NOT | `~(s > 3)` | Element-wise NOT |
| XOR | `(s > 2) ^ (s < 4)` | Element-wise XOR |

---

## AGGREGATION & STATISTICS

### Basic Statistics

| **Method** | **Returns** | **Example** |
|------------|-------------|-------------|
| `.sum()` | Sum of values | `s.sum()` → `6` |
| `.mean()` | Average | `s.mean()` → `2.0` |
| `.median()` | Median value | `s.median()` → `2.0` |
| `.min()` | Minimum | `s.min()` → `1` |
| `.max()` | Maximum | `s.max()` → `3` |
| `.std()` | Standard deviation | `s.std()` → `1.0` |
| `.var()` | Variance | `s.var()` → `1.0` |
| `.count()` | Non-null count | `s.count()` → `3` |

### Advanced Statistics

| **Method** | **Returns** | **Example** |
|------------|-------------|-------------|
| `.quantile(q)` | Quantile | `s.quantile(0.5)` → median |
| `.mode()` | Most frequent | `s.mode()` → Series |
| `.sem()` | Std error of mean | `s.sem()` |
| `.skew()` | Skewness | `s.skew()` |
| `.kurt()` | Kurtosis | `s.kurt()` |
| `.describe()` | Summary stats | Full statistics |
| `.value_counts()` | Frequency counts | Count of each value |
| `.nunique()` | Unique count | Number of unique values |

### Cumulative Operations

| **Method** | **Returns** | **Example** |
|------------|-------------|-------------|
| `.cumsum()` | Cumulative sum | `[1, 3, 6]` |
| `.cumprod()` | Cumulative product | `[1, 2, 6]` |
| `.cummin()` | Cumulative minimum | `[1, 1, 1]` |
| `.cummax()` | Cumulative maximum | `[1, 2, 3]` |

---

## MISSING DATA

### Detection

| **Method** | **Returns** | **Example** |
|------------|-------------|-------------|
| `.isna()` / `.isnull()` | Boolean mask | `s.isna()` → `[False, True, False]` |
| `.notna()` / `.notnull()` | Inverse mask | `s.notna()` → `[True, False, True]` |
| `.hasnans` | True if any NaN | `s.hasnans` → `True` |

### Handling

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.dropna()` | Remove NaN | `s.dropna()` |
| `.fillna(value)` | Fill with value | `s.fillna(0)` |
| `.fillna(method='ffill')` | Forward fill | Propagate last valid |
| `.fillna(method='bfill')` | Backward fill | Use next valid |
| `.interpolate()` | Interpolate | Linear interpolation |
| `.replace(old, new)` | Replace values | `s.replace(0, np.nan)` |

---

## SORTING & RANKING

### Sorting

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.sort_values()` | Sort by values | `s.sort_values()` |
| `.sort_values(ascending=False)` | Descending | Largest first |
| `.sort_index()` | Sort by index | `s.sort_index()` |
| `.nlargest(n)` | Top n values | `s.nlargest(3)` |
| `.nsmallest(n)` | Bottom n values | `s.nsmallest(3)` |

### Ranking

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.rank()` | Assign ranks | `s.rank()` |
| `.rank(method='min')` | Min rank for ties | Minimum ranking |
| `.rank(method='max')` | Max rank for ties | Maximum ranking |
| `.rank(method='first')` | First occurrence | Order of appearance |
| `.rank(pct=True)` | Percentile ranks | 0 to 1 scale |

---

## STRING OPERATIONS

### Basic String Methods

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.str.lower()` | Lowercase | `s.str.lower()` |
| `.str.upper()` | Uppercase | `s.str.upper()` |
| `.str.title()` | Title case | `s.str.title()` |
| `.str.capitalize()` | Capitalize first | `s.str.capitalize()` |
| `.str.strip()` | Remove whitespace | `s.str.strip()` |
| `.str.replace(old, new)` | Replace substring | `s.str.replace('a', 'b')` |
| `.str.contains(pat)` | Check contains | `s.str.contains('abc')` |
| `.str.startswith(pat)` | Check starts with | `s.str.startswith('a')` |
| `.str.endswith(pat)` | Check ends with | `s.str.endswith('z')` |

### String Extraction

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.str.split(sep)` | Split string | `s.str.split(',')` |
| `.str.extract(pat)` | Extract regex groups | `s.str.extract(r'(\d+)')` |
| `.str.findall(pat)` | Find all matches | `s.str.findall(r'\d+')` |
| `.str.slice(start, stop)` | Slice strings | `s.str.slice(0, 3)` |
| `.str[start:stop]` | Index slice | `s.str[0:3]` |
| `.str.len()` | String length | `s.str.len()` |

---

## DATETIME OPERATIONS

### Datetime Properties

| **Property** | **Returns** | **Example** |
|--------------|-------------|-------------|
| `.dt.year` | Year | `s.dt.year` |
| `.dt.month` | Month | `s.dt.month` |
| `.dt.day` | Day | `s.dt.day` |
| `.dt.hour` | Hour | `s.dt.hour` |
| `.dt.minute` | Minute | `s.dt.minute` |
| `.dt.second` | Second | `s.dt.second` |
| `.dt.dayofweek` | Day of week (0=Mon) | `s.dt.dayofweek` |
| `.dt.dayofyear` | Day of year | `s.dt.dayofyear` |
| `.dt.quarter` | Quarter | `s.dt.quarter` |

### Datetime Methods

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.dt.strftime(fmt)` | Format datetime | `s.dt.strftime('%Y-%m-%d')` |
| `.dt.normalize()` | Set time to midnight | `s.dt.normalize()` |
| `.dt.floor(freq)` | Round down | `s.dt.floor('D')` |
| `.dt.ceil(freq)` | Round up | `s.dt.ceil('D')` |
| `.dt.round(freq)` | Round | `s.dt.round('H')` |

---

## TRANSFORMATION

### Apply & Map

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.apply(func)` | Apply function | `s.apply(lambda x: x**2)` |
| `.map(dict)` | Map with dict | `s.map({1: 'a', 2: 'b'})` |
| `.map(func)` | Map with function | `s.map(str)` |
| `.transform(func)` | Transform | `s.transform(lambda x: x + 1)` |

### Binning & Categorization

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `pd.cut(s, bins)` | Bin into intervals | `pd.cut(s, bins=3)` |
| `pd.qcut(s, q)` | Quantile-based bins | `pd.qcut(s, q=4)` |
| `.astype('category')` | Convert to category | `s.astype('category')` |
| `.cat.categories` | Get categories | Category labels |
| `.cat.codes` | Get category codes | Integer codes |

### Type Conversion

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.astype(dtype)` | Convert type | `s.astype(float)` |
| `.astype(str)` | To string | `s.astype(str)` |
| `pd.to_numeric(s)` | To numeric | `pd.to_numeric(s, errors='coerce')` |
| `pd.to_datetime(s)` | To datetime | `pd.to_datetime(s)` |
| `.to_list()` | To Python list | `s.to_list()` |
| `.to_dict()` | To dictionary | `s.to_dict()` |
| `.to_numpy()` | To NumPy array | `s.to_numpy()` |

---

## COMBINING SERIES

### Concatenation

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `pd.concat([s1, s2])` | Concatenate | Vertical stack |
| `pd.concat([s1, s2], axis=1)` | Side by side | Creates DataFrame |
| `.append(s2)` | Append series | `s1.append(s2)` |

### Set Operations

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `s1.add(s2)` | Add aligned | Index-aligned addition |
| `s1.sub(s2)` | Subtract aligned | Index-aligned subtraction |
| `s1.mul(s2)` | Multiply aligned | Index-aligned multiplication |
| `s1.div(s2)` | Divide aligned | Index-aligned division |

---

## RESHAPING

### Duplicates

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.duplicated()` | Find duplicates | Boolean mask |
| `.drop_duplicates()` | Remove duplicates | Keep first occurrence |
| `.drop_duplicates(keep='last')` | Keep last | Remove earlier duplicates |
| `.unique()` | Unique values | Array of unique values |

### Reindexing

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.reindex(new_index)` | New index | `s.reindex(['a', 'b', 'c'])` |
| `.reindex(fill_value=0)` | Fill missing | Fill new indices |
| `.reset_index()` | Reset to default | Returns DataFrame |
| `.reset_index(drop=True)` | Drop old index | Returns Series |
| `.set_axis(labels)` | Set new index | `s.set_axis(['x', 'y', 'z'])` |

---

## GROUPING & AGGREGATION

### GroupBy Operations

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.groupby(level=0)` | Group by index | Multi-index grouping |
| `.groupby(func)` | Group by function | `s.groupby(lambda x: x[0])` |
| `.groupby().sum()` | Group sum | Aggregate by group |
| `.groupby().mean()` | Group mean | Average by group |
| `.groupby().count()` | Group count | Count by group |
| `.groupby().agg(func)` | Custom aggregation | Multiple functions |

---

## WINDOW FUNCTIONS

### Rolling Windows

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.rolling(window)` | Rolling window | `s.rolling(3)` |
| `.rolling(3).mean()` | Moving average | 3-period average |
| `.rolling(3).sum()` | Moving sum | 3-period sum |
| `.rolling(3).std()` | Moving std dev | 3-period std |
| `.rolling(3).min()` | Moving minimum | 3-period min |
| `.rolling(3).max()` | Moving maximum | 3-period max |

### Expanding Windows

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.expanding()` | Expanding window | All previous values |
| `.expanding().mean()` | Cumulative average | Growing average |
| `.expanding().sum()` | Cumulative sum | Growing sum |

### Exponential Weighted

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.ewm(span=3)` | EW window | Exponential weighting |
| `.ewm(span=3).mean()` | EW moving avg | Exponentially weighted |

---

## PLOTTING

### Basic Plots

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.plot()` | Line plot | `s.plot()` |
| `.plot.line()` | Line plot | Explicit line |
| `.plot.bar()` | Bar chart | `s.plot.bar()` |
| `.plot.barh()` | Horizontal bar | `s.plot.barh()` |
| `.plot.hist()` | Histogram | `s.plot.hist()` |
| `.plot.box()` | Box plot | `s.plot.box()` |
| `.plot.kde()` | Density plot | `s.plot.kde()` |
| `.plot.area()` | Area plot | `s.plot.area()` |
| `.plot.pie()` | Pie chart | `s.plot.pie()` |

---

## I/O OPERATIONS

### Reading

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `pd.read_csv()` | Read CSV column | `pd.read_csv('file.csv')['col']` |
| `pd.read_json()` | Read JSON | `pd.read_json('file.json', typ='series')` |
| `pd.read_excel()` | Read Excel column | `pd.read_excel('file.xlsx')['col']` |

### Writing

| **Method** | **Description** | **Example** |
|------------|-----------------|-------------|
| `.to_csv(file)` | Write to CSV | `s.to_csv('file.csv')` |
| `.to_json(file)` | Write to JSON | `s.to_json('file.json')` |
| `.to_excel(file)` | Write to Excel | `s.to_excel('file.xlsx')` |
| `.to_clipboard()` | Copy to clipboard | `s.to_clipboard()` |

---

## COMMON PATTERNS

### Creating Series

```python
# From list
s = pd.Series([1, 2, 3, 4, 5])

# With custom index
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])

# From dictionary
s = pd.Series({'a': 1, 'b': 2, 'c': 3})

# With name
s = pd.Series([1, 2, 3], name='my_series')

# From range
s = pd.Series(range(10))
```

### Filtering

```python
# Single condition
s[s > 5]

# Multiple conditions
s[(s > 2) & (s < 8)]

# Using isin
s[s.isin([1, 3, 5])]

# Using between
s[s.between(2, 8)]
```

### Handling Missing Data

```python
# Drop NaN
s.dropna()

# Fill with value
s.fillna(0)

# Forward fill
s.fillna(method='ffill')

# Interpolate
s.interpolate()
```

### String Operations

```python
# Convert to lowercase
s.str.lower()

# Check contains
s.str.contains('pattern')

# Extract numbers
s.str.extract(r'(\d+)')

# Split and expand
s.str.split(',', expand=True)
```

### Datetime Operations

```python
# Convert to datetime
s = pd.to_datetime(s)

# Extract components
s.dt.year
s.dt.month
s.dt.day

# Format
s.dt.strftime('%Y-%m-%d')
```

### Aggregation

```python
# Basic stats
s.mean()
s.median()
s.std()

# Value counts
s.value_counts()

# Describe
s.describe()

# Custom aggregation
s.agg(['mean', 'std', 'min', 'max'])
```

---

## PERFORMANCE TIPS

1. **Use vectorized operations** instead of loops
   ```python
   # Good: s * 2
   # Bad: s.apply(lambda x: x * 2)
   ```

2. **Use `.loc[]` and `.iloc[]` explicitly** for clarity and performance

3. **Chain operations** for readability
   ```python
   s.dropna().sort_values().head(10)
   ```

4. **Use `.copy()`** to avoid SettingWithCopyWarning
   ```python
   s_new = s[s > 5].copy()
   ```

5. **Use categorical dtype** for repeated string values
   ```python
   s = s.astype('category')
   ```

---

## QUICK TIPS

- **Index alignment**: Operations automatically align on index
- **Broadcasting**: Scalar operations broadcast to all elements
- **NaN handling**: Most operations skip NaN by default
- **Method chaining**: Most methods return Series for chaining
- **Inplace operations**: Use `inplace=True` to modify in place
- **Copy vs view**: Use `.copy()` when you need independent data

---

**Print Settings:** Landscape orientation, narrow margins, fit to page  
**Pro Tip:** Laminate for durable desk reference!

**Last Updated:** January 2026
