'''
用于构建rag的Chain
'''
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.documents import Document
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history


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
                ("system","并且我提供了历史对话记录,记录如下"),
                MessagesPlaceholder("history"),
                ("user","请回答用户提问{input}")
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

        def format_for_retriever(value) -> str:
            return value["input"]

        def format_for_template(value) -> dict:
            #{input, context, history}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["history"] = value["input"]["history"]
            new_value["context"] = value["context"]
            return new_value


        chain = (
            {"input" : RunnablePassthrough(),
             "context" : RunnableLambda(format_for_retriever) | retriview | format_docment }
            | RunnableLambda(format_for_template)
            | self.prompt_template
            | print_prompt
            | self.chat_model
            | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",  # 用户输入再模板中的占位符
            history_messages_key="history",  # 表示用户输入再模板中的占位符
        )

        return conversation_chain


if __name__ == '__main__':
    #配置session id
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }
    res = RagService().chain.invoke({"input":"针织毛衣如何保养？"}, session_config)
    print(res)