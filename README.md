# Muti-Agent-RAG-System

* Engineered a LangGraph-based system with multiple agents that dynamically decide between document retrieval and web search using LLM-driven reasoning based on query context and content relevance.
* Set up two separate MCP tool servers, one for document search and one for web search and integrated them into the agent workflow.
* Integrated FastAPI for PDF upload and question handling, with document parsing, embedding, and similarity search. Implemented intelligent fallback from document context to web tools when information was insufficient.

<div align="center">
  <img src="graph/langgraph_visualization.png" height="400" width="200" />
</div>

## 📁 Project Structure

| File           | Description |
|----------------|-------------|
| `app.py`       | Sets up the FastAPI app and defines the endpoint for PDF upload and question answering. |
| `main.py`      | Runs the whole RAG workflow to answer questions. |
| `workflow.py`  | Configures and runs the LangGraph-based agent workflow. |
| `mcp_agent.py` | Agent routing logic that dynamically selects document or web search tools based on query context. |

### 📂 `mcp_servers/` – MCP Tools

| File           | Description |
|----------------|-------------|
| `doc_server.py`       | Launches document search tool server for retrieving semantic chunks from parsed PDFs. |
| `web_server.py`       | Launches web search tool server to answer queries from the internet. |


### 📂 `utils/` – Document and Vectorstore Utilities

| File           | Description |
|----------------|-------------|
| `doc_process.py`      | Parses PDF documents, chunks content, generates embeddings, and manages the vector store.  |
| `search_doc.py`       | Implements semantic search logic to retrieve relevant chunks from the vector store.|
