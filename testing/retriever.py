# from langchain_community.vectorstores import Milvus
# from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain_community.retrievers import BM25Retriever
# from langchain.retrievers import EnsembleRetriever
# from langchain.schema import Document


# def create_hybrid_retriever(collection_name="langchain_milvus", k=4, embedding_model_name="all-MiniLM-L6-v2"):
#     """
#     Create a hybrid retriever combining Milvus (semantic search) and BM25 (keyword).
    
#     Args:
#         collection_name: Name of the Milvus collection.
#         k: Number of documents to retrieve.
#         embedding_model_name: SentenceTransformer model name.
        
#     Returns:
#         A hybrid EnsembleRetriever instance.
#     """
#     # Setup the embedding function
#     embedding_function = SentenceTransformerEmbeddings(model_name=embedding_model_name)

#     # Connect to Milvus and wrap with LangChain
#     vector_store = Milvus(
#         embedding_function=embedding_function,
#         collection_name=collection_name,
#         connection_args={"host": "localhost", "port": "19530"}
#     )

#     # Create a retriever for Milvus
#     milvus_retriever = vector_store.as_retriever(search_kwargs={"k": k})

   
   
#     # So we must assume you have access to the original documents separately.
#     # If not, you cannot build a BM25 retriever.

#     # Placeholder: Load your original docs from wherever you indexed them
#     # Example:
#     # all_docs = load_documents_from_disk_or_source()
#     # For demo:
#     all_docs = vector_store.similarity_search(" ", k=1000)  # get all docs via dummy query

#     # Filter only valid Documents
#     all_docs = [doc for doc in all_docs if isinstance(doc, Document)]

#     # BM25 keyword-based retriever
#     bm25_retriever = BM25Retriever.from_documents(all_docs)
#     bm25_retriever.k = k

#     # Combine them in a hybrid retriever
#     hybrid_retriever = EnsembleRetriever(
#         retrievers=[milvus_retriever, bm25_retriever],
#         weights=[0.5, 0.5]
#     )

#     return hybrid_retriever

# print("done ")

from pymilvus import connections, Collection, utility, FieldSchema, CollectionSchema, DataType
from langchain_community.vectorstores import Milvus
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.schema import Document

def create_hybrid_retriever_milvus(
    collection_name: str,
    documents: list[Document],
    host: str = "localhost",
    port: str = "19530",
    k: int = 4,
    embedding_model_name: str = "all-MiniLM-L6-v2"
):
    # Step 1: Connect to Milvus
    connections.connect("default", host=host, port=port)

    # Step 2: Define schema (if it doesn’t already exist)
    if not utility.has_collection(collection_name):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
        ]
        schema = CollectionSchema(fields, description="Hybrid search test")
        collection = Collection(name=collection_name, schema=schema)
    else:
        collection = Collection(name=collection_name)

    # Step 3: Create HNSW index on the vector field
    index_params = {
        "index_type": "HNSW",
        "metric_type": "L2",
        "params": {"M": 16, "efConstruction": 200}
    }

    if not collection.has_index():
        collection.create_index(field_name="embedding", index_params=index_params)

    # Step 4: Embed documents
    embedding_fn = SentenceTransformerEmbeddings(model_name=embedding_model_name)
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]
    embeddings = embedding_fn.embed_documents(texts)

    # Step 5: Insert into Milvus
    if collection.num_entities == 0:
        collection.insert([
            embeddings,  # embedding vectors
            texts        # original texts
        ])
        collection.flush()

    # Step 6: Create Milvus retriever (semantic)
    milvus_vectorstore = Milvus(
        embedding_function=embedding_fn,
        collection_name=collection_name,
        connection_args={"host": host, "port": port}
    )
    milvus_retriever = milvus_vectorstore.as_retriever(search_kwargs={"k": k})

    # Step 7: Create BM25 retriever (keyword)
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = k

    # Step 8: Combine into hybrid retriever
    hybrid_retriever = EnsembleRetriever(
        retrievers=[milvus_retriever, bm25_retriever],
        weights=[0.5, 0.5]
    )

    return hybrid_retriever

print("hello ")

from langchain.schema import Document

# Sample documents to be inserted
sample_docs = [
    Document(page_content="The Eiffel Tower is located in Paris.", metadata={"id": "doc1"}),
    Document(page_content="Mount Everest is the highest mountain on Earth.", metadata={"id": "doc2"}),
    Document(page_content="The Great Wall of China is visible from space.", metadata={"id": "doc3"}),
    Document(page_content="Paris is known for its cafes and the Eiffel Tower.", metadata={"id": "doc4"}),
    Document(page_content="K2 is the second-highest mountain after Everest.", metadata={"id": "doc5"})
]

# Create the hybrid retriever
retriever = create_hybrid_retriever_milvus(
    collection_name="test_collection_hybrid",
    documents=sample_docs,
    k=3  # top-3 results
)

# Test queries
test_queries = [
    "Where is the Eiffel Tower?",      # Should retrieve doc1 and doc4
    "Tallest mountain?",               # Should retrieve doc2
    "Chinese landmarks visible from space"  # Should retrieve doc3
]

# Run test queries
for i, query in enumerate(test_queries):
    print(f"\n--- Query {i+1}: {query} ---")
    results = retriever.get_relevant_documents(query)
    for idx, doc in enumerate(results):
        print(f"Result {idx+1}: {doc.page_content} (metadata: {doc.metadata})")
