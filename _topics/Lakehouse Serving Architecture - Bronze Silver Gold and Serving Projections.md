---
title: "Lakehouse Serving Architecture: Bronze, Silver, Gold, and Serving Projections"
category: Data
order: 5
permalink: /topics/lakehouse-serving-architecture/
tags:
  - data-lakehouse
  - iceberg
  - bronze-silver-gold
  - serving-layer
  - starrocks
  - trino
  - gravitino
  - redis
  - scylla
  - clickhouse
  - architecture
  - mermaid
  - agentic-ai
  - semantic-layer
  - mcp
summary: "A practical architecture guide explaining why Bronze/Silver/Gold describe data quality while Serving describes consumption. Covers how to keep Gold as the authoritative Iceberg source of truth and publish workload-specific serving projections to Trino, StarRocks/ClickHouse, and Redis/Scylla, plus how to expose governed metrics to AI agents through a semantic layer and MCP server — with Mermaid diagrams throughout."
date: 2026-08-08
---

# Lakehouse Serving Architecture: Bronze, Silver, Gold, and Serving Projections

> **Core idea:** Bronze → Silver → Gold describes **data quality**. Serving describes **how the data is consumed**. These are two different axes, and conflating them leads to a weaker architecture.

<img src="{{ site.baseurl }}/assets/img/lakehoust.png" alt="Modern Lakehouse Architecture: data sources feed Bronze/Silver/Gold Iceberg zones, Gold is served through Trino, StarRocks, and Redis/Scylla, an Agentic Semantic Layer sits in front of consumption, and Gravitino/IRC governs everything end-to-end" width="100%" />

*The full picture: data sources feed Bronze (raw) → Silver (clean) → Gold (curated) Iceberg zones, Gold is served through Trino, StarRocks, and Redis/Scylla, an Agentic Semantic Layer sits in front of consumption, and Gravitino/IRC governs everything end-to-end.*

---

## 1. The mistake to avoid

A tempting but flawed design looks like this:

<div class="mermaid">
flowchart LR
    A[Bronze Iceberg] --> B[Silver Iceberg]
    B --> C[Gold Iceberg]
    C --> D[Serving Iceberg]
</div>

This treats **Serving** as just another data-quality stage, like a "Platinum" tier. But serving is not about quality — Gold is already clean, governed, and business-ready. Serving is about **physically optimizing** that same Gold data for a specific consumer's latency and concurrency requirements.

> **Memory trick:** Bronze/Silver/Gold answers "how trustworthy is this data?" Serving answers "how fast do I need to read it, and in what shape?"

---

## 2. Recommended architecture

Keep Gold in Iceberg as the governed analytical source of truth. Then **publish** workload-specific serving projections from Gold — do not make Serving another Iceberg tier.

<div class="mermaid">
flowchart TB
    subgraph LAKEHOUSE["Data Lakehouse"]
        BZ[Bronze Iceberg<br/>Raw] --> SV[Silver Iceberg<br/>Clean]
        SV --> GD[Gold Iceberg<br/>Business-ready Data Products]
        GD -.-> OBJ[Pure Object Storage<br/>Gravitino Catalog]
    end

    GD -->|Publish / Materialize| PUB[Serving Publisher]

    PUB --> AS[Analytical Serving<br/>Trino over Iceberg Gold]
    PUB --> OLAP[Low-Latency OLAP Serving<br/>StarRocks / ClickHouse / Pinot]
    PUB --> OPS[Operational Serving<br/>Redis / Scylla / Cassandra / PostgreSQL]

    AS --> BI[BI / Analysts<br/>Ad-hoc SQL / Data Science]
    OLAP --> DASH[Dashboards / Analytics APIs<br/>High concurrency]
    OPS --> API[REST APIs / Applications<br/>Point lookup]
</div>

---

## 3. Keep Gold in Iceberg

Gold should remain the single authoritative business representation of your data.

<div class="mermaid">
flowchart TB
    subgraph Bronze
        B1[customer_raw]
        B2[transaction_raw]
    end
    subgraph Silver
        S1[customer_clean]
        S2[transaction_clean]
    end
    subgraph Gold
        G1[customer_360]
        G2[account_position]
        G3[customer_balance]
        G4[transaction_summary]
    end
    B1 --> S1 --> G1
    B2 --> S2 --> G4
    S1 --> G2
    S1 --> G3
</div>

Iceberg is well suited for Gold because it provides:

- **Snapshots** — point-in-time, reproducible views of a table
- **Schema evolution** — add, drop, or rename columns without rewriting data
- **Partition evolution** — change partitioning strategy over time
- **Metadata pruning** — skip irrelevant files using metadata, not full scans
- **File-level statistics** — eliminate files before reading them

These optimizations make large analytical scans efficient. But even with them, two very different query shapes emerge:

```sql
-- Point lookup — latency-sensitive
SELECT balance
FROM customer_account
WHERE account_id = 'A123456';
```

```sql
-- Analytical aggregation — the Iceberg/lakehouse sweet spot
SELECT region, SUM(balance)
FROM customer_account
WHERE business_date = DATE '2026-08-08'
GROUP BY region;
```

The aggregation query is what Iceberg and lakehouse engines excel at. The point lookup belongs in a serving database when strict latency matters.

---

## 4. Three serving classes

This distinction is the key design principle: **Serving Zone is not one database — it is a publishing architecture.**

| Requirement | Serving technology | Source |
|---|---|---|
| Seconds, large analytical queries | Trino → Iceberg | Gold Iceberg |
| 100 ms–1 sec, high-concurrency analytics | StarRocks / ClickHouse | Gold Iceberg |
| 1–20 ms point lookup | Redis / Scylla / Cassandra / PostgreSQL | Projection from Gold |
| Full-text / search | OpenSearch | Projection from Gold |
| ML / vector retrieval | Vector index / store | Projection from Gold |

<div class="mermaid">
flowchart LR
    GD[Gold Iceberg] --> T[Trino<br/>Seconds]
    GD --> SR[StarRocks / ClickHouse<br/>100ms - 1s]
    GD --> KV[Redis / Scylla<br/>1-20ms]
    GD --> OS[OpenSearch<br/>Search]
    GD --> VEC[Vector Store<br/>ML / RAG]
</div>

---

## 5. Architecture for Iceberg + Gravitino + Trino platforms

<div class="mermaid">
flowchart TB
    APP[Applications] --> SQL[SQL / BI]
    APP --> AAPI[Analytics API]
    APP --> RAPI[REST API]

    SQL --> TRINO[Trino]
    AAPI --> SRK[StarRocks<br/>Hot OLAP]
    RAPI --> KV[Redis / Scylla]

    TRINO --> PUB[Serving Publisher<br/>Snapshot detection / CDC<br/>transformations / projection<br/>indexing / materialization]
    SRK -.->|reads or is refreshed from| PUB
    KV -.->|reads or is refreshed from| PUB

    PUB --> GOLD[Gold Data Products<br/>Apache Iceberg]
    GOLD --> GRAV[Gravitino / IRC]
    GRAV --> OBJ[Pure Object Storage]
</div>

**Gravitino** continues to be the catalog and governance control point for Iceberg datasets. Its Iceberg REST service exposes the standard Iceberg REST API and includes capabilities such as credential vending, audit logging, and access control.

**Trino** remains the general-purpose lakehouse query engine. It can query Iceberg directly and supports metadata/file caching and Iceberg materialized views.

---

## 6. StarRocks as the analytical serving zone

StarRocks is worth evaluating seriously for the analytical serving tier because it offers two modes.

### Mode A — query Iceberg directly

<div class="mermaid">
flowchart TB
    APP[Application] --> SR[StarRocks]
    SR --> GREST[Gravitino REST Catalog]
    GREST --> GOLD[Iceberg Gold]
    GOLD --> OBJ[Pure Object Storage]
</div>

StarRocks can query external Iceberg catalogs and supports the Iceberg REST catalog interface. Gravitino exposes an Iceberg REST catalog, so this pairing is worth testing against your specific Gravitino/StarRocks versions.

This mode still ultimately reads lake/object-storage data — it is not the right choice for the most latency-sensitive workloads.

### Mode B — materialize hot Gold data

<div class="mermaid">
flowchart TB
    GOLD["Gold.customer_360<br/>(20 billion rows)"] -->|incremental materialization| SR[StarRocks]
    SR --> C1[customer_summary]
    SR --> C2[customer_position]
    SR --> C3[daily_balance]
    C1 --> Q[100ms-1s queries]
    C2 --> Q
    C3 --> Q
</div>

Once materialized, StarRocks owns an optimized copy and can add:

- Indexes
- Distribution / bucketing
- Materialized views
- Local cache / storage
- Pre-aggregations

StarRocks explicitly supports asynchronous materialized views over Iceberg tables, incrementally refreshes partitions when underlying Iceberg data changes, and can rewrite queries to use those materialized views automatically. StarRocks describes its engine as targeting sub-second, high-concurrency analytical queries.

---

## 7. Don't use StarRocks for everything

Consider an API with strict SLAs:

```text
GET /customers/12345/balance

P50 = 2 ms
P99 = 8 ms
20,000 requests/sec
```

Neither `API → Trino → Iceberg` nor a distributed analytical database is the right first choice here. Instead, publish a specialized projection:

<div class="mermaid">
flowchart LR
    GOLD[Gold Iceberg] --> PUB[Serving Publisher]
    PUB --> KV["Scylla / Redis<br/>Key: customer_id<br/>Value: balance, status, timestamp"]
    KV --> API[API]
</div>

The stored record is intentionally tiny:

```json
{
  "customer_id": "12345",
  "balance": 12540.32,
  "currency": "CAD",
  "as_of": "2026-08-08T07:30:00"
}
```

You do not copy the entire Gold dataset — you publish only the serving projection required by that specific service.

---

## 8. One Gold product, multiple projections

<div class="mermaid">
flowchart TB
    GOLD["Gold Iceberg<br/>CUSTOMER_360"] --> TRINO[Trino<br/>Full data analytical access]
    GOLD --> SRK[StarRocks<br/>Analytics projection]
    GOLD --> SCY[Scylla<br/>Keyed projection]
    GOLD --> OS[OpenSearch<br/>Search]
    GOLD --> VEC[Vector Index<br/>AI / RAG]

    TRINO --> AN[Analyst]
    SRK --> DASH[Dashboard]
    SCY --> API[API]
</div>

This is a stronger model than a linear `Bronze → Silver → Gold → Serving` Iceberg chain, because Serving is not a data-quality stage — it is **a physical optimization of Gold for a consumer SLA**.

---

## 9. Avoid dual writes

Never let applications or pipelines independently write to two stores without a consistency strategy:

<div class="mermaid">
flowchart LR
    SRC[Source] -->|write| ICE[Iceberg]
    SRC -->|write, uncoordinated| RED[Redis]
</div>

Without coordination you can easily end up with:

```text
Iceberg = balance $100
Redis   = balance $90
```

Instead, create an explicit publishing mechanism with checkpoints:

<div class="mermaid">
flowchart TB
    COMMIT[Iceberg Commit] --> SNAP["Snapshot 105"]
    SNAP --> PUB[Serving Publisher]
    PUB --> SR2[StarRocks]
    PUB --> SC2[Scylla]
    PUB --> OS2[OpenSearch]
    PUB --> CP["Checkpoint:<br/>Snapshot 105 published successfully"]
</div>

If the publisher crashes partway through:

```text
Snapshot 104 ✓
Snapshot 105 ✕

restart → 105 → replay
```

This gives you **idempotency** and **recoverability**.

---

## 10. Real-time freshness

If you require seconds or milliseconds of freshness, don't wait for large Iceberg batch commits.

<div class="mermaid">
flowchart TB
    KAFKA[Kafka / Event Stream] --> ICEP[Iceberg pipeline]
    KAFKA --> SVP[Serving pipeline]
    ICEP --> BSG[Bronze / Silver / Gold]
    SVP --> SRSC[StarRocks / Scylla]
    BSG -.->|periodic reconciliation| SRSC
</div>

```text
FAST PATH
Kafka ─────────────────────► Serving DB

DURABLE / TRUTH PATH
Kafka ──► Iceberg ──────────► reconciliation
```

This dual-path approach is particularly useful when the API requires very fresh data, while Iceberg remains the eventual source of truth for reconciliation.

---

## 11. Preferred end-to-end architecture

<div class="mermaid">
flowchart TB
    subgraph Consumption
        SQLBI[SQL / BI]
        AAPI[Analytical API]
        OAPI[Operational API]
    end

    SQLBI --> TRINO[Trino]
    AAPI --> SRK[StarRocks]
    OAPI --> KV[Redis / Scylla]

    TRINO --> GOLD[Gold Iceberg<br/>Data Products]
    SRK -.->|Serving Projections| GOLD
    KV -.->|Serving Projections| GOLD

    GOLD --> SILVER[Silver Iceberg]
    SILVER --> BRONZE[Bronze Iceberg]

    GOLD -.-> GRAV["Gravitino / IRC<br/>Governance, Classification,<br/>Authorization, Metadata,<br/>Credential Vending"]
    GRAV -.-> OBJ[Pure Object Storage]
</div>

**Architectural rule:** *Iceberg Gold is authoritative. Serving stores are disposable, rebuildable projections optimized for consumer SLAs.*

The major benefit: you never create a second system of record. If StarRocks, Redis, or Scylla is lost or corrupted, rebuild it from Gold Iceberg.

---

## 12. Agentic / semantic serving

AI agents are a fifth kind of consumer, and they need something none of the other serving classes provide: a **governed vocabulary of business meaning**, not raw table access.

### 12.1 Why raw Iceberg/Trino access is the wrong interface for agents

An LLM-based agent asked "what was our Q2 churn rate in the West region?" cannot be handed a live SQL editor against Gold and be trusted to get it right every time. Three things go wrong:

- **Join and grain errors** — the agent may join `customer_360` to `transaction_summary` on the wrong key, or aggregate at the wrong grain, and produce a confident but incorrect number.
- **Metric drift** — "churn rate" might be defined three different ways across three different generated queries, even though there is one correct definition.
- **Ungoverned access** — a free-text SQL agent can accidentally read columns or rows a human requester was never authorized to see.

<div class="mermaid">
flowchart LR
    A[Agent generates raw SQL] --> B[Trino / StarRocks]
    B --> C[Gold Iceberg]
    A -.->|risk| D["Wrong joins<br/>Inconsistent metric logic<br/>No row/column governance"]
</div>

### 12.2 Insert a semantic layer between agents and Gold

A **semantic layer** (also called a metrics layer — tools like dbt Semantic Layer, Cube, AtScale, or LookML) sits between agents and Gold. It exposes pre-defined, governed **metrics and dimensions** — not tables and columns — as the only interface agents are allowed to call.

<div class="mermaid">
flowchart TB
    AGENT[AI Agent / LLM] -->|natural language| ORCH[Agent Orchestrator]
    ORCH -->|tool call: get_metric| MCP[MCP Server<br/>Semantic Layer Tools]
    MCP --> SEM[Semantic Layer<br/>dbt Semantic Layer / Cube / AtScale]
    SEM -->|compiled, governed SQL| TRINO[Trino / StarRocks]
    TRINO --> GOLD[Gold Iceberg]
</div>

The agent never writes SQL against Gold directly. It calls a **named, versioned metric** — e.g. `churn_rate(region="West", quarter="2026-Q2")` — and the semantic layer compiles that request into the one correct, pre-approved query.

### 12.3 The Model Context Protocol (MCP) as the agent-facing contract

MCP gives the agent a discoverable, typed set of tools instead of an open SQL socket:

- **Tool discovery** — the agent lists available metrics/dimensions (`list_metrics`, `describe_metric`) instead of guessing table names.
- **Typed calls** — `get_metric(name, filters, grain)` replaces free-text SQL, so malformed or out-of-scope requests fail fast instead of returning a wrong answer.
- **Guardrails at the boundary** — row-level security, column masking, per-metric access control, and query cost/row limits are enforced once, in the MCP/semantic layer, rather than trusted to prompt engineering.

<div class="mermaid">
flowchart TB
    subgraph MCP["MCP Server"]
        T1[list_metrics]
        T2[describe_metric]
        T3[get_metric]
    end
    AGENT[Agent] --> T1
    AGENT --> T2
    AGENT --> T3
    T3 --> GUARD[Guardrails<br/>RLS / column masking /<br/>row & cost limits]
    GUARD --> SEM[Semantic Layer]
    SEM --> GOLD[Gold Iceberg]
</div>

### 12.4 Agentic/semantic serving as a fourth serving class

This slots directly into the serving-class table from Section 4 — it is not a replacement for Trino, StarRocks, or Redis, it sits **in front of** them for a specific consumer type:

| Requirement | Serving technology | Source |
|---|---|---|
| Natural-language question → governed metric | Semantic layer + MCP → Trino/StarRocks | Gold Iceberg |

<div class="mermaid">
flowchart TB
    GOLD[Gold Iceberg] --> TRINO2[Trino / StarRocks]
    TRINO2 --> SEM2[Semantic Layer<br/>Metrics + Dimensions]
    SEM2 --> MCP2[MCP Server]
    MCP2 --> AGENTS["Agents<br/>(chat, autonomous workflows, RAG)"]
    GOLD --> TRINO3[Trino]
    GOLD --> SRK3[StarRocks / ClickHouse]
    GOLD --> KV3[Redis / Scylla]
    TRINO3 --> BI2[BI / Analysts]
    SRK3 --> DASH2[Dashboards]
    KV3 --> API2[APIs]
</div>

The same principle from the rest of this guide still holds: **the semantic layer and MCP server are stateless and rebuildable.** They hold no data of their own — only metric definitions and a mapping to Gold. If they are lost, redeploy them from source control; Gold Iceberg remains the only system of record.

---

## 13. Summary

| Layer | Purpose | Technology |
|---|---|---|
| Bronze | Raw ingestion | Iceberg |
| Silver | Cleaned, conformed | Iceberg |
| Gold | Business-ready, governed source of truth | Iceberg |
| Analytical serving | Ad-hoc SQL, large scans | Trino over Gold |
| Sub-second OLAP serving | Dashboards, high concurrency | StarRocks / ClickHouse materializations |
| Operational serving | Point lookups, strict SLAs | Redis / Scylla projections from Gold |
| Search serving | Full-text queries | OpenSearch projections |
| ML serving | Vector retrieval / RAG | Vector store projections |
| Agentic / semantic serving | Governed metrics for AI agents | Semantic layer + MCP over Trino/StarRocks |

**Default choices for an on-prem Iceberg + Gravitino platform:**

- **Trino + Iceberg** for normal analytical serving
- **StarRocks materializations** for high-concurrency, sub-second analytical serving
- **Redis / Scylla-style projections** only for true point-lookup APIs
- **Semantic layer + MCP server** as the only interface AI agents use to reach Gold — never raw SQL

This keeps the architecture open while avoiding the mistake of forcing Iceberg to behave like an OLTP or key-value store.
