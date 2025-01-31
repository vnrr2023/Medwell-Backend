import googlemaps
from django.conf import settings
gmaps_client=googlemaps.Client(settings.GOOGLE_MAPS_SECRET)


def geocodeAddress(address):
    geocode_result = gmaps_client.geocode(address)
    if geocode_result:
        return {"formatted_address":geocode_result[0]["formatted_address"],"location":geocode_result[0]["geometry"]["location"],"status":True}
    return {"status":False}
