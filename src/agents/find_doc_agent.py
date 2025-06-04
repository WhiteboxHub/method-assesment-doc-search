from typing import List

def find_docs(docs):
        

    """Search for documents that contain specific information"""
    # file_name , slide no , filetitle

    filter_data = []

    for doc in docs:
        filter_data.append({"file_location":doc.get("filename"),"slide no":doc.get('slideno')})
    

    return filter_data