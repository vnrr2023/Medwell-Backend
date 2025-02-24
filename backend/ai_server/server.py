from dotenv import load_dotenv
load_dotenv()
from fastapi import Request,FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from celery_config import process_pdf,get_task_status
from ai import get_model_response
from prompt_templates import EXPENSE_PROMPT


app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  API's
@app.get("/test")
async def test():
    return {'data':"Server is running"}


@app.post("/process_report")
async def process_report(request:Request):
    data=await request.json()
    task=process_pdf.delay(data['file'],data['report_id'],data['user_id'],data["email"],data["first_name"])
    return JSONResponse({"task_id":task.id},status_code=200)

    
@app.post("/process_expense_query")
async def process_expense_query(request:Request):
    data=await request.json()
    query=data["data"]
    for _ in range(5):
        try:
            resp=eval(get_model_response(EXPENSE_PROMPT,query))
            break
        except:pass
    if resp["status"]=="true":return JSONResponse({"status":True,"amount":resp["amount"],"expenditure":resp["expenditure"]})
    return JSONResponse({"status":False,"mssg":"Enter relevant expense"})

    

@app.get("/get_task_status/{task_id}")
async def get_status(task_id:str):
    return JSONResponse(get_task_status(task_id))


@app.post("/generate_mail_body")
async def getMailBody(request:Request):
    data= await request.json()
    prompt='''
You are a Mail Body Generator. Your task is to create a concise and engaging email body (strictly 4 to 5 sentences) based on the given subject and prompt. The email will be sent by a doctor to patients for marketing services, customer retention, and relationship building. The prompt may be null at times.

If any other question is asked beyond your task, respond with "I can't do this.".

Provide only the email body without any preamble or extra text.
    '''
    subject=data.get("subject")
    prompt=data.get("prompt","No prompt given so use subject")
    text=f"<Subject>{subject}</Subject>\n<doctorPrompt>{prompt}</doctorPrompt>"
    body=get_model_response(prompt,text)
    return JSONResponse({"mail_body":body})


if __name__=="__main__":
    uvicorn.run("server:app",host="localhost",port=8888,reload=True)

