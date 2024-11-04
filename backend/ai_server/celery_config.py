from celery import Celery
from celery.result import AsyncResult
import psycopg2
import uuid
import json
import urllib3
import pdfplumber
import io
import requests
from ai import get_model_response
from prompt_templates import prompts,data_template
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

from langchain_core.output_parsers import JsonOutputParser
parser=JsonOutputParser()

class Config:
    CELERY_BROKER_URL:str="redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND:str="redis://127.0.0.1:6379/0"


settings=Config()
celery_app=Celery(__name__,broker=settings.CELERY_BROKER_URL,backend=settings.CELERY_RESULT_BACKEND)




def connect_db():

    connection = psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='medwell_db' ,
        user='myuser' ,
        password='root' 
    )
    return connection,connection.cursor()


def send_status_to_mail(user_id,file,status):
    resp=requests.post("http://127.0.0.1:8000/patient/send_status_of_task_to_mail/",json={"user_id":user_id,"pdf_file":file.split("/")[-1],"status":status})
    

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


def save_health_and_diet_data(user_id):
    print('came to health summary')
    df=pd.read_sql_query(sql=to_sql_text('''
    select date_of_report,report_type,report_data from patient_report r join patient_reportdetail d on r.id=d.report_id 
    where user_id={user_id}
    order by r.submitted_at desc
    limit 5;
    '''.format(user_id=user_id)),con=conn)
    df["report_data"]=df.report_data.apply(generate_report_text)
    entire_data_text=""
    for index,data in df.iterrows():
        text=f'''
        report date:{data.date_of_report} report type : {data.report_type}
        report data :
        {data.report_data}
        \n
        '''
        entire_data_text+=text
    for _ in range(5):
        try:
            resp=get_model_response(prompts["health_summary_prompt"],entire_data_text)
            resp=parser.parse(resp)
            break
        except Exception as e:
            print(e)
            pass
    health_query='''
    update patient_patientprofile
    set health_summary=%s,diet_plan=%s
    where user_id=%s;
    '''
    health_values=(resp["summary"],resp["plans"],user_id)
    connection,cursor=connect_db()
    cursor.execute(health_query,health_values)
    connection.commit()
    connection.close()
    cursor.close()


@celery_app.task
def process_pdf(file,report_id,user_id):
    try:
        http = urllib3.PoolManager()
        temp = io.BytesIO()
        temp.write(http.request("GET", file).data)
        text = ''
        pdf=pdfplumber.open(temp)
        for pdf_page in pdf.pages[:2]:
            text += pdf_page.extract_text()+"\n"

        print("read pdf")

        type_of_report=eval(get_model_response(prompts['type_prompt'],text=text))['type']
        for page in pdf.pages[2:7]:
            text+=page.extract_text()+"\n"
        print(f"got report type=={type_of_report}\n")
        if type_of_report=="other":
            for i in range(5):
                try:
                    data=eval(
                        get_model_response(prompts['other_prompt'],text)
                    )
                    break
                except:
                    print("error")
                    if i==4:
                        send_status_to_mail(user_id,file,"FAILED")
                        return
                    else:pass
                    
            report_query='''
            update patient_report
            set doctor_name= %s,date_of_report=%s,date_of_collection=%s,
            report_type=%s,summary=%s,processed=%s
            where id=%s;
            '''
            report_values = (data['doctor_name'], data["date_of_report"], data['date_of_collection'],type_of_report,data['summary'],True,report_id)  
            connection,cursor=connect_db()
            cursor.execute(report_query,report_values)
            connection.commit()
            connection.close()
            cursor.close()
            print("stored to db")
            send_status_to_mail(user_id,file,"SUCCESS")
            
        else:
            for i in range(5):
                try:
                    data=eval(
                        get_model_response(prompts['blood_prompt'],text)
                    )
                    break
                except:
                    print("error")
                    if i==4:
                        send_status_to_mail(user_id,file,"FAILED")
                        return
                    else:pass
                    
            sett={"doctor_name","date_of_report","date_of_collection","summary"}
            for i in data:
                if i not in sett:
                    data_template[i]['value']=data[i] if data[i] else -1
            report_query='''
            update patient_report
            set doctor_name= %s,date_of_report=%s,date_of_collection=%s,
            report_type=%s,summary=%s,processed=%s
            where id=%s;
            '''
            report_values = (data['doctor_name'], data["date_of_report"], data['date_of_collection'],type_of_report,data['summary'],True,report_id)  
            connection,cursor=connect_db()
            cursor.execute(report_query,report_values)
            connection.commit()
            report_detail_query='''
            insert into patient_reportdetail
                ( id,
                report_id,
                hemoglobin,
                rbc_count,
                wbc_count,
                platelet_count,
                pcv,
                bilirubin,
                proteins,
                calcium,
                blood_urea,
                sr_cholestrol,
                report_data
                )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s);
            '''
            report_detail_values=(
                str(uuid.uuid4()),
                report_id,
                str(data['hemoglobin']) if data['hemoglobin'] is not None else str(-1),
                str(data['rbc_count']) if data['rbc_count'] is not None else str(-1),
                str(data['wbc_count']) if data['wbc_count'] is not None else str(-1),
                str(data['platelet_count']) if data['platelet_count'] is not None else str(-1),
                str(data['pcv']) if data['pcv'] is not None else str(-1),
                str(data['bilirubin_total']) if data['bilirubin_total'] is not None else str(-1),
                str(data['proteins']) if data['proteins'] is not None else str(-1),
                str(data['calcium']) if data['calcium'] is not None else str(-1),
                str(data['blood_urea']) if data['blood_urea'] is not None else str(-1),
                str(data['sr_cholesterol']) if data['sr_cholesterol'] is not None else str(-1),
                json.dumps(data_template)
                )
            connection,cursor=connect_db()
            cursor.execute(report_detail_query,report_detail_values)
            connection.commit()   
            cursor.close()
            connection.close()
            print("stored to db")
        send_status_to_mail(user_id,file,"SUCCESS")
        save_health_and_diet_data(user_id)
        print("done")
    except Exception as e:
        print(e)
        send_status_to_mail(user_id,file,"FAILED")


     
def get_task_status(task_id):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        response = {
            "state": task_result.state,
            "status": "Pending..."
        }
    elif task_result.state == 'STARTED':
        response = {
            "state": task_result.state,
            "status": "In progress..."
        }
    elif task_result.state == 'SUCCESS':
        response = {
            "state": task_result.state,
            "result": task_result.result
        }
    elif task_result.state == 'FAILURE':
        response = {
            "state": task_result.state,
            "status": str(task_result.info)  # Exception info
        }
    else:
        response = {
            "state": task_result.state,
            "status": "Unknown state"
        }
    return response