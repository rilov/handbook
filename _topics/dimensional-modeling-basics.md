---
title: Dimensional Modeling — A Beginner's Guide
category: Data
tags:
  - data-warehouse
  - dimensional-modeling
  - kimball
  - star-schema
summary: Learn the fundamentals of Kimball dimensional modeling with simple analogies, diagrams, and practical examples.
---

## What is Dimensional Modeling?

Dimensional modeling is a way to organize data in a data warehouse so that it's **easy to understand** and **fast to query**. It was popularized by Ralph Kimball in the 1990s and is still widely used today.

### The Core Idea

Instead of storing data in complex, normalized tables (like in a regular database), we organize it around **business processes** using two types of tables:

<div class="mermaid">
flowchart LR
    subgraph dim["Dimension Tables (The Context)"]
        D1["📅 When?<br/>Date"]
        D2["📦 What?<br/>Product"]
        D3["👤 Who?<br/>Customer"]
        D4["🏪 Where?<br/>Store"]
    end
    
    subgraph fact["Fact Table (The Measurements)"]
        F["💰 Sales<br/>• quantity<br/>• revenue<br/>• cost"]
    end
    
    D1 --> F
    D2 --> F
    D3 --> F
    D4 --> F
    
    style F fill:#dbeafe,stroke:#2563eb
    style D1 fill:#d1fae5,stroke:#059669
    style D2 fill:#d1fae5,stroke:#059669
    style D3 fill:#d1fae5,stroke:#059669
    style D4 fill:#d1fae5,stroke:#059669
</div>

### Real-World Analogy

Think of a **receipt** from a store:
- **Fact** = The numbers on the receipt (quantity, price, total)
- **Dimensions** = The context (what store, what date, what product, which customer)

---

## Fact Tables: The Numbers

### What is a Fact Table?

A fact table stores the **measurements** of a business process — things you can count, sum, or average.

<div class="mermaid">
flowchart TD
    subgraph fact["📊 Fact Table: Sales"]
        direction LR
        F1["date_key<br/>(FK)"]
        F2["product_key<br/>(FK)"]
        F3["customer_key<br/>(FK)"]
        F4["store_key<br/>(FK)"]
        F5["quantity_sold<br/>(measure)"]
        F6["revenue<br/>(measure)"]
        F7["discount<br/>(measure)"]
    end
    
    style F1 fill:#fef3c7,stroke:#d97706
    style F2 fill:#fef3c7,stroke:#d97706
    style F3 fill:#fef3c7,stroke:#d97706
    style F4 fill:#fef3c7,stroke:#d97706
    style F5 fill:#dbeafe,stroke:#2563eb
    style F6 fill:#dbeafe,stroke:#2563eb
    style F7 fill:#dbeafe,stroke:#2563eb
</div>

### Types of Facts

| Type | Description | Example |
|------|-------------|---------|
| **Additive** | Can be summed across all dimensions | Revenue, Quantity |
| **Semi-Additive** | Can be summed across some dimensions | Account Balance (can't sum across time) |
| **Non-Additive** | Cannot be summed | Ratios, Percentages |

### Example Fact Table

| date_key | product_key | customer_key | store_key | quantity | revenue | cost |
|----------|-------------|--------------|-----------|----------|---------|------|
| 20240115 | 1001 | 5001 | 10 | 2 | 59.98 | 30.00 |
| 20240115 | 1002 | 5002 | 10 | 1 | 149.99 | 80.00 |
| 20240116 | 1001 | 5001 | 11 | 3 | 89.97 | 45.00 |

---

## Dimension Tables: The Context

### What is a Dimension Table?

A dimension table provides the **descriptive context** for the facts — the who, what, when, and where.

<div class="mermaid">
flowchart TD
    subgraph dim["👤 Dimension Table: Customer"]
        direction TB
        D1["customer_key (PK)"]
        D2["customer_name"]
        D3["email"]
        D4["city"]
        D5["state"]
        D6["country"]
        D7["signup_date"]
        D8["customer_segment"]
    end
    
    style D1 fill:#fef3c7,stroke:#d97706
    style D2 fill:#d1fae5,stroke:#059669
    style D3 fill:#d1fae5,stroke:#059669
    style D4 fill:#d1fae5,stroke:#059669
    style D5 fill:#d1fae5,stroke:#059669
    style D6 fill:#d1fae5,stroke:#059669
    style D7 fill:#d1fae5,stroke:#059669
    style D8 fill:#d1fae5,stroke:#059669
</div>

### Common Dimensions

| Dimension | Answers | Example Attributes |
|-----------|---------|-------------------|
| **Date** | When? | Year, Quarter, Month, Day, Is_Weekend |
| **Product** | What? | Name, Category, Brand, Price |
| **Customer** | Who? | Name, Segment, Location, Loyalty_Level |
| **Store/Location** | Where? | Address, City, Region, Manager |
| **Employee** | By whom? | Name, Department, Hire_Date |

### Example Dimension Table: Product

| product_key | product_name | category | brand | unit_price | is_active |
|-------------|--------------|----------|-------|------------|-----------|
| 1001 | Wireless Mouse | Electronics | TechBrand | 29.99 | Yes |
| 1002 | Mechanical Keyboard | Electronics | KeyMaster | 149.99 | Yes |
| 1003 | USB Hub | Accessories | TechBrand | 19.99 | No |

---

## Star Schema: The Classic Design

### What is a Star Schema?

The most common dimensional model. It's called a "star" because the diagram looks like a star — one fact table in the center, surrounded by dimension tables.

<div class="mermaid">
flowchart TD
    DIM_DATE["📅 dim_date<br/>─────────<br/>date_key<br/>full_date<br/>day_name<br/>month<br/>quarter<br/>year"]
    
    DIM_PRODUCT["📦 dim_product<br/>─────────<br/>product_key<br/>product_name<br/>category<br/>brand<br/>unit_price"]
    
    FACT["💰 fact_sales<br/>─────────<br/>date_key (FK)<br/>product_key (FK)<br/>customer_key (FK)<br/>store_key (FK)<br/>─────────<br/>quantity<br/>revenue<br/>cost"]
    
    DIM_CUSTOMER["👤 dim_customer<br/>─────────<br/>customer_key<br/>customer_name<br/>email<br/>segment<br/>country"]
    
    DIM_STORE["🏪 dim_store<br/>─────────<br/>store_key<br/>store_name<br/>city<br/>state<br/>manager"]
    
    DIM_DATE --> FACT
    DIM_PRODUCT --> FACT
    FACT --> DIM_CUSTOMER
    FACT --> DIM_STORE
    
    style FACT fill:#dbeafe,stroke:#2563eb
    style DIM_DATE fill:#d1fae5,stroke:#059669
    style DIM_PRODUCT fill:#d1fae5,stroke:#059669
    style DIM_CUSTOMER fill:#d1fae5,stroke:#059669
    style DIM_STORE fill:#d1fae5,stroke:#059669
</div>

### Why Star Schema?

| Benefit | Explanation |
|---------|-------------|
| **Simple to understand** | Business users can easily read it |
| **Fast queries** | Fewer joins = faster performance |
| **Tool-friendly** | BI tools (Tableau, Power BI) love it |
| **Flexible** | Easy to add new dimensions |

---

## Snowflake Schema: The Normalized Cousin

### What is a Snowflake Schema?

A variation where dimension tables are **normalized** (split into sub-tables). It looks like a snowflake because of the branching.

<div class="mermaid">
flowchart TD
    FACT["💰 fact_sales"]
    
    DIM_PRODUCT["📦 dim_product<br/>product_key<br/>product_name<br/>category_key (FK)"]
    
    DIM_CATEGORY["🏷️ dim_category<br/>category_key<br/>category_name<br/>department_key (FK)"]
    
    DIM_DEPARTMENT["🏢 dim_department<br/>department_key<br/>department_name"]
    
    FACT --> DIM_PRODUCT
    DIM_PRODUCT --> DIM_CATEGORY
    DIM_CATEGORY --> DIM_DEPARTMENT
    
    style FACT fill:#dbeafe,stroke:#2563eb
    style DIM_PRODUCT fill:#d1fae5,stroke:#059669
    style DIM_CATEGORY fill:#fef3c7,stroke:#d97706
    style DIM_DEPARTMENT fill:#fce7f3,stroke:#db2777
</div>

### Star vs Snowflake

| Aspect | Star Schema | Snowflake Schema |
|--------|-------------|------------------|
| **Structure** | Denormalized (flat) | Normalized (hierarchical) |
| **Query Speed** | ⚡ Faster (fewer joins) | 🐢 Slower (more joins) |
| **Storage** | More space (duplicate data) | Less space |
| **Simplicity** | ✅ Easier to understand | ❌ More complex |
| **Recommendation** | ✅ Usually preferred | Use when storage is critical |

---

## The Date Dimension: A Special Case

### Why is Date Special?

Every data warehouse needs a **date dimension**. It's pre-built with useful attributes for time-based analysis.

<div class="mermaid">
flowchart LR
    subgraph date_dim["📅 dim_date"]
        D1["date_key: 20240115"]
        D2["full_date: 2024-01-15"]
        D3["day_name: Monday"]
        D4["day_of_week: 2"]
        D5["week_of_year: 3"]
        D6["month: January"]
        D7["month_number: 1"]
        D8["quarter: Q1"]
        D9["year: 2024"]
        D10["is_weekend: No"]
        D11["is_holiday: No"]
        D12["fiscal_year: FY2024"]
    end
</div>

### Example Date Dimension Table

| date_key | full_date | day_name | month | quarter | year | is_weekend | is_holiday |
|----------|-----------|----------|-------|---------|------|------------|------------|
| 20240115 | 2024-01-15 | Monday | January | Q1 | 2024 | No | No |
| 20240116 | 2024-01-16 | Tuesday | January | Q1 | 2024 | No | No |
| 20240120 | 2024-01-20 | Saturday | January | Q1 | 2024 | Yes | No |

This lets you easily query things like:
- "Show me all sales on weekends"
- "Compare Q1 vs Q2"
- "What's the trend for Mondays?"

---

## Slowly Changing Dimensions (SCD)

### The Problem

What happens when dimension data changes? A customer moves to a new city. A product gets a new price. How do you track history?

<div class="mermaid">
flowchart LR
    subgraph before["Before Move"]
        B["👤 John Smith<br/>City: New York"]
    end
    
    subgraph after["After Move"]
        A["👤 John Smith<br/>City: Los Angeles"]
    end
    
    before --> |"Moves!"| after
    
    Q["❓ What do we do<br/>with old sales in NY?"]
    
    style Q fill:#fef3c7,stroke:#d97706
</div>

### SCD Types

<div class="mermaid">
flowchart TD
    SCD["Slowly Changing Dimension Types"]
    
    SCD --> T0["Type 0<br/>Never change<br/>(retain original)"]
    SCD --> T1["Type 1<br/>Overwrite<br/>(lose history)"]
    SCD --> T2["Type 2<br/>Add new row<br/>(keep history)"]
    SCD --> T3["Type 3<br/>Add new column<br/>(limited history)"]
    
    style T0 fill:#f1f5f9,stroke:#64748b
    style T1 fill:#fecaca,stroke:#dc2626
    style T2 fill:#d1fae5,stroke:#059669
    style T3 fill:#fef3c7,stroke:#d97706
</div>

### SCD Type 2 Example (Most Common)

| customer_key | customer_id | name | city | start_date | end_date | is_current |
|--------------|-------------|------|------|------------|----------|------------|
| 1001 | C100 | John Smith | New York | 2020-01-01 | 2024-06-30 | No |
| 1002 | C100 | John Smith | Los Angeles | 2024-07-01 | 9999-12-31 | Yes |

**Same customer, two rows!** Old sales link to key 1001 (NY), new sales link to key 1002 (LA).

### When to Use Each Type

| Type | Use When | Example |
|------|----------|---------|
| **Type 0** | Value should never change | Original signup date |
| **Type 1** | History doesn't matter | Fixing typos |
| **Type 2** | Need full history | Customer address, product price |
| **Type 3** | Only need previous value | Previous manager |

---

## Building a Dimensional Model: Step by Step

<div class="mermaid">
flowchart TD
    S1["1️⃣ Select Business Process<br/>'What are we measuring?'"]
    S2["2️⃣ Declare the Grain<br/>'What does one row represent?'"]
    S3["3️⃣ Identify Dimensions<br/>'What context do we need?'"]
    S4["4️⃣ Identify Facts<br/>'What numbers do we measure?'"]
    
    S1 --> S2 --> S3 --> S4
    
    style S1 fill:#dbeafe,stroke:#2563eb
    style S2 fill:#d1fae5,stroke:#059669
    style S3 fill:#fef3c7,stroke:#d97706
    style S4 fill:#fce7f3,stroke:#db2777
</div>

### Example: E-Commerce Orders

| Step | Question | Answer |
|------|----------|--------|
| **1. Business Process** | What are we analyzing? | Online Orders |
| **2. Grain** | What's one row? | One order line item |
| **3. Dimensions** | What's the context? | Date, Customer, Product, Promotion |
| **4. Facts** | What do we measure? | Quantity, Revenue, Discount, Shipping Cost |

---

## Is Dimensional Modeling Still Relevant?

**Yes!** Here's why it's still widely used:

| Modern Context | Why Dimensional Modeling Works |
|----------------|-------------------------------|
| **Cloud Data Warehouses** (Snowflake, BigQuery, Redshift) | Still optimized for star schemas |
| **BI Tools** (Tableau, Power BI, Looker) | Expect dimensional models |
| **Business Users** | Understand star schemas intuitively |
| **Performance** | Denormalized data = fast queries |

### Modern Adaptations

<div class="mermaid">
flowchart LR
    subgraph traditional["Traditional (Kimball)"]
        T1["ETL → Star Schema"]
    end
    
    subgraph modern["Modern Approach"]
        M1["ELT → Raw Data"]
        M2["dbt transforms"]
        M3["Star Schema"]
        M1 --> M2 --> M3
    end
    
    style T1 fill:#f1f5f9,stroke:#64748b
    style M3 fill:#d1fae5,stroke:#059669
</div>

Tools like **dbt** now help build dimensional models using SQL transformations, making it easier than ever.

---

## Quick Reference

### Fact vs Dimension Cheat Sheet

| Question | Fact Table | Dimension Table |
|----------|------------|-----------------|
| What does it store? | Measurements | Context/Descriptions |
| Example columns | Revenue, Quantity, Cost | Name, Category, Date |
| Row count | Many (millions+) | Fewer (thousands) |
| Changes often? | New rows added constantly | Changes slowly |
| Width | Narrow (few columns) | Wide (many columns) |

### Key Terms

| Term | Simple Definition |
|------|-------------------|
| **Grain** | What one row in a fact table represents |
| **Surrogate Key** | System-generated ID (1, 2, 3...) used as primary key |
| **Natural Key** | Business ID from source system (SKU, Customer ID) |
| **Conformed Dimension** | Same dimension used across multiple fact tables |
| **Junk Dimension** | Groups miscellaneous flags/indicators |
| **Degenerate Dimension** | Dimension stored in fact table (e.g., Order Number) |

---

## Summary

<div class="mermaid">
flowchart TD
    DM["Dimensional Modeling"]
    
    DM --> FACT["📊 Fact Tables<br/>Store measurements<br/>(revenue, quantity)"]
    DM --> DIM["📦 Dimension Tables<br/>Store context<br/>(who, what, when, where)"]
    DM --> STAR["⭐ Star Schema<br/>Simple, fast, popular"]
    DM --> SCD["🔄 Handle Changes<br/>SCD Type 1, 2, 3"]
    
    style DM fill:#dbeafe,stroke:#2563eb
    style FACT fill:#d1fae5,stroke:#059669
    style DIM fill:#fef3c7,stroke:#d97706
    style STAR fill:#fce7f3,stroke:#db2777
    style SCD fill:#e0e7ff,stroke:#6366f1
</div>

**Remember:**
- **Fact tables** = The numbers you measure
- **Dimension tables** = The context around those numbers
- **Star schema** = Facts in the center, dimensions around it
- **Keep it simple** = Business users should understand it!

---

*Inspired by Ralph Kimball's dimensional modeling methodology. For deeper learning, check out "The Data Warehouse Toolkit" by Ralph Kimball.*

