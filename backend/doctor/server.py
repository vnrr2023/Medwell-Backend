from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import get_patients

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_active_patients/{user_id}")
async def get_active_patients(user_id):
    data=get_patients(user_id)
    return JSONResponse(data,status_code=200)