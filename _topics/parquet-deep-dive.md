---
title: Parquet Deep Dive — How It Actually Stores Data
category: Data
tags:
  - parquet
  - file-formats
  - data-engineering
  - columnar-storage
summary: Understanding how Parquet stores, encodes, and compresses data under the hood — from row groups to encoding schemes.
---

> **Think of Parquet as a super-efficient way to save spreadsheet data.** Instead of saving rows (like Excel does), it saves columns together. This makes it much faster to read and takes up way less space. If you've ever waited forever for a big Excel file to open, Parquet solves that problem!

## Why Parquet Exists

Imagine you're analyzing a table with 1 billion rows and 100 columns. You only need 3 columns. Would you rather:

- **Read all 100 columns** (CSV way) — waste 97% of your I/O
- **Read only the 3 columns you need** (Parquet way) — 33x faster

**Think of it like a filing cabinet** where documents are organized by topic (columns) instead of by date (rows). If you need to find all emails, you go to one drawer. With traditional filing (rows), you'd have to open every single drawer to find emails scattered everywhere.

That's the power of **columnar storage**. But Parquet doesn't stop there — it also uses clever encoding and compression tricks to make files 10-100x smaller.

Parquet is the format companies like Netflix and Uber use to analyze huge amounts of data quickly. It's not human-readable (you can't open it in Excel), but it's incredibly fast and small.

---

## The Architecture: Row Groups & Column Chunks

> **Here's how it works:** Imagine a huge spreadsheet with 1 million rows. Parquet breaks it into smaller chunks (like 10,000 rows each), then within each chunk, it stores all values from Column A together, all values from Column B together, etc. This makes it super fast to read just one column!

Parquet uses a hybrid approach called **PAX (Partition Attributes Across)** layout:

<div class="mermaid">
flowchart TD
    FILE["Parquet File"] --> RG1["Row Group 1<br/>(e.g., 10,000 rows)"]
    FILE --> RG2["Row Group 2<br/>(e.g., 10,000 rows)"]
    FILE --> RG3["Row Group 3<br/>(e.g., 10,000 rows)"]
    
    RG1 --> C1["Column Chunk:<br/>name"]
    RG1 --> C2["Column Chunk:<br/>age"]
    RG1 --> C3["Column Chunk:<br/>city"]
    
    C1 --> P1["Page 1"]
    C1 --> P2["Page 2"]
    
    style FILE fill:#dbeafe,stroke:#2563eb
    style RG1 fill:#d1fae5,stroke:#059669
    style C1 fill:#fef3c7,stroke:#d97706
    style P1 fill:#fce7f3,stroke:#db2777
</div>

### 1. Row Groups (Horizontal Partition)
- File is split into **row groups** (typically 128 MB each)
- Each row group contains a subset of rows (e.g., 10,000 rows)
- Allows parallel processing across row groups

### 2. Column Chunks (Vertical Partition)
- Within each row group, data is stored **column by column**
- Each column's values are stored together in a **column chunk**
- Similar values cluster together → better compression

### 3. Pages (Compression Unit)
- Each column chunk is further divided into **pages**
- Pages are the unit of encoding and compression
- Typically 1 MB per page

**Why This Works:**
```
Same column values cluster together:
  age: [25, 25, 26, 25, 27, 25, 26, ...]
  
Much easier to compress than mixed data:
  row: ["John", 25, "NYC", "Engineer", "John", 25, "LA", ...]
```

---

## Type System: Logical vs Physical

> **The clever trick:** Parquet stores everything using just 8 basic building blocks (like numbers and text), but it remembers what those building blocks actually represent (like dates or money). It's like how your phone stores photos as 0s and 1s, but displays them as images.

Parquet separates **what data means** (logical) from **how it's stored** (physical).

### Physical Types (Only 8!)

Parquet only knows how to write these types to disk:

| Physical Type | Size | Example |
|---------------|------|---------|
| `BOOLEAN` | 1 bit | `true`, `false` |
| `INT32` | 4 bytes | `-2,147,483,648` to `2,147,483,647` |
| `INT64` | 8 bytes | Very large integers |
| `FLOAT` | 4 bytes | `3.14` |
| `DOUBLE` | 8 bytes | `3.141592653589793` |
| `BYTE_ARRAY` | Variable | Raw bytes (e.g., strings) |
| `FIXED_LEN_BYTE_ARRAY` | Fixed | Fixed-size binary data |
| `INT96` | 12 bytes | ⚠️ Deprecated (old timestamps) |

**Why so few?** Keeps the Parquet reader/writer implementation simple.

### Logical Types (Rich Semantics)

Your application needs more than 8 types! Logical types add meaning:

| Logical Type | Stored As | Meaning |
|--------------|-----------|---------|
| `STRING` | `BYTE_ARRAY` | UTF-8 encoded text |
| `DATE` | `INT32` | Days since Unix epoch (Jan 1, 1970) |
| `TIMESTAMP` | `INT64` | Microseconds since Unix epoch |
| `DECIMAL` | `BYTE_ARRAY` or `INT32/64` | Fixed-point decimal (e.g., money) |
| `UUID` | `FIXED_LEN_BYTE_ARRAY(16)` | 128-bit UUID |
| `JSON` | `BYTE_ARRAY` | UTF-8 JSON string |

**Example:**
```python
# Your data
date = "2024-12-16"

# Stored in Parquet as INT32
physical_value = 20072  # days since 1970-01-01

# Logical type annotation tells reader: "interpret as DATE"
```

---

## Encoding Schemes

> **What's encoding?** It's finding patterns to save space. If you see "NYC" written 1000 times, instead of saving "NYC" 1000 times, you save it once and write "repeat 1000 times." That's what encoding does!

This is where Parquet gets clever. Different data patterns use different encodings.

### 1. PLAIN (No Encoding)

Just serialize values back-to-back in little-endian format.

```
INT32: [1, 2, 3]
Bytes: 01 00 00 00 | 02 00 00 00 | 03 00 00 00
       (4 bytes each)
```

**When Used:**
- High cardinality data (many unique values)
- Random/unpredictable data
- As a fallback when nothing else works

### 2. RLE_DICTIONARY (Most Common!)

> **Think of it like this:** Imagine writing an essay where you mention "Massachusetts" 100 times. Instead of writing it out every time, you write "MA (1)" once at the top, then just write "(1)" everywhere else. That's dictionary encoding!

Build a dictionary of unique values, then reference them by ID.

**Example:**
```python
# Original data (1000 rows)
cities = ["NYC", "LA", "NYC", "SF", "NYC", "LA", ...]

# Dictionary (stored once)
dictionary = {
  0: "NYC",
  1: "LA", 
  2: "SF"
}

# Data (stored as IDs)
ids = [0, 1, 0, 2, 0, 1, ...]  # Much smaller!
```

<div class="mermaid">
flowchart LR
    subgraph original["Original: 1000 rows × 10 bytes = 10 KB"]
        O1["NYC"]
        O2["LA"]
        O3["NYC"]
        O4["..."]
    end
    
    subgraph encoded["Dictionary: 30 bytes<br/>IDs: 1000 bytes = 1 KB"]
        DICT["Dict:<br/>0=NYC<br/>1=LA<br/>2=SF"]
        IDS["IDs:<br/>0,1,0,2,0,..."]
    end
    
    original --> |"10x smaller"| encoded
    
    style original fill:#fecaca,stroke:#dc2626
    style encoded fill:#d1fae5,stroke:#059669
</div>

**When Used:**
- Low cardinality columns (few unique values)
- Repeated values (e.g., categories, status codes)
- String columns with duplicates

**Compression Ratio:** Often 10-100x for categorical data!

### 3. RLE (Run-Length Encoding)

Store repeated values as `(value, count)` pairs.

```python
# Original data
values = [5, 5, 5, 5, 7, 7, 3, 3, 3]

# RLE encoded
encoded = [(5, 4), (7, 2), (3, 3)]  # Much smaller!
```

**When Used:**
- Long sequences of repeated values
- Boolean columns with many consecutive trues/falses
- Sorted data

### 4. DELTA_BINARY_PACKED

Store first value, then only the **differences** (deltas).

```python
# Original timestamps
timestamps = [1000, 1001, 1002, 1003, 1004]

# Delta encoded
base = 1000
deltas = [1, 1, 1, 1]  # Much smaller numbers!
```

**When Used:**
- Sequential data (timestamps, IDs)
- Sorted integers
- Time series data

### 5. DELTA_LENGTH_BYTE_ARRAY

For variable-length strings, store the lengths as deltas.

```python
# Original strings
strings = ["hello", "world", "test", "data"]

# Store lengths as deltas
lengths = [5, 5, 4, 4]
delta_lengths = [5, 0, -1, 0]  # Differences!
```

**When Used:**
- Variable-length strings with similar lengths
- Text columns

### 6. DELTA_BYTE_ARRAY

Store the first string, then only the prefix/suffix changes.

```python
# Original data (sorted)
values = ["apple", "apply", "application"]

# Delta encoded
values = [
  "apple",           # Full value
  (3, "y"),          # Keep 3 chars ("app"), add "y" 
  (3, "lication")    # Keep 3 chars ("app"), add "lication"
]
```

**When Used:**
- Sorted strings with common prefixes
- URLs, file paths

---

## Compression

> **What's compression?** It's like zipping a file on your computer — makes it smaller so it takes less space and is faster to send. Parquet uses different "zippers" depending on whether you need maximum speed or maximum space savings.

After encoding, Parquet applies compression algorithms:

| Compression | Speed | Ratio | CPU Usage | Best For |
|-------------|-------|-------|-----------|----------|
| **Snappy** | ⚡⚡⚡ Fast | Good | Low | Default choice |
| **GZIP** | 🐌 Slow | Better | Medium | Archival storage |
| **LZ4** | ⚡⚡⚡ Very Fast | Good | Very Low | Real-time processing |
| **ZSTD** | ⚡⚡ Fast | Excellent | Medium | Best balance |
| **Brotli** | 🐌 Slowest | Best | High | Cold storage |
| **Uncompressed** | ⚡⚡⚡⚡ Instant | None | None | Already compressed data |

**Compression Stack:**
```
1. Physical Type:  "NYC", "LA", "NYC", "SF" ... (BYTE_ARRAY)
2. Encoding:       Dictionary + IDs (RLE_DICTIONARY)
3. Compression:    Snappy/GZIP (further reduces size)
4. Disk:          Final bytes written to file
```

---

## Putting It All Together

Let's see how Parquet stores this data:

```python
# DataFrame with 1 million rows
df = pd.DataFrame({
    'user_id': range(1, 1_000_001),           # Sequential
    'status': ['active'] * 800_000 + ['inactive'] * 200_000,  # Repetitive
    'city': random.choices(['NYC', 'LA', 'SF'], k=1_000_000),  # Low cardinality
    'timestamp': pd.date_range('2024-01-01', periods=1_000_000, freq='1s')
})
```

**How Parquet Stores This:**

<div class="mermaid">
flowchart TD
    subgraph user_id["user_id Column"]
        U1["Physical: INT64"]
        U2["Encoding: DELTA_BINARY_PACKED<br/>(base + deltas)"]
        U3["Compression: Snappy"]
        U4["Result: ~1 MB"]
    end
    
    subgraph status["status Column"]
        S1["Physical: BYTE_ARRAY"]
        S2["Encoding: RLE<br/>(800k active, 200k inactive)"]
        S3["Compression: Snappy"]
        S4["Result: ~100 KB"]
    end
    
    subgraph city["city Column"]
        C1["Physical: BYTE_ARRAY"]
        C2["Encoding: RLE_DICTIONARY<br/>(3 values in dict)"]
        C3["Compression: Snappy"]
        C4["Result: ~500 KB"]
    end
    
    style user_id fill:#dbeafe,stroke:#2563eb
    style status fill:#d1fae5,stroke:#059669
    style city fill:#fef3c7,stroke:#d97706
</div>

| Column | Raw Size | Parquet Size | Compression |
|--------|----------|--------------|-------------|
| `user_id` | 8 MB | ~1 MB | 8x |
| `status` | 7 MB | ~100 KB | 70x! |
| `city` | 5 MB | ~500 KB | 10x |
| **Total** | **20 MB** | **~1.6 MB** | **~12x** |

---

## Reading Parquet Files

Parquet's structure enables **predicate pushdown** and **column pruning**:

### Column Pruning
```python
# Only read 2 columns
df = pd.read_parquet('data.parquet', columns=['user_id', 'city'])
# ✅ Only reads those column chunks — ignores others!
```

### Predicate Pushdown

> **What's this?** A fancy way of saying "don't even bother reading data you don't need." Like if you're looking for files from December, you don't open the folders for January-November. Parquet keeps a "cheat sheet" at the beginning of the file that tells it which sections to skip.

```python
# Filter by value
df = pd.read_parquet('data.parquet', filters=[('status', '==', 'active')])
# ✅ Reads statistics → skips row groups where status != 'active'
```

### Statistics in Footer

Each column chunk stores min/max statistics:

```python
# Parquet footer metadata
Column: age
  Row Group 1: min=18, max=25
  Row Group 2: min=26, max=35
  Row Group 3: min=36, max=65

# Query: WHERE age > 40
# ✅ Skip row groups 1 & 2 (max < 40)
# ✅ Only read row group 3
```

---

## File Structure Example

```
my_data.parquet
│
├── [4 bytes] Magic Number: "PAR1"
│
├── Row Group 1
│   ├── Column Chunk: user_id
│   │   ├── Dictionary Page (if using dictionary)
│   │   ├── Data Page 1 (encoded + compressed)
│   │   ├── Data Page 2
│   │   └── Metadata (min, max, null count)
│   │
│   ├── Column Chunk: status
│   └── Column Chunk: city
│
├── Row Group 2
│   └── ... (same structure)
│
├── Footer
│   ├── Schema
│   ├── Row Group Metadata (locations, stats)
│   ├── Column Metadata
│   └── Footer Length (4 bytes)
│
└── [4 bytes] Magic Number: "PAR1"
```

---

## Best Practices

### 1. Choose the Right Row Group Size

```python
# Default: 128 MB row groups
df.to_parquet('data.parquet', row_group_size=128 * 1024 * 1024)

# Smaller row groups → More parallelism, more metadata overhead
# Larger row groups → Less parallelism, less metadata overhead
```

**Rule of Thumb:** 128-512 MB per row group

### 2. Use Dictionary Encoding for Categories

```python
# Convert to categorical before writing
df['status'] = df['status'].astype('category')
df.to_parquet('data.parquet')  # Uses dictionary encoding
```

### 3. Sort Data for Better Compression

```python
# Sort by frequently filtered columns
df = df.sort_values(['date', 'status'])
df.to_parquet('data.parquet')
# ✅ Better compression, better statistics, faster filtering
```

### 4. Choose Compression Based on Use Case

```python
# Real-time analytics
df.to_parquet('data.parquet', compression='snappy')  # Fast reads

# Archival storage
df.to_parquet('data.parquet', compression='zstd')  # Best compression

# Best balance
df.to_parquet('data.parquet', compression='zstd', compression_level=3)
```

### 5. Partition Large Datasets

```python
# Partition by date for time-series data
df.to_parquet('data.parquet', partition_cols=['year', 'month'])

# Creates structure:
# data.parquet/
#   year=2024/
#     month=01/part-00000.parquet
#     month=02/part-00000.parquet
#   year=2025/
#     month=01/part-00000.parquet

# ✅ Query only reads relevant partitions
```

---

## Common Pitfalls

### 1. Too Many Small Files
```
❌ 10,000 files × 1 KB = Slow
✅ 10 files × 1 MB = Fast
```

**Why:** Opening files has overhead. Combine small files.

### 2. Wide Schemas (Too Many Columns)
```
❌ 10,000 columns = Huge metadata overhead
✅ < 1,000 columns = Reasonable
```

**Solution:** Split into multiple tables or nest columns.

### 3. Not Using Partitioning
```
❌ Single 100 GB file
✅ Partitioned by date/region
```

### 4. Wrong Compression for Use Case
```
❌ GZIP for real-time queries (slow decompression)
✅ Snappy/LZ4 for real-time (fast decompression)
```

---

## Performance Tips

| Operation | Tip | Speed Gain |
|-----------|-----|------------|
| **Read Specific Columns** | Use `columns=[...]` parameter | 10-100x faster |
| **Filter Early** | Use `filters=[...]` parameter | 2-10x faster |
| **Partition Data** | Partition by frequently filtered columns | 10-1000x faster |
| **Sort Before Writing** | Sort by filter columns | 2-5x faster reads |
| **Use Categories** | Convert strings to categorical | 5-20x smaller |

---

## Should You Use Parquet?

> **Quick Decision Guide:**
> - ✅ **Use Parquet:** You have lots of data (>100 MB) and need to analyze it fast
> - ❌ **Skip Parquet:** You have small files or need to read data like a book (row by row)
> - ✅ **Use Parquet:** You're using tools like Python, Spark, or cloud databases
> - ❌ **Skip Parquet:** You need to open files in Excel or edit them manually

## When NOT to Use Parquet

Parquet isn't always the answer:

| Use Case | Better Choice | Why |
|----------|---------------|-----|
| Small files (< 1 MB) | CSV, JSON | Overhead not worth it |
| Frequently updated data | Delta Lake, Iceberg | Parquet is write-once |
| Row-wise access | Avro, JSON | Parquet optimized for columns |
| Human readability | CSV, JSON | Parquet is binary |
| Streaming writes | Avro | Parquet needs to buffer row groups |

---

## Real-World Example

```python
import pandas as pd
import time

# Create test data
df = pd.DataFrame({
    'id': range(10_000_000),
    'category': np.random.choice(['A', 'B', 'C'], 10_000_000),
    'value': np.random.randn(10_000_000)
})

# Save as CSV
start = time.time()
df.to_csv('data.csv', index=False)
csv_time = time.time() - start
csv_size = os.path.getsize('data.csv') / 1024 / 1024

# Save as Parquet
start = time.time()
df.to_parquet('data.parquet', compression='snappy')
parquet_time = time.time() - start
parquet_size = os.path.getsize('data.parquet') / 1024 / 1024

print(f"CSV:     {csv_size:.1f} MB in {csv_time:.1f}s")
print(f"Parquet: {parquet_size:.1f} MB in {parquet_time:.1f}s")

# Read specific column
start = time.time()
df_csv = pd.read_csv('data.csv', usecols=['category'])
csv_read = time.time() - start

start = time.time()
df_parquet = pd.read_parquet('data.parquet', columns=['category'])
parquet_read = time.time() - start

print(f"\nRead 1 column:")
print(f"CSV:     {csv_read:.2f}s")
print(f"Parquet: {parquet_read:.2f}s ({csv_read/parquet_read:.1f}x faster)")
```

**Typical Output:**
```
CSV:     650.0 MB in 45.3s
Parquet: 85.0 MB in 3.2s (7.6x smaller, 14x faster write)

Read 1 column:
CSV:     12.50s
Parquet: 0.15s (83x faster)
```

---

## Summary

> **Quick Takeaways:**
> - **What is Parquet?** A super-efficient way to store large datasets (think millions of rows)
> - **Why use it?** 10-100x smaller files, way faster to analyze
> - **When to use it?** Anytime you're working with data bigger than a few Excel spreadsheets
> - **When NOT to use it?** Small files, data you need to edit manually, or files you need to open in Excel
> - **Bottom line:** Analyzing data in Python, SQL, or cloud tools → use Parquet. Working in Excel → stick with CSV.

Parquet achieves amazing compression and speed through:

1. **Columnar Layout** — Store similar values together (like organizing a filing cabinet by topic)
2. **Smart Encoding** — Find patterns to save space (like using "MA" instead of writing "Massachusetts")
3. **Compression** — Zip files to make them even smaller
4. **Statistics** — Quick lookup to skip irrelevant data
5. **Type System** — Remember what data means, not just how it's stored

**The Magic Formula:**
```
Raw Data → Physical Type → Encoding → Compression → Disk
  ↓           ↓              ↓           ↓          ↓
1000 MB  →  1000 MB    →   100 MB   →  10 MB   = 100x smaller!
```

**Use Parquet when:**
- ✅ Analytical queries (aggregations, filtering)
- ✅ Large datasets (> 100 MB)
- ✅ Column-heavy reads (SELECT a few columns)
- ✅ Data warehouses, data lakes
- ✅ You're using Python, Spark, SQL databases

**Skip Parquet when:**
- ❌ Small files (< 1 MB) — overhead not worth it
- ❌ Frequent updates — Parquet is write-once
- ❌ Row-by-row access — use CSV or databases
- ❌ Human needs to read it — use CSV or JSON

---

## Further Reading

- [Apache Parquet Documentation](https://parquet.apache.org/docs/)
- [Parquet Format Specification](https://github.com/apache/parquet-format)
- [Dremel Paper (Parquet's Inspiration)](https://research.google/pubs/pub36632/)
