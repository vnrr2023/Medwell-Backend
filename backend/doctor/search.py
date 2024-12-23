from elasticsearch import Elasticsearch
from colorama import Fore

client=Elasticsearch("http://127.0.0.1:9200")
if client.ping():
    print(Fore.GREEN+"Elastic Server is Up and Running")
else:
    print(Fore.RED+"Elastic Server not running")
print(Fore.WHITE)

############# CONFIG ###################
index_name="doctors_and_hospitals"
mappings={
    "mappings":{
        "properties":{
            "user_id":{"type":"keyword"},
            "name":{"type":"text"},
            "phone_number":{"type":"text"},
            "role":{"type":"text"},
            "speciality":{"type":"text"},
            "address":{"type":"text"},
            "location":{"type":"geo_point"}
            
        }
        
    }
}
######################################

def execute_elastic_query(query):
    data=[]
    response=client.search(index=index_name,body=query)
    for hit in response["hits"]["hits"]:
        data.append({"data":hit["_source"],"id":hit["_id"]})
    return data

def insert_to_elastic(data:dict):
    try:
        data["document"]["location"]["lat"]=float(data["document"]["location"]["lat"])
        data["document"]["location"]["lon"]=float(data["document"]["location"]["lon"])
        client.index(index=index_name,id=data["doc_id"],document=data["document"])
        return True
    except Exception as e:
        print(e)
        return False

def get_by_current_location(lat,lon,km,size=10):
    geo_query = {
    "size": size,
    "query": {
        "geo_distance": {
            "distance": f"{km}km",
            "location": {"lat": float(lat), "lon":float( lon)}
        }
    },
    "sort": [
        {
            "_geo_distance": {
                "location": {"lat": float(lat), "lon": float(lon)},
                "order": "asc",
                "unit": "km"
            }
        }
    ]
    }
    return execute_elastic_query(geo_query)

def get_by_location_and_speciality(lat,lon,km,speciality):
    query = {
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "speciality": {
                            "query": speciality,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            ],
            "filter": [
                {
                    "geo_distance": {
                        "distance": f"{km}km",
                        "location": {
                            "lat": float(lat),
                            "lon": float(lon)
                        }
                    }
                }
            ]
        }
    },
    "sort": [
        {
            "_geo_distance": {
                "location": {
                    "lat": float(lat),
                    "lon": float(lon)
                },
                "order": "asc",
                "unit": "km"
            }
        }
    ]
    }

    return execute_elastic_query(query)


def search_doc_and_hos(query):
    multi_query={
        "query": {
        "multi_match": {
            "query": query,
            "fields": ["name", "speciality","address"],
            "fuzziness":"AUTO"
        }
        }
    }
    return execute_elastic_query(multi_query)

    
