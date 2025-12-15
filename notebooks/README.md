# LangChain Learning Path - Jupyter Notebooks

Interactive Jupyter notebooks for the complete LangChain learning path. Each notebook contains runnable code examples, exercises, and hands-on practice.

## 📚 Available Notebooks

| Part | Topic | Notebook | Description |
|------|-------|----------|-------------|
| 1 | Foundations | [part1-langchain-foundations.ipynb](part1-langchain-foundations.ipynb) | Understanding LLMs, LangChain, and orchestration |
| 2 | Essentials | [part2-langchain-essentials.ipynb](part2-langchain-essentials.ipynb) | Chat models, prompting, structured outputs, LCEL |
| 3 | Tool Calling | [part3-tool-calling.ipynb](part3-tool-calling.ipynb) | Creating tools and building agents |
| 4 | RAG Basics | [part4-rag-basics.ipynb](part4-rag-basics.ipynb) | Document loading, embeddings, vector stores, retrieval |
| 5 | LangGraph | [part5-langgraph-agents.ipynb](part5-langgraph-agents.ipynb) | Complex workflows with states, nodes, and edges |
| 6 | Project | [part6-project-agent.ipynb](part6-project-agent.ipynb) | Build a complete Research Assistant agent |
| 7 | Observability | [part7-observability.ipynb](part7-observability.ipynb) | Debugging and monitoring with LangSmith |

## 🚀 Getting Started

### 1. Install Jupyter

```bash
pip install jupyter
```

### 2. Download a Notebook

Click the download link on any topic page, or clone the repository:

```bash
git clone https://github.com/your-repo/handbook.git
cd handbook/notebooks
```

### 3. Open Jupyter

```bash
jupyter notebook
```

### 4. Get API Keys

You'll need:
- **OpenAI API Key**: Get one at https://platform.openai.com/api-keys
- **LangSmith API Key** (for Part 7): Get one at https://smith.langchain.com

## 💡 How to Use These Notebooks

Each notebook includes:

✅ **Setup Instructions** - Install packages and configure API keys  
✅ **Code Examples** - All code from the tutorial, ready to run  
✅ **Explanations** - Markdown cells explaining concepts  
✅ **Practice Exercises** - Hands-on exercises to reinforce learning  
✅ **Complete Examples** - Full working applications

### Running a Notebook

1. Open the notebook in Jupyter
2. Run the first cells to install packages
3. Enter your API key when prompted
4. Run each cell sequentially (Shift + Enter)
5. Modify code to experiment!

## 🔑 API Key Setup

### Option 1: Input When Prompted (Recommended)

Notebooks will prompt you for your API key:

```python
import getpass
api_key = getpass.getpass("Enter your OpenAI API key: ")
```

### Option 2: Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_key_here
LANGCHAIN_API_KEY=your_langsmith_key_here
```

Then in the notebook:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Option 3: Direct Assignment (Not Recommended)

```python
import os
os.environ["OPENAI_API_KEY"] = "your_key_here"
```

⚠️ **Warning**: Never commit API keys to version control!

## 📝 Tips for Learning

1. **Work Through in Order** - Notebooks build on each other
2. **Run All Cells** - Don't skip cells or you'll miss dependencies
3. **Experiment** - Modify code to see what happens
4. **Take Notes** - Add your own markdown cells
5. **Practice** - Complete the exercises at the end

## 🐛 Troubleshooting

### Import Errors

Make sure packages are installed:

```bash
pip install langchain langchain-openai langgraph python-dotenv pydantic
```

### API Key Errors

Verify your key is set:

```python
import os
print("Key set:" if os.getenv("OPENAI_API_KEY") else "Key missing")
```

### Package Version Issues

Update to latest versions:

```bash
pip install --upgrade langchain langchain-openai
```

## 🎯 What You'll Learn

By completing all notebooks, you'll be able to:

- ✅ Build AI applications with LangChain
- ✅ Create custom tools for LLMs
- ✅ Implement RAG systems for document Q&A
- ✅ Build complex agentic workflows with LangGraph
- ✅ Debug and monitor production AI systems
- ✅ Deploy your own AI agents

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

## 💬 Need Help?

- **Tutorial Pages**: Each notebook has a corresponding tutorial page with detailed explanations
- **LangChain Discord**: Join the community at https://discord.gg/langchain
- **GitHub Issues**: Report problems or suggest improvements

## 🎉 Happy Learning!

Start with Part 1 and work your way through. By the end, you'll have built real AI agents!

---

**Note**: These notebooks use OpenAI's GPT models which require API credits. Check pricing at https://openai.com/pricing
