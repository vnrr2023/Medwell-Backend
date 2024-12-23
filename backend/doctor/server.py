from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import get_patients
from search import insert_to_elastic,get_by_current_location,get_by_location_and_speciality,search_doc_and_hos

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

@app.post("/add_address/")
async def add_address(request:Request):
    data=await request.json()
    if insert_to_elastic(data):
        return JSONResponse({"mssg":"Added address to elastic search successfully"},status_code=201)
    return JSONResponse({"mssg":"Not able to add address to elastic search"},status_code=406)

@app.post("/get_nearby_doctor/")
async def get_nearby_data(request:Request):
    data=await request.json()
    lat,lon,km,speciality=data["lat"],data["lon"],data.get("km",5),data.get("speciality",None)
    try:
        if speciality:
            return JSONResponse({"data":get_by_location_and_speciality(lat,lon,km,speciality)},status_code=200)
        return JSONResponse({"data":get_by_current_location(lat,lon,km)},status_code=200)
    except:
        return JSONResponse({"mssg":"Oops!! There might be some problem"},status_code=400)
    
@app.post("/search_doctors_and_hospitals/")
async def search_data(request:Request):
    data=await request.json()
    query=data["query"]
    try:
        return JSONResponse({"data":search_doc_and_hos(query)},status_code=200)
    except:
        return JSONResponse({"mssg":"Oops!! There might be some problem"},status_code=400)



    
