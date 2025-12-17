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

> **🎓 Want to go deeper?** This guide covers the essentials. For in-depth technical details, check out our deep dive articles on [Parquet](/topics/parquet-deep-dive/), [ORC](/topics/orc-deep-dive/), [Avro](/topics/avro-deep-dive/), and [Delta Lake](/topics/delta-lake-deep-dive/).

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

**Real-World Analogy:** Instead of reading entire books to find all mentions of "data," you have an index that lists every page with "data."

📖 **[Deep dive into Parquet →](/topics/parquet-deep-dive/)** Learn how Parquet actually stores data, encoding schemes, and performance optimization.

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

**Which to choose?** Use Parquet unless you're deep in the Hadoop ecosystem.

📖 **[Deep dive into ORC →](/topics/orc-deep-dive/)** Explore ORC's three-level indexing, Bloom filters, and when it beats Parquet.

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

**When to Use:**
- ✅ Kafka / event streaming
- ✅ Schema evolution (adding fields over time)
- ❌ Analytics (use Parquet instead)

📖 **[Deep dive into Avro →](/topics/avro-deep-dive/)** Understand schema evolution, Schema Registry, and why Kafka uses Avro.

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

---

### BZIP2 (.bz2)

**What it is:** Slower compression, but better compression ratio than GZIP.

| Format | Compression | Speed | Use When |
|--------|-------------|-------|----------|
| **GZIP** | Good | Fast | Default choice |
| **BZIP2** | Better | Slower | Archiving, storage |
| **ZIP** | Good | Fast | Multiple files |

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

📖 **[Deep dive into Delta Lake →](/topics/delta-lake-deep-dive/)** Learn about transaction logs, time travel, ACID guarantees, and optimization strategies.

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
- **[Parquet Deep Dive →](/topics/parquet-deep-dive/)** — Columnar storage, encoding schemes, compression
- **[ORC Deep Dive →](/topics/orc-deep-dive/)** — Three-level indexing, Bloom filters, Hadoop optimization
- **[Avro Deep Dive →](/topics/avro-deep-dive/)** — Schema evolution, streaming, Kafka integration
- **[Delta Lake Deep Dive →](/topics/delta-lake-deep-dive/)** — ACID transactions, time travel, optimization

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

**→ [Learn how Parquet works under the hood](/topics/parquet-deep-dive/)**

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

- **[Parquet Deep Dive](/topics/parquet-deep-dive/)** — How columnar storage actually works, encoding schemes, compression strategies, and performance tips
- **[ORC Deep Dive](/topics/orc-deep-dive/)** — Three-level indexing, Bloom filters, ACID support in Hive, and why it's optimized for Hadoop
- **[Avro Deep Dive](/topics/avro-deep-dive/)** — Schema evolution, Schema Registry, variable-length encoding, and Kafka integration
- **[Delta Lake Deep Dive](/topics/delta-lake-deep-dive/)** — Transaction logs, ACID guarantees, time travel, MERGE operations, and optimization strategies

