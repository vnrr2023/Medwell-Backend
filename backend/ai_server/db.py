import psycopg2
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from secret import Secret

uri = f"mongodb+srv://{Secret.MONGO_USER}:{Secret.MONGO_PASSWORD}@cluster0.lxnui.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
DB=client["user_report_data_db"]
COLLECTION = DB["report_data"]
host=Secret.HOST
port='5432'
dbname=Secret.DB_NAME
user=Secret.USER
password=Secret.PASSWORD

def connect_db():
    connection = psycopg2.connect(
        host=host,
        port='5432',
        dbname=dbname,
        user=user,
        password=password
    )
    return connection,connection.cursor()


def executeQuery(query,values):
    connection,cursor=connect_db()
    cursor.execute(query,values)
    connection.commit()
    connection.close()
    cursor.close()

