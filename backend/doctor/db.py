import psycopg2
import pandas as pd
from sqlalchemy import create_engine,text as to_sql_text


db_username = 'myuser'
db_password = 'root'
db_host = 'localhost'
db_port = '5432'
db_name = 'medwell_db'

connection_string = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)
conn=engine.connect()

def connect_db():
    connection = psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='medwell_db' ,
        user='myuser' ,
        password='root' 
    )
    return connection,connection.cursor()

queries={
    'get_patients_with access':'''
    select patient_id,concat(p.first_name,p.last_name) as name,requested_at::timestamp::text
    from doctor_requestaccess d join authentication_customuser p
    on p.id=d.patient_id
    where doctor_id={user_id};
    '''
}


def get_patients(user_id):
    df=pd.read_sql_query(sql=to_sql_text(queries["get_patients_with access"].format(user_id=user_id)),con=conn)
    return df.to_dict("records")