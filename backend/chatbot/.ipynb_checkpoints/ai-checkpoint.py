from langchain_groq import ChatGroq
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from groq import Groq
from dotenv import load_dotenv
from report_chatbot import client as redis_client
load_dotenv()


client=Groq(api_key=os.environ['GROQ_API_KEY_'])
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


def get_llm_response_for_report_chatbot(data,question):
    chat_completion = client.chat.completions.create(
    messages=[
         {"role":"system", "content":"""
         You are task is to answer questions based on the context only.Give me the reponse in json format only with two keys
         "ans": the answer in short about 60 to 70 words based on the context only. paraphrase the question while answering
         "status": value should be "true" if the answer is found in the context else will be "false".
         give me the response in json format with no preamble and no nested json and only text.
         Context: {context}
        """.format(context=data)
         },
         {
            "role": "user",
            "content": question,
        }
    ],
    model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content
    

def get_report_data_response(key,question):
    data=redis_client.get(key)
    if not data:
        pass
    return get_llm_response_for_report_chatbot(data,question)