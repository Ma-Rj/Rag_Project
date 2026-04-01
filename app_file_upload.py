'''
代码基于streamlit完成web网页上传服务
功能为：离线上传文档，并且可以获取到文件内容
'''

import streamlit  as st

st.title("知识库更新服务")

#文件上传
uploader_file = st.file_uploader(
    "请上传txt文件",
    type=['txt'],
    accept_multiple_files=False,  # 仅接收一个文件上传
)

if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024  #转为KB单位

    st.subheader(f"文件名为{file_name}")

    st.write(f"文件的格式为:{file_type},文件大小为:{file_size:.2f}KB")

    #获取文件内容  get_value -> byte ->decode(utf-8)
    text = uploader_file.getvalue().decode("utf-8")
    st.write(text)