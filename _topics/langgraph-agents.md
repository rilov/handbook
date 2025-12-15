---
title: "Part 5 - LangGraph & Agents: Building Intelligent Workflows"
category: Generative AI
order: 5
tags:
  - langgraph
  - agents
  - workflows
  - state-management
summary: Learn how to build sophisticated agentic systems with LangGraph using states, nodes, edges, and workflows - explained simply.
related:
  - langchain-rag-basics
  - langchain-tool-calling
  - langchain-observability
---

> **🎓 LangChain Learning Path - Step 5 of 7**
> - **[← Step 4: RAG Basics]({{ site.baseurl }}{% link _topics/langchain-rag-basics.md %})**
> - **Step 5 (this page):** LangGraph & Agents
> - **[Step 6: Building Your Agent Project →]({{ site.baseurl }}{% link _topics/langchain-project-agent.md %})**

---

## Why LangGraph?

Remember from our foundations: **LangChain** is great for linear workflows, but what about complex scenarios that need:
- Loops and conditionals
- Multiple decision points
- State management across steps
- Human-in-the-loop interactions

<div class="mermaid">
flowchart TB
    subgraph chain["🔗 LangChain - Linear"]
        C1["Step 1"] --> C2["Step 2"] --> C3["Step 3"] --> C4["Done"]
    end
    
    subgraph graph["🌊 LangGraph - Complex"]
        G1["Start"] --> G2{"Check State"}
        G2 -->|Need more info| G3["Use Tool"]
        G3 --> G2
        G2 -->|Ready| G4["Generate"]
        G4 --> G5{"Review"}
        G5 -->|Not good| G2
        G5 -->|Good| G6["Done"]
    end
    
    style chain fill:#fef3c7,stroke:#d97706
    style graph fill:#d1fae5,stroke:#059669
</div>

**LangGraph gives you the flexibility to build agents that can think, plan, and adapt!**

---

## Core Concepts

### 1. State

**State** is like a notepad that gets passed between steps and keeps track of information.

```python
from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_info: dict
    next_action: str
```

<div class="mermaid">
flowchart LR
    Node1["Node 1<br/>Reads & Updates State"] --> State["📝 State<br/>messages: []<br/>user_info: {}<br/>next_action: 'search'"]
    State --> Node2["Node 2<br/>Reads & Updates State"]
    
    style State fill:#fef3c7,stroke:#d97706
    style Node1 fill:#dbeafe,stroke:#2563eb
    style Node2 fill:#d1fae5,stroke:#059669
</div>

**Real-world analogy:** Like a relay race baton that each runner passes along, but this baton can hold notes that each runner adds to!

### 2. Nodes

**Nodes** are functions that do work and update the state.

```python
def search_node(state: AgentState):
    """Search for information."""
    query = state["messages"][-1].content
    results = search_tool(query)
    
    return {
        "messages": [AIMessage(content=f"Found: {results}")],
        "next_action": "analyze"
    }
```

<div class="mermaid">
flowchart TB
    subgraph node["🔵 Node = Function"]
        N1["1. Receives state"]
        N2["2. Does work"]
        N3["3. Returns updates"]
    end
    
    style node fill:#dbeafe,stroke:#2563eb
</div>

### 3. Edges

**Edges** connect nodes and determine the flow.

<div class="mermaid">
flowchart LR
    A["Node A"] -->|Normal Edge| B["Node B"]
    B -->|Conditional Edge| C{"Decision"}
    C -->|Path 1| D["Node D"]
    C -->|Path 2| E["Node E"]
    
    style A fill:#dbeafe,stroke:#2563eb
    style B fill:#fef3c7,stroke:#d97706
    style C fill:#fce7f3,stroke:#db2777
    style D fill:#d1fae5,stroke:#059669
    style E fill:#d1fae5,stroke:#059669
</div>

**Types of edges:**
- **Normal edge:** Always go to the same next node
- **Conditional edge:** Choose next node based on state

---

## Building Your First Graph

### Simple Example: Search → Analyze → Respond

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# Define state
class State(TypedDict):
    query: str
    search_results: str
    answer: str

# Define nodes
def search(state: State):
    """Search for information."""
    results = f"Results for: {state['query']}"
    return {"search_results": results}

def analyze(state: State):
    """Analyze results."""
    analysis = f"Analyzed: {state['search_results']}"
    return {"answer": analysis}

# Build the graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("search", search)
workflow.add_node("analyze", analyze)

# Add edges
workflow.add_edge("search", "analyze")
workflow.add_edge("analyze", END)

# Set entry point
workflow.set_entry_point("search")

# Compile
app = workflow.compile()

# Use it!
result = app.invoke({"query": "What is LangGraph?"})
print(result["answer"])
```

**Flow:**
```
Start → search → analyze → End
```

---

## Adding Conditional Logic

### Example: Search Only If Needed

<div class="mermaid">
flowchart TB
    Start["Start"] --> Check{"Can answer<br/>directly?"}
    Check -->|Yes| Answer["Generate Answer"]
    Check -->|No| Search["Search Info"]
    Search --> Answer
    Answer --> End["End"]
    
    style Start fill:#dbeafe,stroke:#2563eb
    style Check fill:#fef3c7,stroke:#d97706
    style Search fill:#fce7f3,stroke:#db2777
    style Answer fill:#d1fae5,stroke:#059669
</div>

```python
from langgraph.graph import StateGraph, END

# Define router function
def should_search(state):
    """Decide if we need to search."""
    query = state["query"]
    
    # Simple heuristic: search for questions
    if "?" in query:
        return "search"
    else:
        return "answer"

# Build graph
workflow = StateGraph(State)

workflow.add_node("check", check_node)
workflow.add_node("search", search_node)
workflow.add_node("answer", answer_node)

# Conditional edge from check
workflow.add_conditional_edges(
    "check",
    should_search,  # Router function
    {
        "search": "search",
        "answer": "answer"
    }
)

workflow.add_edge("search", "answer")
workflow.add_edge("answer", END)

workflow.set_entry_point("check")

app = workflow.compile()
```

---

## Building an Agent with Tools

### The ReAct Pattern

Agents use the **ReAct** (Reasoning + Acting) pattern:

<div class="mermaid">
flowchart TB
    Start["User Request"] --> Think["🤔 Think:<br/>What do I need?"]
    Think --> Act{"Act:<br/>Use tool?"}
    Act -->|Yes| Tool["🔧 Use Tool"]
    Tool --> Observe["👀 Observe Results"]
    Observe --> Think
    Act -->|No, ready| Respond["💬 Respond to User"]
    Respond --> End["End"]
    
    style Think fill:#dbeafe,stroke:#2563eb
    style Tool fill:#fef3c7,stroke:#d97706
    style Observe fill:#fce7f3,stroke:#db2777
    style Respond fill:#d1fae5,stroke:#059669
</div>

### Complete Agent Example

```python
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

# Define tools
@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 72°F"

@tool
def get_time() -> str:
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%I:%M %p")

tools = [get_weather, get_time]

# Create model
model = ChatOpenAI(model="gpt-4")

# Create agent (LangGraph does the heavy lifting!)
agent = create_react_agent(model, tools)

# Use it
response = agent.invoke({
    "messages": [("user", "What's the weather in Boston and what time is it?")]
})

for message in response["messages"]:
    print(f"{message.type}: {message.content}")
```

**What happens behind the scenes:**

```
User: "What's the weather in Boston and what time is it?"

Agent thinks: "I need two tools"

Step 1:
  Thought: Get weather first
  Action: get_weather("Boston")
  Observation: "Weather in Boston: Sunny, 72°F"

Step 2:
  Thought: Now get time
  Action: get_time()
  Observation: "2:30 PM"

Step 3:
  Thought: I have everything
  Final Answer: "It's sunny and 72°F in Boston, and the current time is 2:30 PM."
```

---

## Advanced: Custom Agent Loop

Let's build a custom agent from scratch to understand how it works:

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Literal

class AgentState(TypedDict):
    messages: list
    next_action: str

# Node 1: Agent decides what to do
def agent_node(state: AgentState):
    """Agent thinks and decides."""
    messages = state["messages"]
    
    # Call LLM to decide
    response = model_with_tools.invoke(messages)
    
    # Check if it wants to use tools
    if response.tool_calls:
        return {
            "messages": [response],
            "next_action": "tools"
        }
    else:
        return {
            "messages": [response],
            "next_action": "end"
        }

# Node 2: Execute tools
tool_node = ToolNode(tools)

# Router: Decide next step
def should_continue(state: AgentState) -> Literal["tools", "end"]:
    return state["next_action"]

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)

workflow.add_edge("tools", "agent")  # Loop back!

app = workflow.compile()
```

**The flow:**

<div class="mermaid">
flowchart TB
    Start["User Message"] --> Agent["🤖 Agent<br/>Thinks & Decides"]
    Agent --> Check{"Needs tools?"}
    Check -->|Yes| Tools["🔧 Execute Tools"]
    Tools --> Agent
    Check -->|No| End["📝 Final Answer"]
    
    style Agent fill:#dbeafe,stroke:#2563eb
    style Tools fill:#fef3c7,stroke:#d97706
    style End fill:#d1fae5,stroke:#059669
</div>

---

## Human-in-the-Loop

Sometimes you want the agent to ask for human approval before taking actions.

### Adding Interrupts

```python
from langgraph.checkpoint.memory import MemorySaver

# Add checkpointing for interrupts
memory = MemorySaver()

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# ... add edges ...

# Compile with checkpointer
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["tools"]  # Pause before using tools!
)

# First run - will pause
config = {"configurable": {"thread_id": "1"}}
result = app.invoke({"messages": [("user", "Send email to boss")]}, config)

print("Agent wants to use tools. Approve?")
# Show what tools it wants to use
print(result)

# If approved, continue
result = app.invoke(None, config)  # Resume from checkpoint
```

<div class="mermaid">
sequenceDiagram
    participant U as 👤 User
    participant A as 🤖 Agent
    participant H as 🛑 Human Approval
    participant T as 🔧 Tools
    
    U->>A: Send email to boss
    A->>A: Plans to use email tool
    A->>H: Request approval
    H-->>A: ✅ Approved
    A->>T: Execute email tool
    T-->>U: Email sent!
</div>

---

## Real-World Example: Customer Support Agent

Let's build a complete customer support agent:

```python
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Define tools
@tool
def check_order_status(order_id: str) -> str:
    """Check order status."""
    orders = {
        "123": "Shipped - Arriving Tuesday",
        "456": "Processing"
    }
    return orders.get(order_id, "Order not found")

@tool
def check_account_balance(customer_id: str) -> str:
    """Check account balance."""
    return f"Balance for {customer_id}: $1,234.56"

@tool
def create_ticket(issue: str) -> str:
    """Create support ticket."""
    ticket_id = "TICK-" + str(hash(issue))[:6]
    return f"Created ticket {ticket_id} for: {issue}"

tools = [check_order_status, check_account_balance, create_ticket]

# Create agent with system message
model = ChatOpenAI(model="gpt-4")
system_message = """You are a helpful customer support agent.

Guidelines:
- Be polite and professional
- Use tools to look up information
- If you can't help, create a ticket
- Always confirm actions with the customer
"""

agent = create_react_agent(
    model,
    tools,
    state_modifier=system_message
)

# Test it
messages = [
    ("user", "Hi, can you check my order 123?"),
]

result = agent.invoke({"messages": messages})
print(result["messages"][-1].content)

# Continue conversation
messages.append(("assistant", result["messages"][-1].content))
messages.append(("user", "Great! Can you also check my account balance? My ID is CUST-789"))

result = agent.invoke({"messages": messages})
print(result["messages"][-1].content)
```

---

## Managing Agent Memory

### Short-Term Memory (Within Conversation)

This is automatic - the `messages` in state act as memory:

```python
# Message 1
agent.invoke({"messages": [("user", "My name is Alice")]})
# Response: "Nice to meet you, Alice!"

# Message 2 - Agent remembers!
agent.invoke({
    "messages": [
        ("user", "My name is Alice"),
        ("assistant", "Nice to meet you, Alice!"),
        ("user", "What's my name?")
    ]
})
# Response: "Your name is Alice!"
```

### Long-Term Memory (Across Conversations)

Use checkpointing to save state:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
agent = create_react_agent(model, tools, checkpointer=memory)

# Conversation 1
config = {"configurable": {"thread_id": "user_123"}}
agent.invoke({"messages": [("user", "My favorite color is blue")]}, config)

# Later conversation - remembers!
agent.invoke({"messages": [("user", "What's my favorite color?")]}, config)
# Response: "Your favorite color is blue!"
```

---

## Advanced Patterns

### Pattern 1: Multi-Agent System

Multiple specialized agents working together:

<div class="mermaid">
flowchart TB
    User["👤 User"] --> Router["🎯 Router Agent"]
    Router --> Check{"What kind<br/>of request?"}
    Check -->|Technical| Tech["🔧 Tech Agent"]
    Check -->|Billing| Bill["💰 Billing Agent"]
    Check -->|General| Gen["💬 General Agent"]
    Tech --> Response["📝 Response"]
    Bill --> Response
    Gen --> Response
    
    style Router fill:#dbeafe,stroke:#2563eb
    style Tech fill:#fef3c7,stroke:#d97706
    style Bill fill:#fce7f3,stroke:#db2777
    style Gen fill:#d1fae5,stroke:#059669
</div>

### Pattern 2: Planning Agent

Agent that plans before acting:

```
1. Plan: Break down task into steps
2. Execute: Do step 1
3. Review: Did it work?
4. Replan if needed
5. Continue to next step
```

### Pattern 3: Reflection Agent

Agent that critiques its own work:

```
1. Generate answer
2. Critique: "Is this good?"
3. If not good: Revise
4. If good: Done
```

---

## Debugging & Visualization

### Print State at Each Step

```python
def debug_node(state):
    print("Current state:", state)
    return state

workflow.add_node("debug", debug_node)
```

### Visualize Your Graph

```python
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))
```

### Stream Events

```python
for event in app.stream({"messages": [("user", "Hello")]}):
    print(event)
```

---

## Best Practices

### 1. Keep Nodes Focused

Each node should do one thing:

❌ Bad: `process_everything_node()`  
✅ Good: `search_node()`, `analyze_node()`, `format_node()`

### 2. Use Type Hints

```python
class State(TypedDict):
    messages: list  # Clear what type
    count: int      # Clear what type
    ready: bool     # Clear what type
```

### 3. Handle Errors Gracefully

```python
def tool_node(state):
    try:
        result = risky_operation()
        return {"result": result}
    except Exception as e:
        return {"error": str(e), "next_action": "handle_error"}
```

### 4. Test Individual Nodes

```python
# Test nodes independently first
test_state = {"messages": [("user", "test")]}
result = agent_node(test_state)
print(result)  # Make sure it works!
```

### 5. Start Simple, Add Complexity

1. Build linear flow first
2. Add conditional edges
3. Add loops if needed
4. Add human-in-the-loop last

---

## Common Patterns Recap

<div class="mermaid">
flowchart TB
    subgraph patterns["🎯 Common Patterns"]
        P1["Linear Chain<br/>A → B → C"]
        P2["Conditional Branch<br/>A → {B or C}"]
        P3["Loop<br/>A → B → A"]
        P4["Human Approval<br/>A → 🛑 → B"]
    end
    
    style P1 fill:#dbeafe,stroke:#2563eb
    style P2 fill:#fef3c7,stroke:#d97706
    style P3 fill:#fce7f3,stroke:#db2777
    style P4 fill:#d1fae5,stroke:#059669
</div>

---

## What You've Learned

✅ Core concepts: States, Nodes, Edges  
✅ Building basic and conditional graphs  
✅ Creating agents with the ReAct pattern  
✅ Using tools in agents  
✅ Human-in-the-loop workflows  
✅ Memory management  
✅ Advanced patterns and best practices  

You can now build sophisticated agentic systems that can think, plan, and adapt! Next, you'll put it all together in a project.

---

## What's Next?

In the next section, you'll **build your own agentic application** from scratch, combining everything you've learned:
- Tool calling
- RAG for knowledge
- LangGraph for workflow
- Memory for context

**[→ Continue to Step 6: Build Your Agent Project]({{ site.baseurl }}{% link _topics/langchain-project-agent.md %})**

---

## Quick Reference

### Basic Graph Template

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    field1: str
    field2: int

def node_a(state: State):
    return {"field1": "updated"}

workflow = StateGraph(State)
workflow.add_node("a", node_a)
workflow.add_edge("a", END)
workflow.set_entry_point("a")

app = workflow.compile()
result = app.invoke({"field1": "initial", "field2": 0})
```

### Agent Template

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(model, tools)
result = agent.invoke({"messages": [("user", "question")]})
```

Ready to build your own agent? Let's do it! 🚀

**[Next: Build Your Agent Project →]({{ site.baseurl }}{% link _topics/langchain-project-agent.md %})**
