from src.indexing import builer
from fastapi import FastAPI


ROOT_FOLDER = r"C:\Users\RanjithBalasubramani\OneDrive - IBM\Desktop\AI\Mistral AI\RAG\test_folder_rag"

app =  FastAPI()
@app.get("/")
def indexing():
    indexing_status = builer(ROOT_FOLDER)
    return {
        "Indexing_status" : indexing_status
    }



