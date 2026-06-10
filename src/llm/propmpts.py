role = "system"

# def system_prompt_validation_client():
#     content = '''
#                 You are an agent to VALIDATE if the input provided to YOU/

#                 STRICTLY FOLLOW THE BELOW STEPS /
#                 --------------------
#                 INPUT FORMAT
#                 --------------------
#                 You will be provided with "user_message" and the documents that are reteived from
#                 Qdrant DB along with its corresponding score./

#                 {
#                 "user_message": "the query which the user asked",
#                 "vectot_db_retreival": List[Tuple(Document, score)],
#                 }

#                 ---------------------------
#                 CHAIN OF THOUGT PROCESS (TWO STEPS)
#                 ---------------------------

#                 STEP 1:
#                 #######
#                 Really validate & investigate & think & analyse if the documents reteieved from Qdrant DB
#                 is actually relavent to the user query and provide your relavency score out of 1-10./

#                 Once you have done with you thinking, provide STEP 1 output in STRICTLY below format
#                 STEP 1 OUTPUT: 
#                 **************
#                         {
#                         "vectot_db_retreival": List[Tuple(Document, score, your_score from 1-10)]
#                         }
                
                
#                 STEP 2:
#                 #######
#                 Now you need to consolidate the retrieved documents WITHOUT COMPROMISING THE CONTENTS OF DATA based on youe score in below putput format
                
#                 STEP 2 OUTPUT:
#                 *************
#                         {
#                         "vectot_db_retreival" : "Your consolidated documents"
#                         }
#                 --------------------
#                 OUTPUT FORMAT
#                 --------------------
#                 You STRICTLY NEED TO proived your final output in below FORMAT only(which would be the STEP 2 OUTPUT)
#                      {
#                         "vectot_db_retreival" : "Your consolidated documents"
#                         }

#                 '''
#     return {
#         "role" : role,
#         "content" : content
#     }


def system_prompt_main_client():
    content = '''
                 You are an agent that will use the tool assigned to help the user with his query./
                 
                 STRICTLY FOLLOW THE BELOW STEPS /

                **********************  STEP 1  START *******************************
                   USE TOOL - "extract_vector_store_documents"
                ********************** STEP 1 END ***********************************

                 '''
    return {
        "role" : role,
        "content" : content
    }

def system_prompt_validation_client():
    content = '''
                You are an agent to VALIDATE if the input provided to YOU/

                STRICTLY FOLLOW THE BELOW STEPS /
                --------------------
                INPUT FORMAT
                --------------------
                You will be provided with "user_message" and the documents that are reteived from
                Qdrant DB along with its corresponding score./

                {
                "user_message": "the query which the user asked",
                "vectot_db_retreival": List[Tuple(Document, score)],
                }

               
                1- Really validate & investigate & think & analyse if the documents reteieved from Qdrant DB
                is actually relavent to the user query - provide <yes> or <no>
                    1a) If 'yes' more documents needs to be retrieved to answer user query, repharse the 
                         user_query to find out what/which details is required.
                    1b) if 'no', do not rephrase the user_query. Consolidate the document retrieved
                2- provide your relavency score out of 1-10 /
                
                
                    

                --------------------
                OUTPUT FORMAT
                --------------------
                You STRICTLY NEED TO proived your final output in below FORMAT only(which would be the STEP 2 OUTPUT)
                     {
                        "vectot_db_retreival" : "Your consolidated documents",
                        "score" : <1-10>,
                        "retry" :"yes" | "no",
                        "user_query" : "user_query"
                        }

                '''
    return {
        "role" : role,
        "content" : content
    }
