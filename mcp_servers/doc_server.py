from mcp.server.fastmcp import FastMCP
from ..utils.data_process import data_processor

mcp = FastMCP()

@mcp.tool()
async def search_document(question: str) -> str:
    """Search the provided document for relevant context to answer the question."""
    try:
        
        chunks = data_processor.search(question, k=5)
        
        if chunks:
            
            context = "\n\n".join(chunks)
            return context
        else:
            return "No relevant information found in the uploaded documents."
            
    except Exception as e:
        return f"Error searching documents: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")