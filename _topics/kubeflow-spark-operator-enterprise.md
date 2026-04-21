---
title: "Kubeflow Spark Operator - Enterprise & Multi-Tenant"
category: Data
order: 16
tags: [spark, kubernetes, multi-tenant, enterprise, devops, platform-engineering]
summary: "Enterprise-grade Spark on Kubernetes: multi-tenant architecture, centralized logging and monitoring, self-service job submission portals, cost tracking, and security best practices for running Spark at scale."
---

# Kubeflow Spark Operator - Enterprise & Multi-Tenant Architecture

## What is This?

**Simple Answer:** This guide shows you how to run Spark for multiple teams on a shared Kubernetes cluster with centralized logging, cost tracking, and self-service job submission—**without giving teams direct kubectl access**.

**Why Should You Care?**
- 🏢 **Multi-Team Support**: Multiple teams share one cluster safely
- 🔒 **No kubectl Access Needed**: Teams submit jobs via web portal or API
- ⏰ **Self-Service Scheduling**: Teams schedule their own recurring jobs (hourly, daily, weekly)
- 📊 **Centralized Logging**: All logs in one place (Elasticsearch/Kibana)
- 💰 **Cost Tracking**: Know exactly what each team is spending
- 🎯 **Resource Quotas**: Prevent teams from hogging resources
- 🔐 **Security**: Network isolation, RBAC, audit trails

## The Enterprise Challenge

### Scenario: You're a Platform Team

You manage a Kubernetes cluster and need to support:
- **Team A (Data Engineering)**: Runs ETL pipelines daily
- **Team B (ML Platform)**: Trains models weekly
- **Team C (Analytics)**: Generates reports on-demand

**Requirements:**
1. ❌ Teams should **NOT** have `kubectl` or `oc` access
2. ✅ Each team gets their own resource quota
3. ✅ Teams can submit AND schedule jobs via web UI or API
4. ✅ All logs go to a central location
5. ✅ Track costs per team for chargeback
6. ✅ Secure: teams can't see each other's data

## Architecture Overview

<div class="mermaid">
graph TB
    subgraph PLATFORM["<b>Platform Team - Shared Services</b>"]
        OPERATOR["<b>Spark Operator</b><br/>Watches all namespaces"]
        HISTORY["<b>History Server</b><br/>Centralized Spark UI"]
        LOGGING["<b>Logging Stack</b><br/>Elasticsearch + Kibana"]
        MONITORING["<b>Monitoring</b><br/>Prometheus + Grafana"]
        PORTAL["<b>Job Portal</b><br/>Self-service UI"]
    end
    
    subgraph TEAM_A["<b>Team A - Data Engineering</b>"]
        NS_A["<b>Namespace</b><br/>team-a-spark"]
        QUOTA_A["<b>Quota</b><br/>10 CPU, 40Gi RAM"]
    end
    
    subgraph TEAM_B["<b>Team B - ML Platform</b>"]
        NS_B["<b>Namespace</b><br/>team-b-spark"]
        QUOTA_B["<b>Quota</b><br/>20 CPU, 80Gi RAM"]
    end
    
    subgraph TEAM_C["<b>Team C - Analytics</b>"]
        NS_C["<b>Namespace</b><br/>team-c-spark"]
        QUOTA_C["<b>Quota</b><br/>5 CPU, 20Gi RAM"]
    end
    
    PORTAL -->|Submit jobs| OPERATOR
    OPERATOR -->|Manage| NS_A
    OPERATOR -->|Manage| NS_B
    OPERATOR -->|Manage| NS_C
    
    NS_A -.->|Logs| LOGGING
    NS_B -.->|Logs| LOGGING
    NS_C -.->|Logs| LOGGING
    
    NS_A -.->|Metrics| MONITORING
    NS_B -.->|Metrics| MONITORING
    NS_C -.->|Metrics| MONITORING
    
    NS_A -.->|Event logs| HISTORY
    NS_B -.->|Event logs| HISTORY
    NS_C -.->|Event logs| HISTORY
    
    style PLATFORM fill:#E8EAF6,stroke:#3F51B5,stroke-width:3px,color:#000
    style TEAM_A fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#000
    style TEAM_B fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#000
    style TEAM_C fill:#FCE4EC,stroke:#E91E63,stroke-width:2px,color:#000
</div>

**Key Components:**
- **Platform Team** manages shared services (operator, logging, monitoring, portal)
- **Each Team** gets their own namespace with resource quotas
- **Centralized Services** collect logs, metrics, and provide UIs
- **Job Portal** allows teams to submit jobs without kubectl access

## Part 1: Multi-Tenant Setup

### Step 1: Create Team Namespaces

Each team gets their own namespace with labels for tracking:

```yaml
# Team A namespace
apiVersion: v1
kind: Namespace
metadata:
  name: team-a-spark
  labels:
    team: data-engineering
    cost-center: "1001"
    environment: production
---
# Team B namespace
apiVersion: v1
kind: Namespace
metadata:
  name: team-b-spark
  labels:
    team: ml-platform
    cost-center: "1002"
    environment: production
```

### Step 2: Set Resource Quotas

Prevent teams from using too many resources:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: spark-quota
  namespace: team-a-spark
spec:
  hard:
    requests.cpu: "10"        # Max 10 CPUs requested
    requests.memory: 40Gi     # Max 40GB memory requested
    limits.cpu: "20"          # Max 20 CPUs total
    limits.memory: 80Gi       # Max 80GB memory total
    pods: "50"                # Max 50 pods
```

**What This Means:**
- Team A can run jobs using up to 10 CPUs and 40GB RAM
- If they try to exceed this, new jobs will be rejected
- Prevents one team from starving others

### Step 3: Configure RBAC (Permissions)

**Platform Team** (has full access):

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark-operator
  namespace: spark-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: spark-operator-role
rules:
- apiGroups: ["sparkoperator.k8s.io"]
  resources: ["sparkapplications", "scheduledsparkapplications"]
  verbs: ["*"]
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["*"]
```

**Team Service Accounts** (namespace-scoped):

```yaml
# Team A - Driver can create executors in team-a-spark namespace only
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark-driver
  namespace: team-a-spark
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: spark-driver-role
  namespace: team-a-spark
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["create", "get", "list", "delete"]
```

**Result:** Teams can only create resources in their own namespace.

## Part 2: Centralized Logging

### Why Centralized Logging?

**Without it:**
- Each team runs `kubectl logs` individually
- Logs disappear when pods are deleted
- Hard to search across multiple jobs
- No historical analysis

**With it:**
- All logs in Elasticsearch
- Search across all teams (with filters)
- Logs persist after pods are deleted
- Team-specific dashboards in Kibana

### Architecture

<div class="mermaid">
graph LR
    SPARK["<b>Spark Pods</b><br/>All Teams"] -->|stdout/stderr| FLUENTD["<b>Fluentd</b><br/>Collects logs"]
    FLUENTD -->|Parse & tag| ELASTIC["<b>Elasticsearch</b><br/>Stores logs"]
    ELASTIC -->|Query| KIBANA["<b>Kibana</b><br/>Search UI"]
    
    USER["<b>Team Member</b>"] -->|Search logs| KIBANA
    
    style SPARK fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style FLUENTD fill:#FF9800,stroke:#F57C00,stroke-width:2px,color:#fff
    style ELASTIC fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#fff
    style KIBANA fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style USER fill:#E91E63,stroke:#C2185B,stroke-width:2px,color:#fff
</div>

### Fluentd Configuration

Fluentd runs on every Kubernetes node and:
1. Collects all container logs
2. Filters for Spark pods
3. Adds team metadata from namespace labels
4. Sends to Elasticsearch with team-specific indices

```yaml
# Fluentd config (simplified)
<source>
  @type tail
  path /var/log/containers/*spark*.log
  tag kubernetes.*
</source>

# Add team metadata from namespace labels
<filter kubernetes.**>
  @type record_transformer
  <record>
    team ${record.dig("kubernetes", "namespace_labels", "team")}
    cost_center ${record.dig("kubernetes", "namespace_labels", "cost-center")}
    namespace ${record.dig("kubernetes", "namespace_name")}
  </record>
</filter>

# Send to Elasticsearch with team-specific index
<match kubernetes.**>
  @type elasticsearch
  host elasticsearch.logging.svc.cluster.local
  logstash_prefix spark-${team}  # Creates spark-data-engineering-*, spark-ml-platform-*
</match>
```

**Result:**
- Team A logs go to `spark-data-engineering-*` index
- Team B logs go to `spark-ml-platform-*` index
- Each team can only see their own logs in Kibana

### Kibana Dashboards

Teams get pre-configured dashboards showing:
- Recent job failures
- Error rate trends
- Slowest jobs
- Resource usage over time

## Part 3: Centralized History Server

### What is Spark History Server?

A web UI that shows:
- All completed Spark jobs
- Job timelines and stages
- Task metrics and executor info
- SQL query plans

### Setup

**S3 Bucket Structure:**
```
s3://company-spark-logs/
├── team-a-spark/
│   ├── etl-pipeline-20260420-120000/
│   └── data-quality-20260420-130000/
├── team-b-spark/
│   ├── feature-engineering-20260420-140000/
│   └── model-training-20260420-150000/
└── team-c-spark/
    └── reporting-20260420-160000/
```

**History Server Deployment:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-history-server
  namespace: spark-history
spec:
  containers:
  - name: spark-history-server
    image: apache/spark:3.5.0
    command:
    - /opt/spark/bin/spark-class
    - org.apache.spark.deploy.history.HistoryServer
    env:
    - name: SPARK_HISTORY_OPTS
      value: >-
        -Dspark.history.fs.logDirectory=s3a://company-spark-logs
        -Dspark.history.ui.port=18080
```

**Team Job Configuration:**

```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: etl-pipeline
  namespace: team-a-spark
spec:
  sparkConf:
    "spark.eventLog.enabled": "true"
    "spark.eventLog.dir": "s3a://company-spark-logs/team-a-spark"
```

**Access:** `https://spark-history.company.com` shows all teams' jobs (with authentication)

## Part 4: Cost Tracking

### Why Track Costs?

- **Chargeback**: Bill teams for their usage
- **Optimization**: Identify expensive jobs
- **Budgeting**: Plan capacity needs

### How It Works

Prometheus collects metrics → Recording rules calculate costs → Grafana displays dashboards

**Prometheus Recording Rules:**

```yaml
groups:
- name: spark_cost_tracking
  rules:
  # CPU usage by team
  - record: spark:cpu_usage:by_team
    expr: |
      sum by (team, namespace) (
        rate(container_cpu_usage_seconds_total{
          namespace=~"team-.*-spark",
          pod=~".*-(driver|exec)-.*"
        }[5m])
      )
  
  # Cost calculation ($0.05 per CPU-hour, $0.01 per GB-hour)
  - record: spark:cost:hourly:by_team
    expr: |
      (
        spark:cpu_usage:by_team * 0.05 +
        (spark:memory_usage:by_team / 1024 / 1024 / 1024) * 0.01
      )
```

**Grafana Dashboard Shows:**
- Team A: $45/day
- Team B: $120/day
- Team C: $18/day
- **Total: $183/day**

## Part 5: Job Submission Without kubectl Access

### The Problem

You **don't want** teams running:
```bash
kubectl apply -f my-job.yaml
```

**Why not?**
- Security risk (teams could modify other resources)
- No validation (teams could exceed quotas)
- No audit trail (who submitted what?)

### Solution: Self-Service Portal

Teams submit jobs via a web UI or REST API instead of kubectl.

<div class="mermaid">
sequenceDiagram
    participant User as Team Member
    participant Portal as Web Portal
    participant API as Backend API
    participant K8s as Kubernetes
    
    User->>Portal: Fill job form
    Portal->>API: POST /api/jobs/submit
    API->>API: Validate quota
    API->>API: Check S3 paths
    API->>K8s: Create SparkApplication
    K8s-->>API: Created
    API-->>Portal: Job submitted!
    Portal-->>User: Success message
</div>

### Option 1: Web Portal (Recommended)

**User Experience:**
1. User opens `https://spark-portal.company.com`
2. Fills out a form:
   - Team: Data Engineering
   - JAR path: `s3://team-a-data/etl.jar`
   - Main class: `com.company.ETL`
   - Resources: 5 executors, 2 cores each
   - **Schedule (Optional):** `0 2 * * *` (daily at 2 AM)
3. Clicks "Submit" or "Schedule"
4. Portal validates and creates SparkApplication or ScheduledSparkApplication

**Backend API (Python/FastAPI):**

```python
from fastapi import FastAPI, HTTPException
from kubernetes import client, config

app = FastAPI()
config.load_incluster_config()
k8s_custom = client.CustomObjectsApi()

TEAM_CONFIG = {
    "data-engineering": {
        "namespace": "team-a-spark",
        "max_executor_instances": 20,
        "allowed_s3_paths": ["s3://team-a-data/*"]
    }
}

@app.post("/api/jobs/submit")
async def submit_job(request: SparkJobRequest):
    # Validate team quota
    config = TEAM_CONFIG[request.team]
    if request.executor_instances > config["max_executor_instances"]:
        raise HTTPException(400, "Too many executors")
    
    # Check S3 path access
    if not request.jar_path.startswith("s3://team-a-data/"):
        raise HTTPException(403, "Access denied to S3 path")
    
    # Build base job spec
    job_spec = {
        "type": "Scala",
        "image": f"company-registry/spark:3.5.0",
        "mainClass": request.main_class,
        "mainApplicationFile": request.jar_path,
        "driver": {"cores": 1, "memory": "1g"},
        "executor": {
            "cores": request.executor_cores,
            "instances": request.executor_instances,
            "memory": "2g"
        }
    }
    
    # Check if this is a scheduled job
    if request.schedule:
        # Create ScheduledSparkApplication
        spark_app = {
            "apiVersion": "sparkoperator.k8s.io/v1beta2",
            "kind": "ScheduledSparkApplication",
            "metadata": {
                "name": request.job_name,
                "namespace": config["namespace"]
            },
            "spec": {
                "schedule": request.schedule,  # Cron format
                "concurrencyPolicy": "Forbid",  # Don't run if previous still running
                "template": job_spec
            }
        }
        plural = "scheduledsparkapplications"
    else:
        # Create one-time SparkApplication
        spark_app = {
            "apiVersion": "sparkoperator.k8s.io/v1beta2",
            "kind": "SparkApplication",
            "metadata": {
                "name": request.job_name,
                "namespace": config["namespace"]
            },
            "spec": job_spec
        }
        plural = "sparkapplications"
    
    # Submit to Kubernetes (using portal's service account)
    k8s_custom.create_namespaced_custom_object(
        group="sparkoperator.k8s.io",
        version="v1beta2",
        namespace=config["namespace"],
        plural=plural,
        body=spark_app
    )
    
    status = "scheduled" if request.schedule else "submitted"
    return {
        "status": status,
        "job_name": request.job_name,
        "schedule": request.schedule if request.schedule else None
    }
```

**Key Points:**
- ✅ Portal has a service account with SparkApplication create permissions
- ✅ Teams authenticate via OAuth (Okta, Azure AD, etc.)
- ✅ Backend validates quotas and S3 paths
- ✅ All submissions are logged for audit

### Option 2: REST API (For Automation)

Teams can submit jobs from CI/CD pipelines or notebooks:

```python
# Client library for teams
import requests

client = SparkJobClient(
    api_url="https://spark-portal.company.com",
    team="data-engineering",
    api_token="team-a-token-xyz"
)

# Submit one-time job
result = client.submit_job(
    job_name="etl-pipeline-20260420",
    jar_path="s3://team-a-data/etl-pipeline.jar",
    main_class="com.company.etl.Pipeline",
    executor_instances=10
)

# Schedule recurring job (daily at 2 AM)
scheduled = client.submit_job(
    job_name="daily-etl",
    jar_path="s3://team-a-data/etl-pipeline.jar",
    main_class="com.company.etl.DailyPipeline",
    executor_instances=10,
    schedule="0 2 * * *"  # Cron format
)

# Schedule hourly aggregation
hourly = client.submit_job(
    job_name="hourly-agg",
    jar_path="s3://team-a-data/aggregation.jar",
    main_class="com.company.agg.Hourly",
    executor_instances=5,
    schedule="0 * * * *"  # Every hour
)
```

**Common Cron Schedules:**
- `0 2 * * *` - Daily at 2 AM
- `0 * * * *` - Every hour
- `*/15 * * * *` - Every 15 minutes
- `0 0 * * 0` - Weekly on Sunday at midnight
- `0 0 1 * *` - Monthly on the 1st at midnight

### Option 3: GitOps (For Production)

Teams push YAML files to Git → CI/CD validates and applies:

**One-Time Job:**
```yaml
# teams/data-engineering/etl-pipeline.yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: etl-pipeline
  namespace: team-a-spark
spec:
  type: Scala
  image: company-registry/spark:3.5.0
  mainClass: com.company.etl.Pipeline
  mainApplicationFile: s3://team-a-data/etl.jar
  driver:
    cores: 1
    memory: "1g"
  executor:
    cores: 2
    instances: 10
    memory: "2g"
```

**Scheduled Job (Recurring):**
```yaml
# teams/data-engineering/daily-etl.yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: ScheduledSparkApplication
metadata:
  name: daily-etl
  namespace: team-a-spark
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  concurrencyPolicy: Forbid  # Don't run if previous job still running
  successfulRunHistoryLimit: 3  # Keep last 3 successful runs
  failedRunHistoryLimit: 1      # Keep last failed run
  
  template:
    type: Scala
    image: company-registry/spark:3.5.0
    mainClass: com.company.etl.DailyPipeline
    mainApplicationFile: s3://team-a-data/etl.jar
    driver:
      cores: 2
      memory: "2g"
    executor:
      cores: 4
      instances: 10
      memory: "4g"
```

**GitHub Actions Workflow:**
1. Developer pushes YAML to Git
2. CI validates against team quota
3. If valid, CI runs `kubectl apply`
4. PR comment shows job status

### Team Scheduling Capabilities

**What Teams Can Schedule:**

Teams have full control to schedule their own Spark jobs using cron expressions:

| Schedule Type | Cron Expression | Use Case | Example |
|--------------|-----------------|----------|---------|
| **Hourly** | `0 * * * *` | Real-time aggregations | Hourly sales summaries |
| **Daily** | `0 2 * * *` | Nightly ETL pipelines | Daily data warehouse refresh |
| **Weekly** | `0 0 * * 0` | Weekly reports | Sunday night model training |
| **Monthly** | `0 0 1 * *` | Monthly processing | First of month billing |
| **Custom** | `*/15 * * * *` | High-frequency jobs | Every 15 minutes monitoring |

**Scheduling Features:**

✅ **Concurrency Control**: `concurrencyPolicy: Forbid` prevents overlapping runs

✅ **History Limits**: Keep last N successful/failed runs for debugging

✅ **Timezone Support**: Configure timezone for schedules

✅ **Suspend/Resume**: Temporarily pause scheduled jobs without deleting

**Example: Managing Scheduled Jobs**

```python
# List all scheduled jobs for a team
GET /api/jobs/data-engineering/scheduled

# Suspend a scheduled job (pause it)
PATCH /api/jobs/data-engineering/daily-etl
{
  "suspend": true
}

# Resume a scheduled job
PATCH /api/jobs/data-engineering/daily-etl
{
  "suspend": false
}

# Delete a scheduled job
DELETE /api/jobs/data-engineering/daily-etl
```

### Comparison

| Method | Best For | Scheduling Support | Pros | Cons |
|--------|----------|-------------------|------|------|
| **Web Portal** | Non-technical users, ad-hoc jobs | ✅ Yes - cron picker UI | Easy to use, visual validation | Requires portal maintenance |
| **REST API** | Automated pipelines, notebooks | ✅ Yes - schedule parameter | Scriptable, CI/CD friendly | Requires API tokens |
| **GitOps** | Production jobs, compliance | ✅ Yes - ScheduledSparkApplication | Version control, code review | Slower feedback loop |

## Part 6: Security & Network Isolation

### Network Policies

Prevent teams from talking to each other:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: spark-isolation
  namespace: team-a-spark
spec:
  podSelector:
    matchLabels:
      spark-role: driver
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Only allow from executors in same namespace
  - from:
    - namespaceSelector:
        matchLabels:
          name: team-a-spark
  egress:
  # Allow to executors and external services (S3)
  - to:
    - namespaceSelector:
        matchLabels:
          name: team-a-spark
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443  # HTTPS for S3
```

**Result:** Team A's Spark jobs can't communicate with Team B's jobs.

## Complete Architecture Summary

<div class="mermaid">
graph TB
    subgraph USERS["<b>Team Members</b>"]
        DEV["<b>Developer</b>"]
    end
    
    subgraph SUBMISSION["<b>Job Submission</b>"]
        PORTAL["<b>Web Portal</b>"]
        API["<b>REST API</b>"]
    end
    
    subgraph PLATFORM["<b>Platform Services</b>"]
        VALIDATE["<b>Validation</b><br/>Check quotas & policies"]
        OPERATOR["<b>Spark Operator</b><br/>Manages jobs"]
        LOGGING["<b>Logging</b><br/>Elasticsearch + Kibana"]
        MONITORING["<b>Monitoring</b><br/>Prometheus + Grafana"]
        HISTORY["<b>History Server</b><br/>Spark UI"]
    end
    
    subgraph TEAMS["<b>Team Namespaces</b>"]
        TEAM_A["<b>team-a-spark</b><br/>Quota: 10 CPU, 40Gi"]
        TEAM_B["<b>team-b-spark</b><br/>Quota: 20 CPU, 80Gi"]
    end
    
    DEV --> PORTAL
    DEV --> API
    
    PORTAL --> VALIDATE
    API --> VALIDATE
    
    VALIDATE --> OPERATOR
    OPERATOR --> TEAM_A
    OPERATOR --> TEAM_B
    
    TEAM_A -.-> LOGGING
    TEAM_B -.-> LOGGING
    
    TEAM_A -.-> MONITORING
    TEAM_B -.-> MONITORING
    
    TEAM_A -.-> HISTORY
    TEAM_B -.-> HISTORY
    
    style USERS fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#000
    style SUBMISSION fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#000
    style PLATFORM fill:#E3F2FD,stroke:#2196F3,stroke-width:3px,color:#000
    style TEAMS fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px,color:#000
</div>

## Key Takeaways

### What You Learned

✅ **Multi-Tenancy**: Multiple teams share one cluster safely with namespaces and quotas

✅ **No kubectl Access**: Teams submit jobs via web portal or API

✅ **Self-Service Scheduling**: Teams can schedule their own recurring jobs (hourly, daily, weekly, monthly)

✅ **Centralized Logging**: All logs in Elasticsearch, searchable by team

✅ **Cost Tracking**: Prometheus tracks usage, Grafana shows costs per team

✅ **History Server**: Centralized Spark UI for all completed jobs

✅ **Security**: Network policies, RBAC, and audit logging

### Benefits

| Aspect | Benefit |
|--------|---------|
| **Platform Team** | Manage one cluster for all teams, centralized observability |
| **Application Teams** | Self-service job submission AND scheduling, no Kubernetes knowledge needed |
| **Finance** | Accurate cost tracking and chargeback per team |
| **Security** | Strong isolation, audit trails, no direct cluster access |
| **Compliance** | All actions logged, version-controlled job definitions |

## Next Steps

**For Platform Teams:**
1. Set up namespaces and quotas for each team
2. Deploy centralized logging (Fluentd + Elasticsearch + Kibana)
3. Configure Prometheus for cost tracking
4. Build or deploy a job submission portal

**For Application Teams:**
1. Get familiar with the job submission portal
2. Understand your team's resource quota
3. Use the History Server to debug failed jobs
4. Check Kibana for logs instead of `kubectl logs`

## Quick Reference

### Platform Team Checklist

- [ ] Install Spark Operator cluster-wide
- [ ] Create namespace per team with labels
- [ ] Set ResourceQuota per namespace
- [ ] Configure RBAC (service accounts, roles)
- [ ] Deploy Fluentd for log collection
- [ ] Set up Elasticsearch + Kibana
- [ ] Deploy Spark History Server
- [ ] Configure Prometheus cost tracking
- [ ] Build job submission portal
- [ ] Set up network policies

### Team Onboarding Checklist

- [ ] Receive team namespace and quota
- [ ] Get portal/API credentials
- [ ] Understand S3 path restrictions
- [ ] Learn how to submit jobs via portal
- [ ] Access Kibana dashboard for logs
- [ ] Access History Server for job details
- [ ] Review cost dashboard in Grafana

## Summary

**Enterprise Spark on Kubernetes** requires:
- **Isolation**: Namespaces + quotas + network policies
- **Observability**: Centralized logging + monitoring + history
- **Self-Service**: Web portal or API for job submission AND scheduling
- **Scheduling**: Teams can schedule their own recurring jobs (cron-based)
- **Cost Tracking**: Prometheus metrics + Grafana dashboards
- **Security**: RBAC + audit logging + no direct kubectl access

This architecture allows you to run Spark for dozens of teams on a shared cluster while maintaining security, observability, cost control, and giving teams full autonomy to schedule their workloads.

**Ready to get started?** Check out the **[Getting Started Guide](kubeflow-spark-operator-basics.html)** to learn the basics first, then come back here to implement the enterprise features.
