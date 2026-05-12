from src.file_types import DataSource
#pdf, csv, text, word loader
from langchain_community.document_loaders import PyPDFLoader,CSVLoader,TextLoader,Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing_extensions import TypedDict
from langgraph.graph import START,END, StateGraph
from langchain_mistralai import MistralAIEmbeddings
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore


load_dotenv()

# Langgraph Graph  design

# defind the states 
class IndexingState(TypedDict):
     path : str
     categotize_files : str
     load_files : str
     chunking_docs : str
     embedding_docs : str
     load_pdf_status : str
     load_docx_status : str
     load_csv_status : str
     load_txt_status : str
     chuncking_textsplitter_pdf_status : str
     chuncking_textsplitter_csv_status : str
     chuncking_textsplitter_txt_status : str
     chuncking_textsplitter_doc_status : str
     db_connection_vector_store : str
     load_pdf_doc : list
     load_csv_doc : list
     load_txt_doc : list
     load_word_doc : list
     category_file : dict
     chunks_pdf : list
     chunks_csv : list
     chunks_txt : list
     chunks_word : list


# define nodes
def node_categorize_file(state:IndexingState):
    data_source = DataSource()
    #categorized_files = data_source.scan_folder(state["path"])
    data_source.scan_folder(state["path"])
    for category, files in data_source.categorized_files.items():
        print(f"\n--- {category} ---")
        if category == 'PDF':
            for file in files:
                    print(file)

    return {"categotize_files": "Yes",
            "category_file" : data_source.categorized_files}

def node_load_file(state: IndexingState):
    temp_categorized_files = state["category_file"]

    pdf_load_doc = []
    csv_load_doc = []
    text_load_doc = []
    word_load_doc = []
    for category, files in temp_categorized_files.items():
        if category == 'PDF':
            for file in files:
                    pdf_loader =  PyPDFLoader(file,mode='page')
                    pdf_load = pdf_loader.load()
                    pdf_load_doc.extend(pdf_load)
            print(f'Number of PDF documents loaded --> {len(pdf_load_doc)}')

        if category == 'CSV':
            for file in files:
                  csv_loader = CSVLoader(file)
                  csv_load = csv_loader.load()
                  csv_load_doc.extend(csv_load)
            print(f'Number of CSV documents loaded --> {len(csv_load_doc)}')

        if category == 'Text':
            for file in files:
                  text_loader = TextLoader(file)
                  text_load = text_loader.load()
                  text_load_doc.extend(text_load)
            print(f'Number of Text documents loaded --> {len(text_load_doc)}')


        if category == 'Word':
            for file in files:
                
                word_loader = Docx2txtLoader(file)
                word_load = word_loader.load()
                word_load_doc.extend(word_load)
            print(f'Number of Word documents loaded --> {len(word_load_doc)}')  
    return {
        "load_doc_status" : "Yes",
        'load_word_doc': word_load_doc,
        "load_pdf_status" : "Yes",
        'load_pdf_doc' : pdf_load_doc,
        "load_csv_status" : "Yes",
        'load_csv_doc' : csv_load_doc,
        "load_txt_status" : "Yes",
        'load_txt_doc' : text_load_doc,
        'load_files' : "Yes"   
            }        

def node_chuncking_textsplitter_doc(state: IndexingState):

    pdf_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=300)
    csv_text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    txt_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=300)
    word_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=300)
    pdf_chunks = pdf_text_splitter.split_documents(state['load_pdf_doc'])
    csv_chunks = csv_text_splitter.split_documents(state['load_csv_doc'])
    txt_chunks = txt_text_splitter.split_documents(state['load_txt_doc'])
    word_chunks = word_text_splitter.split_documents(state['load_word_doc'])
    print(f' Chunking of loaded documents completed successfully..........')
    return{
        'chuncking_textsplitter_pdf_status' : "Yes",
        'chuncking_textsplitter_csv_status' : "Yes",
        'chuncking_textsplitter_txt_status' : "Yes",
        'chuncking_textsplitter_doc_status' : "Yes",
        'chunks_pdf' : pdf_chunks,
        'chunks_csv' : csv_chunks,
        'chunks_txt' : txt_chunks,
        'chunks_word' : word_chunks

    }
    

def node_db_connection_vectore_store(state: IndexingState):
    pdf_embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=os.getenv('MISTRAL_API_KEY'))
    csv_embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=os.getenv('MISTRAL_API_KEY'))
    word_embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=os.getenv('MISTRAL_API_KEY'))
    text_embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=os.getenv('MISTRAL_API_KEY'))
    print('LLM embedding models are created successfully...........')
    #used different embedding instance so that in future I can use different embedding models for high performance
    # embedded pdf -  low level design -  for manual vector creator
    # vector_pdf = pdf_embeddings.embed_documents(state['chunks_pdf'])
    # vector_csv = csv_embeddings.embed_documents(state['chunks_csv'])
    # vector_txt = text_embeddings.embed_documents(state['chunks_txt'])
    # vector_word = word_embeddings.embed_documents(state['chunks_word'])

    client = QdrantClient(
    host="localhost",
    port=6333 )
    
    vector_store_word = QdrantVectorStore.from_documents(
    documents=state["chunks_word"],
    embedding=word_embeddings,
    collection_name="rag_collection_word",
    url='http://localhost:6333/'
    )
    
    print(f'Successfully created embedding for word documents and vector store is created under "rag_collection_word"')
    vector_store_pdf = QdrantVectorStore.from_documents(
    documents=state["chunks_pdf"],
    embedding=pdf_embeddings,
    collection_name="rag_collection_pdf",
    url='http://localhost:6333/'
    )
    print(f'Successfully created embedding for pdf documents and vector store is created under "rag_collection_pdf"')


    vector_store_csv = QdrantVectorStore.from_documents(
    documents=state["chunks_csv"],
    embedding=csv_embeddings,
    collection_name="rag_collection_csv",
    url='http://localhost:6333/'
    )
    print(f'Successfully created embedding for wcsv documents and vector store is created under "rag_collection_csv"')

    vector_stortxt = QdrantVectorStore.from_documents(
    documents=state["chunks_txt"],
    embedding=text_embeddings,
    collection_name="rag_collection_txt",
    url='http://localhost:6333/'
    )
    print(f'Successfully created embedding for text documents and vector store is created under "rag_collection_txt"')

    return {
          "db_connection_vector_store" : "Yes"
     }


    

def builer(root_folder): 

    load_builder = StateGraph(IndexingState)

    load_builder.add_node("node_1", node_categorize_file)
    load_builder.add_node("node_2", node_load_file)
    load_builder.add_node("node_3", node_chuncking_textsplitter_doc)
    load_builder.add_node("node_4", node_db_connection_vectore_store)

    print("Graph nodes are created.......")
    load_builder.add_edge(START, "node_1")
    load_builder.add_edge("node_1", "node_2")
    load_builder.add_edge("node_2", "node_3")
    load_builder.add_edge("node_3", "node_4")
    load_builder.add_edge("node_4", END)
    print('Graph edges are created.......')
    graph = load_builder.compile() 

    final_state = graph.invoke({
        "path": root_folder
    })

    return {
         
         "embedding_state" : final_state}



     
     

