---
title: "How Iceberg Query Engines Work Internally — Trino, Spark & the REST Catalog"
category: Data
order: 3
tags:
  - iceberg
  - trino
  - spark
  - rest-catalog
  - query-engine
  - data-architecture
  - s3
summary: A deep dive into how query engines like Trino and Spark execute queries against Iceberg tables — from REST Catalog API calls to reading Parquet files from S3.
---

# How Iceberg Query Engines Work Internally

> **What this guide covers:** When you run `SELECT * FROM customers WHERE country = 'US'` against an Iceberg table, what actually happens? This guide traces every step — from the query engine contacting the catalog, to reading metadata from S3, to scanning only the relevant Parquet files. We cover Trino, Spark, and the REST Catalog protocol in detail.

---

## The Big Picture: What Happens When You Query an Iceberg Table?

Every Iceberg query follows the same fundamental pattern, regardless of which engine you use. Understanding this pattern is the key to understanding Iceberg internals.

<div class="mermaid">
graph TD
    Q["<b>SQL Query</b><br/>SELECT * FROM customers<br/>WHERE country = 'US'"] --> E["<b>Query Engine</b><br/>Trino / Spark / Flink"]
    E -->|"<b>Step 1:</b> Load table"| CAT["<b>Catalog</b><br/>REST / Hive / Glue / Polaris"]
    CAT -->|"<b>Returns:</b> metadata location"| E
    E -->|"<b>Step 2:</b> Read metadata"| META["<b>Metadata File</b><br/>v42.metadata.json<br/>(on S3)"]
    META -->|"<b>Returns:</b> current snapshot"| E
    E -->|"<b>Step 3:</b> Read manifest list"| ML["<b>Manifest List</b><br/>snap-xxx.avro<br/>(on S3)"]
    ML -->|"<b>Returns:</b> manifest entries"| E
    E -->|"<b>Step 4:</b> Read manifests + prune"| MF["<b>Manifest Files</b><br/>xxx-m0.avro, xxx-m1.avro<br/>(on S3)"]
    MF -->|"<b>Returns:</b> data file list<br/>(after partition pruning)"| E
    E -->|"<b>Step 5:</b> Read data files"| DF["<b>Data Files</b><br/>data-001.parquet<br/>data-002.parquet<br/>(on S3)"]
    DF -->|"<b>Returns:</b> query results"| E

    style Q fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style E fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style CAT fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style META fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style ML fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style MF fill:#607D8B,stroke:#455A64,stroke-width:2px,color:#fff
    style DF fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
</div>

### The 5-Step Query Flow (Every Engine Follows This)

| Step | What Happens | Where | I/O Cost |
|------|-------------|-------|----------|
| **1. Load Table** | Engine asks catalog for table's current metadata file location | Catalog (HTTP/Thrift) | 1 API call |
| **2. Read Metadata** | Engine reads the JSON metadata file to find the current snapshot | S3 (single file) | 1 S3 GET |
| **3. Read Manifest List** | Engine reads the Avro manifest list to find all manifest files | S3 (single file) | 1 S3 GET |
| **4. Read Manifests** | Engine reads manifest files, applies partition pruning to eliminate irrelevant files | S3 (multiple files) | N S3 GETs |
| **5. Read Data** | Engine reads only the Parquet data files that survived pruning | S3 (multiple files) | M S3 GETs |

**Key insight:** Steps 1-4 are metadata operations. The actual data reading only happens in Step 5. This is why Iceberg can skip 90%+ of data files — it knows exactly which files contain relevant data before reading any of them.

---

## The Iceberg REST Catalog Protocol

The REST Catalog is the standard way for query engines to interact with Iceberg catalogs. It's a language-agnostic HTTP API that replaced the older pluggable Java-only catalog approach.

### Why REST Catalog Exists

Before the REST protocol, every catalog (Hive Metastore, AWS Glue, Nessie) needed a separate client implementation in every language (Java, Python, Go, Rust). This created a combinatorial explosion:

```
Old approach (pluggable catalogs):
  Trino (Java) → needs: HiveCatalog.java, GlueCatalog.java, NessieCatalog.java
  Spark (Java) → needs: HiveCatalog.java, GlueCatalog.java, NessieCatalog.java
  PyIceberg (Python) → needs: hive_catalog.py, glue_catalog.py, nessie_catalog.py
  
  = 3 engines × 3 catalogs × custom code each = 9 implementations

REST approach:
  Trino → RESTCatalog (HTTP client)
  Spark → RESTCatalog (HTTP client)
  PyIceberg → RESTCatalog (HTTP client)
  
  = 3 engines × 1 standard HTTP client = 3 implementations
  Catalog server handles all backend logic
```

### REST Catalog API — The Key Endpoints

<div class="mermaid">
graph LR
    ENGINE["<b>Query Engine</b><br/>Trino / Spark"] -->|"<b>HTTP GET/POST</b>"| REST["<b>REST Catalog Server</b><br/>Polaris / Nessie / Lakekeeper"]
    REST -->|"<b>Reads/writes</b>"| S3["<b>Object Storage</b><br/>S3 / GCS / ADLS"]
    REST -->|"<b>Manages</b>"| DB["<b>Catalog State</b><br/>Postgres / DynamoDB"]

    style ENGINE fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style REST fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style S3 fill:#FF9800,stroke:#F57C00,stroke-width:2px,color:#fff
    style DB fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
</div>

Here are the critical REST API endpoints that every query touches:

#### Configuration & Authentication

```http
# Step 0: Get catalog configuration
GET /v1/config
→ Returns: warehouse location, default settings, overrides

# Step 0b: Get OAuth token (if using OAuth2)
POST /v1/oauth/tokens
Body: { "grant_type": "client_credentials", "client_id": "...", "client_secret": "..." }
→ Returns: { "access_token": "...", "token_type": "bearer", "expires_in": 3600 }
```

#### Namespace & Table Operations

```http
# List namespaces (databases)
GET /v1/{prefix}/namespaces
→ Returns: { "namespaces": [["analytics"], ["raw_data"]] }

# Load a table (THE KEY OPERATION)
GET /v1/{prefix}/namespaces/{namespace}/tables/{table}
→ Returns: {
    "metadata-location": "s3://bucket/db/table/metadata/v42.metadata.json",
    "metadata": { ... full table metadata ... },
    "config": {
      "s3.access-key-id": "...",        ← credential vending!
      "s3.secret-access-key": "...",
      "s3.session-token": "..."
    }
  }
```

#### Credential Vending — The Security Model

One of the REST Catalog's most powerful features is **credential vending**. Instead of the query engine having permanent S3 credentials, the catalog issues short-lived, scoped credentials:

<div class="mermaid">
sequenceDiagram
    participant E as Query Engine
    participant RC as REST Catalog
    participant IAM as IAM / STS
    participant S3 as S3 Storage

    E->>RC: GET /v1/.../tables/customers
    RC->>IAM: AssumeRole(table-scoped policy)
    IAM-->>RC: Temporary credentials (15 min TTL)
    RC-->>E: Table metadata + scoped S3 credentials
    E->>S3: GET data-001.parquet (using temp creds)
    S3-->>E: Parquet data
    Note over E,S3: Credentials only allow access to THIS table's files
</div>

```
Why this matters:
  ✅ Engine never has broad S3 access
  ✅ Credentials expire automatically (15-60 min)
  ✅ Access is scoped to specific table paths
  ✅ Catalog controls WHO can access WHAT
  ✅ No static credentials stored in engine config
```

#### Table Commits (Writes)

```http
# Commit a table update (atomic metadata swap)
POST /v1/{prefix}/namespaces/{namespace}/tables/{table}
Body: {
  "requirements": [
    { "type": "assert-current-schema-id", "current-schema-id": 1 },
    { "type": "assert-table-uuid", "uuid": "abc-123" }
  ],
  "updates": [
    { "action": "add-snapshot", "snapshot": { ... } },
    { "action": "set-current-schema", "schema-id": 2 }
  ]
}
→ Returns: updated table metadata (or 409 Conflict if requirements fail)
```

**The commit protocol is change-based, not state-based.** The engine sends a list of requirements (preconditions) and updates (changes). The catalog server validates requirements atomically and applies updates. If another writer modified the table, the commit fails with a 409 Conflict and the engine retries.

---

## How Trino Queries Iceberg Tables

Trino is a **distributed SQL query engine** with a coordinator-worker architecture. Here's exactly what happens when you run an Iceberg query in Trino.

### Trino Architecture Overview

<div class="mermaid">
graph TD
    CLIENT["<b>SQL Client</b><br/>JDBC / CLI / BI Tool"] -->|"SQL query"| COORD["<b>Trino Coordinator</b><br/>Query planning<br/>Split generation<br/>Result assembly"]
    COORD -->|"Assigns splits"| W1["<b>Worker 1</b>"]
    COORD -->|"Assigns splits"| W2["<b>Worker 2</b>"]
    COORD -->|"Assigns splits"| W3["<b>Worker 3</b>"]
    
    COORD -->|"Metadata calls"| CONN["<b>Iceberg Connector</b><br/>REST / Hive / Glue"]
    
    W1 -->|"Reads data"| S3["<b>S3 / Object Storage</b>"]
    W2 -->|"Reads data"| S3
    W3 -->|"Reads data"| S3

    style CLIENT fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style COORD fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style CONN fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#fff
    style W1 fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style W2 fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style W3 fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style S3 fill:#607D8B,stroke:#455A64,stroke-width:2px,color:#fff
</div>

### Step-by-Step: Trino Query Execution on Iceberg

Let's trace what happens for this query:

```sql
SELECT customer_id, name, total_spent
FROM iceberg.analytics.customers
WHERE country = 'US' AND signup_date > DATE '2024-01-01'
ORDER BY total_spent DESC
LIMIT 100;
```

#### Phase 1: Query Parsing & Planning (Coordinator)

<div class="mermaid">
sequenceDiagram
    participant CLI as SQL Client
    participant C as Trino Coordinator
    participant IC as Iceberg Connector
    participant CAT as REST Catalog
    participant S3 as S3

    CLI->>C: Submit SQL query
    Note over C: 1. Parse SQL → AST
    Note over C: 2. Analyze: resolve table "iceberg.analytics.customers"
    
    C->>IC: getTableHandle("analytics", "customers")
    IC->>CAT: GET /v1/.../tables/customers
    CAT-->>IC: metadata-location: s3://bucket/metadata/v42.metadata.json
    IC->>S3: GET v42.metadata.json
    S3-->>IC: Table metadata (schema, partitions, current snapshot)
    IC-->>C: TableHandle + schema + partition spec
    
    Note over C: 3. Optimize query plan
    Note over C: 4. Push down predicates:<br/>country = 'US'<br/>signup_date > 2024-01-01
</div>

**What the coordinator does:**

1. **Parses** the SQL into an Abstract Syntax Tree (AST)
2. **Resolves** the table reference `iceberg.analytics.customers` through the Iceberg connector
3. **Fetches** table metadata from the catalog (schema, partition spec, current snapshot)
4. **Creates** a logical plan and optimizes it
5. **Pushes down** predicates to the Iceberg connector — this is critical for performance

#### Phase 2: Split Generation (Coordinator)

This is where Iceberg's metadata really shines. The coordinator uses Iceberg's metadata to determine exactly which files to read.

<div class="mermaid">
sequenceDiagram
    participant C as Trino Coordinator
    participant IC as Iceberg Connector
    participant S3 as S3
    
    Note over C: Phase 2: Generate Splits
    
    IC->>S3: GET snap-xxx.avro (manifest list)
    S3-->>IC: List of manifest files with partition bounds
    
    Note over IC: Partition Pruning Round 1:<br/>Check partition bounds in manifest list<br/>Table partitioned by country, signup_month<br/>Skip manifests with no 'US' partition
    
    IC->>S3: GET manifest-m0.avro (only relevant ones)
    IC->>S3: GET manifest-m1.avro
    S3-->>IC: File entries with column stats
    
    Note over IC: Partition Pruning Round 2:<br/>Check each file's partition values<br/>Skip files where country ≠ 'US'
    
    Note over IC: Min/Max Pruning Round 3:<br/>Check column statistics per file<br/>Skip files where max(signup_date) < 2024-01-01
    
    IC-->>C: Final split list: [data-007.parquet, data-012.parquet, data-019.parquet]
    
    Note over C: Only 3 of 500 data files need scanning!<br/>99.4% of data skipped
</div>

```
Pruning example:
  Table has 500 data files across all partitions
  
  Manifest list pruning:
    → 100 manifests → 15 manifests (country='US' partition range)
    
  Manifest file pruning (partition values):
    → 150 data files → 40 data files (exact country='US' match)
    
  Column statistics pruning (min/max on signup_date):
    → 40 data files → 3 data files (signup_date > 2024-01-01)
    
  Result: Read 3 files instead of 500 = 99.4% data skipped
```

**Each surviving data file becomes a "split"** — a unit of work that Trino assigns to a worker.

#### Phase 3: Distributed Execution (Workers)

```
Coordinator assigns splits to workers:
  Worker 1 → data-007.parquet (rows 0-125,000)
  Worker 2 → data-012.parquet (rows 0-125,000)
  Worker 3 → data-019.parquet (rows 0-125,000)

Each worker independently:
  1. Opens S3 connection to its assigned Parquet file
  2. Reads Parquet footer to find column chunks
  3. Reads only needed columns: customer_id, name, total_spent
     (Parquet columnar format = skip unneeded columns)
  4. Applies remaining filters in-memory
  5. Streams results back to coordinator

Coordinator:
  1. Receives partial results from all workers
  2. Merges, sorts by total_spent DESC
  3. Takes top 100 rows
  4. Returns to client
```

### Trino Iceberg Connector Configuration

```properties
# /etc/trino/catalog/iceberg.properties

# Using REST Catalog
connector.name=iceberg
iceberg.catalog.type=rest
iceberg.rest-catalog.uri=https://polaris.example.com/api/catalog
iceberg.rest-catalog.warehouse=analytics_warehouse

# Using Hive Metastore
connector.name=iceberg
iceberg.catalog.type=hive_metastore
hive.metastore.uri=thrift://hive-metastore:9083

# Using AWS Glue
connector.name=iceberg
iceberg.catalog.type=glue
```

### Trino-Specific Iceberg Behaviors

| Feature | How Trino Handles It |
|---------|---------------------|
| **Deletes** | Merge-on-read: creates positional delete files (not copy-on-write) |
| **Updates** | Decomposes into delete + insert |
| **Predicate pushdown** | Pushes filters into Iceberg scan planning for partition and file pruning |
| **Column pruning** | Reads only referenced Parquet columns |
| **Statistics** | Uses Iceberg column stats for cost-based optimization |
| **Time travel** | `SELECT * FROM t FOR TIMESTAMP AS OF ...` or `FOR VERSION AS OF ...` |

---

## How Spark Queries Iceberg Tables

Spark has a fundamentally different architecture from Trino. It's a **distributed compute engine** with a driver-executor model, and uses the **DataSource V2 API** to integrate with Iceberg.

### Spark Architecture Overview

<div class="mermaid">
graph TD
    APP["<b>Spark Application</b><br/>spark.sql() or DataFrame API"] --> DRIVER["<b>Spark Driver</b><br/>Query planning<br/>Job scheduling<br/>Task distribution"]
    
    DRIVER -->|"<b>Uses Iceberg library</b>"| ICE["<b>Iceberg Library</b><br/>(SparkSessionCatalog)<br/>DataSource V2 API"]
    ICE -->|"Catalog calls"| CAT["<b>Catalog</b><br/>REST / Hive / Glue"]
    ICE -->|"Metadata reads"| S3M["<b>S3 Metadata</b><br/>metadata.json<br/>manifest list/files"]
    
    DRIVER -->|"<b>Task 1</b>"| EX1["<b>Executor 1</b><br/>(JVM on worker node)"]
    DRIVER -->|"<b>Task 2</b>"| EX2["<b>Executor 2</b><br/>(JVM on worker node)"]
    DRIVER -->|"<b>Task 3</b>"| EX3["<b>Executor 3</b><br/>(JVM on worker node)"]
    
    EX1 -->|"Reads data"| S3D["<b>S3 Data Files</b><br/>Parquet files"]
    EX2 -->|"Reads data"| S3D
    EX3 -->|"Reads data"| S3D

    style APP fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style DRIVER fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style ICE fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#fff
    style CAT fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style S3M fill:#607D8B,stroke:#455A64,stroke-width:2px,color:#fff
    style EX1 fill:#E91E63,stroke:#C2185B,stroke-width:2px,color:#fff
    style EX2 fill:#E91E63,stroke:#C2185B,stroke-width:2px,color:#fff
    style EX3 fill:#E91E63,stroke:#C2185B,stroke-width:2px,color:#fff
    style S3D fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
</div>

### Step-by-Step: Spark Query Execution on Iceberg

```python
# The query
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.my_catalog.type", "rest") \
    .config("spark.sql.catalog.my_catalog.uri", "https://polaris.example.com/api/catalog") \
    .config("spark.sql.catalog.my_catalog.warehouse", "analytics_warehouse") \
    .getOrCreate()

df = spark.sql("""
    SELECT customer_id, name, total_spent
    FROM my_catalog.analytics.customers
    WHERE country = 'US' AND signup_date > '2024-01-01'
    ORDER BY total_spent DESC
    LIMIT 100
""")
df.show()
```

#### Phase 1: Catalog Resolution (Driver)

<div class="mermaid">
sequenceDiagram
    participant App as Spark App
    participant D as Spark Driver
    participant SC as SparkCatalog<br/>(Iceberg)
    participant RC as REST Catalog
    participant S3 as S3

    App->>D: spark.sql("SELECT ... FROM my_catalog.analytics.customers ...")
    
    Note over D: 1. Parse SQL
    Note over D: 2. Resolve catalog: "my_catalog" → SparkCatalog (Iceberg)
    
    D->>SC: loadTable(Identifier["analytics", "customers"])
    SC->>RC: GET /v1/.../namespaces/analytics/tables/customers
    RC-->>SC: metadata-location + credentials
    SC->>S3: GET v42.metadata.json
    S3-->>SC: Full table metadata
    SC-->>D: SparkTable object (schema, partitions, properties)
    
    Note over D: 3. Create logical plan
    Note over D: 4. Catalyst optimizer pushes predicates
</div>

#### Phase 2: Scan Planning via DataSource V2 (Driver)

Spark uses the **DataSource V2 API** — Iceberg implements this interface to control how scans are planned:

```
Spark calls Iceberg's DataSource V2 implementation:

1. SparkScanBuilder.build()
   → IcebergScan created with pushed-down filters

2. IcebergScan.planInputPartitions()
   → Iceberg library reads manifest list from S3
   → Reads manifest files from S3
   → Applies partition pruning (country = 'US')
   → Applies column statistics pruning (signup_date > 2024-01-01)
   → Returns list of IcebergInputPartition objects
   
3. Each IcebergInputPartition maps to:
   → One or more Parquet files on S3
   → A specific set of columns to read
   → Residual filters to apply after read
```

**The key difference from Trino:** In Spark, the Iceberg Java library runs directly inside the Driver JVM. There's no separate connector process — Iceberg's scan planning code is embedded in the Spark application.

#### Phase 3: Task Execution (Executors)

<div class="mermaid">
sequenceDiagram
    participant D as Spark Driver
    participant E1 as Executor 1
    participant E2 as Executor 2
    participant S3 as S3

    Note over D: Distribute tasks based on<br/>IcebergInputPartitions

    D->>E1: Task: read data-007.parquet<br/>columns: [customer_id, name, total_spent]
    D->>E2: Task: read data-012.parquet<br/>columns: [customer_id, name, total_spent]
    
    E1->>S3: GET data-007.parquet (range request for column chunks)
    S3-->>E1: Column data (only 3 columns, not all)
    Note over E1: 1. Deserialize Parquet column chunks<br/>2. Apply residual filters<br/>3. Create InternalRow batch<br/>4. Vectorized if enabled
    
    E2->>S3: GET data-012.parquet (range request for column chunks)
    S3-->>E2: Column data (only 3 columns, not all)
    Note over E2: Same processing as Executor 1
    
    E1-->>D: Partial results (RDD partition)
    E2-->>D: Partial results (RDD partition)
    
    Note over D: Shuffle + Sort by total_spent DESC<br/>Take top 100 rows<br/>Return to application
</div>

### Spark-Specific Iceberg Behaviors

| Feature | How Spark Handles It |
|---------|---------------------|
| **Write mode** | Copy-on-write (default) or merge-on-read (configurable) |
| **Deletes** | Copy-on-write: rewrites entire Parquet files without deleted rows |
| **DataSource V2** | Iceberg implements `TableProvider`, `ScanBuilder`, `WriteBuilder` |
| **Predicate pushdown** | Catalyst optimizer pushes filters into `IcebergScanBuilder` |
| **Vectorized reads** | Supports vectorized Parquet reading for better throughput |
| **Partitioned writes** | Automatically distributes data by partition using Spark shuffle |
| **Streaming** | Supports Structured Streaming for incremental reads/writes |
| **Time travel** | `spark.read.option("as-of-timestamp", "...").table("t")` |

### Spark Write Flow

When Spark writes to an Iceberg table, the flow reverses:

```python
# Spark write
df.writeTo("my_catalog.analytics.customers").append()
```

<div class="mermaid">
sequenceDiagram
    participant D as Spark Driver
    participant E1 as Executor 1
    participant E2 as Executor 2
    participant S3 as S3
    participant RC as REST Catalog

    D->>E1: Write partition country='US'
    D->>E2: Write partition country='UK'
    
    E1->>S3: PUT data-new-001.parquet
    S3-->>E1: Success
    E2->>S3: PUT data-new-002.parquet
    S3-->>E2: Success
    
    E1-->>D: File report: data-new-001.parquet (50K rows, stats)
    E2-->>D: File report: data-new-002.parquet (30K rows, stats)
    
    Note over D: Assemble new snapshot:<br/>- New manifest file listing new data files<br/>- New manifest list pointing to new + existing manifests<br/>- New metadata.json with new snapshot
    
    D->>S3: PUT new manifest file
    D->>S3: PUT new manifest list  
    D->>S3: PUT v43.metadata.json
    
    D->>RC: POST /v1/.../tables/customers (commit)
    Note over RC: Validate: current metadata == v42<br/>Update pointer: v42 → v43
    RC-->>D: Success (or 409 Conflict → retry)
</div>

---

## Trino vs Spark: How They Differ with Iceberg

<div class="mermaid">
graph LR
    subgraph TRINO["<b>Trino Architecture</b>"]
        TC["Coordinator"]
        TW1["Worker 1"]
        TW2["Worker 2"]
        TC --> TW1
        TC --> TW2
    end
    
    subgraph SPARK["<b>Spark Architecture</b>"]
        SD["Driver"]
        SE1["Executor 1"]
        SE2["Executor 2"]
        SD --> SE1
        SD --> SE2
    end

    style TRINO fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#000
    style SPARK fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#000
    style TC fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style TW1 fill:#64B5F6,stroke:#1976D2,stroke-width:2px,color:#fff
    style TW2 fill:#64B5F6,stroke:#1976D2,stroke-width:2px,color:#fff
    style SD fill:#FF9800,stroke:#F57C00,stroke-width:2px,color:#fff
    style SE1 fill:#FFB74D,stroke:#F57C00,stroke-width:2px,color:#fff
    style SE2 fill:#FFB74D,stroke:#F57C00,stroke-width:2px,color:#fff
</div>

| Aspect | Trino | Spark |
|--------|-------|-------|
| **Architecture** | Coordinator + stateless workers | Driver + executors (JVMs with memory) |
| **Iceberg integration** | Connector plugin (separate JAR) | Iceberg library in Driver classpath |
| **Scan planning** | Coordinator via Iceberg Connector | Driver via DataSource V2 API |
| **Data reading** | Workers read Parquet directly from S3 | Executors read Parquet directly from S3 |
| **Catalog access** | Coordinator only (connector layer) | Driver only (SparkCatalog) |
| **Split/Task unit** | One split ≈ one Parquet file | One task ≈ one InputPartition (1+ files) |
| **Default delete mode** | Merge-on-read (positional deletes) | Copy-on-write (rewrite files) |
| **Best for** | Ad-hoc SQL queries, interactive BI | ETL, batch processing, ML pipelines |
| **Latency** | Low (seconds) — always running | Higher (minutes) — JVM startup + shuffle |
| **Shuffle** | Pipeline-based (streaming between stages) | Disk-based (write shuffle files) |

---

## Deep Dive: Reading Parquet Files from S3

Both Trino and Spark ultimately read Parquet files from S3. Here's exactly what happens at the storage level.

### Parquet File Internal Structure

```
data-007.parquet (125,000 rows, 15 columns)
│
├── Row Group 0 (rows 0-65,535)
│   ├── Column Chunk: customer_id    [offset: 0,    length: 450KB]
│   ├── Column Chunk: name           [offset: 450K, length: 2.1MB]
│   ├── Column Chunk: email          [offset: 2.5M, length: 1.8MB]
│   ├── Column Chunk: country        [offset: 4.3M, length: 180KB]
│   ├── Column Chunk: signup_date    [offset: 4.5M, length: 290KB]
│   ├── Column Chunk: total_spent    [offset: 4.8M, length: 510KB]
│   └── ... (9 more columns)
│
├── Row Group 1 (rows 65,536-125,000)
│   └── ... (same column chunk structure)
│
└── Footer (at end of file)
    ├── Schema definition
    ├── Row group metadata
    │   ├── Column chunk locations (offset + size)
    │   └── Column statistics (min, max, null count)
    └── Key-value metadata
```

### S3 Read Sequence

<div class="mermaid">
sequenceDiagram
    participant W as Trino Worker / Spark Executor
    participant S3 as Amazon S3

    Note over W: Need: customer_id, name, total_spent<br/>from data-007.parquet

    W->>S3: GET data-007.parquet<br/>Range: bytes=-8<br/>(read magic bytes at end to find footer offset)
    S3-->>W: Footer offset: 12,450,000

    W->>S3: GET data-007.parquet<br/>Range: bytes=12450000-12451234<br/>(read Parquet footer)
    S3-->>W: Footer with column chunk offsets + stats

    Note over W: Footer tells us:<br/>customer_id @ offset 0, 450KB<br/>name @ offset 450K, 2.1MB<br/>total_spent @ offset 4.8M, 510KB<br/><br/>Skip: email, country, signup_date, ...<br/>(not in SELECT)

    W->>S3: GET data-007.parquet<br/>Range: bytes=0-460800<br/>(customer_id column chunk)
    S3-->>W: Compressed column data

    W->>S3: GET data-007.parquet<br/>Range: bytes=450000-2600000<br/>(name column chunk)
    S3-->>W: Compressed column data

    W->>S3: GET data-007.parquet<br/>Range: bytes=4800000-5310000<br/>(total_spent column chunk)
    S3-->>W: Compressed column data

    Note over W: Total: 5 S3 GET requests<br/>Read: ~3MB of 15MB file<br/>Skipped: 80% of file data
</div>

**Key optimization — HTTP Range Requests:**

S3 supports reading specific byte ranges from a file. The query engine uses this to:
1. Read just the footer (to discover column locations)
2. Read only the columns needed by the query
3. Skip entire row groups based on column statistics in the footer

```
Without column pruning:
  Read entire file: 15 MB × 500 files = 7.5 GB from S3

With Iceberg partition pruning + Parquet column pruning:
  Read 3 columns from 3 files: 3 MB × 3 files = 9 MB from S3
  
  Savings: 99.88% less data read from S3
```

### S3 Request Costs

Every S3 GET request has a cost beyond just data transfer:

| Operation | Cost (us-east-1) | Notes |
|-----------|-------------------|-------|
| GET request | $0.0004 per 1,000 | Each range request = 1 GET |
| Data transfer | $0.00/GB (same region) | Free within same region |
| Data transfer | $0.09/GB (cross-region) | Expensive! Co-locate compute + storage |

```
Query cost breakdown:
  Metadata reads: ~5 GET requests (metadata.json + manifest list + manifests)
  Data reads: 3 files × 5 range requests each = 15 GET requests
  Total: ~20 GET requests = $0.008 (less than 1 cent)
  
  Without Iceberg pruning:
  Data reads: 500 files × 5 range requests each = 2,500 GET requests
  Total: ~2,505 GET requests = $1.00
  
  125x cost reduction with Iceberg metadata pruning
```

---

## Complete End-to-End Flow: Trino + REST Catalog + S3

Here's the complete picture showing every network call for a single Trino query:

<div class="mermaid">
sequenceDiagram
    participant U as User
    participant TC as Trino Coordinator
    participant IC as Iceberg Connector
    participant RC as REST Catalog<br/>(Polaris)
    participant S3 as Amazon S3
    participant TW as Trino Workers

    U->>TC: SELECT ... FROM customers WHERE country='US'
    
    rect rgb(230, 245, 255)
    Note over TC,RC: Phase 1: Table Resolution
    TC->>IC: getTableHandle("customers")
    IC->>RC: GET /v1/.../tables/customers
    RC-->>IC: metadata-location + temp S3 credentials
    end
    
    rect rgb(255, 243, 224)
    Note over IC,S3: Phase 2: Metadata Traversal
    IC->>S3: GET v42.metadata.json
    S3-->>IC: Schema, partition spec, current snapshot ID
    IC->>S3: GET snap-xxx.avro (manifest list)
    S3-->>IC: List of manifests with partition bounds
    IC->>S3: GET manifest-m0.avro (only matching manifests)
    S3-->>IC: Data file entries with column stats
    end
    
    rect rgb(232, 245, 233)
    Note over IC,TW: Phase 3: Pruning + Split Generation
    Note over IC: Partition pruning: 500 → 40 files<br/>Stats pruning: 40 → 3 files
    IC-->>TC: 3 splits (one per data file)
    TC->>TW: Assign splits to workers
    end
    
    rect rgb(243, 229, 245)
    Note over TW,S3: Phase 4: Data Reading
    TW->>S3: GET data-007.parquet (footer)
    S3-->>TW: Column offsets
    TW->>S3: GET data-007.parquet (column chunks)
    S3-->>TW: Parquet column data
    TW-->>TC: Partial results
    end
    
    TC-->>U: Final result (100 rows)
</div>

**Total network calls for this query:**

```
REST Catalog:  1 API call    (load table)
S3 Metadata:   3 GET requests (metadata.json + manifest list + 1 manifest)
S3 Data:      15 GET requests (3 files × 5 range requests each)
─────────────────────────────────
Total:        19 network calls
Time:         ~2-5 seconds (mostly S3 latency)
Data read:    ~9 MB (out of 7.5 GB total table size)
```

---

## Complete End-to-End Flow: Spark + REST Catalog + S3

```python
# Spark application
df = spark.sql("""
    SELECT customer_id, name, total_spent
    FROM my_catalog.analytics.customers
    WHERE country = 'US' AND signup_date > '2024-01-01'
""")
df.write.mode("overwrite").saveAsTable("my_catalog.analytics.us_customers")
```

<div class="mermaid">
sequenceDiagram
    participant App as PySpark App
    participant D as Spark Driver
    participant ICE as Iceberg Library
    participant RC as REST Catalog
    participant S3 as S3
    participant EX as Executors

    App->>D: spark.sql("SELECT ... WHERE country='US'")
    
    rect rgb(230, 245, 255)
    Note over D,RC: Phase 1: Catalog Resolution
    D->>ICE: loadTable("analytics.customers")
    ICE->>RC: GET /v1/.../tables/customers
    RC-->>ICE: metadata-location + credentials
    end
    
    rect rgb(255, 243, 224)
    Note over ICE,S3: Phase 2: Scan Planning (all on Driver)
    ICE->>S3: GET v42.metadata.json
    ICE->>S3: GET snap-xxx.avro
    ICE->>S3: GET manifest-m0.avro (pruned)
    Note over ICE: Build InputPartitions:<br/>3 Parquet files to read
    ICE-->>D: List of InputPartitions
    end
    
    rect rgb(232, 245, 233)
    Note over D,EX: Phase 3: Distributed Read
    D->>EX: Task: read data-007.parquet
    D->>EX: Task: read data-012.parquet
    EX->>S3: GET Parquet files (range requests)
    S3-->>EX: Column data
    EX-->>D: InternalRow batches
    end
    
    rect rgb(255, 235, 238)
    Note over D,RC: Phase 4: Write Results
    D->>EX: Write tasks for us_customers table
    EX->>S3: PUT new Parquet data files
    EX-->>D: File commit reports
    D->>S3: PUT new metadata files
    D->>RC: POST /v1/.../tables/us_customers (atomic commit)
    RC-->>D: Commit success
    end
</div>

---

## Performance Tips: Reducing S3 Calls

Understanding the internal flow helps you optimize performance:

### 1. Partition Your Tables Wisely

```sql
-- Good: queries frequently filter by country and date
CREATE TABLE customers (
    customer_id BIGINT,
    name STRING,
    country STRING,
    signup_date DATE,
    total_spent DECIMAL(10,2)
)
USING iceberg
PARTITIONED BY (country, months(signup_date));

-- This means:
-- WHERE country = 'US' → skips all non-US partitions in manifests
-- WHERE signup_date > '2024-01-01' → skips old month partitions
```

### 2. Keep Metadata Compact

```sql
-- Too many small files = too many manifest entries = slow scan planning
-- Run compaction regularly
CALL system.rewrite_data_files('analytics.customers');
CALL system.rewrite_manifests('analytics.customers');

-- Expire old snapshots to reduce manifest list size
CALL system.expire_snapshots('analytics.customers', TIMESTAMP '2024-06-01 00:00:00');
```

### 3. Use Column Statistics

```sql
-- Iceberg collects min/max stats per column per file
-- This enables file-level pruning even without partitioning
-- Make sure stats collection is enabled (it is by default)
ALTER TABLE customers SET TBLPROPERTIES (
    'write.metadata.metrics.default' = 'truncate(16)'
);
```

### 4. Co-locate Compute and Storage

```
Bad:  Trino in us-east-1, S3 bucket in eu-west-1
      → Every S3 GET has cross-region latency + $0.09/GB transfer
      
Good: Trino in us-east-1, S3 bucket in us-east-1
      → Low latency, free data transfer
```

---

## Summary

### What Happens When You Query Iceberg

```
1. ENGINE → CATALOG: "Where is the table?"
   Response: metadata file location + credentials

2. ENGINE → S3: Read metadata.json
   Response: current snapshot, schema, partition spec

3. ENGINE → S3: Read manifest list (Avro)
   Response: list of manifests with partition bounds

4. ENGINE → S3: Read relevant manifests (Avro)
   Response: list of data files with column stats
   (engine prunes files based on query predicates)

5. ENGINE → S3: Read data files (Parquet)
   Response: actual column data
   (engine reads only needed columns via range requests)
```

### Key Takeaways

- **REST Catalog** is a standard HTTP API — any engine that speaks HTTP can query Iceberg tables
- **Trino** does scan planning on the coordinator, distributes splits to stateless workers
- **Spark** does scan planning on the driver via DataSource V2, distributes tasks to executors
- **Both engines** use Iceberg's metadata tree (metadata.json → manifest list → manifests) to prune files before reading any data
- **Parquet range requests** mean engines read only the columns they need, not entire files
- **Credential vending** from REST Catalog means engines get short-lived, scoped S3 credentials
- **The real performance win:** Iceberg's metadata lets engines skip 90-99% of data files, turning a full table scan into a targeted read of a few files

---

## Further Reading

- [Iceberg REST Catalog Spec](https://iceberg.apache.org/rest-catalog-spec/)
- [Trino Iceberg Connector Docs](https://trino.io/docs/current/connector/iceberg.html)
- [Trino on Ice: Deep Dive into Iceberg Internals](https://trino.io/blog/2021/08/12/deep-dive-into-iceberg-internals.html)
- [Apache Iceberg Table Spec](https://iceberg.apache.org/spec/)
- [Spark Iceberg Integration](https://iceberg.apache.org/docs/latest/spark-queries/)
- [Apache Polaris Catalog](https://polaris.apache.org/)
