import streamlit as st
from rag import RagService
import config_data as config


st.title("智能客服")
st.divider()

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role" : "assisant","content":"你好, 有什么可以帮助你"}
    ]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

#在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:
    #在页面输出用户的提问
    st.chat_message("user").write(prompt)

    #此处仅保存
    st.session_state["message"].append({"role" : "user", "content" : prompt})
    with st.spinner("AI思考中"):
        #获取rag输出
        res = st.session_state["rag"].chain.invoke({"input":prompt},config.session_config)
        #页面输出rag输出
        st.chat_message("assistant").write(res)
        #保留历史对话
        st.session_state["message"].append({"role": "assisant", "content": res})