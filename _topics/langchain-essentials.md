---
title: "Part 2 - LangChain Essentials: Building Blocks of AI Applications"
category: Generative AI
order: 2
tags:
  - langchain
  - chat-models
  - prompting
  - lcel
summary: Learn the core LangChain building blocks - chat models, prompting patterns, structured outputs, and chaining - explained simply.
related:
  - langchain-foundations
  - langchain-tool-calling
---

> **🎓 LangChain Learning Path - Step 2 of 7**
> - **[← Step 1: Foundations]({{ site.baseurl }}{% link _topics/langchain-foundations.md %})**
> - **Step 2 (this page):** LangChain Essentials
> - **[Step 3: Tool Calling →]({{ site.baseurl }}{% link _topics/langchain-tool-calling.md %})**

---

## What You'll Learn

In this guide, we'll cover the four essential building blocks of LangChain:

<div class="mermaid">
flowchart LR
    CM["🤖 Chat Models"]
    PP["💬 Prompting Patterns"]
    SO["📊 Structured Outputs"]
    CH["🔗 Chaining (LCEL)"]
    
    CM --> PP --> SO --> CH
    
    style CM fill:#dbeafe,stroke:#2563eb
    style PP fill:#fef3c7,stroke:#d97706
    style SO fill:#fce7f3,stroke:#db2777
    style CH fill:#d1fae5,stroke:#059669
</div>

By the end, you'll be able to build your first LangChain application!

---

## Part 1: Chat Models

### What is a Chat Model?

A **chat model** is like having a conversation partner that responds to messages. Unlike older "completion" models that just continue text, chat models understand **roles** and **conversation flow**.

<div class="mermaid">
sequenceDiagram
    participant Y as 👤 You
    participant C as 🤖 Chat Model
    
    Y->>C: System: You are a helpful teacher
    Y->>C: User: Explain gravity
    C-->>Y: Assistant: Gravity is the force that pulls objects...
    Y->>C: User: Can you give an example?
    C-->>Y: Assistant: Sure! When you drop a ball...
</div>

### The Three Roles

<div class="mermaid">
flowchart TB
    subgraph roles["💬 Message Roles"]
        S["👨‍🏫 System<br/>Sets behavior & context"]
        U["👤 User<br/>Your questions/requests"]
        A["🤖 Assistant<br/>Model's responses"]
    end
    
    style S fill:#dbeafe,stroke:#2563eb
    style U fill:#fef3c7,stroke:#d97706
    style A fill:#d1fae5,stroke:#059669
</div>

| Role | Purpose | Example |
|------|---------|---------|
| **System** | Gives the AI its instructions and personality | "You are a friendly teacher" |
| **User** | Your questions or requests | "How does photosynthesis work?" |
| **Assistant** | The AI's responses | "Photosynthesis is the process..." |

### Using Chat Models in LangChain

```python
from langchain_openai import ChatOpenAI

# Create a chat model
chat = ChatOpenAI(model="gpt-4", temperature=0.7)

# Send a message
response = chat.invoke("Explain quantum physics in simple terms")
print(response.content)
```

**Output:**
```
Think of quantum physics like a magic show where particles can be 
in two places at once and instantly know what each other are doing, 
even from far away...
```

### Temperature: Creativity Control

The **temperature** setting controls how creative or predictable the model is:

<div class="mermaid">
flowchart LR
    subgraph low["🎯 Temperature = 0"]
        L1["Predictable"]
        L2["Consistent"]
        L3["Factual"]
    end
    
    subgraph mid["⚖️ Temperature = 0.7"]
        M1["Balanced"]
        M2["Creative but sensible"]
    end
    
    subgraph high["🎨 Temperature = 1.5"]
        H1["Very creative"]
        H2["Unpredictable"]
        H3["Experimental"]
    end
    
    style low fill:#dbeafe,stroke:#2563eb
    style mid fill:#fef3c7,stroke:#d97706
    style high fill:#fce7f3,stroke:#db2777
</div>

**When to use what:**
- `0.0` - Math problems, factual answers, consistent outputs
- `0.7` - General conversation, balanced creativity
- `1.5+` - Creative writing, brainstorming, experimental ideas

---

## Part 2: Prompting Patterns

### What is a Prompt?

A **prompt** is how you talk to the AI. Good prompts get good results. Bad prompts get confusing results!

### The Anatomy of a Good Prompt

<div class="mermaid">
flowchart TB
    P["📝 Complete Prompt"]
    
    P --> R["🎭 Role<br/>Who should the AI be?"]
    P --> C["🎯 Context<br/>What background info?"]
    P --> T["✅ Task<br/>What to do?"]
    P --> F["📊 Format<br/>How to structure output?"]
    
    style P fill:#dbeafe,stroke:#2563eb
    style R fill:#fef3c7,stroke:#d97706
    style C fill:#fce7f3,stroke:#db2777
    style T fill:#d1fae5,stroke:#059669
</div>

### Pattern 1: Role-Based Prompting

Give the AI a specific role to play:

```python
from langchain.prompts import ChatPromptTemplate

# Define a role-based prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful teacher explaining concepts to a 10-year-old."),
    ("user", "{question}")
])

# Use it
chain = prompt | chat
response = chain.invoke({"question": "What is DNA?"})
```

**Why it works:**
- Gives the AI a clear perspective
- Makes tone and complexity consistent
- Helps it know what NOT to do

### Pattern 2: Few-Shot Prompting

Show the AI examples of what you want:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sentiment analyzer."),
    ("user", "Review: This movie was amazing! → Sentiment: Positive"),
    ("user", "Review: Terrible waste of time → Sentiment: Negative"),
    ("user", "Review: {review} → Sentiment:")
])
```

<div class="mermaid">
flowchart LR
    subgraph examples["📚 Examples"]
        E1["Example 1"]
        E2["Example 2"]
        E3["Example 3"]
    end
    
    subgraph new["❓ New Input"]
        N["Your actual task"]
    end
    
    subgraph ai["🤖 AI"]
        A["Understands pattern<br/>from examples"]
    end
    
    examples --> ai
    new --> ai
    
    style examples fill:#fef3c7,stroke:#d97706
    style new fill:#dbeafe,stroke:#2563eb
    style ai fill:#d1fae5,stroke:#059669
</div>

### Pattern 3: Chain-of-Thought

Ask the AI to think step-by-step:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math tutor. Show your work step by step."),
    ("user", """
    Solve this problem step-by-step:
    
    Problem: {problem}
    
    Think through it:
    1. First...
    2. Then...
    3. Finally...
    """)
])
```

**Why it works:**
- Reduces errors in complex tasks
- Makes reasoning visible
- Better results on math and logic

### Pattern 4: Output Format Control

Tell the AI exactly how to format its response:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You extract company information from text.
    Always respond in this format:
    
    Company Name: [name]
    Industry: [industry]
    Founded: [year]
    """),
    ("user", "{text}")
])
```

---

## Part 3: Structured Outputs

### The Problem with Free Text

When you ask an AI a question, it gives you text. But what if you need **data** you can use in your code?

<div class="mermaid">
flowchart TB
    subgraph problem["❌ Free Text Output"]
        P1["User: What's the weather?"]
        P2["AI: It's 72 degrees and sunny!"]
        P3["Your code: ??? How to extract 72?"]
    end
    
    subgraph solution["✅ Structured Output"]
        S1["User: What's the weather?"]
        S2["AI: temperature=72, condition='sunny'"]
        S3["Your code: weather.temperature → 72"]
    end
    
    style problem fill:#fecaca,stroke:#dc2626
    style solution fill:#d1fae5,stroke:#059669
</div>

### Using Pydantic Models

Pydantic lets you define the structure you want:

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# Define the structure
class Person(BaseModel):
    name: str = Field(description="Person's full name")
    age: int = Field(description="Person's age in years")
    occupation: str = Field(description="Person's job")

# Create a chat model with structured output
llm = ChatOpenAI(model="gpt-4")
structured_llm = llm.with_structured_output(Person)

# Use it
text = "John Smith is a 35-year-old software engineer"
person = structured_llm.invoke(f"Extract person info from: {text}")

print(person.name)        # "John Smith"
print(person.age)         # 35
print(person.occupation)  # "software engineer"
```

### Real-World Example: Invoice Extraction

```python
class Invoice(BaseModel):
    invoice_number: str
    date: str
    vendor: str
    total_amount: float
    items: list[str]

structured_llm = llm.with_structured_output(Invoice)

invoice_text = """
Invoice #INV-2024-001
Date: January 15, 2024
From: Acme Corp
Items: Office supplies, Printer paper, Pens
Total: $247.50
"""

invoice = structured_llm.invoke(f"Extract invoice data from:\n{invoice_text}")

# Now you have structured data!
print(f"Invoice: {invoice.invoice_number}")
print(f"Total: ${invoice.total_amount}")
```

---

## Part 4: Chaining with LCEL

### What is LCEL?

**LCEL (LangChain Expression Language)** is a way to connect multiple steps together using the `|` (pipe) operator.

Think of it like a **factory assembly line** where each step does one thing:

<div class="mermaid">
flowchart LR
    I["📥 Input"] -->|pipe| S1["Step 1"]
    S1 -->|pipe| S2["Step 2"]
    S2 -->|pipe| S3["Step 3"]
    S3 -->|pipe| O["📤 Output"]
    
    style I fill:#dbeafe,stroke:#2563eb
    style S1 fill:#fef3c7,stroke:#d97706
    style S2 fill:#fef3c7,stroke:#d97706
    style S3 fill:#fef3c7,stroke:#d97706
    style O fill:#d1fae5,stroke:#059669
</div>

### Simple Chain Example

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Create a prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{question}")
])

# Step 2: Create a model
model = ChatOpenAI()

# Step 3: Create an output parser
parser = StrOutputParser()

# Chain them together!
chain = prompt | model | parser

# Use the chain
result = chain.invoke({"question": "What is 2+2?"})
print(result)  # "2+2 equals 4"
```

### How the Chain Works

<div class="mermaid">
sequenceDiagram
    participant I as 📥 Input
    participant P as 📝 Prompt
    participant M as 🤖 Model
    participant O as 📤 Parser
    
    I->>P: {question: "What is 2+2?"}
    P->>M: Formatted prompt
    M->>O: AI response object
    O->>I: Clean string: "4"
</div>

### Multi-Step Chain Example

Let's build a chain that:
1. Takes a topic
2. Generates a poem about it
3. Translates it to Spanish

```python
# Step 1: Generate poem
poem_prompt = ChatPromptTemplate.from_template(
    "Write a short 2-line poem about {topic}"
)

# Step 2: Translate
translate_prompt = ChatPromptTemplate.from_template(
    "Translate this to Spanish: {poem}"
)

# Create the chain
chain = (
    {"poem": poem_prompt | model | StrOutputParser()}
    | translate_prompt
    | model
    | StrOutputParser()
)

# Use it
result = chain.invoke({"topic": "mountains"})
print(result)
```

**Flow:**
```
Topic: "mountains"
    ↓
Generate poem: "Mountains high and peaks so grand..."
    ↓
Translate: "Montañas altas y picos tan grandes..."
```

### Parallel Chains

You can run multiple chains at the same time:

```python
from langchain_core.runnables import RunnableParallel

# Define multiple chains
summary_chain = summary_prompt | model | StrOutputParser()
sentiment_chain = sentiment_prompt | model | StrOutputParser()
keywords_chain = keywords_prompt | model | StrOutputParser()

# Run them in parallel
parallel_chain = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain,
    keywords=keywords_chain
)

result = parallel_chain.invoke({"text": "Your article here..."})
print(result["summary"])
print(result["sentiment"])
print(result["keywords"])
```

<div class="mermaid">
flowchart TB
    I["📥 Input Text"]
    
    I --> C1["Chain 1: Summary"]
    I --> C2["Chain 2: Sentiment"]
    I --> C3["Chain 3: Keywords"]
    
    C1 --> O["📤 Combined Results"]
    C2 --> O
    C3 --> O
    
    style I fill:#dbeafe,stroke:#2563eb
    style C1 fill:#fef3c7,stroke:#d97706
    style C2 fill:#fef3c7,stroke:#d97706
    style C3 fill:#fef3c7,stroke:#d97706
    style O fill:#d1fae5,stroke:#059669
</div>

---

## Putting It All Together: A Complete Example

Let's build a **Product Review Analyzer** that:
1. Extracts structured data from reviews
2. Analyzes sentiment
3. Generates a summary

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

# Step 1: Define structure
class ReviewData(BaseModel):
    product: str = Field(description="Product name")
    rating: int = Field(description="Rating 1-5")
    pros: list[str] = Field(description="Positive points")
    cons: list[str] = Field(description="Negative points")

# Step 2: Create extraction chain
extraction_llm = ChatOpenAI(model="gpt-4").with_structured_output(ReviewData)

# Step 3: Create summary chain
summary_prompt = ChatPromptTemplate.from_template(
    "Summarize this review in one sentence: {review}"
)
summary_chain = summary_prompt | ChatOpenAI() | StrOutputParser()

# Step 4: Combine everything
from langchain_core.runnables import RunnableParallel

full_chain = RunnableParallel(
    data=extraction_llm,
    summary=summary_chain
)

# Use it!
review = """
I bought the SuperWidget 3000 and I'm impressed! The build quality 
is amazing and it's very easy to use. However, the battery life 
could be better and it's a bit expensive. Overall, I'd give it 4/5 stars.
"""

result = full_chain.invoke(review)

print("Product:", result["data"].product)
print("Rating:", result["data"].rating)
print("Pros:", result["data"].pros)
print("Cons:", result["data"].cons)
print("Summary:", result["summary"])
```

**Output:**
```
Product: SuperWidget 3000
Rating: 4
Pros: ['Amazing build quality', 'Easy to use']
Cons: ['Battery life could be better', 'A bit expensive']
Summary: A high-quality, user-friendly product with minor drawbacks in battery and price.
```

---

## Best Practices

### 1. Start Simple, Then Chain

<div class="mermaid">
flowchart LR
    A["Test each step<br/>separately"] --> B["Combine into<br/>simple chain"]
    B --> C["Add complexity<br/>gradually"]
    
    style A fill:#dbeafe,stroke:#2563eb
    style B fill:#fef3c7,stroke:#d97706
    style C fill:#d1fae5,stroke:#059669
</div>

### 2. Be Specific in Prompts

❌ Bad: "Analyze this"  
✅ Good: "Extract the key findings and sentiment from this research paper"

### 3. Use Structured Outputs When Possible

Text is flexible but hard to use in code. Structured data is easier to work with.

### 4. Control Temperature Based on Task

| Task Type | Temperature |
|-----------|-------------|
| Extract data | 0.0 |
| Answer questions | 0.3 |
| Have conversation | 0.7 |
| Generate creative content | 1.0+ |

### 5. Test with Edge Cases

- Empty inputs
- Very long inputs
- Unusual formatting
- Multiple languages

---

## Common Patterns Recap

### The Building Blocks

```python
# 1. Chat Model
chat = ChatOpenAI(model="gpt-4", temperature=0.7)

# 2. Prompt Template
prompt = ChatPromptTemplate.from_messages([...])

# 3. Output Parser
parser = StrOutputParser()

# 4. Chain them
chain = prompt | chat | parser
```

### The LCEL Operators

| Operator | What It Does | Example |
|----------|--------------|---------|
| `\|` (pipe) | Connect steps sequentially | `prompt \| model \| parser` |
| `RunnableParallel` | Run steps in parallel | `{a: chain1, b: chain2}` |
| `RunnableLambda` | Add custom functions | `RunnableLambda(my_function)` |

---

## What You've Learned

✅ How to use **chat models** with different roles  
✅ **Prompting patterns** that get better results  
✅ Creating **structured outputs** with Pydantic  
✅ **Chaining** components together with LCEL  

You now have the core building blocks! Next, we'll learn how to give your AI **superpowers** by connecting it to tools and APIs.

---

## What's Next?

In the next section, we'll learn about **Tool Calling** - how to let your LLM:
- Search the web
- Query databases
- Send emails
- Call APIs
- And much more!

**[→ Continue to Step 3: Tool Calling]({{ site.baseurl }}{% link _topics/langchain-tool-calling.md %})**

---

## Quick Reference

### Essential Imports

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from pydantic import BaseModel, Field
```

### Basic Chain Template

```python
# Define
prompt = ChatPromptTemplate.from_messages([...])
model = ChatOpenAI()
parser = StrOutputParser()

# Chain
chain = prompt | model | parser

# Use
result = chain.invoke({"input": "..."})
```

Ready to give your AI superpowers? Let's learn about tools! 🚀

**[Next: Tool Calling →]({{ site.baseurl }}{% link _topics/langchain-tool-calling.md %})**
