from data_process import data_processor


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

