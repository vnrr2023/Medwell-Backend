from fastapi import Request,FastAPI,BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
from tasks import process_pdf

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


######### For Background Processing #####
tasks = {} 

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
async def process_report(request:Request, background_tasks: BackgroundTasks):
    data=await request.json()
    task_id = str(uuid.uuid4())  # Generate a unique task ID
    tasks[task_id] = "RUNNING"  # Store task status
    print("came to background tasks\n\n")
    background_tasks.add_task(process_pdf,tasks,task_id,data['file'],data['report_id'],data['user_id'])
    print("sending the task id ====")
    return JSONResponse({"task_id":task_id},status_code=200)
    
    

@app.get("/check_task_status/")
async def check(task_id:str):
    status=tasks.get(task_id,"DIED")
    if status=="SUCCESS" or status=="FAILED":
        del tasks[task_id]
    return JSONResponse(
        {'status':status},status_code=200
    )
