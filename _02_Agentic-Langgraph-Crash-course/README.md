# 🤖 Agentic AI with LangGraph Crash Course

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Framework-orange.svg)
![LangChain](https://img.shields.io/badge/LangChain-LLM_Orchestration-green.svg)
![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-purple.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

---

# 📖 Overview

This repository contains my hands-on implementation of **LangGraph**, a framework for building stateful, agentic AI systems.

The course covers:

* Graph-based AI workflows
* Agent orchestration
* Human-in-the-loop systems
* Model Context Protocol (MCP)
* Custom MCP servers
* Debugging LangGraph applications
* Multi-Agent Systems

The implementations demonstrate how to build production-ready AI agents capable of reasoning, tool usage, human approval workflows, and external system integrations.

---

# 🎯 Learning Objectives

Through this course, I explored:

* LangGraph Fundamentals
* State Management
* Graph API
* Human-in-the-Loop Agents
* MCP Integration
* Custom MCP Server Development
* Agent Debugging
* Multi-Agent Systems
* Tool Calling Workflows
* Agent Orchestration

---

# ✅ Course Progress

* [x] Basic Chatbot with LangGraph
* [x] Human-in-the-Loop Workflow
* [x] MCP Integration
* [x] Custom MCP Server
* [x] LangGraph Debugging
* [x] Multi-Agent Systems

---

# 📚 Course Structure

## 1️⃣ Basic Chatbot

**Folder:** `1-BasicChatbot`

### Topics Covered

* StateGraph
* Nodes and Edges
* START and END Nodes
* Message State
* Graph Compilation
* Chatbot Workflow

### Key Learning

Built a stateful chatbot using LangGraph Graph API and learned how graph-based execution differs from traditional chains.

---

## 2️⃣ Human-in-the-Loop

**Folder:** `2-HumanAssistance`

### Topics Covered

* Human Approval Workflows
* Interrupt Mechanisms
* Manual Validation
* Agent Control

### Key Learning

Implemented workflows where human feedback and approval can influence agent decisions before execution.

---

## 3️⃣ MCP Integration

**Folder:** `3-MCPDemoLangchain`

### Topics Covered

* Model Context Protocol (MCP)
* MCP Client
* MCP Servers
* Tool Discovery
* Multi-Server Connections
* LangChain Agent Integration

### Files

```text
client.py
mathserver.py
weather.py
```

### Implementations

* Mathematical MCP Server
* Weather MCP Server
* Multi-Server MCP Client
* LangChain Agent + MCP Integration

### Key Learning

Connected multiple external tools to AI agents using MCP and dynamically exposed tools to agents.

---

## 4️⃣ Custom MCP Server

**Folder:** `4-CustomMCPServer`

### Topics Covered

* FastMCP
* Custom Tool Creation
* System Monitoring
* CPU Usage
* Memory Usage
* Disk Usage
* File System Operations

### Files

```text
server.py
test_client.py
```

### Implementations

Custom MCP tools for:

* System Information
* CPU Monitoring
* Memory Monitoring
* Disk Usage
* Directory Listing

### Key Learning

Built production-style MCP servers exposing custom business functionality to AI agents.

---

## 5️⃣ Debugging LangGraph Applications

**Folder:** `4-Debugging`

### Topics Covered

* LangGraph Studio
* Graph Visualization
* Agent Tracing
* Tool Execution Tracking
* Debugging Workflows
* LangSmith Integration

### Files

```text
debugging.ipynb
agent.py
langgraph.json
```

### Key Learning

Learned how to inspect, trace, visualize, and debug complex agent workflows.

---

## 6️⃣ Multi-Agent Systems

**Folder:** `5-Multimodal\ Agents`

### Topics Covered

* Multi-Agent Architectures
* Agent Collaboration
* Agent Delegation
* Workflow Coordination
* Tool Sharing

### Files

```text
multiaiagent.ipynb
```

### Key Learning

Built collaborative AI systems where multiple agents coordinate to solve tasks.

---

# 🛠️ Technologies Used

* Python
* LangGraph
* LangChain
* LangSmith
* MCP (Model Context Protocol)
* FastMCP
* Groq
* Ollama
* Google Gemini
* OpenAI
* Jupyter Notebook
* python-dotenv

---

# 📂 Project Structure

```text
02_Agentic-Langgraph-Crash-course
│
├── 1-BasicChatbot
│   └── chatbot.ipynb
│
├── 2-HumanAssistance
│   └── humanintheloop.ipynb
│
├── 3-MCPDemoLangchain
│   ├── client.py
│   ├── mathserver.py
│   └── weather.py
│
├── 4-CustomMCPServer
│   ├── server.py
│   └── test_client.py
│
├── 4-Debugging
│   ├── debugging.ipynb
│   ├── agent.py
│   └── langgraph.json
│
├── 5-Multimodal Agents
│   └── multiaiagent.ipynb
│
└── README.md
```

---

# 🚀 Skills Acquired

## LangGraph Fundamentals

* StateGraph
* Nodes & Edges
* State Management
* Graph Execution
* Message Handling

## Agent Engineering

* Agent Orchestration
* Tool Calling
* Human-in-the-Loop Systems
* Agent Memory
* Agent Coordination

## MCP Development

* MCP Clients
* MCP Servers
* FastMCP
* Tool Discovery
* External System Integration

## Production AI Engineering

* Debugging
* Monitoring
* Observability
* Tracing
* Agent Evaluation

---

# 💡 Key Takeaways

* Built stateful AI agents using LangGraph.
* Implemented Human-in-the-Loop workflows.
* Developed MCP servers and MCP clients.
* Connected external tools to AI agents.
* Learned graph-based agent orchestration.
* Built multi-agent collaborative systems.
* Debugged and monitored agent workflows using LangGraph tooling.
* Established a strong foundation for advanced Agentic AI development.

---

# 🔜 Next Learning Path

After completing this module, the next learning journey includes:

* Advanced RAG Systems
* Vector Databases
* Hybrid Search
* Deep Agents
* AI Security
* LLMOps
* Production AI Deployment

---

# 👨‍💻 Author

**Cherupally Naveen Chandra**

* Python Developer
* Data Analyst
* Aspiring AI Engineer

### GitHub

https://github.com/chandracherupally

---

⭐ This repository is part of my AI Engineering learning journey focused on Agentic AI, LangGraph, MCP, and production-ready AI systems.
