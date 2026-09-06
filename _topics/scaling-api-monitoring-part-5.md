---
title: "Scaling Your API Part 5: Monitoring & Performance"
category: Architecture
tags:
  - monitoring
  - performance
  - api
  - observability
  - metrics
series: "Scaling Your API"
part: 5
summary: Learn how to monitor your API and improve performance — with simple explanations and practical examples anyone can understand.
related:
  - scaling-api-1-to-1-million-rps
  - scaling-api-design-architecture-part-2
  - choosing-the-right-database
  - scaling-api-load-balancing-part-4
---

> **📚 This is Part 5 of the "Scaling Your API" Series**
> - **[Part 1: Performance & Infrastructure ←]({{ site.baseurl }}/topics/scaling-api-1-to-1-million-rps/)** - Technical techniques to handle millions of requests
> - **[Part 2: Design & Architecture ←]({{ site.baseurl }}/topics/scaling-api-design-architecture-part-2/)** - Organizational strategies and API design patterns
> - **[Part 3: Choosing the Right Database ←]({{ site.baseurl }}/topics/choosing-the-right-database/)** - Database selection for your API
> - **[Part 4: Load Balancing & High Availability ←]({{ site.baseurl }}/topics/scaling-api-load-balancing-part-4/)** - Keeping your API always available
> - **Part 5 (this page):** Monitoring & Performance - Tracking and improving API performance

## Why Monitor Your API?

> **Think of it like this:** Monitoring your API is like having a dashboard in your car. You need to know your speed, fuel level, and engine temperature — before problems happen!

### Without Monitoring ❌

```
User: "Your API is down!"
You: "What? Since when?"
User: "For the last 2 hours!"
You: *panic* 😱

Problem: You didn't know there was an issue until users complained
```

### With Monitoring ✅

```
11:00 AM - Monitor detects high error rate
11:01 AM - Alert sent to your phone 📱
11:02 AM - You start investigating
11:05 AM - Problem fixed

Problem: Caught and fixed in 5 minutes, most users didn't even notice!
```

---

## The 4 Golden Signals (What to Monitor)

> **These 4 metrics tell you everything about your API's health:**

<div class="mermaid">
flowchart TD
    MONITOR["📊 Monitor Your API"]
    
    LATENCY["⏱️ Latency<br/>(How fast?)"]
    TRAFFIC["📈 Traffic<br/>(How busy?)"]
    ERRORS["❌ Errors<br/>(What's broken?)"]
    SATURATION["🔥 Saturation<br/>(How full?)"]
    
    MONITOR --> LATENCY
    MONITOR --> TRAFFIC
    MONITOR --> ERRORS
    MONITOR --> SATURATION
    
    style MONITOR fill:#dbeafe,stroke:#2563eb
    style LATENCY fill:#d1fae5,stroke:#059669
    style TRAFFIC fill:#fef3c7,stroke:#d97706
    style ERRORS fill:#fee,stroke:#f00
    style SATURATION fill:#fce7f3,stroke:#db2777
</div>

---

### 1. Latency (How Fast Is Your API?)

> **Latency = How long it takes to respond to a request**

**Good API:**
```
User makes request at 10:00:00.000
API responds at     10:00:00.050  (50ms later)

Latency: 50ms ✅ (Very fast!)
```

**Slow API:**
```
User makes request at 10:00:00.000
API responds at     10:00:02.500  (2.5 seconds later)

Latency: 2,500ms ❌ (Too slow!)
```

**What to Aim For:**
```
Excellent:   < 100ms
Good:        100-300ms
Acceptable:  300-1000ms
Slow:        > 1000ms (need to optimize!)
```

**Real-World Example:**
```javascript
// Measure latency in your API
app.get('/api/users/:id', async (req, res) => {
  const startTime = Date.now();
  
  const user = await database.getUser(req.params.id);
  
  const latency = Date.now() - startTime;
  console.log(`Request took ${latency}ms`);
  
  res.json(user);
});

// Output:
// Request took 45ms ✅
// Request took 52ms ✅
// Request took 1200ms ❌ (Something is wrong!)
```

---

### 2. Traffic (How Busy Is Your API?)

> **Traffic = Number of requests your API receives**

**Why it matters:**
```
Normal day:     1,000 requests/second
Black Friday:   10,000 requests/second

If you don't monitor traffic, you won't know when to add more servers!
```

**Example Traffic Patterns:**

<div class="mermaid">
graph LR
    A[Morning: 1000 req/s] --> B[Noon: 5000 req/s]
    B --> C[Evening: 3000 req/s]
    C --> D[Night: 500 req/s]
    
    style A fill:#d1fae5
    style B fill:#fef3c7
    style C fill:#fef3c7
    style D fill:#d1fae5
</div>

**What to Track:**
```
- Requests per second (RPS)
- Requests per minute (RPM)
- Most popular endpoints
- Peak traffic times
```

---

### 3. Errors (What's Breaking?)

> **Errors = Requests that fail**

**Types of Errors:**

```
200 OK           ✅ Success! Everything worked
400 Bad Request  ⚠️  User sent invalid data
401 Unauthorized ⚠️  User not logged in
404 Not Found    ⚠️  Endpoint doesn't exist
500 Server Error ❌ YOUR API IS BROKEN!
503 Unavailable  ❌ Server overloaded!
```

**Error Rate Example:**
```
Total Requests: 1,000
Errors: 10
Error Rate: 1% (acceptable)

Total Requests: 1,000
Errors: 500
Error Rate: 50% (CRITICAL PROBLEM! 🚨)
```

**What Good Looks Like:**
```
Target Error Rate: < 0.1% (1 error per 1,000 requests)
Acceptable: < 1%
Problem: > 5%
Critical: > 10%
```

---

### 4. Saturation (How Full Is Your System?)

> **Saturation = How close to maximum capacity**

**Think of it like a highway:**
```
10 cars on highway   = 10% saturation  ✅ (Fast and smooth)
50 cars on highway   = 50% saturation  ✅ (Still good)
80 cars on highway   = 80% saturation  ⚠️  (Slowing down)
100 cars on highway  = 100% saturation ❌ (Traffic jam!)
```

**What to Monitor:**

```
CPU Usage:
- 30% = Healthy ✅
- 70% = Getting busy ⚠️
- 90% = Near limit! ❌
- 100% = SLOW! Need more servers!

Memory Usage:
- 40% = Good ✅
- 80% = Watch carefully ⚠️
- 95% = Critical! ❌

Database Connections:
- 20/100 = Plenty available ✅
- 90/100 = Running out! ⚠️
- 100/100 = Requests failing! ❌
```

---

## Simple Monitoring Setup (Step-by-Step)

### Option 1: Basic Logging (Free, 10 Minutes)

**Step 1: Add logging to your API**

```javascript
// Log every request
app.use((req, res, next) => {
  const startTime = Date.now();
  
  // When response finishes
  res.on('finish', () => {
    const duration = Date.now() - startTime;
    
    console.log({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: `${duration}ms`,
      timestamp: new Date().toISOString()
    });
  });
  
  next();
});
```

**Step 2: Check your logs**

```bash
# View recent logs
tail -f /var/log/myapi.log

# Output:
{ method: 'GET', path: '/api/users/123', status: 200, duration: '45ms', timestamp: '2024-01-01T10:00:00Z' }
{ method: 'POST', path: '/api/orders', status: 201, duration: '120ms', timestamp: '2024-01-01T10:00:01Z' }
{ method: 'GET', path: '/api/users/456', status: 500, duration: '5000ms', timestamp: '2024-01-01T10:00:02Z' }
                                            ↑ ERROR! Took 5 seconds!
```

**You now know:**
- ✅ Which requests are slow
- ✅ Which requests are failing
- ✅ When problems happen

---

### Option 2: Simple Dashboard (Free, 30 Minutes)

**Tools:** Express + Simple Stats Endpoint

```javascript
// Track stats in memory
let stats = {
  totalRequests: 0,
  successfulRequests: 0,
  failedRequests: 0,
  totalDuration: 0
};

// Update stats for each request
app.use((req, res, next) => {
  const startTime = Date.now();
  
  stats.totalRequests++;
  
  res.on('finish', () => {
    const duration = Date.now() - startTime;
    stats.totalDuration += duration;
    
    if (res.statusCode < 400) {
      stats.successfulRequests++;
    } else {
      stats.failedRequests++;
    }
  });
  
  next();
});

// Dashboard endpoint
app.get('/admin/stats', (req, res) => {
  const avgDuration = stats.totalDuration / stats.totalRequests;
  const errorRate = (stats.failedRequests / stats.totalRequests) * 100;
  
  res.json({
    totalRequests: stats.totalRequests,
    successRate: `${(stats.successfulRequests / stats.totalRequests * 100).toFixed(2)}%`,
    errorRate: `${errorRate.toFixed(2)}%`,
    avgResponseTime: `${avgDuration.toFixed(0)}ms`
  });
});
```

**Visit http://yourapi.com/admin/stats:**
```json
{
  "totalRequests": 15234,
  "successRate": "99.2%",
  "errorRate": "0.8%",
  "avgResponseTime": "67ms"
}
```

**Now you can check your API health anytime! ✅**

---

### Option 3: Professional Monitoring (Paid, 1 Hour Setup)

#### Best Tools for Beginners:

| Tool | Cost | Best For | Setup Time |
|------|------|----------|------------|
| **Datadog** | $15/month | Beautiful dashboards | 30 min ⭐ |
| **New Relic** | Free tier available | Easy to use | 30 min ⭐ |
| **Grafana Cloud** | Free tier | Open source | 1 hour ⭐⭐ |
| **AWS CloudWatch** | ~$10/month | AWS users | 20 min ⭐ |

---

#### Example: Setting Up Datadog (Simple!)

**Step 1: Sign up at datadog.com**

**Step 2: Install agent on your server**
```bash
# One command!
DD_API_KEY=your-key bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

**Step 3: Install library in your app**
```bash
npm install dd-trace
```

**Step 4: Add to your code**
```javascript
// At the very top of your main file
require('dd-trace').init();

// That's it! 🎉
```

**Step 5: Check Datadog dashboard**

You now see:
- 📊 Request rate graph
- ⏱️ Average response time
- ❌ Error rate
- 🖥️ CPU & memory usage
- 📈 Everything automatically!

---

## Setting Up Alerts (Get Notified When Things Break)

> **Alerts = Automatic notifications when something is wrong**

### Alert Example: High Error Rate

**What you want:**
```
If error rate > 5% for more than 5 minutes
→ Send me a text message! 📱
```

**How to set up (Example with Datadog):**

```
1. Go to Monitors → New Monitor
2. Choose "Metric Monitor"
3. Set condition:
   - Metric: error_rate
   - Alert when: above 5%
   - For: 5 minutes
4. Set notification:
   - Send to: your-phone@sms.com
   - Message: "API errors are high! Check immediately"
5. Save!
```

**Now you get alerted the moment things break ✅**

---

### Smart Alerts (What to Alert On)

#### ✅ DO Alert On These (Important!):

```
1. Error Rate > 5%
   → Something is broken!

2. Response Time > 1 second
   → API is too slow!

3. Traffic drops to 0
   → API might be down!

4. CPU > 90% for 10 minutes
   → Need more servers!

5. Database connections > 95%
   → About to run out!
```

#### ❌ DON'T Alert On These (Too Noisy):

```
1. Single error (happens all the time)
2. Response time spike for 1 second (temporary)
3. CPU > 50% (still plenty of capacity)
4. One slow request (users make mistakes)
```

**Golden Rule:** Only alert on things that need immediate action!

---

## Performance Optimization (Making Your API Faster)

### Step 1: Find the Slow Parts

**Add timing to your code:**

```javascript
app.get('/api/orders/:id', async (req, res) => {
  console.time('Total Request');
  
  console.time('Database Query');
  const order = await db.query('SELECT * FROM orders WHERE id = $1', [req.params.id]);
  console.timeEnd('Database Query');  // Output: Database Query: 150ms
  
  console.time('User Lookup');
  const user = await db.query('SELECT * FROM users WHERE id = $1', [order.userId]);
  console.timeEnd('User Lookup');  // Output: User Lookup: 120ms
  
  console.time('Product Details');
  const products = await getProductDetails(order.items);
  console.timeEnd('Product Details');  // Output: Product Details: 800ms ← SLOW!
  
  console.timeEnd('Total Request');  // Output: Total Request: 1070ms
  
  res.json({ order, user, products });
});
```

**Now you know:** Getting product details is the slow part!

---

### Step 2: Add Caching (Make It 10x Faster)

**Before (Slow):**
```javascript
// Every request hits database (slow!)
app.get('/api/products/:id', async (req, res) => {
  const product = await db.query('SELECT * FROM products WHERE id = $1', [req.params.id]);
  res.json(product);
  // Response time: 150ms
});
```

**After (Fast):**
```javascript
const redis = require('redis');
const client = redis.createClient();

app.get('/api/products/:id', async (req, res) => {
  const cacheKey = `product:${req.params.id}`;
  
  // Try cache first
  const cached = await client.get(cacheKey);
  if (cached) {
    return res.json(JSON.parse(cached));  // Response time: 2ms ⚡
  }
  
  // Cache miss: get from database
  const product = await db.query('SELECT * FROM products WHERE id = $1', [req.params.id]);
  
  // Store in cache for 5 minutes
  await client.setex(cacheKey, 300, JSON.stringify(product));
  
  res.json(product);  // Response time: 150ms first time, then 2ms
});
```

**Result: 75x faster! (150ms → 2ms)**

---

### Step 3: Database Indexes (Speed Up Queries)

**Problem: Slow Query**
```sql
-- Without index: Scans ALL 1 million users (SLOW!)
SELECT * FROM users WHERE email = 'john@example.com';
-- Query time: 2000ms ❌
```

**Solution: Add Index**
```sql
-- Create index on email column
CREATE INDEX idx_users_email ON users(email);

-- Same query now:
SELECT * FROM users WHERE email = 'john@example.com';
-- Query time: 5ms ✅ (400x faster!)
```

**When to Add Indexes:**
```
Add index if you query by that column frequently:
- User IDs ✅ (query all the time)
- Email addresses ✅ (login queries)
- Product SKUs ✅ (product lookups)
- Order dates ✅ (date range queries)
```

---

### Step 4: Reduce Data Transfer

**Bad: Sending Too Much Data**
```javascript
// Returns EVERYTHING (including huge description)
app.get('/api/products', async (req, res) => {
  const products = await db.query('SELECT * FROM products');
  res.json(products);  
  // Response: 5 MB of data
  // Time: 500ms ❌
});
```

**Good: Send Only What's Needed**
```javascript
// Returns only ID, name, price (what user sees in list)
app.get('/api/products', async (req, res) => {
  const products = await db.query('SELECT id, name, price FROM products');
  res.json(products);  
  // Response: 100 KB of data
  // Time: 50ms ✅ (10x faster!)
});

// Full details only when user clicks product
app.get('/api/products/:id', async (req, res) => {
  const product = await db.query('SELECT * FROM products WHERE id = $1', [req.params.id]);
  res.json(product);
});
```

---

### Step 5: Parallel Requests (Do Multiple Things at Once)

**Bad: Sequential (Slow)**
```javascript
// Do one thing at a time (SLOW!)
app.get('/api/dashboard', async (req, res) => {
  const user = await getUser();         // 100ms
  const orders = await getOrders();     // 150ms
  const products = await getProducts(); // 200ms
  
  res.json({ user, orders, products });
  // Total time: 450ms ❌
});
```

**Good: Parallel (Fast)**
```javascript
// Do everything at the same time!
app.get('/api/dashboard', async (req, res) => {
  const [user, orders, products] = await Promise.all([
    getUser(),         // ← All 3 run simultaneously
    getOrders(),       // ←
    getProducts()      // ←
  ]);
  
  res.json({ user, orders, products });
  // Total time: 200ms ✅ (2x faster!)
});
```

---

## Performance Monitoring Dashboard (What to Display)

### Simple Dashboard Example:

```
┌─────────────────────────────────────────┐
│  API Performance Dashboard              │
├─────────────────────────────────────────┤
│                                         │
│  🚀 Requests/Second: 1,234             │
│  ⏱️  Avg Response Time: 67ms           │
│  ✅ Success Rate: 99.8%                 │
│  ❌ Error Rate: 0.2%                    │
│                                         │
│  📊 Slowest Endpoints:                  │
│    1. POST /api/upload     - 2.3s      │
│    2. GET /api/reports     - 890ms     │
│    3. GET /api/analytics   - 450ms     │
│                                         │
│  🔥 Resource Usage:                     │
│    CPU: ████████░░ 45%                 │
│    Memory: ██████░░░░ 60%              │
│    Database: ███░░░░░░░ 30%            │
│                                         │
└─────────────────────────────────────────┘
```

---

## Real-World Monitoring Examples

### Example 1: E-Commerce API

**What to Monitor:**
```
1. Checkout endpoint response time
   → Alert if > 500ms (users abandon slow checkouts!)

2. Product search response time
   → Alert if > 200ms (users expect instant search)

3. Payment gateway errors
   → Alert immediately on ANY error (lost revenue!)

4. Shopping cart endpoint traffic
   → Spike means potential sales increase

5. Database connection pool
   → Alert if > 80% (about to run out)
```

**Dashboard:**
```
Top Priority Metrics:
- Checkout success rate: 98.5% ✅
- Average cart value: $67.32
- Payment failures: 1.2% ⚠️ (investigate!)
- Page load time: 1.2s
```

---

### Example 2: Social Media API

**What to Monitor:**
```
1. Feed load time
   → Alert if > 300ms (users scroll fast!)

2. Image upload success rate
   → Alert if < 95% (broken uploads frustrate users)

3. Real-time notification latency
   → Should be < 1 second

4. API calls per user
   → Detect unusual patterns (possible abuse)

5. Peak traffic times
   → Know when to scale up
```

**Dashboard:**
```
Real-Time Metrics:
- Active users: 45,234
- Posts per second: 127
- Image uploads/min: 890
- Failed uploads: 12 (1.3%) ✅
- Average feed load: 245ms ✅
```

---

### Example 3: Banking API

**What to Monitor:**
```
1. Transaction endpoint errors
   → Alert on ANY error (money is involved!)

2. Authentication failures
   → Spike might indicate attack

3. Account balance query time
   → Must be < 100ms (users check often)

4. Database replication lag
   → Alert if > 1 second (stale data)

5. Security events
   → Failed logins, suspicious patterns
```

**Dashboard:**
```
Critical Metrics:
- Transactions processed: 15,234
- Transaction errors: 0 ✅ (must be zero!)
- Avg transaction time: 45ms ✅
- Failed auth attempts: 23 ⚠️ (monitor for attacks)
- Uptime today: 100% ✅
```

---

## Common Performance Problems & Solutions

### Problem 1: Slow Database Queries

**Symptom:**
```
API response time: 2000ms (way too slow!)
```

**Diagnosis:**
```javascript
// Add query timing
const start = Date.now();
const users = await db.query('SELECT * FROM users WHERE status = "active"');
console.log(`Query took ${Date.now() - start}ms`);
// Output: Query took 1800ms ← PROBLEM FOUND!
```

**Solution:**
```sql
-- Add index
CREATE INDEX idx_users_status ON users(status);

-- Now query takes 50ms instead of 1800ms ✅
```

---

### Problem 2: Memory Leak

**Symptom:**
```
Memory usage slowly increases over time
Hour 1: 200 MB
Hour 2: 400 MB
Hour 3: 600 MB
Hour 4: 800 MB
Hour 5: SERVER CRASH! ❌
```

**Diagnosis:**
```javascript
// Bad: Storing data in global variable (never gets cleaned up!)
const cache = {};  // ← Memory leak!

app.get('/api/users/:id', async (req, res) => {
  cache[req.params.id] = await getUser(req.params.id);
  res.json(cache[req.params.id]);
});
// Cache grows forever, using more and more memory
```

**Solution:**
```javascript
// Good: Use Redis with expiration
app.get('/api/users/:id', async (req, res) => {
  const cached = await redis.get(`user:${req.params.id}`);
  if (cached) return res.json(JSON.parse(cached));
  
  const user = await getUser(req.params.id);
  await redis.setex(`user:${req.params.id}`, 300, JSON.stringify(user));  // Auto-expires in 5 min
  res.json(user);
});
// Memory stays constant ✅
```

---

### Problem 3: Too Many Database Connections

**Symptom:**
```
Error: "Too many connections to database"
Some requests fail randomly
```

**Diagnosis:**
```javascript
// Bad: Creating new connection for each request
app.get('/api/users/:id', async (req, res) => {
  const db = new Database();  // ← New connection every time!
  const user = await db.query(...);
  res.json(user);
  // Connection not closed!
});
```

**Solution:**
```javascript
// Good: Use connection pool (reuse connections)
const pool = new Pool({
  max: 20,  // Maximum 20 connections
  min: 5    // Always keep 5 ready
});

app.get('/api/users/:id', async (req, res) => {
  const user = await pool.query(...);  // ← Reuses existing connection
  res.json(user);
});
// Connections are reused efficiently ✅
```

---

## Monitoring Checklist

Before going to production:

- [ ] **Basic Logging:** Every request logged with duration
- [ ] **Error Tracking:** All errors captured with details
- [ ] **Performance Metrics:** Latency, traffic, errors, saturation tracked
- [ ] **Alerts Set Up:** Get notified when problems occur
- [ ] **Dashboard:** Can see API health at a glance
- [ ] **Database Monitoring:** Query performance tracked
- [ ] **Resource Monitoring:** CPU, memory, disk usage tracked
- [ ] **Uptime Monitoring:** External service checks if API is reachable
- [ ] **Regular Reviews:** Check metrics weekly
- [ ] **Documentation:** Team knows how to read dashboards

---

## Simple Monitoring Tools Comparison

| Tool | Cost | Complexity | Best For | Setup Time |
|------|------|------------|----------|------------|
| **Console.log** | Free | Very Low ⭐ | Learning/testing | 5 min |
| **Morgan (Express)** | Free | Low ⭐ | Simple logging | 10 min |
| **PM2 Monitoring** | Free | Low ⭐ | Node.js apps | 15 min |
| **Datadog** | $15/mo | Medium ⭐⭐ | Professional teams | 30 min |
| **New Relic** | Free tier | Medium ⭐⭐ | Great dashboards | 30 min |
| **Grafana + Prometheus** | Free | High ⭐⭐⭐ | Self-hosted | 2 hours |
| **AWS CloudWatch** | ~$10/mo | Low ⭐ | AWS users | 20 min |

---

## Quick Start: 15-Minute Monitoring Setup

**Step 1: Install Morgan (Request Logger)**
```bash
npm install morgan
```

**Step 2: Add to Your App**
```javascript
const morgan = require('morgan');

// Log every request
app.use(morgan('combined'));

// Now you see:
// 127.0.0.1 - - [01/Jan/2024:10:00:00 +0000] "GET /api/users/123 HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
```

**Step 3: Add Error Tracking**
```javascript
app.use((err, req, res, next) => {
  console.error({
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    timestamp: new Date()
  });
  
  res.status(500).json({ error: 'Internal server error' });
});
```

**Step 4: Create Health Endpoint**
```javascript
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    timestamp: new Date()
  });
});
```

**Step 5: Set Up Uptime Monitoring (Free)**

Go to **uptimerobot.com**:
1. Sign up (free)
2. Add your API: `https://yourapi.com/health`
3. Check every 5 minutes
4. Email you if it's down

**Done! You now have basic monitoring in 15 minutes! ✅**

---

## Summary: Monitoring & Performance

> **The Golden Rules:**
> 
> 1. **Monitor the 4 Golden Signals** → Latency, Traffic, Errors, Saturation
> 2. **Set up alerts** → Know about problems before users complain
> 3. **Start simple** → Basic logging is better than nothing
> 4. **Measure before optimizing** → Find the slow parts first
> 5. **Cache aggressively** → Can make APIs 10-100x faster

### What Good Monitoring Gives You

```
Without Monitoring:
- Find out about problems from angry users ❌
- Don't know what's slow ❌
- Can't prove improvements ❌
- Constantly putting out fires ❌

With Monitoring:
- Know about problems before users ✅
- See exactly what's slow ✅
- Measure impact of optimizations ✅
- Proactively prevent issues ✅
- Sleep better at night 😴✅
```

### Progressive Monitoring Approach

```
Week 1: Basic Logging
- Console.log with timestamps
- Error tracking
- Cost: $0

Week 2: Simple Dashboard
- Request counter
- Average response time
- Error rate
- Cost: $0

Week 3: Add Alerts
- High error rate alert
- Slow response time alert
- Cost: $0 (use free tier)

Week 4: Professional Tool
- Datadog or New Relic
- Beautiful dashboards
- Advanced alerts
- Cost: ~$15/month

Month 2+: Fine-tune
- Optimize based on data
- Add custom metrics
- Improve alerts
```

---

## Continue the Series

This is **Part 5** of the "Scaling Your API" series:

- **[Part 1: Performance & Infrastructure →]({{ site.baseurl }}/topics/scaling-api-1-to-1-million-rps/)** - Technical techniques to handle millions of requests
- **[Part 2: Design & Architecture →]({{ site.baseurl }}/topics/scaling-api-design-architecture-part-2/)** - Organizational strategies and API design patterns
- **[Part 3: Choosing the Right Database →]({{ site.baseurl }}/topics/choosing-the-right-database/)** - Database selection for your API
- **[Part 4: Load Balancing & High Availability →]({{ site.baseurl }}/topics/scaling-api-load-balancing-part-4/)** - Keeping your API always available
- **Part 5:** Monitoring & Performance ← You are here

---

## Further Reading

- **[Datadog Documentation](https://docs.datadoghq.com/)** — Learn professional monitoring
- **[Prometheus & Grafana Guide](https://prometheus.io/docs/introduction/overview/)** — Open source monitoring
- **[Google SRE Book](https://sre.google/books/)** — How Google monitors services
- **[New Relic University](https://learn.newrelic.com/)** — Free monitoring courses

---

**Remember:** You can't improve what you don't measure. Start monitoring today, even if it's just basic logging. Your future self (and your users) will thank you!


