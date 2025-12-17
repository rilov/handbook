---
title: "Case Study: How Uber Built Their Data Infrastructure (Part 1)"
category: Case Studies
tags:
  - case-study
  - uber
  - data-infrastructure
  - kafka
  - hadoop
  - spark
  - flink
  - real-world
series: "Uber Data Infrastructure"
part: 1
summary: How Uber built a data platform to handle 137 million monthly users and billions of events per day — explained simply.
related:
  - uber-data-infrastructure-part-2-modernization
---

> **Part 1 of the Uber Data Infrastructure Series**
> 
> This article explains how Uber built one of the world's largest data infrastructures from scratch. You'll learn why traditional databases don't work at Uber's scale and how they solved it with specialized tools.
> 
> **Next:** [Part 2 - Modernizing with Google Cloud →]({{ site.baseurl }}{% link _topics/uber-data-infrastructure-part-2-modernization.md %})

## Introduction: The Uber Data Challenge

Imagine you're running a service that needs to track:

- **137 million monthly active users**
- **7 billion trips per year** (19 million trips per day!)
- **Millions of drivers** in real-time
- **GPS updates every second** from millions of devices
- **Payments, pricing, matching, analytics** — all happening simultaneously

Every single second, Uber processes:
- 🚗 Thousands of ride requests
- 📍 Millions of GPS location updates
- 💰 Thousands of payments
- 📊 Billions of data points for analytics

**The problem:** No single database can handle this. Traditional databases would crash instantly.

**The solution:** Uber had to build a completely custom data infrastructure using multiple specialized systems working together.

---

## Why Traditional Databases Don't Work at Uber Scale

Let's understand the problem first:

### The Traditional Approach (Won't Work!)

```
Typical startup database:
- PostgreSQL or MySQL
- Handles: 10,000 requests/second
- Storage: Up to 10 TB
- Cost: $500-5,000/month

Uber's requirements:
- Events: 1,000,000+ per second (100x more!)
- Storage: Multiple petabytes (1,000,000 GB)
- Cost: Can't throw unlimited money at it
- Result: Traditional database = 💥 CRASH!
```

### What Uber Needs Instead

Think of it like a city's infrastructure:

```
Single Database = One huge warehouse
- Everything in one place
- Hard to scale
- One failure = everything stops

Uber's Approach = Specialized city systems
- Highways (Kafka) for moving data
- Warehouses (HDFS) for storage
- Factories (Spark) for processing
- Real-time centers (Flink) for instant decisions
- Search centers (Pinot/Presto) for finding data
```

---

## Part 1: The Data Collection Layer

### Apache Kafka — The Event Highway

> **Think of Kafka as:** A super-fast highway system that can move millions of cars (data events) per second without ever getting jammed.

#### What Problem Does It Solve?

**Without Kafka:**
```
Uber App → Database → CRASH!
(Too many events hitting database at once)
```

**With Kafka:**
```
Uber App → Kafka (buffer) → Database
(Kafka handles the flood, database processes at its own pace)
```

#### How Kafka Works at Uber

<div class="mermaid">
flowchart LR
    RIDERS["📱 Rider Apps"] --> KAFKA["Kafka<br/>Event Stream"]
    DRIVERS["🚗 Driver Apps"] --> KAFKA
    PAYMENTS["💳 Payment Systems"] --> KAFKA
    MAPS["🗺️ Maps/GPS"] --> KAFKA
    
    KAFKA --> TOPIC1["Topic: Rides"]
    KAFKA --> TOPIC2["Topic: GPS"]
    KAFKA --> TOPIC3["Topic: Payments"]
    
    TOPIC1 --> CONSUMERS["Data Consumers<br/>(Spark, Flink, etc.)"]
    TOPIC2 --> CONSUMERS
    TOPIC3 --> CONSUMERS
    
    style KAFKA fill:#fef3c7,stroke:#d97706
    style CONSUMERS fill:#d1fae5,stroke:#059669
</div>

#### Real Example: A Single Ride

```
1. Rider opens app
   → Kafka captures: {"event": "app_opened", "user_id": 12345, "time": "10:00:00"}

2. Rider requests ride
   → Kafka captures: {"event": "ride_requested", "from": "Times Square", "to": "JFK"}

3. Driver accepts
   → Kafka captures: {"event": "ride_accepted", "driver_id": 67890}

4. GPS updates (every second)
   → Kafka captures: {"event": "location", "lat": 40.7580, "lng": -73.9855}

5. Ride completes
   → Kafka captures: {"event": "ride_completed", "fare": $45.50}

All these events flow through Kafka at the rate of:
- 1,000,000+ events per second
- 86,400,000,000+ events per day (86 billion!)
```

#### Why Uber Chose Kafka

| Feature | Traditional Queue | Kafka |
|---------|------------------|-------|
| **Throughput** | 10,000 events/sec | 1,000,000+ events/sec |
| **Retention** | Minutes-Hours | Days-Weeks |
| **Replay** | ❌ Once consumed, gone | ✅ Can replay anytime |
| **Durability** | ❌ Can lose data | ✅ Never loses data |
| **Scalability** | Hard to scale | Scales horizontally |

**Key benefit:** Kafka acts as a "replayable log" — Uber can go back and reprocess events from days ago if needed!

---

## Part 2: The Storage Layer

### HDFS (Hadoop Distributed File System) — The Massive Warehouse

> **Think of HDFS as:** A warehouse so massive it spans thousands of buildings (servers), but you can still find any item instantly.

#### What Problem Does It Solve?

**Traditional storage problem:**
```
Regular hard drive: 10 TB max
Uber's data: 1,000 TB (1 petabyte) per day!

Can't fit on one machine!
```

**HDFS solution:**
```
Split data across 1,000+ machines
Each machine stores small pieces
Data never lost (3 copies of everything)
```

#### How HDFS Works (Simplified)

Imagine saving a huge movie file:

```
Normal computer:
Movie.mp4 (100 GB) → Saved on single hard drive

HDFS:
Movie.mp4 (100 GB) → Split into 100 pieces (1 GB each)
- Piece 1 → Server A, Server B, Server C (3 copies)
- Piece 2 → Server D, Server E, Server F (3 copies)
- Piece 3 → Server G, Server H, Server I (3 copies)
... and so on

If Server A crashes? No problem! Piece 1 still on B and C
```

#### Uber's HDFS Scale

| Metric | Scale |
|--------|-------|
| **Total storage** | Multiple petabytes (1 PB = 1,000,000 GB) |
| **Files stored** | Billions of files |
| **Servers** | Thousands of machines |
| **Daily growth** | Terabytes of new data every day |
| **Data retention** | Years of historical data |
| **Availability** | 99.9% (almost never down) |

#### What Uber Stores in HDFS

```
1. Trip Records
   - Every ride ever taken
   - Date, time, pickup, dropoff, fare, driver, rider
   - Billions of records

2. GPS Traces
   - Every GPS ping from every driver
   - Used for: maps, ETAs, routing
   - Trillions of data points

3. Payment Data
   - Every transaction
   - Used for: accounting, fraud detection
   - Years of history

4. Logs
   - Every app action, API call, error
   - Used for: debugging, analytics
   - Petabytes of logs

5. Analytics Data
   - Pre-computed metrics, reports
   - Used for: dashboards, business decisions
```

---

## Part 3: The Smart Storage Layer

### Apache Hudi — The Time-Traveling Librarian

> **Think of Hudi as:** A magical librarian who can not only find any book in a library of billions but can also show you what the library looked like yesterday, last week, or last year.

#### What Problem Does It Solve?

**HDFS problem:**
```
HDFS is great for storing data
But:
- Can't update existing data (only append)
- Can't delete old data easily
- Can't query efficiently
- Can't go back in time

Example problem:
Ride #12345 status: "in_progress"
Driver completes ride
Need to update to: "completed"
HDFS: Can't update! Must write entire new file!
```

**Hudi solution:**
```
✅ Can update records (like a database)
✅ Can delete records
✅ Can query efficiently
✅ Can time travel (see data from any point in time)
✅ Works on top of HDFS
```

#### Real Example: Updating a Ride

```
Without Hudi (pure HDFS):
1. Read entire file (1 GB) with 1 million rides
2. Find ride #12345
3. Update status
4. Write entire file (1 GB) back
Time: Minutes, Space: 1 GB extra

With Hudi:
1. Update ride #12345 directly
2. Hudi tracks the change
Time: Seconds, Space: Few KB
```

#### Hudi's Time Travel Feature

This is incredibly powerful for Uber:

```
Question: "Show me all rides in NYC on Dec 1st as they appeared at 2pm"

Hudi can answer this!

It keeps track of:
- What data looked like at 2pm
- What changed between 2pm and 3pm
- What changed between 3pm and 4pm
- Etc.

Use cases:
✅ Debugging: "Why did driver earnings look wrong yesterday?"
✅ Auditing: "Show me all payments as they were last month"
✅ Machine Learning: "Train model on data from exactly 1 week ago"
```

#### Uber's Hudi Use Cases

| Use Case | How Hudi Helps |
|----------|----------------|
| **Trip Updates** | Update ride status, fare, duration in real-time |
| **Pricing Corrections** | Fix pricing errors after the fact |
| **GDPR Compliance** | Delete user data when requested |
| **Data Quality** | Fix bad data without reprocessing everything |
| **A/B Testing** | Compare metrics before/after changes |
| **Auditing** | Show exact state of data at any point in time |

---

## Part 4: The Processing Layer

### Apache Spark — The Overnight Factory

> **Think of Spark as:** A massive factory that works overnight to process millions of items in parallel, preparing everything for the next day.

#### What Problem Does It Solve?

**The batch processing problem:**
```
Task: Calculate yesterday's earnings for 5 million drivers

Single computer:
- Process 1 driver at a time
- 5 million drivers × 10 seconds each = 57 days!
- Impossible!

Spark:
- Process 5,000 drivers simultaneously
- 5 million ÷ 5,000 = 1,000 batches
- 1,000 × 10 seconds = 2.7 hours
- Done overnight! ✅
```

#### How Spark Works (Simplified)

<div class="mermaid">
flowchart LR
    DATA["Huge Dataset<br/>(1 PB)"] --> SPLIT["Split into<br/>1000 pieces"]
    
    SPLIT --> WORKER1["Worker 1<br/>Process piece 1"]
    SPLIT --> WORKER2["Worker 2<br/>Process piece 2"]
    SPLIT --> WORKER3["Worker 3<br/>Process piece 3"]
    SPLIT --> DOTS["..."]
    SPLIT --> WORKER1000["Worker 1000<br/>Process piece 1000"]
    
    WORKER1 --> COMBINE["Combine Results"]
    WORKER2 --> COMBINE
    WORKER3 --> COMBINE
    DOTS --> COMBINE
    WORKER1000 --> COMBINE
    
    COMBINE --> RESULT["Final Result"]
    
    style DATA fill:#dbeafe,stroke:#2563eb
    style COMBINE fill:#d1fae5,stroke:#059669
    style RESULT fill:#fce7f3,stroke:#db2777
</div>

#### What Uber Uses Spark For

**1. Nightly Earnings Calculations**
```sql
-- Every night, Spark calculates:
SELECT 
  driver_id,
  SUM(fare) as total_earnings,
  COUNT(*) as total_rides,
  AVG(rating) as avg_rating
FROM trips
WHERE date = YESTERDAY
GROUP BY driver_id

Processes: Billions of trips
Time: 2-3 hours (overnight)
Output: Driver earnings ready by morning
```

**2. Surge Pricing Maps**
```python
# Every hour, Spark builds heatmaps:
- Where demand is high
- Where supply is low
- Calculate surge multiplier (1.5x, 2x, 3x)

Processes: Real-time demand data
Time: 15-30 minutes
Output: Updated pricing for entire city
```

**3. Machine Learning Models**
```python
# Weekly, Spark trains ML models:
- ETA prediction (how long will ride take?)
- Demand forecasting (where will rides be needed?)
- Fraud detection (identify suspicious patterns)

Processes: Weeks of historical data
Time: Hours to days
Output: Updated ML models
```

**4. Report Generation**
```
Every day, Spark generates reports:
- City-by-city metrics
- Driver performance stats
- Revenue analytics
- Customer satisfaction trends

Processes: All previous day's data
Time: 1-2 hours
Output: Thousands of reports for business teams
```

#### Spark's Performance at Uber

| Task | Data Size | Time | Speed-up vs Single Machine |
|------|-----------|------|----------------------------|
| **Daily earnings** | 1 TB | 2 hours | 100x faster |
| **Weekly reports** | 7 TB | 5 hours | 200x faster |
| **ML training** | 50 TB | 12 hours | 500x faster |
| **Data cleanup** | 100 TB | 24 hours | 1000x faster |

---

## Part 5: The Real-Time Processing Layer

### Apache Flink — The Instant Response System

> **Think of Flink as:** A lightning-fast brain that makes decisions in milliseconds, not hours. While Spark processes data overnight, Flink processes it right now!

#### Spark vs Flink: What's the Difference?

```
Spark (Batch Processing):
- Like mail delivery: collect all day, deliver at night
- Processes data in large batches
- Takes minutes to hours
- Used for: reports, analytics, ML training

Flink (Stream Processing):
- Like phone calls: instant communication
- Processes data immediately as it arrives
- Takes milliseconds
- Used for: real-time decisions, instant alerts
```

#### What Problem Does Flink Solve?

**Real-time decision problem:**
```
Scenario: New Year's Eve in Times Square
- 100,000 people requesting rides simultaneously
- Need to calculate surge pricing NOW
- Can't wait for Spark's overnight batch job!

Solution: Flink processes events in real-time
1. Event arrives: Ride requested
2. Flink calculates: Demand spike detected
3. Flink decides: Apply 3x surge pricing
4. Response sent: < 100ms!
```

#### How Flink Works (Simplified)

<div class="mermaid">
flowchart LR
    EVENTS["Events Stream<br/>(Kafka)"] --> FLINK["Flink<br/>Real-time Processing"]
    
    FLINK --> DECISION1["Surge Pricing<br/>(< 100ms)"]
    FLINK --> DECISION2["Fraud Detection<br/>(< 50ms)"]
    FLINK --> DECISION3["Driver Matching<br/>(< 200ms)"]
    FLINK --> DECISION4["ETA Calculation<br/>(< 100ms)"]
    
    DECISION1 --> ACTION["Immediate Actions"]
    DECISION2 --> ACTION
    DECISION3 --> ACTION
    DECISION4 --> ACTION
    
    style FLINK fill:#fef3c7,stroke:#d97706
    style ACTION fill:#d1fae5,stroke:#059669
</div>

#### Uber's Real-Time Use Cases with Flink

**1. Surge Pricing (Real-Time)**
```
Input: Ride requests per minute per zone
Processing:
- Count requests in last 5 minutes
- Compare to available drivers
- Calculate supply/demand ratio
- Determine surge multiplier

Output: Updated pricing every 30 seconds
Latency: < 100ms
```

**2. Fraud Detection (Real-Time)**
```
Input: Payment transaction
Processing:
- Check against known fraud patterns
- Verify card/user history
- Calculate risk score
- Approve or flag

Output: Approve/Reject decision
Latency: < 50ms (must be instant!)
```

**3. Driver-Rider Matching (Real-Time)**
```
Input: New ride request
Processing:
- Find drivers within 5 miles
- Calculate ETA for each driver
- Consider driver rating, preferences
- Select best match

Output: Matched driver
Latency: < 200ms
```

**4. Real-Time Dashboards**
```
Input: All events (rides, GPS, payments)
Processing:
- Aggregate by city, time, type
- Calculate KPIs (rides/minute, revenue/hour)
- Detect anomalies

Output: Live dashboard metrics
Latency: < 500ms
```

---

## Part 6: The Analytics & Query Layer

### Apache Pinot — The Speed Demon for Analytics

> **Think of Pinot as:** A super-smart librarian who can answer complex questions about billions of books in under a second.

#### What Problem Does It Solve?

**The analytics problem:**
```
Question: "How many rides in NYC in the last hour?"

HDFS/Hudi:
- Scan entire dataset (terabytes)
- Filter for NYC
- Filter for last hour
- Count results
Time: 5-10 minutes ❌

Pinot:
- Pre-indexed data
- Knows exactly where NYC data is
- Instant filtering
Time: 100-500 milliseconds ✅
```

#### How Pinot Achieves Speed

**Secret 1: Columnar Storage**
```
Normal database stores rows:
[John, 25, NYC] [Jane, 30, LA] [Bob, 28, CHI]

To count people from NYC:
- Must read every row
- Check city for each
- Slow!

Pinot stores columns:
Names: [John, Jane, Bob]
Ages:  [25, 30, 28]
Cities: [NYC, LA, CHI]

To count people from NYC:
- Only read Cities column
- Much faster!
```

**Secret 2: Pre-Aggregation**
```
Instead of calculating on the fly:
"Count rides in NYC last hour" (takes minutes)

Pinot pre-calculates:
- Rides per minute per city
- Updated in real-time
- Query just reads pre-computed value
- Instant!
```

#### What Uber Uses Pinot For

**1. Real-Time Dashboards**
```sql
-- Business teams query instantly:
SELECT 
  city,
  COUNT(*) as rides,
  AVG(fare) as avg_fare,
  SUM(fare) as total_revenue
FROM trips
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY city

Query time: 200ms
Updates: Every 10 seconds
```

**2. Operational Monitoring**
```sql
-- Monitor system health:
SELECT 
  COUNT(*) as failed_payments,
  AVG(response_time) as latency
FROM events
WHERE event_type = 'payment_failed'
  AND timestamp > NOW() - INTERVAL '5 minutes'

Query time: 100ms
Critical for: Detecting outages
```

**3. Ad-Hoc Analysis**
```
Product managers can explore data:
- "Show me peak demand times by city"
- "Compare weekend vs weekday rides"
- "Find highest-earning drivers"

All queries return in < 1 second!
```

### Presto — The Universal Query Tool

> **Think of Presto as:** A universal translator that lets you ask questions about data stored anywhere, in any format, using simple English-like queries (SQL).

#### What Problem Does It Solve?

**The data silo problem:**
```
Uber's data is everywhere:
- Ride data in HDFS
- User profiles in PostgreSQL
- Real-time metrics in Pinot
- Logs in Elasticsearch

Traditional approach:
- Learn different tools for each system
- Write different code for each
- Complex and error-prone

Presto solution:
- One tool to query everything
- Simple SQL language
- Joins across different systems
```

#### Real Example: Cross-System Query

```sql
-- Join data from multiple systems:
SELECT 
  u.name,
  u.signup_date,
  COUNT(t.trip_id) as total_trips,
  AVG(t.fare) as avg_fare
FROM postgres.users u  -- PostgreSQL database
JOIN hdfs.trips t      -- HDFS data lake
  ON u.user_id = t.user_id
WHERE u.city = 'NYC'
GROUP BY u.name, u.signup_date

-- Presto handles all the complexity!
-- Data engineers write simple SQL
```

#### What Uber Uses Presto For

| Use Case | Data Sources | Why Presto? |
|----------|--------------|-------------|
| **User Analytics** | PostgreSQL + HDFS + Pinot | Join user profiles with trip history |
| **Data Science** | HDFS + S3 + Hive | Access all data with SQL |
| **Business Intelligence** | All systems | One tool for all reports |
| **Ad-Hoc Queries** | Any data source | Quick exploration |

---

## How Everything Works Together

Let's follow a single ride through Uber's entire data infrastructure:

### Timeline of a Ride

```
10:00:00 - Rider opens app
├─ Kafka: Captures "app_opened" event
├─ Flink: Updates real-time "active users" count
└─ Pinot: Dashboard shows +1 active user

10:00:30 - Rider requests ride
├─ Kafka: Captures "ride_requested" event
├─ Flink: Matches with nearest driver (200ms)
├─ Pinot: Dashboard shows +1 pending ride
└─ HDFS: Stores request details

10:01:00 - Driver accepts
├─ Kafka: Captures "ride_accepted" event
├─ Flink: Notifies rider, starts ETA calculation
└─ Pinot: Dashboard updates ride status

10:01:00-10:15:00 - Trip in progress
├─ Kafka: Captures GPS updates (every second)
├─ Flink: Updates ETA in real-time
├─ HDFS: Stores GPS trace
└─ Pinot: Dashboard shows active trips

10:15:00 - Trip completes
├─ Kafka: Captures "ride_completed" event
├─ Flink: Processes payment in real-time
├─ Hudi: Stores complete trip record
├─ Pinot: Dashboard shows completed trip
└─ HDFS: Archives all data

Overnight (02:00 AM)
└─ Spark: Calculates driver earnings, surge patterns, reports

Next Morning (08:00 AM)
├─ Driver sees earnings in app (from Spark job)
├─ Business team sees reports (from Pinot)
└─ Data scientists query data (using Presto)
```

### The Complete Architecture

<div class="mermaid">
flowchart TD
    APPS["Uber Apps<br/>Riders & Drivers"] --> KAFKA["Apache Kafka<br/>Event Streaming"]
    
    KAFKA --> FLINK["Apache Flink<br/>Real-Time Processing"]
    KAFKA --> SPARK["Apache Spark<br/>Batch Processing"]
    
    FLINK --> HDFS["HDFS<br/>Raw Storage"]
    SPARK --> HDFS
    
    HDFS --> HUDI["Apache Hudi<br/>Smart Data Lake"]
    
    HUDI --> PINOT["Apache Pinot<br/>Fast Analytics"]
    HUDI --> PRESTO["Presto<br/>SQL Queries"]
    
    PINOT --> DASHBOARDS["Real-Time<br/>Dashboards"]
    PRESTO --> REPORTS["Reports &<br/>Analysis"]
    
    FLINK -.->|Real-time alerts| APPS
    SPARK -.->|Daily updates| APPS
    
    style KAFKA fill:#fef3c7,stroke:#d97706
    style HDFS fill:#d1fae5,stroke:#059669
    style HUDI fill:#dbeafe,stroke:#2563eb
    style DASHBOARDS fill:#fce7f3,stroke:#db2777
</div>

---

## The Numbers: Uber's Scale

### Infrastructure Scale

| Metric | Scale | Context |
|--------|-------|---------|
| **Daily Events** | 100+ billion | That's 1,000,000+ per second |
| **Data Storage** | Multiple petabytes | 1 PB = 1,000,000 GB |
| **Kafka Throughput** | 1,000,000+ events/sec | Never loses data |
| **HDFS Servers** | Thousands | Across multiple data centers |
| **Spark Jobs** | 100,000+ per day | Processing in parallel |
| **Flink Latency** | < 100ms | Real-time decisions |
| **Pinot Query Time** | 100-500ms | Billions of records |
| **Data Retention** | Years | For compliance & ML training |

### Cost & Complexity

| Aspect | Reality |
|--------|---------|
| **Infrastructure Cost** | $100+ million/year |
| **Data Engineers** | 300+ engineers |
| **Servers** | Thousands of machines |
| **Data Centers** | Multiple global locations |
| **Complexity** | Very high (7 major systems) |
| **Maintenance** | 24/7 on-call teams |

---

## Key Lessons Learned

### Lesson 1: Start Simple!

> **Uber's Reality:** This infrastructure wasn't built in a day. They started with simple databases and gradually added complexity as they grew.

**Startup Journey:**
```
Year 1 (10K users):
- Simple PostgreSQL
- Cost: $100/month
- Team: 1 engineer

Year 2 (100K users):
- PostgreSQL + Redis cache
- Cost: $1,000/month
- Team: 2-3 engineers

Year 3 (1M users):
- PostgreSQL + Redis + Kafka
- Cost: $10,000/month
- Team: 5-10 engineers

Year 5 (10M users):
- Started building custom infrastructure
- Cost: $100,000+/month
- Team: 50+ engineers

Year 10 (100M users):
- Full custom stack (Kafka, HDFS, Spark, etc.)
- Cost: $100M+/year
- Team: 300+ engineers
```

**Don't build Uber's infrastructure until you have Uber's scale!**

### Lesson 2: Specialize Systems for Different Jobs

> **Why Uber uses 7 different systems:** Each tool solves a specific problem better than a general-purpose solution.

| System | Job | Why Specialized? |
|--------|-----|------------------|
| **Kafka** | Event streaming | 100x faster than database writes |
| **HDFS** | Storage | Stores petabytes, regular disks can't |
| **Hudi** | Updates | HDFS can't update, Hudi can |
| **Spark** | Batch processing | 1000x faster with parallel processing |
| **Flink** | Real-time | Millisecond latency, Spark takes hours |
| **Pinot** | Analytics | Sub-second queries on billions of rows |
| **Presto** | Queries | Query any system with SQL |

### Lesson 3: Real-Time vs Batch Processing

> **Different problems need different speeds:**

**Real-Time (Flink):**
```
Use when:
- Need instant decisions (< 1 second)
- User-facing features
- Critical operations

Examples:
- Surge pricing
- Driver matching
- Fraud detection
- Payment processing

Cost: More expensive (always running)
```

**Batch (Spark):**
```
Use when:
- Can wait hours for results
- Processing large datasets
- Background jobs

Examples:
- Daily reports
- Earnings calculations
- ML model training
- Data cleanup

Cost: Cheaper (runs periodically)
```

### Lesson 4: Data Never Lies... If You Keep It All

> **Uber's philosophy:** Store everything forever. You never know what data you'll need later.

**Benefits of keeping all data:**
```
✅ Can replay events (reprocess with new logic)
✅ Train ML models on historical data
✅ Debug production issues months later
✅ Comply with audits/regulations
✅ Discover new insights from old data

Cost: Storage is cheap ($20/TB/month)
Value: Insights are priceless
```

---

## Challenges Uber Faced

### Challenge 1: Complexity

**Problem:**
```
Managing 7 different systems:
- Each needs separate expertise
- Different upgrade cycles
- Complex interactions
- 24/7 monitoring needed

Result: 300+ engineers just to keep systems running
```

### Challenge 2: Cost

**Problem:**
```
Annual infrastructure costs:
- Server hardware: $50M
- Data centers: $30M
- Network: $20M
- Maintenance: $10M
- Engineers: $50M (salaries)
Total: $160M/year
```

### Challenge 3: Global Expansion

**Problem:**
```
To expand to new country:
- Build/rent data center
- Ship hardware
- Install and configure
- Hire local engineers
Time: 6-12 months
Cost: $10-50M per region
```

### Challenge 4: Scalability Bottlenecks

**Problem:**
```
Growing faster than infrastructure:
- Order servers (3-6 months lead time)
- Capacity planning nightmares
- Risk of running out of space
- Over-provisioning wastes money
```

These challenges led Uber to modernize...

---

## What's Next?

This infrastructure powered Uber for years, but by 2020, they faced serious challenges:
- **Too complex** (300+ engineers needed)
- **Too expensive** ($160M+/year)
- **Slow to scale** (months to add capacity)
- **Hard to expand globally** (rebuild everything per region)

**The solution?** Move to Google Cloud Platform and simplify everything.

**Continue to:** [Part 2 - Modernizing with Google Cloud →]({{ site.baseurl }}{% link _topics/uber-data-infrastructure-part-2-modernization.md %})

---

## Summary: The Original Uber Data Stack

### The Architecture

```
Layer 1: Collection
- Kafka: Capture all events (1M+/sec)

Layer 2: Storage
- HDFS: Store petabytes of data

Layer 3: Smart Storage
- Hudi: Enable updates and time travel

Layer 4: Processing
- Spark: Batch processing (overnight)
- Flink: Real-time processing (milliseconds)

Layer 5: Analytics
- Pinot: Fast analytics (sub-second)
- Presto: Universal SQL queries
```

### Key Takeaways

1. **Specialized systems** beat general-purpose at scale
2. **Start simple** — add complexity only when needed
3. **Real-time vs batch** — use the right tool for the job
4. **Store everything** — data is valuable forever
5. **Expect challenges** — scale brings complexity and cost

### By the Numbers

- 📊 **137 million** monthly active users
- 🔄 **1 million+** events per second
- 💾 **Multiple petabytes** of data stored
- ⚡ **< 100ms** real-time processing
- 💰 **$160M+/year** infrastructure cost
- 👥 **300+** engineers to manage

**Next:** Learn how Uber modernized this entire stack with Google Cloud Platform, reducing complexity by 50% and costs by 40%!

→ [Part 2 - Modernizing with Google Cloud]({{ site.baseurl }}{% link _topics/uber-data-infrastructure-part-2-modernization.md %})

---

## Further Reading

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Hadoop HDFS Architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [Apache Hudi Documentation](https://hudi.apache.org/docs/overview)
- [Apache Spark Overview](https://spark.apache.org/docs/latest/)
- [Apache Flink Architecture](https://flink.apache.org/flink-architecture.html)
- [Apache Pinot Documentation](https://docs.pinot.apache.org/)
- [Presto Documentation](https://prestodb.io/docs/current/)