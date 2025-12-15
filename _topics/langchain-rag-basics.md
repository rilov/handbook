---
title: "Part 4 - RAG Basics: Teaching AI About Your Documents"
category: Generative AI
order: 4
tags:
  - langchain
  - rag
  - vector-stores
  - embeddings
  - retrieval
summary: Learn how to build RAG (Retrieval Augmented Generation) systems that let AI answer questions from your documents - explained simply.
related:
  - langchain-tool-calling
  - langgraph-agents
---

> **🎓 LangChain Learning Path - Step 4 of 7**
> - **[← Step 3: Tool Calling]({{ site.baseurl }}{% link _topics/langchain-tool-calling.md %})**
> - **Step 4 (this page):** RAG Basics
> - **[Step 5: LangGraph & Agents →]({{ site.baseurl }}{% link _topics/langgraph-agents.md %})**

---

## The Problem: LLMs Don't Know Your Data

LLMs are trained on public internet data, but they don't know about:
- Your company's internal documents
- Your personal notes
- Recent information (after their training cutoff)
- Proprietary data

<div class="mermaid">
flowchart LR
    subgraph knows["✅ LLM Knows"]
        K1["Public facts"]
        K2["General knowledge"]
        K3["Common patterns"]
    end
    
    subgraph unknown["❌ LLM Doesn't Know"]
        U1["Your documents"]
        U2["Recent events"]
        U3["Private data"]
    end
    
    style knows fill:#d1fae5,stroke:#059669
    style unknown fill:#fecaca,stroke:#dc2626
</div>

**RAG solves this problem!**

---

## What is RAG?

### The Simple Explanation

**RAG (Retrieval Augmented Generation)** is like giving an AI a library card and teaching it to look things up before answering.

<div class="mermaid">
flowchart TB
    Q["👤 User: What's our refund policy?"]
    R["🔍 Search Documents"]
    F["📄 Find relevant info"]
    AI["🤖 LLM + Found Info"]
    A["💬 Answer with citations"]
    
    Q --> R --> F --> AI --> A
    
    style Q fill:#dbeafe,stroke:#2563eb
    style R fill:#fef3c7,stroke:#d97706
    style F fill:#fce7f3,stroke:#db2777
    style AI fill:#d1fae5,stroke:#059669
    style A fill:#d1fae5,stroke:#059669
</div>

### Real-World Analogy

Imagine asking a librarian a question:

**Without RAG (Bad Librarian):**
```
You: "What does our employee handbook say about vacation days?"
Librarian: "I think it's probably 10-15 days? That seems normal..."
```
*(Making it up!)*

**With RAG (Good Librarian):**
```
You: "What does our employee handbook say about vacation days?"
Librarian: (pulls out handbook, reads page 23)
Librarian: "According to page 23, employees get 15 vacation days annually."
```
*(Looks it up first!)*

---

## How RAG Works: The Four Steps

<div class="mermaid">
flowchart TD
    S1["1️⃣ Load Documents"]
    S2["2️⃣ Create Embeddings<br/>& Store in Vector DB"]
    S3["3️⃣ Retrieve Relevant Docs<br/>for Question"]
    S4["4️⃣ Generate Answer<br/>Using Retrieved Docs"]
    
    S1 --> S2 --> S3 --> S4
    
    style S1 fill:#dbeafe,stroke:#2563eb
    style S2 fill:#fef3c7,stroke:#d97706
    style S3 fill:#fce7f3,stroke:#db2777
    style S4 fill:#d1fae5,stroke:#059669
</div>

Let's break down each step!

---

## Step 1: Loading Documents

### What is Document Loading?

Reading files and breaking them into manageable chunks.

<div class="mermaid">
flowchart LR
    F["📄 Large File<br/>(100 pages)"]
    L["Document Loader"]
    C["📚 Many Chunks<br/>(Each ~500 words)"]
    
    F --> L --> C
    
    style F fill:#fecaca,stroke:#dc2626
    style L fill:#fef3c7,stroke:#d97706
    style C fill:#d1fae5,stroke:#059669
</div>

### Loading Different File Types

```python
from langchain.document_loaders import (
    TextLoader,
    PDFLoader,
    WebBaseLoader,
    DirectoryLoader
)

# Load a text file
text_loader = TextLoader("company_policy.txt")
text_docs = text_loader.load()

# Load a PDF
pdf_loader = PDFLoader("manual.pdf")
pdf_docs = pdf_loader.load()

# Load from a website
web_loader = WebBaseLoader("https://example.com/docs")
web_docs = web_loader.load()

# Load all files in a directory
dir_loader = DirectoryLoader("./documents", glob="**/*.txt")
all_docs = dir_loader.load()
```

### Why Split Documents?

Documents are split into chunks because:
1. LLMs have token limits (can't read entire book at once)
2. Smaller chunks = more precise retrieval
3. Better performance and cost

<div class="mermaid">
flowchart TB
    subgraph wrong["❌ Whole Document"]
        W["Send entire<br/>100-page document<br/>to LLM"]
        P1["Expensive"]
        P2["Slow"]
        P3["Hits token limit"]
    end
    
    subgraph right["✅ Smart Chunks"]
        C["Send only<br/>relevant paragraphs"]
        B1["Cheap"]
        B2["Fast"]
        B3["Focused"]
    end
    
    style wrong fill:#fecaca,stroke:#dc2626
    style right fill:#d1fae5,stroke:#059669
</div>

### Splitting Documents

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load documents
loader = TextLoader("big_document.txt")
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # ~500 characters per chunk
    chunk_overlap=50,    # 50 character overlap between chunks
)

chunks = text_splitter.split_documents(documents)

print(f"Split into {len(chunks)} chunks")
```

**Why overlap?**
Overlap ensures important information at chunk boundaries isn't lost.

```
Chunk 1: "...employees get 15 vacation days. This includes..."
                                            ↓ overlap
Chunk 2: "...This includes holidays and sick leave..."
```

---

## Step 2: Embeddings & Vector Stores

### What are Embeddings?

**Embeddings** convert text into numbers that capture meaning. Similar meanings = similar numbers!

<div class="mermaid">
flowchart TB
    subgraph text["📝 Text"]
        T1["dog"]
        T2["puppy"]
        T3["car"]
    end
    
    subgraph embed["🔢 Embeddings"]
        E1["[0.8, 0.9, 0.1]"]
        E2["[0.7, 0.85, 0.15]"]
        E3["[0.1, 0.2, 0.9]"]
    end
    
    T1 --> E1
    T2 --> E2
    T3 --> E3
    
    Note["dog & puppy are close<br/>car is far away"]
    
    style text fill:#dbeafe,stroke:#2563eb
    style embed fill:#fef3c7,stroke:#d97706
</div>

### Real-World Analogy

Think of embeddings like a **coordinate system for meanings**:

```
Coordinates on a map:
- New York:  (40.7°N, 74.0°W)
- Boston:    (42.4°N, 71.1°W)  ← Close to New York!
- Los Angeles: (34.1°N, 118.2°W)  ← Far from New York

Embeddings for words:
- "king":   [0.8, 0.5, 0.1]
- "queen":  [0.75, 0.48, 0.12]  ← Close to "king"!
- "apple":  [0.2, 0.9, 0.7]  ← Far from "king"
```

### Creating Embeddings

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# Embed some text
text = "The quick brown fox jumps over the lazy dog"
vector = embeddings.embed_query(text)

print(f"Embedding has {len(vector)} dimensions")
# Output: Embedding has 1536 dimensions
```

### Vector Stores

A **vector store** is like a library catalog but for embeddings. It stores documents and lets you search by meaning!

<div class="mermaid">
flowchart LR
    subgraph docs["📚 Documents"]
        D1["Doc 1"]
        D2["Doc 2"]
        D3["Doc 3"]
    end
    
    E["Create Embeddings"]
    
    subgraph vs["🗄️ Vector Store"]
        V1["Vector 1"]
        V2["Vector 2"]
        V3["Vector 3"]
    end
    
    docs --> E --> vs
    
    style docs fill:#dbeafe,stroke:#2563eb
    style E fill:#fef3c7,stroke:#d97706
    style vs fill:#d1fae5,stroke:#059669
</div>

### Creating a Vector Store

```python
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# 1. Load documents
loader = TextLoader("company_handbook.txt")
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings
embeddings = OpenAIEmbeddings()

# 4. Create vector store
vectorstore = FAISS.from_documents(chunks, embeddings)

print(f"Created vector store with {len(chunks)} documents")
```

---

## Step 3: Retrieval

### What is a Retriever?

A **retriever** searches the vector store for documents relevant to a question.

<div class="mermaid">
sequenceDiagram
    participant U as 👤 Question
    participant R as 🔍 Retriever
    participant V as 🗄️ Vector Store
    
    U->>R: "What's the vacation policy?"
    R->>R: Convert to embedding
    R->>V: Find similar embeddings
    V-->>R: Top 3 matching chunks
    R-->>U: Return relevant documents
</div>

### Creating a Retriever

```python
# Turn the vector store into a retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Return top 3 matches
)

# Test it
question = "What's the vacation policy?"
relevant_docs = retriever.invoke(question)

for doc in relevant_docs:
    print(doc.page_content)
    print("---")
```

### How Similarity Search Works

<div class="mermaid">
flowchart TB
    Q["❓ Question:<br/>What's the refund policy?"]
    QE["Convert to embedding"]
    
    subgraph vs["🗄️ All Documents"]
        D1["Vacation policy<br/>❌ Not similar"]
        D2["Refund policy<br/>✅ Very similar!"]
        D3["Hiring policy<br/>❌ Not similar"]
        D4["Return process<br/>✅ Similar"]
    end
    
    R["Return top matches"]
    
    Q --> QE --> vs --> R
    
    style Q fill:#dbeafe,stroke:#2563eb
    style QE fill:#fef3c7,stroke:#d97706
    style D2 fill:#d1fae5,stroke:#059669
    style D4 fill:#d1fae5,stroke:#059669
    style R fill:#d1fae5,stroke:#059669
</div>

---

## Step 4: Generation (Putting It Together)

### Creating a RAG Chain

Now we combine everything:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Create the prompt
template = """Answer the question based only on the following context:

Context:
{context}

Question: {question}

Answer: """

prompt = ChatPromptTemplate.from_template(template)

# Create the chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | ChatOpenAI(model="gpt-4")
    | StrOutputParser()
)

# Use it!
answer = rag_chain.invoke("What's our vacation policy?")
print(answer)
```

### How the Chain Works

<div class="mermaid">
sequenceDiagram
    participant U as 👤 User
    participant R as 🔍 Retriever
    participant F as 📋 Format
    participant P as 📝 Prompt
    participant L as 🤖 LLM
    
    U->>R: Question
    R->>F: Relevant documents
    F->>P: Formatted context
    P->>L: Prompt with context + question
    L->>U: Generated answer
</div>

---

## Complete RAG Example

Let's build a complete Q&A system for company policies:

```python
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Step 1: Load all company policy documents
loader = DirectoryLoader(
    "./company_policies",
    glob="**/*.txt"
)
documents = loader.load()

print(f"Loaded {len(documents)} documents")

# Step 2: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
chunks = text_splitter.split_documents(documents)

print(f"Split into {len(chunks)} chunks")

# Step 3: Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# Step 4: Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# Step 5: Create RAG chain
template = """You are a helpful assistant answering questions about company policies.

Use the following context to answer the question. If you can't find the answer in the context, say "I don't have that information in the company policies."

Context:
{context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | ChatOpenAI(model="gpt-4", temperature=0)
    | StrOutputParser()
)

# Step 6: Use it!
questions = [
    "How many vacation days do employees get?",
    "What's the work from home policy?",
    "How do I request time off?"
]

for q in questions:
    print(f"\nQ: {q}")
    print(f"A: {rag_chain.invoke(q)}")
```

---

## Advanced: Adding Citations

### Why Citations Matter

Users should know where answers come from!

<div class="mermaid">
flowchart LR
    subgraph bad["❌ Without Citations"]
        B["Answer: You get 15 days<br/>(Where from?)"]
    end
    
    subgraph good["✅ With Citations"]
        G["Answer: You get 15 days<br/>(Source: Employee Handbook, p.12)"]
    end
    
    style bad fill:#fecaca,stroke:#dc2626
    style good fill:#d1fae5,stroke:#059669
</div>

### Implementing Citations

```python
from langchain_core.runnables import RunnableParallel

# Modified chain that returns both answer and sources
rag_chain_with_sources = RunnableParallel(
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
).assign(
    answer=lambda x: (
        prompt 
        | ChatOpenAI(model="gpt-4") 
        | StrOutputParser()
    ).invoke({
        "context": format_docs(x["context"]),
        "question": x["question"]
    })
)

# Use it
result = rag_chain_with_sources.invoke("What's the vacation policy?")

print("Answer:", result["answer"])
print("\nSources:")
for doc in result["context"]:
    print(f"- {doc.metadata.get('source', 'Unknown')}")
```

---

## Common RAG Patterns

### Pattern 1: Multi-Query

Generate multiple versions of the question for better retrieval:

```python
from langchain.retrievers import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=ChatOpenAI(temperature=0)
)

# This will:
# 1. Generate variations of your question
# 2. Retrieve for each variation
# 3. Combine and deduplicate results
```

### Pattern 2: Contextual Compression

Only keep the most relevant parts of retrieved documents:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(ChatOpenAI())
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)

# Returns shorter, more focused results
```

### Pattern 3: Conversational RAG

Remember chat history:

```python
from langchain.chains import create_history_aware_retriever

# Reformulate questions based on chat history
history_retriever = create_history_aware_retriever(
    llm=ChatOpenAI(),
    retriever=vectorstore.as_retriever(),
    prompt=history_prompt
)

# User: "What's the vacation policy?"
# Bot: "15 days per year"
# User: "Can I roll them over?"  ← Uses history to understand "them" = "vacation days"
```

---

## Best Practices

### 1. Chunk Size Matters

<div class="mermaid">
flowchart TB
    subgraph small["Chunks Too Small"]
        S1["Chunk: 'vacation'"]
        S2["Missing context"]
    end
    
    subgraph large["Chunks Too Large"]
        L1["Chunk: entire handbook"]
        L2["Too much noise"]
    end
    
    subgraph right["Just Right"]
        R1["Chunk: full paragraph<br/>about vacation policy"]
        R2["Complete context"]
    end
    
    style small fill:#fecaca,stroke:#dc2626
    style large fill:#fecaca,stroke:#dc2626
    style right fill:#d1fae5,stroke:#059669
</div>

**Guidelines:**
- General text: 500-1000 characters
- Code: 100-300 lines
- Tables: Keep rows together

### 2. Test Retrieval Quality

Before building the full chain, test your retriever:

```python
# Test if retrieval works
test_questions = [
    "vacation policy",
    "remote work",
    "sick leave"
]

for q in test_questions:
    docs = retriever.invoke(q)
    print(f"Question: {q}")
    print(f"Retrieved {len(docs)} docs")
    print(docs[0].page_content[:200])
    print("---")
```

### 3. Use Appropriate Search Parameters

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 3,  # Return top 3 results
        "score_threshold": 0.7  # Only return if similarity > 0.7
    }
)
```

### 4. Keep Prompt Instructions Clear

```python
template = """Rules:
1. Only answer from the provided context
2. If information isn't in context, say "I don't know"
3. Cite your sources
4. Be concise

Context: {context}
Question: {question}
Answer:"""
```

### 5. Monitor and Improve

Track:
- Questions that fail to find answers
- Low-quality retrievals
- User feedback

---

## Common Issues & Solutions

### Issue 1: Poor Retrieval Quality

**Problem:** Retriever returns irrelevant documents

**Solutions:**
- Adjust chunk size and overlap
- Try different embedding models
- Use metadata filtering
- Implement hybrid search (keyword + semantic)

### Issue 2: Hallucinations

**Problem:** AI makes up answers not in documents

**Solutions:**
- Make prompt more strict
- Lower temperature (0-0.3)
- Add explicit instructions to only use context
- Implement citation requirements

### Issue 3: Slow Performance

**Problem:** Takes too long to answer

**Solutions:**
- Reduce number of retrieved documents (k parameter)
- Use faster embedding models
- Implement caching
- Use local vector stores

---

## RAG Architecture Overview

<div class="mermaid">
flowchart TB
    subgraph ingest["📥 Ingestion (One-Time)"]
        I1["Load Documents"]
        I2["Split Chunks"]
        I3["Create Embeddings"]
        I4["Store in Vector DB"]
        
        I1 --> I2 --> I3 --> I4
    end
    
    subgraph query["❓ Query (Every Request)"]
        Q1["User Question"]
        Q2["Retrieve Relevant Docs"]
        Q3["Generate Answer"]
        
        Q1 --> Q2 --> Q3
    end
    
    I4 -.->|"Data ready"| Q2
    
    style ingest fill:#fef3c7,stroke:#d97706
    style query fill:#d1fae5,stroke:#059669
</div>

---

## What You've Learned

✅ What RAG is and why it's useful  
✅ Loading and splitting documents  
✅ Understanding embeddings and vector stores  
✅ Creating retrievers  
✅ Building complete RAG chains  
✅ Adding citations and advanced features  
✅ Best practices and troubleshooting  

You can now build AI systems that answer questions from your own documents! Next, we'll learn about LangGraph - building complex agentic workflows.

---

## What's Next?

In the next section, we'll learn about **LangGraph & Agents**:
- Building workflows with states and nodes
- Creating agents that can plan and adapt
- Using tools in agentic systems
- Managing complex decision flows

**[→ Continue to Step 5: LangGraph & Agents]({{ site.baseurl }}{% link _topics/langgraph-agents.md %})**

---

## Quick Reference

### Basic RAG Setup

```python
# 1. Load & split
loader = TextLoader("docs.txt")
docs = loader.load()
chunks = text_splitter.split_documents(docs)

# 2. Create vector store
vectorstore = FAISS.from_documents(chunks, embeddings)

# 3. Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 4. Create chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI()
    | StrOutputParser()
)

# 5. Use it
answer = rag_chain.invoke("Your question")
```

Ready to build agents? Let's go! 🚀

**[Next: LangGraph & Agents →]({{ site.baseurl }}{% link _topics/langgraph-agents.md %})**
