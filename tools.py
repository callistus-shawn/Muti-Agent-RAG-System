from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from dotenv import load_dotenv
from data_process import data_processor
load_dotenv()

@tool
def search_document(question: str) -> str:
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

web_search_tool = TavilySearchResults()

@tool
def search_web(query: str) -> str:
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