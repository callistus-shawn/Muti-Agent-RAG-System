from fastapi import FastAPI, UploadFile, File, Form
from dotenv import load_dotenv
from .utils.data_process import data_processor

from fastapi import FastAPI, UploadFile, File, Form
from main import main

load_dotenv()

app = FastAPI()

@app.post("/ask_pdf")
async def ask_pdf(
    question: str = Form(...),
    pdf: UploadFile = File(None)
):
    data_processor.clear_vectorstore()
    print("cleared")
    if pdf:
        file_content = await pdf.read()
        await main(pdf_bytes=file_content, question=question)
    else:
        await main(question=question)
    
    result="done"
 

    return {"result": result}   
