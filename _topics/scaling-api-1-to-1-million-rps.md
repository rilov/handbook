---
title: Scaling Your API from 1 to 1 Million RPS
category: Architecture
tags:
  - scaling
  - performance
  - api
  - infrastructure
summary: A beginner-friendly guide to scaling your API from handling 1 request per second to 1 million, with diagrams and simple explanations.
---

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

Let's break down each technique, starting from the simplest to the most advanced.

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
    
    before --> |"💰 Upgrade"| after
    
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
    
    LB --> |"1, 4"| S1["🖥️ Server 1"]
    LB --> |"2, 5"| S2["🖥️ Server 2"]
    LB --> |"3, 6"| S3["🖥️ Server 3"]
    
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

## Level 4: Caching (Remember & Reuse)

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

**Good for:** 10,000 → 100,000 RPS

---

## Level 5: Content Delivery Network (CDN)

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

## Level 6: Asynchronous Processing (Don't Make Users Wait)

### What is it?

For slow operations, accept the request immediately and process it in the background.

<div class="mermaid">
sequenceDiagram
    participant U as 👤 User
    participant A as 🖥️ API Server
    participant Q as 📬 Message Queue
    participant W as ⚙️ Worker
    participant E as 📧 Email Service
    
    Note over U,E: Synchronous (Slow) ❌
    U->>A: POST /send-email
    A->>E: Send email (3 seconds)
    E-->>A: Done
    A-->>U: 200 OK (waited 3 seconds 😴)
    
    Note over U,E: Asynchronous (Fast) ✅
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

## Level 7: Database Sharding (Split Your Data)

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

## Level 8: Rate Limiting (Protect Your System)

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

## Level 9: Keep Responses Lightweight

### What is it?

Send only the data users need, in the most efficient format.

<div class="mermaid">
flowchart LR
    subgraph heavy["❌ Heavy Response (10KB)"]
        H["Full user object<br/>+ nested data<br/>+ unused fields"]
    end
    
    subgraph light["✅ Light Response (500B)"]
        L["Only requested<br/>fields"]
    end
    
    heavy --> |"20x smaller"| light
    
    style H fill:#fecaca,stroke:#dc2626
    style L fill:#d1fae5,stroke:#059669
</div>

### Techniques

#### 1. Field Selection (GraphQL / Sparse Fields)

```
# Instead of getting everything:
GET /users/123

# Request only what you need:
GET /users/123?fields=name,email
```

#### 2. Pagination

```
# Don't return 10,000 items at once!
GET /users?page=1&limit=20
```

#### 3. Compression

```
# Enable gzip compression
Response: 100KB → 15KB
```

#### 4. Efficient Formats

| Format | Size | Speed | Use Case |
|--------|------|-------|----------|
| JSON | Medium | Fast | Most APIs |
| Protocol Buffers | Small | Fastest | High-performance |
| MessagePack | Small | Fast | Binary data |

### Real-World Analogy

Instead of shipping a whole catalog, send just the page the customer asked for.

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
        CDN["📡 CDN"]
        RL["🚦 Rate Limiter"]
    end
    
    subgraph app["Application Layer"]
        LB["⚖️ Load Balancer"]
        S1["🖥️ Server"]
        S2["🖥️ Server"]
        S3["🖥️ Server"]
    end
    
    subgraph cache["Cache Layer"]
        RC["⚡ Redis Cache"]
    end
    
    subgraph async["Async Layer"]
        Q["📬 Queue"]
        W["⚙️ Workers"]
    end
    
    subgraph data["Data Layer"]
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
| **1 → 100** | Vertical scaling, basic optimization |
| **100 → 1K** | Add caching (Redis), optimize database queries |
| **1K → 10K** | Horizontal scaling, load balancer, CDN |
| **10K → 100K** | Database read replicas, async processing |
| **100K → 1M** | Database sharding, microservices, rate limiting |
| **1M+** | Multi-region deployment, edge computing |

---

## Quick Reference

<div class="mermaid">
flowchart TD
    Q["🤔 What's your bottleneck?"]
    
    Q --> CPU["CPU maxed out?"]
    Q --> MEM["Memory full?"]
    Q --> DB["Database slow?"]
    Q --> NET["Network saturated?"]
    
    CPU --> CPU_S["Add more servers<br/>(horizontal scaling)"]
    MEM --> MEM_S["Add caching<br/>(Redis/Memcached)"]
    DB --> DB_S["Read replicas,<br/>sharding, caching"]
    NET --> NET_S["CDN, compression,<br/>lighter responses"]
    
    style Q fill:#f1f5f9,stroke:#64748b
    style CPU_S fill:#d1fae5,stroke:#059669
    style MEM_S fill:#d1fae5,stroke:#059669
    style DB_S fill:#d1fae5,stroke:#059669
    style NET_S fill:#d1fae5,stroke:#059669
</div>

---

## Summary

| Technique | What It Does | When to Use |
|-----------|--------------|-------------|
| **Vertical Scaling** | Bigger server | Quick fix, low traffic |
| **Horizontal Scaling** | More servers | Sustained growth |
| **Load Balancing** | Distribute traffic | Multiple servers |
| **Caching** | Remember results | Repeated queries |
| **CDN** | Serve from edge | Global users, static content |
| **Async Processing** | Background jobs | Slow operations |
| **Database Sharding** | Split data | Massive datasets |
| **Rate Limiting** | Protect system | Prevent abuse |
| **Light Responses** | Send less data | Always! |

**Remember:** Start simple, measure everything, and scale based on actual bottlenecks — not imagined ones!

