
from sentence_transformers import SentenceTransformer

class Embedding:

    def __init__(self, model_name : str = "sentence-transformers/LaBSE"):
        
        self.model = SentenceTransformer(model_name)
        

    def emb_text(self,text : str):

        embeddings = self.model.encode(text)
        return embeddings


        
