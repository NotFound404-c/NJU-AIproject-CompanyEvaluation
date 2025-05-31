import streamlit as st
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
from pymilvus import MilvusClient
import asyncio
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import TextNode
import time
from pathlib import Path
from typing import List, Dict
import os
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.core.schema import TextNode
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import PromptTemplate
from transformers import AutoModelForCausalLM, AutoTokenizer
from llama_index.core.llms import ChatMessage
from llama_index.llms.huggingface import HuggingFaceLLM
import torch
import pandas as pd 
import json
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from pymilvus import model

# Streamlit 界面
st.set_page_config(page_title="Company-Evaluation", page_icon="🦜🔗")
st.title("Company-Evaluation")

# 初始化组件
@st.cache_resource
def init_query_engine():
    def create_vector_store():
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return MilvusVectorStore(
            uri="/root/milvus_filter_demo.db",
            collection_name="companyinfo",
            dim=512,
            overwrite=False,
        )

    vector_store = create_vector_store()
    # 创建 LlamaIndex 的 OpenAI LLM 实例
    embed_model = HuggingFaceEmbedding(
        model_name=r"/root/embed"
    )
    
    llm = OpenAI(
        model="gpt-4o",
        api_base='your-apibase',
        api_key='your-apikey'
    )

    # client = MilvusClient(uri="milvus_filter_demo.db")
    # 连接到本地 Milvus Lite（sqlite 文件）
    # 注意：uri 需要用 sqlite:/// 前缀，且路径要绝对路径
    #vector_store = MilvusVectorStore(
     #   uri="./milvus_filter_demo.db",
      #  collection_name="companyinfo",
       # dim=512,
        #overwrite=True,
   # )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store,embed_model=embed_model)

    # 创建查询引擎
    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=1
    )

    return query_engine


# 检查是否需要初始化模型
if 'query_engine' not in st.session_state:
    st.session_state['query_engine'] = init_query_engine()

def get_response_text(question):
    response = st.session_state['query_engine'].query(question)
    # 提取纯文本响应，移除任何额外节点信息
    return str(response).split("\n\n")[0]

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是AI小南，我可以评价很多A股上市公司!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是AI小南，我可以评价很多A股上市公司!"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

def generate_response(prompt_input):
    return get_response_text(prompt_input)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 获取纯文本响应
            response_text = generate_response(prompt)
            
            # 确保只显示纯文本内容
            if "Response object" in response_text:
                response_text = response_text.split("Response object.")[0]
            
            # 移除可能的额外节点信息
            if "source_nodes" in response_text:
                response_text = response_text.split("source_nodes")[0]
            
            # 显示响应
            st.write(response_text)
    
    # 存储纯文本响应
    message = {"role": "assistant", "content": response_text}
    st.session_state.messages.append(message)
# 运行命令：streamlit run /root/finc.py
