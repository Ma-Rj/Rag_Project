#Chroma
collection_name = 'rag'
embedding_model = 'text-embedding-v4'
persist_directory = './chroma_db'
similarity_threshold = 1   #相似度检索阈值，检索返回的匹配文档数量


#spliter
chunk_size = 1000
chunk_overlap = 100
separators =["，", "。", "？","！", "", " ", ",", ".", "?","!","\n\n", "\n"]
max_split_char_number = 1000 #文本分割阈值


chat_model_name = "qwen3-max"


md5_path = "./md5.text"


#session_config
session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }