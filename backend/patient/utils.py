from redis import StrictRedis
import os,json
from colorama import Fore
import jwt

def printWithColor(text):
    print(Fore.GREEN+text+Fore.WHITE)


SECRET_KEY = os.environ["SECRET_KEY"]

redis_client=StrictRedis(host=os.environ["REDIS_HOST"],port=int(os.environ["REDIS_PORT"]),password=os.environ["REDIS_PASS"])
if redis_client.ping():
    printWithColor("Connected To Redis")
else:
    print(Fore.RED+"Oops Connection with Redis Failed"+Fore.WHITE)


def setData(key,data):
    value=json.dumps(data)
    redis_client.setex(key,200,value)
    return True

def getData(key):
    data=redis_client.get(key)
    if data==None:return {"status":False}
    print("CACHE  HIT")
    return {"status":True,"data":json.loads(data)}


def validateToken(token):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return str(payload["user_id"])
    except:
        return None
    

