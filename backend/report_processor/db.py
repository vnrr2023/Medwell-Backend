from dotenv import load_dotenv
load_dotenv()
import psycopg2
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from colorama import Fore
from urllib.parse import quote

Mongo_User=os.environ["MONGO_USER"]
Mongo_Password=os.environ["MONGO_PASS"]
uri = f"mongodb+srv://{Mongo_User}:{Mongo_Password}@cluster0.lxnui.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print(Fore.GREEN+"Pinged your deployment. You successfully connected to MongoDB!"+Fore.WHITE)
except Exception as e:
    print(e)
    
DB=client["user_report_data_db"]
COLLECTION = DB["report_data"]

host=os.environ["DB_HOST"]
port="6543"
dbname=os.environ["DB_NAME"]
user=os.environ["USER"]

connection_string = f"postgresql://postgres.ntfzmxgdxqjtijvxktra:{quote(os.environ['PASSWORD'])}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"

try:
    conn = psycopg2.connect(
    connection_string        
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")

def connect_db():
    connection = psycopg2.connect(
        connection_string
    )
    return connection,connection.cursor()


def executeQuery(query,values):
    connection,cursor=connect_db()
    cursor.execute(query,values)
    connection.commit()
    connection.close()
    cursor.close()

