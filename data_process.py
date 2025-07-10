from typing import List
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class DataProcessor:
    def __init__(self):
        """Initialize PDF processor with fresh vector store."""
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=0,
        )
        
        self.vectorstore = Chroma(
            embedding_function=self.embeddings
        )
    def clear_vectorstore(self):
        """Clear the vector store."""
        self.vectorstore = Chroma(embedding_function=self.embeddings)
    
    def process_pdf(self, pdf_bytes: bytes) -> bool:
        """Process PDF and add to vector store."""
        try:
     
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            
     
            chunks = self.text_splitter.split_text(text)
          
            
            self.vectorstore.add_texts(
                texts=chunks
            )
            
            print(f"Successfully processed and added {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"Error processing PDF : {e}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[str]:
        """Search documents in vector store."""
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []


data_processor = DataProcessor() 