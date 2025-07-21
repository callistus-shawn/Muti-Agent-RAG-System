from typing import Optional
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate
from .utils.search_doc import search_document
from langchain_mcp_adapters.client import MultiServerMCPClient


class ToolState(BaseModel):
    question: str
    answer: Optional[str] = None 
    tool_used: Optional[str] = None
    error: Optional[str] = None
    retrieved_chunks: Optional[str] = None


MCP_SERVERS ={
        "search_web": {
            "command": "python",
            
            "args": ["./mcp_servers/web_server.py"],
            "transport": "stdio",
        },
        "search_doc": {
            "command": "python",
            
            "args": ["./mcp_servers/doc_server.py"],
            "transport": "stdio",
        }
    }
mcp_client = None
mcp_tools = []

async def get_all_tools():
    global mcp_client, mcp_tools
    
    if MCP_SERVERS and not mcp_client:
        mcp_client = MultiServerMCPClient(MCP_SERVERS)
        mcp_tools = await mcp_client.get_tools()
    
    return mcp_tools




async def tool_decision_agent(state: ToolState) -> ToolState:
    """First agent: Decide if user explicitly requested tools."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    system_prompt = """
You are a routing agent that decides whether the user explicitly requested tool usage and gives a proper answer to the user's question.

IMPORTANT RULES:
1. ONLY use tools if the question EXPLICITLY requests document or web search.
2. If NO explicit keywords are found, respond with exactly "use_rag" and do NOT use any tools.
3. Your response should be either the tool result or exactly "use_rag".

Give a proper answer to the user's question if you have used the tools.
"""
    TOOLS = await get_all_tools()
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Question: {question}"),
        ("ai", "{agent_scratchpad}")
    ])
    agent = create_openai_functions_agent(
        llm,
        TOOLS,
        prompt=prompt
    )
    executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=True, return_intermediate_steps=True)
    
    try:
        result = await executor.ainvoke({
            "question": state.question,
            "agent_scratchpad": ""
        })
        
        
        if result["output"].strip().lower() == "use_rag":
            state.answer = "use_rag"
            state.tool_used = "none"
        else:
            state.answer = result["output"]
            state.tool_used = str(result.get("intermediate_steps", []))
        
        return state
    except Exception as e:
        state.error = f"Tool decision agent error: {str(e)}"
        return state



async def rag_agent(state: ToolState) -> ToolState:
    """Second agent: Use RAG to answer from retrieved chunks, fallback to web if needed."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    state.retrieved_chunks = search_document(state.question)
    
    chunks_text = state.retrieved_chunks if state.retrieved_chunks else "No chunks available"
    
    system_prompt = """
You are a RAG agent that answers questions based on retrieved chunks.

IMPORTANT RULES:
1. Analyze the question and the provided chunks carefully.
2. If you can provide a COMPLETE and ACCURATE answer using ONLY the chunks, do so.
3. If the chunks are insufficient, incomplete, or don't contain the information needed, use the search_web tool.
4. Your answer should be based ONLY on the provided chunks - do not use external knowledge unless using the web tool.
5. Be honest about whether the chunks contain enough information to answer the question.

Chunks provided:
{chunks}
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Question: {question}"),
        ("ai", "{agent_scratchpad}")
    ])

    TOOLS = await get_all_tools()

    agent = create_openai_functions_agent(
        llm,
        TOOLS,
        prompt=prompt
    )
    executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=True, return_intermediate_steps=True)
    
    try:
        result = await executor.ainvoke({
            "question": state.question,
            "chunks": chunks_text,
            "agent_scratchpad": ""
        })
        
        state.answer = result["output"]
        state.tool_used = str(result.get("intermediate_steps", []))
        return state
    except Exception as e:
        state.error = f"RAG agent error: {str(e)}"
        return state 