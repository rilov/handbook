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
summary: A plain-English guide to what LTAP (Lake Transactional/Analytical Processing) actually means — including the important nuance that it does not replace the transactional database, but instead unifies OLTP and OLAP at the storage layer. Also covers how the Iceberg REST Catalog (IRC) works, and how a SQL query travels through the Iceberg stack from catalog lookup to Parquet rows.
date: 2026-06-29
---

# LTAP, the IRC Catalog, and the Hidden Layers of Apache Iceberg

> *You write `SELECT * FROM orders`. Three letters later, rows appear on your screen. But between those two moments, something remarkable happens — metadata files, catalog API calls, file pruning, and snapshot isolation all coordinate silently underneath. This guide shows you exactly what's going on.*

---

## Why LTAP matters

LTAP may be the next major architecture pattern in data — and open-source Apache Iceberg could play a critical role.

For decades we maintained two separate worlds.

**Operational databases** process orders, payments, customer updates, and application transactions. **Analytical platforms** process reporting, machine learning, and large-scale data exploration.

Connecting them usually requires CDC, ETL pipelines, replicas, and multiple copies of the same data.

LTAP — Lake Transactional and Analytical Processing — proposes a different model. Instead of constantly moving data between operational and analytical systems, **separate engines work over one shared and governed data foundation**.

This is where Apache Iceberg becomes important. Iceberg gives data stored in object storage many database-like capabilities:

- Atomic commits
- Concurrent writes
- `MERGE`, `UPDATE`, and `DELETE` operations
- Schema evolution
- Time travel
- Access from Spark, Trino, Flink, DuckDB, and other engines

**But Iceberg alone is not an OLTP database.** It does not replace PostgreSQL or the transactional engine serving an application. The LTAP pattern still needs a transactional layer capable of fast point reads, writes, indexes, and application-level transactions.

This is where projects such as `pg_lake` become interesting. `pg_lake` allows PostgreSQL to create, query, and modify Iceberg-backed tables directly. PostgreSQL applications can continue using a familiar transactional interface, while analytical engines access the same open Iceberg tables.

**Apache Gravitino** can provide the shared Iceberg REST Catalog, metadata, and governance layer. The data itself can live on S3-compatible object storage such as Pure Storage FlashBlade, MinIO, Ceph, Cloudian, or Dell ECS.

An open-source, on-premises LTAP-style architecture could look like this:

<div class="mermaid">
flowchart TB
    subgraph apps["Applications & AI Agents"]
        APP["🖥️ App / AI Agent"]
    end

    subgraph oltp["Transactional Layer"]
        PG["🐘 PostgreSQL + pg_lake"]
    end

    subgraph format["Open Table Format"]
        ICE["🧊 Apache Iceberg tables<br/>(Parquet files)"]
    end

    subgraph catalog["Catalog & Governance"]
        GRV["📖 Apache Gravitino<br/>IRC, metadata, access control"]
    end

    subgraph storage["Object Storage (S3-compatible)"]
        OBJ["💾 FlashBlade / MinIO / Ceph / Dell ECS"]
    end

    subgraph analytics["Analytical Engines"]
        SP["⚡ Spark"]
        TR["🔍 Trino"]
        FL["🌊 Flink"]
        DK["🦆 DuckDB"]
    end

    APP --> PG
    PG --> ICE
    ICE --> GRV
    GRV --> OBJ
    OBJ --> SP
    OBJ --> TR
    OBJ --> FL
    OBJ --> DK
</div>

This does not mean every pipeline disappears. Pipelines will still be needed for enrichment, validation, aggregation, external ingestion, and data quality. But it can remove the need for a separate CDC pipeline whose only purpose is to create another analytical copy of operational data.

The bigger shift is simple: **we stop constantly moving copies of data between systems. We bring specialized compute engines to the same open data.**

The future data platform may not be one engine trying to do everything. It may be multiple engines working independently over one open and governed data foundation — and that foundation should not belong to a single vendor.

---

## The Iceberg You Can't See

Imagine an actual iceberg floating in the ocean. What you see above the waterline is a small, clean tip. But 90% of the mass is hidden below.

Apache Iceberg works the same way.

Above the water: table names, SQL queries, schemas you can browse. The comfortable, familiar surface that analysts interact with every day.

Below the water: an entire hidden machinery — metadata files, snapshots, manifest lists, manifest files, and thousands of Parquet data files. None of this is visible when you run a query. But it's all doing work.

<div class="mermaid">
flowchart TB
    subgraph above["🌊 Above the waterline"]
        SQL["SQL query: SELECT * FROM orders"]
        TBL["Table name: db.orders"]
        SCH["Schema: order_id, customer, amount"]
    end

    subgraph below["🧊 Below the waterline"]
        META["metadata.json<br/>(root of everything)"]
        SNAP["Snapshots<br/>(immutable point-in-time versions)"]
        MFLIST["Manifest List<br/>(index of manifest files)"]
        MF["Manifest Files<br/>(column stats per data file)"]
        PARQ["Parquet Data Files<br/>(millions of rows on S3)"]
    end

    SQL --> META
    META --> SNAP
    SNAP --> MFLIST
    MFLIST --> MF
    MF --> PARQ
</div>

The reason this matters is simple: **the hidden machinery is exactly what makes LTAP possible.**

---

## 1. What Is LTAP?

LTAP stands for **Lake Transactional/Analytical Processing**.

It was announced by Databricks in 2026. Before we explain what it *is*, let's understand the problem it solves — and the important nuance of what it does and does not replace.

### The old world had two separate systems

In the traditional data architecture, you had a hard split:

- **Transactional systems** (OLTP): databases like PostgreSQL or MySQL that handle writes — inserts, updates, deletes. Fast for individual row operations. Stores data in **row format** on disk.
- **Analytical systems** (OLAP): warehouses like Redshift or Snowflake that handle reporting and aggregations. Fast for large scans. Stores data in **columnar format** for efficient reads.

To get data from one world to the other, teams built ETL pipelines — nightly batch jobs that copied data across. The result: your analytics were always hours or days behind reality. And you were paying to store the same data twice.

<div class="mermaid">
flowchart TB
    subgraph before["❌ Before LTAP"]
        PG1["🐘 Postgres<br/>(row format, fresh data)"]
        ETL["⏳ ETL Pipeline<br/>(hours of lag)"]
        WH["🏭 Data Warehouse<br/>(columnar, stale data)"]
        PG1 --> ETL --> WH
    end

    subgraph after["✅ With LTAP"]
        PG2["🐘 Postgres / Lakebase<br/>(OLTP transactions)"]
        PS["PageServer<br/>transcodes rows to Parquet"]
        S3["💾 Object Storage<br/>(Parquet / Iceberg)"]
        ENG["⚡ Spark / Trino / DuckDB<br/>(OLAP analytics)"]
        PG2 --> PS --> S3 --> ENG
    end
</div>

### Does LTAP replace the transactional database?

**No.** This is the most important thing to understand about LTAP.

LTAP does **not** replace PostgreSQL or any transactional database. Postgres still handles all your OLTP workloads — inserts, updates, deletes, row-level locking, ACID transactions.

What LTAP does is unify the two worlds **at the storage layer**, not at the engine layer.

<div class="mermaid">
flowchart LR
    subgraph before["❌ Before"]
        A["Postgres<br/>row format"] -->|"ETL pipeline<br/>hours of lag"| B["Data Warehouse<br/>columnar format"]
    end
    subgraph after["✅ After LTAP"]
        C["Postgres<br/>OLTP"] -->|"WAL"| D["PageServer<br/>row to Parquet"]
        D -->|"writes"| E["Object Storage<br/>Parquet/Iceberg"]
        E -->|"reads"| F["Spark / Trino<br/>OLAP"]
    end
</div>

The key architectural decision: **keep the best tool for each job**.

| Job | Engine | Why |
|---|---|---|
| Transactions (OLTP) | PostgreSQL / Lakebase | Full ACID, row-level locking, mature ecosystem |
| Analytics (OLAP) | Spark, Trino, DuckDB | Column-oriented, optimized for large scans |

What changes is the **data underneath** them — instead of two copies in two formats maintained by a pipeline, there is one durable copy in open columnar format (Parquet/Iceberg) on object storage that both sides read.

### What is Lakebase?

LTAP is built on top of **Lakebase** — Databricks' serverless PostgreSQL built on the [Neon](https://neon.tech) architecture (a company Databricks acquired).

Lakebase separates the traditional monolithic database into two parts:

<div class="mermaid">
flowchart TB
    subgraph mono["❌ Traditional Postgres Monolith"]
        M1["🖥️ Compute + WAL + Data files<br/>all on one machine"]
    end

    subgraph lakebase["✅ Lakebase (disaggregated)"]
        COMP["🖥️ Postgres Compute<br/>(stateless)"]
        SK["📝 SafeKeeper<br/>(WAL - durable log)"]
        PGS["📄 PageServer<br/>(data files in object storage)"]
        COMP --> SK
        COMP --> PGS
    end
</div>

- **SafeKeeper** stores the write-ahead log (WAL) — the durable record of every committed transaction.
- **PageServer** materializes the WAL changes into actual data pages, stored in object storage (S3).

This gives you unlimited storage, elastic compute, and instant branching — and it is the foundation that makes LTAP possible.

### How LTAP works at the storage layer

When a transaction commits in Lakebase, the PageServer does something new: as it writes the data pages to object storage, it **transcodes the row-format Postgres data into Parquet columnar format**.

<div class="mermaid">
sequenceDiagram
    participant App as 🖥️ Application
    participant PG as 🐘 Postgres
    participant SK as 📝 SafeKeeper WAL
    participant PS as 📄 PageServer
    participant S3 as 💾 Object Storage
    participant SP as ⚡ Spark or Trino

    App->>PG: INSERT or UPDATE
    PG->>SK: Write WAL entry - commit
    SK-->>PG: Durably acknowledged
    PG-->>App: Transaction committed
    SK->>PS: Stream WAL changes
    PS->>S3: Materialize pages - row to Parquet
    SP->>S3: Read Parquet via Iceberg
    S3-->>SP: Columnar data - no ETL needed
</div>

Postgres reads row-format pages from the PageServer's local cache (fast for OLTP point reads). Spark and other analytical engines read the columnar Parquet files from object storage (fast for analytical scans). Both are reading from the same underlying durable store.

> **Memory trick:** LTAP is like a bilingual document — the same content exists in English for one audience and French for another, but there is only one source of truth underneath.

### LTAP vs HTAP: an important distinction

**HTAP** (Hybrid Transactional/Analytical Processing) was a previous attempt at the same goal — build a **single engine** that handles both workloads.

HTAP largely failed in practice because:
- Building one engine great at both transactions AND analytics is enormously complex
- The two workloads contend for the same CPU and memory — an analytical query slows down your OLTP
- New engines lack the ecosystem and maturity of Postgres or Spark

LTAP takes a different approach: **unify at the storage layer, not the engine layer**. Keep Postgres for transactions, keep Spark/Lakehouse for analytics, make them read the same data.

<div class="mermaid">
flowchart TB
    subgraph htap["❌ HTAP approach"]
        ONE["One engine<br/>trying to do both"]
        ONE --> SLOW["Usually compromises on both<br/>slow OLTP or slow analytics"]
    end

    subgraph ltap["✅ LTAP approach"]
        PGE["🐘 Postgres<br/>(OLTP)"]
        ANA["⚡ Spark / Trino<br/>(OLAP)"]
        STO["💾 Unified storage<br/>(Parquet / Iceberg)"]
        PGE --> STO
        ANA --> STO
    end
</div>

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

<div class="mermaid">
flowchart LR
    subgraph engines["Query Engines"]
        SP["⚡ Spark"]
        TR["🔍 Trino"]
        DK["🦆 DuckDB"]
        FL["🌊 Flink"]
        SF["❄️ Snowflake"]
    end

    IRC["📖 IRC Catalog<br/>Apache Gravitino<br/>REST API endpoint"]

    subgraph s3["Object Storage"]
        META["metadata.json"]
        PARQ["Parquet files"]
    end

    SP -->|"lookup"| IRC
    TR -->|"lookup"| IRC
    DK -->|"lookup"| IRC
    FL -->|"lookup"| IRC
    SF -->|"lookup"| IRC
    IRC -->|"metadata-location"| SP
    IRC -->|"metadata-location"| TR
    IRC -->|"metadata-location"| DK
    SP -->|"read"| s3
    TR -->|"read"| s3
    DK -->|"read"| s3
</div>

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

<div class="mermaid">
sequenceDiagram
    participant ENG as ⚡ Query Engine
    participant IRC as 📖 IRC Gravitino
    participant S3M as 📄 Metadata File
    participant MFL as 📋 Manifest List
    participant MF as 📁 Manifest Files
    participant PQ as 💾 Parquet Files

    ENG->>IRC: Lookup table: db.orders
    IRC-->>ENG: metadata-location path on S3
    ENG->>S3M: Fetch metadata.json
    S3M-->>ENG: current-snapshot-id and manifest-list path
    ENG->>MFL: Fetch manifest list
    MFL-->>ENG: List of manifest files
    ENG->>MF: Read manifest files with column stats
    Note over ENG,MF: File pruning: 10,000 files reduced to 60 matching order_date filter
    ENG->>PQ: Read only 60 matching Parquet files
    PQ-->>ENG: Rows returned to user
</div>

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

Here is a realistic scenario showing how the two engines play their separate roles in LTAP.

The **transactional write** happens through Postgres (Lakebase). The **analytical query** happens through Spark. There is no ETL pipeline connecting them — they share the same underlying Parquet/Iceberg storage.

```python
import psycopg2
from pyspark.sql import SparkSession

# ── Transactional: write new orders via Postgres (Lakebase) ───────────────────
# Postgres handles the OLTP side — row-level ACID, fast point writes
conn = psycopg2.connect("postgresql://lakebase.company.com/orders_db")
cur = conn.cursor()

cur.execute("""
    INSERT INTO orders (order_id, customer, region, amount, order_date)
    VALUES
        (1001, 'Alice', 'EU',   149.99, '2026-06-29'),
        (1002, 'Bob',   'US',    89.50, '2026-06-29'),
        (1003, 'Carla', 'APAC', 210.00, '2026-06-29')
""")
conn.commit()
# ↑ Commits to Postgres via WAL → PageServer transcodes to Parquet in object storage
# ↑ No ETL needed — the columnar copy is created as part of the commit path

# ── Analytical: immediately query via Spark — no ETL needed ───────────────────
# Spark reads the same Parquet/Iceberg data that Postgres just wrote
spark = (SparkSession.builder
    .config("spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.my_catalog.type", "rest")
    .config("spark.sql.catalog.my_catalog.uri", "https://my-catalog.company.com")
    .getOrCreate())

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

The transactional write uses Postgres. The analytical query uses Spark. No pipeline. No separate copy to maintain. The freshness of the analytics is determined by how quickly the PageServer transcodes committed rows into the columnar store — which is near real-time, not hours.

<div class="mermaid">
flowchart LR
    A["🐘 Postgres commits rows<br/>(OLTP)"] -->|"WAL to PageServer"| B["💾 Parquet on Object Storage<br/>(Iceberg)"]
    B -->|"Spark reads via IRC"| C["⚡ Spark query<br/>(OLAP)"]
</div>

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

## 10. Running LTAP-style architecture on-premises

Databricks' LTAP is a managed cloud product — Lakebase runs on their infrastructure, PageServer writes to S3, and the Lakehouse engines are hosted Spark/Trino clusters.

But the same architecture can be assembled on-premises using open-source components. You need to replace each layer independently.

### The four layers and their on-prem replacements

```text
Databricks LTAP layer         On-prem open-source equivalent
─────────────────────         ──────────────────────────────
Lakebase (serverless Postgres) →  Self-hosted Neon OR standard Postgres + pg_lake
PageServer (WAL → Parquet)     →  pg_lake extension (Postgres writes Iceberg natively)
Object storage (S3)            →  Pure Storage FlashBlade (enterprise on-prem)
                                   OR MinIO (commodity hardware / dev)
IRC Catalog                    →  Apache Gravitino (recommended)
Analytics engine               →  Trino OR Apache Spark (self-hosted)
```

### Object storage: Pure Storage FlashBlade

For enterprise on-prem deployments, [Pure Storage FlashBlade](https://www.purestorage.com/products/unstructured-data-storage/flashblade-s.html) is the recommended object storage layer. FlashBlade exposes a native **S3-compatible API** — the same API used by AWS S3 — so every tool in the stack (pg_lake, Gravitino, Spark, Trino, DuckDB) connects to it without modification.

Key properties relevant to this architecture:

| Property | FlashBlade |
|---|---|
| S3 API compatibility | ✅ Native S3 REST API |
| Path-style access | ✅ Required — set `path_style: true` |
| Protocols | NFS, S3, SMB on the same system |
| Scale | Tens of terabytes to multiple petabytes |
| Tested SDKs | Java, Python, Go, C#, .NET S3 clients |

#### Critical FlashBlade configuration: `stsUnavailable`

FlashBlade does not support AWS STS (Security Token Service) — the credential-vending mechanism that cloud-native tools like Polaris or Gravitino may try to call. You must disable this explicitly in your catalog config.

For **Gravitino IRC** pointing at FlashBlade:

```properties
gravitino.iceberg-rest.s3-endpoint   = https://<FLASHBLADE_DATA_VIP>:80
gravitino.iceberg-rest.s3-path-style = true
gravitino.iceberg-rest.s3-region     = us-east-1
gravitino.iceberg-rest.s3-access-key = <flashblade_access_key>
gravitino.iceberg-rest.s3-secret-key = <flashblade_secret_key>
```

For **Spark** connecting directly to FlashBlade via S3A:

```properties
spark.hadoop.fs.s3a.endpoint               = <FLASHBLADE_DATA_VIP>
spark.hadoop.fs.s3a.path.style.access      = true
spark.hadoop.fs.s3a.connection.ssl.enabled = false
spark.hadoop.fs.s3a.access.key             = <flashblade_access_key>
spark.hadoop.fs.s3a.secret.key             = <flashblade_secret_key>
```

For **pg_lake** connecting to FlashBlade instead of MinIO — only the S3 endpoint changes in the Docker Compose environment variables:

```bash
AWS_S3_ENDPOINT=https://<FLASHBLADE_DATA_VIP>:80
AWS_S3_PATH_STYLE=true
AWS_ACCESS_KEY_ID=<flashblade_access_key>
AWS_SECRET_ACCESS_KEY=<flashblade_secret_key>
```

> **MinIO vs FlashBlade:** MinIO is ideal for dev/test or commodity hardware. FlashBlade is the enterprise choice — all-flash hardware, unified NFS+S3 access, petabyte scale, and enterprise support. The configuration is identical from the software side; only the endpoint changes.

### Why Gravitino for the IRC catalog?

[Apache Gravitino](https://gravitino.apache.org) is a fully open-source, Apache-licensed unified metadata catalog. It implements the Iceberg REST Catalog (IRC) specification natively and adds governance, multi-engine access control, and multi-catalog federation on top.

Key reasons to choose it over alternatives like Polaris or Lakekeeper:

| Feature | Gravitino |
|---|---|
| IRC spec compliant | ✅ Full HTTP API at `/iceberg/` |
| Catalog backends | Hive Metastore, JDBC (Postgres, MySQL), REST |
| Object storage | S3 / MinIO, GCS, Azure ADLS, HDFS, OSS |
| Access control | ✅ When run as auxiliary service |
| Multi-catalog federation | ✅ One Gravitino instance, many catalogs |
| Docker image | `apache/gravitino-iceberg-rest` |
| License | Apache 2.0 |

#### Two deployment modes

**Standalone** — quickest to run, no access control:

```bash
docker run --rm -d -p 9001:9001 apache/gravitino-iceberg-rest:0.8.0-incubating
# IRC endpoint available at: http://localhost:9001/iceberg/
```

**Auxiliary service** (embedded in Gravitino server) — adds access control and Web UI:

```bash
# Gravitino server exposes:
#   port 8090 → Web UI + metadata API
#   port 9001 → Iceberg REST catalog endpoint
```

#### Configuration for on-prem with MinIO and Postgres

Production config in `gravitino.conf` (auxiliary mode):

```properties
# Enable Iceberg REST as an auxiliary service
gravitino.auxService.names = iceberg-rest
gravitino.iceberg-rest.classpath = iceberg-rest-server/libs,iceberg-rest-server/conf

# Use Postgres as the catalog backend (reliable, persistent)
gravitino.iceberg-rest.catalog-backend = jdbc
gravitino.iceberg-rest.jdbc-driver     = org.postgresql.Driver
gravitino.iceberg-rest.uri             = jdbc:postgresql://localhost:5432/gravitino_catalog
gravitino.iceberg-rest.jdbc-user       = gravitino
gravitino.iceberg-rest.jdbc-password   = yourpassword

# Point warehouse at MinIO (S3-compatible on-prem)
gravitino.iceberg-rest.warehouse       = s3a://iceberg-warehouse/
gravitino.iceberg-rest.io-impl         = org.apache.iceberg.aws.s3.S3FileIO
gravitino.iceberg-rest.s3-endpoint     = http://minio:9000
gravitino.iceberg-rest.s3-access-key   = minioadmin
gravitino.iceberg-rest.s3-secret-key   = minioadmin
gravitino.iceberg-rest.s3-path-style   = true
```

#### Connecting engines to Gravitino IRC

Any engine that speaks the IRC spec points to the same endpoint:

```python
# Spark
spark = SparkSession.builder \
    .config("spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.my_catalog.type", "rest") \
    .config("spark.sql.catalog.my_catalog.uri", "http://gravitino:9001/iceberg/") \
    .getOrCreate()
```

```sql
-- Trino
CREATE CATALOG iceberg USING iceberg
WITH (
    "iceberg.catalog.type" = 'rest',
    "iceberg.rest-catalog.uri" = 'http://gravitino:9001/iceberg/'
);
```

```python
# DuckDB
import duckdb
duckdb.sql("ATTACH 'http://gravitino:9001/iceberg/' AS cat (TYPE ICEBERG)")
duckdb.sql("SELECT * FROM cat.db.orders LIMIT 10")
```

All three engines read from the same Iceberg tables on MinIO, coordinated by Gravitino.

### Option A: Self-hosted Neon stack (closest to Lakebase)

[Neon went fully open source in 2024 (MIT license)](https://github.com/neondatabase/neon). You can run the entire Neon stack yourself — the same codebase that powers Neon Cloud.

The stack runs via Docker Compose:

```yaml
services:
  storage_broker:   # lightweight pub-sub coordination
  safekeeper1:      # WAL durability with quorum replication
  pageserver:       # materializes WAL pages → object storage
  compute:          # stateless Postgres connected to pageserver
  minio:            # S3-compatible object storage
```

The `pageserver` connects to MinIO instead of AWS S3. Everything else is the same architecture.

Hardware minimum to run this stack:

| Environment | RAM | CPU |
|---|---|---|
| Dev / testing | 2 GB | 1 vCPU |
| Small production | 4 GB | 2 vCPUs |
| Multi-tenant / sustained writes | 8 GB+ | 4 vCPUs |

For Kubernetes environments, the [Neon Operator](https://github.com/lovablelabs/neon-operator) deploys all components as Kubernetes workloads with S3-compatible storage (MinIO, Ceph, or Rook).

**Limitation:** The on-prem Neon stack does not yet do the LTAP-specific Parquet transcoding automatically during PageServer materialization — that part is Databricks' proprietary extension to the Neon architecture. You need to bridge that gap with one of the options below.

### Option B: Postgres + pg_lake (Snowflake open source)

[`pg_lake`](https://github.com/Snowflake-Labs/pg_lake) (Apache 2.0, originally built by Crunchy Data, open-sourced by Snowflake in 2025) turns standard Postgres into a standalone lakehouse. You can create and write Iceberg tables directly from Postgres — they land as Parquet files on any S3-compatible store — and any other Iceberg engine (Spark, Trino, DuckDB) can read them immediately.

#### Architecture

`pg_lake` has two components:

```text
User → PostgreSQL (with pg_lake extensions)
              ↓
         pgduck_server  ← separate process, PostgreSQL wire protocol
              ↓
           DuckDB       ← handles column-oriented scanning and computation
              ↓
     S3-compatible object store (MinIO / Pure Storage FlashBlade / AWS S3)
```

`pgduck_server` runs DuckDB as a separate multi-threaded process and exposes it via the Postgres wire protocol. The `pg_lake` extension delegates scanning and analytical computation to DuckDB transparently — users just write standard SQL against Postgres.

#### What you can do

- Create Iceberg tables with `USING iceberg` — data goes straight to Parquet on S3
- Query Iceberg tables, heap tables, and raw Parquet/CSV/JSON files **in the same SQL query**
- `COPY` data to/from S3 in Parquet, CSV, or JSON
- Create foreign tables directly from files in object storage — columns are inferred automatically
- Full transactional guarantees across all table types

#### SQL examples

```sql
-- Create an Iceberg table — data lands in S3 as Parquet
CREATE TABLE orders USING iceberg AS
    SELECT i AS order_id, 'customer_' || i AS customer
    FROM generate_series(1, 1000) i;

-- Standard query
SELECT COUNT(*) FROM orders;

-- See where the Iceberg metadata lives on S3
SELECT table_name, metadata_location FROM iceberg_tables;
-- orders | s3://warehouse/pglake/public/orders/metadata/00001-....metadata.json

-- COPY results to S3 as Parquet
COPY (SELECT * FROM orders WHERE order_id > 500)
TO 's3://warehouse/exports/orders_recent.parquet';

-- Query raw Parquet files on S3 without importing them
CREATE FOREIGN TABLE parquet_logs ()
    SERVER pg_lake
    OPTIONS (path 's3://warehouse/logs/*.parquet');

SELECT COUNT(*) FROM parquet_logs;
-- columns are inferred automatically from the file schema

-- Mix Iceberg, heap, and foreign tables in one query
SELECT o.customer, l.event
FROM orders o
JOIN parquet_logs l ON o.order_id = l.order_id
WHERE o.order_id > 100;
```

#### Setup (Docker)

```bash
git clone https://github.com/Snowflake-Labs/pg_lake
cd pg_lake
docker compose up
# connects to MinIO by default; swap endpoint for FlashBlade or any S3-compatible store
```

### Option C: Postgres + ColdFront (pgEdge, open source)

[`ColdFront`](https://github.com/pgEdge/coldfront) is an open source Postgres extension (PostgreSQL License) that keeps hot data in native Postgres partitions and automatically tiers cold data to Apache Iceberg on any S3-compatible store. Both tiers are readable and writable through the same SQL — no application changes needed.

```text
Postgres table (unified SQL view)
├── Hot tier:  recent rows in native Postgres partitions
└── Cold tier: older rows in Iceberg Parquet on MinIO
```

Both tiers look like the same table to the application. The archiver moves rows from hot to cold on a schedule based on a watermark you define.

Stack:

| Component | Version |
|---|---|
| PostgreSQL | 16, 17, or 18 (stock, no fork) |
| pg_duckdb | Iceberg reads/writes via DuckDB in-process |
| Lakekeeper | Iceberg REST catalog (Rust) |
| MinIO / SeaweedFS | S3-compatible object storage |

### Option D: EDB Postgres + Iceberg reference architecture

EnterpriseDB (EDB) published a [converged analytics reference architecture](https://github.com/milesrichardson-edb/converged-analytics-reference) that replicates from Postgres to Iceberg automatically using their PGAA (Postgres Analytics Accelerator) extension:

```text
EDB Postgres Distributed (PGD)
→ PGAA extension replicates rows → Iceberg on MinIO
→ Lakekeeper (IRC catalog)
→ WarehousePG / Spark for analytics
```

This is the most production-ready fully on-prem option but requires EDB licensing.

### Option E: Full open-source lakehouse stack for learning / prototyping

[`iceduck`](https://github.com/pfabrici/iceduck) provides a complete Docker Compose on-prem lakehouse stack for learning and prototyping with zero cloud dependencies:

```yaml
services:
  minio:           # S3-compatible object storage
  polaris:         # Apache Polaris — Iceberg REST catalog
  postgres:        # Metastore for Polaris + relational store
  trino:           # SQL query engine over Iceberg
  spark:           # Distributed processing
  duckdb:          # Fast local analytical queries
  jupyter:         # Interactive notebooks
```

Run locally with `docker compose up`. All services connect to each other automatically.

### Summary: which option for which situation

| Situation | Recommended approach |
|---|---|
| Enterprise on-prem (production) | `pg_lake` + **Pure Storage FlashBlade** + **Gravitino IRC** + Trino/Spark |
| Closest to Databricks LTAP architecture | Self-hosted Neon + FlashBlade/MinIO + **Gravitino IRC** + Trino |
| Hot/cold tiering from Postgres to Iceberg | `ColdFront` (pgEdge) + FlashBlade/MinIO + **Gravitino IRC** |
| Enterprise on-prem with EDB licensing | EDB PGD + PGAA + **Gravitino IRC** + FlashBlade |
| Dev / commodity hardware | `pg_lake` + MinIO + **Gravitino IRC** |
| Learning and prototyping locally | `iceduck` Docker Compose stack (uses Apache Polaris) |

### The one thing you cannot self-host yet

The specific Databricks innovation in LTAP — where the **PageServer automatically transcodes committed Postgres rows into Parquet columnar format as part of the WAL materialization path** — is proprietary to Databricks' fork of Neon. The open-source Neon PageServer writes row-format pages to object storage, not Parquet.

You can achieve the same end result (Postgres transactions readable by Spark/Trino via Iceberg) using `pg_lake` or `ColdFront`, but the transcoding happens at a different layer — via extension rather than inside the storage engine itself.

---

## Final Mental Model

Before LTAP, the data world looked like this:

```
[Postgres / MySQL]  ──ETL pipeline──►  [Data Warehouse]
  OLTP: fresh data      hours of lag     OLAP: stale data
  row format                             columnar format
```

With LTAP:

```
         ┌─────────────────────────────────────────────┐
         │           Lakebase (Postgres)               │
         │     SafeKeeper (WAL) + PageServer           │
         └────────────────────┬────────────────────────┘
                              │ transcodes rows → Parquet
                              ▼
         ┌─────────────────────────────────────────────┐
         │    Object Storage (S3)                      │
         │    Parquet files in Apache Iceberg format   │
         │    IRC Catalog maps table names → metadata  │
         └────────┬──────────────────────┬─────────────┘
                  │                      │
                  ▼                      ▼
         Postgres reads           Spark · Trino · DuckDB
         (row cache, OLTP)        (columnar, OLAP)
         point queries            aggregations, reports
         millisecond latency      petabyte-scale scans
```

LTAP does not replace the transactional database. It removes the ETL pipeline between the transactional database and the analytical system by unifying them at the storage layer.

The IRC is the front door. The metadata chain is the map. The PageServer transcoding is the bridge. And LTAP is the outcome: the same data, fresh, readable by both worlds.
