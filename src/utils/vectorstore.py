
from pymilvus import (connections,
                      utility,
                      FieldSchema,
                      CollectionSchema,
                      DataType,
                      Collection,
                      MilvusClient)

from dotenv import load_dotenv
import os
from typing import Annotated
import threading


load_dotenv()

_mivus_thread = threading.Lock()



class Milvus_init:
    def __init__(self,embedding_dim = None, collection_name = None):
        self.COLLECTION_NAME = os.getenv("MILVUS_COLLECTION_NAME",collection_name)
        self.MILVUS_DB_ALIAS = os.getenv('MILVUS_DB_Alias')
        self.MILVUS_HOST = os.getenv("MILVUS_HOST","localhost")
        self.MILVUS_PORT = os.getenv("MILVUS_PORT","19530")
        self.MILVUS_URI = os.getenv("MILVUS_URI")
        self.MILVUS_TOKEN = os.getenv('MILVUS_TOKEN')
        self.CLIENT = MilvusClient(
                    uri= self.MILVUS_URI,
                    token = self.MILVUS_TOKEN
                )
        
    def initialize_collection(self,collection_name = None,Drop_collection = False):
        with _mivus_thread:
            try:
                if collection_name == None:
                    collection_name = self.COLLECTION_NAME
                
                if Drop_collection or collection_name not in self.CLIENT.list_collections() :
                    self.CLIENT.drop_collection(
                        collection_name=self.COLLECTION_NAME
                    )

                    db_schema = MilvusClient.create_schema(
                        auto_id = False
                    )

                    db_schema.add_field(field_name='pk', datatype=DataType.INT64, is_primary=True, auto_id= True)
                    db_schema.add_field(field_name='filename', datatype=DataType.VARCHAR,max_length = 500)
                    db_schema.add_field(field_name='file_title', datatype=DataType.VARCHAR,max_length = 500)
                    db_schema.add_field(field_name='embeddings', datatype=DataType.FLOAT_VECTOR,dim=768)
                    db_schema.add_field(field_name='embed_text', datatype=DataType.VARCHAR , max_length = 8000)
                    db_schema.add_field(field_name='slideno', datatype=DataType.INT64)
                    db_schema.add_field(field_name='isfullslide', datatype=DataType.BOOL)
                    db_schema.add_field(field_name='slide_title', datatype=DataType.VARCHAR, max_length = 10000)
                    # db_schema.add_field(field_name='text', datatype=DataType.VARCHAR , max_length = 800)

                    index_params = self.CLIENT.prepare_index_params()

                    index_params.add_index(
                        field_name="embeddings",
                        index_type="AUTOINDEX",
                        metric_type = "COSINE"
                    )


                    self.CLIENT.create_collection(
                        collection_name=self.COLLECTION_NAME,
                        schema = db_schema,
                        index_params=index_params
                    )

                    res = self.CLIENT.get_load_state(
                        collection_name=self.COLLECTION_NAME
                    )

                    return "Collection ceated successfully"
                

                
                return f"{self.COLLECTION_NAME} Collection already Exists. please drop the collection and try again 'drop_collection=True' "
            except Exception as e:
                print(e)
                return None
  
    def Client_connection(self):
        with _mivus_thread:
            try:
                return self.CLIENT
            except Exception as e:
                return None
            
    def milvus_insert_data_corpus(self,corpus_data : list[dict]):
        
        try:

            if self.COLLECTION_NAME not in self.CLIENT.list_collections():
                raise Exception
            

            insert_data = []

            for corpus in corpus_data:
                data = {}
                for key,value in corpus.items():
                    data[key]= value

                insert_data.append(data)
            res = self.CLIENT.insert(
                collection_name = self.COLLECTION_NAME,
                data = insert_data
            )
            return "data inserted successfully "
            
        except Exception as e:
            raise e
    
    def milvus_insert_data(self,data : list[dict]):
        try:
            print("insert started")
            connections.connect("default", host=self.MILVUS_HOST, port=self.MILVUS_PORT)
            insert_data = []
            print('connection 1')
            collection = Collection(self.COLLECTION_NAME)
            print('connection 2')
            
            collection.insert(data)
            print('connection 3')

            collection.flush()
            # for d in data:
            #     info = {}
            #     for key,value in d.items():
            #         info[key] = value
                
            #     insert_data.append(info)
            # res = self.CLIENT.insert(
            #     collection_name = self.COLLECTION_NAME,
            #     data = insert_data
            # )
            # inserting = milvusdb.insert(insert_data)
            # milvusdb.flush()
            print("data inserted successfully ")
            return "data inserted successfully "    

        except Exception as e:
            print(e)
            return f"Error: {e} has occured"
    # def milvus_insert_data(self, data: list[dict]):
    #     try:
    #         print("Insert started")
    #         connections.connect("default", host=self.MILVUS_HOST, port=self.MILVUS_PORT)

    #         # Load the collection
    #         collection = Collection(self.COLLECTION_NAME)

    #         # insert_data = []

    #         # d = {}
    #         # for i in data:
    #         #     for key,value in i.items():
    #         #         if d[key]:
    #         #             d[key].append(value)
    #         #         else:
    #         #             d[key] = [value]

    #         # for key,value in d.items():
    #         #     insert_data.append(value)
    #         # Validate schema and order fields properly
    #         field_names = [field.name for field in collection.schema.fields]

    #         # Milvus expects column-wise data (i.e., list of lists)
    #         insert_data = [[doc[field] for doc in data] for field in field_names]

    #         # Insert and flush
    #         print(insert_data)
    #         collection.insert(insert_data)
    #         collection.flush()

    #         print("Data inserted successfully")
    #         return "Data inserted successfully"

    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return f"Error: {e} has occurred"


