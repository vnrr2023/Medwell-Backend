import chromadb
import pandas as pd,psycopg2
from sqlalchemy import create_engine,text as to_sql_text
import redis
client = redis.StrictRedis(host='localhost', port=6379, db=0)

db_username = 'myuser'
db_password = 'root'
db_host = 'localhost'
db_port = '5432'
db_name = 'medwell_db'

connection_string = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)
conn=engine.connect()
db = chromadb.PersistentClient(path="user_report_data")


REPORT_QUERY='''
SELECT date_of_collection, report_type, summary, report_data 
FROM patient_report p 
JOIN patient_reportdetail r ON p.id = r.report_id 
WHERE p.id = :report_id;
'''

def generate_report_text(report_data):
    report_text = ""
    for test, details in report_data.items():
        min_val = details['min']
        max_val = details['max']
        unit = details['unit']
        value = details['value'] 
        if value==-1:continue
        
        value_text = f"{value} {unit}" if value != -1 else "Not available"
        
        report_text += f"{test.capitalize()}: Normal range {min_val}-{max_val} {unit}, Current value: {value_text}\n"
    
    return report_text

def add_to_collection(collection,data,id):
    collection.add(
        documents=[data],ids=[id]
    )



def save_to_vector_db(report_id,user_id,email:str):
    # try:
    df = pd.read_sql_query(
        sql=to_sql_text(REPORT_QUERY), 
        con=conn, 
        params={'report_id': report_id}
    )
    df["report_data"]=df.report_data.apply(generate_report_text)
    print("got data and processed it")
    text=f'''
    Date of report: {df.iloc[0]["date_of_collection"]}
    Report Type: {df.iloc[0]["report_type"]}
    Summary of report: {df.iloc[0]["summary"]}
    Report data : {df.iloc[0]["report_data"]}
    '''
    print(text)
    email=email.split("@")[0]
    collection=db.get_or_create_collection(email+user_id)
    count=collection.count()
    if count<5:
        add_to_collection(collection,text,str(count))
    else:
        to_delete=collection.get(limit=1)["ids"][0]
        collection.delete(ids=[to_delete])
        add_to_collection(collection,text,str(int(to_delete)+5))
    print("saved to db")
    return True
    # except:
    #     return False

def create_user_data(user_id:str,email:str):
    email=email.split("@")[0]
    collection=db.get_or_create_collection(email+user_id)
    user_data="\n".join(collection.get()["documents"])
    key=f"report_chatbot_{email+user_id}"
    client.setex(key,900,user_data)
    return True,key


    



