from langgraph.graph import StateGraph, END
from mcp_agent import ToolState, tool_decision_agent, rag_agent

def route_after_tool_decision(state: ToolState) -> str:
    """Route after tool decision agent."""
    if state.answer == "use_rag":
        return "retrieve_chunks"
    else:
        return END

def create_langgraph_tool_workflow():
    workflow = StateGraph(ToolState)
    
    workflow.add_node("tool_decision_agent", tool_decision_agent)
    
    workflow.add_node("rag_agent", rag_agent)
    
    workflow.set_entry_point("tool_decision_agent")
 
    workflow.add_conditional_edges(
        "tool_decision_agent",
        route_after_tool_decision,
        {
            "retrieve_chunks": "rag_agent",
            END: END
        }
    )
    workflow.add_edge("rag_agent", END)
    
    return workflow

async def run_langgraph_tool_workflow(question: str):
    initial_state = ToolState(question=question)
    workflow = create_langgraph_tool_workflow()
    
    app = workflow.compile()
    result = await app.ainvoke(initial_state)

    if isinstance(result, dict):
        result = ToolState(**result)
    return result
