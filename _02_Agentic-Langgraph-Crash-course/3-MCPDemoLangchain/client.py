from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
import os

import asyncio




from dotenv import load_dotenv
load_dotenv()

async def main():
    #Create MCP server connection
    client = MultiServerMCPClient(
        {
        "math":{
            "command": r"C:\Users\cheru\OneDrive\Desktop\GitHub\Langchain_Agent_course\.venv\Scripts\python.exe", 
            "args":[r"C:\Users\cheru\OneDrive\Desktop\GitHub\Langchain_Agent_course\_02_Agentic-LanggraphCrash-course\3-MCPDemoLangchain\mathserver.py"], ##Ensure correct absolute path
            "transport":"stdio"
            },
         "weather":{
            "url": r"http://localhost:8000/mcp", ##Ensure server is running here
            "transport":"streamable-http"
            }
        }
    )
        
    tools = await client.get_tools()
    print("Loaded tools:")
    for tool in tools:
        print(tool.name)
    
    llm = ChatGroq(model="llama-3.3-70b-versatile")

    #Create LangGraph agent
    agent = create_agent(
        model=llm,
        tools=tools
    )

    weather_response = await agent.ainvoke({"messages":[{"role":"user",
                                                     "content":"What is the weather like in Hyderabad?"}]})
    print("Weather Response:", weather_response['messages'][-1].content)
    print("\n")
    weather_response['messages'][-1].pretty_print()
    print()


"""
    math_response = await agent.ainvoke({"messages":[{"role":"user",
                                                     "content":"What is (3+5)*12"}]})
    print("Math Response:", math_response['messages'][-1].content)
    print("\n")
    math_response['messages'][-1].pretty_print()
    print()
"""    

asyncio.run(main())
