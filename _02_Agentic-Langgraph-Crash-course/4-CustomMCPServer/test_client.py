import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Configure connection to the new custom system utility MCP server via stdio transport
    client = MultiServerMCPClient(
        {
            "system_utility": {
                "command": r"C:\Users\cheru\OneDrive\Desktop\GitHub\Langchain_Agent_course\.venv\Scripts\python.exe",
                "args": [r"C:\Users\cheru\OneDrive\Desktop\GitHub\Langchain_Agent_course\_02_Agentic-LanggraphCrash-course\4-CustomMCPServer\server.py"],
                "transport": "stdio"
            }
        }
    )

    # 1. Fetch and list loaded tools
    tools = await client.get_tools()
    print("=== Loaded Tools ===")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    print("====================\n")

    # 2. Setup the LangChain Agent
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    agent = create_agent(
        model=llm,
        tools=tools
    )

    # 3. Test queries
    print("Asking Agent for CPU/Memory usage:")
    response_usage = await agent.ainvoke({
        "messages": [{"role": "user", "content": "Check the system's properties and let me know I can run ollama qwen:8b model locally"}]
    })
    print("\nAgent Response (CPU/Memory):")
    response_usage['messages'][-1].pretty_print()
    print()

    print("Asking Agent for System Info:")
    response_info = await agent.ainvoke({
        "messages": [{"role": "user", "content": "What operating system and CPU architecture am I running on?"}]
    })
    print("\nAgent Response (System Info):")
    response_info['messages'][-1].pretty_print()
    print()

if __name__ == "__main__":
    asyncio.run(main())
