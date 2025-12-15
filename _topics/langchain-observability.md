---
title: "Observability with LangSmith: Debug and Monitor Your AI"
category: Generative AI
tags:
  - langsmith
  - debugging
  - monitoring
  - observability
  - tracing
summary: Learn how to use LangSmith to debug, trace, and monitor your AI applications - find issues fast and optimize performance.
related:
  - langchain-project-agent
  - langgraph-agents
---

> **🎓 LangChain Learning Path - Step 7 of 7**
> - **[← Step 6: Build Your Agent Project]({{ site.baseurl }}{% link _topics/langchain-project-agent.md %})**
> - **Step 7 (this page):** Observability with LangSmith
> - **🎉 Course Complete!**

---

## The Problem: AI is a Black Box

When your AI agent doesn't work as expected, it's hard to know why:

<div class="mermaid">
flowchart LR
    Q["❓ User Question"] --> BB["⬛ Black Box<br/>Agent"] --> R["❌ Wrong Answer"]
    
    Note["What happened inside?<br/>- Which tools were called?<br/>- What did the LLM see?<br/>- Where did it go wrong?"]
    
    style BB fill:#fecaca,stroke:#dc2626
    style Note fill:#fef3c7,stroke:#d97706
</div>

**Common problems:**
- Agent uses wrong tool
- LLM hallucinates
- Slow performance
- Unexpected errors
- High costs

**LangSmith solves this by making everything visible!**

---

## What is LangSmith?

**LangSmith** is like a video replay system for your AI - it records every step so you can see exactly what happened.

<div class="mermaid">
flowchart TB
    A["🤖 Your Agent"] --> LS["📹 LangSmith<br/>Records Everything"]
    
    LS --> T["📊 Traces<br/>See each step"]
    LS --> D["🔍 Debugging<br/>Find issues"]
    LS --> P["⚡ Performance<br/>Optimize speed"]
    LS --> C["💰 Costs<br/>Track spending"]
    
    style A fill:#dbeafe,stroke:#2563eb
    style LS fill:#fef3c7,stroke:#d97706
    style T fill:#d1fae5,stroke:#059669
    style D fill:#fce7f3,stroke:#db2777
    style P fill:#e0e7ff,stroke:#6366f1
    style C fill:#fef3c7,stroke:#d97706
</div>

**Real-world analogy:** Like a sports replay - you can see every play, slow it down, and understand what went wrong.

---

## Getting Started

### Step 1: Sign Up

1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Sign up for free account
3. Create a new project

### Step 2: Get API Key

1. Go to Settings → API Keys
2. Create new API key
3. Copy it

### Step 3: Configure Your Code

```bash
# Add to .env file
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=your_project_name
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

# That's it! LangSmith is now tracking your agent
```

---

## Understanding Traces

### What is a Trace?

A **trace** is a complete record of one interaction with your agent.

<div class="mermaid">
flowchart TB
    Start["👤 User: What's the weather?"] --> Trace["📹 Trace Starts"]
    
    Trace --> Step1["🤖 LLM Call 1:<br/>Decides to use tool"]
    Step1 --> Step2["🔧 Tool Call:<br/>get_weather('NYC')"]
    Step2 --> Step3["🤖 LLM Call 2:<br/>Formats answer"]
    Step3 --> End["💬 Response:<br/>It's sunny, 72°F"]
    
    style Trace fill:#fef3c7,stroke:#d97706
    style Step1 fill:#dbeafe,stroke:#2563eb
    style Step2 fill:#fce7f3,stroke:#db2777
    style Step3 fill:#dbeafe,stroke:#2563eb
    style End fill:#d1fae5,stroke:#059669
</div>

Each trace shows:
- **Inputs**: What went in
- **Outputs**: What came out
- **Steps**: Everything in between
- **Timing**: How long each step took
- **Costs**: How much each call cost

---

## Viewing Traces in LangSmith

### The Trace View

When you open a trace, you see a timeline:

```
Trace: "What's the weather in New York?"
├─ 🤖 ChatOpenAI (230ms, $0.002)
│  ├─ Input: "What's the weather in New York?"
│  └─ Output: [calls get_weather tool]
│
├─ 🔧 get_weather (45ms, $0.000)
│  ├─ Input: {"city": "New York"}
│  └─ Output: "Sunny, 72°F"
│
└─ 🤖 ChatOpenAI (180ms, $0.001)
   ├─ Input: [tool result + original question]
   └─ Output: "It's sunny and 72°F in New York!"

Total: 455ms, $0.003
```

### What You Can See

<div class="mermaid">
flowchart LR
    subgraph info["📊 Trace Information"]
        I1["Inputs & Outputs"]
        I2["Token usage"]
        I3["Latency"]
        I4["Costs"]
        I5["Errors"]
    end
    
    style info fill:#d1fae5,stroke:#059669
</div>

---

## Common Debugging Scenarios

### Scenario 1: Agent Uses Wrong Tool

**Problem:** Agent calls `send_email` instead of `search_email`

**How to debug:**

1. Open trace in LangSmith
2. Find the LLM call before tool use
3. Check the **Prompt** tab
4. See what the LLM saw

**What you might find:**
```
Available tools:
- send_email: Send an email    ← Tool description unclear!
- search_email: Find emails

User: "Find my emails from Bob"
```

**Fix:** Improve tool description:
```python
@tool
def search_email(query: str) -> str:
    """
    SEARCH for existing emails (does NOT send).
    Use this to FIND or LOOKUP emails.
    """
```

### Scenario 2: LLM Hallucination

**Problem:** Agent makes up information not in the retrieved documents

**How to debug:**

1. Find the generation step
2. Check the **Context** provided
3. Compare to the output

**Example:**
```
Context provided:
"Employee handbook says: 15 vacation days"

LLM output:
"You get 20 vacation days and unlimited sick leave"
                ↑ Made up!        ↑ Not in context!
```

**Fix:** Add stricter prompt:
```python
prompt = """
CRITICAL: Only use information from the provided context.
If info is not in context, say "I don't have that information."
Do NOT make up or infer information.

Context: {context}
"""
```

### Scenario 3: Slow Performance

**Problem:** Agent takes 10 seconds to respond

**How to debug:**

1. Look at timing for each step
2. Find the bottleneck

**Example trace:**
```
├─ Retrieval (50ms) ✅ Fast
├─ LLM Call 1 (8000ms) ❌ SLOW!
└─ LLM Call 2 (100ms) ✅ Fast

Total: 8150ms
```

**Fix:** Reduce input size for slow LLM call:
```python
# Before: Sending entire document (10,000 tokens)
# After: Send only relevant chunks (500 tokens)
```

### Scenario 4: High Costs

**Problem:** $50 bill for 100 requests

**How to debug:**

1. Click "Analytics" in LangSmith
2. See cost breakdown
3. Find expensive calls

**What you might find:**
```
GPT-4 calls: $45 (10,000 requests with 4,000 tokens each)
GPT-3.5 calls: $5 (1,000 requests)
```

**Fix:** Use cheaper model when possible:
```python
# For simple tasks
cheap_model = ChatOpenAI(model="gpt-3.5-turbo")

# For complex tasks only
expensive_model = ChatOpenAI(model="gpt-4")
```

---

## Monitoring Patterns

### Pattern 1: Testing Changes

Compare before and after:

```python
# Tag your runs
from langsmith import traceable

@traceable(run_type="chain", tags=["version-1"])
def old_chain(input):
    # Old implementation
    pass

@traceable(run_type="chain", tags=["version-2"])
def new_chain(input):
    # New improved implementation
    pass

# In LangSmith, filter by tags and compare metrics
```

### Pattern 2: Quality Monitoring

Track quality metrics:

<div class="mermaid">
flowchart TB
    Prod["🚀 Production Agent"] --> Track["📊 Track Metrics"]
    
    Track --> M1["✅ Success rate"]
    Track --> M2["⏱️ Response time"]
    Track --> M3["💰 Cost per request"]
    Track --> M4["😊 User satisfaction"]
    
    Track --> Alert{"Metrics<br/>drop?"}
    Alert -->|Yes| Notify["🔔 Alert team"]
    
    style Prod fill:#dbeafe,stroke:#2563eb
    style Track fill:#fef3c7,stroke:#d97706
    style Alert fill:#fce7f3,stroke:#db2777
    style Notify fill:#fecaca,stroke:#dc2626
</div>

### Pattern 3: Error Tracking

Automatically detect issues:

```python
from langsmith import Client

client = Client()

# Get failed runs
failed_runs = client.list_runs(
    project_name="my-project",
    filter="error eq true",
    start_time=yesterday
)

for run in failed_runs:
    print(f"Error: {run.error}")
    print(f"Input: {run.inputs}")
    # Alert or fix automatically
```

---

## Advanced Features

### 1. Datasets & Testing

Create test sets to ensure quality:

```python
from langsmith import Client

client = Client()

# Create dataset
dataset = client.create_dataset("customer-service-tests")

# Add examples
client.create_examples(
    dataset_id=dataset.id,
    inputs=[
        {"question": "What's my order status?"},
        {"question": "How do I return an item?"},
    ],
    outputs=[
        {"should_use_tool": "check_order"},
        {"should_use_tool": "return_policy"},
    ]
)

# Run tests
def test_agent():
    for example in dataset.examples:
        result = agent.invoke(example.inputs)
        # Validate result matches expected output
```

### 2. Feedback & Ratings

Collect user feedback:

```python
from langsmith import Client

client = Client()

# User gives feedback
client.create_feedback(
    run_id=run_id,
    key="helpfulness",
    score=5,  # 1-5 stars
    comment="Very helpful!"
)

# View feedback in LangSmith dashboard
```

### 3. Playground Testing

Test prompts interactively:

1. Go to LangSmith Playground
2. Paste your prompt
3. Try different inputs
4. See results immediately
5. Compare versions side-by-side

---

## Real-World Example

Let's add full observability to our Research Assistant:

```python
import os
from dotenv import load_dotenv
from langsmith import traceable
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Enable tracing
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "research-assistant"

# Tools with better descriptions for debugging
@traceable(name="web_search_tool")
def web_search(query: str) -> str:
    """
    Search the web for information.
    
    WHEN TO USE: User asks about current info, facts, or research topics.
    DO NOT USE: For personal info, past conversations, or saved notes.
    """
    # Implementation
    pass

@traceable(name="save_notes_tool")
def save_notes(content: str, title: str) -> str:
    """
    Save research findings to notes.
    
    WHEN TO USE: After finding important information worth remembering.
    DO NOT USE: For every small detail.
    """
    # Implementation
    pass

# Create agent with metadata
agent = create_react_agent(
    ChatOpenAI(model="gpt-4"),
    tools=[web_search, save_notes],
    state_modifier="You are a research assistant..."
)

# Track user sessions
@traceable(
    run_type="chain",
    name="research_session",
    tags=["production", "v2.0"]
)
def handle_user_query(user_id: str, query: str):
    """Handle user query with full tracing."""
    
    config = {
        "configurable": {"thread_id": user_id},
        "metadata": {
            "user_id": user_id,
            "environment": "production"
        },
        "tags": ["user_query"]
    }
    
    result = agent.invoke({"messages": [("user", query)]}, config)
    
    return result["messages"][-1].content

# Use it
response = handle_user_query("user_123", "Research quantum computing")
```

**What you get in LangSmith:**

```
Session: research_session
├─ Metadata: user_id=user_123, environment=production
├─ Tags: production, v2.0, user_query
│
├─ 🔧 web_search_tool (234ms, $0.000)
│  └─ Output: "Quantum computing uses..."
│
├─ 🤖 ChatOpenAI (890ms, $0.005)
│  └─ Decides to save notes
│
└─ 🔧 save_notes_tool (45ms, $0.000)
   └─ Saved: "Quantum Computing Basics"

Total: 1169ms, $0.005
✅ Success
```

---

## Best Practices

### 1. Add Meaningful Tags

```python
tags = [
    "environment:production",
    "user_type:premium",
    "feature:research",
    "version:2.1"
]
```

### 2. Include Metadata

```python
metadata = {
    "user_id": "12345",
    "session_id": "abc",
    "feature_flags": ["new_ui"],
    "model_version": "gpt-4"
}
```

### 3. Name Your Traces

```python
@traceable(name="generate_report", run_type="chain")
def generate_report(data):
    # Clear name in dashboard
    pass
```

### 4. Monitor Key Metrics

Set up alerts for:
- Error rate > 5%
- Average latency > 2s
- Cost per request > $0.10
- Success rate < 95%

### 5. Regular Reviews

Weekly:
- Check failed runs
- Review slow traces
- Analyze cost trends
- Read user feedback

---

## Troubleshooting Tips

### Traces Not Showing Up?

Check:
```python
# 1. Environment variables set?
print(os.getenv("LANGCHAIN_TRACING_V2"))  # Should be "true"
print(os.getenv("LANGCHAIN_API_KEY"))     # Should have value

# 2. Internet connection working?

# 3. Project name correct?
print(os.getenv("LANGCHAIN_PROJECT"))

# 4. Try manual trace
from langsmith import Client
client = Client()
client.create_run(...)  # Test connection
```

### Too Many Traces?

Filter traces:
```python
# Only trace in development
if os.getenv("ENVIRONMENT") == "development":
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
```

### Need to Hide Sensitive Data?

```python
@traceable(name="process_payment", 
          hide_inputs=True,   # Don't log input
          hide_outputs=True)  # Don't log output
def process_payment(card_number, cvv):
    # Sensitive operation
    pass
```

---

## The Debugging Workflow

<div class="mermaid">
flowchart TB
    Issue["🐛 Issue Reported"] --> Find["🔍 Find Trace<br/>in LangSmith"]
    Find --> Analyze["📊 Analyze Steps"]
    Analyze --> Root["🎯 Find Root Cause"]
    Root --> Fix["🔧 Fix Code"]
    Fix --> Test["✅ Test with<br/>Same Input"]
    Test --> Verify["📹 Compare<br/>New Trace"]
    Verify --> Deploy["🚀 Deploy Fix"]
    
    style Issue fill:#fecaca,stroke:#dc2626
    style Find fill:#fef3c7,stroke:#d97706
    style Analyze fill:#dbeafe,stroke:#2563eb
    style Root fill:#fce7f3,stroke:#db2777
    style Fix fill:#d1fae5,stroke:#059669
    style Deploy fill:#d1fae5,stroke:#059669
</div>

---

## What You've Learned

✅ Why observability matters for AI  
✅ Setting up LangSmith  
✅ Reading and understanding traces  
✅ Debugging common issues  
✅ Monitoring production systems  
✅ Testing and quality assurance  
✅ Best practices for tracing  

You now have the tools to build, debug, and monitor production AI systems!

---

## 🎉 Congratulations!

You've completed the LangChain Learning Path! You now know:

1. **Foundations** - LLM orchestration concepts
2. **Essentials** - Chat models, prompting, LCEL
3. **Tool Calling** - Extending LLMs with capabilities
4. **RAG** - Teaching AI about your documents
5. **LangGraph** - Building complex agent workflows
6. **Projects** - Building complete applications
7. **Observability** - Debugging and monitoring

### What's Next?

- **Build your own projects** using what you've learned
- **Explore advanced patterns** in the LangChain docs
- **Join the community** on Discord
- **Share your creations** on GitHub

---

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith Blog](https://blog.langchain.dev/tag/langsmith/)
- [Best Practices Guide](https://docs.smith.langchain.com/concepts/tracing#best-practices)
- [LangChain Community](https://discord.gg/langchain)

---

## Keep Learning

**More Topics to Explore:**
- Advanced prompting techniques
- Multi-modal AI (images, audio)
- Fine-tuning custom models
- Scaling to production
- Security and privacy

**Other Resources:**
- **[← Back to Foundations]({{ site.baseurl }}{% link _topics/langchain-foundations.md %})** to review
- Explore other topics in the handbook
- Try building your own agent variations

---

**Thank you for learning with us!** 🚀

Now go build amazing AI applications! 🎯
