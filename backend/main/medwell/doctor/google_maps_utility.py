import googlemaps
import requests

GMAPS_SERVICE_URL="https://gmapsmedwell.vercel.app"

def geocodeAddress(address):
    resp=requests.get(GMAPS_SERVICE_URL+f"/geocode-address/{address}")
    if resp.status_code==200:
        return resp.json()
    else:
        return None