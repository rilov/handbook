---
title: "Scaling Your API Part 4: Load Balancing & High Availability"
category: Architecture
tags:
  - load-balancing
  - high-availability
  - api
  - scaling
  - infrastructure
series: "Scaling Your API"
part: 4
summary: Learn how to keep your API running smoothly with load balancing and high availability — explained in simple terms anyone can understand.
related:
  - scaling-api-1-to-1-million-rps
  - scaling-api-design-architecture-part-2
  - choosing-the-right-database
  - scaling-api-monitoring-part-5
---

> **📚 This is Part 4 of the "Scaling Your API" Series**
> - **[Part 1: Performance & Infrastructure ←]({{ site.baseurl }}/topics/scaling-api-1-to-1-million-rps/)** - Technical techniques to handle millions of requests
> - **[Part 2: Design & Architecture ←]({{ site.baseurl }}/topics/scaling-api-design-architecture-part-2/)** - Organizational strategies and API design patterns
> - **[Part 3: Choosing the Right Database ←]({{ site.baseurl }}/topics/choosing-the-right-database/)** - Database selection for your API
> - **Part 4 (this page):** Load Balancing & High Availability - Keeping your API always available
> - **[Part 5: Monitoring & Performance →]({{ site.baseurl }}/topics/scaling-api-monitoring-part-5/)** - Tracking and improving API performance

## What is Load Balancing? (Explained Simply)

> **Think of it like a restaurant:** Imagine a busy restaurant with multiple cashiers. When customers arrive, a host directs them to the cashier with the shortest line. That's exactly what a load balancer does for your API!

<div class="mermaid">
flowchart LR
    USERS["👥 Users<br/>(1000s of requests)"]
    LB["⚖️ Load Balancer<br/>(Traffic Director)"]
    S1["🖥️ Server 1"]
    S2["🖥️ Server 2"]
    S3["🖥️ Server 3"]
    
    USERS --> LB
    LB --> S1
    LB --> S2
    LB --> S3
    
    style USERS fill:#dbeafe,stroke:#2563eb
    style LB fill:#fef3c7,stroke:#d97706
    style S1 fill:#d1fae5,stroke:#059669
    style S2 fill:#d1fae5,stroke:#059669
    style S3 fill:#d1fae5,stroke:#059669
</div>

### Without Load Balancer ❌

```
1 Server handling ALL requests
↓
Server gets overloaded
↓
API becomes slow or crashes
↓
Users get errors 😞
```

### With Load Balancer ✅

```
Load Balancer distributes requests across 3 servers
↓
Each server handles 1/3 of the traffic
↓
API stays fast and stable
↓
Users happy 😊
```

---

## Why Your API Needs Load Balancing

### Problem 1: Too Much Traffic for One Server

**Real-World Example:**
```
Your API normally gets 1,000 requests/second
One server can handle this easily

Black Friday arrives 🛍️
Suddenly: 10,000 requests/second
One server crashes 💥

With load balancer + 10 servers:
Each server handles 1,000 requests/second
API works perfectly ✅
```

### Problem 2: Server Crashes (It Happens!)

**What happens without load balancing:**
```
11:00 AM - Server running fine
11:30 AM - Server crashes due to bug
11:31 AM - Your entire API is DOWN
12:00 PM - You fix and restart server
Result: 30 minutes of downtime = Lost money & angry users
```

**What happens with load balancing (3 servers):**
```
11:00 AM - All 3 servers running fine
11:30 AM - Server 1 crashes
11:30 AM - Load balancer detects crash
11:31 AM - Traffic automatically goes to Server 2 & 3
11:31 AM - Your API is STILL WORKING
12:00 PM - You fix Server 1 in the background
Result: ZERO downtime = Happy users 😊
```

---

## How Load Balancers Work (Simple Explanation)

### 1. Round Robin (The Simplest Method)

> **Like taking turns:** Request 1 → Server A, Request 2 → Server B, Request 3 → Server C, Request 4 → Server A again...

```
Request 1 → Server 1 ✅
Request 2 → Server 2 ✅
Request 3 → Server 3 ✅
Request 4 → Server 1 ✅
Request 5 → Server 2 ✅
```

**When to use:** When all your servers are the same size and handle requests equally fast.

---

### 2. Least Connections

> **Like the shortest checkout line:** Send the next customer to the cashier with the fewest people waiting.

```
Server 1: 10 active connections
Server 2: 5 active connections ← Load balancer chooses this one!
Server 3: 8 active connections

Next request goes to Server 2 (least busy)
```

**When to use:** When some requests take longer than others (like uploading files).

---

### 3. Health Checks (Automatic Server Monitoring)

> **Like a doctor checking patients:** The load balancer regularly "pings" each server to make sure it's healthy.

```
Every 10 seconds:
Load Balancer: "Hey Server 1, are you ok?"
Server 1: "Yes! ✅"

Load Balancer: "Hey Server 2, are you ok?"
Server 2: "Yes! ✅"

Load Balancer: "Hey Server 3, are you ok?"
Server 3: *No response* ❌

Load Balancer: "Server 3 is down! Stop sending traffic there!"
```

**Result:** Users never see errors because traffic automatically goes to healthy servers.

---

## What is High Availability? (Simple Explanation)

> **High Availability = Your API is ALWAYS available, even when things break**

### The 9's of Availability

| Availability | Downtime per Year | What This Means |
|--------------|-------------------|-----------------|
| **99% ("Two Nines")** | 3.65 days | Your API is down for nearly 4 days/year ❌ |
| **99.9% ("Three Nines")** | 8.76 hours | Down for less than 9 hours/year 😐 |
| **99.99% ("Four Nines")** | 52 minutes | Down for less than 1 hour/year ✅ |
| **99.999% ("Five Nines")** | 5 minutes | Down for only 5 minutes/year 🎯 |

**Most companies aim for 99.9% - 99.99%**

---

## Building High Availability (Step by Step)

### Step 1: Multiple Servers (No Single Point of Failure)

<div class="mermaid">
flowchart TD
    BAD["❌ Single Server<br/>(If it crashes, you're done)"]
    GOOD["✅ Multiple Servers<br/>(If one crashes, others continue)"]
    
    style BAD fill:#fee,stroke:#f00
    style GOOD fill:#d1fae5,stroke:#059669
</div>

**Example Setup:**
```
Minimum: 2 servers (one can fail, API still works)
Recommended: 3+ servers (better for traffic distribution)
Enterprise: 10+ servers across multiple data centers
```

---

### Step 2: Health Checks (Automatic Problem Detection)

**Simple Health Check Example:**

```javascript
// Your API endpoint that load balancer checks
app.get('/health', (req, res) => {
  // Check if database is connected
  if (database.isConnected()) {
    res.status(200).json({ status: 'healthy' });
  } else {
    res.status(500).json({ status: 'unhealthy' });
  }
});
```

**Load balancer checks this every 10 seconds:**
```
Response 200 (OK) → Server is healthy ✅ → Keep sending traffic
Response 500 (Error) → Server is unhealthy ❌ → Stop sending traffic
```

---

### Step 3: Automatic Failover

> **Failover = Automatically switching to backup when main server fails**

**How It Works:**

<div class="mermaid">
sequenceDiagram
    participant Users
    participant LoadBalancer
    participant Server1
    participant Server2
    
    Users->>LoadBalancer: Request
    LoadBalancer->>Server1: Forward request
    Server1--xLoadBalancer: No response (crashed!)
    LoadBalancer->>Server2: Try Server 2
    Server2->>LoadBalancer: Success!
    LoadBalancer->>Users: Response
    
    Note over LoadBalancer: Server 1 marked unhealthy<br/>All traffic goes to Server 2
</sequenceDiagram>
</div>

**What users experience:** Nothing! They don't even know Server 1 crashed.

---

### Step 4: Multiple Data Centers (Geographic Redundancy)

> **Think of it like having restaurant locations in different cities**

<div class="mermaid">
flowchart TD
    USERS["🌍 Global Users"]
    DNS["🌐 DNS / Global Load Balancer"]
    
    DC1["🏢 Data Center 1<br/>New York"]
    DC2["🏢 Data Center 2<br/>London"]
    DC3["🏢 Data Center 3<br/>Tokyo"]
    
    USERS --> DNS
    DNS --> DC1
    DNS --> DC2
    DNS --> DC3
    
    style USERS fill:#dbeafe,stroke:#2563eb
    style DNS fill:#fef3c7,stroke:#d97706
    style DC1 fill:#d1fae5,stroke:#059669
    style DC2 fill:#d1fae5,stroke:#059669
    style DC3 fill:#d1fae5,stroke:#059669
</div>

**Benefits:**
```
✅ If entire data center goes down → Traffic goes to other data centers
✅ Users get routed to closest data center → Faster responses
✅ Can handle MASSIVE traffic (millions of requests/second)
```

---

## Popular Load Balancer Solutions

### For Beginners (Managed Services)

| Service | Best For | Cost | Complexity |
|---------|----------|------|------------|
| **AWS Application Load Balancer** | Most people on AWS | ~$20/month | Low ⭐ |
| **Google Cloud Load Balancing** | Google Cloud users | ~$20/month | Low ⭐ |
| **Cloudflare Load Balancing** | Simple setup, any provider | $5-50/month | Very Low 🌟 |
| **DigitalOcean Load Balancer** | Small projects | $12/month | Very Low 🌟 |

---

### Self-Hosted (More Control)

| Tool | Best For | Cost | Complexity |
|------|----------|------|------------|
| **Nginx** | Most flexible, free | Free | Medium ⭐⭐ |
| **HAProxy** | High performance | Free | Medium ⭐⭐ |
| **Traefik** | Modern, Docker-friendly | Free | Low ⭐ |

---

## Real-World Setup Examples

### Example 1: Small Startup (1,000 requests/second)

```
Setup:
├── 2 API Servers (for redundancy)
├── 1 Load Balancer (DigitalOcean or AWS)
└── Health checks every 10 seconds

Cost: ~$50/month
Uptime: 99.9% (less than 9 hours downtime/year)
Can handle: One server failure with zero downtime
```

**Configuration:**
```nginx
# Simple Nginx Load Balancer Config
upstream api_servers {
    server api1.example.com:3000;  # Server 1
    server api2.example.com:3000;  # Server 2
}

server {
    listen 80;
    
    location / {
        proxy_pass http://api_servers;
        
        # Health check
        proxy_next_upstream error timeout http_500;
        proxy_connect_timeout 2s;
    }
}
```

---

### Example 2: Growing Company (10,000 requests/second)

```
Setup:
├── 5 API Servers (distributed load)
├── 2 Load Balancers (for load balancer redundancy!)
├── Auto-scaling (add more servers when traffic spikes)
└── Health checks every 5 seconds

Cost: ~$500/month
Uptime: 99.95% (4 hours downtime/year)
Can handle: 2 server failures + traffic spikes
```

**Features:**
- **Auto-scaling:** Automatically add servers during traffic spikes
- **Load balancer redundancy:** Even the load balancer has a backup
- **Advanced health checks:** Check database connections, not just "is server on?"

---

### Example 3: Enterprise (100,000+ requests/second)

```
Setup:
├── 3 Geographic Regions (US, Europe, Asia)
│   ├── 10 API Servers per region
│   ├── Local load balancers
│   └── Local databases
├── Global Load Balancer (routes by geography)
├── Auto-scaling in each region
└── Health checks every 2 seconds

Cost: ~$10,000/month
Uptime: 99.99% (52 minutes downtime/year)
Can handle: Entire data center failure
```

---

## Common Load Balancing Patterns

### Pattern 1: Active-Active (All Servers Working)

```
All servers handle traffic simultaneously
Load balancer distributes evenly

Server 1: ████████ 33% traffic
Server 2: ████████ 33% traffic
Server 3: ████████ 34% traffic

Best for: Maximum performance, all resources utilized
```

---

### Pattern 2: Active-Passive (Backup on Standby)

```
One server handles traffic, backup ready

Server 1: ████████████████ 100% traffic (ACTIVE)
Server 2: ................ 0% traffic (STANDBY)

If Server 1 fails:
Server 2: ████████████████ 100% traffic (NOW ACTIVE)

Best for: Critical systems where you need guaranteed backup
```

---

### Pattern 3: Session Sticky (User Always Goes to Same Server)

> **Like having a regular cashier at your favorite store**

```
User A always → Server 1
User B always → Server 2
User C always → Server 1

Why? User's session data is stored on that server
```

**When to use:** When you store user sessions in server memory (not recommended for high availability)

**Better approach:** Store sessions in Redis so any server can handle any user

---

## Step-by-Step: Setting Up Your First Load Balancer

### Option 1: Using Cloudflare (Easiest - 5 Minutes)

```
Step 1: Sign up for Cloudflare (free)
Step 2: Add your domain
Step 3: Go to Traffic → Load Balancing
Step 4: Add your server IPs
Step 5: Enable health checks
Done! ✅

Your API now has:
- Load balancing
- Automatic failover
- DDoS protection (bonus!)
```

---

### Option 2: AWS Application Load Balancer (15 Minutes)

```
Step 1: Go to AWS EC2 Console
Step 2: Click "Load Balancers" → "Create"
Step 3: Choose "Application Load Balancer"
Step 4: Add your EC2 instances
Step 5: Configure health check:
        - Path: /health
        - Interval: 10 seconds
        - Healthy threshold: 2
Step 6: Create!

Cost: ~$20/month
Setup time: 15 minutes
```

---

### Option 3: Simple Nginx Setup (30 Minutes)

**Install Nginx:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx
```

**Create config file:**
```nginx
# /etc/nginx/sites-available/loadbalancer

upstream myapi {
    # Round-robin between 3 servers
    server 192.168.1.10:3000;
    server 192.168.1.11:3000;
    server 192.168.1.12:3000;
}

server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://myapi;
        
        # Forward user's real IP
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Automatic retry on failure
        proxy_next_upstream error timeout http_500;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200;
    }
}
```

**Enable and restart:**
```bash
sudo ln -s /etc/nginx/sites-available/loadbalancer /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

**Done! Your API now has load balancing ✅**

---

## Testing Your Load Balancer

### Test 1: Is Traffic Being Distributed?

**Add logging to your API:**
```javascript
app.get('/api/test', (req, res) => {
  console.log(`Request handled by: ${process.env.SERVER_NAME}`);
  res.json({ 
    server: process.env.SERVER_NAME,
    timestamp: new Date()
  });
});
```

**Make multiple requests:**
```bash
# Request 1
curl https://api.example.com/api/test
# Response: {"server":"Server-1","timestamp":"2024-01-01..."}

# Request 2
curl https://api.example.com/api/test
# Response: {"server":"Server-2","timestamp":"2024-01-01..."}

# Request 3
curl https://api.example.com/api/test
# Response: {"server":"Server-3","timestamp":"2024-01-01..."}
```

**If you see different servers → Load balancing is working! ✅**

---

### Test 2: Does Failover Work?

**Simulate server crash:**
```bash
# Stop one API server
ssh server1.example.com
sudo systemctl stop myapi

# Make requests - they should still work!
for i in {1..10}; do
  curl https://api.example.com/api/test
done

# All requests should succeed (using other servers)
```

**If requests still work → Failover is working! ✅**

---

### Test 3: Health Check Working?

**Check load balancer status:**

**AWS:**
```
Go to EC2 → Target Groups → Your group
Check "Targets" tab
Healthy targets: 2/3 (one is down)
```

**Nginx:**
```bash
# Check error logs
sudo tail -f /var/log/nginx/error.log

# You should see:
# "upstream server 192.168.1.10:3000 failed... no live upstreams"
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: No Health Checks

```
Bad: Load balancer sends traffic to crashed server
Result: Users get errors

Good: Health checks detect crash in seconds
Result: Traffic automatically goes to healthy servers
```

**Fix:** Always configure health checks (every 10-30 seconds)

---

### ❌ Mistake 2: Only 1 Server (No Redundancy)

```
Bad: 1 server + load balancer
Result: If server crashes, API is completely down

Good: Minimum 2 servers
Result: One can fail, API still works
```

**Fix:** Always have at least 2 servers for production

---

### ❌ Mistake 3: Session Stored on Individual Servers

```
Bad: User logged in on Server 1, load balancer sends next request to Server 2
Result: User appears logged out (session lost)

Good: Store sessions in Redis (shared across all servers)
Result: User stays logged in regardless of which server handles request
```

**Fix:** Use centralized session storage (Redis, database)

---

### ❌ Mistake 4: All Servers in Same Data Center

```
Bad: 5 servers all in same building
Result: Power outage → ALL servers down

Good: Servers in multiple data centers or cloud regions
Result: One location fails → Other locations continue working
```

**Fix:** Use multiple availability zones or regions

---

## High Availability Checklist

Before launching your API to production:

- [ ] **Multiple Servers:** At least 2, preferably 3+
- [ ] **Load Balancer:** Distributing traffic automatically
- [ ] **Health Checks:** Configured to detect failures (10-30 second intervals)
- [ ] **Automatic Failover:** Traffic routes away from failed servers
- [ ] **Centralized Sessions:** Redis or database (not server memory)
- [ ] **Database Redundancy:** Read replicas or backup database
- [ ] **Monitoring:** Alerts when servers go down
- [ ] **Backup Plan:** Know how to quickly add more servers
- [ ] **Testing:** Regularly test failover scenarios
- [ ] **Documentation:** Team knows how to respond to outages

---

## Summary: Load Balancing & High Availability

> **The Golden Rules:**
> 
> 1. **Never run just 1 server in production** → Minimum 2 for redundancy
> 2. **Always use load balancer** → Automatic traffic distribution + failover
> 3. **Configure health checks** → Detect failures in seconds, not minutes
> 4. **Store sessions centrally** → Users stay logged in across all servers
> 5. **Test your failover** → Don't wait for real crash to find out it doesn't work!

### What You Get With Proper Load Balancing

```
Without Load Balancer:
- Single point of failure ❌
- Limited traffic capacity ❌
- Manual intervention when things break ❌
- Downtime during deployments ❌

With Load Balancer:
- Automatic failover ✅
- Handle 10x more traffic ✅
- Self-healing (automatic recovery) ✅
- Zero-downtime deployments ✅
- Happy users even when things break ✅
```

### Next Steps

1. **Start Simple:** 2 servers + managed load balancer (AWS, DigitalOcean, Cloudflare)
2. **Monitor:** Set up alerts for server health
3. **Test:** Regularly test failover by intentionally stopping servers
4. **Scale:** Add more servers as traffic grows
5. **Improve:** Add multiple regions when needed

---

## Continue the Series

This is **Part 4** of the "Scaling Your API" series:

- **[Part 1: Performance & Infrastructure →]({{ site.baseurl }}/topics/scaling-api-1-to-1-million-rps/)** - Technical techniques to handle millions of requests
- **[Part 2: Design & Architecture →]({{ site.baseurl }}/topics/scaling-api-design-architecture-part-2/)** - Organizational strategies and API design patterns
- **[Part 3: Choosing the Right Database →]({{ site.baseurl }}/topics/choosing-the-right-database/)** - Database selection for your API
- **Part 4:** Load Balancing & High Availability ← You are here
- **[Part 5: Monitoring & Performance →]({{ site.baseurl }}/topics/scaling-api-monitoring-part-5/)** - Tracking and improving API performance

---

## Further Reading

- **[Nginx Load Balancing Docs](https://nginx.org/en/docs/http/load_balancing.html)** — Learn Nginx load balancing
- **[AWS Application Load Balancer](https://aws.amazon.com/elasticloadbalancing/)** — Managed load balancing on AWS
- **[HAProxy Configuration](https://www.haproxy.org/)** — High-performance load balancer
- **[Site Reliability Engineering Book](https://sre.google/books/)** — Google's approach to reliability

---

**Remember:** Load balancing isn't about perfection — it's about keeping your API running when things go wrong (and they will!). Start simple, test often, and improve over time.


