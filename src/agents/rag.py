from src.utils.vectorstore import Milvus_init
from src.utils.ingestion.preprocess import process_retrived_text
m = Milvus_init()

def data_retriver(text : str):
    
    data = m.retriver(text)

    retrived_data = []

    for d in data:
        for i in d:
            retrived_data.append(process_retrived_text(str(i)))
    return retrived_data



