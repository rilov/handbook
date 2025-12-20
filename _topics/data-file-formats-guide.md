---
title: Data File Formats — The Complete Guide
category: Data
tags:
  - file-formats
  - data-engineering
  - csv
  - json
  - parquet
summary: A beginner-friendly guide to every data file format from CSV to Delta Lake with simple explanations and visual examples.
---

## Understanding File Formats

Think of file formats as different languages for storing data. Just like you might write a grocery list (simple) or a legal document (structured), different formats serve different purposes.

<div class="mermaid">
flowchart TD
    FILES["📁 Data File Formats"]
    
    FILES --> TEXT["📝 Text-Based<br/>Human-readable"]
    FILES --> BINARY["⚙️ Binary<br/>Machine-optimized"]
    FILES --> COMPRESSED["📦 Compressed<br/>Space-saving"]
    FILES --> TABLE["🗄️ Table Formats<br/>ACID transactions"]
    
    TEXT --> CSV["CSV, TSV, TXT<br/>JSON, XML, YAML"]
    BINARY --> BIG["Parquet, ORC, Avro<br/>XLS, XLSX"]
    COMPRESSED --> COMP["GZIP, ZIP, BZIP2"]
    TABLE --> LAKE["Delta Lake<br/>Iceberg, Hudi"]
    
    style FILES fill:#dbeafe,stroke:#2563eb
    style TEXT fill:#d1fae5,stroke:#059669
    style BINARY fill:#fef3c7,stroke:#d97706
    style COMPRESSED fill:#fce7f3,stroke:#db2777
    style TABLE fill:#e0e7ff,stroke:#6366f1
</div>

> **🎓 Want to go deeper?** This guide covers the essentials. For in-depth technical details, check out our deep dive articles on [Parquet](/handbook/topics/parquet-deep-dive/), [ORC](/handbook/topics/orc-deep-dive/), [Avro](/handbook/topics/avro-deep-dive/), and [Delta Lake](/handbook/topics/delta-lake-deep-dive/).

---

## Text-Based Formats (Human-Readable)

### CSV (Comma-Separated Values)

**What it looks like:**
```csv
name,age,city
John,25,New York
Jane,30,Los Angeles
Bob,28,Chicago
```

<div class="mermaid">
flowchart LR
    subgraph csv["CSV File Structure"]
        H["name,age,city<br/>(header)"]
        R1["John,25,New York"]
        R2["Jane,30,Los Angeles"]
        R3["Bob,28,Chicago"]
    end
    
    style H fill:#dbeafe,stroke:#2563eb
    style R1 fill:#d1fae5,stroke:#059669
    style R2 fill:#d1fae5,stroke:#059669
    style R3 fill:#d1fae5,stroke:#059669
</div>

| Feature | Details |
|---------|---------|
| **Pros** | Simple, universal, opens in Excel |
| **Cons** | No data types, struggles with commas in data |
| **Best For** | Small datasets, sharing data |
| **File Size** | Medium |

**When to use CSV:**
```
✅ Export data from a database for a colleague
✅ Share data with non-technical users (opens in Excel)
✅ Small datasets (< 100 MB)
✅ Simple reporting or one-time analysis
✅ Testing/prototyping data pipelines

❌ Large-scale analytics (use Parquet instead)
❌ Complex nested data (use JSON instead)
❌ When data contains lots of commas (use TSV)
```

**Real-world example:**
```
Use case: Monthly sales report for business team
- Export 50,000 sales records to CSV
- Email to business analysts
- They open in Excel, make pivot tables
- Perfect! CSV is simple and works everywhere
```

---

### TSV (Tab-Separated Values)

**What it looks like:**
```tsv
name	age	city
John	25	New York
Jane	30	Los Angeles
```

**Key Difference from CSV:** Uses tabs (`\t`) instead of commas, so commas in data don't break things.

| Use TSV When... | Example |
|-----------------|---------|
| Data contains commas | Addresses: "123 Main St, Apt 4" |
| Exporting from databases | More reliable than CSV |

**When to use TSV:**
```
✅ Data with addresses ("123 Main St, Apt 5, NYC")
✅ Text that naturally contains commas
✅ Database exports (PostgreSQL COPY)
✅ When CSV parsing keeps breaking

❌ Sharing with Excel users (CSV is more common)
❌ When data contains both commas AND tabs
```

**Real-world example:**
```
Use case: Exporting customer addresses
Customers: 10,000 records with addresses

CSV problem: "John Smith, 123 Main St, Apt 5"
Result: Parser thinks these are 3 columns!

TSV solution: John Smith[TAB]123 Main St, Apt 5
Result: Works perfectly! ✅
```

---

### TXT (Plain Text)

**What it looks like:**
```txt
This is just plain text.
No structure, no rules.
Whatever you want to write.
```

**Real-World Analogy:** Like a notebook — write anything, but no organization.

| Feature | Details |
|---------|---------|
| **Pros** | Simplest possible, works anywhere |
| **Cons** | No structure, hard to parse |
| **Best For** | Logs, notes, unstructured data |

**When to use TXT:**
```
✅ Application logs
✅ Error messages
✅ Documentation/notes
✅ Simple data dumps
✅ Human-readable output

❌ Structured data (use CSV/JSON)
❌ Machine parsing (too unstructured)
❌ Large-scale processing
```

**Real-world example:**
```
Use case: Application error logs
2025-01-15 10:30:00 ERROR: Database connection timeout
2025-01-15 10:30:05 ERROR: Retry attempt 1 failed
2025-01-15 10:30:10 INFO: Connection restored

Perfect for debugging, grep searching, human reading
```

---

### JSON (JavaScript Object Notation)

**What it looks like:**
```json
{
  "name": "John",
  "age": 25,
  "city": "New York",
  "hobbies": ["reading", "coding"],
  "address": {
    "street": "123 Main St",
    "zip": "10001"
  }
}
```

<div class="mermaid">
flowchart TD
    subgraph json["JSON Structure"]
        ROOT["{ }"]
        NAME["name: 'John'"]
        AGE["age: 25"]
        HOBBIES["hobbies: [ ]"]
        H1["reading"]
        H2["coding"]
        ADDRESS["address: { }"]
        STREET["street: '123 Main St'"]
        
        ROOT --> NAME
        ROOT --> AGE
        ROOT --> HOBBIES
        HOBBIES --> H1
        HOBBIES --> H2
        ROOT --> ADDRESS
        ADDRESS --> STREET
    end
    
    style ROOT fill:#dbeafe,stroke:#2563eb
    style HOBBIES fill:#fef3c7,stroke:#d97706
    style ADDRESS fill:#d1fae5,stroke:#059669
</div>

| Feature | Details |
|---------|---------|
| **Pros** | Flexible, supports nesting, widely used |
| **Cons** | Verbose (lots of brackets), larger files |
| **Best For** | APIs, config files, web applications |
| **File Size** | Large (human-readable) |

**When to use JSON:**
```
✅ REST API responses
✅ Configuration files (settings.json)
✅ NoSQL databases (MongoDB)
✅ Nested/hierarchical data
✅ JavaScript/web applications
✅ When data has varying structure

❌ Large datasets (use Parquet)
❌ High-performance analytics
❌ When file size matters (too verbose)
```

**Real-world examples:**
```
Example 1: API response
GET /api/users/123
{
  "id": 123,
  "name": "John",
  "orders": [
    {"id": 1, "total": 99.99},
    {"id": 2, "total": 149.99}
  ]
}

Example 2: Application config
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "credentials": {...}
  },
  "features": {
    "darkMode": true,
    "notifications": false
  }
}

Perfect for nested, hierarchical data!
```

---

### XML (eXtensible Markup Language)

**What it looks like:**
```xml
<person>
  <name>John</name>
  <age>25</age>
  <city>New York</city>
  <hobbies>
    <hobby>reading</hobby>
    <hobby>coding</hobby>
  </hobbies>
</person>
```

**Real-World Analogy:** Like HTML but for data. Very structured, lots of tags.

| Feature | Details |
|---------|---------|
| **Pros** | Strict validation, supports attributes |
| **Cons** | VERY verbose, hard to read |
| **Best For** | Enterprise systems, SOAP APIs, legacy systems |
| **Modern Usage** | Being replaced by JSON |

**When to use XML:**
```
✅ Legacy enterprise systems (you have no choice!)
✅ SOAP APIs (older web services)
✅ When you need strict schema validation (XSD)
✅ Microsoft Office formats (docx, xlsx are XML!)
✅ RSS feeds, sitemaps

❌ New projects (use JSON)
❌ Performance-critical systems (too verbose)
❌ Human readability (JSON is cleaner)
```

**Real-world example:**
```
Use case: Enterprise SOAP API integration
Your company's 20-year-old ERP system only speaks XML

Request:
<soap:Envelope>
  <soap:Body>
    <GetCustomer>
      <CustomerId>12345</CustomerId>
    </GetCustomer>
  </soap:Body>
</soap:Envelope>

You don't choose XML - XML chooses you! 😅
```

---

### YAML (YAML Ain't Markup Language)

**What it looks like:**
```yaml
name: John
age: 25
city: New York
hobbies:
  - reading
  - coding
address:
  street: 123 Main St
  zip: 10001
```

**Key Feature:** Uses indentation (like Python) instead of brackets.

| Feature | Details |
|---------|---------|
| **Pros** | Very readable, clean, supports comments |
| **Cons** | Whitespace-sensitive (can be fragile) |
| **Best For** | Config files (Kubernetes, Docker Compose) |

**When to use YAML:**
```
✅ Kubernetes manifests
✅ Docker Compose files
✅ CI/CD pipelines (GitHub Actions, GitLab CI)
✅ Configuration files (human-edited frequently)
✅ When you need comments in config

❌ APIs (use JSON)
❌ Large data files (use Parquet)
❌ When precision matters (whitespace errors!)
```

**Real-world examples:**
```
Example 1: Docker Compose
version: '3'
services:
  web:
    image: nginx
    ports:
      - "80:80"
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: secret

Example 2: GitHub Actions
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm test

Clean, readable, perfect for DevOps!
```

<div class="mermaid">
flowchart LR
    subgraph compare["JSON vs YAML vs XML"]
        JSON_["JSON<br/>{ 'name': 'John' }"]
        YAML_["YAML<br/>name: John"]
        XML_["XML<br/>&lt;name&gt;John&lt;/name&gt;"]
    end
    
    JSON_ --> |"Most common"| API["APIs"]
    YAML_ --> |"Most readable"| CONFIG["Config Files"]
    XML_ --> |"Most verbose"| LEGACY["Legacy Systems"]
    
    style JSON_ fill:#dbeafe,stroke:#2563eb
    style YAML_ fill:#d1fae5,stroke:#059669
    style XML_ fill:#fecaca,stroke:#dc2626
</div>

---

## Spreadsheet Formats

### XLS (Excel Binary Format - Old)

**What it is:** Microsoft Excel's old binary format (pre-2007).

| Feature | Details |
|---------|---------|
| **Max Rows** | 65,536 (very limited!) |
| **Max Columns** | 256 |
| **Status** | ⚠️ Deprecated — don't use for new projects |
| **Opens In** | Excel, LibreOffice |

**When to use XLS:**
```
❌ Never for new projects!
✅ Only if forced to support old Excel (pre-2007)
✅ Legacy systems that can't be upgraded

Real talk: If someone asks for XLS, give them XLSX instead
```

---

### XLSX (Excel Open XML Format - Modern)

**What it is:** Modern Excel format, actually a ZIP file containing XML files!

<div class="mermaid">
flowchart LR
    XLSX["my-file.xlsx"] --> ZIP["(Actually a ZIP)"]
    ZIP --> XML1["worksheets/sheet1.xml"]
    ZIP --> XML2["styles.xml"]
    ZIP --> XML3["workbook.xml"]
    
    style XLSX fill:#d1fae5,stroke:#059669
    style ZIP fill:#fef3c7,stroke:#d97706
</div>

| Feature | Details |
|---------|---------|
| **Max Rows** | 1,048,576 |
| **Max Columns** | 16,384 |
| **Pros** | Formulas, formatting, multiple sheets |
| **Cons** | Bloated for large data, proprietary |
| **Best For** | Business reports, sharing with non-technical users |

**When to use XLSX:**
```
✅ Sharing data with business users (Excel is universal)
✅ Reports with formatting, charts, formulas
✅ Multiple sheets in one file
✅ < 100K rows (stays performant)
✅ Monthly/quarterly business reports

❌ Large datasets (>1M rows hits Excel limits)
❌ Data pipeline intermediate storage (use Parquet)
❌ Production systems (too slow)
❌ Version control (binary, can't diff)
```

**Real-world examples:**
```
Example 1: Monthly executive dashboard
- Sheet 1: Revenue by region (with chart)
- Sheet 2: Top 10 customers (formatted table)
- Sheet 3: YoY comparison (with formulas)
Send to CEO - they open in Excel, perfect! ✅

Example 2: Ad-hoc analysis for business analyst
- Export 50K customer records
- Business analyst adds pivot tables
- Shares with their manager
- Everyone has Excel, everyone's happy!

Example 3: When NOT to use XLSX
- 5 million log records ❌
- Real-time data pipeline ❌
- Use Parquet instead!
```

**Fun Fact:** Rename `.xlsx` to `.zip` and unzip it — you'll see the XML files inside!

---

## Big Data Formats (Binary, Optimized)

### Parquet

**What it is:** Columnar storage format optimized for analytics.

<div class="mermaid">
flowchart LR
    subgraph csv_storage["Row-Based (CSV)"]
        R1["Row 1: John,25,NYC"]
        R2["Row 2: Jane,30,LA"]
        R3["Row 3: Bob,28,CHI"]
    end
    
    subgraph parquet_storage["Column-Based (Parquet)"]
        C1["Name: John,Jane,Bob"]
        C2["Age: 25,30,28"]
        C3["City: NYC,LA,CHI"]
    end
    
    csv_storage --> |"Slow for analytics"| SLOW["😰"]
    parquet_storage --> |"Fast for analytics"| FAST["🚀"]
    
    style csv_storage fill:#fecaca,stroke:#dc2626
    style parquet_storage fill:#d1fae5,stroke:#059669
</div>

| Feature | Details |
|---------|---------|
| **Storage** | Columnar (like columnar databases) |
| **Compression** | Excellent (10x smaller than CSV) |
| **Speed** | Very fast for reads |
| **Best For** | Data warehouses, analytics, Spark/Hadoop |
| **Tools** | Spark, Pandas, DuckDB, Snowflake |

**When to use Parquet:**
```
✅ Large datasets (> 100 MB)
✅ Analytics queries (SELECT specific columns)
✅ Data warehouses / data lakes
✅ Apache Spark / Hadoop processing
✅ When you need compression (10x smaller than CSV!)
✅ Cloud storage (S3, GCS) - saves $$

❌ Streaming data (use Avro)
❌ Transactional updates (use Delta Lake)
❌ Need Excel compatibility (use CSV/XLSX)
❌ Very small files (< 1 MB, overhead not worth it)
```

**Real-world examples:**
```
Example 1: Data warehouse storage
Situation: 1 billion e-commerce orders
- CSV size: 500 GB
- Parquet size: 50 GB (10x smaller!)
- Query time: 100x faster for analytics
- Cloud storage cost: 10x cheaper
Perfect choice! ✅

Example 2: Spark analytics pipeline
Raw data (CSV) → Transform in Spark → Save as Parquet
- Read 100 GB CSV: 10 minutes
- Save as Parquet: 10 GB
- Future queries: 10 seconds (100x faster!)

Example 3: AWS Athena / Google BigQuery
Upload Parquet to S3 → Query with SQL
- 1 TB CSV: $5 per query scan
- 100 GB Parquet: $0.50 per query scan
10x cost savings!
```

**Real-World Analogy:** Instead of reading entire books to find all mentions of "data," you have an index that lists every page with "data."

📖 **[Deep dive into Parquet →](/handbook/topics/parquet-deep-dive/)** Learn how Parquet actually stores data, encoding schemes, and performance optimization.

---

### ORC (Optimized Row Columnar)

**What it is:** Like Parquet, but optimized for Hive/Hadoop.

<div class="mermaid">
flowchart TD
    ORC["ORC File"]
    
    ORC --> STRIPE1["Stripe 1<br/>(10K rows)"]
    ORC --> STRIPE2["Stripe 2<br/>(10K rows)"]
    
    STRIPE1 --> INDEX["Index"]
    STRIPE1 --> DATA["Compressed<br/>Column Data"]
    STRIPE1 --> FOOTER["Footer<br/>(metadata)"]
    
    style ORC fill:#dbeafe,stroke:#2563eb
    style STRIPE1 fill:#d1fae5,stroke:#059669
    style DATA fill:#fef3c7,stroke:#d97706
</div>

| Feature | Parquet | ORC |
|---------|---------|-----|
| **Ecosystem** | Spark, Python | Hive, Hadoop |
| **Compression** | Excellent | Slightly better |
| **Speed** | Very fast | Slightly faster |
| **Use In** | Most cases | Hadoop-heavy environments |

**When to use ORC:**
```
✅ Using Apache Hive extensively
✅ Heavy Hadoop ecosystem (not Spark)
✅ Need best possible compression
✅ ACID transactions in Hive

❌ Using Spark (Parquet is better integrated)
❌ Using Python/Pandas (Parquet has better support)
❌ Cloud-native (Parquet is more common)
```

**Real-world examples:**
```
Example 1: Legacy Hadoop cluster
Company has:
- 1000-node Hadoop cluster
- All data in Hive
- Hive queries for everything
Use ORC! Perfect fit ✅

Example 2: Modern cloud stack
Company has:
- AWS S3 data lake
- Spark for processing
- Python for data science
Use Parquet! Better ecosystem ✅

Rule of thumb:
Hive/Hadoop → ORC
Everything else → Parquet
```

**Which to choose?** Use Parquet unless you're deep in the Hadoop ecosystem.

📖 **[Deep dive into ORC →](/handbook/topics/orc-deep-dive/)** Explore ORC's three-level indexing, Bloom filters, and when it beats Parquet.

---

### Avro

**What it is:** Row-based format with embedded schema. Great for streaming.

**Example Schema:**
```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "age", "type": "int"}
  ]
}
```

<div class="mermaid">
flowchart LR
    subgraph avro["Avro File"]
        SCHEMA["Schema<br/>(JSON)"]
        DATA["Binary Data"]
    end
    
    SCHEMA --> |"Self-describing"| READ["Can always<br/>read the file"]
    
    style SCHEMA fill:#dbeafe,stroke:#2563eb
    style DATA fill:#d1fae5,stroke:#059669
    style READ fill:#fef3c7,stroke:#d97706
</div>

| Feature | Details |
|---------|---------|
| **Storage** | Row-based (not columnar) |
| **Schema** | Embedded in file |
| **Best For** | Kafka, streaming, evolving schemas |
| **Speed** | Fast writes, slower reads than Parquet |

**When to use Avro:**
```
✅ Apache Kafka streaming (most common use!)
✅ Schema evolution (adding fields without breaking)
✅ High-throughput writes
✅ When schema changes frequently
✅ Event streaming / message queues

❌ Analytics queries (use Parquet)
❌ Data warehouse storage (use Parquet)
❌ When schema never changes
```

**Real-world examples:**
```
Example 1: Kafka event streaming (MOST COMMON)
Producer: Website clicks → Kafka (Avro format)
Consumer: Read from Kafka → Process events

Why Avro?
- Fast writes (1M events/sec)
- Schema embedded (self-documenting)
- Compact binary format
- Schema Registry handles evolution

Example 2: Schema evolution
Week 1: User event { user_id, action }
Week 5: Add field { user_id, action, timestamp }
Week 10: Add field { user_id, action, timestamp, device }

Old consumers still work! Avro handles it ✅

Example 3: When NOT to use Avro
Storing 1 TB of sales data for analytics ❌
- Avro is row-based (slow for analytics)
- Use Parquet instead (100x faster queries)

Rule of thumb:
Streaming/Kafka → Avro
Analytics/Storage → Parquet
```

📖 **[Deep dive into Avro →](/handbook/topics/avro-deep-dive/)** Understand schema evolution, Schema Registry, and why Kafka uses Avro.

---

## Database & Serialization Formats

### SQL (Structured Query Language)

**What it is:** A text file with database commands, not a data format itself.

**Example:**
```sql
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  age INT
);

INSERT INTO users VALUES (1, 'John', 25);
INSERT INTO users VALUES (2, 'Jane', 30);
```

| Feature | Details |
|---------|---------|
| **Use Case** | Database exports, backups, migrations |
| **Pros** | Portable, human-readable |
| **Cons** | Slow for large datasets |
| **Best For** | Sharing database structures, small exports |

**When to use SQL dumps:**
```
✅ Database migration (MySQL → PostgreSQL)
✅ Sharing database schema with team
✅ Version controlling database structure
✅ Small database backups (< 100 MB)
✅ Seeding test databases

❌ Large production backups (too slow)
❌ Big data transfers (use binary dumps)
❌ Analytics (export to Parquet)
```

**Real-world examples:**
```
Example 1: Share database schema with new developer
$ pg_dump --schema-only my_db > schema.sql
Send schema.sql to developer
They run: psql < schema.sql
Perfect! They have exact same structure ✅

Example 2: Version control migrations
git repository:
migrations/
  001_create_users.sql
  002_add_email_column.sql
  003_create_orders.sql
Team always knows database history!

Example 3: When NOT to use SQL
Backing up 500 GB production database ❌
- SQL dump takes 10 hours
- Use pg_dump -Fc (binary) instead: 30 minutes
```

---

### Pickle (Python Serialization)

**What it is:** Python's native format for saving Python objects.

**Example:**
```python
import pickle

data = {'name': 'John', 'age': 25, 'hobbies': ['coding']}

# Save
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)

# Load
with open('data.pkl', 'rb') as f:
    loaded = pickle.load(f)
```

<div class="mermaid">
flowchart LR
    PY["Python Object"] --> |"pickle.dump()"| PKL["data.pkl"]
    PKL --> |"pickle.load()"| PY2["Python Object"]
    
    style PY fill:#dbeafe,stroke:#2563eb
    style PKL fill:#fef3c7,stroke:#d97706
    style PY2 fill:#d1fae5,stroke:#059669
</div>

| Feature | Details |
|---------|---------|
| **Pros** | Saves Python objects exactly (lists, dicts, classes) |
| **Cons** | ⚠️ Python-only, security risk (code execution) |
| **Best For** | ML models, temporary Python data |
| **⚠️ Warning** | Never load untrusted pickle files! |

**When to use Pickle:**
```
✅ Temporary ML model storage (prototyping)
✅ Caching Python objects during development
✅ Saving complex Python data structures
✅ Quick experiments / notebooks

❌ Production ML models (use ONNX, SavedModel)
❌ Sharing between languages
❌ Long-term storage (pickle breaks across Python versions!)
❌ Untrusted data (SECURITY RISK! Can execute code)
```

**Real-world examples:**
```
Example 1: ML model prototyping (OK for dev)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)
pickle.dump(model, open('model.pkl', 'wb'))

Dev environment: ✅ Fast and easy
Production: ❌ Use proper model serving

Example 2: Caching expensive computations
expensive_result = run_10_hour_computation()
pickle.dump(expensive_result, 'cache.pkl')
# Next time: just load in 1 second!

Example 3: THE DANGER ⚠️
# Someone sends you data.pkl
import pickle
data = pickle.load(open('data.pkl', 'rb'))  # ☠️ DANGER!
# This can execute arbitrary code! Could delete your files!

NEVER load pickle from untrusted sources!

Example 4: Version incompatibility
# Python 3.8: save model
pickle.dump(model, 'model.pkl')

# Python 3.11: load model
model = pickle.load('model.pkl')  # ERROR: incompatible!

Use JSON/ONNX for long-term storage
```

---

## Compressed Formats

### GZIP (.gz)

**What it is:** Compression algorithm that makes files smaller.

<div class="mermaid">
flowchart LR
    ORIG["data.csv<br/>100 MB"] --> |"gzip"| COMP["data.csv.gz<br/>10 MB"]
    COMP --> |"gunzip"| ORIG2["data.csv<br/>100 MB"]
    
    style ORIG fill:#fecaca,stroke:#dc2626
    style COMP fill:#d1fae5,stroke:#059669
    style ORIG2 fill:#dbeafe,stroke:#2563eb
</div>

| Feature | Details |
|---------|---------|
| **Compression Ratio** | ~10x smaller |
| **Speed** | Fast |
| **Best For** | Single files, log files, streaming |
| **Common Use** | `data.csv.gz`, `logs.txt.gz` |

**When to use GZIP:**
```
✅ Compress any file before storing/sending
✅ Log files (they compress amazingly well!)
✅ CSV files for storage
✅ Transferring data over network
✅ Cloud storage (S3, GCS) - save costs

❌ Already compressed files (JPEG, PNG, video)
❌ When you need to read data without decompressing
```

**Real-world examples:**
```
Example 1: Saving storage costs on S3
data.csv: 1 GB
data.csv.gz: 100 MB (10x smaller!)
S3 cost: $0.023/GB/month
- CSV: $0.023/month
- GZ: $0.0023/month
10x savings! ✅

Example 2: Log file compression
application.log: 10 GB/day
application.log.gz: 500 MB/day (20x smaller!)
Store 30 days of logs:
- Uncompressed: 300 GB
- Compressed: 15 GB
Massive savings!

Example 3: Pandas can read GZ directly!
import pandas as pd
df = pd.read_csv('data.csv.gz')  # Automatic decompression!
No need to decompress first ✅

Rule: Always gzip CSVs before storing
```

**Example:**
```bash
# Compress
gzip data.csv  # Creates data.csv.gz

# Decompress
gunzip data.csv.gz  # Restores data.csv
```

---

### ZIP

**What it is:** Archive format that compresses multiple files.

<div class="mermaid">
flowchart TD
    subgraph before["Before Zipping"]
        F1["report.pdf"]
        F2["data.csv"]
        F3["image.png"]
    end
    
    subgraph after["After Zipping"]
        ZIP["archive.zip<br/>(all files compressed)"]
    end
    
    F1 --> ZIP
    F2 --> ZIP
    F3 --> ZIP
    
    style before fill:#fecaca,stroke:#dc2626
    style after fill:#d1fae5,stroke:#059669
</div>

| Feature | Details |
|---------|---------|
| **Compression** | Good |
| **Multiple Files** | ✅ Yes (like a folder) |
| **Best For** | Sharing multiple files, downloads |
| **Opens In** | Every OS built-in |

**When to use ZIP:**
```
✅ Distributing software / code
✅ Sharing multiple files with users
✅ Email attachments (multiple files)
✅ Archiving project backups
✅ Website downloads

❌ Single large file (use gzip instead)
❌ Production data pipelines (Parquet has better compression)
```

**Real-world examples:**
```
Example 1: Sending project files to client
project/
  code/
  docs/
  images/
  
$ zip -r project.zip project/
Email project.zip to client
Client unzips - gets exact folder structure ✅

Example 2: Monthly report package
monthly_report.zip containing:
  - sales_report.xlsx
  - customer_data.csv
  - charts/graph1.png
  - charts/graph2.png
  - readme.txt

Perfect for business users!

Example 3: Code repository downloads
GitHub → Download as ZIP
Get entire repository in one file
```

---

### BZIP2 (.bz2)

**What it is:** Slower compression, but better compression ratio than GZIP.

| Format | Compression | Speed | Use When |
|--------|-------------|-------|----------|
| **GZIP** | Good | Fast | Default choice |
| **BZIP2** | Better | Slower | Archiving, storage |
| **ZIP** | Good | Fast | Multiple files |

**When to use BZIP2:**
```
✅ Long-term archival (best compression)
✅ When storage space is expensive
✅ When compression time doesn't matter
✅ Maximum compression needed

❌ Real-time processing (too slow)
❌ Frequently accessed files
❌ Most normal use cases (use gzip instead)
```

**Real-world example:**
```
Compressing 1 GB log file:

GZIP:
- Result: 100 MB
- Time: 10 seconds
- Use for: Active logs ✅

BZIP2:
- Result: 80 MB (20% smaller!)
- Time: 60 seconds (6x slower)
- Use for: Archive old logs ✅

Rule of thumb:
- Active files → GZIP (fast)
- Archive/storage → BZIP2 (smaller)
```

**Real-World Analogy:**
- GZIP = Quick packing for a trip
- BZIP2 = Carefully vacuum-packing for long-term storage

---

## Table Formats (ACID on Data Lakes)

These formats add **database features** (transactions, versioning, updates) to data lakes.

<div class="mermaid">
flowchart TD
    subgraph traditional["Traditional Data Lake"]
        FILES["Just files<br/>(Parquet, CSV)"]
        PROBLEMS["Problems:<br/>❌ No ACID<br/>❌ No time travel<br/>❌ Hard to update"]
    end
    
    subgraph modern["Modern Table Formats"]
        FORMAT["Delta/Iceberg/Hudi"]
        FEATURES["Features:<br/>✅ ACID transactions<br/>✅ Time travel<br/>✅ Schema evolution<br/>✅ Easy updates"]
    end
    
    traditional --> |"Upgrade"| modern
    
    style traditional fill:#fecaca,stroke:#dc2626
    style modern fill:#d1fae5,stroke:#059669
</div>

---

### Delta Lake

**What it is:** Open format by Databricks. Adds ACID to Parquet files.

<div class="mermaid">
flowchart LR
    subgraph delta["Delta Lake Structure"]
        LOG["_delta_log/<br/>(transaction log)"]
        PARQUET["Parquet Files<br/>(actual data)"]
    end
    
    LOG --> |"Tracks changes"| PARQUET
    
    style LOG fill:#dbeafe,stroke:#2563eb
    style PARQUET fill:#d1fae5,stroke:#059669
</div>

**Features:**
```sql
-- Time travel
SELECT * FROM users VERSION AS OF 5;

-- Rollback
RESTORE TABLE users TO VERSION AS OF 3;

-- Schema evolution
ALTER TABLE users ADD COLUMN email STRING;
```

| Feature | Details |
|---------|---------|
| **ACID** | ✅ Full transactions |
| **Time Travel** | ✅ Query old versions |
| **Updates** | ✅ Efficient UPDATE/DELETE |
| **Ecosystem** | Databricks, Spark |

**When to use Delta Lake:**
```
✅ Need ACID transactions on data lake
✅ Frequent UPDATE/DELETE operations
✅ Need to undo changes (time travel)
✅ Using Databricks or Apache Spark
✅ Data quality requirements (schema enforcement)
✅ Regulatory compliance (audit trail)

❌ Simple read-only analytics (Parquet is simpler)
❌ Not using Spark ecosystem
❌ Real-time streaming (consider Hudi)
```

**Real-world examples:**
```
Example 1: GDPR compliance (Delete user data)
Traditional Parquet:
- Find user data across 1000 files
- Rewrite all files without that user
- Hours of work! ❌

Delta Lake:
DELETE FROM users WHERE user_id = 12345;
- Done in seconds!
- Transactional - either all data deleted or none
- Can rollback if mistake! ✅

Example 2: Time travel for debugging
User: "Report was correct yesterday, wrong today!"

Traditional:
- No way to see yesterday's data ❌

Delta Lake:
SELECT * FROM revenue 
  VERSION AS OF 5;  -- Yesterday's version
  
Find exactly what changed! ✅

Example 3: Concurrent writes
Situation: 10 Spark jobs writing to same table

Traditional Parquet:
- Data corruption possible! ❌
- Manual coordination needed

Delta Lake:
- ACID transactions prevent corruption ✅
- All writes succeed or fail cleanly

Example 4: Slowly changing dimensions
UPDATE customers 
  SET address = '123 New St' 
  WHERE customer_id = 456;
  
Traditional: Rewrite entire file
Delta Lake: Just write changes, super fast!
```

📖 **[Deep dive into Delta Lake →](/handbook/topics/delta-lake-deep-dive/)** Learn about transaction logs, time travel, ACID guarantees, and optimization strategies.

---

### Apache Iceberg

**What it is:** Netflix's table format. Works with multiple engines.

<div class="mermaid">
flowchart TD
    ICEBERG["Apache Iceberg"]
    
    ICEBERG --> SPARK["Spark"]
    ICEBERG --> FLINK["Flink"]
    ICEBERG --> TRINO["Trino"]
    ICEBERG --> PRESTO["Presto"]
    
    style ICEBERG fill:#dbeafe,stroke:#2563eb
    style SPARK fill:#d1fae5,stroke:#059669
    style FLINK fill:#d1fae5,stroke:#059669
    style TRINO fill:#d1fae5,stroke:#059669
    style PRESTO fill:#d1fae5,stroke:#059669
</div>

| Feature | Details |
|---------|---------|
| **ACID** | ✅ Yes |
| **Hidden Partitioning** | ✅ Auto-manages partitions |
| **Schema Evolution** | ✅ Safe column changes |
| **Ecosystem** | Engine-agnostic (Spark, Flink, Trino) |

**When to use Iceberg:**
```
✅ Multi-engine environment (Spark + Trino + Flink)
✅ Need vendor independence (avoid lock-in)
✅ Large tables with complex partitioning
✅ Open-source requirements
✅ Using AWS, Azure, or GCP (good cloud support)

❌ Only using Databricks (Delta Lake is better integrated)
❌ Simple use case (Parquet is simpler)
❌ Small team (Delta Lake has more resources)
```

**Real-world examples:**
```
Example 1: Multi-engine analytics platform
Company uses:
- Apache Spark for ETL
- Trino for interactive queries  
- Flink for streaming

Delta Lake: Only works well with Spark ❌
Iceberg: Works with all three! ✅

Example 2: Hidden partitioning (awesome feature!)
Traditional:
SELECT * FROM events 
WHERE date = '2025-01-15'
You must remember table is partitioned by date!

Iceberg:
SELECT * FROM events 
WHERE timestamp = '2025-01-15 10:30:00'
Iceberg automatically finds right partition! ✅

Example 3: Avoiding vendor lock-in
Databricks offers Delta Lake... but worried about lock-in?
Iceberg is vendor-neutral, works anywhere ✅
- AWS Athena: ✅
- Google BigQuery: ✅  
- Azure Synapse: ✅
- Apache Spark: ✅
```

---

### Apache Hudi

**What it is:** Uber's table format. Optimized for streaming updates.

<div class="mermaid">
flowchart LR
    subgraph hudi["Hudi Write Modes"]
        COW["Copy-on-Write<br/>Fast reads"]
        MOR["Merge-on-Read<br/>Fast writes"]
    end
    
    STREAM["Streaming<br/>Updates"] --> |"Choose mode"| hudi
    
    style COW fill:#dbeafe,stroke:#2563eb
    style MOR fill:#fef3c7,stroke:#d97706
    style STREAM fill:#d1fae5,stroke:#059669
</div>

| Feature | Details |
|---------|---------|
| **ACID** | ✅ Yes |
| **Incremental Processing** | ✅ Read only changes |
| **Best For** | Streaming data, frequent updates |
| **Write Modes** | Copy-on-Write, Merge-on-Read |

**When to use Hudi:**
```
✅ High-frequency updates (every minute/second)
✅ CDC (Change Data Capture) from databases
✅ Streaming ingestion from Kafka
✅ Need incremental processing (only read new data)
✅ Uber-style use case (constantly updating data)

❌ Read-only data lake (use Parquet)
❌ Batch updates only (Delta Lake or Iceberg simpler)
❌ Small team (less documentation than Delta/Iceberg)
```

**Real-world examples:**
```
Example 1: Real-time CDC from database
MySQL → Debezium → Kafka → Hudi

Updates streaming every second!
- User updates profile: Immediate
- Order status changes: Immediate  
- Analytics always current ✅

Hudi's Merge-on-Read perfect for this!

Example 2: Incremental processing
Situation: Daily ETL on 1 billion records

Traditional:
- Process entire 1 billion records daily
- 8 hours to complete ❌

Hudi:
- Read only records changed today (1 million)
- 5 minutes to complete ✅
- 100x faster!

Example 3: Uber ride updates
10 million rides in progress
Each ride status updates every 30 seconds
- Traditional: Impossible to keep current ❌
- Hudi: Designed for exactly this! ✅

Rule of thumb:
- Batch updates → Delta Lake or Iceberg
- Streaming updates → Hudi
```

---

### Delta vs Iceberg vs Hudi

| Feature | Delta Lake | Iceberg | Hudi |
|---------|-----------|---------|------|
| **ACID** | ✅ | ✅ | ✅ |
| **Time Travel** | ✅ | ✅ | ✅ |
| **Best Ecosystem** | Databricks | Multi-engine | Spark streaming |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Streaming** | Good | Good | Excellent |
| **Popularity** | Most popular | Growing fast | Niche |

**Which to choose?**
- **Delta Lake:** Using Databricks or want easiest option
- **Iceberg:** Need multi-engine support (Spark + Trino)
- **Hudi:** Heavy streaming workloads

**📚 Deep Dive Articles:**
- **[Parquet Deep Dive →](/handbook/topics/parquet-deep-dive/)** — Columnar storage, encoding schemes, compression
- **[ORC Deep Dive →](/handbook/topics/orc-deep-dive/)** — Three-level indexing, Bloom filters, Hadoop optimization
- **[Avro Deep Dive →](/handbook/topics/avro-deep-dive/)** — Schema evolution, streaming, Kafka integration
- **[Delta Lake Deep Dive →](/handbook/topics/delta-lake-deep-dive/)** — ACID transactions, time travel, optimization

---

## Decision Guide

<div class="mermaid">
flowchart TD
    START["🤔 What are you storing?"]
    
    START --> Q1{"File size?"}
    
    Q1 --> |"< 100 MB"| SMALL["Use CSV or JSON"]
    Q1 --> |"> 100 MB"| Q2
    
    Q2{"Need analytics?"}
    Q2 --> |"Yes"| PARQUET["Use Parquet"]
    Q2 --> |"No"| Q3
    
    Q3{"Need to share<br/>with Excel?"}
    Q3 --> |"Yes"| XLSX["Use XLSX"]
    Q3 --> |"No"| Q4
    
    Q4{"Streaming data?"}
    Q4 --> |"Yes"| AVRO["Use Avro"]
    Q4 --> |"No"| Q5
    
    Q5{"Need ACID<br/>transactions?"}
    Q5 --> |"Yes"| DELTA["Use Delta Lake"]
    Q5 --> |"No"| Q6
    
    Q6{"Human needs<br/>to read it?"}
    Q6 --> |"Yes"| JSON2["Use JSON/YAML"]
    Q6 --> |"No"| PARQUET2["Use Parquet"]
    
    style START fill:#f1f5f9,stroke:#64748b
    style SMALL fill:#d1fae5,stroke:#059669
    style PARQUET fill:#fef3c7,stroke:#d97706
    style XLSX fill:#dbeafe,stroke:#2563eb
    style AVRO fill:#fce7f3,stroke:#db2777
    style DELTA fill:#e0e7ff,stroke:#6366f1
    style JSON2 fill:#d1fae5,stroke:#059669
    style PARQUET2 fill:#fef3c7,stroke:#d97706
</div>

---

## Quick Reference Table

| Format | Type | Size | Speed | Best For |
|--------|------|------|-------|----------|
| **CSV** | Text | Medium | Medium | Small datasets, Excel |
| **JSON** | Text | Large | Medium | APIs, configs |
| **XML** | Text | Very Large | Slow | Legacy systems |
| **YAML** | Text | Medium | Medium | Config files |
| **Parquet** | Binary | Small | Very Fast | Analytics, data warehouses |
| **ORC** | Binary | Small | Very Fast | Hadoop/Hive |
| **Avro** | Binary | Medium | Fast | Kafka, streaming |
| **XLSX** | Binary | Medium | Medium | Excel, business reports |
| **Pickle** | Binary | Small | Fast | Python-only temp storage |
| **GZIP** | Compressed | Very Small | Fast | Any file compression |
| **Delta Lake** | Table | Small | Very Fast | Data lake with ACID |
| **Iceberg** | Table | Small | Very Fast | Multi-engine data lake |
| **Hudi** | Table | Small | Very Fast | Streaming updates |

---

## Common Combinations

Real-world data pipelines often use multiple formats:

<div class="mermaid">
flowchart LR
    SOURCE["📱 App<br/>JSON"] --> KAFKA["📬 Kafka<br/>Avro"]
    KAFKA --> LANDING["🗄️ Landing Zone<br/>Parquet"]
    LANDING --> LAKE["🌊 Data Lake<br/>Delta Lake"]
    LAKE --> WAREHOUSE["❄️ Warehouse<br/>Parquet"]
    WAREHOUSE --> BI["📊 BI Tool<br/>XLSX export"]
    
    style SOURCE fill:#dbeafe,stroke:#2563eb
    style KAFKA fill:#fce7f3,stroke:#db2777
    style LANDING fill:#fef3c7,stroke:#d97706
    style LAKE fill:#e0e7ff,stroke:#6366f1
    style WAREHOUSE fill:#d1fae5,stroke:#059669
    style BI fill:#dbeafe,stroke:#2563eb
</div>

---

## Pro Tips

### 1. Start Simple
```
CSV → Parquet → Delta Lake
```
Don't jump to complex formats until you need them.

### 2. Compression is Free
```bash
# Always compress large files
data.csv → data.csv.gz  # 10x smaller
```

### 3. Parquet for Everything
If unsure, use Parquet. It's fast, small, and widely supported.

**→ [Learn how Parquet works under the hood](/handbook/topics/parquet-deep-dive/)**

### 4. Never Use Pickle for Long-Term Storage
```
❌ model.pkl  (can't read in 2 years)
✅ model.json (always readable)
```

### 5. Match Format to Tool
| Tool | Best Format |
|------|-------------|
| Excel | XLSX, CSV |
| Pandas | Parquet, CSV |
| Spark | Parquet, Delta |
| Kafka | Avro |
| APIs | JSON |

---

## Summary

<div class="mermaid">
flowchart TD
    NEED["What do you need?"]
    
    NEED --> SIMPLE["Keep it simple"] --> CSV
    NEED --> FAST["Fast analytics"] --> PARQUET
    NEED --> STREAM["Streaming"] --> AVRO
    NEED --> ACID["Transactions"] --> DELTA
    NEED --> SHARE["Share with others"] --> XLSX
    NEED --> CONFIG["Config files"] --> YAML
    
    style NEED fill:#dbeafe,stroke:#2563eb
    style CSV fill:#d1fae5,stroke:#059669
    style PARQUET fill:#fef3c7,stroke:#d97706
    style AVRO fill:#fce7f3,stroke:#db2777
    style DELTA fill:#e0e7ff,stroke:#6366f1
    style XLSX fill:#dbeafe,stroke:#2563eb
    style YAML fill:#d1fae5,stroke:#059669
</div>

**Remember:** The best format is the one that solves your problem simply. Start with CSV or JSON, upgrade when you need speed or features!

---

## Further Reading

Want to understand how these formats work under the hood? Check out our in-depth technical guides:

- **[Parquet Deep Dive](/handbook/topics/parquet-deep-dive/)** — How columnar storage actually works, encoding schemes, compression strategies, and performance tips
- **[ORC Deep Dive](/handbook/topics/orc-deep-dive/)** — Three-level indexing, Bloom filters, ACID support in Hive, and why it's optimized for Hadoop
- **[Avro Deep Dive](/handbook/topics/avro-deep-dive/)** — Schema evolution, Schema Registry, variable-length encoding, and Kafka integration
- **[Delta Lake Deep Dive](/handbook/topics/delta-lake-deep-dive/)** — Transaction logs, ACID guarantees, time travel, MERGE operations, and optimization strategies

