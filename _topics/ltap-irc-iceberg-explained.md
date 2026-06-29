---
title: "LTAP, the IRC Catalog, and the Hidden Layers of Apache Iceberg"
category: Data
order: 4
tags:
  - iceberg
  - LTAP
  - IRC
  - catalog
  - data-lakehouse
  - transactions
  - analytics
  - beginners
  - friendly
summary: A plain-English guide to what LTAP (Lake Transactional/Analytical Processing) means, how the Iceberg REST Catalog (IRC) works as the universal phone book for tables, and how a SQL query actually travels through the Iceberg stack — from catalog lookup all the way to Parquet rows.
date: 2026-06-29
---

# LTAP, the IRC Catalog, and the Hidden Layers of Apache Iceberg

> *You write `SELECT * FROM orders`. Three letters later, rows appear on your screen. But between those two moments, something remarkable happens — metadata files, catalog API calls, file pruning, and snapshot isolation all coordinate silently underneath. This guide shows you exactly what's going on.*

---

## The Iceberg You Can't See

Imagine an actual iceberg floating in the ocean. What you see above the waterline is a small, clean tip. But 90% of the mass is hidden below.

Apache Iceberg works the same way.

Above the water: table names, SQL queries, schemas you can browse. The comfortable, familiar surface that analysts interact with every day.

Below the water: an entire hidden machinery — metadata files, snapshots, manifest lists, manifest files, and thousands of Parquet data files. None of this is visible when you run a query. But it's all doing work.

<img src="{{ site.baseurl }}/assets/img/iceberg-metaphor.svg" alt="Iceberg metaphor: SQL tables above the water, hidden metadata layers below" width="100%" />

The reason this matters is simple: **the hidden machinery is exactly what makes LTAP possible.**

---

## 1. What Is LTAP?

LTAP stands for **Lake Transactional/Analytical Processing**.

Before we explain what it *is*, let's understand the problem it solves.

### The old world had two separate systems

In the traditional data architecture, you had a hard split:

- **Transactional systems** (OLTP): databases like PostgreSQL or MySQL that handle writes — inserts, updates, deletes. Fast for individual row operations. Bad for large analytical scans.
- **Analytical systems** (OLAP): warehouses like Redshift or Snowflake that handle reporting and aggregations. Fast for large scans. Not designed for constant writes.

To get data from one world to the other, teams built ETL pipelines — nightly batch jobs that copied data across. The result: your analytics were always hours or days behind reality. And you were paying to store the same data twice.

<img src="{{ site.baseurl }}/assets/img/ltap-vs-traditional.svg" alt="LTAP vs Traditional: before shows two siloed systems with ETL lag; after shows one Iceberg lakehouse handling both" width="100%" />

### LTAP collapses that split

LTAP means doing both transactional and analytical work on the **same** table, on the **same** lake, at the **same** time — with no ETL lag, no data duplication, and full ACID guarantees.

You can run:

```sql
-- A transactional write
INSERT INTO orders VALUES (1234, 'Alice', 99.99, NOW());

-- And immediately after, an analytical query on the same table
SELECT region, SUM(amount) FROM orders GROUP BY region;
```

Both operations hit the same Iceberg table. There is no pipeline in between. The write and the read are isolated from each other by snapshot versioning — the analytical query sees a consistent view even while a write is in progress.

> **Memory trick:** LTAP is like a live spreadsheet that everyone edits and reads at the same time, but nobody ever sees a half-saved row.

---

## 2. What Makes LTAP Possible on a Data Lake?

Traditional data lakes (raw files on S3) had none of the properties needed for LTAP:

| Property | Raw S3 Files | Apache Iceberg |
|---|---|---|
| ACID transactions | ❌ No | ✅ Atomic commits |
| Read isolation during writes | ❌ No | ✅ Snapshot isolation |
| Row-level deletes and updates | ❌ Rewrite entire files | ✅ Delete files |
| Schema evolution | ❌ Manual, fragile | ✅ Tracked in metadata |
| Time travel | ❌ No history | ✅ Any past snapshot |
| Multi-engine access | ❌ Format-specific | ✅ Any engine via IRC |

Iceberg adds a metadata layer between the engine and the raw files. That metadata layer is what turns a dumb file store into a database-quality table.

And the entry point to all of it is the **IRC**.

---

## 3. The IRC — Iceberg REST Catalog

### What a catalog does

Before any query engine can read an Iceberg table, it needs to answer one question:

> *Where is the metadata for this table?*

A table called `db.orders` is just a name. The catalog maps that name to the physical location of a `metadata.json` file on S3 — something like:

```
s3://my-bucket/warehouse/db/orders/metadata/v3.metadata.json
```

That's the catalog's core job: **it's a phone book for tables.**

### What makes the IRC special

Before the Iceberg REST Catalog specification existed, every engine used a different catalog: Spark used the Hive Metastore, Trino had its own connectors, and so on. Sharing a table between Spark and Trino was painful.

The **IRC (Iceberg REST Catalog)** is a standardized HTTP API specification. Any engine that implements the client side of this spec can read any Iceberg table from any server that implements the server side.

This means:
- Spark, Trino, DuckDB, Flink, Snowflake, and Dremio all speak the same language when looking up tables.
- You can swap your catalog backend (Polaris, Nessie, Gravitino, Unity Catalog) without changing your engine configuration.
- Teams can share tables across completely different tools with zero data copying.

<img src="{{ site.baseurl }}/assets/img/irc-architecture.svg" alt="IRC Architecture: multiple engines connect to one REST catalog which maps table names to S3 metadata paths" width="100%" />

### What the IRC API looks like

The catalog exposes simple HTTP endpoints:

```
GET  /v1/namespaces                        → list all schemas
GET  /v1/namespaces/{ns}/tables            → list tables in a schema
GET  /v1/namespaces/{ns}/tables/{table}    → get table metadata location
POST /v1/namespaces/{ns}/tables            → create a new table
POST /v1/transactions/commit               → commit an ACID transaction
```

When an engine looks up a table, the catalog responds with something like this:

```json
{
  "metadata-location": "s3://my-bucket/warehouse/orders/metadata/v3.metadata.json",
  "metadata": {
    "table-uuid": "abc-123",
    "format-version": 2,
    "schema": { ... },
    "current-snapshot-id": 8749201
  }
}
```

That `metadata-location` is everything the engine needs. It goes directly to S3 and reads the rest itself — the catalog is not in the hot path for data reading.

> **Memory trick:** The catalog is the receptionist who tells you which room your meeting is in. After that, you walk there yourself — the receptionist isn't carrying you.

---

## 4. The Metadata Chain: What Lives Below the Waterline

Once an engine has the `metadata-location`, it follows a chain of files. Each file points to the next. Understanding this chain is the key to understanding why Iceberg queries are so fast.

### Level 1 — metadata.json

The root of everything. Contains:

- The table schema (column names and types)
- The partition spec (how data is physically split)
- The current snapshot ID
- A list of all past snapshots (for time travel)

```json
{
  "current-snapshot-id": 8749201,
  "snapshots": [
    { "snapshot-id": 8749201, "manifest-list": "s3://…/snap-8749201.avro" },
    { "snapshot-id": 8749200, "manifest-list": "s3://…/snap-8749200.avro" }
  ]
}
```

### Level 2 — Snapshot

A snapshot is a complete, immutable picture of the table at one point in time. When you insert 1,000 rows, Iceberg creates a new snapshot — it does **not** modify the old one. The old snapshot remains valid and readable. This is how time travel works:

```sql
-- Read the table as it was yesterday
SELECT * FROM orders FOR SYSTEM_TIME AS OF '2026-06-28';
```

### Level 3 — Manifest List

Each snapshot points to a manifest list — an Avro file listing all the manifest files that belong to this snapshot. It's a lightweight index.

### Level 4 — Manifest Files

Each manifest file is an Avro file containing one entry per data file. Crucially, each entry includes **column-level statistics**:

- Minimum value of each column
- Maximum value of each column
- Row count
- Null count

This is where the magic happens.

### Level 5 — Parquet Data Files

The actual rows. Each file typically contains millions of rows stored in columnar Parquet format on S3.

---

## 5. LTAP in Action: Tracing a Query End to End

Let's trace exactly what happens when you run:

```sql
SELECT region, SUM(amount)
FROM orders
WHERE order_date = '2026-06-29'
GROUP BY region;
```

<img src="{{ site.baseurl }}/assets/img/ltap-flow.svg" alt="LTAP query flow: 5 steps from SQL to Parquet rows, with file pruning reducing 10,000 files to 60" width="100%" />

**Step 1 — Parse the query.** Spark or Trino receives the SQL and identifies that it needs the `orders` table.

**Step 2 — Ask the IRC.** The engine calls:

```
GET /v1/namespaces/db/tables/orders
```

The catalog responds with the S3 path to `metadata.json`.

**Step 3 — Read metadata.json.** The engine fetches the metadata file directly from S3. It finds the current snapshot ID and the path to the manifest list.

**Step 4 — Prune files.** The engine reads the manifest list, then reads the manifest files. For each data file entry, it checks the statistics:

```
File: part-00042.parquet
  order_date min: 2026-06-29
  order_date max: 2026-06-29  ← matches filter → INCLUDE

File: part-00001.parquet
  order_date min: 2026-01-01
  order_date max: 2026-03-31  ← doesn't match → SKIP
```

If the table has 10,000 data files but only 60 contain data for June 29, only 60 files are read. The other 9,940 are skipped without a single I/O operation.

**Step 5 — Read data.** The engine reads only the matching Parquet files, applying any remaining filters at the column level (Parquet also stores per-row-group statistics). Rows are returned to the user.

The entire process — catalog lookup, metadata reads, pruning, data reads — is what LTAP relies on. The transactional guarantees (ACID) are enforced at the snapshot layer: a write either produces a new committed snapshot or it doesn't. Readers always see a consistent snapshot and are never affected by an in-progress write.

---

## 6. A Concrete LTAP Example: Order Processing

Here is a realistic scenario showing transactions and analytics on the same Iceberg table simultaneously.

```python
from pyspark.sql import SparkSession

spark = (SparkSession.builder
    .config("spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.my_catalog.type", "rest")
    .config("spark.sql.catalog.my_catalog.uri", "https://my-catalog.company.com")
    .getOrCreate())

# ── Transactional: write new orders ──────────────────────────────────────────
new_orders = spark.createDataFrame([
    (1001, "Alice",   "EU",  149.99, "2026-06-29"),
    (1002, "Bob",     "US",   89.50, "2026-06-29"),
    (1003, "Carla",   "APAC", 210.00, "2026-06-29"),
], ["order_id", "customer", "region", "amount", "order_date"])

new_orders.writeTo("my_catalog.db.orders").append()
# ↑ Creates a new snapshot atomically. Readers see the old snapshot until commit.

# ── Analytical: immediately query — no ETL needed ─────────────────────────────
result = spark.sql("""
    SELECT
        region,
        COUNT(*)          AS num_orders,
        SUM(amount)       AS total_revenue,
        AVG(amount)       AS avg_order_value
    FROM my_catalog.db.orders
    WHERE order_date = '2026-06-29'
    GROUP BY region
    ORDER BY total_revenue DESC
""")

result.show()
```

Both operations complete on the same table. No copy. No pipeline. No lag.

---

## 7. Time Travel — The Hidden Superpower

Because every write creates a new snapshot rather than modifying data in place, you can read the table at any past point in time:

```sql
-- What did our orders table look like before the last write?
SELECT COUNT(*) FROM orders
FOR SYSTEM_TIME AS OF '2026-06-28 23:59:59';

-- Roll back a bad write by restoring a previous snapshot
CALL catalog.system.rollback_to_snapshot('db.orders', 8749200);
```

This also means you can audit: who changed what, and when? Every snapshot has a parent, forming an immutable history.

> **Memory trick:** Iceberg's snapshots are like Git commits for your data. You can always check out an old commit.

---

## 8. Multi-Engine Access via IRC

One of the most powerful properties of the IRC + Iceberg combination is that **any engine can read and write the same table**. The catalog is the shared source of truth:

```python
# Spark writes new data
new_orders.writeTo("my_catalog.db.orders").append()

# Trino reads it immediately
trino_query = "SELECT * FROM orders WHERE order_date = '2026-06-29'"

# DuckDB reads it for a quick local analysis
import duckdb
duckdb.sql("ATTACH 'https://my-catalog.company.com' AS cat (TYPE ICEBERG)")
duckdb.sql("SELECT * FROM cat.db.orders LIMIT 10")
```

No data is copied between engines. They all point at the same Parquet files on S3. The IRC ensures everyone agrees on which snapshot is current.

---

## 9. Quick Reference

| Term | What it is | One-line memory trick |
|---|---|---|
| **LTAP** | Lake Transactional/Analytical Processing | Do transactions AND analytics on the same lake |
| **IRC** | Iceberg REST Catalog | A phone book mapping table names to S3 metadata paths |
| **metadata.json** | Root metadata file | The table of contents for a table |
| **Snapshot** | Immutable point-in-time version of the table | A Git commit for your data |
| **Manifest List** | Index of manifest files per snapshot | The chapter index in a book |
| **Manifest File** | List of data files with column statistics | A smart file directory |
| **File Pruning** | Skipping irrelevant files using column stats | Reading the chapter titles before reading the chapter |
| **Time Travel** | Querying past snapshots | `git checkout` for data |
| **ACID** | Atomicity, Consistency, Isolation, Durability | All-or-nothing, always-consistent, always-safe |

---

## Final Mental Model

Before Iceberg and LTAP, the data world looked like this:

```
Transactions:  [Operational DB]  ──ETL──►  [Data Warehouse]  :Analytics
               (fresh data)       (hours)   (stale data)
```

With LTAP on Apache Iceberg:

```
            ┌─────────────────────────────────┐
            │     Apache Iceberg Table        │
            │  (S3 + metadata chain + IRC)    │
            └────────────┬────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   Transactions      Analytics       Time Travel
   (INSERT/UPDATE)  (SELECT/AGG)   (past snapshots)
   
   Any engine:  Spark · Trino · DuckDB · Flink · Snowflake
```

The IRC is the front door. The metadata chain is the map. The snapshots are the safety net. And LTAP is the outcome: one lake that handles it all.
