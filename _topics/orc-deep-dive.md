---
title: ORC Deep Dive — Optimized Row Columnar Format Explained
category: Data
tags:
  - orc
  - file-formats
  - data-engineering
  - hadoop
  - columnar-storage
summary: A deep dive into how ORC (Optimized Row Columnar) stores, compresses, and indexes data for Hadoop and Hive workloads.
---

> **What is ORC?** Parquet's cousin, designed specifically for Hadoop (a big data processing system). It's faster than Parquet in Hadoop, but ONLY works well in Hadoop. 
> 
> **Should you care about ORC?**
> - ✅ **Yes:** You're working with Hadoop, Hive, or enterprise big data systems
> - ❌ **No:** You're using Python, Spark, or modern cloud tools
> - 🤷 **Maybe:** Your company already uses ORC
> 
> **The honest take:** Unless you're specifically in a Hadoop/Hive environment, **use Parquet instead**. It's more widely supported and works everywhere. ORC is a specialized tool for a specific ecosystem.

## Why ORC Exists

ORC was created by Hortonworks to be the **fastest** columnar format for Hadoop/Hive. While Parquet focuses on compatibility across engines, ORC focuses on **raw performance** in the Hadoop ecosystem.

**Think of it like this:** ORC is like a racing car tuned for a specific track (Hadoop). It's faster on that track than a regular sports car (Parquet), but you can only race it on that one track. Parquet is like a versatile sports car that performs well on any road.

**The Problem ORC Solves:**
- Hive queries on TB-scale data were too slow
- Existing formats (RCFile) had poor compression
- Need for built-in indexes and statistics

**ORC's Solution:**
```
Traditional: Read 1 TB → Filter → Process = Slow
ORC: Read indexes → Skip 90% → Read 100 GB → Process = 10x faster
```

---

## Architecture: Stripes, Indexes & Statistics

ORC organizes files into **stripes** (similar to Parquet's row groups, but with better indexing):

<div class="mermaid">
flowchart TD
    FILE["ORC File"] --> STRIPE1["Stripe 1<br/>(250 MB default)"]
    FILE --> STRIPE2["Stripe 2"]
    FILE --> STRIPE3["Stripe 3"]
    
    STRIPE1 --> INDEX["Index Data<br/>(lightweight)"]
    STRIPE1 --> DATA["Column Data<br/>(compressed)"]
    STRIPE1 --> FOOTER["Stripe Footer<br/>(metadata)"]
    
    DATA --> C1["Column 1 Data"]
    DATA --> C2["Column 2 Data"]
    DATA --> C3["Column 3 Data"]
    
    INDEX --> I1["Row Index<br/>(every 10K rows)"]
    INDEX --> I2["Bloom Filters"]
    
    style FILE fill:#dbeafe,stroke:#2563eb
    style STRIPE1 fill:#d1fae5,stroke:#059669
    style INDEX fill:#fef3c7,stroke:#d97706
    style DATA fill:#fce7f3,stroke:#db2777
</div>

### 1. File Structure

```
my_data.orc
│
├── Postscript (metadata about file)
│
├── Stripe 1 (250 MB default)
│   ├── Index Data
│   │   ├── Row Group Index (every 10,000 rows)
│   │   │   ├── Min/Max values
│   │   │   ├── Sum (for numeric columns)
│   │   │   ├── HasNull flag
│   │   │   └── Positions (byte offsets)
│   │   │
│   │   └── Bloom Filters (optional)
│   │       └── Probabilistic set membership
│   │
│   ├── Column Data (compressed)
│   │   ├── Column 0 Stream (PRESENT stream - nulls)
│   │   ├── Column 0 Stream (DATA stream - values)
│   │   ├── Column 1 Stream
│   │   └── ...
│   │
│   └── Stripe Footer
│       └── Stream locations & metadata
│
├── Stripe 2
│   └── ... (same structure)
│
└── File Footer
    ├── Schema (type tree)
    ├── Stripe Statistics (min/max across stripes)
    ├── Column Statistics (global)
    ├── Stripe Locations
    └── User Metadata
```

---

## Key Difference from Parquet: Three-Level Indexing

> **How it works:** ORC is like a book with a table of contents, chapter summaries, AND page indexes — three levels of shortcuts! Parquet just has a table of contents. This makes ORC faster at finding specific data, but only if you're using software (like Hive) that knows how to use all three levels.
> 
> **Think of it like this:** Imagine looking for a specific scene in a movie. ORC gives you: (1) which DVD, (2) which chapter, (3) which minute. Parquet just tells you which DVD. Both work, but ORC can skip more if your player supports it!

ORC has **much more aggressive indexing** than Parquet:

<div class="mermaid">
flowchart TD
    QUERY["Query:<br/>WHERE age > 40"]
    
    QUERY --> L1["Level 1: File Statistics<br/>Min age: 18, Max age: 65"]
    L1 --> |"✅ File contains matches"| L2
    
    L2["Level 2: Stripe Statistics<br/>Stripe 1: min=18, max=35<br/>Stripe 2: min=36, max=65"]
    L2 --> |"❌ Skip Stripe 1"| SKIP1
    L2 --> |"✅ Read Stripe 2"| L3
    
    L3["Level 3: Row Group Index<br/>RG1: min=36, max=40<br/>RG2: min=41, max=50<br/>RG3: min=51, max=65"]
    L3 --> |"❌ Skip RG1"| SKIP2
    L3 --> |"✅ Read RG2 & RG3"| READ
    
    style QUERY fill:#dbeafe,stroke:#2563eb
    style L1 fill:#fef3c7,stroke:#d97706
    style L2 fill:#d1fae5,stroke:#059669
    style L3 fill:#fce7f3,stroke:#db2777
    style SKIP1 fill:#fecaca,stroke:#dc2626
    style SKIP2 fill:#fecaca,stroke:#dc2626
    style READ fill:#d1fae5,stroke:#059669
</div>

**Result:** ORC can skip 90%+ of data before even decompressing it!

---

## Type System

ORC has a rich built-in type system (unlike Parquet's physical/logical split):

| ORC Type | Description | Storage |
|----------|-------------|---------|
| **Primitives** |
| `boolean` | true/false | 1 bit (RLE encoded) |
| `tinyint` | 8-bit signed integer | 1 byte |
| `smallint` | 16-bit signed integer | 2 bytes |
| `int` | 32-bit signed integer | 4 bytes |
| `bigint` | 64-bit signed integer | 8 bytes |
| `float` | 32-bit floating point | 4 bytes |
| `double` | 64-bit floating point | 8 bytes |
| `string` | UTF-8 text | Variable |
| `binary` | Raw bytes | Variable |
| `timestamp` | Date + time (nanosecond precision) | 8 bytes |
| `date` | Date only | 4 bytes (days since epoch) |
| `decimal` | Fixed-point decimal | Variable |
| **Complex Types** |
| `array<T>` | List of elements | Nested encoding |
| `map<K,V>` | Key-value pairs | Nested encoding |
| `struct<...>` | Named fields | Nested encoding |
| `union<...>` | One of several types | Tagged union |

### Nested Types Example

```sql
CREATE TABLE events (
  id bigint,
  user struct<
    name: string,
    age: int,
    emails: array<string>
  >,
  metadata map<string, string>
) STORED AS ORC;
```

ORC stores this as a **column tree**:

```
Column 0: id (bigint)
Column 1: user (struct)
  Column 2: user.name (string)
  Column 3: user.age (int)
  Column 4: user.emails (array)
    Column 5: user.emails.element (string)
Column 6: metadata (map)
  Column 7: metadata.key (string)
  Column 8: metadata.value (string)
```

Each column in the tree is compressed independently!

---

## Encoding Schemes

ORC uses different encodings based on data type and patterns:

### 1. Run Length Encoding (RLE)

For repeated values (especially booleans and integers):

```python
# Original data
values = [5, 5, 5, 5, 7, 7, 3, 3, 3]

# RLE encoded
encoded = [(5, 4), (7, 2), (3, 3)]
```

**ORC's RLE Versions:**
- **RLE v1:** Original encoding
- **RLE v2:** Improved, handles varying run lengths better

### 2. Dictionary Encoding

For low-cardinality columns:

```python
# Original (1M rows)
status = ["active", "inactive", "pending", "active", ...]

# Dictionary
dictionary = {
  0: "active",
  1: "inactive", 
  2: "pending"
}

# Data stored as IDs (integer stream)
ids = [0, 1, 2, 0, ...]
```

**When Used:**
- String columns with < 50% unique values
- Automatically enabled by ORC writer

### 3. Delta Encoding

For sequential/sorted integers:

```python
# Original timestamps
values = [1000, 1001, 1002, 1003]

# Delta encoded
base = 1000
deltas = [0, 1, 1, 1]  # Smaller numbers → better compression
```

### 4. Direct Encoding

For random/unpredictable data, store values directly (no encoding).

### 5. PRESENT Stream (Null Tracking)

ORC separates null tracking into its own stream:

```python
# Original data
values = [5, null, 7, null, 9]

# ORC storage
PRESENT stream: [1, 0, 1, 0, 1]  # Bitmap (1 = present, 0 = null)
DATA stream:    [5, 7, 9]         # Only non-null values
```

**Benefit:** Can skip entire DATA stream if all values are null!

---

## Compression

ORC supports multiple compression codecs:

| Codec | Speed | Ratio | CPU | Best For |
|-------|-------|-------|-----|----------|
| **ZLIB** | 🐌 Slow | Excellent | High | Default, archival |
| **Snappy** | ⚡⚡⚡ Very Fast | Good | Low | Real-time queries |
| **LZO** | ⚡⚡ Fast | Good | Medium | Hadoop standard |
| **LZ4** | ⚡⚡⚡ Very Fast | Good | Low | Best speed/ratio balance |
| **ZSTD** | ⚡⚡ Fast | Best | Medium | Modern default |
| **None** | ⚡⚡⚡⚡ Instant | 1x | None | Pre-compressed data |

**Compression Stack:**
```
1. Type System:   INT, STRING, etc.
2. Encoding:      RLE, Dictionary, Delta
3. Compression:   ZLIB/Snappy/ZSTD (per stream)
4. Disk:         Final bytes
```

**Unlike Parquet:** ORC compresses each stream independently!

```
Column: age (INT)
  └─ PRESENT stream (nulls) → Compressed with ZLIB
  └─ DATA stream (values)   → Compressed with ZLIB

Column: name (STRING)  
  └─ PRESENT stream         → Compressed with ZLIB
  └─ DATA stream (values)   → Compressed with ZLIB
  └─ LENGTH stream (lengths)→ Compressed with ZLIB
```

---

## Bloom Filters: ORC's Secret Weapon

> **What's a Bloom filter?** A super-fast "cheat sheet" that says "this data definitely ISN'T here" without checking every single row. 
> 
> **Real-world example:** You're looking for your friend John at a huge concert. Instead of checking every single person, someone at the entrance says "John definitely didn't enter through this gate." You just saved hours! That's what Bloom filters do — they quickly rule out where data ISN'T, so you don't waste time looking there.

ORC can build **Bloom filters** for columns to test set membership:

<div class="mermaid">
flowchart LR
    QUERY["Query:<br/>WHERE email = 'john@example.com'"]
    
    QUERY --> BLOOM["Check Bloom Filter"]
    BLOOM --> |"Definitely NOT in row group"| SKIP["Skip entire row group"]
    BLOOM --> |"Might be in row group"| READ["Read & check data"]
    
    style QUERY fill:#dbeafe,stroke:#2563eb
    style BLOOM fill:#fef3c7,stroke:#d97706
    style SKIP fill:#fecaca,stroke:#dc2626
    style READ fill:#d1fae5,stroke:#059669
</div>

**How It Works:**
```python
# Bloom filter characteristics
- False Positive Rate: ~1% (configurable)
- Space: ~1-2% of column size
- Speed: O(1) membership test

# Query: WHERE user_id = 12345
1. Check Bloom filter → "Definitely not in this row group"
2. Skip reading 10,000 rows!
```

**Enable Bloom Filters:**
```sql
CREATE TABLE users (
  id bigint,
  email string
) STORED AS ORC
TBLPROPERTIES (
  "orc.bloom.filter.columns"="email",
  "orc.bloom.filter.fpp"="0.01"  -- 1% false positive rate
);
```

**When to Use:**
- High-cardinality columns (user IDs, emails)
- Equality predicates (`WHERE id = 123`)
- NOT useful for range queries (`WHERE age > 30`)

---

## Predicate Pushdown: Three Layers

ORC's multi-level statistics enable aggressive pruning:

### Layer 1: Stripe-Level Statistics

```python
# Query: WHERE age BETWEEN 25 AND 35

Stripe 1: min_age=18, max_age=24  → ❌ Skip (max < 25)
Stripe 2: min_age=25, max_age=40  → ✅ Read (overlaps range)
Stripe 3: min_age=41, max_age=65  → ❌ Skip (min > 35)
```

### Layer 2: Row Group Statistics

```python
# Within Stripe 2
Row Group 1: min=25, max=28  → ✅ Read (in range)
Row Group 2: min=29, max=32  → ✅ Read (in range)  
Row Group 3: min=33, max=36  → ✅ Read (overlaps)
Row Group 4: min=37, max=40  → ❌ Skip (min > 35)
```

### Layer 3: Bloom Filter Check

```python
# Query: WHERE email = 'alice@example.com'

Row Group 1: Bloom filter says "NOT present" → ❌ Skip
Row Group 2: Bloom filter says "MAYBE present" → ✅ Read & verify
```

**Combined Effect:**
```
Original: 1 TB of data
After stripe pruning: 200 GB (skipped 800 GB)
After row group pruning: 50 GB (skipped 150 GB)
After bloom filters: 10 GB (skipped 40 GB)

Final: Read only 1% of data! 🚀
```

---

## ACID Support (in Hive 3.0+)

> **Important limitation:** This ACID feature ONLY works in Hive — not in Spark, Python, or most other tools. If you need ACID transactions that work everywhere, use **Delta Lake** instead (which works with Parquet and is much more widely supported).

ORC is the **only** format with native ACID support in Hive:

<div class="mermaid">
flowchart TD
    BASE["Base File<br/>base_0001.orc"]
    
    UPDATE1["Update:<br/>UPDATE users SET status = 'active'"]
    UPDATE1 --> DELTA1["Delta File<br/>delta_0002.orc"]
    
    UPDATE2["Delete:<br/>DELETE FROM users WHERE age < 18"]
    UPDATE2 --> DELTA2["Delta File<br/>delta_0003.orc"]
    
    READ["Read Query"] --> MERGE["Merge base + deltas"]
    BASE --> MERGE
    DELTA1 --> MERGE
    DELTA2 --> MERGE
    
    COMPACT["Compaction"] --> NEWBASE["New Base File<br/>(merged)"]
    
    style BASE fill:#dbeafe,stroke:#2563eb
    style DELTA1 fill:#fef3c7,stroke:#d97706
    style DELTA2 fill:#fef3c7,stroke:#d97706
    style MERGE fill:#d1fae5,stroke:#059669
</div>

**How ACID Works:**

```sql
-- Enable ACID on table
CREATE TABLE users (
  id bigint,
  name string,
  status string
) STORED AS ORC
TBLPROPERTIES ('transactional'='true');

-- Now you can UPDATE/DELETE (not possible with plain Parquet!)
UPDATE users SET status = 'inactive' WHERE id = 123;
DELETE FROM users WHERE created_date < '2020-01-01';
```

**Under the Hood:**
1. **Base files:** Original data (immutable)
2. **Delta files:** Changes (updates/deletes)
3. **Read:** Merge base + deltas on-the-fly
4. **Compaction:** Periodically merge deltas into new base

**Limitations:**
- Only works in Hive/Tez (not Spark, Presto)
- Performance degrades without compaction
- More complex than append-only formats

---

## ORC vs Parquet: Head-to-Head

| Feature | ORC | Parquet | Winner |
|---------|-----|---------|--------|
| **Indexing** | 3-level + Bloom filters | Basic statistics | 🏆 **ORC** |
| **Compression** | Slightly better | Excellent | 🏆 **ORC** (slightly) |
| **Read Speed** | Faster (in Hive) | Fast | 🏆 **ORC** (in Hadoop) |
| **Compatibility** | Hadoop-focused | Engine-agnostic | 🏆 **Parquet** |
| **Nested Types** | Excellent | Excellent | 🤝 Tie |
| **ACID Support** | ✅ Yes (Hive 3+) | ❌ No | 🏆 **ORC** |
| **Ecosystem** | Hive, Pig, Presto | Spark, Pandas, DuckDB, Snowflake | 🏆 **Parquet** |
| **Bloom Filters** | ✅ Built-in | ❌ No | 🏆 **ORC** |
| **Popularity** | Declining | Growing | 🏆 **Parquet** |

---

## Performance Comparison

```python
import time
import pandas as pd

# Create test data (10M rows)
df = pd.DataFrame({
    'id': range(10_000_000),
    'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 10_000_000),
    'value': np.random.randn(10_000_000)
})

# Write ORC
df.to_orc('data.orc', compression='zlib')
orc_size = os.path.getsize('data.orc') / 1024 / 1024

# Write Parquet
df.to_parquet('data.parquet', compression='snappy')
parquet_size = os.path.getsize('data.parquet') / 1024 / 1024

print(f"ORC size:     {orc_size:.1f} MB")
print(f"Parquet size: {parquet_size:.1f} MB")

# Read with filter
start = time.time()
df_orc = pd.read_orc('data.orc')  # Note: pandas doesn't support ORC predicate pushdown
df_orc = df_orc[df_orc['category'] == 'A']
orc_time = time.time() - start

start = time.time()
df_parquet = pd.read_parquet('data.parquet', filters=[('category', '==', 'A')])
parquet_time = time.time() - start

print(f"\nFiltered read:")
print(f"ORC:     {orc_time:.2f}s")
print(f"Parquet: {parquet_time:.2f}s")
```

**Typical Results (Hive/Spark with predicate pushdown):**
```
Size:
ORC:     78 MB (slightly smaller)
Parquet: 85 MB

Filtered Read (with pushdown):
ORC:     0.12s (bloom filters help!)
Parquet: 0.18s
```

**But in Python/Pandas:**
```
ORC:     3.50s (no predicate pushdown support)
Parquet: 0.15s (excellent pushdown support)
```

**Winner depends on tool!**

---

## Best Practices

### 1. Sort Data Before Writing

```sql
-- Sort by frequently filtered columns
CREATE TABLE users_sorted
STORED AS ORC
AS SELECT * FROM users
ORDER BY country, signup_date;

-- Result: Better statistics → more pruning
```

### 2. Enable Bloom Filters for High-Cardinality Columns

```sql
CREATE TABLE events (
  event_id string,
  user_id bigint,
  timestamp timestamp
) STORED AS ORC
TBLPROPERTIES (
  "orc.bloom.filter.columns"="event_id,user_id",
  "orc.bloom.filter.fpp"="0.05"
);
```

### 3. Tune Stripe Size

```sql
-- Default: 250 MB (good for most cases)
-- Smaller stripes → more parallelism, more overhead
-- Larger stripes → less parallelism, better compression

CREATE TABLE large_table (...)
STORED AS ORC
TBLPROPERTIES ("orc.stripe.size"="134217728");  -- 128 MB
```

### 4. Use ZSTD Compression (Modern Default)

```sql
CREATE TABLE users (...)
STORED AS ORC
TBLPROPERTIES ("orc.compress"="ZSTD");
```

**Compression Advice:**
- **ZSTD:** Best all-around (modern default)
- **Snappy:** Fastest reads (real-time analytics)
- **ZLIB:** Smallest files (archival)

### 5. Monitor Schema Evolution

```sql
-- Add column (safe)
ALTER TABLE users ADD COLUMNS (phone string);

-- Rename column (requires rewrite)
ALTER TABLE users CHANGE COLUMN email email_address string;
```

ORC supports schema evolution, but some operations are expensive.

---

## Common Pitfalls

### 1. Using ORC Outside Hadoop Ecosystem

```
❌ Python/Pandas → Poor ORC support, slow
✅ Python/Pandas → Use Parquet instead

❌ DuckDB → Limited ORC support
✅ DuckDB → Use Parquet instead

✅ Hive/Presto → Excellent ORC support
```

### 2. Not Using Bloom Filters

```sql
-- Without bloom filters
SELECT * FROM users WHERE user_id = 123;
-- Reads all row groups → Slow

-- With bloom filters
CREATE TABLE users (...)
TBLPROPERTIES ("orc.bloom.filter.columns"="user_id");
-- Skips 99% of row groups → 100x faster
```

### 3. Small Files Problem

```
❌ 10,000 files × 1 MB = Huge metadata overhead
✅ 100 files × 100 MB = Fast
```

### 4. Not Compacting ACID Tables

```sql
-- ACID tables accumulate delta files
-- Without compaction: Reads become slow!

-- Solution: Regular compaction
ALTER TABLE users COMPACT 'MAJOR';
```

### 5. Wrong Stripe Size

```
❌ Stripe size = 10 MB → Too much metadata overhead
❌ Stripe size = 1 GB → Not enough parallelism
✅ Stripe size = 128-256 MB → Good balance
```

---

## Should You Use ORC?

> **Quick Decision Guide:**
> - ✅ **Use ORC:** Your company uses Hadoop/Hive and someone told you to use ORC
> - ❌ **Use Parquet:** You're using anything else (Python, Spark, cloud databases, modern tools)
> - ✅ **Use ORC:** You need ACID transactions in Hive specifically
> - ❌ **Use Parquet:** You need to work with multiple tools or systems
> 
> **The reality:** ORC adoption is declining. Most companies are moving to Parquet because it works everywhere. Unless you're locked into a Hadoop environment, **use Parquet**. Even Apache Spark (which used ORC initially) now recommends Parquet as the default.
> 
> **When ORC actually makes sense:**
> - You're at a company with a huge existing Hadoop investment
> - You're doing data warehousing specifically in Hive
> - You need Hive's ACID feature

## When to Use ORC

<div class="mermaid">
flowchart TD
    START["Choose ORC when:"]
    
    START --> H["Using Hive/Hadoop"]
    START --> A["Need ACID transactions"]
    START --> B["Have high-cardinality<br/>columns (IDs, emails)"]
    START --> P["Need best possible<br/>compression"]
    
    START2["Choose Parquet when:"]
    
    START2 --> S["Using Spark/Pandas"]
    START2 --> M["Multi-engine compatibility"]
    START2 --> E["Python/R analytics"]
    
    style START fill:#d1fae5,stroke:#059669
    style START2 fill:#fef3c7,stroke:#d97706
</div>

### ✅ Use ORC For:

1. **Hadoop/Hive workloads**
   ```sql
   -- ORC is optimized for Hive
   CREATE TABLE users (...) STORED AS ORC;
   ```

2. **ACID transactions**
   ```sql
   -- Only ORC supports ACID in Hive
   UPDATE users SET status = 'active' WHERE id = 123;
   ```

3. **High-cardinality columns**
   ```sql
   -- Bloom filters excel here
   WHERE user_id = '8f3a7b2c-...'
   ```

4. **Maximum compression**
   - ORC typically 5-10% smaller than Parquet

### ❌ Use Parquet Instead For:

1. **Multi-engine compatibility**
   - Spark, Pandas, DuckDB, Snowflake, BigQuery

2. **Python/R data science**
   - Much better library support

3. **Cloud-native analytics**
   - Parquet is the de facto standard

4. **Modern data lakes**
   - Delta Lake, Iceberg use Parquet (not ORC)

---

## Migration Guide: Parquet ↔ ORC

### Parquet to ORC

```sql
-- In Hive
CREATE TABLE users_orc
STORED AS ORC
AS SELECT * FROM users_parquet;

-- Preserve partitions
CREATE TABLE users_orc (...)
PARTITIONED BY (year int, month int)
STORED AS ORC;

INSERT INTO users_orc PARTITION (year, month)
SELECT * FROM users_parquet;
```

### ORC to Parquet

```python
# In PySpark
df = spark.read.orc("data.orc")
df.write.parquet("data.parquet", compression="snappy")
```

---

## Real-World Example

```sql
-- E-commerce events table (100 TB)
CREATE TABLE events (
  event_id string,
  user_id bigint,
  event_type string,
  product_id bigint,
  timestamp timestamp,
  metadata map<string, string>
)
PARTITIONED BY (
  year int,
  month int,
  day int
)
STORED AS ORC
TBLPROPERTIES (
  "orc.compress"="ZSTD",
  "orc.stripe.size"="268435456",  -- 256 MB stripes
  "orc.bloom.filter.columns"="event_id,user_id,product_id",
  "orc.bloom.filter.fpp"="0.01"
);

-- Query: Find specific user's events
SELECT *
FROM events
WHERE year = 2024
  AND month = 12
  AND user_id = 123456;

-- Execution:
-- 1. Partition pruning: Only scan year=2024/month=12 (skip 99%)
-- 2. Stripe pruning: Check stripe statistics
-- 3. Bloom filter: Skip stripes without user_id=123456
-- 4. Row group pruning: Skip row groups without user_id=123456
-- Result: Read < 0.1% of data!
```

---

## Summary

> **Quick Takeaways:**
> - **What is ORC?** A file format designed specifically for Hadoop (a big data system)
> - **Like Parquet but...** Faster in Hadoop, but ONLY works well in Hadoop
> - **Should you use it?** Only if you're in a Hadoop/Hive environment
> - **When NOT to use it?** Python, Spark, cloud tools, modern data systems
> - **The reality:** ORC is declining in popularity. Most companies use Parquet now.
> - **Bottom line:** Unless someone at your company specifically told you to use ORC for Hadoop/Hive, **use Parquet instead**. Parquet works everywhere; ORC doesn't.

ORC is a **high-performance** columnar format designed for Hadoop:

**Key Strengths:**
1. ✅ **Three-level indexing** (like a book with table of contents, chapter summaries, AND page indexes)
2. ✅ **Bloom filters** (super-fast "this data isn't here" checks)
3. ✅ **Excellent compression** (5-10% better than Parquet)
4. ✅ **ACID support** in Hive (but ONLY in Hive!)
5. ✅ **Aggressive predicate pushdown** (skips irrelevant data very efficiently)

**Key Weaknesses:**
1. ❌ **Hadoop-focused** (limited support in Python, R, modern tools)
2. ❌ **Not the de facto standard** (Parquet is more popular and universal)
3. ❌ **Poor Python/R support** (hard to use outside Hadoop)
4. ❌ **Declining ecosystem** (fewer tools being built for it)
5. ❌ **Vendor lock-in** (ties you to Hadoop/Hive infrastructure)

**Decision Matrix:**

| Your Situation | Recommendation |
|----------------|----------------|
| Hive/Hadoop data warehouse | 🏆 **Use ORC** |
| Spark + multi-engine | Use Parquet |
| Python data science | Use Parquet |
| Need ACID (in Hive) | 🏆 **Use ORC** |
| Cloud-native data lake | Use Parquet |
| Maximum compression | 🏆 **Use ORC** (slightly better) |

**The Bottom Line:**
- **Hive-centric?** → ORC is faster
- **Everything else?** → Parquet is safer

---

## Further Reading

- [ORC Specification](https://orc.apache.org/specification/)
- [ORC vs Parquet Benchmark](https://www.youtube.com/watch?v=1j8SdS7s_NY)
- [Hive ACID Tables](https://cwiki.apache.org/confluence/display/Hive/Hive+Transactions)
