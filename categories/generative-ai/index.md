---
layout: category
title: Generative AI
category: Generative AI
show_topic_list: false
---

Learn about LLMs, LangChain, RAG, agents, and building AI-powered applications — explained in simple terms for everyone.

**Recommended Learning Path:**

1. **[Part 1 - LangChain Foundations: Understanding LLMs and Orchestration]({{ site.baseurl }}/topics/langchain-foundations/)** — What an LLM is, why orchestration frameworks exist, and the core LangChain building blocks.
2. **[Part 2 - LangChain Essentials: Building Blocks of AI Applications]({{ site.baseurl }}/topics/langchain-essentials/)** — Prompts, chains, and output parsers used in real applications.
3. **[Part 3 - Tool Calling: Giving Your AI Real-World Superpowers]({{ site.baseurl }}/topics/langchain-tool-calling/)** — Letting an LLM call functions and APIs instead of just generating text.
4. **[Part 4 - RAG Basics: Teaching AI About Your Documents]({{ site.baseurl }}/topics/langchain-rag-basics/)** — Retrieval-augmented generation: embeddings, vector stores, and grounding answers in your own data.
5. **[Part 5 - LangGraph & Agents: Building Intelligent Workflows]({{ site.baseurl }}/topics/langgraph-agents/)** — Multi-step, stateful AI workflows and agent loops with LangGraph.
6. **[Part 6 - Project: Build Your Own AI Agent]({{ site.baseurl }}/topics/langchain-project-agent/)** — A hands-on project putting the previous five parts together.
7. **[Part 7 - Observability with LangSmith: Debug and Monitor Your AI]({{ site.baseurl }}/topics/langchain-observability/)** — Tracing, debugging, and monitoring LLM applications in production.

**Deep Learning for Generative AI — Context Behind Transformers:**

1. **[Word Embeddings]({{ site.baseurl }}/topics/dl-genai-word-embeddings/)** — How computers turn words into meaningful numbers: one-hot encoding, Word2Vec, cosine similarity, and the embedding layer.
2. **[Encoder-Decoder Architecture]({{ site.baseurl }}/topics/dl-genai-encoder-decoder/)** — The seq2seq model: how an encoder compresses a sentence into a context vector and a decoder generates the output one word at a time.
3. **[Attention-Based Encoder-Decoder]({{ site.baseurl }}/topics/dl-genai-attention-encoder-decoder/)** — How attention lets the decoder look back at every encoder word instead of relying on a single vector.
4. **[Math Behind Attention]({{ site.baseurl }}/topics/dl-genai-attention-math/)** — Dot products, scaling, softmax, and the Query-Key-Value framework with worked numerical examples.
5. **[Drawbacks of Attention-Based Encoder-Decoder]({{ site.baseurl }}/topics/dl-genai-attention-drawbacks/)** — Sequential processing, vanishing gradients, and why the Transformer was invented.

**Opinion, case studies, and explainers:**

- **[Saturday Morning Coffee ☕ Thoughts on Agentic AI]({{ site.baseurl }}/topics/agentic-ai-saturday-thoughts/)** — Informal reflections on where agentic AI is heading.
- **[Case Study: Amazon Rufus - AI Shopping Assistant Done Right]({{ site.baseurl }}/topics/rufus-amazon-ai-case-study/)** — What Amazon's Rufus gets right about AI-assisted shopping.
- **[Skills vs MCP vs Agents: The Future of AI (Explained Simply)]({{ site.baseurl }}/topics/anthropic-skills-vs-mcp/)** — Untangling three related but distinct ideas in plain language.

**Related Computer Vision topic:**

- **[Image Processing Fundamentals]({% link _topics/Computer Vision - Part 1 - Image Processing Fundamentals.md %})** — Pixels, colour models, kernels, convolution, and feature extraction. Now the first entry in the [Computer Vision]({{ site.baseurl }}/categories/computer-vision/) series, since it's foundational to vision rather than generative AI specifically.

**What You'll Learn:**

- What large language models are and how orchestration frameworks like LangChain fit around them
- How to build prompts, chains, and structured output parsers
- How to give an LLM tools and let it call real functions and APIs
- How retrieval-augmented generation (RAG) grounds answers in your own documents
- How to build multi-step, stateful agent workflows with LangGraph
- How to trace, debug, and monitor LLM applications in production
- How these ideas connect to real products and the broader direction of agentic AI
