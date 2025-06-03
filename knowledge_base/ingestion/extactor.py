# from pptx import Presentation
# import os
# import json

# def extract_pptx_info(filepath):
#     # Load presentation
#     prs = Presentation(filepath)

#     # Metadata
#     core_props = prs.core_properties
#     metadata = {
#         "filename": os.path.basename(filepath),
#         "title": core_props.title,
#         "author": core_props.author
#     }

#     # Extract text slide by slide
#     slides = []
#     for i, slide in enumerate(prs.slides):
#         text_list = []
#         for shape in slide.shapes:
#             if hasattr(shape, "text"):
#                 text_list.append(shape.text.strip())

#         slide_data = {
#             "slide_number": i + 1,
#             "text": "\n".join(text_list)
#         }
#         slides.append(slide_data)

#     # Combine all data
#     result = {
#         "metadata": metadata,
#         "slides": slides
#     }

#     return result

# def save_to_json(data, output_path):
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)

# # Example usage
# if __name__ == "__main__":
#     file_path = "knowledge_base\Raw\Ajmeer2.pptx"  # Replace with your actual file path
#     output_json_path = "output1.json"

#     pptx_data = extract_pptx_info(file_path)
#     save_to_json(pptx_data, output_json_path)

#     print(f"Data extracted and saved to {output_json_path}")




# import os
# import json
# from pptx import Presentation
# from sentence_transformers import SentenceTransformer
# from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
# from pymilvus import utility

# # Connect to Milvus
# connections.connect("default", host="localhost", port="19530")

# # Define Milvus Collection Schema (only once)
# def create_collection_if_not_exists():
#     if "pptx_slides" not in utility.list_collections():
#         fields = [
#             FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#             FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
#             FieldSchema(name="slide_text", dtype=DataType.VARCHAR, max_length=1024),
#             FieldSchema(name="filename", dtype=DataType.VARCHAR, max_length=255),
#             FieldSchema(name="slide_number", dtype=DataType.INT64),
#             FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=255),
#             FieldSchema(name="author", dtype=DataType.VARCHAR, max_length=255),
#         ]
#         schema = CollectionSchema(fields, description="PPTX slide embeddings")
#         collection = Collection(name="pptx_slides", schema=schema)
#         collection.create_index(field_name="embedding", index_params={"metric_type": "COSINE", "index_type": "IVF_FLAT", "params": {"nlist": 128}})
#         collection.load()
#     else:
#         print("Collection already exists.")

# # Extract text and metadata from a single pptx file
# def extract_pptx(filepath):
#     prs = Presentation(filepath)
#     core_props = prs.core_properties
#     metadata = {
#         "filename": os.path.basename(filepath),
#         "title": core_props.title or "",
#         "author": core_props.author or ""
#     }
#     slides = []
#     for i, slide in enumerate(prs.slides):
#         text = "\n".join([shape.text.strip() for shape in slide.shapes if hasattr(shape, "text")])
#         if text:
#             slides.append({
#                 "slide_number": i + 1,
#                 "text": text,
#                 **metadata
#             })
#     return slides

# # Process all .pptx files and insert to Milvus
# def process_and_store(folder_path):
#     model = SentenceTransformer("all-MiniLM-L6-v2")
#     collection = Collection("pptx_slides")
    
#     for file in os.listdir(folder_path):
#         if file.endswith(".pptx"):
#             full_path = os.path.join(folder_path, file)
#             slides = extract_pptx(full_path)
#             for slide in slides:
#                 embedding = model.encode(slide["text"]).tolist()
#                 data = [
#                     [embedding],
#                     [slide["text"]],
#                     [slide["filename"]],
#                     [slide["slide_number"]],
#                     [slide["title"]],
#                     [slide["author"]]
#                 ]
#                 collection.insert(data)

#     collection.flush()
#     print("All data inserted into Milvus.")

# if __name__ == "__main__":
#     create_collection_if_not_exists()
#     process_and_store(r"knowledge_base/corpus/raw")  # Your folder with pptx_







from pptx import Presentation
import os
import json

def extract_pptx_info(filepath):
    prs = Presentation(filepath)

    # Metadata
    core_props = prs.core_properties
    metadata = {
        "filename": os.path.basename(filepath),
        "title": core_props.title,
        "author": core_props.author
    }

    # Extract text slide-by-slide
    slides = []
    for i, slide in enumerate(prs.slides):
        text_list = []
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                text_list.append(shape.text.strip())

        slide_data = {
            "slide_number": i + 1,
            "text": "\n".join(text_list)
        }
        slides.append(slide_data)

    return {
        "metadata": metadata,
        "slides": slides
    }

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def process_all_pptx_in_folder(folder_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(folder_path):
        if file.endswith(".pptx"):
            file_path = os.path.join(folder_path, file)
            print(f"Processing: {file_path}")
            extracted_data = extract_pptx_info(file_path)

            output_filename = os.path.splitext(file)[0] + ".json"
            output_path = os.path.join(output_folder, output_filename)

            save_to_json(extracted_data, output_path)
            print(f"Saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    input_folder = r"knowledge_base\corpus\raw"        # <-- Update if needed
    output_folder = r"knowledge_base\corpus\JsonOut"   # <-- Output JSONs will be saved here

    process_all_pptx_in_folder(input_folder, output_folder)