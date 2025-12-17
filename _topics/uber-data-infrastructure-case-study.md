---
title: "Case Study: How Uber Built & Modernized Their Data Infrastructure"
category: Case Studies
tags:
  - case-study
  - uber
  - data-infrastructure
  - gcp
  - kafka
  - real-world
summary: Learn how Uber evolved their data infrastructure from serving 137 million users to modernizing with Google Cloud — explained simply.
---

> **What you'll learn:** How one of the world's largest tech companies built and then completely modernized their data infrastructure to handle billions of events per day. No technical background needed!

## Introduction: Uber's Data Challenge

Imagine processing data for:
- **137 million monthly active users**
- **7 billion trips per year**
- **Billions of events every single day** (GPS locations, ride requests, payments, etc.)

That's Uber's challenge. Every second, millions of data points are generated:
- Riders requesting rides
- Drivers accepting requests
- GPS tracking every movement
- Payments being processed
- Maps being updated

**The question:** How do you store, process, and analyze all this data in real-time?

This case study shows how Uber solved this problem — twice!

---

## Part 1: The Original Infrastructure (2015-2020)

### The Challenge Uber Faced

Think of Uber like a massive restaurant chain that needs to know:
- What every customer is ordering (ride requests)
- Where every delivery driver is (driver locations)
- How much everything costs (pricing, payments)
- What's working and what's not (analytics)
- All happening **right now, in real-time**

Traditional databases couldn't handle this. Here's why:

```
Traditional Database (like PostgreSQL):
- Handles: 10,000 requests/second
- Uber's need: 1,000,000+ events/second
- Result: Database would crash! 🔥
```

### Uber's Original Solution: The Data Pipeline

Uber built a complex but powerful system using multiple specialized tools:

<div class="mermaid">
flowchart LR
    APPS["Uber Apps<br/>(Riders & Drivers)"] --> KAFKA["Kafka<br/>(Event Streaming)"]
    
    KAFKA --> FLINK["Flink<br/>(Real-time Processing)"]
    KAFKA --> SPARK["Spark<br/>(Batch Processing)"]
    
    FLINK --> HDFS["HDFS<br/>(Storage)"]
    SPARK --> HDFS
    
    HDFS --> HUDI["Hudi<br/>(Data Lake)"]
    HUDI --> PINOT["Pinot<br/>(Analytics)"]
    HUDI --> PRESTO["Presto<br/>(Queries)"]
    
    PINOT --> DASHBOARDS["Dashboards<br/>(Insights)"]
    PRESTO --> DASHBOARDS
    
    style APPS fill:#dbeafe,stroke:#2563eb
    style KAFKA fill:#fef3c7,stroke:#d97706
    style HDFS fill:#d1fae5,stroke:#059669
    style DASHBOARDS fill:#fce7f3,stroke:#db2777
</div>

### Breaking Down the Components (Simplified)

Let me explain each piece in simple terms:

#### 1. Apache Kafka — The Event Highway

> **Think of it like:** A super-fast conveyor belt that moves millions of packages (data events) per second.

**What it does:**
- Captures every event (ride request, GPS update, payment)
- Moves data at incredible speed (millions per second)
- Never loses data (even if something crashes)

**Real example:**
```
Rider opens app → Kafka captures event
Driver accepts → Kafka captures event
GPS updates location → Kafka captures event
Payment processed → Kafka captures event

All happening simultaneously for 137 million users!
```

#### 2. HDFS (Hadoop Distributed File System) — The Warehouse

> **Think of it like:** A massive warehouse that can store unlimited boxes (data files) across thousands of rooms (servers).

**What it does:**
- Stores petabytes of data (1 petabyte = 1 million gigabytes!)
- Splits data across thousands of servers
- Never loses data (keeps 3 copies of everything)

**Uber's scale:**
```
Data stored: Multiple petabytes
Files: Billions of files
Servers: Thousands of machines
Daily growth: Terabytes of new data every day
```

#### 3. Apache Hudi — The Smart Librarian

> **Think of it like:** A librarian who can instantly update any book in a library of billions of books.

**What it does:**
- Lets Uber update old data (like fixing a completed trip's details)
- Keeps track of all changes (time travel - see data from yesterday)
- Makes querying fast even with billions of records

**Why Uber needed it:**
```
Problem: Can't update data in traditional data lakes
Uber's need: Update trip status, fix pricing errors, correct GPS data
Hudi's solution: Updates data in seconds, not hours
```

#### 4. Apache Spark — The Batch Processor

> **Think of it like:** A factory that processes millions of items at once, overnight.

**What it does:**
- Processes huge amounts of data in batches
- Runs complex calculations (pricing algorithms, demand prediction)
- Generates reports and summaries

**Uber's use cases:**
```
Every night:
- Calculate driver earnings
- Generate surge pricing maps
- Create demand forecasts
- Build ML models

Processing: Petabytes of data in hours
```

#### 5. Apache Flink — The Real-Time Brain

> **Think of it like:** A super-fast chef who cooks orders the instant they come in (no waiting).

**What it does:**
- Processes data in real-time (milliseconds)
- Detects patterns instantly (fraud, surge pricing)
- Updates dashboards live

**Uber's use cases:**
```
Real-time:
- Surge pricing (demand spikes)
- Fraud detection (suspicious rides)
- Driver matching (find nearest driver)
- ETA calculation (time to arrival)

Response time: Under 1 second!
```

#### 6. Apache Pinot — The Analytics Speed Demon

> **Think of it like:** A super-smart calculator that can answer complex questions about billions of numbers instantly.

**What it does:**
- Answers analytical queries in milliseconds
- Powers dashboards and reports
- Handles thousands of users querying simultaneously

**Uber's use cases:**
```
Questions answered instantly:
- "How many rides in NYC right now?"
- "Average trip duration by city?"
- "Peak demand times this week?"
- "Driver earnings trends?"

Query time: 100-500 milliseconds!
```

#### 7. Presto — The Query Language Translator

> **Think of it like:** A universal translator that lets you ask questions in simple language about data stored anywhere.

**What it does:**
- Queries data across different systems (HDFS, databases, cloud storage)
- Uses SQL (simple query language)
- Federates queries (combines data from multiple sources)

**Uber's use cases:**
```sql
-- Data engineers can write simple queries:
SELECT city, COUNT(*) as rides
FROM trips
WHERE date = '2024-01-01'
GROUP BY city

-- Works across petabytes of data!
```

---

### How It All Worked Together

Here's the complete flow of a single ride at Uber:

```
1. CAPTURE (Kafka)
   Rider opens app → Event captured → Sent to Kafka
   
2. PROCESS (Flink - Real-time)
   Kafka → Flink → Match with nearest driver (100ms)
   
3. STORE (HDFS + Hudi)
   Trip data → Saved to HDFS → Indexed by Hudi
   
4. ANALYZE (Spark - Batch)
   Every night → Calculate pricing, earnings, forecasts
   
5. QUERY (Pinot + Presto)
   Dashboards → Query data → Show insights
   
6. INSIGHTS
   Business teams see: trends, patterns, anomalies
```

### The Numbers (At Scale)

| Metric | Scale |
|--------|-------|
| **Events per second** | 1,000,000+ |
| **Data processed daily** | Multiple petabytes |
| **Storage** | Petabytes of data |
| **Query latency** | < 1 second |
| **Data retention** | Years of historical data |
| **Servers** | Thousands of machines |

---

## Part 2: The Modernization (2020-2024)

### Why Uber Needed to Change

Even with this powerful system, Uber faced challenges:

#### Problem 1: Complexity

> **The issue:** Managing dozens of different systems is like managing a city with 50 different public transport systems!

```
What Uber managed:
- Kafka clusters (event streaming)
- HDFS clusters (storage)
- Spark clusters (processing)
- Flink clusters (real-time)
- Pinot clusters (analytics)
- Presto clusters (queries)

Each needed:
- Separate teams to manage
- Different expertise
- Individual updates/patches
- Security management
- Monitoring systems

Result: Hundreds of engineers just to keep systems running!
```

#### Problem 2: Cost

> **The issue:** Running your own data centers is like owning and maintaining thousands of buildings.

```
Uber's costs:
- Server hardware (thousands of machines)
- Data centers (buildings, power, cooling)
- Network infrastructure
- Maintenance staff
- Upgrades and replacements

Annual cost: $100+ million just for infrastructure!
```

#### Problem 3: Scalability Bottlenecks

> **The issue:** Adding capacity meant buying more servers and waiting months.

```
Traditional scaling:
1. Predict demand (guess next year's growth)
2. Order servers (3-6 months lead time)
3. Install in data center (weeks)
4. Configure and test (weeks)
5. Finally ready! (but demand changed)

Problem: Can't scale quickly during unexpected growth
```

#### Problem 4: Global Expansion

> **The issue:** Uber operates in 70+ countries. Data needs to stay in each country (regulations).

```
Problem:
- EU data must stay in EU (GDPR)
- Asia data must stay in Asia
- Need to replicate entire infrastructure in each region
- Maintaining consistency across regions = nightmare

Cost: 3x-5x more expensive per region
```

---

### The Solution: Google Cloud Platform (GCP)

Uber decided to modernize by moving to GCP. Here's what changed:

<div class="mermaid">
flowchart LR
    APPS["Uber Apps"] --> PUBSUB["Pub/Sub<br/>(replaces Kafka)"]
    
    PUBSUB --> DATAFLOW["Dataflow<br/>(replaces Flink/Spark)"]
    
    DATAFLOW --> GCS["Cloud Storage<br/>(replaces HDFS)"]
    DATAFLOW --> BIGQUERY["BigQuery<br/>(replaces Pinot/Presto/Hudi)"]
    
    BIGQUERY --> LOOKER["Looker<br/>(Dashboards)"]
    
    style APPS fill:#dbeafe,stroke:#2563eb
    style PUBSUB fill:#fef3c7,stroke:#d97706
    style GCS fill:#d1fae5,stroke:#059669
    style BIGQUERY fill:#fce7f3,stroke:#db2777
    style LOOKER fill:#e0e7ff,stroke:#6366f1
</div>

### The New Architecture (Simplified)

#### 1. Google Cloud Pub/Sub (Replaces Kafka)

> **What changed:** Instead of managing Kafka clusters, Google manages it for you.

**Benefits:**
```
Before (Kafka):
- Uber manages 100+ servers
- 24/7 on-call engineers
- Manual scaling
- Upgrade headaches

After (Pub/Sub):
- Google manages everything
- Auto-scaling
- Always available
- Pay only for what you use

Result: 10x fewer engineers needed!
```

#### 2. Google Cloud Storage (Replaces HDFS)

> **What changed:** Instead of thousands of servers in data centers, data lives in Google's cloud.

**Benefits:**
```
Before (HDFS):
- Own and maintain servers
- Manage disk failures
- Plan capacity months ahead
- Limited to data center locations

After (Cloud Storage):
- Google manages hardware
- Infinite storage
- Pay per GB used
- Available worldwide

Cost savings: 40-60% cheaper!
```

#### 3. BigQuery (Replaces Hudi + Pinot + Presto)

> **What changed:** One system instead of three! This is like replacing 3 specialized tools with 1 Swiss Army knife.

**The magic of BigQuery:**

```
What it does (all in one):
✅ Stores petabytes of data (like Hudi)
✅ Queries in milliseconds (like Pinot)
✅ Uses SQL (like Presto)
✅ Scales automatically
✅ No servers to manage
✅ Updates data easily

Uber's experience:
- Query time: Same speed (100-500ms)
- Capacity: Unlimited (auto-scales)
- Management: Zero servers to manage
- Cost: Pay only for queries run

Example:
Query 10 TB of data → Takes 5 seconds → Costs $5
```

#### 4. Dataflow (Replaces Spark + Flink)

> **What changed:** One managed service for both real-time and batch processing.

**Benefits:**
```
Before:
- Manage Spark clusters (batch)
- Manage Flink clusters (real-time)
- Two different systems, two teams

After:
- One Dataflow service
- Handles both real-time and batch
- Google manages infrastructure
- Auto-scales based on load

Complexity: Reduced by 50%!
```

---

### The Migration Journey

Uber didn't switch overnight. Here's how they did it:

#### Phase 1: Pilot (6 months)

```
Step 1: Choose one small use case
- Selected: Trip analytics (non-critical)
- Migrated 5% of data
- Tested thoroughly

Result: Success! 40% faster, 50% cheaper
```

#### Phase 2: Gradual Migration (18 months)

```
Step 2: Migrate by priority
- Month 1-6: Analytics and reporting
- Month 7-12: Real-time dashboards
- Month 13-18: Critical systems

Strategy: Run both systems in parallel
- Old system: Production
- New system: Shadow (testing)
- Validate: Compare results

Result: Zero downtime!
```

#### Phase 3: Full Migration (12 months)

```
Step 3: Move everything
- Migrate remaining systems
- Shut down old infrastructure
- Train teams on new tools

Final result: 100% on GCP
```

---

### The Results: What Changed?

#### 1. Cost Savings

```
Infrastructure costs:
Before: $100+ million/year
After:  $60 million/year
Savings: 40% reduction

Why?
- No server hardware to buy
- No data centers to maintain
- Pay only for what you use
- Auto-scaling prevents over-provisioning
```

#### 2. Speed Improvements

```
Development time:
Before: 3-6 months to launch new data product
After:  2-4 weeks

Why?
- No infrastructure setup needed
- Pre-built integrations
- Self-service for data teams
```

#### 3. Reliability

```
System uptime:
Before: 99.9% (9 hours downtime/year)
After:  99.99% (52 minutes downtime/year)

Why?
- Google's infrastructure is battle-tested
- Automatic failover
- Built-in redundancy
```

#### 4. Scalability

```
Scaling time:
Before: 3-6 months (buy servers, install, configure)
After:  Automatic (scales in minutes)

Example:
- Black Friday traffic spike (10x normal)
- Old system: Would crash or need months of prep
- New system: Auto-scales, handles spike perfectly
```

#### 5. Global Expansion

```
New region setup:
Before: 6-12 months, $10+ million
After:  1-2 weeks, $1 million

Why?
- No need to build data centers
- Just enable GCP regions
- Copy configurations
- Done!

Result: Uber expanded to 20 new countries in 2 years
```

---

## Key Lessons for Your Business

### Lesson 1: Start Simple, Scale Later

> **Uber's mistake:** Built complex system too early
> 
> **Better approach:** Start with simple cloud services, add complexity only when needed

**For your startup:**
```
Don't build like Uber (initially)!

Start with:
- Simple database (PostgreSQL)
- Managed services (AWS RDS, GCP BigQuery)
- Basic analytics tools

Add complexity only when:
- Handling 100K+ requests/second
- Processing petabytes of data
- Operating in 10+ countries
```

### Lesson 2: Managed Services Save Money

> **Uber's learning:** Managing infrastructure is expensive

**Cost breakdown:**
```
Self-managed (like old Uber):
- Infrastructure: $100M
- Engineers: $50M (salaries)
- Total: $150M/year

Managed (like new Uber):
- Infrastructure: $60M (GCP)
- Engineers: $20M (fewer needed)
- Total: $80M/year

Savings: $70M/year (47% reduction)
```

### Lesson 3: Migration Takes Time

> **Uber's approach:** 3 years to fully migrate

**Your migration timeline:**
```
Small company (< 10 engineers):
- Plan: 1 month
- Migrate: 3-6 months
- Optimize: 3 months
- Total: 6-12 months

Enterprise (100+ engineers):
- Plan: 6 months
- Migrate: 18-36 months
- Optimize: 12 months
- Total: 3-5 years

Key: Don't rush! Parallel run old and new systems
```

### Lesson 4: Cloud isn't Always Cheaper (Initially)

> **Uber's reality:** First year cost MORE, long-term saved money

**Cost curve:**
```
Year 1: $120M (running both systems)
Year 2: $80M (mostly migrated)
Year 3: $60M (fully migrated)
Year 4+: $60M (stable)

Total 4-year cost:
Old approach: $400M
New approach: $320M
Savings: $80M over 4 years

ROI: Positive after 2.5 years
```

---

## The Technology Stack Comparison

### Old Stack (Self-Managed)

| Component | Purpose | Complexity | Cost |
|-----------|---------|------------|------|
| Kafka | Event streaming | High | High |
| HDFS | Storage | Very High | Very High |
| Hudi | Data lake | High | Medium |
| Spark | Batch processing | High | High |
| Flink | Real-time processing | Very High | High |
| Pinot | Analytics | High | Medium |
| Presto | Queries | Medium | Medium |

**Total complexity:** ⭐⭐⭐⭐⭐ (Maximum)
**Total cost:** $$$$$ (Very expensive)
**Management:** 300+ engineers needed

### New Stack (GCP Managed)

| Component | Purpose | Complexity | Cost |
|-----------|---------|------------|------|
| Pub/Sub | Event streaming | Low | Medium |
| Cloud Storage | Storage | Very Low | Low |
| BigQuery | Analytics + queries + data lake | Low | Medium |
| Dataflow | Batch + real-time processing | Medium | Medium |
| Looker | Dashboards | Low | Low |

**Total complexity:** ⭐⭐ (Much simpler)
**Total cost:** $$$ (Cheaper)
**Management:** 100 engineers needed

---

## What This Means for You

### If You're a Startup

**Don't build like Uber!** Start with:

```
Phase 1 (0-100K users):
- Database: PostgreSQL (managed)
- Analytics: Google Analytics / Mixpanel
- Cost: $100-500/month

Phase 2 (100K-1M users):
- Database: PostgreSQL + Redis cache
- Analytics: BigQuery
- Cost: $1K-5K/month

Phase 3 (1M-10M users):
- Database: PostgreSQL + MongoDB
- Analytics: BigQuery + Looker
- Streaming: Pub/Sub (if needed)
- Cost: $10K-50K/month

Only at 10M+ users:
Consider Uber-level infrastructure
```

### If You're Mid-Size Company

**Consider managed services:**

```
Instead of building:
✅ Use BigQuery (instead of building data warehouse)
✅ Use Pub/Sub (instead of managing Kafka)
✅ Use Cloud Storage (instead of HDFS)
✅ Use Dataflow (instead of Spark/Flink)

Benefits:
- 50% cheaper long-term
- 80% less complexity
- 5x faster to market
- Focus engineers on product, not infrastructure
```

### If You're Enterprise

**Uber's migration playbook:**

```
Year 1: Assessment
- Audit current infrastructure
- Calculate costs (TCO)
- Identify pain points
- Build business case
- Get executive buy-in

Year 2-3: Migration
- Start with non-critical systems
- Run in parallel (old + new)
- Validate results
- Train teams
- Gradually migrate critical systems

Year 4: Optimization
- Shut down old infrastructure
- Optimize cloud costs
- Document learnings
- Celebrate wins!
```

---

## Summary: Uber's Data Infrastructure Journey

> **What we learned:**

### The Old System (2015-2020)

**Built to handle:**
- 137 million monthly users
- 1 million+ events/second
- Petabytes of data

**Components:**
- Kafka → Event streaming
- HDFS → Storage
- Hudi → Data lake
- Spark → Batch processing
- Flink → Real-time processing
- Pinot → Analytics
- Presto → Queries

**Problems:**
- Complex (300+ engineers to manage)
- Expensive ($150M/year)
- Slow to scale (months)
- Hard to expand globally

### The New System (2020-2024)

**Migrated to GCP:**
- Pub/Sub → Event streaming
- Cloud Storage → Storage
- BigQuery → Everything else!
- Dataflow → Processing

**Benefits:**
- Simpler (100 engineers needed)
- Cheaper ($80M/year, 47% savings)
- Fast to scale (automatic)
- Easy global expansion

**Migration:**
- Took 3 years
- Zero downtime
- Massive success

---

## Key Takeaways

1. **Start Simple:** Don't build Uber-scale infrastructure for a small app
2. **Managed Services Win:** Let cloud providers handle infrastructure
3. **Migration Takes Time:** Plan for years, not months
4. **It's Worth It:** Long-term savings are massive

**The bottom line:** Even the most complex tech companies are moving to managed cloud services. If Uber can simplify, you can too!

---

## Further Reading

- [Uber's Engineering Blog](https://www.uber.com/blog/engineering/)
- [Google Cloud Case Study: Uber](https://cloud.google.com/customers/uber)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Data Engineering Best Practices](https://www.databricks.com/glossary/data-engineering)
