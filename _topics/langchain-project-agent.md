---
title: "Part 6 - Project: Build Your Own AI Agent"
category: Generative AI
order: 6
tags:
  - langgraph
  - project
  - agents
  - hands-on
summary: Step-by-step guide to building a complete agentic application with tools, memory, and workflows - a hands-on project for beginners.
related:
  - langgraph-agents
  - langchain-tool-calling
  - langchain-observability
---

> **🎓 LangChain Learning Path - Step 6 of 7**
> - **[← Step 5: LangGraph & Agents]({{ site.baseurl }}{% link _topics/langgraph-agents.md %})**
> - **Step 6 (this page):** Build Your Agent Project
> - **[Step 7: Observability with LangSmith →]({{ site.baseurl }}{% link _topics/langchain-observability.md %})**

> **📓 Hands-On Practice**  
> **[⬇️ Download Jupyter Notebook]({{ site.baseurl }}/notebooks/part6-project-agent.ipynb)** - Build a complete Research Assistant agent with tools, memory, and conversation management.

---

## What We're Building

Let's build a **Research Assistant Agent** that can:
- Search the web for information
- Remember conversation history
- Take notes in a file
- Summarize findings
- Cite sources

<div class="mermaid">
flowchart TB
    User["👤 User Request"] --> Agent["🤖 Research Agent"]
    
    Agent --> Tools["🔧 Tools"]
    Tools --> Search["🔍 Web Search"]
    Tools --> Notes["📝 Take Notes"]
    Tools --> Read["📄 Read Notes"]
    
    Agent --> Memory["🧠 Memory"]
    Memory --> Short["Short-term:<br/>Conversation"]
    Memory --> Long["Long-term:<br/>Saved Notes"]
    
    Agent --> Output["💬 Response<br/>with Citations"]
    
    style Agent fill:#dbeafe,stroke:#2563eb
    style Tools fill:#fef3c7,stroke:#d97706
    style Memory fill:#fce7f3,stroke:#db2777
    style Output fill:#d1fae5,stroke:#059669
</div>

---

## Prerequisites

### Install Required Packages

```bash
pip install langgraph langchain-openai langchain-community python-dotenv
```

### Set Up Environment

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

## Step 1: Define Our Tools

Let's create three tools for our agent:

```python
# research_agent.py

from langchain.tools import tool
import json
from datetime import datetime

@tool
def web_search(query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query: The search query
        
    Returns:
        Search results with sources
    """
    # For this example, we'll simulate search results
    # In production, use actual search API (SerpAPI, Tavily, etc.)
    
    results = f"""
    Search Results for "{query}":
    
    1. [Wikipedia] Brief overview of {query}
    2. [Research Paper] Detailed analysis of {query}
    3. [News] Recent developments about {query}
    """
    
    return results

@tool
def save_notes(content: str, title: str) -> str:
    """
    Save research notes to a file.
    
    Args:
        content: The note content
        title: Title/topic of the note
        
    Returns:
        Confirmation message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    note = {
        "title": title,
        "content": content,
        "timestamp": timestamp
    }
    
    # Save to file
    try:
        with open("research_notes.json", "r") as f:
            notes = json.load(f)
    except FileNotFoundError:
        notes = []
    
    notes.append(note)
    
    with open("research_notes.json", "w") as f:
        json.dump(notes, f, indent=2)
    
    return f"✅ Saved note: '{title}' at {timestamp}"

@tool
def read_notes(query: str = "") -> str:
    """
    Read previously saved research notes.
    
    Args:
        query: Optional search term to filter notes
        
    Returns:
        Matching notes
    """
    try:
        with open("research_notes.json", "r") as f:
            notes = json.load(f)
    except FileNotFoundError:
        return "No notes found. Start taking notes!"
    
    if query:
        # Filter notes by query
        matching = [n for n in notes if query.lower() in n["title"].lower() or query.lower() in n["content"].lower()]
    else:
        matching = notes
    
    if not matching:
        return f"No notes found matching '{query}'"
    
    result = "📚 Your Research Notes:\n\n"
    for note in matching:
        result += f"**{note['title']}** ({note['timestamp']})\n"
        result += f"{note['content']}\n\n"
    
    return result

# Export tools
tools = [web_search, save_notes, read_notes]
```

---

## Step 2: Create the Agent

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the LLM
model = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define system message
system_message = """You are a helpful Research Assistant.

Your capabilities:
- Search the web for information using web_search()
- Save important findings using save_notes()
- Recall past notes using read_notes()

Guidelines:
- Always cite your sources
- Save key findings to notes
- Be thorough but concise
- If asked about past research, check your notes first
- Break down complex research into steps

Example workflow:
1. Search for information
2. Analyze and summarize
3. Save important points
4. Provide answer with citations
"""

# Create agent with memory
memory = MemorySaver()

agent = create_react_agent(
    model,
    tools,
    state_modifier=system_message,
    checkpointer=memory
)

print("✅ Research Assistant Agent created!")
```

---

## Step 3: Create a User Interface

Let's create a simple chat interface:

```python
def chat():
    """Interactive chat with the research assistant."""
    
    print("=" * 60)
    print("🤖 Research Assistant")
    print("=" * 60)
    print("Ask me to research anything!")
    print("Type 'quit' to exit, 'clear' to start new conversation")
    print("=" * 60)
    
    # Conversation ID for memory
    thread_id = "user_session_1"
    config = {"configurable": {"thread_id": thread_id}}
    
    messages = []
    
    while True:
        # Get user input
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye! 👋")
            break
        
        if user_input.lower() == 'clear':
            messages = []
            thread_id = f"user_session_{datetime.now().timestamp()}"
            config = {"configurable": {"thread_id": thread_id}}
            print("🔄 Started new conversation")
            continue
        
        if not user_input:
            continue
        
        # Add user message
        messages.append(("user", user_input))
        
        # Get agent response
        try:
            print("\n🤔 Thinking...")
            result = agent.invoke(
                {"messages": messages},
                config
            )
            
            # Get the last message (agent's response)
            response = result["messages"][-1].content
            
            print(f"\n🤖 Assistant: {response}")
            
            # Update messages
            messages = result["messages"]
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    chat()
```

---

## Step 4: Test Your Agent

### Example Conversation

```
👤 You: Research the history of artificial intelligence

🤔 Thinking...
[Agent searches web]
[Agent saves notes]

🤖 Assistant: I've researched the history of AI for you. Here are the key points:

**Early Foundations (1950s)**
- Alan Turing proposed the Turing Test in 1950
- Term "Artificial Intelligence" coined by John McCarthy in 1956
- First AI conference at Dartmouth College

**Development Phases**
- 1950s-1970s: Early optimism and symbolic AI
- 1980s: Rise of expert systems
- 1990s-2000s: Machine learning emerges
- 2010s-Present: Deep learning revolution

I've saved these findings to your research notes.

Sources:
1. Wikipedia - History of Artificial Intelligence
2. Stanford AI Lab - AI Timeline
3. MIT Technology Review - AI Evolution

👤 You: What did you save about AI?

🤖 Assistant: Let me check my notes...
[Agent reads notes]

I have notes on "History of Artificial Intelligence" from just now, covering:
- Early foundations in the 1950s with Turing and McCarthy
- Development phases through the decades
- The recent deep learning revolution

Would you like me to expand on any of these topics?
```

---

## Step 5: Add Enhanced Features

### Feature 1: Streaming Responses

Show the agent's thinking in real-time:

```python
def chat_with_streaming():
    """Chat with streaming responses."""
    
    config = {"configurable": {"thread_id": "user_1"}}
    messages = []
    
    while True:
        user_input = input("\n👤 You: ").strip()
        if user_input.lower() == 'quit':
            break
        
        messages.append(("user", user_input))
        
        print("\n🤖 Assistant: ", end="", flush=True)
        
        # Stream events
        for event in agent.stream({"messages": messages}, config):
            for value in event.values():
                if "messages" in value:
                    last_message = value["messages"][-1]
                    if hasattr(last_message, 'content'):
                        print(last_message.content, end="", flush=True)
        
        print()  # New line
```

### Feature 2: Progress Indicators

Show what the agent is doing:

```python
def chat_with_progress():
    """Chat with progress indicators."""
    
    config = {"configurable": {"thread_id": "user_1"}}
    messages = []
    
    while True:
        user_input = input("\n👤 You: ").strip()
        if user_input.lower() == 'quit':
            break
        
        messages.append(("user", user_input))
        
        # Track steps
        for event in agent.stream({"messages": messages}, config, stream_mode="updates"):
            for node_name, values in event.items():
                if node_name == "tools":
                    tool_calls = values["messages"][-1].tool_calls if values.get("messages") else []
                    for tool_call in tool_calls:
                        print(f"🔧 Using tool: {tool_call['name']}")
                elif node_name == "agent":
                    print(f"💭 Agent thinking...")
        
        # Get final response
        result = agent.invoke({"messages": messages}, config)
        response = result["messages"][-1].content
        print(f"\n🤖 Assistant: {response}")
        
        messages = result["messages"]
```

### Feature 3: Export Research Report

```python
@tool
def generate_report(topic: str) -> str:
    """
    Generate a research report from saved notes.
    
    Args:
        topic: The research topic
        
    Returns:
        Formatted research report
    """
    try:
        with open("research_notes.json", "r") as f:
            notes = json.load(f)
    except FileNotFoundError:
        return "No notes available for report."
    
    # Filter relevant notes
    relevant = [n for n in notes if topic.lower() in n["title"].lower()]
    
    if not relevant:
        return f"No notes found for topic: {topic}"
    
    # Generate report
    report = f"""
# Research Report: {topic}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
This report compiles {len(relevant)} notes on {topic}.

## Findings

"""
    
    for i, note in enumerate(relevant, 1):
        report += f"### {i}. {note['title']}\n"
        report += f"*{note['timestamp']}*\n\n"
        report += f"{note['content']}\n\n"
    
    report += "\n## Conclusion\n"
    report += f"Research completed with {len(relevant)} key findings documented.\n"
    
    # Save report
    filename = f"report_{topic.replace(' ', '_')}.md"
    with open(filename, "w") as f:
        f.write(report)
    
    return f"✅ Report saved to {filename}"

# Add to tools
tools.append(generate_report)
```

---

## Step 6: Add Error Handling

Make your agent more robust:

```python
def safe_agent_invoke(messages, config, max_retries=3):
    """Invoke agent with error handling and retries."""
    
    for attempt in range(max_retries):
        try:
            result = agent.invoke({"messages": messages}, config)
            return result
        
        except Exception as e:
            print(f"⚠️  Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                print("🔄 Retrying...")
                continue
            else:
                print("❌ Max retries reached")
                return {
                    "messages": messages + [
                        ("assistant", "I encountered an error. Please try rephrasing your question.")
                    ]
                }
```

---

## Complete Code

Here's the complete `research_agent.py`:

```python
"""
Research Assistant Agent
A complete AI agent with tools, memory, and conversation management.
"""

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

# ===== TOOLS =====

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}\n[Simulated results]"

@tool
def save_notes(content: str, title: str) -> str:
    """Save research notes."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = {"title": title, "content": content, "timestamp": timestamp}
    
    try:
        with open("research_notes.json", "r") as f:
            notes = json.load(f)
    except FileNotFoundError:
        notes = []
    
    notes.append(note)
    
    with open("research_notes.json", "w") as f:
        json.dump(notes, f, indent=2)
    
    return f"✅ Saved: '{title}'"

@tool
def read_notes(query: str = "") -> str:
    """Read saved research notes."""
    try:
        with open("research_notes.json", "r") as f:
            notes = json.load(f)
    except FileNotFoundError:
        return "No notes found."
    
    if query:
        notes = [n for n in notes if query.lower() in str(n).lower()]
    
    if not notes:
        return "No matching notes."
    
    result = "📚 Your Notes:\n\n"
    for note in notes[-5:]:  # Last 5 notes
        result += f"**{note['title']}**\n{note['content']}\n\n"
    
    return result

tools = [web_search, save_notes, read_notes]

# ===== AGENT =====

model = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

system_message = """You are a Research Assistant. You can:
- Search the web
- Save notes
- Recall past research

Always cite sources and save key findings."""

memory = MemorySaver()
agent = create_react_agent(model, tools, state_modifier=system_message, checkpointer=memory)

# ===== INTERFACE =====

def chat():
    """Main chat loop."""
    print("🤖 Research Assistant (type 'quit' to exit)")
    
    config = {"configurable": {"thread_id": "user_1"}}
    messages = []
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye! 👋")
            break
        
        if not user_input:
            continue
        
        messages.append(("user", user_input))
        
        try:
            print("🤔 Thinking...")
            result = agent.invoke({"messages": messages}, config)
            response = result["messages"][-1].content
            print(f"\n🤖: {response}")
            messages = result["messages"]
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    chat()
```

---

## Testing Checklist

Test your agent with these scenarios:

- [ ] Simple question
- [ ] Research request (triggers web_search)
- [ ] Save information (triggers save_notes)
- [ ] Recall past research (triggers read_notes)
- [ ] Multi-step task
- [ ] Error handling
- [ ] Memory across messages

---

## Next Steps

### Enhancements You Can Add

1. **Real Web Search**
   - Use Tavily API or SerpAPI
   - Parse and format results

2. **Better Note System**
   - Use a database instead of JSON
   - Add tags and categories
   - Implement search

3. **Export Options**
   - PDF reports
   - Email summaries
   - Integration with note apps

4. **Advanced Features**
   - Web scraping for deep research
   - Image analysis
   - Data visualization

---

## What You've Built

✅ A complete AI agent with custom tools  
✅ Memory for conversation context  
✅ Note-taking and retrieval  
✅ Interactive chat interface  
✅ Error handling  
✅ Extensible architecture  

You now have a working agent you can customize and extend!

---

## What's Next?

Learn how to **monitor and debug** your agent with LangSmith:
- Trace agent decisions
- Debug tool calls
- Optimize performance
- Track costs

**[→ Continue to Step 7: Observability with LangSmith]({{ site.baseurl }}{% link _topics/langchain-observability.md %})**

---

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/)
- [Example Projects](https://github.com/langchain-ai/langgraph/tree/main/examples)

Congratulations on building your first agent! 🎉

**[Next: Observability with LangSmith →]({{ site.baseurl }}{% link _topics/langchain-observability.md %})**




