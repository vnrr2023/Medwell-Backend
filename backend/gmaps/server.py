from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import googlemaps
import os

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


gmaps = googlemaps.Client(key=os.environ.get("GMAPS_API_KEY"))


@app.get("/")
async def checkStatus():
    return {
        "Message":"Server is Up and Running.."
    }

@app.get("/get-encoded-polyline/{sourceLat}/{sourceLon}/{destinationLat}/{destinationLon}")
async def getEncodedPolyline(sourceLat:float,sourceLon:float,destinationLat:float,destinationLon:float):
    origin=f"{sourceLat},{sourceLon}"
    destination=f"{destinationLat},{destinationLon}"

    directions = gmaps.directions(origin, destination)

    if directions and "overview_polyline" in directions[0]:
        polyline=directions[0]["overview_polyline"]["points"]
        return JSONResponse({"polyline":polyline},status_code=200)
    else:
        return JSONResponse({"polyline":"Not Dound"},status_code=400)
    
@app.get("/geocode-address/{address}")
async def getEncodedPolyline(address:str):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        resp={"formatted_address":geocode_result[0]["formatted_address"],"location":geocode_result[0]["geometry"]["location"]}
        return JSONResponse(resp,status_code=200)
    else:
        return JSONResponse({},status_code=400)
    


