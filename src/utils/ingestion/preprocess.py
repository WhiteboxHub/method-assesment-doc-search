from typing import List
from src.utils.embedding.embedder import Embedding

def preprocess_text(data: List[dict], file_name: str):
    embed = Embedding()
    insert_data = []
    doc_title = ""

    for d in data:
        elements = d.get('elements', [])
        if not elements:
            continue  # skip if there are no elements

        if d.get('slideno') == 1:
            doc_title = elements[0].get('text', '')

        s_title = elements[0].get('text', '')

        for ele in elements:
            text = ele.get('text', '')
            if len(text) > 5:
                doc = {
                    'filename': file_name,
                    'file_title': doc_title,
                    'embed_text': text,
                    'slideno': d.get('slideno'),
                    'isfullslide': False,
                    'slide_title': s_title,
                    'embeddings': embed.emb_text(text)
                }
                insert_data.append(doc)

        # Now insert the full slide data
        raw_text = d.get('raw_text', '')
        doc = {
            'filename': file_name,
            'file_title': doc_title,
            'embed_text': raw_text,
            'slideno': d.get('slideno'),
            'isfullslide': True,
            'slide_title': doc_title,
            'embeddings': embed.emb_text(raw_text)
        }
        insert_data.append(doc)

    return insert_data
