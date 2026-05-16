---
title: "Building a Modern Containerized Open Data Stack"
category: Data
tags:
  - data-architecture
  - data-platform
  - iceberg
  - kubernetes
  - lakehouse
  - hybrid-cloud
  - ai
summary: A practical architecture guide for hybrid data platforms in the AI era — separating storage and compute, embracing open table formats, and building portable governed ecosystems.
---

# Building a Modern Containerized Open Data Stack

## A practical architecture guide for hybrid data platforms in the AI era

For many years, enterprises bought large data platforms the same way they bought ERP systems.

One vendor.
One platform.
One ecosystem.

The promise was simple:

> "Put all your data here and we will handle everything."

And honestly, this worked for a long time.

But modern data workloads changed the entire equation.

Today organizations are dealing with:

- Batch pipelines
- Real-time streaming
- AI workloads
- GPU clusters
- Data science notebooks
- Developer local analytics
- Multi-cloud deployments
- Regulatory restrictions
- Cross-region architectures
- Unstructured data
- Edge computing

Suddenly the old idea of one centralized platform controlling everything starts breaking down.

**Not because the vendors failed.**

**But because the architecture itself changed.**

This article is not about attacking SaaS platforms. This is about understanding how modern open architectures work technically, what challenges they introduce, and how organizations can solve them step by step.

---

## The biggest mindset shift happening right now

In older Hadoop architectures, storage and compute were tightly connected.

HDFS stored data inside cluster nodes. Spark and MapReduce jobs tried to run near the data.

The philosophy was: **"Move compute to data."**

This was necessary because networks were slower and storage was local.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    subgraph OLD["<b>Old: Hadoop Era</b>"]
        N1["<b>Node 1</b><br/>HDFS + Spark"]
        N2["<b>Node 2</b><br/>HDFS + Spark"]
        N3["<b>Node 3</b><br/>HDFS + Spark"]
        N1 --- N2 --- N3
    end
    subgraph NEW["<b>New: Open Era</b>"]
        S["<b>Shared Object Storage</b><br/>S3 / ADLS / GCS / MinIO"]
        C1["<b>Spark</b><br/>(ephemeral)"]
        C2["<b>Trino</b><br/>(ephemeral)"]
        C3["<b>DuckDB</b><br/>(local)"]
        C4["<b>GPU / AI</b><br/>(ephemeral)"]
        C1 --> S
        C2 --> S
        C3 --> S
        C4 --> S
    end
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef darkgray fill:#bdbdbd,stroke:#222,stroke-width:2px,color:#000
    class N1,N2,N3,C1,C2,C3,C4 gray
    class S darkgray
    style OLD fill:#f5f5f5,stroke:#666,stroke-width:1.5px,color:#111
    style NEW fill:#f5f5f5,stroke:#666,stroke-width:1.5px,color:#111
</div>

But modern architectures work differently. Today storage is mostly object storage:

- S3
- ADLS
- GCS
- MinIO
- Ceph
- Pure Storage FlashBlade

Compute is now temporary and portable.

- Spark clusters can start and stop dynamically
- Trino can run in Kubernetes
- DuckDB can run on laptops
- AI workloads may run in GPU clusters in another cloud

Now the architecture becomes: **"Shared storage + independent compute."**

This sounds simple. But it changes everything technically.

---

## The new foundation: object storage

Modern architectures start with **object storage**.

Not compute. Not warehouses. Not databases.

**Storage becomes the foundation layer.**

Why? Because object storage solves several difficult problems:

- Cheap scaling
- High durability
- Cloud independence
- Container compatibility
- Easy replication
- Separation from compute

This allows organizations to store data **once** and use **many** compute engines on top of it.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    S["<b>Object Storage</b><br/>Single Source of Truth"]
    S --> A["<b>Spark</b><br/>ETL Pipelines"]
    S --> B["<b>Trino</b><br/>SQL Analytics"]
    S --> C["<b>dbt</b><br/>Transformations"]
    S --> D["<b>DuckDB</b><br/>Local Analytics"]
    S --> E["<b>AI Pipelines</b><br/>Embeddings &amp; Inference"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    class A,B,C,D,E gray
    style S fill:#9e9e9e,stroke:#111,stroke-width:3px,color:#000
</div>

All reading the **same data**. Without copying it everywhere.

That is a huge architectural shift.

---

## Why Apache Iceberg becomes important

Raw parquet files alone are not enough for enterprise systems. You eventually hit problems like:

- Concurrent writes
- Schema changes
- Broken partitions
- Streaming consistency
- Rollback requirements
- Time travel needs

This is where open table formats like **Apache Iceberg** become critical.

Iceberg adds a metadata layer on top of object storage.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    Q["<b>Query Engines</b><br/>Spark / Trino / Flink / DuckDB"]
    Q --> M["<b>Iceberg Metadata Layer</b><br/>ACID • Snapshots • Schema Evolution<br/>Time Travel • Streaming"]
    M --> P["<b>Parquet Files in Object Storage</b>"]
    style Q fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    style M fill:#9e9e9e,stroke:#111,stroke-width:2.5px,color:#000
    style P fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
</div>

Now the platform gains:

- **ACID transactions**
- **Snapshot isolation**
- **Schema evolution**
- **Partition evolution**
- **Versioning**
- **Time travel**
- **Streaming support**

The important part is this: **Iceberg is not tied to one compute engine.**

That changes the economics of the platform. You no longer need separate storage systems for every tool. **One shared data layer becomes possible.**

---

## The catalog layer becomes the real brain

Most people think the catalog is just metadata. That is no longer true.

In modern architectures, the catalog becomes the **control plane**.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    CAT["<b>Catalog Layer</b><br/>(The Operating System)"]
    CAT --> AUTH["<b>Authentication</b>"]
    CAT --> RBAC["<b>RBAC</b>"]
    CAT --> LIN["<b>Lineage</b>"]
    CAT --> POL["<b>Policies</b>"]
    CAT --> OWN["<b>Ownership</b>"]
    CAT --> DISC["<b>Discovery</b>"]
    CAT --> AUD["<b>Auditability</b>"]
    CAT --> GOV["<b>Governance</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    class AUTH,RBAC,LIN,POL,OWN,DISC,AUD,GOV gray
    style CAT fill:#757575,stroke:#000,stroke-width:3px,color:#fff
</div>

This layer becomes extremely important in **AI environments** — because AI systems need controlled access to trusted data. **Without governance, AI systems become dangerous very quickly.**

This is why many organizations are investing heavily in:

- Iceberg REST catalogs
- Apache Gravitino
- Polaris
- Custom governance APIs

The catalog is becoming the **operating system of the data platform**.

---

## The real technical challenge: networking

This is the part many non-technical discussions completely ignore.

Once compute and storage become separated, **the network becomes the backbone of the architecture.**

In Hadoop systems, local disks handled most operations. In modern architectures, **everything moves through the network**:

- Object storage reads
- Shuffle operations
- Metadata calls
- Cross-region replication
- AI inference traffic
- Streaming pipelines
- Federated queries

Network design directly impacts:

- Performance
- Latency
- Cost
- Scalability
- Reliability

**This is why modern architectures require much better network planning than older systems.**

---

## Common network challenges

### 1. Cross-region traffic cost

Many cloud providers charge heavily for data movement between regions.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    subgraph R1["<b>Region A</b>"]
        C["<b>Compute</b>"]
    end
    subgraph R2["<b>Region B</b>"]
        S["<b>Storage</b>"]
    end
    C -.->|"<b>$$$ Egress</b><br/>Every query"| S
    style C fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    style S fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    style R1 fill:#f5f5f5,stroke:#666,color:#111
    style R2 fill:#f5f5f5,stroke:#666,color:#111
</div>

**Solution:** Keep compute close to storage whenever possible.

- Regional compute placement
- Local caching layers
- Data locality strategies
- Workload-aware routing

### 2. Object storage latency

Object storage is **not** local disk. Small file reads create latency problems. Millions of tiny parquet files can destroy performance.

**Solution:** Good file management.

- Compaction
- Partition optimization
- Iceberg metadata pruning
- Large optimized parquet files
- Z-ordering or clustering

This is one reason modern data engineering spends so much effort on table optimization.

### 3. Distributed shuffle bottlenecks

Large Spark joins move huge amounts of data across the network. Poor network design creates bottlenecks very quickly.

**Solution:** Use distributed compute only where necessary.

This is why engines like **DuckDB** and **Polars** became important. Not every workload needs a giant cluster. Sometimes local execution is faster and cheaper.

Modern architecture is becoming **workload-aware** instead of blindly distributed.

### 4. AI workload pressure

AI pipelines create new challenges:

- Training data movement
- Embedding pipelines
- Vector indexing
- GPU data loading

GPU clusters are **extremely sensitive to network throughput**. Slow storage pipelines can leave expensive GPUs sitting idle.

**Solution:** Modern AI architectures increasingly use:

- High-bandwidth networking
- RDMA
- InfiniBand
- NVMe over Fabric
- Smart caching layers
- GPU-aware storage placement

The AI era is pushing infrastructure design far beyond traditional analytics systems.

---

## Why Kubernetes changes the operating model

Container orchestration platforms like **Kubernetes** and **OpenShift** are becoming central to modern data systems.

Why? Because **compute becomes temporary**.

Instead of maintaining large permanent clusters:

- Start Spark only when needed
- Start Trino dynamically
- Run dbt pipelines temporarily
- Scale AI inference independently
- Deploy workloads closer to users

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    K["<b>Kubernetes / OpenShift</b>"]
    K --> SP["<b>Spark Job</b><br/>(spins up &amp; tears down)"]
    K --> TR["<b>Trino Cluster</b><br/>(autoscales)"]
    K --> DBT["<b>dbt Run</b><br/>(temporary pod)"]
    K --> AI["<b>AI Inference</b><br/>(scales independently)"]
    K --> ENV["<b>Same Manifests</b>"]
    ENV --> ON["<b>On-Prem</b>"]
    ENV --> AWS["<b>AWS</b>"]
    ENV --> AZ["<b>Azure</b>"]
    ENV --> GCP["<b>GCP</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class SP,TR,DBT,AI gray
    class ON,AWS,AZ,GCP gray
    class ENV midgray
    style K fill:#757575,stroke:#000,stroke-width:2.5px,color:#fff
</div>

This reduces infrastructure waste. It also creates **portability**.

The same architecture can run on-prem, AWS, Azure, or Google Cloud. That portability becomes **strategically important**.

---

## The rise of hybrid architecture

Most enterprises are now hybrid — whether they planned for it or not.

- Some systems remain on-prem because of regulation
- Some workloads run in cloud because of elasticity
- Some AI systems need specialized GPU providers
- Some analytics workloads require local execution

A containerized open architecture allows all these environments to work together.

This is one of the biggest reasons enterprises are moving toward **open table formats** and **portable compute**.

---

## Why single-node computing is making a comeback

One of the most fascinating shifts today is the return of powerful **single-node analytics**.

For years the industry believed everything needed distributed clusters. But modern hardware changed the equation.

Today: **DuckDB, Polars, Arrow, modern CPUs, large memory systems** allow many analytics workloads to run locally with incredible performance.

This reduces:

- Network movement
- Cluster overhead
- Infrastructure complexity
- Operational cost

Sometimes one optimized node outperforms badly tuned distributed systems.

This is why the future is probably **not** "everything distributed."

The future is: **"Use the right compute model for the workload."**

---

## A practical modern architecture

A modern open data stack often looks like this:

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    subgraph AI["<b>AI Layer</b>"]
        V["<b>Vector Pipelines</b>"]
        E["<b>Embedding Services</b>"]
        G["<b>GPU Clusters</b>"]
        AG["<b>AI Agents</b>"]
    end
    subgraph ORCH["<b>Orchestration Layer</b>"]
        K8S["<b>Kubernetes / OpenShift</b>"]
        AF["<b>Airflow / Temporal</b>"]
    end
    subgraph COMP["<b>Compute Layer</b>"]
        SP["<b>Spark</b>"]
        TR["<b>Trino</b>"]
        FL["<b>Flink</b>"]
        DUCK["<b>DuckDB / Polars</b>"]
        DBT["<b>dbt</b>"]
    end
    subgraph CAT["<b>Catalog Layer</b>"]
        REST["<b>Iceberg REST</b>"]
        GRAV["<b>Gravitino / Polaris</b>"]
        RBAC["<b>RBAC &amp; Governance APIs</b>"]
    end
    subgraph TBL["<b>Open Table Format</b>"]
        ICE["<b>Apache Iceberg</b>"]
    end
    subgraph STO["<b>Storage Layer</b>"]
        OBJ["<b>S3 / ADLS / GCS / MinIO / Ceph</b>"]
    end
    AI --> ORCH
    ORCH --> COMP
    COMP --> CAT
    CAT --> TBL
    TBL --> STO
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    class V,E,G,AG,K8S,AF,SP,TR,FL,DUCK,DBT,REST,GRAV,RBAC,ICE,OBJ gray
    style AI fill:#fafafa,stroke:#555,stroke-width:1.5px,color:#111
    style ORCH fill:#f0f0f0,stroke:#555,stroke-width:1.5px,color:#111
    style COMP fill:#e0e0e0,stroke:#444,stroke-width:1.5px,color:#111
    style CAT fill:#cccccc,stroke:#333,stroke-width:1.5px,color:#111
    style TBL fill:#b0b0b0,stroke:#222,stroke-width:1.5px,color:#000
    style STO fill:#909090,stroke:#000,stroke-width:2px,color:#000
</div>

All connected through **open standards** instead of vendor-specific storage engines.

---

## The hardest part is not technology

Ironically, the hardest challenge is usually not technical.

It is **operational maturity**.

Open architectures require:

- Strong governance
- Good engineering practices
- Platform thinking
- Cost awareness
- Network planning
- Observability
- Automation

**Without discipline, open architectures can become chaos.**

But when designed correctly, they create something extremely powerful:

### Freedom.

- Freedom to move workloads
- Freedom to adopt new technologies
- Freedom to optimize cost
- Freedom to avoid platform dependency

And in the AI era, that flexibility may become one of the most valuable capabilities an organization can have.

The future may not belong to the biggest closed platform.

It may belong to organizations that understand how to build **portable, governed, network-aware, containerized open data ecosystems**.
