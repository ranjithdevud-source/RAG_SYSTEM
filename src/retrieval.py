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
from mistralai import MistralAI
from src.llm.propmpts import system_prompt_main_client, system_prompt_validation_client
from src.llm.models import main_client, validation_client
from src.llm.tools import extract_vector_store_documents


load_dotenv()
'''
1- Get user input - map to fastapi put request
2- load Mistral to accept the user input; define system prompt
3- embeded the user input 
4- load the qdrant db vector store
5- retrieve the corresponding vectors from Q-DB
6- Pass both the score, user input & vector response to another agent to validate
7- once validated, send to main LLM, if not retrieved properly search again the db
8- once the loop is complete, send to main LLM
9- LLM will send message to user'''

class RetrievalState(TypedDict):
    main_client_message_history : list
    user_input : str
    main_client_response : dict
    main_tool_response : dict
    validation_client_response : dict
    main_client_tool_inovked : str
    validation_client_response_retry : str
    validation_client_reposne_message : str
    source_documents : list
    tool_response : dict




def get_user_query(state:RetrievalState):
    '''
    Gets user query and generates the main assistant system prompt
    '''
    user_input = input("-----> ")
    messages = [
        system_prompt_main_client(),
        {
        "role" : "user",
        "content" : user_input
    }]

    return {
        'main_client_message_history' : messages,
        'user_input' : user_input
    }

def get_main_client_response(state:RetrievalState):
    main_client_response = main_client(state['main_client_messages_history'])
    message = list(
        state['main_client_messages_history'].append(
            {
        "role" : "assistant",
        "content": main_client_response.choices[0].messages.content,
        "tool_calls" : main_client_response.choices[0].messages.tool_calls
    }
    )
    )

    return {
        'main_client_message_history' : message,
        'main_client_response' : main_client_response 
    }

def router(state:RetrievalState):
    
    if state['main_client_response'].choice[0].messages.tool_calls == 'extract_vector_store_documents':
        return "route_to_execute_main_client_tool"
    if state['main_client_response'].choice[0].messages.tool_calls == None:
        return "route_to_put_main_client_response"
    if state['validation_client_response_retry'] == 'yes':
        return "reteieve_from_sources"
    if state['validation_client_response_retry'] == 'no':
        return "route_to_put_main_client_response"
    

def execute_main_client_tool(state:RetrievalState):
    # main_client_response_tool_calls = state['main_client_response'].choice[0].messages.tool_calls
    # if main_client_response_tool_calls == 'extract_vector_store_documents':
    #     main_tool_response = list(
    #         {
    #             "role" : "tool",
    #             "content" : extract_vector_store_documents(state['user_input'])
    #         }
    #     )    
    # else:
    #     print('Agent did not call the tool and no messages was retrieved')
    # history = [state['main_client_message_history'].append(main_client_response_content)]

    documents_reteieved = list(extract_vector_store_documents(state['user_input']))
    tool_response = {
        {
    "role": "tool",
    "tool_call_id": state['main_client_response'].choice[0].messages.tool_calls[0].id,
    "name": "extract_vector_store_documents",
    "content": documents_reteieved
        }
    }
    return {
            'source_documents' : documents_reteieved,
            'tool_response' : tool_response
    }

def execute_validation_client(state:RetrievalState):
    messages = [
        system_prompt_validation_client(),
        {
        "role" : "user",
        "content" : state['source_documents']
    }]
    validation_client_response = validation_client(messages)
    return{
        'validation_client_response_retry' : validation_client_response.choices[0].message['retry'],
        'validation_client_reposne_message' : validation_client_response.choices[0].message['vectot_db_retreival'],
        'user_input' : validation_client_response.choices[0].message['user_input']
    }

def retry_db_extract_for_info(state:RetrievalState):
    messages = [
        system_prompt_validation_client(),
        {
        "role" : "user",
        "content" : state['user_input']
    }]
    validation_client_response = validation_client(messages)
    return{
        'validation_client_response_retry' : validation_client_response.choices[0].message['retry'],
        'validation_client_reposne_message' : validation_client_response.choices[0].message['vectot_db_retreival'],
        'user_input' : validation_client_response.choices[0].message['user_input']
    }

def route_to_main_client(state:RetrievalState):
    # update the state variable with the validation client output to main client tool
    tool_response = {
         "role": "tool",
        "tool_call_id": state['tool_response']['tool_call_id'],
    "name": "extract_vector_store_documents",
    "content": state['validation_client_reposne_message']
    }

    message_history = list(state['main_client_message_history'],tool_response)
    

    return {'tool_response' : tool_response,
            'main_client_message_history' : message_history }


def builer(root_folder): 

    load_builder = StateGraph(RetrievalState)

    load_builder.add_node("node_user_query", get_user_query)
    load_builder.add_node("node_main_client", get_main_client_response)
    load_builder.add_node("node_router", router)
    load_builder.add_node("node_tool", execute_main_client_tool)
    load_builder.add_node("node_validation_client",execute_validation_client)
    load_builder.add_node("node_retry",retry_db_extract_for_info)
    load_builder.add_node("node_return_to_main",route_to_main_client)


    print("Graph nodes are created.......")
    load_builder.add_edge(START, "node_user_query")
    load_builder.add_edge("node_user_query", "node_main_client")
    load_builder.add_edge("node_main_client", "node_router")
    load_builder.add_edge("node_3", "node_4")
    load_builder.add_edge("node_4", END)
    print('Graph edges are created.......')
    graph = load_builder.compile() 

    final_state = graph.invoke({
        "path": root_folder
    })

    return {
         
         "embedding_state" : final_state}

