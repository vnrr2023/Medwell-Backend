import psycopg2
import pandas as pd
from sqlalchemy import create_engine


db_username = 'myuser'
db_password = 'root'
db_host = 'localhost'
db_port = '5432'
db_name = 'medwell_db'

connection_string = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)

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
    'health_check':'''
    select submitted_at,hemoglobin,rbc_count,wbc_count,platelet_count,pcv,bilirubin,proteins, calcium,blood_urea,sr_cholestrol
    from patient_report pr join patient_reportdetail rd
    on pr.id=rd.report_id
    where user_id={user_id};
    ''',
    'average_query':'''
    SELECT 
        AVG(CASE WHEN hemoglobin <> '-1' THEN CAST(hemoglobin AS FLOAT) END) AS avg_hemoglobin,
        AVG(CASE WHEN rbc_count <> '-1' THEN CAST(rbc_count AS FLOAT) END) AS avg_rbc_count,
        AVG(CASE WHEN wbc_count <> '-1' THEN CAST(wbc_count AS FLOAT) END) AS avg_wbc_count,
        AVG(CASE WHEN platelet_count <> '-1' THEN CAST(platelet_count AS FLOAT) END) AS avg_platelet_count,
        AVG(CASE WHEN pcv <> '-1' THEN CAST(pcv AS FLOAT) END) AS avg_pcv,
        AVG(CASE WHEN bilirubin <> '-1' THEN CAST(bilirubin AS FLOAT) END) AS avg_bilirubin,
        AVG(CASE WHEN proteins <> '-1' THEN CAST(proteins AS FLOAT) END) AS avg_proteins,
        AVG(CASE WHEN calcium <> '-1' THEN CAST(calcium AS FLOAT) END) AS avg_calcium,
        AVG(CASE WHEN blood_urea <> '-1' THEN CAST(blood_urea AS FLOAT) END) AS avg_blood_urea,
        AVG(CASE WHEN sr_cholestrol <> '-1' THEN CAST(sr_cholestrol AS FLOAT) END) AS avg_sr_cholestrol
    FROM 
        patient_report pr 
    JOIN 
        patient_reportdetail rd ON pr.id = rd.report_id
    WHERE 
        user_id = {user_id};
    ''',
    'report_count_query': '''select count(*) as num_reports from patient_report where user_id={user_id}; ''',
    "overall_expense":'''SELECT SUM(CAST(amount AS DECIMAL)) as total_expense from patient_expense where user_id={user_id} ;''',
    "recent_expenses":'''select expense_type,amount,date(date) from patient_expense where user_id={user_id} order by date desc limit 10;'''
}


def provide_health_check_data(user_id):
    count=pd.read_sql_query(queries['report_count_query'].format(user_id=user_id),engine)['num_reports'][0]
    if count<=3:
        return {"status":False,"count":count}
    df=pd.read_sql_query(queries['health_check'].format(user_id=user_id),engine)
    df.replace("-1",None,inplace=True)
    df['submitted_at'] = df['submitted_at'].astype(str)
    data=df.to_dict("list")
    avg_data=pd.read_sql_query(queries['average_query'].format(user_id=user_id),engine).to_dict("records")[0]
    return {"status":True,"data":data,"avg_data":avg_data}


def provide_expense_data(user_id):
    conn,cursor=connect_db()
    cursor.execute(queries["overall_expense"].format(user_id=user_id))
    overall_expense=str(cursor.fetchone()[0])
    df=pd.read_sql_query(queries["recent_expenses"].format(user_id=user_id),engine)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    data=df.to_dict("records")
    return {"overall_expense":overall_expense,"expenses":data}
    