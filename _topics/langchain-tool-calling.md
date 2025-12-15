---
title: "Part 3 - Tool Calling: Giving Your AI Real-World Superpowers"
category: Generative AI
order: 3
tags:
  - langchain
  - tools
  - function-calling
  - mcp
  - apis
summary: Learn how to extend LLMs with real-world capabilities - from calling APIs to using MCP adapters - explained in simple terms.
related:
  - langchain-essentials
  - langchain-rag-basics
---

> **🎓 LangChain Learning Path - Step 3 of 7**
> - **[← Step 2: LangChain Essentials]({{ site.baseurl }}{% link _topics/langchain-essentials.md %})**
> - **Step 3 (this page):** Tool Calling
> - **[Step 4: RAG Basics →]({{ site.baseurl }}{% link _topics/langchain-rag-basics.md %})**

> **📓 Hands-On Practice**  
> **[⬇️ Download Jupyter Notebook]({{ site.baseurl }}/notebooks/part3-tool-calling.ipynb)** - Create custom tools and build agents with runnable code examples.

---

## The Problem: LLMs Can't DO Things

Remember from our foundations: LLMs are like super-smart people who have read everything but can't interact with the world.

<div class="mermaid">
flowchart LR
    subgraph cant["❌ LLM Alone"]
        L1["🤖 LLM"]
        N1["Can only generate text"]
        N2["No real-world access"]
    end
    
    subgraph can["✅ LLM + Tools"]
        L2["🤖 LLM"]
        T["🔧 Tools"]
        A1["Can check weather"]
        A2["Can send emails"]
        A3["Can query databases"]
    end
    
    style cant fill:#fecaca,stroke:#dc2626
    style can fill:#d1fae5,stroke:#059669
</div>

**This is where Tool Calling comes in!**

---

## What is Tool Calling?

### The Simple Explanation

**Tool calling** is like giving your AI a toolbox and teaching it when and how to use each tool.

<div class="mermaid">
flowchart TB
    U["👤 User: What's the weather in NYC?"]
    A["🤖 AI thinks..."]
    A --> D{"Do I know this?"}
    D -->|No| T["🔧 Use weather tool"]
    T --> G["🌐 Get real data"]
    G --> R["📝 Generate answer with data"]
    D -->|Yes| R
    
    style U fill:#dbeafe,stroke:#2563eb
    style T fill:#fef3c7,stroke:#d97706
    style G fill:#fce7f3,stroke:#db2777
    style R fill:#d1fae5,stroke:#059669
</div>

### Real-World Analogy

Imagine you're helping someone over the phone:

**Without tools:**
```
Them: "What's my account balance?"
You: "I don't have access to that information."
```

**With tools:**
```
Them: "What's my account balance?"
You: (checks the computer system)
You: "Your balance is $1,234.56"
```

The AI + Tools work the same way!

---

## How Tool Calling Works

### The Process

<div class="mermaid">
sequenceDiagram
    participant U as 👤 User
    participant AI as 🤖 LLM
    participant TC as 🎯 Tool Controller
    participant T as 🔧 Tool
    
    U->>AI: "What's the weather in Paris?"
    AI->>TC: I need to call: get_weather("Paris")
    TC->>T: Execute get_weather("Paris")
    T-->>TC: {temp: 72, condition: "sunny"}
    TC-->>AI: Here's the data
    AI-->>U: "It's 72°F and sunny in Paris!"
</div>

### The Three Steps

1. **Tool Discovery**: AI knows what tools are available
2. **Tool Selection**: AI decides which tool to use
3. **Tool Execution**: The tool runs and returns data

---

## Creating Your First Tool

### Simple Function as a Tool

```python
from langchain.tools import tool

@tool
def get_current_time() -> str:
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%I:%M %p")

# The AI now knows about this tool!
print(get_current_time.name)  # "get_current_time"
print(get_current_time.description)  # "Get the current time."
```

### Why the Docstring Matters

The **docstring** (`"""text"""`) is crucial! It tells the AI:
- What the tool does
- When to use it
- What parameters it needs

<div class="mermaid">
flowchart LR
    DS["📝 Docstring"] --> AI["🤖 AI reads it"]
    AI --> D["🤔 Decides when<br/>to use tool"]
    
    style DS fill:#fef3c7,stroke:#d97706
    style AI fill:#dbeafe,stroke:#2563eb
    style D fill:#d1fae5,stroke:#059669
</div>

**Good docstrings:**
```python
@tool
def search_products(query: str, max_results: int = 5) -> list:
    """
    Search for products in the database.
    
    Args:
        query: The search term (e.g., "laptop", "shoes")
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        List of matching products with name and price
    """
    # ... implementation
```

---

## Common Tool Patterns

### Pattern 1: API Wrapper Tool

Wrap an external API call:

```python
import requests
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    Get current weather for a city.
    
    Args:
        city: Name of the city (e.g., "New York", "London")
    """
    # Call weather API
    response = requests.get(
        f"https://api.weather.com/v1/current",
        params={"city": city}
    )
    data = response.json()
    
    return f"Temperature: {data['temp']}°F, Conditions: {data['conditions']}"
```

### Pattern 2: Database Query Tool

```python
@tool
def search_customers(name: str) -> str:
    """
    Search for customers by name in the database.
    
    Args:
        name: Customer name to search for
    """
    import sqlite3
    
    conn = sqlite3.connect('customers.db')
    cursor = conn.execute(
        "SELECT * FROM customers WHERE name LIKE ?",
        (f"%{name}%",)
    )
    results = cursor.fetchall()
    
    if not results:
        return "No customers found"
    
    return f"Found {len(results)} customers: {results}"
```

### Pattern 3: Calculator Tool

```python
@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: Math expression like "2 + 2" or "sqrt(16)"
        
    Example: calculate("10 * 5 + 2")
    """
    try:
        # Safe evaluation
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

---

## Using Tools with LangChain

### Binding Tools to a Model

```python
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# Define tools
@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 75°F"

@tool
def get_time() -> str:
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%I:%M %p")

# Create model and bind tools
model = ChatOpenAI(model="gpt-4")
model_with_tools = model.bind_tools([get_weather, get_time])

# Use it
response = model_with_tools.invoke("What's the weather in Seattle?")
```

### The AI Decides Which Tool to Use

<div class="mermaid">
flowchart TD
    Q1["User: What time is it?"]
    Q2["User: What's the weather?"]
    Q3["User: What's 2+2?"]
    
    AI["🤖 AI Analyzes"]
    
    Q1 --> AI
    Q2 --> AI
    Q3 --> AI
    
    AI --> T1["Use: get_time()"]
    AI --> T2["Use: get_weather()"]
    AI --> T3["No tool needed"]
    
    style AI fill:#fef3c7,stroke:#d97706
    style T1 fill:#d1fae5,stroke:#059669
    style T2 fill:#d1fae5,stroke:#059669
    style T3 fill:#dbeafe,stroke:#2563eb
</div>

---

## Building a Tool-Using Agent

### Creating an Agent

An **agent** is an AI system that can:
1. Understand your request
2. Decide which tools to use
3. Use multiple tools if needed
4. Combine results into an answer

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate

# Define tools
@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 72°F"

@tool
def get_population(city: str) -> str:
    """Get population of a city."""
    return f"Population of {city}: 8.3 million"

tools = [get_weather, get_population]

# Create agent prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Create agent
llm = ChatOpenAI(model="gpt-4")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Use it
response = agent_executor.invoke({
    "input": "What's the weather and population of New York?"
})

print(response["output"])
```

**What happens:**
```
Thought: I need to get both weather and population
Action: get_weather("New York")
Observation: Weather in New York: Sunny, 72°F
Action: get_population("New York")
Observation: Population of New York: 8.3 million
Thought: I have all the information
Answer: New York has sunny weather at 72°F and a population of 8.3 million.
```

---

## Advanced: MCP (Model Context Protocol)

### What is MCP?

**MCP (Model Context Protocol)** is a standard way for AI models to connect to tools and data sources. Think of it as USB-C for AI - one standard that works everywhere!

<div class="mermaid">
flowchart TB
    subgraph old["❌ Before MCP"]
        A1["Custom adapter"]
        A2["Custom adapter"]
        A3["Custom adapter"]
    end
    
    subgraph new["✅ With MCP"]
        M["Standard MCP Interface"]
        T1["Any tool"]
        T2["Any database"]
        T3["Any API"]
    end
    
    old --> new
    
    style old fill:#fecaca,stroke:#dc2626
    style new fill:#d1fae5,stroke:#059669
</div>

### Using MCP in LangChain

```python
from langchain.tools import MCPAdapter

# Connect to any MCP-compatible tool
weather_tool = MCPAdapter(
    name="weather",
    mcp_server="https://mcp.weather.com",
    description="Get weather information"
)

# Use it like any other tool
model_with_tools = model.bind_tools([weather_tool])
```

### Why MCP Matters

| Without MCP | With MCP |
|-------------|----------|
| Write custom code for each tool | Use standard interface |
| Breaks when tools update | Automatically compatible |
| Hard to share tools | Tools work everywhere |
| Limited to specific frameworks | Framework-agnostic |

---

## Real-World Example: Customer Service Bot

Let's build a bot that can:
- Check order status
- Look up customer info
- Process refunds

```python
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate

# Define tools
@tool
def check_order_status(order_id: str) -> str:
    """
    Check the status of an order.
    
    Args:
        order_id: The order ID (e.g., "ORD-12345")
    """
    # Simulate database lookup
    orders = {
        "ORD-12345": "Shipped - Arriving Tuesday",
        "ORD-67890": "Processing - Will ship tomorrow"
    }
    return orders.get(order_id, "Order not found")

@tool
def get_customer_info(email: str) -> str:
    """
    Get customer information by email.
    
    Args:
        email: Customer's email address
    """
    # Simulate database lookup
    customers = {
        "john@example.com": "John Smith, Premium Member since 2020",
        "jane@example.com": "Jane Doe, Standard Member since 2023"
    }
    return customers.get(email, "Customer not found")

@tool
def process_refund(order_id: str, reason: str) -> str:
    """
    Process a refund for an order.
    
    Args:
        order_id: The order ID to refund
        reason: Reason for the refund
    """
    # Simulate refund processing
    return f"Refund processed for {order_id}. Reason: {reason}. Amount will be credited in 3-5 days."

# Create agent
tools = [check_order_status, get_customer_info, process_refund]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful customer service agent. 
    You can check orders, look up customer info, and process refunds.
    Always be polite and helpful."""),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Test it
print(agent_executor.invoke({
    "input": "Hi, I'm john@example.com and I want to know about order ORD-12345"
})["output"])
```

**Output:**
```
Hello! I found your account - you're John Smith, a Premium Member since 2020.
Your order ORD-12345 has been shipped and should arrive on Tuesday!
Is there anything else I can help you with?
```

---

## Best Practices

### 1. Write Clear Tool Descriptions

<div class="mermaid">
flowchart LR
    subgraph bad["❌ Bad"]
        B["def search(q): ..."<br/>No description!"]
    end
    
    subgraph good["✅ Good"]
        G["def search(query: str):<br/>\"\"\"Search products<br/>by name or keyword\"\"\""]
    end
    
    style bad fill:#fecaca,stroke:#dc2626
    style good fill:#d1fae5,stroke:#059669
</div>

### 2. Keep Tools Focused

Each tool should do **one thing well**:

❌ Bad: `manage_order()` - too broad  
✅ Good: `check_order_status()`, `cancel_order()`, `update_address()`

### 3. Handle Errors Gracefully

```python
@tool
def get_stock_price(ticker: str) -> str:
    """Get current stock price."""
    try:
        # API call
        price = fetch_price(ticker)
        return f"{ticker}: ${price}"
    except Exception as e:
        return f"Could not fetch price for {ticker}. Error: {str(e)}"
```

### 4. Use Type Hints

Type hints help the AI understand what data to provide:

```python
@tool
def schedule_meeting(
    title: str,
    date: str,
    duration_minutes: int,
    attendees: list[str]
) -> str:
    """Schedule a meeting."""
    # Implementation
```

### 5. Test Tools Independently

Before giving tools to the AI, test them yourself:

```python
# Test the tool directly
result = get_weather("London")
print(result)  # Make sure it works!

# Then give to AI
model_with_tools = model.bind_tools([get_weather])
```

---

## Common Tool Categories

### 1. Information Retrieval
- Search databases
- Query APIs
- Read files
- Web search

### 2. Data Manipulation
- Calculate numbers
- Transform data
- Generate reports
- Parse documents

### 3. External Actions
- Send emails
- Post to social media
- Create calendar events
- Make purchases

### 4. System Integration
- Database operations
- File system access
- API calls
- Service integrations

---

## Debugging Tools

### Enable Verbose Mode

See what the agent is doing:

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # Shows agent's thinking!
)
```

**Output:**
```
> Entering new AgentExecutor chain...

Thought: I need to check the weather
Action: get_weather
Action Input: {'city': 'Boston'}
Observation: Weather in Boston: Rainy, 65°F

Thought: I have the answer
Final Answer: It's rainy and 65°F in Boston.

> Finished chain.
```

### Log Tool Calls

```python
@tool
def my_tool(param: str) -> str:
    """Does something."""
    print(f"[TOOL CALLED] my_tool({param})")
    result = do_something(param)
    print(f"[TOOL RESULT] {result}")
    return result
```

---

## What You've Learned

✅ What tool calling is and why it's powerful  
✅ How to create tools with the `@tool` decorator  
✅ Binding tools to models  
✅ Building agents that use multiple tools  
✅ Using MCP adapters for standard integrations  
✅ Best practices for tool design  

You can now give your AI real-world capabilities! Next, we'll learn about RAG - how to give your AI knowledge of your documents.

---

## What's Next?

In the next section, we'll learn about **RAG (Retrieval Augmented Generation)**:
- Loading documents
- Creating vector stores
- Building retrievers
- Wiring everything together

**[→ Continue to Step 4: RAG Basics]({{ site.baseurl }}{% link _topics/langchain-rag-basics.md %})**

---

## Quick Reference

### Basic Tool Template

```python
from langchain.tools import tool

@tool
def tool_name(param: str) -> str:
    """
    Clear description of what this tool does.
    
    Args:
        param: Description of parameter
    """
    # Do something
    return result
```

### Agent Template

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor

tools = [tool1, tool2, tool3]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke({"input": "Your question"})
```

Ready to learn about RAG? Let's go! 🚀

**[Next: RAG Basics →]({{ site.baseurl }}{% link _topics/langchain-rag-basics.md %})**
