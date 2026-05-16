---
title: "Case Study: How Netflix Solved the 100 Petabyte Problem with Apache Iceberg"
category: Case Studies
tags:
  - case-study
  - netflix
  - iceberg
  - data-lake
  - hive
  - s3
  - data-architecture
summary: A simple story about why Netflix had to invent a new way to manage data, what was breaking, and how the fix changed the entire data industry.
date: 2025-06-23
---

# Case Study: How Netflix Solved the 100 Petabyte Problem with Apache Iceberg

## A simple story about why Netflix had to invent a new way to manage data

Most people know Netflix for movies and shows.

But behind the scenes, Netflix is actually one of the largest data companies in the world.

Every time you click play, pause, search, scroll, rate, or skip, that action becomes a row of data.

Multiply that by 250 million users, every day, all year. The numbers get scary very quickly.

By 2017, Netflix had over 100 petabytes of data sitting in Amazon S3.

That is 100,000 terabytes.

To put that in perspective, if you tried to download all of it on a normal home internet connection, it would take you several thousand years.

And that data was growing every single day.

Two engineers at Netflix, Ryan Blue and Daniel Weeks, were responsible for keeping all of this data usable. They were the ones who had to make sure analysts could query it, machine learning teams could train on it, and product teams could trust the numbers.

And by 2017, the system they were using was starting to break.

This is the story of how they fixed it. And how that fix accidentally became the foundation for almost every modern data platform you hear about today.

---

## What was the system they were using?

For years, the standard tool for managing big data was something called **Apache Hive**.

You can think of Hive as a way to organize data files inside folders, and then run SQL queries on top of those folders.

Here is the basic idea.

Imagine you have a folder on your computer called `events`. Inside that folder, you have one folder per day:

```
events/
  date=2017-01-01/
    file1.parquet
    file2.parquet
  date=2017-01-02/
    file1.parquet
  date=2017-01-03/
    file1.parquet
    file2.parquet
    file3.parquet
```

Hive treated this folder structure as a table.

When you ran a query like "give me everything from January 2", Hive would go to the folder `date=2017-01-02`, list all the files inside, and read them.

Simple. Clean. Made sense in 2008.

The problem is that 2017 looked very different from 2008.

---

## Why this idea stopped working

Hive was originally built in the era of Hadoop.

In Hadoop, data was stored on real computers with real disks. Folders were real folders. Renaming a file was instant. Listing files was fast. Everything was predictable. Hive was designed around all of that.

Now here is the important part.

Netflix did use Hive. But Netflix did not store its data on Hadoop disks. Netflix stored its data on Amazon S3.

This is a small detail that turns out to be enormous.

Hive was being asked to behave like it was running on a Hadoop file system, but the actual storage underneath it was S3. And S3 is not really a file system at all.

S3 is what people call **object storage**. It just stores blobs of data with names. There are no real folders. There are no real renames. Nothing is instant.

When you ask S3 to "list a folder", what you are really doing is searching all the keys in a giant flat namespace that happen to start with the same prefix. If there are millions of keys, this takes a long time.

When you ask S3 to "rename a file", what really happens is that S3 copies the entire file to a new name and deletes the old one. For a tiny file this is fine. For a hundred gigabyte file, this is painful.

So Hive was built on three big assumptions:

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph LR
    subgraph HIVE["<b>What Hive Assumed</b>"]
        H1["<b>Folders are real</b>"]
        H2["<b>Renames are instant</b>"]
        H3["<b>Listing is fast</b>"]
    end
    subgraph S3["<b>What S3 Actually Does</b>"]
        R1["<b>Folders are fake</b>"]
        R2["<b>Renames copy the whole file</b>"]
        R3["<b>Listing is slow at scale</b>"]
    end
    H1 -.->|"breaks on"| R1
    H2 -.->|"breaks on"| R2
    H3 -.->|"breaks on"| R3
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class H1,H2,H3 gray
    class R1,R2,R3 midgray
    style HIVE fill:#f5f5f5,stroke:#666,color:#111
    style S3 fill:#f5f5f5,stroke:#666,color:#111
</div>

Every one of those assumptions was wrong on S3.

So when Netflix tried to do normal things on Hive tables, normal things kept going badly.

---

## The five things that kept going wrong

Let me describe each problem in plain language, because this is the part most articles skip.

### Problem 1. Queries took forever to even start running

Imagine you want to run this query.

```sql
SELECT count(*) FROM events WHERE date = '2017-06-15';
```

Before any actual reading happens, Hive has to figure out which files to read.

To do that, it goes to the table location and asks, "what folders are inside this table?" That alone might list ten thousand date folders. Then for each matching folder, it asks, "what files are inside?"

On a real disk this is microseconds.

On S3 this might be minutes.

Netflix had tables with hundreds of thousands of partition folders. Just figuring out where to look could take five or ten minutes before even the first byte of data was read.

That is unacceptable when an analyst is sitting there waiting.

### Problem 2. There was no safe way to write to a table

Here is something most people do not realize.

When you write to a Hive table, your changes do not appear all at once. They appear file by file as each one finishes uploading.

So while a job is running, anyone reading the table sees a half written version. Some new files are visible, some are not, and the data may not even be self consistent.

Worse, if your job crashes halfway, the table is now permanently in a half written state. Nobody knows what is real and what is leftover garbage from the failed job.

There is no way to say, "this whole batch of changes either appears completely or does not appear at all."

That property is called **atomicity**, and Hive simply did not have it on S3.

### Problem 3. Different tools disagreed about what the table even was

This sounds crazy, but it is true.

Hive never had a real specification. It was a collection of conventions that grew over time.

So when Spark, Presto, Trino, Impala, and Hive itself all tried to read the same table, they sometimes disagreed about things like:

* How exactly to hash a value to decide which bucket file it goes into
* How to handle null values in partition columns
* How to read corrupted or partial files
* What to do when a column was added or removed

This meant that running the same query through two different engines could give two different answers.

In a company that makes business decisions on these numbers, that is a disaster.

### Problem 4. Locking did not actually work

Hive tried to support safe concurrent writes by adding a locking system.

The problem was that the lock only worked if every tool obeyed it. And most tools did not.

So in practice, two jobs could write to the same table at the same time and corrupt it. The only safe rule was, "make sure only one writer touches each table at any time." That is fine in theory but impossible in practice when you have thousands of pipelines.

### Problem 5. Engineers stopped trusting their own data

This is the deepest problem, and it is the one that actually pushed Netflix to build something new.

When the data warehouse becomes unsafe to change, engineers start avoiding it.

They stop running compactions, even though small files are killing performance. They stop fixing partition mistakes, even though queries are scanning extra data. They stop backfilling old corrections, even when the numbers are wrong.

Why? Because every change might leave the table in a broken state. And the cost of breaking a production table that thousands of people depend on is huge.

So instead of fixing things, people just learn to live with them. The system slowly rots.

> **The single most important sentence in this whole story is this one.**
> 
> **Netflix engineers had stopped touching their own warehouse because they were afraid of breaking it.**

That is when Ryan Blue and Daniel Weeks decided enough was enough. There had to be a better way.

---

## The big idea behind the fix

Here is the insight that changed everything. It is so simple that it is easy to miss why it matters.

In Hive, the folder structure on disk **is** the table. To know what is in the table, you have to go list the folders.

In Iceberg, the folder structure on disk does not matter at all. There is a small file somewhere that says, "here are the exact files that make up this table right now, with their statistics, their partition values, and their schema."

That small file is the table.

The data files just sit there as plain Parquet files. They never move. They never get renamed. They are written once and read many times.

When you want to change the table, you do not move data around. You just write a new version of the small metadata file that points to a different set of data files.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    subgraph BEFORE["<b>Hive way: the folder is the table</b>"]
        T1["<b>Table</b>"]
        T1 --> P1["<b>folder for Jan 1</b><br/>(list to find files)"]
        T1 --> P2["<b>folder for Jan 2</b><br/>(list to find files)"]
        T1 --> P3["<b>folder for Jan 3</b><br/>(list to find files)"]
    end
    subgraph AFTER["<b>Iceberg way: a tiny file is the table</b>"]
        M1["<b>metadata.json</b><br/>'this is version 42'"]
        M1 --> SN["<b>snapshot</b><br/>list of files at this moment"]
        SN --> F1["<b>file 1</b>"]
        SN --> F2["<b>file 2</b>"]
        SN --> F3["<b>file 3</b>"]
        SN --> F4["<b>file 4</b>"]
    end
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    classDef midgray fill:#bdbdbd,stroke:#222,stroke-width:1.5px,color:#000
    class T1,P1,P2,P3,F1,F2,F3,F4 gray
    class M1,SN midgray
    style BEFORE fill:#f5f5f5,stroke:#666,color:#111
    style AFTER fill:#f5f5f5,stroke:#666,color:#111
</div>

That tiny shift, from "folder is table" to "metadata file is table", solves almost every problem at once. Let me show you why.

---

## Why this fixes everything

### It fixes atomic writes

When a job wants to add data to an Iceberg table, here is what happens.

Step 1. The job writes its new Parquet files to S3. These files exist, but no metadata points to them yet, so nobody can see them.

Step 2. The job writes a new metadata file that lists both the old data files and the new ones.

Step 3. The job tells the catalog, "the current version of this table is now this new metadata file."

That last step is one tiny atomic operation. Either it succeeds and everyone immediately sees the new data, or it fails and nothing changes.

There is no half written state. There is no partial visibility. Either the change happened, or it did not.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
sequenceDiagram
    participant J as Job
    participant S as S3
    participant C as Catalog
    J->>S: Step 1. Write new data files (invisible to readers)
    J->>S: Step 2. Write new metadata file pointing to those files
    J->>C: Step 3. Atomically swap pointer to new metadata
    Note over J,C: If another job swapped first,<br/>this job retries from step 2
    C-->>J: Done. Everyone now sees the new version.
</div>

### It fixes slow query planning

Because the metadata file already lists every data file with statistics like minimum and maximum values, the query engine never has to list folders on S3.

It just opens the metadata file, looks at the statistics, and skips files that cannot match the query.

What used to take five minutes now takes a fraction of a second.

### It fixes the trust problem

Because every change creates a new metadata file, the old metadata file still exists. The old data files still exist.

That means you can do something amazing. You can ask, "show me the table as it was yesterday at 3pm." Iceberg just reads the metadata file from that moment.

This is called **time travel**.

It also means if someone runs a bad query that messes up a table, you can roll back to the previous version with one tiny operation. No restoring from backup. No recovering files. Just point the catalog at the old metadata file and you are done.

Engineers stopped being scared of changing tables, because every change was reversible.

### It fixes the engine disagreement problem

Iceberg started life with a real specification. Not a wiki page. Not a collection of habits. An actual document that says exactly how a compliant tool must read and write tables.

That means Spark, Trino, Flink, Presto, Snowflake, Databricks, Amazon Athena, and Google BigQuery can all read the same Iceberg table and they will all see the same thing.

This is huge. Before Iceberg, the choice of storage format locked you into a specific tool. After Iceberg, the storage and the compute became independent.

### It fixes the schema change problem

In Hive, adding a new column often meant rewriting the entire table. For a 100 terabyte table, that could take days.

In Iceberg, the schema is part of the metadata file. Adding a column is a metadata change, not a data change. It takes milliseconds.

You can rename columns, drop columns, add columns, and even change the partitioning of the table, without touching a single byte of actual data.

---

## A really nice extra: hidden partitioning

Here is one more feature that mattered a lot for Netflix data scientists.

In Hive, if a table was partitioned by day, every query had to remember to filter on day. If you forgot, your query would scan the entire table and probably crash.

In Iceberg, the user does not need to know how the table is partitioned. They just write the natural query.

```sql
SELECT user_id, count(*)
FROM events
WHERE event_time > '2024-06-01'
GROUP BY user_id;
```

Iceberg sees that the table is partitioned by day of `event_time`, automatically figures out which partitions to read, and only reads those.

The user did not have to know anything about the physical layout. The platform team can change that layout later without breaking a single query.

For a company with thousands of analysts running millions of queries, this saves enormous amounts of time and prevents endless mistakes.

---

## The numbers Netflix actually saw

Here is what changed at Netflix after they switched to Iceberg.

| What was measured | Before, with Hive | After, with Iceberg |
|---|---|---|
| Total tables managed | tens of thousands | over 1 million |
| Warehouse size | tens of petabytes | over 100 petabytes |
| Time to plan a query on a huge table | several minutes | well under a second |
| Atomic writes that cannot be half done | not possible | yes |
| Time travel to old versions | not possible | yes |
| Concurrent writers without corruption | dangerous | safe |
| Schema change on a huge table | hours or days | milliseconds |

But honestly, the biggest change was not in any of these numbers.

The biggest change was that engineers started writing to the warehouse again.

When something is safe to change, people change it. They optimize it. They fix old mistakes. They run experiments. They make the platform better.

That cultural shift is what really mattered.

---

## Why Netflix gave it away

Here is something a lot of companies would not have done.

Netflix did not keep Iceberg as an internal advantage. They open sourced it.

They gave it to the Apache Software Foundation in November 2018. By May 2020 it was a top level Apache project. Today it is used by Apple, Airbnb, LinkedIn, Adobe, Lyft, Expedia, Stripe, and basically every major data platform you can think of.

Why give away such a valuable invention?

The team had three reasons, and they are worth understanding.

<div class="mermaid">
%%{init: {'theme':'neutral', 'themeVariables': {'fontSize':'16px', 'fontFamily':'Helvetica, Arial, sans-serif'}}}%%
graph TD
    OS["<b>Why open source?</b>"]
    OS --> R1["<b>1. The problem was not unique to Netflix</b><br/>Every company on cloud storage<br/>was hitting the same wall"]
    OS --> R2["<b>2. They needed many engines to agree</b><br/>Spark, Trino, Flink all had to read<br/>the same tables the same way"]
    OS --> R3["<b>3. It made hiring easier</b><br/>Engineers want to work on<br/>industry standard tools, not<br/>private internal hacks"]
    classDef gray fill:#e8e8e8,stroke:#333,stroke-width:1.5px,color:#111
    class R1,R2,R3 gray
    style OS fill:#757575,stroke:#000,stroke-width:2.5px,color:#fff
</div>

The first reason is the most important.

If you build something that solves an industry wide problem, and you keep it private, two things happen. Other companies will eventually build their own version. Your version will fall behind because it only has your engineers working on it. Your private fork becomes a maintenance burden.

If you open source it, the rest of the industry helps you maintain it. You still get to use it. You just get a lot more help.

That is exactly what happened. The Iceberg community now has hundreds of contributors from dozens of companies. Netflix did not have to fund all of that work themselves.

---

## What everyone else can learn from this story

You do not need to be Netflix for this story to matter.

Five lessons stand out.

### Lesson one. The right abstraction matters more than the right tool

Hive was not a bad tool. It was a great tool for its time. The problem was that the world moved from disks to object storage, and Hive's basic mental model did not move with it.

When the underlying technology changes, sometimes you have to change the abstraction layer too. You cannot just keep adding patches.

### Lesson two. Trust is part of performance

Most people measure data platforms by query latency or storage cost. Netflix realized that the real bottleneck was something else entirely. Engineers had stopped trusting the system, so they stopped using it fully.

If your team is afraid to make changes, you have a much bigger problem than slow queries.

### Lesson three. Treat metadata like a real product

Most teams think of metadata as bookkeeping. Iceberg flipped this. The metadata is the product. The data files are just the bytes the metadata happens to point at.

Once you take metadata seriously, you get atomicity, rollback, time travel, and engine independence almost for free.

### Lesson four. Write a specification, not just code

Hive's biggest weakness was that it never had a real spec. Different tools implemented different behaviors and called it Hive. The result was years of subtle bugs and disagreements.

Iceberg started with a spec. That single decision is why Snowflake, Databricks, BigQuery, Athena, Spark, and Trino can all read the same tables today without arguing.

### Lesson five. Sometimes the right thing to build is a standard

Most companies build internal tools to solve internal problems. Sometimes the bigger move is to recognize that everyone has the same problem, and build a standard that the whole industry can adopt.

It is more work upfront. It pays back many times over.

---

## Closing thought

When you look at Iceberg as a piece of software, it is honestly not that flashy.

A few JSON files. Some manifest files. A list of Parquet paths. A small library that knows how to read and write all of that consistently.

It is not glamorous. It is not built on some new programming language. It does not use exotic algorithms.

What it does is redraw one boundary in the data stack. The boundary between "what is the table" and "where are the bytes." And by drawing that boundary in a slightly different place, it made everything above and below it simpler, faster, and safer.

That is the kind of work that quietly changes an industry.

When asked what would happen if Iceberg disappeared from Netflix tomorrow, an engineer on the data team gave an answer that sums it all up.

> "Iceberg is at the heart of Netflix. Without it, both the company and the streaming platform would cease to exist."

The lesson for the rest of us is not to use Iceberg specifically.

The lesson is this.

When your data platform makes engineers afraid to touch their own data, the answer is not better tools on top of the broken layer. The answer is to fix the broken layer itself, even if it means rebuilding something the whole industry has been using for ten years.

Sometimes that is the only way forward.
