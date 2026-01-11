---
title: "Unified Data Infrastructure Layer (EDW + Snowflake + Databricks)"
category: Data
tags:
  - data-architecture
  - data-platform
  - lakehouse
  - snowflake
  - iceberg
  - governance
summary: A very simple, practical reference architecture for a unified data platform across on-prem EDW + Snowflake + Databricks — implemented incrementally.
---

## Modernizing Data Infrastructure: From Legacy EDW to Unified Platform

**Your data warehouse is becoming your biggest bottleneck.** The on-prem EDW that powered your business for the last decade can't keep up with AI, real-time analytics, and cloud-scale workloads. It's expensive to scale, slow to adapt, and wasn't built for the demands of modern data and ML.

**AI needs a unified data foundation.** You can't train models on fragmented data. You can't govern data across three different systems. You can't move fast when teams spend days reconciling numbers and searching for datasets.

**The reality:**

You have a **legacy on-prem EDW** built over 10-15 years. It holds critical historical data, runs finance and compliance workloads, and has hundreds of reports depending on it. You can't just "lift and shift" it to the cloud — the risk is too high, the cost is unclear, and the business won't tolerate downtime.

You also have an **on-prem Enterprise Data Lake (EDL)** — typically Cloudera Data Platform (CDP) with Hadoop and Spark. It was built to handle big data workloads that the EDW couldn't, but it's become another silo with its own data, governance, and access patterns.

But you also **can't scale on-prem anymore.** Storage is expensive, compute is limited, and your team wants cloud-native tools and flexibility. So you've added cloud platforms — Snowflake for analytics, Databricks for engineering and ML.

**Now you have a hybrid mess:**
- Your **new cloud infrastructure** needs to fetch data from **both EDW and CDP/EDL**
- Data exists in three places: EDW (structured), CDP/Hadoop (big data), and cloud (Snowflake/Databricks)
- Teams build the same pipelines multiple times (EDW, CDP, cloud)
- Data is duplicated, governance diverges, and nobody knows which system has the "truth"
- You're paying for four platforms (EDW + CDP + Snowflake + Databricks) but getting one fragmented experience

**You can't put all data in the cloud.** Compliance, latency, and legacy dependencies keep some data on-prem.

**You can't stay fully on-prem.** You need cloud scale, modern tools, and flexibility to power AI and modern analytics.

**The solution:** A unified data infrastructure layer built on **on-prem object storage + Iceberg + Spark + federated query** that makes EDW + Snowflake + Databricks feel like one platform — giving you the strong data foundation needed to scale AI, without forcing a big-bang migration.

**The core layer:**
- **On-prem object storage** (MinIO, Ceph, Dell ECS) as your lakehouse foundation
- **Apache Iceberg** for open table format (works everywhere)
- **Spark** for transformations (on-prem or cloud)
- **Federated query** (Trino/Presto) to query across on-prem and cloud seamlessly

> **Think of it like a city with old and new infrastructure.** You don't tear down the old water system overnight. You build new pipes (object storage + Iceberg) that connect to the old ones (EDW), standardize the quality checks (Spark), and give everyone one map (federated query) to find what they need — even if data lives both on-prem and in cloud.

---

## The Pain: Which Platform Should We Use?

### Problem 1: Platform Paralysis

```
Data Engineer: "Where should I build this new pipeline?"
  Option A: EDW (legacy, but finance depends on it)
  Option B: Databricks (modern, but not everyone has access)
  Option C: Snowflake (fast, but expensive for large transforms)

Result: 3-day debate, no decision, project delayed
```

**The real issue:** You don't have a clear answer to "which platform for what workload?"

### Problem 2: Every Team Picks a Different Platform

```
Finance team: "We only trust the EDW"
Data Science team: "We only use Databricks"
BI team: "We only use Snowflake"
Analytics Engineering: "We use dbt... but where do we run it?"

Result: Data scattered across 3 platforms, no one can find anything
```

**The real issue:** No unified strategy, every team optimizes locally.

### Problem 3: Same Dataset, Three Different Versions

```
Customer data exists in:
- EDW: customer_master (legacy schema)
- Databricks: silver.customers (Delta Lake)
- Snowflake: analytics.dim_customer (star schema)

Which one is the source of truth? Nobody knows.

Result: Teams build their own versions, making it worse
```

**The real issue:** No single system of record for curated data.

### Problem 4: Platform Lock-In Fears

```
Executive: "If we go all-in on Snowflake, what if we need to move?"
Architect: "If we standardize on Databricks, can BI teams still use Tableau?"
CFO: "Why are we paying for three platforms?"

Result: Analysis paralysis, no modernization happens
```

**The real issue:** Fear of vendor lock-in prevents any decision.

### Problem 5: New Workloads Don't Know Where to Go

```
ML Engineer: "I need to train a model on customer data"
  - EDW has historical data (but no GPU, no Spark)
  - Databricks has ML tools (but data is in EDW)
  - Snowflake has some data (but expensive for training)

Result: Copy data everywhere, waste time, duplicate storage costs
```

**The real issue:** No clear platform strategy for different workload types.

**The root cause?** You have multiple platforms, but no **unified strategy** or **clear decision framework** for which platform to use for what.

---

## The Solution: One Logical Platform (Not One Physical System)

> **Key insight:** You don't need to replace everything with one tool. You need to standardize **how things work together** — including on-prem platforms like EDL/CDP, EDW, and cloud platforms like Snowflake and Databricks.

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','secondaryColor':'#f0f0f0','tertiaryColor':'#fff','fontSize':'14px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TB
    subgraph BEFORE["❌ BEFORE: Fragmented"]
        direction TB
        EDW1["🏢<br/>EDW<br/>(on-prem)"]
        CDP1["🐘<br/>CDP/EDL<br/>(on-prem)"]
        SNOW1["❄️<br/>Snowflake<br/>(cloud)"]
        DBX1["⚡<br/>Databricks<br/>(cloud)"]
        
        EDW1 -."different<br/>rules".-> CDP1
        CDP1 -."different<br/>rules".-> SNOW1
        SNOW1 -."different<br/>rules".-> DBX1
        DBX1 -."different<br/>rules".-> EDW1
    end
    
    ARROW["⬇️<br/>TRANSFORM"]
    
    subgraph AFTER["✅ AFTER: Unified"]
        direction TB
        UNIFIED["📦 Unified Data Infra Layer<br/>━━━━━━━━━━━━━━━━━━<br/>📚 Catalog | 🔒 Governance | 📋 Contracts | 🗄️ Object Storage + Iceberg"]
        
        EDW2["🏢<br/>EDW"]
        CDP2["🐘<br/>CDP/EDL"]
        SNOW2["❄️<br/>Snowflake"]
        DBX2["⚡<br/>Databricks"]
        
        UNIFIED ==>|"same<br/>rules"| EDW2
        UNIFIED ==>|"same<br/>rules"| CDP2
        UNIFIED ==>|"same<br/>rules"| SNOW2
        UNIFIED ==>|"same<br/>rules"| DBX2
    end
    
    BEFORE --> ARROW
    ARROW --> AFTER
    
    style BEFORE fill:#ffcdd2,stroke:#c62828,stroke-width:3px,stroke-dasharray: 5 5
    style AFTER fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style UNIFIED fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style ARROW fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style EDW1 fill:#fff,stroke:#000,stroke-width:2px
    style CDP1 fill:#fff,stroke:#000,stroke-width:2px
    style SNOW1 fill:#fff,stroke:#000,stroke-width:2px
    style DBX1 fill:#fff,stroke:#000,stroke-width:2px
    style EDW2 fill:#fff,stroke:#000,stroke-width:2px
    style CDP2 fill:#fff,stroke:#000,stroke-width:2px
    style SNOW2 fill:#fff,stroke:#000,stroke-width:2px
    style DBX2 fill:#fff,stroke:#000,stroke-width:2px
</div>

What makes it feel like "one platform"? You standardize:

- **How data lands** (ingestion contracts)
- **How it's stored** (one open table format + consistent zones)
- **How it's governed** (one catalog + one policy model)
- **How it's observed** (lineage + data quality)
- **How it's consumed** (semantic layer + APIs)

If you do *just that*, you can modernize without a big-bang migration.

---

## The 2-Plane Model (Control Plane vs Data Plane)

> **Think of it like air traffic control.** The control tower (Control Plane) coordinates all the planes (Data Plane), but the planes still fly independently. The tower ensures they don't crash into each other and follow the same rules.

Most enterprises end up with this split:

- **Control Plane**: the *unified experience* (catalog, policies, contracts, quality, lineage, portal)
- **Data Plane**: where *data + compute* actually live (EDW / Snowflake / Databricks / object storage)

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TB
    subgraph CP["🎯 CONTROL PLANE: Unified Data Infrastructure Layer"]
        direction LR
        CATALOG["📚<br/>Catalog +<br/>Discovery"]
        POLICY["🔒<br/>Policy<br/>Engine"]
        CONTRACTS["📋<br/>Data<br/>Contracts"]
        LINEAGE["🔗<br/>Lineage +<br/>Audit"]
        QUALITY["✅<br/>Quality<br/>Framework"]
        PORTAL["🌐<br/>Self-serve<br/>Portal"]
    end

    subgraph DP["💾 DATA PLANE: Where Data Lives"]
        subgraph ONPREM["🏢 ON-PREM"]
            direction TB
            EDW["🏢 EDW<br/>(Legacy)"]
            CDP["🐘 CDP/Hadoop<br/>(Legacy EDL)"]
            SRC1["💾 DBs<br/>📁 Files<br/>📱 Apps"]
            OBJ["🗄️ Object Storage<br/>━━━━━━━━━━━━<br/>MinIO/Ceph/Dell ECS<br/>📊 Iceberg Tables<br/>🥉 Bronze | 🥈 Silver | 🥇 Gold"]
            SPARK["⚡ Spark<br/>(CDP or standalone)<br/>Transformations"]
        end

        subgraph CLOUD["☁️ CLOUD"]
            direction TB
            DBX["⚡ Databricks<br/>Engineering + ML"]
            SNOW["❄️ Snowflake<br/>Analytics + BI"]
            SAAS["🌍 SaaS<br/>Sources"]
        end
    end

    SRC1 ==>|"📥 Batch<br/>CDC<br/>Streams"| OBJ
    SAAS ==>|"📥 Batch<br/>Streams"| OBJ

    OBJ <===>|"read/write"| SPARK
    OBJ <===>|"read via VPN<br/>(Iceberg)"| DBX
    OBJ <===>|"read via VPN<br/>(Iceberg)"| SNOW
    EDW -.->|"optional sync"| OBJ
    CDP -.->|"optional sync"| OBJ

    CP -."🔐 governs".-> EDW
    CP -."🔐 governs".-> OBJ
    CP -."🔐 governs".-> DBX
    CP -."🔐 governs".-> SNOW
    
    style CP fill:#e3f2fd,stroke:#1565c0,stroke-width:4px
    style DP fill:#fff8e1,stroke:#f57f17,stroke-width:4px
    style ONPREM fill:#ffebee,stroke:#c62828,stroke-width:3px,stroke-dasharray: 5 5
    style CLOUD fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style OBJ fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style CATALOG fill:#fff,stroke:#000,stroke-width:2px
    style POLICY fill:#fff,stroke:#000,stroke-width:2px
    style CONTRACTS fill:#fff,stroke:#000,stroke-width:2px
    style LINEAGE fill:#fff,stroke:#000,stroke-width:2px
    style QUALITY fill:#fff,stroke:#000,stroke-width:2px
    style PORTAL fill:#fff,stroke:#000,stroke-width:2px
    style EDW fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
    style CDP fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
    style SRC1 fill:#fff,stroke:#000,stroke-width:2px
    style SPARK fill:#fff,stroke:#000,stroke-width:2px
    style DBX fill:#fff,stroke:#000,stroke-width:2px
    style SNOW fill:#fff,stroke:#000,stroke-width:2px
    style SAAS fill:#fff,stroke:#000,stroke-width:2px
</div>

**The Control Plane** is what makes teams say: "This feels unified."

**The Data Plane** is where the actual work happens (storage + compute).

---

## How Data Flows Through the System

> **Real example:** A customer places an order on your website. Let's trace that data through the entire platform.

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart LR
    subgraph ONPREM_FLOW["🏢 ON-PREM"]
        ORDER["🛍️<br/>Order Placed<br/>━━━━━━━<br/>Website DB"]
        
        INGEST["📥<br/>Ingestion<br/>Layer<br/>━━━━━━<br/>CDC Capture"]
        
        LANDING["🥉 BRONZE<br/>On-Prem Object Storage<br/>━━━━━━━━<br/>Raw Order Data<br/>Iceberg Table"]
        
        CURATED["🥈 SILVER<br/>On-Prem Object Storage<br/>━━━━━━━━<br/>Cleaned + Joined<br/>Orders + Customers"]
        
        PRODUCTS["🥇 GOLD<br/>On-Prem Object Storage<br/>━━━━━━━━<br/>Order Analytics<br/>Customer 360"]
        
        EDW_FIN["🏢<br/>EDW (Legacy)<br/>━━━━━━<br/>Finance Reports"]
    end
    
    subgraph CLOUD_FLOW["☁️ CLOUD"]
        SNOW_BI["❄️<br/>Snowflake<br/>━━━━━━<br/>BI Dashboards"]
        DBX_ML["⚡<br/>Databricks<br/>━━━━━━<br/>ML Models"]
    end
    
    ORDER ==>|"❶ Capture"| INGEST
    INGEST ==>|"❷ Validate +<br/>Publish"| LANDING
    LANDING ==>|"❸ Transform<br/>(Spark)"| CURATED
    CURATED ==>|"❹ Build<br/>Products"| PRODUCTS
    
    PRODUCTS ==>|"❺ Read via VPN<br/>(Iceberg)"| SNOW_BI
    PRODUCTS ==>|"❻ Read via VPN<br/>(Iceberg)"| DBX_ML
    PRODUCTS -.->|"❼ Optional<br/>sync"| EDW_FIN
    
    style ONPREM_FLOW fill:#ffebee,stroke:#c62828,stroke-width:4px,stroke-dasharray: 5 5
    style CLOUD_FLOW fill:#e8f5e9,stroke:#2e7d32,stroke-width:4px
    style ORDER fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style INGEST fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style LANDING fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style CURATED fill:#bbdefb,stroke:#1565c0,stroke-width:3px
    style PRODUCTS fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style SNOW_BI fill:#fff,stroke:#000,stroke-width:2px
    style DBX_ML fill:#fff,stroke:#000,stroke-width:2px
    style EDW_FIN fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
</div>

**Step-by-step:**

1. **Order placed** → captured by CDC (Change Data Capture)
2. **Ingestion** → validated against contract, published to Landing zone
3. **Curation** → cleaned, joined with customer data, published to Curated zone
4. **Data Products** → domain team builds "Order Analytics" product
5. **Consumption** → served to Snowflake (BI), Databricks (ML), EDW (Finance)

**Key point:** Data flows through **one path**, but can be consumed by **multiple engines**.

---

## The Lakehouse Zones (Bronze → Silver → Gold)

> **Think of it like a factory assembly line.** Raw materials come in (Bronze), get processed (Silver), and become finished products (Gold).

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart LR
    subgraph BRONZE["🥉 BRONZE: Landing Zone"]
        direction TB
        B1["✅ Raw, Immutable<br/>✅ Source-aligned<br/>✅ No transformations"]
        B2["📝 Example:<br/>• raw_orders<br/>• raw_customers<br/>• raw_events"]
    end
    
    subgraph SILVER["🥈 SILVER: Curated Zone"]
        direction TB
        S1["✅ Cleaned, Standardized<br/>✅ Conformed dimensions<br/>✅ Quality checks passed"]
        S2["📝 Example:<br/>• clean_orders<br/>• clean_customers<br/>• conformed_products"]
    end
    
    subgraph GOLD["🥇 GOLD: Products Zone"]
        direction TB
        G1["✅ Business-ready<br/>✅ Dimensional models<br/>✅ Feature sets<br/>✅ Aggregates"]
        G2["📝 Example:<br/>• order_analytics<br/>• customer_360<br/>• ml_features"]
    end
    
    BRONZE ==>|"⚙️ Transform<br/>+ Clean"| SILVER
    SILVER ==>|"🛠️ Build<br/>Products"| GOLD
    
    style BRONZE fill:#ffcdd2,stroke:#c62828,stroke-width:4px
    style SILVER fill:#bbdefb,stroke:#1565c0,stroke-width:4px
    style GOLD fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px
    style B1 fill:#fff,stroke:#000,stroke-width:2px
    style B2 fill:#fff,stroke:#000,stroke-width:2px
    style S1 fill:#fff,stroke:#000,stroke-width:2px
    style S2 fill:#fff,stroke:#000,stroke-width:2px
    style G1 fill:#fff,stroke:#000,stroke-width:2px
    style G2 fill:#fff,stroke:#000,stroke-width:2px
</div>

### Bronze Zone (Landing)

**Purpose:** Store raw data exactly as it arrived

**Characteristics:**
- Immutable (never modified)
- Source-aligned (one table per source table)
- No transformations
- Keep everything (even bad data goes to quarantine)

**Example:**
```
s3://lakehouse/bronze/orders/
  - raw_orders_2024_01_11.parquet
  - raw_orders_2024_01_12.parquet
```

### Silver Zone (Curated)

**Purpose:** Cleaned, standardized, ready for analytics

**Characteristics:**
- Data quality checks passed
- Standardized formats (dates, currencies, etc.)
- Conformed dimensions (one customer table, not five)
- Deduplicated

**Example:**
```
s3://lakehouse/silver/orders/
  - clean_orders/ (Iceberg table)
  - clean_customers/ (Iceberg table)
```

### Gold Zone (Products)

**Purpose:** Business-ready datasets for specific use cases

**Characteristics:**
- Domain-owned (Finance owns revenue tables)
- Documented + versioned
- Optimized for consumption
- SLAs enforced

**Example:**
```
s3://lakehouse/gold/finance/
  - revenue_daily/ (dimensional model)
  - customer_lifetime_value/ (aggregate)
```

---

## Reference Architecture: The 7 Layers

> **Each layer solves a specific problem.** You can implement them incrementally (you don't need all 7 on day one).

### Layer A: Connectivity and Ingestion

**Goal:** Move data reliably between on-prem and cloud, batch + streaming

**Typical sources:**
- On-prem databases (CDC / log-based replication)
- Legacy file drops (SFTP, NFS)
- Application events / streams (Kafka, Kinesis)
- SaaS and cloud databases (Salesforce, Workday, etc.)

**Standard pattern:** Treat ingestion as **pipelines with contracts**

A contract should include:

| Field | Example |
|-------|---------|
| **Schema** | `{order_id: int, amount: decimal, customer_id: int}` |
| **SLA** | Freshness: < 15 minutes, Latency: < 5 minutes |
| **PII tags** | `customer_email` tagged as PII |
| **Owner** | Team: Orders, Escalation: orders-oncall@company.com |
| **Retention** | Keep raw data for 90 days |
| **Expected volume** | 10K-50K records/hour |

**Pipeline shape** (standardize this everywhere):

```
ingest → validate → quarantine → publish
```

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart LR
    SOURCE["💾<br/>Data Source<br/>━━━━━━━<br/>DB / API / File"]
    INGEST["📥<br/>Ingest<br/>━━━━━━<br/>CDC / Batch"]
    VALIDATE["✅<br/>Validate<br/>━━━━━━━<br/>Against Contract<br/>Schema + SLA"]
    QUARANTINE["❌<br/>Quarantine<br/>━━━━━━━━<br/>Bad Data<br/>Alert Owner"]
    PUBLISH["📤<br/>Publish<br/>━━━━━━<br/>Landing Zone<br/>Iceberg Table"]
    
    SOURCE ==> INGEST
    INGEST ==> VALIDATE
    VALIDATE ==>|"✅ Valid"| PUBLISH
    VALIDATE ==>|"❌ Invalid"| QUARANTINE
    
    style SOURCE fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style INGEST fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style VALIDATE fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style QUARANTINE fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style PUBLISH fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
</div>

**Why this matters:** This single pattern prevents "every team reinvents ingestion differently."

---

### Layer B: Unified Storage (Lakehouse Foundation)

**Goal:** One consistent data representation across platforms using **object storage + Iceberg**

**The core architecture: On-prem object storage as your lakehouse**

```
🏢 On-Prem Object Storage (Primary Option)
├── MinIO (S3-compatible, open source)
├── Ceph (enterprise-grade, scalable)
├── Dell ECS (enterprise storage)
└── NetApp StorageGRID (hybrid cloud)

+ Apache Iceberg tables
+ Spark for transformations
+ Trino/Presto for federated query
```

**Why on-prem object storage?**

- ✅ **Data stays on-prem** (compliance, latency, governance)
- ✅ **S3-compatible API** (works with all modern tools)
- ✅ **No cloud egress costs** (data doesn't leave your datacenter)
- ✅ **Scales like cloud** (petabyte-scale, elastic)
- ✅ **Works with Iceberg** (same as S3/ADLS/GCS)

**Use a single "platform default" open table format:**

- **Apache Iceberg** (recommended - works everywhere: on-prem, Snowflake, Databricks, Trino)
- Delta Lake or Hudi can work too, but **pick one** to reduce fragmentation

**Why open format (Iceberg)?**

```
Proprietary format (Snowflake-only):
- Data locked in Snowflake
- Can't use Databricks without copying
- Can't query from on-prem Spark
- Vendor lock-in

Open format (Iceberg on object storage):
- On-prem Spark can read it ✅
- Snowflake can read it (external tables) ✅
- Databricks can read it ✅
- Trino/Presto can read it ✅
- Future tools can read it ✅
```

**Key rule:** Object storage (on-prem or cloud) becomes your **system-of-record for analytical data** going forward.

**Deployment options:**

1. **On-prem only:** Object storage + Iceberg on-prem, federated query to cloud when needed
2. **Hybrid:** Primary data on-prem, replicate to cloud for specific workloads
3. **Cloud primary:** S3/ADLS/GCS, replicate back to on-prem if needed

**The directional goal:**
- Publish curated datasets to object storage (on-prem or cloud) in Iceberg format
- Let Spark, Snowflake, Databricks, Trino all read from that same truth
- Use federated query (Trino/Presto) to query across locations seamlessly

#### Detailed Hybrid Architecture: Object Storage + Iceberg Internals

> **This shows how on-prem and cloud connect, and what's inside the lakehouse storage layer.**

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'12px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TB
    subgraph ONPREM["🏢 ON-PREM DATA CENTER"]
        direction TB
        
        EDW_SYS["🏢 EDW (Legacy)<br/>━━━━━━<br/>Teradata/Oracle<br/>Netezza"]
        APPS["📱 Apps<br/>━━━━━━<br/>CRM/ERP<br/>Legacy Systems"]
        DBS["💾 Databases<br/>━━━━━━<br/>SQL Server<br/>PostgreSQL"]
        
        subgraph ONPREM_STORAGE["🗄️ ON-PREM OBJECT STORAGE (Primary)"]
            direction TB
            MINIO["MinIO / Ceph / Dell ECS<br/>━━━━━━━━━━━━━━━━<br/>S3-compatible API"]
            
            subgraph ICEBERG["📊 ICEBERG TABLE STRUCTURE"]
                direction LR
                META["📋 Metadata<br/>━━━━━━━━<br/>metadata.json<br/>snapshots/"]
                MANIFEST["📑 Manifest Files<br/>━━━━━━━━━━━<br/>manifest.avro<br/>(pointers to data)"]
                DATA["📦 Data Files<br/>━━━━━━━━━━<br/>parquet files<br/>immutable"]
            end
            
            BRONZE_S["🥉 bronze/<br/>raw_orders/<br/>raw_customers/"]
            SILVER_S["🥈 silver/<br/>clean_orders/<br/>clean_customers/"]
            GOLD_S["🥇 gold/<br/>order_analytics/<br/>customer_360/"]
        end
        
        SPARK_ONPREM["⚡ Spark (On-Prem)<br/>━━━━━━━━━━━<br/>Transformations<br/>reads/writes Iceberg"]
        
        TRINO["🔍 Trino/Presto<br/>━━━━━━━━━━━<br/>Federated Query<br/>across on-prem + cloud"]
    end
    
    subgraph CLOUD["☁️ CLOUD (AWS/Azure/GCP)"]
        direction TB
        
        CLOUD_STORAGE["🗄️ Cloud Object Storage<br/>━━━━━━━━━━━━━━<br/>S3/ADLS/GCS<br/>(Optional: replicated data)"]
        
        subgraph CATALOG_SYS["📚 CATALOG SYSTEM"]
            direction TB
            CATALOG_DB["📚 Catalog<br/>━━━━━━━━<br/>DataHub/Atlan<br/>Unity Catalog"]
            LINEAGE_DB["🔗 Lineage<br/>━━━━━━━━<br/>Table → Table<br/>Column → Column"]
        end
        
        subgraph COMPUTE["⚙️ COMPUTE ENGINES"]
            direction LR
            DBX_ENG["⚡ Databricks<br/>━━━━━━━━━<br/>Spark clusters<br/>reads Iceberg"]
            SNOW_ENG["❄️ Snowflake<br/>━━━━━━━━━<br/>Virtual warehouses<br/>reads Iceberg"]
        end
        
        VPN["🔐 VPN / Direct Connect<br/>━━━━━━━━━━━━━━━━<br/>Secure tunnel"]
    end
    
    EDW_SYS -.->|"optional sync"| ONPREM_STORAGE
    APPS ==>|"CDC/Batch"| ONPREM_STORAGE
    DBS ==>|"CDC/Batch"| ONPREM_STORAGE
    
    ONPREM_STORAGE <===>|"read/write"| SPARK_ONPREM
    ONPREM_STORAGE <===>|"federated<br/>query"| TRINO
    
    ONPREM_STORAGE -.->|"optional<br/>replication"| CLOUD_STORAGE
    CLOUD_STORAGE <===>|"via VPN"| VPN
    
    META -.->|"points to"| MANIFEST
    MANIFEST -.->|"points to"| DATA
    
    ONPREM_STORAGE -.->|"registers tables"| CATALOG_DB
    CATALOG_DB -.->|"tracks"| LINEAGE_DB
    
    CLOUD_STORAGE <===>|"read/write<br/>via Iceberg API"| DBX_ENG
    CLOUD_STORAGE <===>|"read/write<br/>via Iceberg API"| SNOW_ENG
    
    TRINO <===>|"federated query<br/>via VPN"| DBX_ENG
    TRINO <===>|"federated query<br/>via VPN"| SNOW_ENG
    
    DBX_ENG -.->|"pushes metadata"| CATALOG_DB
    SNOW_ENG -.->|"pushes metadata"| CATALOG_DB
    SPARK_ONPREM -.->|"pushes metadata"| CATALOG_DB
    
    style ONPREM fill:#ffebee,stroke:#c62828,stroke-width:4px
    style CLOUD fill:#e8f5e9,stroke:#2e7d32,stroke-width:4px
    style ONPREM_STORAGE fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    style CLOUD_STORAGE fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style ICEBERG fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style CATALOG_SYS fill:#f3e5f5,stroke:#6a1b9a,stroke-width:3px
    style COMPUTE fill:#fff3e0,stroke:#e65100,stroke-width:3px
    style VPN fill:#fff,stroke:#000,stroke-width:3px
    style EDW_SYS fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
    style APPS fill:#fff,stroke:#000,stroke-width:2px
    style DBS fill:#fff,stroke:#000,stroke-width:2px
    style MINIO fill:#fff,stroke:#000,stroke-width:2px
    style SPARK_ONPREM fill:#fff,stroke:#000,stroke-width:2px
    style TRINO fill:#fff,stroke:#000,stroke-width:2px
    style META fill:#fff,stroke:#000,stroke-width:2px
    style MANIFEST fill:#fff,stroke:#000,stroke-width:2px
    style DATA fill:#fff,stroke:#000,stroke-width:2px
    style BRONZE_S fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style SILVER_S fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    style GOLD_S fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style CATALOG_DB fill:#fff,stroke:#000,stroke-width:2px
    style LINEAGE_DB fill:#fff,stroke:#000,stroke-width:2px
    style DBX_ENG fill:#fff,stroke:#000,stroke-width:2px
    style SNOW_ENG fill:#fff,stroke:#000,stroke-width:2px
</div>

**Key components explained:**

1. **On-prem object storage (Primary)**: MinIO/Ceph/Dell ECS as your lakehouse foundation
   - S3-compatible API (works with all modern tools)
   - Data stays on-prem (compliance, latency, governance)
   - Holds Bronze/Silver/Gold zones in Iceberg format

2. **Iceberg structure**:
   - **Metadata files**: Track table schema, snapshots, and versions
   - **Manifest files**: Point to actual data files (like an index)
   - **Data files**: Immutable Parquet files with the actual data

3. **On-prem Spark**: Transformations run on-prem, read/write Iceberg tables directly

4. **Trino/Presto (Federated Query)**: Query across on-prem and cloud seamlessly
   - Single SQL query can join on-prem Iceberg tables with cloud Snowflake tables
   - No data movement required
   - Users don't need to know where data lives

5. **Catalog**: Registers all tables (on-prem and cloud) and tracks lineage

6. **Cloud compute engines**: Databricks and Snowflake can read Iceberg tables (via replication or federated query)

7. **Optional cloud replication**: Replicate specific datasets to cloud for cloud-native workloads

**Why this works:**
- **Primary data stays on-prem** (compliance, cost, control)
- **Multiple engines can read it** (Spark, Trino, Snowflake, Databricks via Iceberg)
- **Federated query** eliminates need to copy data everywhere
- **Catalog knows about everything** (unified discovery across on-prem and cloud)
- **Gradual cloud adoption** (replicate only what needs to be in cloud)

---

### Layer C: Compute (Multi-Engine, Same Rules)

**Goal:** Allow Snowflake and Databricks to coexist without duplicated logic or governance

**Use each engine for what it's good at:**

| Engine | Best For | Why |
|--------|----------|-----|
| **Databricks** | Engineering, streaming, heavy transforms, ML/feature pipelines | Spark-native, notebooks, MLflow integration |
| **Snowflake** | SQL analytics, BI concurrency, governed marts, data sharing | Fast SQL, easy to use, great for BI tools |
| **On-prem CDP/Hadoop** | Legacy big data workloads, existing Spark jobs | Already exists, Spark/Hive workloads depend on it |
| **On-prem EDW** | Legacy structured workloads (finance, compliance) | Already exists, critical SQL reports depend on it |

**Important rule:** Avoid building *two different curated layers* (one in Snowflake and one in Databricks) that drift.

**Prefer:**
- Curate once in open format (Iceberg on on-prem object storage)
- Serve through either engine (via VPN or replication)
- Build engine-specific marts only when there's a strong reason (cost, performance, concurrency)

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TB
    subgraph ONPREM_COMP["🏢 ON-PREM"]
        CURATED["🥈 Curated Zone<br/>━━━━━━━━━━━━<br/>📊 Iceberg Tables<br/>🗄️ MinIO/Ceph/Dell ECS"]
        CDP_COMP["🐘<br/>CDP/Hadoop (Legacy)<br/>━━━━━━━━<br/>Spark/Hive jobs"]
        EDW["🏢<br/>EDW (Legacy)<br/>━━━━━━━━<br/>Finance"]
    end
    
    subgraph CLOUD_COMP["☁️ CLOUD"]
        DBX["⚡<br/>Databricks<br/>━━━━━━━━<br/>Heavy transforms<br/>+ ML"]
        SNOW["❄️<br/>Snowflake<br/>━━━━━━━━<br/>BI + Analytics"]
    end
    
    CURATED ==>|"📖 Read via VPN<br/>(Iceberg)"| DBX
    CURATED ==>|"📖 Read via VPN<br/>(Iceberg)"| SNOW
    CURATED -.->|"🔄 Optional sync"| CDP_COMP
    CURATED -.->|"🔄 Optional sync"| EDW
    
    DBX ==>|"✏️ Write"| DBX_MARTS["⚡ Databricks-specific<br/>━━━━━━━━━━━━━━<br/>ML Feature Store<br/>(Cloud)"]
    SNOW ==>|"✏️ Write"| SNOW_MARTS["❄️ Snowflake-specific<br/>━━━━━━━━━━━━━━<br/>BI Aggregates<br/>(Cloud)"]
    
    style ONPREM_COMP fill:#ffebee,stroke:#c62828,stroke-width:4px,stroke-dasharray: 5 5
    style CLOUD_COMP fill:#e8f5e9,stroke:#2e7d32,stroke-width:4px
    style CURATED fill:#bbdefb,stroke:#1565c0,stroke-width:4px
    style DBX fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style SNOW fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style CDP_COMP fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
    style EDW fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
    style DBX_MARTS fill:#fff,stroke:#000,stroke-width:2px
    style SNOW_MARTS fill:#fff,stroke:#000,stroke-width:2px
</div>

---

### Layer C+: Federated Query (Query Anywhere, Data Stays Put)

**Goal:** Query data across on-prem and cloud without moving it

> **The problem:** You have data in on-prem object storage (Iceberg), Snowflake, Databricks, and legacy EDW. Users need to join data across all of them. Copying data everywhere is expensive and slow.

**The solution:** Federated query engine (Trino or Presto)

**What is federated query?**

A single SQL query that can access multiple data sources simultaneously:

```sql
-- Query joins on-prem Iceberg table with cloud Snowflake table
-- No data movement required!

SELECT 
    o.order_id,
    o.amount,
    c.customer_name,
    c.segment
FROM onprem_lakehouse.gold.orders o
JOIN snowflake.analytics.customers c
    ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
```

**How it works:**

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart LR
    USER["👤 User<br/>━━━━━━<br/>SQL Query"]
    
    TRINO["🔍 Trino/Presto<br/>━━━━━━━━━━━<br/>Federated Query Engine"]
    
    ONPREM_LAKE["🏢 On-Prem<br/>Iceberg Tables<br/>━━━━━━━━━<br/>orders table"]
    
    SNOW["❄️ Snowflake<br/>━━━━━━━━━<br/>customers table"]
    
    DBX["⚡ Databricks<br/>━━━━━━━━━<br/>events table"]
    
    EDW["🏢 EDW<br/>━━━━━━━━━<br/>finance table"]
    
    USER ==>|"1. Submit query"| TRINO
    TRINO ==>|"2a. Fetch orders"| ONPREM_LAKE
    TRINO ==>|"2b. Fetch customers"| SNOW
    TRINO ==>|"2c. Fetch events"| DBX
    TRINO ==>|"2d. Fetch finance"| EDW
    TRINO ==>|"3. Join + return"| USER
    
    style USER fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style TRINO fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    style ONPREM_LAKE fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style SNOW fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style DBX fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style EDW fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
</div>

**Trino/Presto connectors:**

| Connector | What It Connects To |
|-----------|---------------------|
| **Iceberg** | On-prem object storage (MinIO/Ceph) with Iceberg tables |
| **Snowflake** | Snowflake tables (via JDBC) |
| **Delta Lake** | Databricks Delta tables |
| **Hive** | Legacy Hive tables on HDFS |
| **PostgreSQL/MySQL** | Operational databases |
| **MongoDB** | NoSQL databases |

**Real-world example:**

```
Business question: "What's the revenue by customer segment for Q1 2024?"

Data needed:
- Orders (on-prem Iceberg lakehouse)
- Customers (Snowflake)
- Product catalog (Databricks)
- Revenue adjustments (legacy EDW)

Traditional approach:
1. Copy orders to Snowflake (2 hours)
2. Copy product catalog to Snowflake (1 hour)
3. Copy revenue adjustments to Snowflake (30 min)
4. Run query in Snowflake
Total: 3.5 hours + storage costs

Federated query approach:
1. Run Trino query joining all 4 sources
Total: 5 minutes, no data movement
```

**When to use federated query:**

✅ **Use federated query when:**
- Ad-hoc analytics across multiple sources
- Exploratory data analysis
- One-time reports
- Data validation (comparing on-prem vs cloud)
- Low-latency requirements (< 1 minute)

❌ **Don't use federated query when:**
- High-frequency queries (> 100/sec)
- Complex aggregations on large datasets
- Production dashboards with strict SLAs
- → Instead: Replicate data to a single location and optimize there

**Deployment:**

```
On-Prem Trino Cluster:
- 1 coordinator node (query planning)
- 5-10 worker nodes (query execution)
- Connects to: on-prem Iceberg, Snowflake (via VPN), Databricks (via VPN), EDW

Cost: ~$50K-100K/year (hardware + maintenance)
Benefit: Query across all systems without data movement
```

---

### Layer D: Metadata, Catalog, and Discovery

**Goal:** One place to discover, understand, and trust data

> **Think of it like Google for your data.** Instead of asking "Does anyone know where the customer table is?", you search the catalog and find it in 10 seconds.

Your catalog experience should hold:

| Metadata Type | Example |
|---------------|---------|
| **Technical** | Schema: `{customer_id: int, email: string}`, Partitions: `date`, Format: Iceberg |
| **Business** | Domain: Customer, Owner: Customer Team, Glossary: "Active customer = purchased in last 90 days" |
| **Lineage** | `raw_orders` → `clean_orders` → `customer_360` → `revenue_dashboard` |
| **Quality** | Score: 95%, Last check: 2 hours ago, Issues: 3 null emails |
| **Access** | Tags: PII, Confidential, Policy: Mask email for non-finance users |

**Example catalog entry:**

```
Table: customer_360
Location: s3://lakehouse/gold/customer/customer_360/
Format: Iceberg
Owner: Customer Analytics Team
Domain: Customer
Tags: PII, Confidential
Quality Score: 98%

Schema:
  customer_id (int) - Primary key
  email (string) - PII, masked for non-finance
  lifetime_value (decimal) - Calculated monthly
  last_purchase_date (date)

Lineage:
  ← raw_customers (bronze)
  ← raw_orders (bronze)
  → revenue_dashboard (Tableau)
  → churn_model (Databricks ML)

Access:
  Finance team: Full access
  Marketing team: Email masked
  External contractors: No access
```

**This is the "unified layer" people feel daily.**

---

### Layer E: Governance and Security (Policy Everywhere)

**Goal:** Consistent access control across all stores/engines

> **The problem:** You set up masking in Snowflake, but forget to do it in Databricks. Now PII is leaking.

**The solution:** Central policy engine that enforces rules everywhere.

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TB
    POLICY["🎯 Policy Decision Point<br/>━━━━━━━━━━━━━━━<br/>🔒 Central Policy Engine<br/>OPA / Immuta / Privacera"]
    
    SNOW_PEP["❄️ Snowflake<br/>━━━━━━━━━<br/>🛡️ Policy Enforcement<br/>Masking + RBAC"]
    DBX_PEP["⚡ Databricks<br/>━━━━━━━━━<br/>🛡️ Policy Enforcement<br/>Dynamic Views"]
    EDW_PEP["🏢 EDW<br/>━━━━━━━━━<br/>🛡️ Policy Enforcement<br/>Row-level Security"]
    
    USER["👤 User<br/>━━━━━━━━━<br/>analyst@company.com"]
    
    USER ==>|"❶ Request:<br/>SELECT * FROM customers"| SNOW_PEP
    SNOW_PEP ==>|"❷ Check policy"| POLICY
    POLICY ==>|"❸ Decision:<br/>Mask email"| SNOW_PEP
    SNOW_PEP ==>|"❹ Return<br/>masked data"| USER
    
    POLICY -."enforces".-> DBX_PEP
    POLICY -."enforces".-> EDW_PEP
    
    style POLICY fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    style SNOW_PEP fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style DBX_PEP fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style EDW_PEP fill:#ffcdd2,stroke:#c62828,stroke-width:3px,stroke-dasharray: 5 5
    style USER fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
</div>

**Design around:**

- **Identity**: SSO + groups/roles (use existing AD/Okta)
- **Authorization**: RBAC + ABAC (tags like `PII`, `PCI`, `Confidential`)
- **Masking / row filtering**: Enforced centrally where possible
- **Key management**: Encryption at rest + in transit (CMK if needed)

**Example policy:**

```yaml
Policy: mask_customer_email
Applies to: Tables tagged with "PII"
Rule:
  - IF user.role IN ["Finance", "Legal"]
    THEN show full email
  - ELSE mask email (show first 3 chars + "***@***.com")
  
Enforcement:
  - Snowflake: Column masking policy
  - Databricks: Dynamic view with CASE statement
  - EDW: Row-level security view
```

**Best practice:** Use a **Policy Decision Point (PDP)** with engine-specific **Policy Enforcement Points (PEPs)**.

That's how you stop "Snowflake rules" and "Databricks rules" from drifting.

---

### Layer F: Data Product and Consumption

**Goal:** Stop everyone querying raw tables forever

> **Think of data products like APIs.** You don't give everyone direct database access. You publish well-defined products with contracts.

**Publish Data Products (domain-owned) with:**

- Contract + schema guarantees
- Documentation + examples
- Versioning + deprecation
- Access modes (SQL/BI, APIs, streaming topics)

**Example data product:**

```
Product: customer_360
Owner: Customer Analytics Team
Version: 2.1.0
SLA: Updated daily by 6 AM EST

Contract:
  - Schema: {customer_id, email, lifetime_value, segment, ...}
  - Freshness: < 24 hours
  - Quality: > 95% completeness
  - Breaking changes: 30-day deprecation notice

Access modes:
  - SQL: SELECT * FROM gold.customer_360
  - API: GET /api/v2/customers/{id}
  - Streaming: kafka://customer-updates

Documentation:
  - README: How to use this product
  - Examples: Common queries
  - Changelog: What changed in v2.1.0
```

**Add a semantic layer** for consistent metrics:

```
Metric: Revenue
Definition: SUM(order_amount) WHERE order_status = 'completed'
Owner: Finance Team
Used in: 47 dashboards

This ensures "Revenue" means the same thing everywhere.
```

**Consumption modes:**

- **BI/SQL**: Snowflake or SQL over lakehouse (Tableau, Looker, Power BI)
- **ML/features**: Databricks pipelines (feature engineering, model training)
- **Real-time services**: Streams + materialized views (fraud detection, recommendations)

---

### Layer G: Observability and Operations

**Goal:** Treat data pipelines like production software

> **If your website goes down, you get paged. If your data pipeline fails, you should also get paged.**

**Platform-wide monitoring:**

| What to Monitor | Example |
|-----------------|---------|
| **Pipeline health** | Latency: orders pipeline running 2 hours late ⚠️ |
| **Data quality** | Anomaly: customer count dropped 50% today 🚨 |
| **Cost** | Alert: Databricks spend up 200% this week 💰 |
| **SLAs** | Violation: customer_360 not updated in 36 hours ❌ |
| **Access** | Audit: user@external.com accessed PII table 🔒 |

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart LR
    PIPELINES["⚙️ Data Pipelines<br/>━━━━━━━━━━━<br/>Ingestion<br/>Transformation<br/>Publishing"]
    
    MONITOR["📊 Monitoring<br/>━━━━━━━━━<br/>Datadog/Grafana<br/>Latency + Errors"]
    QUALITY["✅ Quality Checks<br/>━━━━━━━━━━━<br/>Great Expectations<br/>Anomaly Detection"]
    COST["💰 Cost Tracking<br/>━━━━━━━━━━<br/>Per domain/product<br/>Budget alerts"]
    AUDIT["🔒 Audit Logs<br/>━━━━━━━━━<br/>Who accessed what<br/>Compliance"]
    
    PIPELINES ==> MONITOR
    PIPELINES ==> QUALITY
    PIPELINES ==> COST
    PIPELINES ==> AUDIT
    
    MONITOR ==>|"🚨 Alert"| ONCALL["👨‍🔧 On-call Engineer<br/>━━━━━━━━━━━━<br/>PagerDuty/Slack<br/>Runbooks"]
    QUALITY ==>|"🚨 Alert"| ONCALL
    COST ==>|"🚨 Alert"| ONCALL
    
    style PIPELINES fill:#e1f5fe,stroke:#01579b,stroke-width:4px
    style MONITOR fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style QUALITY fill:#bbdefb,stroke:#1565c0,stroke-width:3px
    style COST fill:#fff3e0,stroke:#e65100,stroke-width:3px
    style AUDIT fill:#f3e5f5,stroke:#6a1b9a,stroke-width:3px
    style ONCALL fill:#ffcdd2,stroke:#c62828,stroke-width:3px
</div>

**Example alert:**

```
🚨 ALERT: Data Quality Violation

Pipeline: customer_360_daily
Issue: NULL values in customer_id column
Impact: 1,247 rows affected (2.3% of total)
SLA: Quality threshold is 98%, currently at 97.7%

Action required:
1. Check upstream raw_customers table
2. Review data quality rules
3. Quarantine bad records

Runbook: https://wiki.company.com/data/runbooks/customer-360
On-call: @data-platform-oncall
```

---

## Concrete Enterprise Deployment Shape

### Control Plane (Unified Data Infra Layer)

This is what you build once and everyone uses:

- **Catalog + lineage + glossary** (e.g., DataHub, Atlan, Collibra)
- **Policy engine + RBAC/ABAC + masking** (e.g., Immuta, Privacera, Open Policy Agent)
- **Data contracts + schema registry** (e.g., Confluent Schema Registry, custom)
- **Quality framework + scorecards** (e.g., Great Expectations, Monte Carlo, Soda)
- **Orchestration standards** (e.g., Airflow, Prefect, Dagster)
- **Self-serve portal** (e.g., Backstage, custom)

### Data Plane (Where Data Lives)

This is where the actual data and compute happen:

**On-Prem:**
- **Object storage** (MinIO/Ceph/Dell ECS with Iceberg tables)
- **Spark** (transformations on-prem, can use CDP Spark)
- **CDP/Hadoop** (legacy EDL, gradual modernization)
- **EDW** (legacy, gradual modernization)

**Cloud:**
- **Databricks** (engineering + ML workloads)
- **Snowflake** (analytics marts + BI workloads)

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TB
    subgraph CONTROL["🎯 CONTROL PLANE"]
        direction LR
        CATALOG2["📚<br/>Catalog"]
        POLICY2["🔒<br/>Policy"]
        QUALITY2["✅<br/>Quality"]
        LINEAGE2["🔗<br/>Lineage"]
    end
    
    subgraph DATA["💾 DATA PLANE"]
        subgraph ONPREM_DEP["🏢 ON-PREM"]
            direction TB
            LAKE["🗄️ Object Storage<br/>━━━━━━━━━<br/>MinIO/Ceph + Iceberg<br/>🥉 🥈 🥇"]
            SPARK_DEP["⚡ Spark<br/>(CDP or standalone)<br/>Transformations"]
            CDP_DEP["🐘 CDP/Hadoop<br/>(Legacy EDL)"]
            EDW2["🏢 EDW<br/>(Legacy)"]
        end
        
        subgraph CLOUD_DEP["☁️ CLOUD"]
            direction TB
            DBX2["⚡<br/>Databricks"]
            SNOW2["❄️<br/>Snowflake"]
        end
    end
    
    CONTROL -."🔐 governs".-> ONPREM_DEP
    CONTROL -."🔐 governs".-> CLOUD_DEP
    
    LAKE <==> SPARK_DEP
    LAKE ==>|"read via VPN"| DBX2
    LAKE ==>|"read via VPN"| SNOW2
    LAKE -.->|"optional sync"| CDP_DEP
    LAKE -.->|"optional sync"| EDW2
    
    style CONTROL fill:#e3f2fd,stroke:#1565c0,stroke-width:4px
    style DATA fill:#fff8e1,stroke:#f57f17,stroke-width:4px
    style ONPREM_DEP fill:#ffebee,stroke:#c62828,stroke-width:3px,stroke-dasharray: 5 5
    style CLOUD_DEP fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style LAKE fill:#bbdefb,stroke:#1565c0,stroke-width:3px
    style SPARK_DEP fill:#fff,stroke:#000,stroke-width:2px
    style CDP_DEP fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
    style CATALOG2 fill:#fff,stroke:#000,stroke-width:2px
    style POLICY2 fill:#fff,stroke:#000,stroke-width:2px
    style QUALITY2 fill:#fff,stroke:#000,stroke-width:2px
    style LINEAGE2 fill:#fff,stroke:#000,stroke-width:2px
    style DBX2 fill:#fff,stroke:#000,stroke-width:2px
    style SNOW2 fill:#fff,stroke:#000,stroke-width:2px
    style EDW2 fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
</div>

---

## Implementation Strategy (Avoid a 2-Year Project)

> **Start small, deliver value quickly, expand incrementally.**

### Phase 1: Unify Discovery + Governance First (Months 1-3)

**Goal:** Give everyone one place to find and understand data

**What to build:**
- Deploy catalog tool (DataHub, Atlan, etc.)
- Register existing datasets (EDW, Snowflake, Databricks)
- Capture lineage for top 20 critical pipelines
- Define RBAC/ABAC tags (PII, Confidential, etc.)
- Set up data product registration process

**Success metrics:**
- 80% of datasets discoverable in catalog
- Lineage visible for critical pipelines
- Teams can request access via portal

**Effort:** 2-3 engineers, 3 months

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart LR
    CURRENT1["❌ Current State<br/>━━━━━━━━━━━<br/>🔴 Data scattered<br/>🔴 No discovery<br/>🔴 Manual lineage"]
    
    PHASE1["✅ Phase 1<br/>━━━━━━━━━━━<br/>🟢 Catalog deployed<br/>🟢 Lineage captured<br/>🟢 Access governed"]
    
    CURRENT1 ==>|"📅 3 months<br/>👥 2-3 engineers"| PHASE1
    
    style CURRENT1 fill:#ffcdd2,stroke:#c62828,stroke-width:4px,stroke-dasharray: 5 5
    style PHASE1 fill:#fff9c4,stroke:#f57f17,stroke-width:4px
</div>

---

### Phase 2: Unify the Curated Layer (Months 4-9)

**Goal:** One source of truth for curated data

**What to build:**
- Adopt Iceberg as platform standard
- Migrate top 10 curated datasets to Iceberg on S3
- Connect Snowflake to read Iceberg tables (external tables)
- Connect Databricks to read Iceberg tables (native)
- Deprecate duplicate curated tables

**Success metrics:**
- Top 10 datasets available in open format
- Both Snowflake and Databricks reading from same tables
- 50% reduction in duplicate datasets

**Effort:** 3-4 engineers, 6 months

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart LR
    PHASE1B["✅ Phase 1 Complete<br/>━━━━━━━━━━━━<br/>🟢 Catalog live<br/>🟢 Teams onboarded"]
    
    PHASE2["✅ Phase 2<br/>━━━━━━━━━━━<br/>🟢 Iceberg adopted<br/>🟢 Curated layer unified<br/>🟢 Duplicates removed"]
    
    PHASE1B ==>|"📅 6 months<br/>👥 3-4 engineers"| PHASE2
    
    style PHASE1B fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    style PHASE2 fill:#bbdefb,stroke:#1565c0,stroke-width:4px
</div>

---

### Phase 3: Modernize EDW Usage (Months 10-18)

**Goal:** Reduce EDW dependency, move workloads to lakehouse

**What to build:**
- Identify EDW workloads that can move to lakehouse
- Migrate non-critical reports to Snowflake/Databricks
- Keep critical finance/compliance workloads on EDW
- Set up bi-directional sync (EDW ↔ Lakehouse)

**Success metrics:**
- 30% of EDW workloads migrated
- EDW costs reduced by 20%
- Critical workloads still running on EDW

**Effort:** 4-5 engineers, 9 months

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart LR
    PHASE2B["✅ Phase 2 Complete<br/>━━━━━━━━━━━━<br/>🟢 Unified curated layer<br/>🟢 Multi-engine access"]
    
    PHASE3["✅ Phase 3<br/>━━━━━━━━━━━<br/>🟢 EDW modernized<br/>🟢 Workloads migrated<br/>🟢 Costs reduced 20%"]
    
    PHASE2B ==>|"📅 9 months<br/>👥 4-5 engineers"| PHASE3
    
    style PHASE2B fill:#bbdefb,stroke:#1565c0,stroke-width:4px
    style PHASE3 fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px
</div>

---

## EDW Migration Strategies: How to Retire Your Legacy Platform

> **The goal is not to replace the EDW overnight. The goal is to gradually reduce dependency until you can retire it safely.**

### Critical Principle: Invert the Dependency

**The biggest mistake:** Building your new modern system (DataHub, Snowflake, Databricks) that depends on the old EDW for data.

```
❌ WRONG: New system depends on old system

Sources → EDW (old) → Lakehouse (new) → Snowflake/Databricks
                ↓
         DataHub catalogs EDW tables

Problem: You can NEVER retire the EDW because everything depends on it.
```

**The right approach:** Invert the dependency. Make the lakehouse the source of truth, and let the EDW sync FROM the lakehouse if needed.

```
✅ RIGHT: Old system depends on new system (or coexists independently)

Sources → Lakehouse (new) → Snowflake/Databricks
            ↓                     ↓
         DataHub            (Optional: EDW syncs FROM lakehouse
         catalogs           for legacy reports that can't move yet)
         lakehouse
         
Result: You CAN retire the EDW when legacy reports are migrated.
```

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'12px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TB
    subgraph WRONG["❌ WRONG ARCHITECTURE"]
        direction TB
        SRC1["📊 Sources"]
        EDW_OLD["🏢 EDW (Old)<br/>━━━━━━━━━<br/>System of Record"]
        LAKE_WRONG["☁️ Lakehouse (New)<br/>━━━━━━━━━<br/>Depends on EDW"]
        
        SRC1 --> EDW_OLD
        EDW_OLD --> LAKE_WRONG
    end
    
    subgraph RIGHT["✅ RIGHT ARCHITECTURE"]
        direction TB
        SRC2["📊 Sources"]
        LAKE_RIGHT["☁️ Lakehouse (New)<br/>━━━━━━━━━<br/>System of Record"]
        EDW_NEW["🏢 EDW (Old)<br/>━━━━━━━━━<br/>Syncs FROM lakehouse<br/>(optional, temporary)"]
        
        SRC2 --> LAKE_RIGHT
        LAKE_RIGHT -.->|"optional sync"| EDW_NEW
    end
    
    style WRONG fill:#ffcdd2,stroke:#c62828,stroke-width:4px
    style RIGHT fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px
    style EDW_OLD fill:#fff,stroke:#000,stroke-width:2px
    style LAKE_WRONG fill:#fff,stroke:#000,stroke-width:2px
    style SRC1 fill:#fff,stroke:#000,stroke-width:2px
    style EDW_NEW fill:#fff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5
    style LAKE_RIGHT fill:#fff,stroke:#000,stroke-width:2px
    style SRC2 fill:#fff,stroke:#000,stroke-width:2px
</div>

**How to implement this:**

1. **Replicate sources directly to lakehouse** (not through EDW)
   - Set up CDC from source databases → Lakehouse Bronze
   - Bypass the EDW entirely for new data flows

2. **Build curated layers in lakehouse** (not in EDW)
   - Transform Bronze → Silver → Gold in Databricks/Spark
   - Store as Iceberg tables in object storage

3. **Catalog the lakehouse** (not the EDW)
   - DataHub/Atlan catalogs lakehouse tables
   - EDW tables are NOT in the catalog (they're legacy)

4. **Optional: Sync lakehouse → EDW** (temporary, for legacy reports)
   - If you have critical reports that can't move yet
   - Reverse ETL: Push curated data FROM lakehouse TO EDW
   - This keeps EDW alive temporarily, but it's now a downstream consumer

5. **Retire EDW when ready**
   - Once all reports migrate off EDW
   - Stop the reverse ETL sync
   - Decommission the EDW

**Key insight:** The new system must be the source of truth from day one. The old system can consume from the new system temporarily, but never the other way around.

---

### The Three Migration Strategies

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'13px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TB
    START["🏢 Legacy EDW<br/>━━━━━━━━━━━<br/>All workloads<br/>on-prem"]
    
    ASSESS["📊 Assess Workloads<br/>━━━━━━━━━━━━━<br/>Categorize by:<br/>• Criticality<br/>• Complexity<br/>• Dependencies"]
    
    STRATEGY1["🟢 Strategy 1:<br/>COEXIST<br/>━━━━━━━━━━━<br/>Keep EDW for critical<br/>Sync to lakehouse<br/>New work in cloud"]
    
    STRATEGY2["🟡 Strategy 2:<br/>GRADUAL SUNSET<br/>━━━━━━━━━━━<br/>Migrate workloads<br/>in waves<br/>Retire EDW in 18-24mo"]
    
    STRATEGY3["🔴 Strategy 3:<br/>FULL REPLACEMENT<br/>━━━━━━━━━━━<br/>Rebuild everything<br/>in cloud<br/>High risk, high cost"]
    
    START ==> ASSESS
    ASSESS ==> STRATEGY1
    ASSESS ==> STRATEGY2
    ASSESS ==> STRATEGY3
    
    style START fill:#ffcdd2,stroke:#c62828,stroke-width:4px,stroke-dasharray: 5 5
    style ASSESS fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    style STRATEGY1 fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px
    style STRATEGY2 fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    style STRATEGY3 fill:#ffcdd2,stroke:#c62828,stroke-width:4px
</div>

### Strategy 1: Coexist (Recommended for Most)

**When to use:** You have critical workloads that can't move, but want to stop growing EDW footprint.

**Approach:**
- Keep EDW for critical finance/compliance workloads
- Set up bi-directional sync (EDW ↔ Lakehouse)
- Route all new workloads to cloud (Snowflake/Databricks)
- Gradually migrate non-critical workloads when safe

**Timeline:** Indefinite coexistence, EDW becomes smaller over time

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'12px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart LR
    subgraph YEAR0["📅 Year 0: Current State"]
        EDW0["🏢 EDW<br/>━━━━━━<br/>100% workloads<br/>$500K/year"]
    end
    
    subgraph YEAR1["📅 Year 1: Coexist"]
        EDW1["🏢 EDW<br/>━━━━━━<br/>60% workloads<br/>$400K/year"]
        CLOUD1["☁️ Cloud<br/>━━━━━━<br/>40% workloads<br/>$200K/year"]
    end
    
    subgraph YEAR2["📅 Year 2: Steady State"]
        EDW2["🏢 EDW<br/>━━━━━━<br/>30% workloads<br/>$250K/year"]
        CLOUD2["☁️ Cloud<br/>━━━━━━<br/>70% workloads<br/>$400K/year"]
    end
    
    YEAR0 ==> YEAR1
    YEAR1 ==> YEAR2
    
    style YEAR0 fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style YEAR1 fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style YEAR2 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style EDW0 fill:#fff,stroke:#000,stroke-width:2px
    style EDW1 fill:#fff,stroke:#000,stroke-width:2px
    style EDW2 fill:#fff,stroke:#000,stroke-width:2px
    style CLOUD1 fill:#fff,stroke:#000,stroke-width:2px
    style CLOUD2 fill:#fff,stroke:#000,stroke-width:2px
</div>

**Pros:**
- ✅ Low risk (critical workloads stay put)
- ✅ Gradual cost reduction
- ✅ Teams learn cloud at their own pace

**Cons:**
- ❌ Maintain two systems indefinitely
- ❌ Sync complexity
- ❌ EDW costs never go to zero

---

### Strategy 2: Gradual Sunset (Aggressive Modernization)

**When to use:** You have executive buy-in to retire EDW completely in 18-24 months.

**Critical principle: Don't modernize what you're retiring**

```
❌ WRONG: Modernize EDW pipelines before migrating

"Let's refactor this 10-year-old ETL job in the EDW first,
then migrate it to Databricks"

Problem: You spend 3 months modernizing code you'll throw away.
No business value. Wasted effort.
```

```
✅ RIGHT: Freeze EDW, rebuild in new platform

"Leave the old ETL job as-is. Build the new version directly
in Databricks with modern patterns. Run parallel. Cut over. 
Decommission old."

Result: You only invest in the new platform. Business gets
modern pipeline immediately.
```

**The EDW is frozen, not modernized:**
- **No new features** in EDW pipelines (they're being retired)
- **No refactoring** of EDW code (it's legacy, leave it alone)
- **Only bug fixes** if critical (minimal investment)
- **All new work** goes to lakehouse/Snowflake/Databricks

**Approach:**
- Categorize all EDW workloads (critical → nice-to-have)
- **Rebuild** (not refactor) in waves (easiest first, critical last)
- Set hard deadline to decommission EDW
- Allocate dedicated migration team
- **Freeze EDW development** (no new features, only critical fixes)

**Timeline:** 18-24 months to full retirement

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'12px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TB
    subgraph WAVE1["🌊 Wave 1 (Months 1-6)<br/>Low-hanging fruit"]
        W1_ITEMS["📊 Reports (non-critical)<br/>🔄 ETL jobs (simple)<br/>📈 Dashboards (BI)"]
    end
    
    subgraph WAVE2["🌊 Wave 2 (Months 7-12)<br/>Medium complexity"]
        W2_ITEMS["📊 Operational reports<br/>🔄 Complex ETL<br/>🗄️ Data marts"]
    end
    
    subgraph WAVE3["🌊 Wave 3 (Months 13-18)<br/>Critical workloads"]
        W3_ITEMS["💰 Finance reports<br/>📋 Compliance<br/>🏛️ Regulatory"]
    end
    
    subgraph FINAL["✅ Month 18-24<br/>Decommission"]
        RETIRE["🏢 EDW Retired<br/>━━━━━━━━━━<br/>Hardware returned<br/>Licenses cancelled<br/>Team reassigned"]
    end
    
    WAVE1 ==> WAVE2
    WAVE2 ==> WAVE3
    WAVE3 ==> FINAL
    
    style WAVE1 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style WAVE2 fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style WAVE3 fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style FINAL fill:#bbdefb,stroke:#1565c0,stroke-width:4px
    style W1_ITEMS fill:#fff,stroke:#000,stroke-width:2px
    style W2_ITEMS fill:#fff,stroke:#000,stroke-width:2px
    style W3_ITEMS fill:#fff,stroke:#000,stroke-width:2px
    style RETIRE fill:#fff,stroke:#000,stroke-width:2px
</div>

**Pros:**
- ✅ Clear end date
- ✅ Full cost elimination
- ✅ Forces modernization

**Cons:**
- ❌ High risk if timeline slips
- ❌ Requires significant investment
- ❌ Business disruption

---

### Strategy 3: Full Replacement (Not Recommended)

**When to use:** Rarely. Only if EDW is completely broken or vendor is EOL.

**Approach:**
- Rebuild everything in cloud from scratch
- Big-bang cutover
- High risk, high cost

**We don't recommend this.** Use Strategy 1 or 2 instead.

---

### Workload Migration Decision Framework

Use this framework to decide which workloads to migrate first:

<div class="mermaid">
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fff','primaryTextColor':'#000','primaryBorderColor':'#000','lineColor':'#000','fontSize':'12px','fontFamily':'Comic Sans MS, cursive'}}}%%
flowchart TD
    START["🔍 Evaluate Workload"]
    
    CRITICAL{"❓ Business Critical?<br/>(Finance, Compliance,<br/>Regulatory)"}
    
    COMPLEX{"❓ High Complexity?<br/>(Many dependencies,<br/>custom code)"}
    
    USAGE{"❓ High Usage?<br/>(Daily users,<br/>SLA requirements)"}
    
    MIGRATE_LAST["🔴 MIGRATE LAST<br/>━━━━━━━━━━━<br/>Keep on EDW<br/>until Wave 3"]
    
    MIGRATE_MID["🟡 MIGRATE MID<br/>━━━━━━━━━━━<br/>Wave 2<br/>Months 7-12"]
    
    MIGRATE_FIRST["🟢 MIGRATE FIRST<br/>━━━━━━━━━━━<br/>Wave 1<br/>Quick wins"]
    
    START --> CRITICAL
    CRITICAL -->|Yes| MIGRATE_LAST
    CRITICAL -->|No| COMPLEX
    COMPLEX -->|Yes| MIGRATE_MID
    COMPLEX -->|No| USAGE
    USAGE -->|High| MIGRATE_MID
    USAGE -->|Low| MIGRATE_FIRST
    
    style START fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style CRITICAL fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style COMPLEX fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style USAGE fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style MIGRATE_LAST fill:#ffcdd2,stroke:#c62828,stroke-width:4px
    style MIGRATE_MID fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    style MIGRATE_FIRST fill:#c8e6c9,stroke:#2e7d32,stroke-width:4px
</div>

---

### Practical Migration Patterns

#### Pattern 1: Report Migration

```
EDW Report → Snowflake Report

Steps:
1. Identify source tables in EDW
2. Replicate tables to lakehouse (CDC or batch)
3. Rebuild report logic in Snowflake SQL
4. Run parallel (EDW + Snowflake) for 2-4 weeks
5. Validate numbers match
6. Cut over to Snowflake
7. Decommission EDW report

Timeline: 2-4 weeks per report
Risk: Low
```

#### Pattern 2: ETL Pipeline Migration

```
EDW ETL → Databricks Pipeline

Steps:
1. Document current ETL logic
2. Identify source systems
3. Set up CDC/streaming ingestion to lakehouse
4. Rebuild transformation logic in Spark
5. Run parallel pipelines
6. Validate data quality
7. Cut over to Databricks
8. Decommission EDW ETL

Timeline: 4-8 weeks per pipeline
Risk: Medium
```

#### Pattern 3: Data Mart Migration

```
EDW Mart → Lakehouse Gold Zone

Steps:
1. Understand mart schema and business logic
2. Migrate source data to lakehouse Silver zone
3. Rebuild mart as Iceberg tables in Gold zone
4. Create external tables in Snowflake (for BI access)
5. Migrate downstream reports one by one
6. Validate with business users
7. Decommission EDW mart

Timeline: 2-3 months per mart
Risk: Medium-High
```

---

### Cost Comparison: EDW vs Cloud

| Item | On-Prem EDW | Cloud (Snowflake + Databricks) |
|------|-------------|-------------------------------|
| **Hardware** | $200K-500K/year (depreciation) | $0 (pay-as-you-go) |
| **Licenses** | $300K-800K/year | $200K-600K/year (usage-based) |
| **Storage** | $50K-100K/year | $10K-30K/year (object storage) |
| **Maintenance** | 3-5 FTEs ($300K-500K/year) | 1-2 FTEs ($100K-200K/year) |
| **Scaling** | Requires hardware purchase (6-12 months lead time) | Instant (scale up/down in minutes) |
| **Total** | $850K-1.9M/year | $310K-830K/year |

**Typical savings: 40-60% after full migration**

---

## Common Traps to Avoid

### Trap 1: Building Two Curated Layers

```
❌ Bad:
Databricks: silver.customers (version A)
Snowflake: silver.customers (version B)
Result: They drift, teams confused

✅ Good:
Lakehouse: silver.customers (Iceberg)
Databricks: reads from lakehouse
Snowflake: reads from lakehouse
Result: One source of truth
```

### Trap 2: No Data Product Ownership

```
❌ Bad:
Platform team owns all data products
Result: Bottleneck, slow delivery

✅ Good:
Domain teams own their products
Platform team provides tools + standards
Result: Scalable, fast delivery
```

### Trap 3: Governance as Documentation Only

```
❌ Bad:
Policy: "Don't share PII"
Enforcement: Trust developers to follow it
Result: PII leaks happen

✅ Good:
Policy: "Don't share PII"
Enforcement: Automated masking in catalog
Result: Impossible to leak PII
```

### Trap 4: Ad-Hoc Ingestion

```
❌ Bad:
Every team builds custom ingestion scripts
Result: No standards, maintenance nightmare

✅ Good:
Standard ingestion framework with contracts
Result: Reusable, maintainable, governed
```

---

## Summary: The North Star

> **Create one logical platform, not one physical system.**

You can keep multiple engines (on-prem EDW, Snowflake, Databricks). What makes it feel like "one platform" is that you standardize:

- **How data lands** (ingestion contracts)
- **How it's stored** (one open table format + consistent zones)
- **How it's governed** (one catalog + one policy model)
- **How it's observed** (lineage + data quality)
- **How it's consumed** (semantic layer + APIs)

If you do *just that*, you can modernize without a big-bang migration.

---

## Two Questions to Tailor This to Your Environment

1. **Are you aiming for Iceberg as the common table format, or are you already standardized on Delta somewhere?**
   
   If you're already deep into Delta Lake (Databricks-native), you might stick with Delta. But if you want true multi-engine interoperability (Snowflake + Databricks + Trino), Iceberg is the better choice.

2. **Is the "CDP" (EDL) mainly a customer-event platform (streaming + identity), or a data lake landing zone?**
   
   If it's event-focused (Segment, mParticle style), treat it as a streaming source. If it's a landing zone, treat it as Bronze storage.
