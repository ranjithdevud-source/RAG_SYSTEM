import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_mistralai import MistralAIEmbeddings

load_dotenv()

main_assistant_tools=[
        {
            "type": "function",
            "function": {
                "name": "extract_vector_store_documents",
                "description": "Use this tool to retrieve document contents related to user query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_message": {
                            "type":"string",
                            "description": "The query requested by the user"
                        },
                        "retreived_contents": "The output of the tools which is documents reterevied from the vector_db"

                    },
                    "required": ["user_message", "retreived_contents"]
                }
            }
        },
          {
            "type": "function",
            "function": {
                "name": "validate_vector_store_documents",
                "description": "Use this tool to validate document contents related to user query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_message": {
                            "type":"string",
                            "description": "The query requested by the user"
                        },
                        "retreived_contents": "The output of the tools which is documents reterevied from the vector_db"

                    },
                    "required": ["user_message", "retreived_contents"]
                }
            }
        },

    ]

qdrant_url="https://261344c1-e380-420e-bcbe-7e178c6f2927.us-east4-0.gcp.cloud.qdrant.io:6333" 
qdrant_api_key=os.getenv('QDRANT_CLOUD_API_KEY')
embeddings = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=os.getenv("MISTRAL_API_KEY")
    )

def get_vector_store(collection_name):
    vector_store= QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=collection_name,
        url=qdrant_url, api_key=qdrant_api_key
    )
    return vector_store

def get_similarity_search_with_score(vector_store, user_input):
    vector_store_result = vector_store.similarity_search_with_score(
        query=user_input, k=5 
    )

def extract_vector_store_documents(user_input):

    vector_store_pdf = get_vector_store('rag_collection_pdf')
    vector_store_csv = get_vector_store('rag_collection_csv')
    vector_store_word = get_vector_store('rag_collection_word')
    vector_store_txt = get_vector_store('rag_collection_txt')

    vector_store_result_pdf = get_similarity_search_with_score(vector_store_pdf, user_input)
    vector_store_result_csv = get_similarity_search_with_score(vector_store_csv, user_input)
    vector_store_result_txt = get_similarity_search_with_score(vector_store_csv, user_input)
    vector_store_result_word = get_similarity_search_with_score(vector_store_word, user_input)

    return {
        "vector_store_result_pdf" : vector_store_result_pdf,
        "vector_store_result_csv" : vector_store_result_csv,
        "vector_store_result_txt" : vector_store_result_txt,
        "vector_store_result_word" : vector_store_result_word,
    }


