---
title: "Case Study: How Netflix Solved the 100 Petabyte Problem with Apache Iceberg"
category: Case Studies
tags:
  - case-study
  - netflix
  - iceberg
  - data-lake
  - hive
  - s3
  - data-architecture
summary: A deep look at why Netflix's data platform engineers had to invent a new table format - and how Iceberg's three core ideas (file-level tracking, snapshot metadata, and atomic commits) replaced two decades of Hive assumptions.
date: 2025-06-23
---

# Case Study: How Netflix Solved the 100 Petabyte Problem with Apache Iceberg

> **Context:** This case study examines the engineering story behind Apache Iceberg — why Netflix built it, what specifically broke at scale, and what the design teaches us about modern data platforms. It is based on publicly available talks, blog posts, and conference materials from Ryan Blue, Daniel Weeks, and the Netflix data team.

---

## The Setup: A Streaming Giant Outgrowing Its Tools

By 2017, Netflix was no longer "a streaming company that does some analytics." It was a **data company that happened to stream movies**.

Every play, pause, search, recommendation refresh, A/B test exposure, encoder run, content fingerprint, and CDN cache hit was logged and analyzed. The data warehouse held over **100 petabytes in S3** and was growing fast.

Two engineers — **Ryan Blue** and **Daniel Weeks** — were responsible for keeping that warehouse usable.

The standard tool of the era was **Apache Hive**: tables defined by directories on a filesystem, partitions stored in a metastore, files discovered by listing folders. It had powered big data for nearly a decade. It was the de facto standard.

And at Netflix's scale, it was actively breaking.

---

## The Real Problem Was Not Performance — It Was Trust

Most articles about Iceberg start with performance numbers. Netflix's story is more interesting than that.

The deeper issue was **trust**. Engineers stopped using certain pipelines because they were afraid of corrupting tables.

Imagine that for a second.

> *"Many at Netflix avoided using these services and making changes to the data to avert unintended consequences from the Hive format."* — Ryan Blue

Think about what that means in practice:

- A data scientist needs to backfill three days of data — but won't, because the rewrite might leave the table in a half-updated state visible to downstream jobs.
- An engineer wants to compact thousands of small files — but won't, because there's no atomic way to swap them out.
- A platform team wants to fix a partitioning mistake — but won't, because the migration could break every consumer.

When your data platform makes engineers afraid to change data, you don't have a performance problem. You have an **architectural** problem.

---

## Why Hive Broke at Cloud Scale

Hive was designed in the HDFS era. Its mental model assumed:

- A real filesystem with directories
- Cheap, atomic file renames
- A small number of large files
- Compute and storage living on the same machines

S3 violates **every single one** of those assumptions.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    subgraph HIVE["<b>Hive Assumptions (HDFS Era)</b>"]
        H1["<b>Directory =<br/>Partition</b>"]
        H2["<b>Rename is<br/>atomic &amp; cheap</b>"]
        H3["<b>Listing folders<br/>is fast</b>"]
        H4["<b>Strong<br/>consistency</b>"]
    end
    subgraph S3["<b>S3 Reality (Cloud Era)</b>"]
        R1["<b>No real<br/>directories</b>"]
        R2["<b>Rename =<br/>copy + delete</b>"]
        R3["<b>Listing<br/>millions of keys<br/>is slow</b>"]
        R4["<b>Eventual<br/>consistency</b>"]
    end
    H1 -.->|"breaks"| R1
    H2 -.->|"breaks"| R2
    H3 -.->|"breaks"| R3
    H4 -.->|"breaks"| R4
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class H1,H2,H3,H4 gray
    class R1,R2,R3,R4 midgray
    style HIVE fill:#f5f5f5,stroke:#666,color:#111
    style S3 fill:#f5f5f5,stroke:#666,color:#111
</div>

Each of these mismatches caused real, painful production problems.

### The five symptoms Netflix kept hitting

| # | Symptom | Why it happened |
|---|---------|-----------------|
| 1 | **Slow query planning** | Listing thousands of partition paths on S3 took minutes |
| 2 | **Non-atomic writes** | Renames in S3 are copies; jobs were visible mid-write |
| 3 | **Engine drift** | No formal spec → Hive and Spark hashed buckets differently |
| 4 | **Cross-partition pain** | Locking worked only for Hive; nothing else honored it |
| 5 | **Painful schema changes** | Adding a column often meant rewriting the whole table |

Each problem on its own looked like a tooling annoyance. Together they meant **the abstraction was wrong for the underlying storage**.

---

## The Insight: Track Files, Not Folders

The breakthrough is almost embarrassingly simple in retrospect.

> Stop letting the filesystem describe the table.
> 
> Let a small set of metadata files describe the table — and let those metadata files describe the data files explicitly.

That one decision unlocks everything.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    subgraph BEFORE["<b>Hive: Folder Is The Table</b>"]
        T1["<b>Table Definition</b>"]
        T1 --> P1["<b>s3://bucket/events/dt=2024-01-01/</b><br/>(list to discover files)"]
        T1 --> P2["<b>s3://bucket/events/dt=2024-01-02/</b><br/>(list to discover files)"]
    end
    subgraph AFTER["<b>Iceberg: Metadata Is The Table</b>"]
        M1["<b>Metadata File</b><br/>v42.metadata.json"]
        M1 --> SN["<b>Snapshot</b><br/>(point in time)"]
        SN --> ML["<b>Manifest List</b>"]
        ML --> MF1["<b>Manifest</b><br/>+ stats per file"]
        ML --> MF2["<b>Manifest</b><br/>+ stats per file"]
        MF1 --> F1["<b>data file 1</b>"]
        MF1 --> F2["<b>data file 2</b>"]
        MF2 --> F3["<b>data file 3</b>"]
    end
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class T1,P1,P2,F1,F2,F3 gray
    class M1,SN,ML,MF1,MF2 midgray
    style BEFORE fill:#f5f5f5,stroke:#666,color:#111
    style AFTER fill:#f5f5f5,stroke:#666,color:#111
</div>

Once you describe a table by an explicit list of files (with statistics, partition values, schema versions, and snapshot IDs baked in), several things become true *for free*:

- **Atomic commits** are just swapping one metadata pointer for another
- **Time travel** is just reading an older metadata file
- **Schema evolution** is a metadata change, not a data rewrite
- **Query planning** uses the embedded statistics — no folder listings
- **Concurrent writers** can use optimistic concurrency on the metadata pointer

That last one is what Netflix really wanted.

---

## How an Iceberg Commit Actually Works

Here is the move that replaced locking, renames, and partial-write panic:

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
sequenceDiagram
    participant W as Writer
    participant S as S3 (Data)
    participant C as Catalog
    W->>S: 1. Write new parquet files (private, not visible)
    W->>S: 2. Write new manifests pointing to those files
    W->>S: 3. Write new metadata.json (new snapshot)
    W->>C: 4. Atomic compare-and-swap of metadata pointer
    Note over W,C: If pointer changed (someone else committed first),<br/>retry from step 2
    C-->>W: 5. Commit succeeded
</div>

The data files are written first, but **invisible** to readers because nothing points at them yet.

The commit itself is one tiny atomic operation: change which metadata file is "current."

If two writers race, only one wins. The loser retries. **No locks, no half-writes, no surprises.**

---

## Snapshots: The Quiet Superpower

Netflix's team realized that once every commit produces an immutable metadata file, the table effectively becomes a **versioned object**.

That gives you four capabilities most teams pay separate vendors for:

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    S1["<b>Snapshot 1</b><br/>10:00 AM"] --> S2["<b>Snapshot 2</b><br/>10:15 AM<br/>backfill"]
    S2 --> S3["<b>Snapshot 3</b><br/>10:30 AM<br/>compaction"]
    S3 --> S4["<b>Snapshot 4</b><br/>10:45 AM<br/>late data"]
    S4 -.->|"<b>rollback</b>"| S2
    S2 -.->|"<b>time travel</b>"| Q1["<b>Query as of<br/>10:15 AM</b>"]
    S3 -.->|"<b>audit</b>"| Q2["<b>Why did<br/>row count change?</b>"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class S1,S2,S3,S4 midgray
    class Q1,Q2 gray
</div>

- **Time travel** — query the table as it existed at any past snapshot
- **Rollback** — reverse a bad write in one metadata flip
- **Audit** — explain why a number changed between two reports
- **Safe maintenance** — compact small files into big ones as a separate snapshot, then promote

The last one is what made compaction safe to run continuously in the background — something Hive could never offer.

---

## The Hidden Partitioning Win

This one is subtle but huge for Netflix's data scientists.

In Hive, if a table is partitioned by `event_date`, every query has to filter on `event_date` to be fast. Forget that filter and you scan the world.

Iceberg breaks the link between **how a user writes the query** and **how the table is physically laid out**.

```sql
-- User writes the natural query
SELECT * FROM events WHERE event_time > '2024-06-01';

-- Iceberg knows the table is partitioned by day(event_time)
-- It transforms the predicate automatically
-- Only the relevant partitions are scanned
```

The user does not need to know the partition scheme. The platform team can **change** the partition scheme later without breaking a single query.

For a company with thousands of analysts and millions of queries, this is enormous.

---

## The Numbers That Mattered to Netflix

The published outcomes after Iceberg adoption:

| Metric | Before (Hive) | After (Iceberg) |
|--------|---------------|-----------------|
| Tables managed | tens of thousands | **1+ million** |
| Warehouse size | ~tens of PB | **100+ PB** |
| Query planning on huge tables | minutes | **sub-second** |
| Atomic writes | no | **yes** |
| Concurrent writers | brittle | **optimistic concurrency** |
| Hidden partitioning | no | **yes** |
| Time travel / rollback | no | **yes** |

But the more important number is the one that does not appear in any chart:

> **The number of engineers who stopped being afraid of their own data warehouse.**

That is the metric Ryan Blue actually optimized for.

---

## Why Open Source Was the Plan from Day One

Netflix made an unusual call: build it as if it were already an open project.

Three reasons stand out:

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    OS["<b>Open Source<br/>From Day One</b>"]
    OS --> R1["<b>The problem<br/>was not Netflix-specific</b><br/>Every cloud-era<br/>warehouse hits this"]
    OS --> R2["<b>Multi-engine adoption</b><br/>Spark, Trino, Flink, Hive<br/>need to agree on a spec"]
    OS --> R3["<b>Future hiring</b><br/>Engineers want to work<br/>on industry-standard tools"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    class R1,R2,R3 gray
    style OS fill:#757575,stroke:#000,stroke-width:2.5px,color:#fff
</div>

The result:

- **2017** — Project starts internally at Netflix
- **November 2018** — Donated to Apache Software Foundation
- **May 2020** — Graduates to Apache top-level project
- **2024+** — Adopted by Apple, Airbnb, LinkedIn, Adobe, Lyft, Expedia, Stripe, and effectively every major cloud data platform

A formal **specification** (not just a reference implementation) meant Spark, Trino, Flink, Snowflake, Databricks, BigQuery, and Athena could all read the same tables and behave the same way. That alone fixed one of Hive's biggest historical pain points.

---

## What Engineers Should Take Away From This Story

Five lessons that generalize beyond Netflix:

### 1. The abstraction must match the storage

Hive was not "bad." It was built for the right problem in 2008. By 2017 the problem had changed (HDFS → S3) and the abstraction had not. **When the substrate changes, the abstraction must change too.**

### 2. Metadata is a first-class product

Most teams treat metadata as bookkeeping. Iceberg treats metadata as the table itself. That single shift gives you ACID, time travel, rollback, and engine independence — for free.

### 3. Trust is a performance metric

Netflix's real win was not query latency. It was that engineers were willing to write to the warehouse again. **You cannot ship features on top of data nobody trusts.**

### 4. Specifications beat implementations

Hive's lack of a spec is why bucketing in Spark and Hive were incompatible. Iceberg started with a spec. Every engine implements it the same way. **If you want a multi-engine future, write a spec.**

### 5. Build the standard you wish existed

The boldest move was assuming the problem was bigger than Netflix and building accordingly. Most companies would have built an internal-only fix. Netflix built an industry.

---

## Closing: A Quiet Revolution

Iceberg does not look revolutionary at first glance. It is a JSON metadata file, some manifest files, and a list of parquet paths.

But it represents one of the cleanest examples in modern data engineering of doing the boring, careful work of **redrawing an abstraction line** so that everything above and below it gets simpler.

When a Netflix engineer was asked what would happen if Iceberg disappeared, the answer was:

> *"Iceberg is at the heart of Netflix. Without it, both the company and the streaming platform would cease to exist."*

That is the kind of quiet infrastructure work that does not make headlines — and yet quietly powers most of the modern data ecosystem.

The lesson for the rest of us is not "use Iceberg." The lesson is:

**When your platform makes engineers afraid to touch their own data, the answer is not better tooling on top. It is a better abstraction underneath.**
