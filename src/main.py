from src.indexing import builer
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# load_dotenv()

ROOT_FOLDER = os.environ.get("GCS_BUCKET_NAME")
#ROOT_FOLDER = r"C:\Users\RanjithBalasubramani\OneDrive - IBM\Desktop\AI\Mistral AI\RAG\test_folder_rag"
# /* provide the google cloud bucket name and pass it to root folder */

app =  FastAPI()
@app.get("/health")          # ← Cloud Run startup probe points here
def health():
    return {"status": "ok"}  


@app.get("/index")
def indexing():
    print("GCP Bucket name" , ROOT_FOLDER)
    indexing_status = builer(ROOT_FOLDER)
    print("GCP Bucket name" , ROOT_FOLDER)
    return {
        "Indexing_status" : indexing_status
    }





