from celery import Celery
from celery.result import AsyncResult
import psycopg2
import uuid
import json
import urllib3
import pdfplumber
import io
from groq import Groq
import os
from dotenv import load_dotenv
import requests

load_dotenv()
client=Groq(api_key=os.environ['GROQ'])

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

prompts={
    "type_prompt":'''
you are a medical report classifier.
you will be given a medical report in text and you have to classify it in blood_report or other.
if there are values of hemoglobin,rbc count wbc count,platelet count bilirubin etc then it is a blood report else other.
Give me the result in Json format with key as "type" with no preamble and no nested json.
''',
    'blood_prompt':'''
you are a medical report parser.
Give me the output in json format strictly with no preamble.
If you dont get any value assign it None
Extract the following fields
    name of the doctor with key as "doctor_name"
    date of report with key as "date_of_report" with dd/mm/yy format with no leading zeroes
    date of collection with key as "date_of_collection" with dd/mm/yy format with no leading zeroes
    hemoglobin with key as "hemoglobin"
    rbc count with key as "rbc_count"
    wbc count with key as "wbc_count"
    pcv with key as "pcv"
    iron with key as "iron"
    sodium with key "sodium"
    pottasium with key "potassium"
    phosphorus with key "phosphorus"
    chloride with key "chloride"
    platelet count with key as "platelet_count"
    bilirubin total with key as "bilirubin_total"
    bilirubin direct with key as "bilirubin_direct"
    bilirubin indirect with key as "bilirubin_indirect"
    proteins with key as "proteins"
    calcium with key as "calcium"
    albumin with key as "albumin"
    Globulin with key as "globulin"
    Blood Urea with the key "blood_urea"
    Blood Urea Nitrogen with the key "blood_urea_nitrogen"
    S. Creatinine with the key "s_creatinine"
    S. Uric Acid with the key "s_uric_acid"
    S. Phosphorus with the key "s_phosphorus"
    Neutrophils with the key "neutrophils".
    Lymphocytes with the key "lymphocytes".
    Sr. Cholesterol with the key "sr_cholesterol".
    HDL Cholesterol with the key "hdl_cholesterol".
    fasting sugar with key "fasting_sugar"
    after lunch sugar with key "after_lunch_sugar"
Summarize the medical report, focusing on any values that are abnormal or outside the normal range with key "summary"
Strictly give me in proper json format with no nested json and  with no preamble.
''' ,
    "other_prompt":'''
you are a medical report summarizer and entity extractor.
Give me the following details in json format
    name of the doctor with key as "doctor_name"
    date of report with key as "date_of_report" with dd/mm/yy format with no leading zeroes
    date of collection with key as "date_of_collections" with dd/mm/yy format with no leading zeroes
    summary the report with key as "summary".
Only give me json with no preamble
'''
}

data_template={
  "hemoglobin": {
    "value": -1,
    "min": 12.1,
    "max": 15.5,
    "unit": "g/dL"
  },
  "rbc_count": {
    "value": -1,
    "min": 4.2,
    "max": 5.4,
    "unit": "million cells/μL"
  },
  "wbc_count": {
    "value": -1,
    "min": 4.5,
    "max": 11.0,
    "unit": "thousand cells/μL"
  },
  "pcv": {
    "value": -1,
    "min": 36,
    "max": 50,
    "unit": "%"
  },
  "iron": {
    "value": -1,
    "min": 60,
    "max": 170,
    "unit": "μg/dL"
  },
  "sodium": {
    "value": -1,
    "min": 135,
    "max": 145,
    "unit": "mmol/L"
  },
  "potassium": {
    "value": -1,
    "min": 3.5,
    "max": 5.0,
    "unit": "mmol/L"
  },
  "phosphorus": {
    "value": -1,
    "min": 2.5,
    "max": 4.5,
    "unit": "mg/dL"
  },
  "chloride": {
    "value": -1,
    "min": 98,
    "max": 107,
    "unit": "mmol/L"
  },
  "platelet_count": {
    "value": -1,
    "min": 150000,
    "max": 450000,
    "unit": "cells/μL"
  },
  "bilirubin_total": {
    "value": -1,
    "min": 0.1,
    "max": 1.2,
    "unit": "mg/dL"
  },
  "bilirubin_direct": {
    "value": -1,
    "min": 0.0,
    "max": 0.3,
    "unit": "mg/dL"
  },
  "bilirubin_indirect": {
    "value": -1,
    "min": 0.1,
    "max": 0.8,
    "unit": "mg/dL"
  },
  "proteins": {
    "value": -1,
    "min": 6.0,
    "max": 8.0,
    "unit": "g/dL"
  },
  "calcium": {
    "value": -1,
    "min": 8.5,
    "max": 10.2,
    "unit": "mg/dL"
  },
  "albumin": {
    "value": -1,
    "min": 3.5,
    "max": 5.0,
    "unit": "g/dL"
  },
  "globulin": {
    "value": -1,
    "min": 2.0,
    "max": 4.0,
    "unit": "g/dL"
  },
  "blood_urea": {
    "value": -1,
    "min": 7,
    "max": 20,
    "unit": "mg/dL"
  },
  "blood_urea_nitrogen": {
    "value": -1,
    "min": 7,
    "max": 20,
    "unit": "mg/dL"
  },
  "s_creatinine": {
    "value": -1,
    "min": 0.6,
    "max": 1.2,
    "unit": "mg/dL"
  },
  "s_uric_acid": {
    "value": -1,
    "min": 3.5,
    "max": 7.2,
    "unit": "mg/dL"
  },
  "s_phosphorus": {
    "value": -1,
    "min": 2.5,
    "max": 4.5,
    "unit": "mg/dL"
  },
  "neutrophils": {
    "value": -1,
    "min": 40,
    "max": 75,
    "unit": "%"
  },
  "lymphocytes": {
    "value": -1,
    "min": 20,
    "max": 45,
    "unit": "%"
  },
  "sr_cholesterol": {
    "value": -1,
    "min": 0,
    "max": 200,
    "unit": "mg/dL"
  },
  "hdl_cholesterol": {
    "value": -1,
    "min": 40,
    "max": 60,
    "unit": "mg/dL"
  },
  "fasting_sugar": {
    "value": -1,
    "min": 70,
    "max": 100,
    "unit": "mg/dL"
  },
  "after_lunch_sugar": {
    "value": -1,
    "min": 70,
    "max": 140,
    "unit": "mg/dL"
  }
}


def get_model_response(prompt,text):
    chat_completion=client.chat.completions.create(
        messages=[{'role':"system","content":prompt},{"role":"user","content":text}],
        model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content


def send_status_to_mail(user_id,file,status):
    resp=requests.post("http://127.0.0.1:8000/patient/send_status_of_task_to_mail/",json={"user_id":user_id,"pdf_file":file.split("/")[-1],"status":status})
    

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