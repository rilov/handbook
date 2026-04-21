---
title: "Kubeflow Spark Operator - Getting Started"
category: Data
order: 15
tags: [spark, kubernetes, kubeflow, data-engineering, containers]
summary: "Learn how to run Apache Spark on Kubernetes using the Spark Operator. This guide covers the basics: what it is, how it works, and how to submit your first Spark job without manual spark-submit commands."
---

# Kubeflow Spark Operator - Getting Started

## What is This?

**Simple Answer:** The Spark Operator lets you run Apache Spark jobs on Kubernetes by writing simple YAML files instead of complex `spark-submit` commands.

**Why Should You Care?**
- ✅ No more manual `spark-submit` commands
- ✅ Jobs defined as code (YAML) - version control friendly
- ✅ Automatic retries and monitoring
- ✅ Native Kubernetes integration
- ✅ Schedule jobs like cron jobs

## The Problem It Solves

### Before Spark Operator (The Hard Way)

```bash
# You had to run complex commands like this:
spark-submit \
  --master k8s://https://kubernetes.default.svc:443 \
  --deploy-mode cluster \
  --name spark-pi \
  --class org.apache.spark.examples.SparkPi \
  --conf spark.executor.instances=5 \
  --conf spark.kubernetes.container.image=spark:3.5.0 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  local:///opt/spark/examples/jars/spark-examples.jar
```

**Problems:**
- Hard to remember all the flags
- No automatic retries if the job fails
- Manual monitoring required
- Difficult to schedule recurring jobs
- Not version controlled

### After Spark Operator (The Easy Way)

```yaml
# Just write a simple YAML file:
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: spark-pi
spec:
  type: Scala
  mode: cluster
  image: spark:3.5.0
  mainClass: org.apache.spark.examples.SparkPi
  mainApplicationFile: local:///opt/spark/examples/jars/spark-examples.jar
  
  driver:
    cores: 1
    memory: 512m
  
  executor:
    cores: 1
    instances: 5
    memory: 1g
```

**Benefits:**
- ✅ Easy to read and understand
- ✅ Can be version controlled in Git
- ✅ Automatic retries built-in
- ✅ Apply with `kubectl apply -f spark-pi.yaml`

## How It Works (Simple Explanation)

Think of the Spark Operator as a **robot assistant** that watches for Spark job requests and handles all the complexity for you.

<div class="mermaid">
graph LR
    YOU["<b>You</b><br/>Write YAML file"] -->|kubectl apply| K8S["<b>Kubernetes</b><br/>Receives request"]
    K8S -->|Notifies| OPERATOR["<b>Spark Operator</b><br/>Robot Assistant"]
    OPERATOR -->|Creates| DRIVER["<b>Driver Pod</b><br/>Job Coordinator"]
    DRIVER -->|Creates| EXEC1["<b>Executor 1</b><br/>Worker"]
    DRIVER -->|Creates| EXEC2["<b>Executor 2</b><br/>Worker"]
    DRIVER -->|Creates| EXEC3["<b>Executor 3</b><br/>Worker"]
    
    EXEC1 -->|Process data| RESULT["<b>Results</b>"]
    EXEC2 -->|Process data| RESULT
    EXEC3 -->|Process data| RESULT
    
    style YOU fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#000
    style K8S fill:#E3F2FD,stroke:#2196F3,stroke-width:2px,color:#000
    style OPERATOR fill:#FFF3E0,stroke:#FF9800,stroke-width:3px,color:#000
    style DRIVER fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px,color:#000
    style EXEC1 fill:#E1F5FE,stroke:#0288D1,stroke-width:2px,color:#000
    style EXEC2 fill:#E1F5FE,stroke:#0288D1,stroke-width:2px,color:#000
    style EXEC3 fill:#E1F5FE,stroke:#0288D1,stroke-width:2px,color:#000
    style RESULT fill:#C8E6C9,stroke:#388E3C,stroke-width:2px,color:#000
</div>

**Step-by-Step:**
1. **You write** a YAML file describing your Spark job
2. **You apply** it to Kubernetes: `kubectl apply -f my-job.yaml`
3. **Spark Operator sees** the new job request
4. **Operator creates** a Driver pod (the coordinator)
5. **Driver creates** Executor pods (the workers)
6. **Executors process** your data in parallel
7. **Results are saved** to your specified location
8. **Pods clean up** automatically when done

## Kubernetes Terms (Simplified)

Before we continue, here are the key Kubernetes concepts you need to know:

| Term | Simple Explanation | Spark Example |
|------|-------------------|---------------|
| **Pod** | A running container (like a Docker container) | Driver pod, Executor pods |
| **Namespace** | A folder to organize resources | `team-a-spark`, `team-b-spark` |
| **Service Account** | An identity/permission for pods | Allows driver to create executors |
| **ConfigMap** | A file with configuration settings | Log4j properties, Spark configs |
| **Secret** | Encrypted configuration (passwords, keys) | AWS credentials, database passwords |
| **CRD** | Custom Resource Definition - extends Kubernetes | `SparkApplication` is a CRD |

## Your First Spark Job

Let's run a simple example that calculates Pi.

### Step 1: Install Spark Operator

```bash
# Add Helm repository
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator

# Install the operator
helm install spark-operator spark-operator/spark-operator \
  --namespace spark-operator \
  --create-namespace
```

### Step 2: Create a Namespace for Your Jobs

```bash
kubectl create namespace spark-jobs
```

### Step 3: Create a Service Account

```yaml
# spark-rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: spark-jobs
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: spark-role
  namespace: spark-jobs
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["create", "get", "list", "watch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: spark-role-binding
  namespace: spark-jobs
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: spark-role
subjects:
- kind: ServiceAccount
  name: spark
  namespace: spark-jobs
```

```bash
kubectl apply -f spark-rbac.yaml
```

### Step 4: Submit Your First Job

```yaml
# spark-pi.yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: spark-pi
  namespace: spark-jobs
spec:
  type: Scala
  mode: cluster
  image: apache/spark:3.5.0
  imagePullPolicy: Always
  mainClass: org.apache.spark.examples.SparkPi
  mainApplicationFile: local:///opt/spark/examples/jars/spark-examples_2.12-3.5.0.jar
  
  sparkVersion: "3.5.0"
  
  restartPolicy:
    type: Never
  
  driver:
    cores: 1
    coreLimit: "1200m"
    memory: "512m"
    labels:
      version: "3.5.0"
    serviceAccount: spark
  
  executor:
    cores: 1
    instances: 2
    memory: "512m"
    labels:
      version: "3.5.0"
```

```bash
# Submit the job
kubectl apply -f spark-pi.yaml

# Watch the job status
kubectl get sparkapplication -n spark-jobs -w

# Check logs
kubectl logs -n spark-jobs spark-pi-driver
```

### Step 5: Check the Results

```bash
# Get job status
kubectl get sparkapplication spark-pi -n spark-jobs

# Output will show:
# NAME       STATUS      ATTEMPTS   START                  FINISH                 AGE
# spark-pi   COMPLETED   1          2026-04-20T21:00:00Z   2026-04-20T21:01:30Z   2m
```

**Success!** 🎉 You just ran your first Spark job on Kubernetes!

## Common Use Cases

### 1. Running a Python PySpark Job

```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: pyspark-job
  namespace: spark-jobs
spec:
  type: Python
  mode: cluster
  image: apache/spark-py:3.5.0
  mainApplicationFile: s3a://my-bucket/jobs/process_data.py
  
  sparkConf:
    "spark.hadoop.fs.s3a.access.key": "YOUR_ACCESS_KEY"
    "spark.hadoop.fs.s3a.secret.key": "YOUR_SECRET_KEY"
  
  driver:
    cores: 1
    memory: "1g"
    serviceAccount: spark
  
  executor:
    cores: 2
    instances: 5
    memory: "2g"
```

### 2. Scheduled Job (Runs Daily at 2 AM)

```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: ScheduledSparkApplication
metadata:
  name: daily-etl
  namespace: spark-jobs
spec:
  schedule: "0 2 * * *"  # Cron format
  concurrencyPolicy: Forbid  # Don't run if previous job still running
  
  template:
    type: Scala
    mode: cluster
    image: my-registry/spark-etl:latest
    mainClass: com.company.ETLPipeline
    mainApplicationFile: s3a://my-bucket/etl-pipeline.jar
    
    driver:
      cores: 2
      memory: "2g"
      serviceAccount: spark
    
    executor:
      cores: 4
      instances: 10
      memory: "4g"
```

### 3. Job with Automatic Retries

```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: resilient-job
  namespace: spark-jobs
spec:
  type: Scala
  mode: cluster
  image: apache/spark:3.5.0
  mainClass: com.company.MyApp
  mainApplicationFile: s3a://my-bucket/my-app.jar
  
  # Retry configuration
  restartPolicy:
    type: OnFailure
    onFailureRetries: 3
    onFailureRetryInterval: 10  # Wait 10 seconds between retries
  
  driver:
    cores: 1
    memory: "1g"
    serviceAccount: spark
  
  executor:
    cores: 2
    instances: 5
    memory: "2g"
```

## Job Lifecycle

Understanding what happens to your job:

<div class="mermaid">
stateDiagram-v2
    [*] --> NEW: kubectl apply
    NEW --> SUBMITTED: Operator picks up job
    SUBMITTED --> RUNNING: Driver pod starts
    
    RUNNING --> COMPLETED: Job succeeds
    RUNNING --> FAILED: Job fails
    
    FAILED --> RUNNING: Retry (if configured)
    FAILED --> [*]: Max retries reached
    
    COMPLETED --> [*]: Job done
    
    note right of NEW
        Job is queued
    end note
    
    note right of RUNNING
        Driver + Executors
        processing data
    end note
    
    note right of COMPLETED
        Success!
    end note
</div>

**States Explained:**
- **NEW**: Job YAML applied, waiting to start
- **SUBMITTED**: Operator sent job to Kubernetes
- **RUNNING**: Driver and executors are processing data
- **COMPLETED**: Job finished successfully ✅
- **FAILED**: Job encountered an error ❌

## Monitoring Your Jobs

### Check Job Status

```bash
# List all jobs
kubectl get sparkapplication -n spark-jobs

# Get detailed status
kubectl describe sparkapplication spark-pi -n spark-jobs

# Watch for changes
kubectl get sparkapplication -n spark-jobs -w
```

### View Logs

```bash
# Driver logs
kubectl logs -n spark-jobs spark-pi-driver

# Executor logs
kubectl logs -n spark-jobs spark-pi-exec-1

# Follow logs in real-time
kubectl logs -f -n spark-jobs spark-pi-driver
```

### Access Spark UI

```bash
# Port-forward to access Spark UI
kubectl port-forward -n spark-jobs spark-pi-driver 4040:4040

# Open in browser: http://localhost:4040
```

## Common Configuration Options

### Resource Allocation

```yaml
driver:
  cores: 1              # Number of CPU cores
  coreLimit: "1200m"    # Max CPU (prevents throttling)
  memory: "1g"          # Memory allocation
  memoryOverhead: "400m"  # Extra memory for off-heap usage

executor:
  cores: 2
  coreLimit: "2400m"
  memory: "2g"
  memoryOverhead: "512m"
  instances: 5          # Number of executor pods
```

### Environment Variables

```yaml
driver:
  env:
  - name: AWS_REGION
    value: "us-east-1"
  - name: LOG_LEVEL
    value: "INFO"

executor:
  env:
  - name: AWS_REGION
    value: "us-east-1"
```

### Using Secrets

```yaml
# First, create a secret
# kubectl create secret generic aws-creds \
#   --from-literal=access-key=YOUR_KEY \
#   --from-literal=secret-key=YOUR_SECRET \
#   -n spark-jobs

driver:
  envFrom:
  - secretRef:
      name: aws-creds

executor:
  envFrom:
  - secretRef:
      name: aws-creds
```

### Mounting ConfigMaps

```yaml
driver:
  configMaps:
  - name: spark-config
    path: /opt/spark/conf

executor:
  configMaps:
  - name: spark-config
    path: /opt/spark/conf
```

## Troubleshooting

### Job Stuck in SUBMITTED State

**Problem:** Job never starts running.

**Check:**
```bash
# Check if driver pod was created
kubectl get pods -n spark-jobs

# Check operator logs
kubectl logs -n spark-operator deployment/spark-operator
```

**Common Causes:**
- Service account doesn't have permissions
- Image pull errors
- Resource quota exceeded

### Job Fails Immediately

**Problem:** Job goes to FAILED state right away.

**Check:**
```bash
# Check driver pod events
kubectl describe pod spark-pi-driver -n spark-jobs

# Check driver logs
kubectl logs spark-pi-driver -n spark-jobs
```

**Common Causes:**
- Wrong main class name
- JAR file not found
- Missing dependencies

### Executors Not Starting

**Problem:** Driver starts but executors don't.

**Check:**
```bash
# Check if executor pods exist
kubectl get pods -n spark-jobs -l spark-role=executor

# Check driver logs for errors
kubectl logs spark-pi-driver -n spark-jobs | grep -i executor
```

**Common Causes:**
- Service account can't create pods
- Resource quota exceeded
- Node selector/affinity issues

## Best Practices

### 1. Always Set Resource Limits

```yaml
driver:
  cores: 1
  coreLimit: "1200m"  # Prevents CPU throttling
  memory: "1g"
  memoryOverhead: "400m"  # Prevents OOM errors
```

### 2. Use Specific Image Tags

```yaml
# ❌ Bad - uses latest
image: apache/spark:latest

# ✅ Good - specific version
image: apache/spark:3.5.0
```

### 3. Configure Retries for Production

```yaml
restartPolicy:
  type: OnFailure
  onFailureRetries: 3
  onFailureRetryInterval: 10
```

### 4. Add Labels for Organization

```yaml
metadata:
  labels:
    team: data-engineering
    env: production
    app: etl-pipeline
```

### 5. Use Namespaces for Isolation

```bash
# Separate namespaces for different environments
kubectl create namespace spark-dev
kubectl create namespace spark-staging
kubectl create namespace spark-prod
```

## Next Steps

Now that you understand the basics, you can explore:

- **[Multi-Tenant Architecture](kubeflow-spark-operator-enterprise.html)** - Learn how to run Spark for multiple teams with centralized logging, cost tracking, and job submission portals
- **Spark History Server** - Set up persistent UI for completed jobs
- **Advanced Scheduling** - Complex cron patterns and dependencies
- **Performance Tuning** - Optimize resource allocation and parallelism

## Quick Reference

### Common Commands

```bash
# Submit a job
kubectl apply -f my-job.yaml

# List jobs
kubectl get sparkapplication -n spark-jobs

# Get job status
kubectl get sparkapplication my-job -n spark-jobs

# Delete a job
kubectl delete sparkapplication my-job -n spark-jobs

# View driver logs
kubectl logs my-job-driver -n spark-jobs

# Access Spark UI
kubectl port-forward my-job-driver 4040:4040 -n spark-jobs
```

### Job Template

```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: my-job
  namespace: spark-jobs
spec:
  type: Scala  # or Python
  mode: cluster
  image: apache/spark:3.5.0
  mainClass: com.company.MyApp
  mainApplicationFile: s3a://bucket/my-app.jar
  
  driver:
    cores: 1
    memory: "1g"
    serviceAccount: spark
  
  executor:
    cores: 2
    instances: 5
    memory: "2g"
  
  restartPolicy:
    type: OnFailure
    onFailureRetries: 3
```

## Summary

**What You Learned:**
- ✅ Spark Operator replaces manual `spark-submit` commands with simple YAML
- ✅ Jobs are defined as Kubernetes resources
- ✅ Automatic retries and monitoring built-in
- ✅ Easy to schedule recurring jobs
- ✅ Version control friendly

**Key Takeaway:** The Spark Operator makes running Spark on Kubernetes as easy as writing a YAML file and running `kubectl apply`. No more complex commands or manual monitoring!

Ready for enterprise features? Check out the **[Multi-Tenant Architecture Guide](kubeflow-spark-operator-enterprise.html)** to learn about centralized logging, cost tracking, and self-service job submission portals.
