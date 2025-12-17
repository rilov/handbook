---
title: "Scaling Your API Part 3: Choosing the Right Database"
category: Architecture
tags:
  - databases
  - architecture
  - api
  - scaling
  - performance
series: "Scaling Your API"
part: 3
summary: Learn how to choose the right database for your API — from handling thousands to millions of requests per second.
related:
  - scaling-api-1-to-1-million-rps
  - scaling-api-design-architecture-part-2
  - scaling-api-load-balancing-part-4
  - scaling-api-monitoring-part-5
---

> **📚 This is Part 3 of the "Scaling Your API" Series**
> - **[Part 1: Performance & Infrastructure ←]({{ site.baseurl }}{% link _topics/scaling-api-1-to-1-million-rps.md %})** - Technical techniques to handle millions of requests
> - **[Part 2: Design & Architecture ←]({{ site.baseurl }}{% link _topics/scaling-api-design-architecture-part-2.md %})** - Organizational strategies and API design patterns
> - **Part 3 (this page):** Choosing the Right Database - Database selection for your API
> - **[Part 4: Load Balancing & High Availability →]({{ site.baseurl }}{% link _topics/scaling-api-load-balancing-part-4.md %})** - Keeping your API always available
> - **[Part 5: Monitoring & Performance →]({{ site.baseurl }}{% link _topics/scaling-api-monitoring-part-5.md %})** - Tracking and improving API performance
> 
> You've designed your API and thought about scaling strategies. Now comes the most critical decision: **choosing the right database.** Your database choice will determine your API's speed, scalability, and reliability.
> 
> **Think of it like this:** Your API is a restaurant's waitstaff, and your database is the kitchen. Even the best waiters can't serve food fast if the kitchen is slow!

## Why Database Selection Matters for APIs

When building APIs, your database directly impacts:

- **Response Time:** Can you respond in < 100ms?
- **Throughput:** Can you handle 10,000 requests/second?
- **Concurrency:** Can 1,000 users access data simultaneously?
- **Scalability:** Can you grow from 1K to 1M users?
- **Reliability:** What happens if your database crashes?

**The harsh truth:** A bad database choice can kill your API's performance, no matter how well-designed your code is.

## The API Database Landscape

<div class="mermaid">
flowchart TD
    START["🚀 What's your API serving?"]
    
    START --> REST["REST API<br/>(CRUD operations)"]
    START --> REALTIME["Real-time API<br/>(live updates)"]
    START --> SEARCH["Search API<br/>(text queries)"]
    START --> ANALYTICS["Analytics API<br/>(aggregations)"]
    
    REST --> SQL["SQL Database<br/>(PostgreSQL)"]
    REALTIME --> COMBO["NoSQL + Cache<br/>(MongoDB + Redis)"]
    SEARCH --> ELASTIC["Search Engine<br/>(Elasticsearch)"]
    ANALYTICS --> COLUMNAR["Column Store<br/>(Cassandra/ClickHouse)"]
    
    style START fill:#dbeafe,stroke:#2563eb
    style SQL fill:#d1fae5,stroke:#059669
    style COMBO fill:#fef3c7,stroke:#d97706
    style ELASTIC fill:#fce7f3,stroke:#db2777
    style COLUMNAR fill:#e0e7ff,stroke:#6366f1
</div>

## API Performance Requirements

Before choosing a database, understand your API's performance needs:

| Metric | Low Volume | Medium Volume | High Volume |
|--------|------------|---------------|-------------|
| **Requests/sec** | < 100 | 100 - 10,000 | > 10,000 |
| **Response Time** | < 500ms | < 200ms | < 100ms |
| **Concurrent Users** | < 1,000 | 1,000 - 100,000 | > 100,000 |
| **Data Size** | < 10 GB | 10 GB - 1 TB | > 1 TB |
| **Database Choice** | Any SQL | SQL + Cache | NoSQL + Cache + CDN |

**Key Insight:** Most APIs start in "Low Volume" and need to scale. Choose a database that can grow with you!

---

## 1. Relational Databases (SQL) — The API Workhorse

> **For APIs:** The default choice for 90% of REST APIs. Reliable, proven, and powerful.

### Perfect For These API Endpoints

```
GET  /api/users/:id          → Fast single record lookup
GET  /api/orders?userId=123  → Filtered queries with relationships
POST /api/checkout           → Transactions (all-or-nothing)
PUT  /api/users/:id          → Updates with validation
```

### API Performance Characteristics

| Metric | Performance |
|--------|-------------|
| **Read Latency** | 1-10ms (with proper indexes) |
| **Write Latency** | 5-50ms |
| **Concurrent Connections** | 100-1,000 (single server) |
| **Throughput** | 1,000-10,000 req/sec |
| **Scalability** | Vertical (bigger server) |

### When to Use for Your API

- ✅ Your API serves structured data (users, orders, products)
- ✅ You need ACID transactions (payments, bookings)
- ✅ Your data has relationships (users → orders → products)
- ✅ You need complex queries (filtering, sorting, joining)
- ✅ Your API handles < 10,000 requests/second

### When to Consider Alternatives

- ❌ You need > 100,000 requests/second
- ❌ Your API response time > 100ms even with optimization
- ❌ Your data model changes every week
- ❌ You need to scale horizontally across 100+ servers

### Popular Options for APIs

| Database | API Response Time | Scaling | Best For |
|----------|------------------|---------|----------|
| **PostgreSQL** | 5-20ms | Vertical (10K req/s) | Most REST APIs, complex queries |
| **MySQL** | 3-15ms | Vertical (15K req/s) | Simple CRUD APIs, read-heavy |
| **CockroachDB** | 10-50ms | Horizontal (100K+ req/s) | Global APIs, multi-region |
| **Amazon Aurora** | 5-20ms | Auto-scaling | AWS-based APIs, serverless |
| **PlanetScale** | 5-15ms | Serverless scaling | Modern APIs, easy scaling |

**💡 API Recommendation:** Start with PostgreSQL. Migrate to CockroachDB/Aurora when you outgrow a single server.

### API Code Example

```javascript
// Express.js API with PostgreSQL
app.get('/api/users/:id', async (req, res) => {
  const user = await db.query(
    'SELECT * FROM users WHERE id = $1',
    [req.params.id]
  );
  res.json(user); // Typical response time: 5-20ms
});

// With proper indexing + connection pooling:
// - Handles 5,000-10,000 requests/second
// - 95th percentile latency < 50ms
```

---

## 2. Document Databases (NoSQL) — Flexible & Fast

> **For APIs:** Choose when your API needs flexibility and high write throughput.

### What They Store

Documents (usually JSON format) that can have different fields.

**Real-World Example:**
```json
// User 1 (has address)
{
  "name": "John",
  "email": "john@example.com",
  "address": {
    "city": "NYC",
    "country": "USA"
  }
}

// User 2 (no address, has phone)
{
  "name": "Jane",
  "email": "jane@example.com",
  "phone": "+1-555-0123"
}
```

### API Performance Characteristics

| Metric | Performance |
|--------|-------------|
| **Read Latency** | 1-5ms |
| **Write Latency** | 1-10ms |
| **Concurrent Connections** | 10,000+ |
| **Throughput** | 50,000-500,000 req/sec |
| **Scalability** | Horizontal (add servers) |

### When to Use for Your API

- ✅ Your API serves flexible data (user profiles, product catalogs)
- ✅ You need high write throughput (logging, analytics)
- ✅ Your API needs to scale horizontally
- ✅ Your data is naturally nested (user → settings → preferences)
- ✅ You're building fast and iterating quickly

### When to Stick with SQL

- ❌ You need complex joins across tables
- ❌ You need strong ACID transactions (payments)
- ❌ Your team is unfamiliar with NoSQL
- ❌ Your data is highly relational

### Popular Options for APIs

| Database | API Response Time | Scaling | Best For |
|----------|------------------|---------|----------|
| **MongoDB** | 2-10ms | Horizontal | General-purpose APIs, flexible data |
| **Amazon DynamoDB** | 1-5ms | Auto-scaling | Serverless APIs, AWS Lambda |
| **Firebase/Firestore** | 50-200ms | Auto-scaling | Mobile APIs, real-time sync |
| **Couchbase** | 1-5ms | Horizontal | High-performance APIs, caching |

**💡 API Recommendation:** MongoDB for self-hosted, DynamoDB for serverless AWS APIs.

### API Code Example

```javascript
// Express.js API with MongoDB
app.get('/api/products/:id', async (req, res) => {
  const product = await Product.findById(req.params.id);
  res.json(product); // Response time: 2-10ms
});

// Benefits for APIs:
// - Schema flexibility (add fields anytime)
// - Fast reads/writes (1-10ms)
// - Easy horizontal scaling
// - Handles 50K+ requests/second
```

---

## 3. Key-Value Stores — API Speed Boost

> **For APIs:** Essential for caching and reducing database load. Can turn 50ms responses into 1ms responses!

### What They're Good For

Lightning-fast storage and retrieval of simple data.

**Real-World Example:**
```
Key: "session:abc123"
Value: {"user_id": 456, "logged_in": true}

Key: "cart:user456"
Value: ["item1", "item2", "item3"]
```

### API Performance Characteristics

| Metric | Performance |
|--------|-------------|
| **Read Latency** | < 1ms (sub-millisecond) |
| **Write Latency** | < 1ms |
| **Concurrent Connections** | 100,000+ |
| **Throughput** | 1,000,000+ req/sec |
| **Scalability** | Horizontal |

### When to Use for Your API

- ✅ **Caching:** Store frequently accessed data (80% of API calls hit cache)
- ✅ **Session Management:** Store user sessions, JWT tokens
- ✅ **Rate Limiting:** Track API request counts per user
- ✅ **Real-time Features:** Leaderboards, counters, live updates
- ✅ **Reduce Database Load:** Cache database query results

### When NOT to Use as Primary Database

- ❌ You need to query/filter data
- ❌ You need data persistence guarantees
- ❌ You need complex queries

### Popular Options for APIs

| Database | API Response Time | Use Case |
|----------|------------------|----------|
| **Redis** | < 1ms | API caching, sessions, rate limiting |
| **Memcached** | < 1ms | Simple API caching only |
| **Amazon ElastiCache** | < 1ms | AWS API caching |
| **Dragonfly** | < 0.5ms | Drop-in Redis replacement (faster) |

**💡 API Recommendation:** Every API should use Redis for caching. Period.

### API Code Example

```javascript
// API with Redis caching
app.get('/api/products/:id', async (req, res) => {
  // Try cache first
  const cached = await redis.get(`product:${req.params.id}`);
  if (cached) {
    return res.json(JSON.parse(cached)); // 1ms response!
  }
  
  // Cache miss: query database
  const product = await db.query('SELECT * FROM products WHERE id = $1');
  
  // Store in cache for 5 minutes
  await redis.setex(`product:${req.params.id}`, 300, JSON.stringify(product));
  
  res.json(product); // 20ms first time, 1ms afterwards
});

// Result: 80% of requests served from cache = 20x faster!
```

---

## 4. Column-Family Stores

> **Think of it like:** Instead of storing entire rows together, you store columns together. Great for reading specific columns from billions of rows.

### What They're Good For

Massive amounts of data where you read specific columns.

**Real-World Example:**
```
Instead of storing:
[John, 25, NYC] [Jane, 30, LA] [Bob, 28, CHI]

Store like:
Names: [John, Jane, Bob]
Ages:  [25, 30, 28]
Cities: [NYC, LA, CHI]
```

### When to Use

- ✅ You have billions of rows
- ✅ You query specific columns (not full rows)
- ✅ Time-series data (sensor readings, logs)
- ✅ You need to write massive amounts of data fast

### When NOT to Use

- ❌ You frequently need entire rows
- ❌ You have complex queries with joins
- ❌ Your data fits in memory

### Popular Options

| Database | Best For | Used By |
|----------|----------|---------|
| **Apache Cassandra** | Massive scale, always available | Netflix, Apple, Discord |
| **HBase** | Hadoop ecosystem | Adobe, Salesforce |
| **ScyllaDB** | High performance Cassandra alternative | Discord, Comcast |
| **Amazon Keyspaces** | Managed Cassandra on AWS | AWS customers |

**💡 Best for:** Massive scale applications like Netflix or Uber.

---

## 5. Search Engines

> **Think of it like:** Google for your data. You can search text, filter, aggregate, and find things super fast.

### What They're Good For

Full-text search, log analysis, complex queries.

**Real-World Example:**
```
Search: "smartphone under $500"
Results: All phones matching criteria, sorted by relevance

Search logs: "ERROR" in the last hour
Results: All error logs with context
```

### When to Use

- ✅ You need full-text search (search boxes on websites)
- ✅ You need to analyze logs (find errors, patterns)
- ✅ You need faceted search (filters on e-commerce sites)
- ✅ You need autocomplete, fuzzy matching, suggestions

### When NOT to Use

- ❌ As your primary database (use it alongside one)
- ❌ For transactional data
- ❌ When you don't need search features

### Popular Options

| Database | Best For | Used By |
|----------|----------|---------|
| **Elasticsearch** | Modern choice, great features | Netflix, Uber, Microsoft |
| **Apache Solr** | Enterprise search | Apple, Netflix, AT&T |
| **Amazon OpenSearch** | Managed Elasticsearch on AWS | AWS customers |
| **Algolia** | Instant search-as-a-service | Twitch, Stripe, Slack |

**💡 Most popular:** Elasticsearch — powerful, scalable, great ecosystem.

---

## 6. Graph Databases

> **Think of it like:** Facebook's friend network. It's all about relationships — who knows who, what's connected to what.

### What They're Good For

Data where relationships are as important as the data itself.

**Real-World Example:**
```
John --[FRIENDS_WITH]--> Jane
Jane --[WORKS_AT]--> Google
Google --[LOCATED_IN]--> California
John --[LIKES]--> Pizza
Jane --[LIKES]--> Pizza
```

### When to Use

- ✅ Social networks (who knows who)
- ✅ Recommendation engines (people who bought X also bought Y)
- ✅ Fraud detection (finding suspicious patterns)
- ✅ Knowledge graphs (how concepts relate)

### When NOT to Use

- ❌ Simple data without complex relationships
- ❌ You just need to store and retrieve records
- ❌ You don't need to traverse relationships

### Popular Options

| Database | Best For | Used By |
|----------|----------|---------|
| **Neo4j** | Most popular, great tools | eBay, Walmart, NASA |
| **Amazon Neptune** | Managed graph on AWS | AWS customers |
| **ArangoDB** | Multi-model (graph + document) | Startups |
| **TigerGraph** | Large-scale analytics | Banks, healthcare |

**💡 Start here:** Neo4j — excellent documentation and community.

---

## 7. Time-Series Databases

> **Think of it like:** A database optimized for data that changes over time — like temperature readings every minute or stock prices every second.

### What They're Good For

Data that's timestamped and constantly arriving.

**Real-World Example:**
```
2024-01-01 10:00:00 | Temperature: 72°F
2024-01-01 10:01:00 | Temperature: 72.5°F
2024-01-01 10:02:00 | Temperature: 73°F
```

### When to Use

- ✅ IoT sensor data (temperature, pressure, motion)
- ✅ Application metrics (CPU, memory, requests)
- ✅ Financial data (stock prices, trades)
- ✅ You need to analyze trends over time

### When NOT to Use

- ❌ Your data isn't timestamped
- ❌ You don't analyze time-based patterns
- ❌ You rarely query by time ranges

### Popular Options

| Database | Best For | Used By |
|----------|----------|---------|
| **InfluxDB** | General purpose, easy to use | Cisco, IBM, eBay |
| **TimescaleDB** | PostgreSQL extension | Comcast, IBM, Walmart |
| **Prometheus** | Monitoring and alerting | SoundCloud, Docker |
| **Amazon Timestream** | Managed on AWS | AWS customers |

**💡 Best choice:** InfluxDB for IoT, TimescaleDB if you already use PostgreSQL.

---

## 8. Vector Databases

> **Think of it like:** A database for AI. Stores data as numbers (vectors) and finds similar items super fast.

### What They're Good For

AI/ML applications, similarity search, recommendations.

**Real-World Example:**
```
"Find images similar to this photo"
"Find products similar to what this user liked"
"Find documents related to this topic"
```

### When to Use

- ✅ Building AI-powered search (ChatGPT-like features)
- ✅ Recommendation systems (similar products/content)
- ✅ Image/video similarity search
- ✅ Semantic search (search by meaning, not keywords)

### When NOT to Use

- ❌ You're not building AI features
- ❌ You don't need similarity search
- ❌ Traditional keyword search is enough

### Popular Options

| Database | Best For | Used By |
|----------|----------|---------|
| **Pinecone** | Easiest, fully managed | AI startups |
| **Weaviate** | Open source, flexible | Enterprises |
| **Milvus** | High performance, scalable | AI companies |
| **Qdrant** | Fast, modern | ML applications |
| **pgvector** | PostgreSQL extension | Existing Postgres users |

**💡 Trending:** Pinecone for ease of use, pgvector if you want to stay in PostgreSQL.

---

## 9. In-Memory Databases

> **Think of it like:** Everything stored in RAM (super fast memory) instead of disk. Like keeping your tools in your hand instead of in the garage.

### What They're Good For

Extreme speed when you need microsecond response times.

### When to Use

- ✅ High-frequency trading (stocks)
- ✅ Real-time bidding (ads)
- ✅ Gaming leaderboards
- ✅ Fraud detection (real-time)

### When NOT to Use

- ❌ You have huge amounts of data (RAM is expensive)
- ❌ Speed isn't critical
- ❌ You need data to persist long-term

### Popular Options

| Database | Best For | Used By |
|----------|----------|---------|
| **Redis** | Caching, data structures | Twitter, GitHub |
| **Memcached** | Simple caching | Facebook, Wikipedia |
| **Apache Ignite** | Distributed computing | Banks, retail |
| **VoltDB** | High-speed transactions | Telecom, finance |

**💡 Most common:** Redis (it's both key-value AND in-memory).

---

## Quick Decision Tree

<div class="mermaid">
flowchart TD
    START["🤔 Choose Your Database"]
    
    START --> Q1{"Is your data<br/>structured in tables?"}
    
    Q1 --> |"Yes"| Q2{"Need to scale<br/>to billions of records?"}
    Q2 --> |"No"| SQL["PostgreSQL<br/>or MySQL"]
    Q2 --> |"Yes"| SCALE["Cassandra<br/>or CockroachDB"]
    
    Q1 --> |"No"| Q3{"What type of data?"}
    
    Q3 --> |"Flexible documents"| MONGO["MongoDB"]
    Q3 --> |"Just key-value pairs"| REDIS["Redis"]
    Q3 --> |"Time-series"| INFLUX["InfluxDB"]
    Q3 --> |"Relationships/Network"| NEO4J["Neo4j"]
    Q3 --> |"Text/logs to search"| ELASTIC["Elasticsearch"]
    Q3 --> |"AI/embeddings"| VECTOR["Pinecone"]
    
    style START fill:#dbeafe,stroke:#2563eb
    style SQL fill:#d1fae5,stroke:#059669
    style MONGO fill:#fef3c7,stroke:#d97706
    style ELASTIC fill:#fce7f3,stroke:#db2777
</div>

---

## Real-World API Architectures

### Scenario 1: E-Commerce API (10,000 req/s)

**API Endpoints:**
```
GET  /api/products          → List products
GET  /api/products/:id      → Get product details
POST /api/checkout          → Process order
GET  /api/search?q=laptop   → Search products
```

**Database Stack:**
```
PostgreSQL:     Store products, users, orders
                - Response time: 10-20ms
                - Connection pool: 100
                
Redis:          Cache product details, shopping carts
                - Response time: 1ms
                - Hit rate: 80%
                
Elasticsearch:  Product search API
                - Response time: 50-100ms
                - Handles complex queries

Result: Average API response time: 5-15ms
```

---

### Scenario 2: Social Media API (100,000 req/s)

**API Endpoints:**
```
GET  /api/feed              → Get user feed
POST /api/posts             → Create post
GET  /api/users/:id         → Get profile
GET  /api/notifications     → Get notifications
```

**Database Stack:**
```
MongoDB:        User profiles, posts (flexible schema)
                - Write: 2-5ms
                - Read: 2-10ms
                - Sharded across 10 servers
                
Redis:          Real-time notifications, session cache
                - Response time: < 1ms
                - Pub/sub for live updates
                
Cassandra:      Activity logs (high write volume)
                - Write: 1-2ms
                - Handles 500K writes/sec

Result: API handles 100K+ requests/second
```

---

### Scenario 3: Analytics API (High Volume Reads)

**API Endpoints:**
```
GET  /api/metrics?timeRange=7d    → Get metrics
GET  /api/reports/:id             → Get report
POST /api/events                  → Log event
```

**Database Stack:**
```
ClickHouse:     Time-series analytics
                - Query time: 100-500ms
                - Billion rows in seconds
                
PostgreSQL:     Metadata, user accounts
                - Response time: 5-15ms
                
Redis:          Cache aggregated results
                - Response time: 1ms
                - Cache for 5 minutes

Result: Complex analytics served in < 200ms
```

---

### Scenario 4: Banking API (ACID Critical)

**API Endpoints:**
```
POST /api/transfer          → Transfer money
GET  /api/balance           → Get balance
GET  /api/transactions      → Transaction history
```

**Database Stack:**
```
PostgreSQL:     Primary database (ACID guarantee)
                - All transactions in DB transactions
                - Response time: 20-50ms
                - Read replicas for scaling
                
Redis:          Session management only
                - No financial data in cache!
                
TimescaleDB:    Transaction history analysis
                - Fast time-series queries

Result: 100% data integrity, 10K req/s
```

---

## Comparison Table

| Database Type | Speed | Scalability | Complexity | Best Use Case |
|--------------|-------|-------------|------------|---------------|
| **SQL (PostgreSQL)** | Medium | Medium | Low | Most applications |
| **Document (MongoDB)** | Fast | High | Medium | Flexible data |
| **Key-Value (Redis)** | Very Fast | High | Very Low | Caching |
| **Column (Cassandra)** | Fast | Very High | High | Massive scale |
| **Search (Elasticsearch)** | Fast | High | Medium | Search & logs |
| **Graph (Neo4j)** | Medium | Medium | Medium | Relationships |
| **Time-Series (InfluxDB)** | Fast | High | Low | Sensor data |
| **Vector (Pinecone)** | Fast | High | Medium | AI features |

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Using MongoDB When You Need PostgreSQL

```
Bad: Using MongoDB for highly structured, relational data
Good: Use PostgreSQL when data has clear relationships
```

**Why:** MongoDB is great for flexibility, but if your data is structured, SQL databases are simpler and more powerful.

### ❌ Mistake 2: Using PostgreSQL as a Cache

```
Bad: Caching frequently accessed data in PostgreSQL
Good: Use Redis for caching, PostgreSQL for persistent data
```

**Why:** Redis is 10-100x faster for caching.

### ❌ Mistake 3: Using Elasticsearch as Primary Database

```
Bad: Storing all your data only in Elasticsearch
Good: Store in PostgreSQL/MongoDB, sync to Elasticsearch for search
```

**Why:** Elasticsearch is a search engine, not a database. Use it alongside your primary database.

### ❌ Mistake 4: Choosing Based on Hype

```
Bad: "Everyone uses MongoDB, let's use it!"
Good: Analyze your actual needs and choose accordingly
```

**Why:** Popular doesn't mean right for your use case.

---

## The Safe Default API Stack

If you're just starting your API and unsure, this stack works for 90% of APIs:

```
Primary Database:   PostgreSQL
                   - All your main data
                   - Response time: 5-20ms
                   - Handles 5,000-10,000 req/s

Cache Layer:       Redis
                   - Cache hot data (80% hit rate)
                   - API sessions, rate limiting
                   - Response time: < 1ms

Search (optional): Elasticsearch
                   - Only if you need search endpoints
                   - Response time: 50-100ms
```

**Why this works for APIs:**
- ✅ PostgreSQL handles complex queries, transactions, relationships
- ✅ Redis reduces database load by 80% and speeds up responses 20x
- ✅ Together they handle 10,000+ requests/second easily
- ✅ Can scale vertically (bigger servers) to 50,000 req/s
- ✅ Battle-tested by thousands of companies

**Performance with this stack:**
```
Without Redis:    50ms average response time
With Redis:       5ms average response time (10x faster!)
Database load:    Reduced by 80%
```

---

## API Scaling Path: When to Add/Switch Databases

**Grow your database stack as your API scales:**

```
Phase 1: Starting Out (0-100 req/s)
└── PostgreSQL
    Performance: 10-50ms response time
    Complexity: Low
    Cost: $20-50/month

Phase 2: Getting Traction (100-5,000 req/s)
├── PostgreSQL (add indexes, connection pooling)
└── Redis (cache hot data)
    Performance: 5-15ms response time
    Complexity: Medium
    Cost: $100-300/month

Phase 3: Growing Fast (5,000-50,000 req/s)
├── PostgreSQL (read replicas, bigger server)
├── Redis (cache + session management)
└── Elasticsearch (if you have search endpoints)
    Performance: 2-10ms response time
    Complexity: Medium-High
    Cost: $500-2,000/month

Phase 4: High Scale (50,000-500,000 req/s)
├── PostgreSQL (for critical transactional data)
├── MongoDB or Cassandra (for high-volume data)
├── Redis (distributed cache)
└── Elasticsearch (for search)
    Performance: 1-5ms response time
    Complexity: High
    Cost: $5,000-20,000/month

Phase 5: Massive Scale (500,000+ req/s)
├── PostgreSQL / CockroachDB (critical data)
├── Cassandra / ScyllaDB (high-volume writes)
├── Redis Cluster (distributed caching)
├── Elasticsearch Cluster (search)
└── ClickHouse (analytics)
    Performance: < 1ms response time
    Complexity: Very High
    Cost: $50,000+/month
```

**Key principle for APIs:** Only add complexity when your current setup can't handle the load!

---

## Summary: Database Selection for APIs

> **Quick Takeaways for API Developers:**
> 
> - **Starting your API?** → PostgreSQL + Redis (handles 10K req/s)
> - **Need search endpoints?** → Add Elasticsearch
> - **Flexible data model?** → Consider MongoDB
> - **Need 100K+ req/s?** → Add Cassandra or MongoDB sharding
> - **Real-time features?** → Redis pub/sub
> - **Analytics endpoints?** → Consider ClickHouse or TimescaleDB
> - **AI-powered API?** → Add pgvector or Pinecone

### The Golden Rule for APIs

**Start with PostgreSQL + Redis. This combo handles 95% of APIs up to 10,000 requests/second. Only add more databases when you hit specific bottlenecks.**

### API Performance Checklist

Before adding another database, optimize what you have:

- [ ] Added database indexes on filtered/sorted columns
- [ ] Implemented Redis caching (80% hit rate = 5x faster)
- [ ] Using connection pooling (100-200 connections)
- [ ] Optimized slow queries (use EXPLAIN)
- [ ] Added read replicas for read-heavy endpoints
- [ ] Implemented API rate limiting
- [ ] Using CDN for static data

**Most slow APIs have poorly optimized databases, not the wrong database!**

---

## Continue the Series

This is **Part 3** of the "Scaling Your API" series:

- **[Part 1: Performance & Infrastructure →]({{ site.baseurl }}{% link _topics/scaling-api-1-to-1-million-rps.md %})** - Technical techniques to handle millions of requests
- **[Part 2: Design & Architecture →]({{ site.baseurl }}{% link _topics/scaling-api-design-architecture-part-2.md %})** - Organizational strategies and API design patterns for large-scale systems
- **Part 3:** Choosing the Right Database ← You are here
- **[Part 4: Load Balancing & High Availability →]({{ site.baseurl }}{% link _topics/scaling-api-load-balancing-part-4.md %})** - Keeping your API always available
- **[Part 5: Monitoring & Performance →]({{ site.baseurl }}{% link _topics/scaling-api-monitoring-part-5.md %})** - Tracking and improving API performance

---

## Further Reading

- **[PostgreSQL Official Docs](https://www.postgresql.org/docs/)** — Learn the most versatile database
- **[MongoDB University](https://university.mongodb.com/)** — Free courses on document databases
- **[Redis Documentation](https://redis.io/documentation)** — Master caching and real-time data
- **[Elasticsearch Guide](https://www.elastic.co/guide/)** — Learn search and analytics
- **[Database Rankings](https://db-engines.com/en/ranking)** — See popularity trends

---

**Remember:** The best database for your API is the one that meets your performance requirements simply. Premature optimization is the root of all evil — but so is choosing the wrong database!
