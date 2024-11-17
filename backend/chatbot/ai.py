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
import numpy as np
import pickle
import spacy
nlp=spacy.load("en_core_web_lg")
chatbot_model=pickle.load(open("chatbot.pkl","rb"))

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

response_map={
    "welcome": [
    "Hey, I'm MedBuddy! I can help analyze your reports and answer questions like... For example, can you show me my hemoglobin trend?",
    "Hello! I'm MedBuddy, your electronic report assistant. How can I assist you with your health reports today?",
    "Heyy! i am medbuddy your electronic report assistant which answers questions by analyzing your reports. Eg: Whats my hemoglobin trend.."
    "Hello! I’m MedBuddy. I can provide insights on your medical reports. Would you like to know about your hemoglobin trends?",
    "Hi! I’m MedBuddy, your report assistant. Want to see your hemoglobin levels over the last few months?",
    "I’m MedBuddy! Need to analyze your medical reports? I can show you trends in hemoglobin, blood pressure, and more.",
    "Hey! It’s MedBuddy. I analyze your reports for you. Want to see your hemoglobin levels and how they’ve changed?",
    "Hi, MedBuddy here! I can help you track trends in your reports. Do you want to see how they’ve changed?",
    "Hi, I'm MedBuddy! Need help with your medical reports? I can show you the hemoglobin trends, blood pressure, and more.",
    "Hey! I’m MedBuddy. I analyze your health reports. Want me to summarize your hemoglobin trend or any other data?"
],
    "thank_you": [
      "You're welcome!",
      "Glad I could help!",
      "No problem at all!",
      "It was my pleasure!",
      "You're very welcome!",
      "Anytime, happy to help!",
      "Glad I could assist you!",
      "You're welcome, feel free to ask if you need anything!",
      "It was nothing, happy to help!",
      "You're welcome, take care!"
    ]
,
    "bye": [
      "Goodbye! Have a great day!",
      "See you later!",
      "Take care!",
      "Goodbye! Feel free to come back anytime!",
      "Bye! It was nice talking to you!",
      "Have a wonderful day ahead!",
      "Take care and see you soon!",
      "Goodbye! Don't hesitate to ask if you need anything else!",
      "See you soon, take care!",
      "Bye! Stay safe and take care!"
    ]
 ,
    "about": [
    "Hello! I'm MedBuddy, your Electronic Report Assistant, created by VNRR.",
    "Hi, I'm MedBuddy, your personalized Electronic Report Assistant, brought to you by VNRR.",
    "Greetings! I'm MedBuddy, your Electronic Report Assistant, designed by VNRR.",
    "Hey there! I'm MedBuddy, your trusty Electronic Report Assistant developed by VNRR.",
    "Hi! MedBuddy here, your Electronic Report Assistant, created by the team at VNRR.",
    "Hello, I'm MedBuddy, your Electronic Report Assistant, developed by VNRR to assist you.",
    "Greetings from MedBuddy, your Electronic Report Assistant, made by VNRR.",
    "Hey! I’m MedBuddy, your Electronic Report Assistant designed and created by VNRR.",
    "Hello, this is MedBuddy, your Electronic Report Assistant, built by VNRR.",
    "Hi, MedBuddy at your service! Your Electronic Report Assistant, designed by VNRR."
]
  }

intent_map={0: 'welcome', 1: 'thank_you', 2: 'bye', 3: 'help', 4: 'about'}

def predicted_intent(question):
    vector=[nlp(question).vector]
    predicted=chatbot_model.predict(vector)
    if intent_map[predicted[0]]!="help":return {"status":True,"intent":intent_map[predicted[0]]}
    return {'status':False}

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