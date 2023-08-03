#step-5 save vector DB
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import openai
import os
import sys
from config import (
proxy,embedding_conf
)


    # Create embedding

def get_embedding_return_array_or_list_of_array(text_list, model="text-embedding-ada-002"):
        #输入一个list of string，获得一个list of embedding array 
        #        (a list of lists of floats: [[float, float...],[float, float...]...])
        #或者输入一个sting，获得单个的embedding array (a list of floats)
        # print(" Embedding.....................")
        

    # proxy = 'http://100.72.64.19:12798'
    # proxy = '127.0.0.1:2001'

    os.environ['http_proxy'] = proxy['proxy'] 
    os.environ['HTTP_PROXY'] = proxy['proxy']
    os.environ['https_proxy'] = proxy['proxy']
    os.environ['HTTPS_PROXY'] = proxy['proxy']


    openai.api_key = embedding_conf['embedding']['api_key']
    openai.api_base = embedding_conf['embedding']['api_base']
    openai.api_type = 'azure'
    openai.api_version = embedding_conf['embedding']['api_version']
    api_engine: str = embedding_conf['embedding']['api_engine']
    

        
    return_list=True
    if isinstance(text_list, str):
        text_list = [text_list]
        return_list = False
    elif isinstance(text_list, list):
        return_list = True
    else:
        raise ValueError("get_embedding_return_array_or_list_of_array only accept a single string or a list of strings")
 
    #Azure
    MAX_RETRIES = 3
    DELAY = 5
    import time

    result_list=[]
    for i in range(MAX_RETRIES):
        try:
            for doc in text_list:
                # print(f'embedding...{doc[:10]}')
                response = openai.Embedding.create(
                    input=[doc],    
                    engine="text-embedding-ada-002" )
                result_list.append(response["data"][0]["embedding"])
            break
        except Exception as e:
            print(e)
            
        time.sleep(DELAY)
    if len(result_list)==0:return ''
    return result_list if return_list == True else result_list[0]

class VectorDB:
    def __init__(self):
        self.db = chromadb.Client(Settings(chroma_db_impl = "duckdb+parquet", persist_directory="/root/temp/poc_db_gxp"))
        self.collection = self.db.get_or_create_collection(name = "poc_db")
        
    def embedding_query(self, query_embeddings, query_texts=None, n_results=20,
              where=None, where_document=None):
        return self.collection.query(
            query_embeddings=get_embedding_return_array_or_list_of_array(query_embeddings),
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            where_document=where_document
        )

    def embedding_query_byids(self, query_embeddings, query_texts=None, n_results=1,
              where=None, where_document=None):
        return self.collection.query(
            query_embeddings=get_embedding_return_array_or_list_of_array(query_embeddings),
            query_texts=query_texts,
            n_results=n_results,
            where={'ids':query_embeddings[0]},
            where_document=where_document
        )
    
    



if __name__ == "__main__":
    # def comeback_list_from_pickle(file_name):
    #     import pickle
    #     path="D:/Users/86188/PycharmProjects/db"
    #     with open(f"{path}\{file_name}.pickle",'rb') as f:
    #         return pickle.load(f)
        

    db = chromadb.Client(Settings(
        chroma_db_impl = "duckdb+parquet", 
        persist_directory=r"/root/temp/poc_db_gxp")
        )
    collection = db.get_or_create_collection(name = "vector_DB")
    # embeddings = comeback_list_from_pickle("embedding_vector_230702")
    # documents = comeback_list_from_pickle("documents_m_230702")
    # ids = comeback_list_from_pickle("ids_m_230702")
    # metadatas = comeback_list_from_pickle("metadatas_m_230702")
    print("pickel.........Done")
    # collection.add(
    # documents=documents, # we embed for you, or bring your own
    # metadatas=metadatas, # filter on arbitrary metadata!
    # embeddings=embeddings,# embedding by openAI
    # ids=ids, # must be unique for each doc 
    # )
    # db.persist()
    # print("-Persist-----------------Done")
    # print(collection.count())
    # print("check ......")
    query_embeddings=get_embedding_return_array_or_list_of_array(["SCNT"])
    results = collection.query(
        query_embeddings=query_embeddings,
        # query_texts=["SCNT technology"],
        n_results=3
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    ) 
    print(results)
    print("------------------------Done")
