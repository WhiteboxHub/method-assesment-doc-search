# from pymilvus import FieldSchema, CollectionSchema, DataType, Collection, connections

# def create_collection():
#     # Connect to Milvus
#     connections.connect(alias="default", host="localhost", port="19530")

#     # Define schema
#     fields = [
#         FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#         FieldSchema(name="document_name", dtype=DataType.VARCHAR, max_length=512),
#         FieldSchema(name="chunk_text", dtype=DataType.VARCHAR, max_length=2048),
#         FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
#         FieldSchema(name="created_ts", dtype=DataType.INT64),
#     ]

#     schema = CollectionSchema(fields, description="Store PDF document chunks with embeddings")

#     # Create collection
#     collection_name = "pdf_docs"
#     if Collection.exists(collection_name):
#         print(f"Collection '{collection_name}' already exists.")
#         return

#     collection = Collection(name=collection_name, schema=schema)                     

#     # Create vector index
#     index_params = {
#         "metric_type": "COSINE",
#         "index_type": "IVF_FLAT",
#         "params": {"nlist": 128}
#     }
#     collection.create_index(field_name="embedding", index_params=index_params)

#     # Load into memory
#     collection.load()
#     print(f"Collection '{collection_name}' created and loaded.")


# if __name__ == "__main__":
#     create_collection()



from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, utility



def connect_to_milvus(host="localhost", port="19530"):
    connections.connect(alias="default", host=host, port=port)

def create_pdf_collection(collection_name="pdf_docs"):
    connect_to_milvus()

    if utility.has_collection(collection_name):
        print(f"Collection '{collection_name}' already exists.")
        return

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="document_name", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="chunk_text", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
        FieldSchema(name="created_ts", dtype=DataType.INT64)
    ]

    schema = CollectionSchema(fields=fields, description="PDF document chunks with embeddings")
    collection = Collection(name=collection_name, schema=schema)

    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    collection.load()

    print(f"Collection '{collection_name}' created and loaded.")


if __name__ == "__main__":
    create_pdf_collection()
