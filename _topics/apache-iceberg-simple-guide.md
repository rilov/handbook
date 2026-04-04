---
title: "How Apache Iceberg Actually Works (And Why It's Perfect for AI)"
category: Data
order: 2
tags:
  - iceberg
  - data-architecture
  - generative-ai
  - machine-learning
  - table-format
  - lakehouse
summary: A user-friendly technical guide to Apache Iceberg's architecture - how it works under the hood, why it's different from traditional tables, and why it's the go-to choice for AI/ML workloads.
---

# How Apache Iceberg Actually Works (And Why It's Perfect for AI)

## The Definitive Winner of the Table Format Wars

Apache Iceberg has emerged as the **definitive winner in the table format wars of 2024–2025**. With Databricks acquiring Tabular (founded by Iceberg's creators), Snowflake launching Polaris (an Iceberg-based catalog), and major cloud providers standardizing on Iceberg, it's clear that this isn't just another data technology.

**Apache Iceberg isn't just a table format; it's the foundation of the modern data lakehouse**, turning chaos into a structured, reliable, and blazing-fast platform.

### Industry Adoption in 2025

The momentum behind Iceberg is undeniable:

- **Databricks + Tabular:** Databricks acquired Tabular (founded by Iceberg creators Ryan Blue, Dan Weeks, and Jason Reid) to double down on Iceberg support
- **Snowflake Polaris:** Snowflake's open-source Iceberg catalog service, making Iceberg a first-class citizen
- **AWS, Azure, GCP:** All three major cloud providers now offer native Iceberg support in their data lake services
- **Netflix, Apple, Adobe, LinkedIn, Airbnb:** Production deployments at petabyte scale
- **Query engines:** Spark, Flink, Trino, Presto, Hive, Impala, Dremio, StarRocks all support Iceberg

**But what makes Iceberg so revolutionary? And more importantly, how does it actually work under the hood?**

This guide will take you on a journey from the fundamental problems Iceberg solves to the cutting-edge features arriving in 2025.

---

## The Data Lake Problems Iceberg Was Built to Solve

Every data engineer who has wrangled a large data lake knows the pain points. Traditional Hive-style tables on HDFS or cloud storage tend to accumulate a lot of baggage over time. Apache Iceberg was created to tackle several of these very real problems head-on:

### 1. The Small Files Problem

**The Issue:**
As data volumes grow, you often end up with thousands of tiny files scattered across your data lake. Each file requires separate I/O operations, metadata tracking, and planning overhead.

**Real-world impact:**
- A simple query on a day's data can take **minutes just to plan** because it has to scan every partition directory and open thousands of files
- 10,000 small files (10MB each) vs. 100 large files (1GB each): Same data, 100x slower queries
- Cloud storage charges per API call: More files = higher costs

**How Iceberg solves it:**
- Manifest files track all data files with statistics
- Query planning reads manifests (small), not data files (large)
- Built-in compaction to merge small files
- Planning time: Seconds instead of minutes

### 2. Data Corruption and Inconsistency

**The Issue:**
Without proper ACID guarantees, concurrent writes or job failures leave behind partial data. Maybe one process deletes rows by overwriting files while another reads mid-change; the result is often half-updated data and corruption.

**Real-world scenarios:**
- Job A deletes old data by removing files
- Job B reads the table at the same time
- Job B sees partial data (some files deleted, some not)
- Result: Incorrect analytics, broken pipelines

**How Iceberg solves it:**
- Full ACID transactions with snapshot isolation
- Atomic commits: All changes succeed or all fail
- Readers always see consistent snapshots
- No more "eventually consistent" data lakes

### 3. Brittle Partitioning Schemes

**The Issue:**
In older systems, how you partitioned the data was something every user had to know. If the table was partitioned by date, but a user's query forgot to filter on that column, it would inadvertently scan the whole dataset.

**The Hive problem:**
```sql
-- Table partitioned as: /data/year=2024/month=01/day=15/
-- User MUST include partition columns in WHERE clause
SELECT * FROM events 
WHERE year=2024 AND month=1 AND day=15  -- Forgot this? Full scan!
  AND user_id = 12345;
```

**How Iceberg solves it:**
- **Hidden partitioning:** Users query natural columns, Iceberg handles partition pruning
- **Partition evolution:** Change partitioning without rewriting data
- No more exposing physical layout to users

### 4. Painful Schema Changes

**The Issue:**
Evolving a table's schema (adding columns, changing data types) used to be a risky operation. In Hive you might have to rebuild the table or live with awkward hacks. Many teams avoided schema updates altogether because renaming or removing a column could break downstream jobs or require rewriting all your data.

**Traditional approach:**
1. Create new table with new schema
2. Copy all data to new table (days/weeks for TB/PB)
3. Update all queries to use new table
4. Hope nothing breaks

**How Iceberg solves it:**
- Schema evolution in **milliseconds** (metadata-only)
- Column IDs ensure backward compatibility
- Add, rename, drop, reorder columns safely
- Old files work with new schema automatically

---

## What Exactly Is Apache Iceberg?

Apache Iceberg is a **table format for large analytic datasets**; essentially a set of rules and metadata that define how to treat a bunch of data files as a coherent table.

**Key points:**
- **Not a processing engine:** Doesn't replace Spark or Trino
- **Not a file format:** Your data stays in Parquet, ORC, or Avro
- **Not a storage system:** Works with S3, HDFS, Azure, GCS

**What it IS:**
A specification (and library implementations) for how to manage table metadata. This means you can use Iceberg tables with your engine of choice; Spark, Flink, Trino, Presto, Hive, Impala can all read and write the same Iceberg table in a transactionally consistent way.

**The key insight:** Instead of treating data as a collection of files, Iceberg treats it as a **table** with full ACID guarantees, schema evolution, time travel, and partition evolution - all while keeping your data in open formats.

## Iceberg's Architecture: The Three Layers

Iceberg's power comes from its **three-layer architecture**. Understanding these layers is key to understanding how Iceberg works.

<div class="mermaid">
graph TD
    A["<b>Query Engine</b><br/>Spark/Trino/Flink"] --> B["<b>Catalog Layer</b>"]
    B --> C["<b>Metadata File</b><br/>v42.metadata.json"]
    C --> D["<b>Manifest List</b><br/>snap-123.avro"]
    D --> E1["<b>Manifest 1</b><br/>Jan 2024"]
    D --> E2["<b>Manifest 2</b><br/>Feb 2024"]
    D --> E3["<b>Manifest 3</b><br/>Mar 2024"]
    E1 --> F1["<b>Data Files</b><br/>data-001.parquet"]
    E1 --> F2["<b>Data Files</b><br/>data-002.parquet"]
    E2 --> F3["<b>Data Files</b><br/>data-003.parquet"]
    E2 --> F4["<b>Data Files</b><br/>data-004.parquet"]
    E3 --> F5["<b>Data Files</b><br/>data-005.parquet"]
    E3 --> F6["<b>Data Files</b><br/>data-006.parquet"]
    
    style A fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style B fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style C fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style D fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style E1 fill:#607D8B,stroke:#455A64,stroke-width:2px,color:#fff
    style E2 fill:#607D8B,stroke:#455A64,stroke-width:2px,color:#fff
    style E3 fill:#607D8B,stroke:#455A64,stroke-width:2px,color:#fff
    style F1 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style F2 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style F3 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style F4 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style F5 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style F6 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
</div>

### Layer 1: The Catalog

**What it is:** A simple pointer to the current metadata file.

**What it does:** The catalog stores the location of the current metadata file for each table. That's it. It's intentionally simple.

**Examples:**
- **Hive Metastore:** Traditional choice, widely supported
- **AWS Glue:** Managed catalog for AWS
- **Nessie:** Git-like catalog with branching
- **REST Catalog:** HTTP-based catalog for cloud-native setups

```python
# Catalog just points to metadata location
catalog.get_table("my_database.customers")
# Returns: s3://warehouse/customers/metadata/v42.metadata.json
```

### Layer 2: The Metadata Layer

This is where the magic happens. The metadata layer consists of:

#### 2a. Metadata Files (JSON)

**What it stores:**
- Current schema (columns, types)
- Partition spec (how data is organized)
- Snapshot history (every version of the table)
- Current snapshot pointer
- Table properties and configuration

**Example metadata.json:**
```json
{
  "format-version": 2,
  "table-uuid": "9c12d441-03fe-4693-9a96-a0705ddf69c1",
  "location": "s3://warehouse/customers",
  "last-updated-ms": 1704067200000,
  "last-column-id": 5,
  "schema": {
    "type": "struct",
    "fields": [
      {"id": 1, "name": "customer_id", "required": true, "type": "long"},
      {"id": 2, "name": "name", "required": false, "type": "string"},
      {"id": 3, "name": "email", "required": false, "type": "string"},
      {"id": 4, "name": "signup_date", "required": false, "type": "date"}
    ]
  },
  "current-snapshot-id": 3051729675574597004,
  "snapshots": [
    {
      "snapshot-id": 3051729675574597004,
      "timestamp-ms": 1704067200000,
      "manifest-list": "s3://warehouse/customers/metadata/snap-3051729675574597004-1-a4d5.avro"
    }
  ],
  "partition-spec": [
    {"name": "signup_date_month", "transform": "month", "source-id": 4, "field-id": 1000}
  ]
}
```

**Key insight:** Metadata files are **immutable**. Each change creates a new metadata file. This enables atomic commits and time travel.

#### 2b. Manifest Lists (Avro)

**What it is:** A list of manifest files for a snapshot.

**What it stores:**
- Paths to manifest files
- Partition summaries (min/max values)
- File counts and sizes

**Why it matters:** Query engines can skip entire manifest files based on partition filters without reading them.

#### 2c. Manifest Files (Avro)

**What it is:** A list of data files with detailed statistics.

**What it stores for each data file:**
- File path
- File format (Parquet, ORC, Avro)
- Partition values
- Record count
- File size
- Column-level statistics (min, max, null count)
- Lower/upper bounds for each column

**Example manifest entry:**
```json
{
  "data_file": {
    "file_path": "s3://warehouse/customers/data/signup_date_month=2024-01/data-001.parquet",
    "file_format": "PARQUET",
    "partition": {"signup_date_month": "2024-01"},
    "record_count": 125000,
    "file_size_in_bytes": 52428800,
    "column_sizes": {"1": 1000000, "2": 5000000, "3": 3000000},
    "value_counts": {"1": 125000, "2": 125000, "3": 125000},
    "null_value_counts": {"1": 0, "2": 50, "3": 100},
    "lower_bounds": {"1": 1, "4": "2024-01-01"},
    "upper_bounds": {"1": 125000, "4": "2024-01-31"}
  }
}
```

**Why this matters:** Query engines can skip data files based on column statistics without reading them. This is called **data skipping** or **predicate pushdown**.

### Layer 3: Data Files

**What it is:** Your actual data in open formats (Parquet, ORC, Avro).

**Key point:** Iceberg doesn't dictate the data file format. You can use Parquet (most common), ORC, or Avro. The data files are completely independent of Iceberg's metadata.

**File organization:**
```
s3://warehouse/customers/
├── metadata/
│   ├── v1.metadata.json
│   ├── v2.metadata.json
│   ├── snap-3051729675574597004-1-a4d5.avro  (manifest list)
│   └── a4d5-m0.avro  (manifest file)
└── data/
    ├── signup_date_month=2024-01/
    │   ├── data-001.parquet
    │   └── data-002.parquet
    └── signup_date_month=2024-02/
        └── data-003.parquet
```

**Visual representation of the metadata hierarchy:**

<div class="mermaid">
graph LR
    A["<b>Catalog</b><br/>Hive/Glue/Nessie"] -->|"<b>points to</b>"| B["<b>v42.metadata.json</b>"]
    B -->|"<b>current snapshot</b>"| C["<b>Snapshot</b><br/>3051729675574597004"]
    C -->|"<b>manifest list</b>"| D["<b>snap-305...a4d5.avro</b>"]
    D -->|"<b>contains</b>"| E["<b>Manifest</b><br/>a4d5-m0.avro"]
    E -->|"<b>lists</b>"| F1["<b>data-001.parquet</b><br/>125K rows<br/>customer_id: 1-62500"]
    E -->|"<b>lists</b>"| F2["<b>data-002.parquet</b><br/>125K rows<br/>customer_id: 62501-125000"]
    
    style A fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style B fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style C fill:#E91E63,stroke:#C2185B,stroke-width:3px,color:#fff
    style D fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style E fill:#607D8B,stroke:#455A64,stroke-width:3px,color:#fff
    style F1 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style F2 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
</div>

## How Queries Work: The Power of Metadata

Let's walk through what happens when you query an Iceberg table:

### Query Example

```sql
SELECT name, email 
FROM customers 
WHERE signup_date >= '2024-01-01' 
  AND signup_date < '2024-02-01'
  AND customer_id > 50000;
```

### Step-by-Step Execution

**Step 1: Catalog Lookup**
```
Query Engine → Catalog: "Where is customers table?"
Catalog → Query Engine: "s3://warehouse/customers/metadata/v42.metadata.json"
```

**Step 2: Read Metadata File**
```
Query Engine reads v42.metadata.json
- Current snapshot: 3051729675574597004
- Manifest list: snap-3051729675574597004-1-a4d5.avro
- Schema: customer_id (long), name (string), email (string), signup_date (date)
- Partition spec: month(signup_date)
```

**Step 3: Read Manifest List**
```
Query Engine reads manifest list
- Manifest 1: signup_date_month=2024-01 (125,000 rows)
- Manifest 2: signup_date_month=2024-02 (130,000 rows)
- Manifest 3: signup_date_month=2024-03 (128,000 rows)

Partition Pruning: Skip Manifests 2 and 3 (not in date range)
```

**Step 4: Read Manifest Files**
```
Query Engine reads Manifest 1
- data-001.parquet: customer_id range [1-62500]
- data-002.parquet: customer_id range [62501-125000]

Data Skipping: Skip data-001.parquet (customer_id max is 62500, query needs > 50000)
Read only data-002.parquet
```

**Step 5: Read Data Files**
```
Query Engine reads data-002.parquet
- Column pruning: Only read 'name' and 'email' columns (skip customer_id, signup_date)
- Row filtering: Apply customer_id > 50000 filter
- Return results
```

### Performance Impact

**Traditional approach (no Iceberg):**
- Read all 3 months of data (383,000 rows)
- Read all columns
- Filter in memory
- **Time: 30 seconds**

**With Iceberg:**
- Partition pruning: Skip 2 months (255,000 rows)
- Data skipping: Skip 1 data file (62,500 rows)
- Column pruning: Read only 2 columns instead of 4
- **Time: 2 seconds (15x faster)**

**This is why Iceberg is so fast for AI/ML workloads that need to scan massive datasets.**

## Snapshots and Time Travel

### What is a Snapshot?

A **snapshot** is a complete state of the table at a specific point in time. Each snapshot has:
- A unique snapshot ID
- A timestamp
- A pointer to a manifest list
- The schema at that time
- The partition spec at that time

**Key insight:** Snapshots are **immutable**. Once created, they never change.

### How Snapshots Enable Time Travel

```python
# Current data
df_current = spark.read.table("customers")

# Data as of specific timestamp
df_yesterday = spark.read \
    .option("as-of-timestamp", "2024-01-15 10:00:00") \
    .table("customers")

# Data as of specific snapshot ID
df_snapshot = spark.read \
    .option("snapshot-id", "3051729675574597004") \
    .table("customers")

# View all snapshots
spark.sql("SELECT * FROM customers.snapshots").show()
```

**Output:**
```
+--------------------+-------------------+----------+-----------+
|      snapshot_id   |committed_at       |parent_id |operation  |
+--------------------+-------------------+----------+-----------+
|3051729675574597004 |2024-01-15 10:00:00|null      |append     |
|3051729675574597005 |2024-01-15 14:30:00|...97004  |append     |
|3051729675574597006 |2024-01-16 09:15:00|...97005  |overwrite  |
+--------------------+-------------------+----------+-----------+
```

### Snapshot Lifecycle

<div class="mermaid">
graph LR
    A["<b>Snapshot 1</b><br/>Jan 15, 10am<br/>ID: ...7004"] --> B["<b>Snapshot 2</b><br/>Jan 15, 2pm<br/>ID: ...7005"]
    B --> C["<b>Snapshot 3</b><br/>Jan 16, 9am<br/>ID: ...7006"]
    
    A -.->|"<b>references</b>"| D1["<b>100 data files</b>"]
    B -.->|"<b>references</b>"| D1
    B -.->|"<b>adds</b>"| D2["<b>2 new files</b>"]
    C -.->|"<b>references</b>"| D1
    C -.->|"<b>references</b>"| D2
    C -.->|"<b>adds</b>"| D3["<b>3 new files</b>"]
    
    style A fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style B fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style C fill:#E91E63,stroke:#C2185B,stroke-width:3px,color:#fff
    style D1 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style D2 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style D3 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
</div>

**Important:** Old data files are NOT deleted when new snapshots are created. They're kept for time travel and rollback.

**Snapshot evolution over time:**
- Snapshot 1: 100 files
- Snapshot 2: 102 files (100 old + 2 new)
- Snapshot 3: 105 files (100 old + 2 from S2 + 3 new)

### Snapshot Expiration

To prevent unlimited growth, old snapshots are eventually expired:

```sql
-- Expire snapshots older than 7 days
CALL catalog.system.expire_snapshots(
  table => 'customers',
  older_than => TIMESTAMP '2024-01-08 00:00:00',
  retain_last => 10  -- Always keep at least 10 snapshots
);
```

**What happens:**
- Snapshots older than 7 days are removed from metadata
- Data files referenced ONLY by expired snapshots are deleted
- Data files referenced by retained snapshots are kept

## Schema Evolution: Adding Columns Without Rewrites

### The Problem with Traditional Tables

In traditional data lakes, adding a column requires:
1. Rewrite every single data file with the new column
2. Update partition folders
3. Rebuild indexes
4. **Time:** Days or weeks for petabyte-scale data
5. **Cost:** Thousands of dollars in compute

### How Iceberg Handles Schema Evolution

Iceberg uses **schema-on-read** with column IDs:

**Initial schema:**
```json
{
  "fields": [
    {"id": 1, "name": "customer_id", "type": "long"},
    {"id": 2, "name": "name", "type": "string"},
    {"id": 3, "name": "email", "type": "string"}
  ]
}
```

**Add a column:**
```sql
ALTER TABLE customers ADD COLUMN phone STRING;
```

**New schema:**
```json
{
  "fields": [
    {"id": 1, "name": "customer_id", "type": "long"},
    {"id": 2, "name": "name", "type": "string"},
    {"id": 3, "name": "email", "type": "string"},
    {"id": 4, "name": "phone", "type": "string"}  // NEW!
  ]
}
```

**What happens:**
1. New metadata file created with updated schema (takes milliseconds)
2. Old data files: Don't have column 4, readers return NULL
3. New data files: Include column 4
4. **Time:** Instant (metadata-only operation)
5. **Cost:** Free

### Supported Schema Changes

```sql
-- Add column (safe)
ALTER TABLE customers ADD COLUMN loyalty_points INT;

-- Rename column (safe - uses column IDs)
ALTER TABLE customers RENAME COLUMN email TO email_address;

-- Drop column (safe - column ID marked as deleted)
ALTER TABLE customers DROP COLUMN old_field;

-- Change column type (safe if compatible)
ALTER TABLE customers ALTER COLUMN customer_id TYPE BIGINT;

-- Reorder columns (safe - uses column IDs)
ALTER TABLE customers ALTER COLUMN phone AFTER name;
```

**Why this works:** Iceberg uses **column IDs** instead of column positions. Old files with column ID 1 map to `customer_id` regardless of position.

## Partition Evolution: Changing Organization Without Rewrites

### The Problem with Traditional Partitioning

Traditional Hive-style partitioning is **physical** - the partition is part of the file path:

```
s3://data/customers/signup_year=2024/signup_month=01/data.parquet
```

**Problems:**
1. Users must include partition filters: `WHERE signup_year=2024 AND signup_month=01`
2. Forget the filter? Full table scan!
3. Change partitioning? Rewrite all data!

### Iceberg's Hidden Partitioning

Iceberg uses **logical partitioning** - partitions are derived from column values:

```sql
CREATE TABLE events (
  event_id BIGINT,
  event_time TIMESTAMP,
  user_id BIGINT
)
PARTITIONED BY (days(event_time));
```

**User query (no partition knowledge needed):**
```sql
SELECT * FROM events 
WHERE event_time >= '2024-01-15' 
  AND event_time < '2024-01-16';
```

**What Iceberg does:**
1. Transforms `event_time >= '2024-01-15'` to `days(event_time) = 19737`
2. Reads only files with partition value 19737
3. User doesn't need to know about partitioning!

### Partition Spec Evolution

**Start with daily partitions:**
```sql
PARTITIONED BY (days(event_time))
```

**Later, change to hourly (no data rewrite!):**
```sql
ALTER TABLE events 
SET PARTITION SPEC (hours(event_time));
```

**What happens:**
- Old data: Still partitioned by day
- New data: Partitioned by hour
- Queries work on both!
- Metadata tracks which files use which partition spec

**Partition transforms available:**
```sql
-- Temporal
PARTITIONED BY (years(timestamp_col))   -- Year
PARTITIONED BY (months(timestamp_col))  -- Month
PARTITIONED BY (days(timestamp_col))    -- Day
PARTITIONED BY (hours(timestamp_col))   -- Hour

-- Bucketing
PARTITIONED BY (bucket(16, user_id))    -- 16 buckets

-- Truncation
PARTITIONED BY (truncate(10, name))     -- First 10 chars

-- Identity
PARTITIONED BY (region)                 -- Use value as-is
```

## ACID Transactions and Optimistic Concurrency

### The Problem: Concurrent Writes

Multiple writers updating the same table simultaneously can cause:
- **Lost updates:** Writer 2 overwrites Writer 1's changes
- **Partial writes:** Failure leaves table in inconsistent state
- **Duplicate data:** Same data written twice

### How Iceberg Provides ACID Guarantees

Iceberg uses **optimistic concurrency control** with atomic metadata swaps:

**Write Process:**

1. **Writer reads current metadata**
   ```
   Current metadata: v42.metadata.json
   Current snapshot: 3051729675574597004
   ```

2. **Writer creates new data files**
   ```
   Write new data to: data-new-001.parquet, data-new-002.parquet
   ```

3. **Writer creates new manifest**
   ```
   Create manifest listing new data files
   ```

4. **Writer creates new metadata file**
   ```
   Create v43.metadata.json:
   - Parent snapshot: 3051729675574597004
   - New snapshot: 3051729675574597007
   - New manifest list pointing to new manifests
   ```

5. **Atomic commit**
   ```
   Catalog.compareAndSwap(
     expected: "v42.metadata.json",
     new: "v43.metadata.json"
   )
   ```

**If successful:** Table now points to v43
**If failed:** Another writer updated first, retry with new base

### Concurrent Write Example

**Scenario:** Two writers append data simultaneously

<div class="mermaid">
sequenceDiagram
    participant W1 as Writer 1
    participant Cat as Catalog
    participant W2 as Writer 2
    
    W1->>Cat: Read current metadata (v42)
    W2->>Cat: Read current metadata (v42)
    
    Note over W1: Write data-w1.parquet
    Note over W2: Write data-w2.parquet
    
    Note over W1: Create v43.metadata<br/>(parent: v42)
    Note over W2: Create v43.metadata<br/>(parent: v42, different!)
    
    W1->>+Cat: Commit v42→v43 ✅
    Cat-->>-W1: Success!
    
    W2->>+Cat: Commit v42→v43 ❌
    Cat-->>-W2: Conflict! Current is v43
    
    W2->>Cat: Read current metadata (v43)
    Note over W2: Create v44.metadata<br/>(parent: v43)
    W2->>+Cat: Commit v43→v44 ✅
    Cat-->>-W2: Success!
</div>

**Result:** Both writes succeed, no data loss, table is consistent.

**Key insight:** Optimistic concurrency with atomic compare-and-swap ensures ACID guarantees without locks.

### Supported Operations

```python
# Append (add new data)
df.writeTo("customers").append()

# Overwrite (replace all data)
df.writeTo("customers").overwrite()

# Overwrite partition (replace specific partition)
df.writeTo("customers") \
  .overwritePartitions()

# Merge (upsert)
spark.sql("""
  MERGE INTO customers t
  USING updates s
  ON t.customer_id = s.customer_id
  WHEN MATCHED THEN UPDATE SET *
  WHEN NOT MATCHED THEN INSERT *
""")

# Delete
spark.sql("DELETE FROM customers WHERE signup_date < '2020-01-01'")
```

All operations are **atomic** - either fully succeed or fully fail.

## Why Iceberg is Perfect for AI/ML Workloads

### 1. Fast Data Scanning with Partition Pruning

**AI training needs to scan billions of rows.** Iceberg's partition pruning makes this 10-100x faster.

**Example: Training a recommendation model**
```python
# Need last 90 days of user interactions
training_data = spark.read.table("user_interactions") \
    .filter("event_date >= current_date() - interval 90 days")
```

**Without Iceberg:**
- Scan all 2 years of data (730 days)
- Read 10 billion rows
- Time: 2 hours

**With Iceberg:**
- Partition pruning: Read only 90 days
- Read 1.2 billion rows
- Time: 8 minutes (15x faster)

### 2. Reproducible ML with Time Travel

**Problem:** "Our model performed better last week. What changed?"

**Solution:**
```python
# Current training data
current_data = spark.read.table("training_corpus")
model_v2 = train_model(current_data)
# Accuracy: 87%

# Last week's training data (exact snapshot)
last_week_data = spark.read \
    .option("as-of-timestamp", "2024-01-15 10:00:00") \
    .table("training_corpus")
model_v1 = train_model(last_week_data)
# Accuracy: 92%

# Compare data distributions
current_stats = current_data.describe()
last_week_stats = last_week_data.describe()
# Found: Data quality dropped due to new source
```

**Use cases:**
- **Model reproducibility:** Retrain with exact same data
- **A/B testing:** Compare models trained on different snapshots
- **Debugging:** Identify when data quality degraded
- **Compliance:** "What data was used to train this model?"

### 3. Schema Evolution for Feature Engineering

**AI models need new features constantly.** Iceberg makes this instant.

**Week 1: Basic features**
```sql
CREATE TABLE features (
  user_id BIGINT,
  total_purchases DOUBLE,
  avg_session_duration DOUBLE
);
```

**Week 2: Add embeddings (instant!)**
```sql
ALTER TABLE features 
ADD COLUMN user_embedding ARRAY<FLOAT>;
```

**Week 3: Add sentiment scores (instant!)**
```sql
ALTER TABLE features 
ADD COLUMN avg_sentiment DOUBLE;
```

**No data rewrites, no downtime, no cost.**

### 4. Concurrent Access for Real-Time Features

**Modern ML needs real-time feature updates while training.**

```python
# Streaming job: Update features every minute
streaming_features = spark.readStream \
    .format("kafka") \
    .load() \
    .select("user_id", "last_click", "session_duration")

streaming_features.writeStream \
    .format("iceberg") \
    .outputMode("append") \
    .toTable("features.user_behavior")

# Training job: Read features (concurrent!)
training_data = spark.read.table("features.user_behavior") \
    .filter("timestamp >= current_date() - interval 30 days")

model = train_model(training_data)
```

**Both jobs run simultaneously without conflicts!**

### 5. Efficient Storage for Embeddings

**AI generates massive embedding datasets.** Iceberg handles this efficiently.

```python
# Generate embeddings for 1 billion documents
embeddings = documents.select(
    "doc_id",
    "category",
    generate_embedding_udf("text").alias("embedding")  # 768-dim vector
)

# Store in Iceberg with partitioning
embeddings.writeTo("embeddings.documents") \
    .partitionedBy("category") \
    .create()

# Query similar documents (partition pruning!)
query_embedding = generate_embedding("machine learning")

similar = spark.read.table("embeddings.documents") \
    .filter("category = 'technology'")  # Reads only tech partition \
    .select(
        "doc_id",
        cosine_similarity("embedding", query_embedding).alias("score")
    ) \
    .orderBy("score", ascending=False) \
    .limit(10)
```

**Iceberg only reads the 'technology' partition, skipping millions of irrelevant documents.**

---

## Format Version 3: The Future is Here (2025)

Apache Iceberg v3, arriving in 2025, brings revolutionary new capabilities that further cement its position as the lakehouse standard.

### New Data Types for Modern Workloads

**Geospatial Support:**
```sql
-- Native geospatial data types
CREATE TABLE locations (
    id BIGINT,
    point GEOMETRY,
    region GEOGRAPHY,
    timestamp TIMESTAMP WITH TIME ZONE  -- Nanosecond precision
);

-- Query with spatial predicates
SELECT * FROM locations
WHERE ST_Within(point, ST_MakeEnvelope(-122.5, 37.7, -122.3, 37.9));
```

**Semi-Structured Data with VARIANT Type:**
```sql
-- Flexible schema for JSON-like data
CREATE TABLE events (
    id BIGINT,
    metadata VARIANT,  -- Stores any JSON structure
    timestamp TIMESTAMP WITH TIME ZONE
);

-- Query nested fields without schema definition
SELECT 
    id,
    metadata:user.name::STRING as user_name,
    metadata:event.type::STRING as event_type
FROM events
WHERE metadata:event.category::STRING = 'purchase';
```

**Why this matters for AI:**
- Store embeddings, model metadata, and feature vectors in VARIANT columns
- Geospatial AI for location-based predictions
- Nanosecond timestamps for high-frequency trading and IoT data

### Row Lineage and Advanced CDC

Row lineage enables efficient change data capture by tracking row evolution:

<div class="mermaid">
graph LR
    A["<b>Original Row</b><br/>customer_id: 123<br/>name: Alice<br/>version: 1"] -->|"<b>UPDATE</b>"| B["<b>Updated Row</b><br/>customer_id: 123<br/>name: Alice Smith<br/>version: 2"]
    B -->|"<b>UPDATE</b>"| C["<b>Updated Row</b><br/>customer_id: 123<br/>name: Alice Johnson<br/>version: 3"]
    
    A -.->|"<b>lineage tracked</b>"| D["<b>Row ID: abc-123</b>"]
    B -.->|"<b>lineage tracked</b>"| D
    C -.->|"<b>lineage tracked</b>"| D
    
    style A fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style B fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style C fill:#E91E63,stroke:#C2185B,stroke-width:3px,color:#fff
    style D fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
</div>

```sql
-- Enable row lineage
ALTER TABLE customers SET TBLPROPERTIES (
    'format-version' = '3',
    'write.metadata.row-lineage.enabled' = 'true'
);

-- Track changes over time
SELECT 
    customer_id,
    name,
    _iceberg_row_id,
    _iceberg_row_version,
    _iceberg_commit_timestamp
FROM customers.changes
WHERE _iceberg_commit_timestamp > TIMESTAMP '2024-01-15 00:00:00';
```

**Benefits:**
- Efficient incremental processing (only process changed rows)
- Complete audit trail for compliance
- Simplified CDC pipelines
- Track data lineage for ML feature stores

### Materialized Views

V3 introduces native materialized view support:

```sql
-- Create a materialized view
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    region, 
    date_trunc('day', order_date) as day, 
    sum(amount) as total_sales,
    count(*) as order_count
FROM orders
GROUP BY region, date_trunc('day', order_date);

-- Automatic incremental refresh based on source changes
REFRESH MATERIALIZED VIEW sales_summary;

-- Query the materialized view (blazing fast!)
SELECT * FROM sales_summary
WHERE region = 'US-WEST' AND day >= '2024-01-01';
```

**Why this matters:**
- Pre-aggregated data for real-time dashboards
- Incremental refresh (only process new data)
- Automatic dependency tracking
- Perfect for ML feature stores with aggregated features

---

## Performance Optimization: Making Iceberg Sing

### File Layout Strategies and Compaction

Compaction is crucial for maintaining performance as data accumulates:

**The Problem:**
- Streaming writes create many small files
- Small files = slow queries (more I/O operations)
- Cloud storage charges per API call

**The Solution:**
```sql
-- Compact small files into larger ones
CALL system.rewrite_data_files(
    table => 'events',
    strategy => 'binpack',
    options => map(
        'target-file-size-bytes', '536870912',  -- 512MB target
        'min-input-files', '5'  -- Only compact if 5+ small files
    )
);
```

**Results:**
- Before: 10,000 files @ 10MB each = 100GB
- After: 200 files @ 512MB each = 100GB
- Query planning: 30 seconds → 2 seconds
- Query execution: 5 minutes → 30 seconds

### Z-Ordering for Multi-Dimensional Queries

Z-ordering optimizes data layout for queries across multiple dimensions:

**The Problem:**
Traditional partitioning works for one dimension (e.g., date), but queries often filter on multiple columns (user_id, event_type, timestamp).

**Z-Ordering Solution:**
```sql
-- Apply Z-ordering during compaction
CALL system.rewrite_data_files(
    table => 'events',
    strategy => 'sort',
    sort_order => 'zorder(user_id, event_time, session_id)'
);
```

**How it works:**
Z-ordering interleaves values from multiple columns, creating a space-filling curve that preserves locality across all dimensions.

<div class="mermaid">
graph TD
    subgraph S1["<b>Without Z-Ordering (Row-based)</b>"]
        A1["<b>user_id:</b> 1,1,1,2,2,2,3,3,3"]
        A2["<b>event_time:</b> 10:00,10:05,10:10,10:00,10:05,10:10,10:00,10:05,10:10"]
        A3["<b>Query: user_id=2 AND time=10:05</b><br/>Must scan entire dataset"]
    end
    
    subgraph S2["<b>With Z-Ordering (Interleaved)</b>"]
        B1["<b>Z-curve:</b> (1,10:00), (1,10:05), (2,10:00), (1,10:10), (2,10:05), (3,10:00)..."]
        B2["<b>Query: user_id=2 AND time=10:05</b><br/>Skip to relevant section<br/>2.5x fewer rows scanned!"]
    end
    
    style S1 fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#000
    style S2 fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#000
    style A1 fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    style A2 fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    style A3 fill:#F44336,stroke:#B71C1C,stroke-width:3px,color:#fff
    style B1 fill:#66BB6A,stroke:#2E7D32,stroke-width:2px,color:#fff
    style B2 fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
</div>

**Visual representation of Z-ordering space-filling curve:**

```
Traditional (sorted by user_id only):
  File 1: user_id [1-1000], all times mixed
  File 2: user_id [1001-2000], all times mixed
  → Query for user_id=1500 AND time=10:00 scans entire File 2

Z-ordered (interleaved user_id and time):
  File 1: user_id [1-500, time 09:00-10:00]
  File 2: user_id [1-500, time 10:00-11:00]
  File 3: user_id [501-1000, time 09:00-10:00]
  → Query for user_id=1500 AND time=10:00 reads only relevant files
```

**Real-world benchmark:**
- Query: `WHERE user_id = 12345 AND event_time BETWEEN '10:00' AND '11:00'`
- Without Z-ordering: Scan 5.4M rows → 5.0 seconds
- With Z-ordering: Scan 1.2M rows → 2.1 seconds
- **Improvement: 2.5x fewer rows scanned, 2.4x faster**

### Partition Evolution in Action

Iceberg allows you to change partitioning schemes without rewriting data:

```sql
-- Start with daily partitions (low data volume)
CREATE TABLE events (
    event_id BIGINT,
    event_time TIMESTAMP,
    user_id BIGINT
)
PARTITIONED BY (days(event_time));

-- 6 months later: Data volume increased, need hourly partitions
ALTER TABLE events 
ADD PARTITION FIELD hours(event_time);

-- Old data: Still uses daily partitions
-- New data: Uses hourly partitions
-- Queries work seamlessly across both schemes!

SELECT * FROM events
WHERE event_time BETWEEN '2024-01-15 10:00:00' AND '2024-01-15 11:00:00';
-- Iceberg automatically prunes both daily and hourly partitions
```

**Why this matters:**
- No downtime for partition changes
- No expensive data rewrites
- Adapt partitioning as data volume grows
- Perfect for evolving AI workloads

---

## Real-World Performance: The Numbers Don't Lie

Recent benchmarks demonstrate Iceberg's performance advantages in production environments:

### Query Planning Speed

**Traditional Hive on S3:**
- Table: 10TB, 50,000 files
- Query planning time: **3-5 minutes**
- Reason: Must list all files in S3, read partition metadata

**Iceberg:**
- Same table: 10TB, 50,000 files
- Query planning time: **< 1 second**
- Reason: Read single metadata file with all file statistics

**Impact:** 180-300x faster query planning

### File Skipping Efficiency

**Benchmark: TPC-DS Query on 1TB Dataset**

| Configuration | Rows Scanned | Files Read | Query Time |
|--------------|--------------|------------|------------|
| No optimization | 5.4M rows | 1,200 files | 5.0s |
| Partitioning only | 3.2M rows | 720 files | 3.5s |
| Partitioning + Z-ordering | 1.2M rows | 280 files | 2.1s |

**Result: 2.4x faster with Z-ordering**

### Storage Efficiency: Compaction Matters

**Case Study: Streaming CDC Table (1 week of data)**

**Without Compaction (Upsolver-optimized):**
- Table size: 77GB
- Storage used: 78GB (1% overhead)
- File count: 141 files
- Average file size: 545MB
- Query time: 2.3 seconds

**With Poor Compaction (AWS Glue default):**
- Table size: 144GB
- Storage used: 1,600GB (11x overhead!)
- File count: 326 files
- Average file size: 442MB
- Query time: 8.7 seconds

**Impact:**
- **20x storage overhead** with poor compaction
- **3.8x slower queries**
- **Higher cloud storage costs**

**Lesson:** Compaction strategy matters enormously!

### Real-Time Analytics Performance

**Use Case: Media Company Processing 50TB Daily**

**Setup:**
- Streaming ingestion with Apache Flink
- Merge-on-read for high-frequency updates
- Hidden partitioning by hour(timestamp)
- Z-ordering on (user_id, content_id, timestamp)

**Results:**
- Ingestion throughput: 500K events/second
- Query latency (p95): < 500ms
- Concurrent queries: 100+ without degradation
- Data freshness: Real-time (< 1 second lag)

**Traditional approach would require:**
- Separate streaming and batch systems
- Data duplication (2x storage cost)
- Minutes of latency for batch updates

---

## Real-World Examples

### Example 1: Training ChatGPT-Style AI

**The Situation:**
OpenAI needs to train a new language model using text from websites, books, and code.

**With Iceberg:**
1. **Collect data** from different sources (websites, books, code) - all goes into one organized place
2. **Add quality ratings** later when they figure out how to measure quality - takes 5 seconds
3. **Filter for best data** - Iceberg instantly finds only high-quality English text from recent years
4. **Train the model** - 100x faster because Iceberg skips irrelevant data
5. **Model not working well?** Go back in time to see what data they used last month
6. **Compare versions** - Figure out what changed and why

### Example 2: Netflix Recommendations

**The Situation:**
Netflix wants to recommend shows based on what you're watching RIGHT NOW.

**With Iceberg:**
- **Real-time updates:** Every time you click, that data is added immediately
- **AI training:** At the same time, their AI is learning from everyone's clicks
- **No conflicts:** Both can happen simultaneously without breaking anything
- **Always current:** Recommendations get better every minute

### Example 3: Self-Driving Cars

**The Situation:**
Tesla trains AI using videos from millions of cars.

**With Iceberg:**
- **Track every version:** "Model v1.0 used data from January, Model v2.0 used data from February"
- **Reproduce results:** 6 months later, they can retrain Model v1.0 with the EXACT same data
- **Debug problems:** "Why did the car make a mistake?" → Check what training data was used
- **Compliance:** "What data trained this AI?" → Iceberg knows exactly

### Example 4: Cross-Engine Data Mesh

**The Situation:**
An enterprise retail company runs a federated data mesh where different teams use their preferred tools.

**With Iceberg:**
- **Marketing team:** Runs ad-hoc queries with Trino for campaign analysis
- **Data engineering:** Processes batch jobs with Spark for ETL
- **Real-time team:** Uses Flink for streaming aggregations
- **ML team:** Trains models with PyTorch reading Iceberg tables via Arrow

**All teams read and write the same tables with full consistency:**
- No data silos
- No data duplication
- No conflicts
- Single source of truth

### Example 5: Financial Services CDC

**The Situation:**
A financial services firm uses Iceberg's equality delete files to implement efficient CDC from transactional systems.

**Implementation:**
```sql
-- Updates to customer records captured as deletes + inserts
MERGE INTO customers t
USING customer_updates s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

**Benefits:**
- Complete audit trail for regulatory compliance
- Fast incremental processing (only scan changed data)
- Time travel for point-in-time regulatory reports
- Efficient storage (equality deletes are small)

---

## The Iceberg Ecosystem Right Now

Based on the **2025 State of the Apache Iceberg Ecosystem Survey** with data professionals actively using Iceberg in production:

### Catalog Landscape: Competitive and Fragmented

The catalog market remains highly competitive with no single dominant player:

**Leading Catalogs by Adoption:**
- **AWS Glue (39.3%):** Leading adoption due to AWS gravity, native Iceberg support with automatic compaction
- **Project Nessie (28.6%):** Git-like catalog with branching, merging, tagging, and cross-table transactions
- **Amazon S3 Tables (25%):** AWS-native Iceberg table management
- **Apache Polaris (21.4%):** Snowflake's open-source catalog, now an Apache Top-Level Project with vendor-neutral REST API
- **Lakekeeper (21.4%):** Lightweight Rust-based catalog with single binary deployment
- **Hive Metastore (17.9%):** Traditional choice, still widely supported

**Emerging Catalogs:**
- **Apache Gravitino (Incubating):** Federated metadata lake for multi-source governance
- **Databricks Unity Catalog:** Open-sourced in 2024, multi-format (Delta + Iceberg via UniForm), multi-engine governance
- **REST Catalog:** Lightweight HTTP-based catalog for cloud-native deployments

**Key Insight:** Polaris's 21.4% adoption early in its Apache lifecycle signals strong momentum around open REST-aligned governance. The fragmented landscape reflects active competition in governance, federation, and metadata standardization.

### Cloud and Infrastructure Patterns

**Primary Deployment Environments:**
- **AWS (64.3%):** Dominant cloud platform, driven by S3 performance and Glue integration
- **Local Development (42.9%):** Strong developer-driven experimentation
- **On-Premises (28.6%):** Significant enterprise deployments
- **Multi-Cloud (21.4%):** Growing hybrid architectures
- **Azure (17.9%):** Synapse Analytics integration
- **GCP (17.9%):** BigLake support

**Managed Services:**
- **AWS:** Athena (serverless queries), EMR (Spark/Flink/Hive), Glue (catalog + ETL)
- **Azure:** Synapse Analytics with native Iceberg support
- **GCP:** BigLake for multi-cloud analytics
- **Databricks:** Unity Catalog with Delta-Iceberg interoperability
- **Snowflake:** Native Iceberg tables + Polaris catalog

### Query Engines: Spark Dominates, Multi-Engine Reality

**Survey Results - Engine Usage:**
- **Apache Spark (96.4%):** Near-universal adoption, foundational for ingestion, transformation, and metadata operations
- **Trino OSS (60.7%):** Strong traction for interactive analytics
- **Apache Flink (32.1%):** Stream processing and real-time ingestion
- **DuckDB (28.6%):** Growing interest in lightweight, embedded analytics
- **Amazon Athena (21.4%):** Serverless query engine
- **Dremio (17.9%):** High-performance lakehouse engine optimized for Iceberg

**Full Iceberg Support by Category:**

**Batch Processing:**
- Apache Spark 3.5+ (full read/write, merge, delete, time travel)
- Trino 400+ (full DML support, partition evolution)
- Presto (read/write operations)
- Apache Hive 4.0+ (legacy compatibility)
- Dremio (optimized metadata handling)

**Stream Processing:**
- Apache Flink 1.18+ (streaming read/write, CDC)
- Spark Structured Streaming (micro-batch + continuous)
- Apache Kafka with Iceberg Sink Connector

**Interactive Analytics:**
- Snowflake (native Iceberg tables)
- Databricks SQL (Delta + Iceberg via UniForm)
- AWS Athena (serverless, native support)
- Google BigQuery (via BigLake)
- StarRocks (high-performance OLAP)
- Apache Doris (real-time analytics)

**Lightweight/Embedded:**
- DuckDB (in-process analytics)
- PyIceberg (Python-native library)

**Key Insight:** Iceberg is inherently multi-engine. While Spark dominates at 96.4%, the ecosystem supports diverse workloads from streaming (Flink) to interactive (Trino) to embedded (DuckDB).

### Ingestion Patterns: Engine-Centric Workflows

**Primary Ingestion Methods:**
- **Distributed OSS Engines (71.4%):** Spark or Flink for data landing
- **Same Engine for Ingestion + Analytics (10.7%):** Unified workflows

**ETL and Streaming Tools:**
- **Apache Kafka Connect (50%):** Leading streaming integration
- **AWS Glue Jobs (22.7%):** Managed ETL service
- **Debezium (18.2%):** Change data capture
- **Airbyte:** Iceberg destination connector
- **Fivetran:** Iceberg connector for SaaS data
- **Apache NiFi:** Iceberg processors for data flow

**Key Insight:** The ecosystem remains oriented around open compute engines rather than turnkey SaaS ELT platforms.

### Data Transformation & Modeling

**SQL-Centric Tools:**
- **dbt (dbt-iceberg):** Iceberg models with incremental strategies
- **SQL Interface (46.4%):** Dominant interface preference
- **Python (25%):** PyIceberg, PySpark
- **Java/Scala (25%):** Spark, Flink applications

### Governance & Observability

**Access Control:**
- Apache Ranger (fine-grained permissions)
- Unity Catalog (unified governance)
- Polaris (catalog-level access control)
- Nessie (branch-based isolation)

**Metadata Management:**
- OpenMetadata (catalog and lineage)
- DataHub (metadata discovery)
- Apache Atlas (metadata governance)

**Data Quality & Observability:**
- Monte Carlo (data observability)
- Great Expectations (data validation)
- Soda (data quality checks)

### ML & AI Platforms

**Feature Stores:**
- Feast (feature store on Iceberg)
- Tecton (real-time feature platform)
- Databricks Feature Store (Unity Catalog integration)

**ML Frameworks:**
- Ray (distributed ML on Iceberg)
- PyTorch/TensorFlow (via PyArrow)
- MLflow (experiment tracking with Iceberg tables)

**AI/ML Integration:**
- PyIceberg (Python-native library for ML workflows)
- Arrow Flight (high-performance data transfer)
- Pandas/Polars (DataFrame integration)

### Production Scale Reality

**Largest Iceberg Table Sizes in Production:**
- **10-100 TB (28.6%):** Most common production scale
- **< 1 TB (21.4%):** Smaller workloads and experimentation
- **1-10 TB (17.9%):** Mid-size deployments
- **100 TB - 1 PB (17.9%):** Large-scale analytics
- **> 1 PB (10.7%):** Massive data lakes

**Key Insight:** Iceberg is not confined to small datasets. Nearly half of production deployments manage tables larger than 10 TB, with 28.6% operating at petabyte scale.

### Feature Priorities: What Users Want

**Most Interesting v3 Features:**
- **Row-Level Lineage (33.3%):** Governance visibility and CDC
- **Deletion Vectors (25.9%):** Update efficiency
- **Variant Datatype (22.2%):** Semi-structured data support
- **Geo Types:** Geospatial analytics

**Most Exciting Potential v4 Features:**
- **Materialized Views (37%):** Performance acceleration
- **Parquet-Based Metadata (22.2%):** Faster metadata operations
- **Secondary Indexes (22.2%):** Query optimization
- **Relative Paths:** Portability improvements

**Key Insight:** Production-driven concerns dominate. Users want performance optimization, governance visibility, and metadata intelligence layered onto the existing format foundation.

### Core Value Proposition

**What Resonates Most with Users:**
- **Interoperability Among Lakehouse Tools (35.7%):** Multi-engine compatibility
- **ACID Transactions with Less Duplicative Storage (35.7%):** Reliability + efficiency
- **Cost Reductions (14.3%):** Lower storage and compute costs
- **Faster Transactions vs Hive/Parquet (14.3%):** Performance improvements

### Satisfaction and Community Engagement

**Performance & Reliability Satisfaction (5-point scale):**
- **4 out of 5 (51.9%):** Strong satisfaction
- **5 out of 5 (18.5%):** Excellent
- **3 out of 5 (29.6%):** Moderate satisfaction
- **Low ratings:** Negligible

**Open Source Contribution:**
- **Occasional Contributors (46.2%):** Active participation
- **Plans to Contribute (42.3%):** Future engagement
- **Active Contributors (7.7%):** Core community members

**Key Insight:** The ecosystem is participatory and evolving through practitioner input. High satisfaction combined with strong contribution signals a healthy, production-ready technology.

### Strategic Observations for 2025

1. **Multi-Engine is Reality:** Spark at 96.4% is foundational, but Iceberg's value lies in cross-engine interoperability
2. **Catalog Fragmentation Persists:** No dominant catalog; Glue leads at 39.3%, but Nessie (28.6%) and Polaris (21.4%) show strong momentum
3. **AWS Gravity:** 64.3% on AWS, but multi-cloud (21.4%) and on-prem (28.6%) deployments are significant
4. **Production Scale:** Nearly half manage tables > 10 TB; this is not experimental technology
5. **Feature Direction:** Materialized views (37%), deletion vectors (25.9%), and row lineage (33.3%) point toward performance and governance focus
6. **Interoperability Wins:** 35.7% cite multi-tool compatibility as top value; Iceberg's open standard is its strength

**The Bottom Line:** Iceberg has crossed the production threshold. The next phase focuses on metadata optimization, governance clarity, and multi-engine coherence rather than basic transactional guarantees.

---

## Quick Comparison

| **What You Want to Do** | **Old Way** | **Iceberg Way** |
|-------------|----------------------|-------------------|
| Find specific data | Check every file (slow) | Check smart index (100x faster) |
| Add new information | Rewrite everything (days) | Update index (seconds) |
| See old versions | ❌ Can't do it | ✅ Go back to any date |
| Multiple people working | ❌ Conflicts and errors | ✅ Everyone works smoothly |
| Organize data | Manual work, easy to mess up | Automatic, always optimized |
| Fix mistakes | ❌ Can't undo | ✅ Instant rollback |
| Use for AI | ⚠️ Slow and difficult | ✅ Fast and easy |

---

## The Bottom Line

**What is Iceberg?**
A super-smart filing system for massive amounts of data.

**Why does it matter?**
- Makes finding data 100x faster
- Lets you go back in time to any version
- Lets you add new information instantly
- Lets multiple teams work together without conflicts

**Why do AI companies love it?**
1. **Speed:** Training AI models is 100x faster
2. **Time travel:** Can reproduce any result from the past
3. **Flexibility:** Can add new features in seconds, not weeks
4. **Reliability:** Multiple teams can work on the same data safely

**The simple truth:**
AI needs to read billions of pieces of data quickly, track every version, and let many people work together. Iceberg makes all of this easy.

That's why companies like Netflix, Apple, Adobe, LinkedIn, and Airbnb use Iceberg for their AI systems.

---

## Want to Learn More?

- **Official website:** [Apache Iceberg](https://iceberg.apache.org/)
- **Technical details:** [On-Premises Data Modernization Strategy](/handbook/topics/enterprise-data-modernization-strategy/)

---

## Final Thought

Iceberg isn't magic. It's just a smart way to keep track of where your data is, so you don't waste time looking in the wrong places.

But when you're working with billions of pieces of information (like training ChatGPT), that simple idea makes the difference between:
- Waiting 5 hours ❌
- Getting results in 5 minutes ✅

That's why every major AI company uses Iceberg. It's the secret ingredient that makes modern AI possible.
