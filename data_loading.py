from src.utils.ingestion import file_loader,ppt_reader,preprocess


def data_load(folder_path : str = "./knowledge_base/corpus/processed" ):
    ppt_file_paths = file_loader.get_all_file_paths(folder_path)

    from src.utils.vectorstore import Milvus_init

    milvus = Milvus_init()
    print(milvus.initialize_collection(Drop_collection=True))
    try:
        for index,path in enumerate(ppt_file_paths):
            print(f"file {index + 1} out of {len(ppt_file_paths)} ")
            data = ppt_reader.extract_unknow_slide(path)
            process_data = preprocess.preprocess_text(data,path)
            # print(process_data)
            milvus.milvus_insert_data(process_data)
        return "upload successful"
    except Exception as e:
        print(e)