from fastapi import Request,FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from celery_config import process_pdf,get_task_status
from celery.result import AsyncResult
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# logic for bg task
'''
read file using pdf plumber and urllib
give to groq
extarct get the json
put to db
ask django to send mail
set task id to completed
'''



#  API's
@app.get("/test")
async def test():
    '''
    Used for testing purpose to check if server is up and running
    '''
    return {'data':"Server is running"}


@app.post("/process_report/")
async def process_report(request:Request):
    data=await request.json()
    task=process_pdf.delay(data['file'],data['report_id'],data['user_id'])
    return JSONResponse({"task_id":task.id},status_code=200)
    
    


@app.get("/get_task_status/")
async def get_status(request:Request):
    data=request.query_params.get("task_id")
    return JSONResponse(get_task_status(data))
