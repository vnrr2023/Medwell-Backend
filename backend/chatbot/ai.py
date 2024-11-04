from langchain_groq import ChatGroq
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-70b-versatile",api_key=os.environ.get("GROQ_API_KEY_")
)

template='''
You are tasked with answering questions based on the provided medical context, which includes information about home remedies, symptoms, risk factors, and prevention methods for a specific disease. Please return the answer in JSON format with the following two keys:

ans: A brief answer to the question, around 40 to 50 words, starting with context related to the question.
status: This should be "true" if the answer is present in the context;if you dont find an ans in the context then it should be "absent";otherwise if the question is not revelant to medical then it  should be "false."
Ensure your response is concise and friendly, without any preamble or extra text.

<context>{context} <context>
Question: {input}
'''

embeddings=HuggingFaceEmbeddings()
persist_directory = "chatbot_db"
collection_name="remedies_chatbot_v2"
vector_store=Chroma(persist_directory=persist_directory,collection_name=collection_name, embedding_function=embeddings)
##RAG config
retriever = vector_store.as_retriever()
prompt=ChatPromptTemplate.from_template(template)
document_chain=create_stuff_documents_chain(llm,prompt)
retrieval_chain=create_retrieval_chain(retriever,document_chain)
   
def get_llm_response(question):
    response=retrieval_chain.invoke({"input":question})['answer']
    return response
    