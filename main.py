from typing import Optional
from dotenv import load_dotenv
from workflow import run_langgraph_tool_workflow
from .utils.data_process import data_processor

load_dotenv()

async def main(pdf_bytes: Optional[bytes] = None, question: Optional[str] = None):
    """
    Main function to run the LangGraph workflow.
    
    Args:
        pdf_path: Optional path to a PDF file to upload and process
        question: The user's question
    """


    if pdf_bytes:
        success = data_processor.process_pdf(pdf_bytes)
        if success:
            print("PDF uploaded and processed successfully!")
        else:
            print("Failed to upload PDF")
            return
    
 
    if not question:
        question = input("\nWhat would you like to know? ")
    
    
    try:
        result = await run_langgraph_tool_workflow(question)
        
        # Display results
        print("\nRESULTS:\n\n")
  
        
        if result.error:
            print(f"Error: {result.error}")
        
        print(f"Tool Used: {result.tool_used}")
        
        if result.answer:
            print(f"\nAnswer:")
            print(result.answer)
        
        if result.retrieved_chunks:
            print(f"\nRetrieved Chunks:")
            print(result.retrieved_chunks)

    except Exception as e:
        print(f"Workflow failed: {e}")

