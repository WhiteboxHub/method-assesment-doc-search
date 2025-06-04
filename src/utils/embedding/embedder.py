
from sentence_transformers import SentenceTransformer
'''This class wraps a SentenceTransformer model (default: LaBSE) to convert text into dense embeddings. '''

class Embedding:

    def __init__(self, model_name : str = "sentence-transformers/LaBSE"):
        
        self.model = SentenceTransformer(model_name)
        '''Loads a pretrained sentence embedding model using the SentenceTransformer library.'''
        

    def emb_text(self,text : str):
        """Accepts a string (text). Returns its vector embedding (usually a NumPy array or list of floats)."""

        embeddings = self.model.encode(text)
        return embeddings


        
