'''
用于构建rag的Chain
'''
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser

def print_prompt(prompts):
    print("==" * 10)
    print(prompts.to_string())
    print("==" * 10)
    return prompts


class RagService(object):
    def __init__(self):

        self.vecotr_service = VectorStoreService(
            embedding= DashScopeEmbeddings(model = config.embedding_model),
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的参考资料为主，简洁和专业的回答用户问题，参考资料：{context}"),
                ("Human","请回答用户提问{input}")
            ]
        )

        self.chat_model = ChatTongyi(model = config.chat_model_name)

        self.chain = self.__get_chain__()

    def __get_chain__(self):
        '''获取执行链'''
        retriview = self.vecotr_service.get_retriever()

        def format_docment(docs: list[Document]):
            if not docs:
                return "无参考文献"
            format_str = ""
            for doc in docs:
                format_str += f"文档片段{doc.page_content}\n文档元数据{doc.metadata}\n\n"
            return format_str

        chain = (
            {"input" : RunnablePassthrough(),
             "context" : retriview | format_docment }
            | self.prompt_template
            | print_prompt
            | self.chat_model
            | StrOutputParser()
        )

        return chain


if __name__ == '__main__':
    res = RagService().chain.invoke("我体重180斤，尺码推荐")
    print(res)