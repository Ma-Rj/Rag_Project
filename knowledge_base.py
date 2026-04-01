'''
知识库
三个方法：检查md5， 保存md5，  计算md5
为了去重，防止上传相同的内容
'''
import hashlib
import os
import config_data as config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str : str) -> bool :
    '''False代码未处理，True代表已处理'''
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w').close()
        return False;

    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if md5_str in line:
                return True
        return False

def save_md5(md5_str : str):
    if check_md5(md5_str):
        "内容已存在"
        return ;
    with open(config.md5_path, 'a',encoding='utf-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(Str : str, encoding = 'utf-8') -> str:
    #将字符转换为bytes数组
    str_bytes = Str.encode(encoding=encoding)

    #创建md5对象
    # md5_obj = hashlib.md5()   #得到md5对象
    # md5_obj.update(str_bytes)   #更新内容（传入即将要转换的字节数组）
    # md5_hex = md5_obj.hexdigest()  #得到md5的十六进制字符串

    return hashlib.md5(str_bytes).hexdigest()

#字符串向量化并嵌入向量
class KnowledgeBaseService(object):
    def __init__(self):
        #如果文件夹不存在则创建，存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function= DashScopeEmbeddings(model = config.embedding_model),
            persist_directory=config.persist_directory    #数据库本地存储文件夹
        )   #向量存储的实例Chroma向量库对象

        #文本分割器
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,  #分割文本段最大长度
            chunk_overlap = config.chunk_overlap,  #自然段落分割最大重合
            separators = config.separators,
            length_function = len
        )  #文本分割器对象

    def upload_by_str(self,data,filename) -> str:
        '''将传入的字符串向量化，并存入到向量数据库中'''

        #先获取MD5
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[跳过] 内容已存在知识库中"

        if len(data) > config.max_split_char_number:
            knowledge_chunks : list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks : list[str] = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "operater": "小马"
        }

        self.chroma.add_texts(   #这段执行完成后就加入到向量库中去了
            #iterator  list \ tuple
            knowledge_chunks,
            metadatas = [metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)

        return "[成功],内容已成功上传到向量知识库中"

if __name__ == '__main__':
    pass
    # service = KnowledgeBaseService()
    #
    # res = service.upload_by_str("","testfile")
    #
    # print(res)