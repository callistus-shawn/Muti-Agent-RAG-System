from langchain_community.tools.tavily_search import TavilySearchResults
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

web_search_tool = TavilySearchResults()

mcp = FastMCP()
@mcp.tool()
async def search_web(query: str) -> str:
    """Search the web for up-to-date information to answer the question."""
    results = web_search_tool.invoke(query)
    if isinstance(results, list):
        context = "\n\n".join(
            f"Title: {r.get('title', '')}\nSnippet: {r.get('content', '')}"
            for r in results
        )
    else:
        context = str(results)
    return context or "No relevant information found on the web." 


if __name__ == "__main__":
    mcp.run(transport="stdio")