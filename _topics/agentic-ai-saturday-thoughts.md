---
title: "Saturday Morning Coffee ☕ Thoughts on Agentic AI"
category: Generative AI
order: 8
tags:
  - agentic-ai
  - agents
  - workflows
  - architecture
summary: Why Agentic AI isn't failing because it's weak it's failing because we're asking it to do the wrong job. Agents should orchestrate workflows, not replace them.
date: 2025-01-24
---

# Saturday Morning Coffee ☕ Thoughts on Agentic AI

![Agentic AI](/handbook/assets/img/agentimage.png)

## The Complaint I Keep Hearing

Whenever I speak with friends mostly outside my organization they usually complain that there's a **huge push for generative AI, but not many visible success stories.**

Everyone's excited about demos. Few are confident about production.

And I think I know why.

---

## The Real Problem

**Agentic AI is not failing because it's weak.**

**It's failing because we're asking it to do the wrong job.**

I see many teams focusing on creating new workflows while moving away from deterministic pipelines. They're trying to replace proven, boring infrastructure with intelligent agents.

That's backwards.

---

## The Right Approach

Here's what I believe:

> **Agentic AI should decide WHAT to do.**
> 
> **Deterministic pipelines should decide HOW it's done.**

Let me break this down.

### What Agents Are Good At

Agents are excellent at:
- ✅ Understanding intent
- ✅ Breaking ambiguity into plans
- ✅ Choosing the next best action
- ✅ Adapting to context

### What Agents Are NOT Good At

They're not built for:
- ❌ Repeatability
- ❌ Compliance
- ❌ Audit trails
- ❌ Guaranteed execution

### What Pipelines Are Good At

Pipelines are the opposite:
- ✅ Repeatable
- ✅ Auditable
- ✅ Compliant
- ✅ Boring (and that's exactly why they work in production)

---

## The Winning Model

**The winning model isn't "agents replacing workflows."**

**It's agents orchestrating workflows.**

<div class="mermaid">
graph TB
    Agent["🤖 AGENTIC AI<br/>Understands Intent<br/>Decides WHAT to do"]
    Pipeline["⚙️ DETERMINISTIC PIPELINE<br/>Executes HOW<br/>(includes policies & validation)"]
    Human["👤 HUMAN<br/>Reviews & Approves<br/>Stays Accountable"]
    
    Agent -->|"Creates Execution Plan"| Pipeline
    Pipeline -->|"High-stakes decisions"| Human
    Human -->|"Approval"| Pipeline
    Pipeline -->|"Feedback & Learning"| Agent
    
    style Agent fill:#e1f5ff,stroke:#0066cc,stroke-width:3px
    style Pipeline fill:#fff4e6,stroke:#ff9800,stroke-width:3px
    style Human fill:#f3e5f5,stroke:#9c27b0,stroke-width:3px
</div>

**Agents plan. Pipelines execute (with policies baked in). Humans stay accountable.**

That's how you move agentic AI from demos to infrastructure—without creating operational anxiety.

---

## A Word About MCP (Model Context Protocol)

**MCP is a great idea.** It's a powerful way to give agents access to external tools and data.

**But you don't need to put MCP everywhere.**

I see teams adding MCP servers for everything:
- Database queries → MCP server
- API calls → MCP server  
- File operations → MCP server
- Email sending → MCP server

Then they wonder why their system is complex and hard to debug.

### When to Use MCP

✅ **Use MCP when:**
- Agents need **dynamic discovery** of tools
- You want **standardized tool interfaces** across multiple agents
- You're building **reusable tool libraries**
- You need **runtime tool registration**

### When NOT to Use MCP

❌ **Don't use MCP when:**
- You have **deterministic pipelines** (just call them directly!)
- You need **strict compliance** (policies should be in your pipeline code)
- You want **simple, auditable flows** (MCP adds indirection)
- You're building **production-critical workflows** (keep it simple)

### The Right Mental Model

<div class="mermaid">
graph LR
    subgraph "Agent Layer (Flexible)"
        A[Agent]
    end
    
    subgraph "Tool Discovery (MCP)"
        MCP["MCP Server<br/>Dynamic Tools"]
    end
    
    subgraph "Pipeline Layer (Deterministic)"
        P1["Pipeline 1<br/>Check Order"]
        P2["Pipeline 2<br/>Process Refund"]
        P3["Pipeline 3<br/>Send Email"]
    end
    
    A -->|"Discovers tools"| MCP
    A -->|"Calls directly"| P1
    A -->|"Calls directly"| P2
    A -->|"Calls directly"| P3
    
    style A fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    style MCP fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    style P1 fill:#fff4e6,stroke:#ff9800,stroke-width:2px
    style P2 fill:#fff4e6,stroke:#ff9800,stroke-width:2px
    style P3 fill:#fff4e6,stroke:#ff9800,stroke-width:2px
</div>

**Think beyond MCP:**
- MCP is for **tool discovery and flexibility**
- Pipelines are for **deterministic execution**
- Use the right tool for the right job

**You need to understand what that pipeline does.** If it's deterministic, repeatable, and needs audit trails it's a pipeline. Call it directly. Don't wrap it in MCP just because you can.

---

## Real-World Example: Intelligent Email Assistant

Let me show you what this looks like in practice.

### The Problem

You receive hundreds of emails daily:
- Customer support requests
- Sales inquiries
- Internal questions
- Spam and noise

You want AI to help, but you can't just let an agent "do whatever it thinks is best" with your email.

### The Wrong Approach ❌

**Pure Agentic Solution:**

<div class="mermaid">
graph LR
    Email[📧 Email] --> Agent[🤖 Agent]
    Agent --> Decision{Agent Decides}
    Decision --> Execute[⚡ Agent Executes]
    Execute --> Done[❓ What happened?]
    
    style Email fill:#fff,stroke:#333
    style Agent fill:#ffebee,stroke:#f44336,stroke-width:2px
    style Decision fill:#ffebee,stroke:#f44336,stroke-width:2px
    style Execute fill:#ffebee,stroke:#f44336,stroke-width:2px
    style Done fill:#ffebee,stroke:#f44336,stroke-width:2px
</div>

**Problems:**
- ❌ What if the agent misunderstands?
- ❌ How do you audit what it did?
- ❌ Can you rollback a sent email?
- ❌ How do you ensure compliance?

### The Right Approach ✅

**Agent Orchestrates Pipelines (with policies baked in):**

<div class="mermaid">
graph TB
    Email["📧 Email Arrives"]
    
    subgraph Agent["🤖 AGENT LAYER"]
        Intent["Understand Intent<br/>• Support request?<br/>• Sales inquiry?<br/>• Urgent?<br/>• Sentiment?"]
        Plan["Create Execution Plan<br/>Intent: Customer needs refund<br/>→ Check order<br/>→ Verify eligibility<br/>→ Draft response"]
    end
    
    subgraph Pipeline["⚙️ DETERMINISTIC PIPELINE (with policies)"]
        P1["Step 1: Check Order<br/>→ Query database<br/>→ Return structured data"]
        P2["Step 2: Verify Eligibility<br/>🛡️ Policy: Check refund window<br/>🛡️ Policy: Check order status<br/>→ Return yes/no + reason"]
        P3["Step 3: Draft Response<br/>🛡️ Policy: Use approved template<br/>🛡️ Policy: Check amount threshold<br/>→ Return draft"]
        P4["Step 4: Policy Check<br/>🛡️ Amount < $100 → Auto-approve<br/>🛡️ Amount > $100 → Human review<br/>🛡️ Premium tier → Expedite"]
    end
    
    Human["👤 Human Review<br/>(if needed)"]
    Send["✅ Send with Audit Trail"]
    
    Email --> Intent
    Intent --> Plan
    Plan --> P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 -->|"High stakes"| Human
    P4 -->|"Auto-approved"| Send
    Human -->|"Approved"| Send
    
    style Email fill:#fff,stroke:#333
    style Intent fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    style Plan fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    style P1 fill:#fff4e6,stroke:#ff9800,stroke-width:2px
    style P2 fill:#fff4e6,stroke:#ff9800,stroke-width:2px
    style P3 fill:#fff4e6,stroke:#ff9800,stroke-width:2px
    style P4 fill:#fff4e6,stroke:#ff9800,stroke-width:2px
    style Human fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    style Send fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
</div>

**Key insight:** Policies are **part of the pipeline**, not a separate layer. They're baked into each step as validation rules, compliance checks, and business logic.

---

## The Architecture in Code

Here's what this looks like in practice:

### The Agent (Intent Understanding)

```python
class EmailAgent:
    def understand_intent(self, email: Email) -> Intent:
        """Agent decides WHAT to do"""
        prompt = f"""
        Analyze this email and determine:
        1. Category (support, sales, internal, spam)
        2. Intent (refund, question, complaint, inquiry)
        3. Urgency (low, medium, high, critical)
        4. Sentiment (positive, neutral, negative)
        
        Email: {email.body}
        """
        
        response = claude.messages.create(
            model="claude-3-5-sonnet",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return Intent.from_llm_response(response)
    
    def create_plan(self, intent: Intent) -> ExecutionPlan:
        """Agent creates a plan using deterministic pipelines"""
        if intent.category == "support" and intent.intent == "refund":
            return ExecutionPlan(
                steps=[
                    PipelineStep("check_order_status"),
                    PipelineStep("verify_refund_eligibility"),
                    PipelineStep("draft_response"),
                    PolicyCheck("require_approval_if_over_threshold"),
                ]
            )
        # ... other intents
```

### The Pipelines (Deterministic Execution with Policies Baked In)

```python
class RefundPipeline:
    """Deterministic pipeline with policies baked in"""
    
    def check_order_status(self, order_id: str) -> OrderStatus:
        """Step 1: Boring, repeatable, auditable"""
        # Policy: Only query authorized database
        if not self.is_authorized_database():
            raise PolicyViolation("Unauthorized database access")
        
        order = database.query(
            "SELECT * FROM orders WHERE id = ?", 
            order_id
        )
        
        # Policy: Log all data access for audit
        audit_log.record("order_lookup", order_id=order_id)
        
        return OrderStatus(
            order_id=order.id,
            status=order.status,
            date=order.created_at,
            amount=order.total
        )
    
    def verify_refund_eligibility(self, order: OrderStatus) -> EligibilityResult:
        """Step 2: Deterministic rules with policies"""
        days_since_order = (datetime.now() - order.date).days
        
        # Policy: 30-day refund window
        if days_since_order > 30:
            return EligibilityResult(
                eligible=False,
                reason="Order is older than 30-day refund window",
                policy_violated="REFUND_WINDOW_POLICY"
            )
        
        # Policy: No double refunds
        if order.status == "refunded":
            return EligibilityResult(
                eligible=False,
                reason="Order already refunded",
                policy_violated="DOUBLE_REFUND_POLICY"
            )
        
        # Policy: Check fraud indicators
        if self.check_fraud_indicators(order):
            return EligibilityResult(
                eligible=False,
                reason="Fraud indicators detected",
                policy_violated="FRAUD_PREVENTION_POLICY",
                requires_manual_review=True
            )
        
        return EligibilityResult(eligible=True)
    
    def draft_response(self, context: dict) -> EmailDraft:
        """Step 3: Use approved template with policy checks"""
        # Policy: Only use approved templates
        template = self.load_approved_template("refund_approved")
        if not template.is_approved:
            raise PolicyViolation("Template not approved for use")
        
        # Policy: Check amount threshold for auto-approval
        requires_approval = context['refund_amount'] > 100
        
        # Policy: Premium customers get expedited processing
        processing_time = "1-2 business days" if context.get('customer_tier') == 'premium' else "3-5 business days"
        
        draft = EmailDraft(
            subject=f"Re: Refund Request for Order #{context['order_id']}",
            body=template.render(
                customer_name=context['customer_name'],
                order_id=context['order_id'],
                refund_amount=context['refund_amount'],
                processing_time=processing_time
            ),
            requires_human_approval=requires_approval,
            metadata={
                "template_id": template.id,
                "template_version": template.version,
                "generated_at": datetime.now(),
                "policies_applied": [
                    "APPROVED_TEMPLATE_POLICY",
                    "AMOUNT_THRESHOLD_POLICY",
                    "CUSTOMER_TIER_POLICY"
                ]
            }
        )
        
        # Policy: Log all email drafts for audit
        audit_log.record("email_drafted", draft=draft)
        
        return draft
```

### Putting It All Together

```python
class EmailAssistant:
    def __init__(self):
        self.agent = EmailAgent()
        self.policy = PolicyLayer()
        self.pipeline = RefundPipeline()
    
    async def process_email(self, email: Email):
        # 1. Agent understands intent
        intent = self.agent.understand_intent(email)
        
        # 2. Agent creates execution plan
        plan = self.agent.create_plan(intent)
        
        # 3. Execute pipelines to gather context
        context = {}
        for step in plan.pipeline_steps:
            if step.name == "check_order_status":
                order = self.pipeline.check_order_status(email.order_id)
                context["order"] = order
                context["refund_amount"] = order.amount
            
            elif step.name == "verify_refund_eligibility":
                eligibility = self.pipeline.verify_refund_eligibility(
                    context["order"]
                )
                context["eligible"] = eligibility.eligible
                context["reason"] = eligibility.reason
        
        # 4. Check if human approval is needed (policy in pipeline)
        if context.get("requires_human_approval"):
            return self.request_human_approval(draft, context)
        
        # 5. Send (with full audit trail)
        return self.send_with_audit(draft, context)
```

---

## Why This Works

### 1. **Agents Do What They're Good At**
- Understanding messy, ambiguous input
- Choosing the right pipeline for the job
- Adapting to context
- Creating execution plans

### 2. **Pipelines Do What They're Good At (with policies baked in)**
- Repeatable execution
- Compliance with rules (enforced at each step)
- Audit trails (logged automatically)
- Guaranteed behavior
- Policy enforcement (not a separate layer)

### 3. **Humans Stay in Control**
- Review high-stakes decisions
- Override when needed
- Maintain accountability
- Policies escalate to humans when needed

---

## The Benefits

**For Engineering:**
- ✅ Deterministic pipelines are testable
- ✅ Clear separation of concerns
- ✅ Easy to debug (agent vs pipeline vs policy)
- ✅ Can upgrade agents without touching pipelines

**For Compliance:**
- ✅ Full audit trail of decisions
- ✅ Policy enforcement is explicit (in pipeline code)
- ✅ Human approval for sensitive actions (triggered by policies)
- ✅ Rollback capability
- ✅ Policies are versioned with pipeline code

**For Business:**
- ✅ Agents improve over time without risk
- ✅ Pipelines remain stable and reliable
- ✅ Clear accountability
- ✅ Gradual automation (start with human approval, remove as confidence grows)

---

## The Implementation Path

### Phase 1: Agent as Advisor
```
Email → Agent analyzes → Shows recommendation → Human decides → Pipeline executes
```
**Risk: Low | Value: Learning**

### Phase 2: Agent with Approval
```
Email → Agent analyzes → Agent creates plan → Human approves → Pipeline executes
```
**Risk: Medium | Value: Efficiency**

### Phase 3: Agent Orchestrates (with guardrails)
```
Email → Agent analyzes → Policy validates → Pipeline executes → Log for audit
```
**Risk: Managed | Value: Scale**

---

## Real Results

Here's what this looks like in practice:

**Before (Manual):**
- 200 emails/day
- 5 minutes per email
- 1000 minutes = 16.7 hours/day (impossible)

**After (Agent-Orchestrated):**
- Agent handles 80% automatically (160 emails)
- Human reviews 20% (40 emails)
- 40 emails × 2 minutes = 80 minutes/day
- **Time saved: 920 minutes/day (15.3 hours)**

**And critically:**
- ✅ Full audit trail
- ✅ Compliance maintained
- ✅ Humans review high-stakes decisions
- ✅ No "AI did something weird" incidents

---

## The Key Insight

**Hype fades. Good architecture survives.**

The teams succeeding with Agentic AI aren't the ones replacing everything with agents.

They're the ones who understand:
- **Agents are great at planning**
- **Pipelines are great at executing**
- **Policies keep everything safe**
- **Humans maintain accountability**

Don't ask agents to be deterministic. Don't ask pipelines to be intelligent.

**Let each component do what it does best.**

---

## Takeaways

1. **Agents should orchestrate, not replace**
   - Use agents to understand intent and create plans
   - Use pipelines to execute those plans reliably

2. **Policies are not optional**
   - They're the guardrails that make agents production-safe
   - They enforce business rules and compliance

3. **Humans stay accountable**
   - High-stakes decisions require human approval
   - Agents assist, humans decide

4. **Start small, scale gradually**
   - Phase 1: Agent as advisor
   - Phase 2: Agent with approval
   - Phase 3: Agent orchestrates (with guardrails)

5. **Good architecture beats hype**
   - Boring pipelines + intelligent agents = production success
   - Pure agent solutions = demo success, production anxiety

---

## Final Thought

The next time someone tells you "Agentic AI isn't working," ask them:

**"Are you asking agents to replace workflows, or orchestrate them?"**

Because the answer determines whether you're building a demo or building infrastructure.

☕ *End of Saturday morning thoughts. Time for a refill.*

---

## Further Reading

- [Skills vs MCP vs Agents](/handbook/topics/anthropic-skills-vs-mcp/) - Understanding the agent ecosystem
- [LangGraph & Agents](/handbook/topics/langgraph-agents/) - Building intelligent workflows
- [RAG Basics](/handbook/topics/langchain-rag-basics/) - Teaching AI about your documents

## Try It Yourself

Want to build this email assistant? Here's a starter template:

```python
# email_assistant.py
from anthropic import Anthropic
import json

class SimpleEmailAssistant:
    def __init__(self):
        self.client = Anthropic()
    
    def analyze_email(self, email_body: str):
        """Agent: Understand intent"""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""Analyze this email and return JSON:
                {{
                    "category": "support|sales|internal|spam",
                    "intent": "refund|question|complaint|inquiry",
                    "urgency": "low|medium|high|critical",
                    "sentiment": "positive|neutral|negative"
                }}
                
                Email: {email_body}
                """
            }]
        )
        
        return json.loads(response.content[0].text)
    
    def create_plan(self, intent: dict):
        """Agent: Create execution plan"""
        if intent["category"] == "support" and intent["intent"] == "refund":
            return {
                "pipelines": ["check_order", "verify_eligibility", "draft_response"],
                "requires_approval": True if intent["urgency"] == "high" else False
            }
        return {"pipelines": ["draft_response"]}
    
    def execute_pipeline(self, pipeline_name: str, context: dict):
        """Pipeline: Deterministic execution"""
        if pipeline_name == "check_order":
            # Call your database/API
            return {"order_id": "12345", "amount": 99.99, "status": "completed"}
        
        elif pipeline_name == "draft_response":
            # Use template
            return f"Dear customer, regarding your request..."
        
        # Add more pipelines as needed

# Usage
assistant = SimpleEmailAssistant()
intent = assistant.analyze_email("I want a refund for order #12345")
plan = assistant.create_plan(intent)
# Execute pipelines...
```

Start simple. Add complexity as you learn. Keep agents and pipelines separate.

That's how you go from demo to production.
