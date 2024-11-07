from fastapi import Request,FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.output_parsers import JsonOutputParser
import json,random
from ai import get_llm_response,get_report_data_response
from report_chatbot import save_to_vector_db,create_user_data

parser=JsonOutputParser()
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

irrelavant_question_error=[
    "I apologize, but I'm unable to respond to questions that aren't related to medical topics.",
    "Sorry, but I can only answer questions that pertain to medical matters.",
    "I regret to inform you that I can't answer questions outside the medical field.",
    "Unfortunately, I'm not able to address inquiries that are unrelated to medicine.",
    "I'm sorry, but my expertise is limited to medical-related questions only.",
    "Regrettably, I can't provide answers to questions that don't involve medical issues.",
    "I appreciate your understanding, but I can only engage with medical inquiries.",
    "Sorry, I'm unable to help with questions that are not connected to medical topics.",
    "I'm afraid I can't assist with anything that isn't related to medical matters.",
    "Unfortunately, I can only provide information on medical-related questions."
]

@app.post("/query/")
async def answer_query(request:Request):
    data=await request.json()
    question=data['queryResult']["queryText"]
    response=get_llm_response(question)
    try:
        data=parser.parse(response)
    except:
        return JSONResponse({
            'fulfillmentText':"Ooops!! I think i am tired. Please try again.."
        })

    if data['status']=="true":
        return JSONResponse(
            {
            'fulfillmentText':data['ans'],
            },
            status_code=200
            )
    elif data["status"]=="absent":
        return JSONResponse(
            {
            'fulfillmentText':"Oops!! I dont have this information in my knoledge base. Please try something else..",
            },
            status_code=200
            )
    else:
        return JSONResponse(
            {
            'fulfillmentText':irrelavant_question_error[random.randint(0,9)],
            },
            status_code=200
            )

@app.get("/test")
async def test():
    return {"data":"ok"}


@app.post("/add_user_data/")
async def add_user_report_data(request:Request):
    data=await request.json()
    report_id,user_id,email=data["report_id"],data["user_id"],data["email"]
    status=save_to_vector_db(report_id,user_id,email)
    if status:
        return JSONResponse({"mssg":"Saved to Vector DB"},status_code=201)
    return JSONResponse({"mssg":"Error saving to Vector DB"},status_code=400)


@app.post("/create_agent/")
async def create_agent(request:Request):
    data=await request.json()
    user_id,email=data["user_id"],data["email"]
    status,key=create_user_data(str(user_id),email)
    if status:
        return JSONResponse({"mssg":"Agent Created","key":key},status_code=201)
    return JSONResponse({"mssg":"Error creating agent"},status_code=400)

@app.post("/chat/")
async def chat(request:Request):
    data=await request.json()
    key,question=data["key"],data["question"]
    resp=get_report_data_response(key,question)
    try:
        data=parser.parse(resp)
    except:
        try:
            data=eval(resp)
        except:
            JSONResponse({"data":"Error retreiving data.."},status_code=200)
    if data["status"]=="true":
        return JSONResponse({"data":data["ans"]},status_code=200)
    return JSONResponse({"data":"It seems the information relevant to your question doesnt exist..."},status_code=400)

