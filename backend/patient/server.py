from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import provide_health_check_data,provide_expense_data,provide_expense_dashboard,dashboard_data

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_health_check/")
async def get_health_check(request:Request):
    data= await request.json()
    health_check_data=provide_health_check_data(data["user_id"])
    print(health_check_data)
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

@app.post("/get_expense_data/")
async def get_expense_data(request:Request):
    data= await request.json()
    user_id=data["user_id"]
    resp=provide_expense_data(user_id)
    return JSONResponse(resp,status_code=200)

@app.post("/expenses_dashboard/")
async def get_expense_dashboard(request:Request):
    data= await request.json()
    user_id=data["user_id"]
    resp=provide_expense_dashboard(user_id)
    return JSONResponse(resp)


@app.post("/get_dashboard_data/")
async def get_dashboard_data(request:Request):
    data=await request.json()
    user_id=data["user_id"]
    data=dashboard_data(user_id)
    print(data)
    return JSONResponse(data,status_code=200)



@app.get("/test/")
async def test():
    return {"test":"Server Up"}
