from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException,Request,Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from db import Patient,Doctor
from utils import validateToken,printWithColor

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def authenticateUser(request:Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")
    token = auth_header.split(" ")[1]
    user_id = validateToken(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Session expired..Login again")
    
    return user_id


@app.get("/patient/health-check")
async def getPatientHealthCheck(user_id: int = Depends(authenticateUser)):
    health_check_data=Patient.provide_health_check_data(user_id)
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

@app.get("/patient/expense")
async def getPatientExpense(user_id: int = Depends(authenticateUser)):
    resp=Patient.provide_expense_data(user_id)
    return JSONResponse(resp,status_code=200)

@app.get("/patient/expense-dashboard")
async def getPatientExpenseDashboard(user_id: int = Depends(authenticateUser)):
    resp=Patient.provide_expense_dashboard(user_id)
    return JSONResponse(resp)

@app.get("/patient/dashboard")
async def getPatientDashboard(user_id: int = Depends(authenticateUser)):
    data=Patient.dashboard_data(user_id)
    return JSONResponse(data,status_code=200)


@app.get("/doctor/dashboard")
async def getDoctorDashboard():
    data=Doctor.getDoctorDashboardData(1)
    return JSONResponse(data,status_code=200)

@app.get("/doctor/analytics")
async def getDoctorAnalytics():
    data=Doctor.getDoctorAnalytics(1)
    return JSONResponse(data,status_code=200)


@app.get("/doctor/patient-health-check/{user_id}")
async def getPatientHealthCheckForDoctor(user_id: int):
    health_check_data=Patient.provide_health_check_data(user_id)
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

    


@app.get("/test")
async def test():
    return {"test":"Server Up"}


if __name__=="__main__":
    printWithColor("Server running on port 5000")
    uvicorn.run("server:app",host="127.0.0.1",port=5000)