---
title: "Scaling Your API: Part 1 - Performance & Infrastructure"
category: Architecture
tags:
  - scaling
  - performance
  - api
  - infrastructure
summary: A beginner-friendly guide to scaling your API from handling 1 request per second to 1 million, with diagrams and simple explanations.
related:
  - scaling-api-design-architecture-part-2
  - choosing-the-right-database
  - scaling-api-load-balancing-part-4
  - scaling-api-monitoring-part-5
---

> **📚 This is Part 1 of the "Scaling Your API" Series**
> - **Part 1 (this page):** Performance & Infrastructure - Technical techniques to handle millions of requests
> - **[Part 2: Design & Architecture →]({{ site.baseurl }}/topics/scaling-api-design-architecture-part-2/)** - Organizational strategies and API design patterns for large-scale systems
> - **[Part 3: Choosing the Right Database →]({{ site.baseurl }}/topics/choosing-the-right-database/)** - Database selection for your API
> - **[Part 4: Load Balancing & High Availability →]({{ site.baseurl }}/topics/scaling-api-load-balancing-part-4/)** - Keeping your API always available
> - **[Part 5: Monitoring & Performance →]({{ site.baseurl }}/topics/scaling-api-monitoring-part-5/)** - Tracking and improving API performance

## The Journey: 1 RPS → 1,000,000 RPS

Imagine your API is a restaurant. At first, you have one chef (server) handling one order at a time. But what happens when you go viral and suddenly have a million customers waiting?

<div class="mermaid">
flowchart LR
    subgraph before["😰 Before Scaling"]
        U1["👤 User"] --> S1["🖥️ 1 Server"]
        S1 --> D1["🗄️ 1 Database"]
    end
    
    subgraph after["😎 After Scaling"]
        U2["👥 Millions<br/>of Users"] --> LB["⚖️ Load<br/>Balancer"]
        LB --> S2["🖥️ Server 1"]
        LB --> S3["🖥️ Server 2"]
        LB --> S4["🖥️ Server N..."]
        S2 --> C["⚡ Cache"]
        S3 --> C
        S4 --> C
        C --> DB["🗄️ Database<br/>Cluster"]
    end
</div>

---

## Overview: The 14 Key Scaling Techniques

Scaling an API isn't about implementing all techniques at once—it's about choosing the right tools for your current stage. This guide covers 14 proven techniques in order of complexity:

### Foundation (Must-Haves for Every API)
1. **Vertical Scaling** - Start here: upgrade your single server's resources
2. **Connection Pooling** - Reuse database connections instead of opening new ones
3. **Avoid N+1 Queries** - Fetch related data efficiently with joins

### Essential Optimizations (1-10K RPS)
4. **Horizontal Scaling** - Add more servers to distribute the load
5. **Load Balancing** - Intelligently route traffic across servers
6. **Caching** - Store frequently accessed data in memory (Redis/Memcached)
7. **Pagination** - Send data in manageable chunks instead of all at once

### Performance Enhancements (10K-100K RPS)
8. **Fast JSON Serializers** - Use optimized libraries for data serialization
9. **Compression** - Reduce payload sizes with Gzip or Brotli
10. **CDN** - Serve content from edge servers close to users
11. **Async Processing** - Move slow tasks to background workers

### Advanced Scaling (100K+ RPS)
12. **Async Logging** - Make logging non-blocking
13. **Database Sharding** - Split your database horizontally
14. **Rate Limiting** - Protect your system from abuse

### The Three Critical Insights

**1. Start Simple, Scale Progressively**
Don't build for 1M RPS on day one. A single well-optimized server can handle 10,000+ RPS with proper caching and database optimization.

**2. Fix the Bottleneck, Not Everything**
Measure your system to identify the actual bottleneck (CPU? Memory? Database? Network?) and address that specific issue first.

**3. Some Techniques Are Always Worth It**
Connection pooling, avoiding N+1 queries, basic caching, pagination, and compression should be implemented from the start—they're simple and have massive impact.

Let's dive into each technique in detail, starting from the simplest to the most advanced.

---

## Level 1: Vertical Scaling (The Easy Start)

### What is it?

Make your single server bigger and more powerful — more CPU, more RAM, faster disk.

<div class="mermaid">
flowchart LR
    subgraph before["Before"]
        A["🖥️ Small Server<br/>2 CPU, 4GB RAM"]
    end
    
    subgraph after["After"]
        B["🖥️ Big Server<br/>32 CPU, 128GB RAM"]
    end
    
    before -->|💰 Upgrade| after
    
    style A fill:#fecaca,stroke:#dc2626
    style B fill:#d1fae5,stroke:#059669
</div>

### Real-World Analogy

Instead of hiring more chefs, you give your one chef a bigger kitchen with better equipment.

### Limits

- ❌ There's a ceiling — servers can only get so big
- ❌ Single point of failure — if it crashes, everything goes down
- ❌ Expensive at the top end

**Good for:** 1 → 100 RPS

---

## Level 2: Horizontal Scaling (Add More Servers)

### What is it?

Instead of one big server, use many smaller servers working together.

<div class="mermaid">
flowchart TD
    U["👥 Users"] --> LB["⚖️ Load Balancer"]
    LB --> S1["🖥️ Server 1"]
    LB --> S2["🖥️ Server 2"]
    LB --> S3["🖥️ Server 3"]
    LB --> S4["🖥️ Server 4"]
    
    style LB fill:#dbeafe,stroke:#2563eb
    style S1 fill:#d1fae5,stroke:#059669
    style S2 fill:#d1fae5,stroke:#059669
    style S3 fill:#d1fae5,stroke:#059669
    style S4 fill:#d1fae5,stroke:#059669
</div>

### Real-World Analogy

Hire more chefs! Each chef can work independently, handling their own orders.

### Benefits

- ✅ No ceiling — just add more servers
- ✅ No single point of failure — if one dies, others keep working
- ✅ Cost-effective — use cheaper commodity hardware

**Good for:** 100 → 10,000 RPS

---

## Level 3: Load Balancing (Traffic Cop)

### What is it?

A load balancer distributes incoming requests across multiple servers evenly.

<div class="mermaid">
flowchart TD
    subgraph clients["Incoming Requests"]
        R1["Request 1"]
        R2["Request 2"]
        R3["Request 3"]
        R4["Request 4"]
        R5["Request 5"]
        R6["Request 6"]
    end
    
    R1 --> LB
    R2 --> LB
    R3 --> LB
    R4 --> LB
    R5 --> LB
    R6 --> LB
    
    LB["⚖️ Load Balancer"]
    
    LB -->|1, 4| S1["🖥️ Server 1"]
    LB -->|2, 5| S2["🖥️ Server 2"]
    LB -->|3, 6| S3["🖥️ Server 3"]
    
    style LB fill:#fef3c7,stroke:#d97706
</div>

### Common Algorithms

| Algorithm | How it Works | Best For |
|-----------|--------------|----------|
| **Round Robin** | Takes turns: 1→2→3→1→2→3 | Equal server capacity |
| **Least Connections** | Sends to server with fewest active requests | Varying request times |
| **IP Hash** | Same user always goes to same server | Session persistence |
| **Weighted** | Stronger servers get more traffic | Mixed server sizes |

### Real-World Analogy

A host at a restaurant who seats customers at different tables to keep all waiters equally busy.

---

## Level 4: Database Connection Pooling

### What is it?

Instead of opening a new database connection for every request, maintain a pool of ready-to-use connections that can be reused.

<div class="mermaid">
sequenceDiagram
    participant R1 as 📨 Request 1
    participant R2 as 📨 Request 2
    participant R3 as 📨 Request 3
    participant P as 🏊 Connection Pool
    participant DB as 🗄️ Database
    
    Note over P,DB: Pool has 3 connections ready
    
    R1->>P: Need connection
    P->>R1: ✅ Connection #1
    R1->>DB: Query
    
    R2->>P: Need connection
    P->>R2: ✅ Connection #2
    R2->>DB: Query
    
    R3->>P: Need connection
    P->>R3: ✅ Connection #3
    R3->>DB: Query
    
    R1->>P: Done! Return connection
    Note over P: Connection #1 back in pool
    
    R2->>P: Done! Return connection
    R3->>P: Done! Return connection
</div>

### Why It Matters

Opening a database connection is expensive:

| Action | Time |
|--------|------|
| Open new connection | 50-100ms |
| Reuse from pool | < 1ms |

With 1000 requests/sec, you save **50-100 seconds** of work!

### Without vs With Connection Pooling

<div class="mermaid">
flowchart TD
    subgraph without["❌ Without Pooling (Slow)"]
        direction TB
        S1["Request"] --> O1["Open connection<br/>50ms"]
        O1 --> Q1["Query<br/>10ms"]
        Q1 --> C1["Close connection<br/>5ms"]
        C1 --> T1["Total: 65ms"]
    end
    
    subgraph with["✅ With Pooling (Fast)"]
        direction TB
        S2["Request"] --> G2["Get from pool<br/>< 1ms"]
        G2 --> Q2["Query<br/>10ms"]
        Q2 --> R2["Return to pool<br/>< 1ms"]
        R2 --> T2["Total: 12ms"]
    end
    
    style without fill:#fecaca,stroke:#dc2626
    style with fill:#d1fae5,stroke:#059669
</div>

### Real-World Analogy

Instead of getting a new fork for every bite of food, you keep your fork and reuse it throughout the meal.

### Implementation Tips

```python
# Python example with connection pooling
from sqlalchemy import create_engine

# Create engine with connection pool
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=20,           # Keep 20 connections ready
    max_overflow=10,        # Allow 10 more if needed
    pool_pre_ping=True      # Check if connection is alive
)
```

**Good for:** All production APIs with databases

---

## Level 5: Avoiding N+1 Query Problems

### What is it?

The N+1 problem happens when you fetch a list of items, then make a separate query for each item's related data. This turns 1 query into N+1 queries!

<div class="mermaid">
sequenceDiagram
    participant A as 🖥️ API
    participant DB as 🗄️ Database
    
    Note over A,DB: ❌ N+1 Problem (10 queries!)
    
    A->>DB: Get all users (1 query)
    DB-->>A: User 1, User 2, User 3
    
    A->>DB: Get posts for User 1
    A->>DB: Get posts for User 2
    A->>DB: Get posts for User 3
    A->>DB: Get comments for Post 1
    A->>DB: Get comments for Post 2
    A->>DB: Get comments for Post 3
    A->>DB: Get likes for Post 1
    A->>DB: Get likes for Post 2
    A->>DB: Get likes for Post 3
    
    Note over A,DB: Total: 10 queries, 500ms
</div>

### The Better Way: Join or Batch Queries

<div class="mermaid">
sequenceDiagram
    participant A as 🖥️ API
    participant DB as 🗄️ Database
    
    Note over A,DB: ✅ Optimized (1-2 queries!)
    
    A->>DB: Get users with posts and comments<br/>(using JOIN)
    DB-->>A: All data in one result
    
    Note over A,DB: Total: 1 query, 50ms
</div>

### Problem Example

```python
# ❌ BAD: N+1 Problem
users = User.query.all()  # 1 query

for user in users:  # 100 users
    posts = user.posts  # 100 more queries!
    # Total: 101 queries
```

### Solution Example

```python
# ✅ GOOD: Eager Loading
users = User.query.options(
    joinedload(User.posts)
).all()  # Just 1 query with JOIN!

for user in users:
    posts = user.posts  # No additional query!
```

### Performance Impact

<div class="mermaid">
flowchart LR
    subgraph problem["❌ N+1 Problem"]
        direction TB
        P1["100 users"]
        P2["101 queries"]
        P3["2000ms response"]
    end
    
    subgraph solution["✅ Optimized"]
        direction TB
        S1["100 users"]
        S2["1-2 queries"]
        S3["50ms response"]
    end
    
    problem -->|40x faster| solution
    
    style problem fill:#fecaca,stroke:#dc2626
    style solution fill:#d1fae5,stroke:#059669
</div>

### Real-World Analogy

Instead of making 100 trips to the store to buy 100 items, you make one trip with a shopping list and get everything at once.

**Good for:** Any API that returns lists with related data

---

## Level 6: Caching (Remember & Reuse)

### What is it?

Store frequently accessed data in fast memory so you don't have to compute or fetch it again.

<div class="mermaid">
sequenceDiagram
    participant U as 👤 User
    participant S as 🖥️ Server
    participant C as ⚡ Cache (Redis)
    participant D as 🗄️ Database
    
    Note over U,D: First Request (Cache Miss)
    U->>S: GET /user/123
    S->>C: Check cache
    C-->>S: ❌ Not found
    S->>D: Query database
    D-->>S: User data
    S->>C: Store in cache
    S-->>U: Response (200ms)
    
    Note over U,D: Second Request (Cache Hit)
    U->>S: GET /user/123
    S->>C: Check cache
    C-->>S: ✅ Found!
    S-->>U: Response (5ms) 🚀
</div>

### Types of Caching

<div class="mermaid">
flowchart LR
    subgraph layers["Caching Layers"]
        direction TB
        B["🌐 Browser Cache<br/>Client-side"]
        CDN["📡 CDN Cache<br/>Edge servers"]
        APP["⚡ App Cache<br/>Redis/Memcached"]
        DB["🗄️ DB Cache<br/>Query cache"]
    end
    
    B --> CDN --> APP --> DB
    
    style B fill:#dbeafe,stroke:#2563eb
    style CDN fill:#d1fae5,stroke:#059669
    style APP fill:#fef3c7,stroke:#d97706
    style DB fill:#fce7f3,stroke:#db2777
</div>

### What to Cache

- ✅ API responses that don't change often
- ✅ Database query results
- ✅ Session data
- ✅ Computed values (totals, aggregations)

### Real-World Analogy

A chef who preps ingredients in advance. Instead of chopping onions for every order, they chop a big batch and grab from it.

**Good for:** 1,000 → 100,000 RPS

---

## Level 7: Pagination (Send Data in Chunks)

### What is it?

Instead of returning thousands of records at once, break them into small pages that load quickly.

<div class="mermaid">
sequenceDiagram
    participant C as 👤 Client
    participant A as 🖥️ API
    participant D as 🗄️ Database
    
    Note over C,D: ❌ Without Pagination
    C->>A: GET /users
    A->>D: SELECT * FROM users
    D-->>A: 10,000 records (5MB)
    A-->>C: Response takes 5 seconds 😴
    
    Note over C,D: ✅ With Pagination
    C->>A: GET /users?page=1&limit=20
    A->>D: SELECT * FROM users<br/>LIMIT 20 OFFSET 0
    D-->>A: 20 records (10KB)
    A-->>C: Response takes 50ms 🚀
</div>

### Common Pagination Approaches

<div class="mermaid">
flowchart TD
    subgraph offset["Offset-Based"]
        direction TB
        O1["Page 1: OFFSET 0, LIMIT 20"]
        O2["Page 2: OFFSET 20, LIMIT 20"]
        O3["Page 3: OFFSET 40, LIMIT 20"]
    end
    
    subgraph cursor["Cursor-Based (Better!)"]
        direction TB
        C1["Page 1: id > 0, LIMIT 20"]
        C2["Page 2: id > 20, LIMIT 20"]
        C3["Page 3: id > 40, LIMIT 20"]
    end
    
    style offset fill:#fef3c7,stroke:#d97706
    style cursor fill:#d1fae5,stroke:#059669
</div>

### Implementation

```javascript
// Offset-based pagination (simple but slower for large offsets)
GET /api/users?page=1&limit=20

// Cursor-based pagination (faster, handles real-time changes)
GET /api/users?cursor=abc123&limit=20
```

### Response Format

```json
{
  "data": [...],
  "pagination": {
    "total": 10000,
    "page": 1,
    "limit": 20,
    "total_pages": 500,
    "next_cursor": "xyz789"
  }
}
```

### Real-World Analogy

Instead of downloading an entire encyclopedia, you download one page at a time as you read it.

**Good for:** Any endpoint that returns lists or collections

---

## Level 8: Lightweight JSON Serializers

### What is it?

JSON serialization (converting data structures to JSON) can be a bottleneck. Fast serializers can be 2-10x faster than default ones.

<div class="mermaid">
flowchart LR
    subgraph slow["❌ Default Serializer"]
        direction TB
        D1["Python dict"]
        D2["json.dumps()"]
        D3["100ms"]
    end
    
    subgraph fast["✅ Fast Serializer"]
        direction TB
        F1["Python dict"]
        F2["orjson.dumps()"]
        F3["10ms"]
    end
    
    slow -->|10x faster| fast
    
    style slow fill:#fecaca,stroke:#dc2626
    style fast fill:#d1fae5,stroke:#059669
</div>

### Performance Comparison

| Language | Default | Fast Library | Speedup |
|----------|---------|--------------|---------|
| Python | `json` | `orjson` or `ujson` | 5-10x |
| Node.js | `JSON.stringify()` | `fast-json-stringify` | 2-3x |
| Java | `Jackson` | `Jackson` (already fast!) | - |
| Go | `encoding/json` | `jsoniter` | 3-4x |

### Example Implementation

```python
# ❌ Default (slower)
import json
response = json.dumps(data)

# ✅ Fast serializer
import orjson
response = orjson.dumps(data)  # 5-10x faster!
```

```javascript
// ❌ Default (slower)
const json = JSON.stringify(data);

// ✅ Fast serializer with schema
const fastJson = require('fast-json-stringify');
const stringify = fastJson({
  type: 'object',
  properties: {
    name: { type: 'string' },
    age: { type: 'integer' }
  }
});
const json = stringify(data);  // 2-3x faster!
```

### Real-World Analogy

Using a high-speed printer instead of an old dot-matrix printer to print the same document.

**Good for:** High-traffic APIs with large response payloads

---

## Level 9: Compression (Shrink the Data)

### What is it?

Compress API responses before sending them over the network, reducing bandwidth and transfer time.

<div class="mermaid">
sequenceDiagram
    participant C as 👤 Client
    participant S as 🖥️ Server
    
    Note over C,S: ❌ Without Compression
    C->>S: GET /api/data
    S-->>C: 1MB uncompressed (slow)
    Note over C: Download time: 8 seconds
    
    Note over C,S: ✅ With Compression (Gzip)
    C->>S: GET /api/data<br/>Accept-Encoding: gzip
    S-->>C: 100KB compressed (fast!)
    Note over C: Download time: 0.8 seconds 🚀
</div>

### Compression Algorithms

<div class="mermaid">
flowchart TD
    subgraph comparison["Compression Comparison"]
        direction TB
        N["None: 1000KB"]
        G["Gzip: 150KB (85% smaller)"]
        B["Brotli: 120KB (88% smaller)"]
    end
    
    style N fill:#fecaca,stroke:#dc2626
    style G fill:#fef3c7,stroke:#d97706
    style B fill:#d1fae5,stroke:#059669
</div>

| Algorithm | Compression | Speed | Browser Support |
|-----------|------------|-------|-----------------|
| **Gzip** | Good (70-80%) | Fast | ✅ Universal |
| **Brotli** | Better (75-85%) | Medium | ✅ Modern browsers |
| **Deflate** | Good (70-80%) | Fast | ✅ Universal |

### When to Use Compression

- ✅ Text responses (JSON, HTML, CSS, JS)
- ✅ Responses larger than 1KB
- ❌ Already compressed data (images, videos)
- ❌ Very small responses (< 1KB)

### Implementation

```javascript
// Express.js (Node.js)
const compression = require('compression');
app.use(compression());  // Automatically compress all responses
```

```python
# Flask (Python)
from flask_compress import Compress
Compress(app)  # Enable compression
```

```nginx
# Nginx configuration
gzip on;
gzip_types application/json text/css application/javascript;
gzip_min_length 1000;
```

### Real-World Analogy

Vacuum-sealing clothes before packing them in a suitcase — same clothes, much less space.

**Good for:** All text-based API responses

---

## Level 10: Content Delivery Network (CDN)

### What is it?

A network of servers spread around the world that cache your content closer to users.

<div class="mermaid">
flowchart TD
    subgraph origin["🏠 Your Origin Server<br/>(New York)"]
        O["🖥️ Main Server"]
    end
    
    subgraph cdn["🌍 CDN Edge Servers"]
        E1["📡 London"]
        E2["📡 Tokyo"]
        E3["📡 Sydney"]
        E4["📡 São Paulo"]
    end
    
    O --> E1
    O --> E2
    O --> E3
    O --> E4
    
    U1["👤 UK User"] --> E1
    U2["👤 Japan User"] --> E2
    U3["👤 Australia User"] --> E3
    U4["👤 Brazil User"] --> E4
    
    style O fill:#dbeafe,stroke:#2563eb
    style E1 fill:#d1fae5,stroke:#059669
    style E2 fill:#d1fae5,stroke:#059669
    style E3 fill:#d1fae5,stroke:#059669
    style E4 fill:#d1fae5,stroke:#059669
</div>

### Without CDN vs With CDN

| | Without CDN | With CDN |
|---|------------|----------|
| **User in Tokyo** | Request travels to New York (200ms) | Request goes to Tokyo edge (20ms) |
| **Server Load** | Every request hits your server | Most requests served by CDN |
| **Bandwidth Cost** | You pay for all traffic | CDN handles most traffic |

### Real-World Analogy

Instead of one restaurant in New York, you open franchises worldwide. Customers get the same food from their local branch.

### Best For

- Static assets (images, CSS, JS)
- API responses that don't change per user
- Video streaming

---

## Level 11: Asynchronous Processing

### What is it?

For slow operations, accept the request immediately and process it in the background.

<div class="mermaid">
sequenceDiagram
    participant U as 👤 User
    participant A as 🖥️ API Server
    participant Q as 📬 Message Queue
    participant W as ⚙️ Worker
    participant E as 📧 Email Service
    
    Note over U,E: ❌ Synchronous (Slow)
    U->>A: POST /send-email
    A->>E: Send email (3 seconds)
    E-->>A: Done
    A-->>U: 200 OK (waited 3 seconds 😴)
    
    Note over U,E: ✅ Asynchronous (Fast)
    U->>A: POST /send-email
    A->>Q: Add to queue
    A-->>U: 202 Accepted (instant! 🚀)
    Q->>W: Process job
    W->>E: Send email
    Note over W: User already moved on!
</div>

### Common Use Cases

| Operation | Sync Time | Async Benefit |
|-----------|-----------|---------------|
| Send email | 2-5 seconds | Instant response |
| Generate PDF | 10+ seconds | User doesn't wait |
| Process payment | 3-5 seconds | Faster checkout |
| Resize image | 5-15 seconds | Upload feels instant |

### Tools

- **Message Queues:** RabbitMQ, Amazon SQS, Redis
- **Task Processors:** Celery (Python), Sidekiq (Ruby), Bull (Node.js)

### Real-World Analogy

At a busy restaurant, the waiter takes your order and immediately moves to the next table. The kitchen processes orders in the background.

---

## Level 12: Asynchronous Logging

### What is it?

Logging can slow down your API if it writes to disk synchronously. Async logging writes to a buffer first, then a background thread handles the disk writes.

<div class="mermaid">
sequenceDiagram
    participant R as 📨 Request
    participant A as 🖥️ API Code
    participant B as 📝 Buffer
    participant T as 🧵 Background Thread
    participant D as 💾 Disk
    
    Note over R,D: ❌ Synchronous Logging (Blocks request)
    R->>A: Process request
    A->>D: Write log (10ms) ⏳
    D-->>A: Done
    A-->>R: Response (slow)
    
    Note over R,D: ✅ Asynchronous Logging (Non-blocking)
    R->>A: Process request
    A->>B: Write to buffer (< 1ms) ⚡
    A-->>R: Response (fast!)
    Note over B,T: Background thread
    T->>B: Read from buffer
    T->>D: Write log
</div>

### Performance Impact

<div class="mermaid">
flowchart LR
    subgraph sync["❌ Sync Logging"]
        direction TB
        S1["1000 requests"]
        S2["10ms per log write"]
        S3["10 seconds wasted"]
    end
    
    subgraph async["✅ Async Logging"]
        direction TB
        A1["1000 requests"]
        A2["< 1ms per log write"]
        A3["< 1 second"]
    end
    
    sync -->|10x faster| async
    
    style sync fill:#fecaca,stroke:#dc2626
    style async fill:#d1fae5,stroke:#059669
</div>

### Implementation

```python
# Python with async logging
import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

# Create a queue for async logging
log_queue = Queue()

# Main thread uses QueueHandler (non-blocking)
handler = QueueHandler(log_queue)
logger = logging.getLogger()
logger.addHandler(handler)

# Background thread processes the queue
listener = QueueListener(log_queue, logging.FileHandler('app.log'))
listener.start()

# Now logging is async!
logger.info('This is non-blocking')  # < 1ms
```

```javascript
// Node.js with async logging (pino)
const pino = require('pino');
const logger = pino({
  transport: {
    target: 'pino/file',
    options: { destination: 'app.log' }
  }
});

// Logs are buffered and written asynchronously
logger.info('This is non-blocking');
```

### Real-World Analogy

Instead of stopping to write down every detail in a notebook, you jot quick notes on sticky notes and organize them into the notebook later.

**Good for:** High-traffic APIs with extensive logging

---

## Level 13: Database Sharding (Split Your Data)

### What is it?

Divide your database into smaller pieces (shards), each handling a portion of the data.

<div class="mermaid">
flowchart TD
    subgraph before["❌ Single Database (Bottleneck)"]
        DB1["🗄️ One Database<br/>100M users"]
    end
    
    subgraph after["✅ Sharded Database"]
        R["🔀 Router"]
        R --> S1["🗄️ Shard 1<br/>Users A-H"]
        R --> S2["🗄️ Shard 2<br/>Users I-P"]
        R --> S3["🗄️ Shard 3<br/>Users Q-Z"]
    end
    
    style DB1 fill:#fecaca,stroke:#dc2626
    style R fill:#fef3c7,stroke:#d97706
    style S1 fill:#d1fae5,stroke:#059669
    style S2 fill:#d1fae5,stroke:#059669
    style S3 fill:#d1fae5,stroke:#059669
</div>

### Sharding Strategies

<div class="mermaid">
flowchart LR
    subgraph range["Range-Based"]
        direction TB
        R1["Users 1-1M → Shard 1"]
        R2["Users 1M-2M → Shard 2"]
    end
    
    subgraph hash["Hash-Based"]
        direction TB
        H1["user_id % 3 = 0 → Shard 1"]
        H2["user_id % 3 = 1 → Shard 2"]
        H3["user_id % 3 = 2 → Shard 3"]
    end
    
    subgraph geo["Geographic"]
        direction TB
        G1["US users → US Shard"]
        G2["EU users → EU Shard"]
    end
</div>

### Trade-offs

| Benefit | Challenge |
|---------|-----------|
| ✅ Each shard handles less load | ❌ Cross-shard queries are complex |
| ✅ Can scale horizontally | ❌ Rebalancing shards is hard |
| ✅ Failure affects only one shard | ❌ Application logic becomes complex |

### Real-World Analogy

Instead of one giant warehouse, you have regional warehouses. Each handles orders for their region.

**Good for:** 100,000 → 1,000,000+ RPS

---

## Level 14: Rate Limiting (Protect Your System)

### What is it?

Limit how many requests a user or client can make in a given time period.

<div class="mermaid">
sequenceDiagram
    participant U as 👤 User
    participant R as 🚦 Rate Limiter
    participant A as 🖥️ API
    
    U->>R: Request 1
    R->>A: ✅ Allow
    A-->>U: 200 OK
    
    U->>R: Request 2
    R->>A: ✅ Allow
    A-->>U: 200 OK
    
    U->>R: Request 3
    R->>A: ✅ Allow
    A-->>U: 200 OK
    
    Note over U,A: Limit reached (3 req/sec)
    
    U->>R: Request 4
    R-->>U: ❌ 429 Too Many Requests
    
    U->>R: Request 5
    R-->>U: ❌ 429 Too Many Requests
    
    Note over U,A: Wait 1 second...
    
    U->>R: Request 6
    R->>A: ✅ Allow
    A-->>U: 200 OK
</div>

### Common Algorithms

| Algorithm | How it Works | Visual |
|-----------|--------------|--------|
| **Token Bucket** | Tokens added at fixed rate; request consumes a token | 🪣 Bucket fills up over time |
| **Sliding Window** | Count requests in rolling time window | 📊 Moving window of time |
| **Fixed Window** | Reset counter at fixed intervals | ⏰ Reset every minute |

### Rate Limit Headers

```
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 67
X-RateLimit-Reset: 1640995200
```

### Real-World Analogy

A bouncer at a club who only lets in 100 people per hour, no matter how long the line is.

---

## The Complete Picture

Here's how all these techniques work together at scale:

<div class="mermaid">
flowchart TB
    subgraph users["🌍 Users Worldwide"]
        U1["👤"]
        U2["👤"]
        U3["👤"]
    end
    
    subgraph edge["Edge Layer"]
        CDN["📡 CDN + Compression"]
        RL["🚦 Rate Limiter"]
    end
    
    subgraph app["Application Layer"]
        LB["⚖️ Load Balancer"]
        S1["🖥️ Server<br/>Fast JSON"]
        S2["🖥️ Server<br/>Async Logging"]
        S3["🖥️ Server<br/>Connection Pool"]
    end
    
    subgraph cache["Cache Layer"]
        RC["⚡ Redis Cache"]
    end
    
    subgraph async["Async Layer"]
        Q["📬 Queue"]
        W["⚙️ Workers"]
    end
    
    subgraph data["Data Layer<br/>(Optimized Queries)"]
        SH1["🗄️ Shard 1"]
        SH2["🗄️ Shard 2"]
        SH3["🗄️ Shard 3"]
    end
    
    U1 --> CDN
    U2 --> CDN
    U3 --> CDN
    CDN --> RL
    RL --> LB
    LB --> S1
    LB --> S2
    LB --> S3
    S1 --> RC
    S2 --> RC
    S3 --> RC
    S1 --> Q
    RC --> SH1
    RC --> SH2
    RC --> SH3
    Q --> W
    W --> SH1
    
    style CDN fill:#d1fae5,stroke:#059669
    style RL fill:#fef3c7,stroke:#d97706
    style LB fill:#dbeafe,stroke:#2563eb
    style RC fill:#fce7f3,stroke:#db2777
    style Q fill:#e0e7ff,stroke:#6366f1
</div>

---

## Scaling Roadmap

| RPS Target | Techniques to Add |
|------------|-------------------|
| **1 → 100** | Vertical scaling, connection pooling, avoid N+1 queries |
| **100 → 1K** | Caching (Redis), pagination, compression |
| **1K → 10K** | Horizontal scaling, load balancer, fast JSON serializers |
| **10K → 100K** | CDN, async processing, async logging |
| **100K → 1M** | Database sharding, rate limiting, microservices |
| **1M+** | Multi-region deployment, edge computing |

---

## Quick Reference: What to Use When

<div class="mermaid">
flowchart TD
    Q["🤔 What's your bottleneck?"]
    
    Q --> CPU["CPU maxed out?"]
    Q --> MEM["Memory full?"]
    Q --> DB["Database slow?"]
    Q --> NET["Network saturated?"]
    Q --> LOG["Logging slow?"]
    
    CPU --> CPU_S["Add more servers<br/>(horizontal scaling)"]
    MEM --> MEM_S["Add caching<br/>(Redis/Memcached)"]
    DB --> DB_S["Connection pooling,<br/>avoid N+1, sharding"]
    NET --> NET_S["CDN, compression,<br/>pagination"]
    LOG --> LOG_S["Async logging"]
    
    style Q fill:#f1f5f9,stroke:#64748b
    style CPU_S fill:#d1fae5,stroke:#059669
    style MEM_S fill:#d1fae5,stroke:#059669
    style DB_S fill:#d1fae5,stroke:#059669
    style NET_S fill:#d1fae5,stroke:#059669
    style LOG_S fill:#d1fae5,stroke:#059669
</div>

---

## Complete Summary

| Technique | What It Does | Impact | When to Use |
|-----------|--------------|--------|-------------|
| **Vertical Scaling** | Bigger server | Quick wins | Start here |
| **Horizontal Scaling** | More servers | High | Growing traffic |
| **Load Balancing** | Distribute traffic | High | Multiple servers |
| **Connection Pooling** | Reuse DB connections | Very High | Always! |
| **Avoid N+1 Queries** | Optimize DB queries | Very High | Always! |
| **Caching** | Remember results | Very High | Repeated queries |
| **Pagination** | Send data in chunks | High | Large datasets |
| **Fast JSON Serializers** | Faster responses | Medium | High traffic |
| **Compression** | Smaller payloads | High | Text responses |
| **CDN** | Serve from edge | High | Global users |
| **Async Processing** | Background jobs | High | Slow operations |
| **Async Logging** | Non-blocking logs | Medium | Heavy logging |
| **Database Sharding** | Split data | Very High | Massive datasets |
| **Rate Limiting** | Protect system | Medium | Always! |

---

## Bringing It All Together: Your Scaling Journey

Scaling from 1 to 1 million RPS is not a single leap—it's a series of strategic steps. Here's how to think about your progression:

### Phase 1: Foundation (1-1K RPS)
**Focus:** Get the basics right
- ✅ Start with vertical scaling (bigger server)
- ✅ Implement connection pooling immediately
- ✅ Fix N+1 query problems
- ✅ Add basic caching for read-heavy operations
- ✅ Enable compression

**Mindset:** At this stage, a single well-configured server is sufficient. Don't over-engineer.

### Phase 2: Growth (1K-10K RPS)
**Focus:** Distribute and optimize
- ✅ Add horizontal scaling (multiple servers)
- ✅ Set up a load balancer
- ✅ Implement pagination for all list endpoints
- ✅ Use fast JSON serializers
- ✅ Expand caching strategy

**Mindset:** Your single server is maxed out. Time to distribute the load.

### Phase 3: Scale (10K-100K RPS)
**Focus:** Edge optimization and async patterns
- ✅ Deploy a CDN for static content and cacheable responses
- ✅ Move slow operations to async workers
- ✅ Implement async logging
- ✅ Optimize database with better indexing and query patterns

**Mindset:** Every millisecond counts. Optimize the request path and offload work.

### Phase 4: Massive Scale (100K-1M+ RPS)
**Focus:** Database distribution and protection
- ✅ Implement database sharding
- ✅ Add rate limiting to protect against abuse
- ✅ Consider multi-region deployment
- ✅ Implement circuit breakers and failover mechanisms

**Mindset:** You're operating at web scale. Focus on reliability, distribution, and resilience.

---

## Critical Success Factors

### 1. Measure Before You Optimize
The bottleneck you imagine is rarely the real one. Use monitoring and profiling tools:
- **Application Performance Monitoring (APM):** New Relic, Datadog, or Grafana
- **Database Profiling:** Identify slow queries with EXPLAIN plans
- **Load Testing:** Use tools like k6, Gatling, or Apache JMeter

Don't guess—measure, identify the bottleneck, then fix it.

### 2. Implement Quick Wins First
Some techniques have massive impact with minimal complexity:
- **Connection pooling:** 5-10x faster database operations
- **Avoid N+1 queries:** 40x faster response times
- **Compression:** 70-85% smaller payloads
- **Basic caching:** 100x faster for repeated queries

Start here before jumping to complex solutions.

### 3. Progressive Enhancement Over Big Rewrites
Add capabilities incrementally rather than rewriting everything:
- Add caching without changing your API
- Add horizontal scaling without modifying application code
- Add async processing for new features first

This reduces risk and delivers value continuously.

### 4. Know When NOT to Scale
- **Traffic patterns:** Don't optimize for traffic spikes that happen once a year
- **Cost vs. benefit:** Sometimes accepting slower responses is cheaper than scaling
- **Product stage:** Pre-product-market fit? Focus on features, not scale

Premature optimization wastes time and money.

---

## Common Scaling Mistakes to Avoid

❌ **Mistake 1: Jumping to Microservices Too Early**
A well-optimized monolith can handle 10,000+ RPS. Microservices add complexity—only adopt them when you have clear organizational or technical reasons.

❌ **Mistake 2: Ignoring Database Optimization**
Adding more application servers won't help if your database is the bottleneck. Fix queries first.

❌ **Mistake 3: Not Testing Under Load**
Load test before you have a problem, not during an outage. Know your limits.

❌ **Mistake 4: Caching Everything**
Cache only what's expensive to compute and read frequently. Over-caching adds complexity.

❌ **Mistake 5: Forgetting About Cache Invalidation**
As Phil Karlton said: "There are only two hard things in Computer Science: cache invalidation and naming things." Plan your cache invalidation strategy from day one.

---

## Key Takeaways

1. **Start Simple**: A single optimized server with connection pooling, query optimization, and basic caching can handle 10,000+ RPS. Don't over-engineer early.

2. **Measure First, Optimize Second**: Use APM tools and profiling to find your actual bottlenecks. The problem is rarely where you think it is.

3. **Low-Hanging Fruit Matters Most**:
   - Connection pooling (implement immediately)
   - Avoid N+1 queries (implement immediately)
   - Basic caching (implement early)
   - Pagination (implement for all list endpoints)
   - Compression (enable by default)

4. **Progressive Enhancement**: Your architecture should evolve with your traffic:
   - 1-1K RPS: Single server + optimizations
   - 1K-10K RPS: Horizontal scaling + load balancing
   - 10K-100K RPS: CDN + async patterns
   - 100K-1M+ RPS: Sharding + multi-region

5. **Always Profile**: The bottleneck you imagine is rarely the real one. Measure, don't guess!

---

## Final Thoughts

Scaling is a journey, not a destination. The techniques in this guide will take you from handling your first user to serving millions. The key is to:

- **Start with fundamentals** (connection pooling, query optimization)
- **Add capabilities progressively** (don't jump to advanced techniques)
- **Measure constantly** (know your bottlenecks)
- **Optimize deliberately** (focus on impact, not complexity)

Remember: Twitter started as a Ruby on Rails monolith. Facebook started on a single server. Instagram scaled to 30+ million users with just 3 engineers. **Good architecture and simple optimizations can take you incredibly far.**

Build for today's needs with an eye toward tomorrow's scale. When you need the next level, you'll know—your monitoring will tell you. Until then, keep it simple and keep shipping. 🚀

---

## Continue Your Journey

This guide covered the **technical and infrastructure** aspects of scaling APIs. But as your organization grows, you'll face a different kind of scaling challenge: **organizational and design complexity**.

**[→ Continue to Part 2: Design & Architecture Strategies]({{ site.baseurl }}/topics/scaling-api-design-architecture-part-2/)** to learn about:
- API portfolio management
- Design-first methodologies
- Organizational patterns for large-scale API development
- Versioning strategies
- Governance and evangelism at scale
