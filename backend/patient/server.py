from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from colorama import Fore

from db import provide_health_check_data,provide_expense_data,provide_expense_dashboard,dashboard_data

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_health_check/{user_id}")
async def get_health_check(user_id:int):
    health_check_data=provide_health_check_data(user_id)
    if health_check_data["status"]==False:
        return JSONResponse(
            {"count":str(health_check_data['count']),'status':False},status_code=200
            )
  
    return JSONResponse(
        {
            'avg_data':health_check_data["avg_data"],
            'data':health_check_data['data'],
            'status':True
        },status_code=200
    )

@app.get("/get_expense_data/{user_id}")
async def get_expense_data(user_id:int):
    resp=provide_expense_data(user_id)
    return JSONResponse(resp,status_code=200)

@app.get("/expenses_dashboard/{user_id}")
async def get_expense_dashboard(user_id:int):
    resp=provide_expense_dashboard(user_id)
    return JSONResponse(resp)


@app.get("/get_dashboard_data/{user_id}")
async def get_dashboard_data(user_id:int):
    data=dashboard_data(user_id)
    return JSONResponse(data,status_code=200)



@app.get("/test")
async def test():
    return {"test":"Server Up"}


if __name__=="__main__":
    print(Fore.GREEN+"Server Running on Port = 5000"+Fore.WHITE)
    uvicorn.run("server:app",host="localhost",port=5000,reload=True)